import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout,QWidget
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import ( FigureCanvasQTAgg as FigureCanvas,  NavigationToolbar2QT as NavigationToolbar)
import mplfinance as mpl
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Mplfinance Example")
        
        button = QPushButton("Plot", self)
        button.clicked.connect(self.on_button_click)
        
    def on_button_click(self):
        self.figure, axlist = plot(self)
        canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        toolbar = NavigationToolbar(canvas)
        layout.addWidget(canvas)
        layout.addWidget(toolbar)
        widget = QWidget()
        
        widget.setLayout(layout)
        self.setCentralWidget(widget)

def plot(self):
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())





