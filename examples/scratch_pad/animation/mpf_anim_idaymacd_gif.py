'''
This file contains a animation demo using mplfinance "external axes mode",
in which animate both the display of candlesticks as well as the display
of MACD (Moving Average Convergence Divergence) visual analysis.

In this example, instead of creating the Figure and Axes external to mplfiance,
we allow mplfinance to create the Figure and Axes using its "panel method", and
set kwarg `returnfig=True` so that mplfinance will return the Figure and Axes.

We then take those Axes and pass them back into mplfinance ("external axes mode")
as part of the animation.

Note that presently mplfinance does not support "blitting" (blitting makes animation
more efficient).  Nonetheless, the animation is efficient enough to update at least
once per second, and typically more frequently depending on the size of the plot.
'''
import pandas as pd
import mplfinance as mpf
import matplotlib.animation as animation

mpf.__version__

## Class to simulate getting more data from API:

class RealTimeAPI():
    def __init__(self):
        self.data_pointer = 0
        self.data_frame = pd.read_csv('data/SP500_NOV2019_IDayRVol.csv',index_col=0,parse_dates=True)
        #self.data_frame = self.data_frame.iloc[0:120,:]
        self.df_len = len(self.data_frame)

    def fetch_next(self):
        r1 = self.data_pointer
        self.data_pointer += 1
        if self.data_pointer >= self.df_len:
            return None
        return self.data_frame.iloc[r1:self.data_pointer,:]

    def initial_fetch(self,num):
        if self.data_pointer > 0:
            return
        r1 = self.data_pointer
        self.data_pointer += num
        return self.data_frame.iloc[r1:self.data_pointer,:]

rtapi = RealTimeAPI()

# =======
#  MACD:

df = rtapi.initial_fetch(450)

resample_map ={'Open'  :'first',
               'High'  :'max'  ,
               'Low'   :'min'  ,
               'Close' :'last' ,
               'Volume':'sum'  }

resample_period = '5T'

rs = df.resample(resample_period).agg(resample_map).dropna()

exp12     = rs['Close'].ewm(span=12, adjust=False).mean()
exp26     = rs['Close'].ewm(span=26, adjust=False).mean()
macd      = exp12 - exp26
signal    = macd.ewm(span=9, adjust=False).mean()
histogram = macd - signal

apds = [mpf.make_addplot(exp12,color='lime'),
        mpf.make_addplot(exp26,color='c'),
        mpf.make_addplot(histogram,type='bar',width=0.7,panel=1,
                         color='dimgray',alpha=1,secondary_y=False),
        mpf.make_addplot(macd,panel=1,color='fuchsia',secondary_y=True),
        mpf.make_addplot(signal,panel=1,color='b',secondary_y=True),
       ]

s = mpf.make_mpf_style(base_mpf_style='classic',rc={'figure.facecolor':'lightgray'})

fig, axes = mpf.plot(rs,type='candle',addplot=apds,figscale=1.5,figratio=(7,5),title='\n\nMACD',
                     style=s,volume=True,volume_panel=2,panel_ratios=(6,3,2),returnfig=True)

ax_main = axes[0]
ax_emav = ax_main
ax_hisg = axes[2]
ax_macd = axes[3]
ax_sign = ax_macd
ax_volu = axes[4]


def animate(ival):
    global df, rs
    nxt = rtapi.fetch_next()
    if nxt is None:
        print('no more data to plot')
        exit()
    df = df.append(nxt)
    rs = df.resample(resample_period).agg(resample_map).dropna()
    if len(rs) > 90:
        rs = rs[-90:]
    data = rs
    exp12     = data['Close'].ewm(span=12, adjust=False).mean()
    exp26     = data['Close'].ewm(span=26, adjust=False).mean()
    macd      = exp12 - exp26
    signal    = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal
    apds = [mpf.make_addplot(exp12,color='lime',ax=ax_emav),
            mpf.make_addplot(exp26,color='c',ax=ax_emav),
            mpf.make_addplot(histogram,type='bar',width=0.7,
                             color='dimgray',alpha=1,ax=ax_hisg),
            mpf.make_addplot(macd,color='fuchsia',ax=ax_macd),
            mpf.make_addplot(signal,color='b',ax=ax_sign),
           ]

    for ax in axes:
        ax.clear()
    mpf.plot(data,type='candle',addplot=apds,ax=ax_main,volume=ax_volu)

ani = animation.FuncAnimation(fig,animate,interval=50)

print('about to save')
ani.save('idaygcmacd.gif', writer='imagemagick',fps=5)
print('DONE saving')

mpf.show()
