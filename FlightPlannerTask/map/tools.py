'''
Created on Mar 24, 2015

@author: Administrator
'''
from PyQt4.QtGui import QMessageBox, QApplication, QColor
from PyQt4.QtCore import Qt, QPoint, QRect, SIGNAL

from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnapper
from qgis.core import QGis, QgsRectangle, QgsGeometry, QgsCsException, QgsPoint,\
        QgsFeatureRequest, QgsCoordinateTransform, QgsFeature

from FlightPlanner.helpers import MathHelper, Unit
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint

from FlightPlanner.types import Point3D, TurnDirection
import math,define

class SelectedFeatureByRectTasDraw(QgsMapTool):

    def __init__(self, canvas, distance):
        self.mCanvas = canvas
        QgsMapTool.__init__(self, canvas)
        self.mCursor = Qt.ArrowCursor
        self.mRubberBand = None
        self.mDragging = False
        self.mSelectRect = QRect()
        self.rubberBandLine = None
        self.distance = distance
        self.mSnapper = QgsMapCanvasSnapper(canvas)
#     QgsRubberBand* mRubberBand;
#     def reset(self):
#         self.startPoint = None
#         self.endPoint = None
#         self.isDrawing = False
#         SelectByRect.RubberRect.reset(QGis.Polygon)
#         self.layer = self.canvas.currentLayer()

    def canvasPressEvent(self, e):
        self.mSelectRect.setRect( 0, 0, 0, 0 )
        self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
        self.startPoint, self.pointID, self.layer= self.snapPoint(e.pos())
#         self.reset()
#         self.startPoint = self.toMapCoordinates(e.pos())
#         self.isDrawing = True

    def canvasMoveEvent(self, e):
        if ( e.buttons() != Qt.LeftButton ):
            return
        if ( not self.mDragging ):
            self.mDragging = True
            self.mSelectRect.setTopLeft( e.pos() )
        self.mSelectRect.setBottomRight( e.pos() )
        QgsMapToolSelectUtils.setRubberBand( self.mCanvas, self.mSelectRect,self.mRubberBand )
