import os                as os
import pandas            as pd
import mplfinance        as mpf
import matplotlib.pyplot as plt

print('pd.__version__  =',pd.__version__ )                 # for the record
print('mpf.__version__ =',mpf.__version__)                 # for the record
print("plt.rcParams['backend'] =",plt.rcParams['backend']) # for the record

import subprocess
result = subprocess.run(['pwd'], stdout=subprocess.PIPE)
print('result.stdout=',result.stdout)


df = pd.read_csv('../data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)
print('df.shape='  , df.shape  )
print('df.head(3)=', df.head(3))
print('df.tail(3)=', df.tail(3))


mpf.plot(df,volume=True,savefig='test01.jpg')

os.system('ls -l test01.jpg')

rc = os.system('diff test01.jpg reference_images/test01.jpg')
assert rc == 0

apdict = mpf.make_addplot(df['LowerB'])
mpf.plot(df,volume=True,addplot=apdict,savefig='test02.jpg')

os.system('ls -l test02.jpg')
rc = os.system('diff test02.jpg reference_images/test02.jpg')
assert rc == 0
