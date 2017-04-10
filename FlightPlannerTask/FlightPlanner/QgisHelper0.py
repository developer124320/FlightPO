# -*- coding: UTF-8 -*-
from qgis.core import QgsVectorLayer,QgsRasterLayer,  QgsMapLayerRegistry, QgsFeature, QgsPoint\
    ,QgsFeatureRequest, QGis, QgsProject, QgsSnapper, QgsTolerance, QgsCoordinateTransform, \
    QgsCoordinateReferenceSystem, QgsRectangle, QgsMapLayer, QgsLayerTreeNode, \
    QgsLayerTreeLayer, QgsLayerTreeGroup, QgsField, QgsSymbolV2, QgsSvgMarkerSymbolLayerV2, \
    QgsRendererCategoryV2, QgsCategorizedSymbolRendererV2
from qgis.gui import QgsMapCanvasLayer, QgsTextAnnotationItem,QgsRubberBand
from qgis.core import QgsGeometry, QgsPalLayerSettings
from PyQt4.QtGui import QAction, QIcon, QMessageBox
from PyQt4.QtCore import SIGNAL, QCoreApplication,QSize, Qt,QVariant
from PyQt4.QtGui import QColor, QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.gui import QgsTextAnnotationItem, QgsAnnotationItem, QgsRubberBand
from qgis.core import QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2

from FlightPlanner.types import Point3D, SurfaceTypes, SelectionModeType, Point3dCollection,\
                                GeoCalculationType, DistanceUnits
from FlightPlanner.expressions import Expressions
from FlightPlanner.messages import Messages
from FlightPlanner.helpers import MathHelper, Distance, Unit
# from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint

import define, math


#from qgis.gui import *
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
class QgisHelper:
    def __init__(self):
        pass
    
#     @staticmethod
#     def intersectVectors(point1, point2, point3, point4):
#         line1 = QgsGeometry.fromPolyline([point1, point2])
#         line2 = QgsGeometry.fromPolyline([point3, point4])

    @staticmethod
    def showMessageBoxYesNo(text, informText):
        msgBox = QMessageBox()
        msgBox.setText(text)
        msgBox.setInformativeText(informText)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)
        ret = msgBox.exec_()
        if ret == QMessageBox.Yes:
            return True
        else:
            return False
    @staticmethod
    def findArcOrLineInLineGeometry(inputLineGeom, intersectGeom):
        # This method find the arc or line that intersects with geometry named "intersectGeom"  when user input the line named "inputLineGeom".
        #//////// Input Parameter //////////#
            # Here, "intersectGeom" can be Polygon or Line.
            # "inputLineGeom" must be Line containing curves.
        #/////// Return Value /////////////#
            # Here, arc or line has two points and arc has his bulge.
            # The return value is array with start point and end point, bulge.

        pointArray = inputLineGeom.asPolyline()
        dist0 = MathHelper.calcDistance(pointArray[0], pointArray[1])
        equalCount = 0
        findPointArrayInLine = []
        temppointArray = [pointArray[0], pointArray[1]]
        pointCount  = len(pointArray)
        startNum = 0
        endNum = 1
        for i in range(1, pointCount):
            if i == pointCount - 1:
                break
            dist1 = MathHelper.calcDistance(pointArray[i], pointArray[i + 1])
            if round(dist0, 2) == round(dist1, 2):
                temppointArray.append(pointArray[i + 1])
                equalCount += 1

            else:
                if equalCount > 3:
                    endNum = i
                    # c0 = MathHelper.calcDistance(temppointArray[0], temppointArray[1])
                    # c1 = MathHelper.calcDistance(temppointArray[0], pointArray[startNum - 1])
                    # c2 = MathHelper.calcDistance(temppointArray[len(temppointArray) -1], pointArray[endNum + 1])

                    temppointArray.insert(0, pointArray[startNum - 1])
                    temppointArray.append(pointArray[endNum + 1])
                    findPointArrayInLine.append(temppointArray)
                temppointArray = [pointArray[i], pointArray[i + 1]]
                dist0 = dist1
                equalCount = 0
                startNum = i

        for ptArray in findPointArrayInLine:
            line = QgsGeometry.fromPolyline(ptArray)
            if line.intersects(intersectGeom):
                startPoint3d = Point3D(ptArray[0].x(), ptArray[0].y())
                endPoint3d = Point3D(ptArray[len(ptArray) - 1].x(), ptArray[len(ptArray) - 1].y())
                middlePoint3d = Point3D(ptArray[int(len(ptArray) / 2)].x(), ptArray[int(len(ptArray) / 2)].y())
                bulge0 = MathHelper.smethod_60(startPoint3d, middlePoint3d, endPoint3d)

                return [startPoint3d, endPoint3d, bulge0]

        for i in range(1, pointCount):
            line = QgsGeometry.fromPolyline([pointArray[i - 1], pointArray[i]])
            if line.intersects(intersectGeom):
                startPoint3d = Point3D(pointArray[i - 1].x(), pointArray[i - 1].y())
                endPoint3d = Point3D(pointArray[i].x(), pointArray[i].y())
                return [startPoint3d, endPoint3d, 0.0]

        return None

    @staticmethod
    def removeGroupFromName(qgsLayerTreeView, groupName):
        layerTreeModel = qgsLayerTreeView.layerTreeModel()
        layerTreeGroup = layerTreeModel.rootGroup()
        rowCount = layerTreeModel.rowCount()
        if rowCount > 0:
            for i in range(rowCount):
                qgsLayerTreeNode = layerTreeModel.index2node(layerTreeModel.index(i, 0))
                if qgsLayerTreeNode.nodeType() == 0:
                    qgsLayerTreeNode._class_ =  QgsLayerTreeGroup
                    if isinstance(qgsLayerTreeNode, QgsLayerTreeGroup) and qgsLayerTreeNode.name() == groupName:
                        qgsLayerTreeNode._class_ = QgsLayerTreeNode
                        parntNode = qgsLayerTreeNode.parent()
                        parntNode.removeChildNode(qgsLayerTreeNode)
                        return

                    pass

    @staticmethod
    def convexFull(polylineAreaList):
        geom = QgsGeometry()
        geomTemp = QgsGeometry()
        point3dCollection = []
        i = 0
        for polylineArea in polylineAreaList:
            point3dCollection.extend(polylineArea.method_14_closed())
            
#             if i == 0:
#                 geomTemp = QgsGeometry.fromPolyline(point3dCollection)
#             else:
#                 geom = geomTemp.combine(QgsGeometry.fromPolyline(point3dCollection))
#                 geomTemp = geom
#         
#             i += 1
        geomTemp = QgsGeometry.fromPolyline(point3dCollection)    
        geom = geomTemp.convexHull()
        polylineList= geom.asPolygon()
