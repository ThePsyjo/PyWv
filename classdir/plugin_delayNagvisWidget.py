#################################
# plugin_delayNagvisWidget.py	#
#				#
# Copyright 2011 ThePsyjo	#
#				#
# distributed under the terms	#
# of the			#
# GNU General Public License v2	#
#################################
from .plugin_delayWidget import DelayWidget
from PyQt4.QtCore import QUrl

PLUGIN_CLASS = 'DelayNagvisWidget'
PLUGIN_NAME = 'Delayed Nagvis Widget'

class DelayNagvisWidget(DelayWidget):
	def __init__(self, name, cfg, parent = None):
		DelayWidget.__init__(self, name, cfg, parent)

		self.realUrl = QUrl()
		self.realUrl.setUrl(self.config.loadLinks()[str(self.objectName())]['data'])

	def resizeEvent(self, event):
		self.url.setUrl('%s&width=%d&height=%d' % (self.realUrl.toString(),
								self.width()/self.webView.zoomFactor()-20,
								self.height()/self.webView.zoomFactor()-65))
