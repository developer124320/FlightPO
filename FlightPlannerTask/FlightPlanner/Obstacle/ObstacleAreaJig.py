'''
Created on Mar 24, 2015

@author: Administrator
'''
from PyQt4.QtGui import QMessageBox, QApplication, QColor, QMenu, QHBoxLayout, QCalendarWidget
from PyQt4.QtCore import Qt, QPoint, QRect, SIGNAL

from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnapper
from qgis.core import QGis, QgsRectangle, QgsGeometry, QgsCsException, QgsPoint,\
        QgsFeatureRequest, QgsCoordinateTransform, QgsFeature
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.types import SurfaceTypes, ProtectionAreaType
from FlightPlanner.helpers import MathHelper
from map.tools import QgsMapToolSelectUtils
from FlightPlanner.types import Point3D
from FlightPlanner.polylineArea import PolylineAreaPoint, PolylineArea
from FlightPlanner.Obstacle.ObstacleArea import SecondaryObstacleArea, PrimaryObstacleArea, PrimarySecondaryObstacleArea, SecondaryObstacleAreaWithManyPoints
import math,define

class ObstacleAreaJigSelectArea(QgsMapTool):

    def __init__(self, canvas, areaType):
        self.mCanvas = canvas
        self.areaType = areaType
        QgsMapTool.__init__(self, canvas)
        self.mCursor = Qt.ArrowCursor
        self.mRubberBand = None
        self.mDragging = False
        self.mSelectRect = QRect()
        self.mRubberBandResult = None
        self.mSnapper = QgsMapCanvasSnapper(canvas)
        self.lineCount = 0
        self.resultGeomList = []
        self.geomList = []
        self.area = None
        self.isFinished = False
