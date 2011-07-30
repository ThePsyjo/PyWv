#################################
# pluginHelper.py		#
#				#
# Copyright 2011 ThePsyjo	#
#				#
# distributed under the terms	#
# of the			#
# GNU General Public License v2	#
#################################
from glob import glob
from os import path

class classdirPlugins():
	def __init__(self):
		self.__plugins = []

		for plugin in glob('classdir/plugin_*.py'):
			file_ = path.basename(plugin.replace('.py', ''))
			plug = __import__('classdir.%s' % file_, fromlist=['PLUGIN_NAME', 'PLUGIN_CLASS'])
			self.__plugins.append({ 'name': plug.PLUGIN_NAME, 'class': plug.PLUGIN_CLASS, 'file': file_ })
			del plug
			del file_

	def names(self):
		return [p['name'] for p in self.__plugins]

	def classes(self):
		return [p['class'] for p in self.__plugins]

	def files(self):
		return [p['file'] for p in self.__plugins]

	def all_(self):
		return self.__plugins
	
	def classFromName(self, name):
		for p in self.__plugins:
			if p['name'] == name:
				return p['class']
			else:
				continue
		return ''

	def nameFromClass(self, class_):
		for p in self.__plugins:
			if p['class'] == class_:
				return p['name']
			else:
				continue
		return class_
