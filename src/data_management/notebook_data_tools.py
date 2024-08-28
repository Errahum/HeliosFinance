import pandas as pd
import numpy as np

def impute_df(df):
    df.dropna(axis=0, how='all', inplace=True)
    df.ffill(inplace=True)
    df.bfill(inplace=True)
    return df

def delete_duplicates(df):
    df.drop_duplicates(inplace=True)
    df[~df.index.duplicated(keep='first')]
    return df

def log_return_df(df):
    return np.log(df).diff()

def drop_negative_values(df):
    return df[df['Close'] >= 0]