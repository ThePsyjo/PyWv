#################################
# MainWindow.py			#
#				#
# Copyright 2011 ThePsyjo	#
#				#
# distributed under the terms	#
# of the			#
# GNU General Public License v2	#
#################################
from PyQt4.QtCore import QTimer,SIGNAL, SLOT, pyqtSlot, Qt
from PyQt4.QtGui import QMainWindow, QStyleFactory, QApplication, QCloseEvent, QWidget, QStatusBar, QProgressBar, QStyleFactory, QMenu, QAction, QSystemTrayIcon, QIcon, QInputDialog, QKeySequence, QMessageBox
from .genericWidget import *
from .config import ConfigHandler
from .trayManager import TrayManager
from .linkInput import LinkInput
import os, time
from threading import Event
from pluginHelper import classdirPlugins
from . import res
plugins = classdirPlugins().all_()
for p in plugins:
#	print('registering %s from %s' % (p['class'], p['file']))
	exec('from %s import %s' % (p['file'], p['class']))

class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		
		self.setWindowTitle('%s %s' % (QApplication.applicationName(), QApplication.applicationVersion()));

		self.config = ConfigHandler(os.path.join(os.path.expanduser('~'), '.pywv/pywv.cfg'), self)

		self.setStyle(QStyleFactory.create(self.config.loadStyle()))
		if self.config.loadStyleSheet():
			self.setStyleSheet(self.config.loadStyleSheet())
		else:
			self.setStyleSheet("* {}") # without any stylesheet, windowstyles won't apply


		self.setDockOptions(QMainWindow.AnimatedDocks | QMainWindow.AllowNestedDocks | QMainWindow.AllowTabbedDocks | QMainWindow.VerticalTabs);

#		self.dummy = QWidget(self)
		self.setCentralWidget(QWidget(self))

		self.pBar = QProgressBar(self)
		self.pBar.setRange(0, self.config.loadReloadInterval())
		self.pBar.setFormat("%v Sekunden")

		self.statusBar = QStatusBar(self)
		self.setStatusBar(self.statusBar)
		self.statusBar.addWidget(self.pBar)

		self.reloadTimer = QTimer(self);
		self.reloadTimer.start(self.config.loadReloadInterval() * 1000)
		self.connect(self.reloadTimer, SIGNAL('timeout()'), self.reload_)

		self.statTimer = QTimer(self)
		self.statTimer.start(1000) # 1 sec
		self.connect(self.statTimer, SIGNAL('timeout()'), self.stat)

		self.mAction = self.menuBar().addMenu(self.tr("&Action"))
		self.mAction.addAction(self.tr("&update"), self.reload_, QKeySequence('F5'))
		self.mAction.addAction(self.tr("e&xit"), self.onExit, 'Ctrl+Q')

		self.mStyle = QMenu(self.tr("&Style"), self)
		for s in list(QStyleFactory.keys()):#       // fill in all available Styles
			self.mStyle.addAction(s)
		self.connect(self.mStyle, SIGNAL('triggered(QAction*)'), self.onStyleMenu)

		self.mOption = self.menuBar().addMenu(self.tr("&Options"))
		self.mOption.addAction(self.tr("reloadinterval") , self.onReloadTime , 'F8')
		self.mOption.addAction(self.tr("manage links")   , self.onNewLink    , 'F6')
		self.mOption.addSeparator()

		self.ontopAction       = QAction(self.tr("always on &top"),  self)
		self.showTrayAction    = QAction(self.tr("show tray &icon"), self)
		self.closeToTrayAction = QAction(self.tr("close to &tray"),  self)

		self.ontopAction.setCheckable(True)
		self.showTrayAction.setCheckable(True)
		self.closeToTrayAction.setCheckable(True)

		self.showTrayAction.setChecked   (self.config.loadShowTray()   )
		self.ontopAction.setChecked      (self.config.loadOntop()      )
		self.closeToTrayAction.setChecked(self.config.loadCloseToTray())

		self.connect(self.ontopAction       , SIGNAL('toggled(bool)') , self.onOntopAction)
		self.connect(self.showTrayAction    , SIGNAL('toggled(bool)') , self.onShowTrayAction)
		self.connect(self.closeToTrayAction , SIGNAL('toggled(bool)') , self.onCloseToTrayAction)

		self.mOption.addAction(self.ontopAction)
		self.mOption.addAction(self.showTrayAction)
		self.mOption.addAction(self.closeToTrayAction)
		self.mOption.addSeparator()
		self.mOption.addMenu(self.mStyle)

		self.trayIcon = QSystemTrayIcon(QIcon(':/appicon'), self);
		self.trayMgr = TrayManager(self.config, self.trayIcon)
		self.connect(self.trayIcon, SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self.onTrayIcon)
		if self.config.loadShowTray(): self.trayIcon.show()

		self.trayIconMenu = QMenu()
		self.trayIconMenu.addAction(self.tr("e&xit"), self.onExit)
		self.trayIcon.setContextMenu(self.trayIconMenu)

		self.mAbout = self.menuBar().addMenu(self.tr("&about"))
		self.mAbout.addAction(QApplication.applicationName(), self.onAboutAppAction)
		self.mAbout.addAction("Qt", self.onAboutQtAction)

		self.createWidgets()

		self.resize(self.config.loadWindowSize())
		self.restoreState(self.config.loadWindowState())
		self.reload_()
		if self.config.loadIsVisible():
			self.show()

	def __del__(self):
		self.config.saveWindowState(self.saveState())

	def createSingleWidget(self, name):
