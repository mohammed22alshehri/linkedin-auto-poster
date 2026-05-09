import os
import requests
import json
import random
from groq import Groq

# استيراد المواضيع
try:
    from topics import topics_list 
except ImportError:
    topics_list = ["AI Systems Integration", "Full-stack Engineering Trends"]

LINKEDIN_TOKEN = os.getenv("LINKEDIN_TOKEN")
LINKEDIN_PERSON_ID = os.getenv("LINKEDIN_PERSON_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_new_topic():
    used_topics = []
    if os.path.exists("used_topics.json"):
        try:
            with open("used_topics.json", "r", encoding="utf-8") as f:
                used_topics = json.load(f)
        except: used_topics = []
    available = [t for t in topics_list if t not in used_topics]
    if not available:
        available = topics_list
        used_topics = []
    selected = random.choice(available)
    return selected, used_topics

def generate_content(topic):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = (
        f"Write a professional LinkedIn post in English about: '{topic}'.\n"
        "Style: Expert AI Engineer. Structure: Catchy hook, 3 bullet points, CTA, and 3 hashtags."
    )
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a professional software architect."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def post_to_linkedin(content, topic, used_topics):
    author = f"urn:li:person:{LINKEDIN_PERSON_ID.replace('urn:li:person:', '')}"
    url = "https://api.linkedin.com/rest/posts"
    
    # ملاحظة: تأكد أن هذا التاريخ هو الأحدث في صفحة LinkedIn Developers لديك
    # تأكد أن هذا السطر وما بعده يبدأ بنفس الإزاحة داخل الدالة
        headers = {
        "Authorization": f"Bearer {LINKEDIN_TOKEN}",
        "LinkedIn-Version": "202502",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
        }

    payload = {
        "author": author,
        "commentary": content,
        "visibility": "PUBLIC",
        "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"Success! Posted: {topic}")
        used_topics.append(topic)
        with open("used_topics.json", "w", encoding="utf-8") as f:
            json.dump(used_topics, f, ensure_ascii=False, indent=4)
    else:
        print(f"Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    topic, history = get_new_topic()
    content = generate_content(topic)
    post_to_linkedin(content, topic, history)
