# Автоматическое обновление резюме на HH.ru

[English version](README_EN.md)

🕒 Скрипт для автоматического обновления одного или нескольких резюме на hh.ru. Работает как локально, так и через GitHub Actions.

---

## 🚀 Возможности
- Обновляет одно или несколько резюме с помощью [hh.ru API](https://github.com/hhru/api).
- Поддерживает запуск каждые 4 часа через GitHub Actions.
- Использует `.env` файл для безопасного хранения токенов и конфигурации.
- Позволяет подставлять временный `access_token` вручную при локальном тестировании.
- Отправляет уведомления о результатах обновления в Telegram.

---

## 🧰 Что нужно

1. **Зарегистрируй приложение на hh.ru**  
   https://dev.hh.ru/admin  
   Получи `client_id` и `client_secret`.

2. **Получить `refresh_token`**  
   Сначала получаешь `code` через OAuth, затем обмениваешь его на `access_token` и `refresh_token`.

3. **Узнать ID своих резюме**  
   Выполни запрос `GET https://api.hh.ru/resumes/mine`, используя `access_token`.

4. **Настроить Telegram бота (опционально)**  
   - Создай бота через [@BotFather](https://t.me/botfather)
   - Получи `TG_BOT_TOKEN`
   - Узнай свой `TG_CHAT_ID` (можно через [@userinfobot](https://t.me/userinfobot))

---

## 🔐 Переменные окружения (.env)

Создай `.env` файл рядом со скриптом и добавь:

```
HH_CLIENT_ID=твой_client_id
HH_CLIENT_SECRET=твой_client_secret
HH_REFRESH_TOKEN=твой_refresh_token
HH_RESUME_IDS=resume_id1,resume_id2,resume_id3
# Опционально, только для локального запуска:
HH_ACCESS_TOKEN=временный_access_token

# Опционально, для уведомлений в Telegram:
TG_BOT_TOKEN=твой_токен_бота
TG_CHAT_ID=твой_chat_id
```

---

## 📆 GitHub Actions (если используешь)

Файл `update_resume.yml` запускается:

```yaml
on:
  schedule:
    - cron: "0 */4 * * *"  # Каждые 4 часа
  workflow_dispatch:       # Вручную
```

В GitHub → Settings → Secrets добавь:

| Название              | Описание                        |
|------------------------|---------------------------------|
| `HH_CLIENT_ID`         | ID приложения                   |
| `HH_CLIENT_SECRET`     | Секрет приложения               |
| `HH_REFRESH_TOKEN`     | Токен обновления                |
| `HH_RESUME_IDS`        | ID резюме через запятую         |
| `TG_BOT_TOKEN`         | Токен Telegram бота             |
| `TG_CHAT_ID`           | ID чата для уведомлений         |

---

## 💻 Как запустить локально

1. Создай виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate  # или .\venv\Scripts\activate на Windows
```

2. Установи зависимости:

```bash
pip install -r requirements.txt
```

3. Создай `.env` файл, как указано выше.

4. Запусти скрипт:

```bash
python update_resume.py
```

---

## 🧪 Отладка вручную

Если `refresh_token` ещё не истёк и HH возвращает `token not expired`, можно временно подставить `access_token` вручную через переменную `HH_ACCESS_TOKEN`.

---

Сделано с ❤️ чтобы твоё резюме всегда было наверху.
