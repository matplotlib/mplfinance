[![Build Status](https://travis-ci.org/matplotlib/mplfinance.svg?branch=master)](https://travis-ci.org/matplotlib/mplfinance)

# mplfinance (to replace mpl-finance sometime in 2020).

## Introduction
My name is Daniel Goldfarb.  Last month (November 2019) I became the maintainer of `matplotlib/mpl-finance`.  This module consists of code extracted from the deprecated `matplotlib.finance` module along with a few examples of usage.  The code has been mostly un-maintained for the past three years.

## Purpose
I'd like to come up with a single statement of purpose to guide development going forward.  The original documention says `matplotlib.finance` is a set of functions "*for collecting, analyzing and plotting financial data.*"  --- I disagree with the "*for collecting*" part: **&nbsp;&nbsp; `mplfinance` is part of `matplotlib`.**  &nbsp;&nbsp;Therefore, I would say **the primary purpose of mplfinance is the visualization of financial data.**  However, since analyzing financial data often involves visualization (for example moving averages, oscillators, bollinger bands, etc.) let's say this **also includes analyzing financial data** (at least to the extent that such analysis involves visualization).  Putting this into a single statement to guide development going forward:

---
**The `mplfinance` package provides utilities for the visualization, and visual analysis, of financial data**

---

Let's leave the acquistion of financial data to other packages.  We will focus on visualization, and visual analysis, while other packages can focus on various ways of acquiring the data.  That said, we can certainly provide APIs for interfacing with packages that acquire financial data, in order to more easily and directly visualize and analyze that data.

## Going forward
My own take on the existing code is that it is too low-level, and thus too cumbersome to use.  
I have already started work on a higher-level API that allows users to call a single function, passing in nothing more than a Pandas Dataframe, to display either an OHLC bar or Candlestick plot.  The new API automatically does the additional matplotlib work that the caller otherwise has to do with the existing APIs.  For example, with the new API the caller does not have to worry about communicating to matplotlib that the x-axis is dates.  Even if the x-axis represents time (not dates) for intra-day data, the appropriate axis adjustment and labeling is done automatically under the hood.  (Of course, the API will accept data in other formats, not just pandas dataframes).

The new API will have options that allow the caller to customize some aspects of the plot; for example, whether or not they want to display volume, and/or moving averages, or other technical studies.  Providing a simpler, higher-level, API will allow users of `mplfinance` to focus on the visualization and analysis of financial data without having to learn intricate matplotlib details.

The above plan is based on my _possibly incorrect assumption_ that _most_ of the users of mpl-finance are like me in that their main desire is to do some sort of financial analysis, and quickly/easily visualize the results, and would prefer to avoid getting bogged down in the fine details of matplotlib.  That said, I expect the existing API, or similar low-level equivalent, will remain available for those who want to get into the matplotlib details and/or want to customize their plots perhaps more creatively.

I am very interested to hear from you how you are using mpl-finance, and what you think about my plans as stated above.  I will be honored if you will share your code with me, so I can see specifically *how you are calling the existing mpl-finance APIs, and what additional matplotlib stuff you are doing around them.*  I am particularly interested to hear about what you found frustrating or challenging in using mpl-finance, plus any suggestions you have for improvement.  You can reach me at dgoldfarb.github@gmail.com

Regarding the new API described above, I am hoping to have a version ready for beta testing in January 2020.
