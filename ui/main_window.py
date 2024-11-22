from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel


class ScanPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Scan Page Content"))
        self.setLayout(layout)


class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("History Page Content"))
        self.setLayout(layout)


class QuarantinePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Quarantine Page Content"))
        self.setLayout(layout)


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings Page Content"))
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Antivirus Program")
        self.setGeometry(100, 100, 800, 600)

        # Создание вкладок
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Добавляем вкладки
        self.tabs.addTab(ScanPage(), "Scan")
        self.tabs.addTab(HistoryPage(), "History")
        self.tabs.addTab(QuarantinePage(), "Quarantine")
        self.tabs.addTab(SettingsPage(), "Settings")
