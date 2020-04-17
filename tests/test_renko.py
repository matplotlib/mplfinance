import os
import os.path
import glob
import mplfinance        as mpf
import matplotlib.pyplot as plt
from   matplotlib.testing.compare import compare_images

print('mpf.__version__ =',mpf.__version__)                 # for the record
print("plt.rcParams['backend'] =",plt.rcParams['backend']) # for the record

base='renko'
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

def test_renko01(bolldata):

    df = bolldata

    fname = base+'01.png'
    tname = os.path.join(tdir,fname)
    rname = os.path.join(refd,fname)

    fig_axis = mpf.plot(df,type='renko',volume=True,savefig=tname,returnfig=True)
    plt.close(fig_axis[0])
   
    tsize = os.path.getsize(tname)
    print(glob.glob(tname),'[',tsize,'bytes',']')

    rsize = os.path.getsize(rname)
    print(glob.glob(rname),'[',rsize,'bytes',']')

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None


def test_renko02(bolldata):

    df = bolldata

    fname = base+'02.png'
    tname = os.path.join(tdir,fname)
    rname = os.path.join(refd,fname)

    fig_axis = mpf.plot(df,type='renko',renko_params=dict(brick_size=4),volume=True,savefig=tname,returnfig=True)
    plt.close(fig_axis[0])

    tsize = os.path.getsize(tname)
    print(glob.glob(tname),'[',tsize,'bytes',']')

    rsize = os.path.getsize(rname)
    print(glob.glob(rname),'[',rsize,'bytes',']')

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None


def test_renko03(bolldata):

    df = bolldata

    fname = base+'03.png'
    tname = os.path.join(tdir,fname)
    rname = os.path.join(refd,fname)

    fig_axis = mpf.plot(df,type='renko',renko_params=dict(brick_size='atr',atr_length=2),volume=True,savefig=tname,returnfig=True)
    plt.close(fig_axis[0])

    tsize = os.path.getsize(tname)
    print(glob.glob(tname),'[',tsize,'bytes',']')

    rsize = os.path.getsize(rname)
    print(glob.glob(rname),'[',rsize,'bytes',']')

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None

def test_renko04(bolldata):

    df = bolldata

    fname = base+'04.png'
    tname = os.path.join(tdir,fname)
    rname = os.path.join(refd,fname)

    fig_axis = mpf.plot(df,type='renko',renko_params=dict(brick_size='atr',atr_length='total'),mav=(8,20,30),volume=True,savefig=tname,returnfig=True)
    plt.close(fig_axis[0])

    tsize = os.path.getsize(tname)
    print(glob.glob(tname),'[',tsize,'bytes',']')

    rsize = os.path.getsize(rname)
    print(glob.glob(rname),'[',rsize,'bytes',']')

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None

def test_renkovalues(bolldata):

    df = bolldata

    rcv = {}
    fig_axis = mpf.plot(df,type='renko',return_calculated_values=rcv,returnfig=True)
    plt.close(fig_axis[0])

    assert rcv['renko_bricks'][-1] == 133.919998