import matplotlib.dates  as mdates
import pandas   as pd
import numpy    as np
import datetime

def _check_and_prepare_data(data, config):
    '''
    Check and Prepare the data input:
    For now, data must be a Pandas DataFrame with a DatetimeIndex
    and columns named 'Open', 'High', 'Low', 'Close', and optionally 'Volume'

    Later (if there is demand for it) we may accept all of the following data formats:
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

    o, h, l, c, v = config["columns"]
    cols = [o, h, l, c]

    dates   = mdates.date2num(data.index.to_pydatetime())
    opens   = data[o].values
    highs   = data[h].values
    lows    = data[l].values
    closes  = data[c].values
    if v in data.columns:
        volumes = data[v].values
        cols.append(v)
    else:
        volumes = None

    for col in cols:
        if not all( isinstance(v,(float,int)) for v in data[col] ):
            raise ValueError('Data for column "'+str(col)+'" must be ALL float or int.')

    return dates, opens, highs, lows, closes, volumes


def _mav_validator(mav_value):
    ''' 
    Value for mav (moving average) keyword may be:
    scalar int greater than 1, or tuple of ints, or list of ints (greater than 1).
    tuple or list limited to length of 7 moving averages (to keep the plot clean).
    '''
    if isinstance(mav_value,int) and mav_value > 1:
        return True
    elif not isinstance(mav_value,tuple) and not isinstance(mav_value,list):
        return False

    if not len(mav_value) < 8:
        return False
    for num in mav_value:
        if not isinstance(num,int) and num > 1:
            return False
    return True

def _hlines_validator(value):
    return ( isinstance(value,(float,int)) or (isinstance(value,(list,tuple)) and
             all([isinstance(v,(float,int)) for v in value])) )

def _is_datelike(value):
    if isinstance(value, (pd.Timestamp,datetime.datetime,datetime.date)):
        return True
    if isinstance(value,str):
        try:
            dt = pd.to_datetime(value)
            return True
        except:
            return False
    return False

def _vlines_validator(value):
    '''Validate `vlines` kwarg value:  must be "datelike" or sequence of "datelike"
    '''
    if _is_datelike(value): return True
    if not isinstance(value,(list,tuple)): return False
    if not all([_is_datelike(v) for v in value]): return False
    return True

def _lines_validator(value):
    '''
    Value for segments to be passed into LineCollection constructor must be:
    - a sequence of `lines`, where
    - a `lines` is a sequence of 2 or more vertices, where
    - a vertex is a `pair`, aka a sequence of two values, an x and a y point.

    From matplotlib.collections:
        `segments` are:
        A sequence of (line0, line1, line2), where:

        linen = (x0, y0), (x1, y1), ... (xm, ym)
       
        or the equivalent numpy array with two columns. Each line can be a different length.
    '''
    if not isinstance(value,(list,tuple)):
        return False
    if not all([isinstance(line,(list,tuple)) and len(line) > 1 for line in value]):
        return False
    #point_list = [point for line in value for point in line]
    #print('point_list=',point_list)
    if not all([isinstance(point,(list,tuple)) and len(point)==2 for line in value for point in line]):
        return False
    return True

def _bypass_kwarg_validation(value):
    ''' For some kwargs, we either don't know enough, or
        the validation is too complex to make it worth while,
        so we bypass kwarg validation.  If the kwarg is 
        invalid, then eventually an exception will be 
        raised at the time the kwarg value is actually used.
    '''
    return True

def _kwarg_not_implemented(value):
    ''' If you want to list a kwarg in a valid_kwargs dict for a given
        function, but you have not yet, or don't yet want to, implement
        the kwarg; or you simply want to (temporarily) disable the kwarg,
        then use this function as the kwarg validator
    '''
    raise NotImplementedError('kwarg NOT implemented.')

def _validate_vkwargs_dict(vkwargs):
    # Check that we didn't make a typo in any of the things
    # that should be the same for all vkwargs dict items:
    for key, value in vkwargs.items():
        if len(value) != 2:
            raise ValueError('Items != 2 in valid kwarg table, for kwarg "'+key+'"')
        if 'Default' not in value:
            raise ValueError('Missing "Default" value for kwarg "'+key+'"')
        if 'Validator' not in value:
            raise ValueError('Missing "Validator" function for kwarg "'+key+'"')

def _process_kwargs(kwargs, vkwargs):
    '''
    Given a "valid kwargs table" and some kwargs, verify that each key-word
    is valid per the kwargs table, and that the value of the kwarg is the
    correct type.  Fill a configuration dictionary with the default value
    for each kwarg, and then substitute in any values that were provided 
    as kwargs and return the configuration dictionary.
    '''
    # initialize configuration from valid_kwargs_table:
    config  = {}
    for key, value in vkwargs.items():
        config[key] = value['Default']

    # now validate kwargs, and for any valid kwargs
    #  replace the appropriate value in config:
    for key in kwargs.keys():
        if key not in vkwargs:
            raise KeyError('Unrecognized kwarg="'+str(key)+'"')
        else:
            value = kwargs[key]
            try:
                valid = vkwargs[key]['Validator'](value)
            except Exception as ex:
                ex.extra_info = 'kwarg "'+key+'" validator raised exception to value: "'+str(value)+'"'
                raise
            if not valid:
                import inspect
                v = inspect.getsource(vkwargs[key]['Validator']).strip()
                raise TypeError('kwarg "'+key+'" validator returned False for value: "'+str(value)+'"\n    '+v)

       # ---------------------------------------------------------------
       #  At this point in the loop, if we have not raised an exception,
       #      then kwarg is valid as far as we can tell, therefore, 
       #      go ahead and replace the appropriate value in config:

        config[key] = value

    return config
