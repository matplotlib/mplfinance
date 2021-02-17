"""
A collection of utilities for analyzing and plotting financial data.
"""

import numpy  as np
import pandas as pd
import matplotlib.dates as mdates
import datetime

from itertools import cycle

from matplotlib             import colors as mcolors
from matplotlib.patches     import Ellipse
from matplotlib.collections import LineCollection, PolyCollection, PatchCollection

from mplfinance._arg_validators import _process_kwargs, _validate_vkwargs_dict
from mplfinance._arg_validators import _alines_validator, _bypass_kwarg_validation
from mplfinance._styles         import _get_mpfstyle

from six.moves import zip

def _check_input(opens, closes, highs, lows):
    """Checks that *opens*, *highs*, *lows* and *closes* have the same length.
    NOTE: this code assumes if any value open, high, low, close is
    missing (*-1*) they all are missing

    Parameters
    ----------
    opens : sequence
        sequence of opening values
    highs : sequence
        sequence of high values
    lows : sequence
        sequence of low values
    closes : sequence
        sequence of closing values

    Raises
    ------
    ValueError
        if the input sequences don't have the same length
        if the input sequences don't have NaN is same locations
    """
    same_length = len(opens) == len(highs) == len(lows) == len(closes)
    if not same_length:
        raise ValueError('O,H,L,C must have the same length!')

    o = np.where(np.isnan(opens))[0]
    h = np.where(np.isnan(highs))[0]
    l = np.where(np.isnan(lows))[0]
    c = np.where(np.isnan(closes))[0]

    # First check that they have the same number of NaN:
    same_numnans = len(o) == len(h) == len(l) == len(c)
    if not same_numnans:
        raise ValueError('O,H,L,C must have the same amount of missing data!')

    same_missing = ((o == h).all() and
                    (o == l).all() and
                    (o == c).all()
                   )
    if not same_missing:
        raise ValueError('O,H,L,C must have the same missing data!')

def _construct_mpf_collections(ptype,dates,xdates,opens,highs,lows,closes,volumes,config,style):
    collections = None
    if ptype == 'candle' or ptype == 'candlestick':
        collections = _construct_candlestick_collections(xdates, opens, highs, lows, closes,
                                                         marketcolors=style['marketcolors'],config=config )

    elif ptype =='hollow_and_filled':
            collections = _construct_hollow_candlestick_collections(xdates, opens, highs, lows, closes,
                                                         marketcolors=style['marketcolors'],config=config )

    elif ptype == 'ohlc' or ptype == 'bars' or ptype == 'ohlc_bars':
        collections = _construct_ohlc_collections(xdates, opens, highs, lows, closes,
                                                  marketcolors=style['marketcolors'],config=config )
    elif ptype == 'renko':
        collections = _construct_renko_collections(
            dates, highs, lows, volumes, config['renko_params'], closes, marketcolors=style['marketcolors'])

    elif ptype == 'pnf':
        collections = _construct_pointnfig_collections(
            dates, highs, lows, volumes, config['pnf_params'], closes, marketcolors=style['marketcolors'])
    else:
        raise TypeError('Unknown ptype="',str(ptype),'"')
     
    return collections


def _calculate_atr(atr_length, highs, lows, closes):
    """Calculate the average true range
    atr_length : time period to calculate over
    all_highs : list of highs
    all_lows : list of lows
    all_closes : list of closes
    """
    if atr_length < 1:
        raise ValueError("Specified atr_length may not be less than 1")
    elif atr_length >= len(closes):
        raise ValueError("Specified atr_length is larger than the length of the dataset: " + str(len(closes)))
    atr = 0
    for i in range(len(highs)-atr_length, len(highs)):
        high = highs[i]
        low = lows[i]
        close_prev = closes[i-1]
        tr = max(abs(high-low), abs(high-close_prev), abs(low-close_prev))
        atr += tr
    return atr/atr_length

def combine_adjacent(arr):
    """Sum like signed adjacent elements
    arr : starting array

    Returns
    -------
    output: new summed array
    indexes: indexes indicating the first 
             element summed for each group in arr
    """
    output, indexes = [], []
    curr_i = 0
    while len(arr) > 0:
        curr_sign = arr[0]/abs(arr[0])
        index = 0
        while index < len(arr) and arr[index]/abs(arr[index]) == curr_sign:
            index += 1
        output.append(sum(arr[:index]))
        indexes.append(curr_i)
        curr_i += index
        
        for _ in range(index):
            arr.pop(0)
    return output, indexes

def coalesce_volume_dates(in_volumes, in_dates, indexes):
    """Sums volumes between the indexes and ouputs
    dates at the indexes
    in_volumes : original volume list
    in_dates : original dates list
    indexes : list of indexes

    Returns
    -------
    volumes: new volume array
    dates: new dates array
    """
    volumes, dates = [], []
    for i in range(len(indexes)):
        dates.append(in_dates[indexes[i]])
        to_sum_to = indexes[i+1] if i+1 < len(indexes) else len(in_volumes)
        volumes.append(sum(in_volumes[indexes[i]:to_sum_to]))
    return volumes, dates


def _updown_colors(upcolor,downcolor,opens,closes,use_prev_close=False):
    if upcolor == downcolor:
        return upcolor
    cmap = {True : upcolor, False : downcolor}
    if not use_prev_close:
        return [ cmap[opn < cls] for opn,cls in zip(opens,closes) ]
    else:
        first = cmap[opens[0] < closes[0]] 
        _list = [ cmap[pre < cls] for cls,pre in zip(closes[1:], closes) ]
        return [first] + _list


