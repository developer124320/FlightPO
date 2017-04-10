# -*- coding: UTF-8 -*-
from qgis.core import QgsVectorFileWriter ,QgsRasterLayer,  QgsMapLayerRegistry, QgsFeature, QgsPoint\
    ,QgsFeatureRequest, QGis, QgsProject, QgsSnapper, QgsTolerance, QgsCoordinateTransform, \
    QgsCoordinateReferenceSystem, QgsRectangle, QgsMapLayer, QgsLayerTreeNode, \
    QgsLayerTreeLayer, QgsLayerTreeGroup, QgsField, QgsSymbolV2, QgsSvgMarkerSymbolLayerV2, \
    QgsRendererCategoryV2, QgsCategorizedSymbolRendererV2
from qgis.gui import QgsMapCanvasLayer, QgsTextAnnotationItem,QgsRubberBand
from qgis.core import QgsGeometry, QgsPalLayerSettings
from PyQt4.QtGui import QAction, QIcon, QMessageBox
from PyQt4.QtCore import *
from PyQt4.QtGui import QColor, QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QDialog, QSpinBox, QFrame, QHBoxLayout
from qgis.gui import QgsTextAnnotationItem, QgsAnnotationItem, QgsRubberBand
from qgis.core import QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, \
    QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2, QgsPluginLayer

from FlightPlanner.types import Point3D, SurfaceTypes, SelectionModeType, DegreesType,\
                                GeoCalculationType, DistanceUnits, MagneticModel
from FlightPlanner.expressions import Expressions
from FlightPlanner.messages import Messages
from FlightPlanner.helpers import MathHelper, Distance, Unit
# from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from Type.Degrees import Degrees
import define, math


#from qgis.gui import *
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *

class AerodromeAndRwyCmb:
    currentLayer = None
    aerodromeCmbObj = None
    aerodromePositionPanelObj = None
    rwyDirCmbObj = None
    rwyStartPositionPanel = None
    rwyEndPositionPanel = None
    rwyFeatureArray = []
    arpFeatureArray = []
    def __init__(self):
        pass
    @staticmethod
    def aerodromeAndRwyCmbFill(layer, aerodromeCmbObj, aerodromePositionPanelObj, rwyDirCmbObj = None, rwyStartPositionPanel = None, rwyEndPositionPanel = None):
        AerodromeAndRwyCmb.currentLayer = layer
        AerodromeAndRwyCmb.aerodromePositionPanelObj = aerodromePositionPanelObj
        AerodromeAndRwyCmb.aerodromeCmbObj = aerodromeCmbObj
        AerodromeAndRwyCmb.rwyDirCmbObj = rwyDirCmbObj
        AerodromeAndRwyCmb.rwyStartPositionPanel = rwyStartPositionPanel
        AerodromeAndRwyCmb.rwyEndPositionPanel = rwyEndPositionPanel

        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')
        arpList = []
        arpFeatureList = []
        if idx >= 0:
            featIter = layer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idx].toString()
                attrValue = QString(attrValue)
                attrValue = attrValue.replace(" ", "")
                attrValue = attrValue.toUpper()
                if attrValue == "AERODROMEREFERENCEPOINT":
                    arpList.append(attrValue)
                    arpFeatureList.append(feat)
            if len(arpList) != 0:

                i = -1
                for feat in arpFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    items = aerodromeCmbObj.Items
                    if len(items) != 0:
                        existFlag = False
                        for item in items:
                            if item == attrValue:
                                existFlag = True
                        if existFlag:
                            continue
                    aerodromeCmbObj.Add(attrValue)
                aerodromeCmbObj.SelectedIndex = 0

                # if idxAttributes
                for feat in arpFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    if attrValue != aerodromeCmbObj.SelectedItem:
                        continue
                    attrValue = feat.attributes()[idxLat].toDouble()
                    lat = attrValue[0]

                    attrValue = feat.attributes()[idxLong].toDouble()
                    long = attrValue[0]

                    attrValue = feat.attributes()[idxAltitude].toDouble()
                    alt = attrValue[0]

                    aerodromePositionPanelObj.Point3d = Point3D(long, lat, alt)
                    QObject.connect(AerodromeAndRwyCmb.aerodromeCmbObj, SIGNAL("Event_0"), AerodromeAndRwyCmb.aerodromeCmbObj_Event_0)
                    break
            if rwyDirCmbObj != None:
                idxAttr = layer.fieldNameIndex('Attributes')
                if idxAttr >= 0:
                    rwyFeatList = []
                    featIter = layer.getFeatures()
                    for feat in featIter:
                        attrValue = feat.attributes()[idxAttr].toString()
                        if attrValue == aerodromeCmbObj.SelectedItem:
                            attrValue = feat.attributes()[idxName].toString()
                            s = attrValue.replace(" ", "")
                            compStr = s.left(6).toUpper()
                            if compStr == "THRRWY":
                                valStr = s.right(s.length() - 6)
                                rwyDirCmbObj.Add(aerodromeCmbObj.SelectedItem + " RWY " + valStr)
                                rwyFeatList.append(feat)
                    QObject.connect(AerodromeAndRwyCmb.rwyDirCmbObj, SIGNAL("Event_0"), AerodromeAndRwyCmb.rwyDirCmbObj_Event_0)
                    AerodromeAndRwyCmb.rwyFeatureArray = rwyFeatList

                    items = rwyDirCmbObj.Items
                    if len(items) != 0:
                        rwyDirCmbObj.SelectedIndex = 0
                        for feat in rwyFeatList:
                            attrValue = feat.attributes()[idxName].toString()
                            if attrValue != rwyDirCmbObj.SelectedItem:
                                continue
                            latAttrValue = feat.attributes()[idxLat].toDouble()
                            lat = latAttrValue[0]

                            longAttrValue = feat.attributes()[idxLong].toDouble()
                            long = longAttrValue[0]

                            altAttrValue = feat.attributes()[idxAltitude].toDouble()
                            alt = altAttrValue[0]

                            AerodromeAndRwyCmb.rwyStartPositionPanel.Point3d = Point3D(long, lat, alt)

                            valStr = None
                            if attrValue.right(1).toUpper() =="L" or attrValue.right(1).toUpper() =="R":
                                s = attrValue.right(attrValue.length() - 1)
                                valStr = s.right(2)
                            else:
                                valStr = attrValue.right(2)
                            val = int(valStr)
                            val += 18
                            if val > 36:
                                val -= 36
                            newValStr = None
                            if len(str(val)) == 1:
                                newValStr = "0" + str(val)
                            else:
                                newValStr = str(val)
                            otherAttrValue = attrValue.replace(valStr, newValStr)
                            for feat in rwyFeatList:
                                attrValue = feat.attributes()[idxName].toString()
                                if attrValue != otherAttrValue:
                                    continue
                                latAttrValue = feat.attributes()[idxLat].toDouble()
                                lat = latAttrValue[0]

                                longAttrValue = feat.attributes()[idxLong].toDouble()
                                long = longAttrValue[0]

                                altAttrValue = feat.attributes()[idxAltitude].toDouble()
                                alt = altAttrValue[0]

                                AerodromeAndRwyCmb.rwyEndPositionPanel.Point3d = Point3D(long, lat, alt)
                                break
                            break

                    # if len(rwyFeatList) != 0:
                    #     for feat in rwyFeatList:







        AerodromeAndRwyCmb.arpFeatureArray = arpFeatureList
    @staticmethod
    def rwyDirCmbObj_Event_0(index):
        if len(AerodromeAndRwyCmb.rwyFeatureArray) == 0:
            return
        idxName = AerodromeAndRwyCmb.currentLayer.fieldNameIndex('Name')
        idxLat = AerodromeAndRwyCmb.currentLayer.fieldNameIndex('Latitude')
        idxLong = AerodromeAndRwyCmb.currentLayer.fieldNameIndex('Longitude')
        idxAltitude = AerodromeAndRwyCmb.currentLayer.fieldNameIndex('Altitude')
        idxAttr = AerodromeAndRwyCmb.currentLayer.fieldNameIndex('Attributes')
        # rwyFeatList = []
        featIter = AerodromeAndRwyCmb.currentLayer.getFeatures()
        # for feat in featIter:
        #     attrValue = feat.attributes()[idxAttr].toString()
        #     if attrValue == AerodromeAndRwyCmb.cmbAerodrome.SelectedItem:
        #         attrValue = feat.attributes()[idxName].toString()
        #         s = attrValue.replace(" ", "")
        #         compStr = s.left(6).toUpper()
        #         if compStr == "THRRWY":
        #             valStr = s.right(s.length() - 6)
        #             rwyFeatList.append(feat)
        for feat in AerodromeAndRwyCmb.rwyFeatureArray:
            attrValue = feat.attributes()[idxName].toString()
            attrValueStr = QString(attrValue)
            attrValueStr = attrValueStr.replace(" ", "").right(attrValueStr.length() - 3)
            itemStr = AerodromeAndRwyCmb.rwyDirCmbObj.SelectedItem
            itemStr = QString(itemStr)
            itemStr = itemStr.replace(" ", "").right(itemStr.length() - 4)
            if attrValueStr != itemStr:
                continue
            latAttrValue = feat.attributes()[idxLat].toDouble()
            lat = latAttrValue[0]

            longAttrValue = feat.attributes()[idxLong].toDouble()
            long = longAttrValue[0]

            altAttrValue = feat.attributes()[idxAltitude].toDouble()
            alt = altAttrValue[0]

            AerodromeAndRwyCmb.rwyStartPositionPanel.Point3d = Point3D(long, lat, alt)

            valStr = None
            if attrValue.right(1).toUpper() =="L" or attrValue.right(1).toUpper() =="R":
                s = attrValue.left(attrValue.length() - 1)
                valStr = s.right(2)
            else:
                valStr = attrValue.right(2)
            val = int(valStr)
            val += 18
            if val > 36:
                val -= 36
            newValStr = None
            if len(str(val)) == 1:
                newValStr = "0" + str(val)
            else:
                newValStr = str(val)
            otherAttrValue = attrValue.replace(valStr, newValStr)
            for feat in AerodromeAndRwyCmb.rwyFeatureArray:
                attrValue = feat.attributes()[idxName].toString()
                if attrValue != otherAttrValue:
                    continue
                latAttrValue = feat.attributes()[idxLat].toDouble()
                lat = latAttrValue[0]

                longAttrValue = feat.attributes()[idxLong].toDouble()
                long = longAttrValue[0]

                altAttrValue = feat.attributes()[idxAltitude].toDouble()
                alt = altAttrValue[0]

                AerodromeAndRwyCmb.rwyEndPositionPanel.Point3d = Point3D(long, lat, alt)
                break
            break
    @staticmethod
    def aerodromeCmbObj_Event_0(index):
        if len(AerodromeAndRwyCmb.arpFeatureArray) == 0:
            return
        AerodromeAndRwyCmb.aerodromePositionPanelObj.Point3d = None
        AerodromeAndRwyCmb.rwyStartPositionPanel.Point3d = None
        AerodromeAndRwyCmb.rwyEndPositionPanel.Point3d = None
        idxName = AerodromeAndRwyCmb.currentLayer.fieldNameIndex('Name')
        idxLat = AerodromeAndRwyCmb.currentLayer.fieldNameIndex('Latitude')
        idxLong = AerodromeAndRwyCmb.currentLayer.fieldNameIndex('Longitude')
        idxAltitude = AerodromeAndRwyCmb.currentLayer.fieldNameIndex('Altitude')
        AerodromeAndRwyCmb.rwyFeatureArray = []
        # if idxAttributes
        for feat in AerodromeAndRwyCmb.arpFeatureArray:
            attrValue = feat.attributes()[idxName].toString()
            if attrValue != AerodromeAndRwyCmb.aerodromeCmbObj.SelectedItem:
                continue
            attrValue = feat.attributes()[idxLat].toDouble()
            lat = attrValue[0]

            attrValue = feat.attributes()[idxLong].toDouble()
            long = attrValue[0]

            attrValue = feat.attributes()[idxAltitude].toDouble()
            alt = attrValue[0]

            AerodromeAndRwyCmb.aerodromePositionPanelObj.Point3d = Point3D(long, lat, alt)
            break
        idxAttr = AerodromeAndRwyCmb.currentLayer.fieldNameIndex('Attributes')
        if idxAttr >= 0:
            AerodromeAndRwyCmb.rwyDirCmbObj.Clear()
            rwyFeatList = []
            featIter = AerodromeAndRwyCmb.currentLayer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idxAttr].toString()
                if attrValue == AerodromeAndRwyCmb.aerodromePositionPanelObj.SelectedItem:
                    attrValue = feat.attributes()[idxName].toString()
                    s = attrValue.replace(" ", "")
                    compStr = s.left(6).toUpper()
                    if compStr == "THRRWY":
                        valStr = s.right(s.length() - 6)
                        AerodromeAndRwyCmb.rwyDirCmbObj.Add(AerodromeAndRwyCmb.aerodromePositionPanelObj.SelectedItem + " RWY " + valStr)
                        rwyFeatList.append(feat)
                        AerodromeAndRwyCmb.rwyFeatureArray = rwyFeatList
            AerodromeAndRwyCmb.rwyDirCmbObj_Event_0()

