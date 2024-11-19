from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from core.database import Database

class QuarantinePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.quarantine_label = QLabel("Quarantine Files")
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "File Path", "Date Quarantined"])

        self.restore_button = QPushButton("Restore File")
        self.delete_button = QPushButton("Delete File")

        layout.addWidget(self.quarantine_label)
        layout.addWidget(self.table)
        layout.addWidget(self.restore_button)
        layout.addWidget(self.delete_button)
        self.setLayout(layout)

        self.db = Database()
        self.load_quarantine_files()

        self.restore_button.clicked.connect(self.restore_file)
        self.delete_button.clicked.connect(self.delete_file)

    def load_quarantine_files(self):
        quarantine_files = self.db.get_quarantine_files()
        self.table.setRowCount(len(quarantine_files))

        for row_idx, row_data in enumerate(quarantine_files):
            for col_idx, data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def restore_file(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            file_id = self.table.item(selected_row, 0).text()
            self.db.restore_file_from_quarantine(file_id)
            self.load_quarantine_files()

    def delete_file(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            file_id = self.table.item(selected_row, 0).text()
            self.db.delete_quarantine_file(file_id)
            self.load_quarantine_files()
