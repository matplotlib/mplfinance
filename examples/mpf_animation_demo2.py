import pandas as pd
import mplfinance as mpf
import matplotlib.animation as animation

idf = pd.read_csv('data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)

df = idf.loc['2011-07-01':'2011-12-30',:]

pkwargs=dict(type='candle',mav=(10,20))

fig, axes = mpf.plot(df.iloc[0:20],returnfig=True,volume=True,figsize=(11,8),panel_ratios=(2,1),title='\n\nS&P 500 ETF',**pkwargs)
ax1 = axes[0]
ax2 = axes[2]

def animate(ival):
    if (20+ival) > len(df):
        print('no more data to plot')
        ani.event_source.interval *= 3
        if ani.event_source.interval > 12000:
            exit()
        return
    data = df.iloc[0:(20+ival)]
    ax1.clear()
    ax2.clear()
    mpf.plot(data,ax=ax1,volume=ax2,**pkwargs)

ani = animation.FuncAnimation(fig, animate, interval=200)

mpf.show()
