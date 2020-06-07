import os
import os.path
import glob
import mplfinance        as mpf
import matplotlib.pyplot as plt
from   matplotlib.testing.compare import compare_images

print('mpf.__version__ =',mpf.__version__)                 # for the record
print("plt.rcParams['backend'] =",plt.rcParams['backend']) # for the record

base='alines'
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

def test_alines01(bolldata):

    df = bolldata

    fname = base+'01.png'
    tname = os.path.join(tdir,fname)
    rname = os.path.join(refd,fname)
    segments1 = [('2011-09-13', 115.),('2012-02-06', 135.)]
    mpf.plot(df,volume=True,savefig=tname,alines=segments1)

    tsize = os.path.getsize(tname)
    print(glob.glob(tname),'[',tsize,'bytes',']')

    rsize = os.path.getsize(rname)
    print(glob.glob(rname),'[',rsize,'bytes',']')

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
        print('result=',result)
    assert result is None

