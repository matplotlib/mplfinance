import pandas as pd
import mplfinance as mpf
from matplotlib.widgets import MultiCursor
from matplotlib.collections import LineCollection

# read the data:
idf = pd.read_csv('../data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)
df  = idf.loc['2011-07-01':'2011-12-30',:]


# macd related calculations:
exp12 = df['Close'].ewm(span=12, adjust=False).mean()
exp26 = df['Close'].ewm(span=26, adjust=False).mean()
macd = exp12 - exp26
signal    = macd.ewm(span=9, adjust=False).mean()
histogram = macd - signal

# initial plot:
apds = [mpf.make_addplot(exp12,color='lime'),
        mpf.make_addplot(exp26,color='c'),
        mpf.make_addplot(histogram,type='bar',width=0.7,panel=1,
                         color='dimgray',alpha=1,secondary_y=False),
        mpf.make_addplot(macd,panel=1,color='fuchsia',secondary_y=True),
        mpf.make_addplot(signal,panel=1,color='b',secondary_y=True),
       ]

# For some reason, which i have yet to determine, MultiCursor somehow
# causes ymin to be set to zero for the main candlestick Axes, but we
# can correct that problem by passing in specific values:
ymin = min(df['Low'])  * 0.98
ymax = max(df['High']) * 1.02

# initial plot with cursor:
fig, axlist = mpf.plot(df,type='candle',addplot=apds,figscale=1.25,figratio=(8,6),title='\nMACD', ylim=(ymin,ymax),
                       style='blueskies',volume=True,volume_panel=2,panel_ratios=(6,3,2),returnfig=True)
multi = MultiCursor(fig.canvas, axlist[0:2], horizOn=True, vertOn=True, color='pink', lw=1.2)

# ---------------------------------------------------
# set up an event loop where we wait for two
# mouse clicks, and then draw a line in between them,
# and then wait again for another two mouse clicks.

# This is a crude way to do it, but its quick and easy.
# Disadvantage is: user has 8 seconds to provide two clicks
# or the first click will be erased.  But the 8 seconds
# repeats as long as the user does not close the Figure,
# so user can draw as many trend lines as they want.
# The advantage of doing it this way is we don't have
# to write all the mouse click handling stuff that's
# already written in `Figure.ginput()`.


alines = []

not_closed = True
def on_close(event):
    global not_closed
    not_closed = False

fig.canvas.mpl_connect('close_event', on_close)

while not_closed:

    vertices = fig.ginput(n=2,timeout=8)
    if len(vertices) < 2:
        continue
    p1 = vertices[0]
    p2 = vertices[1]

    d1 = df.index[ round(p1[0]) ]
    d2 = df.index[ round(p2[0]) ]

    alines.append( [ (d1,p1[1]), (d2,p2[1]) ] )

    apds = [mpf.make_addplot(exp12,color='lime',ax=axlist[0]),
            mpf.make_addplot(exp26,color='c',ax=axlist[0]),
            mpf.make_addplot(histogram,type='bar',width=0.7,panel=1,ax=axlist[2],color='dimgray',alpha=1),
            mpf.make_addplot(macd,panel=1,color='fuchsia',ax=axlist[3]),
            mpf.make_addplot(signal,panel=1,color='b',ax=axlist[3])
           ]

    mpf.plot(df,ax=axlist[0],type='candle',addplot=apds,ylim=(ymin,ymax),
             alines=dict(alines=alines,colors='r'),
             style='blueskies',volume=axlist[4],volume_panel=2,panel_ratios=(6,3,2))

    fig.canvas.draw_idle()

