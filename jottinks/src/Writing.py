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

from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import cPickle


class WritingCanvas(QGraphicsView, NoteWidget):
	buttonMappings = {
		Qt.LeftButton : "Pen",
		Qt.RightButton : "Knife"
		}
	"Qt.MiddleButton ???"
	
  	def __init__(self,writing=None):
		QGraphicsView.__init__(self)
		NoteWidget.__init__(self)
		if not writing:
			self.setScene(Writing())
		else:
			self.setScene(writing)
		#self.viewport().setAttribute(Qt.WA_PaintOutsidePaintEvent)
		
		self.toolDict = {
			"Pen" : Pen(self.scene(), self.viewport()),
			"Knife" : Knife(self.scene(), self.viewport()),
			"Spacer" : Spacer(self.scene(), self.viewport()),
			"Lasso" : Lasso(self.scene(), self.viewport())
			}
		self.noTool = Tool(None,None)
		self.currentTool = self.noTool
		
		self.setCursor(Qt.BlankCursor)
		
		self.actionList = None
		
		self.setRenderHint(QPainter.Antialiasing)
		
		self.connect(self.scene(),SIGNAL("updateSceneRect()"),self.updatePageSize)
		self.updatePageSize()
		
		self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
		
		self.centerOn(QPointF(0,0))
		
	def mouseMoveEvent(self,event):
		point = self.mapToScene(QPoint(event.x(),event.y()))
		self.currentTool.mouseMove(point)
		
	def mousePressEvent(self,event):
		point = self.mapToScene(QPoint(event.x(),event.y()))
		" We mouseUp in case another button was already held down. Common on tablets "
		self.currentTool.mouseUp(point)
		self.currentTool = self.toolDict[self.buttonMappings[event.button()]]
		self.currentTool.mouseDown(point)
		
	def mouseReleaseEvent(self,event):
		point = self.mapToScene(QPoint(event.x(),event.y()))
		self.currentTool.mouseUp(point)
		self.currentTool = self.noTool
		
	def updatePageSize(self):
		itemsRect = self.scene().itemsBoundingRect()
		itemsRect.setBottom(itemsRect.bottom() + 500)
		size = self.viewport().size()
		vPoint = self.mapToScene(QPoint(size.width(),size.height()))
		rect = QRectF(0,0,max(itemsRect.right(),vPoint.x()),max(itemsRect.bottom(),vPoint.y()))
		self.setSceneRect(rect)		
	
	def actions(self):
		if not self.actionList:
			# Eugh. Can this be made tidier in the full app? Look up action groups
			
			choosePen = KAction(KIcon("draw-freehand"),i18n("Pen"), self)
			def choosePenF():
				self.buttonMappings[Qt.LeftButton]="Pen"
			self.connect(choosePen,SIGNAL("triggered()"),choosePenF)
			
			chooseKnife = KAction(KIcon("edit-clear"),i18n("Knife"), self)
			def chooseKnifeF():
				self.buttonMappings[Qt.LeftButton]="Knife"
			self.connect(chooseKnife,SIGNAL("triggered()"),chooseKnifeF)
			
			chooseLasso = KAction(KIcon("select-rectangular"),i18n("Lasso"), self)
			def chooseLassoF():
				self.buttonMappings[Qt.LeftButton]="Lasso"
			self.connect(chooseLasso,SIGNAL("triggered()"),chooseLassoF)
			
			chooseSpacer = KAction(KIcon("arrow-down"),i18n("Spacer"), self)
			def chooseSpacerF():
				self.buttonMappings[Qt.LeftButton]="Spacer"
			self.connect(chooseSpacer,SIGNAL("triggered()"),chooseSpacerF)
			
			self.actionList = [choosePen,chooseKnife,chooseLasso,chooseSpacer]
		return self.actionList
			