#         if not self.isDrawing:
#             return
#         SelectByRect.RubberRect.reset(QGis.Polygon)
#         self.endPoint = self.toMapCoordinates(e.pos())
#         self.rect = QgsRectangle(self.startPoint, self.endPoint)
#         SelectByRect.RubberRect.addGeometry(QgsGeometry.fromRect(self.rect), None)
#         SelectByRect.RubberRect.show()

    def canvasReleaseEvent(self, e):
        self.endPoint, self.pointID, self.layer= self.snapPoint(e.pos())
        if len(define._newGeometryList) > 0:
            geom = define._newGeometryList[0]
            if geom.intersects(self.mRubberBand.asGeometry()):
                pointArray = geom.asPolyline()
                # pointArray1 = QgisHelper.offsetCurve(pointArray, 1200)
                if self.rubberBandLine != None:
                    self.rubberBandLine.reset(QGis.Line)
                    del self.rubberBandLine
                    self.rubberBandLine = None
                self.rubberBandLine = QgsRubberBand(self.mCanvas,QGis.Line)
                self.rubberBandLine.setColor(Qt.blue)
                bearing = 0.0
                if self.startPoint.y() >= self.endPoint.y() and (math.fabs(self.startPoint.x() - self.endPoint.x()) < math.fabs(self.startPoint.y() - self.endPoint.y())):
                    bearing = Unit.ConvertDegToRad(180)
                elif self.startPoint.x() >= self.endPoint.x() and (math.fabs(self.startPoint.x() - self.endPoint.x()) > math.fabs(self.startPoint.y() - self.endPoint.y())):
                    bearing = Unit.ConvertDegToRad(270)
                elif self.startPoint.x() < self.endPoint.x() and (math.fabs(self.startPoint.x() - self.endPoint.x()) > math.fabs(self.startPoint.y() - self.endPoint.y())):
                    bearing = Unit.ConvertDegToRad(90)
                else:
                    bearing = 0.0

                for point in pointArray:

                    pt = MathHelper.distanceBearingPoint(Point3D(point.x(), point.y()), bearing, self.distance) # MathHelper.getBearing(self.startPoint, self.endPoint), self.distance)
                    self.rubberBandLine.addPoint(pt)
                gg= self.rubberBandLine.asGeometry()
                g = gg.asPolyline()
                # self.rubberBandLine.show()
                if ( self.mRubberBand != None):
                    self.mRubberBand.reset( QGis.Polygon )
                    del self.mRubberBand
                    self.mRubberBand = None
                    self.mDragging = False
                    self.emit(SIGNAL("resultSelectedFeatureByRectTasDraw"), gg, self.distance,bearing)# MathHelper.getBearing(self.startPoint, self.endPoint))
                return
        vlayer = QgsMapToolSelectUtils.getCurrentVectorLayer( self.mCanvas )
        if ( vlayer == None ):
            if ( self.mRubberBand != None):
                self.mRubberBand.reset( QGis.Polygon )
                del self.mRubberBand
                self.mRubberBand = None
                self.mDragging = False
            return


        if (not self.mDragging ):
            QgsMapToolSelectUtils.expandSelectRectangle(self. mSelectRect, vlayer, e.pos() )
        else:
            if ( self.mSelectRect.width() == 1 ):
                self.mSelectRect.setLeft( self.mSelectRect.left() + 1 )
            if ( self.mSelectRect.height() == 1 ):
                self.mSelectRect.setBottom( self.mSelectRect.bottom() + 1 )

        if ( self.mRubberBand != None ):
            QgsMapToolSelectUtils.setRubberBand( self.mCanvas, self.mSelectRect, self.mRubberBand )
            selectGeom = self.mRubberBand.asGeometry()


            # QgsMapToolSelectUtils.setSelectFeatures( self.mCanvas, selectGeom, e )
            selectedFeatures = QgsMapToolSelectUtils.setSelectFeaturesOrRubberband_Tas_1( self.mCanvas, selectGeom, e )
            if len(selectedFeatures) > 0:
                geom = selectedFeatures[0].geometry()
                if geom.intersects(self.mRubberBand.asGeometry()):
                    pointArray = geom.asPolyline()
                    # pointArray1 = QgisHelper.offsetCurve(pointArray, 1200)
                    if self.rubberBandLine != None:
                        self.rubberBandLine.reset(QGis.Line)
                        del self.rubberBandLine
                        self.rubberBandLine = None
                    self.rubberBandLine = QgsRubberBand(self.mCanvas,QGis.Line)
                    self.rubberBandLine.setColor(Qt.blue)
                    bearing = 0.0
                    gg = None
                    if self.startPoint.y() >= self.endPoint.y() and (math.fabs(self.startPoint.x() - self.endPoint.x()) < math.fabs(self.startPoint.y() - self.endPoint.y())):
                        bearing = Unit.ConvertDegToRad(180)
                        gg= self.newCreateLine(geom, self.distance, 180)
                    elif self.startPoint.x() >= self.endPoint.x() and (math.fabs(self.startPoint.x() - self.endPoint.x()) > math.fabs(self.startPoint.y() - self.endPoint.y())):
                        bearing = Unit.ConvertDegToRad(270)
                        gg= self.newCreateLine(geom, self.distance, 270)
                    elif self.startPoint.x() < self.endPoint.x() and (math.fabs(self.startPoint.x() - self.endPoint.x()) > math.fabs(self.startPoint.y() - self.endPoint.y())):
                        bearing = Unit.ConvertDegToRad(90)
                        gg= self.newCreateLine(geom, self.distance, 90)
                    else:
                        bearing = 0.0
                        gg= self.newCreateLine(geom, self.distance, 0)
                    for point in pointArray:
                        pt = MathHelper.distanceBearingPoint(Point3D(point.x(), point.y()), bearing, self.distance) #MathHelper.getBearing(self.startPoint, self.endPoint), self.distance)

                        self.rubberBandLine.addPoint(pt)
                    # gg= self.newCreateLine(geom, -self.distance, 0)

                    self.emit(SIGNAL("resultSelectedFeatureByRectTasDraw"), gg, self.distance, bearing) #MathHelper.getBearing(self.startPoint, self.endPoint))
                    self.rubberBandLine.reset(QGis.Line)
            del selectGeom

            self.mRubberBand.reset( QGis.Polygon )
            del self.mRubberBand
            self.mRubberBand = None
        self.mDragging = False