def _updownhollow_colors(upcolor,downcolor,hollowcolor,opens,closes):
    if upcolor == downcolor:
        return upcolor
    umap = {True : hollowcolor, False : upcolor  }
    dmap = {True : hollowcolor, False : downcolor}
    first = umap[closes[0] > opens[0]]
    _list = [ umap[cls > opn] if cls > cls0 else dmap[cls > opn] for cls0,opn,cls in zip(closes[0:-1],opens[1:],closes[1:]) ]
    return [first] + _list


def _date_to_iloc(dtseries,date):
    d1s = dtseries.loc[date:]
    if len(d1s) < 1:
        sdtrange = str(dtseries[0])+' to '+str(dtseries[-1])
        raise ValueError('User specified line date "'+str(date)+'" is beyond (greater than) range of plotted data ('+sdtrange+').')
    d1 = d1s.index[0]
    d2s = dtseries.loc[:date]
    if len(d2s) < 1:
        sdtrange = str(dtseries[0])+' to '+str(dtseries[-1])
        raise ValueError('User specified line date "'+str(date)+'" is before (less than) range of plotted data ('+sdtrange+').')
    d2 = dtseries.loc[:date].index[-1]
    # If there are duplicate dates in the series, for example in a renko plot
    # then .get_loc(date) will return a slice containing all the dups, so:
    loc1 = dtseries.index.get_loc(d1)
    if isinstance(loc1,slice): loc1 = loc1.start
    loc2 = dtseries.index.get_loc(d2)
    if isinstance(loc2,slice): loc2 = loc2.stop - 1
    return (loc1+loc2)/2.0

def _date_to_mdate(date):
    if isinstance(date,str):
        pydt = pd.to_datetime(date).to_pydatetime()
    elif isinstance(date,pd.Timestamp):
        pydt = date.to_pydatetime()
    elif isinstance(date,(datetime.datetime,datetime.date)):
        pydt = date
    else:
        return None
    return mdates.date2num(pydt)

def _convert_segment_dates(segments,dtindex):
    '''
    Convert line segment dates to matplotlib dates 
    Inputted segment dates may be: pandas-parseable date-time string, pandas timestamp,
                                   or a python datetime or date, or (if dtindex is not None) integer index
    A "segment" is a "sequence of lines",
        see: https://matplotlib.org/api/collections_api.html#matplotlib.collections.LineCollection
    '''
    #import pdb
    #pdb.set_trace()
    if dtindex is not None:
        dtseries = dtindex.to_series()
    converted = []
    for line in segments:
        new_line = []
        for dt,value in line:
            if dtindex is not None:
                date = _date_to_iloc(dtseries,dt)  
            else:
                date = _date_to_mdate(dt)
            if date is None:
                raise TypeError('NON-DATE in segment line='+str(line))
            new_line.append((date,value))
        converted.append(new_line)
    return converted

def _valid_renko_kwargs():
    '''
    Construct and return the "valid renko kwargs table" for the mplfinance.plot(type='renko') 
    function. A valid kwargs table is a `dict` of `dict`s. The keys of the outer dict are 
    the valid key-words for the function.  The value for each key is a dict containing 2 
    specific keys: "Default", and "Validator" with the following values:
        "Default"      - The default value for the kwarg if none is specified.
        "Validator"    - A function that takes the caller specified value for the kwarg,
                         and validates that it is the correct type, and (for kwargs with 
                         a limited set of allowed values) may also validate that the
                         kwarg value is one of the allowed values.
    '''
    vkwargs = {
        'brick_size'  : { 'Default'     : 'atr',
                          'Validator'   : lambda value: isinstance(value,(float,int)) or value == 'atr' },
        'atr_length'  : { 'Default'     : 14,
                          'Validator'   : lambda value: isinstance(value,int) or value == 'total' },               
    }

    _validate_vkwargs_dict(vkwargs)

    return vkwargs

def _valid_pnf_kwargs():
    '''
    Construct and return the "valid pnf kwargs table" for the mplfinance.plot(type='pnf') 
    function. A valid kwargs table is a `dict` of `dict`s. The keys of the outer dict are 
    the valid key-words for the function.  The value for each key is a dict containing 2 
    specific keys: "Default", and "Validator" with the following values:
        "Default"      - The default value for the kwarg if none is specified.
        "Validator"    - A function that takes the caller specified value for the kwarg,
                         and validates that it is the correct type, and (for kwargs with 
                         a limited set of allowed values) may also validate that the
                         kwarg value is one of the allowed values.
    '''
    vkwargs = {
        'box_size'    : { 'Default'     : 'atr',
                          'Validator'   : lambda value: isinstance(value,(float,int)) or value == 'atr' },
        'atr_length'  : { 'Default'     : 14,
                          'Validator'   : lambda value: isinstance(value,int) or value == 'total' },               
    }

    _validate_vkwargs_dict(vkwargs)

    return vkwargs

