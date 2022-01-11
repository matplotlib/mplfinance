import mplfinance as mpf
import pandas as pd

#daily = pd.read_csv('/Users/jsb/Desktop/mplfinance-master/examples/data/SP500_NOV2019_Hist.csv',
#                    index_col=0, parse_dates=True)
daily = pd.read_csv('../../data/SP500_NOV2019_Hist.csv',
                    index_col=0, parse_dates=True)
daily.index.name = 'Date'
# print(daily.shape)
print(daily)
# daily = daily.loc[:, ['Open', 'High', 'Low', 'Close', 'Volume']]

mpf.figure(figsize=(20, 8), dpi=100)

mpf.plot(daily, type='candle', tight_layout=True)
