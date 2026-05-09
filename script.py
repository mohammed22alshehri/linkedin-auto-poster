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
    api_key = os.getenv('GROQ_API_KEY')
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {
                "role": "user",
                "content": f"Write a professional LinkedIn post about: {topic}\nKeep it 120-160 words. Add a question and 3-5 hashtags. Make it engaging."
            }
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            raise Exception(f"Status {response.status_code}")
    except Exception as e:
        raise Exception(f"Groq: {str(e)}")

def post_to_linkedin(text):
    token = os.getenv('LINKEDIN_TOKEN')
    person_id = os.getenv('LINKEDIN_PERSON_ID')
    
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {token}",
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
    
    return requests.post(url, headers=headers, json=payload, timeout=10)

print("Starting LinkedIn Auto Post...")
try:
    history = load_history()
    topic = pick_topic(history)
    print(f"Topic: {topic}")
    
    print("Generating with Groq AI...")
    content = generate_post(topic)
    print(f"Generated: {len(content)} chars")
    
    print("Publishing to LinkedIn...")
    result = post_to_linkedin(content)
    
    if result.status_code in [200, 201]:
        history[topic] = datetime.now().isoformat()
        save_history(history)
        print("✅ SUCCESS - Posted to LinkedIn!")
    else:
        print(f"❌ LinkedIn Error {result.status_code}")
        print(result.text[:300])
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
