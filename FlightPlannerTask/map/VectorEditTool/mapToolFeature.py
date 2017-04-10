'''
Created on Apr 2, 2015
 
@author: jin
'''
from qgis.core import QgsFeatureRequest, QgsGeometry, QgsSnapper, \
        QgsVectorLayer, QgsLogger, QgsMapLayer, QGis, QgsFeature, QgsPoint
from qgis.gui import QgsMapCanvasSnapper, QgsMapTool, QgsRubberBand

from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QMessageBox, QColor

from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.helpers import MathHelper, Point3D
from FlightPlanner.polylineArea import PolylineAreaPoint, PolylineArea
from FlightPlanner.Dialogs.DlgUserInputPanel import DlgUserInputPanel
from FlightPlanner.types import TurnDirection
import define, math

class QgsMapToolAddCircularString(QgsMapTool):
    def __init__(self, layer, type = "Point"):
        QgsMapTool.__init__(self, define._canvas)
        self.canvas = define._canvas
        self.mSnapper = QgsMapCanvasSnapper(self.canvas)
        self.rubberBand = None
        self.geometryType = layer.geometryType()
        # if layer.geometryType() == QGis.Line:
        self.rubberBand = QgsRubberBand(self.canvas,QGis.Line)
        # elif layer.geometryType() == QGis.Polygon:
        #     self.rubberBand = QgsRubberBand(self.canvas,QGis.Polygon)
        # else:
        #     self.rubberBand = QgsRubberBand(self.canvas,QGis.Point)

        self.rubberBand.setBorderColor(Qt.red)
        self.rubberBand.setFillColor(QColor(0, 255, 0, 100))
        self.rubberBand.setWidth(1)
        if layer.geometryType() == QGis.Point:
            self.rubberBand.setWidth(10)
        self.rubberBandLine = QgsRubberBand(define._canvas, QGis.Line)
        self.rubberBandLine.setColor(Qt.red)
        self.rubberBandLine.setWidth(2)

        self.rubberBandPtList = []

        self.editingLayer = define._canvas.currentLayer()


        self.mouseClickCount = 0
        self.polylineArea = PolylineArea()
        self.resultPolylineArea = PolylineArea()
        self.type = type
        self.turnDirection = TurnDirection.Nothing
        self.dlgUserInputPanel = None
        self.centerPt0 = None
        self.centerPt1 = None
        self.bulge0 = None
        self.bulge1 = None
        self.realBulge = None
        self.beaforeRadius = None
        if self.type == "Radius":
            self.dlgUserInputPanel = DlgUserInputPanel(self.parent())
        self.reset()
    def reset(self):
        if self.geometryType == QGis.Line:
            self.rubberBand.reset(QGis.Line)
        elif self.geometryType == QGis.Polygon:
            self.rubberBand.reset(QGis.Polygon)
        else:
            self.rubberBand.reset(QGis.Point)
        self.rubberBand.setBorderColor(Qt.red)
        self.rubberBand.setFillColor(QColor(0, 255, 0, 100))
        self.rubberBand.setWidth(1)

        self.rubberBandLine.reset(QGis.Line)

        # self.rubberBandPt.reset(QGis.Point)

        self.startPoint = None
        self.middlePoint = None
        self.endPoint = None
        self.isDrawing = False

        self.mouseClickCount = 0
        self.lineType = "Line"
        self.resultPolylineArea = PolylineArea()
        self.turnDirection = TurnDirection.Nothing

        if len(self.rubberBandPtList) > 0:
            QgisHelper.ClearRubberBandInCanvas(define._canvas, self.rubberBandPtList)
            self.rubberBandPtList = []

    def canvasPressEvent(self, e):
        if self.geometryType == QGis.Point:
            return

        pt = None
        snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)
        if snapPoint == None:
            pt = self.toMapCoordinates(e.pos())
        else:
            pt = snapPoint
        if self.type == "Point":
            if self.mouseClickCount == 0:
                self.rubberBandLine.addPoint(pt)
                self.startPoint = pt
            elif self.mouseClickCount == 1:
                self.middlePoint = pt
                self.lineType = "Arc"
            else:
                self.resultPolylineArea.Add(self.polylineArea[0])
                self.startPoint = pt
                self.mouseClickCount = 0
                self.lineType = "Line"
                for p in self.polylineArea.method_14(4):
                    self.rubberBand.addPoint(p)
        else:
            if self.mouseClickCount == 0:
                self.rubberBandLine.addPoint(pt)
                self.startPoint = pt
            elif self.mouseClickCount == 1:
                # self.mouseClickCount = 0
                self.endPoint = pt
                centerPt = MathHelper.smethod_71(self.startPoint, self.endPoint, 0.5)

                self.dlgUserInputPanel.show()
                self.dlgUserInputPanel.Value = MathHelper.calcDistance(self.startPoint, centerPt)
                self.beaforeRadius = self.dlgUserInputPanel.Value
                self.polylineArea = PolylineArea()
                self.polylineArea.Add(PolylineAreaPoint(Point3D(self.startPoint.x(), self.startPoint.y()), 0.5))
                self.polylineArea.Add(PolylineAreaPoint(Point3D(pt.x(), pt.y()), 0.5))
                # for p in self.polylineArea.method_14(4):
                #     self.rubberBandLine.addPoint(p)
                self.lineType = "Arc"

            else:
                # self.polylineArea = PolylineArea()
                # r = self.dlgUserInputPanel.Value
                # d = MathHelper.calcDistance(self.startPoint, self.endPoint) / 2
                # angleT = (math.pi / 2 - math.acos(d / r)) * 2
                #
                # h = math.sqrt(r * r - d * d)
                # h0 = r - h
                # l = math.sqrt(d * d + h0 * h0)
                # angle0 = math.atan(h0 / d)
                # bearingT = None
                # if self.turnDirection == TurnDirection.Right:
                #     bearingT = MathHelper.getBearing(self.startPoint, self.endPoint) - angle0
                # else:
                #     bearingT = MathHelper.getBearing(self.startPoint, self.endPoint) + angle0
                # tempPt = MathHelper.distanceBearingPoint(self.startPoint, bearingT, l)
                # bearingTT = MathHelper.smethod_60(self.startPoint, tempPt, self.endPoint)
                #
                #
                # bulge = math.tan(angleT / 4) * self.turnDirection
                # self.centerPt0 = MathHelper.smethod_71(self.startPoint, self.endPoint, bulge)
                #
                # bulge = math.tan((math.pi * 2 - angleT) / 4) * self.turnDirection
                # self.centerPt1 = MathHelper.smethod_71(self.startPoint, self.endPoint, bulge)


                self.resultPolylineArea.Add(PolylineAreaPoint(Point3D(self.startPoint.x(), self.startPoint.y()), self.realBulge))

                self.polylineArea = PolylineArea()
                self.polylineArea.Add(PolylineAreaPoint(Point3D(self.startPoint.x(), self.startPoint.y()), self.realBulge))
                self.polylineArea.Add(PolylineAreaPoint(Point3D(self.endPoint.x(), self.endPoint.y())))


                self.startPoint = self.endPoint
                self.mouseClickCount = 0
                for p in self.polylineArea.method_14(4):
                    self.rubberBand.addPoint(p)
                self.lineType = "Line"
                self.dlgUserInputPanel.hide()

        self.mouseClickCount += 1


    def canvasReleaseEvent(self, e):
        if ( e.button() == Qt.LeftButton ):
            return
        if self.type == "Point":
            pt = None
            for pt in self.polylineArea.method_14(4):
                self.rubberBand.addPoint(pt)
            snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)
            if snapPoint == None:
                pt = self.toMapCoordinates(e.pos())
            else:
                pt = snapPoint
            self.rubberBand.addPoint(pt)
            self.resultPolylineArea.Add(self.polylineArea[0])
            self.resultPolylineArea.Add(PolylineAreaPoint(Point3D(pt.x(), pt.y())))
            pointList = None
            if self.geometryType == QGis.Line:
                pointList = self.resultPolylineArea.method_14()
            elif self.geometryType == QGis.Polygon:
                pointList = self.resultPolylineArea.method_14_closed()
            else:
                self.reset()
                return
        else:
            self.resultPolylineArea.Add(PolylineAreaPoint(Point3D(self.endPoint.x(), self.endPoint.y())))

            pointList = None
            if self.geometryType == QGis.Line:
                pointList = self.resultPolylineArea.method_14()
            elif self.geometryType == QGis.Polygon:
                pointList = self.resultPolylineArea.method_14_closed()
            else:
                self.reset()
                return
        layer = define._canvas.currentLayer()
        if layer.isEditable():
            f = QgsFeature(layer.pendingFields(), 0)
            if self.geometryType == QGis.Line:
                f.setGeometry(QgsGeometry.fromPolyline(pointList))
            elif self.geometryType == QGis.Polygon:
                f.setGeometry(QgsGeometry.fromPolygon([pointList]))
            pr = layer.dataProvider()
            pr.addFeatures([f])
            # layer.addFeature(f)
            define._canvas.refresh()
        self.reset()

    def canvasMoveEvent(self, e):
        if self.geometryType == QGis.Point:
            return
        # self.rubberBandPt.reset(QGis.Point)
        self.rubberBandLine.reset(QGis.Line)
        self.rubberBandLine.setColor(Qt.red)
        self.rubberBandLine.setWidth(1)
        self.rubberBandLine.setLineStyle(Qt.DotLine)

        pt = None
        snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)
        if snapPoint == None:
            pt = self.toMapCoordinates(e.pos())
        else:
            pt = snapPoint
        if self.type == "Point":
            if self.lineType == "Line":
                self.rubberBandLine.addPoint(self.startPoint)
                self.rubberBandLine.addPoint(pt)
            else:
                endPoint = pt
                self.polylineArea = PolylineArea()
                bulge = MathHelper.smethod_60(self.startPoint, self.middlePoint, endPoint)
                self.polylineArea.Add(PolylineAreaPoint(Point3D(self.startPoint.x(), self.startPoint.y()), bulge))
                self.polylineArea.Add(PolylineAreaPoint(Point3D(endPoint.x(), endPoint.y())))
                for p in self.polylineArea.method_14(4):
                    self.rubberBandLine.addPoint(p)
        else:
            if self.lineType == "Line":
                self.rubberBandLine.addPoint(self.startPoint)
                self.rubberBandLine.addPoint(pt)
            else:
                bearing = MathHelper.getBearing(self.startPoint, self.endPoint) + math.pi / 2
                newPt = MathHelper.distanceBearingPoint(pt, bearing, 100)
                intersectPt = MathHelper.getIntersectionPoint(pt, newPt, self.startPoint, self.endPoint)
                dist = MathHelper.calcDistance(intersectPt, pt)
                turnDirection = None
                bulge = MathHelper.smethod_60(self.startPoint, pt, self.endPoint)
                if bulge < 0:
                    self.turnDirection = TurnDirection.Right
                elif bulge > 0:
                    self.turnDirection = TurnDirection.Left
                else:
                    self.turnDirection = TurnDirection.Nothing

                self.polylineArea = PolylineArea()
                r = self.dlgUserInputPanel.Value
                d = MathHelper.calcDistance(self.startPoint, self.endPoint) / 2
                if d / r > 1:
                    self.dlgUserInputPanel.Value = self.beaforeRadius
                    r = self.dlgUserInputPanel.Value
                    d = MathHelper.calcDistance(self.startPoint, self.endPoint) / 2
                angleT = (math.pi / 2 - math.acos(d / r)) * 2

                h = math.sqrt(r * r - d * d)
                h0 = r - h
                l = math.sqrt(d * d + h0 * h0)
                angle0 = math.atan(h0 / d)
                bearingT = None
                if self.turnDirection == TurnDirection.Right:
                    bearingT = MathHelper.getBearing(self.startPoint, self.endPoint) - angle0
                else:
                    bearingT = MathHelper.getBearing(self.startPoint, self.endPoint) + angle0
                tempPt = MathHelper.distanceBearingPoint(self.startPoint, bearingT, l)
                bearingTT = MathHelper.smethod_60(self.startPoint, tempPt, self.endPoint)


                self.bulge0 = math.tan(angleT / 4) * self.turnDirection
                self.centerPt0 = MathHelper.smethod_71(self.startPoint, self.endPoint, self.bulge0)

                self.bulge1 = math.tan((math.pi * 2 - angleT) / 4) * self.turnDirection
                self.centerPt1 = MathHelper.smethod_71(self.startPoint, self.endPoint, self.bulge1)

                if MathHelper.calcDistance(self.centerPt0, pt) > r * 1.7:
                    self.polylineArea = PolylineArea()
                    self.polylineArea.Add(PolylineAreaPoint(Point3D(self.startPoint.x(), self.startPoint.y()), self.bulge1))
                    self.polylineArea.Add(PolylineAreaPoint(Point3D(self.endPoint.x(), self.endPoint.y())))
                    self.realBulge = self.bulge1
                else:#if MathHelper.calcDistance(self.centerPt1, pt) > r * 0.7:
                    self.polylineArea = PolylineArea()
                    self.polylineArea.Add(PolylineAreaPoint(Point3D(self.startPoint.x(), self.startPoint.y()), self.bulge0))
                    self.polylineArea.Add(PolylineAreaPoint(Point3D(self.endPoint.x(), self.endPoint.y())))
                    self.realBulge = self.bulge0

                # # bulge *= turnDirection
                # if math.fabs(bulge) > 1.5:
                #     bulge = 1.5 * self.turnDirection
                # else:
                #     bulge = 0.7 * self.turnDirection

                for p in self.polylineArea.method_14(4):
                    self.rubberBandLine.addPoint(p)
                self.beaforeRadius = r
                # centerPt = MathHelper.smethod_71(self.startPoint, self.endPoint, bulge)
                # self.dlgUserInputPanel.Value = MathHelper.calcDistance(self.startPoint, centerPt)

        self.rubberBandLine.show()

    def deactivate(self):
        # self.rubberBandPt.reset(QGis.Point)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))

