import pandas as pd

def impute_df(df):
    df.dropna(axis=0, how='all', inplace=True)
    df.ffill(inplace=True)
    df.bfill(inplace=True)
    return df

def delete_duplicates(df):
    df.drop_duplicates(inplace=True)
    return df