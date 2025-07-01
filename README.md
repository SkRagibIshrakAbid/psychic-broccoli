# Python Desktop Bulk Email Sender

This application is a professional desktop GUI for bulk email sending, supporting admin and customer roles, MongoDB Atlas integration, Gmail account rotation, and CSV import/export. Customers register and are activated by admins before use. Failed email addresses are saved if all sender accounts hit their limits.

## Features
- Admin and customer user types
- Customer registration and admin activation
- MongoDB Atlas for user and email data
- Bulk email sending with multiple Gmail accounts (rotates on limit)
- CSV upload for destination emails
- Failed emails saved to file if all senders are exhausted
- Professional, easy-to-use GUI

## Setup
1. Ensure Python 3.8+ is installed
2. Install dependencies: `conda install --file requirements.txt` or `pip install -r requirements.txt`
3. Configure MongoDB Atlas connection in `.env`
4. Run the app: `python main.py`

## Notes
- Use only free Gmail accounts for sending
- Replace placeholder assets as needed
