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
    return random.choice(available if available else TOPICS)

def generate_post(topic):
    api_key = os.getenv('GEMINI_API_KEY')
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"
    
    prompt = (
        "You are a senior software engineer and tech expert.\n"
        "Write a professional LinkedIn post in English about: " + topic + "\n"
        "Requirements:\n"
        "- Start with a bold statement\n"
        "- 120-160 words\n"
        "- End with a question\n"
        "- Add 3-5 hashtags"
    )
    
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"Gemini error: {response.status_code}")

def post_to_linkedin(text):
    token = os.getenv('LINKEDIN_TOKEN')
    
    # استخدام Simple Share Endpoint (أسهل وأكثر موثوقية)
    url = "https://api.linkedin.com/v2/shares"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    payload = {
        "content": {
            "contentEntities": [
                {
                    "entity": "urn:li:digitalmediaAsset:test"
                }
            ],
            "title": "Professional Insights",
            "shareCommentary": text
        },
        "distribution": {
            "linkedInDistributionTarget": {}
        },
        "owner": "urn:li:person:" + os.getenv('LINKEDIN_PERSON_ID'),
        "shareMediaCategory": "NONE",
        "text": {
            "text": text
        }
    }
    
    return requests.post(url, headers=headers, json=payload)

print("Starting LinkedIn Auto Post...")
try:
    history = load_history()
    topic = pick_topic(history)
    print(f"Topic: {topic}")
    
    post_content = generate_post(topic)
    print(f"Post generated successfully")
    
    result = post_to_linkedin(post_content)
    
    if result.status_code in [200, 201]:
        history[topic] = datetime.now().isoformat()
        save_history(history)
        print("SUCCESS!")
    else:
        print(f"Status: {result.status_code}")
        print(f"Response: {result.text}")
        
except Exception as e:
    print(f"Error: {str(e)}")
