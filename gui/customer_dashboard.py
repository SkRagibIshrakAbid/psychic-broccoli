from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QListWidget, QMessageBox, QLineEdit, QInputDialog, QTextEdit, QHBoxLayout
import pandas as pd
from pymongo import MongoClient
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email, EmailNotValidError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
import logging
import glob

logging.basicConfig(filename='customer_dashboard_debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

class CustomerDashboard(QWidget):
    def __init__(self, mongo_uri, user_email):
        super().__init__()
        self.setWindowTitle("Customer Dashboard")
        self.setGeometry(200, 200, 600, 500)
        self.mongo_uri = mongo_uri
        self.user_email = user_email
        self.client = MongoClient(self.mongo_uri) if self.mongo_uri else None
        self.db = self.client['bulk_email_app'] if self.client else None
        self.logout_success = None
        self.init_ui()
        self.center()
        self.sender_emails = []
        self.failed_emails = []
        self.dest_emails = []

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel(f"Welcome, {self.user_email}")
        self.add_sender_btn = QPushButton("Add Gmail Sender Account (OAuth)")
        self.add_sender_btn.clicked.connect(self.add_sender)
        self.sender_list = QListWidget()
        self.reset_sender_btn = QPushButton("Reset Senders")
        self.reset_sender_btn.clicked.connect(self.reset_senders)
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Email Subject")
        self.reset_subject_btn = QPushButton("Reset Subject")
        self.reset_subject_btn.clicked.connect(lambda: self.subject_input.clear())
        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("Email Body (Rich Text Supported)")
        self.reset_body_btn = QPushButton("Reset Body")
        self.reset_body_btn.clicked.connect(lambda: self.body_input.clear())
        self.attach_btn = QPushButton("Add Attachments")
        self.attach_btn.clicked.connect(self.add_attachments)
        self.attach_list = QListWidget()
        self.reset_attach_btn = QPushButton("Reset Attachments")
        self.reset_attach_btn.clicked.connect(self.reset_attachments)
        self.upload_csv_btn = QPushButton("Upload Destination Emails (CSV)")
        self.upload_csv_btn.clicked.connect(self.upload_csv)
        self.dest_list = QListWidget()
        self.reset_dest_btn = QPushButton("Reset Destinations")
        self.reset_dest_btn.clicked.connect(self.reset_destinations)
        self.send_btn = QPushButton("Send Bulk Emails")
        self.send_btn.clicked.connect(self.send_bulk_emails)
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.logout)
        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.add_sender_btn)
        layout.addWidget(self.sender_list)
        layout.addWidget(self.reset_sender_btn)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.reset_subject_btn)
        layout.addWidget(self.body_input)
        layout.addWidget(self.reset_body_btn)
        layout.addWidget(self.attach_btn)
        layout.addWidget(self.attach_list)
        layout.addWidget(self.reset_attach_btn)
        layout.addWidget(self.upload_csv_btn)
        layout.addWidget(self.dest_list)
        layout.addWidget(self.reset_dest_btn)
        layout.addWidget(self.send_btn)
        layout.addWidget(self.logout_btn)
        self.setLayout(layout)
        self.attachments = []
        self.load_senders_from_tokens()
        self.setStyleSheet("""
            QWidget {
                background: #f7f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2d3a4a;
            }
            QPushButton {
                background: #1976d2;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #1565c0;
            }
            QLineEdit, QTextEdit, QListWidget {
                background: #fff;
                border: 1px solid #cfd8dc;
                border-radius: 4px;
                padding: 6px;
            }
        """)
        # Consistent button colors
        add_btn_style = "background: #1976d2; color: white; border-radius: 6px; padding: 8px 16px; font-size: 14px;"
        reset_btn_style = "background: #f5f5f5; color: #333; border-radius: 6px; padding: 8px 16px; font-size: 14px; border: 1px solid #bdbdbd;"
        self.add_sender_btn.setStyleSheet(add_btn_style)
        self.attach_btn.setStyleSheet(add_btn_style)
        self.upload_csv_btn.setStyleSheet(add_btn_style)
        self.send_btn.setStyleSheet("background: #43a047; color: white; border-radius: 6px; padding: 8px 16px; font-size: 14px;")
        self.reset_sender_btn.setStyleSheet(reset_btn_style)
        self.reset_subject_btn.setStyleSheet(reset_btn_style)
        self.reset_body_btn.setStyleSheet(reset_btn_style)
        self.reset_attach_btn.setStyleSheet(reset_btn_style)
        self.reset_dest_btn.setStyleSheet(reset_btn_style)
        self.logout_btn.setStyleSheet("background: #e53935; color: white; border-radius: 6px; padding: 8px 16px; font-size: 14px;")

    def load_senders_from_tokens(self):
        self.sender_emails = []
        self.sender_list.clear()
        for token_file in glob.glob(os.path.join(os.getcwd(), 'token_*.pickle')):
            try:
                import pickle
                with open(token_file, 'rb') as f:
                    creds = pickle.load(f)
                from googleapiclient.discovery import build
                service = build('gmail', 'v1', credentials=creds)
                profile = service.users().getProfile(userId='me').execute()
                email = profile.get('emailAddress', 'Unknown')
                self.sender_emails.append({'email': email, 'creds': creds, 'token_path': token_file, 'limit': 500})
                self.sender_list.addItem(email)
            except Exception as e:
                print(f"Failed to load sender from {token_file}: {e}")

    def add_sender(self):
        import traceback
        SCOPES = [
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/gmail.readonly'
        ]
        creds = None
        email = None
        from google_auth_oauthlib.flow import InstalledAppFlow
        try:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            from googleapiclient.discovery import build
            service = build('gmail', 'v1', credentials=creds)
            profile = service.users().getProfile(userId='me').execute()
            email = profile.get('emailAddress', 'Unknown')
            token_path = os.path.join(os.getcwd(), f'token_{email}.pickle')
            import pickle
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            self.sender_emails.append({'email': email, 'creds': creds, 'token_path': token_path, 'limit': 500})
            self.sender_list.addItem(email)
            QMessageBox.information(self, "Success", f"Sender {email} added and token saved as {token_path}")
        except Exception as e:
            print("Error in add_sender:", e)
            print(traceback.format_exc())
            QMessageBox.critical(self, "Error", f"Failed to add sender: {e}")

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            df = pd.read_csv(file_path)
            emails = df.iloc[:,0].dropna().tolist()
            self.dest_emails = emails
            self.dest_list.clear()
            self.dest_list.addItems(emails)

    def add_attachments(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Attachments")
        if files:
            self.attachments.extend(files)
            self.attach_list.addItems(files)

    def send_bulk_emails(self):
        if not self.sender_emails:
            QMessageBox.warning(self, "Error", "Add at least one Gmail sender account.")
            return
        if not self.dest_emails:
            QMessageBox.warning(self, "Error", "Upload a CSV with destination emails.")
            return
        subject = self.subject_input.text().strip()
        body = self.body_input.toHtml()
        attachments = getattr(self, 'attachments', [])
        failed = []
        sender_idx = 0
        sender_limits = [500 for _ in self.sender_emails]
        for dest in self.dest_emails:
            try:
                validate_email(dest)
            except EmailNotValidError:
                failed.append(dest)
                continue
            # Find next sender with quota
            while sender_idx < len(self.sender_emails) and sender_limits[sender_idx] <= 0:
                sender_idx += 1
            if sender_idx >= len(self.sender_emails):
                failed.append(dest)
                continue
            sender = self.sender_emails[sender_idx]
            try:
                service = build('gmail', 'v1', credentials=sender['creds'])
                message = self.create_message(sender['email'], dest, subject, body, attachments)
                service.users().messages().send(userId='me', body=message).execute()
                sender_limits[sender_idx] -= 1
            except Exception as e:
                failed.append(dest)
                if 'limit' in str(e).lower():
                    sender_limits[sender_idx] = 0
        if failed:
            failed_path = os.path.join(os.getcwd(), "failed_emails.csv")
            pd.DataFrame(failed).to_csv(failed_path, index=False, header=False)
            QMessageBox.warning(self, "Failed", f"Some emails failed. See {failed_path}")
        else:
            QMessageBox.information(self, "Success", "All emails sent!")

    def create_message(self, sender, to, subject, body, attachments):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        import base64
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        message.attach(MIMEText(body, 'html'))
        for file in attachments:
            with open(file, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file)}"')
                message.attach(part)
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw}

    def logout(self):
        from session import clear_session
        clear_session()
        QMessageBox.information(self, "Logged Out", "You have been logged out.")
        self.close()
        if self.logout_success:
            self.logout_success()

    def reset_fields(self):
        self.subject_input.clear()
        self.body_input.clear()
        self.attachments = []
        self.attach_list.clear()
        self.dest_emails = []
        self.dest_list.clear()
        self.sender_emails = []
        self.sender_list.clear()

    def reset_senders(self):
        self.sender_emails = []
        self.sender_list.clear()

    def reset_attachments(self):
        self.attachments = []
        self.attach_list.clear()

    def reset_destinations(self):
        self.dest_emails = []
        self.dest_list.clear()

    def center(self):
        # Center the window on the screen
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showEvent(self, event):
        super().showEvent(event)
        self.center()
