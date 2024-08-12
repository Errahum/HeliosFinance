import sqlite3
import pandas as pd
from src.utils.logger import logger
import os

class TransformExtractData:
    def __init__(self, db_file, output):
        self.data = {}
        self.conn = sqlite3.connect(db_file)
        self.output = output

    def list_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql_query(query, self.conn)
        return tables['name'].tolist()

    def extract_data(self, suffix="1d"):
        try:
            all_tables = self.list_tables()
            select_tables = [table for table in all_tables if table.endswith(suffix)]

            for table in select_tables:
                query = f'SELECT * FROM "{table}"'
                self.data[table] = pd.read_sql_query(query, self.conn)

            return self.data

        except Exception as e:
            logger.error(f"Error {e}")

        finally:
            self.conn.close()

    def transform_data(self, extract_data):
        if not os.path.exists(self.output):
            os.makedirs(self.output)

        for table, df in extract_data.items():
            csv_path = os.path.join(self.output, f"{table}.csv")
            df.to_csv(csv_path)
            print(f"Data from table '{table}' saved to {csv_path}")
            