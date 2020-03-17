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

##  prefix='addplot'
##  tdir='test_images/'
##  refd='reference_images/'
##  #os.system('rm -f '+tdir+prefix+'*.jpg')
##  os.system('rm -f '+tdir+prefix+'*.png')

import pytest

#   @pytest.fixture(scope='session',autouse=True)
#   def root_directory(request):
#       return str(request.config.rootdir)

#def test_raise_ex(root_directory):
def test_raise():
    #print("root_directory=",root_directory)
    apdict = mpf.make_addplot(df['LowerB'])
    with pytest.raises(ValueError):
        mpf.plot(df,volume='True',addplot=apdict)
