import requests
import os

print("Testing LinkedIn API Connection...")

token = os.getenv('LINKEDIN_TOKEN')
person_id = os.getenv('LINKEDIN_PERSON_ID')

print(f"Token: {token[:20]}...")
print(f"Person ID: {person_id}")

# 1️⃣ اختبر الـ token أولاً
print("\n1. Testing token validity...")
result = requests.get(
    "https://api.linkedin.com/v2/me",
    headers={"Authorization": f"Bearer {token}"}
)
print(f"Status: {result.status_code}")
if result.status_code == 200:
    me = result.json()
    print(f"Your LinkedIn ID: {me.get('id')}")
    print(f"Your sub: {me.get('sub')}")
else:
    print(f"Error: {result.text}")

# 2️⃣ حاول النشر باستخدام urn:li:person
print("\n2. Attempting to post...")
url = "https://api.linkedin.com/v2/ugcPosts"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

payload = {
    "author": f"urn:li:member:{person_id}", 
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {"text": "Test post from automation"},
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

result = requests.post(url, headers=headers, json=payload)
print(f"Status: {result.status_code}")
print(f"Response: {result.text}")
