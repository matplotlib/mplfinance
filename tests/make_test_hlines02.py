import os
import pandas as pd
import os.path
import mplfinance as mpf

def bolldata():
   return df

if __name__ == "__main__":
    os.environ['MPLBACKEND'] = 'agg'

    print('\npd.__version__  =',pd.__version__ )                 # for the record

    infile = os.path.join('examples','data','SPY_20110701_20120630_Bollinger.csv')
    df = pd.read_csv(infile,index_col=0,parse_dates=True)
    print('df.shape='  , df.shape  )
    print('df.head(3)=', df.head(3))
    print('df.tail(3)=', df.tail(3))

    tname='/ws/forks/mplfinance/tests/reference_images/hlines02.png'
    mpf.plot(
        df,
        type='ohlc',
        volume=True,
        savefig=tname,
        returnfig=True,
        hlines=dict(hlines=[120.000001, 130.0],linestyle='-.',colors='g')
    )