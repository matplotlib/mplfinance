import sys
# Import 'QApplication' from PySide 6 For Create Empty App With PySide6
from PySide6.QtWidgets import QApplication
# gui is file Where We Creating GUI Component Such As Button And Layout
from gui import MainWindow

if __name__ == "__main__":
    # sys.argv Created App Will Recieved Mouse and Keep Board Inputs
    app = QApplication(sys.argv)
    # Create Main Window of App
    window = MainWindow()
    # Show Main Window of App
    window.show()
    sys.exit(app.exec())