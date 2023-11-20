import re
import pandas as pd
from datetime import datetime

def train_test_split(df):
    '''
    Split dataframe into train/test sets where train contains 2020 data and test contains 2021 data

    Parameters:
    df: dataframe containg 2020 - 2021 stock market data

    Returns:
    train_df: dataframe containing 2020 stock market data
    test_df: dataframe containg 2021 stock market data
    '''
    date_2021 = datetime.strptime('2020-12-31', "%Y-%m-%d")
    df['Date'] = pd.to_datetime(df['Date'])
    test_df = df[df['Date'] > date_2021]
    train_df = df[df['Date'] <= date_2021]

    return train_df, test_df

def vol_change(str):
    '''
    Changes string quantifiers into numeric form.

    Parameters: 
    str: string containing volume data

    Returns:
    float: float containing volume data
    '''
    if "M" in str:
        return float(re.sub('M', "", str)) * 1000000
    elif "K" in str:
        return float(re.sub("K", "", str)) * 1000
    
    
def prep_weekly_monthly(df):
    '''
    Given daily stock market data, convert and return weekly, monthly version of data. 

    Parameters:
    df: dataframe containing daily stock market data

    Returns:
    df_weekly: dataframe containg weekly stock market data
    df_monthly: dataframe containing monthly stock market data
    '''
    df['Vol.'] = df['Vol.'].apply(lambda x: vol_change(x))

    logic = {'Open'  : 'first',
            'High'  : 'max',
            'Low'   : 'min',
            'Price' : 'last',
            'Vol.': 'sum',
            'Change %': 'sum'}
    
    df_weekly = df.set_index('Date')
    df_weekly = df_weekly.sort_index()
    df_weekly = df_weekly.resample('W').apply(logic)
    df_weekly.index = df_weekly.index - pd.tseries.frequencies.to_offset("6D")
    df_weekly = df_weekly.reset_index()

    df_monthly = df.set_index('Date')
    df_monthly = df_monthly.sort_index()
    df_monthly = df_monthly.resample('M').apply(logic)
    df_monthly.index = df_monthly.index - pd.tseries.frequencies.to_offset("M")
    df_monthly = df_monthly.reset_index()
    
    return df_weekly, df_monthly

    
