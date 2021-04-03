import pandas as pd
import matplotlib
print(matplotlib.__version__)
print(matplotlib.get_backend())

import matplotlib.pyplot as plt

import mplfinance as mpf
print(mpf.__version__)

#idf = pd.read_csv('abc.csv',index_col=0,parse_dates=True)
idf = pd.read_csv('../data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)
idf.shape
idf.head(3)
idf.tail(3)
df = idf.loc['2011-07-01':'2011-12-30',:]*1000000.

x = [0,1,2,3,4,5,6,7,8,9]
y = [n*1000000 for n in x]


fig = plt.figure()

ax  = fig.add_subplot(1,1,1)

#ax.ticklabel_format(useOffset=False)
ax.ticklabel_format(useOffset=False,scilimits=(5,5),axis='y')
ax.ticklabel_format(useOffset=False,scilimits=(0,0),axis='x')
#ax.yaxis.offsetText.set_visible(False)


ax.plot(x,y)

plt.show()

