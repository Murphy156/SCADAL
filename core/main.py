import serial
import time
import sys
from core.QT.qt_show import *
from core.DataAnalysis.DataDeal import *
from PyQt6.QtWidgets import *

def main():
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec())


if __name__ == '__main__':
   main()