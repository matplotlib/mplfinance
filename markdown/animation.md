### Animation Support in mplfinance

* **Real-time updates** to mplfinance plots are accomplished through the technique known as "**animation**"
* **`mplfinance`** animation requires the use of [**`mplfinance` External Axes Mode**](https://github.com/matplotlib/mplfinance/blob/master/markdown/subplots.md#external-axes-method)
* [**External Axes Mode**](https://github.com/matplotlib/mplfinance/blob/master/markdown/subplots.md#external-axes-method) allows mplfinance users to create and manage their own Figure and Axes (SubPlots), and pass Axes objects into mplfinance.  _This also gives users access to matplotlib's animation features_.
* It can be tricky to display animations properly in jupyter notebooks,<br>&nbsp; therefore, to keep things simple, the mplfinance animation examples are scripts.
* To run the animation examples, clone this repository, then **`cd`** into the **`mplfinance/examples`** folder, and run:
  - [**`python mpf_animation_demo1.py`**](https://github.com/matplotlib/mplfinance/blob/master/examples/mpf_animation_demo1.py)
  - [**`python mpf_animation_demo2.py`**](https://github.com/matplotlib/mplfinance/blob/master/examples/mpf_animation_demo2.py)
  - [**`python mpf_animation_macd.py`**](https://github.com/matplotlib/mplfinance/blob/master/examples/mpf_animation_macd.py)
  - [**`python mpf_animation_growingcandle.py`**](https://github.com/matplotlib/mplfinance/blob/master/examples/mpf_animation_growingcandle.py)    
* **NOTE: There are comments,** in each of the above example files, that explain what's going on and how to use animation with mplfinance.  You can view the code by clicking each of the above links.
