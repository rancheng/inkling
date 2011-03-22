"""
Copyright 2008 Jamie Brandon, Mark Haines

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
import Utils
from Writing import *

from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import cPickle
import pickle


class NoteTree(QTreeWidget):
	def __init__(self, root=None):
		QTreeWidget.__init__(self)
		self.header().hide()
		self.setColumnCount(1)
		
		if root:
			self.root = root
		else:
			self.root = NoteTreeRoot()
		self.addTopLevelItem(self.root)
		self.root.setTitle()
			
		self.connect(self,SIGNAL("itemClicked (QTreeWidgetItem *,int)"),self.treeItemClicked)
			
		self.actionList = None
		self.selectedItem = self.root.next()
		
	def treeItemClicked(self,item,column):
		print "Got click", item.noteData.title
		self.clearSelection()
		self.selectedItem = item
		item.setSelected(True)
		self.scrollToItem(item)
		self.showNote(item.noteData)
		item.setTitle()
		
	def showNote(self,noteData):
		self.emit(SIGNAL("showNote(PyQt_PyObject)"),noteData)
		
	def click(self,item):
		print "Sent click", item.noteData.title
		self.emit(SIGNAL("itemClicked (QTreeWidgetItem *,int)"),item,0)
		
	# !!! Do I need this?
	def addNote(self,note):
		self.root.addChild(NoteTreeItem(note))
		
	def newNote(self):
		item = NoteTreeItem(Writing())
		self.selectedItem.parent().insertChild(self.selectedItem.index()+1,item)
		item.setTitle()
		self.click(item)
		print "added" , item, item.parent()
		
	def newSubNote(self):
		item = NoteTreeItem(Writing())
		self.selectedItem.addChild(item)
		item.setTitle()
		self.click(item)
		
	def deleteNote(self):
		print "Will delete:", self.selectedItem
		print "Parent is:" , self.selectedItem.parent()
		deletee = self.selectedItem
		self.click(deletee.previousItem())
		deletee.remove()
		
	def actions(self):
		if not self.actionList:
			newNote = KAction(KIcon("new"),i18n("New note"), self)
			self.connect(newNote,SIGNAL("triggered()"),self.newNote)
			
			newSubNote = KAction(KIcon("new"),i18n("New subnote"), self)
			self.connect(newSubNote,SIGNAL("triggered()"),self.newSubNote)
			
			deleteNote = KAction(KIcon("delete"),i18n("Delete note"), self)
			self.connect(deleteNote,SIGNAL("triggered()"),self.deleteNote)
			
			self.actionList = [newNote, newSubNote, deleteNote]
		return self.actionList
		
	def topLevelItems(self):
		i = 0
		length = self.root.childCount()
		while i<length:
			yield self.root.child(i)
			i += 1
			
	def __reduce__(self):
		(NoteTree,(self.root,))
		
	def __reduce_ex__(self,i):
		return self.__reduce__()
		
class NoteTreeItem(QTreeWidgetItem):
	def __init__(self, noteData=None, children = []):
		QTreeWidgetItem.__init__(self)
		self.noteData = noteData
		for child in children:
			self.addChild(child)
			
	# Cant call this until the item has been added to the tree
	def setTitle(self):
		self.treeWidget().setItemWidget(self,0,QLabel("Bugger"))
		for child in self.children():
			child.setTitle()
			
	def children(self):
		children = []
		for i in range(0,self.childCount()):
			children.append(self.child(i))
		return children
			
	def index(self):
		return self.parent().indexOfChild(self)
			
	def previousItem(self):
		i = self.index()
		if i==0:
			return self.parent()
		else:
			return self.parent().child(i-1)
		
	def nextItem(self):
		i = self.index()
		if i+1 == self.parent().childCount():
			return self.parent().nextItem()
		else:
			return self.parent().child(i+1)
				
	def remove(self):
		self.parent().removeChild(self)
		
	def __reduce__(self):
		return (NoteTreeItem,(self.noteData,self.children()))
	
class NoteTreeRoot(NoteTreeItem):
	def __init__(self,children=[]):
		NoteTreeItem.__init__(self,Writing(),children)
		self.setText(0,"Root")
	
	def parent(self):
		return self
	
	# This makes the new note function work. 
	# If we use index anywhere else it may cause some pain
	def index(self):
		return self.childCount() - 1
	
	def previous(self):
		return self
	
	def next(self):
		if self.childCount():
			return self.child(0)
		else:
			return self
		
	def remove(self):
		pass
		
	def __reduce__(self):
		return (NoteTreeRoot,(self.children(),))