
from qgis.gui import QgsMapToolEmitPoint, QgsMapTool, QgsMapCanvasSnapper, QgsRubberBand
from qgis.core import QGis, QgsFeatureRequest, QgsRaster,QgsPoint, QgsSnapper, QgsVectorLayer
from PyQt4.QtCore import Qt, SIGNAL

from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.types import SurfaceTypes

import define

class CaptureCoordinateTool(QgsMapTool):
    def __init__(self, canvas, txtXCoord, txtYCoord, annotation = None):
        self.canvas = canvas
        self.txtXCoord = txtXCoord
        self.txtYCoord = txtYCoord
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.annotation = annotation
        self.mSnapper = QgsMapCanvasSnapper(canvas)
        self.rubberBand = QgsRubberBand(canvas, QGis.Point)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(10)
        self.rubberBandClick = QgsRubberBand(canvas, QGis.Point)
        self.rubberBandClick.setColor(Qt.green)
        self.rubberBandClick.setWidth(3)
#         lblDoc = QTextDocument(label)
#         self.annotation.setDocument(lblDoc)
#         self.annotation.setFrameBackgroundColor(QColor(0,0,0,0)) 
#         self.annotation.setFrameSize( QSizeF( 30, 20 ) )
                
        self.reset()
    def reset(self):
        self.Point = None
#     def canvasPressEvent(self, e):        
    def canvasReleaseEvent(self, e):     
#         self.Point = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas)
        self.Point = self.snapPoint(e.pos())
        if self.annotation is not None:
            self.annotation.setMapPosition(self.Point)
            self.annotation.show()
        else:
            self.rubberBandClick.reset(QGis.Point)
#         snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)
        
            self.rubberBandClick.addPoint(self.Point)
            self.rubberBandClick.show()
#         self.setOffsetFromReferencePoint (QPointF(self.Point.x(),self.Point.y()))
        self.txtXCoord.setText(str(self.Point.x()))
#         print str(self.Point.x())
        self.txtYCoord.setText(str(self.Point.y()))
    def canvasMoveEvent(self, e):
        if define._snapping == False:
            return
        self.rubberBand.reset(QGis.Point)
#         snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)
        snapPoint = self.snapPoint(e.pos(), True)
        if snapPoint == None:
            return
        self.rubberBand.addPoint(snapPoint)
        self.rubberBand.show()
    def snapPoint(self, p, bNone = False):
        if define._snapping == False:
            return define._canvas.getCoordinateTransform().toMapCoordinates( p )
        snappingResults = self.mSnapper.snapToBackgroundLayers( p )
        if ( snappingResults[0] != 0 or len(snappingResults[1]) < 1 ):
            if bNone:
                return None
            else:
                return define._canvas.getCoordinateTransform().toMapCoordinates( p )
        else:
            return snappingResults[1][0].snappedVertex
        
    def deactivate(self):
        self.rubberBand.reset(QGis.Point)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))
        
        
class CaptureCoordinateToolUpdate(QgsMapTool):
    def __init__(self, canvas, annotation = None):
        self.canvas = canvas
#         self.tableView = tableView
#         self.standardItemModel = standardItemModel
#         self.txtXCoord = txtXCoord
#         self.txtYCoord = txtYCoord
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.annotation = annotation
        self.mSnapper = QgsMapCanvasSnapper(canvas)
        self.rubberBand = QgsRubberBand(canvas, QGis.Point)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(10)
        self.rubberBandClick = QgsRubberBand(canvas, QGis.Point)
        self.rubberBandClick.setColor(Qt.green)
        self.rubberBandClick.setWidth(3)
        self.obstaclesLayerList = QgisHelper.getSurfaceLayers(SurfaceTypes.Obstacles)
        self.demLayerList = QgisHelper.getSurfaceLayers(SurfaceTypes.DEM)
