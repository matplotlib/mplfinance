import os
import os.path
import glob
import mplfinance        as mpf
import matplotlib.pyplot as plt
from   matplotlib.testing.compare import compare_images

print('mpf.__version__ =',mpf.__version__)                 # for the record
print("plt.rcParams['backend'] =",plt.rcParams['backend']) # for the record

base='vlines'
tdir = os.path.join('tests','test_images')
refd = os.path.join('tests','reference_images')

globpattern = os.path.join(tdir,base+'*.png')
oldtestfiles = glob.glob(globpattern)

for fn in oldtestfiles:
    try:
        os.remove(fn)
    except:
        print('Error removing file "'+fn+'"')

IMGCOMP_TOLERANCE = 10.0  # this works fine for linux
# IMGCOMP_TOLERANCE = 11.0  # required for a windows pass. (really 10.25 may do it).

def test_vlines01(bolldata):

    df = bolldata

    fname = base+'01.png'
    tname = os.path.join(tdir,fname)
    rname = os.path.join(refd,fname)

    fig_axis = mpf.plot(
        df,volume=True,savefig=tname,returnfig=True,vlines=['2011-09-13']
    )
    plt.close(fig_axis[0])

    tsize = os.path.getsize(tname)
    print(glob.glob(tname),'[',tsize,'bytes',']')

    rsize = os.path.getsize(rname)
    print(glob.glob(rname),'[',rsize,'bytes',']')

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
        print('result=',result)
    assert result is None

def test_vlines02(bolldata):
    df = bolldata

    fname = base+'02.png'
    tname = os.path.join(tdir,fname)
    rname = os.path.join(refd,fname)

    fig_axis = mpf.plot(
        df,
        volume=True,
        savefig=tname,
        returnfig=True,
        vlines=['2011-09-13', '2012-02-06', '2011-07-01', '2012-06-28']
    )
    plt.close(fig_axis[0])

    tsize = os.path.getsize(tname)
    print(glob.glob(tname),'[',tsize,'bytes',']')

    rsize = os.path.getsize(rname)
    print(glob.glob(rname),'[',rsize,'bytes',']')

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
        print('result=',result)
    assert result is None


def test_vlines03(bolldata):
    df = bolldata

    fname = base+'03.png'
    tname = os.path.join(tdir,fname)
    rname = os.path.join(refd,fname)

    vl = dict(vlines='02-06-2012',linestyle='-.',colors='g')
    fig_axis = mpf.plot(
        df,
        type='pnf',
        vlines=vl,
        savefig=tname,
        returnfig=True
    )
    plt.close(fig_axis[0])

    tsize = os.path.getsize(tname)
    print(glob.glob(tname),'[',tsize,'bytes',']')

    rsize = os.path.getsize(rname)
    print(glob.glob(rname),'[',rsize,'bytes',']')

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
        print('result=',result)
    assert result is None

