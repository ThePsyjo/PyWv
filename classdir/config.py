#################################
# config.py			#
#				#
# Copyright 2011 ThePsyjo	#
#				#
# distributed under the terms	#
# of the			#
# GNU General Public License v2	#
#################################
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QUrl, QObject, QSize, QString
import os
import json
from zlib import compress, decompress
from binascii import hexlify, unhexlify
from copy import deepcopy
from shutil import copy as cp

class ConfigHandler(QObject):
	def __init__(self, filepath, parent = None):
		QObject.__init__(self)
		self.setParent(parent)
		self.filepath = filepath

		if not os.path.exists(os.path.dirname(filepath)):
			os.makedirs(os.path.dirname(filepath))

		self.doSave = True
 
		try:
			self.cfg = json.loads(open(filepath).read())
			cp(filepath, filepath + '.bak')
		except Exception as e:
			if os.path.exists(filepath):
				QMessageBox.warning(None, 'Configfile Error', 'Error while parsing the config File. Message is\n\n"%s"' % e)
#				print 'nerv'
				self.doSave = False
			else:
				self.saveFile()
				QMessageBox.information(None, 'Config created', 'Configuration file "%s" was created' % filepath)
#				print 'erstellt "%s"' % filepath

		self.create(['General'])
#		self.addLink('google', {'type':'generic', 'data':'http://www.google.de'})
#		self.addLink('osk', {'type':'generic', 'data':'http://osaftkonzentrat.funpic.de'})
#		self.addLink('ngz', {'type':'generic', 'data':'http://www.ngz-server.de'})
#		self.addLink('tp', {'type':'generic', 'data':'http://www.teamplay.de'})
#		self.addLink('sc', {'type':'generic', 'data':'http://www.servercamp.de'})
#		self.addLink('uc', {'type':'generic', 'data':'http://www.unitedcolo.de'})

	def create(self, l):
		itm = self.cfg
		for section in l:
			try:
				itm = itm[section]
				#print 's: habe', section
			except Exception as e:
				#print 's: lege an', section
				itm[section] = {}
				itm = itm[section]

	def getVal(self, l, default = None):
		itm = self.cfg
		for section in l:
			try:
				itm = itm[section]
				#print 'l: habe', section
			except:
				#print 'nicht da', section
				return default
		return itm

	def saveFile(self):

#		print ('%s save %s' % ('-'*30, '-'*30))

		toRenew = []
		for s in self.cfg['Links']:
			if type(s) is type(QString()):
				toRenew.append(s)

		for s in toRenew:
			self.cfg['Links'][unicode(s)] = self.cfg['Links'][s]
			del self.cfg['Links'][s]

		for s in self.cfg['Links']:
			if type(self.cfg['Links'][s]['type']) is type(QString()):
				self.cfg['Links'][s]['type'] = unicode(self.cfg['Links'][s]['type'])

#		for s in self.cfg['Links']:
#			print s, self.cfg['Links'][s]

#		print self.cfg

		with open(self.filepath, 'wb') as configfile:
			json.dump(self.cfg, configfile, indent=3)

	def __del__(self):
		if self.doSave:
			self.saveFile()

	def loadStyleSheet(self):
		return self.getVal(['General','Style'], '')

	def loadStyle(self):
		return self.getVal(['General','WindowStyle'], '')
	def saveStyle(self, style):
		self.cfg['General']['WindowStyle'] = str(style)
		self.saveFile()

	def loadWindowState(self):
		try:	return decompress(unhexlify(self.cfg['General']['WindowState']))
		except:	return ''
	def saveWindowState(self, state):
		self.cfg['General']['WindowState'] = hexlify(compress(state, 9))
		self.saveFile()

	def loadWindowSize(self):
		return QSize(self.getVal(['General','WindowSize','width'], 640), self.getVal(['General','WindowSize','height'], 480))
	def saveWindowSize(self, size):
		self.create(['General', 'WindowSize'])

		self.cfg['General']['WindowSize']['height'] = size.height()
		self.cfg['General']['WindowSize']['width'] = size.width()

		self.saveFile()

	def loadReloadInterval(self):
		return self.getVal(['General', 'ReloadInterval'], 600)
	def saveReloadInterval(self, interval):
		self.cfg['General']['ReloadInterval'] = interval
		self.saveFile()

	def loadLinks(self):
		try:	Links = deepcopy(self.cfg['Links'])
		except:	return {}
		for name in Links: Links[name]['data'] = decompress(unhexlify(Links[name]['data']))
		return Links
	def saveLinks(self, links):
		for name in links: links[name]['data'] = hexlify(compress(unicode(links[name]['data']), 9))
		self.cfg['Links'] = links
		self.saveFile()
	def addLink(self, name, link):
		Links = self.loadLinks()
		name = unicode(name)
		if name in Links: return False
		else:
			Links[name] = link
			self.saveLinks(Links)
			return True
	def saveLink(self, name, link):
		name = unicode(name)
		Links = self.loadLinks()
		if name not in Links:	return False
		else:
			Links[name] = link
			self.saveLinks(Links)
			return True
	def delLink(self, name):
		Links = self.loadLinks()
		name = unicode(name)
		if name in Links:
			del Links[name]
			self.saveLinks(Links)
			return True
		else: return False

	def loadZoomFactor(self, name):
		return self.getVal(['Links', unicode(name), 'zf'], 1)
	def saveZoomFactor(self, name, zf):
		Links = self.loadLinks()
		name = str(name)
		if name in Links:
			Links[name]['zf'] = zf
			self.saveLinks(Links)
			return True
		else:	return False
	
	def loadIsVisible(self):
		return self.getVal(['General', 'Visible'], True)
	def saveIsVisible(self, visible):
		self.cfg['General']['Visible'] = visible
		self.saveFile()

	def loadOntop(self):
		return self.getVal(['General', 'Ontop'], False)
	def saveOntop(self, ontop):
		self.cfg['General']['Ontop'] = ontop
		self.saveFile()

	def loadShowTray(self):
		return self.getVal(['General', 'ShowTray'], True)
	def saveShowTray(self, showTray):
		self.cfg['General']['ShowTray'] = showTray
		self.saveFile()

	def loadCloseToTray(self):
		return self.getVal(['General', 'CloseToTray'], True)
	def saveCloseToTray(self, closeToTray):
		self.cfg['General']['CloseToTray'] = closeToTray
		self.saveFile()