#         polylineArea = PolylineArea()
#         for point in pointList:
#             polylineArea.Add(PolylineAreaPoint(point))
        return polylineList[0]
    @staticmethod
    def createWPTPointLayer(layerName, pointList):
        mapUnits = define._canvas.mapUnits()
        if define._mapCrs == None:
            if mapUnits == QGis.Meters:
                resultLayer = QgsVectorLayer("Point?crs=EPSG:32633", "NominalTrack", "memory")
            else:
                resultLayer = QgsVectorLayer("Point?crs=EPSG:4326", "NominalTrack", "memory")
        else:
            resultLayer = QgsVectorLayer("Point?crs=%s"%define._mapCrs.authid (), "NominalTrack", "memory")
#         if mapUnits == QGis.Meters:
#             resultLayer = QgsVectorLayer("Point?crs=EPSG:32633", "WPT", "memory")
#         else:
#             resultLayer = QgsVectorLayer("Point?crs=EPSG:4326", "WPT", "memory")
        fieldName = "CATEGORY"
        resultLayer.dataProvider().addAttributes( [QgsField(fieldName, QVariant.String)] )
        resultLayer.startEditing()
        fields = resultLayer.pendingFields()
        i = 1
        feature = QgsFeature()
        feature.setFields(fields)
        for point, categoryText in pointList:
            feature.setGeometry(QgsGeometry.fromPoint (point))                
            feature.setAttribute(fieldName, categoryText)
            
            resultLayer.addFeature(feature)
        resultLayer.commitChanges()
        
        '''FlyOver'''
        symbolFlyOver = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
        symbolFlyOver.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyover.svg", 9.0, 0.0)
        symbolFlyOver.appendSymbolLayer(svgSymLayer)
        renderCatFlyOver = QgsRendererCategoryV2(1, symbolFlyOver,"FlyOver")
        
        '''FlyBy'''
        symbolFlyBy = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
        symbolFlyBy.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyby.svg", 9.0, 0.0)
        symbolFlyBy.appendSymbolLayer(svgSymLayer)
        renderCatFlyBy = QgsRendererCategoryV2(0, symbolFlyBy,"FlyBy")

        symRenderer = QgsCategorizedSymbolRendererV2(Expressions.COMMON_WPT_EXPRESION, [renderCatFlyOver, renderCatFlyBy])

        resultLayer.setRendererV2(symRenderer)
        return resultLayer
        
    @staticmethod
    def createPolylineLayer(layerName, featureData, fields = []):
        mapUnits = define._canvas.mapUnits()
        if define._mapCrs == None:
            if mapUnits == QGis.Meters:
                resultLayer = QgsVectorLayer("linestring?crs=EPSG:32633", layerName, "memory")
            else:
                resultLayer = QgsVectorLayer("linestring?crs=EPSG:4326", layerName, "memory")
        else:
            resultLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), layerName, "memory")
        
#         if mapUnits == QGis.Meters:
#             resultLayer = QgsVectorLayer("linestring?crs=EPSG:32633", layerName, "memory")
#         else:
#             resultLayer = QgsVectorLayer("linestring?crs=EPSG:4326", layerName, "memory")
        fieldName = "CATEGORY"
        resultLayer.dataProvider().addAttributes( fields )
        resultLayer.startEditing()
        fields = resultLayer.pendingFields()
        feature = QgsFeature()
        feature.setFields(fields)
        
        for pointList, attrValues in featureData:
            feature.setGeometry(QgsGeometry.fromPolyline(pointList))   
            for fieldName, fieldValue in attrValues:             
                feature.setAttribute(fieldName, fieldValue)
            
            resultLayer.addFeature(feature)
        resultLayer.commitChanges()
        return resultLayer
        
    @staticmethod
    def setLabelSettingToPolyline(lineLayer, expression):
        palSetting = QgsPalLayerSettings()
        palSetting.readFromLayer(lineLayer)
        palSetting.enabled = True
        palSetting.fieldName = expression
        palSetting.isExpression = True
        palSetting.placement = QgsPalLayerSettings.Line
        palSetting.placementFlags = QgsPalLayerSettings.AboveLine
#         palSetting.addDirectionSymbol = True
#         palSetting.leftDirectionSymbol = "<"
#         palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '6', "")
        palSetting.writeToLayer(lineLayer)
        
    @staticmethod
    def drawPolyline(pointArray):
#         resultLayer = QgsVectorLayer("linestring?crs=epsg:4326", "result", "memory")
        
        if define._mapCrs == None:
            resultLayer = QgsVectorLayer("linestring?crs=EPSG:4326", "result", "memory")
        else:
            resultLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), "result", "memory")        
        
        QgsMapLayerRegistry.instance().addMapLayer(resultLayer)
#         print resultLayer
        feature = QgsFeature()
        feature.setGeometry( QgsGeometry.fromPolyline(pointArray) )
        resultLayer.startEditing()
        resultLayer.addFeature(feature)
        resultLayer.commitChanges()
        return resultLayer
    
    @staticmethod
    def drawPolygon(pointArray):
        qgsPoints = []
        for point in pointArray:
            qgsPoints.append(QgsPoint(point.x(), point.y()))
            
        if define._mapCrs == None:
            resultLayer = QgsVectorLayer("MultiPolygon?crs=EPSG:4326", "result", "memory")
        else:
            resultLayer = QgsVectorLayer("MultiPolygon?crs=%s"%define._mapCrs.authid (), "result", "memory")        
#         resultLayer = QgsVectorLayer("MultiPolygon?crs=epsg:4326", "result", "memory")
        QgsMapLayerRegistry.instance().addMapLayer(resultLayer)

        feature = QgsFeature()
        feature.setGeometry( QgsGeometry.fromPolygon(qgsPoints) )
        resultLayer.startEditing()
        resultLayer.addFeature(feature)
        resultLayer.commitChanges()
        return resultLayer

    @staticmethod
    def appendToCanvas(canvas, layers, groupName = None, groupRemove = False):

        canvasLayers = canvas.layers()
        newCanvasLayers = []
        for mapLayer in canvasLayers:
            newCanvasLayers.append(QgsMapCanvasLayer(mapLayer))
            
        if groupRemove:
            
            ltModel = define._mLayerTreeView.layerTreeModel()
            rootGroup = ltModel.rootGroup()
            matchesList = ltModel.match(ltModel.index(0, 0), Qt.DisplayRole, groupName)
            if len(matchesList) > 0:
                newGroup = ltModel.index2node(matchesList[0])
                for childNode in newGroup.children():
                    if not isinstance(childNode, (QgsLayerTreeLayer, QgsLayerTreeGroup)):
                        continue
                    newGroup.removeChildNode(childNode)
        if groupName != None:
            
            ltModel = define._mLayerTreeView.layerTreeModel()
            rootGroup = ltModel.rootGroup()
            matchesList = ltModel.match(ltModel.index(0, 0), Qt.DisplayRole, groupName)
            if len(matchesList) > 0:
                newGroup = ltModel.index2node(matchesList[0])
                for childNode in newGroup.children():
                    if not isinstance(childNode, (QgsLayerTreeLayer, QgsLayerTreeGroup)):
                        continue
                    nodeName = childNode.layer().name()
                    for layer in layers:
                        if layer.name() == nodeName:
                            newGroup.removeChildNode(childNode)
            else:                
                if groupName == SurfaceTypes.Obstacles:
                    newGroup = rootGroup.insertGroup(0, groupName)
                else:
                    matchesList = ltModel.match(ltModel.index(0, 0), Qt.DisplayRole, SurfaceTypes.DEM)
                    if len(matchesList) > 0:                        
                        newGroup = rootGroup.insertGroup(matchesList[0].row(), groupName)
                    else:
                        newGroup = rootGroup.addGroup(groupName)    
            idx = define._mLayerTreeView.layerTreeModel().node2index(newGroup)
