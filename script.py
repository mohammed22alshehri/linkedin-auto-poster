import requests
import os
import json
import random
from google import genai
from datetime import datetime, timedelta
from topics import TOPICS

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

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
        used_date = datetime.fromisoformat(date_str)
        if used_date > cutoff:
            recently_used.add(topic)
    available = [t for t in TOPICS if t not in recently_used]
    if not available:
        print("All topics used, restarting the cycle...")
        available = TOPICS
    return random.choice(available)

def generate_post(topic):
    prompt = f"""You are a senior software engineer and tech expert with years of hands-on experience.
Write a professional LinkedIn post in English about: {topic}

Requirements:
- Start with a bold statement or question that grabs attention immediately
- Provide real practical value that engineers can apply directly
- Use concrete examples or numbers where possible
- Length: 120 to 160 words
- End with a question that encourages comments
- Add 3 to 5 relevant hashtags on the last line
- Write it as if you are sharing from your own personal experience"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text

def post_to_linkedin(text):
    access_token = os.getenv('LINKEDIN_TOKEN')
    person_id = os.getenv('LINKEDIN_PERSON_ID')
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    payload = {
        "author": f"urn:li:person:{person_id}",
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
    return requests.post(url, headers=headers, json=payload)

print(f"Runtime: {datetime.now()}")
history = load_history()
topic = pick_topic(history)
print(f"Selected topic: {topic}")
post_content = generate_post(topic)
print(f"Generated post:\n{post_content}\n")
result = post_to_linkedin(post_content)

if result.status_code == 201:
    history[topic] = datetime.now().isoformat()
    save_history(history)
    print("Posted successfully!")
else:
    print(f"Post failed. Status code: {result.status_code}")
    print(result.text)
