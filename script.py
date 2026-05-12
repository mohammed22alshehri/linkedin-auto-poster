import os
import requests
import random
import json
from groq import Groq
from topics import topics_dict

ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
API_VERSION = '202601'

def get_random_topic():
    used_topics = []
    last_category = None
    
    if os.path.exists('used_topics.json'):
        with open('used_topics.json', 'r') as f:
            try:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    used_topics = data
                    last_topic = data[-1]
                    # تحديد فئة آخر منشور
                    for cat, topics in topics_dict.items():
                        if last_topic in topics:
                            last_category = cat
                            break
            except:
                used_topics = []

    # استبعاد فئة آخر منشور لضمان التنوع
    available_categories = [c for c in topics_dict.keys() if c != last_category]
    random.shuffle(available_categories)
    
    for category in available_categories:
        possible_topics = [t for t in topics_dict[category] if t not in used_topics]
        if possible_topics:
            return random.choice(possible_topics)
            
    return None

def generate_with_ai(topic):
    client = Groq(api_key=GROQ_API_KEY)
    
    # استخدام """ لحل مشكلة الـ SyntaxError
    prompt = f"""Act as me — Mohammed Al-Shehri, a Software & AI Engineer and Computer Science student specialized in web development, databases, AI integration, and enterprise systems. 
Write a professional LinkedIn post in English about: {topic}

Writing Style:
- Sound natural, smart, and professional.
- Write like a real engineer sharing experience or insight.
- Keep the tone confident and modern.
- Avoid fake motivation and corporate buzzwords.
- Keep it concise and impactful (90–120 words).

Structure:
1. Start with a Very strong hook.
2. Explain the topic clearly in a practical engineering way.
3. Use short paragraphs or bullet points for readability.
4. End with a real takeaway or question.

Extra Instructions:
- Mention relevant techs (AI, Python, SQL, APIs, etc.).
- Add professional hashtags at the end, two lines below the text."""
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

def update_history(topic):
    used_topics = []
    if os.path.exists('used_topics.json'):
        with open('used_topics.json', 'r') as f:
            try:
                data = json.load(f)
                used_topics = data if isinstance(data, list) else []
            except:
                used_topics = []
    
    used_topics.append(topic)
    with open('used_topics.json', 'w', encoding='utf-8') as f:
        json.dump(used_topics, f, indent=4)

def post_to_linkedin():
    topic = get_random_topic()
    if not topic: return
    
    content = generate_with_ai(topic)
    if not content: return

    try:
        user_info = requests.get(
            "https://api.linkedin.com/v2/userinfo", 
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        ).json()
        person_id = user_info.get('sub')
        
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
            update_history(topic)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if ACCESS_TOKEN and GROQ_API_KEY:
        post_to_linkedin()
