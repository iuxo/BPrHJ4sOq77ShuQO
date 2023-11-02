from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA

def ADF_Stationarity_Test(time, alpha):
    '''
    Takes time series and alpha (significance level) and 
    prints the adfuller test result
    print the conclusion of statonarity based on ADF

    Parameters:
    time: a time series
    alpha: significance level for Null Hypothesis Testing

    Return:
    None
    '''
    result = adfuller(time['Price'])
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    for key, value in result[4].items():
        print('Critial Values:')
        print(f'   {key}, {value}')  
    if result[1] > alpha:
        print('We accept the null hypothesis, the time series has a unit root and is not stationary.')
    else:
        print('We reject the null hypothesis, the time series does not have a unit root and is stationary.')

def predict(df, test_size):
    '''
    Using data from a non stationary time series, use ARIMA model to predict data points.

    Parameters:
    df: dataframe containing stock market data
    test_size: number of data points to predict

    Returns:
    predictions: data frame of predictions of length test_size
    '''
    X = df['Price']
    history = [x for x in X]
    predictions = list()

    # iteration step for each time point
    for time_point in range(test_size):
        model = ARIMA(history, order=(5,1,0))
        model_fit = model.fit()
        output = model_fit.forecast()
        predicted= output[0]
        predictions.append(predicted)

    return predictions