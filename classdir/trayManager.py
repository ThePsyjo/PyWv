#################################
# trayManager.py		#
#				#
# Copyright 2011 ThePsyjo	#
#				#
# distributed under the terms	#
# of the			#
# GNU General Public License v2	#
#################################
from PyQt4.QtGui import QSystemTrayIcon
from PyQt4.QtCore import QObject, QTimer

class TrayManager(QObject):
	def __init__(self, cfg, ico, parent = None):
		QObject.__init__(self, parent)
		self.config = cfg
		self.icon = ico
		self.stack = []
		self.busy = False
	
	def checkMessageStack(self):
		if not self.busy:
			if self.stack:
				self.busy = True
				data = self.stack.pop(0)
				self.icon.showMessage(data['title'], data['msg'], data['ico'], data['time'])
				QTimer.singleShot(data['time'], self.freeStack)

	def freeStack(self):
		print('free stack')
		self.busy=False
		self.checkMessageStack()

	def showMessage(self, title, message, ico = QSystemTrayIcon.Information, time = 10000):
		self.stack.append({'title':title, 'msg':message, 'ico':ico, 'time':time})
		self.checkMessageStack()
