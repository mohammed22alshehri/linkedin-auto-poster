import os
import requests
from google import genai
import json

# إعداد المتغيرات من البيئة
LINKEDIN_TOKEN = os.getenv("LINKEDIN_TOKEN")
LINKEDIN_PERSON_ID = os.getenv("LINKEDIN_PERSON_ID") # تأكد أنه يبدأ بـ urn:li:person:
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_content():
    """توليد محتوى المنشور باستخدام Gemini"""
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = "اكتب منشوراً احترافياً وقصيراً لمنصة LinkedIn حول أهمية الذكاء الاصطناعي في تحسين كفاءة العمل التقني، مع استخدام الوسوم المناسبة."
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text

def post_to_linkedin(content):
    """نشر المحتوى على LinkedIn مع معالجة إصدار الـ API"""
    
    # التأكد من تنسيق الـ Person ID كـ URN
    if not LINKEDIN_PERSON_ID.startswith("urn:li:person:"):
        author = f"urn:li:person:{LINKEDIN_PERSON_ID}"
    else:
        author = LINKEDIN_PERSON_ID

    # تحديث الإصدار إلى 202604 لتلافي خطأ 426
    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_TOKEN}",
        "LinkedIn-Version": "202604", 
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

    print(f"Attempting to post with version 202604...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print("Successfully posted to LinkedIn!")
    else:
        print(f"Failed to post. Status Code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    try:
        print("Generating content...")
        post_content = generate_content()
        print("Posting to LinkedIn...")
        post_to_linkedin(post_content)
    except Exception as e:
        print(f"An error occurred: {e}")
