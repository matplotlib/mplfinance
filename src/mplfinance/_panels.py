def _list_of_dict(x):
    return isinstance(x,list) and all([isinstance(item,dict) for item in x])

def _determine_relative_panel_heights( addplot, want_volume, panel_ratio ):
    """
    Determine panel needs (how many, size, order) for the given
    mplfinance.plot() configuration.   

    We allow up to three panels: 'A', 'B', and 'C'.
    We can simplify the code by limiting certain features:
    'A' is the main panel (where OHLC/Candles are plotted).
    Volume always goes on panel 'B'.
    Additional plots (`addplot`) may be placed on 'A','B', or 'C'

    We require that panel 'B' must be used (either by addplot
    or by volume) if panel 'C' is used; the code can then
    assume if we have panel 'C', then we have 3 panels.

    We always create a primary and secondary (twinx) axis for
    any panel that we need (even if the secondary axis ends up 
    not being used).  This also helps simplify the code in that
    we don't have to think about creating axes in the portion
    of code that is determining from the data whether or not
    to use a `secondary_y` if some addplot data has a different
    order of magnitude than data already on the primary axes.

    For the three panels, then, we have these axes,
    i.e. a primary and secondary axes for each panel:
    axA1, axA2, axB1, axB2, axC1, axC2 

    Note:
    The panel previously called 'main'  is now axA1.
    The panel previously called 'lower' is now axB1.
   
    """

    # -------------------------------------------------------------------------------
    #  First determine how many (which) panels we need.
    #  We always need panel A.
    #  We just need to know whether we also need B and C:

    panelB = False
    panelC = False
    if addplot is not None:
        if isinstance(addplot,dict):
            addplot = [addplot,]   # make list of dict to be consistent
        elif not _list_of_dict(addplot):
            raise TypeError('addplot must be `dict`, or `list of dict`, NOT '+str(type(addplot)))
        for apdict in addplot:
            panel = apdict['panel']
            if panel == 'lower' or panel == 'B':
                panelB = True
            elif panel == 'C':
                panelC = True

    if not panelB and want_volume:
        panelB = True

    if panelC and not panelB:
        raise ValueError('addplot may not specify panel \'C\' without also using panel \'B\'')

    # -------------------------------------------------------------------------------
    #  Now determine the height for each panel:
    #  To leave room for title above Axes, the upper panel stops at 88% of Figure
    #  To leave room for x-axis labels, the bottom panel stops at 18% of Figure
    #  Thus, all panels (1, 2, or 3) fit within 18% to 88% up from bottom of Figure.
    #  Therefore, the code below scales the "panel ratios" by 0.7 (the proportion
    #  from 18% to 88%)

    pratio = panel_ratio

    if panelC:    # need 3 panels
        psum  = float(sum(pratio[0:3]))
        ha = 0.7 * pratio[0]/psum
        hb = 0.7 * pratio[1]/psum
        hc = 0.7 * pratio[2]/psum
    elif panelB:  # need 2 panels
        psum  = float(sum(pratio[0:2]))
        ha = 0.7 * pratio[0]/psum
        hb = 0.7 * pratio[1]/psum
        hc = 0.0
    else:         # just 1 panel:
        ha = 0.7 
        hb = 0.0
        hc = 0.0

    return ha, hb, hc  


