import os
import requests

# السحب من GitHub Secrets
ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')
PERSON_ID = os.getenv('LINKEDIN_PERSON_ID')

# التحديث إلى النسخة المقترحة من لينكدإن (بصيغة YYYYMM)
API_VERSION = '202411' 

def post_to_linkedin():
    url = "https://api.linkedin.com/rest/posts"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Linkedin-Version": API_VERSION,  # تم ربطها بالمتغير المحدث أعلاه
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    post_data = {
        "author": f"urn:li:person:{PERSON_ID}",
        "commentary": "اختبار نهائي للأتمتة 🚀",
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
        # الآن سيطبع الكود النسخة الفعلية المستخدمة في الإرسال
        print(f"🚀 جاري النشر باستخدام إصدار: {API_VERSION}...")
        response = requests.post(url, headers=headers, json=post_data)
        
        if response.status_code in [201, 200]:
            print("✅ تم النشر بنجاح على بروفايلك!")
        else:
            # طباعة الخطأ بالتفصيل للفحص في حال وجود تحديث آخر مطلوب
            print(f"❌ فشل الطلب: {response.status_code}")
            print(f"تفاصيل الخطأ: {response.text}")
            
    except Exception as e:
        print(f"⚠️ خطأ تقني: {e}")

if __name__ == "__main__":
    if not ACCESS_TOKEN or not PERSON_ID:
        print("❌ خطأ: تأكد من ضبط Secrets في GitHub!")
    else:
        post_to_linkedin()
