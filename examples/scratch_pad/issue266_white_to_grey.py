import pandas as pd
import mplfinance as mpf

df = pd.read_csv('data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)
df.shape
df.head(3)
df.tail(3)

#kwargs=dict(style='mike',figscale=1.5,type='candle',width_adjuster_version='v0')
kwargs=dict(style='mike',figscale=1.0,type='candle')#,update_width_config=dict(candle_linewidth=0.6))

wcfg={}
mpf.plot(df.iloc[0:100,:],**kwargs,block=False,return_width_config=wcfg)
print('\nwcfg(100)=',wcfg)

wcfg={}
mpf.plot(df.iloc[0:250,:],**kwargs,block=True,return_width_config=wcfg)
print('\nwcfg(250)=',wcfg)
