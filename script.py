import os
import requests

# السحب من GitHub Secrets
ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')
PERSON_ID = os.getenv('LINKEDIN_PERSON_ID')

# بناءً على صور الـ Endpoints، هذا هو الإصدار المتوافق مع منتجك
API_VERSION = '202401' 

def post_to_linkedin():
    url = "https://api.linkedin.com/rest/posts"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "LinkedIn-Version": API_VERSION,
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    post_data = {
        "author": f"urn:li:person:{PERSON_ID}",
        "commentary": "تم تحديث نظام الأتمتة بنجاح للتوافق مع إصدار 202401 🚀✨",
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
        print(f"🚀 المحاولة باستخدام إصدار API: {API_VERSION}...")
        response = requests.post(url, headers=headers, json=post_data)
        
        if response.status_code in [201, 200]:
            print("✅ تم النشر بنجاح!")
        else:
            print(f"❌ خطأ {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"⚠️ خطأ غير متوقع: {e}")

if __name__ == "__main__":
    if not ACCESS_TOKEN or not PERSON_ID:
        print("❌ خطأ: المتغيرات البيئية مفقودة!")
    else:
        post_to_linkedin()