#         self.canvasMoveEvent(e)
#         if self.layer != None:
#             self.layer.removeSelection()
#             if self.layer.crs().mapUnits() != self.canvas.mapUnits():
#                 if self.layer.crs().mapUnits == QGis.Meters:
#                     lstPoint = QgisHelper.Degree2MeterList([self.startPoint, self.endPoint])
#                 else:
#                     lstPoint = QgisHelper.Meter2DegreeList([self.startPoint, self.endPoint])
#                 rect = QgsRectangle(lstPoint[0], lstPoint[1])
#                 self.layer.select(rect, True)
#             else:
#                 self.layer.select(self.rect, False)
#         else:
#             QMessageBox.warning(None, "Information", "Please select layer!")
#         self.reset()

    def snapPoint(self, p, bNone = False):
        if define._snapping == False:
            return (define._canvas.getCoordinateTransform().toMapCoordinates( p ), None, None)
        snappingResults = self.mSnapper.snapToBackgroundLayers( p )
        if ( snappingResults[0] != 0 or len(snappingResults[1]) < 1 ):

            if bNone:
                return (None, None, None)
            else:
                return (define._canvas.getCoordinateTransform().toMapCoordinates( p ), None, None)
        else:
            return (snappingResults[1][0].snappedVertex, snappingResults[1][0].snappedAtGeometry, snappingResults[1][0].layer)


    def newCreateLine(self, geom, dist, angle):
        if define._units != QGis.Meters:
            dist = define._qgsDistanceArea.convertMeasurement(dist, QGis.Meters, QGis.Degrees, False)[0]
        g = geom.offsetCurve(dist, 0, 2, 2)
        pointArrayOld = geom.asPolyline()
        pointArrayNew = g.asPolyline()
        if MathHelper.calcDistance(pointArrayNew[0], pointArrayOld[0]) > MathHelper.calcDistance(pointArrayNew[0], pointArrayOld[len(pointArrayOld) - 1]):
            array = []
            i  = len(pointArrayNew) - 1
            while i >= 0:
                array.append(pointArrayNew[i])
                i -= 1
            pointArrayNew = array
        if angle == 0:
            if pointArrayNew[0].y() < pointArrayOld[0].y():
                g = geom.offsetCurve(-dist, 0, 2, 2)
                pointArrayNew = g.asPolyline()
        elif angle == 90:
            if pointArrayNew[0].x() < pointArrayOld[0].x():
                g = geom.offsetCurve(-dist, 0, 2, 2)
                pointArrayNew = g.asPolyline()
        elif angle == 180:
            if pointArrayNew[0].y() > pointArrayOld[0].y():
                g = geom.offsetCurve(-dist, 0, 2, 2)
                pointArrayNew = g.asPolyline()
        elif angle == 270:
            if pointArrayNew[0].x() > pointArrayOld[0].x():
                g = geom.offsetCurve(-dist, 0, 2, 2)
                pointArrayNew = g.asPolyline()
        if MathHelper.calcDistance(pointArrayNew[0], pointArrayOld[0]) > MathHelper.calcDistance(pointArrayNew[0], pointArrayOld[len(pointArrayOld) - 1]):
            array = []
            i  = len(pointArrayNew) - 1
            while i >= 0:
                array.append(pointArrayNew[i])
                i -= 1
            pointArrayNew = array
        i = 0


        while i < len(pointArrayNew)-1:
            if i == 0:
                i += 1
                continue
            line = None
            if define._units == QGis.Meters:
                if angle == 0:
                    line = QgsGeometry.fromPolyline([pointArrayOld[0], QgsPoint(pointArrayOld[0].x(), 100000000)])
                elif angle == 90:
                    line = QgsGeometry.fromPolyline([pointArrayOld[0], QgsPoint(100000000, pointArrayOld[0].y())])
                elif angle == 180:
                    line = QgsGeometry.fromPolyline([pointArrayOld[0], QgsPoint(pointArrayOld[0].x(), 0)])
                elif angle == 270:
                    line = QgsGeometry.fromPolyline([pointArrayOld[0], QgsPoint(0, pointArrayOld[0].y())])
            else:
                if angle == 0:
                    line = QgsGeometry.fromPolyline([pointArrayOld[0], QgsPoint(pointArrayOld[0].x(), pointArrayOld[0].y() + 0.1)])
                elif angle == 90:
                    line = QgsGeometry.fromPolyline([pointArrayOld[0], QgsPoint(pointArrayOld[0].x()+ 0.1, pointArrayOld[0].y())])
                elif angle == 180:
                    line = QgsGeometry.fromPolyline([pointArrayOld[0], QgsPoint(pointArrayOld[0].x(), pointArrayOld[0].y() - 0.1)])
                elif angle == 270:
                    line = QgsGeometry.fromPolyline([pointArrayOld[0], QgsPoint(pointArrayOld[0].x()- 0.1, pointArrayOld[0].y())])
            lineNew = QgsGeometry.fromPolyline([MathHelper.distanceBearingPoint(Point3D(pointArrayNew[i].x(), pointArrayNew[i].y()),MathHelper.getBearing(pointArrayNew[i], pointArrayNew[i-1]), 100000 ), pointArrayNew[i]])

            if line.intersects(lineNew):
                pointGeom = line.intersection(lineNew)
                intersectPoint = pointGeom.asPoint()
                pointArrayNew.pop(i-1)
                pointArrayNew.insert(i-1, intersectPoint)
                break
            else:
                pointArrayNew.pop(i-1)
                continue
            i += 1
        i = len(pointArrayNew)-1
        while i > 1:
            line = None
            if define._units == QGis.Meters:
                if angle == 0:
                    line = QgsGeometry.fromPolyline([pointArrayOld[len(pointArrayOld) - 1], QgsPoint(pointArrayOld[len(pointArrayOld) - 1].x(), 100000000)])
                elif angle == 90:
                    line = QgsGeometry.fromPolyline([pointArrayOld[len(pointArrayOld) - 1], QgsPoint(100000000, pointArrayOld[len(pointArrayOld) - 1].y())])
                elif angle == 180:
                    line = QgsGeometry.fromPolyline([pointArrayOld[len(pointArrayOld) - 1], QgsPoint(pointArrayOld[len(pointArrayOld) - 1].x(), 0)])
                elif angle == 270:
                    line = QgsGeometry.fromPolyline([pointArrayOld[len(pointArrayOld) - 1], QgsPoint(0, pointArrayOld[len(pointArrayOld) - 1].y())])
            else:
                if angle == 0:
                    line = QgsGeometry.fromPolyline([pointArrayOld[len(pointArrayOld) - 1], QgsPoint(pointArrayOld[len(pointArrayOld) - 1].x(), pointArrayOld[len(pointArrayOld) - 1].y() + 0.1)])
                elif angle == 90:
                    line = QgsGeometry.fromPolyline([pointArrayOld[len(pointArrayOld) - 1], QgsPoint(pointArrayOld[len(pointArrayOld) - 1].x() + 0.1, pointArrayOld[len(pointArrayOld) - 1].y())])
                elif angle == 180:
                    line = QgsGeometry.fromPolyline([pointArrayOld[len(pointArrayOld) - 1], QgsPoint(pointArrayOld[len(pointArrayOld) - 1].x(), pointArrayOld[len(pointArrayOld) - 1].y() - 0.1)])
                elif angle == 270:
                    line = QgsGeometry.fromPolyline([pointArrayOld[len(pointArrayOld) - 1], QgsPoint(pointArrayOld[len(pointArrayOld) - 1].x() - 0.1, pointArrayOld[len(pointArrayOld) - 1].y())])
            # line = QgsGeometry.fromPolyline([pointArrayOld[len(pointArrayOld) - 1], QgsPoint(pointArrayOld[len(pointArrayOld) - 1].x(), 100000000)])
            lineNew = QgsGeometry.fromPolyline([MathHelper.distanceBearingPoint(Point3D(pointArrayNew[i].x(), pointArrayNew[i].y()),MathHelper.getBearing(pointArrayNew[i-1], pointArrayNew[i]), 100000 ), pointArrayNew[i - 1]])
            if line.intersects(lineNew):
                pointGeom = line.intersection(lineNew)
                intersectPoint = pointGeom.asPoint()
                pointArrayNew.pop(i)
                pointArrayNew.insert(i, intersectPoint)
                break
            else:
                pointArrayNew.pop(i)
                i -= 1
                continue
            i -= 1
        return QgsGeometry.fromPolyline(pointArrayNew)





