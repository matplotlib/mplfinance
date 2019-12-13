"""
A collection of utilities for analyzing and plotting financial data.

"""
#from __future__ import (absolute_import, division, print_function, unicode_literals)

import numpy as np
from matplotlib import colors as mcolors
from matplotlib.collections import LineCollection, PolyCollection
from matplotlib.lines import TICKLEFT, TICKRIGHT, Line2D
from matplotlib.patches import Rectangle
from matplotlib.transforms import Affine2D

from six.moves import xrange, zip

def _check_input(opens, closes, highs, lows, miss=-1):
    """Checks that *opens*, *highs*, *lows* and *closes* have the same length.
    NOTE: this code assumes if any value open, high, low, close is
    missing (*-1*) they all are missing

    Parameters
    ----------
    ax : `Axes`
        an Axes instance to plot to
    opens : sequence
        sequence of opening values
    highs : sequence
        sequence of high values
    lows : sequence
        sequence of low values
    closes : sequence
        sequence of closing values
    miss : int
        identifier of the missing data

    Raises
    ------
    ValueError
        if the input sequences don't have the same length
    """

    def _missing(sequence, miss=-1):
        """Returns the index in *sequence* of the missing data, identified by
        *miss*

        Parameters
        ----------
        sequence :
            sequence to evaluate
        miss :
            identifier of the missing data

        Returns
        -------
        where_miss: numpy.ndarray
            indices of the missing data
        """
        return np.where(np.array(sequence) == miss)[0]

    same_length = len(opens) == len(highs) == len(lows) == len(closes)
    _missopens = _missing(opens)
    same_missing = ((_missopens == _missing(highs)).all() and
                    (_missopens == _missing(lows)).all() and
                    (_missopens == _missing(closes)).all())

    if not (same_length and same_missing):
        msg = ("*opens*, *highs*, *lows* and *closes* must have the same"
               " length. NOTE: this code assumes if any value open, high,"
               " low, close is missing (*-1*) they all must be missing.")
        raise ValueError(msg)

def _construct_ohlc_collections(dates, opens, highs, lows, closes, colorup='k', colordown='k'):
    """Represent the time, open, high, low, close as a vertical line
    ranging from low to high.  The left tick is the open and the right
    tick is the close.
    *opens*, *highs*, *lows* and *closes* must have the same length.
    NOTE: this code assumes if any value open, high, low, close is
    missing (*-1*) they all are missing

    Parameters
    ----------
    opens : sequence
        sequence of opening values
    highs : sequence
        sequence of high values
    lows : sequence
        sequence of low values
    closes : sequence
        sequence of closing values
    colorup : color
        the color of the lines where close >= open
    colordown : color
        the color of the lines where close <  open

    Returns
    -------
    ret : list 
        a list or tuple of matplotlib collections to be added to the axes
    """

    _check_input(opens, highs, lows, closes)

    rangeSegments = [((dt, low), (dt, high)) for dt, low, high in
                     zip(dates, lows, highs) if low != -1]

    avg_dist_between_points = (dates[-1] - dates[0]) / float(len(dates))

    ticksize = avg_dist_between_points / 2.5

    # the ticks will be from ticksize to 0 in points at the origin and
    # we'll translate these to the date, open location
    openSegments = [((dt-ticksize, op), (dt, op)) for dt, op in zip(dates, opens) if op != -1]
    

    # the ticks will be from 0 to ticksize in points at the origin and
    # we'll translate these to the date, close location
    closeSegments = [((dt, close), (dt+ticksize, close)) for dt, close in zip(dates, closes) if close != -1]

    colorup = mcolors.to_rgba(colorup)
    colordown = mcolors.to_rgba(colordown)
    colord = {True: colorup, False: colordown}
    colors = [colord[open < close] for open, close in
              zip(opens, closes) if open != -1 and close != -1]

    #    avg_dist_between_points = (dates[-1] - dates[0]) / float(len(dates))

    useAA = 0,    # use tuple here
    lw    = 0.5,  # use tuple here
    lw = None
    rangeCollection = LineCollection(rangeSegments,
                                     colors=colors,
                                     linewidths=lw,
                                     antialiaseds=useAA
                                     )

    openCollection = LineCollection(openSegments,
                                    colors=colors,
                                    linewidths=lw,
                                    antialiaseds=useAA
                                    )

    closeCollection = LineCollection(closeSegments,
                                     colors=colors,
                                     antialiaseds=useAA,
                                     linewidths=lw
                                     )

    #    minx = dates[0]  - avg_dist_between_points
    #    maxx = dates[-1] + avg_dist_between_points
    #
    #    miny = min([low for low in lows if low != -1])
    #    maxy = max([high for high in highs if high != -1])
    #    corners = (minx, miny), (maxx, maxy)
    #    ax.update_datalim(corners)
    #    ax.autoscale_view()
    #
    #    # add these last
    #    ax.add_collection(rangeCollection)
    #    ax.add_collection(openCollection)
    #    ax.add_collection(closeCollection)

    return rangeCollection, openCollection, closeCollection


