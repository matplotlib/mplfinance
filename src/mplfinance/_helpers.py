"""
Some helper functions for mplfinance.
"""

import matplotlib.dates as mdates
import numpy as np

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

def _valid_panel_id(panid):
    return panid in ['main','lower'] or (isinstance(panid,int) and panid >= 0 and panid < 10)