class QgisHelper:
    def __init__(self):
        pass
    @staticmethod
    def matchingDialogSize(dlg, w, h):
        if not isinstance(dlg, QDialog):
            return
        # dlg.resize(w, h)
        newWidth = int(define._appWidth / float(1280) * w)
        newHeight = int(define._appHeight / float(800) * h)
        # if newWidth > w:
        #     newWidth -= 50
        # if newHeight > h:
        #     newHeight -= 50
        dlg.resize(newWidth, newHeight)

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
                        # model = define._mLayerTreeView.layerTreeModel()
                        index = layerTreeModel.node2index(qgsLayerTreeNode)
                        layerTreeModel.setCurrentIndex(index)
                        print index.row()
                        parntNode.removeChildren(index.row(), 1)
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
    def createPolylineLayer(layerName, featureData, fields = []):
        mapUnits = define._canvas.mapUnits()
        if define._mapCrs == None:
            if mapUnits == QGis.Meters:
                resultLayer = QgsVectorLayer("linestring?crs=EPSG:32633", layerName, "memory")
            else:
                resultLayer = QgsVectorLayer("linestring?crs=EPSG:4326", layerName, "memory")
        else:
            resultLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), layerName, "memory")

        shpPath = ""
        if define.obstaclePath != None:
            shpPath = define.obstaclePath
        elif define.xmlPath != None:
            shpPath = define.xmlPath
        else:
            shpPath = define.appPath
        layerName = layerName.replace(" ", "_")
        layerName = layerName.replace("(", "_")
        layerName = layerName.replace(")", "_")

        er = QgsVectorFileWriter.writeAsVectorFormat(resultLayer, shpPath + "/" + QString(layerName).replace(" ", "") + ".shp", "utf-8", resultLayer.crs())
        resultLayer = QgsVectorLayer(shpPath + "/" + QString(layerName).replace(" ", "") + ".shp", layerName, "ogr")

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
            pr = resultLayer.dataProvider()
            pr.addFeatures([feature])
            # resultLayer.addFeature(feature)
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

        shpPath = ""
        if define.obstaclePath != None:
            shpPath = define.obstaclePath
        elif define.xmlPath != None:
            shpPath = define.xmlPath
        else:
            shpPath = define.appPath
        er = QgsVectorFileWriter.writeAsVectorFormat(resultLayer, shpPath + "/" + "result" + ".shp", "utf-8", resultLayer.crs())
        resultLayer = QgsVectorLayer(shpPath + "/" + "result" + ".shp", "result", "ogr")


        QgsMapLayerRegistry.instance().addMapLayer(resultLayer)
#         print resultLayer
        feature = QgsFeature()
        feature.setGeometry( QgsGeometry.fromPolyline(pointArray) )
        resultLayer.startEditing()
        pr = resultLayer.dataProvider()
        pr.addFeatures([feature])
        # resultLayer.addFeature(feature)
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
        pr = resultLayer.dataProvider()
        pr.addFeatures([feature])
        # resultLayer.addFeature(feature)
        resultLayer.commitChanges()
        return resultLayer

    @staticmethod
    def appendToCanvas(canvas, layers, groupNameList = None, groupRemove = False):

        groupName = ""
        subGroupName = None
        if groupNameList != None:
            if isinstance(groupNameList, list):
                groupName = groupNameList[0]
                if len(groupNameList) > 1:
                    subGroupName = groupNameList[1]
            else:
                groupName = groupNameList

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
                if subGroupName == None:
                    # newGroup.removeAllChildren()
                    for childNode in newGroup.children():
                        if not isinstance(childNode, (QgsLayerTreeLayer, QgsLayerTreeGroup)):
                            continue
                        if isinstance(childNode, QgsLayerTreeGroup):
                            for childNode0 in childNode.children():
                                if not isinstance(childNode0, QgsLayerTreeLayer):
                                    continue
                                nodeName = childNode0.layer().name()
                                for layer in layers:
                                    if layer.name() == nodeName:
                                        newGroup.removeChildNode(childNode0)
                        else:
                            nodeName = childNode.layer().name()
                            for layer in layers:
                                if layer.name() == nodeName:
                                    newGroup.removeChildNode(childNode)
                else:
                    subGroup = newGroup.findGroup(subGroupName)
                    newGroup.removeChildNode(subGroup)
            else:                
                if groupName == SurfaceTypes.Obstacles:
                    newGroup = rootGroup.insertGroup(0, groupName)
                else:
                    matchesList = ltModel.match(ltModel.index(0, 0), Qt.DisplayRole, SurfaceTypes.DEM)
                    if len(matchesList) > 0:                        
                        newGroup = rootGroup.insertGroup(matchesList[0].row(), groupName)
                    else:
                        newGroup = rootGroup.addGroup(groupName)
            if subGroupName != None:
                newSubGroup = newGroup.addGroup(subGroupName)
                idx = define._mLayerTreeView.layerTreeModel().node2index(newSubGroup)
            else:
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
    def getSurfaceLayers(groupName, subGroupNames = []):
        if groupName != None:
            sufLayers = []
            ltModel = define._mLayerTreeView.layerTreeModel()
            matchesList = ltModel.match(ltModel.index(0, 0), Qt.DisplayRole, groupName)
            if len(matchesList) > 0:
                newGroup = ltModel.index2node(matchesList[0])
                if len(subGroupNames) > 0:
                    i = 0
                    tempGroup = newGroup
                    while i < len(subGroupNames):
                        tempGroup = tempGroup.findGroup(subGroupNames[i])
                        i += 1
                    newGroup = tempGroup

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

        vectorExtent = None
        i = 0
        for layer in layers:
            if i == 0:
                vectorExtent = layer.extent()
                i += 1
                continue
            vectorExtent.combineExtentWith(layer.extent())
            i += 1
        vGeom = QgsGeometry.fromRect(vectorExtent)
        rGeom = QgsGeometry.fromRect(obstacleLayer.extent())
        resultGeom = None
        if vGeom.intersects(rGeom):
            resultGeom = vGeom.intersection(rGeom)
        if resultGeom != None:
            resultExtent = resultGeom.boundingBox()
            return resultExtent
        else:
            return None
#         for layer in layers:
#             featureList = layer.getFeatures()
#             for feature in featureList:
#                 geom = feature.geometry()
#                 bound = geom.boundingBox()
#                 xMin = bound.xMinimum()
#                 xMax = bound.xMaximum()
#                 yMin = bound.yMinimum()
#                 yMax = bound.yMaximum()
#                 if define._canvas.mapUnits() != obstacleLayer.crs().mapUnits():
#
# #                     if obstacleLayer.crs().mapUnits() == QGis.Meters:
#                     minPoint = QgisHelper.CrsTransformPoint(xMin, yMin, define._mapCrs, obstacleLayer.crs())
#                     maxPoint = QgisHelper.CrsTransformPoint(xMax, yMax, define._mapCrs, obstacleLayer.crs())
#                     bound = QgsRectangle(minPoint, maxPoint)
# #                     else:
# #                         minPoint = QgisHelper.CrsTransformPoint(xMin, yMin, define._mapCrs, obstacleLayer.crs())
# #                         maxPoint = QgisHelper.CrsTransformPoint(xMax, yMax, define._mapCrs, obstacleLayer.crs())
# #                         bound = QgsRectangle(minPoint, maxPoint)
# #                 if define._canvas.mapUnits() == obstacleLayer.crs().mapUnits():
#                 else:
#                     if define._mapCrs != None and define._mapCrs != obstacleLayer.crs():
#                         minPoint = QgisHelper.CrsTransformPoint(xMin, yMin, define._mapCrs, obstacleLayer.crs())
#                         maxPoint = QgisHelper.CrsTransformPoint(xMax, yMax, define._mapCrs, obstacleLayer.crs())
#                         bound = QgsRectangle(minPoint, maxPoint)
#                 intersectGeom = boundGeom.intersection(QgsGeometry.fromRect(bound))
#                 if intersectGeom == None:
#                     continue
#                 extent.combineExtentWith(intersectGeom.boundingBox())
#         if extent.isNull():
#             return None
#         extent.scale( 1.05 )
#         return resultExtent

        

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
        layer = define._canvas.currentLayer()
        if isinstance(layer, QgsPluginLayer):
            return layer.extent()
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
    def Reverse_Point(ipCp, alpha, SrcPoint):
        talpha = 2 * alpha - MathHelper.getBearing(ipCp, SrcPoint);
        d = MathHelper.calcDistance(ipCp, SrcPoint);
        tagetPoint = MathHelper.distanceBearingPointArcGIS(ipCp, talpha, d);
        return tagetPoint;
    # @staticmethod
    # def Reverse_Point(ipCp, alpha, SrcPoint):
    #     talpha = 2 * alpha - MathHelper.getBearing(ipCp, SrcPoint);
    #     d = MathHelper.calcDistance(ipCp, SrcPoint);
    #     tagetPoint = MathHelper.distanceBearingPointArcGIS(ipCp, talpha, d);
    #     return tagetPoint;
    @staticmethod
    def Rotate_Point(ipCp, alpha, SrcPoint, flag = "QGIS"):
        d = MathHelper.calcDistance(ipCp, SrcPoint);
        delta = MathHelper.getBearing(ipCp, SrcPoint);
        if flag != "QGIS":
            return MathHelper.distanceBearingPointArcGIS(ipCp, alpha + delta, d);
        tagPoint = MathHelper.distanceBearingPoint(ipCp, alpha + delta, d);
        return tagPoint;
    @staticmethod
    def offsetCurve(pointList, distance, segment = 0, joinStyle = 0, mitreLimit = 0):
        if define._units != QGis.Meters:
            distance = define._qgsDistanceArea.convertMeasurement(distance, QGis.Meters, QGis.Degrees, False)[0]
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
        # if define._mapCrs == None or define._mapCrs.mapUnits() == QGis.DecimalDegrees:
        #     meterCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
        # elif define._mapCrs.mapUnits() == QGis.Meters:
        #     meterCrs = define._mapCrs
        # if define._mapCrs == None or define._mapCrs.mapUnits() == QGis.Meters:
        #     latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        # elif define._mapCrs.mapUnits() == QGis.DecimalDegrees:
        #     latCrs = define._mapCrs
            
        if unit == QGis.Meters:
            define._qgsDistanceArea.setSourceCrs(define._xyCrs)
        else:
