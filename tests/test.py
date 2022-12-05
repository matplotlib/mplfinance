import pandas as pd
import mplfinance as mpf
df = pd.read_csv('data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)

apdict = [mpf.make_addplot(df['LowerB']),
        mpf.make_addplot(df['UpperB'],panel=1)]
vls = pd.date_range(df.index.min(), df.index.max(), freq='D').tolist()
kwargs = dict(type='candle', vlines=dict(vlines=vls[0], linewidths=0.5, colors=('r')))
mpf.plot(df,volume=False,addplot=apdict,**kwargs)