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
		self.setUniformRowHeights(True)
		
		if root == None:
			self.root = NoteTreeRoot(Writing())
		else:
			self.root = root
		self.addTopLevelItem(self.root)
		self.root.setTitle()
		self.setRootIndex(self.indexFromItem(self.root))
			
		self.connect(self,SIGNAL("itemClicked (QTreeWidgetItem *,int)"),self.itemClicked)
		self.connect(self,SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"),self.showNote)
			
		self.actionList = None
		self.setCurrentItem(self.root)
		
	def itemClicked(self,item,column=0):
		item.setExpanded(not(item.isExpanded()))
		self.setNote(item)
		
	def setNote(self,item):
		self.setCurrentItem(item)
		self.scrollToItem(item)
		self.emit(SIGNAL("setNote(PyQt_PyObject)"),item.noteData)
		
	def showNote(self,item,column=0):
		self.setNote(item)
		self.emit(SIGNAL("showNote(PyQt_PyObject)"),item.noteData)
		
	def newNote(self):
		item = NoteTreeItem(Writing())
		self.currentItem().parent().insertChild(self.currentItem().index()+1,item)
		item.setTitle()
		self.setNote(item)
		
	def newSubNote(self):
		item = NoteTreeItem(Writing())
		self.currentItem().addChild(item)
		item.setTitle()
		self.setNote(item)
		
	def deleteNote(self):
		deletee = self.currentItem()
		if deletee.prevItem() == deletee:
			self.setNote(deletee.parent())
		else:
			self.setNote(deletee.prevItem())
		deletee.remove()
		
	def nextNote(self):
		self.setNote(self.currentItem().nextItem())
		
	def prevNote(self):
		self.setNote(self.currentItem().prevItem())
		
	def subNote(self):
		self.setNote(self.currentItem().subItem())
		
	def parentNote(self):
		self.setNote(self.currentItem().parent())
		
	def actions(self):
		if not self.actionList:
			newNote = KAction(KIcon("new"),i18n("New note"), self)
			self.connect(newNote,SIGNAL("triggered()"),self.newNote)
			
			newSubNote = KAction(KIcon("new"),i18n("New subnote"), self)
			self.connect(newSubNote,SIGNAL("triggered()"),self.newSubNote)
			
			deleteNote = KAction(KIcon("delete"),i18n("Delete note"), self)
			self.connect(deleteNote,SIGNAL("triggered()"),self.deleteNote)
			
			prevNote = KAction(KIcon("back"),i18n("Previous note"), self)
			self.connect(prevNote,SIGNAL("triggered()"),self.prevNote)
			
			nextNote = KAction(KIcon("forward"),i18n("Next note"), self)
			self.connect(nextNote,SIGNAL("triggered()"),self.nextNote)
			
			subNote = KAction(KIcon("down"),i18n("Into subnote"), self)
			self.connect(subNote,SIGNAL("triggered()"),self.subNote)
			
			parentNote = KAction(KIcon("up"),i18n("Parent note"), self)
			self.connect(parentNote,SIGNAL("triggered()"),self.parentNote)
			
			self.actionList = [newNote, newSubNote, deleteNote, prevNote, nextNote, subNote, parentNote]
		return self.actionList
		
	def topLevelItems(self):
		return [self.topLevelItem(i) for i in range(0,self.topLevelItemCount())]
			
	def __reduce__(self):
		return (NoteTree,(self.root,))
		
	def __reduce_ex__(self,i):
		return self.__reduce__()
		
class NoteTreeItem(QTreeWidgetItem):
	def __init__(self, noteData=None, children = []):
		QTreeWidgetItem.__init__(self)
		self.noteData = noteData
		for child in children:
			self.addChild(child)
		self.setSizeHint(0,QSize(1000,40))
			
	# Cant call this until the item has been added to the tree
	def setTitle(self):
		title = self.noteData.titleWidget()
		title.setParent(self.treeWidget())
		self.treeWidget().setItemWidget(self,0,title)
		for child in self.children():
			child.setTitle()
			
	def children(self):
		return [self.child(i) for i in range(0,self.childCount())]
			
	def index(self):
		return self.parent().indexOfChild(self)
			
	def prevItem(self):
		i = self.index()
		if i==0:
			return self
		else:
			return self.parent().child(i-1)
		
	def nextItem(self):
		i = self.index()
		if i+1 == self.parent().childCount():
			return self
		else:
			return self.parent().child(i+1)
		
	def subItem(self):
		if self.childCount():
			return self.child(0)
		else:
			return self
				
	def remove(self):
		self.parent().removeChild(self)
		
	def __reduce__(self):
		return (NoteTreeItem,(self.noteData,self.children()))
	
class NoteTreeRoot(NoteTreeItem):
	def __init__(self,noteData,children=[]):
		NoteTreeItem.__init__(self,noteData,children)
		self.setText(0,"Root")
	
	def parent(self):
		return self
	
	# This makes the new note function work. 
	# If we use index anywhere else it may cause some pain
	def index(self):
		return self.childCount() - 1
	
	def prevItem(self):
		return self
	
	def nextItem(self):
		if self.childCount():
			return self.child(0)
		else:
			return self
		
	def remove(self):
		pass
	
	"""def removeChild(self,child):
		if self.childCount() == 1:"""
			
			
	def __reduce__(self):
		return (NoteTreeRoot,(self.noteData,self.children()))