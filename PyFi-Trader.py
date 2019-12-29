import bs4 as bs
import pickle
import requests


def save_sp500_tickers():
    """
    gets a list of the current S&P 500 stock symbols and downloads them from https://www.slickcharts.com/sp500
    :return:
    tickers object of 500 stock symbols comprising the Standards & Poor 500 Index
    """
    response = requests.get('https://www.slickcharts.com/sp500')
    soup = bs.BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', {'class': 'table table-hover table-borderless table-sm'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[2].text
        tickers.append(ticker)

    with open("sp500_tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    return tickers

print(save_sp500_tickers())