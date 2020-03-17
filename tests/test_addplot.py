import os                as os
import mplfinance        as mpf
import matplotlib.pyplot as plt
from   matplotlib.testing.compare import compare_images

print('mpf.__version__ =',mpf.__version__)                 # for the record
print("plt.rcParams['backend'] =",plt.rcParams['backend']) # for the record

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

def percentB_aboveone(percentB,price):
    import numpy as np
    signal   = []
    previous = 2
    for date,value in percentB.iteritems():
        if value > 1 and previous <= 1:
            signal.append(price[date]*1.01)
        else:
            signal.append(np.nan)
        previous = value
    return signal

def percentB_belowzero(percentB,price):
    import numpy as np
    signal   = []
    previous = -1.0
    for date,value in percentB.iteritems():
        if value < 0 and previous >= 0:
            signal.append(price[date]*0.99)
        else:
            signal.append(np.nan)
        previous = value
    return signal

def test_addplot03(bolldata):
    df = bolldata
    fname=prefix+'03.png'

    tcdf = df[['LowerB','UpperB']]  # DataFrame with two columns

    low_signal  = percentB_belowzero(df['PercentB'], df['Close']) 
    high_signal = percentB_aboveone(df['PercentB'], df['Close'])

    apds = [ mpf.make_addplot(tcdf),
             mpf.make_addplot(low_signal,scatter=True,markersize=200,marker='^'),
             mpf.make_addplot(high_signal,scatter=True,markersize=200,marker='v'),
             mpf.make_addplot((df['PercentB']),panel='lower',color='g')
           ]

    mpf.plot(df,addplot=apds,figscale=1.3,volume=True,savefig=tdir+fname)

    os.system('ls -l '+tdir+fname)

    result = compare_images(refd+fname,tdir+fname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None

def test_addplot04(bolldata):
    df = bolldata
    fname=prefix+'04.png'

    tcdf = df[['LowerB','UpperB']]  # DataFrame with two columns

    low_signal  = percentB_belowzero(df['PercentB'], df['Close']) 
    high_signal = percentB_aboveone(df['PercentB'], df['Close'])

    apds = [ mpf.make_addplot(tcdf,linestyle='dashdot'),
             mpf.make_addplot(low_signal,scatter=True,markersize=200,marker='^'),
             mpf.make_addplot(high_signal,scatter=True,markersize=200,marker='v'),
             mpf.make_addplot((df['PercentB']),panel='lower',color='g',linestyle='dotted')
           ]

    mpf.plot(df,addplot=apds,figscale=1.5,volume=True,
             style='starsandstripes',savefig=tdir+fname)

    os.system('ls -l '+tdir+fname)

    result = compare_images(refd+fname,tdir+fname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None
