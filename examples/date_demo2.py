"""
Show how to make date plots in matplotlib using date tick locators and
formatters.  See major_minor_demo1.py for more information on
controlling major and minor ticks
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import (MONDAY, DateFormatter, MonthLocator,
                              WeekdayLocator)

date1 = "2002-1-5"
date2 = "2003-12-1"

# every monday
mondays = WeekdayLocator(MONDAY)

# every 3rd month
months = MonthLocator(range(1, 13), bymonthday=1, interval=3)
monthsFmt = DateFormatter("%b '%y")


quotes = pd.read_csv('data/yahoofinance-INTC-19950101-20040412.csv',
                     index_col=0,
                     parse_dates=True,
                     infer_datetime_format=True)

# select desired range of dates
quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]

dates = quotes.index
opens = quotes['Open']


fig, ax = plt.subplots()
ax.plot_date(dates, opens, '-')
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.xaxis.set_minor_locator(mondays)
ax.autoscale_view()
# ax.xaxis.grid(False, 'major')
# ax.xaxis.grid(True, 'minor')
ax.grid(True)

fig.autofmt_xdate()

plt.show()