def _valid_lines_kwargs():
    '''
    Construct and return the "valid lines (hlines,vlines,alines,tlines) kwargs table" 
    for the mplfinance.plot() `[h|v|a|t]lines=` kwarg functions.
    A valid kwargs table is a `dict` of `dict`s. The keys of the outer dict are 
    the valid key-words for the function.  The value for each key is a dict containing 2 
    specific keys: "Default", and "Validator" with the following values:
        "Default"      - The default value for the kwarg if none is specified.
        "Validator"    - A function that takes the caller specified value for the kwarg,
                         and validates that it is the correct type, and (for kwargs with 
                         a limited set of allowed values) may also validate that the
                         kwarg value is one of the allowed values.
    '''
    valid_linestyles = ['-','solid','--','dashed','-.','dashdot',':','dotted',None,' ','']
    vkwargs = {
        'hlines'    : { 'Default'     : None,
                        'Validator'   : _bypass_kwarg_validation },
        'vlines'    : { 'Default'     : None,
                        'Validator'   : _bypass_kwarg_validation },
        'alines'    : { 'Default'     : None,
                        'Validator'   : _bypass_kwarg_validation },
        'tlines'    : { 'Default'     : None,
                        'Validator'   : _bypass_kwarg_validation },
        'colors'    : { 'Default'     : None,
                        'Validator'   : lambda value: value is None or
                                            mcolors.is_color_like(value) or
                                            ( isinstance(value,(list,tuple)) and
                                              all([mcolors.is_color_like(v) for v in value]) ) },
        'linestyle' : { 'Default'     : '-',
                        'Validator'   : lambda value: value is None or value in valid_linestyles },
        'linewidths': { 'Default'     : None,
                        'Validator'   : lambda value: value is None or
                                            isinstance(value,(float,int)) or 
                                            all([isinstance(v,(float,int)) for v in value]) },
        'alpha'     : { 'Default'     : 1.0,
                        'Validator'   : lambda value: isinstance(value,(float,int)) },

        'tline_use' : { 'Default'     : 'close', 
                        'Validator'   : lambda value: isinstance(value,str) or (isinstance(value,(list,tuple)) and
                                                                      all([isinstance(v,str) for v in value]) ) },
        'tline_method': { 'Default'   : 'point-to-point',
                          'Validator' : lambda value: value in ['point-to-point','least-squares'] }
    }

    _validate_vkwargs_dict(vkwargs)

    return vkwargs


def _construct_ohlc_collections(dates, opens, highs, lows, closes, marketcolors=None, config=None):
    """Represent the time, open, high, low, close as a vertical line
    ranging from low to high.  The left tick is the open and the right
    tick is the close.
    *opens*, *highs*, *lows* and *closes* must have the same length.
    NOTE: this code assumes if any value open, high, low, close is
    missing (*-1*) they all are missing

    Parameters
    ----------
    opens : sequence
        sequence of opening values
    highs : sequence
        sequence of high values
    lows : sequence
        sequence of low values
    closes : sequence
        sequence of closing values
    marketcolors : dict of colors: 'up', 'down'

    Returns
    -------
    ret : list 
        a list or tuple of matplotlib collections to be added to the axes
    """

    _check_input(opens, highs, lows, closes)

    if marketcolors is None:
        mktcolors = _get_mpfstyle('classic')['marketcolors']['ohlc']
        #print('default mktcolors=',mktcolors)
    else:
        mktcolors = marketcolors['ohlc']

    rangeSegments = [((dt, low), (dt, high)) for dt, low, high in zip(dates, lows, highs)]

    datalen = len(dates)

    avg_dist_between_points = (dates[-1] - dates[0]) / float(datalen)

    ticksize = config['_width_config']['ohlc_ticksize']

    # the ticks will be from ticksize to 0 in points at the origin and
    # we'll translate these to the date, open location
    openSegments = [((dt-ticksize, op), (dt, op)) for dt, op in zip(dates, opens)]

    # the ticks will be from 0 to ticksize in points at the origin and
    # we'll translate these to the date, close location
    closeSegments = [((dt, close), (dt+ticksize, close)) for dt, close in zip(dates, closes)]

    if mktcolors['up'] == mktcolors['down']:
        colors = mktcolors['up']
    else:
        colorup = mcolors.to_rgba(mktcolors['up'])
        colordown = mcolors.to_rgba(mktcolors['down'])
        colord = {True: colorup, False: colordown}
        colors = [colord[open < close] for open, close in zip(opens, closes)]

    lw = config['_width_config']['ohlc_linewidth']

    rangeCollection = LineCollection(rangeSegments,
                                     colors=colors,
                                     linewidths=lw,
                                     )

    openCollection = LineCollection(openSegments,
                                    colors=colors,
                                    linewidths=lw,
                                    )

    closeCollection = LineCollection(closeSegments,
                                     colors=colors,
                                     linewidths=lw
                                     )

    return [rangeCollection, openCollection, closeCollection]


def _construct_candlestick_collections(dates, opens, highs, lows, closes, marketcolors=None, config=None):
    """Represent the open, close as a bar line and high low range as a
    vertical line.

    NOTE: this code assumes if any value open, low, high, close is
    missing they all are missing


    Parameters
    ----------
    opens : sequence
        sequence of opening values
    highs : sequence
        sequence of high values
    lows : sequence
        sequence of low values
    closes : sequence
        sequence of closing values
    marketcolors : dict of colors: up, down, edge, wick, alpha
    alpha : float
        bar transparency

    Returns
    -------
    ret : list
        (lineCollection, barCollection)
    """
    
    _check_input(opens, highs, lows, closes)

    if marketcolors is None:
        marketcolors = _get_mpfstyle('classic')['marketcolors']
        #print('default market colors:',marketcolors)

    datalen = len(dates)

    avg_dist_between_points = (dates[-1] - dates[0]) / float(datalen)

    delta = config['_width_config']['candle_width'] / 2.0

    barVerts = [((date - delta, open),
                 (date - delta, close),
                 (date + delta, close),
                 (date + delta, open))
                for date, open, close in zip(dates, opens, closes)]

    rangeSegLow   = [((date, low), (date, min(open,close)))
                     for date, low, open, close in zip(dates, lows, opens, closes)]
    
    rangeSegHigh  = [((date, high), (date, max(open,close)))
                     for date, high, open, close in zip(dates, highs, opens, closes)]
                      
    rangeSegments = rangeSegLow + rangeSegHigh

    alpha  = marketcolors['alpha']

    uc     = mcolors.to_rgba(marketcolors['candle'][ 'up' ], alpha)
    dc     = mcolors.to_rgba(marketcolors['candle']['down'], alpha)
    colors = _updown_colors(uc, dc, opens, closes)

    uc     = mcolors.to_rgba(marketcolors['edge'][ 'up' ], 1.0)
    dc     = mcolors.to_rgba(marketcolors['edge']['down'], 1.0)
    edgecolor = _updown_colors(uc, dc, opens, closes)
    
    uc     = mcolors.to_rgba(marketcolors['wick'][ 'up' ], 1.0)
    dc     = mcolors.to_rgba(marketcolors['wick']['down'], 1.0)
    wickcolor = _updown_colors(uc, dc, opens, closes)

    lw = config['_width_config']['candle_linewidth']

    rangeCollection = LineCollection(rangeSegments,
                                     colors=wickcolor,
                                     linewidths=lw,
                                     )

    barCollection = PolyCollection(barVerts,
                                   facecolors=colors,
                                   edgecolors=edgecolor,
                                   linewidths=lw
                                   )

    return [rangeCollection, barCollection]


