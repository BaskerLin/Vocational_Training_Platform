# coding=utf8
import sys
import dayu_widgets
from dayu_widgets.qt import *
from scripts import MainWindow

app = QApplication(sys.argv)
Window = MainWindow.MainWindow()
dayu_widgets.dayu_theme.apply(Window)
Window.show()
sys.exit(app.exec_())
