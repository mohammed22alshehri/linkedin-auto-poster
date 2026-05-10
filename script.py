import os
import requests
import random
import json
from google import genai  # المكتبة الجديدة
from topics import topics_list

# Configuration & Secrets
ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
API_VERSION = '202601'

def get_random_topic():
    """Selects a topic that hasn't been used yet."""
    used_topics = []
    if os.path.exists('used_topics.json'):
        with open('used_topics.json', 'r') as f:
            try:
                used_topics = json.load(f)
            except:
                used_topics = []
    
    available_topics = [t for t in topics_list if t not in used_topics]
    
    if not available_topics:
        return None
    
    return random.choice(available_topics)

def generate_with_gemini(topic):
    """Generates professional English LinkedIn content using the new Gemini SDK."""
    # التعديل الجوهري هنا: استخدام google-genai بدل المكتبة القديمة
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    You are an expert Systems Engineer and AI Specialist.
    Write a high-authority LinkedIn post in English about the following topic: {topic}.
    
    Guidelines:
    1. Start with a strong 'hook' to grab attention.
    2. Use bullet points for key takeaways to ensure scannability.
    3. Include a practical 'pro-tip' or engineering insight.
    4. Maintain a professional, insightful, and non-salesy tone.
    5. End with relevant hashtags like #SoftwareEngineering #AI #CloudComputing #SystemDesign.
    6. Ensure the post is engaging and formatted for the LinkedIn feed.
    """
    
    # استخدام الموديل المستقر في 2026
    response = client.models.generate_content(
        model='gemini-3-flash', 
        contents=prompt
    )
    return response.text

def update_history(topic):
    """Saves the used topic to prevent duplicates in the future."""
    used_topics = []
    if os.path.exists('used_topics.json'):
        with open('used_topics.json', 'r') as f:
            try:
                used_topics = json.load(f)
            except:
                used_topics = []
    
    used_topics.append(topic)
    with open('used_topics.json', 'w', encoding='utf-8') as f:
        json.dump(used_topics, f, indent=4)

def post_to_linkedin():
    # 1. Topic selection
    topic = get_random_topic()
    if not topic:
        print("🎉 Success: All topics in the list have been exhausted!")
        return

    print(f"✍️ Generating content for topic: {topic}")
    content = generate_with_gemini(topic)

    # 2. Fetching Member ID (URN) dynamically
    try:
        user_info_res = requests.get(
            "https://api.linkedin.com/v2/userinfo", 
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        person_id = user_info_res.json().get('sub')
    except Exception as e:
        print(f"❌ Error fetching user info: {e}")
        return

    if not person_id:
        print("❌ Error: Could not verify Person ID. Check token permissions.")
        return

    # 3. Executing the LinkedIn Post
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
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        print(f"🚀 Successfully posted to LinkedIn: {topic}")
        update_history(topic)
    else:
        print(f"❌ Failed to post. Status: {response.status_code}")
        print(f"📄 Response Error: {response.text}")

if __name__ == "__main__":
    if not ACCESS_TOKEN or not GEMINI_API_KEY:
        print("❌ Missing environment variables. Ensure LINKEDIN_TOKEN and GEMINI_API_KEY are set.")
    else:
        post_to_linkedin()
