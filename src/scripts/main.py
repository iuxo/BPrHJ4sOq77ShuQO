from data_viz import *
from preprocess import *
from time_series import *

def main():
    stocks = pd.ExcelFile("../../data/2020Q1Q2Q3Q4-2021Q1.xlsx")
    tickers = ["SBER", "KCHOL", "MNHD", "BEEF3", "PAMP", "CCB", "IMPJ", "001230"]
    df_dict = pd.read_excel(stocks, None)

    d = zip(tickers, df_dict.values())

    for k, v in d:
        # k is the ticker name
        # v is the df
        v = v[:-1]
        v = v[::-1]
        v.reset_index(drop=True,inplace=True)

        k_train, k_test = train_test_split(v)

        k_train_weekly, k_train_monthly = prep_weekly_monthly(k_train)
        k_test_weekly, k_test_monthly = prep_weekly_monthly(k_test)

        k_test = k_test.reset_index()

        # time series
        alpha = 0.05
        ADF_Stationarity_Test(k_train, alpha)

        # create dataframes using date from corresponding k_test, and predictions
        k_predict = k_test.copy()
        k_weekly_predict = k_test_weekly.copy()
        # k_monthly_predict = k_test_monthly.copy()

        k_predict['Predicted'] = predict(k_train, k_test)
        k_weekly_predict['Predicted'] = predict(k_train_weekly, k_test_weekly)
        # k_monthly_predict['Predicted'] = predict(k_train_monthly, k_test_monthly)

        # add bollinger bands, signals and plot

        k_train_predictions = bollinger_bands(k_predict, 10, 2)
        k_train_weekly_predictions = bollinger_bands(k_weekly_predict, 5, 2)
        # k_train_monthly_predictions = bollinger_bands(k_monthly_predict, 1, 2)

        k_train_predictions_signal = add_signal(k_train_predictions, "daily")
        k_train_weekly_predictions_signal = add_signal(k_train_weekly_predictions, "weekly")
        # k_train_monthly_predictions = add_signal(k_train_monthly_predictions, "monthly")

        plot_signals(k_train_predictions_signal, k, "daily")
        plot_signals(k_train_weekly_predictions_signal, k, "weekly")
        # plot_signals(k_train_monthly_predictions, k, "monthly")

if __name__ == "__main__":
    main()