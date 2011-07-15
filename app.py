#!/usr/bin/env python2
#################################
# app.py			#
#				#
# Copyright 2011 ThePsyjo	#
#				#
# distributed under the terms	#
# of the			#
# GNU General Public License v2	#
#################################
import sys
from PyQt4.QtGui import QApplication, QIcon

from classdir.MainWindow import MainWindow

app = QApplication(sys.argv)

#app.installTranslator(&translator)
app.setWindowIcon(QIcon('../res/appicon.png'))
app.setApplicationName('PyWebViewer')
app.setApplicationVersion('0.0.2')
app.setQuitOnLastWindowClosed(False)


w = MainWindow()

sys.exit(app.exec_())