#     QgsRubberBand* mRubberBand;
#     def reset(self):
#         self.startPoint = None
#         self.endPoint = None
#         self.isDrawing = False
#         SelectByRect.RubberRect.reset(QGis.Polygon)
#         self.layer = self.canvas.currentLayer()

    def canvasPressEvent(self, e):
        QgisHelper.ClearRubberBandInCanvas(define._canvas)
        self.mSelectRect.setRect( 0, 0, 0, 0 )
        self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
        self.startPoint, self.pointID, self.layer= self.snapPoint(e.pos())

    def canvasMoveEvent(self, e):
        if self.areaType == ProtectionAreaType.Secondary:
            if self.lineCount == 0:
                define._messageLabel.setText("Select a line or arc representing the INNER edge of the secondary area.")
            elif self.lineCount == 1:
                define._messageLabel.setText("Select a line representing the OUTER edge of the secondary area.")
        elif self.areaType == ProtectionAreaType.Primary:
            define._messageLabel.setText("")
        elif self.areaType == ProtectionAreaType.PrimaryAndSecondary:
            if self.lineCount == 0:
                define._messageLabel.setText("Select a line or arc representing the INNER edge of the FIRST secondary area.")
            elif self.lineCount == 1:
                define._messageLabel.setText("Select a line representing the OUTER edge of the FIRST secondary area.")
            elif self.lineCount == 2:
                define._messageLabel.setText("Select a line or arc representing the INNER edge of the SECOND secondary area.")
            elif self.lineCount == 3:
                define._messageLabel.setText("Select a line representing the OUTER edge of the SECOND secondary area.")
        else:
            define._messageLabel.setText("")


        if ( e.buttons() != Qt.LeftButton ):
            return
        if ( not self.mDragging ):
            self.mDragging = True
            self.mSelectRect.setTopLeft( e.pos() )
        self.mSelectRect.setBottomRight( e.pos() )
        QgsMapToolSelectUtils.setRubberBand( self.mCanvas, self.mSelectRect,self.mRubberBand )

    def canvasReleaseEvent(self, e):
        self.endPoint, self.pointID, self.layer= self.snapPoint(e.pos())

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


            selectedFeatures = QgsMapToolSelectUtils.setSelectFeaturesOrRubberband_Tas_1( self.mCanvas, selectGeom, e )
            if len(selectedFeatures) > 0:
                self.lineCount += 1
                geom = selectedFeatures[0].geometry()
                resultArray = QgisHelper.findArcOrLineInLineGeometry(geom, selectGeom)
                # if resultArray != None:
                #     bulge = MathHelper.smethod_60(resultArray[0], resultArray[int(len(resultArray)/2)], resultArray[len(resultArray)-1])
                #     bulge1 = MathHelper.smethod_60(resultArray[len(resultArray)-1], resultArray[int(len(resultArray)/2)], resultArray[0])
                #     n = 0
                pointArray0 = geom.asPolyline()
                self.resultGeomList.append(resultArray)
                self.geomList.append(pointArray0)
                if self.lineCount == 2 and self.areaType != ProtectionAreaType.PrimaryAndSecondary and self.areaType != ProtectionAreaType.Complex:
                    self.area = self.makeArea(self.resultGeomList, self.areaType)
                    pointArray = self.getPointArray(self.resultGeomList).method_14_closed()
                    self.mRubberBandResult = None
                    self.mRubberBandResult = QgsRubberBand( self.mCanvas, QGis.Polygon )
                    self.mRubberBandResult.setFillColor(QColor(255, 255, 255, 100))
                    self.mRubberBandResult.setBorderColor(QColor(0, 0, 0))
                    for point in pointArray:
                        self.mRubberBandResult.addPoint(point)
                    self.mRubberBandResult.show()


                    self.emit(SIGNAL("outputResult"), self.area, self.mRubberBandResult)
                    self.lineCount = 0
                    self.resultGeomList = []
                    self.isFinished = True
                    # self.rubberBandLine.reset(QGis.Line)
                elif self.lineCount == 4 and self.areaType == ProtectionAreaType.PrimaryAndSecondary:
                    self.area = self.makeArea(self.resultGeomList, self.areaType)
                    pointArray = self.getPointArray([self.resultGeomList[1], self.resultGeomList[3]]).method_14_closed()
                    self.mRubberBandResult = None
                    self.mRubberBandResult = QgsRubberBand( self.mCanvas, QGis.Polygon )
                    self.mRubberBandResult.setFillColor(QColor(255, 255, 255, 100))
                    self.mRubberBandResult.setBorderColor(QColor(0, 0, 0))
                    for point in pointArray:
                        self.mRubberBandResult.addPoint(point)
                    self.mRubberBandResult.show()


                    self.emit(SIGNAL("outputResult"), self.area, self.mRubberBandResult)
                    self.lineCount = 0
                    self.resultGeomList = []
                # else:
                #     return
            del selectGeom

            self.mRubberBand.reset( QGis.Polygon )
            del self.mRubberBand
            self.mRubberBand = None
        self.mDragging = False
    def getPointArray(self, geomList):
        pointArrayInner = geomList[0]
        pointArray1Outer = geomList[1]

        innerStartPoint = pointArrayInner[0]
        innerEndPoint = pointArrayInner[1]
        innerBulge = pointArrayInner[2]
        outerStartPoint = pointArray1Outer[0]
        outerEndPoint = pointArray1Outer[1]
        outerBulge = pointArray1Outer[2]

        line0 = QgsGeometry.fromPolyline([innerStartPoint, outerStartPoint])
        line1 = QgsGeometry.fromPolyline([innerEndPoint, outerEndPoint])

        # for i in range(1, len(pointArray0)):

        if line0.intersects(line1):
            tempPoint = outerStartPoint
            outerStartPoint = outerEndPoint
            outerEndPoint = tempPoint
            outerBulge = -outerBulge

        polylineArea = PolylineArea()
        polylineArea.Add(PolylineAreaPoint(innerStartPoint, innerBulge))
        polylineArea.Add(PolylineAreaPoint(innerEndPoint))
        polylineArea.Add(PolylineAreaPoint(outerEndPoint, -outerBulge))
        polylineArea.Add(PolylineAreaPoint(outerStartPoint))
        return polylineArea
    def makeArea(self, geomList, areaType):
        if areaType == ProtectionAreaType.Primary or areaType == ProtectionAreaType.Secondary:
            return self.makePrimaryAreaOrSecondaryArea(geomList, areaType)
        elif areaType == ProtectionAreaType.PrimaryAndSecondary:
            pointArray0 = geomList[0]
            pointArray1 = geomList[1]
            pointArray2 = geomList[2]
            pointArray3 = geomList[3]
            primaryArea = self.makePrimaryAreaOrSecondaryArea([pointArray0, pointArray2], ProtectionAreaType.Primary)
            secondaryArea1 = self.makePrimaryAreaOrSecondaryArea([pointArray0, pointArray1], ProtectionAreaType.Secondary)
            secondaryArea2 = self.makePrimaryAreaOrSecondaryArea([pointArray2, pointArray3], ProtectionAreaType.Secondary)
            return PrimarySecondaryObstacleArea(primaryArea, secondaryArea1, secondaryArea2)
            # if len(geomList[0]) == 2 and len(geomList[1]) == 2 and len(geomList[2]) == 2 and len(geomList[3]) == 2:
            #     for i in range(1, len(geomList)):
            #         pointArray0 = geomList[0]
            #         pointArray1 = geomList[i]
            #         line0 = QgsGeometry.fromPolyline([pointArray0[0], pointArray1[0]])
            #         line1 = QgsGeometry.fromPolyline([pointArray0[len(pointArray0) - 1], pointArray1[len(pointArray1) - 1]])
            #         if line0.intersects(line1):
            #             pointArray1.reverse()
            #     pointArray0 = geomList[0]
            #     pointArray1 = geomList[1]
            #     pointArray2 = geomList[2]
            #     pointArray3 = geomList[3]
            #     area = PrimarySecondaryObstacleArea()
            #     area.set_areas(pointArray0, pointArray1, pointArray2, pointArray3)
            #     return area
            # return None

        return None
    def makePrimaryAreaOrSecondaryArea(self, geomList, areaType):
        pointArrayInner = geomList[0]
        pointArray1Outer = geomList[1]

        innerStartPoint = pointArrayInner[0]
        innerEndPoint = pointArrayInner[1]
        innerBulge = pointArrayInner[2]
        outerStartPoint = pointArray1Outer[0]
        outerEndPoint = pointArray1Outer[1]
        outerBulge = pointArray1Outer[2]

        line0 = QgsGeometry.fromPolyline([innerStartPoint, outerStartPoint])
        line1 = QgsGeometry.fromPolyline([innerEndPoint, outerEndPoint])

        # for i in range(1, len(pointArray0)):

        if line0.intersects(line1):
            tempPoint = Point3D(outerStartPoint.get_X(), outerStartPoint.get_Y())
            outerStartPoint = Point3D(outerEndPoint.get_X(), outerEndPoint.get_Y())
            outerEndPoint = Point3D(tempPoint.get_X(), tempPoint.get_Y())
            outerBulge = -outerBulge
        if areaType == ProtectionAreaType.Primary:
            polylineArea = PolylineArea()
            polylineArea.Add(PolylineAreaPoint(innerStartPoint, innerBulge))
            polylineArea.Add(PolylineAreaPoint(innerEndPoint))
            polylineArea.Add(PolylineAreaPoint(outerEndPoint, -outerBulge))
            polylineArea.Add(PolylineAreaPoint(outerStartPoint))
            return PrimaryObstacleArea(polylineArea)
        elif areaType == ProtectionAreaType.Secondary:
            if innerBulge == 0 and outerBulge == 0:
                return SecondaryObstacleArea(innerStartPoint, innerEndPoint, outerStartPoint, outerEndPoint, MathHelper.getBearing(innerStartPoint, innerEndPoint))
            elif innerBulge != 0 and outerBulge != 0:
                if round(innerBulge, 1) != round(outerBulge, 1):
                    return None
                innerCenterPoint = MathHelper.smethod_71(innerStartPoint, innerEndPoint, innerBulge)
                outerCenterPoint = MathHelper.smethod_71(outerStartPoint, outerEndPoint, outerBulge)

                innerRadius = MathHelper.calcDistance(innerCenterPoint, innerStartPoint);
                outerRadius = MathHelper.calcDistance(outerCenterPoint, outerStartPoint);

                bearing = (MathHelper.getBearing(innerCenterPoint, innerStartPoint) + MathHelper.getBearing(innerCenterPoint, innerEndPoint)) / 2
                innerMiddlePoint = MathHelper.distanceBearingPoint(innerCenterPoint, bearing, innerRadius)
                if round(MathHelper.smethod_60(innerStartPoint, innerMiddlePoint, innerEndPoint), 4) != round(outerBulge, 4):
                    bearing += 3.14159265358979
                    innerMiddlePoint = MathHelper.distanceBearingPoint(innerCenterPoint, bearing, innerRadius)

                bearing = (MathHelper.getBearing(outerCenterPoint, outerStartPoint) + MathHelper.getBearing(outerCenterPoint, outerEndPoint)) / 2
                outerMiddlePoint = MathHelper.distanceBearingPoint(outerCenterPoint, bearing, outerRadius)
                if round(MathHelper.smethod_60(outerStartPoint, outerMiddlePoint, outerEndPoint), 4) != round(outerBulge, 4):
                    bearing += 3.14159265358979
                    outerMiddlePoint = MathHelper.distanceBearingPoint(outerCenterPoint, bearing, outerRadius)
                return SecondaryObstacleArea(innerStartPoint, innerMiddlePoint, innerEndPoint, outerStartPoint, None, outerMiddlePoint, outerEndPoint, innerBulge, innerBulge)
            return None
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



