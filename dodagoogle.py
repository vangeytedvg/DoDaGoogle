from PyQt5 import QtWidgets, QtGui, Qt
from frmMain_ui import Ui_MainWindow


class Doda (QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Doda, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    import sys
    import os

    app = QtWidgets.QApplication(sys.argv)
    main_form = Doda ()
    main_form.show()
    sys.exit(app.exec_())