---

# Subplots in mplfinance
#### "Subplots" is the matplotlib term for making **multiple plots** on the same figure.

---

## There are two ways to make subplots in mplfinance:
- Panels Method
- External Axes Method
#### Below is a brief description of each method, with links to tutorials on how to use each method:

---
### [The Panels Method](https://github.com/matplotlib/mplfinance/blob/master/examples/panels.ipynb)
* The Panels Method ***is easy to use and requires little or no knowledge of matplotlib***, and no need to import matplotlib.
* The Panels Method handles 95% of the most common types of financial plots and market studies.
* The Panels Method attains its simplicity, in part, by having certain limitations.<br>These limitiations are:
   - Subplots are always stacked vertically.
   - All subplots share the same x-axis.
   - There is a maximum of 32 subplots.
* The Panels Method is adequate to plot:
  - ohlc, candlesticks, etc.
  - with volume, and
  - with one or more studies/indicators, such as:
    - MACD, DMI, RSI, Bollinger, Accumulation/Distribution Oscillator, Commodity Channel Index, Etc.
* [**See here for a tutorial and details on implementing the mplfinance Panels Method for subplots.**](https://github.com/matplotlib/mplfinance/blob/master/examples/panels.ipynb)

---

### [External Axes Method](https://github.com/matplotlib/mplfinance/blob/master/examples/external_axes.ipynb)
* The External Axes method of subplots **allows the user to create and manage their own Figure and Axes (SubPlots), and pass Axes into `mplfinance`**.
* Details on how to use this feature are described below.<br>&nbsp;&nbsp;(code examples can be found in the [**External Axes notebook**](https://github.com/matplotlib/mplfinance/blob/master/examples/external_axes.ipynb)).
* When passing `Axes` into `mplfinance`, some `mplfinance` features may be  _not_ available, or may behave differently.  For example,
  - The user is responsible to configure the size and geometry of the Figure, and size and location of the Axes objects within the Figure.
  - The user is responsible to display the Figure by calling **`mplfinance.show()`** (or `pyplot.show()`).
* Passing external Axes into `mplfinance` results in more complex code **but it also provides all the power and flexibility of `matplotlib` for those who know how to and what to use it.** This includes:
  - plotting on as many subplots as desired, in any geometry desired.
  - plotting multiple ohlc/candlestick plots on the same Figure or Axes.
  - plotting multiple candlestick plots side-by-side, or in any other geometry desired.
  - anitmating or updating plots in real time.
  - event handling
* Use method **`mpf.figure()`** to create Figures.<br>This method behaves exactly like [`pyplot.figure()`](https://matplotlib.org/3.3.0/api/_as_gen/matplotlib.pyplot.figure.html) except that **`mpf.figure()`** also accepts kwarg `style=` to set the mplfinance style.
* Call the usual methods for creating Subplot Axes on the figure:
  - [fig.add_subplot()](https://matplotlib.org/3.3.0/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.add_subplot)
  - [fig.add_axes()](https://matplotlib.org/3.3.0/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.add_axes)
  - [fig.subplots()](https://matplotlib.org/3.3.0/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.subplots)
* When calling the above subplot creation methods, if `fig` was creating using **`mpf.figure()`** then the Subplot Axes will inheret the mpfinance style information from the figure.  Alternatively the user may pass in kwarg `style=` to set different style information for an Axes than for the Figure or other Axes.
* Please note the following:
  - Use kwarg **`ax=`** to pass **any matplotlib Axes** that you want into **`mpf.plot()`**
  - If you also want to plot volume, **then you must pass in an Axes instance for the volume**,<br>&nbsp; so instead of `volume=True`, use **`volume=<myVolumeAxesInstance>`**.
  - If you specify `ax=` for `mpf.plot()` **then you must also specify** `ax=` **for all calls to `make_addplot()`**
