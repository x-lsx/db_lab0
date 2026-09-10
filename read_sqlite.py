import sqlite3
import json
import os


class SQLiteReader:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def extract_data_to_json(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Файл базы данных не найден: {self.db_path}")
        
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        print("Чтение данных из базы данных.")
        cursor.execute("SELECT * FROM games_1nf")
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        connection.close()
        
        with open("games.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        
        print("Данные успешно извлечены и сохранены в games.json.")

if __name__ == "__main__":
    db_path = "games.db"
    reader = SQLiteReader(db_path)
    reader.extract_data_to_json()