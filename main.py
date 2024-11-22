from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
)
import sqlite3
import requests
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Константы
VT_API_KEY = "8da69ff389ad791ebe9e588cff3258bdccc36a085cd4c225e2c177f534133f42"
DATABASE = "virus_signatures.db"
VT_URL = "https://www.virustotal.com/api/v3/files"


# Инициализация базы данных
def initialize_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash TEXT UNIQUE,
            virus_name TEXT
        )
    """)
    connection.commit()
    connection.close()


# Функция для добавления сигнатур в базу данных
def add_signature_to_db(hash_value, virus_name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO signatures (hash, virus_name) VALUES (?, ?)", (hash_value, virus_name))
        connection.commit()
        print(f"Добавлено в базу: {hash_value}, {virus_name}")  # Отладка
    except sqlite3.IntegrityError:
        print(f"Дубликат записи: {hash_value}")  # Отладка
    finally:
        connection.close()



# Функция для получения сигнатур из базы данных
def get_signatures_from_db():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT hash, virus_name FROM signatures")
    results = cursor.fetchall()
    print(f"Сигнатуры из базы: {results}")  # Отладка
    connection.close()
    return results



# Функция для запроса к VirusTotal API
def fetch_signatures_from_virustotal(file_path):
    logging.info(f"Начинаю загрузку файла: {file_path}")
    headers = {"x-apikey": VT_API_KEY}
    files = {"file": open(file_path, "rb")}

    try:
        # Отправка запроса к API
        logging.debug("Отправка запроса к VirusTotal API...")
        response = requests.post(VT_URL, headers=headers, files=files)

        # Обработка ответа от API
        if response.status_code == 200:
            logging.debug("Ответ от API получен успешно.")
            result = response.json()
            hash_value = result.get("data", {}).get("id", None)
            virus_name = result.get("data", {}).get("attributes", {}).get("meaningful_name", "Unknown")

            # Если хеш найден, сохраняем его в базу
            if hash_value:
                logging.info(f"Сигнатура найдена: {virus_name}, хеш: {hash_value}")
                add_signature_to_db(hash_value, virus_name)
                logging.info(f"Сигнатура добавлена в базу данных: {virus_name} ({hash_value})")
                return f"Сигнатура добавлена: {virus_name} ({hash_value})"
            else:
                logging.warning("Ошибка: не удалось получить данные о сигнатуре.")
                return f"Ошибка: невозможно получить данные о сигнатуре."
        else:
            # Ошибка API
            logging.error(f"Ошибка API: {response.status_code} {response.text}")
            return f"Ошибка API: {response.status_code} {response.text}"
    except Exception as e:
        # Ошибка соединения
        logging.exception(f"Ошибка при соединении с сервером: {str(e)}")
        return f"Ошибка соединения: {str(e)}"
    finally:
        # Закрываем файл
        files["file"].close()
        logging.debug("Файл закрыт.")

# Вкладка Scan
class ScanPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.upload_file_button = QPushButton("Загрузить файл")
        self.upload_file_button.clicked.connect(self.upload_file_action)

        layout.addWidget(QLabel("Scan Page Content"))
        layout.addWidget(self.upload_file_button)
        self.setLayout(layout)

    def upload_file_action(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл для анализа")
        if file_path:
            result = fetch_signatures_from_virustotal(file_path)
            QMessageBox.information(self, "Результат", result)


# Вкладка History
class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("History Page Content"))
        self.setLayout(layout)


# Вкладка Quarantine
class QuarantinePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Quarantine Page Content"))
        self.setLayout(layout)


# Вкладка Settings
class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings Page Content"))
        self.setLayout(layout)


# Вкладка Signatures
class SignaturesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Hash", "Virus Name"])
        self.load_signatures()

        layout.addWidget(QLabel("Signatures"))
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_signatures(self):
        signatures = get_signatures_from_db()
        if not signatures:
            print("Таблица сигнатур пуста!")  # Отладка
        self.table.setRowCount(len(signatures))
        for row, (hash_value, virus_name) in enumerate(signatures):
            self.table.setItem(row, 0, QTableWidgetItem(hash_value))
            self.table.setItem(row, 1, QTableWidgetItem(virus_name))
        print(f"Таблица обновлена: {len(signatures)} записей")  # Отладка



# Основное окно
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
        self.tabs.addTab(SignaturesPage(), "Signatures")


# Основной запуск приложения
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    initialize_database()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
