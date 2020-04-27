- There are many ways to contribute, including contributions as simple as **asking questions**, participating in discussions, suggesting enhancements, etc.  **All** of these are valuable!

- All of the usual/typical open source contribution guidelines apply (see for example, https://matplotlib.org/3.1.1/devel/contributing.html and https://opensource.guide/how-to-contribute/) 
so we will mention here just a few items here for which we may be particular in mplfinance.

- Coding:
  - If you write code, please don't use tabs, rather use spaces.
  - If you add a significant feature, that is a feature for which explaining its usage takes more than just a sentence or two, please also create a "tutorial notebook" for that feature.  For example, see the jupyter notebooks in the examples folder: https://github.com/matplotlib/mplfinance/tree/master/examples
  - If you add a significant feature, please also create a regression test file in the tests folder, https://github.com/matplotlib/mplfinance/tree/master/tests, similar to the other regression tests that are there.  *Often, the simplest way to do this is to take a few of the examples from the feature's "tutorial notebook"* (see previous point).
