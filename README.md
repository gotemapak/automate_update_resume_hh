# HeadHunter Resume Auto-Updater

A Python script to automatically update your HeadHunter.ru resumes.

## Features

- Automatic resume updates on HeadHunter.ru
- OAuth2 authentication with refresh token support
- Support for multiple resumes
- Environment-based configuration

## Setup

1. Clone the repository:
```bash
git clone git@github.com:gotemapak/automate_update_resume_hh.git
cd automate_update_resume_hh
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your HeadHunter API credentials:
```env
HH_CLIENT_ID=your_client_id
HH_CLIENT_SECRET=your_client_secret
HH_REFRESH_TOKEN=your_refresh_token
HH_ACCESS_TOKEN=your_access_token
HH_RESUME_IDS=resume_id1,resume_id2
```

## Usage

Run the script to update your resumes:
```bash
python update_resume.py
```

## Getting API Credentials

1. Go to [HeadHunter Developer Portal](https://dev.hh.ru/)
2. Create a new application
3. Get your Client ID and Client Secret
4. Follow the OAuth2 flow to get your refresh token

## License

MIT 