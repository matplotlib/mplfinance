import pandas as pd

def _get_widths_df():
    '''
    Provide a dataframe of width data that appropriate scales widths of
    various aspects of the plot (candles,ohlc bars,volume bars) based on
    the amount or density of data.  These numbers were arrived at by 
    carefully testing many use cases of plots with various styles.
    '''
    numpoints = [n for n in range(30,241,30)]
    #volume_width     = (0.95, 0.90,  0.85,  0.80,  0.75,  0.70,  0.65, 0.60 )
    #volume_width     = (0.95, 0.925,  0.90,  0.875,  0.85,  0.825,  0.80, 0.775 )
    volume_width     = (0.98, 0.96,  0.95,  0.925,  0.9,  0.9,  0.875, 0.825 )
    volume_linewidth = tuple([0.65]*8)
    candle_width     = (0.65, 0.575, 0.50, 0.425, 0.350, 0.312, 0.312, 0.321)
    candle_linewidth = (1.00, 0.875, 0.75, 0.625, 0.500, 0.438, 0.438, 0.438)
    ohlc_tickwidth   = tuple([0.35]*8)
    ohlc_linewidth   = (1.50, 1.175, 0.85, 0.525, 0.525, 0.525, 0.525, 0.525)
    widths = {}
    widths['vw']  = volume_width
    widths['vlw'] = volume_linewidth
    widths['cw']  = candle_width
    widths['clw'] = candle_linewidth
    widths['ow']  = ohlc_tickwidth
    widths['olw'] = ohlc_linewidth
    return pd.DataFrame(widths,index=numpoints)

_widths = _get_widths_df()

def _determine_widths_config( xdates, config ):
    '''
    Given x-axis xdates, and `mpf.plot()` kwargs config,
    determine the widths and linewidths for candles,
    volume bars, ohlc bars, etc.
    '''
    datalen = len(xdates)
    avg_dist_between_points = (xdates[-1] - xdates[0]) / float(datalen)

    tweak  = 1.06 if datalen > 100 else 1.03

    adjust = tweak*avg_dist_between_points if config['show_nontrading'] else 1.0

    widths_config = {}

    if isinstance(config['vol_width'],(float,int)):
        widths_config['volume_width'] = config['vol_width']
    else:
        widths_config['volume_width'] = _dfinterpolate(_widths,datalen,'vw') * adjust

    if isinstance(config['vol_linewidth'],(float,int)):
        widths_config['volume_linewidth']  = config['vol_linewidth']
    else:
        widths_config['volume_linewidth'] = _dfinterpolate(_widths,datalen,'vlw')

    if config is not None and config['ohlc_ticksize'] is not None:
        widths_config['ohlc_ticksize'] = config['ohlc_ticksize']
    else:
        widths_config['ohlc_ticksize'] = _dfinterpolate(_widths,datalen,'ow') * adjust

    if config is not None and config['ohlc_linewidth'] is not None:
        widths_config['ohlc_linewidth'] = config['ohlc_linewidth']
    else:
        widths_config['ohlc_linewidth'] = _dfinterpolate(_widths,datalen,'olw')

    if config is not None and config['candle_width'] is not None:
        widths_config['candle_width'] = config['candle_width']
    else:
        widths_config['candle_width'] = _dfinterpolate(_widths,datalen,'cw') * adjust
    
    if config is not None and config['candle_linewidth'] is not None:
        widths_config['candle_linewidth'] = config['candle_linewidth']
    else:
        widths_config['candle_linewidth'] = _dfinterpolate(_widths,datalen,'clw')

    return widths_config



def _dfinterpolate(df,key,column):
    '''
    Given a DataFrame, with all values and the Index as floats,
    and given a float key, find the row that matches the key, or 
    find the two rows surrounding that key, and return the interpolated
    value for the specified column, based on where the key falls between
    the two rows.  If they key is an exact match for a key in the index,
    the return the exact value from the column.  If the key is less than
    or greater than any key in the index, then return either the first
    or last value for the column.
    '''
    s = df[column]
    s1 = s.loc[:key]
    #print('s1=',s1)
    if len(s1) < 1:
        print('_dfinterpolate returning',s.iloc[0])
        return s.iloc[0]
    j1 = s1.index[-1]
    v1 = s1.iloc[-1]
    #print('j1,v1=',j1,v1)
    
    s2 = s.loc[key:]
    #print('s2=',s2)
    if len(s2) < 1:
        print('_dfinterpolate returning',s.iloc[-1])
        return s.iloc[-1]
    j2 = s2.index[0]
    v2 = s2.iloc[0]
    #print('j2,v2=',j2,v2)

    if j1 == j2:
        print('_dfinterpolate returning',v1)
        return v1
    delta   = j2 - j1
    portion = (key - j1)/delta
    #print('delta,key,portion=',delta,key,portion)
    ans = v1 + (v2-v1)*portion
    print('_dfinterpolate returning',ans)
    return ans
