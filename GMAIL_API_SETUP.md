# Gmail API Integration Instructions

To use the Gmail API for sending emails securely, follow these steps:

## 1. Create a Google Cloud Project
- Go to https://console.cloud.google.com/
- Create a new project (or select an existing one).

## 2. Enable Gmail API
- In the Cloud Console, go to "APIs & Services > Library".
- Search for "Gmail API" and enable it for your project.

## 3. Configure OAuth Consent Screen
- Go to "APIs & Services > OAuth consent screen".
- Set up the consent screen (choose External for most cases).
- Add your app details and authorized domains.

## 4. Create OAuth 2.0 Credentials
- Go to "APIs & Services > Credentials".
- Click "Create Credentials" > "OAuth client ID".
- Choose "Desktop app" as the application type.
- Download the `credentials.json` file and place it in your project root.

## 5. Install Required Packages
- Run: `pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client`

## 6. First-Time Authentication
- When adding a sender, the user will be prompted to log in to their Gmail and grant permission.
- A token will be saved for future use.

---

The code will be updated to use this flow for sender accounts.
