import pandas as pd
import mplfinance as mpf
import matplotlib
import numpy as np

print(matplotlib.__version__)
print(matplotlib.get_backend())
print(mpf.__version__)

#idf = pd.read_csv('abc.csv',index_col=0,parse_dates=True)
idf = pd.read_csv('../data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)
idf.shape
idf.head(3)
idf.tail(3)
# df = idf.loc['2011-07-01':'2011-12-30',:]

factors = [0.9869459423651993, 0.9869459423651994, 90000000000000., 90000000000.,
           90000000., 900000., 30000., 3000., 300., 30., 10., 1.0, 0.1, 0.01, 0.001 ]

#  factors = [0.9869459423651993,]

for factor in factors:
    df = idf.loc['2011-07-01':'2011-12-30',:]
    df.loc[:,'Volume'] *= (0.003*factor)
    vmin = np.nanmin(df.iloc[0:20]['Volume'])
    vmax = np.nanmax(df.iloc[0:20]['Volume'])
    print('vmin=',vmin,' vmax=',vmax)
    mpf.plot(df.iloc[0:20],volume=True,type='candle')

df = idf.loc['2011-07-01':'2011-12-30',:]
df.loc[:,'Volume'] *= (0.003*30000.)
mpf.plot(df.iloc[0:20],volume=True,type='candle',volume_exponent='legacy')
mpf.plot(df.iloc[0:20],volume=True,type='candle',volume_exponent=3)
mpf.plot(df.iloc[0:20],volume=True,type='candle',volume_exponent=5)
mpf.plot(df.iloc[0:20],volume=True,type='candle',volume_exponent=8)
mpf.plot(df.iloc[0:20],volume=True,type='candle',volume_exponent=11)
mpf.plot(df.iloc[0:20],volume=True,type='candle',volume_exponent=13)
mpf.plot(df.iloc[0:20],volume=True,type='candle',volume_exponent='what?')