class SelectByRect(QgsMapTool):
    
    def __init__(self, canvas):
        self.mCanvas = canvas        
        QgsMapTool.__init__(self, canvas)
        self.mCursor = Qt.ArrowCursor
        self.mRubberBand = None
        self.mDragging = False
        self.mSelectRect = QRect()

#     QgsRubberBand* mRubberBand;
#     def reset(self):
#         self.startPoint = None
#         self.endPoint = None
#         self.isDrawing = False
#         SelectByRect.RubberRect.reset(QGis.Polygon)
#         self.layer = self.canvas.currentLayer()
    
    def canvasPressEvent(self, e):
        self.mSelectRect.setRect( 0, 0, 0, 0 )
        self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
#         self.reset()
#         self.startPoint = self.toMapCoordinates(e.pos())
#         self.isDrawing = True
        
    def canvasMoveEvent(self, e):
        if ( e.buttons() != Qt.LeftButton ):
            return
        if ( not self.mDragging ):
            self.mDragging = True
            self.mSelectRect.setTopLeft( e.pos() )
        self.mSelectRect.setBottomRight( e.pos() )
        QgsMapToolSelectUtils.setRubberBand( self.mCanvas, self.mSelectRect,self.mRubberBand )
#         if not self.isDrawing:
#             return
#         SelectByRect.RubberRect.reset(QGis.Polygon)
#         self.endPoint = self.toMapCoordinates(e.pos())
#         self.rect = QgsRectangle(self.startPoint, self.endPoint)
#         SelectByRect.RubberRect.addGeometry(QgsGeometry.fromRect(self.rect), None)
#         SelectByRect.RubberRect.show()

    def canvasReleaseEvent(self, e):
        selectedFeatures = None
        vlayer = QgsMapToolSelectUtils.getCurrentVectorLayer( self.mCanvas )
        if ( vlayer == None ):
            if ( self.mRubberBand != None):
                self.mRubberBand.reset( QGis.Polygon )
                del self.mRubberBand
                self.mRubberBand = None
                self.mDragging = False
            return


        if (not self.mDragging ):
            QgsMapToolSelectUtils.expandSelectRectangle(self. mSelectRect, vlayer, e.pos() )
        else:
            if ( self.mSelectRect.width() == 1 ):
                self.mSelectRect.setLeft( self.mSelectRect.left() + 1 )
            if ( self.mSelectRect.height() == 1 ):
                self.mSelectRect.setBottom( self.mSelectRect.bottom() + 1 )
        
        if ( self.mRubberBand != None ):
            QgsMapToolSelectUtils.setRubberBand( self.mCanvas, self.mSelectRect, self.mRubberBand )
            selectGeom = self.mRubberBand.asGeometry()
            # QgsMapToolSelectUtils.setSelectFeatures( self.mCanvas, selectGeom, e )
            selectedFeatures = QgsMapToolSelectUtils.setSelectFeatures1( self.mCanvas, selectGeom, e )
            del selectGeom
            
            self.mRubberBand.reset( QGis.Polygon )
            del self.mRubberBand
            self.mRubberBand = None
        self.mDragging = False
        self.emit(SIGNAL("getSelectedFeatures"), selectedFeatures)
        
        