#             latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
            define._qgsDistanceArea.setSourceCrs(define._latLonCrs)

        define._qgsDistanceArea.setEllipsoid(define._xyCrs.ellipsoidAcronym())
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
        meterCrs = define._xyCrs
        latCrs = define._latLonCrs
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
            rubberBandList = []
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
#             ]
#         ]
#         else
#         [
#             Point3d point3d = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 0, polylineArea_0.Radius);
#             Point3d point3d1 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 1.5707963267949, polylineArea_0.Radius);
#             Point3d point3d2 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 3.14159265358979, polylineArea_0.Radius);
#             Point3d point3d3 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 4.71238898038469, polylineArea_0.Radius);
#             polyline.AddVertexAt(0, new Point2d(point3d.get_X(), point3d.get_Y()), MathHelper.smethod_60(point3d, point3d1, point3d2), 0, 0);
#             polyline.AddVertexAt(1, new Point2d(point3d2.get_X(), point3d2.get_Y()), MathHelper.smethod_60(point3d2, point3d3, point3d), 0, 0);
#             polyline.AddVertexAt(2, new Point2d(point3d.get_X(), point3d.get_Y()), 0, 0, 0);
#         ]
#         return polyline;
#     ]
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
#         [
#             Exception exception = exception1;
#             self.lastError = string.Format(Messages.ERR_GEO_CALCULATION_PREFIX, exception.Message);
#             flag = false;
#         ]
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
#         if (Geo == null)
#         [
#             throw new Exception(Messages.ERR_GEO_NO_DATUM_LOADED);
#         ]
#         if (math.faAbs(degrees_0.value) >= 89.99999999 or math.fabs(degrees_2.value) >= 89.99999999):
#             throw new Exception(Messages.ERR_GEO_LATITUDE_OUT_OF_RANGE);
#         ]
#         if (math.fabs(degrees_1.Value) >= 180 || math.fabs(degrees_3.Value) >= 180)
#         [
#             throw new Exception(Messages.ERR_GEO_LONGITUDE_OUT_OF_RANGE);
#         ]
#         if (degrees_0 == degrees_2 && degrees_1 == degrees_3)
#         [
#             throw new Exception(Messages.ERR_POSITIONS_CANNOT_BE_EQUAL);
#         ]
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
#         [
#             throw new Exception(Messages.ERR_GEO_LATITUDE_OUT_OF_RANGE);
#         ]
#         if (math.fabs(num) >= 180 || math.fabs(num1) >= 180)
#         [
#             throw new Exception(Messages.ERR_GEO_LONGITUDE_OUT_OF_RANGE);
#         ]
#         if (degrees_0 == degrees_2 && degrees_1 == degrees_3)
#         [
#             throw new Exception(Messages.ERR_POSITIONS_CANNOT_BE_EQUAL);
#         ]
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
#         [
#             return AcadHelper.smethod_151(transaction_0, blockTableRecord_0, point3dCollection_0, point3dCollection_1, string_0, -1, true);

    @staticmethod
    def smethod_151(point3dCollection_0, point3dCollection_1, string_0, int_0, bool_0):
        # if (bool_0):
        #     Point3dCollection.smethod_147(point3dCollection_0, True);
        #     Point3dCollection.smethod_147(point3dCollection_1, True);
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
#         [
#             polygonMesh.set_Layer(string_0);
#         ]
#         if (int_0 >= 0)
#         [
#             polygonMesh.set_ColorIndex(int_0);
#         ]
#         ObjectId objectId = blockTableRecord_0.AppendEntity(polygonMesh);
#         transaction_0.AddNewlyCreatedDBObject(polygonMesh, true);
#         point3dCollection = []
#         for i in range(count):
#             point3dCollection.append(point3dCollection_0[i])
#             point3dCollection.append(point3dCollection_1[i])
#             PolygonMeshVertex polygonMeshVertex = new PolygonMeshVertex(point3dCollection_0.get_Item(i));
#             polygonMeshVertex.SetDatabaseDefaults();
#             if (!string.IsNullOrEmpty(string_0))
#             [
#                 polygonMeshVertex.set_Layer(string_0);
#             ]
#             if (int_0 >= 0)
#             [
#                 polygonMeshVertex.set_ColorIndex(int_0);
#             ]
#             polygonMesh.AppendVertex(polygonMeshVertex);
#             transaction_0.AddNewlyCreatedDBObject(polygonMeshVertex, true);
#             polygonMeshVertex = new PolygonMeshVertex(point3dCollection_1.get_Item(i));
#             polygonMeshVertex.SetDatabaseDefaults();
#             if (!string.IsNullOrEmpty(string_0))
#             [
#                 polygonMeshVertex.set_Layer(string_0);
#             ]
#             if (int_0 >= 0)
#             [
#                 polygonMeshVertex.set_ColorIndex(int_0);
#             ]
#             polygonMesh.AppendVertex(polygonMeshVertex);
#             transaction_0.AddNewlyCreatedDBObject(polygonMeshVertex, true);
#         ]
#         return point3dCollection;

