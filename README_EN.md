# HH Resume Updater

[Русская версия](README.md)

🕒 Automatically updates your HeadHunter (hh.ru) resumes using GitHub Actions or a local script.

## 🚀 Features
- Refreshes one or more resumes via [hh.ru API](https://github.com/hhru/api).
- Can be run locally or scheduled to run every 4 hours via GitHub Actions.
- Supports `.env` configuration for secure key management.
- Sends notifications about update results to Telegram.

---

## 🧰 Requirements

1. **HeadHunter API App**  
   Register your app at: https://dev.hh.ru/admin  
   Save the `client_id` and `client_secret`.

2. **Refresh Token**  
   Manually obtain it using your client credentials and an OAuth authorization code.

3. **Resume IDs**  
   Get them via the `/resumes/mine` API endpoint after logging in with an `access_token`.

4. **Set up Telegram Bot (Optional)**  
   - Create a bot via [@BotFather](https://t.me/botfather)
   - Get your `TG_BOT_TOKEN`
   - Find your `TG_CHAT_ID` (you can use [@userinfobot](https://t.me/userinfobot))

---

## 🔐 Environment Variables

Create a `.env` file with the following variables:

```
HH_CLIENT_ID=your_client_id
HH_CLIENT_SECRET=your_client_secret
HH_REFRESH_TOKEN=your_refresh_token
HH_RESUME_IDS=resume_id1,resume_id2,resume_id3
# Optional fallback for local testing:
HH_ACCESS_TOKEN=temporary_access_token

# Optional, for Telegram notifications:
TG_BOT_TOKEN=your_bot_token
TG_CHAT_ID=your_chat_id
```

---

## 📆 GitHub Actions Schedule

The included GitHub workflow runs every 4 hours and can also be triggered manually.

```yaml
on:
  schedule:
    - cron: "0 */4 * * *"
  workflow_dispatch:
```

Secrets required in GitHub:

| Secret Name         | Description                  |
|---------------------|------------------------------|
| `HH_CLIENT_ID`      | Your app's client ID         |
| `HH_CLIENT_SECRET`  | Your app's client secret     |
| `HH_REFRESH_TOKEN`  | OAuth refresh token          |
| `HH_RESUME_IDS`     | Comma-separated resume IDs   |
| `TG_BOT_TOKEN`      | Your Telegram bot token      |
| `TG_CHAT_ID`        | Chat ID for notifications    |

---

## 💻 Run Locally

1. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file (see example above).

4. Run the script:

```bash
python update_resume.py
```

---

## 🧪 Optional Debug

If your `refresh_token` is still valid and you're getting a `token not expired` error,
you can temporarily provide an `access_token` directly via `HH_ACCESS_TOKEN`.

---

Made with ❤️ to keep your resume on top of the search list. 