def _construct_hollow_candlestick_collections(dates, opens, highs, lows, closes, marketcolors=None, config=None):
    """Represent today's open to close as a "bar" line (candle body)
    and high low range as a vertical line (candle wick)
     
    If config['type']=='hollow_and_filled' (hollow and filled candles) then candle edge and
    wick color depend on PREVIOUS close to today's close (up or down), and the center of the
    candle body (hollow or filled) depends on the today's open to close (up or down).

    NOTE: this code assumes if any value open, low, high, close is
    missing they all are missing

    Parameters
    ----------
    opens : sequence
        sequence of opening values
    highs : sequence
        sequence of high values
    lows : sequence
        sequence of low values
    closes : sequence
        sequence of closing values
    marketcolors : dict of colors: up, down, edge, wick, alpha
    alpha : float
        bar (candle body) transparency

    Returns
    -------
    ret : list
        (lineCollection, barCollection)
    """
    
    _check_input(opens, highs, lows, closes)

    if marketcolors is None:
        marketcolors = _get_mpfstyle('classic')['marketcolors']
        #print('default market colors:',marketcolors)

    datalen = len(dates)

    avg_dist_between_points = (dates[-1] - dates[0]) / float(datalen)

    delta = config['_width_config']['candle_width'] / 2.0

    barVerts = [((date - delta, open),
                 (date - delta, close),
                 (date + delta, close),
                 (date + delta, open))
                for date, open, close in zip(dates, opens, closes)]

    rangeSegLow   = [((date, low), (date, min(open,close)))
                     for date, low, open, close in zip(dates, lows, opens, closes)]
    
    rangeSegHigh  = [((date, high), (date, max(open,close)))
                     for date, high, open, close in zip(dates, highs, opens, closes)]
                      
    rangeSegments = rangeSegLow + rangeSegHigh

    alpha  = marketcolors['alpha']

    uc     = mcolors.to_rgba(marketcolors['candle'][ 'up' ], alpha)
    dc     = mcolors.to_rgba(marketcolors['candle']['down'], alpha)
   
    hc = mcolors.to_rgba(marketcolors['hollow']) if 'hollow' in marketcolors else (0,0,0,0)
    
    colors = _updownhollow_colors(uc, dc, hc, opens, closes)  # for candle body.

    edgecolor = _updown_colors(uc, dc, opens, closes, use_prev_close=True)
    
    wickcolor = _updown_colors(uc, dc, opens, closes, use_prev_close=True)

    # For hollow candles, we scale the candle linewidth up a little:
    lw = 1.25 * config['_width_config']['candle_linewidth']

    rangeCollection = LineCollection(rangeSegments,
                                     colors=wickcolor,
                                     linewidths=lw,
                                     )

    barCollection = PolyCollection(barVerts,
                                   facecolors=colors,
                                   edgecolors=edgecolor,
                                   linewidths=lw
                                   )

    return [rangeCollection, barCollection]