#             define._mLayerTreeView.edit( idx )
            define._mLayerTreeView.setCurrentIndex(idx)
#             define._canvas.setCurrentLayer(newGroup)
        for vectorLayer in layers:
            QgsMapLayerRegistry.instance().addMapLayer(vectorLayer)
            newCanvasLayers.append(QgsMapCanvasLayer(vectorLayer))
#             qgsProject = QgsProject.instance()
#             qgsProject.setSnapSettingsForLayer(vectorLayer.id(), True, QgsSnapper.SnapToVertexAndSegment\
#                                                , QgsTolerance.Pixels, 10, False)
            
        canvas.setLayerSet(newCanvasLayers)

    @staticmethod
    def getSurfaceLayers(groupName):
        if groupName != None:
            sufLayers = []
            ltModel = define._mLayerTreeView.layerTreeModel()
            matchesList = ltModel.match(ltModel.index(0, 0), Qt.DisplayRole, groupName)
            if len(matchesList) > 0:
                newGroup = ltModel.index2node(matchesList[0])
                for childNode in newGroup.children():
                    if childNode.nodeType() == QgsLayerTreeNode.NodeLayer:
                        sufLayers.append(childNode.layer())
                return sufLayers
            else:                
                return None
    
    @staticmethod
    def getIntersectExtent(obstacleLayer, boundGeom, layers):
        extent = QgsRectangle()
        extent.setMinimal()
        
        for layer in layers:
            featureList = layer.getFeatures()
            for feature in featureList:                
                geom = feature.geometry()
                bound = geom.boundingBox()
                xMin = bound.xMinimum()
                xMax = bound.xMaximum()
                yMin = bound.yMinimum()
                yMax = bound.yMaximum()
                if define._canvas.mapUnits() != obstacleLayer.crs().mapUnits():
                      
#                     if obstacleLayer.crs().mapUnits() == QGis.Meters:
                    minPoint = QgisHelper.CrsTransformPoint(xMin, yMin, define._mapCrs, obstacleLayer.crs())
                    maxPoint = QgisHelper.CrsTransformPoint(xMax, yMax, define._mapCrs, obstacleLayer.crs())
                    bound = QgsRectangle(minPoint, maxPoint)
#                     else:
#                         minPoint = QgisHelper.CrsTransformPoint(xMin, yMin, define._mapCrs, obstacleLayer.crs())
#                         maxPoint = QgisHelper.CrsTransformPoint(xMax, yMax, define._mapCrs, obstacleLayer.crs())
#                         bound = QgsRectangle(minPoint, maxPoint)
#                 if define._canvas.mapUnits() == obstacleLayer.crs().mapUnits():
                else:
                    if define._mapCrs != None and define._mapCrs != obstacleLayer.crs():
                        minPoint = QgisHelper.CrsTransformPoint(xMin, yMin, define._mapCrs, obstacleLayer.crs())
                        maxPoint = QgisHelper.CrsTransformPoint(xMax, yMax, define._mapCrs, obstacleLayer.crs())
                        bound = QgsRectangle(minPoint, maxPoint) 
                intersectGeom = boundGeom.intersection(QgsGeometry.fromRect(bound))
                if intersectGeom == None:
                    continue 
                extent.combineExtentWith(intersectGeom.boundingBox())
        if extent.isNull():
            return None
        extent.scale( 1.05 )
        return extent

        

#         unionGeom = None
#         intersectionGeom = None
#         unionPoly = None
#         polygonFlag = False
#         polyLineFlag = False
#         for layer in layers:
#             featureList = layer.getFeatures()
#             for feature in featureList:                
#                 geom = feature.geometry()
#                 if geom.type() == QGis.Polygon:
#                     polygonFlag = True
#                     if unionPoly == None :
#                         unionPoly = geom.asPolygon()
#                         continue
#                     unionPoly.extend(geom.asPolygon())                    
#                 if geom.type() == QGis.Line:
#                     polyLineFlag = True
#                     if unionPoly == None :
#                         unionPoly = geom.asPolyline()
#                         continue
#                     unionPoly.extend(geom.asPolyline())
#         if polyLineFlag:
#             unionGeom = QgsGeometry.fromPolyline(unionPoly)
#         elif polygonFlag:
#             unionGeom = QgsGeometry.fromPolygon(unionPoly)
# #                 unionGeomResult = unionGeom.combine(feature.geometry())
# #                 unionGeom = unionGeomResult
#         intersectionGeom = boundGeom.intersection(unionGeom)
# #         print len(polyLine)
#         if intersectionGeom == None:
#             return None
#         return intersectionGeom.boundingBox()
                
    
    @staticmethod
    def getMultiExtent(layers):
        extent = QgsRectangle()
        extent.setMinimal()
        
        for layer in layers:
            layerExtent = layer.extent()
            if not isinstance(layer , QgsRasterLayer):
                if layer.geometryType() == QGis.NoGeometry:
                    continue
            if layerExtent.isEmpty() and layer.type() == QgsMapLayer.VectorLayer :
                layer.updateExtents()
                layerExtent = layer.extent()
            if ( layerExtent.isNull() ):
                continue
            if define._canvas.hasCrsTransformEnabled() :
                layerExtent = define._canvas.mapSettings().layerExtentToOutputExtent( layer, layerExtent )
            extent.combineExtentWith(layerExtent)
        
        if extent.isNull():
            return None
        extent.scale( 1.05 )
        return extent

    @staticmethod
    def zoomToLayers(layers):
        extent = QgisHelper.getMultiExtent(layers)
        #zoom to bounding box
        if extent == None:
            define._canvas.zoomToFullExtent()
        else:
            define._canvas.setExtent( extent )
        define._canvas.refresh()

    @staticmethod
    def removeFromCanvas(canvas, layers):
        for vectorLayer in layers:
            QgsMapLayerRegistry.instance().removeMapLayer(vectorLayer.id())

    @staticmethod
    def constructPolygon(pointList):
        geometry = QgsGeometry.fromMultiPoint(pointList)
        return geometry.convertToType(QGis.Polygon, False)
    
    @staticmethod
    def offsetCurve(pointList, distance, segment = 0, joinStyle = 0, mitreLimit = 0):
        polyline = QgsGeometry.fromPolyline(pointList)
        curve = polyline.offsetCurve(distance, segment, joinStyle, mitreLimit)
        if curve == None:
            return None
        return curve.asPolyline()
    
    @staticmethod
    def pointInPolygon(point3d, pointList, tolerance = 1.0):
        if define._units != QGis.Meters:
            tolerance /= 111319.49079327358
            
        rect = QgsRectangle(point3d.x() - tolerance, point3d.y() - tolerance, 
                            point3d.x() + tolerance, point3d.y() + tolerance)
        polygon = QgisHelper.constructPolygon(pointList)
        return polygon.intersects(rect)
        
    @staticmethod
    def convertMeasureUnits(unit):
        if define._mapCrs == None or define._mapCrs.mapUnits() == QGis.DecimalDegrees:
            meterCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
        elif define._mapCrs.mapUnits() == QGis.Meters:
            meterCrs = define._mapCrs            
        if define._mapCrs == None or define._mapCrs.mapUnits() == QGis.Meters:
            latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        elif define._mapCrs.mapUnits() == QGis.DecimalDegrees:
            latCrs = define._mapCrs
            
        if unit == QGis.Meters:
            define._qgsDistanceArea.setSourceCrs(meterCrs)
        else:
