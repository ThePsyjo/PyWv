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
from PyQt4.QtCore import QUrl, SIGNAL
from time import sleep

PLUGIN_CLASS = 'Min1024b'
PLUGIN_NAME = 'Reload on less than 1024 received bytes'

class Min1024b(WebWidget):
	def __init__(self, name, cfg, parent = None):
		WebWidget.__init__(self, name, parent)

		self.config = cfg

		self.url.setUrl(self.config.loadLinks()[str(self.objectName())]['data'])

		self.connect(self, SIGNAL('done()'), self.check)

	def check(self):
		if self.webView.page().totalBytes() < 1024:
			sleep(2)
			self.reload_()
