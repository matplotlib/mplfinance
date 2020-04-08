import matplotlib.dates  as mdates
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import numpy  as np
import copy
import io
import math
import warnings

from itertools import cycle
#from pandas.plotting import register_matplotlib_converters
#register_matplotlib_converters()

from mplfinance._utils import _construct_ohlc_collections
from mplfinance._utils import _construct_candlestick_collections
from mplfinance._utils import _construct_renko_collections
from mplfinance._utils import _construct_pointnfig_collections

from mplfinance._utils import _updown_colors
from mplfinance._utils import IntegerIndexDateTimeFormatter

from mplfinance import _styles

from mplfinance._arg_validators import _check_and_prepare_data, _mav_validator
from mplfinance._arg_validators import _process_kwargs, _validate_vkwargs_dict
from mplfinance._arg_validators import _kwarg_not_implemented, _bypass_kwarg_validation


VALID_PMOVE_TYPES = ['renko', 'pnf', 'p&f','pointnfigure']

def with_rc_context(func):
    '''
    This decoractor creates an rcParams context around a function, so that any changes
    the function makes to rcParams will be reversed when the decorated function returns
    (therefore those changes have no effect outside of the decorated function).
    '''
    def decorator(*args, **kwargs):
        with plt.rc_context():
            return func(*args, **kwargs)
    return decorator

def _list_of_dict(x):
    return isinstance(x,list) and all([isinstance(item,dict) for item in x])

def _warn_no_xgaps_deprecated(value):
    warnings.warn('\n `no_xgaps` is deprecated:'+
                  '\n     Default value is now `no_xgaps=True`'+
                  '\n     However, to set `no_xgaps=False` and silence this warning,'+
                  '\n     use instead: `show_nontrading=True`.',
                  category=DeprecationWarning)
    return isinstance(value,bool)


