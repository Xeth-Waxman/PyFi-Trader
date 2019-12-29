import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as panda
import pandas_datareader.data as web
from pandas.plotting import register_matplotlib_converters

# this addresses the future warning about 'implicitly registered datetime converters'
register_matplotlib_converters()

# we'll use ggplot as our charting style
style.use('ggplot')

# let's create a date range - Jan 1 2000 - Dec 27 2019 (yesterday)
start_date = dt.datetime(2000, 1, 1)
end_date = dt.datetime(2019, 12, 27)

# put the symbol's data into a data frame, getting the data from yahoo's API
df = web.DataReader('LPL', 'yahoo', start_date, end_date)

# re-sample the data into 10-day periods
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

# weird date-fu because matplotlib
df_ohlc.reset_index(inplace=True)
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

# set up our axiseseses
ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=5)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex = ax1)
ax1.xaxis_date()

# candlestick that shizz
candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

# show that sh**
plt.show()