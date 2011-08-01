#################################
# webWidget.py			#
#				#
# Copyright 2011 ThePsyjo	#
#				#
# distributed under the terms	#
# of the			#
# GNU General Public License v2	#
#################################
from PyQt4.QtGui import QDockWidget, QKeyEvent, QLabel, QProgressBar
from PyQt4.QtWebKit import QWebView
from PyQt4.QtCore import SIGNAL, SLOT, pyqtSlot, QUrl
from . import config

class WebWidget(QDockWidget):
	def __init__(self, name, parent=None):
		QDockWidget.__init__(self, name, parent)
		self.setObjectName(name)
		
		self.webView = QWebView(self)
		self.url = QUrl()
		self.lastUrl = QUrl()

		self.progressBar = QProgressBar(self)

		self.connect(self.webView, SIGNAL('loadFinished(bool)'), self.webViewDone)
		self.connect(self.webView, SIGNAL('loadProgress(int)'), self, SLOT('onWebViewStatusChange(int)'))

		self.setWidget(self.webView)



	def webViewDone(self):
		self.setTitleBarWidget(None)
		self.emit(SIGNAL('done()'))

	@pyqtSlot(int)
	def onWebViewStatusChange(self, val):
		self.progressBar.setValue(val)

	def keyPressEvent(self, e):
		if e.text() == '+' or e.text() == '-' or e.text() == '0':
			if e.text() == '+':	self.webView.setZoomFactor(self.webView.zoomFactor() + .05)
			elif e.text() == '-':	self.webView.setZoomFactor(self.webView.zoomFactor() - .05)
			elif e.text() == '0':	self.webView.setZoomFactor(1)

			self.config.saveZoomFactor(self.objectName(), self.webView.zoomFactor())

	def reload_(self):
		if not self.isVisible(): return
		self.setTitleBarWidget(self.progressBar)
		if self.url.toString() == self.lastUrl.toString():
			self.webView.reload()
		else:
			self.webView.load(self.url)
		self.lastUrl.setUrl(self.url.toString())
		self.webView.setZoomFactor(self.config.loadZoomFactor(self.objectName()))
