import json
import subprocess
import os
import sys
import psycopg2
from psycopg2 import pool

class ReportExporter:
    def __init__(self, db_config: dict):
        try:
            self.db_pool = psycopg2.pool.SimpleConnectionPool(1, 5, **db_config)
            print("[INFO] Успешное подключение к базе данных.")
        except Exception as e:
            print(f"[ERROR] Не удалось подключиться к БД: {e}")
            sys.exit(1)

    def generate_developers_summary(self, output_excel: str = "Top_Studios_Report.xlsx"):
        connection = self.db_pool.getconn()
        try:
            with connection.cursor() as cursor:
                # SQL-запрос для аналитики по студиям
                query = """
                WITH RankedGames AS (
                    SELECT 
                        company_id, 
                        game_name, 
                        rating,
                        ROW_NUMBER() OVER(PARTITION BY company_id ORDER BY rating DESC) as rank
                    FROM games
                )
                SELECT 
                    c.company_name AS "Компания",
                    co.country_name AS "Страна",
                    COUNT(g.game_id) AS "Количество игр",
                    ROUND(AVG(g.rating), 1) AS "Средний рейтинг",
                    rg.game_name AS "Лучшая игра"
                FROM companies c
                JOIN countries co ON c.country_id = co.country_id
                LEFT JOIN games g ON c.company_id = g.company_id
                LEFT JOIN RankedGames rg ON c.company_id = rg.company_id AND rg.rank = 1
                GROUP BY c.company_name, co.country_name, rg.game_name
                ORDER BY "Средний рейтинг" DESC NULLS LAST;
                """
                
                print("[INFO] Выполнение запроса к БД...")
                cursor.execute(query)
                
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                
                if not rows:
                    print("[WARN] В базе данных нет записей для отчета.")
                    return
                
                # Формируем JSON-данные
                dataset = [dict(zip(columns, row)) for row in rows]
                
                temp_json = "temp_report.json"
                with open(temp_json, "w", encoding="utf-8") as f:
                    json.dump(dataset, f, ensure_ascii=False, default=str)
                
                print(f"[INFO] Данные подготовлены. Вызов генератора Excel...")
                
                # Запускаем второй скрипт как отдельное приложение
                subprocess.run([sys.executable, "excel_generator.py", temp_json, output_excel], check=True)
                
                print(f"[SUCCESS] Отчет успешно сохранен в файл: {output_excel}")
                
        except subprocess.CalledProcessError:
            print("[ERROR] Ошибка при работе внешнего генератора Excel.")
        except Exception as e:
            print(f"[ERROR] Ошибка выполнения: {e}")
            connection.rollback()
        finally:
            if os.path.exists("temp_report.json"):
                os.remove("temp_report.json")
            self.db_pool.putconn(connection)

    def close(self):
        if self.db_pool:
            self.db_pool.closeall()


# if __name__ == "__main__":
#     config = {
#         "dbname": "games_db",
#         "user": "artur",
#         "password": "artursubd",
#         "host": "localhost",
#         "port": "5432"
#     }
    
#     exporter = ReportExporter(config)
#     exporter.generate_developers_summary()
#     exporter.close()