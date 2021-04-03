import pandas as pd
import mplfinance as mpf

print('\nmpf.__version__=',mpf.__version__,'\n')

filename = '../../data/SP500_NOV2019_IDay.csv'

intraday = pd.read_csv(filename,index_col=0,parse_dates=True)
intraday = intraday.drop('Volume',axis=1) # Volume is zero anyway for this intraday data set
intraday.index.name = 'Date'
intraday.shape
intraday.head(3)
intraday.tail(3)

iday = intraday.loc['2019-11-06 15:00':'2019-11-06 16:00',:]

print('len(iday)=',len(iday))

mpf.plot(iday,type='renko',renko_params=dict(brick_size=0.1))
mpf.plot(iday,type='candle')

filename='../../data/SP500_NOV2019_Hist.csv'
df = pd.read_csv(filename,index_col=0,parse_dates=True)
df.index.name = 'Date'
df.shape
df.head(3)
df.tail(3)

print('len(df)=',len(df))

mpf.plot(df,type='candle')
