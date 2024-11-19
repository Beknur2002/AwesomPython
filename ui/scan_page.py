from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
import requests

class ScanPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Folder selection widgets
        self.folder_label = QLabel("Select a folder to scan:")
        self.folder_button = QPushButton("Browse Folder")
        self.folder_button.clicked.connect(self.browse_folder)

        # File selection widgets
        self.file_label = QLabel("Select a file to upload to VirusTotal:")
        self.file_button = QPushButton("Browse File")
        self.file_button.clicked.connect(self.browse_file)

        # Start scan button
        self.start_scan_button = QPushButton("Start Scan")
        self.start_scan_button.clicked.connect(self.start_scan)

        # Upload button
        self.upload_button = QPushButton("Upload File to VirusTotal")
        self.upload_button.clicked.connect(self.upload_file_to_virustotal)

        # Result labels
        self.folder_result_label = QLabel("")
        self.file_result_label = QLabel("")

        # Add widgets to layout
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_button)
        layout.addWidget(self.start_scan_button)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.folder_result_label)
        layout.addWidget(self.file_result_label)

        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_label.setText(f"Selected folder: {folder}")
            self.folder_to_scan = folder

    def browse_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file:
            self.file_label.setText(f"Selected file: {file}")
            self.file_to_upload = file

    def start_scan(self):
        if hasattr(self, 'folder_to_scan'):
            # Replace with your folder scanning logic
            self.folder_result_label.setText(f"Scanned folder: {self.folder_to_scan}")
        else:
            self.folder_result_label.setText("No folder selected.")

    def upload_file_to_virustotal(self):
        if hasattr(self, 'file_to_upload'):
            url = "https://www.virustotal.com/api/v3/files"
            headers = {
                "accept": "application/json",
                # Add your API key here
                "x-apikey": "YOUR_API_KEY",
            }
            files = {
                "file": open(self.file_to_upload, "rb")
            }
            try:
                response = requests.post(url, headers=headers, files=files)
                if response.status_code == 200:
                    result = response.json()
                    self.file_result_label.setText(f"Upload successful! Scan ID: {result.get('data', {}).get('id', 'N/A')}")
                else:
                    self.file_result_label.setText(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                self.file_result_label.setText(f"Error: {str(e)}")
        else:
            self.file_result_label.setText("No file selected.")