class ObstacleAreaJigCreateArea(QgsMapTool):
    def __init__(self, canvas, areaType):
        QgsMapTool.__init__(self, canvas)
        self.mCanvas = canvas
        self.areaType = areaType
        self.annotation = None
        self.rubberBand = QgsRubberBand(canvas, QGis.Point)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(10)
        self.rubberBandClick = QgsRubberBand(canvas, QGis.Point)
        self.rubberBandClick.setColor(Qt.green)
        self.rubberBandClick.setWidth(3)
        self.obstaclesLayerList = QgisHelper.getSurfaceLayers(SurfaceTypes.Obstacles)
        self.demLayerList = QgisHelper.getSurfaceLayers(SurfaceTypes.DEM)

        self.mRubberBand = None
        self.mRubberBand0 = QgsRubberBand( self.mCanvas, QGis.Polygon )
        self.mCursor = Qt.ArrowCursor
        self.mFillColor = QColor( 254, 178, 76, 63 )
        self.mBorderColour = QColor( 254, 58, 29, 100 )
        self.mRubberBand0.setBorderColor( self.mBorderColour )
        self.polygonGeom = None
        self.drawFlag = False
        self.mSnapper = QgsMapCanvasSnapper(canvas)
        self.resultPolylineArea = PolylineArea()
