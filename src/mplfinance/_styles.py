import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import copy
import pprint
import os.path as path

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

        'legacy_rc'     : { 'Default'     : None,  # Just in case someone depended upon old behavior
                            'Validator'   : lambda value: isinstance(value,dict) },

        'style_name'    : { 'Default'     : None,
                            'Validator'   : lambda value: isinstance(value,str) },

    }
    _validate_vkwargs_dict(vkwargs)
    return vkwargs

def available_styles():
    return list(_styles.keys())
       
def make_mpf_style( **kwargs ):
    config = _process_kwargs(kwargs, _valid_make_mpf_style_kwargs())
    if config['rc'] is not None and config['legacy_rc'] is not None:
        raise ValueError('kwargs `rc` and `legacy_rc` may NOT be used together!')

    # -----------
    # March 2021: Found bug that if caller used `base_mpf_style` and `rc` at
    #   the same time, then the caller's `rc` will completely replace the `rc` 
    #   of `base_mpf_style`.  That was never the intention!  Rather it should be
    #   that the caller's `rc` merely adds to and/or modifies the `rc` of the
    #   `base_mpf_style`.  In order to provide a path to "backwards compatibility"
    #   for users who may have depended on the bug behavior (callers `rc` replaces
    #   `rc` of `base_mpf_style`) we provide a new kwarg `legacy_rc` which will
    #   now behave the way that `rc` used to behave.
    # -----------

    if config['base_mpf_style'] is not None:
        style  = _get_mpfstyle(config['base_mpf_style'])
        # Have to handle 'rc' separately, so we don't wipe 
        # out the 'rc' params in the `base_mpf_style` that
        # are not specified in the `make_mpf_style` config:
        if config['rc'] is not None:
            rc = config['rc']
            del config['rc']
            if isinstance(style['rc'],list):
                style['rc'] = dict(style['rc'])
            if style['rc'] is None:
                style['rc'] = {}
            style['rc'].update(rc)
        elif config['legacy_rc'] is not None:
            config['rc'] = config['legacy_rc']
            del config['legacy_rc']
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

        'hollow'     : { 'Default'     : None,
                         'Validator'   : lambda value: mcolors.is_color_like(value) },

        'alpha'      : { 'Default'     : None,
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

        'vcdopcod'   : { 'Default'     : False,
                         'Validator'   : lambda value: isinstance(value,bool) },

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

    if config['hollow'] is not None:
        marketcolors.update({'hollow':config['hollow']})

    if config['alpha'] is not None:
        marketcolors.update({'alpha':config['alpha']})

    if config['vcdopcod'] is not None:
        marketcolors.update({'vcdopcod':config['vcdopcod']})

    return marketcolors

def write_style_file(style,filename):
    pp   = pprint.PrettyPrinter(indent=4,sort_dicts=False,compact=True)
    strl = pp.pformat(style).splitlines()

    if not isinstance(style,dict):
        raise TypeError('Specified style must be in `dict` format')

    if path.exists(filename):
        print('"'+filename+'" exists.') 
        answer = input(' Overwrite(Y/N)? ')
        a = answer.lower()
        if a != 'y' and a != 'yes':
            raise FileExistsError

    f = open(filename,'w')
    f.write('style = '+strl[0].replace('{','dict(',1).replace("'","",2).replace(':',' =',1)+'\n')
    for line in strl[1:-1]:
        if "'" in line[0:5]:
            f.write('            '+line.replace("'","",2).replace(':',' =',1)+'\n')
        else:
            f.write('            '+line+'\n')
    line = strl[-1]
    if "'" in line[0:5]:
        line = line.replace("'","",2).replace(':',' =',1)[::-1]
    else:
        line = line[::-1]
    f.write('            '+line.replace('}',')',1)[::-1]+'\n')
    f.close()
    print('Wrote style file "'+filename+'"')
    return
