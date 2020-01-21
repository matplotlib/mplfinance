import matplotlib.dates  as mdates
import matplotlib.pyplot as plt
import pandas as pd
import numpy  as np

from itertools import cycle
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from mplfinance._utils import _construct_ohlc_collections
from mplfinance._utils import _construct_candlestick_collections
from mplfinance._utils import IntegerIndexDateTimeFormatter

from mplfinance import _styles

from mplfinance._arg_validators import _check_and_prepare_data
from mplfinance._arg_validators import _mav_validator

def with_rc_context(func):
    '''
    This decoractor creates an rcParams context around a function, so that any changes
    the function makes to rcParams will be reversed when the decorated function returns
    (therefore those changes have no effect outside of the decorated function).
    '''
    def decorator(*args, **kwargs):
        with plt.rc_context():
            func(*args, **kwargs)
    return decorator

def _list_of_dict(x):
    return isinstance(x,list) and all([isinstance(item,dict) for item in x])

def _valid_kwargs_table():
    '''
    Construct and return the "valid kwargs table" for the mplfinance.plot() function.
    A valid kwargs table is a `dict` of `dict`s.  The keys of the outer dict are the
    valid key-words for the function.  The value for each key is a dict containing
    3 specific keys: "Default", "Implemented", and "Validator" with the following values:
        "Default"      - The default value for the kwarg if none is specified.
        "Implemented"  - Boolean, has this kwarg been implemented or not.  
                         NOTE: A non-implemented kwarg will still be present in the
                         configuration dict, along with the kwarg's default value.
        "Validator"    - A function that takes the caller specified value for the kwarg,
                         and validates that it is the correct type, and (for kwargs with 
                         a limited set of allowed values) may also validate that the
                         kwarg value is one of the allowed values.
    '''
    vkwargs = {
        'type'        : { 'Default'     : 'ohlc',
 
                          'Implemented' : True,
                          'Validator'   : lambda value: value in ['candle','candlestick','ohlc','bars','ohlc bars','line'] },
 
        'style'       : { 'Default'     : 'classic',
 
                          'Implemented' : True,
                          'Validator'   : lambda value: (value in ['classic','dark','checkers','chanuka','xmas','pastel']) or
                                                         isinstance(value,dict) },
 
        'volume'      : { 'Default'     : False,
 
                          'Implemented' : True,
                          'Validator'   : lambda value: isinstance(value,bool) },
 
        'mav'         : { 'Default'     : None,
 
                          'Implemented' : True,
                          'Validator'   : _mav_validator },
 
        'study'       : { 'Default'     : None,
 
                          'Implemented' : False,
                          'Validator'   : lambda value: isinstance(value,dict) }, #{'studyname': {study parms}} example: {'TE':{'mav':20,'upper':2,'lower':2}}
 
        'marketcolors': { 'Default'     : None, # use 'style' for default, instead.
 
                          'Implemented' : True,
                          'Validator'   : lambda value: isinstance(value,dict) },
 
        'no_xgaps'    : { 'Default'     : None,  # None means follow default logic below:
                                                 # True for intraday data spanning 2 or more days, else False
                          'Implemented' : True,
                          'Validator'   : lambda value: isinstance(value,bool) },
 
        'figscale'    : { 'Default'     : 0.90, # scale base figure size (11" x 8.5") up or down.
                                          
                          'Implemented' : True,
                          'Validator'   : lambda value: isinstance(value,float) or isinstance(value,int) },
 
        'addplot'     : { 'Default'     : None, 
                                          
                          'Implemented' : True,
                          'Validator'   : lambda value: isinstance(value,dict) or (isinstance(value,list) and all([isinstance(d,dict) for d in value])) },
 
        'savefig'     : { 'Default'     : None, 
                                          
                          'Implemented' : True,
                          'Validator'   : lambda value: isinstance(value,dict) or isinstance(value,str) },
 
    }
    # Check that we didn't make a typo in any of the things above:
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
   

