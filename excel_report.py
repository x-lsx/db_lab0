import json

import sys
import psycopg2

class ReportExporter:
    def __init__(self, db_config: dict):
        try:
            self.db_pool = psycopg2.pool.SimpleConnectionPool(1, 5, **db_config)

        except Exception as e:
            sys.exit(1)

    def generate_developers_summary(self):
        connection = self.db_pool.getconn()
        try:
            with connection.cursor() as cursor:
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
            
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()

                if not rows:
                    print("В базе данных нет записей для отчета.")
                    return
                
                dataset = [dict(zip(columns, row)) for row in rows]
                
                report_json = "report.json"
                with open(report_json, "w", encoding="utf-8") as f:
                    json.dump(dataset, f, ensure_ascii=False, default=str)
                
                print(f"Данные для отчёта сохранены в report.json.")
                
                return report_json
        
        except Exception as e:
            print(f"Oшибка выполнения: {e}")
            connection.rollback()
        finally:
            self.db_pool.putconn(connection)

    def close(self):
        if self.db_pool:
            self.db_pool.closeall()
