from data_viz import *
from preprocess import *
from time_series import *

def main():
    stocks = pd.ExcelFile("../data/2020Q1Q2Q3Q4-2021Q1.xlsx")
    tickers = ["SBER", "KCHOL", "MNHD", "BEEF3", "PAMP", "CCB", "IMPJ", "001230"]
    df_dict = pd.read_excel(stocks, None)

    d = dict(zip(tickers, list(df_dict.values)))

    for k, v in d:
        # k is the ticker name
        # v is the df
        v = v.drop(311)
        v = v[::-1]
        v.reset_index(drop=True,inplace=True)

        k_train, k_test = train_test_split(v)

        k_train['Vol.'] = k_train['Vol.'].apply(lambda x: vol_change(x))

        k_train_weekly, k_train_monthly = prep_weekly_monthly(k_train)

        # time series
        alpha = 0.05
        ADF_Stationarity_Test(k_train, alpha)
        ADF_Stationarity_Test(k_train_weekly, alpha)
        ADF_Stationarity_Test(k_train_monthly, alpha)

        test_size = k_test.shape[0]

        k_train_predictions = predict(k_train, test_size)
        k_train_weekly_predictions = predict(k_train_weekly, test_size)
        k_train_monthly_predictions = predict(k_train_monthly, test_size)

        # add bollinger bands, signals and plot

        k_train_predictions = bollinger_bands(k_train_predictions, 20, 2)
        k_train_weekly_predictions = bollinger_bands(k_train_weekly_predictions, 3, 2)
        k_train_monthly_predictions = bollinger_bands(k_train_monthly_predictions, 1, 2)

        k_train_predictions = add_signal(k_train_predictions, "daily")
        k_train_weekly_predictions = add_signal(k_train_weekly_predictions, "weekly")
        k_train_monthly_predictions = add_signal(k_train_monthly_predictions, "monthly")

        plot_signals(k_train_predictions, k)
        plot_signals(k_train_weekly_predictions, k)
        plot_signals(k_train_monthly_predictions, k)


if __name__ == "__main__":
    main()