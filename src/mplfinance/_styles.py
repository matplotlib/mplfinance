import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import copy

from   mplfinance._arg_validators import _process_kwargs, _validate_vkwargs_dict
from   mplfinance._styledata      import _styles


def _get_mpfstyle(style):
    ''' 
    Return a copy of the specified pre-defined mpfstyle.  We return
    a copy, because returning the original will effectively return 
    a pointer which allows style's definition to be modified.
    '''
    return copy.deepcopy(_styles[style])

def _apply_mpfstyle(style):

    plt.style.use('default')

    if style['base_mpl_style'] is not None:
        plt.style.use(style['base_mpl_style']) 

    if style['rc'] is not None:
        plt.rcParams.update(style['rc'])

    if style['facecolor'] is not None:
        plt.rcParams.update({'axes.facecolor' : style['facecolor'] })

    if 'edgecolor' in style and style['edgecolor'] is not None:
        plt.rcParams.update({'axes.edgecolor' : style['edgecolor'] })

    if 'figcolor' in style and style['figcolor'] is not None:
        plt.rcParams.update({'figure.facecolor' : style['figcolor'] })
        plt.rcParams.update({'savefig.facecolor': style['figcolor'] })

    explicit_grid = False
    if style['gridcolor'] is not None:
        explicit_grid = True
        plt.rcParams.update({'grid.color' : style['gridcolor'] })

    if style['gridstyle'] is not None:
        explicit_grid = True
        plt.rcParams.update({'grid.linestyle' : style['gridstyle'] })

    plt.rcParams.update({'axes.grid.axis' : 'both' })
    if 'gridaxis' in style and style['gridaxis'] is not None:
        gax = style['gridaxis']
        explicit_grid = True
        if gax == 'horizontal'[0:len(gax)]:
            plt.rcParams.update({'axes.grid.axis' : 'y' })
        elif gax == 'vertical'[0:len(gax)]:
            plt.rcParams.update({'axes.grid.axis' : 'x' })

    if explicit_grid:
        plt.rcParams.update({'axes.grid' : True })


def _valid_make_mpf_style_kwargs():
    vkwargs = {
        'base_mpf_style': { 'Default'     : None,
                            'Validator'   : lambda value: value in _styles.keys() },

        'base_mpl_style': { 'Default'     : None,
                            'Validator'   : lambda value: isinstance(value,str) }, # and is in plt.style.available

        'marketcolors'  : { 'Default'     : None, # 
                            'Validator'   : lambda value: isinstance(value,dict)  },

        'mavcolors'     : { 'Default'     : None,
                            'Validator'   : lambda value: isinstance(value,list) },  # TODO: all([mcolors.is_color_like(v) for v in value.values()])

        'facecolor'     : { 'Default'     : None,
                            'Validator'   : lambda value: isinstance(value,str) },

        'edgecolor'     : { 'Default'     : None,
                            'Validator'   : lambda value: isinstance(value,str) },

        'figcolor'      : { 'Default'     : None,
                            'Validator'   : lambda value: isinstance(value,str) },

        'gridcolor'     : { 'Default'     : None,
                            'Validator'   : lambda value: isinstance(value,str) },

        'gridstyle'     : { 'Default'     : None,
                            'Validator'   : lambda value: isinstance(value,str) },

        'gridaxis'      : { 'Default'     : None,
                            'Validator'   : lambda value: value in [ 'vertical'[0:len(value)], 'horizontal'[0:len(value)], 'both'[0:len(value)] ] },

        'y_on_right'    : { 'Default'     : None,
                            'Validator'   : lambda value: isinstance(value,bool) },

        'rc'            : { 'Default'     : None,
                            'Validator'   : lambda value: isinstance(value,dict) },

    }
    _validate_vkwargs_dict(vkwargs)
    return vkwargs

def available_styles():
    return list(_styles.keys())
       
def make_mpf_style( **kwargs ):
    config = _process_kwargs(kwargs, _valid_make_mpf_style_kwargs())

    if config['base_mpf_style'] is not None:
        style  = _get_mpfstyle(config['base_mpf_style'])
        update = [ (k,v) for k,v in config.items() if v is not None ]
        style.update(update)
    else:
        style  = config

    if style['marketcolors'] is None:
        style['marketcolors'] = _styles['default']['marketcolors']

    return style

def _valid_mpf_color_spec(value):
    'value must be a color, "inherit"-like, or dict of colors'
    return ( mcolors.is_color_like(value) or 
             ( isinstance(value,str) and value == 'inherit'[0:len(value)]) or
             ( isinstance(value,dict) and
               all([mcolors.is_color_like(v) for v in value.values()])
             )
           )

