import os                as os
import pandas            as pd
import mplfinance        as mpf
import matplotlib.pyplot as plt
from   matplotlib.testing.compare import compare_images

print('pd.__version__  =',pd.__version__ )                 # for the record
print('mpf.__version__ =',mpf.__version__)                 # for the record
print("plt.rcParams['backend'] =",plt.rcParams['backend']) # for the record

import pytest

def test_raise(bolldata):
    df = bolldata
    apdict = mpf.make_addplot(df['LowerB'])
    with pytest.raises(ValueError):
        mpf.plot(df,volume='True',addplot=apdict)
