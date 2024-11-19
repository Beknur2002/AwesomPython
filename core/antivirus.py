import os
import hashlib
from core.database import Database

class Antivirus:
    def __init__(self):
        self.db = Database()

    def scan_folder(self, folder_path):
        virus_signatures = self.db.get_virus_signatures()
        total_files = 0
        threats_found = 0

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                total_files += 1
                if self.scan_file(file_path, virus_signatures):
                    threats_found += 1

        return f"Scanned {total_files} files. Threats found: {threats_found}"

    def scan_file(self, file_path, virus_signatures):
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
                file_hash = hashlib.md5(file_data).hexdigest()

                for signature, name, _ in virus_signatures:
                    if file_hash == signature:
                        return True
        except Exception as e:
            print(f"Error scanning file {file_path}: {e}")
        return False
