import os                as os
import pandas            as pd
import mplfinance        as mpf
import matplotlib.pyplot as plt
from   matplotlib.testing.compare import compare_images

print('pd.__version__  =',pd.__version__ )                 # for the record
print('mpf.__version__ =',mpf.__version__)                 # for the record
print("plt.rcParams['backend'] =",plt.rcParams['backend']) # for the record

import subprocess
pwd = subprocess.run(['pwd'], stdout=subprocess.PIPE)
print('pwd.stdout=',pwd.stdout)

df = pd.read_csv('examples/data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)
print('df.shape='  , df.shape  )
print('df.head(3)=', df.head(3))
print('df.tail(3)=', df.tail(3))

prefix='addplot'
tdir='tests/mpftests/test_images/'
refd='tests/mpftests/reference_images/'
#os.system('rm -f '+tdir+prefix+'*.jpg')
os.system('rm -f '+tdir+prefix+'*.png')

IMGCOMP_TOLERANCE = 7.0

# ---- Test 01 -----

def test_addplot01():

    fname=prefix+'01.png'
    mpf.plot(df,volume=True,savefig=tdir+fname)

    os.system('ls -l '+tdir+fname)

    result = compare_images(refd+fname,tdir+fname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None

# ---- Test 02 -----

def test_addplot02():
    fname=prefix+'02.png'
    apdict = mpf.make_addplot(df['LowerB'])
    mpf.plot(df,volume=True,addplot=apdict,savefig=tdir+fname)

    os.system('ls -l '+tdir+fname)

    result = compare_images(refd+fname,tdir+fname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None
