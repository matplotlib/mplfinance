from select import select
from datetime import datetime

import time
import pandas as pd
import mplfinance as mpf
import sys

import matplotlib
print('backend=',matplotlib.get_backend())

coin = 'BTC' 
bot_status = 'trading'

def limit():
    timeout = 0.5
    print(end='')
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        s = sys.stdin.readline().strip()
        if s == 'g':
            print('\033[1;34m show chart')
            chart()


def dataframe():
    # response = **_api exchange_**.candles(coin + '-EUR', '1m', {})
    # ohlcv = []
    # for s in range(len(response)):
    #     timestamp = (int(response[s][0]))/1000
    #     open = float(response[s][1])
    #     high = float(response[s][2])
    #     low = float(response[s][3])
    #     close = float(response[s][4])
    #     volume = float(response[s][5])
    #     candles = {'timestamp': (datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')), 'open': open, 'high': high, 'low': low, 'close': close, 'volume': volume}
    #     ohlcv.append(candles)
    #     dataframe = pd.DataFrame(data=ohlcv, dtype=float)
    dataframe = pd.read_csv('../../data/SP500_NOV2019_Hist.csv',index_col=0, parse_dates=True)
    return dataframe


def chart():
    df = dataframe()
    #df.index = pd.DatetimeIndex(df['timestamp'])
    #df = df.iloc[::-1]
    s = mpf.make_mpf_style(base_mpf_style='charles', gridcolor='#555555', gridstyle="--", rc={'axes.edgecolor': 'white', 'font.size': 5})
    fig, axlist = mpf.plot(df, type='candle', style=s, title= coin, ylabel = 'Price (€)', volume=True, warn_too_much_data=9999999, returnfig=True)
    mpf.show(block=True)


# trade loop
while bot_status == 'trading':
    limit()
    print('test')
