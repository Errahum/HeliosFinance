from src.utils.logger import logger
from src.api.sqlite_financial_data_creator import FinancialDataCreator
from src.data_management.transform_extract import TransformExtractData

import json

with open('config.json', 'r') as file:
    config = json.load(file)

class ExecuteAnalyze:
    def __init__(self, filepath):
        self.df = filepath
        self.config = config
        self.financial_data_creator = FinancialDataCreator(self.config)
        self.transform_extract = TransformExtractData(filepath, output='data/extract_transform')


    def create_data(self):
        self.financial_data_creator.update_database("1h", merge_bool=False)
        self.financial_data_creator.update_database("1d", merge_bool=False)
        self.financial_data_creator.update_database("1m", merge_bool=False)

    def execute_all(self):
        while True:
            logger.info("\nChoose an action:")
            logger.info("1. Create/Update database")
            logger.info("2. Extract/Transform database")

            logger.info("4. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.create_data()
            elif choice == '2':
                self.transform_extract.transform_data(self.transform_extract.extract_data())
            elif choice == '4':
                logger.info("Exiting the program.")
                break
            else:
                logger.warning("Invalid choice. Please enter 1, 2, 3 or 4.")

filepath = 'data/db/financial_data.db'
app = ExecuteAnalyze(filepath)
app.execute_all()
