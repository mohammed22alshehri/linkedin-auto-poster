import os
import requests

# السحب من GitHub Secrets
ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')

# نسخة الـ API المدعومة
API_VERSION = '202601'

def get_my_urn():
    """جلب معرف المستخدم (Person ID) آلياً باستخدام التوكن"""
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            # في userinfo المعرف يكون في حقل 'sub'
            return user_data.get('sub')
        else:
            print(f"❌ فشل جلب بيانات المستخدم: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ خطأ أثناء جلب المعرف: {e}")
        return None

def post_to_linkedin():
    # 1. الحصول على المعرف الصحيح أولاً
    person_id = get_my_urn()
    if not person_id:
        print("❌ تعذر استخراج Person ID، تأكد من صلاحية التوكن.")
        return

    print(f"✅ تم تحديد المعرف: {person_id}")

    # 2. إعداد طلب النشر
    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "LinkedIn-Version": API_VERSION,
        "X-Restli-Protocol-Version": "2.0.0"
    }

    post_data = {
        "author": f"urn:li:person:{person_id}",
        "commentary": "تم النشر آلياً باستخدام GitHub Actions و LinkedIn API 2026 🚀",
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    try:
        print(f"🚀 جاري محاولة النشر...")
        response = requests.post(url, headers=headers, json=post_data)

        if response.status_code in [200, 201]:
            print("✅ نجحت العملية! تم النشر بنجاح.")
        else:
            print(f"❌ فشل النشر! كود الحالة: {response.status_code}")
            print(f"📄 الرد: {response.text}")
    except Exception as e:
        print(f"⚠️ خطأ برمجـي: {e}")

if __name__ == "__main__":
    if not ACCESS_TOKEN:
        print("❌ تأكد من ضبط Secret: LINKEDIN_TOKEN")
    else:
        post_to_linkedin()
