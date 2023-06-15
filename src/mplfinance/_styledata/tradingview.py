style = dict(style_name    = 'tradingview',
             base_mpl_style= 'fast',
             marketcolors  = {'candle'   : {'up': '#26a69a', 'down': '#ef5350'},  
                              'edge'     : {'up': '#26a69a', 'down': '#ef5350'},  
                              'wick'     : {'up': '#26a69a', 'down': '#ef5350'},  
                              'ohlc'     : {'up': '#26a69a', 'down': '#ef5350'},
                              'volume'   : {'up': '#26a69a', 'down': '#ef5350'},  
                              'vcedge'   : {'up': 'white'  , 'down': 'white'  },  
                              'vcdopcod' : False,
                              'alpha'    : 1.0,
                              'volume_alpha': 0.65,
                             },
             scale_width_adjustment = { 'volume': 0.8 },
             mavcolors     = ['#2962ff','#2962ff',],
             y_on_right    = True,
             gridcolor     = None,
             gridstyle     = '--',
             facecolor     =  None,
             rc            = [ ('axes.grid','True'),
                               ('axes.edgecolor'  , 'grey' ),
                               ('axes.titlecolor','red'),
                               ('figure.titlesize', 'x-large' ),
                               ('figure.titleweight','semibold'),
                               ('figure.facecolor', 'white' ),
                             ],
             base_mpf_style = 'tradingview'
            )