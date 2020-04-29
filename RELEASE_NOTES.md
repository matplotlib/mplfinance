| Version  |  Description   | Release Date |
|:---------|:-------------|:---------------|
| 0.12.3a3   | - `linecolor` kwarg for line plots<br> - implement save figure to in-memory buffer<br> -- Thank you Caleb Coffin @coffincw for contributing the above. | 2020-03-04 |
| 0.12.3a2   | - implement custom markers (issue#30)<br> - fix minor issue with chart `type` validator<br> -- Thank you Amir Atashin @amiaty for contributing the above.<br> - add internal functions: `_bypass_kwarg_validation()` and `_kwarg_not_implemented()` | 2020-02-21 |
| 0.12.3a1   | - fix issue#28: math.log crash on zero in data<br> - remove "Implemented" field from kwarg dicts<br> - yahoo style show colors for `ohlc bars` | 2020-02-16 |
| 0.12.3a0   | - kwarg `block=False` for non-blocking call to `mpf.plot()`<br> - customize aspect ratio, figure title, y-labels<br> - customize colors and other `style` aspects of plot<br> - `no_xgaps` now defaults to True: use `show_nontrading=True` to set no_xgaps to false<br> - secondary y-axis available to `make_addplot()`<br> - bug fix for volume widths | 2020-02-12 |
| 0.12.0a3   | Increase mav limit from 3 to 7 different mavs  | 2020-01-16 |
| 0.12.0a2   | Ability to save plot to a file (pdf, svg, png, jpg, ...) | 2020-01-14 |
| 0.12.0a1   | Ability to plot arbitrary user data (in addition to basic OHLCV data).<br> - both line and scatter plots available.<br> - optionally plot on either the "main" or "lower" (aka "volume") axis. | 2020-01-09 |
| 0.11.x   | Basic Plotting from Pandas DataFrame of OHLC bars and candlesticks.<br> - optional display of volume<br> - optional display of (up to 3 different) moving averages.<br> - old API still available by importing from "mplfinance/original_flavor" | 2019-12-20  |
| 0.10.x   | Old mpl-finance API set up as its own package<br> (i.e. removed from the matplotlib package). | 2016-09-08   |
