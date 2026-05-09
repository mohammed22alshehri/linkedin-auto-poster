import os
import requests

LINKEDIN_TOKEN = os.getenv("LINKEDIN_TOKEN")

def check_token():
    # محاولة جلب بيانات البروفايل للتأكد من صلاحية التوكن
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {"Authorization": f"Bearer {LINKEDIN_TOKEN.strip()}"} # لاحظ الـ .strip() لإزالة المسافات
    
    print(f"Testing token: {LINKEDIN_TOKEN[:10]}...") # يطبع أول 10 حروف للتأكد
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("✅ Token is working perfectly from GitHub!")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"Reason: {response.text}")

if __name__ == "__main__":
    check_token()
