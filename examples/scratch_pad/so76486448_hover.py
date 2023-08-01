import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

# Dates to get stock data
start_date = "2020-01-01"
end_date = "2023-06-15"

# Fetch Tesla stock data
tesla_data = yf.download("TSLA", start=start_date, end=end_date)
tesla_weekly_data = tesla_data.resample("W").agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}
    ).dropna()

# Get the latest closing price
latest_price = tesla_weekly_data['Close'][-1]

# Create additional plot
close_price = tesla_weekly_data['Close']
apd = mpf.make_addplot(close_price, color='cyan', width=2)

# Plot the candlestick chart
fig, axes = mpf.plot(tesla_weekly_data,
                     type='candle',
                     addplot=apd,
                     style='yahoo',
                     title='Tesla Stock Prices',
                     ylabel='Price',
                     xlabel='Date',
                     volume=True,
                     ylabel_lower='Volume',
                     volume_panel=1,
                     figsize=(16, 8),
                     returnfig=True
                     )

# Move the y-axis labels to the left side
axes[0].yaxis.tick_left()
axes[1].yaxis.tick_left()

# Adjust the position of the y-axis label for price
axes[0].yaxis.set_label_coords(-0.08, 0.5)

# Adjust the position of the y-axis label for volume
axes[1].yaxis.set_label_coords(-0.08, 0.5)

# Set y-axis label for price and volume
axes[0].set_ylabel('Price', rotation=0, labelpad=20)
axes[1].set_ylabel('Volume', rotation=0, labelpad=20)

# Make the legend box
handles = axes[0].get_legend_handles_labels()[0]
red_patch = mpatches.Patch(color='red')
green_patch = mpatches.Patch(color='green')
cyan_patch = mpatches.Patch(color='cyan')
handles = handles[:2] + [red_patch, green_patch, cyan_patch]
labels = ["Price Up", "Price Down", "Closing Price"]
axes[0].legend(handles=handles, labels=labels)

# Add a box to display the current price
latest_price_text = f"Current Price: ${latest_price:.2f}"
box_props = dict(boxstyle='round', facecolor='white', edgecolor='black', alpha=0.8)
axes[0].text(0.02, 0.95, latest_price_text, transform=axes[0].transAxes,
             fontsize=12, verticalalignment='top', bbox=box_props)

# Function to create hover annotations
def hover_annotations(data):

    annot_visible = False
    annot = axes[0].text(0, 0, '', visible=False, ha='left', va='top')

    def onmove(event):
        nonlocal annot_visible
        nonlocal annot

        if event.inaxes == axes[0]:
            index = int(event.xdata)
            if index >= len(data.index):
                index = -1
            elif index < 0:
                index = 0
            values = data.iloc[index]
            mytext = (f"{values.name.date().strftime('%m/%d/%Y'):}\n"+
                      f"O: {values['Open']:.2f}\n"+
                      f"H: {values['High']:.2f}\n"+
                      f"L: {values['Low']:.2f}\n"+
                      f"C: {values['Close']:.2f}\n"+
                      f"V: {values['Volume']:.0f}"
                     )

            annot_visible = True
        else:
            mytext = ''
            annot_visible = False

        annot.set_position((event.xdata,event.ydata))
        annot.set_text(mytext)
        annot.set_visible(annot_visible)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', onmove)

    return annot


# Attach hover annotations to the plot
annotations = hover_annotations(tesla_weekly_data)

# Display the chart
plt.show()
