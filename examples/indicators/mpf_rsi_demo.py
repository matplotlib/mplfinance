import pandas as pd
import mplfinance as mpf

infile = '../data/yahoofinance-SPY-20200901-20210113.csv'

df = pd.read_csv(infile, index_col=0, parse_dates=True).iloc[0:60]

import rsi
df['rsi'] = rsi.relative_strength(df['Close'],n=7)

print(df.head())
print(df.tail())

apd = mpf.make_addplot(df['rsi'],panel=2,color='lime',ylim=(10,90),secondary_y=True)

mpf.plot(df,type='candle',volume=True,mav=(10,20),figscale=1.5,addplot=apd,panel_ratios=(1,0.6))
mpf.plot(df,type='candle',style='charles',volume=True,mav=(10,20),figscale=1.5,addplot=apd,panel_ratios=(1,0.6))
mpf.plot(df,type='candle',style='mike',volume=True,mav=(10,20),figscale=1.5,addplot=apd,panel_ratios=(1,0.6))
mpf.plot(df,type='candle',style='checkers',volume=True,mav=(10,20),figscale=1.5,addplot=apd,panel_ratios=(1,0.6))
mpf.plot(df,type='candle',style='yahoo',volume=True,mav=(10,20),figscale=1.5,addplot=apd,panel_ratios=(1,0.6))
