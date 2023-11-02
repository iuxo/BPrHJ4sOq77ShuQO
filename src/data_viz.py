import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def bollinger_bands(df, n, m):
    '''
    Create bollinger bands based on dfs price based on moving average and number of standard deviations.

    Parameters:
    df: dataframe containing price history of stock 
    n: number of time periods/smoothing length
    m: number of standard deviations away from the moving average
    '''
    
    #typical price
    TP = (df['High'] + df['Low'] + df['Price']) / 3
    
    data = TP
    
    # takes one column from dataframe
    B_MA = pd.Series((data.rolling(n, min_periods=n).mean()), name='B_MA')
    sigma = data.rolling(n, min_periods=n).std() 
    
    BU = pd.Series((B_MA + m * sigma), name='BU')
    BL = pd.Series((B_MA - m * sigma), name='BL')
    
    df = df.join(B_MA)
    df = df.join(BU)
    df = df.join(BL)
    
    return df

def add_signal(df, data_type):
    '''
    Create buy and sell signals and add them to the dataframe. If given daily data use the Closing price to compare,
    if given weekly/monthly, use the high/lows to compare. If the price is greater than the upper range of the 
    bollinger band create sell signal. If the price is lower than the lower range of the bollinger band create a
    buy signal.

    Parameters:
    df: dataframe containing the stock market data and the bollinger bands
    data_type: daily/weekly/monthly data

    Returns:
    df: dataframe that contains buy and sell columns appended
    '''
    buy_list = []
    sell_list = []
    
    if data_type == "daily":
        for i in range(len(df['Price'])):
            if df['Price'].iat[i] > df['BU'].iat[i]:           # sell signal     daily
                buy_list.append(np.nan)
                sell_list.append(df['Price'].iat[i])
            elif df['Price'].iat[i] < df['BL'].iat[i]:         # buy signal      daily
                buy_list.append(df['Price'].iat[i])
                sell_list.append(np.nan)  
            else:
                buy_list.append(np.nan)
                sell_list.append(np.nan)  
    else:
        for i in range(len(df['Price'])):
            if df['High'][i] > df['BU'][i]:             # sell signal     weekly/monthly
                buy_list.append(np.nan)
                sell_list.append(df['Price'].iat[i])
            elif df['Low'][i] < df['BL'][i]:            # buy signal      weekly/monthly
                buy_list.append(df['Price'].iat[i])
                sell_list.append(np.nan)  
            else:
                buy_list.append(np.nan)
                sell_list.append(np.nan)  
         
    buy_list = pd.Series(buy_list, name='Buy')
    sell_list = pd.Series(sell_list, name='Sell')
    buy_list = buy_list[::-1]
    sell_list = sell_list[::-1]
        
    df = df.join(buy_list)
    df = df.join(sell_list)        
     
    return df

def plot_signals(df, ticker):
    '''
    Plot the stock market data containing the bollinger bands and the buy/sell signals.

    Parameters:
    df: dataframe containing all the stock market data
    ticker: ticker of the stock

    Returns:
    None
    '''

    # plot  values and significant levels
    plt.figure(figsize=(15,5))
    plt.title('Bollinger Bands chart ' + str(ticker))
    plt.plot(df['Date'], df['Price'], label='Close')

    plt.plot(df['Date'], df['High'], label='High', alpha=0.3)
    plt.plot(df['Date'], df['Low'], label='Low', alpha=0.3)

    plt.plot(df['Date'], df['BU'], label='B_Upper', alpha=0.3)
    plt.plot(df['Date'], df['BL'], label='B_Lower', alpha=0.3)
    plt.plot(df['Date'], df['B_MA'], label='B_SMA', alpha=0.3)
    plt.fill_between(df['Date'], df['BU'], df['BL'], color='grey', alpha=0.1)

    plt.scatter(df['Date'], df['Buy'], label='Buy', marker='^')
    plt.scatter(df['Date'], df['Sell'], label='Sell', marker='v')

    plt.legend()

    plt.show()