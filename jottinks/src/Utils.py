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

from PyQt4.QtGui import *
from PyQt4.QtCore import *

# QPointF
def ptStr(self):
	return "QPointF " + str((self.x(),self.y()))

QPointF.__str__ = ptStr

def ptReduce(self):
	return (QPointF, (self.x(),self.y()))

QPointF.__reduce__ = ptReduce

# QRect

def rectStr(self):
	return "QRectF " + str(self.getCoords())

QRectF.__str__ = rectStr

# QPen

def penReduce(self):
	return (QPen,
		(self.brush(),self.width(),self.style(),self.capStyle(),self.joinStyle())
		)
		
QPen.__reduce__ = penReduce

# QBrush

def brushReduce(self):
	return (QBrush,
		(self.color(),self.style())
		)
		
QBrush.__reduce__ = brushReduce