#         self.canvasMoveEvent(e)
#         if self.layer != None:
#             self.layer.removeSelection()
#             if self.layer.crs().mapUnits() != self.canvas.mapUnits():                
#                 if self.layer.crs().mapUnits == QGis.Meters:
#                     lstPoint = QgisHelper.Degree2MeterList([self.startPoint, self.endPoint])
#                 else:
#                     lstPoint = QgisHelper.Meter2DegreeList([self.startPoint, self.endPoint])
#                 rect = QgsRectangle(lstPoint[0], lstPoint[1])
#                 self.layer.select(rect, True)
#             else:
#                 self.layer.select(self.rect, False)
#         else:
#             QMessageBox.warning(None, "Information", "Please select layer!")
#         self.reset()
        
class QgsMapToolSelectUtils:
    
    @staticmethod
    def getCurrentVectorLayer( canvas ):
        vlayer = canvas.currentLayer()
        if vlayer != None:
            return vlayer
        else:
            QMessageBox.warning(None, "Information", "Please select layer!")
            return None
    
    @staticmethod
    def setRubberBand( canvas, selectRect, rubberBand ):
        transform = canvas.getCoordinateTransform()
        ll = transform.toMapCoordinates( selectRect.left(), selectRect.bottom() )
        ur = transform.toMapCoordinates( selectRect.right(), selectRect.top() )
        
        if ( rubberBand != None ):
            rubberBand.reset( QGis.Polygon )
            rubberBand.addPoint( ll, False )
            rubberBand.addPoint( QgsPoint( ur.x(), ll.y() ), False )
            rubberBand.addPoint( ur, False )
            rubberBand.addPoint( QgsPoint( ll.x(), ur.y() ), True )
    
    @staticmethod
    def expandSelectRectangle( selectRect, vlayer, point ):
        boxSize = 0
        if ( vlayer.geometryType() != QGis.Polygon ):
            #//if point or line use an artificial bounding box of 10x10 pixels
            #//to aid the user to click on a feature accurately
            boxSize = 5
        else:
            #//otherwise just use the click point for polys
            boxSize = 1

        selectRect.setLeft( point.x() - boxSize )
        selectRect.setRight( point.x() + boxSize )
        selectRect.setTop( point.y() - boxSize )
        selectRect.setBottom( point.y() + boxSize )
    
    @staticmethod
    def setSelectFeatures( canvas, selectGeometry, doContains = True, 
                           doDifference = False, singleSelect = False):
        if ( selectGeometry.type() != QGis.Polygon ):
            return
        vlayer = QgsMapToolSelectUtils.getCurrentVectorLayer( canvas )
        if ( vlayer == None ):
            return
        
        #// toLayerCoordinates will throw an exception for any 'invalid' points in
        #// the rubber band.
        #// For example, if you project a world map onto a globe using EPSG 2163
        #// and then click somewhere off the globe, an exception will be thrown.
        selectGeomTrans = QgsGeometry( selectGeometry )
        
        if ( canvas.mapSettings().hasCrsTransformEnabled() ):
            try:
                
                ct = QgsCoordinateTransform( canvas.mapSettings().destinationCrs(), vlayer.crs() )
