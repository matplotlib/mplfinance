import pandas as pd
import mplfinance as mpf

import time
import matplotlib.pyplot as plt

infile = 'data/yahoofinance-SPY-20200901-20210113.csv'

df = pd.read_csv(infile, index_col=0, parse_dates=True)

# print('len(df)=',len(df))


for jj in (0,1,2):
    start = jj*35
    stop  = start + 35
    tdf = df.iloc[start:stop]
    fig,_ = mpf.plot(tdf,type='candle',volume=True,mav=(10,20),figscale=1.5,returnfig=True)
    plt.pause(4)
    plt.close(fig)
    del fig
