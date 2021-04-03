import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import os.path

import mplfinance as mpf

date1 = "2004-2-1"
date2 = "2004-4-12"

infile = os.path.join('data','yahoofinance-INTC-19950101-20040412.csv')
quotes = pd.read_csv(infile, index_col=0, parse_dates=True, infer_datetime_format=True) 

# select desired range of dates
quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]

mpf.plot(quotes,type='candle',style='checkers')
