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

from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class NoteData(object):
	def __init__(self):
		self.title = "Untitled"
	
	def widget(self):
		raise NotImplementedError("I (" + str(type(self)) + ") dont know how to make my widget")
	
class NoteWidget(QWidget):
	buttonMappings = None
	def actions(self):
		raise NotImplementedError("I (" + str(type(self)) + ") dont know how to make my toolbar")
	
	def __init__(self):
		QWidget.__init__(self)
		self.setAttribute(Qt.WA_DeleteOnClose)