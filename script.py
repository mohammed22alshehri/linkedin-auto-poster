import os

import requests



# السحب من GitHub Secrets

ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')

PERSON_ID = os.getenv('LINKEDIN_PERSON_ID')



# النسخة الحالية المدعومة لعام 2026

API_VERSION = '202601'



def post_to_linkedin():

url = "https://api.linkedin.com/rest/posts"



headers = {

"Authorization": f"Bearer {ACCESS_TOKEN}",

"Content-Type": "application/json",

"LinkedIn-Version": API_VERSION,

"X-Restli-Protocol-Version": "2.0.0"

}



# هيكلة البيانات بناءً على التحديثات الأخيرة لـ LinkedIn API

post_data = {

"author": f"urn:li:person:{PERSON_ID}",

"commentary": "تم تحديث الكود للهيكلية الجديدة بنجاح! 🚀",

"visibility": "PUBLIC", # في نظام /rest/posts الجديد تقبل PUBLIC كنص، لكن يفضل اتباع الهيكلية أدناه إذا واجهت رفضاً

"distribution": {

"feedDistribution": "MAIN_FEED",

"targetEntities": [],

"thirdPartyDistributionChannels": []

},

"lifecycleState": "PUBLISHED",

"isReshareDisabledByAuthor": False

}



try:

print(f"🚀 جاري محاولة النشر (إصدار {API_VERSION})...")

response = requests.post(url, headers=headers, json=post_data)



if response.status_code in [200, 201]:

print("✅ نجحت العملية! تم النشر على بروفايلك.")

else:

print(f"❌ فشل الطلب! كود الحالة: {response.status_code}")

# طباعة الـ Request ID مهم جداً لمراسلة دعم لينكدإن لو استمرت المشكلة

x_restli_id = response.headers.get('x-linkedin-id')

print(f"🆔 Request ID: {x_restli_id}")

print(f"📄 تفاصيل رد السيرفر: {response.text}")



except Exception as e:

print(f"⚠️ خطأ برمجـي: {e}")



if __name__ == "__main__":

if not ACCESS_TOKEN or not PERSON_ID:

print("❌ تأكد من ضبط Secrets (LINKEDIN_TOKEN & LINKEDIN_PERSON_ID)")

else:

post_to_linkedin()

