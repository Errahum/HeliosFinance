import numpy as np
import pandas as pd
import os
from src.utils.logger import logger

class DataProcessing:
    def __init__(self, input, output):
        self.input = input
        self.output = output

    def merge_df(self):
        """
        read all the .csv files in the input directory
        put a new column in the dataframe: Name that is the name of the file with a split on the '_1...'
        use pd.concat to merge the dataframes
        save the merged dataframe as a new .csv file
        """
        all_files = [f for f in os.listdir(self.input) if f.endswith('.csv')]
        df_list = []
        
        for file in all_files:
            df = pd.read_csv(os.path.join(self.input, file))
            df['Name'] = file.split('_1')[0]
            df.drop(columns=['Unnamed: 0'], inplace=True)
            df_list.append(df)
        
        merged_df = pd.concat(df_list, ignore_index=True)
        merged_df.to_csv(os.path.join(self.output, 'merged_df.csv'), index=False)
        logger.info(merged_df.head())


    def log_return_df(self, df):
        # take the df from merge_df that is clean and replace the values with the log return
        # Then save it as a new .csv file
        log_return_df = np.log(df).diff()
        log_return_df.to_csv(os.path.join(self.input, 'log_return_df.csv'), index=False)
