import os
import requests

LINKEDIN_TOKEN = os.getenv("LINKEDIN_TOKEN")

def get_my_id():
    # هذا الرابط مخصص لجلب بيانات صاحب التوكن (OpenID)
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {"Authorization": f"Bearer {LINKEDIN_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Your Name: {data.get('name')}")
        print(f"🆔 Your Person ID (sub): {data.get('sub')}")
        print(f"🔗 Full URN: urn:li:person:{data.get('sub')}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    get_my_id()
