from mplfinance._helpers import _list_of_dict
from mplfinance._helpers import _valid_panel_id
import pandas as pd

def _build_panels( figure, config ):
    """
    Create and return a DataFrame containing panel information
    and Axes objects for each panel, etc.

    We allow up to 10 panels, identified by their panel id (panid)
    which is an integer 0 through 9.  

    Parameters
    ----------
    figure       : pyplot.Figure
        figure on which to create the Axes for the panels

    config       : dict
        config dict from `mplfinance.plot()`
        
    Config
    ------
    The following items are used from `config`:

    num_panels   : integer (0-9) or None
        number of panels to create

    addplot      : dict or None
        value for the `addplot=` kwarg passed into `mplfinance.plot()`

    volume_panel : integer (0-9) or None
        panel id (0-number_of_panels)

    main_panel   : integer (0-9) or None
        panel id (0-number_of_panels)

    panel_ratios : sequence or None
        sequence of relative sizes for the panels;

        NOTE: If len(panel_ratios) == number of panels (regardless
        of whether number of panels was specified or inferred),
        then panel ratios are the relative sizes of each panel,
        in panel id order, 0 through N (where N = number of panels).

        If len(panel_ratios) != number of panels, then len(panel_ratios)
        must equal 2, and panel_ratios[0] is the relative size for the 'main'
        panel, and panel_ratios[1] is the relative size for all other panels.

        If the number of panels == 1, the panel_ratios is ignored.

    
Returns
    ----------
    panels  : pandas.DataFrame
        dataframe indexed by panel id (panid) and having the following columns:
          axes           : tuple of matplotlib.Axes (primary and secondary) for each column.
          used secondary : bool indicating whether or not the seconday Axes is in use.
          relative size  : height of panel as proportion of sum of all relative sizes

    """

    num_panels   = config['num_panels']
    addplot      = config['addplot']
    volume       = config['volume']
    volume_panel = config['volume_panel']
    num_panels   = config['num_panels']
    main_panel   = config['main_panel']
    panel_ratios = config['panel_ratios']

    if num_panels is None:  # then infer the number of panels:
        pset = {0} # start with a set including only panel zero
        if addplot is not None:
            if isinstance(addplot,dict):
                addplot = [addplot,]   # make list of dict to be consistent
            elif not _list_of_dict(addplot):
                raise TypeError('addplot must be `dict`, or `list of dict`, NOT '+str(type(addplot)))

            backwards_panel_compatibility = {'main':0,'lower':1,'A':0,'B':1,'C':2}

            for apdict in addplot:
                panel = apdict['panel']
                if panel in backwards_panel_compatibility:
                    panel = backwards_panel_compatibility[panel]
                if not _valid_panel_id(panel):
                    raise ValueError('addplot panel must be integer 0 to 9, but is "'+str(panel)+'"')
                pset.add(panel)

        if volume is True:
            if not _valid_panel_id(volume_panel):
                raise ValueError('volume_panel must be integer 0 to 9, but is "'+str(volume_panel)+'"')
            pset.add(volume_panel)

        pset = sorted(pset)
        missing = [m for m in range(len(pset)) if m not in pset]
        if len(missing) != 0:
            raise ValueError('inferred panel list is missing panels: '+str(missing))

    else:
        if not isinstance(num_panels,int) or num_panels < 1 or num_panels > 10:
            raise ValueError('num_panels must be integer 1 to 10, but is "'+str(volume_panel)+'"')
        pset = range(0,num_panels)

    _nones = [None]*len(pset)
    panels = pd.DataFrame(dict(axes=_nones,
                               relsize=_nones,
                               lift=_nones,
                               height=_nones,
                               used2nd=[False]*len(pset),
                               title=_nones,
                               ylabel=_nones),
                          index=pset)
    panels.index.name = 'panid'

    if not _valid_panel_id(main_panel):
        raise ValueError('main_panel id must be integer 0 to 9, but is '+str(main_panel))

    # Now determine the height for each panel:
    # ( figure, num_panels='infer', addplot=None, volume_panel=None, main_panel=0, panel_ratios=None ):

    if panel_ratios is not None:
        if not isinstance(panel_ratios,(list,tuple)):
            raise TypeError('panel_ratios must be a list or tuple')
        if len(panel_ratios) != len(panels) and not (len(panel_ratios)==2 and len(panels) > 2):
            err  = 'len(panel_ratios) must be 2, or must be same as number of panels'
            err += '\nlen(panel_ratios)='+str(len(panel_ratios))+'  num panels='+str(len(panels))
            raise ValueError(err)
        if len(panel_ratios) == 2 and len(panels) > 2:
            pratios = [panel_ratios[1]]*len(panels)
            pratios[main_panel] = panel_ratios[0]
        else:
            pratios = panel_ratios
    else:
        pratios = [2]*len(panels)
        pratios[main_panel] = 5

    panels['relsize'] = pratios
    #print('len(panels)=',len(panels))
    #print('len(pratios)=',len(pratios))

    #print('pratios=')
    #print(pratios)

    #print('panels=')
    #print(panels)
        
    psum = sum(pratios)
    for panid,size in enumerate(pratios):
        panels.at[panid,'height'] = 0.7 * size / psum

    # Now create the Axes:

    for panid,row in panels.iterrows():
        height = row.height
        lift   = panels['height'].loc[panid+1:].sum()
        panels.at[panid,'lift'] = lift
        if panid == 0:
            ax0 = figure.add_axes( [0.15, 0.18+lift, 0.70, height] )
        else:
            ax0 = figure.add_axes( [0.15, 0.18+lift, 0.70, height], sharex=panels.at[0,'axes'][0] )
        ax1 = ax0.twinx()
        ax1.grid(False)
        if panid == volume_panel:
            ax0.set_axisbelow(True) # so grid does not show through volume bars.
        panels.at[panid,'axes'] = (ax0,ax1)

    return panels
    


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

    if want_volume == 'B': panelB = True
    if want_volume == 'C': panelC = True

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

