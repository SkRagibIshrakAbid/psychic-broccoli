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
- Add your app details and authorized domains (for desktop apps, you can use `localhost`).

## 4. Create OAuth 2.0 Credentials
- Go to "APIs & Services > Credentials".
- Click "Create Credentials" > "OAuth client ID".
- Choose "Desktop app" as the application type.
- Download the `credentials.json` file and place it in your project root (do not commit this file to version control).

## 5. Install Required Packages
- Run: `pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client`

## 6. Adding Sender Accounts (First-Time Authentication)
- In the app, click "Add Gmail Sender Account (OAuth)".
- A browser window will open. Log in to the Gmail account you want to use and grant permission.
- A token file named `token_<email>.pickle` will be saved in your project root for each sender account.
- Repeat this process for each Gmail account you want to use for sending.

## 7. Usage Notes
- Each sender account can send up to 500 emails per day (Gmail free account limit).
- The app will automatically rotate between sender accounts as limits are reached.
- If all senders are exhausted, failed emails are saved to `failed_emails.csv`.
- If you need to remove a sender, delete the corresponding `token_<email>.pickle` file and restart the app.

## Security
- Never commit `credentials.json` or any `token_*.pickle` files to version control (see `.gitignore`).
- Each user must perform the OAuth flow for their own sender accounts.

---

For more details on the overall app setup and usage, see [README.md](README.md).
