import os
import requests

# الإعدادات - يتم سحبها من GitHub Secrets
ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')
PERSON_ID = os.getenv('LINKEDIN_PERSON_ID')
# تم التحديث إلى إصدار أبريل 2026 بناءً على سجلات الأخطاء
# جرب تغيير هذا السطر في الكود عندك
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
        print(f"🚀 Attempting to post using LinkedIn API Version: {API_VERSION}...")
        response = requests.post(url, headers=headers, json=post_data)
        
        if response.status_code in [201, 200]:
            print(f"✅ Success! Post created successfully.")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            if response.status_code == 426:
                print("💡 تلميح: لينكدإن تطلب إصداراً أحدث، جرب '202605' إذا استمر الخطأ.")
            elif response.status_code == 401:
                print("💡 تلميح: الـ Token قد يكون منتهي الصلاحية أو غير صحيح.")
                
    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")

if __name__ == "__main__":
    if not ACCESS_TOKEN or not PERSON_ID:
        print("❌ Error: Missing Environment Variables (LINKEDIN_TOKEN or LINKEDIN_PERSON_ID)")
    else:
        post_to_linkedin()
