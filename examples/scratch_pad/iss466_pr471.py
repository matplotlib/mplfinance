import pandas as pd
import mplfinance as mpf

aapldf  = pd.read_csv('../data/yahoofinance-AAPL-20040819-20180120.csv',index_col=0,parse_dates=True).iloc[-61:-1]
googdf = pd.read_csv('../data/yahoofinance-GOOG-20040819-20180120.csv',index_col=0,parse_dates=True).iloc[-61:-1]

mcblue  = mpf.make_marketcolors(base_mpf_style='default',up='b',down='b',ohlc='b')
mcgreen = mpf.make_marketcolors(base_mpf_style='default',up='limegreen',down='limegreen',ohlc='limegreen')

sblue = mpf.make_mpf_style(base_mpf_style='default',marketcolors=mcblue)

ap = mpf.make_addplot(googdf,type='candle',marketcolors=mcgreen)
mpf.plot(aapldf,type='candle',style=sblue,returnfig=True,addplot=ap)
mpf.show()
