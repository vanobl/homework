from PyQt5 import QtWidgets, uic
import sys
import os
from classies.my_window import MyWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    # window.proverka()
    window.show()
    sys.exit(app.exec_())