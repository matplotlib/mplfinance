'''
__init__ for mplfinance._styledata module
'''

from mplfinance._styledata import default
from mplfinance._styledata import nightclouds
from mplfinance._styledata import classic
from mplfinance._styledata import mike
from mplfinance._styledata import charles
from mplfinance._styledata import blueskies
from mplfinance._styledata import starsandstripes
from mplfinance._styledata import sas
from mplfinance._styledata import brasil
from mplfinance._styledata import yahoo
from mplfinance._styledata import checkers
from mplfinance._styledata import binance

_style_names = [n for n in dir() if not n.startswith('_')]

_styles = {}
for name in _style_names:
    cmd = f'_styles.update({name} = {name}.style)'
    eval(cmd)

def _validate_style(style):
    keys = ['base_mpl_style','marketcolors','mavcolors','y_on_right',
            'gridcolor','gridstyle','facecolor','rc' ]
    for key in keys:
        if key not in style.keys():
            err = f'Key "{key}" not found in style:\n\n    {style}'
            raise ValueError(err)
    
    mktckeys = ['candle','edge','wick','ohlc','volume','alpha']
    for key in mktckeys:
        if key not in style['marketcolors'].keys():
            err = f'Key "{key}" not found in marketcolors for style:\n\n    {style}'
            raise ValueError(err)

#print('type(_styles)=',type(_styles))
#print('_styles=',_styles)
for s in _styles.keys():
    _validate_style(_styles[s])

