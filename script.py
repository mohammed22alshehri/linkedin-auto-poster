import requests
import os

print("Testing LinkedIn API Connection...")

token = os.getenv('LINKEDIN_TOKEN')
person_id = os.getenv('LINKEDIN_PERSON_ID', '').strip()

# الهيدر الموحد لجميع الطلبات
# سنستخدم إصدار 202506 لأنه متوافق مع الأنظمة الحديثة
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0",
    "LinkedIn-Version": "202506" 
}

# 1️⃣ اختبار التوكن (يجب إرسال الهيدر هنا أيضاً لتجنب 404)
print("\n1. Testing token validity...")
test_url = "https://api.linkedin.com/rest/userinfo"
result = requests.get(test_url, headers=headers)

print(f"Status: {result.status_code}")
if result.status_code == 200:
    me = result.json()
    print(f"Connection Successful! Hello {me.get('given_name')}")
    # إذا لم تكن متأكداً من الـ ID، السطر التالي سيطبع لك الـ sub الصحيح
    print(f"Your correct sub ID is: {me.get('sub')}")
else:
    print(f"Error during test: {result.text}")

# 2️⃣ محاولة النشر
print("\n2. Attempting to post...")
post_url = "https://api.linkedin.com/rest/posts"

payload = {
    "author": f"urn:li:person:{person_id}",
    "commentary": "Automation test post - System Update 2026",
    "visibility": "PUBLIC",
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": False
}

response = requests.post(post_url, headers=headers, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
