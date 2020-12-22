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
df = idf.loc['2011-07-01':'2011-12-30',:]

#  df.loc[:,'Volume'] *= (0.003*0.9869459423651993)
#  df.loc[:,'Volume'] *= (0.003*0.9869459423651994)
#  df.loc[:,'Volume'] *= (0.003*90000000000000.)
#  df.loc[:,'Volume'] *= (0.003*90000000000.)
#  df.loc[:,'Volume'] *= (0.003*90000000.)
#  df.loc[:,'Volume'] *= (0.003*900000.)
#  df.loc[:,'Volume'] *= (0.003*30000.)
#  df.loc[:,'Volume'] *= (0.003*3000.)
#  df.loc[:,'Volume'] *= (0.003*300.)
#  df.loc[:,'Volume'] *= (0.003*30.)
#  df.loc[:,'Volume'] *= (0.003*10.)
#  df.loc[:,'Volume'] *= (0.003*1.0)
#  df.loc[:,'Volume'] *= (0.003*0.1)
#  df.loc[:,'Volume'] *= (0.003*0.01)
df.loc[:,'Volume'] *= (0.003*0.001)

vmin = np.nanmin(df.iloc[0:20]['Volume'])
vmax = np.nanmax(df.iloc[0:20]['Volume'])

print('vmin=',vmin,' vmax=',vmax)

mpf.plot(df.iloc[0:20],volume=True,type='candle')
