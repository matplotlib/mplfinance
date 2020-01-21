import matplotlib.pyplot as plt
import copy

def _get_mpfstyle(style):
    return copy.deepcopy(_styles[style])

_styles = {}

_classic = dict(
               base_mplstyle='seaborn-darkgrid', 
               marketcolors = { 'candle' : { 'up'    : 'w',
                                             'down'  : 'k',
                                             'edge'  : 'k',
                                             'wick'  : 'k',
                                             'alpha' : 0.9,
                                           },
                                'ohlc'   : { 'up'    : 'k',
                                             'down'  : 'k',
                                           },
                                'volume' : '#1f77b4',
                              },
               mavcolors    = ['#40e0d0','#ff00ff','#ffd700','#1f77b4',
                               '#ff7f0e','#2ca02c','#e377c2'],
               facecolor    = '#DCE3EF',
               gridcolor    = None,
               gridstyle    = None,
                            # plotting.py has "ax1.set_ylabel('Price',size='x-large',weight='semibold')"
                            # so maybe should we set those here instead ??
                            #   axes.labelsize='x-large' 
                            #   axes.labelweight='semibold' 
               rc           = [ ('axes.edgecolor'  , 'black'  ),
                                ('axes.linewidth'  ,  1.5     ),
                                ('axes.labelsize'  , 'large'  ),
                                ('axes.labelweight', 'medium' ),
                                ('lines.linewidth' ,  2.0     ),
                                ('font.weight'     , 'medium' ),
                                ('font.size'       ,  12.0    ),
                              ]
              )
_styles.update(classic=_classic) 

def _apply_mpfstyle(style):
    if style['base_mplstyle'] is not None:
        plt.style.use(style['base_mplstyle'])
        print('plt.style.use('+style['base_mplstyle']+')')

    if style['rc'] is not None:
        plt.rcParams.update(style['rc'])

    if style['facecolor'] is not None:
        plt.rcParams.update({'axes.facecolor' : style['facecolor'] })

    explicit_grid = False
    if style['gridcolor'] is not None:
        explicit_grid = True
        plt.rcParams.update({'grid.color' : style['gridcolor'] })

    if style['gridstyle'] is not None:
        explicit_grid = True
        plt.rcParams.update({'grid.linestyle' : style['gridstyle'] })

    if explicit_grid:
        plt.rcParams.update({'axes.grid' : True })
       
def make_custom_style(base_mplstyle=None, 
                      marketcolors=None,
                      mavcolors=None,
                      facecolor=None,
                      gridcolor=None,
                      gridstyle=None,
                      rc=None
                     ):
    if marketcolors is None:
        marketcolors = _classic['marketcolors']
    style={}
    style.update([ ('base_mplstyle', base_mplstyle),
                   ('marketcolors' , marketcolors ),
                   ('mavcolors'    , mavcolors    ),
                   ('facecolor'    , facecolor    ),
                   ('gridcolor'    , gridcolor    ),
                   ('gridstyle'    , gridstyle    ),
                   ('rc'           , rc           ) ])
    return style
