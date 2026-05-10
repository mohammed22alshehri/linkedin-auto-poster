import os
import requests
import random
import json
from groq import Groq  # التغيير هنا
from topics import topics_list

# Secrets
ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY') # أضف مفتاح Groq في الـ Secrets
API_VERSION = '202601'

def get_random_topic():
    used_topics = []
    if os.path.exists('used_topics.json'):
        with open('used_topics.json', 'r') as f:
            try: used_topics = json.load(f)
            except: used_topics = []
    available_topics = [t for t in topics_list if t not in used_topics]
    return random.choice(available_topics) if available_topics else None

def generate_with_ai(topic):
    # استبدلنا Gemini بـ Groq لحل مشكلة الـ Quota
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = f" Act as me — Mohammed Al-Shehri, a Software & AI Engineer and Computer Science student specialized in web development, databases, AI integration, and enterprise systems. Write a professional LinkedIn post in English about: {topic} Writing Style: - Sound natural, smart, and professional. - Write like a real engineer sharing experience or insight. - Keep the tone confident and modern. - Avoid fake motivation and corporate buzzwords. - Make it feel personal and authentic. - Keep it concise and impactful (120–180 words). Structure: 1. Start with a strong hook. 2. Explain the topic clearly in a practical engineering way. 3. Use short paragraphs or bullet points for readability. 4. End with a real takeaway, insight, or question. Extra Instructions: - Mention technologies when relevant (AI, Python, Oracle, SQL, APIs, Web Development, Cloud, etc.). - Make the post suitable for LinkedIn engagement. - Add professional hashtags at the end. Also: - Suggest 2 high-quality professional images related to the topic. - Provide direct image URLs from the internet. - Images should match engineering, AI, software, cloud, or development themes.
    
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
                # التأكد أن البيانات المحملة هي قائمة وليست قاموس
                if isinstance(data, list):
                    used_topics = data
                else:
                    used_topics = [] # إعادة ضبطها إذا كانت بتنسيق خاطئ
            except: 
                used_topics = []
                
    used_topics.append(topic) # الآن نضمن أنها قائمة
    with open('used_topics.json', 'w', encoding='utf-8') as f:
        json.dump(used_topics, f, indent=4)

def post_to_linkedin():
    topic = get_random_topic()
    if not topic: return

    print(f"✍️ Generating content for: {topic}")
    content = generate_with_ai(topic) # مناداة الدالة الجديدة

    if not content: return

    # باقي كود LinkedIn كما هو بدون أي تغيير
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
    if ACCESS_TOKEN and GROQ_API_KEY:
        post_to_linkedin()