def _create_panel_axes( figure, ha, hb, hc, panel_order ):
    """
    Create Axes for the 3 panels (A,B,C) given a Figure,
    the relative panel heights and the panel order.
    If panel height is 0, that panel is not used.
    Panel order is a string of length three containing
    'A', 'B', and 'C' in some order, as specified by
    mplfinance.plot() kwarg `panel_order`.
    """

    panel_order = panel_order.upper()

    axB1 = None
    axB2 = None
    axC1 = None
    axC2 = None

    # ------------------------------------------------------------------
    # Always *create* panels in this order: A then B then C.
    # regardless of which panel is on top, middle, or bottom.
    #  For each panel (A,B,C) first determine which, if any, panels
    #  are below that panel, and calculate how much to "lift" the 
    #  panel to make room for those panels below it:

    if hc > 0:     
        actual_order = panel_order                 # All 3 panels
    elif hb > 0: 
        actual_order = panel_order.replace('C','') # Only 2 panels (cause already checked hc)
    else:   
        actual_order = ['A']                       # Only 1 panel

    pbelow = actual_order[ actual_order.index('A')+1 : ]
    lift = 0
    if 'B' in pbelow:
        lift += hb
    if 'C' in pbelow:
        lift += hc
    axA1 = figure.add_axes( [0.15, 0.18+lift, 0.70, ha] )
   
    if hb > 0:
        pbelow = actual_order[ actual_order.index('B')+1 : ]
        lift = 0
        if 'A' in pbelow:
            lift += ha
        if 'C' in pbelow:
            lift += hc
        axB1 = figure.add_axes( [0.15, 0.18+lift, 0.70, hb], sharex=axA1 )

    if hc > 0:
        pbelow = actual_order[ actual_order.index('C')+1 : ]
        lift = 0
        if 'A' in pbelow:
            lift += ha
        if 'B' in pbelow:
            lift += hb
        axC1 = figure.add_axes( [0.15, 0.18+lift, 0.70, hc], sharex=axA1 )

    if axB1 is not None:
       axB1.set_axisbelow(True) # so grid does not show through volume bars.
       axB2 = axB1.twinx()
       axB2.grid(False)

    if axC1 is not None:
       axC2 = axC1.twinx()
       axC2.grid(False)
  
    axA2 = axA1.twinx()
    axA2.grid(False)

    return axA1, axA2, axB1, axB2, axC1, axC2, actual_order

def _adjust_ticklabels_per_bottom_panel(axA1,axB1,axC1,actual_order,hb,hc,formatter):
    """
    Determine which panel is on the bottom, then display ticklabels
    for the bottom panel Axes, and NOT for the other Axes.
    """
    # Which panel is on bottom?
    # Set the formatter for the bottom panel, and set xaxis
    # labels visable=False (labelbottom=False) for the others:

    bottom_panel = actual_order[-1]
    if bottom_panel == 'A':
        axA1.tick_params(axis='x', rotation=45)
        if hb > 0:
            #plt.setp(axB1.get_xticklabels(), visible=False)
            #axB1.tick_params(axis='x', visible=False)
            axB1.tick_params(axis='x', labelbottom=False)
        if hc > 0:
            #plt.setp(axC1.get_xticklabels(), visible=False)
            #axC1.tick_params(axis='x', visible=False)
            axC1.tick_params(axis='x', labelbottom=False)
    elif bottom_panel == 'B':
        axB1.tick_params(axis='x', rotation=45)
        axB1.xaxis.set_major_formatter(formatter)
        #plt.setp(axA1.get_xticklabels(), visible=False)
        #axA1.tick_params(axis='x', visible=False)
        axA1.tick_params(axis='x', labelbottom=False)
        if hc > 0:
            #plt.setp(axA1.get_xticklabels(), visible=False)
            #axC1.tick_params(axis='x', visible=False)
            axC1.tick_params(axis='x', labelbottom=False)
    elif bottom_panel == 'C':
        axC1.tick_params(axis='x', rotation=45)
        axC1.xaxis.set_major_formatter(formatter)
        #plt.setp(axA1.get_xticklabels(), visible=False)
        #plt.setp(axB1.get_xticklabels(), visible=False)
        #axA1.tick_params(axis='x', visible=False)
        #axB1.tick_params(axis='x', visible=False)
        axA1.tick_params(axis='x', labelbottom=False)
        axB1.tick_params(axis='x', labelbottom=False)
    else:
        raise RuntimeError('bottom_panel='+str(bottom_panel))

    return None
