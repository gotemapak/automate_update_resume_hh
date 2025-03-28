import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_telegram_message(text):
    token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")
    if not token or not chat_id:
        print("ℹ️ Telegram переменные не заданы — пропускаем отправку.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("⚠️ Ошибка при отправке в Telegram:", e)

def get_tokens_if_needed():
    if not os.getenv("HH_AUTH_CODE"):
        return
    print("📥 Получаем токены по HH_AUTH_CODE...")
    url = "https://hh.ru/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("HH_CLIENT_ID"),
        "client_secret": os.getenv("HH_CLIENT_SECRET"),
        "code": os.getenv("HH_AUTH_CODE")
    }
    response = requests.post(url, data=data)
    if response.ok:
        tokens = response.json()
        print("✅ Access token:", tokens["access_token"])
        print("🔁 Refresh token:", tokens["refresh_token"])
        send_telegram_message("✅ Получены новые токены (access + refresh).")
    else:
        print("❌ Ошибка при получении токенов:")
        print(response.status_code, response.text)
        send_telegram_message(f"❌ Ошибка при получении токенов: {response.text}")

def list_resumes_if_token():
    access_token = os.getenv("HH_ACCESS_TOKEN")
    if not access_token:
        return
    print("📄 Получаем список резюме...")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.hh.ru/resumes/mine", headers=headers)
    if response.ok:
        data = response.json()
        print("🧾 Найдено резюме:")
        for i, resume in enumerate(data.get("items", []), start=1):
            print(f"{i}. {resume['title']} — ID: {resume['id']}")
    else:
        print("❌ Ошибка при получении списка резюме:")
        print(response.status_code, response.text)

def get_access_token():
    print("🔁 Пытаемся получить access_token через refresh_token...")
    url = "https://hh.ru/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": os.getenv("HH_REFRESH_TOKEN"),
        "client_id": os.getenv("HH_CLIENT_ID"),
        "client_secret": os.getenv("HH_CLIENT_SECRET")
    }
    response = requests.post(url, data=data)
    
    # Проверяем на ошибку "token not expired"
    if not response.ok:
        try:
            error_data = response.json()
            if error_data.get("error") == "invalid_grant" and "not expired" in error_data.get("error_description", ""):
                print("ℹ️ API сообщает, что текущий токен ещё действителен - используем HH_ACCESS_TOKEN")
                access_token = os.getenv("HH_ACCESS_TOKEN")
                if access_token:
                    return access_token
                else:
                    print("⚠️ HH_ACCESS_TOKEN не найден в переменных окружения")
        except:
            pass
            
        print("⚠️ Не удалось получить access_token через refresh_token")
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

def update_resumes_if_possible():
    try:
        access_token = get_access_token()
    except Exception as e:
        print(f"❌ Ошибка при получении access_token: {str(e)}")
        access_token = os.getenv("HH_ACCESS_TOKEN")
        if not access_token:
            error_msg = "❌ Нет access_token и не удалось получить его через refresh_token."
            print(error_msg)
            send_telegram_message(error_msg)
            return
        else:
            print("🔑 Используем резервный HH_ACCESS_TOKEN из переменных окружения")
    
    resume_ids = os.getenv("HH_RESUME_IDS")
    if not resume_ids:
        print("❌ Переменная HH_RESUME_IDS не найдена.")
        send_telegram_message("❌ Переменная HH_RESUME_IDS не найдена.")
        return
    for rid in resume_ids.split(","):
        rid = rid.strip()
        if rid:
            update_resume(access_token, rid)

if __name__ == "__main__":
    print("🚀 Запуск all-in-one resume bot")
    get_tokens_if_needed()
    list_resumes_if_token()
    update_resumes_if_possible()
