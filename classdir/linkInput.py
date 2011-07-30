#################################
# linkInput.py			#
#				#
# Copyright 2011 ThePsyjo	#
#				#
# distributed under the terms	#
# of the			#
# GNU General Public License v2	#
#################################
from PyQt4.QtCore import QRegExp, Qt, SIGNAL, SLOT, QUrl
from PyQt4.QtGui import QWidget, QDialog, QRegExpValidator, QLineEdit, QPushButton, QGridLayout, QComboBox, QLabel, QFont, QMessageBox
from .pluginHelper import classdirPlugins


class StringInput(QDialog):
	def __init__(self, nameList, parent = None):
		QDialog.__init__(self)
		self.setParent(parent)
		self.setWindowFlags(Qt.Dialog)
		self.setWindowTitle(self.tr('new widget'))
		self.setModal(1)

		self.nameList = nameList

		self.re = QRegExp('.*')
		#self.re = QRegExp('[a-zA-Z][a-zA-Z0-9-_.]*')
		self.validator = QRegExpValidator(self.re, self)

		self.edit = QLineEdit(self)
		self.edit.setValidator(self.validator)

		self.okButton     = QPushButton(self.tr('&Ok'), self)
		self.cancelButton = QPushButton(self.tr('&Cancel'), self)

		self.connect(self.okButton,     SIGNAL('clicked()'), self.onOkClick)
		self.connect(self.cancelButton, SIGNAL('clicked()'), self, SLOT('reject()'))

		self.layout = QGridLayout(self)

		self.layout.addWidget(self.edit	 , 0 , 0  , 1 , 2)
		self.layout.addWidget(self.okButton     , 1 , 0)
		self.layout.addWidget(self.cancelButton , 1 , 1)

	def onOkClick(self):
		if not self.edit.text():
			self.edit.setText(self.tr('new name'))
			self.edit.selectAll()
			self.edit.setFocus()
		else:
			for l in self.nameList:
				if l == self.edit.text():
					self.edit.setText(self.tr('name exists'))
					self.edit.selectAll()
					return
			self.val = self.edit.text()
			self.accept()

	def getVal(self):
		return self.val

class LinkInput(QDialog):
	def __init__(self, cfg, parent = None):
		QDialog.__init__(self)
		self.setParent(parent)
		self.setWindowFlags(Qt.Dialog)
		self.setWindowTitle(self.tr('manage links'))
		self.setModal(1)

		self.config = cfg

		self.modified = []

		self.links = self.config.loadLinks()

		self.typeSelect = QComboBox(self)
		self.plugins = classdirPlugins()
		plugs = self.plugins.classes()
		self.typeSelect.addItems(['generic'] + plugs)

		self.nameSelect = QComboBox(self)
		self.nameSelect.addItems([l for l in self.links])

		self.connect(self.nameSelect, SIGNAL('currentIndexChanged(int)'), self.onNameSelectChange)

		self.lUserName   = QLabel(self.tr('userName'), self)
		self.lPass       = QLabel(self.tr('password'), self)
		self.lUrl	= QLabel(self.tr('Url'), self)
		self.lType       = QLabel(self.tr('widgetType'), self)
		self.lWidgetName = QLabel(self.tr('widgetName'), self)

		self.name    = QLineEdit(self)
		self.urlEdit = QLineEdit()
		self.passwd  = QLineEdit(self)
		self.passwd.setEchoMode(QLineEdit.Password)

		self.connect(self.typeSelect , SIGNAL('activated(int)')      , self.onChange)
		self.connect(self.urlEdit    , SIGNAL('textEdited(QString)') , self.onChange)
		self.connect(self.name       , SIGNAL('textEdited(QString)') , self.onChange)
		self.connect(self.passwd     , SIGNAL('textEdited(QString)') , self.onChange)

		self.newButton = QPushButton(self.tr('&new'), self)
		self.delButton = QPushButton(self.tr('&del'), self)
		self.savButton = QPushButton(self.tr('&save'), self)
		self.finButton = QPushButton(self.tr('&finish'), self)

		self.defFont = QFont()

		self.connect(self.newButton, SIGNAL('clicked()'), self.onNewClick)
		self.connect(self.delButton, SIGNAL('clicked()'), self.onDelClick)
		self.connect(self.savButton, SIGNAL('clicked()'), self.onSavClick)
		self.connect(self.finButton, SIGNAL('clicked()'), self.onFinClick)

		self.layout = QGridLayout(self)

		self.layout.addWidget(self.lWidgetName , 0 , 0)
		self.layout.addWidget(self.lType       , 2 , 0)
		self.layout.addWidget(self.lUrl	, 3 , 0)
		self.layout.addWidget(self.lUserName   , 4 , 0)
		self.layout.addWidget(self.lPass       , 5 , 0)

		self.layout.addWidget(self.nameSelect  , 0 , 1)
		self.layout.addWidget(self.typeSelect  , 2 , 1)
		self.layout.addWidget(self.urlEdit     , 3 , 1)
		self.layout.addWidget(self.name	, 4 , 1)
		self.layout.addWidget(self.passwd      , 5 , 1)

		self.layout.addWidget(self.newButton   , 1 , 2)
		self.layout.addWidget(self.delButton   , 2 , 2)
		self.layout.addWidget(self.savButton   , 3 , 2)
		self.layout.addWidget(self.finButton   , 4 , 2)

		self.setMinimumWidth(500)

		self.nameSelect.setCurrentIndex(self.nameSelect.count()-1)

	def onChange(self):
		self.savButton.setFont(QFont(self.defFont.defaultFamily(), -1, QFont.Bold))

	def onSavClick(self):
		if self.urlEdit.text().isEmpty():
			self.urlEdit.setText(self.tr("insert URL here"))
			self.urlEdit.selectAll()
		else:
			u = QUrl()
			u.setUrl(self.urlEdit.text())
			if not u.scheme():
				u.setScheme('http')
			u.setUserName(self.name.text())
			u.setPassword(self.passwd.text())

			self.config.saveLink(self.nameSelect.currentText(), { 'type' : self.typeSelect.currentText(), 'data' : u.toString()})

			#self.links = self.config.loadLinks()
			self.savButton.setFont(QFont())

			self.modified.append(str(self.nameSelect.currentText()))


	def onNewClick(self):
		inp = StringInput([l for l in self.links], self)
		if inp.exec_():
			self.name.clear()
			self.passwd.clear()
			self.urlEdit.clear()
			self.nameSelect.addItem(inp.getVal())
			self.nameSelect.setCurrentIndex(self.nameSelect.findText(inp.getVal()))

	def onDelClick(self):
		if QMessageBox(    QMessageBox.Question,
				self.tr('del_link'),
				self.tr('ask_del_link %1 ?').arg(self.nameSelect.currentText()),
				QMessageBox.Yes | QMessageBox.No,
				self).exec_() == QMessageBox.Yes:
			if not self.config.delLink(self.nameSelect.currentText()):
				print(('link "%s" not deleted !' % self.nameSelect.currentText()))
			self.links = self.config.loadLinks()
			self.nameSelect.removeItem(self.nameSelect.currentIndex())

	def onFinClick(self):
		self.accept()

	def onNameSelectChange(self):
		try:
			l = self.links[str(self.nameSelect.currentText())]
			u = QUrl(l['data'])

			self.name.setText(u.userName())
			self.passwd.setText(u.password())
			self.urlEdit.setText(u.toString(QUrl.RemoveUserInfo))
			self.typeSelect.setCurrentIndex(self.typeSelect.findText(l['type']))
		except Exception as e:
			#print e
			pass

	def modifiedWidgets(self):
		return set(self.modified)
