import matplotlib.dates  as mdates
import matplotlib.pyplot as plt
import pandas as pd
import numpy  as np

plt.style.use('seaborn-darkgrid')
#import matplotlib as mpl
plt.rcParams['axes.edgecolor'  ] = 'black'
plt.rcParams['axes.linewidth'  ] =  1.5
plt.rcParams['axes.labelsize'  ] =  'large'
plt.rcParams['lines.linewidth' ] =  2.0
plt.rcParams['font.weight'     ] = 'medium'
plt.rcParams['font.size'       ] =  12.0
plt.rcParams['axes.labelweight'] = 'medium'

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from mplfinance._utils import _construct_ohlc_collections
from mplfinance._utils import _construct_candlestick_collections
from mplfinance._utils import IntegerIndexDateTimeFormatter

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

    dates   = mdates.date2num(data.index.to_pydatetime())
    opens   = data['Open'].values
    highs   = data['High'].values
    lows    = data['Low'].values
    closes  = data['Close'].values
    if 'Volume' in data.columns:
        volumes = data['Volume'].values
    else:
        volumes = None

    return dates, opens, highs, lows, closes, volumes

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
                          'Validator'   : lambda value: value in ['candle','candlestick','ohlc','bars','ohlc bars','line'] },
 
        'style'       : { 'Default'     : 'classic',
 
                          'Implemented' : False,
                          'Validator'   : lambda value: value in ['classic','dark','checkers','chanuka','xmas','pastel'] },
 
        'volume'      : { 'Default'     : False,
 
                          'Implemented' : True,
                          'Validator'   : lambda value: isinstance(value,bool) },
 
        'mav'         : { 'Default'     : None,
 
                          'Implemented' : True,
                          'Validator'   : _mav_validator },
 
        'study'       : { 'Default'     : None,
 
                          'Implemented' : False,
                          'Validator'   : lambda value: isinstance(value,dict) }, #{'studyname': {study parms}} example: {'TE':{'mav':20,'upper':2,'lower':2}}
 
        'colorup'     : { 'Default'     : None, # use 'style' for default, instead.
 
                          'Implemented' : False,
                          'Validator'   : lambda value: isinstance(value,str) },
 
        'colordown'   : { 'Default'     : None, # use 'style' for default, instead.
 
                          'Implemented' : False,
                          'Validator'   : lambda value: isinstance(value,str) },
 
        'border'      : { 'Default'     : None, # use 'style' for default, instead.
 
                          'Implemented' : False,
                          'Validator'   : lambda value: isinstance(value,str) },
 
        'no_xgaps'      : { 'Default'     : None,  # None means follow default logic below:
                                                 # True for intraday data spanning 2 or more days, else False
                          'Implemented' : True,
                          'Validator'   : lambda value: isinstance(value,bool) },
 
        'figscale'      : { 'Default'   : 0.75, # scale base figure size (11" x 8.5") up or down.
                                          
                          'Implemented' : True,
                          'Validator'   : lambda value: isinstance(value,float) },
 
        'autofmt_xdate':{ 'Default'     : False,
 
                          'Implemented' : True,
                          'Validator'   : lambda value: isinstance(value,bool) }
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
    """
    Given open,high,low,close,volume data for a financial instrument (such as a stock, index,
    currency, future, option, etc.) plot the data.
    Available plots include ohlc bars, candlestick, and line plots.
    Also provide visually analysis in the form of common technical studies, such as:
    moving averages, macd, trading envelope, etc. 
    Also provide ability to plot trading signals, and/or user-defined studies.
    """

    config = _process_kwargs(kwargs)
    
    if _debug_trace():
        print('config=',config)

    dates,opens,highs,lows,closes,volumes = _check_and_prepare_data(data)

    base      = [11.0, 8.5]
    figscale  = config['figscale']
    fsize     = [d*figscale for d in base]
    
    fig = plt.figure()
    fig.set_size_inches(fsize)

    #  fig.add_axes( [left, bottom, width, height] ) ... numbers are fraction of fig
    if config['volume']:
        if volumes is None:
            raise ValueError('Request for volume, but NO volume data.')
        ax1 = fig.add_axes( [0.05, 0.25, 0.9, 0.7] )
        ax2 = fig.add_axes( [0.05, 0.05, 0.9, 0.2], sharex=ax1 )
    else:
        ax1 = fig.add_axes( [0.05, 0.05, 0.9, 0.9] )
        ax2 = None

    avg_days_between_points = (dates[-1] - dates[0]) / float(len(dates))


    # Default logic for 'no_xgaps':  True for intraday data spanning 2 or more days, else False
    # Caller provided 'no_xgaps' kwarg OVERRIDES default logic.

    no_xgaps = False

    # avgerage of 3 or more data points per day we will call intraday data:
    if avg_days_between_points < 0.33:  # intraday
        if mdates.num2date(dates[-1]).date() != mdates.num2date(dates[0]).date():
            # intraday data for more than one day:
            no_xgaps = True
            fmtstring = '%b %d, %H:%M'
        else:  # intraday data for a single day
            fmtstring = '%H:%M'
    else:  # 'daily' data (or could be weekly, etc.)
        if mdates.num2date(dates[-1]).date().year != mdates.num2date(dates[0]).date().year:
           fmtstring = '%Y %b %d'
        else:
           fmtstring = '%b %d'

    if config['no_xgaps'] is not None:  # override whatever was determined above.
        no_xgaps = config['no_xgaps']

    if no_xgaps:
        formatter = IntegerIndexDateTimeFormatter(dates, fmtstring)
        xdates = np.arange(len(dates))
    else:
        formatter = mdates.DateFormatter(fmtstring)
        xdates = dates
    
    ax1.xaxis.set_major_formatter(formatter)
    plt.xticks(rotation=45)

    ptype = config['type']
    if _debug_trace(): 
        print('ptype=',ptype)

    collections = None
    if ptype == 'candle' or ptype == 'candlestick':
        collections = _construct_candlestick_collections(xdates, opens, highs, lows, closes )
    elif ptype == 'ohlc' or ptype == 'bars' or ptype == 'ohlc_bars':
        collections = _construct_ohlc_collections(xdates, opens, highs, lows, closes )
    elif ptype == 'line':
        ax1.plot(xdates, closes, color='k')
    else:
        raise ValueError('Unrecognized plot type = "'+ptype+'"')

    if collections is not None:
        for collection in collections:
            ax1.add_collection(collection)

    mavgs = config['mav']
    if mavgs is not None:
        if isinstance(mavgs,int):
            mavgs = mavgs,      # convert to tuple 
        if len(mavgs) > 3:
            mavgs = mavgs[0:3]  # take at most 3
        mavcolors=['turquoise','magenta','gold']
        jj = 0
        for mav in mavgs:
            mavprices = data['Close'].rolling(mav).mean().values            
            ax1.plot(xdates, mavprices, color=mavcolors[jj])
            jj+=1

    avg_dist_between_points = (xdates[-1] - xdates[0]) / float(len(xdates))
    minx = xdates[0]  - avg_dist_between_points
    maxx = xdates[-1] + avg_dist_between_points
    miny = min([low for low in lows if low != -1])
    maxy = max([high for high in highs if high != -1])
    corners = (minx, miny), (maxx, maxy)
    ax1.update_datalim(corners)

    if config['volume']:
        ax2.bar(xdates,volumes,width=0.7)
        miny = 0.3 * min(volumes)
        maxy = 1.1 * max(volumes)
        ax2.set_ylim( miny, maxy )
        ax2.yaxis.set_label_position('right')
        ax2.yaxis.tick_right()
        ax2.xaxis.set_major_formatter(formatter)
        ax1.spines['bottom'].set_linewidth(0.25)
        ax2.spines['top'   ].set_linewidth(0.25)
        plt.setp(ax1.get_xticklabels(), visible=False)

    # TODO: ================================================================
    # TODO:  Investigate:
    # TODO:  ===========
    # TODO:  It appears to me that there may be some or significant overlap
    # TODO:  between what the following functions actually do:
    # TODO:  At the very least, all three of them appear to communicate 
    # TODO:  to matplotlib that the xaxis should be treated as dates:
    # TODO:   ->  'ax.autoscale_view()'
    # TODO:   ->  'ax.xaxis_dates()'
    # TODO:   ->  'plt.autofmt_xdates()'
    # TODO: ================================================================
    

    #if config['autofmt_xdate']:
        #print('CALLING fig.autofmt_xdate()')
        #fig.autofmt_xdate()

    ax1.autoscale_view()  # Is this really necessary??

    #  really use rcParams: call plt.rc('axes', grid=True)
    #  plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    ax1.set_ylabel('Price',size='x-large',weight='semibold')

    if config['volume']:
        ax2.figure.canvas.draw()  # This is needed to calculate offset
        offset = ax2.yaxis.get_major_formatter().get_offset()
        ax2.yaxis.offsetText.set_visible(False)
        vol_label = 'Volume x '+str(offset)
        ax2.set_ylabel(vol_label,size='x-large',weight='semibold')

    plt.show()