def _valid_plot_kwargs():
    '''
    Construct and return the "valid kwargs table" for the mplfinance.plot() function.
    A valid kwargs table is a `dict` of `dict`s.  The keys of the outer dict are the
    valid key-words for the function.  The value for each key is a dict containing
    2 specific keys: "Default", and "Validator" with the following values:
        "Default"      - The default value for the kwarg if none is specified.
        "Validator"    - A function that takes the caller specified value for the kwarg,
                         and validates that it is the correct type, and (for kwargs with 
                         a limited set of allowed values) may also validate that the
                         kwarg value is one of the allowed values.
    '''

    vkwargs = {
        'columns'     				: { 'Default'     : ('Open', 'High', 'Low', 'Close', 'Volume'),
                          				'Validator'   : lambda value: isinstance(value, (tuple, list))
			                                                          and len(value) == 5
			                                                          and all(isinstance(c, str) for c in value) },
        'type'        				: { 'Default'     : 'ohlc',
                          				'Validator'   : lambda value: value in ['candle','candlestick','ohlc','bars','ohlc_bars','line', 'renko', 'pnf', 'p&f', 'pointnfigure'] },
 
        'style'                     : { 'Default'     : 'default',
                                        'Validator'   : lambda value: value in _styles.available_styles() or isinstance(value,dict) },
 
        'volume'                    : { 'Default'     : False,
                                        'Validator'   : lambda value: isinstance(value,bool) },
 
        'mav'                       : { 'Default'     : None,
                                        'Validator'   : _mav_validator },
        
        'renko_params'              : { 'Default'     : dict(),
                                        'Validator'   : lambda value: isinstance(value,dict) },

        'pointnfig_params'          : { 'Default'     : dict(),
                                        'Validator'   : lambda value: isinstance(value,dict) },
 
        'study'                     : { 'Default'     : None,
                                        #'Validator'   : lambda value: isinstance(value,dict) }, #{'studyname': {study parms}} example: {'TE':{'mav':20,'upper':2,'lower':2}}
                                        'Validator'   : lambda value: _kwarg_not_implemented(value) }, 
 
        'marketcolors'              : { 'Default'     : None, # use 'style' for default, instead.
                                        'Validator'   : lambda value: isinstance(value,dict) },
 
        'no_xgaps'                  : { 'Default'     : True,  # None means follow default logic below:
                                        'Validator'   : lambda value: _warn_no_xgaps_deprecated(value) },
 
        'show_nontrading'           : { 'Default'  : False, 
                                        'Validator'   : lambda value: isinstance(value,bool) },
 
        'figscale'                  : { 'Default'     : 1.0, # scale base figure size up or down.
                                        'Validator'   : lambda value: isinstance(value,float) or isinstance(value,int) },
 
        'figratio'                  : { 'Default'     : (8.00,5.75), # aspect ratio; will equal fig size when figscale=1.0
                                        'Validator'   : lambda value: isinstance(value,(tuple,list))
                                                                      and len(value) == 2
                                                                      and isinstance(value[0],(float,int))
                                                                      and isinstance(value[1],(float,int)) },
 
        'linecolor'                 : { 'Default'     : 'k', # line color in line plot
                                        'Validator'   : lambda value: mcolors.is_color_like(value) },

        'title'                     : { 'Default'     : None, # Plot Title
                                        'Validator'   : lambda value: isinstance(value,str) },
 
        'ylabel'                    : { 'Default'     : 'Price', # y-axis label
                                        'Validator'   : lambda value: isinstance(value,str) },
 
        'ylabel_lower'              : { 'Default'     : None, # y-axis label default logic below
                                        'Validator'   : lambda value: isinstance(value,str) },
 
       #'xlabel'                    : { 'Default'     : None,  # x-axis label, default is None because obvious it's time or date
       #                                'Validator'   : lambda value: isinstance(value,str) },
 
        'addplot'                   : { 'Default'     : None, 
                                        'Validator'   : lambda value: isinstance(value,dict) or (isinstance(value,list) and all([isinstance(d,dict) for d in value])) },
 
        'savefig'                   : { 'Default'     : None, 
                                        'Validator'   : lambda value: isinstance(value,dict) or isinstance(value,str) or isinstance(value, io.BytesIO) },
 
        'block'                     : { 'Default'     : True, 
                                        'Validator'   : lambda value: isinstance(value,bool) },
 
        'returnfig'                 : { 'Default'     : False, 
                                        'Validator'   : lambda value: isinstance(value,bool) },

        'return_calculated_values'  : {'Default': None,
                                       'Validator': lambda value: isinstance(value, dict) and len(value) == 0},
 
    }

    _validate_vkwargs_dict(vkwargs)

    return vkwargs



