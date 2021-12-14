import pandas as pd
import mplfinance as mpf
import ast 

df = pd.read_csv('pr451data.csv',index_col=0,parse_dates=True)

print(df.head(3))

custom_colors = []
for i in range(len(df)):
    if i % 3 == 0:
        #custom_colors.append(mpf.make_marketcolors(up='#29c9ff', down='#f3b5ff', edge='#29c9ff', wick='#29c9ff', ohlc='#32a852', volume='#a89132'))
        custom_colors.append(mpf.make_marketcolors(up='#29c9ff',down='#f3b5ff',edge='#29c9ff',wick='#29c9ff',
                                                   ohlc={'up':'lime','down':'blue'}, volume='#a89132'))
    elif i%5 == 0:
        custom_colors.append("#000000")
    else:
        custom_colors.append(None)

#STYLE = 'binance'
STYLE = 'yahoo'

#mpf.plot(df, type='candle',style=STYLE,volume=True,block=False,figscale=1.25,savefig='pr451t2no.jpg')
#mpf.plot(df, type='ohlc',style=STYLE,volume=True,block=False,figscale=1.25)
mpf.plot(df, type='candle',style=STYLE,volume=True,block=False,figscale=1.25)
#mpf.plot(df, type='hollow',style=STYLE,volume=True,block=False,figscale=1.25)

#mpf.plot(df, type='candle',style=STYLE,marketcolor_overrides=custom_colors,volume=True,figscale=1.25,savefig='pr451t2ye.jpg')
#mpf.plot(df, type='ohlc',style=STYLE,marketcolor_overrides=custom_colors,volume=True,figscale=1.25)
mpf.plot(df, type='candle',style=STYLE,marketcolor_overrides=custom_colors,volume=True,figscale=1.25)
#mpf.plot(df, type='hollow',style=STYLE,marketcolor_overrides=custom_colors,volume=True,figscale=1.25)
