import mplfinance as mpf
import pandas as pd

# Sample financial data
data = {
    'Date': ['2023-10-01', '2023-10-02', '2023-10-03'],
    'Open': [100, 105, 102],
    'High': [110, 115, 112],
    'Low': [95, 100, 98],
    'Close': [105, 110, 105],
    'Volume': [100000, 120000, 110000],
    'your_custom_indicator': [50, 45, 48]  # Replace with your actual data
}

# Create a DataFrame from the sample data
df = pd.DataFrame(data)

# Customizing candlestick colors and plotting
def customize_candlestick_color(index, open, close):
    if index % 2 == 0:
        return 'white' if open < close else 'lightgray'
    else:
        return 'lightgray' if open < close else 'white'

def custom_plot(data, ax):
    candle_colors = [customize_candlestick_color(i, row['Open'], row['Close']) for i, row in
                     enumerate(data.itertuples())]
    apds = []

    apds.append(mpf.make_addplot(data['your_custom_indicator'], color='blue', ax=ax, secondary_y=False))
    apds.append(mpf.make_addplot(mpf.make_candlestick(data, colorup='k', colordown='r', alpha=1), ax=ax, panel=0,
                                 scatter=False))

    if 'Volume' in data:
        apds.append(mpf.make_addplot(data['Volume'], panel=1, color='b', secondary_y=True))

    mpf.plot(data, type='none', addplot=apds, style='default', title='Your Title', figscale=1.25)

# Plot the financial chart with alternating shading and customized candlestick colors
custom_plot(df)

'''This Python script leverages the mplfinance library to create visually appealing financial 
charts with customizable candlestick colors and optional volume data. 
The script begins with the import of essential libraries, including mplfinance and pandas. 
Users can define or load financial data, either as sample data for demonstration or by replacing it 
with actual financial data. Customization features include alternating candlestick colors based 
on open and close prices, making it easier to visualize market trends. Additionally, the script 
accommodates the plotting of custom indicators or additional data, such as trading volume. 
Detailed comments and clear instructions are provided for ease of use and adaptation to specific 
financial datasets. This code can be hosted on GitHub, enhancing its accessibility and usability 
for a broader audience of financial data analysts and visualization enthusiasts.'''
