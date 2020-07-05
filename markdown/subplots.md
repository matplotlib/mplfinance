---

# Subplots in mplfinance
#### "Subplots" is the matplotlib term for making **multiple plots** on the same figure.

---

## There are two ways to make subplots in mplfinance:
- Panels Method
- Matplotlib Method
#### Below is a brief description of each method, with links to tutorials on how to use each method:

---
### [The Panels Method](https://github.com/matplotlib/mplfinance/blob/master/examples/panels.ipynb)
* The Panels Method ***is easy to use and requires little or no knowledge of matplotlib***, and no need to import matplotlib.
* The Panels Method handles 95% of the most common types of financial plots and market studies.
* The Panels Method attains its simplicity, in part, by having certain limitations.<br>These limitiations are:
   - Subplots are always stacked vertically.
   - All subplots share the same x-axis.
   - There is a maximum of 10 subplots.
* The Panels Method is adequate to plot:
  - ohlc, candlesticks, etc.
  - with volume, and 
  - with one or more studies/indicators, such as:
    - MACD, DMI, RSI, Bollinger, Accumulation/Distribution Oscillator, Commodity Channel Index, Etc.
* [**See here for a tutorial and details on implementing the mplfinance Panels Method for subplots.**](https://github.com/matplotlib/mplfinance/blob/master/examples/panels.ipynb)

---

### The Matplotlib Method
* **NOTE: This method is _not yet implemented_.  It is presently expected to be available by the end of July 2020.**
* The `matplotlib` method requires the user to call various matplotlib methods, external to `mplfinance`, in order to create a Figure and Axes (**SubPlots**) that the user then passes into `mpf.plot()`.
  - **The user is responsible** to configure the size and location of the Axes objects within the Figure.
  - **The user is responsible** to display the Figure (as mplfinance will not `show()` the Figure).
* It is expected that this Matplotlib Method will give the user enough full control over the Figure and Axes to do whatever they want to do that matplotlib can do.  This includes:
  - plotting additional data (such as study data from multiple studies, trading signals, etc.) on as many subplots as desired.
  - plotting multiple ohlc/candlestick plots on the same axes.
  - plotting multiple candlestick plots side-by-side, or in any other geometry desired.
  - It is expected that this Matplotlib Method will also provide the ability to do **event handling** and/or **monitoring** (live updating), but presently I'm not 100% sure about this (due to my own limited experience with matplotlib event handling and monitoring).

 * When implemented, the Matplotlib Method will look something like this:  Users to use any matplotlib API they want to create their Figures and Axes (aka subplots), however there will be certain restrictions on how they are passed into `mpf.plot()`

1. `mpf.plot()` will have an `ax=` kwarg to pass in **any matplotlib Axes** that you want, however you **must also pass in the Figure** that contains that Axes instance using the `fig=` kwarg.  (If you pass in a _different_ Figure, one that does not contain your axes, then `mpf.plot()` won't know it, but behavior will be undefined, i.e. no guarantees).
2. If you specify the `ax=` kwarg when calling `mpf.plot()`, **and you also want to plot volume, then you must also** pass in an Axes instance for the volume; so instead of `volume=True`, you would say `volume=my_axes_for_volume` where my_axes_for_volume is an instance of a matplotlib Axes (i.e. subplot).
3. Similarly, if you specify `ax=` for `mpf.plot()` **then you must also specify** `ax=` for all calls to `make_addplot()`