def _construct_renko_collections(dates, highs, lows, volumes, config_renko_params, closes, marketcolors=None):
    """Represent the price change with bricks

    NOTE: this code assumes if any value open, low, high, close is
    missing they all are missing

    Algorithm Explanation
    ---------------------
    In the first part of the algorithm, we populate the cdiff array
    along with adjusting the dates and volumes arrays into the new_dates and
    new_volumes arrays. A single date includes a range from no bricks to many 
    bricks, if a date has no bricks it shall not be included in new_dates, 
    and if it has n bricks then it will be included n times. Volumes use a 
    volume cache to save volume amounts for dates that do not have any bricks
    before adding the cache to the next date that has at least one brick.
    We populate the cdiff array with each close values difference from the 
    previously created brick divided by the brick size.

    In the second part of the algorithm, we iterate through the values in cdiff
    and add 1s or -1s to the bricks array depending on whether the value is 
    positive or negative. Every time there is a trend change (ex. previous brick is
    an upbrick, current brick is a down brick) we draw one less brick to account
    for the price having to move the previous bricks amount before creating a 
    brick in the opposite direction.

    In the final part of the algorithm, we enumerate through the bricks array and
    assign up-colors or down-colors to the associated index in the color array and
    populate the verts list with each bricks vertice to be used to create the matplotlib
    PolyCollection.

    Useful sources:
    https://avilpage.com/2018/01/how-to-plot-renko-charts-with-python.html
    https://school.stockcharts.com/doku.php?id=chart_analysis:renko
    
    Parameters
    ----------
    dates : sequence
        sequence of dates
    highs : sequence
        sequence of high values
    lows : sequence
        sequence of low values
    config_renko_params : kwargs table (dictionary)
        brick_size : size of each brick
        atr_length : length of time used for calculating atr
    closes : sequence
        sequence of closing values
    marketcolors : dict of colors: up, down, edge, wick, alpha

    Returns
    -------
    ret : list
        rectCollection
    """
    renko_params = _process_kwargs(config_renko_params, _valid_renko_kwargs())
    if marketcolors is None:
        marketcolors = _get_mpfstyle('classic')['marketcolors']
        #print('default market colors:',marketcolors)
    
    brick_size = renko_params['brick_size']
    atr_length = renko_params['atr_length']
    

    if brick_size == 'atr':
        if atr_length == 'total':
            brick_size = _calculate_atr(len(closes)-1, highs, lows, closes)
        else:
            brick_size = _calculate_atr(atr_length, highs, lows, closes)
    else: # is an integer or float
        upper_limit = (max(closes) - min(closes)) / 2
        lower_limit = 0.01 * _calculate_atr(len(closes)-1, highs, lows, closes)
        if brick_size > upper_limit:
            raise ValueError("Specified brick_size may not be larger than (50% of the close price range of the dataset) which has value: "+ str(upper_limit))
        elif brick_size < lower_limit:
            raise ValueError("Specified brick_size may not be smaller than (0.01* the Average True Value of the dataset) which has value: "+ str(lower_limit))

    alpha  = marketcolors['alpha']

    uc     = mcolors.to_rgba(marketcolors['candle'][ 'up' ], alpha)
    dc     = mcolors.to_rgba(marketcolors['candle']['down'], alpha)
    euc    = mcolors.to_rgba(marketcolors['edge'][ 'up' ], 1.0)
    edc    = mcolors.to_rgba(marketcolors['edge']['down'], 1.0)
    
    cdiff = [] # holds the differences between each close and the previously created brick / the brick size
    prev_close_brick = closes[0]
    volume_cache = 0 # holds the volumes for the dates that were skipped
    new_dates = [] # holds the dates corresponding with the index
    new_volumes = [] # holds the volumes corresponding with the index.  If more than one index for the same day then they all have the same volume.

    for i in range(len(closes)-1):
        brick_diff = int((closes[i+1] - prev_close_brick) / brick_size)
        if brick_diff == 0:
            if volumes is not None:
                volume_cache += volumes[i]
            continue

        cdiff.extend([int(brick_diff/abs(brick_diff))] * abs(brick_diff))
        if volumes is not None:
            new_volumes.extend([volumes[i] + volume_cache] * abs(brick_diff))
            volume_cache = 0
        new_dates.extend([dates[i]] * abs(brick_diff))
        prev_close_brick += brick_diff *brick_size

    bricks = [] # holds bricks, -1 for down bricks, 1 for up bricks
    curr_price = closes[0]

    last_diff_sign = 0 # direction the bricks were last going in -1 -> down, 1 -> up
    dates_volumes_index = 0 # keeps track of the index of the current date/volume
    for diff in cdiff:
        
        curr_diff_sign = diff/abs(diff)
        if last_diff_sign != 0 and curr_diff_sign != last_diff_sign:
            last_diff_sign = curr_diff_sign
            new_dates.pop(dates_volumes_index)
            if volumes is not None:
                if dates_volumes_index == len(new_volumes)-1:
                    new_volumes[dates_volumes_index-1] += new_volumes[dates_volumes_index]
                else:
                    new_volumes[dates_volumes_index+1] += new_volumes[dates_volumes_index]
                new_volumes.pop(dates_volumes_index)
            continue
        last_diff_sign = curr_diff_sign
    
        if diff > 0:
            bricks.extend([1]*abs(diff))
        else:
            bricks.extend([-1]*abs(diff))
        dates_volumes_index += 1


    verts = [] # holds the brick vertices
    colors = [] # holds the facecolors for each brick
    edge_colors = [] # holds the edgecolors for each brick
    brick_values = [] # holds the brick values for each brick
    for index, number in enumerate(bricks):
        if number == 1: # up brick
            colors.append(uc)
            edge_colors.append(euc)
        else: # down brick
            colors.append(dc)
            edge_colors.append(edc)

        curr_price += (brick_size * number)
        brick_values.append(curr_price)
        
        x, y = index, curr_price

        verts.append((
            (x, y),
            (x, y+brick_size),
            (x+1, y+brick_size),
            (x+1, y)))

    useAA = 0,    # use tuple here
    lw = None
    rectCollection = PolyCollection(verts,
                                    facecolors=colors,
                                    antialiaseds=useAA,
                                    edgecolors=edge_colors,
                                    linewidths=lw
                                    )
    return [rectCollection,], new_dates, new_volumes, brick_values, brick_size


