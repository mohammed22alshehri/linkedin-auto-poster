import os
import requests
import json
import random
from groq import Groq
# استيراد قائمة المواضيع من ملفك الخاص
from topics import topics_list 

# إعداد المتغيرات
LINKEDIN_TOKEN = os.getenv("LINKEDIN_TOKEN")
LINKEDIN_PERSON_ID = os.getenv("LINKEDIN_PERSON_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_new_topic():
    """اختيار موضوع لم يسبق استخدامه"""
    used_topics = []
    if os.path.exists("used_topics.json"):
        with open("used_topics.json", "r", encoding="utf-8") as f:
            try:
                used_topics = json.load(f)
            except: used_topics = []

    # تصفية المواضيع غير المستخدمة
    available_topics = [t for t in topics_list if t not in used_topics]
    
    if not available_topics:
        # إذا انتهت المواضيع، يمكننا تصفير السجل والبدء من جديد
        available_topics = topics_list
        used_topics = []

    selected = random.choice(available_topics)
    return selected, used_topics

def generate_content(topic):
    """صياغة الموضوع المختار باستخدام Groq باللغة الإنجليزية"""
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = (
        f"Based on this topic: '{topic}', write a high-quality, professional LinkedIn post. "
        "The post must be in English, include a brief technical insight, bullet points for clarity, "
        "and appropriate hashtags. Keep it engaging for a technical audience."
    )
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a senior AI & Systems Engineer crafting professional LinkedIn content."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def post_to_linkedin(content, topic, used_topics):
    """نشر المحتوى وتحديث سجل المواضيع المستخدمة"""
    if not LINKEDIN_PERSON_ID.startswith("urn:li:person:"):
        author = f"urn:li:person:{LINKEDIN_PERSON_ID}"
    else:
        author = LINKEDIN_PERSON_ID

    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_TOKEN}",
        "LinkedIn-Version": "202401",
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
        print(f"Successfully posted about: {topic}")
        # تحديث قائمة المواضيع المستخدمة
        used_topics.append(topic)
        with open("used_topics.json", "w", encoding="utf-8") as f:
            json.dump(used_topics, f, ensure_ascii=False, indent=4)
    else:
        print(f"Failed. Error: {response.text}")

if __name__ == "__main__":
    topic, used_history = get_new_topic()
    post_content = generate_content(topic)
    post_to_linkedin(post_content, topic, used_history)
