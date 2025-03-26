import requests
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

client_id = os.getenv("HH_CLIENT_ID")
client_secret = os.getenv("HH_CLIENT_SECRET")
code = os.getenv("HH_AUTH_CODE")  # Временный code из URL

url = "https://hh.ru/oauth/token"
data = {
    "grant_type": "authorization_code",
    "client_id": client_id,
    "client_secret": client_secret,
    "code": code
}

response = requests.post(url, data=data)

if response.ok:
    tokens = response.json()
    print("✅ Access token:", tokens["access_token"])
    print("🔁 Refresh token:", tokens["refresh_token"])
else:
    print("❌ Ошибка при получении токенов:")
    print(response.status_code, response.text)


access_token = os.getenv("HH_ACCESS_TOKEN")  # вставь временный токен сюда

headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get("https://api.hh.ru/resumes/mine", headers=headers)

if response.ok:
    data = response.json()
    print("🧾 Найдено резюме:")
    for i, resume in enumerate(data.get("items", []), start=1):
        print(f"{i}. {resume['title']} — ID: {resume['id']}")
else:
    print("❌ Ошибка при получении списка резюме:")
    print(response.status_code, response.text)   