#             latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
            define._qgsDistanceArea.setSourceCrs(latCrs)

        define._qgsDistanceArea.setEllipsoid(meterCrs.ellipsoidAcronym())
        if unit != QGis.Meters:
            define._qgsDistanceArea.setEllipsoidalMode(True)
        else:
            define._qgsDistanceArea.setEllipsoidalMode(False)

    @staticmethod
    def getFeaturesInPolygon(canvas, vectorLayer, pointList):
        if vectorLayer.crs().mapUnits() != define._units:
            pointList = QgisHelper.Meter2DegreeList(pointList)
        polygon = QgisHelper.constructPolygon(pointList)
        rect = polygon.boundingBox()
        featuresList = []
        fit = vectorLayer.getFeatures( QgsFeatureRequest().setFilterRect( rect ) )
        for feature in fit:
            p = feature.geometry()
            if polygon.intersects(p):
                featuresList.append(feature)
        
        return featuresList
    @staticmethod
    def getFeaturesInSelectedArea(pointLayer, polygonLayers):
        featuresList = []
        for layer in polygonLayers:
            selFeatures = layer.selectedFeatures()
            for selFeature in selFeatures:
                polygon = selFeature.geometry()
                if pointLayer.crs().mapUnits() != layer.crs().mapUnits():
                    if pointLayer.crs().mapUnits() == QGis.Meters:
                        transform = QgisHelper.getDegree2MetersTransform()
                    else:
                        transform = QgisHelper.getMeters2DegreeTransform()
                    polygon.transform(transform)
                
                rect = polygon.boundingBox()
                fit = pointLayer.getFeatures( QgsFeatureRequest().setFilterRect( rect ) )
                for feature in fit:
                    p = feature.geometry()
                    if polygon.intersects(p):
                        featuresList.append(feature)
        
        return featuresList
    @staticmethod
    def getSelectedGeomExtent(surfaceLayers):
        rect = QgsRectangle()
        rect.setMinimal()
        for sfLayer in surfaceLayers:
            features = sfLayer.selectedFeatures()
            for feature in features:
                geom = feature.geometry()
                rect.combineExtentWith(geom.boundingBox())
        return rect
    
