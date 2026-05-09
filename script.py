import requests
import os

print("Testing LinkedIn API Connection...")

token = os.getenv('LINKEDIN_TOKEN')
person_id = os.getenv('LINKEDIN_PERSON_ID').strip()

# الهيدرز الجديدة الإلزامية
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0",
    "LinkedIn-Version": "202401"  # هذا السطر يحل مشكلة NO_VERSION
}

# 1️⃣ اختبر الـ token بالمسار الجديد
print("\n1. Testing token validity...")
# نستخدم /rest/userinfo بدلاً من /v2/me لأنها الأحدث
result = requests.get("https://api.linkedin.com/rest/userinfo", headers=headers)

print(f"Status: {result.status_code}")
if result.status_code == 200:
    me = result.json()
    print(f"Your Profile Name: {me.get('given_name')} {me.get('family_name')}")
    # الـ sub هو الـ ID الذي يجب استخدامه في النشر
    print(f"Your correct ID (sub): {me.get('sub')}")
else:
    print(f"Error: {result.text}")

# 2️⃣ النشر باستخدام المسار المذكور في قائمتك /rest/posts
print("\n2. Attempting to post...")
url = "https://api.linkedin.com/rest/posts"

payload = {
    "author": f"urn:li:person:{person_id}", # تأكد أنها person
    "commentary": "Test post from automation using REST API",
    "visibility": "PUBLIC",
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": False
}

result = requests.post(url, headers=headers, json=payload)
print(f"Status: {result.status_code}")
print(f"Response: {result.text}")