def rcParams_to_df(rcp,name=None):
    keys = []
    vals = []
    for item in rcp:
        keys.append(item)
        vals.append(rcp[item])
    df = pd.DataFrame(vals,index=pd.Index(keys,name='rcParams Key'))
    if name is not None:
        df.columns = [name]
    else:
        df.columns = ['Value']
    return df


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

    config = _process_kwargs(kwargs, _valid_plot_kwargs())
    
    dates,opens,highs,lows,closes,volumes = _check_and_prepare_data(data, config)

    if config['type'] in VALID_PMOVE_TYPES and config['addplot'] is not None:
        err = "`addplot` is not supported for `type='" + config['type'] +"'`"
        raise ValueError(err)

    style = config['style']
    if isinstance(style,str):
        style = _styles._get_mpfstyle(style)

    if isinstance(style,dict):
        _styles._apply_mpfstyle(style)
    
    w,h = config['figratio']
    r = float(w)/float(h)
    if r < 0.25 or r > 4.0:
        raise ValueError('"figratio" (aspect ratio)  must be between 0.25 and 4.0 (but is '+str(r)+')')
    base      = (w,h)
    figscale  = config['figscale']
    fsize     = [d*figscale for d in base]
    
    fig = plt.figure()
    fig.set_size_inches(fsize)

    if config['volume'] and volumes is None:
        raise ValueError('Request for volume, but NO volume data.')

    # -------------------------------------------------------------
    # For now (06-Feb-2020) to keep the code somewhat simpler for
    # implementing `secondary_y` we are going to ALWAYS create
    # secondary (twinx) axes, whether we need them or not, and 
    # then they will be available to use later when we are plotting:
    # -------------------------------------------------------------

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
        ax1 = fig.add_axes( [0.15, 0.38, 0.70, 0.50] )
        ax2 = fig.add_axes( [0.15, 0.18, 0.70, 0.20], sharex=ax1 )
        plt.xticks(rotation=45) # must do this after creation of axis, and
                                # after `sharex`, but must be BEFORE any 'twinx()'
        ax2.set_axisbelow(True) # so grid does not show through volume bars.
        ax4 = ax2.twinx()
        ax4.grid(False)
    else:
        ax1 = fig.add_axes( [0.15, 0.18, 0.70, 0.70] )
        plt.xticks(rotation=45) # must do this after creation of axis, but before any 'twinx()'
        ax2 = None
        ax4 = None
    ax3 = ax1.twinx()
    ax3.grid(False)

    avg_days_between_points = (dates[-1] - dates[0]) / float(len(dates))

    # avgerage of 3 or more data points per day we will call intraday data:
    if avg_days_between_points < 0.33:  # intraday
        if mdates.num2date(dates[-1]).date() != mdates.num2date(dates[0]).date():
            # intraday data for more than one day:
            fmtstring = '%b %d, %H:%M'
        else:  # intraday data for a single day
            fmtstring = '%H:%M'
    else:  # 'daily' data (or could be weekly, etc.)
        if mdates.num2date(dates[-1]).date().year != mdates.num2date(dates[0]).date().year:
           fmtstring = '%Y-%b-%d'
        else:
           fmtstring = '%b %d'

    ptype = config['type'] 

    if ptype not in VALID_PMOVE_TYPES:
        if config['show_nontrading']:
            formatter = mdates.DateFormatter(fmtstring)
            xdates = dates
        else:
            formatter = IntegerIndexDateTimeFormatter(dates, fmtstring)
            xdates = np.arange(len(dates))
        
        ax1.xaxis.set_major_formatter(formatter)

    collections = None
    if ptype == 'candle' or ptype == 'candlestick':
        collections = _construct_candlestick_collections(xdates, opens, highs, lows, closes,
                                                         marketcolors=style['marketcolors'] )
    elif ptype == 'ohlc' or ptype == 'bars' or ptype == 'ohlc_bars':
        collections = _construct_ohlc_collections(xdates, opens, highs, lows, closes,
                                                         marketcolors=style['marketcolors'] )
    elif ptype == 'renko':
        collections, new_dates, volumes, brick_values, size = _construct_renko_collections(dates, highs, lows, volumes, config['renko_params'], closes,
                                                         marketcolors=style['marketcolors'] )
    elif ptype == 'pnf' or ptype == 'p&f' or ptype == 'pointnfigure':
        collections, new_dates, volumes, brick_values, size = _construct_pointnfig_collections(dates, highs, lows, volumes, config['pointnfig_params'], closes,
                                                         marketcolors=style['marketcolors'] )                           
    elif ptype == 'line':
        ax1.plot(xdates, closes, color=config['linecolor'])
    else:
        raise ValueError('Unrecognized plot type = "'+ ptype + '"')

    if ptype in VALID_PMOVE_TYPES:
        formatter = IntegerIndexDateTimeFormatter(new_dates, fmtstring)
        xdates = np.arange(len(new_dates))

        ax1.xaxis.set_major_formatter(formatter)

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
            if ptype in VALID_PMOVE_TYPES:
                mavprices = pd.Series(brick_values).rolling(mav).mean().values
            else:
                mavprices = data['Close'].rolling(mav).mean().values
            if mavc:
                ax1.plot(xdates, mavprices, color=next(mavc))
            else:
                ax1.plot(xdates, mavprices)

    if config['return_calculated_values'] is not None:
        retdict = config['return_calculated_values']
        if ptype == 'renko':
            retdict['renko_bricks'] = brick_values
            retdict['renko_dates'] = mdates.num2date(new_dates)
            if config['volume']:
                retdict['renko_volumes'] = volumes
        if mavgs is not None:
            for i in range(0, len(mavgs)):
                retdict['mav' + str(mavgs[i])] = mavprices

    avg_dist_between_points = (xdates[-1] - xdates[0]) / float(len(xdates))
    minx = xdates[0]  - avg_dist_between_points
    maxx = xdates[-1] + avg_dist_between_points
    if ptype not in VALID_PMOVE_TYPES:
        miny = min([low for low in lows if low != -1])
        maxy = max([high for high in highs if high != -1])
    else:
        miny = min([brick for brick in brick_values])
        maxy = max([brick+size for brick in brick_values])
    corners = (minx, miny), (maxx, maxy)
    ax1.update_datalim(corners)

    if config['volume']:
        vup,vdown = style['marketcolors']['volume'].values()
        #-- print('vup,vdown=',vup,vdown)
        vcolors = _updown_colors(vup, vdown, opens, closes, use_prev_close=style['marketcolors']['vcdopcod'])
        #-- print('len(vcolors),len(opens),len(closes)=',len(vcolors),len(opens),len(closes))
        #-- print('vcolors=',vcolors)
        width = 0.5*avg_dist_between_points
        ax2.bar(xdates,volumes,width=width,color=vcolors)
        miny = 0.3 * min(volumes)
        maxy = 1.1 * max(volumes)
        ax2.set_ylim( miny, maxy )
        ax2.xaxis.set_major_formatter(formatter)
    
    used_ax3 = False
    used_ax4 = False
    addplot = config['addplot']
    if addplot is not None and ptype not in VALID_PMOVE_TYPES:
        # Calculate the Order of Magnitude Range
        # If addplot['secondary_y'] == 'auto', then: If the addplot['data']
        # is out of the Order of Magnitude Range, then use secondary_y.
        # Calculate omrange for Main panel, and for Lower (volume) panel:
        lo = math.log(max(math.fabs(min(lows)),1e-7),10) - 0.5
        hi = math.log(max(math.fabs(max(highs)),1e-7),10) + 0.5
        omrange = {'main' :{'lo':lo,'hi':hi},
                   'lower':None             }
        if config['volume']:
            lo = math.log(max(math.fabs(min(volumes)),1e-7),10) - 0.5
            hi = math.log(max(math.fabs(max(volumes)),1e-7),10) + 0.5
            omrange.update(lower={'lo':lo,'hi':hi})

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

            for column in apdata:
                if havedf:
                    ydata = apdata.loc[:,column]
                else:
                    ydata = column
                yd = [y for y in ydata if not math.isnan(y)]
                ymhi = math.log(max(math.fabs(max(yd)),1e-7),10)
                ymlo = math.log(max(math.fabs(min(yd)),1e-7),10)
                secondary_y = False
                if apdict['secondary_y'] == 'auto':
                    if apdict['panel'] == 'lower':
                        # If omrange['lower'] is not yet set by volume,
                        # then set it here as this is the first ydata
                        # to be plotted on the lower panel, so consider
                        # it to be the 'primary' lower panel axis.
                        if omrange['lower'] is None:
                            omrange.update(lower={'lo':ymlo,'hi':ymhi})
                        elif ymlo < omrange['lower']['lo'] or ymhi > omrange['lower']['hi']:
                            secondary_y = True
                    elif ymlo < omrange['main']['lo'] or ymhi > omrange['main']['hi']:
                        secondary_y = True
                    #   if secondary_y:
                    #       print('auto says USE secondary_y')
                    #   else:
                    #       print('auto says do NOT use secondary_y')
                else:
                    secondary_y = apdict['secondary_y']
                    #   print("apdict['secondary_y'] says secondary_y is",secondary_y)

                if apdict['panel'] == 'lower':
                    ax = ax4 if secondary_y else ax2
                else:
                    ax = ax3 if secondary_y else ax1

                if ax == ax3:
                    used_ax3 = True
                if ax == ax4:
                    used_ax4 = True

                if apdict['scatter']:
                    size  = apdict['markersize']
                    mark  = apdict['marker']
                    color = apdict['color']
                    ax.scatter(xdates, ydata, s=size, marker=mark, color=color)
                else:
                    ls    = apdict['linestyle']
                    color = apdict['color']
                    ax.plot(xdates, ydata, linestyle=ls, color=color)

    # put the twinx() on the "other" side:
    if style['y_on_right']:
        ax1.yaxis.set_label_position('right')
        ax1.yaxis.tick_right()
        ax3.yaxis.set_label_position('left')
        ax3.yaxis.tick_left()
        if ax2 and ax4:
            ax2.yaxis.set_label_position('right')
            ax2.yaxis.tick_right()
            if ax4 != ax2:
                 ax4.yaxis.set_label_position('left')
                 ax4.yaxis.tick_left()
    else:
        ax1.yaxis.set_label_position('left')
        ax1.yaxis.tick_left()
        ax3.yaxis.set_label_position('right')
        ax3.yaxis.tick_right()
        if ax2 and ax4:
            ax2.yaxis.set_label_position('left')
            ax2.yaxis.tick_left()
            if ax4 != ax2:
                ax4.yaxis.set_label_position('right')
                ax4.yaxis.tick_right()

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

    ax1.set_ylabel(config['ylabel'])

    if config['volume']:
        ax2.figure.canvas.draw()  # This is needed to calculate offset
        offset = ax2.yaxis.get_major_formatter().get_offset()
        ax2.yaxis.offsetText.set_visible(False)
        if len(offset) > 0:
            offset = (' x '+offset)
        if config['ylabel_lower'] is None:
            vol_label = 'Volume'+offset
        else:
            if len(offset) > 0:
                offset = '\n'+offset
            vol_label = config['ylabel_lower'] + offset
        ax2.set_ylabel(vol_label)

    if config['title'] is not None:
        fig.suptitle(config['title'],size='x-large',weight='semibold')

    if not used_ax3 and ax3 is not None:
        ax3.get_yaxis().set_visible(False)

    if not used_ax4 and ax4 is not None:
        ax4.get_yaxis().set_visible(False)

    if config['returnfig']:
        axlist = [ax1, ax3]
        if ax2: axlist.append(ax2)
        if ax4: axlist.append(ax4)

    if config['savefig'] is not None:
        save = config['savefig']
        if isinstance(save,dict):
            plt.savefig(**save)
        else:
            plt.savefig(save)
    elif not config['returnfig']:
        # https://stackoverflow.com/a/13361748/1639359 suggests plt.show(block=False)
        plt.show(block=config['block'])
    
    if config['returnfig']:
        return (fig, axlist)

    # rcp   = copy.deepcopy(plt.rcParams)
    # rcpdf = rcParams_to_df(rcp)
    # print('type(rcpdf)=',type(rcpdf))
    # print('rcpdfhead(3)=',rcpdf.head(3))
    # return # rcpdf


def _valid_addplot_kwargs():

    valid_linestyles = ['-','solid','--','dashed','-.','dashdot','.','dotted',None,' ','']


    vkwargs = {
        'scatter'     : { 'Default'     : False,
                          'Validator'   : lambda value: isinstance(value,bool) },

        'panel'       : { 'Default'     : 'main',
                          'Validator'   : lambda value: value in ['main','lower'] },

        'marker'      : { 'Default'     : 'o',
                          'Validator'   : lambda value: _bypass_kwarg_validation(value)  },

        'markersize'  : { 'Default'     : 18,
                          'Validator'   : lambda value: isinstance(value,(int,float)) },

        'color'       : { 'Default'     : None,
                          'Validator'   : lambda value: mcolors.is_color_like(value) },

        'linestyle'   : { 'Default'     : None,
                          'Validator'   : lambda value: value in valid_linestyles },

        'secondary_y' : { 'Default'     : 'auto',
                          'Validator'   : lambda value: isinstance(value,bool) or value == 'auto' }
    }

    _validate_vkwargs_dict(vkwargs)

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

    config = _process_kwargs(kwargs, _valid_addplot_kwargs())

    return dict( data=data, **config)
