import os.path
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from mplfinance.original_flavor import candlestick_ohlc

date1 = "2004-2-1"
date2 = "2004-4-12"
infile = os.path.join('data','yahoofinance-INTC-19950101-20040412.csv')
quotes = pd.read_csv(infile, index_col=0, parse_dates=True, infer_datetime_format=True)

# select desired range of dates
quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]

fig, ax = plt.subplots()
candlestick_ohlc(ax, zip(mdates.date2num(quotes.index.to_pydatetime()),
                         quotes['Open'], quotes['High'],
                         quotes['Low'], quotes['Close']), width=0.6)

fig.subplots_adjust(bottom=0.2)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  # e.g., Jan 12

ax.xaxis_date()
ax.autoscale_view()
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

plt.show()