#     @staticmethod
#     def getFeaturesInLayerExtentFromRaster(canvas, rasterLayer, surfaceLayers):
#         bound = QgisHelper.getMultiExtent(surfaceLayers)
#         authID = rasterLayer.crs().authid()
#         pointLayer = QgsVectorLayer("Point?crs=" + authID, "memoryPointLayer", "memory")
#         pr = pointLayer.dataProvider()
#         # add fields
#         pr.addAttributes( [ QgsField("Name", QVariant.String),
#         QgsField("Altitude", QVariant.Double) ] )
#         # add a feature
#         block = rasterLayer.dataProvider().block(0,rasterLayer.extent(),rasterLayer.width(),rasterLayer.height())
#         xOffSet = rasterLayer.extent().width() / rasterLayer.width()
#         yOffSet = rasterLayer.extent().height() / rasterLayer.height()
#         xMinimum = rasterLayer.extent().xMinimum() + xOffSet / 2
#         yMaximum = rasterLayer.extent().yMaximum() - yOffSet / 2
#         xPixelWidth = 0.0
#         yPixelWidth = 0.0
#         for i in range(rasterLayer.height()):
#             for j in range(rasterLayer.width()):
#                 altitude = block.value(i, j)
#                 fet = QgsFeature()
#                 fet.setGeometry( QgsGeometry.fromPoint(QgsPoint(xMinimum + xPixelWidth, yMaximum - yPixelWidth)) )
#                 fet.setAttributes(["DEM", altitude])
#                 pr.addFeatures([fet])
#                 xPixelWidth += xOffSet
#             yPixelWidth += yOffSet
#         if define._units != pointLayer.crs().mapUnits():
#             xMin = bound.xMinimum()
#             xMax = bound.xMaximum()
#             yMin = bound.yMinimum()
#             yMax = bound.yMaximum()
#             if pointLayer.crs().mapUnits() == QGis.Meters:
#                 minPoint = QgisHelper.Degree2Meter(xMin, yMin)
#                 maxPoint = QgisHelper.Degree2Meter(xMax, yMax)
#                 bound = QgsRectangle(minPoint, maxPoint)
#             else:
#                 minPoint = QgisHelper.Meter2Degree(xMin, yMin)
#                 maxPoint = QgisHelper.Meter2Degree(xMax, yMax)
#                 bound = QgsRectangle(minPoint, maxPoint)
#         return pointLayer.getFeatures( QgsFeatureRequest().setFilterRect(bound) )

    @staticmethod
    def getFeaturesInLayerExtent(canvas, pointLayer, surfaceLayers, selectionMode = SelectionModeType.Automatic):
        if selectionMode == SelectionModeType.Automatic:
            bound = QgisHelper.getMultiExtent(surfaceLayers)
            xMin = bound.xMinimum()
            xMax = bound.xMaximum()
            yMin = bound.yMinimum()
            yMax = bound.yMaximum()
            if define._units != pointLayer.crs().mapUnits():
                
                if pointLayer.crs().mapUnits() == QGis.Meters:
                    minPoint = QgisHelper.Degree2Meter(xMin, yMin)
                    maxPoint = QgisHelper.Degree2Meter(xMax, yMax)
                    bound = QgsRectangle(minPoint, maxPoint)
                else:
                    minPoint = QgisHelper.Meter2Degree(xMin, yMin)
                    maxPoint = QgisHelper.Meter2Degree(xMax, yMax)
                    bound = QgsRectangle(minPoint, maxPoint)
                    bound.setXMaximum(bound.xMaximum() + 0.01)
                    bound.setXMinimum(bound.xMinimum() - 0.01)
                    bound.setYMaximum(bound.yMaximum() + 0.01)
                    bound.setYMinimum(bound.yMinimum() - 0.01)

                    a = bound.xMaximum()
                    b= bound.xMinimum()
                    c = bound.yMaximum()
                    d= bound.yMinimum()
            if define._canvas.mapUnits() == pointLayer.crs().mapUnits():
                if define._mapCrs != None and define._mapCrs != pointLayer.crs():
                    minPoint = QgisHelper.CrsTransformPoint(xMin, yMin, define._mapCrs, pointLayer.crs())
                    maxPoint = QgisHelper.CrsTransformPoint(xMax, yMax, define._mapCrs, pointLayer.crs())
                    bound = QgsRectangle(minPoint, maxPoint)
            return pointLayer.getFeatures( QgsFeatureRequest().setFilterRect(bound) )
        else:
            selectedFeatures = pointLayer.selectedFeatures()
            if len(selectedFeatures) == 0:
                raise UserWarning, "Please select obstacles!"
            return selectedFeatures
    
    @staticmethod
    def createAction(parent, text, slot=None, shortcut=None, icon=None,\
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, parent)
        if icon is not None:
            action.setIcon(QIcon("Resource/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            parent.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    
    @staticmethod
    def snapPoint(p, snapper, canvas, bNone = False):
        snappingResults = snapper.snapToBackgroundLayers( p ) 
        if ( snappingResults[0] != 0 or len(snappingResults[1]) < 1 ):
            if bNone:
                return None
            else:
                return canvas.getCoordinateTransform().toMapCoordinates( p )
        else:
            return snappingResults[1][0].snappedVertex
    
    @staticmethod
    def transformPoint(X, Y, direction = True):
        meterCrs = None
        latCrs = None
        if define._mapCrs == None :
            meterCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
        elif define._mapCrs.mapUnits() == QGis.Meters:
            meterCrs = define._mapCrs            
            
        if define._mapCrs == None :
            latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        elif define._mapCrs.mapUnits() == QGis.DecimalDegrees:
            latCrs = define._mapCrs
#         latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
#         meterCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)

        if define._canvas.mapUnits() == QGis.DecimalDegrees:
            if direction:
                crsTransform = QgsCoordinateTransform (meterCrs, latCrs)
            else:
                crsTransform = QgsCoordinateTransform (latCrs, meterCrs)
        else:
            if direction:
                crsTransform = QgsCoordinateTransform (latCrs, meterCrs)
            else:
                crsTransform = QgsCoordinateTransform (meterCrs, latCrs)
        
        qgsPoint = crsTransform.transform(X, Y)
        return Point3D(qgsPoint.x(), qgsPoint.y(), 0)
    
    @staticmethod
    def CrsTransformPoint(X, Y, inputCrs, outputCrs, altitude = 0):
        crsTransform = QgsCoordinateTransform (inputCrs, outputCrs)
        qgsPoint = crsTransform.transform(X, Y)
        return Point3D(qgsPoint.x(), qgsPoint.y(), altitude)
    @staticmethod
    def Degree2Meter(X, Y):        
        meterCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
        if define._mapCrs !=None and define._mapCrs.mapUnits() == QGis.DecimalDegrees:
            latCrs = define._mapCrs
        else:
            latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        crsTransform = QgsCoordinateTransform (latCrs, meterCrs)

        qgsPoint = crsTransform.transform(X, Y)
        return Point3D(qgsPoint.x(), qgsPoint.y(), 0)

    @staticmethod
    def Meter2Degree(X, Y):
        if define._mapCrs !=None and define._mapCrs.mapUnits() == QGis.Meters:
            meterCrs = define._mapCrs
        else:
            meterCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
        latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        crsTransform = QgsCoordinateTransform (meterCrs, latCrs)

        qgsPoint = crsTransform.transform(X, Y)
        return Point3D(qgsPoint.x(), qgsPoint.y(), 0)

    @staticmethod
    def Degree2MeterPoint3D(point3d):
        latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        if define._mapCrs !=None and define._mapCrs.mapUnits() == QGis.Meters:
            meterCrs = define._mapCrs
        else:
            meterCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
        crsTransform = QgsCoordinateTransform (latCrs, meterCrs)

        qgsPoint = crsTransform.transform(point3d.x(), point3d.y())
        return Point3D(qgsPoint.x(), qgsPoint.y(), point3d.z())

    @staticmethod
    def Meter2DegreePoint3D(point3d):
        if point3d == None:
            return None
        if define._mapCrs !=None and define._mapCrs.mapUnits() == QGis.DecimalDegrees:
            latCrs = define._mapCrs
        else:
            latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        meterCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
        crsTransform = QgsCoordinateTransform (meterCrs, latCrs)

        qgsPoint = crsTransform.transform(point3d.x(), point3d.y())
        if isinstance(point3d, Point3D):
            return Point3D(qgsPoint.x(), qgsPoint.y(), point3d.z())
        else:
            return qgsPoint

    @staticmethod
    def transformPoints(pointsList, direction = False):
        resultList = []
        for point in pointsList:
            resultList.append(QgisHelper.transformPoint(point.x(), point.y(), direction))
        return resultList

    @staticmethod
    def Degree2MeterList(pointsList):
        resultList = []
        for point in pointsList:
            resultList.append(QgisHelper.Degree2MeterPoint3D(point))
        return resultList

    @staticmethod
    def Meter2DegreeList(pointsList):
        resultList = []
        for point in pointsList:
            resultList.append(QgisHelper.Meter2DegreePoint3D(point))
        return resultList
        
    @staticmethod
    def getDegree2MetersTransform():
        
        if define._mapCrs !=None and define._mapCrs.mapUnits() == QGis.Meters:
            latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
            meterCrs = define._mapCrs
        elif define._mapCrs !=None and define._mapCrs.mapUnits() == QGis.DecimalDegrees:
            latCrs = define._mapCrs
            meterCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
        return QgsCoordinateTransform (latCrs, meterCrs)

    @staticmethod
    def getMeters2DegreeTransform():
        if define._mapCrs !=None and define._mapCrs.mapUnits() == QGis.Meters:
            latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
            meterCrs = define._mapCrs
        elif define._mapCrs !=None and define._mapCrs.mapUnits() == QGis.DecimalDegrees:
            latCrs = define._mapCrs
            meterCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
        return QgsCoordinateTransform (meterCrs, latCrs)
    
    @staticmethod
    def ClearCanvas(mapCanvas):
        graphicsItems = mapCanvas.items()
        scene = mapCanvas.scene()
        for item in graphicsItems:
            item._class_ =  QgsTextAnnotationItem
            if isinstance(item, QgsTextAnnotationItem):
                scene.removeItem( item)
    
    @staticmethod
    def ClearRubberBandInCanvas(mapCanvas, rubberBandList = None):
        graphicsItems = mapCanvas.items()
        scene = mapCanvas.scene()
        if rubberBandList != None:
            for rubberBand in rubberBandList:
                scene.removeItem(rubberBand)
            return
        for item in graphicsItems:
            item._class_ =  QgsRubberBand
            if isinstance(item, QgsRubberBand):
                scene.removeItem( item)
                
    @staticmethod
    def selectFeature(layerId, featureId):
        vlayer = QgsMapLayerRegistry.instance().mapLayer(layerId)
        if isinstance(vlayer, QgsVectorLayer):
            vlayer.removeSelection()
            vlayer.select(featureId)
    @staticmethod
    def getMapPosition(layerId, x, y):
        vlayer = QgsMapLayerRegistry.instance().mapLayer(layerId)
        if define._mapCrs != None:
            return QgisHelper.CrsTransformPoint(x, y, vlayer.crs(), define._mapCrs)
        else:
            return Point3D(x, y)
        
    zoomPointRubber = None

    @staticmethod
    def WPT2Layer(waypoint1, waypoint2):
        mapUnits = define._canvas.mapUnits()
        if define._mapCrs == None:
            if mapUnits == QGis.Meters:
                resultLayer = QgsVectorLayer("Point?crs=EPSG:32633", "WPT", "memory")
            else:
                resultLayer = QgsVectorLayer("Point?crs=EPSG:4326", "WPT", "memory")
        else:
            resultLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), "WPT", "memory")
