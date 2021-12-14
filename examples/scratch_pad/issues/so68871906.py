###   !pip install yfinance
###   !pip install mplfinance
import yfinance as yf
import mplfinance as mpf
import numpy as np 
import pandas as pd 

# get the data from yfiance 
df=yf.download('BTC-USD',start='2008-01-04',end='2021-06-3',interval='1d')

#code snippet 5.1
# Fit linear regression on close
# Return the t-statistic for a given parameter estimate.
def tValLinR(close):
    #tValue from a linear trend
    x = np.ones((close.shape[0],2))
    x[:,1] = np.arange(close.shape[0])
    ols = sm1.OLS(close, x).fit()
    return ols.tvalues[1]

    #code snippet 5.2
'''
 #search for the maximum absolutet-value. To identify the trend 
  #  - molecule - index of observations we wish to labels. 
   # - close - which is the time series of x_t
   # - span - is the set of values of L (look forward period) that the algorithm will #try (window_size)
#    The L that maximizes |tHat_B_1| (t-value) is choosen - which is the look-forward #period 
#    with the most significant trend. (optimization)
'''
def getBinsFromTrend(molecule, close, span):
    
    #Derive labels from the sign of t-value of trend line
    #output includes:
     # - t1: End time for the identified trend
     # - tVal: t-value associated with the estimated trend coefficient
      #- bin: Sign of the trend (1,0,-1)
    #The t-statistics for each tick has a different look-back window.
      
    #- idx start time in look-forward window
    #- dt1 stop time in look-forward window
    #- df1 is the look-forward window (window-size)
    #- iloc ? 
    
    out = pd.DataFrame(index=molecule, columns=['t1', 'tVal', 'bin', 'windowSize'])
    hrzns = range(*span)
    windowSize = span[1] - span[0]
    maxWindow = span[1]-1
    minWindow = span[0]
    for idx in close.index:
        idx += (maxWindow*pd.Timedelta('1 day'))
        if idx >= close.index[-1]:
            break
        df_tval = pd.Series(dtype='float64')
        iloc0 = close.index.get_loc(idx)
        if iloc0+max(hrzns) > close.shape[0]:
            continue
        for hrzn in hrzns:
            dt1 = close.index[iloc0-hrzn+1]
            df1 = close.loc[dt1:idx]
            df_tval.loc[dt1] = tValLinR(df1.values) #calculates t-statistics on period
        dt1 = df_tval.replace([-np.inf, np.inf, np.nan], 0).abs().idxmax() #get largest t-statistics calculated over span period

        print(df_tval.index[-1])
        print(dt1)
        print(abs(df_tval.values).argmax() + minWindow)
        out.loc[idx, ['t1', 'tVal', 'bin', 'windowSize']] = df_tval.index[-1], df_tval[dt1], np.sign(df_tval[dt1]), abs(df_tval.values).argmax() + minWindow #prevent leakage
    out['t1'] = pd.to_datetime(out['t1'])
    out['bin'] = pd.to_numeric(out['bin'], downcast='signed')

    #deal with massive t-Value outliers - they dont provide more confidence and they ruin the scatter plot
    tValueVariance = out['tVal'].values.var()
    tMax = 20
    if tValueVariance < tMax:
        tMax = tValueVariance

    out.loc[out['tVal'] > tMax, 'tVal'] = tMax #cutoff tValues > 20
    out.loc[out['tVal'] < (-1)*tMax, 'tVal'] = (-1)*tMax #cutoff tValues < -20
    return out.dropna(subset=['bin'])

if __name__ == '__main__':
    #snippet 5.3
    idx_range_from = 3
    idx_range_to = 10
    df1 = getBinsFromTrend(df.index, df['Close'], [idx_range_from,idx_range_to,1]) #[3,10,1] = range(3,10) This is the issue 
    tValues = df1['tVal'].values #tVal

    doNormalize = False
    #normalise t-values to -1, 1
    if doNormalize:
        np.min(tValues)
        minusArgs = [i for i in range(0, len(tValues)) if tValues[i] < 0]
        tValues[minusArgs] = tValues[minusArgs] / (np.min(tValues)*(-1.0))

        plus_one = [i for i in range(0, len(tValues)) if tValues[i] > 0]
        tValues[plus_one] = tValues[plus_one] / np.max(tValues)

    #+(idx_range_to-idx_range_from+1)
    plt.scatter(df1.index, df0.loc[df1.index].values, c=tValues, cmap='viridis') #df1['tVal'].values, cmap='viridis')
    plt.plot(df0.index, df0.values, color='gray')
    plt.colorbar()
    plt.show()
    plt.savefig('fig5.2.png')
    plt.clf()
    plt.df['Close']()
    plt.scatter(df1.index, df0.loc[df1.index].values, c=df1['bin'].values,  cmap='vipridis')

    #Test methods
    ols_tvalue = tValLinR( np.array([3.0, 3.5, 4.0]) )
