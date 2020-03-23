import os
import os.path
import glob
import mplfinance        as mpf
import matplotlib.pyplot as plt
from   matplotlib.testing.compare import compare_images

print('mpf.__version__ =',mpf.__version__)                 # for the record
print("plt.rcParams['backend'] =",plt.rcParams['backend']) # for the record

base='addplot'
tdir = os.path.join('tests','test_images')
refd = os.path.join('tests','reference_images')

globpattern = os.path.join(tdir,base+'*.png')
oldtestfiles = glob.glob(globpattern)

for fn in oldtestfiles:
    try:
        os.remove(fn)
    except:
        print('Error removing file "'+fn+'"')

# IMGCOMP_TOLERANCE = 7.0  # this works fine for linux
IMGCOMP_TOLERANCE = 11.0  # required for a windows pass. (really 10.25 may do it).

def test_addplot01(bolldata):

    df = bolldata

    fname = base+'01.png'
    tname = os.path.join(tdir,fname)
    rname = os.path.join(refd,fname)

    mpf.plot(df,volume=True,savefig=tname)
   
    tsize = os.path.getsize(tname)
    print(glob.glob(tname),'[',tsize,'bytes',']')

    rsize = os.path.getsize(rname)
    print(glob.glob(rname),'[',rsize,'bytes',']')

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None

def test_addplot02(bolldata):
    df = bolldata

    fname = base+'02.png'
    tname = os.path.join(tdir,fname)
    rname = os.path.join(refd,fname)

    apdict = mpf.make_addplot(df['LowerB'])
    mpf.plot(df,volume=True,addplot=apdict,savefig=tname)

    tsize = os.path.getsize(tname)
    print(glob.glob(tname),'[',tsize,'bytes',']')

    rsize = os.path.getsize(rname)
    print(glob.glob(rname),'[',rsize,'bytes',']')

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None

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

    fname = base+'03.png'
    tname = os.path.join(tdir,fname)
    rname = os.path.join(refd,fname)

    tcdf = df[['LowerB','UpperB']]  # DataFrame with two columns

    low_signal  = percentB_belowzero(df['PercentB'], df['Close']) 
    high_signal = percentB_aboveone(df['PercentB'], df['Close'])

    apds = [ mpf.make_addplot(tcdf),
             mpf.make_addplot(low_signal,scatter=True,markersize=200,marker='^'),
             mpf.make_addplot(high_signal,scatter=True,markersize=200,marker='v'),
             mpf.make_addplot((df['PercentB']),panel='lower',color='g')
           ]

    mpf.plot(df,addplot=apds,figscale=1.3,volume=True,savefig=tname)

    tsize = os.path.getsize(tname)
    print(glob.glob(tname),'[',tsize,'bytes',']')

    rsize = os.path.getsize(rname)
    print(glob.glob(rname),'[',rsize,'bytes',']')

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None

def test_addplot04(bolldata):
    df = bolldata

    fname = base+'04.png'
    tname = os.path.join(tdir,fname)
    rname = os.path.join(refd,fname)

    tcdf = df[['LowerB','UpperB']]  # DataFrame with two columns

    low_signal  = percentB_belowzero(df['PercentB'], df['Close']) 
    high_signal = percentB_aboveone(df['PercentB'], df['Close'])

    apds = [ mpf.make_addplot(tcdf,linestyle='dashdot'),
             mpf.make_addplot(low_signal,scatter=True,markersize=200,marker='^'),
             mpf.make_addplot(high_signal,scatter=True,markersize=200,marker='v'),
             mpf.make_addplot((df['PercentB']),panel='lower',color='g',linestyle='dotted')
           ]

    mpf.plot(df,addplot=apds,figscale=1.5,volume=True,
             style='starsandstripes',savefig=tname)

    tsize = os.path.getsize(tname)
    print(glob.glob(tname),'[',tsize,'bytes',']')

    rsize = os.path.getsize(rname)
    print(glob.glob(rname),'[',rsize,'bytes',']')

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None
