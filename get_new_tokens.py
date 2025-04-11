import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_new_tokens(auth_code):
    """Получение новых токенов по коду авторизации"""
    url = "https://hh.ru/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("HH_CLIENT_ID"),
        "client_secret": os.getenv("HH_CLIENT_SECRET"),
        "code": auth_code,
        "redirect_uri": "https://google.com"  # Используем Google как redirect URI
    }
    
    print("📤 Отправляем запрос на получение токенов...")
    response = requests.post(url, data=data)
    
    if response.ok:
        tokens = response.json()
        print("\n✅ Успешно получены новые токены!")
        print("\n🔑 Access Token (добавьте его в HH_ACCESS_TOKEN):")
        print(tokens["access_token"])
        print("\n🔄 Refresh Token (добавьте его в HH_REFRESH_TOKEN):")
        print(tokens["refresh_token"])
        print("\n⚠️ Важно: Сохраните оба токена в секретах GitHub Actions!")
    else:
        print("\n❌ Ошибка при получении токенов:")
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.text}")

def main():
    print("🚀 Утилита получения новых токенов для HH.ru\n")
    
    client_id = os.getenv("HH_CLIENT_ID")
    if not client_id:
        print("❌ Ошибка: HH_CLIENT_ID не найден в .env файле")
        return
        
    # Формируем URL для авторизации с Google
    auth_url = f"https://hh.ru/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri=https://google.com"
    
    print("❗️ Важно: Убедитесь, что в настройках вашего приложения на dev.hh.ru/admin")
    print("   добавлен Redirect URI: https://google.com")
    print("\n1️⃣ Откройте эту ссылку в браузере для авторизации:")
    print(auth_url)
    print("\n2️⃣ После авторизации вы будете перенаправлены на google.com")
    print("   В URL будет параметр code=XXXXX - скопируйте его значение")
    
    auth_code = input("\n3️⃣ Введите полученный код авторизации: ").strip()
    
    if auth_code:
        get_new_tokens(auth_code)
    else:
        print("❌ Код авторизации не может быть пустым")

if __name__ == "__main__":
    main() 