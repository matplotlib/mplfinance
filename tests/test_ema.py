
import mplfinance as mpf
import requests        # for making http requests to binance
import json            # for parsing what binance sends back to us
import pandas as pd    # for storing and manipulating the data we get back
import numpy as np     # numerical python, i usually need this somewhere
# and so i import by habit nowadays

import matplotlib.pyplot as plt  # for charts and such
import datetime as dt  # for dealing with times

INTERVAL = '1d'


def get_bars(quote, interval=INTERVAL):

    root_url = 'https://api.binance.com/api/v1/klines'
    url = root_url + '?symbol=' + quote + '&interval=' + interval
    data = json.loads(requests.get(url).text)
    df = pd.DataFrame(data)
    df.columns = ['open_time',
                  'o', 'h', 'l', 'c', 'v',
                  'close_time', 'qav', 'num_trades',
                  'taker_base_vol', 'taker_quote_vol', 'ignore']
    df.index = [dt.datetime.fromtimestamp(x/1000.0) for x in df.close_time]

    return df


def coinpair(quote, interval='1d', base='USDT'):
    '''returns ohlc data of the quote cryptocurrency with
        the base currency (i.e. 'market'); base for alts must be either USDT or BTC'''

    btcusd = 1 if quote == 'BTC' else \
        get_bars('BTCUSDT', interval=interval)['c'].astype('float') \
        if base == 'USDT' else 1

    base0 = 'USDT' if quote == 'BTC' else 'BTC'

    df = get_bars(quote + base0, interval=interval)

    df['close'] = df['c'].astype('float')*btcusd
    df['open'] = df['o'].astype('float')*btcusd
    df['high'] = df['h'].astype('float')*btcusd
    df['low'] = df['l'].astype('float')*btcusd

    df.drop(['o', 'h', 'l', 'c'], axis=1, inplace=True)
    print(quote, base, 'on {} candles'.format(interval))

    return df


def test_ema():

    coin = 'BTC'
    market = 'USDT'
    candles = '1M'

    df = coinpair(coin, interval=candles, base=market)

    # mpf.plot(df,type='candle',figratio=(5,2),figscale=0.5,\
    #          title=coin+market+" ({} candles)".format(candles),\
    #          yscale='log'
    #          )
    #

    ema25 = df['close'].ewm(span=25.0, adjust=False).mean()
    mav25 = df['close'].rolling(window=25).mean()

    # mpf.plot(df, type='ohlc', mav=25)

    ap = [
        mpf.make_addplot(df, panel=1, type='ohlc', color='c',
                         ylabel='mpf mav', mav=25, secondary_y=False),
        mpf.make_addplot(ema25, panel=2, type='line', width=2,  color='c',
                         ylabel='calculated', secondary_y=False),
        mpf.make_addplot(mav25, panel=2, type='line', width=2, color='blue',
                         ylabel='calculated', secondary_y=False)

    ]
    mpf.plot(df, ylabel="mpf ema", type='ohlc',
             ema=25, addplot=ap, panel_ratios=(1, 1))


test_ema()
