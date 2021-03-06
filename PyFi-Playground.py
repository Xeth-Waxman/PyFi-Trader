import bs4 as bs
import pickle
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

def save_sp500_tickers():
    '''
    gets a list of the current S&P 500 stock symbols and downloads them from https://www.slickcharts.com/sp500
    :return:
    tickers object of 500 stock symbols comprising the Standards & Poor 500 Index
    '''
    response = requests.get('https://www.slickcharts.com/sp500')
    soup = bs.BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', {'class': 'table table-hover table-borderless table-sm'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[2].text
        # replace '.' with '-', because Yahoo
        ticker = ticker.replace('.', '-')
        tickers.append(ticker)

    with open('sp500_tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)

    return tickers


def get_data_from_yahoo(reloadSP500=False):
    '''
    gets pricing data from yahoo for a stock ticker. If reload is true, the function will refresh
    the ticker list. Use this if you suspect the SP500 index has recently changed.
    :return:
    '''
    if reloadSP500:
        tickers = save_sp500_tickers()
    else:
        with open('sp500_tickers.pickle', 'rb') as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2019, 12, 31)

    for ticker in tickers:
        # replace '.' with '-', because Yahoo
        ticker = ticker.replace('.', '-')
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
            print('processing {}'.format(ticker))

def collate_data():
    '''
    loops through local files and collates all ticker information into a single data frame
    :return:
    '''
    with open('sp500_tickers.pickle', 'rb') as f:
        tickers = pickle.load(f)
    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)
        df.rename(columns = {'Adj Close' : ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)

    print(main_df.head())
    main_df.to_csv('SP500_formatted.csv')

def visualize_data():
    """
    This function visualizes the formatted S&P 500 history
    :return:
    """
    df = pd.read_csv('SP500_formatted.csv')

    # create a correlation dataframe
    df_corr = df.corr()
    data = df_corr.values

    # le plot it
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    #define heatmap
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    column_lables = df_corr.columns
    row_labels = df_corr.index
    ax.set_xticklabels(column_lables)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1, 1)
    plt.tight_layout()
    plt.show()

# We've gotten the data already, we can comment the below out. Uncomment if you want to re-run
# get_data_from_yahoo(True)
# collate_data()
visualize_data()
