import datetime as dt
import matplotlib.pyplot as pyplot
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

# what does this look like?
df['Adj Close'].plot()
pyplot.show()
