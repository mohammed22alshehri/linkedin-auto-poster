import os
import requests
import json
from groq import Groq

# الإعدادات من GitHub Secrets
ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')
PERSON_ID = os.getenv('LINKEDIN_PERSON_ID')
# تأكد أن PERSON_ID في السيكرتس هو الرقم فقط بدون urn:li:person:

def post_to_linkedin():
    url = "https://api.linkedin.com/v2/ugcPosts"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    post_data = {
        "author": f"urn:li:person:{PERSON_ID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": "تم النشر تلقائياً بواسطة Bot بايثون! 🚀"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=post_data)
    
    if response.status_code in [201, 200]:
        print("✅ Success!")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    post_to_linkedin()
