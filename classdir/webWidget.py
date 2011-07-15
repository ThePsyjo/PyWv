#################################
# webWidget.py			#
#				#
# Copyright 2011 ThePsyjo	#
#				#
# distributed under the terms	#
# of the			#
# GNU General Public License v2	#
#################################
from PyQt4.QtGui import QDockWidget, QKeyEvent
from PyQt4.QtWebKit import QWebView
from PyQt4.QtCore import SIGNAL, SLOT, pyqtSlot, QUrl
from . import config

class WebWidget(QDockWidget):
	def __init__(self, name, parent=None):
		QDockWidget.__init__(self, name, parent)
		self.setObjectName(name)
		
		self.webView = QWebView(self)
		self.url = QUrl()

		self.connect(self.webView, SIGNAL('loadFinished(bool)'), self.webViewDone)

		self.setWidget(self.webView)
	
	def webViewDone(self):
		self.emit(SIGNAL('done()'))

	def keyPressEvent(self, e):
		if e.text() == '+' or e.text() == '-' or e.text() == '0':
			if e.text() == '+':	self.webView.setZoomFactor(self.webView.zoomFactor() + .05)
			elif e.text() == '-':	self.webView.setZoomFactor(self.webView.zoomFactor() - .05)
			elif e.text() == '0':	self.webView.setZoomFactor(1)

			self.config.saveZoomFactor(self.objectName(), self.webView.zoomFactor())

	def load(self, url):
		self.url.setUrl(url)
#		print self.url.toString()
		self.webView.load(self.url)