class QgsMapToolAddFeature(QgsMapTool):
    def __init__(self, layer):
        QgsMapTool.__init__(self, define._canvas)
        self.canvas = define._canvas
        self.mSnapper = QgsMapCanvasSnapper(self.canvas)
        self.rubberBand = None
        self.geometryType = layer.geometryType()
        if layer.geometryType() == QGis.Line:
            self.rubberBand = QgsRubberBand(self.canvas,QGis.Line)
        elif layer.geometryType() == QGis.Polygon:
            self.rubberBand = QgsRubberBand(self.canvas,QGis.Polygon)
        else:
            self.rubberBand = QgsRubberBand(self.canvas,QGis.Point)

        self.rubberBand.setBorderColor(Qt.red)
        self.rubberBand.setFillColor(QColor(0, 255, 0, 100))
        self.rubberBand.setWidth(1)
        if layer.geometryType() == QGis.Point:
            self.rubberBand.setWidth(10)
        self.rubberBandPt = QgsRubberBand(define._canvas, QGis.Point)
        self.rubberBandPt.setColor(Qt.green)
        self.rubberBandPt.setWidth(10)
        self.reset()
        self.editingLayer = define._canvas.currentLayer()
        # self.dx = 0
        # self.dy = 0
        # self.editingLayer.beginEditCommand("Feature triangulation")

        # self.newFeature = QgsFeature()
        #
        # fields = self.editingLayer.dataProvider().fields()
        # if fields.count() != 0:
        #     self.newFeature.setFields(fields)

    def reset(self):
        if self.geometryType == QGis.Line:
            self.rubberBand.reset(QGis.Line)
        elif self.geometryType == QGis.Polygon:
            self.rubberBand.reset(QGis.Polygon)
        else:
            self.rubberBand.reset(QGis.Point)
        self.rubberBand.setBorderColor(Qt.red)
        self.rubberBand.setFillColor(QColor(0, 255, 0, 100))
        self.rubberBand.setWidth(1)

        self.rubberBandPt.reset(QGis.Point)

        self.startPoint = None
        self.endPoint = None
        self.isDrawing = False
    def canvasReleaseEvent(self, e):
        if self.geometryType == QGis.Point:
            # self.rubberBand.reset(QGis.Point)
            # self.rubberBandPt.reset(QGis.Point)
            snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)

            if snapPoint == None:
                self.endPoint = self.toMapCoordinates(e.pos())
            else:
                self.endPoint = snapPoint
            # self.rubberBand.addPoint(self.endPoint)

            geom = QgsGeometry.fromPoint(self.endPoint)
            # points = geom.asPolyline()

            if self.editingLayer.isEditable():
                f = QgsFeature(self.editingLayer.pendingFields(), 0)
                f.setGeometry(geom)
                pr = self.editingLayer.dataProvider()
                pr.addFeatures([f])
                # self.editingLayer.addFeature(f)
                define._canvas.refresh()

            self.emit(SIGNAL("resultCreate"), geom)
            self.reset()
            return
        if ( e.button() == Qt.RightButton ):


            geom = self.rubberBand.asGeometry()
            # points = geom.asPolyline()

            if self.editingLayer.isEditable():
                f = QgsFeature(self.editingLayer.pendingFields(), 0)
                f.setGeometry(geom)
                pr = self.editingLayer.dataProvider()
                pr.addFeatures([f])
                # self.editingLayer.addFeature(f)
                define._canvas.refresh()

            self.emit(SIGNAL("resultCreate"), self.rubberBand.asGeometry())
            self.reset()
            self.isDrawing = False
        else:
            self.rubberBandPt.reset(QGis.Point)
            # self.rubberBandPt.reset(QGis.Point)
            snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)
            if self.startPoint == None:
                # self.rubberBand.reset(QGis.Line)
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
        if self.geometryType == QGis.Point:
            return
        self.rubberBandPt.reset(QGis.Point)
        # self.rubberBandPt.reset(QGis.Point)
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

