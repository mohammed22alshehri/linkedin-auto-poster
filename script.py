import os
import requests
import random
import json
from google import genai 
from topics import topics_list

# Configuration & Secrets
ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
API_VERSION = '202601'

def get_random_topic():
    used_topics = []
    if os.path.exists('used_topics.json'):
        with open('used_topics.json', 'r') as f:
            try:
                used_topics = json.load(f)
            except:
                used_topics = []
    available_topics = [t for t in topics_list if t not in used_topics]
    return random.choice(available_topics) if available_topics else None

def generate_with_gemini(topic):
    # استخدام الموديل المستقر تقنياً في 2026
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"Write a professional LinkedIn post in English about: {topic}. Use bullet points and engineering hooks."
    
    # التغيير الجوهري هنا: gemini-2.0-flash هو الاسم المعتمد في الـ API
    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=prompt
    )
    return response.text

def update_history(topic):
    used_topics = []
    if os.path.exists('used_topics.json'):
        with open('used_topics.json', 'r') as f:
            try: used_topics = json.load(f)
            except: used_topics = []
    used_topics.append(topic)
    with open('used_topics.json', 'w', encoding='utf-8') as f:
        json.dump(used_topics, f, indent=4)

def post_to_linkedin():
    topic = get_random_topic()
    if not topic:
        print("🎉 All topics exhausted!")
        return

    print(f"✍️ Generating content for: {topic}")
    content = generate_with_gemini(topic)

    try:
        user_info = requests.get(
            "https://api.linkedin.com/v2/userinfo", 
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        ).json()
        person_id = user_info.get('sub')
    except Exception as e:
        print(f"❌ UserInfo Error: {e}")
        return

    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "LinkedIn-Version": API_VERSION,
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    payload = {
        "author": f"urn:li:person:{person_id}",
        "commentary": content,
        "visibility": "PUBLIC",
        "distribution": {"feedDistribution": "MAIN_FEED"},
        "lifecycleState": "PUBLISHED"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code in [200, 201]:
        print(f"🚀 Success: {topic}")
        update_history(topic)
    else:
        print(f"❌ Failed: {response.text}")

if __name__ == "__main__":
    if ACCESS_TOKEN and GEMINI_API_KEY:
        post_to_linkedin()
