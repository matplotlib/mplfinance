import glob
import mplfinance as mpf
import pandas as pd


df = pd.read_csv('../data/yahoofinance-GOOG-20040819-20180120.csv',index_col=0,parse_dates=True)

tdf = df.iloc[0:2000,:]
mpf.plot(tdf,type='candle',tight_layout=True,datetime_format='%b %d, %H:%M')

df = pd.read_csv('../data/SP500_NOV2019_IDay.csv',index_col=0,parse_dates=True)

tdf = df.loc['2019-11-05 10:47':'2019-11-05 13:13',:]
mpf.plot(tdf,type='candle',tight_layout=True,datetime_format='%b %d, %H:%M')


