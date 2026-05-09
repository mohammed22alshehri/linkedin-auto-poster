import os
import requests
import json
from groq import Groq

# إعداد المتغيرات من البيئة
LINKEDIN_TOKEN = os.getenv("LINKEDIN_TOKEN")
LINKEDIN_PERSON_ID = os.getenv("LINKEDIN_PERSON_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_content():
    """توليد محتوى باستخدام Groq (نموذج Llama 3)"""
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = "اكتب منشوراً احترافياً وقصيراً لمنصة LinkedIn حول أهمية الذكاء الاصطناعي في تحسين كفاءة العمل التقني، مع استخدام الوسوم المناسبة."
    
    # استخدام نموذج llama3-8b وهو سريع جداً ومجاني ضمن حدود معينة
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "أنت خبير في كتابة محتوى LinkedIn باللغة العربية."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def post_to_linkedin(content):
    """نشر المحتوى على LinkedIn"""
    
    # التأكد من تنسيق المعرف
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
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    print("جاري النشر على LinkedIn...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print("تم النشر بنجاح!")
        # تحديث ملف السجل لضمان وجود تغيير يرفعه الـ Action
        with open("used_topics.json", "a") as f:
            f.write(f"\n{content[:30]}...") 
    else:
        print(f"فشل النشر. كود الخطأ: {response.status_code}")
        print(f"الاستجابة: {response.text}")

if __name__ == "__main__":
    try:
        post_content = generate_content()
        post_to_linkedin(post_content)
    except Exception as e:
        print(f"حدث خطأ: {e}")
