import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from gui.login import LoginWindow
from gui.admin_dashboard import AdminDashboard
from gui.customer_dashboard import CustomerDashboard
from dotenv import load_dotenv
import os
from session import save_session, load_session, clear_session

# Load environment variables
load_dotenv()

# MongoDB connection string from .env
MONGO_URI = os.getenv('MONGO_URI')

class MainController:
    def __init__(self, app, mongo_uri):
        self.app = app
        self.mongo_uri = mongo_uri
        self.admin_dashboard = None
        self.customer_dashboard = None
        self.login_window = None
        session_user = load_session()
        if session_user:
            self.on_login_success(session_user, save=False)
        else:
            self.show_login()

    def show_login(self):
        self.login_window = LoginWindow(mongo_uri=self.mongo_uri)
        self.login_window.login_success = self.on_login_success
        self.login_window.logout_success = self.on_logout
        self.login_window.show()

    def on_login_success(self, user, save=True):
        if save:
            save_session(user)
        if self.login_window:
            self.login_window.close()
        if user['role'] == 'admin':
            self.admin_dashboard = AdminDashboard(self.mongo_uri)
            self.admin_dashboard.logout_success = self.on_logout
            self.admin_dashboard.show()
        else:
            self.customer_dashboard = CustomerDashboard(self.mongo_uri, user['username'])
            self.customer_dashboard.logout_success = self.on_logout
            self.customer_dashboard.show()

    def on_logout(self):
        if self.admin_dashboard:
            self.admin_dashboard.close()
            self.admin_dashboard = None
        if self.customer_dashboard:
            self.customer_dashboard.close()
            self.customer_dashboard = None
        self.show_login()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = MainController(app, MONGO_URI)
    sys.exit(app.exec_())
