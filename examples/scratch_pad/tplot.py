import pandas as pd
daily = pd.read_csv('../data/SP500_NOV2019_Hist.csv',index_col=0,parse_dates=True)
daily.head(3)

#   idf = pd.read_csv('data/SP500_NOV2019_IDay.csv',index_col=0,parse_dates=True)
#   idf = idf.drop('Volume',axis=1) # Volume is zero anyway for this intraday data set
#   idf.index.name = 'Date'
#   daily = pd.read_csv('data/SP600_NOV2019_Hist.csv',index_col=0,parse_dates=True)
#   daily = pd.read_csv('data/SP500_NOV2019_Hist.csv',index_col=0,parse_dates=True)
#   daily = pd.read_csv('data/SP500_NOV2019_Hist.csv',index_col=0,parse_dates=True)

import mplfinance as mpf
mpf.__file__
mpf.plot(daily,mav=7,block=False)
mpf.plot(daily,volume=True,block=False)

df = pd.read_csv('../data/yahoofinance-SPY-20080101-20180101.csv',index_col=0,parse_dates=True)
mpf.plot(df[700:850],type='bars',volume=True,mav=(20,40),figscale=0.7,block=False)

mpf.plot(df[700:850],type='bars',no_xgaps=True,mav=(20,40),figscale=0.7,block=False)
mpf.plot(df[700:850],type='candle',volume=True,mav=(20,40),figscale=0.7,style='charles')
