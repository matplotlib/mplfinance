[![Build Status](https://travis-ci.org/matplotlib/mplfinance.svg?branch=master)](https://travis-ci.org/matplotlib/mplfinance)

# mplfinance
(to replace mpl-finance sometime in 2020).

---

## The `mplfinance` package provides utilities for the visualization, and visual analysis, of financial data

## Installation
### &nbsp;&nbsp;&nbsp;`pip install mplfinance`
   - mplfinance requires [matplotlib](https://pypi.org/project/matplotlib/) and [pandas](https://pypi.org/project/pandas/)


## Quick Start Usage
Start with a Pandas DataFrame containing OHLC data.  For example,


---

---

---

# HISTORY
## Introduction
My name is Daniel Goldfarb.  Last month (November 2019) I became the maintainer of `matplotlib/mpl-finance`.  That module is being deprecated in favor of the current `matplotlib/mplfinance`.  The old `mpl-finance` consisted of code extracted from the deprecated `matplotlib.finance` module along with a few examples of usage.  It has been mostly un-maintained for the past three years.  

It is my intention to archive `matplotlib/mpl-finance` soon to be replaced wth `matplotlib/mplfinance`.  The main reason for the rename is to avoid confusion with the hyphen and the underscore: As it was, `mpl-finance` was *installed with the hyphen, but imported with an underscore `mpl_finance`.*  Going forward it will be a simple matter of both installing and importing `mplfinance`.

At present (Dec 2019) this repository, `matplotlib/mplfinance`, contains an initial pre-beta, pre-release version of the new API (see below) for people to play with and provide feedback or pull requests for enhancements.

## The new API

My own take on the old `mpl-finance` API is that the methods were too low-level, and too cumbersome to use.  This current package contains a new API that automatically does the extra matplotlib work that the caller previously had to do "manually, on their own" with the old API.  

The new API is not yet in pypi, however it can be installed as follows:

   1. git clone this `matplotlib/mplfinance` repository
   2. cd into the repository (make sure you are in the directory that contains setup.py)
   3. run `pip install .`  # be sure to include the . (dot) after the word install.

The conventional way to import the new API is as follows:

    import mplfinance as mpf
    
The most common usage is to then call `mpf.plot(data)` where `data` is a `Pandas DataFrame` object containing Open, High, Low and Close data, with a Pandas `DatetimeIndex`.

---
### For details on how to call the new API, see the jupyter notebook in the examples folder:

### https://github.com/matplotlib/mplfinance/blob/master/examples/mplfinance_plot.ipynb

---
I am very interested to hear from you how you are using mpl-finance, and what you think of the new API.  I will be honored if you will share your code with me, so I can see specifically *how you are calling the existing mpl-finance APIs, and what additional matplotlib stuff you are doing around them.*  I am particularly interested to hear about what you found frustrating or challenging in using mpl-finance, plus any suggestions you have for improvement.  You can reach me at dgoldfarb.github@gmail.com

---
### old API availability

With this new `matplotlib/mplfinance` package installed, in addition to the new API, users can still access the old API by changing their import statments<br>
**from:**

    from mpl_finance import <method>

**to:**

    from mplfinance.original_flavor import <method>

where `<method>` indicates the method you want to import,<br>
**for example:**

    from mplfinance.original_flavor import candlestick_ohlc
