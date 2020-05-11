import matplotlib.dates  as mdates
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import numpy  as np
import copy
import io
import math
import warnings
import statistics as stat

from itertools import cycle
#from pandas.plotting import register_matplotlib_converters
#register_matplotlib_converters()

#from mplfinance._utils import _construct_ohlc_collections
#from mplfinance._utils import _construct_candlestick_collections
#from mplfinance._utils import _construct_renko_collections
#from mplfinance._utils import _construct_pointnfig_collections
from mplfinance._utils import _construct_aline_collections
from mplfinance._utils import _construct_hline_collections
from mplfinance._utils import _construct_vline_collections
from mplfinance._utils import _construct_tline_collections
from mplfinance._utils import _construct_mpf_collections

from mplfinance._utils import _updown_colors
from mplfinance._utils import IntegerIndexDateTimeFormatter

from mplfinance import _styles

from mplfinance._arg_validators import _check_and_prepare_data, _mav_validator
from mplfinance._arg_validators import _process_kwargs, _validate_vkwargs_dict
from mplfinance._arg_validators import _kwarg_not_implemented, _bypass_kwarg_validation
from mplfinance._arg_validators import _hlines_validator, _vlines_validator
from mplfinance._arg_validators import _alines_validator, _tlines_validator

from mplfinance._panels import _determine_relative_panel_heights
from mplfinance._panels import _create_panel_axes
from mplfinance._panels import _adjust_ticklabels_per_bottom_panel
from mplfinance._panels import _adjust_ticklabels_per_bottom_panel

from mplfinance._helpers import _determine_format_string
from mplfinance._helpers import _list_of_dict

VALID_PMOVE_TYPES = ['renko', 'pnf']

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