#         if mapUnits == QGis.Meters:
#             resultLayer = QgsVectorLayer("Point?crs=EPSG:32633", "WPT", "memory")
#         else:
#             resultLayer = QgsVectorLayer("Point?crs=EPSG:4326", "WPT", "memory")
        fieldName = "CATEGORY"
        resultLayer.dataProvider().addAttributes( [QgsField(fieldName, QVariant.String)] )
        resultLayer.startEditing()
        fields = resultLayer.pendingFields()
        i = 1
        feature = QgsFeature()
        feature.setFields(fields)

        feature.setGeometry(QgsGeometry.fromPoint (waypoint1))
        feature.setAttribute(fieldName, "Waypoint1")
        resultLayer.addFeature(feature)
        feature.setGeometry(QgsGeometry.fromPoint (waypoint2))
        feature.setAttribute(fieldName, "Waypoint2")
        resultLayer.addFeature(feature)
        resultLayer.commitChanges()

        '''FlyOver'''
        mawpBearing = MathHelper.getBearing(waypoint1, waypoint2)
        symbolFlyOver = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
        symbolFlyOver.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyover.svg", 10.0, 0.0)
        symbolFlyOver.appendSymbolLayer(svgSymLayer)
        renderCatFlyOver = QgsRendererCategoryV2(1, symbolFlyOver,"Fly over")

        '''FlyBy'''
        symbolFlyBy = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
        symbolFlyBy.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyby.svg", 10.0, 0.0)
        symbolFlyBy.appendSymbolLayer(svgSymLayer)
        renderCatFlyBy = QgsRendererCategoryV2(0, symbolFlyBy,"Fly by")

        symRenderer = QgsCategorizedSymbolRendererV2(Expressions.WPT_EXPRESION, [renderCatFlyOver, renderCatFlyBy])

        resultLayer.setRendererV2(symRenderer)
        return resultLayer
    @staticmethod
    def UnionFromPolylineAreaList(polylineAreaList):
        geom = QgsGeometry()
        geomTemp = QgsGeometry()
#         point3dCollection = []
        i = 0
        for polylineArea in polylineAreaList:
            point3dCollection = polylineArea.method_14_closed()
            
            if i == 0:
                geomTemp = QgsGeometry.fromPolygon([point3dCollection])
            else:
                geom = geomTemp.combine(QgsGeometry.fromPolygon([point3dCollection]))
                geomTemp = geom
#         
            i += 1
#         geomTemp = QgsGeometry.fromPolyline(point3dCollection)    
#         geom = geomTemp.convexHull()
        polygonList= geom.asPolygon()
#         polylineArea = PolylineArea()
#         for point in pointList:
#             polylineArea.Add(PolylineAreaPoint(point))
        return polygonList[0]
    
    @staticmethod
    def zoomExtent(centerPoint, extent, factor = 1):
        if extent.width() > extent.height():
            factor *= extent.width() / define._canvas.extent().width()
        else:
            factor *= extent.height() / define._canvas.extent().height()
        define._canvas.zoomByFactor(factor, centerPoint)
        
        if QgisHelper.zoomPointRubber == None:
            QgisHelper.zoomPointRubber = QgsRubberBand(define._canvas, QGis.Point)
        QgisHelper.zoomPointRubber.reset(QGis.Point)
        QgisHelper.zoomPointRubber.setBorderColor (Qt.green)
        QgisHelper.zoomPointRubber.setFillColor(Qt.yellow)
        QgisHelper.zoomPointRubber.setWidth(2)
        QgisHelper.zoomPointRubber.setIconSize(10)
#         QgisHelper.zoomPointRubber.setSize(30)
        QgisHelper.zoomPointRubber.addPoint(centerPoint)
        QgisHelper.zoomPointRubber.show()
    @staticmethod
    def strDegree(value):
        degree = int(value)
        minute = int((value - degree) * 60)
        second = (value - degree) * 3600 - minute * 60
#         print str(degree) + unicode("°", "utf-8") + str(minute) +"'" + "%.4f"%second +"\""
        return str(degree) + unicode("° ", "utf-8") + str(minute) +"' " + "%.4f"%second +"\""
    
