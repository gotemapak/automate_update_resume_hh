# Automatic Resume Updater for HH.RU Website

[Русская версия](README.md)

🕒 Automatically updates your HeadHunter (hh.ru) resumes using GitHub Actions or a local script.

## 📝 Description
A script that automates the process of updating your resume on HeadHunter.ru, helping to keep your resume at the top of search results. Supports both local execution and automated updates via GitHub Actions.

## 🚀 Features
- 🔄 Automatic resume updates via [hh.ru API](https://github.com/hhru/api)
- ⏰ Runs every 4 hours via GitHub Actions
- 🔐 Secure token storage in `.env` file
- 🔑 OAuth2 support with refresh token
- 📱 Telegram notifications for results
- 🛠️ Local execution and debugging support

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

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/gotemapak/automate_update_resume_hh.git
cd automate_update_resume_hh
```

### 2. Install Dependencies
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# For Windows:
venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root:
```env
# Required variables
HH_CLIENT_ID=your_client_id
HH_CLIENT_SECRET=your_client_secret
HH_REFRESH_TOKEN=your_refresh_token
HH_RESUME_IDS=resume_id1,resume_id2,resume_id3

# Recommended for reliability
# Used when "token not expired" error occurs
HH_ACCESS_TOKEN=temporary_access_token

# Optional, for Telegram notifications
TG_BOT_TOKEN=your_bot_token
TG_CHAT_ID=your_chat_id
```

### Important Note About Tokens

The HeadHunter API sometimes returns a `"token not expired"` error when trying to get a new access_token via a refresh_token if the previous token is still valid. In this case, the script will use `HH_ACCESS_TOKEN` from the environment variables.

**Recommendations:**
1. Obtain a valid access_token manually and add it to `.env` or GitHub secrets
2. Update `HH_ACCESS_TOKEN` approximately once a week, as it has a limited lifetime

### 4. Run the Script
```bash
python update_resume.py
```

## 🔍 Detailed Setup Guide

### 1. Getting HH.ru Tokens

1. Go to [dev.hh.ru/admin](https://dev.hh.ru/admin)
2. Create a new application
3. Get your `client_id` and `client_secret`
4. Add redirect URI to your app: `http://localhost:8080`
5. Get the `code` via OAuth:
   - Open in browser: `https://hh.ru/oauth/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8080`
   - After authorization, you'll get the `code` in the URL
6. Add the received `code` to `.env` as `HH_AUTH_CODE`
7. Run the script - it will automatically get `access_token` and `refresh_token`

### 2. Getting Resume IDs

1. After getting `access_token`, run the script
2. The console will show a list of your resumes with their IDs
3. Copy the needed IDs to the `HH_RESUME_IDS` variable, separated by commas

### 3. Setting Up Telegram Bot

1. Find [@BotFather](https://t.me/botfather) in Telegram
2. Send `/newbot` and follow the instructions
3. Save the received token as `TG_BOT_TOKEN`
4. Find [@userinfobot](https://t.me/userinfobot)
5. Send it any message
6. Save the received ID as `TG_CHAT_ID`

## 📆 GitHub Actions (if using)

The automatic update system takes into account HeadHunter's limitation (no more than once every 4 hours):

```yaml
on:
  schedule:
    - cron: "1 */4 * * *"  # Run at minute 1 every 4 hours
  workflow_dispatch:
```

### 🔄 Scheduled Updating
The script runs exactly once every 4 hours (at the first minute of each 4th hour), which aligns with HeadHunter API limitations. Schedule:
- 00:01
- 04:01
- 08:01
- 12:01
- 16:01
- 20:01

This prevents "Can't publish resume: too often" errors and ensures efficient updating.

> **Note:** This is implemented using the workflow file `.github/workflows/check_and_update_resume.yml`, which runs on the defined schedule to update resumes.

Required secrets in GitHub:

| Secret Name         | Description                  |
|---------------------|------------------------------|
| `HH_CLIENT_ID`      | Your app's client ID         |
| `HH_CLIENT_SECRET`  | Your app's client secret     |
| `HH_REFRESH_TOKEN`  | OAuth refresh token          |
| `HH_RESUME_IDS`     | Comma-separated resume IDs   |
| `HH_ACCESS_TOKEN`   | Backup access token*         |
| `TG_BOT_TOKEN`      | Your Telegram bot token      |
| `TG_CHAT_ID`        | Chat ID for notifications    |
| `GITHUB_TOKEN`      | Added automatically          |

\* Used when "token not expired" error occurs

### ⚠️ Important
- Adding `HH_ACCESS_TOKEN` is **mandatory** for correct functioning with GitHub Actions
- Without this token, the script won't be able to update resumes if the API returns a "token not expired" error
- It's recommended to update `HH_ACCESS_TOKEN` about once a week, as it has a limited validity period

## 🧪 Manual Debugging

If your `refresh_token` is still valid and you're getting a `token not expired` error,
you can temporarily provide an `access_token` directly via `HH_ACCESS_TOKEN`.

## 📱 Notification Examples

### Successful Update
```
✅ Resume <b>123456</b> updated successfully.
```

### Update Error
```
Status: ❌ couldn't update resume due to touch_limit_exceeded

Resume: 123456
```

## ❓ Frequently Asked Questions

### Q: How often is the resume updated?
A: Every 4 hours and 1 minute via GitHub Actions (00:01, 04:01, 08:01, 12:01, 16:01, 20:01 UTC). This matches HH.ru's free tier limitation - on a free account, you can only update your resume once every 4 hours. If you try to update it more frequently, HH.ru will return an error.

### Q: Do I need to update tokens?
A: The `refresh_token` is valid for 30 days. The script will automatically notify you when tokens need to be updated. It's advisable to update `HH_ACCESS_TOKEN` once a week.

### Q: Why isn't Telegram working?
A: Check that:
1. The bot is added to the chat
2. The bot has permission to send messages
3. `TG_BOT_TOKEN` and `TG_CHAT_ID` are correctly set

### Q: Why do I get a "token not expired" error?
A: The HeadHunter API won't issue a new access_token via refresh_token if the old token is still valid. In this case, the script automatically uses the `HH_ACCESS_TOKEN` from environment variables as a backup.

---

Made with ❤️ to keep your resume on top of the search list. 