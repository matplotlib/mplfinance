import matplotlib.dates  as mdates
import pandas as pd
import numpy  as np

def _check_and_prepare_data(data):
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

def _validate_vkwargs_dict(vkwargs):
    # Check that we didn't make a typo in any of the things
    # that should be the same for all vkwargs dict items:
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
