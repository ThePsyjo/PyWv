#################################
# plugin_generic_cp1.py		#
#				#
# Copyright 2011 ThePsyjo	#
#				#
# distributed under the terms	#
# of the			#
# GNU General Public License v2	#
#################################
from .config import ConfigHandler
from .webWidget import WebWidget

PLUGIN_CLASS = 'GenericWidget1'
PLUGIN_NAME = 'das selbe wie generic'

class GenericWidget1(WebWidget):
	def __init__(self, name, cfg, parent = None):
		WebWidget.__init__(self, name, parent)

		self.config = cfg
		self.load(self.config.loadLinks()[str(self.objectName())]['data'])
		self.webView.setZoomFactor(self.config.loadZoomFactor(self.objectName()))
	def reload_(self):
		self.webView.reload()
