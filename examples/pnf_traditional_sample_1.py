import mplfinance as mpf
import yfinance as yf
import pandas as pd
data = yf.download("AAPL", period="3mo")

data.columns = data.columns.droplevel(1)  # flatten columns
data = data.astype(float)
print(data.dtypes)
print(mpf.__file__)
print()
mpf.plot(data, type='pnf', pnf_params=dict(box_size='traditional'),savefig='pnf.png')
mpf.plot(data, type='pnf', pnf_params=dict(box_size='atr'), savefig='atr.png')