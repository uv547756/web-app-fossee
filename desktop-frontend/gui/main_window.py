"""
Main Window - Dashboard with charts and data visualization
Complete version combining all functionality
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFileDialog, QMessageBox, QLabel,
                             QTableWidget, QTableWidgetItem, QSplitter, QGroupBox,
                             QListWidget, QListWidgetItem, QHeaderView, QDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from api.client import APIClient
from gui.login_dialog import LoginDialog
from gui.chart_widgets import TypePieChart, FlowrateChart
import os
import subprocess
import platform

class UploadThread(QThread):
    """Background thread for CSV file upload"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_client, file_path):
        super().__init__()
        self.api_client = api_client
        self.file_path = file_path
        
    def run(self):
        """Execute upload in background"""
        try:
            result = self.api_client.upload_csv(self.file_path)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window with dashboard"""
    
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.current_dataset = None
        self.init_ui()
        self.show_login()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set window style with modern color scheme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fb;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e6ed;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
                color: #2c3e50;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #34495e;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Main content splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel (main content)
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel (history and actions)
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 6px;
                font-weight: 500;
            }
        """)
        
    def create_header(self):
        """Create header with title and upload button"""
        header = QWidget()
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #667eea, stop:1 #764ba2);
            border-radius: 8px;
            padding: 20px;
        """)
        layout = QHBoxLayout(header)
        
        # Title
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Upload button
        self.upload_button = QPushButton("📁 Upload CSV")
        self.upload_button.clicked.connect(self.upload_file)
        self.upload_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #56CCF2, stop:1 #2F80ED);
                color: white;
                padding: 12px 28px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #2F80ED, stop:1 #1e5fb8);
            }
            QPushButton:pressed {
                background: #1e5fb8;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        layout.addWidget(self.upload_button)
        
        return header
        
    def create_left_panel(self):
        """Create left panel with summary and charts"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Summary cards
        self.summary_widget = self.create_summary_cards()
        layout.addWidget(self.summary_widget)
        
        # Charts section
        charts_splitter = QSplitter(Qt.Horizontal)
        
        self.type_chart = TypePieChart()
        charts_splitter.addWidget(self.type_chart)
        
        self.flowrate_chart = FlowrateChart()
        charts_splitter.addWidget(self.flowrate_chart)
        
        layout.addWidget(charts_splitter)
        
        # Data table
        self.data_table = self.create_data_table()
        layout.addWidget(self.data_table)
        
        return panel
        
    def create_summary_cards(self):
        """Create summary statistics cards"""
        group = QGroupBox("Summary Statistics")
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        # Create card widgets
        self.total_label = self.create_stat_card("Total Equipment", "--")
        self.avg_flow_label = self.create_stat_card("Avg Flowrate", "--")
        self.avg_pressure_label = self.create_stat_card("Avg Pressure", "--")
        self.avg_temp_label = self.create_stat_card("Avg Temperature", "--")
        
        layout.addWidget(self.total_label)
        layout.addWidget(self.avg_flow_label)
        layout.addWidget(self.avg_pressure_label)
        layout.addWidget(self.avg_temp_label)
        
        group.setLayout(layout)
        return group
        
    def create_stat_card(self, title, value):
        """Create a single statistics card"""
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                           stop:0 #ffffff, stop:1 #f8f9fa);
                border: 2px solid #e3e8ef;
                border-radius: 10px;
                padding: 18px;
            }
            QWidget:hover {
                border: 2px solid #667eea;
                background: white;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #6c757d; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("color: #667eea; font-size: 28px; font-weight: bold; margin-top: 8px;")
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setObjectName("value_label")
        layout.addWidget(value_label)
        
        return card
        
    def update_stat_card(self, card, value):
        """Update the value in a stat card"""
        value_label = card.findChild(QLabel, "value_label")
        if value_label:
            value_label.setText(str(value))
            
    def create_data_table(self):
        """Create data table for displaying equipment data"""
        group = QGroupBox("Equipment Data (Sample Rows)")
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"
        ])
        
        # Style the table
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #e9ecef;
                border: none;
                border-radius: 8px;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f3f5;
            }
            QTableWidget::item:selected {
                background-color: #e7f3ff;
                color: #2F80ED;
            }
        """)
        
        # Stretch columns to fit
        header = self.table.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        
        layout.addWidget(self.table)
        group.setLayout(layout)
        return group
        
    def create_right_panel(self):
        """Create right panel with history and actions"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Action buttons group
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()
        
        self.download_button = QPushButton("📄 Download PDF Report")
        self.download_button.clicked.connect(self.download_report)
        self.download_button.setEnabled(False)
        self.download_button.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #f093fb, stop:1 #f5576c);
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #f5576c, stop:1 #d43f54);
            }
            QPushButton:disabled {
                background-color: #ced4da;
                color: #6c757d;
            }
        """)
        actions_layout.addWidget(self.download_button)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        # History section
        history_group = QGroupBox("Upload History (Last 5)")
        history_layout = QVBoxLayout()
        
        self.refresh_button = QPushButton("🔄 Refresh History")
        self.refresh_button.clicked.connect(self.load_history)
        self.refresh_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #4facfe, stop:1 #00f2fe);
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #00f2fe, stop:1 #4facfe);
            }
        """)
        history_layout.addWidget(self.refresh_button)
        
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f1f3f5;
                border-radius: 6px;
                margin: 2px;
            }
            QListWidget::item:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #ffecd2, stop:1 #fcb69f);
                border: none;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
            }
        """)
        self.history_list.itemClicked.connect(self.load_dataset_from_history)
        history_layout.addWidget(self.history_list)
        
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        layout.addStretch()
        
        return panel
        
    def show_login(self):
        """Show login dialog"""
        dialog = LoginDialog(self.api_client, self)
        if dialog.exec_() == QDialog.Accepted:
            self.statusBar().showMessage("✓ Logged in successfully")
            self.load_history()
        else:
            QMessageBox.warning(self, "Login Required", 
                              "You must login to use this application.")
            self.close()
            
    def upload_file(self):
        """Handle file upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)")
            
        if file_path:
            self.upload_button.setEnabled(False)
            self.upload_button.setText("⏳ Uploading...")
            self.statusBar().showMessage("Uploading file...")
            
            # Upload in background thread
            self.upload_thread = UploadThread(self.api_client, file_path)
            self.upload_thread.finished.connect(self.on_upload_success)
            self.upload_thread.error.connect(self.on_upload_error)
            self.upload_thread.start()
            
    def on_upload_success(self, dataset):
        """Handle successful upload"""
        self.upload_button.setEnabled(True)
        self.upload_button.setText("📁 Upload CSV")
        self.statusBar().showMessage("✓ Upload successful!", 5000)
        self.current_dataset = dataset
        self.update_dashboard(dataset)
        self.load_history()
        
        QMessageBox.information(self, "Success", 
                              f"CSV file uploaded successfully!\n\n"
                              f"Total records: {dataset.get('total_count', 0)}")
        
    def on_upload_error(self, error_msg):
        """Handle upload error"""
        self.upload_button.setEnabled(True)
        self.upload_button.setText("📁 Upload CSV")
        self.statusBar().showMessage("✗ Upload failed", 5000)
        QMessageBox.critical(self, "Upload Error", 
                           f"Failed to upload file:\n\n{error_msg}")
        
    def update_dashboard(self, dataset):
        """Update dashboard with dataset information"""
        # Update summary cards
        self.update_stat_card(self.total_label, dataset.get('total_count', 0))
        self.update_stat_card(self.avg_flow_label, f"{dataset.get('avg_flowrate', 0):.2f}")
        self.update_stat_card(self.avg_pressure_label, f"{dataset.get('avg_pressure', 0):.2f} bar")
        self.update_stat_card(self.avg_temp_label, f"{dataset.get('avg_temperature', 0):.2f}°C")
        
        # Update charts
        self.type_chart.update_chart(dataset.get('type_distribution', {}))
        self.flowrate_chart.update_chart(dataset.get('rows', []))
        
        # Update table
        rows = dataset.get('rows', [])
        self.table.setRowCount(len(rows))
        
        for i, row in enumerate(rows):
            # Equipment Name
            name_item = QTableWidgetItem(str(row.get('Equipment Name', '')))
            name_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, name_item)
            
            # Type
            type_item = QTableWidgetItem(str(row.get('Type', '')))
            type_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, type_item)
            
            # Flowrate
            flow_item = QTableWidgetItem(str(row.get('Flowrate', '')))
            flow_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 2, flow_item)
            
            # Pressure
            pressure_item = QTableWidgetItem(str(row.get('Pressure', '')))
            pressure_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 3, pressure_item)
            
            # Temperature
            temp_item = QTableWidgetItem(str(row.get('Temperature', '')))
            temp_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 4, temp_item)
        
        # Enable download button
        self.download_button.setEnabled(True)
        
    def load_history(self):
        """Load upload history"""
        try:
            history = self.api_client.get_history()
            self.history_list.clear()
            
            for dataset in history:
                # Format item text
                date_str = dataset['uploaded_at'][:16].replace('T', ' ')
                item_text = f"📊 Dataset #{dataset['id']}\n"
                item_text += f"📅 {date_str}\n"
                item_text += f"📈 Count: {dataset['total_count']}, "
                item_text += f"Flow: {dataset['avg_flowrate']:.2f}"
                
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, dataset)
                self.history_list.addItem(item)
                
            if len(history) > 0:
                self.statusBar().showMessage(f"✓ Loaded {len(history)} datasets from history", 3000)
            
        except Exception as e:
            self.statusBar().showMessage(f"✗ Failed to load history: {str(e)}", 5000)
            QMessageBox.warning(self, "History Error", 
                              f"Could not load history:\n{str(e)}")
            
    def load_dataset_from_history(self, item):
        """Load dataset from history"""
        dataset = item.data(Qt.UserRole)
        self.current_dataset = dataset
        self.update_dashboard(dataset)
        self.statusBar().showMessage(f"✓ Loaded dataset #{dataset['id']}", 3000)
        
    def download_report(self):
        """Download PDF report"""
        if not self.current_dataset:
            QMessageBox.warning(self, "No Dataset", 
                              "Please upload or select a dataset first.")
            return
            
        # Get save location from user
        default_filename = f"dataset_{self.current_dataset['id']}_report.pdf"
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", default_filename,
            "PDF Files (*.pdf);;All Files (*)")
            
        if save_path:
            try:
                self.statusBar().showMessage("Downloading report...")
                self.api_client.download_report(self.current_dataset['id'], save_path)
                self.statusBar().showMessage("✓ Report downloaded successfully!", 5000)
                
                # Show success message with option to open
                reply = QMessageBox.question(
                    self, "Success", 
                    f"Report downloaded successfully!\n\n{save_path}\n\nOpen file location?",
                    QMessageBox.Yes | QMessageBox.No)
                
                if reply == QMessageBox.Yes:
                    # Open file location based on OS
                    if platform.system() == 'Windows':
                        subprocess.Popen(f'explorer /select,"{save_path}"')
                    elif platform.system() == 'Darwin':  # macOS
                        subprocess.Popen(['open', '-R', save_path])
                    else:  # Linux
                        subprocess.Popen(['xdg-open', os.path.dirname(save_path)])
                        
            except Exception as e:
                self.statusBar().showMessage("✗ Download failed", 5000)
                QMessageBox.critical(self, "Download Error", 
                                   f"Failed to download report:\n\n{str(e)}")