from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from core.database import Database

class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.history_label = QLabel("Scan History")
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Start Time", "End Time", "Total Files", "Threats Found"])

        layout.addWidget(self.history_label)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.db = Database()
        self.load_history()

    def load_history(self):
        scan_history = self.db.get_scan_history()
        self.table.setRowCount(len(scan_history))

        for row_idx, row_data in enumerate(scan_history):
            for col_idx, data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
