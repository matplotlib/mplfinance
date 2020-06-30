"""
Some helper functions for mplfinance.
"""

import datetime
import matplotlib.dates as mdates
import numpy as np

def _adjust_color_brightness(color,amount=0.5):
    
    def _adjcb(c1, amount):
        import matplotlib.colors as mc
        import colorsys
        # mc.is_color_like(value)
        try:
            c = mc.cnames[c1]
        except:
            c = c1
        c = colorsys.rgb_to_hls(*mc.to_rgb(c))
        return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

    if not isinstance(color,(list,tuple)):
        return _adjcb(color,amount)
        
    cout = []
    cadj = {}
    for c1 in color:
        if c1 in cadj:
            cout.append(cadj[c1])
        else:
            newc = _adjcb(c1,amount)
            cadj[c1] = newc
            cout.append(cadj[c1])
    return cout


def _determine_format_string( dates, datetime_format=None ):
    """
    Determine the datetime format string based on the averge number
    of days between data points, or if the user passed in kwarg
    datetime_format, use that as an override.
    """
    avg_days_between_points = (dates[-1] - dates[0]) / float(len(dates))

    if datetime_format is not None:
        return datetime_format

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
    return fmtstring


def _list_of_dict(x):
    '''
    Return True if x is a list of dict's
    '''
    return isinstance(x,list) and all([isinstance(item,dict) for item in x])

def _num_or_seq_of_num(value):
    return ( isinstance(value,(int,float))  or
             (isinstance(value,(list,tuple,np.ndarray)) and
              all([isinstance(v,(int,float)) for v in value]))
           )

def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time lapse in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt is None : dt = datetime.datetime.now()
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)