class Geo:

    SemiMajorAxis = 6378293.645208759
    Eccentricity = 6356617.987679838 / 6378293.645208759
    gnm_igrf90 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -29775.4, -1851, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -2135.8, 3058.2, 1693.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 1314.6, -2240.2, 1245.6, 806.5, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 938.9, 782.3, 323.9, -422.7, 141.7, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -211, 352.5, 243.8, -110.8, -165.6, -37, 0, 0, 0, 0, 0, 0, 0 ], [ 60.7, 63.9, 60.4, -177.5, 2, 16.7, -96.3, 0, 0, 0, 0, 0, 0 ], [ 76.6, -64.2, 3.7, 27.5, 0.9, 5.7, 9.8, -0.5, 0, 0, 0, 0, 0 ], [ 22.4, 5.1, -0.9, -10.8, -12.4, 3.8, 3.8, 2.6, -6, 0, 0, 0, 0 ], [ 4.4, 9.9, 0.8, -12, 9.3, -3.9, -1.4, 7.3, 1.5, -5.5, 0, 0, 0 ], [ -3.6, -3.9, 2.4, -5.3, -2.4, 4.4, 3, 1.2, 2.2, 2.9, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    hnm_igrf90 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 5410.9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -2277.7, -380, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -286.5, 293.3, -348.5, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 248.1, -239.5, 87, -299.4, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 47.2, 153.5, -154.4, -69.2, 97.7, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -15.8, 82.7, 68.3, -52.5, 1.8, 26.9, 0, 0, 0, 0, 0, 0 ], [ 0, -81.1, -27.3, 0.6, 20.4, 16.4, -22.6, -5, 0, 0, 0, 0, 0 ], [ 0, 9.7, -19.9, 7.1, -22.1, 11.9, 11, -16, -10.7, 0, 0, 0, 0 ], [ 0, -20.8, 15.4, 9.5, -5.7, -6.4, 8.6, 9.1, -6.6, 1.9, 0, 0, 0 ], [ 0, 1.3, 0.4, 3.1, 5.6, -4.2, -0.5, -1.5, 3.8, -0.5, -6.2, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    gtnm_igrf90 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 18, 10.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -12.9, 2.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 3.3, -6.7, 0, -5.9, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0.5, 0.6, -7, 0.5, -5.5, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0.6, -0.1, -1.6, -3.1, 0, 2.3, 0, 0, 0, 0, 0, 0, 0 ], [ 1.3, -0.2, 1.8, 1.3, -0.2, 0.1, 1.2, 0, 0, 0, 0, 0, 0 ], [ 0.6, -0.5, -0.3, 0.6, 1.6, 0.2, 0.2, 0.3, 0, 0, 0, 0, 0 ], [ 0.2, -0.7, -0.2, 0.1, -1.1, 0, 0, -0.5, -0.6, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    htnm_igrf90 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -16.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -15.8, -13.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 4.4, 1.6, -10.6, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 2.6, 1.8, 3.1, -1.4, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -0.1, 0.5, 0.4, 1.7, 0.4, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0.2, -1.3, 0, -0.9, 0.5, 1.2, 0, 0, 0, 0, 0, 0 ], [ 0, 0.6, 0.2, 0.8, -0.5, -0.2, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0.5, -0.2, 0.3, 0.3, 0.4, -0.5, -0.3, 0.6, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    gnm_igrf95 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -29682, -1789, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -2197, 3074, 1685, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 1329, -2268, 1249, 769, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 941, 782, 291, -421, 116, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -210, 352, 237, -122, -167, -26, 0, 0, 0, 0, 0, 0, 0 ], [ 66, 64, 65, -172, 2, 17, -94, 0, 0, 0, 0, 0, 0 ], [ 78, -67, 1, 29, 4, 8, 10, -2, 0, 0, 0, 0, 0 ], [ 24, 4, -1, -9, -14, 4, 5, 0, -7, 0, 0, 0, 0 ], [ 4, 9, 1, -12, 9, -4, -2, 7, 0, -6, 0, 0, 0 ], [ -3, -4, 2, -5, -2, 4, 3, 1, 3, 3, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    hnm_igrf95 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 5318, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -2356, -425, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -263, 302, -406, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 262, -232, 98, -301, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 44, 157, -152, -64, 99, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -16, 77, 67, -57, 4, 28, 0, 0, 0, 0, 0, 0 ], [ 0, -77, -25, 3, 22, 16, -23, -3, 0, 0, 0, 0, 0 ], [ 0, 12, -20, 7, -21, 12, 10, -17, -10, 0, 0, 0, 0 ], [ 0, -19, 15, 11, -7, -7, 9, 7, -8, 1, 0, 0, 0 ], [ 0, 2, 1, 3, 6, -4, 0, -2, 3, -1, -6, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    gtnm_igrf95 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 17.6, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -13.2, 3.7, -0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 1.5, -6.4, -0.2, -8.1, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0.8, 0.9, -6.9, 0.5, -4.6, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0.8, 0.1, -1.5, -2, -0.1, 2.3, 0, 0, 0, 0, 0, 0, 0 ], [ 0.5, -0.4, 0.6, 1.9, -0.2, -0.2, 0, 0, 0, 0, 0, 0, 0 ], [ -0.2, -0.8, -0.6, 0.6, 1.2, 0.1, 0.2, -0.6, 0, 0, 0, 0, 0 ], [ 0.3, -0.2, 0.1, 0.4, -1.1, 0.3, 0.2, -0.9, -0.3, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    htnm_igrf95 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -18.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -15, -8.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 4.1, 2.2, -12.1, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 1.8, 1.2, 2.7, -1, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0.2, 1.2, 0.3, 1.8, 0.9, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0.3, -1.6, -0.2, -0.9, 1, 2.2, 0, 0, 0, 0, 0, 0 ], [ 0, 0.8, 0.2, 0.6, -0.4, 0, -0.3, 0, 0, 0, 0, 0, 0 ], [ 0, 0.4, -0.2, 0.2, 0.7, 0, -1.2, -0.7, -0.6, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    gnm_wmm85 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -29879.8, -1903.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -2070.6, 3040.8, 1696.7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 1303.9, -2203, 1241.7, 839.4, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 933.8, 781.8, 359, -424.5, 164.5, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -216.4, 353, 254.3, -93.7, -157.5, -45.2, 0, 0, 0, 0, 0, 0, 0 ], [ 53.2, 63.8, 51.3, -188.4, 3.3, 20.3, -101.7, 0, 0, 0, 0, 0, 0 ], [ 76.9, -60.7, 0.7, 25.4, -8.1, 6.9, 7, -4.4, 0, 0, 0, 0, 0 ], [ 18.4, 5.1, 1.2, -12, -9.1, 0.1, 4.7, 6.5, -9.5, 0, 0, 0, 0 ], [ 5.7, 10.9, 0.9, -12.2, 9.5, -3.3, -1, 6.5, 1.5, -4.8, 0, 0, 0 ], [ -3.4, -4.7, 2.5, -5.5, -2.1, 4.6, 3.2, 0.6, 1.9, 2.8, -0.2, 0, 0 ], [ 2.3, -0.8, -2, 2.1, 0.2, -0.4, -0.4, 1.6, 1.5, -0.7, 2.3, 3.5, 0 ], [ -1.8, 0, 0.1, -0.3, 0.5, 0.5, -0.6, -0.4, 0, -0.5, 0, 0.7, -0.2 ] ];
    hnm_wmm85 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 5490.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -2189.1, -312, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -310.3, 282.6, -299.2, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 227.2, -246.7, 72.5, -299.1, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 43.4, 148.2, -154.8, -71.8, 91.5, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -12.3, 87.9, 67.8, -51.1, -4, 20.8, 0, 0, 0, 0, 0, 0 ], [ 0, -80.1, -25.9, -0.9, 21.6, 18.5, -20, -7.7, 0, 0, 0, 0, 0 ], [ 0, 3.8, -20.2, 5, -24.2, 12.2, 7.6, -16.3, -10.9, 0, 0, 0, 0 ], [ 0, -20.8, 15.8, 9, -5, -6.4, 9.1, 9.9, -5.8, 2.3, 0, 0, 0 ], [ 0, 1.2, 0.4, 2.5, 5.6, -4.4, -0.5, -1.6, 3.7, -0.5, -6.1, 0, 0 ], [ 0, 1.3, 2, -1.1, -2.8, 0.7, -0.1, -2.4, -0.4, -1.5, -1.5, 0.7, 0 ], [ 0, 0.3, 0.6, 2.5, -1.7, 0.3, 0.2, -0.1, 0.1, 0.1, -1.4, 0.4, 0.7 ] ];
    gtnm_wmm85 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 21.9, 10.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -11.2, 1.8, 9.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 8.3, -2, -0.6, 2.4, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -1.2, 0.1, -9.7, -1.7, -9.3, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 1.4, -0.5, -1.2, -2.2, 0.9, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 3.1, 0, 1.8, -0.2, -0.4, 2.4, 1.8, 0, 0, 0, 0, 0, 0 ], [ -0.1, -0.8, -1.2, 1.1, 0, 0.6, -1.8, -1.2, 0, 0, 0, 0, 0 ], [ 0.2, 0, 0.7, 0.1, 0.2, -0.3, -0.1, 0.2, -2.2, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    htnm_wmm85 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -31.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -9.7, -19.9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 6.1, 1.3, -13, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 1.3, 3.6, 2.5, 0.6, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -0.9, 0.6, 0.3, 2.4, -1.4, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0.7, -2.1, -1.4, -4.3, -0.7, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 1.2, 2, 2.6, 0.9, 0.8, 0.4, 0, 0, 0, 0, 0 ], [ 0, -0.6, -1.5, 0.1, -1.1, 0.4, -2, 0.9, 1.5, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    gnm_wmm90 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -29780.5, -1851.7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -2134.3, 3062.2, 1691.9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 1312.9, -2244.7, 1246.8, 808.6, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 933.5, 784.9, 323.5, -421.7, 139.2, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -208.3, 352.2, 246.5, -110.8, -162.3, -37.2, 0, 0, 0, 0, 0, 0, 0 ], [ 59, 63.7, 60, -181.3, 0.4, 15.4, -96, 0, 0, 0, 0, 0, 0 ], [ 76.1, -62.1, 1.3, 30.2, 4.7, 7.9, 10.1, 1.9, 0, 0, 0, 0, 0 ], [ 22.9, 2.3, -1.2, -11.7, -17.5, 2.2, 5.7, 3, -7, 0, 0, 0, 0 ], [ 3.6, 9.5, -0.9, -10.7, 10.7, -3.2, -1.4, 6.3, 0.8, -5.5, 0, 0, 0 ], [ -3.3, -2.6, 4.5, -5.6, -3.6, 3.9, 3.2, 1.7, 3, 3.7, 0.7, 0, 0 ], [ 1.3, -1.4, -2.5, 3.2, 0.2, -1.1, 0.3, -0.3, 0.9, -1.1, 2.4, 3, 0 ], [ -1.3, 0.1, 0.5, 0.7, 0.4, -0.2, -1.1, 0.9, -0.6, 0.8, 0.2, 0.4, 0.2 ] ];
    hnm_wmm90 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 5407.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -2278.3, -384.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -284.9, 291.7, -352.4, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 249.4, -232.7, 91.3, -296.5, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 40.8, 148.7, -154.6, -67.6, 97.4, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -14.7, 82.2, 70, -56.2, -1.4, 24.6, 0, 0, 0, 0, 0, 0 ], [ 0, -78.6, -26.7, 0.1, 19.9, 17.9, -21.5, -6.8, 0, 0, 0, 0, 0 ], [ 0, 9.7, -19.3, 6.6, -20.1, 13.4, 9.8, -19, -9.1, 0, 0, 0, 0 ], [ 0, -21.9, 14.3, 9.5, -6.7, -6.4, 9.1, 8.9, -8, 2.1, 0, 0, 0 ], [ 0, 2.6, 1.2, 2.6, 5.7, -4, -0.4, -1.7, 3.8, -0.8, -6.5, 0, 0 ], [ 0, 0, 1, -1.6, -2.2, 1.1, -0.7, -1.7, -1.5, -1.3, -1.1, 0.6, 0 ], [ 0, 0.7, 0.7, 1.3, -1.5, 0.3, 0.2, -1.1, 1.2, -0.2, -1.3, 0.6, 0.6 ] ];
    gtnm_wmm90 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 16, 9.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -11.7, 3.7, 1.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 2.1, -7.6, 0, -5.8, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -0.8, 1, -7.4, 0.8, -6.4, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 1.7, 0, 0, -2.7, 0, 3, 0, 0, 0, 0, 0, 0, 0 ], [ 0.8, 0, 1.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0.5, 0, -0.9, 1.5, 2.7, -1, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -1.1, 0, 0, -2.1, 0, 1, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    htnm_wmm90 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -13.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -12.8, -14.9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 3.1, 0.8, -11.3, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 3.3, 3.7, 2.8, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, -2.1, 1.2, 1.2, 0.6, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -0.6, -0.6, 0, -2.3, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0.6, 0.8, 0, 0, 0, 0.4, 0, 0, 0, 0, 0, 0 ], [ 0, 0.4, -0.8, 0.5, 0.3, 0.5, 0, -0.7, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    gnm_wmm95 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -29682.1, -1782.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -2194.7, 3078.6, 1685.7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 1318.8, -2273.6, 1246.9, 766.3, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 940, 782.9, 290.9, -418.9, 113.8, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -209.5, 354, 238.2, -122.1, -162.8, -23.3, 0, 0, 0, 0, 0, 0, 0 ], [ 68.5, 65.6, 64.1, -169.1, -0.5, 16.5, -91, 0, 0, 0, 0, 0, 0 ], [ 78, -68.1, 0.1, 29.6, 6, 8.7, 9.2, -2.4, 0, 0, 0, 0, 0 ], [ 24.7, 3.4, -1.5, -9.6, -16.5, 2.6, 3.6, -4.9, -8.5, 0, 0, 0, 0 ], [ 2.9, 7.5, 0.4, -10.3, 9.7, -2.3, -2.4, 6.8, -0.5, -6.5, 0, 0, 0 ], [ -2.9, -3.3, 2.8, -4.3, -3.1, 2.4, 2.8, 0.7, 4.1, 3.6, 0.6, 0, 0 ], [ 1.7, -1.6, -3.6, 1.2, -0.6, 0.1, -0.7, -0.8, 1.3, -0.3, 2.2, 4.2, 0 ], [ -1.8, 0.9, -0.1, -0.5, 0.8, 0.2, 0.5, 0.4, -0.4, 0.3, 0.2, 0.4, 0.6 ] ];
    hnm_wmm95 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 5315.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -2359.1, -418.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -261.1, 301, -416.5, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 259.4, -230.9, 99.8, -306.1, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 43.7, 157.6, -150.1, -59.2, 104.4, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -15.2, 74.3, 69.4, -55.3, 3, 33.3, 0, 0, 0, 0, 0, 0 ], [ 0, -76.1, -24.5, 1.6, 20, 16.5, -23.6, -6.8, 0, 0, 0, 0, 0 ], [ 0, 14.9, -19.5, 6.3, -20.4, 12.2, 7, -19, -8.8, 0, 0, 0, 0 ], [ 0, -19.8, 14.6, 10.9, -7.5, -6.8, 9.3, 7.7, -8.1, 2.6, 0, 0, 0 ], [ 0, 3.2, 1.7, 2.9, 5.6, -3.4, -0.7, -2.9, 2.3, -1.6, -6.6, 0, 0 ], [ 0, 0.3, 1, -3.6, -1.4, 1.9, 0.2, -1.3, -2.4, -0.6, -2.2, 1.3, 0 ], [ 0, 0.3, 1.4, 0.8, -3, 0.7, 0.5, -0.8, 0.6, 0.1, -1.3, -0.4, 0.9 ] ];
    gtnm_wmm95 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 17.6, 13.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -13.7, 4, -0.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0.8, -6.6, -0.5, -8.5, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 1.2, 1.1, -6.8, 0.3, -4.5, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0.9, 0.5, -1.4, -1.7, 0, 2.1, 0, 0, 0, 0, 0, 0, 0 ], [ 0.4, -0.3, 0.3, 2.1, 0, -0.4, -0.4, 0, 0, 0, 0, 0, 0 ], [ -0.3, -1.1, -0.5, 0.5, 1.3, 0.1, 0, -0.9, 0, 0, 0, 0, 0 ], [ 0.1, 0, 0.4, 0.3, -1.3, 0.5, 0.4, -0.9, 0.1, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    htnm_wmm95 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -14.6, -7.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 4, 2.2, -12.6, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 1.3, 1, 2.5, -1.2, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0.5, 1.5, 0.6, 1.7, 0.6, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0.7, -1.5, -0.5, -0.7, 1.1, 2.6, 0, 0, 0, 0, 0, 0 ], [ 0, 0.3, 0, 0.7, -0.6, 0.1, -0.6, -0.4, 0, 0, 0, 0, 0 ], [ 0, 0.4, -0.3, 0.1, 0.8, -0.1, -1.3, -0.9, -1.1, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    gnm_wmm2000 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -29616, -1722.7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -2266.7, 3070.2, 1677.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 1322.4, -2291.5, 1255.9, 724.8, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 932.1, 786.3, 250.6, -401.5, 106.2, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -211.9, 351.6, 220.8, -134.5, -168.8, -13.3, 0, 0, 0, 0, 0, 0, 0 ], [ 73.8, 68.2, 74.1, -163.5, -3.8, 17.1, -85.1, 0, 0, 0, 0, 0, 0 ], [ 77.4, -73.9, 2.2, 35.7, 7.3, 5.2, 8.4, -1.5, 0, 0, 0, 0, 0 ], [ 23.3, 7.3, -8.5, -6.6, -16.9, 8.6, 4.9, -7.8, -7.6, 0, 0, 0, 0 ], [ 5.7, 8.5, 2, -9.8, 7.6, -7, -2, 9.2, -2.2, -6.6, 0, 0, 0 ], [ -2.2, -5.7, 1.6, -3.7, -0.6, 4.1, 2.2, 2.2, 4.6, 2.3, 0.1, 0, 0 ], [ 3.3, -1.1, -2.4, 2.6, -1.3, -1.7, -0.6, 0.4, 0.7, -0.3, 2.3, 4.2, 0 ], [ -1.5, -0.2, -0.3, 0.5, 0.2, 0.9, -1.4, 0.6, -0.6, -1, -0.3, 0.3, 0.4 ] ];
    hnm_wmm2000 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 5194.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -2484.8, -467.9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -224.7, 293, -486.5, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 273.3, -227.9, 120.9, -302.7, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 42, 173.8, -135, -38.6, 105.2, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -17.4, 61.2, 63.2, -62.9, 0.2, 43, 0, 0, 0, 0, 0, 0 ], [ 0, -62.3, -24.5, 8.9, 23.4, 15, -27.6, -7.8, 0, 0, 0, 0, 0 ], [ 0, 12.4, -20.8, 8.4, -21.2, 15.5, 9.1, -15.5, -5.4, 0, 0, 0, 0 ], [ 0, -20.4, 13.9, 12, -6.2, -8.6, 9.4, 5, -8.4, 3.2, 0, 0, 0 ], [ 0, 0.9, -0.7, 3.9, 4.8, -5.3, -1, -2.4, 1.3, -2.3, -6.4, 0, 0 ], [ 0, -1.5, 0.7, -1.1, -2.3, 1.3, -0.6, -2.8, -1.6, -0.1, -1.9, 1.4, 0 ], [ 0, -1, 0.7, 2.2, -2.5, -0.2, 0, -0.2, 0, 0.2, -0.9, -0.2, 1 ] ];
    gtnm_wmm2000 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 14.7, 11.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -13.6, -0.7, -1.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0.3, -4.3, 0.9, -8.4, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -1.6, 0.9, -7.6, 2.2, -3.2, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -0.9, -0.2, -2.5, -2.7, -0.9, 1.7, 0, 0, 0, 0, 0, 0, 0 ], [ 1.2, 0.2, 1.7, 1.6, -0.1, -0.3, 0.8, 0, 0, 0, 0, 0, 0 ], [ -0.4, -0.8, -0.2, 1.1, 0.4, 0, -0.2, -0.2, 0, 0, 0, 0, 0 ], [ -0.3, 0.6, -0.8, 0.3, -0.2, 0.5, 0, -0.6, 0.1, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    htnm_wmm2000 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -20.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -21.5, -9.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 6.4, -1.3, -13.3, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 2.3, 0.7, 3.7, -0.5, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 2.1, 2.3, 3.1, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -0.3, -1.7, -0.9, -1, -0.1, 1.9, 0, 0, 0, 0, 0, 0 ], [ 0, 1.4, 0.2, 0.7, 0.4, -0.3, -0.8, -0.1, 0, 0, 0, 0, 0 ], [ 0, -0.5, 0.1, -0.2, 0, 0.1, -0.1, 0.3, 0.2, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    gnm_igrf2000 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -29615, -1728, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -2267, 3072, 1672, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 1341, -2290, 1253, 715, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 935, 787, 251, -405, 110, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -217, 351, 222, -131, -169, -12, 0, 0, 0, 0, 0, 0, 0 ], [ 72, 68, 74, -161, -5, 17, -91, 0, 0, 0, 0, 0, 0 ], [ 79, -74, 0, 33, 9, 7, 8, -2, 0, 0, 0, 0, 0 ], [ 25, 6, -9, -8, -17, 9, 7, -8, -7, 0, 0, 0, 0 ], [ 5, 9, 3, -8, 6, -9, -2, 9, -4, -8, 0, 0, 0 ], [ -2, -6, 2, -3, 0, 4, 1, 2, 4, 0, -1, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    hnm_igrf2000 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 5186, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -2478, -458, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -227, 296, -492, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 272, -232, 119, -304, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 44, 172, -134, -40, 107, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -17, 64, 65, -61, 1, 44, 0, 0, 0, 0, 0, 0 ], [ 0, -65, -24, 6, 24, 15, -25, -6, 0, 0, 0, 0, 0 ], [ 0, 12, -22, 8, -21, 15, 9, -16, -3, 0, 0, 0, 0 ], [ 0, -20, 13, 12, -6, -8, 9, 4, -8, 5, 0, 0, 0 ], [ 0, 1, 0, 4, 5, -6, -1, -3, 0, -2, -8, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    gtnm_igrf2000 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 14.6, 10.7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -12.4, 1.1, -1.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0.7, -5.4, 0.9, -7.7, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -1.3, 1.6, -7.3, 2.9, -3.2, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -0.7, -2.1, -2.8, -0.8, 2.5, 0, 0, 0, 0, 0, 0, 0 ], [ 1, -0.4, 0.9, 2, -0.6, -0.3, 1.2, 0, 0, 0, 0, 0, 0 ], [ -0.4, -0.4, -0.3, 1.1, 1.1, -0.2, 0.6, -0.9, 0, 0, 0, 0, 0 ], [ -0.3, 0.2, -0.3, 0.4, -1, 0.3, -0.5, -0.7, -0.4, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    htnm_igrf2000 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -22.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -20.6, -9.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 6, -0.1, -14.2, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 2.1, 1.3, 5, 0.3, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -0.1, 0.6, 1.7, 1.9, 0.1, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -0.2, -1.4, 0, -0.8, 0, 0.9, 0, 0, 0, 0, 0, 0 ], [ 0, 1.1, 0, 0.3, -0.1, -0.6, -0.7, 0.2, 0, 0, 0, 0, 0 ], [ 0, 0.1, 0, 0, 0.3, 0.6, -0.4, 0.3, 0.7, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    gnm_wmm2005 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -29556.8, -1671.7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -2340.6, 3046.9, 1657, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 1335.4, -2305.1, 1246.7, 674, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 919.8, 798.1, 211.3, -379.4, 100, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -227.4, 354.6, 208.7, -136.5, -168.3, -14.1, 0, 0, 0, 0, 0, 0, 0 ], [ 73.2, 69.7, 76.7, -151.2, -14.9, 14.6, -86.3, 0, 0, 0, 0, 0, 0 ], [ 80.1, -74.5, -1.4, 38.5, 12.4, 9.5, 5.7, 1.8, 0, 0, 0, 0, 0 ], [ 24.9, 7.7, -11.6, -6.9, -18.2, 10, 9.2, -11.6, -5.2, 0, 0, 0, 0 ], [ 5.6, 9.9, 3.5, -7, 5.1, -10.8, -1.3, 8.8, -6.7, -9.1, 0, 0, 0 ], [ -2.3, -6.3, 1.6, -2.6, 0, 3.1, 0.4, 2.1, 3.9, -0.1, -2.3, 0, 0 ], [ 2.8, -1.6, -1.7, 1.7, -0.1, 0.1, -0.7, 0.7, 1.8, 0, 1.1, 4.1, 0 ], [ -2.4, -0.4, 0.2, 0.8, -0.3, 1.1, -0.5, 0.4, -0.3, -0.3, -0.1, -0.3, -0.1 ] ];
    hnm_wmm2005 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 5079.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -2594.7, -516.7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -199.9, 269.3, -524.2, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 281.5, -226, 145.8, -304.7, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 42.4, 179.8, -123, -19.5, 103.6, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -20.3, 54.7, 63.6, -63.4, -0.1, 50.4, 0, 0, 0, 0, 0, 0 ], [ 0, -61.5, -22.4, 7.2, 25.4, 11, -26.4, -5.1, 0, 0, 0, 0, 0 ], [ 0, 11.2, -21, 9.6, -19.8, 16.1, 7.7, -12.9, -0.2, 0, 0, 0, 0 ], [ 0, -20.1, 12.9, 12.6, -6.7, -8.1, 8, 2.9, -7.9, 6, 0, 0, 0 ], [ 0, 2.4, 0.2, 4.4, 4.8, -6.5, -1.1, -3.4, -0.8, -2.3, -7.9, 0, 0 ], [ 0, 0.3, 1.2, -0.8, -2.5, 0.9, -0.6, -2.7, -0.9, -1.3, -2, -1.2, 0 ], [ 0, -0.4, 0.3, 2.4, -2.6, 0.6, 0.3, 0, 0, 0.3, -0.9, -0.4, 0.8 ] ];
    gtnm_wmm2005 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 8, 10.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -15.1, -7.8, -0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0.4, -2.6, -1.2, -6.5, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -2.5, 2.8, -7, 6.2, -3.8, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -2.8, 0.7, -3.2, -1.1, 0.1, -0.8, 0, 0, 0, 0, 0, 0, 0 ], [ -0.7, 0.4, -0.3, 2.3, -2.1, -0.6, 1.4, 0, 0, 0, 0, 0, 0 ], [ 0.2, -0.1, -0.3, 1.1, 0.6, 0.5, -0.4, 0.6, 0, 0, 0, 0, 0 ], [ 0.1, 0.3, -0.4, 0.3, -0.3, 0.2, 0.4, -0.7, 0.4, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    htnm_wmm2005 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -20.9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -23.2, -14.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 5, -7, -0.6, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 2.2, 1.6, 5.8, 0.1, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 1.7, 2.1, 4.8, -1.1, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -0.6, -1.9, -0.4, -0.5, -0.3, 0.7, 0, 0, 0, 0, 0, 0 ], [ 0, 0.6, 0.4, 0.2, 0.3, -0.8, -0.2, 0.1, 0, 0, 0, 0, 0 ], [ 0, -0.2, 0.1, 0.3, 0.4, 0.1, -0.2, 0.4, 0.4, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
    gnm_wmm2010 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -29496.6, -1586.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -2396.6, 3026.1, 1668.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 1340.1, -2326.2, 1231.9, 634, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 912.6, 808.9, 166.7, -357.1, 89.4, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -230.9, 357.2, 200.3, -141.1, -163, -7.8, 0, 0, 0, 0, 0, 0, 0 ], [ 72.8, 68.6, 76, -141.4, -22.8, 13.2, -77.9, 0, 0, 0, 0, 0, 0 ], [ 80.5, -75.1, -4.7, 45.3, 13.9, 10.4, 1.7, 4.9, 0, 0, 0, 0, 0 ], [ 24.4, 8.1, -14.5, -5.6, -19.3, 11.5, 10.9, -14.1, -3.7, 0, 0, 0, 0 ], [ 5.4, 9.4, 3.4, -5.2, 3.1, -12.4, -0.7, 8.4, -8.5, -10.1, 0, 0, 0 ], [ -2, -6.3, 0.9, -1.1, -0.2, 2.5, -0.3, 2.2, 3.1, -1, -2.8, 0, 0 ], [ 3, -1.5, -2.1, 1.7, -0.5, 0.5, -0.8, 0.4, 1.8, 0.1, 0.7, 3.8, 0 ], [ -2.2, -0.2, 0.3, 1, -0.6, 0.9, -0.1, 0.5, -0.4, -0.4, 0.2, -0.8, 0 ] ];
    hnm_wmm2010 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 4944.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -2707.7, -576.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -160.2, 251.9, -536.6, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 286.4, -211.2, 164.3, -309.1, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 44.6, 188.9, -118.2, 0, 100.9, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -20.8, 44.1, 61.5, -66.3, 3.1, 55, 0, 0, 0, 0, 0, 0 ], [ 0, -57.9, -21.1, 6.5, 24.9, 7, -27.7, -3.3, 0, 0, 0, 0, 0 ], [ 0, 11, -20, 11.9, -17.4, 16.7, 7, -10.8, 1.7, 0, 0, 0, 0 ], [ 0, -20.5, 11.5, 12.8, -7.2, -7.4, 8, 2.1, -6.1, 7, 0, 0, 0 ], [ 0, 2.8, -0.1, 4.7, 4.4, -7.2, -1, -3.9, -2, -2, -8.3, 0, 0 ], [ 0, 0.2, 1.7, -0.6, -1.8, 0.9, -0.4, -2.5, -1.3, -2.1, -1.9, -1.8, 0 ], [ 0, -0.9, 0.3, 2.1, -2.5, 0.5, 0.6, 0, 0.1, 0.3, -0.9, -0.2, 0.9 ] ];
    gtnm_wmm2010 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 11.6, 16.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -12.1, -4.4, 1.9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0.4, -4.1, -2.9, -7.7, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -1.8, 2.3, -8.7, 4.6, -2.1, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -1, 0.6, -1.8, -1, 0.9, 1, 0, 0, 0, 0, 0, 0, 0 ], [ -0.2, -0.2, -0.1, 2, -1.7, -0.3, 1.7, 0, 0, 0, 0, 0, 0 ], [ 0.1, -0.1, -0.6, 1.3, 0.4, 0.3, -0.7, 0.6, 0, 0, 0, 0, 0 ], [ -0.1, 0.1, -0.6, 0.2, -0.2, 0.3, 0.3, -0.6, 0.2, 0, 0, 0, 0 ], [ 0, -0.1, 0, 0.3, -0.4, -0.3, 0.1, -0.1, -0.4, -0.2, 0, 0, 0 ], [ 0, 0, -0.1, 0.2, 0, -0.1, -0.2, 0, -0.1, -0.2, -0.2, 0, 0 ], [ 0, 0, 0, 0.1, 0, 0, 0, 0, 0, 0, -0.1, 0, 0 ], [ 0, 0, 0.1, 0.1, -0.1, 0, 0, 0, 0, 0, 0, -0.1, 0.1 ] ];
    htnm_wmm2010 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -25.9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -22.5, -11.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 7.3, -3.9, -2.6, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 1.1, 2.7, 3.9, -0.8, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0.4, 1.8, 1.2, 4, -0.6, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -0.2, -2.1, -0.4, -0.6, 0.5, 0.9, 0, 0, 0, 0, 0, 0 ], [ 0, 0.7, 0.3, -0.1, -0.1, -0.8, -0.3, 0.3, 0, 0, 0, 0, 0 ], [ 0, -0.1, 0.2, 0.4, 0.4, 0.1, -0.1, 0.4, 0.3, 0, 0, 0, 0 ], [ 0, 0, -0.2, 0, -0.1, 0.1, 0, -0.2, 0.3, 0.2, 0, 0, 0 ], [ 0, 0.1, -0.1, 0, -0.1, -0.1, 0, -0.1, -0.2, 0, -0.1, 0, 0 ], [ 0, 0, 0.1, 0, 0.1, 0, 0.1, 0, -0.1, -0.1, 0, -0.1, 0 ], [ 0, 0, 0, 0, 0, 0, 0.1, 0, 0, 0, 0, 0, 0 ] ];
    gnm_wmm2015 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -29438.5, -1501.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -2445.3, 3012.5, 1676.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 1351.1, -2352.3, 1225.6, 581.9, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 907.2, 813.7, 120.3, -335, 70.3, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -232.6, 360.1, 192.4, -141, -157.4, 4.3, 0, 0, 0, 0, 0, 0, 0 ], [ 69.5, 67.4, 72.8, -129.8, -29, 13.2, -70.9, 0, 0, 0, 0, 0, 0 ], [ 81.6, -76.1, -6.8, 51.9, 15, 9.3, -2.8, 6.7, 0, 0, 0, 0, 0 ], [ 24, 8.6, -16.9, -3.2, -20.6, 13.3, 11.7, -16, -2, 0, 0, 0, 0 ], [ 5.4, 8.8, 3.1, -3.1, 0.6, -13.3, -0.1, 8.7, -9.1, -10.5, 0, 0, 0 ], [ -1.9, -6.5, 0.2, 0.6, -0.6, 1.7, -0.7, 2.1, 2.3, -1.8, -3.6, 0, 0 ], [ 3.1, -1.5, -2.3, 2.1, -0.9, 0.6, -0.7, 0.2, 1.7, -0.2, 0.4, 3.5, 0 ], [ -2, -0.3, 0.4, 1.3, -0.9, 0.9, 0.1, 0.5, -0.4, -0.4, 0.2, -0.9, 0 ] ];
    hnm_wmm2015 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 4796.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -2845.6, -642, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -115.3, 245, -538.3, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 283.4, -188.6, 180.9, -329.5, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 47.4, 196.9, -119.4, 16.1, 100.1, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -20.7, 33.2, 58.8, -66.5, 7.3, 62.5, 0, 0, 0, 0, 0, 0 ], [ 0, -54.1, -19.4, 5.6, 24.4, 3.3, -27.5, -2.3, 0, 0, 0, 0, 0 ], [ 0, 10.2, -18.1, 13.2, -14.6, 16.2, 5.7, -9.1, 2.2, 0, 0, 0, 0 ], [ 0, -21.6, 10.8, 11.7, -6.8, -6.9, 7.8, 1, -3.9, 8.5, 0, 0, 0 ], [ 0, 3.3, -0.3, 4.6, 4.4, -7.9, -0.6, -4.1, -2.8, -1.1, -8.7, 0, 0 ], [ 0, -0.1, 2.1, -0.7, -1.1, 0.7, -0.2, -2.1, -1.5, -2.5, -2, -2.3, 0 ], [ 0, -1, 0.5, 1.8, -2.2, 0.3, 0.7, -0.1, 0.3, 0.2, -0.9, -0.2, 0.7 ] ];
    gtnm_wmm2015 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 10.7, 17.9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -8.6, -3.3, 2.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 3.1, -6.2, -0.4, -10.4, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -0.4, 0.8, -9.2, 4, -4.2, 0, 0, 0, 0, 0, 0, 0, 0 ], [ -0.2, 0.1, -1.4, 0, 1.3, 3.8, 0, 0, 0, 0, 0, 0, 0 ], [ -0.5, -0.2, -0.6, 2.4, -1.1, 0.3, 1.5, 0, 0, 0, 0, 0, 0 ], [ 0.2, -0.2, -0.4, 1.3, 0.2, -0.4, -0.9, 0.3, 0, 0, 0, 0, 0 ], [ 0, 0.1, -0.5, 0.5, -0.2, 0.4, 0.2, -0.4, 0.3, 0, 0, 0, 0 ], [ 0, -0.1, -0.1, 0.4, -0.5, -0.2, 0.1, 0, -0.2, -0.1, 0, 0, 0 ], [ 0, 0, -0.1, 0.3, -0.1, -0.1, -0.1, 0, -0.2, -0.1, -0.2, 0, 0 ], [ 0, 0, -0.1, 0.1, 0, 0, 0, 0, 0, 0, -0.1, -0.1, 0 ], [ 0.1, 0, 0, 0.1, -0.1, 0, 0.1, 0, 0, 0, 0, 0, 0 ] ];
    htnm_wmm2015 = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -26.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -27.1, -13.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 8.4, -0.4, 2.3, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, -0.6, 5.3, 3, -5.3, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0.4, 1.6, -1.1, 3.3, 0.1, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, -2.2, -0.7, 0.1, 1, 1.3, 0, 0, 0, 0, 0, 0 ], [ 0, 0.7, 0.5, -0.2, -0.1, -0.7, 0.1, 0.1, 0, 0, 0, 0, 0 ], [ 0, -0.3, 0.3, 0.3, 0.6, -0.1, -0.2, 0.3, 0, 0, 0, 0, 0 ], [ 0, -0.2, -0.1, -0.2, 0.1, 0.1, 0, -0.2, 0.4, 0.3, 0, 0, 0 ], [ 0, 0.1, -0.1, 0, 0, -0.2, 0.1, -0.1, -0.2, 0.1, -0.1, 0, 0 ], [ 0, 0, 0.1, 0, 0.1, 0, 0, 0.1, 0, -0.1, 0, -0.1, 0 ], [ 0, 0, 0, -0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ];
	
        # if (self.datums == null)
        # [
        #     self.datums = new GeoDatums();
        # ]
    root = []#new double[13];
    roots = []#new double[13, 13, 2];

    def __init__(self):

        for i in range(13):
            Geo.root.append(0)
            a = []
            for j in range(13):
                a.append([0, 0])
            Geo.roots.append(a)

        for i in range(2, 13):
            Geo.root[i] = math.sqrt((2 * float(i) - 1) / (2 * float(i)));
        for j in range(13):
            num = j * j;
            for k in range(max([j + 1, 2]), 13):
                Geo.roots[j][k][0] = math.sqrt(float((k - 1) * (k - 1) - num));
                Geo.roots[j][k][1] = 1 / math.sqrt(float(k * k - num));
    @staticmethod
    def EarthRadius():
        semiMajorAxis = Geo.SemiMajorAxis
        eccentricity = Geo.Eccentricity
        return Distance(semiMajorAxis + math.sqrt(semiMajorAxis * semiMajorAxis - semiMajorAxis * semiMajorAxis * (eccentricity * eccentricity))) / 2


    @staticmethod
    def smethod_2(double_0, double_1):
        flag = False;
        lat = None;
        long = None;
        try:
            point3dLL = QgisHelper.CrsTransformPoint(double_0, double_1, define._xyCrs, define._latLonCrs)
            lat = point3dLL.get_Y()
            long = point3dLL.get_X()
            return True, Degrees(lat, None, None, DegreesType.Latitude), Degrees(long, None, None, DegreesType.Longitude);
        except:
            pass
        return False, Degrees(lat), Degrees(long);

    @staticmethod
    def smethod_3(degrees_0, degrees_1):
        flag = False;
        long = None;
        lat = None;
        try:
            point3dXY = QgisHelper.CrsTransformPoint(degrees_1.value, degrees_0.value, define._latLonCrs, define._xyCrs)
            lat = point3dXY.get_Y()
            long = point3dXY.get_X()
            return True, long, lat
        except:
            pass
        return False, long, lat

    @staticmethod
    def smethod_4(geoCalculationType_0, degrees_0, degrees_1, degrees_2, degrees_3):
        distance_0 = None
        double_0 = None
        double_1 = None
        flag = False
        if (geoCalculationType_0 != GeoCalculationType.Ellipsoid):
            num1, double_0, double_1 = Geo.smethod_10(degrees_0, degrees_1, degrees_2, degrees_3);
            distance_0 = Distance(num1, DistanceUnits.KM);
            flag = True;
        else:
            num, double_0, double_1 = Geo.smethod_9(degrees_0, degrees_1, degrees_2, degrees_3);
            distance_0 = Distance(num, DistanceUnits.KM);
            flag = True;
        return flag, distance_0, double_0, double_1

    @staticmethod
    def smethod_6(geoCalculationType_0, degrees_0, degrees_1, double_0, distance_0):
        num = None;
        num1 = None;
        flag = False;
        degrees_2 = None;
        degrees_3 = None;
        double_1 = None;
        try:
            if (geoCalculationType_0 != GeoCalculationType.Ellipsoid):
                degrees_2, degrees_3 = Geo.smethod_12(degrees_0, degrees_1, double_0, distance_0.Metres);
                num1, num, double_1 = Geo.smethod_10(degrees_0, degrees_1, degrees_2, degrees_3);
                flag = True;
            else:
                degrees_2, degrees_3, double_1 = Geo.smethod_11(degrees_0, degrees_1, double_0, distance_0.Metres);
                flag = True;
        except:
            raise UserWarning, Messages.ERR_GEO_CALCULATION_PREFIX
            # Exception exception = exception1;
            # Geo.lastError = string.Format(Messages.ERR_GEO_CALCULATION_PREFIX, exception.Message);
            flag = False;

        return flag, degrees_2, degrees_3, double_1;

    @staticmethod
    def smethod_7(degrees_0, degrees_1, altitude_0, magneticModel_0, dateTime_0):
        totalDays = None;
        i = None;
        j = None;
        flag = False;
        numArray = [];
        numArray1 = [];
        gnmWmm2010 = [];
        hnmWmm2010 = [];
        numArray2 = [];
        numArray3 = [];
        degrees_2 = None;

    #         if (!self.DatumLoaded)
    #         [
    #             throw new Exception(Messages.ERR_GEO_NO_DATUM_LOADED);
    #         ]
        if (math.fabs(degrees_0) >= 89.99999999):
            return False, None
            # throw new Exception(Messages.ERR_GEO_LATITUDE_OUT_OF_RANGE);

        if (math.fabs(degrees_1) >= 180):
            return False, None
            # throw new Exception(Messages.ERR_GEO_LONGITUDE_OUT_OF_RANGE);
        semiMajorAxis = Geo.SemiMajorAxis / 1000;
        eccentricity = Geo.Eccentricity;
        num = math.sqrt(semiMajorAxis * semiMajorAxis - semiMajorAxis * semiMajorAxis * (eccentricity * eccentricity));
        num = 6357755.816444299/1000#(6400000 * 2 - Geo.SemiMajorAxis)/ 1000
        num1 = 6371.2;
        num2 = Unit.ConvertDegToRad(degrees_0);
        num3 = Unit.ConvertDegToRad(degrees_1);
        num4 = Unit.smethod_13(altitude_0.Metres);
        num5 = math.sin(num2);
        num6 = math.cos(num2);
        num7 = math.sqrt(semiMajorAxis * semiMajorAxis * num6 * num6 + num * num * num5 * num5);
        num8 = math.atan2(num6 * (num4 * num7 + semiMajorAxis * semiMajorAxis), num5 * (num4 * num7 + num * num));
        num9 = num4 * num4 + 2 * num4 * num7 + (semiMajorAxis * semiMajorAxis * semiMajorAxis * semiMajorAxis - (semiMajorAxis * semiMajorAxis * semiMajorAxis * semiMajorAxis - num * num * num * num) * num5 * num5) / (semiMajorAxis * semiMajorAxis - (semiMajorAxis * semiMajorAxis - num * num) * num5 * num5);
        num9 = math.sqrt(num9);
        num10 = math.cos(num8);
        num11 = math.sin(num8);
        num12 = 1 / MathHelper.smethod_2(num11);
        for i in range(13):
            numArray2.append(0)
            numArray3.append(0)

            numArray.append([0,0,0,0,0,0,0,0,0,0,0,0, 0])
            numArray1.append([0,0,0,0,0,0,0,0,0,0,0,0, 0])
            gnmWmm2010.append([0,0,0,0,0,0,0,0,0,0,0,0, 0])
            hnmWmm2010.append([0,0,0,0,0,0,0,0,0,0,0,0, 0])
        numArray[0][0] = 1;
        numArray[1][1] = num11;
        numArray1[0][0] = 0;
        numArray1[1][1] = num10;
        numArray[1][0] = num10;
        numArray1[1][0] = -num11;
        for i in range(2, 13):
            numArray[i][i] = numArray[i - 1][i - 1] * num11 * Geo.root[i];
            numArray1[i][i] = (numArray1[i - 1][i - 1] * num11 + numArray[i - 1][i - 1] * num10) * Geo.root[i];
        for j in range(13):
            for i in range(max([j + 1, 2]), 13):
                numArray[i][j] = (numArray[i - 1][j] * num10 * (2 * float(i) - 1) - numArray[i - 2][j] * Geo.roots[j][i][0]) * Geo.roots[j][i][1];
                numArray1[i][j] = ((numArray1[i - 1][j] * num10 - numArray[i - 1][j] * num11) * (2 * float(i) - 1) - numArray1[i - 2][j] * Geo.roots[j][i][0]) * Geo.roots[j][i][1];
        if magneticModel_0 == MagneticModel.WMM2015:
            date0 = QDate(2015, 1, 1);
            timeSpan = date0.daysTo(dateTime_0)
            totalDays = timeSpan / 365.25;
            for i in range(1, 13):
                for j in range(13):
                    gnmWmm2010[i][j] = Geo.gnm_wmm2015[i][j] + totalDays * Geo.gtnm_wmm2015[i][j];
                    hnmWmm2010[i][j] = Geo.hnm_wmm2015[i][j] + totalDays * Geo.htnm_wmm2015[i][j];
        elif magneticModel_0 == MagneticModel.WMM2010:
            date0 = QDate(2010, 1, 1);
            timeSpan = date0.daysTo(dateTime_0)
            totalDays = timeSpan / 365.25;
            for i in range(1, 13):
                for j in range(13):
                    gnmWmm2010[i][j] = Geo.gnm_wmm2010[i][j] + totalDays * Geo.gtnm_wmm2010[i][j];
                    hnmWmm2010[i][j] = Geo.hnm_wmm2010[i][j] + totalDays * Geo.htnm_wmm2010[i][j];
        elif magneticModel_0 == MagneticModel.WMM2005:
            date0 = QDate(2005, 1, 1);
            timeSpan = date0.daysTo(dateTime_0)
            totalDays = timeSpan / 365.25;
            for i in range(1, 13):
                for j in range(13):
                    gnmWmm2010[i][j] = Geo.gnm_wmm2005[i][j] + totalDays * Geo.gtnm_wmm2005[i][j];
                    hnmWmm2010[i][j] = Geo.hnm_wmm2005[i][j] + totalDays * Geo.htnm_wmm2005[i][j];
        elif magneticModel_0 == MagneticModel.WMM2000:
            date0 = QDate(2000, 1, 1);
            timeSpan = date0.daysTo(dateTime_0)
            totalDays = timeSpan / 365.25;
            for i in range(1, 13):
                for j in range(13):
                    gnmWmm2010[i][j] = Geo.gnm_wmm2000[i][j] + totalDays * Geo.gtnm_wmm2000[i][j];
                    hnmWmm2010[i][j] = Geo.hnm_wmm2000[i][j] + totalDays * Geo.htnm_wmm2000[i][j];
        elif magneticModel_0 == MagneticModel.WMM95:
            date0 = QDate(1995, 1, 1);
            timeSpan = date0.daysTo(dateTime_0)
            totalDays = timeSpan / 365.25;
            for i in range(1, 13):
                for j in range(13):
                    gnmWmm2010[i][j] = Geo.gnm_wmm95[i][j] + totalDays * Geo.gtnm_wmm95[i][j];
                    hnmWmm2010[i][j] = Geo.hnm_wmm95[i][j] + totalDays * Geo.htnm_wmm95[i][j];
        elif magneticModel_0 == MagneticModel.WMM90:
            date0 = QDate(1990, 1, 1);
            timeSpan = date0.daysTo(dateTime_0)
            totalDays = timeSpan / 365.25;
            for i in range(1, 13):
                for j in range(13):
                    gnmWmm2010[i][j] = Geo.gnm_wmm90[i][j] + totalDays * Geo.gtnm_wmm90[i][j];
                    hnmWmm2010[i][j] = Geo.hnm_wmm90[i][j] + totalDays * Geo.htnm_wmm90[i][j];
        elif magneticModel_0 == MagneticModel.WMM85:
            date0 = QDate(1985, 1, 1);
            timeSpan = date0.daysTo(dateTime_0)
            totalDays = timeSpan / 365.25;
            for i in range(1, 13):
                for j in range(13):
                    gnmWmm2010[i][j] = Geo.gnm_wmm85[i][j] + totalDays * Geo.gtnm_wmm85[i][j];
                    hnmWmm2010[i][j] = Geo.hnm_wmm85[i][j] + totalDays * Geo.htnm_wmm85[i][j];
        elif magneticModel_0 == MagneticModel.IGRF2000:
            date0 = QDate(2000, 1, 1);
            timeSpan = date0.daysTo(dateTime_0)
            totalDays = timeSpan / 365.25;
            for i in range(1, 13):
                for j in range(13):
                    gnmWmm2010[i][j] = Geo.gnm_igrf2000[i][j] + totalDays * Geo.gtnm_igrf2000[i][j];
                    hnmWmm2010[i][j] = Geo.hnm_igrf2000[i][j] + totalDays * Geo.htnm_igrf2000[i][j];
        elif magneticModel_0 == MagneticModel.IGRF95:
            date0 = QDate(1995, 1, 1);
            timeSpan = date0.daysTo(dateTime_0)
            totalDays = timeSpan / 365.25;
            for i in range(1, 13):
                for j in range(13):
                    gnmWmm2010[i][j] = Geo.gnm_igrf95[i][j] + totalDays * Geo.gtnm_igrf95[i][j];
                    hnmWmm2010[i][j] = Geo.hnm_igrf95[i][j] + totalDays * Geo.htnm_igrf95[i][j];
        elif magneticModel_0 == MagneticModel.IGRF90:
            date0 = QDate(1990, 1, 1);
            timeSpan = date0.daysTo(dateTime_0)
            totalDays = timeSpan / 365.25;
            for i in range(1, 13):
                for j in range(13):
                    gnmWmm2010[i][j] = Geo.gnm_igrf90[i][j] + totalDays * Geo.gtnm_igrf90[i][j];
                    hnmWmm2010[i][j] = Geo.hnm_igrf90[i][j] + totalDays * Geo.htnm_igrf90[i][j];
        else:
            raise UserWarning, Messages.ERR_GEO_INVALID_MAGNETIC_MODEL
            # throw new Exception(Messages.ERR_GEO_INVALID_MAGNETIC_MODEL);
        for j in range(13):
            numArray2[j] = math.sin(float(j) * num3);
            numArray3[j] = math.cos(float(j) * num3);
        num13 = 0;
        num14 = 0;
        num15 = 0;
        num16 = num1 / num9;
        num17 = num16 * num16;
        for i in range(1, 13):
            num18 = 0;
            num19 = 0;
            num20 = 0;
            for j in range(i + 1):
                num21 = gnmWmm2010[i][j] * numArray3[j] + hnmWmm2010[i][j] * numArray2[j];
                num18 = num18 + num21 * numArray[i][j];
                num19 = num19 + num21 * numArray1[i][j];
                num20 = num20 + float(j) * (gnmWmm2010[i][j] * numArray2[j] - hnmWmm2010[i][j] * numArray3[j]) * numArray[i][j];
            num17 = num17 * num16;
            num13 = num13 + float(i + 1) * num18 * num17;
            num14 = num14 - num19 * num17;
            num15 = num15 + num20 * num17 * num12;
        num22 = num8 - (1.5707963267949 - num2);
        num23 = math.sin(num22);
        num24 = math.cos(num22);
        num25 = -num14 * num24 - num13 * num23;
        num26 = num15;
        if (num25 == 0):
            if (num26 != 0):
                degrees_2 = Unit.smethod_1(math.atan2(num26, num25));
                flag = True
            degrees_2 = 0
            flag = True
        else:
            degrees_2 = Unit.smethod_1(math.atan2(num26, num25));
            flag = True
        # except:
        #     raise UserWarning, Messages.ERR_GEO_CALCULATION_PREFIX
    #     catch (Exception exception1)
    #     [
    #         Exception exception = exception1;
    #         ErrorMessageBox.smethod_0(null, string.Format(Messages.ERR_GEO_CALCULATION_PREFIX, exception.Message));
    #         return false;
    #     ]
        return (flag, degrees_2);

    @staticmethod
    def smethod_9( degrees_0, degrees_1, degrees_2, degrees_3):
        num10 = Unit.ConvertDegToRad(degrees_0);
        num11 = Unit.ConvertDegToRad(degrees_1);
        num12 = Unit.ConvertDegToRad(degrees_2);
        num13 = Unit.ConvertDegToRad(degrees_3);
        semiMajorAxis = Geo.SemiMajorAxis
        eccentricity = Geo.Eccentricity
        num14 = math.sqrt(semiMajorAxis * semiMajorAxis - semiMajorAxis * semiMajorAxis * (eccentricity * eccentricity));
        num14 = 6367604 * 2 - semiMajorAxis
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
        value = degrees_0;
        num = degrees_1;
        value1 = degrees_2;
        num1 = degrees_3;
        if (math.fabs(value) >= 89.99999999 or math.fabs(value1) >= 89.99999999):
            raise UserWarning, Messages.ERR_GEO_LATITUDE_OUT_OF_RANGE
            # throw new Exception(Messages.ERR_GEO_LATITUDE_OUT_OF_RANGE);

        if (math.fabs(num) >= 180 or math.fabs(num1) >= 180):
            raise UserWarning, Messages.ERR_GEO_LONGITUDE_OUT_OF_RANGE
            # throw new Exception(Messages.ERR_GEO_LONGITUDE_OUT_OF_RANGE);
        if (degrees_0 == degrees_2 and degrees_1 == degrees_3):
            raise UserWarning, Messages.ERR_POSITIONS_CANNOT_BE_EQUAL
            # throw new Exception(Messages.ERR_POSITIONS_CANNOT_BE_EQUAL);
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

        return double_0, double_1, double_2

    @staticmethod
    def smethod_11(degrees_0, degrees_1, double_0, double_1):
        num = None;
        num1 = None;
        num2 = None;
        num3 = None;
       
        if (math.fabs(degrees_0) >= 89.99999999):
            raise UserWarning, Messages.ERR_GEO_LATITUDE_OUT_OF_RANGE
            # throw new Exception(Messages.ERR_GEO_LATITUDE_OUT_OF_RANGE);
        if (math.fabs(degrees_1) >= 180):
            raise UserWarning, Messages.ERR_GEO_LONGITUDE_OUT_OF_RANGE
            # throw new Exception(Messages.ERR_GEO_LONGITUDE_OUT_OF_RANGE);
        if (double_1 <= 0):
            raise UserWarning, Messages.ERR_DISTANCE_MUST_BE_GREATER_THAN_0
            # throw new Exception(Messages.ERR_DISTANCE_MUST_BE_GREATER_THAN_0);
        num4 = Unit.ConvertDegToRad(degrees_0);
        num5 = Unit.ConvertDegToRad(degrees_1);
        num6 = Unit.ConvertDegToRad(double_0);
        semiMajorAxis = Geo.SemiMajorAxis;
        num7 = math.sqrt(semiMajorAxis * semiMajorAxis - semiMajorAxis * semiMajorAxis * (Geo.Eccentricity * Geo.Eccentricity));

        num7 = 6378222.816444299
        num8 = (semiMajorAxis - num7) / semiMajorAxis;
        num9 = 1 - num8;
        double1 = num9 * math.sin(num4) / math.cos(num4);
        num10 = math.sin(num6);
        num11 = math.cos(num6);
        num12 = 0;
        if (num11 != 0):
            num12 = math.atan2(double1, num11) * 2;
        num13 = 1 / math.sqrt(double1 * double1 + 1);
        num14 = double1 * num13;
        num15 = num13 * num10;
        num16 = -num15 * num15 + 1;
        num17 = math.sqrt((1 / num9 / num9 - 1) * num16 + 1) + 1;
        num17 = (num17 - 2) / num17;
        num18 = 1 - num17;
        num18 = (num17 * num17 / 4 + 1) / num18;
        num19 = (0.375 * num17 * num17 - 1) * num17;
        double1 = double_1 / num9 / semiMajorAxis / num18;
        num20 = double1;

        num = math.sin(num20);
        num1 = math.cos(num20);
        num2 = math.cos(num12 + num20);
        num3 = num2 * num2 * 2 - 1;
        num18 = num20;
        num17 = num3 * num1;
        num20 = num3 + num3 - 1;
        num20 = (((num * num * 4 - 3) * num20 * num2 * num19 / 6 + num17) * num19 / 4 - num2) * num * num19 + double1;

        while (math.fabs(num20 - num18) > 5E-14):
            num = math.sin(num20);
            num1 = math.cos(num20);
            num2 = math.cos(num12 + num20);
            num3 = num2 * num2 * 2 - 1;
            num18 = num20;
            num17 = num3 * num1;
            num20 = num3 + num3 - 1;
            num20 = (((num * num * 4 - 3) * num20 * num2 * num19 / 6 + num17) * num19 / 4 - num2) * num * num19 + double1;

        num12 = num13 * num1 * num11 - num14 * num;
        num18 = num9 * math.sqrt(num15 * num15 + num12 * num12);
        num19 = num14 * num1 + num13 * num * num11;
        num21 = math.atan2(num19, num18);
        num18 = num13 * num1 - num14 * num * num11;
        num17 = math.atan2(num * num10, num18);
        num18 = ((-3 * num16 + 4) * num8 + 4) * num16 * num8 / 16;
        num19 = ((num3 * num1 * num18 + num2) * num * num18 + num20) * num15;
        num22 = num5 + num17 - (1 - num18) * num19 * num8;
        num12 = math.atan2(num15, num12) + 3.14159265358979;
        degrees_2 = Unit.smethod_1(num21);
        degrees_3 = Unit.smethod_1(num22);
        double_2 = Unit.smethod_1(MathHelper.smethod_4(num12))
        
        return degrees_2, degrees_3, double_2

    @staticmethod
    def smethod_12(degrees_0, degrees_1, double_0, double_1):
        if (math.fabs(degrees_0) >= 89.99999999):
            raise UserWarning, Messages.ERR_GEO_LATITUDE_OUT_OF_RANGE
            # throw new Exception(Messages.ERR_GEO_LATITUDE_OUT_OF_RANGE);
        if (math.fabs(degrees_1) >= 180):
            raise UserWarning, Messages.ERR_GEO_LONGITUDE_OUT_OF_RANGE
            # throw new Exception(Messages.ERR_GEO_LONGITUDE_OUT_OF_RANGE);
        if (double_1 <= 0):
            raise UserWarning, Messages.ERR_DISTANCE_MUST_BE_GREATER_THAN_0
            # throw new Exception(Messages.ERR_DISTANCE_MUST_BE_GREATER_THAN_0);
        num = Unit.ConvertDegToRad(degrees_0);
        num1 = Unit.ConvertDegToRad(degrees_1);
        double_0 = Unit.ConvertDegToRad(double_0);
        double1 = double_1 / 6400000;
        num2 = math.asin(math.sin(num) * math.cos(double1) + math.cos(num) * math.sin(double1) * math.cos(double_0));
        num3 = math.atan2(math.sin(double_0) * math.sin(double1) * math.cos(num), math.cos(double1) - math.sin(num) * math.sin(num2));
        num4 = (num1 * -1 - num3 + 3.14159265358979) % 6.28318530717959;
        num5 = 3.14159265358979 - num4;
        degrees_2 = Unit.smethod_1(num2);
        degrees_3 = Unit.smethod_1(num5);
        
        return degrees_2, degrees_3
