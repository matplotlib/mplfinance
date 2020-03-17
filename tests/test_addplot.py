import os                as os
import mplfinance        as mpf
import matplotlib.pyplot as plt
from   matplotlib.testing.compare import compare_images

print('mpf.__version__ =',mpf.__version__)                 # for the record
print("plt.rcParams['backend'] =",plt.rcParams['backend']) # for the record

import subprocess
pwd = subprocess.run(['pwd'], stdout=subprocess.PIPE)
print('pwd.stdout=',str(pwd.stdout).strip())

prefix='addplot'
tdir='tests/test_images/'
refd='tests/reference_images/'
os.system('rm -f '+tdir+prefix+'*.png')

IMGCOMP_TOLERANCE = 7.0

def test_addplot01(bolldata):

    df = bolldata

    fname=prefix+'01.png'
    mpf.plot(df,volume=True,savefig=tdir+fname)

    os.system('ls -l '+tdir+fname)

    result = compare_images(refd+fname,tdir+fname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None

def test_addplot02(bolldata):
    df = bolldata
    fname=prefix+'02.png'
    apdict = mpf.make_addplot(df['LowerB'])
    mpf.plot(df,volume=True,addplot=apdict,savefig=tdir+fname)

    os.system('ls -l '+tdir+fname)

    result = compare_images(refd+fname,tdir+fname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None
