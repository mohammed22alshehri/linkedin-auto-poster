import requests
import os
import json
import random
from datetime import datetime, timedelta
from topics import TOPICS

HISTORY_FILE = "used_topics.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def pick_topic(history):
    cutoff = datetime.now() - timedelta(days=60)
    recently_used = set()
    for topic, date_str in history.items():
        try:
            used_date = datetime.fromisoformat(date_str)
            if used_date > cutoff:
                recently_used.add(topic)
        except:
            pass
    available = [t for t in TOPICS if t not in recently_used]
    if not available:
        print("All topics used, restarting cycle...")
        available = TOPICS
    return random.choice(available)

def generate_post(topic):
    api_key = os.getenv('GEMINI_API_KEY')
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
    
    prompt = (
        "You are a senior software engineer and tech expert with years of hands-on experience.\n"
        "Write a professional LinkedIn post in English about: " + topic + "\n\n"
        "Requirements:\n"
        "- Start with a bold statement or question that grabs attention immediately\n"
        "- Provide real practical value that engineers can apply directly\n"
        "- Use concrete examples or numbers where possible\n"
        "- Length: 120 to 160 words\n"
        "- End with a question that encourages comments\n"
        "- Add 3 to 5 relevant hashtags on the last line\n"
        "- Write it as if you are sharing from your own personal experience"
    )
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"Gemini API error: {response.status_code} - {response.text}")

def post_to_linkedin(text):
    access_token = os.getenv('LINKEDIN_TOKEN')
    person_id = os.getenv('LINKEDIN_PERSON_ID')
    
    # تصحيح صيغة الـ ID
    if "urn:li:person:" in person_id:
        author = person_id.replace("urn:li:person:", "urn:li:member:")
    elif person_id.startswith("urn:li:member:"):
        author = person_id
    else:
        author = "urn:li:member:" + person_id
    
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    payload = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response

# Main execution
print("=" * 50)
print("LinkedIn Auto Post - Starting at " + str(datetime.now()))
print("=" * 50)

try:
    history = load_history()
    topic = pick_topic(history)
    print("\n📌 Selected Topic: " + topic)
    
    print("\n⏳ Generating post with Gemini...")
    post_content = generate_post(topic)
    print("\n✍️ Generated Post:")
    print("-" * 50)
    print(post_content)
    print("-" * 50)
    
    print("\n📤 Publishing to LinkedIn...")
    result = post_to_linkedin(post_content)
    
    if result.status_code == 201:
        history[topic] = datetime.now().isoformat()
        save_history(history)
        print("\n✅ SUCCESS! Post published to LinkedIn")
        print("Status: " + str(result.status_code))
    elif result.status_code == 200:
        history[topic] = datetime.now().isoformat()
        save_history(history)
        print("\n✅ SUCCESS! Post published to LinkedIn")
        print("Status: " + str(result.status_code))
    else:
        print("\n❌ FAILED! Could not publish to LinkedIn")
        print("Status Code: " + str(result.status_code))
        print("Response: " + result.text)

except Exception as e:
    print("\n❌ ERROR: " + str(e))
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
