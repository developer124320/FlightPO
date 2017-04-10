from qgis.core import QGis
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnapper
from PyQt4.QtCore import Qt, SIGNAL
from FlightPlanner.helpers import Unit, MathHelper
from FlightPlanner.QgisHelper import QgisHelper, Geo
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
import define

class CaptureBearingTool(QgsMapTool):
    def __init__(self, canvas, txtBearing, txtBearingGeodetic = None):
        self.canvas = canvas
        self.txtBearing = txtBearing
        self.txtBearingGeodetic = txtBearingGeodetic
        QgsMapTool.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas,QGis.Line)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(1)
        self.mSnapper = QgsMapCanvasSnapper(canvas)
        self.M_PI = 3.14159265358979323846
        self.rubberBandPt = QgsRubberBand(canvas, QGis.Point)
        self.rubberBandPt.setColor(Qt.red)
        self.rubberBandPt.setWidth(10)
        self.reset()
        parent = self.parent()
        self.startPoint = None
        self.endPoint = None

        pass
    def reset(self):
        self.isDrawing = False
        self.rubberBand.reset(QGis.Line)
       
    def canvasPressEvent(self, e):       
        #self.isEmittingPoint = True
        self.rubberBandPt.reset(QGis.Point)
        snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)
        if self.isDrawing == False:            
            if snapPoint == None:
                self.startPoint = self.toMapCoordinates(e.pos())
            else:
                self.startPoint = snapPoint            
            self.isDrawing = True
        else:
            self.isDrawing = False
            if snapPoint == None:
                self.endPoint = self.toMapCoordinates(e.pos())
            else:
                self.endPoint = snapPoint            
            self.drawLine() 
            self.reset()
            startPointPlan = None
            endPointPlan = None
            startPointGeodetic = None
            endPointGeodetic = None
            unitDefault = None
            try:
                if self.txtBearingGeodetic == None:
                    startPointPlan = self.startPoint
                    endPointPlan = self.endPoint
                else:
                    if define._units == QGis.Meters:
                        startPointPlan = self.startPoint
                        endPointPlan = self.endPoint

                        startPointGeodetic = QgisHelper.CrsTransformPoint(startPointPlan.x(), startPointPlan.y(), define._xyCrs, define._latLonCrs)
                        endPointGeodetic = QgisHelper.CrsTransformPoint(endPointPlan.x(), endPointPlan.y(), define._xyCrs, define._latLonCrs)

                    else:
                        startPointGeodetic = self.startPoint
                        endPointGeodetic = self.endPoint

                        startPointPlan = QgisHelper.CrsTransformPoint(startPointGeodetic.x(), startPointGeodetic.y(), define._latLonCrs, define._xyCrs)
                        endPointPlan = QgisHelper.CrsTransformPoint(endPointGeodetic.x(), endPointGeodetic.y(), define._latLonCrs, define._xyCrs)
                    unitDefault = QGis.Meters

                pass
            except:
                return

            if isinstance(self.txtBearing, NumberBoxPanel):
                al = MathHelper.getBearing(startPointPlan, endPointPlan, unitDefault)
                al = Unit.ConvertRadToDeg(al)
                self.txtBearing.Value = round(al, 4)
            else:
                al = MathHelper.getBearing(startPointPlan, endPointPlan, unitDefault)
                al = Unit.ConvertRadToDeg(al)
                self.txtBearing.setText(str(round(al, 4)))

            if self.txtBearingGeodetic != None:
                al = MathHelper.getBearing(startPointGeodetic, endPointGeodetic, QGis.DecimalDegrees)
                al = Unit.ConvertRadToDeg(al)
                self.txtBearingGeodetic.Value = round(al, 4)
            
    def canvasMoveEvent(self, e):
        self.rubberBandPt.reset(QGis.Point)
        snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)
        if snapPoint != None:
            self.rubberBandPt.addPoint(snapPoint)
            self.rubberBandPt.show()
        if self.isDrawing:
            if snapPoint == None:
                self.endPoint = self.toMapCoordinates(e.pos())
            else:
                self.endPoint = snapPoint
            self.drawLine()
            
    def drawLine(self):        
        self.rubberBand.reset(QGis.Line)
        self.rubberBand.addPoint(self.startPoint, False)
        self.rubberBand.addPoint(self.endPoint, True)
        self.rubberBand.show()



    def deactivate(self):
        self.rubberBandPt.reset(QGis.Point)
#         self.rubberBand.reset(QGis.Line)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))
    