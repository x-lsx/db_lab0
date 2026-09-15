import json
import psycopg2
from psycopg2 import pool
from datetime import datetime


class PostgreSQLLoader:
    def __init__(self, file_path: str, db_config: dict):
        self.file_path = file_path
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 10, **db_config)
        except Exception as e:
            print(f"Ошибка: {e}")

    def init_db(self):
        connection = self.connection_pool.getconn()
        cursor = connection.cursor()
        try:
            with open('init_schema.sql', 'r', encoding='utf-8') as f:
                sql_script = f.read()
                cursor.execute(sql_script)
                connection.commit()

        except Exception as e:
            print(f"Ошибка: {e}")
            connection.rollback()
        finally:
            cursor.close()
            self.connection_pool.putconn(connection)

    def format_date(self, date_str: str) -> str:
            if not date_str:
                return None
            try:
                date_obj = datetime.strptime(date_str, "%d.%m.%Y")
                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                return None

    def load_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        connection = self.connection_pool.getconn()
        try:
            with connection.cursor() as cursor:
                countries = set()
                companies = set()
                genres = set()
                games = set()
                platforms = set()
                game_platforms = set()
                developers = set()
                game_developers = set()
                ceremonies = set()
                game_ceremonies = set()
                game_modes = set()
                modes_in_game = set()
                languages = set()
                game_languages = set()

                for row in data:
                    if row['country_id']:
                        countries.add((row['country_id'], row['country_name']))
                    if row['company_id']:
                        companies.add(
                            (row['company_id'], row['company_name'], row['company_foundation'], row['country_id']))
                    if row['genre_id']:
                        genres.add((row['genre_id'], row['genre_name']))
                    if row['game_id']:
                        games.add((row['game_id'], row['game_name'], self.format_date(
                            row['release_date']), row["rating"], row['genre_id'], row['company_id']))
                    if row['platform_id']:
                        platforms.add(
                            (row['platform_id'], row['platform_name'], row['platform_description']))
                        if row['game_id']:
                            game_platforms.add(
                                (row['game_id'], row['platform_id']))
                    if row['main_developer_id']:
                        developers.add((row['main_developer_id'], row['main_developer_name'],
                                       row['main_developer_surname'], self.format_date(row['main_developer_date_birth'])))
                        if row['game_id']:
                            game_developers.add(
                                (row['game_id'], row['main_developer_id']))
                    if row['ceremony_id']:
                        ceremonies.add(
                            (row['ceremony_id'], row['ceremony_name'], row['ceremony_foundation']))
                        if row['game_id']:
                            game_ceremonies.add(
                                (row['ceremony_id'], row['game_id'], row['ceremony_year']))
                    if row['game_mode_id']:
                        game_modes.add(
                            (row['game_mode_id'], row['game_mode_name']))
                        if row['game_id']:
                            modes_in_game.add(
                                (row['game_id'], row['game_mode_id']))
                    if row['language_interface_id']:
                        languages.add(
                            (row['language_interface_id'], row['language_interface_name']))
                        if row['game_id']:
                            game_languages.add(
                                (row['game_id'], row['language_interface_id']))
                cursor.executemany(
                    "INSERT INTO countries (country_id, country_name) VALUES (%s, %s) ON CONFLICT (country_id) DO NOTHING", list(countries))
                cursor.executemany(
                    "INSERT INTO companies (company_id, company_name, company_foundation, country_id) VALUES (%s, %s, %s, %s) ON CONFLICT (company_id) DO NOTHING", list(companies))
                cursor.executemany(
                    "INSERT INTO genres (genre_id, genre_name) VALUES (%s, %s) ON CONFLICT (genre_id) DO NOTHING", list(genres))
                cursor.executemany(
                    "INSERT INTO games (game_id, game_name, release_date, rating, genre_id, company_id) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (game_id) DO NOTHING", list(games))
                cursor.executemany(
                    "INSERT INTO platforms (platform_id, platform_name, platform_description) VALUES (%s, %s, %s) ON CONFLICT (platform_id) DO NOTHING", list(platforms))
                cursor.executemany(
                    "INSERT INTO game_platforms (game_id, platform_id) VALUES (%s, %s) ON CONFLICT (game_id, platform_id) DO NOTHING", list(game_platforms))
                cursor.executemany(
                    "INSERT INTO main_developers (main_developers_id, main_developers_name, main_developers_surname, main_developers_date_birth) VALUES (%s, %s, %s, %s) ON CONFLICT (main_developers_id) DO NOTHING", list(developers))
                cursor.executemany(
                    "INSERT INTO game_developers (game_id, main_developers_id) VALUES (%s, %s) ON CONFLICT (game_id, main_developers_id) DO NOTHING", list(game_developers))
                cursor.executemany(
                    "INSERT INTO ceremonies (ceremony_id, ceremony_name, ceremony_foundation) VALUES (%s, %s, %s) ON CONFLICT (ceremony_id) DO NOTHING", list(ceremonies))
                cursor.executemany(
                    "INSERT INTO game_ceremonies (ceremony_id, game_id, ceremony_year) VALUES (%s, %s, %s) ON CONFLICT (ceremony_id, game_id) DO NOTHING", list(game_ceremonies))
                cursor.executemany(
                    "INSERT INTO game_modes (game_mode_id, game_mode_name) VALUES (%s, %s) ON CONFLICT (game_mode_id) DO NOTHING", list(game_modes))
                cursor.executemany(
                    "INSERT INTO modes_in_game (game_id, game_mode_id) VALUES (%s, %s) ON CONFLICT (game_id, game_mode_id) DO NOTHING", list(modes_in_game))
                cursor.executemany(
                    "INSERT INTO languages (language_interface_id, language_interface_name) VALUES (%s, %s) ON CONFLICT (language_interface_id) DO NOTHING", list(languages))
                cursor.executemany(
                    "INSERT INTO game_languages (game_id, language_interface_id) VALUES (%s, %s) ON CONFLICT (game_id, language_interface_id) DO NOTHING", list(game_languages))
                connection.commit()
                print("Данные успешно загружены в базу данных PostgreSQL.")
        except Exception as e:
            print(f"Ошибка: {e}")
            connection.rollback()
        

# if __name__ == "__main__":
#     db_config = {
#         "dbname": "games_db",
#         "user": "artur",
#         "password": "artursubd",
#         "host": "localhost",
#         "port": "5432"
#     }

#     loader = PostgreSQLLoader("games.json", db_config)

#     loader.init_db()

#     loader.load_data()
