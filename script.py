import os
import requests
import json
from groq import Groq

# إعدادات البيئة
LINKEDIN_TOKEN = os.getenv("LINKEDIN_TOKEN").strip()
LINKEDIN_PERSON_ID = os.getenv("LINKEDIN_PERSON_ID").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_post():
    client = Groq(api_key=GROQ_API_KEY)
    # يمكنك تعديل البرومبت هنا ليناسب تخصصك في الـ AI والأنظمة
    prompt = "Write a short, professional LinkedIn post in Arabic about the importance of AI in web engineering. Include 3 hashtags."
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content

def post_to_linkedin(content):
    # استخدام Endpoint الإصدار الثاني والمضمون للنشر
    url = "https://api.linkedin.com/v2/ugcPosts"
    
    headers = {
        "Authorization": f"Bearer {LINKEDIN_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    post_data = {
        "author": f"urn:li:person:{LINKEDIN_PERSON_ID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    response = requests.post(url, headers=headers, json=post_data)
    
    if response.status_code in [200, 201]:
        print("🚀 Post published successfully!")
    else:
        print(f"❌ Failed to post: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    if not LINKEDIN_TOKEN or not LINKEDIN_PERSON_ID:
        print("❌ Missing LinkedIn Credentials!")
    else:
        print("🤖 Generating content...")
        post_content = generate_post()
        print("📤 Sending to LinkedIn...")
        post_to_linkedin(post_content)
