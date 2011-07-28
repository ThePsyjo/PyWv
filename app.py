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
from PyQt4.QtGui import QApplication, QIcon, QMessageBox
from PyQt4.QtCore import QTranslator, QLocale

import classdir.res

app = QApplication(sys.argv)

translator = QTranslator()

if not translator.load(':/%s' % QLocale.languageToString(QLocale.system().language())):
	if not translator.load(":/en.qm"):
		QMessageBox.critical(None, "Error", "Something went wrong while loading language. See project-site if there are any updates.")
		sys.exit(1)

app.installTranslator(translator)
app.setWindowIcon(QIcon(':/appicon'))
app.setApplicationName('PyWebViewer')
app.setApplicationVersion('0.0.3')
app.setQuitOnLastWindowClosed(False)

from classdir.window import MainWindow

w = MainWindow()

sys.exit(app.exec_())
