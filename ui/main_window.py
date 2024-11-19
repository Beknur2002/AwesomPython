from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout
from ui.scan_page import ScanPage
from ui.history_page import HistoryPage
from ui.quarantine_page import QuarantinePage
from ui.settings_page import SettingsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Antivirus Program")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Добавляем вкладки
        self.tabs.addTab(ScanPage(), "Scan")
        self.tabs.addTab(HistoryPage(), "History")
        self.tabs.addTab(QuarantinePage(), "Quarantine")
        self.tabs.addTab(SettingsPage(), "Settings")
