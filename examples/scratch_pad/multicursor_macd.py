import pandas as pd
import mplfinance as mpf
from matplotlib.widgets import MultiCursor

idf = pd.read_csv('../data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)
df  = idf.loc['2011-07-01':'2011-12-30',:]


exp12 = df['Close'].ewm(span=12, adjust=False).mean()
exp26 = df['Close'].ewm(span=26, adjust=False).mean()

macd = exp12 - exp26

signal    = macd.ewm(span=9, adjust=False).mean()
histogram = macd - signal

apds = [mpf.make_addplot(exp12,color='lime'),
        mpf.make_addplot(exp26,color='c'),
        mpf.make_addplot(histogram,type='bar',width=0.7,panel=1,
                         color='dimgray',alpha=1,secondary_y=False),
        mpf.make_addplot(macd,panel=1,color='fuchsia',secondary_y=True),
        mpf.make_addplot(signal,panel=1,color='b',secondary_y=True),
       ]

fig, axlist = mpf.plot(df,type='candle',addplot=apds,figscale=1.1,figratio=(8,5),title='\nMACD',
                       style='blueskies',volume=True,volume_panel=2,panel_ratios=(6,3,2),returnfig=True)

multi = MultiCursor(fig.canvas, axlist, color='r',lw=1.2, horizOn=True, vertOn=True)
mpf.show()