def _construct_pointnfig_collections(dates, highs, lows, volumes, config_pointnfig_params, closes, marketcolors=None):
    """Represent the price change with Xs and Os

    NOTE: this code assumes if any value open, low, high, close is
    missing they all are missing

    Algorithm Explanation
    ---------------------
    In the first part of the algorithm, we populate the boxes array
    along with adjusting the dates and volumes arrays into the new_dates and
    new_volumes arrays. A single date includes a range from no boxes to many 
    boxes, if a date has no boxes it shall not be included in new_dates, 
    and if it has n boxes then it will be included n times. Volumes use a 
    volume cache to save volume amounts for dates that do not have any boxes
    before adding the cache to the next date that has at least one box.
    We populate the boxes array with each close values difference from the 
    previously created brick divided by the box size.

    The second part of the algorithm has a series of step. First we combine the
    adjacent like signed values in the boxes array (ex. [-1, -2, 3, -4] -> [-3, 3, -4]).
    Next we subtract 1 from the absolute value of each element in boxes except the 
    first to ensure every time there is a trend change (ex. previous box is
    an X, current brick is a O) we draw one less box to account for the price 
    having to move the previous box's amount before creating a box in the 
    opposite direction. Next we adjust volume and dates to combine volume into 
    non 0 box indexes and to only use dates from non 0 box indexes. We then
    remove all 0s from the boxes array and once again combine adjacent similarly
    signed differences in boxes.

    Lastly, we enumerate through the boxes to populate the line_seg and circle_patches
    arrays. line_seg holds the / and \ line segments that make up an X and 
    circle_patches holds matplotlib.patches Ellipse objects for each O. We start
    by filling an x and y array each iteration which contain the x and y 
    coordinates for each box in the column. Then for each coordinate pair in
    x, y we add to either the line_seg array or the circle_patches array 
    depending on the value of sign for the current column (1 indicates 
    line_seg, -1 indicates circle_patches). The height of the boxes take 
    into account padding which separates each box by a small margin in 
    order to increase readability.

    Useful sources:
    https://stackoverflow.com/questions/8750648/point-and-figure-chart-with-matplotlib
    https://www.investopedia.com/articles/technical/03/081303.asp
    
    Parameters
    ----------
    dates : sequence
        sequence of dates
    highs : sequence
        sequence of high values
    lows : sequence
        sequence of low values
    config_pointnfig_params : kwargs table (dictionary)
        box_size : size of each box
        atr_length : length of time used for calculating atr
    closes : sequence
        sequence of closing values
    marketcolors : dict of colors: up, down, edge, wick, alpha

    Returns
    -------
    ret : tuple
        rectCollection
    """
    pointnfig_params = _process_kwargs(config_pointnfig_params, _valid_pnf_kwargs())
    if marketcolors is None:
        marketcolors = _get_mpfstyle('classic')['marketcolors']
        #print('default market colors:',marketcolors)
    
    box_size = pointnfig_params['box_size']
    atr_length = pointnfig_params['atr_length']

    if box_size == 'atr':
        if atr_length == 'total':
            box_size = _calculate_atr(len(closes)-1, highs, lows, closes)
        else:
            box_size = _calculate_atr(atr_length, highs, lows, closes)
    else: # is an integer or float
        upper_limit = (max(closes) - min(closes)) / 2
        lower_limit = 0.01 * _calculate_atr(len(closes)-1, highs, lows, closes)
        if box_size > upper_limit:
            raise ValueError("Specified box_size may not be larger than (50% of the close price range of the dataset) which has value: "+ str(upper_limit))
        elif box_size < lower_limit:
            raise ValueError("Specified box_size may not be smaller than (0.01* the Average True Value of the dataset) which has value: "+ str(lower_limit))

    alpha  = marketcolors['alpha']

    uc     = mcolors.to_rgba(marketcolors['ohlc'][ 'up' ], alpha)
    dc     = mcolors.to_rgba(marketcolors['ohlc']['down'], alpha)
    tfc    = mcolors.to_rgba(marketcolors['edge']['down'], 0) # transparent face color

    boxes = [] # each element in an integer representing the number of boxes to be drawn on that indexes column (negative numbers -> Os, positive numbers -> Xs)
    prev_close_box = closes[0] # represents the value of the last box in the previous column
    volume_cache = 0 # holds the volumes for the dates that were skipped
    temp_volumes, temp_dates = [], [] # holds the temp adjusted volumes and dates respectively
    
    for i in range(len(closes)-1):
        box_diff = int((closes[i+1] - prev_close_box) / box_size)
        if box_diff == 0:
            if volumes is not None:
                volume_cache += volumes[i]
            continue

        boxes.append(box_diff)
        if volumes is not None:
            temp_volumes.append(volumes[i] + volume_cache)
            volume_cache = 0
        temp_dates.append(dates[i])
        prev_close_box += box_diff *box_size

    # combine adjacent similarly signed differences
    boxes, indexes = combine_adjacent(boxes)
    new_volumes, new_dates = coalesce_volume_dates(temp_volumes, temp_dates, indexes)
    
    #subtract 1 from the abs of each diff except the first to account for the first box using the last box in the opposite direction
    first_elem = boxes[0]
    boxes = [boxes[i]- int((boxes[i]/abs(boxes[i]))) for i in range(1, len(boxes))]
    boxes.insert(0, first_elem)

    # adjust volume and dates to make sure volume is combined into non 0 box indexes and only use dates from non 0 box indexes
    temp_volumes, temp_dates = [], []
    for i in range(len(boxes)):
        if boxes[i] == 0:
            volume_cache += new_volumes[i]
        else:
            temp_volumes.append(new_volumes[i] + volume_cache)
            volume_cache = 0
            temp_dates.append(new_dates[i])
    
    #remove 0s from boxes
    boxes = list(filter(lambda diff: diff != 0, boxes))

    # combine adjacent similarly signed differences again after 0s removed
    boxes, indexes = combine_adjacent(boxes)
    new_volumes, new_dates = coalesce_volume_dates(temp_volumes, temp_dates, indexes)

    curr_price = closes[0]
    box_values = [] # y values for the boxes
    circle_patches = [] # list of circle patches to be used to create the cirCollection
    line_seg = [] # line segments that make up the Xs
    
    for index, difference in enumerate(boxes):
        diff = abs(difference)

        sign = (difference / abs(difference)) # -1 or 1
        start_iteration = 0 if sign > 0 else 1
        
        x = [index] * (diff)
        y = [curr_price + (i * box_size * sign) for i in range(start_iteration, diff+start_iteration)]
        
        curr_price += (box_size * sign * (diff))
        box_values.append(sum(y) / len(y))
        
        for i in range(len(x)): # x and y have the same length
            height = box_size * 0.85
            width = 0.6
            if height < 0.5:
                width = height
            
            padding = (box_size * 0.075)
            if sign == 1: # X
                line_seg.append([(x[i]-width/2, y[i] + padding), (x[i]+width/2, y[i]+height + padding)]) # create / part of the X
                line_seg.append([(x[i]-width/2, y[i]+height+padding), (x[i]+width/2, y[i]+padding)]) # create \ part of the X
            else: # O
                circle_patches.append(Ellipse((x[i], y[i]-(height/2) - padding), width, height))
    
    useAA = 0,    # use tuple here
    lw = 0.5        

    cirCollection = PatchCollection(circle_patches)
    cirCollection.set_facecolor([tfc] * len(circle_patches))
    cirCollection.set_edgecolor([dc] * len(circle_patches))
    
    xCollection = LineCollection(line_seg,
                                 colors=[uc] * len(line_seg),
                                 linewidths=lw,
                                 antialiaseds=useAA
                                 )
    return [cirCollection, xCollection], new_dates, new_volumes, box_values, box_size


