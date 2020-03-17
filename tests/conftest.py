import pytest
import os                as os
import pandas            as pd

os.environ['MPLBACKEND'] = 'agg'

print('\npd.__version__  =',pd.__version__ )                 # for the record

df = pd.read_csv('examples/data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)
print('df.shape='  , df.shape  )
print('df.head(3)=', df.head(3))
print('df.tail(3)=', df.tail(3))

@pytest.fixture()
def bolldata():
   return df
