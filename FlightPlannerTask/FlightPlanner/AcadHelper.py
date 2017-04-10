#__author__ = 'Administrator'
from FlightPlanner.helpers import  Unit
from FlightPlanner.messages import Messages
from FlightPlanner.types import TurnDirection, Point3D, AngleUnits, Point3dCollection
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.QgisHelper import QgisHelper
from qgis.core import QgsGeometry
from qgis.core import QgsPalLayerSettings,QgsPoint, QGis, QgsVectorFileWriter, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2
from FlightPlanner.expressions import Expressions
from Type.Geometry import DBText
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnapper
from qgis.core import QGis, QgsRectangle, QgsGeometry
from PyQt4.QtCore import QVariant, QObject, QFileInfo, QFile, QDir, QStringList
from PyQt4.QtCore import Qt, QString, QRect, SIGNAL
from FlightPlanner.helpers import MathHelper
from map.tools import QgsMapToolSelectUtils
from FlightPlanner.messages import Messages
from Type.Geometry import Line, Feature
import math, define

class AcadHelper:

    @staticmethod
    def createVectorLayer(layerName, geometryType = QGis.Line, path = "memory"):
        shpPath = ""
        if define.obstaclePath != None:
            shpPath = define.obstaclePath
        elif define.xmlPath != None:
            shpPath = define.xmlPath
        else:
            shpPath = define.appPath
        layerName = layerName.replace(".", "_")
        layerName = layerName.replace("-", "_")
        layerName = layerName.replace(":", "_")
        layerName = layerName.replace(" ", "_")
        layerName = layerName.replace("/", "_")
        layers = define._canvas.layers()
        removeFlag = False
        if len(layers) > 0:
            for ly in layers:
                if layerName == ly.name():
                    QgisHelper.removeFromCanvas(define._canvas, [ly])
                    removeFlag = True
                    break
            define._canvas.refresh()
        if removeFlag:
            directory = QDir(shpPath)
            strList = QStringList()
            strList.append(layerName)
            entryInfoList = directory.entryInfoList()
            for fileInfo in entryInfoList:
                if fileInfo.isFile() and fileInfo.fileName().contains(layerName):
                    b = QFile.remove(fileInfo.filePath())
                    pass
            fileInfo = QFileInfo(shpPath + "/" + layerName + ".shp")
        # if fileInfo.exists():
        #     f = QFile.remove(shpPath + "/" + layerName + ".shp")
        #     # f = file.remove()



        # er = QgsVectorFileWriter.writeAsVectorFormat(layer, destShpName, "utf-8", layer.crs())
        #
        constructionLineLayer = None
        mapUnits = define._canvas.mapUnits()
        if geometryType == QGis.Line:
            if mapUnits == QGis.Meters:
                constructionLineLayer = QgsVectorLayer("linestring?crs=%s"%define._xyCrs.authid (), layerName, path)
            else:
                constructionLineLayer = QgsVectorLayer("linestring?crs=%s"%define._latLonCrs.authid (), layerName, path)


        elif geometryType == QGis.Polygon:
            if mapUnits == QGis.Meters:
                constructionLineLayer = QgsVectorLayer("polygon?crs=%s"%define._xyCrs.authid(), layerName, path)
            else:
                constructionLineLayer = QgsVectorLayer("polygon?crs=%s"%define._latLonCrs.authid (), layerName, path)

        elif geometryType == QGis.Point:
            if mapUnits == QGis.Meters:
                constructionLineLayer = QgsVectorLayer("Point?crs=%s"%define._xyCrs.authid (), layerName, path)
            else:
                constructionLineLayer = QgsVectorLayer("Point?crs=%s"%define._latLonCrs.authid (), layerName, path)


        er = QgsVectorFileWriter.writeAsVectorFormat(constructionLineLayer, shpPath + "/" + layerName
                                                     + ".shp", "utf-8", constructionLineLayer.crs())
        constructionLineLayer = QgsVectorLayer(shpPath + "/" + layerName + ".shp", layerName, "ogr")


        if constructionLineLayer != None:
            constructionLineLayer.startEditing()
            fieldAltitude = "Altitude"
            fieldName = "Caption"
            fieldNameBulge = "Bulge"
            fieldNameGeometryType = "Type"
            fieldCategory = "CATEGORY"
            fieldXdataName = "XDataName"
            fieldXdataPoint = "XDataPoint"
            fieldXDataTolerance = "XDataTol"
            fieldCenterPoint = "CenterPt"
            fieldSurface = "Surface"

            fAltitude = QgsField(fieldAltitude, QVariant.String)
            # print fAltitude.length()
            # fAltitude.setLength(100000)
            constructionLineLayer.dataProvider().addAttributes( [fAltitude,
                                                                 QgsField(fieldName, QVariant.String),
                                                                 QgsField(fieldNameBulge, QVariant.String),
                                                                 QgsField(fieldNameGeometryType, QVariant.String),
                                                                 QgsField(fieldCategory, QVariant.String),
                                                                 QgsField(fieldXdataName, QVariant.String),
                                                                 QgsField(fieldXdataPoint, QVariant.String),
                                                                 QgsField(fieldXDataTolerance, QVariant.String),
                                                                 QgsField(fieldCenterPoint, QVariant.String),
                                                                 QgsField(fieldSurface, QVariant.String)
                                                                 ])
            constructionLineLayer.commitChanges()
        return constructionLineLayer

    @staticmethod
    def createNominalTrackLayer(point3dList, attributes = None, path = "memory", name = "NominalTrack"):
        #######---------------- attributes  :   dictionary Type   ------------------######
        #######---------------- point3dList  :  list containing Point3Ds  ------------- ####

        constructionLineLayer = AcadHelper.createVectorLayer(name)

        typeStr = ""
        if len(point3dList) == 2:
            typeStr = "Line"
        else:
            typeStr = "Polyline"

        altitudesStr = ""
        i = 0
        for point3d in point3dList:
            altitudesStr += str(point3d.get_Z())
            if i != len(point3dList) - 1:
                altitudesStr += ","
            i += 1

        constructionLineLayer.startEditing()
        feature = Feature(QgsGeometry.fromPolyline(point3dList), {"Type":typeStr, "Altitude":altitudesStr})
        pr = constructionLineLayer.dataProvider()
        pr.addFeatures([feature])
        # constructionLineLayer.addFeature(feature)
        constructionLineLayer.commitChanges()

        return constructionLineLayer

    @staticmethod
    def createWPTPointLayer(layerName, pointList):
        resultLayer = AcadHelper.createVectorLayer(layerName, QGis.Point)
        for point, categoryText in pointList:
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, point, False, {"Category":categoryText})

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
    def setGeometryAndAttributesInLayer(layer, polylineArea, isClosed = False, attributesDictionary = {}):
        attributes = {}
        attributes.update(attributesDictionary)
        if layer.geometryType() == QGis.Line:
            if isinstance(polylineArea, Feature):
                layer.startEditing()
                pr = layer.dataProvider()
                pr.addFeatures([polylineArea])
                # layer.addFeature(polylineArea)
                layer.commitChanges()
                return
            elif isinstance(polylineArea, PolylineArea) or isinstance(polylineArea, Line):
                if len(polylineArea) <= 0:
                    return
                i = 0
                startIndex = i
                endPoint = None
                if polylineArea.isCircle:
                    tempPolylineArea = PolylineArea.smethod_131(polylineArea)
                    point3dArray = tempPolylineArea.method_14_closed()
                    layer.startEditing()
                    feature = Feature(QgsGeometry.fromPolyline(point3dArray))
                    altitudeStr = polylineArea[0].Position.get_Z()
                    attributes.update({"Bulge":polylineArea[0].Bulge, "Type":"Circle", "Altitude":altitudeStr, "CenterPt":polylineArea[0].Position})
                    feature.setAttr(attributes)
                    pr = layer.dataProvider()
                    pr.addFeatures([feature])
                    # layer.addFeature(feature)
                    layer.commitChanges()
                    attributes = {}
                    attributes.update(attributesDictionary)
                    return
                while i < len(polylineArea):
                    if i == len(polylineArea) - 1:
                        if polylineArea[i].Bulge != 0:
                            layer.startEditing()
                            if startIndex != i:
                                point3dArray = []
                                altitudeStr = ""
                                for j in range(startIndex, i + 1):
                                    point3dArray.append(polylineArea[j].Position)
                                    altitudeStr += str(polylineArea[j].Position.get_Z())
                                    if j != i:
                                        altitudeStr += ","
                                feature = Feature()
                                feature.setGeom(QgsGeometry.fromPolyline(point3dArray))
                                if len(altitudeStr) > 250:
                                    altitudeStr = altitudeStr[:250]
                                attributes.update({"Altitude":altitudeStr})
                                feature.setAttr(attributes)
                                pr = layer.dataProvider()
                                pr.addFeatures([feature])
                                # layer.addFeature(feature)
                                attributes = {}
                                attributes.update(attributesDictionary)
                            tempPolylineArea = PolylineArea()
                            tempPolylineArea.Add(polylineArea[i])
                            tempPolylineArea.Add(PolylineAreaPoint(polylineArea[0].Position))
                            point3dArray = tempPolylineArea.method_14()
                            altitudeStr = ""
                            for j in range(len(tempPolylineArea)):
                                altitudeStr += str(tempPolylineArea[j].Position.get_Z())
                                if j != len(tempPolylineArea) - 1:
                                    altitudeStr += ","
                            if len(altitudeStr) > 250:
                                altitudeStr = altitudeStr[:250]
                            feature = Feature()
                            feature.setGeom(QgsGeometry.fromPolyline(point3dArray))
                            attributes.update({"Bulge":str(polylineArea[i].Bulge), "Altitude":altitudeStr})
                            feature.setAttr(attributes)
                            pr = layer.dataProvider()
                            pr.addFeatures([feature])
                            # layer.addFeature(feature)
                            layer.commitChanges()
                            attributes = {}
                            attributes.update(attributesDictionary)
                            endPoint = tempPolylineArea[1].Position
                            break
                        elif startIndex == len(polylineArea) - 1:
                            break
                        else:
                            point3dArray = []
                            altitudeStr = ""
                            for j in range(startIndex, i + 1):
                                point3dArray.append(polylineArea[j].Position)
                                altitudeStr += str(polylineArea[j].Position.get_Z())
                                if j != i:
                                    altitudeStr += ","
                            if len(altitudeStr) > 250:
                                altitudeStr = altitudeStr[:250]
                            layer.startEditing()
                            feature = Feature()
                            feature.setGeom(QgsGeometry.fromPolyline(point3dArray))
                            attributes.update({"Altitude":altitudeStr})
                            feature.setAttr(attributes)
                            pr = layer.dataProvider()
                            pr.addFeatures([feature])
                            # layer.addFeature(feature)
                            layer.commitChanges()
                            attributes = {}
                            attributes.update(attributesDictionary)
                            endPoint = polylineArea[i].Position
                            break
                    elif polylineArea[i].Bulge == 0:
                        i += 1
                        continue
                    else:
                        point3dArray = []
                        altitudeStr = ""
                        if i != startIndex:
                            for j in range(startIndex, i + 1):
                                point3dArray.append(polylineArea[j].Position)
                                altitudeStr += str(polylineArea[j].Position.get_Z())
                                if j != i:
                                    altitudeStr += ","
                            if len(altitudeStr) > 250:
                                altitudeStr = altitudeStr[:250]
                            layer.startEditing()
                            feature = Feature()
                            feature.setGeom(QgsGeometry.fromPolyline(point3dArray))
                        
                            attributes.update({"Altitude":altitudeStr})
                            feature.setAttr(attributes)
                            pr = layer.dataProvider()
                            pr.addFeatures([feature])
                            # layer.addFeature(feature)
                            attributes = {}
                            attributes.update(attributesDictionary)
                            layer.commitChanges()

                        layer.startEditing()
                        tempPolylineArea = PolylineArea()
                        tempPolylineArea.Add(polylineArea[i])
                        tempPolylineArea.Add(PolylineAreaPoint(polylineArea[i + 1].Position))
                        point3dArray = tempPolylineArea.method_14()
                        altitudeStr = ""
                        for j in range(len(tempPolylineArea)):
                            altitudeStr += str(tempPolylineArea[j].Position.get_Z())
                            if j != len(tempPolylineArea) - 1:
                                altitudeStr += ","
                        if len(altitudeStr) > 250:
                            altitudeStr = altitudeStr[:250]
                        feature = Feature()
                        feature.setGeom(QgsGeometry.fromPolyline(point3dArray))
                        attributes.update({"Altitude":altitudeStr, "Bulge":polylineArea[i].Bulge})
                        feature.setAttr(attributes)
                        pr = layer.dataProvider()
                        pr.addFeatures([feature])
                        # layer.addFeature(feature)
                        layer.commitChanges()
                        attributes = {}
                        attributes.update(attributesDictionary)
                        endPoint = tempPolylineArea[1].Position
                        startIndex = i + 1
                        i += 1
                        continue
    
                if isClosed == True:
                    point3dArray = [endPoint, polylineArea[0].Position]
                    feature = Feature()
                    layer.startEditing()
                    feature.setGeom(QgsGeometry.fromPolyline(point3dArray))
                    altitudeStr = str(endPoint.get_Z()) + "," + str(polylineArea[0].Position.get_Z())
                    attributes.update({"Altitude":altitudeStr})
                    feature.setAttr(attributes)
                    pr = layer.dataProvider()
                    pr.addFeatures([feature])
                    # layer.addFeature(feature)
                    layer.commitChanges()
                    attributes = {}
                    attributes.update(attributesDictionary)
            elif isinstance(polylineArea, list):
                layer.startEditing()
                feature = Feature()
                feature.setGeom(QgsGeometry.fromPolyline(polylineArea))
                altitudeStr = ""
                if isinstance(polylineArea[0], Point3D):
                    for i in range(len(polylineArea)):
                        altitudeStr += str(polylineArea[i].get_Z())
                        if i != len(polylineArea) - 1:
                            altitudeStr += ","
                if len(altitudeStr) > 250:
                    altitudeStr = altitudeStr[:250]
                attributes.update({"Altitude":altitudeStr})
                feature.setAttr(attributes)
                pr = layer.dataProvider()
                pr.addFeatures([feature])
                # layer.addFeature(feature)
                layer.commitChanges()
                attributes = {}
                attributes.update(attributesDictionary)
        elif layer.geometryType() == QGis.Point:
            if isinstance(polylineArea, Feature):
                layer.startEditing()
                pr = layer.dataProvider()
                pr.addFeatures([polylineArea])
                # layer.addFeature(polylineArea)
                layer.commitChanges()
                return
            elif isinstance(polylineArea, Point3D):
                layer.startEditing()
                feature = Feature()
                feature.setGeom(QgsGeometry.fromPoint(QgsPoint(polylineArea.get_X(), polylineArea.get_Y())))
                attributes.update({"Altitude":polylineArea.get_Z()})
                feature.setAttr(attributes)
                pr = layer.dataProvider()
                pr.addFeatures([feature])
                # layer.addFeature(feature)
                layer.commitChanges()
            elif isinstance(polylineArea, QgsPoint):
                layer.startEditing()
                feature = Feature()
                feature.setGeom(QgsGeometry.fromPoint(polylineArea))
                # attributes.update({"Altitude":polylineArea.get_Z()})
                feature.setAttr(attributes)
                pr = layer.dataProvider()
                pr.addFeatures([feature])
                # layer.addFeature(feature)
                layer.commitChanges()
        elif layer.geometryType() == QGis.Polygon:
            if isinstance(polylineArea, Feature):
                layer.startEditing()
                pr = layer.dataProvider()
                pr.addFeatures([polylineArea])
                # layer.addFeature(polylineArea)
                layer.commitChanges()
                return
            elif isinstance(polylineArea, PolylineArea):
                layer.startEditing()
                point3dArray = polylineArea.method_14_closed()
                altitudeStr = ""
                for i in range(len(polylineArea)):
                    altitudeStr += str(polylineArea[i].Position.get_Z())
                    if i != len(polylineArea) - 1:
                        altitudeStr += ","
                if len(altitudeStr) > 250:
                    altitudeStr = altitudeStr[:250]
                feature = Feature()
                feature.setGeom(QgsGeometry.fromPolygon([point3dArray]))
                attributes.update({"Altitude":altitudeStr})
                feature.setAttr(attributes)
                pr = layer.dataProvider()
                pr.addFeatures([feature])
                # layer.addFeature(feature)
                layer.commitChanges()
            elif isinstance(polylineArea, list):
                layer.startEditing()
                polylineArea.append(polylineArea[0])
                altitudeStr = ""
                for i in range(len(polylineArea)):
                    altitudeStr += str(polylineArea[i].get_Z())
                    if i != len(polylineArea) - 1:
                        altitudeStr += ","
                if len(altitudeStr) > 250:
                    altitudeStr = altitudeStr[:250]
                feature = Feature()
                feature.setGeom(QgsGeometry.fromPolygon([polylineArea]))
                attributes.update({"Altitude":altitudeStr})
                feature.setAttr(attributes)
                pr = layer.dataProvider()
                pr.addFeatures([feature])
                # layer.addFeature(feature)
                layer.commitChanges()




    @staticmethod
    def WPT2Layer(waypoint1, waypoint2, name = "WPT", categoryValurList = []):
        resultLayer = AcadHelper.createVectorLayer(name, QGis.Point)
        if len(categoryValurList) == 0:
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, waypoint1, False, {"Category":"Waypoint1"})
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, waypoint2, False, {"Category":"Waypoint2"})
        else:
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, waypoint1, False, {"Category":categoryValurList[0]})
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, waypoint2, False, {"Category":categoryValurList[1]})

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

        symRenderer = None
        if len(categoryValurList) > 0 and QString(categoryValurList[0]).contains("Fly"):
            symRenderer = QgsCategorizedSymbolRendererV2(Expressions.WPT_EXPRESION_FLY, [renderCatFlyOver, renderCatFlyBy])
        else:
            symRenderer = QgsCategorizedSymbolRendererV2(Expressions.WPT_EXPRESION, [renderCatFlyOver, renderCatFlyBy])

        resultLayer.setRendererV2(symRenderer)
        return resultLayer

    @staticmethod
    def smethod_19(entity_0, constructLayer, int_0):
        ####### int_0 --- color index ------------
        if isinstance(entity_0, Line):
            AcadHelper.setGeometryAndAttributesInLayer(constructLayer,\
                                                       entity_0, \
                                                       False, \
                                                       {"Caption":entity_0.caption, \
                                                        "XDataName":entity_0.xData['ThousandOne'], \
                                                        "XDataPoint":entity_0.xData['ThousandTen'],\
                                                        "XDataTol":entity_0.xData['ThousandForty']})

        elif isinstance(entity_0, PolylineArea):
            if constructLayer.geometryType() == QGis.Line:
                AcadHelper.setGeometryAndAttributesInLayer(constructLayer, entity_0)
            elif constructLayer.geometryType() == QGis.Polygon:
                 AcadHelper.setGeometryAndAttributesInLayer(constructLayer, entity_0, True)
            constructLayer.commitChanges()
        elif isinstance(entity_0, Feature):
            AcadHelper.setGeometryAndAttributesInLayer(constructLayer, entity_0)
        elif isinstance(entity_0, DBText):
            if entity_0.xData == None:
                AcadHelper.setGeometryAndAttributesInLayer(constructLayer, entity_0.geometry, False, {"Caption":entity_0.string, "Type":"DBText"})
            else:
                AcadHelper.setGeometryAndAttributesInLayer(constructLayer, entity_0.geometry, False, {"Caption":entity_0.string, "Type":"DBText", \
                                                                                                      "XDataName":entity_0.xData['ThousandOne'], \
                                                                                                      "XDataPoint":entity_0.xData['ThousandTen'],\
                                                                                                      "XDataTol":entity_0.xData['ThousandForty']})

            palSetting = QgsPalLayerSettings()
            palSetting.readFromLayer(constructLayer)
            palSetting.enabled = True
            palSetting.fieldName = "Caption"
            palSetting.isExpression = True
            palSetting.placement = QgsPalLayerSettings.Line
            palSetting.placementFlags = QgsPalLayerSettings.AboveLine
            palSetting.Rotation = Unit.ConvertRadToDeg(MathHelper.smethod_4(entity_0.rotation))
            palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, str(entity_0.height), "")
            palSetting.writeToLayer(constructLayer)
        elif isinstance(entity_0, list):
            AcadHelper.setGeometryAndAttributesInLayer(constructLayer, entity_0)
        elif isinstance(entity_0, QgsGeometry):
            AcadHelper.setGeometryAndAttributesInLayer(constructLayer, entity_0.asPolyline())


    @staticmethod
    def smethod_18(entity_0, constructLayer):
        if isinstance(entity_0, PolylineArea):
            if constructLayer.geometryType() == QGis.Line:
                AcadHelper.setGeometryAndAttributesInLayer(constructLayer, entity_0)
            elif constructLayer.geometryType() == QGis.Polygon:
                AcadHelper.setGeometryAndAttributesInLayer(constructLayer, entity_0, True)
            constructLayer.commitChanges()
        elif isinstance(entity_0, Line):
            AcadHelper.setGeometryAndAttributesInLayer(constructLayer, entity_0)
        elif isinstance(entity_0, Feature):
            AcadHelper.setGeometryAndAttributesInLayer(constructLayer, entity_0)
        elif isinstance(entity_0, DBText):
            AcadHelper.setGeometryAndAttributesInLayer(constructLayer, entity_0.geometry, False, {"Caption":entity_0.string})

            palSetting = QgsPalLayerSettings()
            palSetting.readFromLayer(constructLayer)
            palSetting.enabled = True
            palSetting.fieldName = "Caption"
            palSetting.isExpression = True
            palSetting.placement = QgsPalLayerSettings.Line
            palSetting.placementFlags = QgsPalLayerSettings.AboveLine
            palSetting.Rotation = Unit.ConvertRadToDeg(MathHelper.smethod_4(entity_0.rotation))
            palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, str(entity_0.height), "")
            palSetting.writeToLayer(constructLayer)
        elif isinstance(entity_0, list):
            AcadHelper.setGeometryAndAttributesInLayer(constructLayer, entity_0)
        elif isinstance(entity_0, QgsGeometry):
            AcadHelper.setGeometryAndAttributesInLayer(constructLayer, entity_0.asPolyline())

    @staticmethod
    def smethod_46(string_0):
        string_0 = QString(string_0)
        # string_0 = string_0.replace('<', '\u005F')
        # string_0 = string_0.replace('>', '\u005F')
        # string_0 = string_0.replace('/', '\u005F')
        # string_0 = string_0.replace('\\', '\u005F')
        # string_0 = string_0.replace('\"', '\u005F')
        # string_0 = string_0.replace(':', '\u005F')
        # string_0 = string_0.replace('', '\u005F')
        # string_0 = string_0.replace('?', '\u005F')
        # string_0 = string_0.replace('*', '\u005F')
        # string_0 = string_0.replace('|', '\u005F')
        # string_0 = string_0.replace(',', '\u005F')
        # string_0 = string_0.replace('=', '\u005F')
        # string_0 = string_0.replace('\u0060', '\u005F')
        return string_0.trimmed()
    
    @staticmethod
    def smethod_57(symbolName, point3d, pointLayer):
        fieldName = "CATEGORY"
        # pointLayer.dataProvider().addAttributes( [QgsField(fieldName, QVariant.String)] )
        pointLayer.startEditing()
        # fields = pointLayer.pendingFields()
        if symbolName == "FlyOver":
            feature = Feature()

            feature.setGeom(QgsGeometry.fromPoint (point3d))
            feature.setAttr({"Category":"FlyOver"})
            pr = pointLayer.dataProvider()
            pr.addFeatures([feature])
            # pointLayer.addFeature(feature)
        else:
            feature = Feature()
            feature.setGeom(QgsGeometry.fromPoint (point3d))
            feature.setAttr({"Category":"FlyBy"})
            pr = pointLayer.dataProvider()
            pr.addFeatures([feature])
            # pointLayer.addFeature(feature)
            # feature = QgsFeature()
            # feature.setGeometry(QgsGeometry.fromPoint (point3d))
            # feature.setAttributes(["FlyBy"])
            # pointLayer.addFeature(feature)

        pointLayer.commitChanges()

        '''FlyOver'''
        # mawpBearing = MathHelper.getBearing(self.annotationMAHWP.mapPosition(), self.annotationMAWP.mapPosition())
        symbolFlyOver = QgsSymbolV2.defaultSymbol(pointLayer.geometryType())
        symbolFlyOver.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyover.svg", 9.0, 0.0)#Unit.ConvertRadToDeg(mawpBearing))
        symbolFlyOver.appendSymbolLayer(svgSymLayer)
        renderCatFlyOver = QgsRendererCategoryV2(1, symbolFlyOver,"FlyOver")

        '''FlyBy'''
        symbolFlyBy = QgsSymbolV2.defaultSymbol(pointLayer.geometryType())
        symbolFlyBy.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyby.svg", 9.0, 0.0)#Unit.ConvertRadToDeg(mawpBearing))
        symbolFlyBy.appendSymbolLayer(svgSymLayer)
        renderCatFlyBy = QgsRendererCategoryV2(0, symbolFlyBy,"FlyBy")

        symRenderer = QgsCategorizedSymbolRendererV2(Expressions.RNAVNOMINAL_EXPRESION, [renderCatFlyOver, renderCatFlyBy])

        pointLayer.setRendererV2(symRenderer)
    @staticmethod
    def smethod_66(point2d_0, point2d_1):
        num = MathHelper.calcDistance(point2d_0, point2d_1) * 0.1
        # acadApplication = Application.get_AcadApplication()
        pt0 = Point3D(point2d_0.get_X() - num, point2d_0.get_Y() - num)
        # numArray = x
        pt1 = Point3D(point2d_1.get_X() + num, point2d_1.get_Y() + num)
        # objArray = [numArray, x1]
        r = QgsRectangle(pt0, pt1)
        define._canvas.setExtent(r)
        define._canvas.refresh()
        # acadApplication.smethod_23("ZoomWindow", objArray)
    @staticmethod
    def smethod_102(string_0, string_1, string_2, dlg):
        define._messageLabel.setText(string_0)
        selectLineMapTool = SelectLine(define._canvas, dlg)
        define._canvas.setMapTool(selectLineMapTool)
        QObject.connect(selectLineMapTool, SIGNAL("outputResult"), AcadHelper.smethod_102_result)
        return selectLineMapTool
        # line, point3d = AcadHelper.smethod_103(string_0, string_1, string_2)
        # return line
    @staticmethod
    def smethod_102_result(geom, parent):
        QObject.emit(parent, SIGNAL("AcadHelper_Smethod_102_Event"), geom)
        pointlist = geom.asPolyline()
        pass

    @staticmethod
    def smethod_121(polyline_0, point3d_0):
        a = []
        count = len(polyline_0)
        i = 0
        while(i < count):
            polyline_0.pop(0)
            i += 1
        for point in point3d_0:
            polyline_0.Add(PolylineAreaPoint(point))
        # polyline_0.Reset(false, 0)
        # for point3d0 in point3d_0:
        #     # Point3d point3d0 = point3d_0[i]
        #     polyline_0.AddVertexAt(i, new Point2d(point3d0.get_X(), point3d0.get_Y()), 0, 0, 0)
        # return PolylineArea(point3d_0)
    @staticmethod
    def smethod_126(point3dList):
        # Polyline polyline = new Polyline()
        # for (int i = 0 i < (int)point3d_0.Length i++)
        # {
        #     Point3d point3d0 = point3d_0[i]
        #     polyline.AddVertexAt(i, new Point2d(point3d0.get_X(), point3d0.get_Y()), 0, 0, 0)
        # }
        return PolylineArea(point3dList)

    @staticmethod
    def smethod_130(pointList):
        # Polyline polyline = new Polyline()
        return QgsGeometry.fromPolyline(pointList)
        # for (int i = 0 i < list_0.Count i++)
        # {
        #     Point3d item = list_0[i]
        #     polyline.AddVertexAt(i, new Point2d(item.get_X(), item.get_Y()), 0, 0, 0)
        # }
        # return polyline
    @staticmethod
    def smethod_133(point3dCollection_0, bool_0):
        pointArray = []
        for pt in point3dCollection_0:
            pointArray.append(pt)
        if bool_0:
            pointArray.append(point3dCollection_0[0])
        return PolylineArea(pointArray)
        # polyline = PolylineArea()#Polyline()
        # for (int i = 0 i < point3dCollection_0.get_Count() i++)
        # {
        #     Point3d item = point3dCollection_0.get_Item(i)
        #     polyline.AddVertexAt(i, new Point2d(item.get_X(), item.get_Y()), 0, 0, 0)
        # }
        # polyline.set_Closed(bool_0)
        # return polyline
    
    @staticmethod
    def smethod_135_v15(polylineArea_0):
        return polylineArea_0
        # polyline = PolylineArea()
        # if (not polylineArea_0.IsCircle):
        #     for (int i = 0 i < polylineArea_0.Count i++)
        #     {
        #         PolylineAreaPoint item = polylineArea_0[i]
        #         double x = item.Position.get_X()
        #         Point3d position = item.Position
        #         polyline.AddVertexAt(i, new Point2d(x, position.get_Y()), item.Bulge, 0, 0)
        #     }
        # }
        # else
        # {
        #     Point3d point3d = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 0, polylineArea_0.Radius)
        #     Point3d point3d1 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 1.5707963267949, polylineArea_0.Radius)
        #     Point3d point3d2 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 3.14159265358979, polylineArea_0.Radius)
        #     Point3d point3d3 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 4.71238898038469, polylineArea_0.Radius)
        #     polyline.AddVertexAt(0, new Point2d(point3d.get_X(), point3d.get_Y()), MathHelper.smethod_61(point3d, point3d1, point3d2), 0, 0)
        #     polyline.AddVertexAt(1, new Point2d(point3d2.get_X(), point3d2.get_Y()), MathHelper.smethod_61(point3d2, point3d3, point3d), 0, 0)
        #     polyline.AddVertexAt(2, new Point2d(point3d.get_X(), point3d.get_Y()), 0, 0, 0)
        # }
        # return polyline

    @staticmethod
    def smethod_137(string_0, point3d_0, double_0, geometryType = QGis.Line):
        dBText = DBText()
        dBText.set_TextString(string_0)
        dBText.set_Position(point3d_0)
        dBText.set_Height(10)#(double_0)
        dBText.set_LayerType(geometryType)
        return dBText
    @staticmethod
    def smethod_137_v15(point3dCollection_0, bool_0):
        pointArray = []
        for pt in point3dCollection_0:
            pointArray.append(pt)
        if bool_0:
            pointArray.append(point3dCollection_0[0])
        return PolylineArea(pointArray)
    @staticmethod
    def smethod_138(string_0, point3d_0, double_0, textHorizontalMode_0):
        dBText = DBText()
        dBText.set_TextString(string_0)
        dBText.set_Position(point3d_0)
        dBText.set_Height(double_0)
        dBText.set_HorizontalMode(textHorizontalMode_0)
        dBText.set_AlignmentPoint(point3d_0)
        return dBText

    @staticmethod
    def smethod_140_v15(polylineArea_0, bool_0):
        polyline = AcadHelper.smethod_135_v15(polylineArea_0)
        if bool_0:
            polyline.append(polylineArea_0[0])
            return polyline
        return polyline

    @staticmethod
    def smethod_140(string_0, point3d_0, double_0, textHorizontalMode_0, textVerticalMode_0, geometryType = QGis.Line):
        dBText = DBText()
        dBText.set_TextString(string_0)
        dBText.set_Position(point3d_0)
        dBText.set_Height(10)#(double_0)
        dBText.set_HorizontalMode(textHorizontalMode_0)
        dBText.set_VerticalMode(textVerticalMode_0)
        dBText.set_AlignmentPoint(point3d_0)
        dBText.set_LayerType(geometryType)
        return dBText

    @staticmethod
    def smethod_144(point3d_0, constructionLayer):
        point2d = Point3D(point3d_0.get_X(), point3d_0.get_Y())
        point2d1 = MathHelper.distanceBearingPoint(point2d, 0.785398163397448, 300 )#* ApplicationSettings.LocateArrowScaleFactor)
        point2d2 = MathHelper.distanceBearingPoint(point2d1, 0.785398163397448, 600)# * ApplicationSettings.LocateArrowScaleFactor)
        polylineArea = PolylineArea([point2d, point2d1, point2d2])

        point0 = point2d2
        point1 = point2d
        point2 = MathHelper.distanceBearingPoint(point2d1, 0.785398163397448 - Unit.ConvertDegToRad(90), 70)
        point3 = point2d
        point4 = MathHelper.distanceBearingPoint(point2d1, 0.785398163397448 + Unit.ConvertDegToRad(90), 70)
        # point3 = MathHelper.distanceBearingPoint(point2d2, 0.785398163397448 + Unit.ConvertDegToRad(90), 100)
        # point6 = MathHelper.distanceBearingPoint(point2d1, 0.785398163397448 - Unit.ConvertDegToRad(90), 300)
        # point5 = MathHelper.distanceBearingPoint(point2d1, 0.785398163397448 - Unit.ConvertDegToRad(90), 100)
        # point4 = MathHelper.distanceBearingPoint(point2d2, 0.785398163397448 - Unit.ConvertDegToRad(90), 100)
        # polylineArea = PolylineArea([point0, point1, point2, point3, point4, point5, point6, point0])
        lineGeom = QgsGeometry.fromPolyline([point0, point1, point2, point3, point4])
        AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [point0, point1, point2, point3, point4])
        return lineGeom

    @staticmethod
    def smethod_145(point3dCollection, constructionLayer ):
        geomList = []
        # for point3d in point3dCollection:
        #     geomList.append(AcadHelper.smethod_144(point3d, constructionLayer))
        num = 0
        origin = None
        maxPoint = None

        for point3d in point3dCollection:
            boundingBox = AcadHelper.smethod_144(point3d, constructionLayer).boundingBox()

            if (num != 0):
                origin = MathHelper.smethod_178(origin, Point3D(boundingBox.xMinimum(), boundingBox.yMinimum()))
                maxPoint = MathHelper.smethod_180(maxPoint, Point3D(boundingBox.xMaximum(), boundingBox.yMaximum()))
            else:
                origin = Point3D(boundingBox.xMinimum(), boundingBox.yMinimum())
                maxPoint = Point3D(boundingBox.xMaximum(), boundingBox.yMaximum())
            num += 1


        extent = QgsRectangle(origin, maxPoint)

        centerPoint = Point3D((origin.get_X() + maxPoint.get_X()) / 2, (origin.get_Y() + maxPoint.get_Y()) / 2)
        QgisHelper.zoomExtent(centerPoint, extent, 2)

        # for geom in geomList:
        #     AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, geom.asPolyline())

    @staticmethod
    def smethod_142(string_0, point3d_0, double_0, attachmentPoint_0):
        mText = DBText()
        mText.set_TextString(string_0)
        mText.set_Position(point3d_0)
        # mText.set_TextHeight(double_0)
        # mText.set_Width(mText.get_ActualWidth() + mText.get_ActualWidth() / 10)
        # mText.set_Attachment(attachmentPoint_0)
        return mText
    
    @staticmethod
    def smethod_142_v15(string_0, point3d_0, double_0, textHorizontalMode_0):
        dBText = DBText()
        dBText.set_TextString(string_0)
        dBText.set_Position(point3d_0)
        dBText.set_Height(double_0)
        dBText.set_HorizontalMode(textHorizontalMode_0)
        dBText.set_AlignmentPoint(point3d_0)
        return dBText
    
    @staticmethod
    def smethod_153_v15(point3dCollection_0, point3dCollection_1, layer):
        return AcadHelper.smethod_157_v15(point3dCollection_0, point3dCollection_1, layer, -1, True)

    @staticmethod
    def smethod_157_v15(point3dCollection_0, point3dCollection_1, layer, int0, bool_0):
        if (bool_0):
            point3dCollection_0 = Point3dCollection.smethod_147(point3dCollection_0, True)
            point3dCollection_1 = Point3dCollection.smethod_147(point3dCollection_1, True)
        # if (point3dCollection_0.get_Count() != point3dCollection_1.get_Count()):
        #     raise Messages.ERR_NUMBER_OF_VERTICES_MUST_BE_EQUAL
            # throw new ArgumentException(Messages.ERR_NUMBER_OF_VERTICES_MUST_BE_EQUAL, "innerPoints, outerPoints")
        count = point3dCollection_0.get_Count()
        if (count < 2):
            raise Messages.ERR_INSUFFICIENT_NUMBER_OF_VERTICES
        AcadHelper.setGeometryAndAttributesInLayer(layer, point3dCollection_0)
        AcadHelper.setGeometryAndAttributesInLayer(layer, point3dCollection_1)
            # throw new ArgumentException(Messages.ERR_INSUFFICIENT_NUMBER_OF_VERTICES, "innerPoints, outerPoints")
        # PolygonMesh polygonMesh = new PolygonMesh()
        # polygonMesh.set_PolyMeshType(0)
        # polygonMesh.set_MSize((short)count)
        # polygonMesh.set_NSize(2)
        # polygonMesh.SetDatabaseDefaults()
        # if (!string.IsNullOrEmpty(string_0))
        # {
        #     polygonMesh.set_Layer(string_0)
        # }
        # if (int_0 >= 0)
        # {
        #     polygonMesh.set_ColorIndex(int_0)
        # }
        # ObjectId objectId = blockTableRecord_0.AppendEntity(polygonMesh)
        # transaction_0.AddNewlyCreatedDBObject(polygonMesh, true)
        # for (int i = 0 i < count i++)
        # {
        #     PolygonMeshVertex polygonMeshVertex = new PolygonMeshVertex(point3dCollection_0.get_Item(i))
        #     polygonMeshVertex.SetDatabaseDefaults()
        #     if (!string.IsNullOrEmpty(string_0))
        #     {
        #         polygonMeshVertex.set_Layer(string_0)
        #     }
        #     if (int_0 >= 0)
        #     {
        #         polygonMeshVertex.set_ColorIndex(int_0)
        #     }
        #     polygonMesh.AppendVertex(polygonMeshVertex)
        #     transaction_0.AddNewlyCreatedDBObject(polygonMeshVertex, true)
        #     polygonMeshVertex = new PolygonMeshVertex(point3dCollection_1.get_Item(i))
        #     polygonMeshVertex.SetDatabaseDefaults()
        #     if (!string.IsNullOrEmpty(string_0))
        #     {
        #         polygonMeshVertex.set_Layer(string_0)
        #     }
        #     if (int_0 >= 0)
        #     {
        #         polygonMeshVertex.set_ColorIndex(int_0)
        #     }
        #     polygonMesh.AppendVertex(polygonMeshVertex)
        #     transaction_0.AddNewlyCreatedDBObject(polygonMeshVertex, true)
        # }
        # return objectId


class SelectLine(QgsMapTool):

    def __init__(self, canvas, dlg):
        self.mCanvas = canvas
        # self.areaType = areaType
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
        self.dlg = dlg
#     QgsRubberBand* mRubberBand
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
                typeName = selectedFeatures[0].attribute("Type").toString()
                if typeName == "Line":
                    # if self.dlg != None:
                    #     self.dlg.show()
                    self.emit(SIGNAL("outputResult"), geom, self)
                else:
                    define._messageLabel.setText(Messages.ONLY_LINE_SEGMENTS_ALLOWED)

                pass

            del selectGeom

            self.mRubberBand.reset( QGis.Polygon )
            del self.mRubberBand
            self.mRubberBand = None
        self.mDragging = False

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

