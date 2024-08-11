from src.utils.logger import logger
from src.api.sqlite_financial_data_creator import FinancialDataCreator

import json

with open('config.json', 'r') as file:
    config = json.load(file)

class ExecuteAnalyze:
    def __init__(self, filepath):
        self.df = filepath
        self.config = config
        self.financial_data_creator = FinancialDataCreator(self.config)

    def execute_all(self):
        self.financial_data_creator.update_database("1h", merge_bool=False)
        self.financial_data_creator.update_database("1d", merge_bool=False)
        self.financial_data_creator.update_database("1m", merge_bool=False)


filepath = 'data/db/financial_data.db'
app = ExecuteAnalyze(filepath)
app.execute_all()
