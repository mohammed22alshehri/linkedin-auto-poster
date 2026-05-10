import os
import requests

# الإعدادات من GitHub Secrets
ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')
# تأكد أن PERSON_ID هو فقط الرقم/الحروف (مثل: abc123XYZ)
PERSON_ID = os.getenv('LINKEDIN_PERSON_ID')

def post_to_linkedin():
    # رابط الـ API الحديث للمنشورات
    url = "https://api.linkedin.com/rest/posts"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202401",  # تحديد إصدار الـ API
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    post_data = {
        "author": f"urn:li:person:{PERSON_ID}",
        "commentary": "تم النشر تلقائياً بواسطة Bot بايثون! 🚀",
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    response = requests.post(url, headers=headers, json=post_data)
    
    if response.status_code in [201, 200]:
        print("✅ Success! Post created.")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    post_to_linkedin()
