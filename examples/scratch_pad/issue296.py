import pandas as pd
import mplfinance as mpf
import matplotlib.animation as animation
import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib
print(matplotlib.__version__)
print(matplotlib.get_backend())

import mplfinance as mpf
print(mpf.__version__)

#idf = pd.read_csv('abc.csv',index_col=0,parse_dates=True)
idf = pd.read_csv('../data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)
idf.shape
idf.head(3)
idf.tail(3)
df = idf.loc['2011-07-01':'2011-12-30',:]

fig = mpf.figure(style='yahoo', figsize=(7, 8))
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(3,1,3)

def animate(ival):
    if (20+ival) > len(df):
        print('no more data to plot')
        ani.event_source.interval *= 3
        if ani.event_source.interval > 12000:
            exit()
        return
    #return
    data = df.iloc[0:(20+ival)]
    ax1.clear()
    ax2.clear()
    mpf.plot(data,ax=ax1,volume=ax2,type='candle')

root = tkinter.Tk()
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
ani = animation.FuncAnimation(fig, animate, interval=250)
mpf.plot(df.iloc[0:20],ax=ax1,volume=ax2,type='candle')

root.mainloop()
