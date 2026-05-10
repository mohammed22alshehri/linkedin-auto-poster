import os
import requests

# الإعدادات
ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')
PERSON_ID = os.getenv('LINKEDIN_PERSON_ID')

def post_to_linkedin():
    url = "https://api.linkedin.com/rest/posts"
    
    # تحديث الإصدار إلى 202512 أو 202601
    # لينكدإن تطلب صيغة YYYYMM
    api_version = "202401" 

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "LinkedIn-Version": api_version,
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

    response = requests.post(url, headers=headers, json=post_data)
    
    if response.status_code in [201, 200]:
        print(f"✅ Success! Post created using version {api_version}")
    else:
        # إذا استمر خطأ الإصدار، سنطبع الاستجابة لنعرف الإصدارات المدعومة حالياً
        print(f"❌ Error {response.status_code}: {response.text}")
        if response.status_code == 426:
            print("💡 تلميح: جرب تغيير api_version في الكود إلى '202601' أو '202604'.")

if __name__ == "__main__":
    post_to_linkedin()