def _set_ticks_on_bottom_panel_only(panels,formatter,rotation=45):

    bot = panels.index.values[-1]
    ax  = panels.at[bot,'axes'][0]
    ax.tick_params(axis='x',rotation=rotation)
    ax.xaxis.set_major_formatter(formatter)

    if len(panels) == 1: return

    for panid in panels.index.values[::-1][1:]:
        panels.at[panid,'axes'][0].tick_params(axis='x',labelbottom=False)

    
def _adjust_ticklabels_per_bottom_panel(axA1,axB1,axC1,actual_order,hb,hc,formatter,rotation=45):
    """
    Determine which panel is on the bottom, then display ticklabels
    for the bottom panel Axes, and NOT for the other Axes.
    """
    # Which panel is on bottom?
    # Set the formatter for the bottom panel, and set xaxis
    # labels visable=False (labelbottom=False) for the others:

    bottom_panel = actual_order[-1]
    if bottom_panel == 'A':
        axA1.tick_params(axis='x', rotation=rotation)
        if hb > 0:
            #plt.setp(axB1.get_xticklabels(), visible=False)
            #axB1.tick_params(axis='x', visible=False)
            axB1.tick_params(axis='x', labelbottom=False)
        if hc > 0:
            #plt.setp(axC1.get_xticklabels(), visible=False)
            #axC1.tick_params(axis='x', visible=False)
            axC1.tick_params(axis='x', labelbottom=False)
    elif bottom_panel == 'B':
        axB1.tick_params(axis='x', rotation=rotation)
        axB1.xaxis.set_major_formatter(formatter)
        #plt.setp(axA1.get_xticklabels(), visible=False)
        #axA1.tick_params(axis='x', visible=False)
        axA1.tick_params(axis='x', labelbottom=False)
        if hc > 0:
            #plt.setp(axA1.get_xticklabels(), visible=False)
            #axC1.tick_params(axis='x', visible=False)
            axC1.tick_params(axis='x', labelbottom=False)
    elif bottom_panel == 'C':
        axC1.tick_params(axis='x', rotation=rotation)
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
