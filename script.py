import os
import requests
import json
from groq import Groq


# استدعاء المتغيرات من البيئة
LINKEDIN_TOKEN = os.getenv('LINKEDIN_TOKEN')
LINKEDIN_PERSON_ID = os.getenv('LINKEDIN_PERSON_ID')

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
                "text": "هذا المنشور تم بواسطة نظام الأتمتة الذكي الخاص بي 🚀" # أو المتغير الخاص بالنص المولد
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

response = requests.post(url, headers=headers, json=post_data)

if response.status_code == 201:
    print("✅ Post successful!")
else:
    print(f"❌ Failed to post: {response.status_code}")
    print(f"Response: {response.text}")