class WritingTitle(QGraphicsView):
	def __init__(self,scene):
		QGraphicsScene.__init__(self)
		self.setScene(scene)
		self.setSceneRect(QRectF(25,25,100,100))
		self.centerOn(25,25)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setRenderHint(QPainter.Antialiasing)
		self.setAutoFillBackground(False)
		self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
		
		#self.setEnabled(False)
		
	def mouseMoveEvent(self,event):
		event.ignore()
		
	def mousePressEvent(self,event):
		event.ignore()
		
	def mouseReleaseEvent(self,event):
		event.ignore()
		
	def mouseDoubleClickEvent(self,event):
		event.ignore()
		
class Writing(QGraphicsScene,NoteData):
	def __init__(self):
		NoteData.__init__(self)
		QGraphicsScene.__init__(self)
		
		self.addRect(QRectF(25,25,1000,40),QPen(),QBrush(Qt.white))
		
	def updateSceneRect(self):
		self.emit(SIGNAL("updateSceneRect()"))
		
	def widget(self):
		return WritingCanvas(self)
	
	def titleWidget(self):
		return WritingTitle(self)
		
	def addStroke(self,stroke):
		self.addItem(stroke)
		
	def removeStroke(self,stroke):
		self.removeItem(stroke)
		self.updateSceneRect()
		
	def deleteSelection(self):
		for stroke in self.selectedItems():
			self.removeItem(stroke)
			self.updateSceneRect()
			
	def moveSelection(self,dx,dy):
		for stroke in self.selectedItems():
			stroke.moveBy(dx,dy)
			# Dont call updateSceneRect() because we will be doing smooth movement a few pixels at a time
			# !!! Change this if updateSceneRect() is made less expensive
				
	def strokesMeeting(self,stroke):
		return self.items(stroke.path(),Qt.IntersectsItemShape)
	
	def strokesIn(self,stroke):
		return self.items(stroke.path(),Qt.ContainsItemShape)
	
	def drawBackground(self,painter,rect):
		k = 30
		# This will occasionally draw more lines than is strictly neccesary
		# Get over it
		startx = (rect.left() // k) * k
		starty = (rect.top() // k)  * k
		
		paleGrey = QColor(100,100,100,30)
		painter.setPen(QPen(paleGrey))
		for x in range(startx,rect.right()+1,k):
			painter.drawLine(x,rect.top(),x,rect.bottom())
			
		grey = QColor(100,100,100,100)
		painter.setPen(QPen(grey))
		for y in range(starty,rect.bottom()+1,k):
			painter.drawLine(rect.left(),y,rect.right(),y)
			
	
	def __reduce__(self):
		return (	Writing,
				(),
				[item for item in self.items() if type(item)==Stroke]
			)
	
	def __setstate__(self,items):
		for item in items:
			self.addItem(item)
	
			
class Stroke(QGraphicsPathItem):
	def __init__(self, point, fineness=0, pen=None):
		QGraphicsPathItem.__init__(self)
		self.centrePoint = None
		self.skipCounter = 0
		self.fineness = fineness
		if not pen:
			brush = QBrush(Qt.black, Qt.SolidPattern)
			pen = QPen(brush, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
		self.setPen(pen)
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self.setPath(QPainterPath(point))

	def addPoint(self,point):
		self.skipCounter += 1
		if self.skipCounter == self.fineness:
			self.skipCounter = 0
			self.centrePoint = None
			path = self.path()
			path.lineTo(point)
			self.setPath(path)
			
	def moveBy(self,dx,dy):
		"QGraphicsItem.moveBy(self,dx,dy)"
		self.setPath(QTransform().translate(dx,dy).map(self.path()))
		
	def __str__(self):
		return str([str(point) for point in self]) + ", Bounds " + str(self.boundingRect())
	
	def __repr__(self):
		return str(self)
		
	def __getitem__(self,i):
		elem = self.path().elementAt(i)
		return QPointF(elem.x,elem.y)
	
	def __setitem__(self,i,point):
		self.path().setElementPositionAt(i,point.x(),point.y())
		
	def __len__(self):
		return self.path().elementCount()
		
	def __iter__(self):
		i = 0
		length = len(self)
		while i<length:
			yield self[i]
			i += 1
			
	def __reduce__(self):
		points = [point for point in self]
		return (	Stroke,
				(points.pop(0),self.fineness),
				(points, self.pen())
			)
			
	def __setstate__(self,state):
		(points,pen) = state
		for point in points:
			self.addPoint(point)
		self.setPen(pen)


class Tool:
	def __init__(self,writing,canvas):
		self.writing = writing
		self.canvas = canvas
	
	def mouseUp(self,point):
		pass
	
	def mouseDown(self,point):
		pass
	
	def mouseMove(self,point):
		pass
	

class Pen(Tool):
	def __init__(self,writing,canvas):
		Tool.__init__(self,writing,canvas)
		self.currentStroke = None
		brush = QBrush(QColor(50,50,100), Qt.SolidPattern)
		self.pen = QPen(brush, 1.2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
		
	def mouseDown(self,point):
		self.currentStroke = Stroke(point,1,self.pen)
		self.writing.addStroke(self.currentStroke)
		
	def mouseMove(self,point):
		self.currentStroke.addPoint(point)
				
	def mouseUp(self,point):
		self.currentStroke = None
		self.writing.updateSceneRect()
	
class Knife(Tool):
	def __init__(self,writing,canvas):
		Tool.__init__(self,writing,canvas)
		self.selection = None
		brush = QBrush(Qt.magenta, Qt.SolidPattern)
		self.pen = QPen(brush, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
		
	def mouseDown(self,point):
		self.selection = Stroke(point,1,self.pen)
		self.writing.addStroke(self.selection)
		
	def mouseMove(self,point):
		self.selection.addPoint(point)
		
	def mouseUp(self,point):
		self.writing.setSelectionArea(self.selection.path())
		self.writing.deleteSelection()
		self.writing.clearSelection()
		self.writing.removeStroke(self.selection)
		self.writing.updateSceneRect()
		self.selection = None
	
	
class Spacer(Tool):
	def __init__(self,writing,canvas):
		Tool.__init__(self,writing,canvas)
		self.y = None
		
	def mouseDown(self,point):
		rect = self.writing.sceneRect()
		rect.moveTop(point.y())
		path = QPainterPath()
		path.addRect(rect)
		self.writing.setSelectionArea(path)
		self.y = point.y()
		
	def mouseMove(self,point):
		y = point.y()
		for item in self.writing.selectedItems():
			item.moveBy(0,y - self.y)
		self.y = y
	
	def mouseUp(self,point):
		self.writing.clearSelection()
		self.writing.updateSceneRect()

	
class Lasso(Tool):
	""" !!! Messy little bugger . Could maybe split it into two classes which create each other"""
	def __init__(self,writing,canvas):
		Tool.__init__(self,writing,canvas)
		self.selection = None
		self.point = None
		brush = QBrush(Qt.blue, Qt.SolidPattern)
		self.pen = QPen(brush, 1.2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
		
	def mouseDown(self,point):
		selected = self.writing.selectedItems()
		if selected and any([stroke.boundingRect().contains(point) for stroke in selected]):
			self.point = point
		else:
			self.writing.clearSelection()
			self.selection = Stroke(point,1,self.pen)
			# !!! Hacky way to ensure that we can select things with a single click
			self.selection.addPoint(point + QPointF(1,1))
			self.selection.addPoint(point)
			self.writing.addStroke(self.selection)
		
	def mouseMove(self,point):
		selected = self.writing.selectedItems()
		if selected:
			delta = point - self.point
			self.writing.moveSelection(delta.x(),delta.y())
			self.point = point
		else:
			self.selection.addPoint(point)
		
	def mouseUp(self,point):
		selected = self.writing.selectedItems()
		if selected:
			self.writing.updateSceneRect()
		else:
			self.writing.setSelectionArea(self.selection.path())
			self.writing.removeStroke(self.selection)
			self.selection = None
		self.canvas.update()
