import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    url = "https://hh.ru/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": os.environ["HH_REFRESH_TOKEN"],
        "client_id": os.environ["HH_CLIENT_ID"],
        "client_secret": os.environ["HH_CLIENT_SECRET"]
    }
    response = requests.post(url, data=data)
    if not response.ok:
        print("⚠️ Не удалось получить access_token (возможно, он ещё не истёк)")
        print("Статус:", response.status_code)
        print("Ответ:", response.text)
        raise Exception("Access token refresh failed.")
    return response.json()["access_token"]

def update_resume(token, resume_id):
    url = f"https://api.hh.ru/resumes/{resume_id}/publish"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers)
    if response.status_code == 204:
        print(f"✅ Resume {resume_id} updated successfully.")
    else:
        print(f"❌ Failed to update resume {resume_id}:")
        print(response.status_code, response.text)

if __name__ == "__main__":
    try:
        access_token = get_access_token()
    except:
        access_token = os.getenv("HH_ACCESS_TOKEN")  # временно вручную вставленный токен

    resume_ids = os.getenv("HH_RESUME_IDS")
    if not resume_ids:
        print("❌ Переменная HH_RESUME_IDS не найдена в окружении!")
        exit(1)
    resume_ids = resume_ids.split(",")

    for rid in resume_ids:
        rid = rid.strip()
        if rid:
            update_resume(access_token, rid)