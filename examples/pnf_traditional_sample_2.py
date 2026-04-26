import yfinance as yf
import mplfinance as mpf
import pandas as pd
tickers = ["AAPL", "TSLA", "RELIANCE.NS"]

for t in tickers:
    data = yf.download(t, period="6mo")
    data.columns = data.columns.droplevel(1)
    data = data.astype(float)

    mpf.plot(data, type='pnf',
             pnf_params=dict(box_size='traditional'),
             savefig=f"{t}_traditional.png")

    mpf.plot(data, type='pnf',
             pnf_params=dict(box_size='atr'),
             savefig=f"{t}_atr.png")