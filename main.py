import read_sqlite as rs
import pg_loader as pl
import excel_report as er
import subprocess
import os
from dotenv import load_dotenv
load_dotenv()

def main():
    
    db_config = {
        "dbname": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("POSTGRES_PORT")
    }
    sqlite_db = "games.db"
    
    reader = rs.SQLiteReader(sqlite_db)
    reader.extract_data_to_json()
    
    
    loader = pl.PostgreSQLLoader("games.json", db_config)
    loader.init_db()
    loader.load_data()

    exporter = er.ReportExporter(db_config)
    report_json = exporter.generate_developers_summary()
    exporter.close()
    
    output_excel = "top_studios.xlsx"
    subprocess.run(["go_service/excel_generator.exe", report_json, output_excel], check=True)
    
    

if __name__ == "__main__":
    main()
