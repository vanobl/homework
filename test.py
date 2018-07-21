import sys
import os
import PySide2
# from PySide2.QtUiTools import QUiLoader
# from PySide2.QtWidgets import QApplication
# from PySide2.QtCore import QFile

from classies.test_form import Form
 
 
if __name__ == "__main__":
    app = PySide2.QtWidgets.QApplication(sys.argv)
    form = Form(os.path.join('mygui', 'main.ui'))
    sys.exit(app.exec_())