class QgsMapToolMoveFeature(QgsMapTool):
    def __init__(self, layer):
        QgsMapTool.__init__(self, define._canvas)
        self.canvas = define._canvas
        self.mSnapper = QgsMapCanvasSnapper(self.canvas)
        self.rubberBand = None
        self.geometryType = layer.geometryType()
        if self.geometryType == QGis.Line:
            self.rubberBand = QgsRubberBand(self.canvas,QGis.Line)
        elif self.geometryType == QGis.Polygon:
            self.rubberBand = QgsRubberBand(self.canvas,QGis.Polygon)
        else:
            self.rubberBand = QgsRubberBand(self.canvas,QGis.Point)

        self.rubberBand.setBorderColor(Qt.red)
        self.rubberBand.setFillColor(QColor(0, 255, 0, 100))
        self.rubberBand.setWidth(1)
        if self.geometryType == QGis.Point:
            self.rubberBand.setWidth(10)
        self.rubberBandPt = QgsRubberBand(define._canvas, QGis.Point)
        self.rubberBandPt.setColor(Qt.green)
        self.rubberBandPt.setWidth(10)
        self.reset()
        self.editingLayer = define._canvas.currentLayer()
        self.selectedFeature = None
        self.selectedGeom = None
        self.isDrawing = False
        pass

    def reset(self):
        if self.geometryType == QGis.Line:
            self.rubberBand.reset(QGis.Line)
        elif self.geometryType == QGis.Polygon:
            self.rubberBand.reset(QGis.Polygon)
        else:
            self.rubberBand.reset(QGis.Point)
        self.rubberBand.setBorderColor(Qt.red)
        self.rubberBand.setFillColor(QColor(0, 255, 0, 100))
        self.rubberBand.setWidth(1)

        self.rubberBandPt.reset(QGis.Point)


        self.endPoint = None


    def canvasPressEvent(self, e):
        self.startPoint = self.toMapCoordinates(e.pos())
        if self.geometryType == QGis.Polygon:
            featIter = define._canvas.currentLayer().getFeatures()
            containFlag = False
            for feat in featIter:
                geom = feat.geometry()
                if geom.contains(self.startPoint):
                    self.selectedFeature = feat
                    self.selectedGeom = self.selectedFeature.geometry()
                    containFlag = True
                    break
            if not containFlag:
                return
        elif self.geometryType == QGis.Line:
            snappingResults0 = self.mSnapper.snapToCurrentLayer(e.pos(), QgsSnapper.SnapToSegment)
            if ( snappingResults0[0] != 0 or len(snappingResults0[1]) < 1 ):
                return
            else:

                snappingResults = None
                for re in snappingResults0[1]:
                    snappingResults = re
                    if snappingResults.layer.isEditable():
                        break
                    return
                featId = snappingResults.snappedAtGeometry

                layer = define._canvas.currentLayer()
                self.selectedFeature = QgsFeature()
                layer.getFeatures(QgsFeatureRequest().setFilterFid(featId)).nextFeature(self.selectedFeature)
                self.selectedGeom = self.selectedFeature.geometry()
        self.rubberBand.setToGeometry(self.selectedGeom, define._canvas.currentLayer())
        self.isDrawing = True

    def canvasReleaseEvent(self, e):
        self.rubberBandPt.reset(QGis.Point)
        self.endPoint = self.toMapCoordinates(e.pos())
        # else:
        #     self.endPoint = snapPoint
        bearing = MathHelper.getBearing(self.startPoint, self.endPoint)
        dist = MathHelper.calcDistance(self.startPoint, self.endPoint)
        if self.geometryType == QGis.Point:
            pt = self.selectedGeom.asPoint()
            newpt = MathHelper.distanceBearingPoint(pt, bearing, dist)
            geom = QgsGeometry.fromPoint(newpt)
        elif self.geometryType == QGis.Line:
            ptList = self.selectedGeom.asPolyline()
            newPtList = []
            for pt in ptList:
                newpt = MathHelper.distanceBearingPoint(pt, bearing, dist)
                newPtList.append(newpt)
            geom = QgsGeometry.fromPolyline(newPtList)
        else:
            ptList = self.selectedGeom.asPolygon()[0]
            newPtList = []
            for pt in ptList:
                newpt = MathHelper.distanceBearingPoint(pt, bearing, dist)
                newPtList.append(newpt)
            geom = QgsGeometry.fromPolygon([newPtList])

        self.rubberBand.setToGeometry(geom, None)
        self.selectedGeom = geom
        # self.selectedFeature.setGeometry(geom)
        # self.selectedGeom = self.selectedFeature.geometry()
        currentLayer = define._canvas.currentLayer()
        if currentLayer.isEditable():
            dx = self.endPoint.x() - self.startPoint.x()
            dy = self.endPoint.y() - self.startPoint.y()
            currentLayer.translateFeature(self.selectedFeature.id(), dx, dy )
        define._canvas.refresh()
        self.reset()
        self.startPoint = None
        self.isDrawing = False
        self.selectedGeom = None

    def canvasMoveEvent(self, e):
        self.reset()
        self.rubberBandPt.reset(QGis.Point)
        if self.isDrawing:
            self.endPoint = self.toMapCoordinates(e.pos())
            bearing = MathHelper.getBearing(self.startPoint, self.endPoint)
            dist = MathHelper.calcDistance(self.startPoint, self.endPoint)
            if self.geometryType == QGis.Point:
                pt = self.selectedGeom.asPoint()
                newpt = MathHelper.distanceBearingPoint(pt, bearing, dist)
                geom = QgsGeometry.fromPoint(newpt)
                # self.rubberBand.addPoint(newpt)
            elif self.geometryType == QGis.Line:
                ptList = self.selectedGeom.asPolyline()
                newPtList = []
                for pt in ptList:
                    newpt = MathHelper.distanceBearingPoint(pt, bearing, dist)
                    newPtList.append(newpt)
                    # self.rubberBand.addPoint(newpt)
                geom = QgsGeometry.fromPolyline(newPtList)
            else:
                ptList = self.selectedGeom.asPolygon()[0]
                newPtList = []
                for pt in ptList:
                    newpt = MathHelper.distanceBearingPoint(pt, bearing, dist)
                    newPtList.append(newpt)
                    # self.rubberBand.addPoint(newpt)
            # self.rubberBand.show()
                geom = QgsGeometry.fromPolygon([newPtList])
            self.rubberBand.setToGeometry(geom, None)
            # self.rubberBand.show()
    def deactivate(self):
        self.rubberBandPt.reset(QGis.Point)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))


