style = dict(style_name    = 'ibd',
             base_mpl_style= 'fast', 
             marketcolors  = {'candle'  : {'up':'#2A3FE5', 'down':'#DB39AD'},
                              'edge'    : {'up':'#2A3FE5', 'down':'#DB39AD'},
                              'wick'    : {'up':'#2A3FE5', 'down':'#DB39AD'},
                              'ohlc'    : {'up':'#2A3FE5', 'down':'#DB39AD'},
                              'volume'  : {'up':'#2A3FE5', 'down':'#DB39AD'},
                              'vcedge'  : {'up':'#2A3FE5', 'down':'#DB39AD'},
                              'vcdopcod': True, # Volume Color is Per Price Change On Day
                              'alpha'   : 1.0,
                             },
             mavcolors     = ['green','red','black','blue'],
             y_on_right    = True,
             gridcolor     = None,
             gridstyle     = None,
             facecolor     = None,
             rc            =  [     ('axes.titlesize',      8),
                                    ('axes.labelsize',      8) , 
                                    ('lines.linewidth',     3),
                                    ('lines.markersize',    4),
                                    ('ytick.left',          False),
                                    ('ytick.right',         True),
                                    ('ytick.labelleft',     False),   
                                    ('ytick.labelright',    True), 
                                    ('xtick.labelsize',     6),
                                    ('ytick.labelsize',     7),
                                    ('axes.linewidth',      0.8),
                                    ('grid.alpha',          0.2), 
                                    ('axes.grid'       ,  True     ),
                                    ('axes.grid.axis'  ,  'y'      ),  
                                    ('grid.color'      , '#b0b0b0' ),
                                    ('grid.linestyle'  , 'solid'      ),
                                    ('grid.linewidth'  ,  0.8      ),
                                    ('figure.titlesize', 'x-large' ),
                                    ('figure.titleweight','semibold'),
                              ],
             base_mpf_style= 'ibd'
            )
