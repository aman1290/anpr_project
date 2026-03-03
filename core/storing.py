import os
import json
import pymysql
from pymysql.cursors import DictCursor
from config import DB_CONFIG , JSON_DIR


# -------------------- JSON STORAGE --------------------
class JSONStorage:
    def __init__(self, json_dir):
        self.json_dir = json_dir
        os.makedirs(self.json_dir, exist_ok=True)

    def save(self, license_plates, start_time, end_time):
        if not license_plates:
            return

        data = {
            "start_time": str(start_time),
            "end_time": str(end_time),
            "license_plates": list(license_plates)
        }

        filename = f"{start_time.strftime('%Y%m%d_%H%M%S')}.json"
        file_path = os.path.join(self.json_dir, filename)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"[JSON] Saved {len(license_plates)} plates")


# -------------------- DATABASE STORAGE --------------------
class DatabaseStorage:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self._connect()

    def _connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.db_config["host"],
                user=self.db_config["user"],
                password=self.db_config["password"],
                database=self.db_config["database"],
                port=self.db_config.get("port", 3306),
                cursorclass=DictCursor,
                autocommit=False
            )
            print("[DB] Connected successfully")

        except pymysql.MySQLError as e:
            print(f"[DB ERROR] Connection failed: {e}")
            self.connection = None

    def save(self, license_plates, start_time, end_time):
        if not self.connection:
            print("[DB ERROR] No DB connection")
            return

        if not license_plates:
            return

        query = """
            INSERT INTO LicensePlates (start_time, end_time, license_plate)
            VALUES (%s, %s, %s)
        """

        try:
            with self.connection.cursor() as cursor:
                data = [
                    (start_time, end_time, plate)
                    for plate in license_plates
                ]
                cursor.executemany(query, data)

            self.connection.commit()
            print(f"[DB] Saved {len(data)} plates")

        except pymysql.MySQLError as e:
            print(f"[DB ERROR] Insert failed: {e}")
            self.connection.rollback()

    def close(self):
        if self.connection:
            self.connection.close()
            print("[DB] Connection closed")