#         lblDoc = QTextDocument(label)
#         self.annotation.setDocument(lblDoc)
#         self.annotation.setFrameBackgroundColor(QColor(0,0,0,0)) 
#         self.annotation.setFrameSize( QSizeF( 30, 20 ) )
                
        self.reset()
    def reset(self):
        self.Point = None
#     def canvasPressEvent(self, e):        
    def canvasReleaseEvent(self, e): 
        pointBackground = e.pos()    
#         self.Point = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas)
        self.Point, self.pointID, self.layer= self.snapPoint(e.pos())
        self.selectedLayerFromSnapPoint = None
        resultValueList = []
        if self.annotation is not None:
            self.annotation.setMapPosition(self.Point)
            self.annotation.show()
        else:
            self.rubberBandClick.reset(QGis.Point)
#         snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)
        
            self.rubberBandClick.addPoint(self.Point)
            self.rubberBandClick.show()
        self.selectedLayerFromSnapPoint = define._canvas.currentLayer()
        # if self.obstaclesLayerList != None:
        #     for obstacleLayer in self.obstaclesLayerList:
        #         if self.layer == None:
        #             break
        #         if obstacleLayer.name() == self.layer.name():
        #             self.selectedLayerFromSnapPoint = self.layer
        #             break
        if self.selectedLayerFromSnapPoint != None and isinstance(self.selectedLayerFromSnapPoint, QgsVectorLayer) and self.pointID != None:
            # if self.pointID == None:
            #     resultValueList.append("Background")
            #
            #     resultValueList.append(str(self.Point.x()))
            #     resultValueList.append(str(self.Point.y()))
            #     resultValueList.append("0.0")
            # else:
            dataProvider = self.selectedLayerFromSnapPoint.dataProvider()
            featureIter = dataProvider.getFeatures( QgsFeatureRequest(self.pointID))
            feature = None
            for feature0 in featureIter:
                feature = feature0

            idx = self.selectedLayerFromSnapPoint.fieldNameIndex('Name')
            if not idx == -1:
                idValue = feature.attributes()[idx]
                resultValueList.append(idValue.toString())
            else:
                resultValueList.append("")
#             itemList.append(QStandardItem(idValue.toString()))

            resultValueList.append(str(self.Point.x()))
            resultValueList.append(str(self.Point.y()))

            idx = self.selectedLayerFromSnapPoint.fieldNameIndex('Altitude')
            if not idx == -1:
                altitudeValue = feature.attributes()[idx]
                resultValueList.append(altitudeValue.toString())
            else:
                resultValueList.append("0.0")

        else:
            
            
            
            if self.Point != None:
                identifyResult = None
                idValue = "Background"
                if self.demLayerList != None:
                    
                    for demLayer in self.demLayerList:
                        identifyResults = demLayer.dataProvider().identify(self.Point, QgsRaster.IdentifyFormatValue)
                        identifyResult = identifyResults.results()
                if identifyResult != None and identifyResult[1].toString() != "":
                    idValue = "DEM"
                
                resultValueList.append(idValue)                
                resultValueList.append(str(self.Point.x()))
                resultValueList.append(str(self.Point.y()))
                if identifyResult != None and identifyResult[1].toString() != "":
                    resultValueList.append(identifyResult[1].toString()) 
                else:
                    resultValueList.append("0") 
        self.emit(SIGNAL("resultPointValueList"), resultValueList)     

    def canvasMoveEvent(self, e):
        if define._snapping == False:
            return
        self.rubberBand.reset(QGis.Point)
#         snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)
        snapPoint, snapPointID, layer = self.snapPoint(e.pos(), True)
        if snapPoint == None:
            return
        self.rubberBand.addPoint(snapPoint)
        self.rubberBand.show()
#         print snapPointID
    def snapPoint(self, p, bNone = False):
        if define._snapping == False:
            return (define._canvas.getCoordinateTransform().toMapCoordinates( p ), None, None)
        snappingResults = self.mSnapper.snapToCurrentLayer( p , QgsSnapper.SnapToVertex)
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