from PySide2.QtWidgets import QApplication
import sys
import os
from classies.my_window_1 import MyWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    # window.proverka()
    window.show()
    sys.exit(app.exec_())