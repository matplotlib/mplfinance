import pandas as pd
import mplfinance as mpf

import matplotlib.dates as mdates

idf = pd.read_csv('../data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)
df = idf.loc['2011-07-01':'2011-12-30',:]


# =======
#  MACD:

#  df = df.iloc[0:30]

exp12     = df['Close'].ewm(span=12, adjust=False).mean()
exp26     = df['Close'].ewm(span=26, adjust=False).mean()
macd      = exp12 - exp26
signal    = macd.ewm(span=9, adjust=False).mean()
histogram = macd - signal

fb_green = dict(y1=macd.values,y2=signal.values,where=signal<macd,color="#93c47d",alpha=0.6,interpolate=True)
fb_red   = dict(y1=macd.values,y2=signal.values,where=signal>macd,color="#e06666",alpha=0.6,interpolate=True)
fb_green['panel'] = 1
fb_red['panel'] = 1
fb       = [fb_green,fb_red]

apds = [mpf.make_addplot(exp12,color='lime'),
        mpf.make_addplot(exp26,color='c'),
        mpf.make_addplot(histogram,type='bar',width=0.7,panel=1,
                         color='dimgray',alpha=1,secondary_y=True),
        mpf.make_addplot(macd,panel=1,color='fuchsia',secondary_y=False),
        mpf.make_addplot(signal,panel=1,color='b',secondary_y=False)#,fill_between=fb),
       ]

s = mpf.make_mpf_style(base_mpf_style='classic',rc={'figure.facecolor':'lightgray'})

mpf.plot(df,type='candle',addplot=apds,figscale=1.6,figratio=(6,5),title='\n\nMACD',
         style=s,volume=True,volume_panel=2,panel_ratios=(3,4,1),fill_between=fb)#,show_nontrading=True)

