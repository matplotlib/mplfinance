from PySide6.QtWidgets import *
from PySide6.QtCore import QThread, Signal
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import ( FigureCanvasQTAgg as FigureCanvas,  NavigationToolbar2QT as NavigationToolbar)
import mplfinance as mpl
import pandas as pd


class ChartWidget(QWidget):
    def __init__(self,main_window,item):
        super().__init__()
        #Main Window Assign
        self.main_window = main_window

    def updateChart(self,figure_in):
        # Generating Canvas Which Hold Our Plot
        self.canvas = FigureCanvas(figure_in)
        # Generating Matplot toolbar
        toolbar = NavigationToolbar(self.canvas)
        # Seting Canvas TO Layout
        self.ui.horizontalLayout.addWidget(self.canvas)
        # Seting Toolbar To Layout
        #self.ui.horizontalLayout.addWidget(toolbar)
        self.canvas.draw()



class ChartThread(QThread):
    # Major Difference PySide6 and PyQt6 is pysignal and signal
    figureReady = Signal(object)
    _name = ''

    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window
        
    def run(self):
            #Figure Return Here
            self.figure, self.ax = plot(self.main_window)
            # Figure Sending To Main Window With Signal
            self.figureReady.emit(self.figure)


def plot(self):
    # OHLCV Data
    idf = pd.read_csv('examples/data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)
    df = idf.loc['2011-07-01':'2011-12-30',:]
    fig, axlist = mpl.plot(
            df,
            returnfig= True,
            tight_layout= True,
            figsize =(4,4),
            style = 'yahoo',
            type = 'candle',
            scale_padding=0.25,
            )
    axlist[0].xaxis.set_tick_params(labelsize=5)
    axlist[0].yaxis.set_tick_params(labelsize=5)
    return fig, axlist[0]