#         self.constructionLayer = constructionLayer
        self.menuString = ""
        self.isPrimaryPolylineStarted = False
        self.primaryPolyline = PolylineArea()
    def createContextMenu(self, areaType, isStarted = False):
        menu = QMenu()
        # h = QHBoxLayout(menu)
        # c = QCalendarWidget()
        # h.addWidget(c)
        if areaType == ProtectionAreaType.Primary:
            actionEnter = QgisHelper.createAction(menu, "Enter", self.menuEnterClick)
            actionCancel = QgisHelper.createAction(menu, "Cancel", self.menuCancelClick)
            actionArc = QgisHelper.createAction(menu, "Arc", self.menuArcClick)
            actionUndo = QgisHelper.createAction(menu, "Undo", self.menuUndoClick)
            menu.addAction( actionEnter )
            menu.addAction( actionCancel )
            menu.addAction( actionArc )
            menu.addAction( actionUndo )
        elif areaType == ProtectionAreaType.Secondary:
            if not isStarted:
                actionEnter = QgisHelper.createAction(menu, "Enter", self.menuEnterClick)
                actionCancel = QgisHelper.createAction(menu, "Cancel", self.menuCancelClick)
                actionUndo = QgisHelper.createAction(menu, "Undo", self.menuUndoClick)
                actionPrimatyPolylineStart = QgisHelper.createAction(menu, "Strat INNER edge of the secondary area", self.menuPrimaryStartClick)
                actionPrimatyPolylineEnd = QgisHelper.createAction(menu, "End INNER edge of the secondary area", self.menuPrimaryEndClick)
                menu.addAction( actionEnter )
                menu.addAction( actionCancel )
                menu.addAction( actionUndo )
                menu.addAction( actionPrimatyPolylineStart )
                menu.addAction( actionPrimatyPolylineEnd )
                actionPrimatyPolylineStart.setEnabled(not self.isPrimaryPolylineStarted)
                actionPrimatyPolylineEnd.setEnabled(self.isPrimaryPolylineStarted)
            else:
                actionPrimatyPolylineStart = QgisHelper.createAction(menu, "Strat INNER edge of the secondary area", self.menuPrimaryStartClick)
                actionPrimatyPolylineEnd = QgisHelper.createAction(menu, "End INNER edge of the secondary area", self.menuPrimaryEndClick)
                menu.addAction( actionPrimatyPolylineStart )
                menu.addAction( actionPrimatyPolylineEnd )
                actionPrimatyPolylineStart.setEnabled(not self.isPrimaryPolylineStarted)
                actionPrimatyPolylineEnd.setEnabled(self.isPrimaryPolylineStarted)
        return menu
    def menuPrimaryStartClick(self):
        self.primaryPolyline = PolylineArea()
        self.isPrimaryPolylineStarted = True
        # self.menuString = "Enter"
    def menuPrimaryEndClick(self):
        self.isPrimaryPolylineStarted = False
        # self.menuString = "Enter"
    def menuEnterClick(self):
        self.menuString = "Enter"
    def menuCancelClick(self):
        self.menuString = "Cancel"
    def menuArcClick(self):
        self.menuString = "Arc"
    def menuUndoClick(self):
        self.menuString = "Undo"
    def reset(self):
        self.Point = None
    def canvasPressEvent( self, e ):
        define._messageLabel.setText("")
        self.menuString = ""
        pointBackground = e.pos()
