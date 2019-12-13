import matplotlib.dates  as mdates
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('seaborn-darkgrid')
import matplotlib as mpl
mpl.rcParams['axes.edgecolor'] = 'black'
mpl.rcParams['axes.linewidth'] = 1.5
mpl.rcParams['lines.linewidth'] = 2.0

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from mplfinance._utils import _construct_ohlc_collections
from mplfinance._utils import _construct_candlestick_collections

def _debug_trace():
    return False

def _check_and_prepare_data(data):
    '''
    Check and Prepare the data input:
    For now, data must be a Pandas DataFrame with a DatetimeIndex
    and columns named 'Open', 'High', 'Low', 'Close', and optionally 'Volume'

    Later we will accept all of the following data formats:
      1. Pandas DataFrame with DatetimeIndex (as described above)
      2. Pandas Series with DatetimeIndex:
             Values are close prices, and Series generates a line plot
      3. Tuple of Lists, or List of Lists:
             The inner Lists are each columns, in the order: DateTime, Open, High, Low, Close, Volume
      4. Tuple of Tuples or List of Tuples:
             The inner tuples are each row, containing values in the order: DateTime, Open, High, Low, Close, Volume

    Return a Tuple of Lists: datetimes, opens, highs, lows, closes, volumes
    '''


    if not isinstance(data, pd.core.frame.DataFrame):
        raise TypeError('Expect data as DataFrame')

    if not isinstance(data.index,pd.core.indexes.datetimes.DatetimeIndex):
        raise TypeError('Expect data.index as DatetimeIndex')

    dates  = mdates.date2num(data.index.to_pydatetime())
    opens  = data['Open'].values
    highs  = data['High'].values
    lows   = data['Low'].values
    closes = data['Close'].values

    return dates, opens, highs, lows, closes, None

def _valid_kwargs_table():

    def _mav_validator(mav_value):
        # value for mav (moving average) keyword may be:
        # scalar int greater than 1, or tuple of ints, or list of ints (greater than 1).
        # tuple or list limited to length of 3 moving averages (to keep the plot clean).
        if isinstance(mav_value,int) and mav_value > 1:
            return True
        elif not isinstance(mav_value,tuple) and not isinstance(mav_value,list):
            return False

        if not len(mav_value) < 4:
            return False
        for num in mav_value:
            if not isinstance(num,int) and num > 1:
                return False
        return True

    vkwargs = {
        'type'        : { 'Default'     : 'ohlc',
 
                          'Implemented' : True,
                          'Validator'   : lambda value: value in ['candlestick','ohlc','bar','line'] },
 
        'style'       : { 'Default'     : 'classic',
 
                          'Implemented' : False,
                          'Validator'   : lambda value: value in ['classic','dark','checkers','chanuka','xmas','pastel'] },
 
        'volume'      : { 'Default'     : False,
 
                          'Implemented' : False,
                          'Validator'   : lambda value: value in [True,False] },
 
        'mav'         : { 'Default'     : None,
 
                          'Implemented' : True,
                          'Validator'   : _mav_validator },
 
        'study'       : { 'Default'     : None,
 
                          'Implemented' : False,
                          'Validator'   : (lambda value: isinstance(value,dict)) }, #{'studyname': {study parms}} example: {'TE':{'mav':20,'upper':2,'lower':2}}
 
        'upcolor'     : { 'Default'     : None, # use 'style' for default, instead.
 
                          'Implemented' : False,
                          'Validator'   : lambda value: isinstance(value,str) },
 
        'downcolor'   : { 'Default'     : None, # use 'style' for default, instead.
 
                          'Implemented' : False,
                          'Validator'   : lambda value: isinstance(value,str) },
 
        'upborder'    : { 'Default'     : None, # use 'style' for default, instead.
 
                          'Implemented' : False,
                          'Validator'   : lambda value: isinstance(value,str) },
 
        'downborder'  : { 'Default'     : None, # use 'style' for default, instead.
 
                          'Implemented' : False,
                          'Validator'   : lambda value: isinstance(value,str) }
    }
    # Check that we didn't make a typo in any of the things above
    #  that should otherwise be the same for all kwags:
    for key, value in vkwargs.items():
        if len(value) != 3:
            raise ValueError('Items != 3 in valid kwarg table, for kwarg "'+key+'"')
        if 'Default' not in value:
            raise ValueError('Missing "Default" value for kwarg "'+key+'"')
        if 'Implemented' not in value:
            raise ValueError('Missing "Implemented" flag for kwarg "'+key+'"')
        if 'Validator' not in value:
            raise ValueError('Missing "Validator" function for kwarg "'+key+'"')
        if value['Implemented'] not in [True,False]:
            raise ValueError('"Implemented" flag NOT True or False for kwarg "'+key+'"')

    return vkwargs
   

def _process_kwargs( kwargs ):

    vkwargs = _valid_kwargs_table()

    # initialize configuration from valid_kwargs_table:
    config = {}
    for key, value in vkwargs.items():
        config[key] = value['Default']

    # now validate kwargs, and for any valid kwargs
    #  replace the appropriate value in config:
    for key in kwargs.keys():
       if key not in vkwargs:
           raise KeyError('Unrecognized kwarg="'+str(key)+'"')
       elif not vkwargs[key]['Implemented']:
           raise NotImplementedError('kwarg "'+key+'" is NOT YET implemented.') 
       else:
           value = kwargs[key]
           if not vkwargs[key]['Validator'](value):
               raise ValueError('kwarg "'+key+'" with invalid value: "'+str(value)+'"')
       # if we are here, then kwarg is valid as far as we can tell;
       #  replace the appropriate value in config:
       config[key] = value

    return config


def plot( data, **kwargs ):

    config = _process_kwargs(kwargs)
    
    if _debug_trace():
        print('config=',config)

    dates,opens,highs,lows,closes,volumes = _check_and_prepare_data(data)
    
    fig, ax = plt.subplots()
    fig.set_size_inches((10,8))
    fig.autofmt_xdate()
    
    avg_days_between_points = (dates[-1] - dates[0]) / float(len(dates))

    if avg_days_between_points < 0.3:
        if (dates[-1] - dates[0]) > 1.3:    
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %H:%M'))
        else:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis_date()

    ptype = config['type']
    if _debug_trace(): 
        print('ptype=',ptype)
    if ptype == 'candlestick':
        collections = _construct_candlestick_collections(dates, opens, highs, lows, closes )
    elif ptype == 'ohlc':
        collections = _construct_ohlc_collections(dates, opens, highs, lows, closes )

    avg_dist_between_points = (dates[-1] - dates[0]) / float(len(dates))
    minx = dates[0]  - avg_dist_between_points
    maxx = dates[-1] + avg_dist_between_points
    miny = min([low for low in lows if low != -1])
    maxy = max([high for high in highs if high != -1])
    corners = (minx, miny), (maxx, maxy)
    ax.update_datalim(corners)
    ax.autoscale_view()

    # add these last (I don't know why, but this comment was in the "original_flavor" code).
    for collection in collections:
        ax.add_collection(collection)

    mavgs = config['mav']
    if mavgs != None:
        if isinstance(mavgs,int):
            mavgs = mavgs,      # convert to tuple 
        if len(mavgs) > 3:
            mavgs = mavgs[0:3]  # take at most 3

        mavcolors=['turquoise','gold','magenta']
        jj = 0
        for mav in mavgs:
            mavprices = (pd.Series(closes).rolling(mav).mean()).values            
            ax.plot(dates, mavprices, color=mavcolors[jj])
            jj+=1

    plt.show()

import datetime
def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time lapse in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt == None : dt = datetime.datetime.now()
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)
