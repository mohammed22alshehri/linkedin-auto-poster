import os
import requests

# الإعدادات
ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')
PERSON_ID = os.getenv('LINKEDIN_PERSON_ID')
# قمنا بتعريف الإصدار هنا لسهولة التغيير واستخدامه في الطباعة لاحقاً
API_VERSION = '202401' 

def post_to_linkedin():
    url = "https://api.linkedin.com/rest/posts"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "LinkedIn-Version": API_VERSION, # تأكد من وجود الفاصلة هنا
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    post_data = {
        "author": f"urn:li:person:{PERSON_ID}",
        "commentary": "تحديث تقني: تم ضبط نظام الأتمتة للعمل مع إصدارات API 2026 بنجاح! 🤖✨",
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
        response = requests.post(url, headers=headers, json=post_data)
        
        if response.status_code in [201, 200]:
            print(f"✅ Success! Post created using version {API_VERSION}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            if response.status_code == 426:
                print("💡 تلميح: جرب تغيير API_VERSION إلى '202604'.")
            elif response.status_code == 403:
                print("💡 تلميح: تأكد من إضافة منتج 'Share on LinkedIn' في لوحة التحكم وتفعيل صلاحية w_member_social.")
                
    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")

if __name__ == "__main__":
    post_to_linkedin()
