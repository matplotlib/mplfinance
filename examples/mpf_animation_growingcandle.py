'''
This file contains a animation demo using mplfinance demonstating resampling
of the data and re-displaying the most recent, partially resampled, candle.

The idea for this example came from Issue #256
(https://github.com/matplotlib/mplfinance/issues/256)

The typical use-case is where the user has real-time data from an API,
perhaps to the second, or minute, but wants to aggregate that data to
15 minutes per canlde, or maybe 30 minutes per candle. At the same time,
during those 15 or 30 minutes, the user wants to see the most recent
candle changing and developing as real-time data continues to come in.

In the example presented in this file, the data is once per minute,
with an aggregation of 15 minutes per candle.  But, for this *simulation*
we set the animation rate to 250ms, which means we are getting 1 minute's
worth of data from the API every 1/4 second. Thus, this simulation is
running 240 times faster than real-time.

In a real-life case, if we have data once per second, and want to aggregate
15 minutes per candle, we would set the animation interval to something
like 5000ms (once every 5 seconds) because a more frequent visualization
might be impractical to watch or to use for decision making.

PLEASE NOTE: In this example, we resample the *entire* data set with each
animation cycle.  This is inefficient, but works fine for less than 5000
data points or so.  For larger data sets it may be practical to cache
the resampled data up to the last "full" candle, and only resample the
data that contributes to the final candle (and append it to the cached
resampled data).  If I have time, I will work up and example doing that.

NOTE: Presently mplfinance does not support "blitting" (blitting makes animation
more efficient).  Nonetheless, the animation is efficient enough to update at least
once per second, and typically more frequently depending on the size of the plot.
'''
import pandas as pd
import mplfinance as mpf
import matplotlib.animation as animation

## Class to simulate getting more data from API:

class RealTimeAPI():
    def __init__(self):
        self.data_pointer = 0
        self.data_frame = pd.read_csv('data/SP500_NOV2019_IDay.csv',index_col=0,parse_dates=True)
        #self.data_frame = self.data_frame.iloc[0:120,:]
        self.df_len = len(self.data_frame)

    def fetch_next(self):
        r1 = self.data_pointer
        self.data_pointer += 1
        if self.data_pointer >= self.df_len:
            return None
        return self.data_frame.iloc[r1:self.data_pointer,:]

    def initial_fetch(self):
        if self.data_pointer > 0:
            return
        r1 = self.data_pointer
        self.data_pointer += int(0.2*self.df_len)
        return self.data_frame.iloc[r1:self.data_pointer,:]

rtapi = RealTimeAPI()

resample_map ={'Open' :'first',
               'High' :'max'  ,
               'Low'  :'min'  ,
               'Close':'last' }
resample_period = '15T'

df = rtapi.initial_fetch()
rs = df.resample(resample_period).agg(resample_map).dropna()

fig, axes = mpf.plot(rs,returnfig=True,figsize=(11,8),type='candle',title='\n\nGrowing Candle')
ax = axes[0]

def animate(ival):
    global df
    global rs
    nxt = rtapi.fetch_next()
    if nxt is None:
        print('no more data to plot')
        ani.event_source.interval *= 3
        if ani.event_source.interval > 12000:
            exit()
        return
    df = df[-700:].append(nxt)
    rs = df.resample(resample_period).agg(resample_map).dropna()
    ax.clear()
    mpf.plot(rs,ax=ax,type='candle')

ani = animation.FuncAnimation(fig, animate, interval=250)

mpf.show()