#                 print selectGeomTrans.boundingBox().xMaximum () 
#                 polygonList = []
#                 for polygon in selectGeomTrans1.asPolygon():
#                     pointList = []
#                     for point in polygon:
#                         transPoint = QgisHelper.CrsTransformPoint(point.x(), point.y(), define._mapCrs, vlayer.crs())
#                         pointList.append(transPoint)
#                     polygonList.extend(pointList)
#                 selectGeomTrans = QgsGeometry.fromPolygon (pointList)
                selectGeomTrans.transform( ct )
                
                
            except QgsCsException as cse:
                raise UserWarning, "Coordinate Transform Error in QgsMapToolSelectUtils\n" + cse.message
        
        QApplication.setOverrideCursor( Qt.WaitCursor )
        
        fit = vlayer.getFeatures( QgsFeatureRequest().setFilterRect( selectGeomTrans.boundingBox() ).setFlags( QgsFeatureRequest.ExactIntersect ).setSubsetOfAttributes( [] ) )
        
        newSelectedFeatures = []
        newSelectedFeatureList = []
        f = QgsFeature()
        closestFeatureId = 0
        foundSingleFeature = False
        closestFeatureDist = 9.0E+10
        for f in fit:
            g = f.geometry()
            if ( doContains ):
                if ( not selectGeomTrans.contains( g ) ):
                    continue
            else:
                if ( not selectGeomTrans.intersects( g ) ):
                    continue
            if ( singleSelect ):
                foundSingleFeature = True
                distance = g.distance( selectGeomTrans )
                if ( distance <= closestFeatureDist ):
                    closestFeatureDist = distance
                    closestFeatureId = f.id()
            else:
                newSelectedFeatures.append( f.id() )
                
                newSelectedFeatureList.append(f)

        if ( singleSelect and foundSingleFeature ):
            newSelectedFeatures.append( closestFeatureId )
            featIter = vlayer.getFeatures (QgsFeatureRequest(closestFeatureId))
            for feat in featIter:                
                newSelectedFeatureList.append(feat)
        
        if ( doDifference ):
            layerSelectedFeatures = vlayer.selectedFeaturesIds()
            deselectedFeatures = []
            selectedFeatures = []
            for i in newSelectedFeatures.reverse():
                if i in layerSelectedFeatures:
                    deselectedFeatures.append( i )
                else:
                    selectedFeatures.append( i )
        
            vlayer.modifySelection( selectedFeatures, deselectedFeatures )
        else:
            vlayer.setSelectedFeatures( newSelectedFeatures )
        
        QApplication.restoreOverrideCursor()
        return newSelectedFeatureList

    @staticmethod
    def setSelectFeaturesOrRubberband_Tas( canvas, selectGeometry, doContains = True,
                           doDifference = False, singleSelect = False):
        if ( selectGeometry.type() != QGis.Polygon ):
            return
        vlayer = QgsMapToolSelectUtils.getCurrentVectorLayer( canvas )
        if ( vlayer == None ):
            return

        #// toLayerCoordinates will throw an exception for any 'invalid' points in
        #// the rubber band.
        #// For example, if you project a world map onto a globe using EPSG 2163
        #// and then click somewhere off the globe, an exception will be thrown.
        selectGeomTrans = QgsGeometry( selectGeometry )

        if ( canvas.mapSettings().hasCrsTransformEnabled() ):
            try:

                ct = QgsCoordinateTransform( canvas.mapSettings().destinationCrs(), vlayer.crs() )
