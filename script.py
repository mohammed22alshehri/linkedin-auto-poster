import os
import requests
from groq import Groq # استبدال مكتبة جيميناي بـ جروك

# إعداد المتغيرات من البيئة
LINKEDIN_TOKEN = os.getenv("LINKEDIN_TOKEN")
LINKEDIN_PERSON_ID = os.getenv("LINKEDIN_PERSON_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY") # استخدام مفتاح جروك

def generate_content():
    """توليد محتوى باستخدام Groq (Llama 3)"""
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = "اكتب منشوراً احترافياً وقصيراً لمنصة LinkedIn حول أهمية الذكاء الاصطناعي في تحسين كفاءة العمل التقني، مع استخدام الوسوم المناسبة."
    
    completion = client.chat.completions.create(
        model="llama3-8b-8192", # موديل سريع وقوي جداً
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

def post_to_linkedin(content):
    # نستخدم نفس دالة النشر السابقة دون تغيير
    if not LINKEDIN_PERSON_ID.startswith("urn:li:person:"):
        author = f"urn:li:person:{LINKEDIN_PERSON_ID}"
    else:
        author = LINKEDIN_PERSON_ID

    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_TOKEN}",
        "LinkedIn-Version": "202401", # تأكد من أن هذا الإصدار يعمل معك
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
        print("Successfully posted to LinkedIn!")
    else:
        print(f"Failed. Status: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    content = generate_content()
    post_to_linkedin(content)
