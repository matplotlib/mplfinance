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

    tname='/ws/forks/mplfinance/tests/reference_images/vlines01.png'
    fig_axis = mpf.plot(
        df,volume=True,savefig=tname,returnfig=True,vlines=['2011-09-13']
    )