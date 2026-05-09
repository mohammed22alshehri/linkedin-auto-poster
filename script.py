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
    api_key = os.getenv('TOGETHER_API_KEY')
    url = "https://api.together.xyz/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta-llama/Llama-2-7b-chat-hf",
        "messages": [
            {
                "role": "user",
                "content": f"Write a professional LinkedIn post about: {topic}\n\nRequirements:\n- 120-160 words\n- End with a question\n- Add 3-5 hashtags\n- Make it engaging and professional\n- In English only"
            }
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=20)
    
    if response.status_code == 200:
        data = response.json()
        return data['choices'][0]['message']['content']
    else:
        raise Exception(f"API Error {response.status_code}: {response.text[:200]}")

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

print("Starting...")
try:
    history = load_history()
    topic = pick_topic(history)
    print(f"Topic: {topic}")
    
    print("Generating post with AI...")
    content = generate_post(topic)
    print("Generated ✓")
    
    print("Publishing to LinkedIn...")
    result = post_to_linkedin(content)
    
    if result.status_code in [200, 201]:
        history[topic] = datetime.now().isoformat()
        save_history(history)
        print("✅ SUCCESS")
    else:
        print(f"❌ Error {result.status_code}")
        
except Exception as e:
    print(f"❌ {str(e)}")
