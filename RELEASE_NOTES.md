- **v0.12.4a0  &nbsp;&nbsp;&nbsp;&nbsp; Released 2020-05-01**

  - regression tests for new API
  - **[Renko plots](https://github.com/matplotlib/mplfinance/blob/master/examples/price-movement_plots.ipynb)** [(issue #11)](https://github.com/matplotlib/mplfinance/issues/11) &nbsp;&nbsp;&nbsp;&nbsp;(Thank you [Caleb Coffin @coffincw](https://github.com/coffincw))
  - **`style='binance'`** &nbsp;&nbsp;&nbsp;&nbsp;(Thank you [@akgna](https://github.com/akgnah))
  - return Figure and Axes (**`return_fig=True`**) ([issue #46](https://github.com/matplotlib/mplfinance/issues/46))
  - check that inputs are all float, and rename IPython.display.Iamge to avoid confusion with PIL.Image
  - ability to **`return_calculated_values=True`** ([issue #63](https://github.com/matplotlib/mplfinance/issues/63)) &nbsp;&nbsp;&nbsp;&nbsp;(Thank you [@WHug0](https://github.com/WHug0))
  - **[Point and Figure (`type='pnf'`) plots.](https://github.com/matplotlib/mplfinance/blob/master/examples/price-movement_plots.ipynb)**  &nbsp;&nbsp;&nbsp;&nbsp;(Thank you [Caleb Coffin @coffincw](https://github.com/coffincw))
  - custom column names &nbsp;&nbsp;&nbsp;&nbsp;(Thank you [@borgstrom](https://github.com/borgstrom))
  - **`set_ylim`** and **`set_ylim_panelB`** kwargs
  - **`hlines`**, **`vlines`**, **`alines`**, **`tlines`** **[Trend, Support, Resistance, and Trading/Signal lines](https://github.com/matplotlib/mplfinance/blob/master/examples/using_lines.ipynb)**
    - (Thank you [Aaron Soellinger @free-soellingeraj](https://github.com/free-soellingeraj) for writing regression tests for this.)
  
  

---
- **v0.12.3a3  &nbsp;&nbsp;&nbsp;&nbsp; Released 2020-03-04**

  - `linecolor` kwarg for line plots &nbsp;&nbsp;&nbsp;&nbsp;(Thank you Caleb Coffin @coffincw)
  - implement save figure to in-memory buffer &nbsp;&nbsp;&nbsp;&nbsp;(Thank you Caleb Coffin @coffincw)
---
- **v0.12.3a2 &nbsp;&nbsp;&nbsp;&nbsp; Released 2020-02-21**

  - implement custom markers (issue#30) &nbsp;&nbsp;&nbsp;&nbsp;(Thank you Amir Atashin @amiaty)
  - fix minor issue with chart `type` validator &nbsp;&nbsp;&nbsp;&nbsp;(Thank you Amir Atashin @amiaty)
  - add internal functions: `_bypass_kwarg_validation()` and `_kwarg_not_implemented()`
---
- **v0.12.3a1 &nbsp;&nbsp;&nbsp;&nbsp; Released 2020-02-16**

  - fix issue#28: math.log crash on zero in data
  - remove "Implemented" field from kwarg dicts
  - yahoo style show colors for `ohlc bars`
---
- **v0.12.3a0  &nbsp;&nbsp;&nbsp;&nbsp; Released 2020-02-12**

  - kwarg `block=False` for non-blocking call to `mpf.plot()`
  - customize aspect ratio, figure title, y-labels
  - customize colors and other `style` aspects of plot
  - `no_xgaps` now defaults to True: use `show_nontrading=True` to set no_xgaps to false
  - secondary y-axis available to `make_addplot()`
  - bug fix for volume widths
---
- **v0.12.0a3  &nbsp;&nbsp;&nbsp;&nbsp; Released 2020-01-16**

  - Increase mav limit from 3 to 7 different mavs
---
- **v0.12.0a2  &nbsp;&nbsp;&nbsp;&nbsp; Released 2020-01-14**

  - Ability to save plot to a file (pdf, svg, png, jpg, ...)
---
- **v0.12.0a1  &nbsp;&nbsp;&nbsp;&nbsp; Released 2020-01-09**

  - Ability to plot arbitrary user data (in addition to basic OHLCV data).
  - both line and scatter plots available.
  - optionally plot on either the "main" or "lower" (aka "volume") axis.
---
- **v0.11.x  &nbsp;&nbsp;&nbsp;&nbsp; Released 2019-12-20**

  - Basic Plotting from Pandas DataFrame of OHLC bars and candlesticks.
  - optional display of volume
  - optional display of (up to 3 different) moving averages.
  - old API still available by importing from "mplfinance/original_flavor"
---
- **v0.10.x  &nbsp;&nbsp;&nbsp;&nbsp; Released 2016-09-08**

  - Old mpl-finance API set up as its own package<br>(i.e. removed from the matplotlib package).
