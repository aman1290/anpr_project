import sqlite3

class DatabaseStorage:
    def __init__(self, db_path):
        self.db_path = db_path

    def save(self, license_plates, start_time, end_time):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for plate in license_plates:
            cursor.execute("""
                INSERT INTO LicensePlates(start_time, end_time, license_plate)
                VALUES (?, ?, ?)
            """, (start_time.isoformat(), end_time.isoformat(), plate))

        conn.commit()
        conn.close()
