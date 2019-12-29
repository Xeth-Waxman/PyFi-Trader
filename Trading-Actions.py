import numpy as np
import pandas as pd
import pickle

def process_labels(ticker, lag_days = 7):
    """
    This function takes a given stock symbol and a lag-time, specified in days, and creates a data-frame
    loaded from 'SP500_formatted.csv', which is created by executing PyFi-Playground. The data-frame will contain
    the original data from SP500_formatted.csv, plus a new set of columns that take the format
    {}_{}d.format(ticker, j), where j is between 1 and lag_days. This column will contain the percentage change
    of the price vs the price j days into the future; e.g., AAPL_1d of -1.00 means the price of Apple will decline
    by 1% the following day
    :param ticker: The stock symbol to be labeled. Must be in the S&P 500 and pre-loaded into SP500_formatted.csv
    :param lag_days: The number of days into the future to evaluate. The default is 7
    :return: tickers, a list of the values of the SP500_formatted.csv file, and df - a dataframe labeled with the
    percentage change of the passed ticker
    """
    lag_days += 1
    df = pd.read_csv('SP500_formatted.csv')
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1, lag_days):
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]

    df.fillna(0, inplace=True)
    return tickers, df

def buy_sell_hold(*args, pct_change = 0.02):
    """

    :param args: The columns we're evaluating for pct change in price
    :param pct_change: the percentage change of the price of the stock to trigger a buy or sell action. The default
    is 0.02 (2%)
    :return: 1 for a buy signal, -1 for a sell signal, and 0 for a hold
    """
    cols = [c for c in args]
    for col in cols:
        if col > pct_change:
            return 1
        if col < -pct_change:
            return -1

    return 0