def _process_kwargs(kwargs, vkwargs):
    '''
    Given a "valid kwargs table" and some kwargs, verify that each key-word
    is valid per the kwargs table, and that the value of the kwarg is the
    correct type.  Fill a configuration dictionary with the default value
    for each kwarg, and then substitute in any values that were provided 
    as kwargs and return the configuration dictionary.
    '''
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
           try:
               valid = vkwargs[key]['Validator'](value)
           except Exception as ex:
               raise ValueError('kwarg "'+key+'" with invalid value: "'+str(value)+'"') from ex
           if not valid:
               import inspect
               v = inspect.getsource(vkwargs[key]['Validator']).strip()
               raise ValueError('kwarg "'+key+'" with invalid value: "'+str(value)+'"\n    '+v)

       # ---------------------------------------------------------------
       #  At this point in the loop, if we have not raised an exception,
       #      then kwarg is valid as far as we can tell, therefore, 
       #      go ahead and replace the appropriate value in config:

       config[key] = value

    return config

@with_rc_context
def plot( data, **kwargs ):
    """
    Given open,high,low,close,volume data for a financial instrument (such as a stock, index,
    currency, future, option, etc.) plot the data.
    Available plots include ohlc bars, candlestick, and line plots.
    Also provide visually analysis in the form of common technical studies, such as:
    moving averages, macd, trading envelope, etc. 
    Also provide ability to plot trading signals, and/or addtional user-defined data.
    """

    dates,opens,highs,lows,closes,volumes = _check_and_prepare_data(data)

    config = _process_kwargs(kwargs, _valid_kwargs_table())

    style = config['style']
    if isinstance(style,str):
        print('plot() about to GET style="'+style+'"')
        style = _styles._get_mpfstyle(style)

    if isinstance(style,dict):
        print('plot() about to apply style=',style)
        _styles._apply_mpfstyle(style)
    
    base      = [11.0, 8.5]
    figscale  = config['figscale']
    fsize     = [d*figscale for d in base]
    
    fig = plt.figure()
    fig.set_size_inches(fsize)

    # check if we need a lower panel for an additional plot.
    #     if volume=True we will share the lower panel.

    need_lower_panel = False
    addplot = config['addplot']
    if addplot is not None:
        if isinstance(addplot,dict):
            addplot = [addplot,]   # make list of dict to be consistent
        elif not _list_of_dict(addplot):
            raise TypeError('addplot must be `dict`, or `list of dict`, NOT '+str(type(addplot)))
        for apdict in addplot:
            if apdict['panel'] == 'lower':
                need_lower_panel = True
                break

    #  fig.add_axes( [left, bottom, width, height] ) ... numbers are fraction of fig
    if need_lower_panel or config['volume']:
        if config['volume'] and volumes is None:
            raise ValueError('Request for volume, but NO volume data.')
        ax1 = fig.add_axes( [0.15, 0.38, 0.70, 0.50] )
        ax2 = fig.add_axes( [0.15, 0.18, 0.70, 0.20], sharex=ax1 )
    else:
        ax1 = fig.add_axes( [0.15, 0.18, 0.70, 0.70] )
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
           fmtstring = '%Y-%b-%d'
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

    collections = None
    if ptype == 'candle' or ptype == 'candlestick':
        collections = _construct_candlestick_collections(xdates, opens, highs, lows, closes,
                                                         marketcolors=style['marketcolors'] )
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
        if len(mavgs) > 7:
            mavgs = mavgs[0:7]  # take at most 7
     
        if style['mavcolors'] is not None:
            mavc = cycle(style['mavcolors'])
        else:
            mavc = None
            
        for mav in mavgs:
            mavprices = data['Close'].rolling(mav).mean().values 
            if mavc:
                ax1.plot(xdates, mavprices, color=next(mavc))
            else:
                ax1.plot(xdates, mavprices)

    avg_dist_between_points = (xdates[-1] - xdates[0]) / float(len(xdates))
    minx = xdates[0]  - avg_dist_between_points
    maxx = xdates[-1] + avg_dist_between_points
    miny = min([low for low in lows if low != -1])
    maxy = max([high for high in highs if high != -1])
    corners = (minx, miny), (maxx, maxy)
    ax1.update_datalim(corners)

    addplot = config['addplot']
    if addplot is not None:
        if isinstance(addplot,dict):
            addplot = [addplot,]   # make list of dict to be consistent

        elif not _list_of_dict(addplot):
            raise TypeError('addplot must be `dict`, or `list of dict`, NOT '+str(type(addplot)))

        for apdict in addplot:
            apdata = apdict['data']
            if isinstance(apdata,list) and not isinstance(apdata[0],(float,int)):
                raise TypeError('apdata is list but NOT of float or int')
            if isinstance(apdata,pd.DataFrame): 
                havedf = True
            else:
                havedf = False      # must be a single series or array
                apdata = [apdata,]  # make it iterable

            if apdict['panel'] == 'lower':
                ax = ax2
                if config['volume']:
                    ax = ax2.twinx()
            else:
                ax = ax1

            for column in apdata:
                if havedf:
                    ydata = apdata.loc[:,column]
                else:
                    ydata = column
                if apdict['scatter']:
                    size = apdict['markersize']
                    mark = apdict['marker']
                    ax.scatter(xdates, ydata, s=size, marker=mark)
                else:
                    ax.plot(xdates, ydata)

    if config['volume']:
        ax2.bar(xdates,volumes,width=0.7,color=style['marketcolors']['volume'])
        miny = 0.3 * min(volumes)
        maxy = 1.1 * max(volumes)
        ax2.set_ylim( miny, maxy )
        #ax2.yaxis.set_label_position('right')
        #ax2.yaxis.tick_right()
        ax2.xaxis.set_major_formatter(formatter)
     
    if need_lower_panel or config['volume']:
        ax1.spines['bottom'].set_linewidth(0.25)
        ax2.spines['top'   ].set_linewidth(0.25)
        plt.setp(ax1.get_xticklabels(), visible=False)

    # TODO: ================================================================
    # TODO:  Investigate:
    # TODO:  ===========
    # TODO:  It appears to me that there may be some or significant overlap
    # TODO:  between what the following functions actually do:
    # TODO:  At the very least, all four of them appear to communicate 
    # TODO:  to matplotlib that the xaxis should be treated as dates:
    # TODO:   ->  'ax.autoscale_view()'
    # TODO:   ->  'ax.xaxis_dates()'
    # TODO:   ->  'plt.autofmt_xdates()'
    # TODO:   ->  'fig.autofmt_xdate()'
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

    if config['savefig'] is not None:
        save = config['savefig']
        if isinstance(save,dict):
            plt.savefig(**save)
        else:
            plt.savefig(save)
    else:
        plt.show()
    #print('.plot() about to return')


