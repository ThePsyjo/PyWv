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
from PyQt4.QtCore import QUrl

PLUGIN_CLASS = 'NagvisWidget'
PLUGIN_NAME = 'Nagvis Widget'

class NagvisWidget(WebWidget):
	def __init__(self, name, cfg, parent = None):
		WebWidget.__init__(self, name, parent)

		self.config = cfg

		self.realUrl = QUrl()

		self.realUrl.setUrl(self.config.loadLinks()[str(self.objectName())]['data'])

	def resizeEvent(self, event):
		self.url.setUrl('%s&width=%d&height=%d' % (self.realUrl.toString(),
								self.width()/self.webView.zoomFactor()-20,
								self.height()/self.webView.zoomFactor()-60))
