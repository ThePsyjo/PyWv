#################################
# plugin_nagvisWidget.py	#
#				#
# Copyright 2011 ThePsyjo	#
#				#
# distributed under the terms	#
# of the			#
# GNU General Public License v2	#
#################################
from .config import ConfigHandler
from .webWidget import WebWidget
from PyQt4.QtCore import QUrl, SIGNAL, QTimer

PLUGIN_CLASS = 'Min1024bWidget'
PLUGIN_NAME = 'Reload on less than 1024 received bytes'

class Min1024bWidget(WebWidget):
	def __init__(self, name, cfg, parent = None):
		WebWidget.__init__(self, name, parent)

		self.config = cfg

		self.url.setUrl(self.config.loadLinks()[str(self.objectName())]['data'])

		self.timer = QTimer(self)
		self.connect(self.timer , SIGNAL('timeout()') , self.reload_)
		self.connect(self       , SIGNAL('done()')    , self.check)

	def check(self):
		if self.webView.page().totalBytes() < 1024:
			self.timer.start(2000)