def _valid_mpf_style(value):
    if value in available_styles():
        return True
    if not isinstance(value,dict):
        return False
    if 'marketcolors' not in value:
        return False
    if not isinstance(value['marketcolors'],dict):
        return False
    # {'candle': {'up': 'b', 'down': 'g'},
    #  'edge': {'up': 'k', 'down': 'k'},
    #  'wick': {'up': 'k', 'down': 'k'},
    #  'ohlc': {'up': 'k', 'down': 'k'},
    #  'volume': {'up': '#1f77b4', 'down': '#1f77b4'},
    #  'vcedge': {'up': '#1f77b4', 'down': '#1f77b4'},
    #  'vcdopcod': False,
    #  'alpha': 0.9}
    for item in ('candle','edge','wick','ohlc','volume'):
        if item not in value['marketcolors']:
            return False
        itemcolors = value['marketcolors'][item]
        if not isinstance(itemcolors,dict):
            return False
        if 'up' not in itemcolors or 'down' not in itemcolors:
            return False
    return True

def _valid_make_marketcolors_kwargs():
    vkwargs = {
        'up'         : { 'Default'     : None,
                         'Validator'   : lambda value: mcolors.is_color_like(value) },

        'down'       : { 'Default'     : None,
                         'Validator'   : lambda value: mcolors.is_color_like(value) },

        'alpha'       : { 'Default'     : None,
                         'Validator'   : lambda value: ( isinstance(value,float) and
                                                         0.0 <= value and 1.0 >= value ) },

        'edge'       : { 'Default'     : None,
                         'Validator'   : lambda value: _valid_mpf_color_spec(value) },

        'wick'       : { 'Default'     : None,
                         'Validator'   : lambda value: isinstance(value,dict)
                                                       or isinstance(value,str) 
                                                       or mcolors.is_color_like(value) },

        'ohlc'       : { 'Default'     : None,
                         'Validator'   : lambda value: isinstance(value,dict)
                                                       or isinstance(value,str) 
                                                       or mcolors.is_color_like(value) },

        'volume'     : { 'Default'   : None,
                         'Validator'   : lambda value: isinstance(value,dict)
                                                       or isinstance(value,str) 
                                                       or mcolors.is_color_like(value) },

        'inherit'    : { 'Default'     : False,
                         'Validator'   : lambda value: isinstance(value,bool) },

        'base_mpf_style': { 'Default'     : None,
                            'Validator'   : lambda value: isinstance(value,str) },
    }
    _validate_vkwargs_dict(vkwargs)
    return vkwargs

def make_marketcolors(**kwargs):
    '''
    Create a 'marketcolors' dict that is structured as expected
    by mplfinance._styles code:
        up     = color for close >= open
        down   = color for close  < open
        edge   = color for edge of candlestick; if "inherit"
                 then edge color will be same as up or down.
        wick   = color for wick of candlestick; if "inherit"
                 then wick color will be same as up or down.
        alpha  = opacity, 0.0 to 1.0, of candlestick face.
        ohlc   = color of ohlc bars when all the same color;
                 if ohlc == "inherit" then use up/down colors.
        volume = color of volume bars when all the same color;
                 if volume == "inherit" then use up/down colors.
    '''

    config = _process_kwargs(kwargs, _valid_make_marketcolors_kwargs())

    if config['base_mpf_style'] is not None:
        style = _get_mpfstyle(config['base_mpf_style'])
    else:
        style = _get_mpfstyle('default')

    marketcolors = style['marketcolors']

    up   = config['up']
    down = config['down']
    if up is not None and down is not None:
        marketcolors.update(candle=dict(up=up,down=down))
    elif up is not None:
        candle = marketcolors['candle']
        candle.update(up=up)
        marketcolors.update(candle=candle)
    elif down is not None:
        candle = marketcolors['candle']
        candle.update(down=down)
        marketcolors.update(down=down)

    def _check_and_set_mktcolor(candle,**kwarg):
        if len(kwarg) != 1:
            raise ValueError('Expect only ONE kwarg')
        key,value = kwarg.popitem()
        if isinstance(value,(dict)):
            colors = value
        elif isinstance(value,str) and value == 'inherit'[0:len(value)]:
            colors = candle
        else:
            colors = dict(up=value, down=value)
        for updown in ['up','down']:
            if not mcolors.is_color_like(colors[updown]):
                err = f'NOT is_color_like() for {key}[\'{updown}\'] = {colors[updown]}'
                raise ValueError(err)
        return colors

    candle = marketcolors['candle']

    for kw in ['edge','volume','ohlc','wick']:
        # `inherit=True` takes precedence:
        if config[kw] is not None or config['inherit'] == True:
            if config['inherit'] == True:
                kwa = {kw:'i'}
            else:
                kwa = {kw:config[kw]}
            c   = _check_and_set_mktcolor(candle,**kwa)
            marketcolors.update([(kw,c)])

    if config['alpha'] is not None:
        marketcolors.update({'alpha':config['alpha']})

    return marketcolors
