import os
import os.path
import glob
import mplfinance as mpf
import pandas as pd   
import matplotlib.pyplot as plt
from   matplotlib.testing.compare import compare_images

print('mpf.__version__ =',mpf.__version__)                 # for the record
print('mpf.__file__ =',mpf.__file__)                       # for the record
print("plt.rcParams['backend'] =",plt.rcParams['backend']) # for the record

base='ema'
tdir = os.path.join('tests','test_images')
refd = os.path.join('tests','reference_images')

IMGCOMP_TOLERANCE = 10.0  # this works fine for linux
# IMGCOMP_TOLERANCE = 11.0  # required for a windows pass. (really 10.25 may do it).

def create_ema_image(tname):

    df = pd.read_csv('./examples/data/yahoofinance-GOOG-20040819-20180120.csv', parse_dates=True)
    df.index = pd.DatetimeIndex(df['Date'])

    df = df[-50:]               # show last 50 data points only                     

    ema25 = df['Close'].ewm(span=25.0, adjust=False).mean()       
    mav25 = df['Close'].rolling(window=25).mean()

    ap = [
        mpf.make_addplot(df, panel=1, type='ohlc', color='c',
                         ylabel='mpf mav', mav=25, secondary_y=False),
        mpf.make_addplot(ema25, panel=2, type='line', width=2,  color='c',
                         ylabel='calculated', secondary_y=False),
        mpf.make_addplot(mav25, panel=2, type='line', width=2, color='blue',
                         ylabel='calculated', secondary_y=False)
    ]

    # plot and save in `tname` path
    mpf.plot(df, ylabel="mpf ema", type='ohlc',
             ema=25, addplot=ap, panel_ratios=(1, 1), savefig=tname
    )


def test_ema():

    fname = base+'01.png'
    tname = os.path.join(tdir,fname)
    rname = os.path.join(refd,fname)

    create_ema_image(tname)

    tsize = os.path.getsize(tname)
    print(glob.glob(tname),'[',tsize,'bytes',']')

    rsize = os.path.getsize(rname)
    print(glob.glob(rname),'[',rsize,'bytes',']')

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
        print('result=',result)
    assert result is None


test_ema()