def _construct_candlestick_collections(dates, opens, highs, lows, closes,
                                       colorup='w', colordown='k', alpha=0.90):
    """Represent the open, close as a bar line and high low range as a
    vertical line.

    NOTE: this code assumes if any value open, low, high, close is
    missing they all are missing


    Parameters
    ----------
    opens : sequence
        sequence of opening values
    highs : sequence
        sequence of high values
    lows : sequence
        sequence of low values
    closes : sequence
        sequence of closing values
    colorup : color
        the color of the lines where close >= open
    colordown : color
        the color of the lines where close <  open
    alpha : float
        bar transparency

    Returns
    -------
    ret : tuple
        (lineCollection, barCollection)
    """
    
    _check_input(opens, highs, lows, closes)

    avg_dist_between_points = (dates[-1] - dates[0]) / float(len(dates))

    delta = avg_dist_between_points / 4.0

    barVerts = [((date - delta, open),
                 (date - delta, close),
                 (date + delta, close),
                 (date + delta, open))
                for date, open, close in zip(dates, opens, closes)
                if open != -1 and close != -1]

    rangeSegLow   = [((date, low), (date, min(open,close)))
                     for date, low, open, close in zip(dates, lows, opens, closes)
                     if low != -1]
    
    rangeSegHigh  = [((date, high), (date, max(open,close)))
                     for date, high, open, close in zip(dates, highs, opens, closes)
                     if high != -1]
                      
    rangeSegments = rangeSegLow + rangeSegHigh

    colorup = mcolors.to_rgba(colorup, alpha)
    colordown = mcolors.to_rgba(colordown, alpha)
    colorup = mcolors.to_rgba(colorup, 1.0)
    colordown = mcolors.to_rgba(colordown, alpha)
    colord = {True: colorup, False: colordown}
    colors = [colord[open < close]
              for open, close in zip(opens, closes)
              if open != -1 and close != -1]
    edgecolor = mcolors.to_rgba('k',1.0)

    useAA = 0,    # use tuple here
    lw    = 0.5,  # use tuple here
    lw = None
    rangeCollection = LineCollection(rangeSegments,
                                     colors='k',
                                     linewidths=lw,
                                     antialiaseds=useAA
                                     )

    barCollection = PolyCollection(barVerts,
                                   facecolors=colors,
                                   edgecolors=edgecolor,
                                   antialiaseds=useAA,
                                   linewidths=lw
                                   )

    #    minx = dates[0]  - avg_dist_between_points
    #    maxx = dates[-1] + avg_dist_between_points
    #    miny = min([low for low in lows if low != -1])
    #    maxy = max([high for high in highs if high != -1])
    #
    #    corners = (minx, miny), (maxx, maxy)
    #    #print('corners=',corners)
    #    ax.update_datalim(corners)
    #    ax.autoscale_view()
    #
    #    # add these last
    #    ax.add_collection(rangeCollection)
    #    ax.add_collection(barCollection)

    return rangeCollection, barCollection

