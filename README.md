# Python Desktop Bulk Email Sender

This application is a professional desktop GUI for bulk email sending, supporting admin and customer roles, MongoDB Atlas integration, Gmail account rotation, and CSV import/export. Customers register and are activated by admins before use. Failed email addresses are saved if all sender accounts hit their limits.

## Features
- Admin and customer user types
- Customer registration and admin activation (admins approve new users)
- MongoDB Atlas for user and email data (see `.env` for connection string)
- Bulk email sending with multiple Gmail accounts (rotates on limit, 500/day per sender)
- Gmail API OAuth2 integration for secure sending (see `GMAIL_API_SETUP.md`)
- CSV upload for destination emails
- Failed emails saved to `failed_emails.csv` if all senders are exhausted
- Professional, easy-to-use, modern GUI (PyQt5)
- Session system for persistent login/logout
- Individual reset buttons for each field
- Consistent color scheme for all buttons

## Setup
1. Ensure Python 3.8+ is installed
2. Install dependencies: `conda install --file requirements.txt` or `pip install -r requirements.txt`
3. Configure MongoDB Atlas connection in `.env` (see example below)
4. Set up Gmail API credentials (see `GMAIL_API_SETUP.md`)
5. Run the app: `python main.py`

### Example `.env` file
```
MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/bulk_email_app?retryWrites=true&w=majority
```

## Usage
- Register as a customer; wait for admin activation.
- Admins can activate/deactivate users from the admin dashboard.
- Customers can add multiple Gmail sender accounts (OAuth2 flow, see `GMAIL_API_SETUP.md`).
- Each sender's token is saved as `token_<email>.pickle` in the project root.
- Upload a CSV of destination emails (first column only).
- Compose your email, add attachments if needed, and send.
- If all sender accounts hit their daily limit, failed emails are saved to `failed_emails.csv`.
- Use the logout button to end your session securely.

## Notes
- Use only free Gmail accounts for sending (500 emails/day/account limit).
- Never commit `credentials.json`, `.env`, or `token_*.pickle` files to version control (see `.gitignore`).
- For Gmail API setup, see the detailed instructions in `GMAIL_API_SETUP.md`.
- For troubleshooting OAuth/token issues, check `customer_dashboard_debug.log`.

---

For detailed Gmail API setup, see [GMAIL_API_SETUP.md](GMAIL_API_SETUP.md).
