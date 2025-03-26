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
        msg = f"✅ Резюме {resume_id} обновлено успешно."
        print(msg)
        send_telegram_message(msg)
    else:
        msg = f"❌ Ошибка при обновлении резюме {resume_id}: {response.status_code} {response.text}"
        print(msg)
        send_telegram_message(msg)

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


def send_telegram_message(text):
    token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")

    if not token or not chat_id:
        print("ℹ️ Telegram переменные не заданы — пропускаем отправку.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print("⚠️ Не удалось отправить сообщение в Telegram.")
    except Exception as e:
        print("⚠️ Ошибка при отправке в Telegram:", e)