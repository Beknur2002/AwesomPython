from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
import requests
import time  

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

        # Analyze button
        self.analyze_button = QPushButton("Analyze File on VirusTotal")
        self.analyze_button.clicked.connect(self.analyze_file_on_virustotal)
        self.analyze_button.setEnabled(False)  # Делаем кнопку неактивной, пока файл не загружен

        # Result labels
        self.folder_result_label = QLabel("")
        self.file_result_label = QLabel("")
        self.analysis_result_label = QLabel("")

        # Add widgets to layout
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_button)
        layout.addWidget(self.start_scan_button)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.folder_result_label)
        layout.addWidget(self.file_result_label)
        layout.addWidget(self.analysis_result_label)

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
                "x-apikey": "8da69ff389ad791ebe9e588cff3258bdccc36a085cd4c225e2c177f534133f42",
            }
            files = {
                "file": open(self.file_to_upload, "rb")
            }
            try:
                response = requests.post(url, headers=headers, files=files)
                if response.status_code == 200:
                    result = response.json()
                    scan_id = result.get('data', {}).get('id', 'N/A')
                    self.file_result_label.setText(f"Upload successful! Scan ID: {scan_id}")
                    self.analysis_id = scan_id  # Сохраняем ID анализа
                    self.analyze_button.setEnabled(True)  # Активируем кнопку анализа
                else:
                    self.file_result_label.setText(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                self.file_result_label.setText(f"Error: {str(e)}")
        else:
            self.file_result_label.setText("No file selected.")

    def analyze_file_on_virustotal(self):
        if hasattr(self, 'analysis_id'):
            url = f"https://www.virustotal.com/api/v3/analyses/{self.analysis_id}"
            headers = {
                "accept": "application/json",
                "x-apikey": "8da69ff389ad791ebe9e588cff3258bdccc36a085cd4c225e2c177f534133f42",
            }
            try:
                while True:  # Проверяем статус анализа
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        result = response.json()
                        status = result.get("data", {}).get("attributes", {}).get("status")
                        if status == "completed":
                            stats = result.get("data", {}).get("attributes", {}).get("stats", {})
                            harmless = stats.get("harmless", 0)
                            malicious = stats.get("malicious", 0)
                            suspicious = stats.get("suspicious", 0)
                            undetected = stats.get("undetected", 0)
                            self.analysis_result_label.setText(
                                f"Analysis Completed:\n"
                                f"Harmless: {harmless}\n"
                                f"Malicious: {malicious}\n"
                                f"Suspicious: {suspicious}\n"
                                f"Undetected: {undetected}"
                            )
                            break
                        elif status == "queued":
                            self.analysis_result_label.setText("Analysis in progress. Please wait...")
                            time.sleep(5)
                        else:
                            self.analysis_result_label.setText(f"Analysis status: {status}")
                            break
                    else:
                        self.analysis_result_label.setText(f"Error: {response.status_code} - {response.text}")
                        break
            except Exception as e:
                self.analysis_result_label.setText(f"Error: {str(e)}")
        else:
            self.analysis_result_label.setText("No analysis ID available.")
