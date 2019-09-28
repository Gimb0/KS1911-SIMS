#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets
from MainUI import MainUI

app = QtWidgets.QApplication(sys.argv)
window = MainUI()
app.exec_()
app.aboutToQuit(window.closeApp())