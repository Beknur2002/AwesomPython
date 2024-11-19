import hashlib
import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('antivirus.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS virus_signatures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                signature TEXT,
                threat_level INTEGER,
                date_added TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_virus_signature(self, name, signature, threat_level):
        self.cursor.execute(
            "INSERT INTO virus_signatures (name, signature, threat_level, date_added) VALUES (?, ?, ?, ?)",
            (name, signature, threat_level, datetime.now())
        )
        self.conn.commit()

    def get_virus_signatures(self):
        self.cursor.execute("SELECT signature, name, threat_level FROM virus_signatures")
        return self.cursor.fetchall()

    def import_signatures_from_cav(self, file_path):
        """Import virus signatures from a CAV file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    # Assuming the format is: name:signature:threat_level
                    parts = line.strip().split(':')
                    if len(parts) == 3:
                        name, signature, threat_level = parts
                        self.add_virus_signature(name, signature, int(threat_level))
                    else:
                        print(f"Invalid line format: {line.strip()}")
            print("Signatures imported successfully.")
        except Exception as e:
            print(f"Error importing signatures: {e}")

    def check_file_signature(self, file_path):
        """Check the file against the stored virus signatures."""
        # Read the file and generate its signature
        file_signature = self.generate_file_signature(file_path)
        if not file_signature:
            print("Failed to generate signature for the file.")
            return

        # Compare with stored signatures in the database
        self.cursor.execute("SELECT name, threat_level FROM virus_signatures WHERE signature = ?", (file_signature,))
        results = self.cursor.fetchall()

        if results:
            print(f"Threat found in file '{file_path}':")
            for name, threat_level in results:
                print(f" - {name} (Threat Level: {threat_level})")
        else:
            print(f"No threats found in file '{file_path}'.")

    def generate_file_signature(self, file_path):
        """Generate a hash signature for the file using SHA256."""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def check_files_from_txt(self, txt_file_path):
        """Check virus signatures for a list of files provided in a text file."""
        try:
            with open(txt_file_path, 'r') as file:
                for line in file:
                    file_to_scan = line.strip()
                    if file_to_scan:  # Ensure it's not an empty line
                        print(f"Scanning '{file_to_scan}'...")
                        self.check_file_signature(file_to_scan)
        except Exception as e:
            print(f"Error reading file list: {e}")

# Example usage
db = Database()

# Import signatures from a CAV file (example)
db.import_signatures_from_cav('bases.cav')

# Option 1: Check a single file from console
while True:
    file_to_scan = input("Enter the path of the file to scan (or type 'exit' to quit): ")
    if file_to_scan.lower() == 'exit':
        break
    db.check_file_signature(file_to_scan)

# Option 2: Check files from a text file
db.check_files_from_txt('files_to_scan.txt')  # Ensure this file exists with paths