def _warn_no_xgaps_deprecated(value):
    warnings.warn('\n\n ================================================================= '+
                  '\n\n   WARNING: `no_xgaps` is deprecated:'+
                  '\n     Default value is now `no_xgaps=True`'+
                  '\n     However, to set `no_xgaps=False` and silence this warning,'+
                  '\n     use instead: `show_nontrading=True`.'+
                  '\n\n ================================================================ ',
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
        'columns'                   : { 'Default'     : ('Open', 'High', 'Low', 'Close', 'Volume'),
                                        'Validator'   : lambda value: isinstance(value, (tuple, list))
                                                                   and len(value) == 5
                                                                   and all(isinstance(c, str) for c in value) },
        'type'                      : { 'Default'     : 'ohlc',
                                        'Validator'   : lambda value: value in ('candle','candlestick','ohlc','ohlc_bars',
                                                                                'line','renko','pnf') },
 
        'style'                     : { 'Default'     : 'default',
                                        'Validator'   : lambda value: value in _styles.available_styles() or isinstance(value,dict) },
 
        'volume'                    : { 'Default'     : False,
                                        'Validator'   : lambda value: isinstance(value,bool) or value in ['B','C'] },
 
        'mav'                       : { 'Default'     : None,
                                        'Validator'   : _mav_validator },
        
        'renko_params'              : { 'Default'     : dict(),
                                        'Validator'   : lambda value: isinstance(value,dict) },

        'pnf_params'                : { 'Default'     : dict(),
                                        'Validator'   : lambda value: isinstance(value,dict) },
 
        'study'                     : { 'Default'     : None,
                                        'Validator'   : lambda value: _kwarg_not_implemented(value) }, 
 
        'marketcolors'              : { 'Default'     : None, # use 'style' for default, instead.
                                        'Validator'   : lambda value: isinstance(value,dict) },
 
        'no_xgaps'                  : { 'Default'     : True,  # None means follow default logic below:
                                        'Validator'   : lambda value: _warn_no_xgaps_deprecated(value) },
 
        'show_nontrading'           : { 'Default'     : False, 
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

        'set_ylim'                  : {'Default': None,
                                       'Validator': lambda value: isinstance(value, (list,tuple)) and len(value) == 2 
                                                                  and all([isinstance(v,(int,float)) for v in value])},
 
        'set_ylim_panelB'           : {'Default': None,
                                       'Validator': lambda value: isinstance(value, (list,tuple)) and len(value) == 2 
                                                                  and all([isinstance(v,(int,float)) for v in value])},
 
        'set_ylim_panelC'           : {'Default': None,
                                       'Validator': lambda value: isinstance(value, (list,tuple)) and len(value) == 2 
                                                                  and all([isinstance(v,(int,float)) for v in value])},
 
        'hlines'                    : { 'Default'     : None, 
                                        'Validator'   : lambda value: _hlines_validator(value) },
 
        'vlines'                    : { 'Default'     : None, 
                                        'Validator'   : lambda value: _vlines_validator(value) },

        'alines'                    : { 'Default'     : None, 
                                        'Validator'   : lambda value: _alines_validator(value) },
 
        'tlines'                    : { 'Default'     : None, 
                                        'Validator'   : lambda value: _tlines_validator(value) },
       
        'panel_order'               : { 'Default'     : 'ABC', 
                                        'Validator'   : lambda value: isinstance(value,str) and len(value) == 3 and
                                                                     (('A' in value and 'B' in value and 'C' in value) or 
                                                                      ('a' in value and 'b' in value and 'c' in value))},

        'panel_ratio'               : { 'Default'     : (5,2,2),
                                        'Validator'   : lambda value: isinstance(value,(tuple,list)) and len(value) == 3 and
                                                                      all([isinstance(v,(int,float)) for v in value]) },

        'datetime_format'           : { 'Default'     : None,
                                        'Validator'   : lambda value: isinstance(value,str) },

        'xrotation'                 : { 'Default'     : 45,
                                        'Validator'   : lambda value: isinstance(value,(int,float)) },

        'axesoff'                   : { 'Default'     : False,
                                        'Validator'   : lambda value: isinstance(value,bool) },

        'axesoffdark'               : { 'Default'     : False,
                                        'Validator'   : lambda value: isinstance(value,bool) },
    }

    _validate_vkwargs_dict(vkwargs)

    return vkwargs


@with_rc_context
def plot( data, **kwargs ):
    """
    Given a Pandas DataFrame containing columns Open,High,Low,Close and optionally Volume
    with a DatetimeIndex, plot the data.
    Available plots include ohlc bars, candlestick, and line plots.
    Also provide visually analysis in the form of common technical studies, such as:
    moving averages, renko, etc.
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

    if config['volume']:
        if config['volume'] not in ['B','C']: config['volume'] = 'B'

    ha,hb,hc = _determine_relative_panel_heights(config['addplot'],
                                                 config['volume'] ,
                                                 config['panel_ratio'])

    axA1,axA2,axB1,axB2,axC1,axC2,actual_order = _create_panel_axes( fig, ha, hb, hc, config['panel_order'] )

    if config['volume'] == 'B':
        volumeAxes = axB1
    elif config['volume'] == 'C':
        volumeAxes = axC1
    else:
       volumeAxes = None

    fmtstring = _determine_format_string( dates, config['datetime_format'] )

    ptype = config['type'] 

    if config['show_nontrading']:
        formatter = mdates.DateFormatter(fmtstring)
        xdates = dates
    else:
        formatter = IntegerIndexDateTimeFormatter(dates, fmtstring)
        xdates = np.arange(len(dates))
    axA1.xaxis.set_major_formatter(formatter)

    collections = None
    if ptype == 'line':
        axA1.plot(xdates, closes, color=config['linecolor'])
    else:
        collections =_construct_mpf_collections(ptype,dates,xdates,opens,highs,lows,closes,volumes,config,style)

    if ptype in VALID_PMOVE_TYPES:
        collections, new_dates, volumes, brick_values, size = collections
        formatter = IntegerIndexDateTimeFormatter(new_dates, fmtstring)
        xdates = np.arange(len(new_dates))
        axA1.xaxis.set_major_formatter(formatter)

    if collections is not None:
        for collection in collections:
            axA1.add_collection(collection)

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
                mavprices = pd.Series(closes).rolling(mav).mean().values
            if mavc:
                axA1.plot(xdates, mavprices, color=next(mavc))
            else:
                axA1.plot(xdates, mavprices)

    avg_dist_between_points = (xdates[-1] - xdates[0]) / float(len(xdates))
    minx = xdates[0]  - avg_dist_between_points
    maxx = xdates[-1] + avg_dist_between_points
    if len(xdates) == 1:  # kludge special case
        minx = minx - 0.75
        maxx = maxx + 0.75
    if ptype not in VALID_PMOVE_TYPES:
        _lows  = [low for low in lows if low != -1]
        _highs = [high for high in highs if high != -1]
    else:
        _lows  = [brick for brick in brick_values]
        _highs = [brick+size for brick in brick_values]

    miny = min(_lows)
    maxy = max(_highs)
    #if len(xdates) > 1:
    #   stdy = (stat.stdev(_lows) + stat.stdev(_highs)) / 2.0
    #else:  # kludge special case
    #   stdy = 0.02 * math.fabs(maxy - miny)
    # print('minx,miny,maxx,maxy,stdy=',minx,miny,maxx,maxy,stdy)

    if config['set_ylim'] is not None:
        axA1.set_ylim(config['set_ylim'][0], config['set_ylim'][1])
    else:
       corners = (minx, miny), (maxx, maxy)
       axA1.update_datalim(corners)

    if config['return_calculated_values'] is not None:
        retdict = config['return_calculated_values']
        if ptype in VALID_PMOVE_TYPES:
            prekey = ptype
            retdict[prekey+'_bricks'] = brick_values
            retdict[prekey+'_dates'] = mdates.num2date(new_dates)
            retdict[prekey+'_size'] = size
            if config['volume']:
                retdict[prekey+'_volumes'] = volumes
        if mavgs is not None:
            for i in range(0, len(mavgs)):
                retdict['mav' + str(mavgs[i])] = mavprices
        retdict['minx'] = minx
        retdict['maxx'] = maxx
        retdict['miny'] = miny
        retdict['maxy'] = maxy

    # Note: these are NOT mutually exclusive, so the order of this
    #       if/elif is important: VALID_PMOVE_TYPES must be first.
    if ptype in VALID_PMOVE_TYPES:
        dtix = pd.DatetimeIndex([dt for dt in mdates.num2date(new_dates)])
    elif not config['show_nontrading']:
        dtix = data.index
    else:
        dtix = None

    line_collections = []
    line_collections.append(_construct_aline_collections(config['alines'], dtix))
    line_collections.append(_construct_hline_collections(config['hlines'], minx, maxx))
    line_collections.append(_construct_vline_collections(config['vlines'], dtix, miny, maxy))
    tlines = config['tlines']
    if isinstance(tlines,(list,tuple)) and all([isinstance(item,dict) for item in tlines]):
        pass
    else:
        tlines = [tlines,]
    for tline_item in tlines:
        line_collections.append(_construct_tline_collections(tline_item, dtix, dates, opens, highs, lows, closes))
     
    for collection in line_collections:
        if collection is not None:
            axA1.add_collection(collection)

    if config['volume']:
        vup,vdown = style['marketcolors']['volume'].values()
        #-- print('vup,vdown=',vup,vdown)
        vcolors = _updown_colors(vup, vdown, opens, closes, use_prev_close=style['marketcolors']['vcdopcod'])
        #-- print('len(vcolors),len(opens),len(closes)=',len(vcolors),len(opens),len(closes))
        #-- print('vcolors=',vcolors)
        width = 0.5*avg_dist_between_points
        volumeAxes.bar(xdates,volumes,width=width,color=vcolors)
        miny = 0.3 * min(volumes)
        maxy = 1.1 * max(volumes)
        volumeAxes.set_ylim( miny, maxy )

    xrotation = config['xrotation']
    _adjust_ticklabels_per_bottom_panel(axA1,axB1,axC1,actual_order,hb,hc,formatter,xrotation)

    used_axA2 = False
    used_axB2 = False
    used_axC2 = False
    addplot = config['addplot']
    if addplot is not None and ptype not in VALID_PMOVE_TYPES:
        # Calculate the Order of Magnitude Range
        # If addplot['secondary_y'] == 'auto', then: If the addplot['data']
        # is out of the Order of Magnitude Range, then use secondary_y.
        # Calculate omrange for Main panel, and for Lower (volume) panel:
        lo = math.log(max(math.fabs(min(lows)),1e-7),10) - 0.5
        hi = math.log(max(math.fabs(max(highs)),1e-7),10) + 0.5

        # May 2020: Main panel is now called 'A', and Lower is called 'B'
        omrange = {'A' : {'lo':lo,'hi':hi},
                   'B' : None             ,
                   'C' : None             }
        if config['volume']:
            lo = math.log(max(math.fabs(min(volumes)),1e-7),10) - 0.5
            hi = math.log(max(math.fabs(max(volumes)),1e-7),10) + 0.5
            omrange.update(B={'lo':lo,'hi':hi})

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
                    if apdict['panel'] == 'lower' or apdict['panel'] == 'B':
                        # If omrange['lower'] is not yet set by volume,
                        # then set it here as this is the first ydata
                        # to be plotted on the lower panel, so consider
                        # it to be the 'primary' lower panel axis.
                        if omrange['B'] is None:
                            omrange.update(B={'lo':ymlo,'hi':ymhi})
                        elif ymlo < omrange['B']['lo'] or ymhi > omrange['B']['hi']:
                            secondary_y = True
                    elif apdict['panel'] == 'C':
                        if omrange['C'] is None:
                            omrange.update(B={'lo':ymlo,'hi':ymhi})
                        elif ymlo < omrange['C']['lo'] or ymhi > omrange['C']['hi']:
                            secondary_y = True
                    elif ymlo < omrange['A']['lo'] or ymhi > omrange['A']['hi']:
                        secondary_y = True
                    #   if secondary_y:
                    #       print('auto says USE secondary_y')
                    #   else:
                    #       print('auto says do NOT use secondary_y')
                else:
                    secondary_y = apdict['secondary_y']
                    #   print("apdict['secondary_y'] says secondary_y is",secondary_y)

                if apdict['panel'] == 'lower' or apdict['panel'] == 'B' :
                    ax = axB2 if secondary_y else axB1
                elif apdict['panel'] == 'C' :
                    ax = axC2 if secondary_y else axC1
                else:
                    ax = axA2 if secondary_y else axA1

                if ax == axA2:
                    used_axA2 = True
                if ax == axB2:
                    used_axB2 = True
                if ax == axC2:
                    used_axC2 = True

                aptype = apdict['type']
                if aptype == 'scatter':
                    size  = apdict['markersize']
                    mark  = apdict['marker']
                    color = apdict['color']
                    # -------------------------------------------------------- #
                    # This fixes Issue#77, but breaks other stuff:
                    # ax.set_ylim(ymin=(miny - 0.4*stdy),ymax=(maxy + 0.4*stdy))
                    # -------------------------------------------------------- #
                    ax.scatter(xdates, ydata, s=size, marker=mark, color=color)
                elif aptype == 'bar':
                    width  = apdict['width']
                    bottom = apdict['bottom']
                    color  = apdict['color']
                    alpha  = apdict['alpha']
                    ax.bar(xdates, ydata, width=width, bottom=bottom, color=color, alpha=alpha)
                elif aptype == 'line':
                    ls    = apdict['linestyle']
                    color = apdict['color']
                    ax.plot(xdates, ydata, linestyle=ls, color=color)
                #elif aptype == 'ohlc' or aptype == 'candle':
                # This won't work as is, because here we are looping through one column at a time
                # and mpf_collections needs ohlc columns:
                #    collections =_construct_mpf_collections(aptype,dates,xdates,opens,highs,lows,closes,volumes,config,style)
                #    if len(collections) == 1: collections = [collections]
                #    for collection in collections:
                #        ax.add_collection(collection)
                else:
                    raise ValueError('addplot type "'+str(aptype)+'" NOT yet supported.')

    if config['set_ylim_panelB'] is not None:
        miny = config['set_ylim_panelB'][0]
        maxy = config['set_ylim_panelB'][1]
        axB1.set_ylim( miny, maxy )

    if config['set_ylim_panelC'] is not None:
        miny = config['set_ylim_panelC'][0]
        maxy = config['set_ylim_panelC'][1]
        axC1.set_ylim( miny, maxy )

    # put the twinx() on the "other" side:
    if style['y_on_right']:
        axA1.yaxis.set_label_position('right')
        axA1.yaxis.tick_right()
        axA2.yaxis.set_label_position('left')
        axA2.yaxis.tick_left()
        if axB1 and axB2:
            axB1.yaxis.set_label_position('right')
            axB1.yaxis.tick_right()
            if axB2 != axB1:
                 axB2.yaxis.set_label_position('left')
                 axB2.yaxis.tick_left()
    else:
        axA1.yaxis.set_label_position('left')
        axA1.yaxis.tick_left()
        axA2.yaxis.set_label_position('right')
        axA2.yaxis.tick_right()
        if axB1 and axB2:
            axB1.yaxis.set_label_position('left')
            axB1.yaxis.tick_left()
            if axB2 != axB1:
                axB2.yaxis.set_label_position('right')
                axB2.yaxis.tick_right()

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

    axA1.autoscale_view()  # Is this really necessary??

    axA1.set_ylabel(config['ylabel'])

    if config['volume']:
        volumeAxes.figure.canvas.draw()  # This is needed to calculate offset
        offset = volumeAxes.yaxis.get_major_formatter().get_offset()
        volumeAxes.yaxis.offsetText.set_visible(False)
        if len(offset) > 0:
            offset = (' x '+offset)
        if config['ylabel_lower'] is None:
            vol_label = 'Volume'+offset
        else:
            if len(offset) > 0:
                offset = '\n'+offset
            vol_label = config['ylabel_lower'] + offset
        volumeAxes.set_ylabel(vol_label)

    if config['title'] is not None:
        fig.suptitle(config['title'],size='x-large',weight='semibold')

    if not used_axA2 and axA2 is not None:
        axA2.get_yaxis().set_visible(False)

    if not used_axB2 and axB2 is not None:
        axB2.get_yaxis().set_visible(False)

    if not used_axC2 and axC2 is not None:
        axC2.get_yaxis().set_visible(False)

    axlist = [axA1, axA2]
    if axB1: axlist.append(axB1)
    if axB2: axlist.append(axB2)
    if axC1: axlist.append(axC1)
    if axC2: axlist.append(axC2)

    if config['axesoffdark']: fig.patch.set_facecolor('black')
    if config['axesoff']: fig.patch.set_visible(False)
    if config['axesoffdark'] or config['axesoff']:
        for ax in axlist:
            ax.set_xlim(xdates[0],xdates[-1])
            ax.set_axis_off()

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

    valid_linestyles = ('-','solid','--','dashed','-.','dashdot','.','dotted',None,' ','')
    #valid_types = ('line','scatter','bar','ohlc','candle')
    valid_types = ('line','scatter','bar')

    vkwargs = {
        'scatter'     : { 'Default'     : False,
                          'Validator'   : lambda value: isinstance(value,bool) },

        'type'        : { 'Default'     : 'line',
                          'Validator'   : lambda value: value in valid_types },

        'panel'       : { 'Default'     : 'A',   # new: use 'A' for 'main', 'B' for 'lower'
                          'Validator'   : lambda value: value in ('A','B','C','main','lower') },

        'marker'      : { 'Default'     : 'o',
                          'Validator'   : lambda value: _bypass_kwarg_validation(value)  },

        'markersize'  : { 'Default'     : 18,
                          'Validator'   : lambda value: isinstance(value,(int,float)) },

        'color'       : { 'Default'     : None,
                          'Validator'   : lambda value: mcolors.is_color_like(value) },

        'linestyle'   : { 'Default'     : None,
                          'Validator'   : lambda value: value in valid_linestyles },

        'width'       : { 'Default'     : 0.8,
                          'Validator'   : lambda value: isinstance(value,(int,float)) or
                                                        all([isinstance(v,(int,float)) for v in value]) },

        'bottom'      : { 'Default'     : 0,
                          'Validator'   : lambda value: isinstance(value,(int,float)) or
                                                        all([isinstance(v,(int,float)) for v in value]) },
        'alpha'       : { 'Default'     : 1,
                          'Validator'   : lambda value: isinstance(value,(int,float)) or
                                                        all([isinstance(v,(int,float)) for v in value]) },

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

    # kwarg `type` replaces kwarg `scatter`
    if config['scatter'] == True and config['type'] == 'line':
        config['type'] = 'scatter'

    return dict( data=data, **config)