#                 print selectGeomTrans.boundingBox().xMaximum ()
#                 polygonList = []
#                 for polygon in selectGeomTrans1.asPolygon():
#                     pointList = []
#                     for point in polygon:
#                         transPoint = QgisHelper.CrsTransformPoint(point.x(), point.y(), define._mapCrs, vlayer.crs())
#                         pointList.append(transPoint)
#                     polygonList.extend(pointList)
#                 selectGeomTrans = QgsGeometry.fromPolygon (pointList)
                selectGeomTrans.transform( ct )


            except QgsCsException as cse:
                raise UserWarning, "Coordinate Transform Error in QgsMapToolSelectUtils\n" + cse.message

        QApplication.setOverrideCursor( Qt.WaitCursor )

        fit = vlayer.getFeatures( QgsFeatureRequest().setFilterRect( selectGeomTrans.boundingBox() ).setFlags( QgsFeatureRequest.ExactIntersect ).setSubsetOfAttributes( [] ) )

        newSelectedFeatures = []
        newSelectedFeatureList = []
        f = QgsFeature()
        closestFeatureId = 0
        foundSingleFeature = False
        closestFeatureDist = 9.0E+10
        for f in fit:
            g = f.geometry()
            if ( doContains ):
                if ( not selectGeomTrans.contains( g ) ):
                    continue
            else:
                if ( not selectGeomTrans.intersects( g ) ):
                    continue
            if ( singleSelect ):
                foundSingleFeature = True
                distance = g.distance( selectGeomTrans )
                if ( distance <= closestFeatureDist ):
                    closestFeatureDist = distance
                    closestFeatureId = f.id()
            else:
                newSelectedFeatures.append( f.id() )

                newSelectedFeatureList.append(f)

        if ( singleSelect and foundSingleFeature ):
            newSelectedFeatures.append( closestFeatureId )
            featIter = vlayer.getFeatures (QgsFeatureRequest(closestFeatureId))
            for feat in featIter:
                newSelectedFeatureList.append(feat)

        if ( doDifference ):
            layerSelectedFeatures = vlayer.selectedFeaturesIds()
            deselectedFeatures = []
            selectedFeatures = []
            for i in newSelectedFeatures.reverse():
                if i in layerSelectedFeatures:
                    deselectedFeatures.append( i )
                else:
                    selectedFeatures.append( i )

            vlayer.modifySelection( selectedFeatures, deselectedFeatures )
        else:
            vlayer.setSelectedFeatures( newSelectedFeatures )

        QApplication.restoreOverrideCursor()
        return newSelectedFeatureList



    @staticmethod
    def setSelectFeatures1( canvas, selectGeometry, e ):
        doContains = True if (e.modifiers() & Qt.ShiftModifier) else False
        doDifference = True if e.modifiers() & Qt.ControlModifier else False
        selectedFeatures = QgsMapToolSelectUtils.setSelectFeatures( canvas, selectGeometry, doContains, doDifference )
        return selectedFeatures
    @staticmethod
    def setSelectFeaturesOrRubberband_Tas_1( canvas, selectGeometry, e ):

        doContains = True if (e.modifiers() & Qt.ShiftModifier) else False
        doDifference = True if e.modifiers() & Qt.ControlModifier else False
        selectedFeatures = QgsMapToolSelectUtils.setSelectFeaturesOrRubberband_Tas( canvas, selectGeometry, doContains, doDifference )
        return selectedFeatures

class QgsMapToolSelectPolygon(QgsMapTool):
    def __init__(self, canvas ):
        QgsMapTool.__init__(self, canvas )
        self.mRubberBand = None
        self.mCursor = Qt.ArrowCursor
        self.mFillColor = QColor( 254, 178, 76, 63 )
        self.mBorderColour = QColor( 254, 58, 29, 100 )
        self.mCanvas = canvas
    
    def canvasPressEvent( self, e ):
        if ( self.mRubberBand == None ):
            self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
            self.mRubberBand.setFillColor( self.mFillColor )
            self.mRubberBand.setBorderColor( self.mBorderColour )
        if ( e.button() == Qt.LeftButton ):
            self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )
        else:
            if ( self.mRubberBand.numberOfVertices() > 2 ):
                polygonGeom = self.mRubberBand.asGeometry()
                # QgsMapToolSelectUtils.setSelectFeatures( self.mCanvas, polygonGeom, e )
                QgsMapToolSelectUtils.setSelectFeatures1( self.mCanvas, polygonGeom, e )
            self.mRubberBand.reset( QGis.Polygon )
            self.mRubberBand = None
    
    def canvasMoveEvent( self, e ):
        if ( self.mRubberBand == None ):
            return
        if ( self.mRubberBand.numberOfVertices() > 0 ):
            self.mRubberBand.removeLastPoint( 0 )
            self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )

