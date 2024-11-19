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

    def get_virus_signatures(self):
        self.cursor.execute("SELECT signature, name, threat_level FROM virus_signatures")
        return self.cursor.fetchall()

    def add_virus_signature(self, name, signature, threat_level):
        self.cursor.execute("INSERT INTO virus_signatures (name, signature, threat_level, date_added) VALUES (?, ?, ?, ?)",
                            (name, signature, threat_level, datetime.now()))
        self.conn.commit()

    def get_scan_history(self):
        self.cursor.execute("SELECT id, start_time, end_time, total_files_scanned, threats_found FROM scan_history")
        return self.cursor.fetchall()

    def get_quarantine_files(self):
        self.cursor.execute("SELECT id, file_path, date_quarantined FROM quarantine")
        return self.cursor.fetchall()

    def restore_file_from_quarantine(self, file_id):
        self.cursor.execute("DELETE FROM quarantine WHERE id = ?", (file_id,))
        self.conn.commit()

    def delete_quarantine_file(self, file_id):
        self.cursor.execute("DELETE FROM quarantine WHERE id = ?", (file_id,))
        self.conn.commit()

