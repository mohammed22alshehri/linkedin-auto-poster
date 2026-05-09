import os
import requests
from groq import Groq

# الإعدادات من GitHub Secrets
LINKEDIN_TOKEN = os.getenv("LINKEDIN_TOKEN")
LINKEDIN_PERSON_ID = os.getenv("LINKEDIN_PERSON_ID") # تأكد أنه يبدأ بـ urn:li:person:
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_post():
    client = Groq(api_key=GROQ_API_KEY)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Write a professional LinkedIn post about AI and Automation."}]
    )
    return completion.choices[0].message.content

def post_to_linkedin(content):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    # التأكد من تنسيق الـ ID
    author = LINKEDIN_PERSON_ID if LINKEDIN_PERSON_ID.startswith("urn:li:person:") else f"urn:li:person:{LINKEDIN_PERSON_ID}"

    payload = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("🚀 DONE! Check your LinkedIn profile now.")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    post_content = generate_post()
    post_to_linkedin(post_content)