#         self.Point = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas)
        self.Point, self.pointID, self.layer= self.snapPoint(e.pos())
        self.selectedLayerFromSnapPoint = None


        if ( self.mRubberBand == None ):
            self.resultPolylineArea = PolylineArea()
            self.mRubberBand0.reset( QGis.Polygon )
#             define._canvas.clearCache ()
            self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
            self.mRubberBand0 = QgsRubberBand( self.mCanvas, QGis.Polygon )
            self.mRubberBand.setFillColor( self.mFillColor )
            self.mRubberBand.setBorderColor( self.mBorderColour )
            self.mRubberBand0.setFillColor( QColor(255, 255, 255, 100) )
            self.mRubberBand0.setBorderColor( QColor(0, 0, 0) )
        if ( e.button() == Qt.LeftButton ):
            if self.Point == None:
                self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )
                self.resultPolylineArea.Add(PolylineAreaPoint(self.toMapCoordinates( e.pos() )))
                if self.isPrimaryPolylineStarted:
                    self.primaryPolyline.Add(PolylineAreaPoint(self.toMapCoordinates( e.pos() )))
            else:
                self.mRubberBand.addPoint( self.Point )
                self.resultPolylineArea.Add(PolylineAreaPoint(self.Point))
                if self.isPrimaryPolylineStarted:
                    self.primaryPolyline.Add(PolylineAreaPoint(self.toMapCoordinates( e.pos() )))
        else:
            menu = None
            if self.areaType == ProtectionAreaType.Secondary and len(self.resultPolylineArea) == 0:
                menu = self.createContextMenu(self.areaType, True)
                menu.exec_( define._canvas.mapToGlobal(e.pos() ))
                return

            if ( self.mRubberBand.numberOfVertices() > 2 ):
                self.polygonGeom = self.mRubberBand.asGeometry()
            else:
                return
