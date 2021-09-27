import pandas as pd
import mplfinance as mpf

infile = 'data/yahoofinance-SPY-20200901-20210113.csv'

df = pd.read_csv(infile, index_col=0, parse_dates=True).iloc[0:60]

# mpf.plot(df,figscale=1.5,type='candle',mav=(10,20))




#mpf.plot(df,type='candle',figscale=1.5)

#df = pd.read_csv(infile, index_col=0, parse_dates=True).iloc[0:180]
#mpf.plot(df,type='renko',figscale=1.5)
#mpf.plot(df,type='pnf',figscale=1.5)

#mpf.plot(df,type='candle',figscale=1.5,mav=10) 

mpf.plot(df,type='candle',volume=True,mav=(10,20),figscale=1.5)
