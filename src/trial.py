import pandas as pd
import random
from datetime import date, timedelta
from mplfinance.plotting import plot
from mplfinance._styles import make_marketcolors

dict_data = []
start_date = date(2019, 1, 1)
end_date = date(2020, 1, 1)
delta = timedelta(days=1)
start = 20
end = 30
while start_date <= end_date:
    openval = random.randint(start, end)
    closeval = random.randint(start, end)
    high = random.randint(max(openval, closeval), end)
    low = random.randint(start, min(openval, closeval))
    change = random.randint(-5, 5)
    volume = random.randint(10000, 20000)
    dict_data.append({
        "Open": openval,
        "Close": closeval,
        "High": high,
        "Low": low,
        "Date": start_date,
        "Volume": volume
    })
    start += change
    end += change
    start_date += delta

df = pd.DataFrame(dict_data)
df.index = pd.to_datetime(df['Date'])

custom_colors = []
for i in range(len(df)):
    if i % 3 == 0:
        custom_colors.append(make_marketcolors(up='#29c9ff', down='#f3b5ff', edge='#29c9ff', wick='#29c9ff', ohlc='#32a852', volume='#a89132'))
    elif i%5 == 0:
        custom_colors.append("#000000")
    else:
        custom_colors.append(None)

plot(df, type='candle', style='yahoo', override_marketcolors=custom_colors, volume=True)
# plot(df, type='candle', style='yahoo', volume=True)
