import os                as os
import io                as io
import pandas            as pd
import mplfinance        as mpf
import matplotlib.pyplot as plt
from   matplotlib.testing.compare import compare_images

print('pd.__version__  =',pd.__version__ )                 # for the record
print('mpf.__version__ =',mpf.__version__)                 # for the record
print("plt.rcParams['backend'] =",plt.rcParams['backend']) # for the record

import pytest

def test_dataframe_typeErr():
    s  = pd.Series([0,1,2])
    with pytest.raises(TypeError) as ex:
        mpf.plot(s)
    assert 'Expect data as DataFrame' in str(ex.value)

    df = pd.DataFrame()
    with pytest.raises(TypeError) as ex:
        mpf.plot(df)
    assert 'Expect data.index as DatetimeIndex' in str(ex.value)
 
def test_kwarg_not_implemented(bolldata):
    df = bolldata
    with pytest.raises(NotImplementedError) as ex:
        mpf.plot(df,volume=True,study='Bollinger')
    assert 'kwarg NOT implemented' in str(ex.value)

def test_unrecognized_kwarg(bolldata):
    df = bolldata
    with pytest.raises(KeyError) as ex:
        mpf.plot(df,volume=True,foo='bar')
    assert 'Unrecognized kwarg' in str(ex.value)

def test_kwarg_validation_error(bolldata):
    '''
        We *could* very exhaustively test all kwargs, but that
        would be hundreds of lines of code, etc.  So just going
        to more-or-less randomly spot check just a few.
    '''
    df = bolldata

    apdict = mpf.make_addplot(df['LowerB'])
    with pytest.raises(TypeError) as ex:
        mpf.plot(df,volume='True',addplot=apdict)
    assert 'validator returned False for value' in str(ex.value)

    apdict = {'data':df['LowerB']}
    with pytest.raises(KeyError) as ex:
        mpf.plot(df,volume=True,addplot=apdict)

    with pytest.raises(TypeError) as ex:
        mpf.plot(df,volume=True,style='some random style name')
    assert 'validator returned False for value' in str(ex.value)
    
    with pytest.raises(ValueError) as ex:
        mpf.make_marketcolors(base_mpf_style='classic',ohlc='chartreussse')
    assert 'NOT is_color_like' in str(ex.value)

def test_renko_addplot(bolldata):
    df = bolldata
    apdict = mpf.make_addplot(df['LowerB'])
    with pytest.raises(ValueError) as ex:
        mpf.plot(df,type='renko',volume=True,addplot=apdict)
    assert '`addplot` is not supported for `type=\'renko\'`' in str(ex.value)
    #mpf.plot(df,type='renko',volume=True)

def test_figratio_bounds(bolldata):
    df = bolldata
    buf = io.BytesIO()
    mpf.plot(df,volume=True,figratio=(10,5),savefig=buf)
    with pytest.raises(ValueError) as ex:
        mpf.plot(df,volume=True,figratio=(11,2),savefig=buf)
    assert '"figratio" (aspect ratio)  must be between' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        mpf.plot(df,volume=True,figratio=(10,41),savefig=buf)
    assert '"figratio" (aspect ratio)  must be between' in str(ex.value)
