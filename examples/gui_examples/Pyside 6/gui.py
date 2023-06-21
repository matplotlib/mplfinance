# import UI `ui_main_window` From QT Designer Call UI_MainWindow
from ui_main_window import Ui_MainWindow
# import Pyside6 > QtWidgets > QMainWindow
from PySide6.QtWidgets import QMainWindow
# import plot_signal.py Where We Working Qthread, mplfinance, mataplotlib
import plot_signal


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # imported UI set as self.ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Title Set 
        self.setWindowTitle("PySide6 Mplfinance Example")
        #UI Button Linked to Function chart_plot_im
        self.ui.plot.clicked.connect(self.chart_plot_im)

    def chart_plot_im(self):
        # Use of Qthread plot_signal.py
        self.temp_thread = plot_signal.ChartThread(self)
        # Signal Generated From Qthread Send To UI part with function handleFigureReady
        self.temp_thread.figureReady.connect(self.handleFigureReady)
        self.temp_thread.start()

    def handleFigureReady(self, figure):
        plot_signal.ChartWidget.updateChart(self,figure)
        

