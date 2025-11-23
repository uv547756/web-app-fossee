"""
Login Dialog for user authentication
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon
from api.client import APIClient

class LoginDialog(QDialog):
    """Modal dialog for user login"""
    
    def __init__(self, api_client: APIClient, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.authenticated = False
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Login - Chemical Equipment Visualizer")
        self.setModal(True)
        self.setFixedSize(450, 300)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Chemical Equipment Visualizer")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: #667eea;
            margin-bottom: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #667eea, stop:1 #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        """)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Please login to continue")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #6c757d; font-size: 12px; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Username field
        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-weight: 600; color: #495057;")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e9ecef;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: #f8f9fa;
            }
        """)
        layout.addWidget(self.username_input)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-weight: 600; color: #495057; margin-top: 10px;")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e9ecef;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: #f8f9fa;
            }
        """)
        self.password_input.returnPressed.connect(self.handle_login)
        layout.addWidget(self.password_input)
        
        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("""
            color: #e74c3c;
            font-size: 12px;
            padding: 5px;
            background-color: #fadbd8;
            border-radius: 3px;
        """)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
        # Spacer
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                border: 2px solid #e9ecef;
                border-radius: 6px;
                background-color: white;
                color: #6c757d;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                border-color: #adb5bd;
                color: #495057;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.login_button = QPushButton("Login")
        self.login_button.setDefault(True)
        self.login_button.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #667eea, stop:1 #764ba2);
                color: white;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #764ba2, stop:1 #667eea);
            }
            QPushButton:disabled {
                background-color: #ced4da;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        button_layout.addWidget(self.login_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Set focus to username input
        self.username_input.setFocus()
        
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        # Validate input
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
        
        # Disable UI during login
        self.login_button.setEnabled(False)
        self.login_button.setText("Logging in...")
        self.username_input.setEnabled(False)
        self.password_input.setEnabled(False)
        self.cancel_button.setEnabled(False)
        self.error_label.hide()
        
        # Attempt login
        try:
            self.api_client.login(username, password)
            self.authenticated = True
            self.accept()
        except Exception as e:
            self.show_error(str(e))
            # Re-enable UI
            self.login_button.setEnabled(True)
            self.login_button.setText("Login")
            self.username_input.setEnabled(True)
            self.password_input.setEnabled(True)
            self.cancel_button.setEnabled(True)
            self.password_input.clear()
            self.password_input.setFocus()
            
    def show_error(self, message: str):
        """Show error message"""
        self.error_label.setText(message)
        self.error_label.show()
        
        # Auto-hide error after 5 seconds
        QTimer.singleShot(5000, self.error_label.hide)