def _construct_aline_collections(alines, dtix=None):
    """construct arbitrary line collections

    Parameters
    ----------
    alines : sequence
        sequences of segments, which are sequences of lines,
        which are sequences of two or more points ( date[time], price ) or (x,y) 

        date[time] may be (a) pandas.to_datetime parseable string,
                          (b) pandas Timestamp, or
                          (c) python datetime.datetime or datetime.date

    alines may also be a dict, containing
    the following keys:

        'alines'     : the same as defined above: sequence of price, or dates, or segments
        'colors'     : colors for the above alines
        'linestyle'  : line types for the above alines
        'linewidths' : line types for the above alines

    dtix:  date index for the x-axis, used for converting the dates when
           x-values are 'evenly spaced integers' (as when skipping non-trading days)

    Returns
    -------
    ret : list
        lines collections
    """
    if alines is None:
        return None

    if isinstance(alines,dict):
        aconfig = _process_kwargs(alines, _valid_lines_kwargs())
        alines = aconfig['alines']
    else:
        aconfig = _process_kwargs({}, _valid_lines_kwargs())

    #print('aconfig=',aconfig)
    #print('alines=',alines)

    alines = _alines_validator(alines, returnStandardizedValue=True)
    if alines is None:
        raise ValueError('Unable to standardize alines value: '+str(alines))

    alines = _convert_segment_dates(alines,dtix)

    lw = aconfig['linewidths']
    co = aconfig['colors']
    ls = aconfig['linestyle']
    al = aconfig['alpha']
    lcollection = LineCollection(alines,colors=co,linewidths=lw,linestyles=ls,antialiaseds=(0,),alpha=al)
    return lcollection


def _construct_hline_collections(hlines,minx,maxx):
    """Construct horizontal lines collection

    Parameters
    ----------
    hlines : sequence
        sequence of [price] values at which to draw horizontal lines

    hlines may also be a dict, containing
    the following keys:

        'hlines'     : the same as defined above: sequence of price, or dates, or segments
        'colors'     : colors for the above hlines
        'linestyle'  : line types for the above hlines
        'linewidths' : line types for the above hlines

    minx : the minimum value for x for the horizontal line, already converted to `xdates` format
    maxx : the maximum value for x for the horizontal line, already converted to `xdates` format

    Returns
    -------
    ret : list
        lines collections
    """

    if hlines is None:
        return None

    #print('_construct_hline_collections() called:',
    #      '\nhlines=',hlines,'\nminx,maxx=',minx,maxx)

    # hlines do NOT require converting segment dates, because the dates
    # are not user-specified, but are from already converted minxdt,maxxdt

    if isinstance(hlines,dict):
        hconfig = _process_kwargs(hlines, _valid_lines_kwargs())
        hlines = hconfig['hlines']
    else:
        hconfig = _process_kwargs({}, _valid_lines_kwargs())

    #print('hconfig=',hconfig)
    #print('hlines=',hlines)
    
    lines = []
    if not isinstance(hlines,(list,tuple)):
        hlines = [hlines,] # may be a single price value

    for val in hlines:
        lines.append( [(minx,val),(maxx,val)] )

    lw = hconfig['linewidths']
    co = hconfig['colors']
    ls = hconfig['linestyle']
    al = hconfig['alpha']
    lcollection = LineCollection(lines,colors=co,linewidths=lw,linestyles=ls,antialiaseds=(0,),alpha=al)
    return lcollection


def _construct_vline_collections(vlines,dtix,miny,maxy):
    """Construct vertical lines collection
    Parameters
    ----------
    vlines : sequence
        sequence of dates or datetimes at which to draw vertical lines
        dates/datetimes may be (a) pandas.to_datetime parseable string,
                               (b) pandas Timestamp
                               (c) python datetime.datetime or datetime.date

    vlines may also be a dict, containing
    the following keys:

        'vlines'     : the same as defined above: sequence of dates/datetimes
        'colors'     : colors for the above vlines
        'linestyle'  : line types for the above vlines
        'linewidths' : line types for the above vlines

    dtix:  date index for the x-axis, used for converting the dates when
           x-values are 'evenly spaced integers' (as when skipping non-trading days)

    miny : minimum y-value for the vertical line

    maxy : maximum y-value for the vertical line

    Returns
    -------
    ret : list
        lines collections
    """

    if vlines is None:
        return None

    #print('_construct_vline_collections() called:',
    #      '\nvlines=',vlines,
    #      '\ndtix=',dtix)
    #print('miny,maxy=',miny,maxy)

    if isinstance(vlines,dict):
        vconfig = _process_kwargs(vlines, _valid_lines_kwargs())
        vlines = vconfig['vlines']
    else:
        vconfig = _process_kwargs({}, _valid_lines_kwargs())

    #print('vconfig=',vconfig)
    #print('vlines=',vlines)
    
    if not isinstance(vlines,(list,tuple)):
        vlines = [vlines,]

    lines = []
    for val in vlines:
        lines.append( [(val,miny),(val,maxy)] )

    lines = _convert_segment_dates(lines,dtix)

    lw = vconfig['linewidths']
    co = vconfig['colors']
    ls = vconfig['linestyle']
    al = vconfig['alpha']
    lcollection = LineCollection(lines,colors=co,linewidths=lw,linestyles=ls,antialiaseds=(0,),alpha=al)
    return lcollection