#     @staticmethod
#     def smethod_131(polylineArea_0):
#         polylineAreaPoint = []
# #         Polyline polyline = new Polyline();
#         if (not polylineArea_0.isCircle):
#             for i in range(len(polylineArea_0)):
#                 item = polylineArea_0[i];
#                 x = item.Position.get_X();
#                 position = item.Position;
#                 polyline.AddVertexAt(i, new Point2d(x, position.get_Y()), item.Bulge, 0, 0);
#             }
#         }
#         else
#         {
#             Point3d point3d = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 0, polylineArea_0.Radius);
#             Point3d point3d1 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 1.5707963267949, polylineArea_0.Radius);
#             Point3d point3d2 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 3.14159265358979, polylineArea_0.Radius);
#             Point3d point3d3 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 4.71238898038469, polylineArea_0.Radius);
#             polyline.AddVertexAt(0, new Point2d(point3d.get_X(), point3d.get_Y()), MathHelper.smethod_60(point3d, point3d1, point3d2), 0, 0);
#             polyline.AddVertexAt(1, new Point2d(point3d2.get_X(), point3d2.get_Y()), MathHelper.smethod_60(point3d2, point3d3, point3d), 0, 0);
#             polyline.AddVertexAt(2, new Point2d(point3d.get_X(), point3d.get_Y()), 0, 0, 0);
#         }
#         return polyline;
#     }
#     
#     @staticmethod
#     def smethod_136(polylineArea_0, bool_0):
#         point3dCollection = QgisHelper.smethod_131(polylineArea_0)
#         return point3dCollection
# #         Polyline polyline = AcadHelper.smethod_131(polylineArea_0);
# #         polyline.set_Closed(bool_0);
# #         return polyline;
    @staticmethod
    def smethod_4(geoCalculationType_0, degrees_0, degrees_1, degrees_2, degrees_3):
        num = None;
        num1 = None;
        flag = None;
        distance_0 = Distance.NaN();
        double_0 = None;
        double_1 = None;
        try:
            if (geoCalculationType_0 != GeoCalculationType.Ellipsoid):
                num1, double_0, double_1 = QgisHelper.smethod_10(degrees_0, degrees_1, degrees_2, degrees_3);
                distance_0 = Distance(num1, DistanceUnits.KM);
                flag = True;
            else:
                num, double_0, double_1 = QgisHelper.smethod_9(degrees_0, degrees_1, degrees_2, degrees_3);
                distance_0 = Distance(num, DistanceUnits.KM);
                flag = True;
        except:
            flag = False
#         catch (Exception exception1)
#         {
#             Exception exception = exception1;
#             Geo.lastError = string.Format(Messages.ERR_GEO_CALCULATION_PREFIX, exception.Message);
#             flag = false;
#         }
        return (flag, distance_0, double_0, double_1);
    
    @staticmethod
    def smethod_9(degrees_0, degrees_1, degrees_2, degrees_3):
        num = None;
        num1 = None;
        num2 = None;
        num3 = None;
        num4 = None;
        num5 = None;
        num6 = None;
        num7 = None;
        num8 = None;
        num9 = None;
#         if (Geo.defaultDatum == null)
#         {
#             throw new Exception(Messages.ERR_GEO_NO_DATUM_LOADED);
#         }
#         if (math.faAbs(degrees_0.value) >= 89.99999999 or math.fabs(degrees_2.value) >= 89.99999999):
#             throw new Exception(Messages.ERR_GEO_LATITUDE_OUT_OF_RANGE);
#         }
#         if (math.fabs(degrees_1.Value) >= 180 || math.fabs(degrees_3.Value) >= 180)
#         {
#             throw new Exception(Messages.ERR_GEO_LONGITUDE_OUT_OF_RANGE);
#         }
#         if (degrees_0 == degrees_2 && degrees_1 == degrees_3)
#         {
#             throw new Exception(Messages.ERR_POSITIONS_CANNOT_BE_EQUAL);
#         }
        num10 = Unit.ConvertDegToRad(degrees_0.value);
        num11 = Unit.ConvertDegToRad(degrees_1.value);
        num12 = Unit.ConvertDegToRad(degrees_2.value);
        num13 = Unit.ConvertDegToRad(degrees_3.value);
        semiMajorAxis = 6378293.645208759 ;
        eccentricity = 6356617.987679838 / 6378293.645208759
        num14 = math.sqrt(semiMajorAxis * semiMajorAxis - semiMajorAxis * semiMajorAxis * (eccentricity * eccentricity));
        num15 = (semiMajorAxis - num14) / semiMajorAxis;
        num16 = 1 - num15;
        num17 = num16 * math.sin(num10) / math.cos(num10);
        num18 = num16 * math.sin(num12) / math.cos(num12);
        num19 = 1 / math.sqrt(num17 * num17 + 1);
        num20 = num19 * num17;
        num21 = 1 / math.sqrt(num18 * num18 + 1);
        num22 = num19 * num21;
        num23 = num22 * num18;
        num24 = num23 * num17;
        num25 = num13 - num11;
        
        num = math.sin(num25);
        num1 = math.cos(num25);
        num17 = num21 * num;
        num18 = num23 - num20 * num21 * num1;
        num2 = math.sqrt(num17 * num17 + num18 * num18);
        num3 = num22 * num1 + num24;
        num4 = math.atan2(num2, num3);
        num26 = num22 * num / num2;
        num5 = -num26 * num26 + 1;
        num6 = num24 + num24;
        if (num5 > 0):
            num6 = -num6 / num5 + num3;
        num7 = num6 * num6 * 2 - 1;
        num8 = ((-3 * num5 + 4) * num15 + 4) * num5 * num15 / 16;
        num9 = num25;
        num25 = ((num7 * num3 * num8 + num6) * num2 * num8 + num4) * num26;
        num25 = (1 - num8) * num25 * num15 + num13 - num11;
        
        while (math.fabs(num9 - num25) > 5E-14):
            num = math.sin(num25);
            num1 = math.cos(num25);
            num17 = num21 * num;
            num18 = num23 - num20 * num21 * num1;
            num2 = math.sqrt(num17 * num17 + num18 * num18);
            num3 = num22 * num1 + num24;
            num4 = math.atan2(num2, num3);
            num26 = num22 * num / num2;
            num5 = -num26 * num26 + 1;
            num6 = num24 + num24;
            if (num5 > 0):
                num6 = -num6 / num5 + num3;
            num7 = num6 * num6 * 2 - 1;
            num8 = ((-3 * num5 + 4) * num15 + 4) * num5 * num15 / 16;
            num9 = num25;
            num25 = ((num7 * num3 * num8 + num6) * num2 * num8 + num4) * num26;
            num25 = (1 - num8) * num25 * num15 + num13 - num11;
        num24 = math.atan2(num17, num18);
        num23 = math.atan2(num19 * num, num23 * num1 - num20 * num21) + 3.14159265358979;
        num25 = math.sqrt((1 / num16 / num16 - 1) * num5 + 1) + 1;
        num25 = (num25 - 2) / num25;
        num8 = 1 - num25;
        num8 = (num25 * num25 / 4 + 1) / num8;
        num9 = (0.375 * num25 * num25 - 1) * num25;
        num25 = num7 * num3;
        num22 = 1 - num7 - num7;
        num22 = ((((num2 * num2 * 4 - 3) * num22 * num6 * num9 / 6 - num25) * num9 / 4 + num6) * num2 * num9 + num4) * num8 * semiMajorAxis * num16;
        double_0 = num22 / 1000;
        double_1 = Unit.smethod_1(MathHelper.smethod_4(num24));
        double_2 = Unit.smethod_1(MathHelper.smethod_4(num23));
        return (double_0, double_1, double_2)
    @staticmethod
    def smethod_10(degrees_0, degrees_1, degrees_2, degrees_3):
        value = degrees_0.value;
        num = degrees_1.value;
        value1 = degrees_2.value;
        num1 = degrees_3.value;