#                 QgsMapToolSelectUtils.setSelectFeatures( self.mCanvas, polygonGeom, e )
            menu = self.createContextMenu(self.areaType)
            menu.exec_( define._canvas.mapToGlobal(e.pos() ))

            if self.menuString == "Cancel" or self.menuString == "Arc":
                return
            elif self.menuString == "Undo":
                if ( self.mRubberBand.numberOfVertices() > 0 ):

                    self.mRubberBand = None
                    QgisHelper.ClearRubberBandInCanvas(define._canvas)
                    self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
                    self.mRubberBand.setFillColor( self.mFillColor )
                    self.mRubberBand.setBorderColor( self.mBorderColour )
                    self.resultPolylineArea[self.resultPolylineArea.Count - 2].bulge = 0.0
                    self.resultPolylineArea.pop(self.resultPolylineArea.Count - 1)
                    if self.isPrimaryPolylineStarted and len(self.primaryPolyline) > 0:
                        self.primaryPolyline.pop(self.primaryPolyline.Count - 1)
                    for pt in self.resultPolylineArea.method_14():
                        self.mRubberBand.addPoint(pt)
                return
            elif self.menuString == "Enter":
                # if self.areaType == ProtectionAreaType.Secondary:
                #     if self.resultPolylineArea.Count != 4:
                #         define._messageLabel.setText("The count of point of Secondary Area must be 4.")
                #         return
                self.mRubberBand.reset( QGis.Polygon )
                self.mRubberBand0.reset( QGis.Polygon )
#             define._canvas.clearCache ()

                self.mRubberBand0 = QgsRubberBand( self.mCanvas, QGis.Polygon )

                self.mRubberBand0.setFillColor( QColor(255, 255, 255, 100) )
                self.mRubberBand0.setBorderColor( QColor(0, 0, 0) )
                for pt in self.resultPolylineArea.method_14():
                    self.mRubberBand0.addPoint(pt)
                # self.mRubberBand0.addGeometry(self.polygonGeom, None)
                n = self.mRubberBand0.numberOfVertices()
                self.mRubberBand0.show()
                self.mRubberBand = None
                area = None
                if self.areaType == ProtectionAreaType.Primary:
                    area = PrimaryObstacleArea(self.resultPolylineArea)
                elif self.areaType == ProtectionAreaType.Secondary:
                    if len(self.resultPolylineArea) == 4:
                        area = SecondaryObstacleArea(self.resultPolylineArea[0].Position, self.resultPolylineArea[1].Position, self.resultPolylineArea[3].Position, self.resultPolylineArea[2].Position, MathHelper.getBearing(self.resultPolylineArea[0].Position, self.resultPolylineArea[1].Position))

                    else:
                        if self.primaryPolyline.Count < 2:
                            define._messageLabel.setText("The PrimaryLine in Secondary Area must exist.")
                            return
                        if self.isPrimaryPolylineStarted:
                            define._messageLabel.setText("You must finish  the input of  PrimaryLine.")
                            return
                        area = SecondaryObstacleAreaWithManyPoints(self.resultPolylineArea, self.primaryPolyline)
                self.emit(SIGNAL("outputResult"), area, self.mRubberBand0)
            n = 0
    def canvasMoveEvent( self, e ):
        self.rubberBand.reset(QGis.Point)
#         snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper , define._canvas, True)
        snapPoint, snapPointID, layer = self.snapPoint(e.pos(), True)
        if snapPoint != None:
            self.rubberBand.addPoint(snapPoint)
            self.rubberBand.show()
        if ( self.mRubberBand == None ):
            return

        if ( self.mRubberBand.numberOfVertices() > 0 ):
            if self.menuString != "Undo":
                self.mRubberBand.removeLastPoint( 0 )
            else:
                self.menuString = ""
            point2 = None
            if snapPoint != None:
                self.mRubberBand.addPoint( snapPoint)
                point2 = snapPoint
            else:
                self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )
                point2 = self.toMapCoordinates( e.pos() )
            if self.menuString == "Arc":
                point0 = self.resultPolylineArea[self.resultPolylineArea.Count - 2].Position
                point1 = self.resultPolylineArea[self.resultPolylineArea.Count - 1].Position
                # point2 = self.mRubberBand.getPoint(self.mRubberBand.numberOfVertices() - 1)
                bulge = MathHelper.smethod_60(point0, point1, point2)
                self.resultPolylineArea[self.resultPolylineArea.Count - 2].bulge = bulge
                self.mRubberBand = None
                QgisHelper.ClearRubberBandInCanvas(define._canvas)
                self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
                self.mRubberBand.setFillColor( self.mFillColor )
                self.mRubberBand.setBorderColor( self.mBorderColour )

                for pt in self.resultPolylineArea.method_14():
                    self.mRubberBand.addPoint(pt)
                self.mRubberBand.addPoint(point2)


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

    def deactivate(self):
        self.rubberBand.reset(QGis.Point)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))