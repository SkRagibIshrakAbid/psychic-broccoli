from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from pymongo import MongoClient

class LoginWindow(QWidget):
    def __init__(self, mongo_uri):
        super().__init__()
        self.setWindowTitle("Bulk Email Sender - Login")
        self.setGeometry(100, 100, 400, 250)
        self.mongo_uri = mongo_uri
        self.client = MongoClient(self.mongo_uri) if self.mongo_uri else None
        self.db = self.client['bulk_email_app'] if self.client else None
        self.logout_success = None
        self.init_ui()
        self.center()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("Login or Register")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #1976d2;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #cfd8dc;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #cfd8dc;")
        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("background: #1976d2; color: white; border-radius: 6px; padding: 8px 16px; font-size: 14px;")
        self.register_btn = QPushButton("Register")
        self.register_btn.setStyleSheet("background: #43a047; color: white; border-radius: 6px; padding: 8px 16px; font-size: 14px;")
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setStyleSheet("background: #e53935; color: white; border-radius: 6px; padding: 8px 16px; font-size: 14px;")
        self.reset_btn = QPushButton("Reset Fields")
        self.reset_btn.setStyleSheet("background: #bdbdbd; color: #222; border-radius: 6px; padding: 8px 16px; font-size: 14px;")
        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.register)
        self.logout_btn.clicked.connect(self.logout)
        self.reset_btn.clicked.connect(self.reset_fields)
        layout.addWidget(self.label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)
        self.logout_btn.hide()
        layout.addWidget(self.logout_btn)
        layout.addWidget(self.reset_btn)
        self.setLayout(layout)
        self.setStyleSheet("background: #f7f9fa; font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px;")

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return
        user = self.db.users.find_one({"username": username, "password": password})
        if not user:
            QMessageBox.warning(self, "Error", "Invalid credentials.")
            return
        if user['role'] == 'customer' and not user.get('active', False):
            QMessageBox.information(self, "Inactive", "Your account is not active. Please wait for admin approval.")
            return
        # Open admin or customer dashboard via callback
        if hasattr(self, 'login_success'):
            self.login_success(user)
        else:
            QMessageBox.information(self, "Success", f"Welcome, {user['role'].capitalize()}!")

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return
        if self.db.users.find_one({"username": username}):
            QMessageBox.warning(self, "Error", "Username already registered.")
            return
        self.db.users.insert_one({
            "username": username,
            "password": password,
            "role": "customer",
            "active": False
        })
        QMessageBox.information(self, "Registered", "Registration successful! Wait for admin activation.")

    def logout(self):
        from session import clear_session
        clear_session()
        QMessageBox.information(self, "Logged Out", "You have been logged out.")
        self.close()
        if self.logout_success:
            self.logout_success()

    def reset_fields(self):
        self.username_input.clear()
        self.password_input.clear()
