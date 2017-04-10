'''
Created on 25 Jan 2015

@author: Administrator
'''
from qgis.core import QgsDistanceArea, QGis
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnapper
from PyQt4.QtCore import Qt, SIGNAL
import define
from QgisHelper import QgisHelper
from FlightPlanner.helpers import MathHelper, Unit
from FlightPlanner.types import DistanceUnits
class MeasureTool(QgsMapTool):
    '''
    classdocs
    '''


    def __init__(self, canvas, txtBearing, disType = DistanceUnits.M):
        '''
        Constructor
        '''
        self.canvas = canvas
        self.txtBearing = txtBearing
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
            self.reset()
            self.emit(SIGNAL("captureFinished"))
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
                dist = MathHelper.calcDistance(self.startPoint, self.endPoint)
                    
                self.distance = self.distance + dist
                if self.type == DistanceUnits.M:
                    self.txtBearing.setText("%f"%round(self.distance, 4))
                elif self.type == DistanceUnits.NM:
                    self.txtBearing.setText("%f"%round(Unit.ConvertMeterToNM(self.distance), 4))
                elif self.type == DistanceUnits.FT:
                    self.txtBearing.setText("%f"%round(Unit.ConvertMeterToFeet(self.distance), 4))
                elif self.type == DistanceUnits.KM:
                    self.txtBearing.setText("%f"%round((self.distance / 1000), 4))
                elif self.type == DistanceUnits.MM:
                    self.txtBearing.setText(str(int(self.distance * 1000)))
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
            dist1 = MathHelper.calcDistance(self.startPoint, self.endPoint)
            dist1 = self.distance + dist1    
            if self.type == DistanceUnits.M:
                self.txtBearing.setText("%f"%round(dist1, 4))
            elif self.type == DistanceUnits.NM:
                self.txtBearing.setText("%f"%round(Unit.ConvertMeterToNM(dist1), 4))
            elif self.type == DistanceUnits.FT:
                self.txtBearing.setText("%f"%round(Unit.ConvertMeterToFeet(dist1), 4))
            elif self.type == DistanceUnits.KM:
                self.txtBearing.setText("%f"%round((dist1 / 1000), 4))
            elif self.type == DistanceUnits.MM:
                self.txtBearing.setText(str(int(dist1 * 1000)))
    def deactivate(self):
        self.rubberBandPt.reset(QGis.Point)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))