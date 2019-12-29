import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as panda
import pandas_datareader.data as web

# we'll use ggplot as our charting style
style.use('ggplot')

# let's create a date range - Jan 1 2000 - Dec 27 2019 (yesterday)
start_date = dt.datetime(2000, 1, 1)
end_date = dt.datetime(2019, 12, 27)

# put the symbol's data into a data frame, getting the data from yahoo's API
df = web.DataReader('LPL', 'yahoo', start_date, end_date)

# let's add a 100 day moving average
df['100ma'] = df['Adj Close'].rolling(window = 100, min_periods=0).mean()

# set up our axiseseses
ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=5)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex = ax1)

# le plot it
ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])
plt.show()