#         if (math.fabs(value) >= 89.99999999 || math.fabs(value1) >= 89.99999999)
#         {
#             throw new Exception(Messages.ERR_GEO_LATITUDE_OUT_OF_RANGE);
#         }
#         if (math.fabs(num) >= 180 || math.fabs(num1) >= 180)
#         {
#             throw new Exception(Messages.ERR_GEO_LONGITUDE_OUT_OF_RANGE);
#         }
#         if (degrees_0 == degrees_2 && degrees_1 == degrees_3)
#         {
#             throw new Exception(Messages.ERR_POSITIONS_CANNOT_BE_EQUAL);
#         }
        num2 = MathHelper.smethod_2(Unit.ConvertDegToRad(num1 - num));
        num3 = Unit.ConvertDegToRad((value1 - value) / 2);
        num4 = Unit.ConvertDegToRad((value1 + value) / 2);
        num5 = math.tan(num2 / 2);
        num6 = math.atan(math.cos(num4) / MathHelper.smethod_2(math.sin(num3)) * num5);
        num7 = math.atan(math.sin(num4) / MathHelper.smethod_2(math.cos(num3)) * num5);
        num8 = num6 - num7;
        num9 = num6 + num7;
        double_0 = math.fabs(math.acos(math.sin(Unit.ConvertDegToRad(value)) * math.sin(Unit.ConvertDegToRad(value1)) + math.cos(Unit.ConvertDegToRad(value)) * math.cos(Unit.ConvertDegToRad(value1)) * math.cos(num2)) * 6400000) / 1000;
        if (value1 - value < 0 and num1 - num < 0):
            double_1 = Unit.smethod_1(num8 + 3.14159265358979);
            double_2 = Unit.smethod_1(num9);
        elif (value1 - value < 0 and num1 - num >= 0):
            double_1 = Unit.smethod_1(num8 + 3.14159265358979);
            double_2 = Unit.smethod_1(num9 + 6.28318530717959);
        elif (value1 - value < 0 or num1 - num >= 0):
            double_1 = Unit.smethod_1(num8);
            double_2 = Unit.smethod_1(num9 + 3.14159265358979);
        else:
            double_1 = Unit.smethod_1(num8 + 6.28318530717959);
            double_2 = Unit.smethod_1(num9 + 3.14159265358979);
        double_1 = MathHelper.smethod_3(double_1);
        double_2 = MathHelper.smethod_3(double_2);
        return(double_0, double_1, double_2)
    @staticmethod
    def smethod_146(point3dCollection_0, point3dCollection_1):
        return QgisHelper.smethod_151(point3dCollection_0, point3dCollection_1, None, -1, True);
    
    @staticmethod
    def smethod_147(point3dCollection_0, point3dCollection_1):
        return QgisHelper.smethod_151(point3dCollection_0, point3dCollection_1, None, -1, True);
#         {
#             return AcadHelper.smethod_151(transaction_0, blockTableRecord_0, point3dCollection_0, point3dCollection_1, string_0, -1, true);
    
    @staticmethod
    def smethod_151(point3dCollection_0, point3dCollection_1, string_0, int_0, bool_0):
        if (bool_0):
            Point3dCollection.smethod_147(point3dCollection_0, True);
            Point3dCollection.smethod_147(point3dCollection_1, True);
        if (len(point3dCollection_0) != len(point3dCollection_1)):
            raise  ValueError(Messages.ERR_NUMBER_OF_VERTICES_MUST_BE_EQUAL)
            return None
        count = len(point3dCollection_0)
        if (count < 2):
            raise  ValueError(Messages.ERR_INSUFFICIENT_NUMBER_OF_VERTICES)
            return None
        return (QgsGeometry.fromPolygon([point3dCollection_0]), QgsGeometry.fromPolygon([point3dCollection_1]))
#         PolygonMesh polygonMesh = new PolygonMesh();
#         polygonMesh.set_PolyMeshType(0);
#         polygonMesh.set_MSize((short)count);
#         polygonMesh.set_NSize(2);
#         polygonMesh.SetDatabaseDefaults();
#         if (!string.IsNullOrEmpty(string_0))
#         {
#             polygonMesh.set_Layer(string_0);
#         }
#         if (int_0 >= 0)
#         {
#             polygonMesh.set_ColorIndex(int_0);
#         }
#         ObjectId objectId = blockTableRecord_0.AppendEntity(polygonMesh);
#         transaction_0.AddNewlyCreatedDBObject(polygonMesh, true);
#         point3dCollection = []
#         for i in range(count):
#             point3dCollection.append(point3dCollection_0[i])
#             point3dCollection.append(point3dCollection_1[i])
#             PolygonMeshVertex polygonMeshVertex = new PolygonMeshVertex(point3dCollection_0.get_Item(i));
#             polygonMeshVertex.SetDatabaseDefaults();
#             if (!string.IsNullOrEmpty(string_0))
#             {
#                 polygonMeshVertex.set_Layer(string_0);
#             }
#             if (int_0 >= 0)
#             {
#                 polygonMeshVertex.set_ColorIndex(int_0);
#             }
#             polygonMesh.AppendVertex(polygonMeshVertex);
#             transaction_0.AddNewlyCreatedDBObject(polygonMeshVertex, true);
#             polygonMeshVertex = new PolygonMeshVertex(point3dCollection_1.get_Item(i));
#             polygonMeshVertex.SetDatabaseDefaults();
#             if (!string.IsNullOrEmpty(string_0))
#             {
#                 polygonMeshVertex.set_Layer(string_0);
#             }
#             if (int_0 >= 0)
#             {
#                 polygonMeshVertex.set_ColorIndex(int_0);
#             }
#             polygonMesh.AppendVertex(polygonMeshVertex);
#             transaction_0.AddNewlyCreatedDBObject(polygonMeshVertex, true);
#         }
#         return point3dCollection;