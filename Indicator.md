---

# Indicators in mplfinance
#### "Indicators" In the world of investing is a vital tool, indicators typically refer to technical chart patterns deriving from the price, volume, or open interest of a given security.

---

## There are two ways to build indicators in mplfinance:
- Building a indicator with **`mpf.addplot()`** method
- Inbuilt Indicator Method (Upcoming Feature)
#### Below is a brief description of each method, with links to tutorials on how to use each method:

---
### [Addplot Method](https://github.com/matplotlib/mplfinance/blob/master/examples/addplot.ipynb)
* The `mpf.addplot()` Method ***is easy to use and requires little or no knowledge of matplotlib***, and no need to import matplotlib.
* The `mpf.addplot()` with `mpf.make_addplot` handles 95% of the most common types of indicators and market studies.
* The `mpf.make_addplot` method attains its simplicity, in part, by having certain limitations.<br>These limitations are:
   - Large code required for complex indicators.
   - Larger calculation required.
   - Legend box support Limited.
* The Inbuilt method is adequate for any kind of complex indicator:
  - Complex indicators can be handled.
  - Legend box fully supported
  - With one or more studies/indicators, such as:
    - Ichimoku, MACD, DMI, RSI, Bollinger, Accumulation/Distribution Oscillator, Commodity Channel Index, Etc.
* [**See here for a tutorial and details on implementing the mplfinance for addplot method.**](https://github.com/matplotlib/mplfinance/blob/master/examples/addplot.ipynb)


### [Following Example of Indicators](https://github.com/matplotlib/mplfinance/blob/master/examples/external_axes.ipynb)
*  [**The Alphatrend Indicator**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/alphatrend.ipynb)
   - For Building Alphatrend Indicator with  `make_addplot`. This method helps plot two lines, named k1 and k2. The area between two lines is filled with `fill_between` method. For color conditional formatting we use the `where`.
   - Details on how to implement Alphatrend Indicator Over are described below.<br>&nbsp;&nbsp;(code examples can be found in the [**examples/indicators/**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/alphatrend.ipynb))
*  [**Awesome Oscillator**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/awesome_oscillator.ipynb)
   - Use method `make_addplot` method Awesome Oscillator Build as Histogram Bar type of plot `bar` in a new panel with `panel` method
   - Details on how to implement Awesome Oscillator is described below.<br>&nbsp;&nbsp;(code examples can be found in the [**examples/indicators/**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/awesome_oscillator.ipynb))
*  [**Dochian Channel**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/donchian_channel.ipynb)
   - For Building Dochian Channel with `make_addplot`. This method helps plot three lines in this indicator, named upper, middle, and lower bands. The area between the upper and lower band is filled with `fill_between` method.
   - Details on how to implement Dochian Channel Over are described below.<br>&nbsp;&nbsp;(code examples can be found in the [**examples/indicators/**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/donchian_channel.ipynb))
*  [**Golden Cross Over**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/golden_cross.ipynb)
   - For Building Golden Cross with `make_addplot` we use two moving averages named short-term moving averages and long-term moving averages. When One Line Cross another that point is marked with `marker` with type `scatter`. while to change the color of the long-term moving average we use a custom function.
   - Details on how to implement Golden Cross Over are described below.<br>&nbsp;&nbsp;(code examples can be found in the [**examples/indicators/**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/golden_cross.ipynb))
*  [**Ichimoku Cloud**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/ichimoku_cloud.ipynb)
   - For Building Ichimoku Cloud with `make_addplot`. The following method helps to plot Five lines used in this indicator, named Tenkan-sen, Kijun-sen, Senkou_Span_A, Senkou_Span_B, Chikou_Span. The area between the  Senkou_Span_A and  Senkou_Span_B is filled with `fill_between` method.
   - Details on how to implement Ichimoku Cloud are described below.<br>&nbsp;&nbsp;(code examples can be found in the [**examples/indicators/**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/ichimoku_cloud.ipynb))
*  [**MACD**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/macd.py)
   - Use method `make_addplot` MACD is built as Histogram Bar type of plot `bar` in a new panel with `panel` method
   - Details on how to implement MACD are described below.<br>&nbsp;&nbsp;(code examples can be found in the [**examples/indicators/**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/macd.py))
*  [**MACD Histogram**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/macd_histogram_gradient.ipynb)
   - Use method `make_addplot` MACD with Histogram is built as Histogram Bar type of plot `bar` in a new panel with `panel` method. For Generating a color list for the histogram we use the custom function.
   - Details on how to implement MACD Histogram are described below.<br>&nbsp;&nbsp;(code examples can be found in the [**examples/indicators/**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/macd_histogram_gradient.ipynb))
*  [**Relative Strength Index**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/mpf_rsi_demo.py)
   - Use methods `make_addplot` and `panel` were used to plot rsi
   - Details on how to implement Relative Strength Index are described below.<br>&nbsp;&nbsp;(code examples can be found in the [**examples/indicators/**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/parabolic_sar.ipynb))
*  [**Parabolic SAR**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/mpf_rsi_demo.py)
   - For Building Parabolic SAR with `make_addplot`. This method helps plot two lines in this indicator, named upper and lower bands. The custom function is used to segregate uptrend and down-trending areas. Which later plot with type `scatter`
   - Details on how to implement Parabolic SAR are described below.<br>&nbsp;&nbsp;(code examples can be found in the [**examples/indicators/**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/parabolic_sar.ipynb))
*  [**Supertrend**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/supertrend.ipynb)
   - For Building Supertrend with `make_addplot`. This method helps plot three lines in this indicator, named upper, trendline, and lower bands. when the price is above the trendline area marked uptrend and downtrend with a custom function, The area between the upper band and high of the candle is filled with `fill_between` method.
   - Details on how to implement Supertrend described below.<br>&nbsp;&nbsp;(code examples can be found in the [**examples/indicators/**](https://github.com/matplotlib/mplfinance/blob/master/examples/indicators/supertrend.ipynb))
