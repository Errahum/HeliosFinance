from src.utils.logger import logger
from src import FinancialDataCreator, TransformExtractData, DataProcessing

import json

with open('config.json', 'r') as file:
    config = json.load(file)

class ExecuteAnalyze:
    def __init__(self, filepath):
        self.df = filepath
        self.config = config
        self.extract_transform='data/extract_transform'
        self.processed='data/processed'

        self.financial_data_creator = FinancialDataCreator(self.config)
        self.transform_extract = TransformExtractData(filepath, self.extract_transform)
        self.DataProcessing = DataProcessing(self.extract_transform, self.processed)


    def create_data(self):
        self.financial_data_creator.update_database("1h", merge_bool=False)
        self.financial_data_creator.update_database("1d", merge_bool=False)
        self.financial_data_creator.update_database("1m", merge_bool=False)

    def execute_all(self):
        while True:
            print("\nChoose an action:")
            print("1. Create/Update database")
            print("2. Extract/Transform database")
            print("3. Data Processing merge_df")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.create_data()
            elif choice == '2':
                suffix_input = input("Enter the suffix, exemple: 1h, 1d, 1m\n").strip().lower()
                suffixes = {'1h': '1h', '1m': '1m', '1d': '1d'}
                if suffix_input in suffixes:
                    self.transform_extract.transform_data(self.transform_extract.extract_data(suffix=suffixes[suffix_input]))
            elif choice == '3':
                self.DataProcessing.merge_df()
            elif choice == '4':
                logger.info("Exiting the program.")
                break
            else:
                logger.warning("Invalid choice. Please enter 1, 2, 3 or 4.")

filepath = 'data/db/financial_data.db'
app = ExecuteAnalyze(filepath)
app.execute_all()
