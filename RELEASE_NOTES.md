####
---

### <a name="v0.12.7a11"></a>v0.12.7a11 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To Be released 2021-03-30

- <a name="v0.12.7a11"></a>v0.12.7a11 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; merged 2021-03-26
  - Prior to this version, **`xlim`** kwarg accepted only float or int:
    - float as matplotlib date; (only when `show_nontrading=True`)
    - int or float as dataframe row number; (only when `show_nontrading=False`)
  - **`xlim`** kwarg now *also* accepts
    - date or datetime **string**
    - date or datetime **object** (`datetime.datetime` or `pandas.Timestamp`)

---

### <a name="v0.12.7a10"></a>v0.12.7a10 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; released 2021-03-15

- <a name="v0.12.7a10"></a>v0.12.7a10 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; merged 2021-03-15
  - Add warning when user tries to plot "too much data" which includes reference to documentation
  - Add [**documentation on "Too Much Data"**](https://github.com/matplotlib/mplfinance/wiki/Plotting-Too-Much-Data).
- <a name="v0.12.7a9"></a>v0.12.7a9 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; merged 2021-03-01
  - new kwarg **`fontscale`** to scale font sizes on plot.
  - fix bug in `mpf.make_mpf_style()`
    - was only an issue when kwargs `base_mpf_style` and `rc` are used at the same time; see comments in code for more detail.
- <a name="v0.12.7a9"></a>v0.12.7a9 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; merged 2021-02-27
  - fix `check_version.sh` to always fetch latest version of `pip`.
    - See https://travis-ci.community/t/pandas-version-advanced-starting-in-jan-2021-numpy-is-now-incompatible/11214

- <a name="v0.12.7a8"></a>v0.12.7a8 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; merged 2021-02-23
  - support `yscale` kwarg.  (See also [**`yscale.ipynb`**](https://github.com/matplotlib/mplfinance/blob/master/examples/yscale.ipynb), and [issue 21](https://github.com/matplotlib/mplfinance/issues/21)).

---

### <a name="v0.12.7a7"></a>v0.12.7a7 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; released 2021-02-22

- Support [**`type=hollow_and_filled` candles**](https://github.com/matplotlib/mplfinance/blob/master/examples/hollow_and_filled_candles.ipynb). &nbsp; (Thank you [Kenan Arik](https://github.com/KenanHArik))
- Add example to show [10 years of daily data and how resampling affects candlesticks](https://github.com/matplotlib/mplfinance/blob/master/examples/resample10years.ipynb).  &nbsp; (See also [issue 307](https://github.com/matplotlib/mplfinance/issues/307))
- new function: **`mpf.write_style_file(style,filename)`** allows users to save their custom mpf styles.
- support alias names for plot types.  <br>(for example "candle" is the same as "candlestick", and "hollow" is the same as "hollow_and_filled").
- new styles: "**ibd**" and "**kenan**".
- kwarg `scale_widths_adjustment` now supports `volume_linewidth`, `ohlc_linewidth`, and `candle_linewidth`.  <br>(see also [widths  notebook/tutorial](https://github.com/matplotlib/mplfinance/blob/master/examples/widths.ipynb))


---

### <a name="v0.12.7a5"></a>v0.12.7a5 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; released 2021-01-23

- Add `style_name` kwarg to `mpf.make_mpf_style()`
- Add `vcdopcod` kwarg to `mpf.make_marketcolors()` (volume color depends on price change-on-day).

---

### <a name="v0.12.7a4"></a>v0.12.7a4 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; released 2020-12-22

- fix [timezone bug](https://github.com/matplotlib/mplfinance/issues/236).
- set kwarg `tz_localize=False` for legacy timezone behavior

- <a name="v0.12.7a3"></a>v0.12.7a3 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; merged 2020-12-21
  - calculate volume exponent ( more efficient than extra call to `draw()`)
  - support `volume_exponent` kwarg to allow user to manually choose volume exponent.
  - add version information to pytest logs

- <a name="v0.12.7a2"></a>v0.12.7a2 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; merged 2020-10-21
  - Add "[growing candle animation](https://github.com/matplotlib/mplfinance/blob/master/examples/mpf_animation_growingcandle.py)" to examples.
  - Bug fix for [issue #279](https://github.com/matplotlib/mplfinance/issues/279) `Mpf_Figure.subplots()` not working (always raising exception).

- <a name="v0.12.7a1"></a>v0.12.7a1 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; merged 2020-08-16
  - Support passing `dict` for kwarg `title=` (instead of just string) to allow modification of title font and all other kwargs available to matplotlib's [`Figure.suptitle()`](https://matplotlib.org/3.3.4/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.suptitle): The dict must include `title=<string>`.  Then just add whatever `Figure.suptitle()` kwargs to the dict that is passed to mplfinance's kwarg `title=`.  [Thank you Teddy Rowan](https://github.com/matplotlib/mplfinance/pull/237)

---

### <a name="v0.12.7a0"></a>v0.12.7a0 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; released 2020-08-09
#### Enhancements

- [**External Axes Mode**](https://github.com/matplotlib/mplfinance/blob/master/markdown/subplots.md#external-axes-method)
  - [Issue #114: Display multiple plots in a row](https://github.com/matplotlib/mplfinance/issues/114).
  - [Issue #209: Allow plotting on the existing AXIS](https://github.com/matplotlib/mplfinance/issues/209).
  
- [**Animation Support**](https://github.com/matplotlib/mplfinance/blob/master/markdown/animation.md#animation-support-in-mplfinance):
  - [Issue #25: Support animation/live updating of OHLCV data plots](https://github.com/matplotlib/mplfinance/issues/25).
  
---
### <a name="v0.12.6a3"></a>v0.12.6a3 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; released 2020-06-28
- accept lower case column names in dataframe (i.e. 'close' is the same as 'Close') ([Issue #197](https://github.com/matplotlib/mplfinance/issues/197))
---
### <a name="v0.12.6a2"></a>v0.12.6a2 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; released 2020-06-28
- `tight_layout` now supports adjusting Figure borders (padding) around plot. ([Issue #196](https://github.com/matplotlib/mplfinance/issues/196))
---
### <a name="v0.12.6a1"></a>v0.12.6a1 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; released 2020-06-25
- `make_mpf_style()` may set `y_on_right=None`: prevent crash by treating `None` the same as `False`. ([Issue #190](https://github.com/matplotlib/mplfinance/issues/190))

---

### <a name="v0.12.6a0"></a>v0.12.6a0 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; released 2020-06-24
#### Enhancements
- **`make_addplot()`** enhancements:
  - **support `type=` ` ohlc ` and ` candle ` (issue [#168](https://github.com/matplotlib/mplfinance/issues/168))**
  - support ` mav ` kwarg
  - support `y_on_right` kwarg
  - support `ylim` kwarg
  - expand impact of `width` and `alpha` kwargs (originally affected only `make_addplot(data,type='bar')` plots).
     - use `alpha` also on `scatter` plots.
     - use `width` and `alpha` also on `line` plots (issue [#185](https://github.com/matplotlib/mplfinance/issues/185))
- improve default line-widths algorithm
- rename `set_ylim` kwarg to `ylim` to be consistent with `ylabel` kwarg.
- deprecate `set_ylim_panelB` (use `ylim` in `make_addplot()` instead).
#### Bug fixes
- `axisoff` and `tight_layout` should be independent of each other (issue [#180](https://github.com/matplotlib/mplfinance/issues/180))
- fix Spyder console block/hang when _not inline_ call `mpf.plot()`.  (issues [#151](https://github.com/matplotlib/mplfinance/issues/151) and [#183](https://github.com/matplotlib/mplfinance/issues/183))
- fix incorrect linestyles character for dotted (issue [#186](https://github.com/matplotlib/mplfinance/issues/186))
---

### <a name="v0.12.5a3"></a>v0.12.5a3 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; released 2020-06-16
#### Enhancements
- improvements to width adjustment algorithm (issue [#174](https://github.com/matplotlib/mplfinance/issues/174))
- automatic width adjustment now also adjusts `mav` lines widths. (issue [#171](https://github.com/matplotlib/mplfinance/issues/171))

---

### <a name="v0.12.5a2"></a>v0.12.5a2 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; released 2020-06-08
#### Enhancements
- Support setting `ylabel` in `make_addplot()` (Thank you [Andy Sum](https://github.com/AndySum) for coding.)
- Add `saxbelow` kwarg to `set_axisbelow()`, defaults to `True` so grid lines do not show through candles, etc.
#### Buf Fixes
- fix `tight_layout` issue [#156](https://github.com/matplotlib/mplfinance/issues/156) (`tight_layout` not affecting Figure Title; Thank you [Markus Schulze](https://github.com/fxhuhn) for pointing this out.)

---

### <a name="v0.12.5a1"></a>v0.12.5a1 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; released 2020-06-07
#### Enhancements
- **[Subplots: Create up to 10 "panels"](https://github.com/matplotlib/mplfinance/blob/master/markdown/subplots.md)**
  - Can modify relative sizes of panels
  - Can modify which is "main" panel
  - Can modify which is "volume" panel
  - addplot can plot to any panel
  - MACD example
- support bar charts in make_addplot (`type=` 'line', 'scatter', or 'bar')
- make_addplot scatter now supports *sequence of markers* and sequence of colors<br>(Thank you [Elan Ernest](https://github.com/ImportanceOfBeingErnest) for posting the [sequence of markers solution here](https://github.com/matplotlib/matplotlib/issues/11155#issuecomment-385939618))
- ability to custom format date/time labels ( ` datetime_format= `) (Thank you [Cam McLean](https://github.com/cammclean182))
- ability to rotate date/time labels (` xrotation= `)
- ability to turn axis off (`axisoff=True`) (Thank you [Will Whitty](https://github.com/tavurth) for testing, code review, and contributing code changes)
- support ` tight_layout=True `
- support ` fill_between= `
- new algorithm for adjustment of candle widths, line widths, volume widths, ohlc tick widths **default change** (Thank you [Charles](https://github.com/char101) for your help).
  - ability to scale the algorithm (up or down)
  - ability to override the algorithm (i.e. set width and linewidth of volume bars, candles, ohlc bars. (iss num 81))
- close plot when not needed to stay open **default change**
  - fixes "20 open plots" warning
  - removed code to close plots from regression tests: no longer needed
- support NaNs in data to indicate missing data (also fix bug related to min/max and mav when NaNs in data) **default change** (Thank you [Charles](https://github.com/char101) for your help)
  - allows display low liquidity
  - remove support for -1 meaning missing data.  -1 is now considered valid data.
- Travis check to ensure each Pull Request has a new version (Thank you [Aaron Soellinger](https://github.com/free-soellingeraj))
- remove rcParams context: modifications made by mplfinance are now availabile after calling mplfinance. **default change**

#### Bug Fixes
  - fix bug displaying a single candle
  - fix bug "StatisticsError" when only a single data point
  - fix poor choice of default color for ` type=line ` chart **default change**
  - fix `savefig` Figure Facecolor bug
  - fix ohlc bars color in "blueskies" style **default change**

---
---

### v0.12.4a0  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; released 2020-05-01

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
- **v0.12.3a3  &nbsp;&nbsp;&nbsp;&nbsp; released 2020-03-04**

  - `linecolor` kwarg for line plots &nbsp;&nbsp;&nbsp;&nbsp;(Thank you [Caleb Coffin @coffincw](https://github.com/coffincw))
  - implement save figure to in-memory buffer &nbsp;&nbsp;&nbsp;&nbsp;(Thank you [Caleb Coffin @coffincw](https://github.com/coffincw))
---
- **v0.12.3a2 &nbsp;&nbsp;&nbsp;&nbsp; released 2020-02-21**

  - implement custom markers (issue#30) &nbsp;&nbsp;&nbsp;&nbsp;(Thank you [Amir Atashin @amiaty](https://github.com/amiaty))
  - fix minor issue with chart `type` validator &nbsp;&nbsp;&nbsp;&nbsp;(Thank you [Amir Atashin @amiaty](https://github.com/amiaty))
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