def _construct_tline_collections(tlines, dtix, dates, opens, highs, lows, closes):
    """construct trend line collections

    Parameters
    ----------
    tlines : sequence
        sequences of pairs of date[time]s

        date[time] may be (a) pandas.to_datetime parseable string,
                          (b) pandas Timestamp, or
                          (c) python datetime.datetime or datetime.date

    tlines may also be a dict, containing
    the following keys:

        'tlines'     : the same as defined above: sequence of pairs of date[time]s
        'colors'     : colors for the above tlines
        'linestyle'  : line types for the above tlines
        'linewidths' : line types for the above tlines

    dtix:  date index for the x-axis, used for converting the dates when
           x-values are 'evenly spaced integers' (as when skipping non-trading days)

    Returns
    -------
    ret : list
        lines collections
    """
    if tlines is None:
        return None

    if isinstance(tlines,dict):
        tconfig = _process_kwargs(tlines, _valid_lines_kwargs())
        tlines  = tconfig['tlines']
    else:
        tconfig = _process_kwargs({}, _valid_lines_kwargs())

    tline_use    = tconfig['tline_use']
    tline_method = tconfig['tline_method']

    #print('tconfig=',tconfig)
    #print('tlines=',tlines)

    # reconstruct the data frame:
    df = pd.DataFrame({'open':opens,'high':highs,'low':lows,'close':closes},
                      index=pd.DatetimeIndex(mdates.num2date(dates))   )

    # possible `tvalue`s : close,open,high,low,oc_avg,hl_avg,ohlc_avg,hilo
    #          'hilo' means high on the up trend, low on the down trend.
    # possible `tmethod`s: point-to-point, leastsquares

    def _tline_point_to_point(dfslice,tline_use):
        p1 = dfslice.iloc[ 0]
        p2 = dfslice.iloc[-1]
        x1 = p1.name
        y1 = p1[tline_use].mean()
        x2 = p2.name
        y2 = p2[tline_use].mean()
        return ((x1,y1),(x2,y2))

    def _tline_lsq(dfslice,tline_use):
        '''
        This closed-form linear least squares algorithm was taken from:
        https://mmas.github.io/least-squares-fitting-numpy-scipy
        '''
        si = dfslice[tline_use].mean(axis=1)
        s  = si.dropna() 
        if len(s) < 2:
            err = 'NOT enough data for Least Squares'
            if (len(si) > 2):
                err += ', due to presence of NaNs'
            raise ValueError(err)
        xs = mdates.date2num(s.index.to_pydatetime())
        ys = s.values
        a  = np.vstack([xs, np.ones(len(xs))]).T
        m, b  = np.dot(np.linalg.inv(np.dot(a.T,a)), np.dot(a.T,ys))
        x1, x2 = xs[0], xs[-1]
        y1 = m*x1 + b
        y2 = m*x2 + b
        x1, x2 = mdates.num2date(x1), mdates.num2date(x2)
        return ((x1,y1),(x2,y2))

    if isinstance(tline_use,str):
        tline_use = [tline_use,]
    tline_use = [ u.lower() for u in tline_use ]

    alines = []
    for d1,d2 in tlines:
        dfslice = df.loc[d1:d2]
        if len(dfslice) < 2:
            dfdr = '\ndf date range: ['+str(df.index[0])+' , '+str(df.index[-1])+']'
            raise ValueError('\ntlines date pair ('+str(d1)+','+str(d2)+
                             ') too close, or wrong order, or out of range!'+dfdr)
        if tline_method == 'least squares' or tline_method == 'least-squares':
            p1,p2 = _tline_lsq(dfslice,tline_use)
        elif tline_method == 'point-to-point':
            p1,p2 = _tline_point_to_point(dfslice,tline_use)
        else:
            raise ValueError('\nUnrecognized value for `tline_method` = "'+str(tline_method)+'"')

        alines.append((p1,p2))

    del tconfig['alines']
    alines = dict(alines=alines,**tconfig) 
    alines['tlines'] = None

    return _construct_aline_collections(alines, dtix)


from matplotlib.ticker import Formatter
class IntegerIndexDateTimeFormatter(Formatter):
    """
    Formatter for axis that is indexed by integer, where the integers
    represent the index location of the datetime object that should be
    formatted at that lcoation.  This formatter is used typically when
    plotting datetime on an axis but the user does NOT want to see gaps
    where days (or times) are missing.  To use: plot the data against
    a range of integers equal in length to the array of datetimes that
    you would otherwise plot on that axis.  Construct this formatter
    by providing the arrange of datetimes (as matplotlib floats). When
    the formatter receives an integer in the range, it will look up the
    datetime and format it.  

    """
    def __init__(self, dates, fmt='%b %d, %H:%M'):
        self.dates = dates
        self.len   = len(dates)
        self.fmt   = fmt

    def __call__(self, x, pos=0):
        #import pdb; pdb.set_trace()
        'Return label for time x at position pos'
        # not sure what 'pos' is for: see
        # https://matplotlib.org/gallery/ticks_and_spines/date_index_formatter.html
        ix = int(np.round(x))
         
        if ix >= self.len or ix < 0:
            date = None
            dateformat = ''
        else:
            date = self.dates[ix]
            dateformat = mdates.num2date(date).strftime(self.fmt)
        #print('x=',x,'pos=',pos,'dates[',ix,']=',date,'dateformat=',dateformat)
        return dateformat

def _mscatter(x,y,ax=None, m=None, **kw):
    import matplotlib.markers as mmarkers
    if not ax: ax=plt.gca()
    sc = ax.scatter(x,y,**kw)
    if (m is not None) and (len(m)==len(x)):
        paths = []
        for marker in m:
            if isinstance(marker, mmarkers.MarkerStyle):
                marker_obj = marker
            else:
                marker_obj = mmarkers.MarkerStyle(marker)
            path = marker_obj.get_path().transformed(
                        marker_obj.get_transform())
            paths.append(path)
        sc.set_paths(paths)
    return sc
