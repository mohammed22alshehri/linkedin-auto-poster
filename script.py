import os
import requests
import json
import random
from groq import Groq
# تأكد أن ملف topics.py يحتوي على قائمة باسم topics_list
try:
    from topics import topics_list 
except ImportError:
    topics_list = ["Professional Growth in AI", "The Future of Systems Engineering"]

# إعداد المتغيرات
LINKEDIN_TOKEN = os.getenv("LINKEDIN_TOKEN")
LINKEDIN_PERSON_ID = os.getenv("LINKEDIN_PERSON_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_new_topic():
    """اختيار موضوع لم يسبق استخدامه"""
    used_topics = []
    if os.path.exists("used_topics.json"):
        try:
            with open("used_topics.json", "r", encoding="utf-8") as f:
                used_topics = json.load(f)
        except: used_topics = []

    available_topics = [t for t in topics_list if t not in used_topics]
    
    if not available_topics:
        available_topics = topics_list
        used_topics = []

    selected = random.choice(available_topics)
    return selected, used_topics

def generate_content(topic):
    """صياغة المنشور بالإنجليزية باستخدام Groq"""
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = (
        f"Write a professional LinkedIn post about: '{topic}'. "
        "The post must be in English. Include a hook, technical value, and hashtags. "
        "Make it sound like it's written by an experienced AI Engineer."
    )
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a senior AI and Systems Engineer."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def post_to_linkedin(content, topic, used_topics):
    """نشر المحتوى مع تحديث إصدار الـ API"""
    if not LINKEDIN_PERSON_ID.startswith("urn:li:person:"):
        author = f"urn:li:person:{LINKEDIN_PERSON_ID}"
    else:
        author = LINKEDIN_PERSON_ID

    url = "https://api.linkedin.com/rest/posts"
    
    # تم تحديث الإصدار هنا إلى 202406 لحل مشكلة الـ 426
    headers = {
        "Authorization": f"Bearer {LINKEDIN_TOKEN}",
        "LinkedIn-Version": "202406", 
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
        print(f"Successfully posted: {topic}")
        used_topics.append(topic)
        with open("used_topics.json", "w", encoding="utf-8") as f:
            json.dump(used_topics, f, ensure_ascii=False, indent=4)
    else:
        print(f"Failed. Status: {response.status_code}")
        print(f"Error Details: {response.text}")
        # إذا استمر الخطأ 426، جرب إصدار "202502" في السطر 67

if __name__ == "__main__":
    try:
        topic, used_history = get_new_topic()
        post_content = generate_content(topic)
        post_to_linkedin(post_content, topic, used_history)
    except Exception as e:
        print(f"Error: {e}")
