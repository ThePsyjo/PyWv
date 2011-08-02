#################################
# plugin_DelayWidget.py		#
#				#
# Copyright 2011 ThePsyjo	#
#				#
# distributed under the terms	#
# of the			#
# GNU General Public License v2	#
#################################
from .webWidget import WebWidget
from PyQt4.QtCore import SIGNAL, QTimer

PLUGIN_CLASS = 'DelayWidget'
PLUGIN_NAME = 'Waits until no other DelayWidget is loading'

class DelayWidget(WebWidget):
	def __init__(self, name, cfg, parent = None):
		WebWidget.__init__(self, name, parent)

		self.config = cfg

		self.url.setUrl(self.config.loadLinks()[str(self.objectName())]['data'])

		self.timer = QTimer(self)
		self.timer.setInterval(1000)
		self.timer.setSingleShot(1)

		self.timeoutTimer = QTimer(self)
		self.timeoutTimer.setInterval(10000)
		self.timeoutTimer.setSingleShot(1)

		self.connect(self.timeoutTimer , SIGNAL('timeout()') , self.clear)
		self.connect(self.timer        , SIGNAL('timeout()') , self.reload_)
		self.connect(self              , SIGNAL('done()')    , self.clear)

	def clear(self):
		self.config.saveDelayWidgetBusy(False)

	def reload_(self):
		if not self.isVisible(): return
		if not self.timeoutTimer.isActive():
			self.timeoutTimer.start()
		if self.config.loadDelayWidgetBusy():
			self.timer.start()
		else:
			self.timeoutTimer.stop()
			self.config.saveDelayWidgetBusy(True)
			WebWidget.reload_(self)