class QgsMapToolSelectFreehand(QgsMapTool):
    def __init__( self, canvas ):
        QgsMapTool.__init__( self, canvas )
        self.mRubberBand = None
        self.mCursor = Qt.ArrowCursor
        self.mFillColor = QColor( 254, 178, 76, 63 )
        self.mBorderColour = QColor( 254, 58, 29, 100 )
        self.mDragging = False
        self.mCanvas = canvas
    
    def canvasPressEvent( self, e ):
        if ( e.button() != Qt.LeftButton ):
            return
        if ( self.mRubberBand == None ):
            self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
            self.mRubberBand.setFillColor( self.mFillColor )
            self.mRubberBand.setBorderColor( self.mBorderColour )
        self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )
        self.mDragging = True
    
    def canvasMoveEvent( self, e ):
        if ( not self.mDragging or self.mRubberBand == None ):
            return
        self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )
    
    
    def canvasReleaseEvent( self, e ):
        selectedFeatures = []
        if ( self.mRubberBand == None ):
            return
        if ( self.mRubberBand.numberOfVertices() > 2 ):
            shapeGeom = self.mRubberBand.asGeometry()
            selectedFeatures = QgsMapToolSelectUtils.setSelectFeatures1( self.mCanvas, shapeGeom, e )
        self.mRubberBand.reset( QGis.Polygon )
        self.mRubberBand = None
        self.mDragging = False
        self.emit(SIGNAL("getSelectFeatures"), selectedFeatures)   
        
class QgsMapToolSelectRadius(QgsMapTool):
    def __init__( self, canvas ):
        QgsMapTool.__init__( self, canvas )
        self.mRubberBand = None
        self.mCursor = Qt.ArrowCursor
#         self.mFillColor = QColor( 254, 178, 76, 63 )
#         self.mBorderColour = QColor( 254, 58, 29, 100 )
        self.mDragging = False
        self.mCanvas = canvas
        
    def canvasPressEvent( self, e ):
        if ( e.button() != Qt.LeftButton ):
            return
        self.mRadiusCenter = self.toMapCoordinates( e.pos() )
    def canvasMoveEvent( self, e ):
        if ( e.buttons() != Qt.LeftButton ):
            return
        if ( not self.mDragging ):
            if ( self.mRubberBand == None ):
                self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
            self.mDragging = True
        radiusEdge = self.toMapCoordinates( e.pos() )
        self.setRadiusRubberBand( radiusEdge )
    def canvasReleaseEvent( self, e ):
        if ( e.button() != Qt.LeftButton ):
            return
        if ( not self.mDragging ):
            if ( self.mRubberBand == None ):
                self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
            self.mRadiusCenter = self.toMapCoordinates( e.pos() )
            radiusEdge = self.toMapCoordinates( QPoint( e.pos().x() + 1, e.pos().y() + 1 ) )
            self.setRadiusRubberBand( radiusEdge )
        radiusGeometry = self.mRubberBand.asGeometry()
        # QgsMapToolSelectUtils.setSelectFeatures( self.mCanvas, radiusGeometry, e )
        QgsMapToolSelectUtils.setSelectFeatures1( self.mCanvas, radiusGeometry, e )
        self.mRubberBand.reset( QGis.Polygon )
        self.mRubberBand = None
        self.mDragging = False    
    def setRadiusRubberBand( self, radiusEdge ):
        r = math.sqrt(self.mRadiusCenter.sqrDist( radiusEdge ) )
        self.mRubberBand.reset( QGis.Polygon )
        i = 0
        while i < 41:
            theta = i * ( 2.0 * 3.141592 / 40 )
            radiusPoint = QgsPoint( self.mRadiusCenter.x() + r * math.cos( theta ), self.mRadiusCenter.y() + r * math.sin( theta ) )
            self.mRubberBand.addPoint( radiusPoint )
            i += 1
    
