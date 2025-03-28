# Автоматическое обновление резюме на сайте HH.RU

[English version](README_EN.md)

🕒 Скрипт для автоматического обновления одного или нескольких резюме на hh.ru. Работает как локально, так и через GitHub Actions.

## 📝 Описание
Скрипт автоматизирует процесс обновления резюме на сайте HeadHunter.ru, что помогает поддерживать актуальность вашего резюме в поиске. Поддерживает как локальный запуск, так и автоматическое обновление через GitHub Actions.

## 🚀 Возможности
- 🔄 Автоматическое обновление резюме через [hh.ru API](https://github.com/hhru/api)
- ⏰ Запуск каждые 4 часа через GitHub Actions
- 🔐 Безопасное хранение токенов в `.env` файле
- 🔑 Поддержка OAuth2 с refresh token
- 📱 Уведомления о результатах в Telegram
- 🛠️ Возможность локального запуска и отладки

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

## 🚀 Быстрый старт

### 1. Клонируем репозиторий
```bash
git clone https://github.com/gotemapak/automate_update_resume_hh.git
cd automate_update_resume_hh
```

### 2. Устанавливаем зависимости
```bash
# Создаем виртуальное окружение
python3 -m venv venv

# Активируем его
# Для Windows:
venv\Scripts\activate
# Для macOS/Linux:
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt
```

### 3. Настраиваем переменные окружения
Создаем файл `.env` в корне проекта:
```env
# Обязательные переменные
HH_CLIENT_ID=твой_client_id
HH_CLIENT_SECRET=твой_client_secret
HH_REFRESH_TOKEN=твой_refresh_token
HH_RESUME_IDS=resume_id1,resume_id2,resume_id3

# Рекомендуется добавить для надежности
# Используется при ошибке "token not expired"
HH_ACCESS_TOKEN=временный_access_token

# Опционально, для уведомлений в Telegram
TG_BOT_TOKEN=твой_токен_бота
TG_CHAT_ID=твой_chat_id
```

### 4. Запускаем скрипт
```bash
python update_resume.py
```

## 🔍 Подробная инструкция по настройке

### 1. Получение токенов HH.ru

1. Перейдите на [dev.hh.ru/admin](https://dev.hh.ru/admin)
2. Создайте новое приложение
3. Получите `client_id` и `client_secret`
4. Добавьте в приложение redirect URI: `http://localhost:8080`
5. Получите `code` через OAuth:
   - Откройте в браузере: `https://hh.ru/oauth/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8080`
   - После авторизации вы получите `code` в URL
6. Добавьте полученный `code` в `.env` как `HH_AUTH_CODE`
7. Запустите скрипт - он автоматически получит `access_token` и `refresh_token`

### 2. Получение ID резюме

1. После получения `access_token`, запустите скрипт
2. В консоли появится список ваших резюме с их ID
3. Скопируйте нужные ID в переменную `HH_RESUME_IDS` через запятую

### 3. Настройка Telegram бота

1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте `/newbot` и следуйте инструкциям
3. Сохраните полученный токен в `TG_BOT_TOKEN`
4. Найдите [@userinfobot](https://t.me/userinfobot)
5. Отправьте ему любое сообщение
6. Сохраните полученный ID в `TG_CHAT_ID`

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
| `HH_ACCESS_TOKEN`      | Резервный токен доступа*        |
| `TG_BOT_TOKEN`         | Токен Telegram бота             |
| `TG_CHAT_ID`           | ID чата для уведомлений         |

\* Используется при ошибке "token not expired"

### ⚠️ Внимание
- Добавление `HH_ACCESS_TOKEN` **обязательно** для корректной работы через GitHub Actions
- Без этого токена скрипт не сможет обновить резюме, если API вернет ошибку "token not expired"
- Рекомендуется обновлять `HH_ACCESS_TOKEN` примерно раз в неделю, так как его срок действия ограничен

## 🧪 Отладка вручную

Если `refresh_token` ещё не истёк и HH возвращает `token not expired`, можно временно подставить `access_token` вручную через переменную `HH_ACCESS_TOKEN`.

## 📱 Примеры уведомлений

### Успешное обновление
```
✅ Резюме <b>123456</b> обновлено успешно.

💼 ID резюме: <code>123456</code>

🕒 Обновлено: 26.03.2024 16:45:30
```

### Ошибка обновления
```
❌ Ошибка при обновлении резюме <b>123456</b>:

💼 ID резюме: <code>123456</code>
⚠️ Статус: 400
📝 Ответ: {"errors": [{"type": "error", "value": "Resume not found"}]}

🕒 Обновлено: 26.03.2024 16:45:30
```

## ❓ Часто задаваемые вопросы

### Q: Как часто обновляется резюме?
A: По умолчанию каждые 4 часа через GitHub Actions. Это соответствует ограничению бесплатного тарифа HH.ru - на бесплатном аккаунте резюме можно обновлять не чаще, чем раз в 4 часа. Если вы попытаетесь обновить резюме чаще, HH.ru вернет ошибку.

### Q: Нужно ли обновлять токены?
A: `refresh_token` действителен 30 дней. Скрипт автоматически уведомит вас, когда нужно обновить токены. `HH_ACCESS_TOKEN` желательно обновлять раз в неделю.

### Q: Почему не работает Telegram?
A: Проверьте, что:
1. Бот добавлен в чат
2. У бота есть права на отправку сообщений
3. Правильно указаны `TG_BOT_TOKEN` и `TG_CHAT_ID`

### Q: Почему появляется ошибка "token not expired"?
A: API HeadHunter не выдает новый access_token через refresh_token, если старый токен еще действителен. В этом случае скрипт автоматически использует `HH_ACCESS_TOKEN` из переменных окружения как резервный вариант.

---

Сделано с ❤️ чтобы твоё резюме всегда было наверху.