class QgsMapToolNodeTool(QgsMapTool):
    def __init__(self, layer):
        QgsMapTool.__init__(self, define._canvas)
        self.canvas = define._canvas
        self.mSnapper = QgsMapCanvasSnapper(self.canvas)
        self.rubberBand = None
        self.geometryType = layer.geometryType()
        if layer.geometryType() == QGis.Line:
            self.rubberBand = QgsRubberBand(self.canvas,QGis.Line)
        elif layer.geometryType() == QGis.Polygon:
            self.rubberBand = QgsRubberBand(self.canvas,QGis.Polygon)
        else:
            self.rubberBand = QgsRubberBand(self.canvas,QGis.Point)

        self.rubberBand.setBorderColor(Qt.red)
        self.rubberBand.setFillColor(QColor(0, 255, 0, 100))
        self.rubberBand.setWidth(2)
        if layer.geometryType() == QGis.Point:
            self.rubberBand.setWidth(10)

        self.rubberBandLine = QgsRubberBand(self.canvas,QGis.Line)
        self.rubberBandLine.setColor(Qt.blue)
        self.rubberBandLine.setWidth(2)

        self.rubberBandPt = QgsRubberBand(define._canvas, QGis.Point)
        self.rubberBandPt.setColor(Qt.green)
        self.rubberBandPt.setWidth(10)
        self.reset()
        self.editingLayer = define._canvas.currentLayer()
        self.littleRubberBandDrawing = False
        self.mouseClickCount = 0
        self.isDrawing = False

        self.pointBubberBandList = []
        self.selectedVertexID = 0
        self.selectedFeatureID = None
        self.startPoint = None
        self.middlePoint = None
        self.endPoint = None
        self.beforeFeatureID = None

        self.vertexPlace = ""
        self.vertexID = None

        self.vertexIdList = []
        self.selectedPointList = None

    def reset(self):
        if self.geometryType == QGis.Line:
            self.rubberBand.reset(QGis.Line)
        elif self.geometryType == QGis.Polygon:
            self.rubberBand.reset(QGis.Polygon)
        else:
            self.rubberBand.reset(QGis.Point)
        self.rubberBand.setBorderColor(Qt.red)
        self.rubberBand.setFillColor(QColor(0, 255, 0, 100))
        self.rubberBand.setWidth(2)

        self.rubberBandLine.reset(QGis.Line)
        self.rubberBandLine.setColor(Qt.blue)
        self.rubberBandLine.setWidth(2)

        self.rubberBandPt.reset(QGis.Point)


        self.startPoint = None
        self.middlePoint = None
        self.endPoint = None
        self.isDrawing = False

        self.vertexIdList = []
        # self.beforeFeatureID = None
    def keyPressEvent(self, keyEvent):
        if keyEvent.key() == Qt.Key_Backspace or keyEvent.key() == Qt.Key_Delete:
            layer = define._canvas.currentLayer()
            if layer.isEditable():
                if self.selectedFeatureID != None:
                    layer.deleteVertex(self.selectedFeatureID, self.selectedVertexID)
                    define._canvas.refresh()

                    pointList = []


                    feat = QgsFeature()
                    layer.getFeatures(QgsFeatureRequest().setFilterFid(self.selectedFeatureID)).nextFeature(feat)
                    geom = feat.geometry()
                    pointList = []
                    if geom.type() == QGis.Line:
                        pointList = geom.asPolyline()
                    elif geom.type() == QGis.Polygon:
                        pointList = geom.asPolygon()[0]

                        # pointList.pop(len(pointList) - 1)
                    else:
                        pointList = [geom.asPoint()]
                    i = 0
                    if len(self.pointBubberBandList) != 0:
                        QgisHelper.ClearRubberBandInCanvas(define._canvas, self.pointBubberBandList)
                        self.pointBubberBandList = []
                    for pt in pointList:
                        self.pointBubberBandList.append(QgsRubberBand(self.canvas,QGis.Polygon))
                    for pt in pointList:
                        self.pointBubberBandList[i].addPoint(QgsPoint(pt.x() - 200, pt.y() + 200))
                        self.pointBubberBandList[i].addPoint(QgsPoint(pt.x() - 200, pt.y() - 200))
                        self.pointBubberBandList[i].addPoint(QgsPoint(pt.x() + 200, pt.y() - 200))
                        self.pointBubberBandList[i].addPoint(QgsPoint(pt.x() + 200, pt.y() + 200))
                        self.pointBubberBandList[i].setBorderColor(Qt.red)
                        self.pointBubberBandList[i].setFillColor(QColor(255, 255, 255, 0))
                        if i != len(pointList) - 1:
                            self.pointBubberBandList[i].show()
                        i += 1
                    if self.selectedVertexID < len(self.pointBubberBandList):
                        self.pointBubberBandList[self.selectedVertexID].setBorderColor(Qt.blue)
    def canvasPressEvent(self, e):
        if self.geometryType == QGis.Point:
            return
        pointList = []

        snappingResults0 = self.mSnapper.snapToCurrentLayer(e.pos(), QgsSnapper.SnapToSegment)
        if ( snappingResults0[0] != 0 or len(snappingResults0[1]) < 1 ):
            return
        else:

            snappingResults = None
            for re in snappingResults0[1]:
                snappingResults = re
                if snappingResults.layer.isEditable():
                    break
                return
            featId = snappingResults.snappedAtGeometry
            self.selectedFeatureID = snappingResults.snappedAtGeometry

            layer = define._canvas.currentLayer()
            feat = QgsFeature()
            layer.getFeatures(QgsFeatureRequest().setFilterFid(featId)).nextFeature(feat)
            geom = feat.geometry()
            if geom.type() == QGis.Line:
                pointList = geom.asPolyline()
            elif geom.type() == QGis.Polygon:
                pointList = geom.asPolygon()[0]

                # pointList.pop(len(pointList) - 1)
            else:
                pointList = [geom.asPoint()]


            atVertex = snappingResults.snappedVertexNr
            self.vertexID = atVertex
            snapedPoint = snappingResults.snappedVertex


            if self.beforeFeatureID == None:
                self.beforeFeatureID = featId
            else:
                if self.beforeFeatureID != featId:
                    self.mouseClickCount = 0
                    self.beforeFeatureID = featId
                else:
                    self.mouseClickCount = 1

        self.mouseClickCount += 1
        if self.mouseClickCount == 1:


            i = 0
            if len(self.pointBubberBandList) != 0:
                QgisHelper.ClearRubberBandInCanvas(define._canvas, self.pointBubberBandList)
                self.pointBubberBandList = []
            for pt in pointList:
                self.pointBubberBandList.append(QgsRubberBand(self.canvas,QGis.Polygon))
            for pt in pointList:
                self.pointBubberBandList[i].addPoint(QgsPoint(pt.x() - 200, pt.y() + 200))
                self.pointBubberBandList[i].addPoint(QgsPoint(pt.x() - 200, pt.y() - 200))
                self.pointBubberBandList[i].addPoint(QgsPoint(pt.x() + 200, pt.y() - 200))
                self.pointBubberBandList[i].addPoint(QgsPoint(pt.x() + 200, pt.y() + 200))
                self.pointBubberBandList[i].setBorderColor(Qt.red)
                self.pointBubberBandList[i].setFillColor(QColor(255, 255, 255, 0))
                if i != len(pointList) - 1:
                    self.pointBubberBandList[i].show()
                i += 1



            # self.rubberBand.setToGeometry(self.selectedGeom, define._canvas.currentLayer())

        elif self.mouseClickCount == 2:
            snappingResults0 = self.mSnapper.snapToCurrentLayer(e.pos(), QgsSnapper.SnapToVertex)
            if ( snappingResults0[0] != 0 or len(snappingResults0[1]) < 1 ):
                snappingResultsLine = self.mSnapper.snapToCurrentLayer(e.pos(), QgsSnapper.SnapToSegment)
                if ( snappingResultsLine[0] != 0 or len(snappingResultsLine[1]) < 1 ):
                    return
                else:
                    snappingResultsL = None
                    for re in snappingResultsLine[1]:
                        snappingResultsL = re
                        if snappingResultsL.layer.isEditable():
                            break
                        return
                    afterVertexID = snappingResultsL.afterVertexNr
                    beforeVertexID = snappingResultsL.beforeVertexNr
                    self.selectedFeatureID = snappingResultsL.snappedAtGeometry

                    afterPoint = snappingResultsL.afterVertex
                    beforePoint = snappingResultsL.beforeVertex
                    self.vertexIdList.append(beforeVertexID)
                    self.vertexIdList.append(afterVertexID)
                    self.selectedPointList = pointList
                    self.startPoint = self.toMapCoordinates(e.pos())
                    
                    self.pointBubberBandList[afterVertexID].setBorderColor(Qt.blue)
                    self.pointBubberBandList[beforeVertexID].setBorderColor(Qt.blue)
                    define._canvas.refresh()
                    self.isDrawing = True
                    pass

                return
            else:

                snappingResults = None
                for re in snappingResults0[1]:
                    snappingResults = re
                    if snappingResults.layer.isEditable():
                        break
                    return
            self.selectedVertexID = snappingResults.snappedVertexNr
            self.pointBubberBandList[self.selectedVertexID].setBorderColor(Qt.blue)
            atVertex = snappingResults.snappedVertexNr
            define._canvas.refresh()

            if atVertex < 0:
                return
            if self.geometryType == QGis.Line:
                if len(pointList) - 1 == atVertex:
                    self.endPoint = snapedPoint
                    self.startPoint = pointList[len(pointList) - 2]
                    self.middlePoint = None
                    self.vertexPlace = "E"
                elif atVertex == 0:
                    self.startPoint= snapedPoint
                    self.endPoint = pointList[1]
                    self.middlePoint = None
                    self.vertexPlace = "S"
                else:
                    self.startPoint= pointList[atVertex - 1]
                    self.endPoint = pointList[atVertex + 1]
                    self.middlePoint = snapedPoint
                    self.vertexPlace = "M"
            elif self.geometryType == QGis.Polygon:
                if len(pointList) - 1 == atVertex:
                    self.endPoint = pointList[1]
                    self.startPoint = pointList[len(pointList) - 2]
                    self.middlePoint = snapedPoint
                    self.vertexPlace = "E"
                elif atVertex == 0:
                    self.startPoint= pointList[len(pointList) - 1]
                    self.endPoint = pointList[1]
                    self.middlePoint = snapedPoint
                    self.vertexPlace = "S"
                else:
                    self.startPoint= pointList[atVertex - 1]
                    self.endPoint = pointList[atVertex + 1]
                    self.middlePoint = snapedPoint
                    self.vertexPlace = "M"
            self.isDrawing = True
    def canvasDoubleClickEvent(self, e):
        pointList = []

        snappingResults0 = self.mSnapper.snapToCurrentLayer(e.pos(), QgsSnapper.SnapToSegment)
        if ( snappingResults0[0] != 0 or len(snappingResults0[1]) < 1 ):
            return
        else:

            snappingResults = None
            for re in snappingResults0[1]:
                snappingResults = re
                if snappingResults.layer.isEditable():
                    break
                return
            featId = snappingResults.snappedAtGeometry

            # layer = define._canvas.currentLayer()
            layerCoords = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)

            if layerCoords == None:
                layerCoords = self.toMapCoordinates(e.pos())
            layer = define._canvas.currentLayer()
            if layer.isEditable():
                layer.insertVertex(layerCoords.x(), layerCoords.y(), featId, snappingResults.afterVertexNr);
                define._canvas.refresh()
            feat = QgsFeature()
            layer.getFeatures(QgsFeatureRequest().setFilterFid(featId)).nextFeature(feat)
            geom = feat.geometry()
            pointList = []
            if geom.type() == QGis.Line:
                pointList = geom.asPolyline()
            elif geom.type() == QGis.Polygon:
                pointList = geom.asPolygon()[0]

                # pointList.pop(len(pointList) - 1)
            else:
                pointList = [geom.asPoint()]
            i = 0
            if len(self.pointBubberBandList) != 0:
                QgisHelper.ClearRubberBandInCanvas(define._canvas, self.pointBubberBandList)
                self.pointBubberBandList = []
            for pt in pointList:
                self.pointBubberBandList.append(QgsRubberBand(self.canvas,QGis.Polygon))
            for pt in pointList:
                self.pointBubberBandList[i].addPoint(QgsPoint(pt.x() - 200, pt.y() + 200))
                self.pointBubberBandList[i].addPoint(QgsPoint(pt.x() - 200, pt.y() - 200))
                self.pointBubberBandList[i].addPoint(QgsPoint(pt.x() + 200, pt.y() - 200))
                self.pointBubberBandList[i].addPoint(QgsPoint(pt.x() + 200, pt.y() + 200))
                self.pointBubberBandList[i].setBorderColor(Qt.red)
                self.pointBubberBandList[i].setFillColor(QColor(255, 255, 255, 0))
                if i != len(pointList) - 1:
                    self.pointBubberBandList[i].show()
                i += 1


    def canvasReleaseEvent(self, e):
        if not self.isDrawing:
            return
        pt = self.toMapCoordinates(e.pos())
        ptBefore = None
        ptAfter = None
        if self.mouseClickCount == 2:
            if self.pointBubberBandList != None and len(self.pointBubberBandList) > 0:
                for pointRB in self.pointBubberBandList:
                    pointRB.setBorderColor(Qt.red)
            if len(self.vertexIdList) > 0:
                self.endPoint = self.toMapCoordinates(e.pos())
                ptBefore = MathHelper.distanceBearingPoint(self.selectedPointList[self.vertexIdList[0]], MathHelper.getBearing(self.startPoint, self.endPoint), MathHelper.calcDistance(self.startPoint, self.endPoint))
                ptAfter = MathHelper.distanceBearingPoint(self.selectedPointList[self.vertexIdList[1]], MathHelper.getBearing(self.startPoint, self.endPoint), MathHelper.calcDistance(self.startPoint, self.endPoint))
                
                self.pointBubberBandList[self.vertexIdList[0]].reset(QGis.Polygon)
                self.pointBubberBandList[self.vertexIdList[0]].setBorderColor(Qt.blue)
                self.pointBubberBandList[self.vertexIdList[0]].addPoint(QgsPoint(ptBefore.x() - 200, ptBefore.y() + 200))
                self.pointBubberBandList[self.vertexIdList[0]].addPoint(QgsPoint(ptBefore.x() - 200, ptBefore.y() - 200))
                self.pointBubberBandList[self.vertexIdList[0]].addPoint(QgsPoint(ptBefore.x() + 200, ptBefore.y() - 200))
                self.pointBubberBandList[self.vertexIdList[0]].addPoint(QgsPoint(ptBefore.x() + 200, ptBefore.y() + 200))
                self.pointBubberBandList[self.vertexIdList[0]].setBorderColor(Qt.blue)
                self.pointBubberBandList[self.vertexIdList[0]].setFillColor(QColor(255, 255, 255, 0))
                self.pointBubberBandList[self.vertexIdList[0]].show()
                
                self.pointBubberBandList[self.vertexIdList[1]].reset(QGis.Polygon)
                self.pointBubberBandList[self.vertexIdList[1]].setBorderColor(Qt.blue)
                self.pointBubberBandList[self.vertexIdList[1]].addPoint(QgsPoint(ptAfter.x() - 200, ptAfter.y() + 200))
                self.pointBubberBandList[self.vertexIdList[1]].addPoint(QgsPoint(ptAfter.x() - 200, ptAfter.y() - 200))
                self.pointBubberBandList[self.vertexIdList[1]].addPoint(QgsPoint(ptAfter.x() + 200, ptAfter.y() - 200))
                self.pointBubberBandList[self.vertexIdList[1]].addPoint(QgsPoint(ptAfter.x() + 200, ptAfter.y() + 200))
                self.pointBubberBandList[self.vertexIdList[1]].setBorderColor(Qt.blue)
                self.pointBubberBandList[self.vertexIdList[1]].setFillColor(QColor(255, 255, 255, 0))
                self.pointBubberBandList[self.vertexIdList[1]].show()
                self.selectedVertexID = self.vertexIdList[0]
            else:
                self.pointBubberBandList[self.selectedVertexID].reset(QGis.Polygon)
                self.pointBubberBandList[self.selectedVertexID].setBorderColor(Qt.blue)
                self.pointBubberBandList[self.selectedVertexID].addPoint(QgsPoint(pt.x() - 200, pt.y() + 200))
                self.pointBubberBandList[self.selectedVertexID].addPoint(QgsPoint(pt.x() - 200, pt.y() - 200))
                self.pointBubberBandList[self.selectedVertexID].addPoint(QgsPoint(pt.x() + 200, pt.y() - 200))
                self.pointBubberBandList[self.selectedVertexID].addPoint(QgsPoint(pt.x() + 200, pt.y() + 200))
                self.pointBubberBandList[self.selectedVertexID].setBorderColor(Qt.blue)
                self.pointBubberBandList[self.selectedVertexID].setFillColor(QColor(255, 255, 255, 0))
                self.pointBubberBandList[self.selectedVertexID].show()
            define._canvas.refresh()
            self.mouseClickCount = 1
        self.rubberBandPt.reset(QGis.Point)
        ly = define._canvas.currentLayer()
        if ly.isEditable():
            if len(self.vertexIdList) > 0:
                ly.moveVertex(ptBefore.x(), ptBefore.y(), self.beforeFeatureID, self.vertexIdList[0])
                ly.moveVertex(ptAfter.x(), ptAfter.y(), self.beforeFeatureID, self.vertexIdList[1])
            else:
                ly.moveVertex(pt.x(), pt.y(), self.beforeFeatureID, self.selectedVertexID)
        define._canvas.refresh()
        self.reset()


    def canvasMoveEvent(self, e):
        self.rubberBandPt.reset(QGis.Point)
        if self.isDrawing:
            self.rubberBandLine.reset(QGis.Line)
            self.rubberBandLine.setColor(Qt.blue)
            self.rubberBandLine.setWidth(2)
            if len(self.vertexIdList) > 0:
                beforeID = self.vertexIdList[0]
                afterID = self.vertexIdList[1]

                self.endPoint = self.toMapCoordinates(e.pos())
                ptBefore = MathHelper.distanceBearingPoint(self.selectedPointList[self.vertexIdList[0]], MathHelper.getBearing(self.startPoint, self.endPoint), MathHelper.calcDistance(self.startPoint, self.endPoint))
                ptAfter = MathHelper.distanceBearingPoint(self.selectedPointList[self.vertexIdList[1]], MathHelper.getBearing(self.startPoint, self.endPoint), MathHelper.calcDistance(self.startPoint, self.endPoint))

                if self.geometryType == QGis.Line:
                    if beforeID == 0:
                        self.rubberBandLine.addPoint(ptBefore)
                        self.rubberBandLine.addPoint(ptAfter)
                        self.rubberBandLine.addPoint(self.selectedPointList[afterID + 1])
                    elif afterID == len(self.selectedPointList) - 1:
                        self.rubberBandLine.addPoint(self.selectedPointList[beforeID - 1])
                        self.rubberBandLine.addPoint(ptBefore)
                        self.rubberBandLine.addPoint(ptAfter)
                    else:
                        self.rubberBandLine.addPoint(self.selectedPointList[beforeID - 1])
                        self.rubberBandLine.addPoint(ptBefore)
                        self.rubberBandLine.addPoint(ptAfter)
                        self.rubberBandLine.addPoint(self.selectedPointList[afterID + 1])
                elif self.geometryType == QGis.Polygon:
                    if beforeID == 0:
                        self.rubberBandLine.addPoint(self.selectedPointList[len(self.selectedPointList) - 2])
                        self.rubberBandLine.addPoint(ptBefore)
                        self.rubberBandLine.addPoint(ptAfter)
                        self.rubberBandLine.addPoint(self.selectedPointList[afterID + 1])
                    elif afterID == len(self.selectedPointList) - 1:
                        self.rubberBandLine.addPoint(self.selectedPointList[beforeID - 1])
                        self.rubberBandLine.addPoint(ptBefore)
                        self.rubberBandLine.addPoint(ptAfter)
                        self.rubberBandLine.addPoint(self.selectedPointList[1])
                    else:
                        self.rubberBandLine.addPoint(self.selectedPointList[beforeID - 1])
                        self.rubberBandLine.addPoint(ptBefore)
                        self.rubberBandLine.addPoint(ptAfter)
                        self.rubberBandLine.addPoint(self.selectedPointList[afterID + 1])

            else:
                if self.geometryType == QGis.Line:
                    if self.vertexPlace == "S":
                        self.startPoint = self.toMapCoordinates(e.pos())
                    elif self.vertexPlace == "E":
                        self.endPoint = self.toMapCoordinates(e.pos())
                    else:
                        self.middlePoint = self.toMapCoordinates(e.pos())

                    self.rubberBandLine.addPoint(self.startPoint)
                    if self.middlePoint != None and isinstance(self.middlePoint, QgsPoint):
                        self.rubberBandLine.addPoint(self.middlePoint)
                    self.rubberBandLine.addPoint(self.endPoint)
                elif self.geometryType == QGis.Polygon:
                    self.middlePoint = self.toMapCoordinates(e.pos())
                    self.rubberBandLine.addPoint(self.startPoint)
                    self.rubberBandLine.addPoint(self.middlePoint)
                    self.rubberBandLine.addPoint(self.endPoint)


    def deactivate(self):
        self.rubberBandPt.reset(QGis.Point)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))