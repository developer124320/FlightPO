'''
Created on 25 Jan 2015

@author: Administrator
'''
from qgis.core import QgsDistanceArea, QGis
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnapper
from PyQt4.QtCore import Qt, SIGNAL
import define
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.helpers import MathHelper, Unit
from FlightPlanner.types import DistanceUnits
class LineCreateTool(QgsMapTool):
    '''
    classdocs
    '''


    def __init__(self, canvas, disType = DistanceUnits.M):
        '''
        Constructor
        '''
        self.canvas = canvas
        QgsMapTool.__init__(self, self.canvas)
        self.mSnapper = QgsMapCanvasSnapper(self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas,QGis.Line)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(1)
        self.rubberBandPt = QgsRubberBand(canvas, QGis.Point)
        self.rubberBandPt.setColor(Qt.red)
        self.rubberBandPt.setWidth(10)
        self.type = disType
        self.reset()

    def reset(self):
        self.startPoint = None
        self.endPoint = None
        self.isDrawing = False
        self.distance = 0.0
    def canvasReleaseEvent(self, e):
        if ( e.button() == Qt.RightButton ):
            self.emit(SIGNAL("resultLineCreate"), self.rubberBand.asGeometry())
            self.reset()
            self.isDrawing = False
        else:
            self.rubberBandPt.reset(QGis.Point)
            snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)            
            if self.startPoint == None:
                self.rubberBand.reset(QGis.Line)
                if snapPoint == None:
                    self.startPoint = self.toMapCoordinates(e.pos())
                else:
                    self.startPoint = snapPoint
                self.rubberBand.addPoint(self.startPoint)
                self.isDrawing = True
            else:
                if snapPoint == None:
                    self.endPoint = self.toMapCoordinates(e.pos())
                else:
                    self.endPoint = snapPoint
                self.rubberBand.addPoint(self.endPoint)
                self.startPoint = self.endPoint
    def canvasMoveEvent(self, e):
        self.rubberBandPt.reset(QGis.Point)
        snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)
        if snapPoint != None:
            self.rubberBandPt.addPoint(snapPoint)
            self.rubberBandPt.show()
        if self.isDrawing:
            if self.isDrawing:
                if snapPoint == None:
                    self.endPoint = self.toMapCoordinates(e.pos())
                else:
                    self.endPoint = snapPoint
            self.rubberBand.movePoint(self.endPoint)
    def deactivate(self):
        self.rubberBandPt.reset(QGis.Point)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))