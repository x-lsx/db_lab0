import read_sqlite as rs
import pg_loader as pl
import excel_report as er
def main():
    db_config = {
        "dbname": "games_db",
        "user": "artur",
        "password": "artursubd",
        "host": "localhost",
        "port": "5432"
    }
    db_path = "games.db"
    
    reader = rs.SQLiteReader(db_path)
    reader.extract_data_to_json()
    
    
    loader = pl.PostgreSQLLoader("games.json", db_config)
    loader.init_db()
    loader.load_data()

    exporter = er.ReportExporter(db_config)
    exporter.generate_developers_summary()
    exporter.close()
    

if __name__ == "__main__":
    main()
