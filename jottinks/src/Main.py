#! /usr/bin/env python

"""
Copyright 2008 Jamie Brandon

This file is part of jottinKs.

    JottinKs is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    JottinKs is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with jottinKs.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys

from Note import *
from Writing import *
from NoteTree import *
import Utils

from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import cPickle as pickle

class JWindow(KMainWindow):
	def __init__(self):
		KMainWindow.__init__(self)
		
		self.showingNote = None
		self.noteTree = None
		self.treeTools = None
		#self.setNoteTree(NoteTree())
		
		self.stack = QStackedWidget()
		self.setCentralWidget(self.stack)
		
		self.noteTools = KToolBar("WritingBar", self, Qt.TopToolBarArea)
		self.addToolBar(self.noteTools)
		
		self.currentNoteWidget = None
	
	def loadNoteTree(self,file):
		self.setNoteTree(pickle.load(file))
		
	def setNoteTree(self,tree):
		if self.noteTree:
			self.stack.removeWidget(self.noteTree)
		
		self.noteTree = tree
		
		self.connect(self.noteTree,SIGNAL("setNote(PyQt_PyObject)"),self.setNoteIfShowing)
		self.connect(self.noteTree,SIGNAL("showNote(PyQt_PyObject)"),self.showNote)
		self.stack.insertWidget(0,self.noteTree)
		
		if self.treeTools:
			self.removeToolBar(self.treeTools)
		self.treeTools = KToolBar("TreeBar", self, Qt.TopToolBarArea)
		showNoteTree = KAction(KIcon("view-list-tree"),i18n("Show tree"), self)
		self.connect(showNoteTree,SIGNAL("triggered()"),self.showNoteTree)
		self.treeTools.addAction(showNoteTree)
		for action in self.noteTree.actions():
			self.treeTools.addAction(action)
		
		self.addToolBar(self.treeTools)
		
	def setNoteIfShowing(self,note):
		if self.showingNote:
			self.setNote(note)
		
	def setNote(self,note):
		widget = note.widget()
		widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))
		
		self.stack.addWidget(widget)
		if self.currentNoteWidget:
			self.stack.removeWidget(self.currentNoteWidget)
			self.currentNoteWidget.close()
		self.currentNoteWidget = widget
		
		self.noteTools.clear()
		for action in widget.actions():
				self.noteTools.addAction(action)
		
	def showNote(self,note):
		self.showingNote = True
		self.setNote(note)
		self.stack.setCurrentIndex(1)
		
	def showNoteTree(self):
		self.showingNote = False
		self.stack.setCurrentIndex(0)
		
	def closeEvent(self,event):
		file = open("example","w")
		pickle.dump(self.noteTree,file)
		file.close()
		KMainWindow.closeEvent(self,event)
	
if __name__ == '__main__':
	KCmdLineArgs.init(sys.argv, "pykdeapp", "", ki18n("PyKDE App"), "0.1", ki18n("My first app"))
	app = KApplication()
	jwin = JWindow()
	
	file = open("example","r")
	jwin.loadNoteTree(file)
	file.close()
	
	#jwin.setNoteTree(NoteTree())
	
	jwin.show()
	
	app.exec_()