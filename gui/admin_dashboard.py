from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox
from pymongo import MongoClient

class AdminDashboard(QWidget):
    def __init__(self, mongo_uri):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(150, 150, 500, 400)
        self.mongo_uri = mongo_uri
        self.client = MongoClient(self.mongo_uri) if self.mongo_uri else None
        self.db = self.client['bulk_email_app'] if self.client else None
        self.logout_success = None
        self.init_ui()
        self.load_pending_users()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("Pending Customer Activations")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #1976d2;")
        self.user_list = QListWidget()
        self.user_list.setStyleSheet("background: #fff; border: 1px solid #cfd8dc; border-radius: 4px; padding: 6px;")
        self.activate_btn = QPushButton("Activate Selected")
        self.activate_btn.setStyleSheet("background: #43a047; color: white; border-radius: 6px; padding: 8px 16px; font-size: 14px;")
        self.activate_btn.clicked.connect(self.activate_user)
        self.reset_btn = QPushButton("Reset List")
        self.reset_btn.setStyleSheet("background: #bdbdbd; color: #222; border-radius: 6px; padding: 8px 16px; font-size: 14px;")
        self.reset_btn.clicked.connect(self.reset_fields)
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setStyleSheet("background: #e53935; color: white; border-radius: 6px; padding: 8px 16px; font-size: 14px;")
        self.logout_btn.clicked.connect(self.logout)
        layout.addWidget(self.label)
        layout.addWidget(self.user_list)
        layout.addWidget(self.activate_btn)
        layout.addWidget(self.reset_btn)
        layout.addWidget(self.logout_btn)
        self.setLayout(layout)
        self.setStyleSheet("background: #f7f9fa; font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px;")

    def load_pending_users(self):
        self.user_list.clear()
        users = self.db.users.find({"role": "customer", "active": False})
        for user in users:
            self.user_list.addItem(user['username'])

    def activate_user(self):
        selected = self.user_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Error", "No user selected.")
            return
        username = selected.text()
        self.db.users.update_one({"username": username}, {"$set": {"active": True}})
        QMessageBox.information(self, "Activated", f"{username} has been activated.")
        self.load_pending_users()

    def reset_fields(self):
        self.user_list.clear()

    def logout(self):
        from session import clear_session
        clear_session()
        QMessageBox.information(self, "Logged Out", "You have been logged out.")
        self.close()
        if self.logout_success:
            self.logout_success()
