# This allows multiple outputs from a single jupyter notebook cell:
import pandas as pd
import mplfinance as mpf

daily = pd.read_csv('../data/SP500_NOV2019_Hist.csv',index_col=0,parse_dates=True)
daily.index.name = 'Date'
daily.shape
daily.head(2)
daily.tail(2)

##mpf.plot(daily)

import matplotlib as mpl
import matplotlib.pyplot as plt


prop_cycle = mpl.rcParams['axes.prop_cycle']
colors = [item['color'] for item in prop_cycle]

#plt.rcParams['axes.facecolor'] = '#b4dced'

jj = 0
fig, axs = plt.subplots(2,5)
for ax in axs.flat:
    plt.rcParams['axes.facecolor'] = colors[jj]
    print("plt.rcParams['axes.facecolor'] = ",plt.rcParams['axes.facecolor'])
    ax.plot([1,1])
    ax.draw()
    jj+=1

plt.show()
