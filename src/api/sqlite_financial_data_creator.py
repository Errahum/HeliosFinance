import yfinance as yf
import os
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from src.utils.logger import logger

class FinancialDataCreator:
    def __init__(self, config):
        self.df = None
        self.config = config
        self.symbols = config.get('symbols', [])
        self.data_raw_data = 'data/db'
        self.sql_db_path = f'{self.data_raw_data}/financial_data.db'  
        self.end_date = datetime.today()
        self.start_date = self.end_date - timedelta(days=729) # Default
        self.date_name = 'Datetime' # default

        # Connection to SQLite database
        os.makedirs(self.data_raw_data, exist_ok=True)
        self.connect_sql = sqlite3.connect(self.sql_db_path)

    def __del__(self):
        self.connect_sql.close()

    def interval_day(self, interval):
        self.interval = interval
        if self.interval == "1h":
            self.date_name = 'Datetime'
            self.end_date = datetime.today()
            self.start_date = self.end_date - timedelta(days=729)
        elif self.interval == "1d":
            self.date_name = 'Date'
            self.end_date = datetime.today()
            self.start_date = "2010-01-01"
        elif self.interval == "1mo":
            self.date_name = 'Date'
            self.end_date = datetime.today()
            self.start_date = "2005-01-01"
        elif self.interval == "1m":
            self.date_name = 'Datetime'
            self.end_date = datetime.today()
            self.start_date = self.end_date - timedelta(days=6)

    def download_data(self, interval):
        self.interval_day(interval)
        for symbol in self.symbols:
            table_name = f"{symbol}_{self.interval}"
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
            table_exists = pd.read_sql(query, self.connect_sql)

            data = yf.download(symbol, start=self.start_date, end=self.end_date, interval=self.interval)

            if not table_exists.empty:
                existing_data = pd.read_sql(f'SELECT * FROM "{table_name}"', self.connect_sql, index_col=self.date_name)
                existing_data.index = existing_data.index.astype(str)
                data = data.combine_first(existing_data)

            if not data.empty:
                data.index = data.index.astype(str)
                data.to_sql(table_name, self.connect_sql, if_exists='replace', index=True)
            else:
                logger.info(f"No data for {symbol} at interval {self.interval}, skip...")

    def create_merged_table(self, interval):
        # sql command, selection of name of the table
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql(query, self.connect_sql)
        # All of the symbol table
        symbol_tables = [table for table in tables['name'] if f'_{interval}' in table and not table.startswith('merged_data_')]

        # create a empty pandas database
        merged_df = pd.DataFrame()

        for symbol in symbol_tables:
            # Extract 'Close' and 'Date'
            df = pd.read_sql(f'SELECT {self.date_name}, Close FROM "{symbol}"', self.connect_sql)
            df.set_index(f'{self.date_name}', inplace=True)

            # Rename Close with the symbol name
            symbol_name = symbol.replace(f'_{interval}', '')
            df.rename(columns={'Close': symbol_name}, inplace=True)

            # Merge dataframe
            if merged_df.empty:
                merged_df = df
            else:
                merged_df = merged_df.join(df, how='outer')

        # save
        merged_df.to_sql(f'merged_data_{interval}', self.connect_sql, if_exists='replace', index=True)
        logger.info(f"Table 'merged_data_{interval}' created/updated.")


    def update_database(self, interval, merge_bool):
        self.download_data(interval)
        if merge_bool:
            self.create_merged_table(interval)
        logger.info(f"Database updated at {self.sql_db_path} for interval {self.interval}.")
