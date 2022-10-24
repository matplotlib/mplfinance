import mplfinance as mpf
import pandas as pd   

def test_ema():

    df = pd.read_csv('./examples/data/yahoofinance-GOOG-20040819-20180120.csv', parse_dates=True)
    df.index = pd.DatetimeIndex(df['Date'])

    df = df[-50:]               # show last 50 data points only                     

    ema25 = df['Close'].ewm(span=25.0, adjust=False).mean()       
    mav25 = df['Close'].rolling(window=25).mean()

    ap = [
        mpf.make_addplot(df, panel=1, type='ohlc', color='c',
                         ylabel='mpf mav', mav=25, secondary_y=False),
        mpf.make_addplot(ema25, panel=2, type='line', width=2,  color='c',
                         ylabel='calculated', secondary_y=False),
        mpf.make_addplot(mav25, panel=2, type='line', width=2, color='blue',
                         ylabel='calculated', secondary_y=False)
    ]

    mpf.plot(df, ylabel="mpf ema", type='ohlc',
             ema=25, addplot=ap, panel_ratios=(1, 1)
    )

test_ema()