def _valid_addplot_kwargs_table():

    valid_markers = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8',
                     's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd', '|', '_', 'P',
                     'X', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 'None', None, ' ', '']

    vkwargs = {
        'scatter'     : { 'Default'     : False,

                          'Implemented' : True,
                          'Validator'   : lambda value: isinstance(value,bool) },

        'panel'       : { 'Default'     : 'main',
    
                          'Implemented' : True,
                          'Validator'   : lambda value: value in ['main','lower'] },

        'marker'      : { 'Default'     : 'o',
    
                          'Implemented' : True,
                          'Validator'   : lambda value: value in valid_markers },

        'markersize'  : { 'Default'     : 18,
    
                          'Implemented' : True,
                          'Validator'   : lambda value: isinstance(value,(int,float)) },

        'secondary_y' : { 'Default' : None,

                          'Implemented' : False,
                          'Validator'   : lambda value: value in [] },
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


def make_addplot(data, **kwargs):
    '''
    Take data (pd.Series, pd.DataFrame, np.ndarray of floats, list of floats), and
    kwargs (see valid_addplot_kwargs_table) and construct a correctly structured dict
    to be passed into plot() using kwarg `addplot`.  
    NOTE WELL: len(data) here must match the len(data) passed into plot()
    '''
    if not isinstance(data, (pd.Series, pd.DataFrame, np.ndarray, list)):
        raise TypeError('Wrong type for data, in make_addplot()')

    config = _process_kwargs(kwargs, _valid_addplot_kwargs_table())

    return dict( data=data, **config)