#		print 'crt', name, type(name), '\n', self.widgets
#		print 'crt', name, type(name)
		links = self.config.loadLinks()
		if links[name]['type'] == 'generic':
			self.widgets[name] = GenericWidget(name, self.config, self)
		else:
			pluginsAvail = classdirPlugins().all_()
			for plugin in pluginsAvail:
				if links[name]['type'] == plugin['class']:
					pluginClass = plugin['class']
					break
				else:
					continue

			exec('self.widgets[name] = %s(name, self.config, self)' % pluginClass)
		#	print(('loaded plugin', self.widgets[name]))

		self.addDockWidget(0x4, self.widgets[name])

	def delWidget(self, name):
		#print 'del', name, type(name), '\n', self.widgets
		self.removeDockWidget(self.widgets[name])
		self.widgets[name].deleteLater()
		self.widgets[name] = None
		del self.widgets[name]

	def createWidgets(self):
		self.widgets = {}
		for name in self.config.loadLinks():
			self.createSingleWidget(name)


	@pyqtSlot()
	def onExit(self):
		self.config.saveWindowSize(self.size())
		QApplication.exit();

	def closeEvent(self, event):
		self.config.saveWindowSize(self.size())
#	       	QApplication.exit()
		# tray is visible -> close to tray
		# else close app
		if self.trayIcon.isVisible():
			event.accept()
		else:
			QApplication.exit()
			return
		# if close-to-tray is set, do so
		if self.config.loadCloseToTray():
			event.accept()
		else:
			QApplication.exit()
			return;
		# save this state
		if	self.trayIcon.isVisible():	self.config.saveIsVisible(False)
		else:					self.config.saveIsVisible(True);
	@pyqtSlot()
	def reload_(self):
		for name in self.widgets:
			self.widgets[name].reload_()
		self.pBar.setValue(self.config.loadReloadInterval())
		self.reloadTimer.start(self.config.loadReloadInterval()*1000)

	@pyqtSlot()
	def stat(self):
		self.pBar.setValue(self.pBar.value()-1)
#		print([idx for idx in self.widgets])

	def onStyleMenu(self, a):
		QApplication.setStyle(QStyleFactory.create(a.text()))
		self.setStyle(QStyleFactory.create(a.text()))
		self.config.saveStyle(a.text())

	def onReloadTime(self):
		ok = False
		value, ok = QInputDialog.getInteger(self,
			self.tr("reloadinterval"), # title
			self.tr("insert time in s"), # text
			self.config.loadReloadInterval(), # default
			10, # minimum
			86400, # maximum (at least once a day)
			1, # step
			)
		if ok:
			self.config.saveReloadInterval(value)
			self.pBar.setRange(0,self.config.loadReloadInterval())
			self.reload_()

	def onNewLink(self):
		inp = LinkInput(self.config, self)
		if inp.exec_():
			# sync active widgets
			for name in inp.modifiedWidgets():
				if name in self.widgets:
					self.delWidget(name)
					self.createSingleWidget(name)
				else:
					self.createSingleWidget(name)

			# remove deleted
#			for name in self.widgets: print 'shown', name
#			for name in self.config.loadLinks(): print 'conf', name
			todel = []
			for name in self.widgets:
				if name not in self.config.loadLinks():
					todel.append(name)

			for widget in todel:
				self.delWidget(widget)

	def onOntopAction(self, b):
		if b:	self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
		else:	self.setWindowFlags(Qt.Dialog)
		self.setWindowIcon(QIcon(':/appicon'))
		self.show();
		self.config.saveOntop(b)

	def onShowTrayAction(self, b):
		if b:	self.trayIcon.show()
		else:	self.trayIcon.hide()
		self.config.saveShowTray(b)

	def onCloseToTrayAction(self, b):
		self.config.saveCloseToTray(b)

	def onTrayIcon(self, reason):
		if reason == QSystemTrayIcon.Trigger:
			if(self.isVisible()):
				self.config.saveWindowSize(self.size())
				self.hide()
				self.config.saveIsVisible(False)
			else:
				self.show()
				self.resize(self.config.loadWindowSize())
				self.config.saveIsVisible(True)

	def onAboutAppAction(self):
		QMessageBox.about(self, self.tr("&about"), self.tr("name %1 version %2").arg(QApplication.applicationName()).arg(QApplication.applicationVersion()))
	def onAboutQtAction(self):
		QMessageBox.aboutQt(self, self.tr("&about"))
