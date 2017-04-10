'''
Created on 14 Jun 2014

@author: Administrator
'''
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QString, SIGNAL

from qgis.core import QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsVectorFileWriter

from FlightPlanner.RnavDmeUpdateArea.ui_RnavDmeUpdateArea0 import Ui_RnavDmeUpdateAreaDlg
from FlightPlanner.FlightPlanBaseSimpleDlg import FlightPlanBaseSimpleDlg
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.types import DistanceUnits, Point3D
from FlightPlanner.helpers import MathHelper, Distance
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.types import SurfaceTypes
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.AcadHelper import AcadHelper
import define
import math

class RnavDmeUpdateAreaDlg(FlightPlanBaseSimpleDlg):    
    def __init__(self, parent):
        FlightPlanBaseSimpleDlg.__init__(self, parent)
        self.setObjectName("RnavDmeUpdateAreaDlg")
        self.surfaceType = SurfaceTypes.DmeUpdateArea
                
        self.initParametersPan()
        self.setWindowTitle("DME Update Area Construction")
        self.resize(450, 370)
        QgisHelper.matchingDialogSize(self, 550, 500)

        self.vorDmeFeatureArray1 = dict()
        self.currentLayer = define._canvas.currentLayer()
        self.initBasedOnCmb1()

        self.vorDmeFeatureArray = dict()
        self.initBasedOnCmb()
    def initBasedOnCmb1(self):

        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.vorDmeFeatureArray1 = self.basedOnCmbFill1(self.currentLayer, self.parametersPanel.cmbBasedOn1, self.parametersPanel.pnlDme1)
    def basedOnCmbFill1(self, layer, basedOnCmbObj, vorDmePositionPanelObj):
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')
        vorDmeList = []
        vorDmeFeatureList = []
        if idx >= 0:
            featIter = layer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idx].toString()
                attrValue = QString(attrValue)
                attrValue = attrValue.replace(" ", "")
                attrValue = attrValue.replace("/", "")
                attrValue = attrValue.toUpper()
                if attrValue == "DME":
                    vorDmeList.append(attrValue)
                    vorDmeFeatureList.append(feat)
            if len(vorDmeList) != 0:

                i = -1
                basedOnCmbObjItems = []
                resultfeatDict = dict()
                for feat in vorDmeFeatureList:
                    typeValue = feat.attributes()[idx].toString()
                    nameValue = feat.attributes()[idxName].toString()
                    basedOnCmbObjItems.append(typeValue + " " + nameValue)
                    resultfeatDict.__setitem__(typeValue + " " + nameValue, feat)
                basedOnCmbObjItems.sort()
                basedOnCmbObj.Items = basedOnCmbObjItems
                basedOnCmbObj.SelectedIndex = 0

                # if idxAttributes
                feat = resultfeatDict.__getitem__(basedOnCmbObjItems[0])
                attrValue = feat.attributes()[idxLat].toDouble()
                lat = attrValue[0]

                attrValue = feat.attributes()[idxLong].toDouble()
                long = attrValue[0]

                attrValue = feat.attributes()[idxAltitude].toDouble()
                alt = attrValue[0]

                vorDmePositionPanelObj.Point3d = Point3D(long, lat, alt)
                self.connect(basedOnCmbObj, SIGNAL("Event_0"), self.basedOnCmbObj_Event_01)

                return resultfeatDict
        return dict()
    def basedOnCmbObj_Event_01(self):
        if self.currentLayer == None or not self.currentLayer.isValid():
            return
        layer = self.currentLayer
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')

        feat = self.vorDmeFeatureArray1.__getitem__(self.parametersPanel.cmbBasedOn1.SelectedItem)
        attrValue = feat.attributes()[idxLat].toDouble()
        lat = attrValue[0]

        attrValue = feat.attributes()[idxLong].toDouble()
        long = attrValue[0]

        attrValue = feat.attributes()[idxAltitude].toDouble()
        alt = attrValue[0]

        self.parametersPanel.pnlDme1.Point3d = Point3D(long, lat, alt)


    def initBasedOnCmb(self):
        # self.currentLayer = define._canvas.currentLayer()
        if self.currentLayer != None and self.currentLayer.isValid():
            self.vorDmeFeatureArray = self.basedOnCmbFill(self.currentLayer, self.parametersPanel.cmbBasedOn2, self.parametersPanel.pnlDme2)
    def basedOnCmbFill(self, layer, basedOnCmbObj, vorDmePositionPanelObj):
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')
        vorDmeList = []
        vorDmeFeatureList = []
        if idx >= 0:
            featIter = layer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idx].toString()
                attrValue = QString(attrValue)
                attrValue = attrValue.replace(" ", "")
                attrValue = attrValue.replace("/", "")
                attrValue = attrValue.toUpper()
                if attrValue == "DME":
                    vorDmeList.append(attrValue)
                    vorDmeFeatureList.append(feat)
            if len(vorDmeList) != 0:

                i = -1
                basedOnCmbObjItems = []
                resultfeatDict = dict()
                for feat in vorDmeFeatureList:
                    typeValue = feat.attributes()[idx].toString()
                    nameValue = feat.attributes()[idxName].toString()
                    basedOnCmbObjItems.append(typeValue + " " + nameValue)
                    resultfeatDict.__setitem__(typeValue + " " + nameValue, feat)
                basedOnCmbObjItems.sort()
                basedOnCmbObj.Items = basedOnCmbObjItems
                basedOnCmbObj.SelectedIndex = 0

                # if idxAttributes
                feat = resultfeatDict.__getitem__(basedOnCmbObjItems[0])
                attrValue = feat.attributes()[idxLat].toDouble()
                lat = attrValue[0]

                attrValue = feat.attributes()[idxLong].toDouble()
                long = attrValue[0]

                attrValue = feat.attributes()[idxAltitude].toDouble()
                alt = attrValue[0]

                vorDmePositionPanelObj.Point3d = Point3D(long, lat, alt)
                self.connect(basedOnCmbObj, SIGNAL("Event_0"), self.basedOnCmbObj_Event_0)

                return resultfeatDict
        return dict()
    def basedOnCmbObj_Event_0(self):
        if self.currentLayer == None or not self.currentLayer.isValid():
            return
        layer = self.currentLayer
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')

        feat = self.vorDmeFeatureArray.__getitem__(self.parametersPanel.cmbBasedOn2.SelectedItem)
        attrValue = feat.attributes()[idxLat].toDouble()
        lat = attrValue[0]

        attrValue = feat.attributes()[idxLong].toDouble()
        long = attrValue[0]

        attrValue = feat.attributes()[idxAltitude].toDouble()
        alt = attrValue[0]

        self.parametersPanel.pnlDme2.Point3d = Point3D(long, lat, alt)

    def btnConstruct_Click(self):
        flag = FlightPlanBaseSimpleDlg.btnConstruct_Click(self)
        if not flag:
            return

        # mapUnits = define._canvas.mapUnits()
        constructionLayer = None
        if self.parametersPanel.cmbConstructionType.currentText() == "2D":
            constructionLayer = AcadHelper.createVectorLayer(SurfaceTypes.DmeUpdateArea)
        #     if define._mapCrs == None:
        #         if mapUnits == QGis.Meters:
        #             constructionLayer = QgsVectorLayer("linestring?crs=EPSG:32633", SurfaceTypes.DmeUpdateArea, "memory")
        #         else:
        #             constructionLayer = QgsVectorLayer("linestring?crs=EPSG:4326", SurfaceTypes.DmeUpdateArea, "memory")
        #     else:
        #         constructionLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), SurfaceTypes.DmeUpdateArea, "memory")
        #     shpPath = ""
        #     if define.obstaclePath != None:
        #         shpPath = define.obstaclePath
        #     elif define.xmlPath != None:
        #         shpPath = define.xmlPath
        #     else:
        #         shpPath = define.appPath
        #     er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + QString(SurfaceTypes.DmeUpdateArea).replace(" ", "") + ".shp", "utf-8", constructionLayer.crs())
        #     constructionLayer = QgsVectorLayer(shpPath + "/" + QString(SurfaceTypes.DmeUpdateArea).replace(" ", "") + ".shp", SurfaceTypes.DmeUpdateArea, "ogr")

            point3d = self.parametersPanel.pnlDme1.Point3d
            point3d1 = self.parametersPanel.pnlDme2.Point3d
            num = MathHelper.calcDistance(point3d, point3d1)
            num1 = num * 0.5
            num2 = math.sqrt(num * num - num1 * num1)
            num3 = MathHelper.getBearing(point3d, point3d1)
            point3d2 = MathHelper.distanceBearingPoint(point3d, num3, 0.5 * num)
            point3d3 = MathHelper.distanceBearingPoint(point3d2, num3 - 1.5707963267949, num2)
            point3d4 = MathHelper.distanceBearingPoint(point3d2, num3 + 1.5707963267949, num2)
            distance = Distance(float(self.parametersPanel.txtDoc1.text()), DistanceUnits.NM)
            metres = distance.Metres
            distance1 = Distance(float(self.parametersPanel.txtDoc2.text()), DistanceUnits.NM)
            metres1 = distance1.Metres
            
            circlePointList = MathHelper.constructCircle(point3d, metres, 100)
            circlePointList1 = MathHelper.constructCircle(point3d1, metres1, 100)
            
            
            circlePointList2 = MathHelper.constructCircle(point3d3, num, 100)
            circlePointList3 = MathHelper.constructCircle(point3d4, num, 100)
            circlePointList4 = MathHelper.constructCircle(point3d, 1900, 100)
            circlePointList5 = MathHelper.constructCircle(point3d1, 1900, 100)
            
            # constructionLayer.startEditing()
            
            polygon = QgsGeometry.fromPolygon([circlePointList])
    #         feature0 = QgsFeature()
    #         feature0.setGeometry(polygon)
    #         constructionLayer.addFeature(feature0)
            polygon = QgsGeometry.fromPolygon([circlePointList])
            polygon1 = QgsGeometry.fromPolygon([circlePointList1])
            polygon2 = QgsGeometry.fromPolygon([circlePointList2])
            polygon3 = QgsGeometry.fromPolygon([circlePointList3])
            polygon4 = QgsGeometry.fromPolygon([circlePointList4])
            polygon5 = QgsGeometry.fromPolygon([circlePointList5])
            
            polygon0 = polygon.intersection(polygon1)
            polygon0 = polygon0.intersection(polygon2)
            polygon0 = polygon0.difference(polygon3)
            polygon0 = polygon0.difference(polygon4)
            polygon0 = polygon0.difference(polygon5)
            
            pointArray = QgsGeometry.asPolygon(polygon0)
            
            # feature1 = QgsFeature()
            # feature1.setGeometry(QgsGeometry.fromPolyline(pointArray[0]))
            # constructionLayer.addFeature(feature1)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, pointArray[0])

            
            polygon0 = polygon.intersection(polygon1)
            polygon0 = polygon0.intersection(polygon3)
            polygon0 = polygon0.difference(polygon2)
            polygon0 = polygon0.difference(polygon4)
            polygon0 = polygon0.difference(polygon5)
            
            pointArray = QgsGeometry.asPolygon(polygon0)
            
            # feature1 = QgsFeature()
            # feature1.setGeometry(QgsGeometry.fromPolyline(pointArray[0]))
            #
            # constructionLayer.addFeature(feature1)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, pointArray[0])

            
            
            
            # constructionLayer.commitChanges()
        else:
            constructionLayer = AcadHelper.createVectorLayer(SurfaceTypes.DmeUpdateArea, QGis.Polygon)
            # if define._mapCrs == None:
            #     if mapUnits == QGis.Meters:
            #         constructionLayer = QgsVectorLayer("polygon?crs=EPSG:32633", SurfaceTypes.DmeUpdateArea, "memory")
            #     else:
            #         constructionLayer = QgsVectorLayer("polygon?crs=EPSG:4326", SurfaceTypes.DmeUpdateArea, "memory")
            # else:
            #     constructionLayer = QgsVectorLayer("polygon?crs=%s"%define._mapCrs.authid (), SurfaceTypes.DmeUpdateArea, "memory")
            # shpPath = ""
            # if define.obstaclePath != None:
            #     shpPath = define.obstaclePath
            # elif define.xmlPath != None:
            #     shpPath = define.xmlPath
            # else:
            #     shpPath = define.appPath
            # er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + QString(SurfaceTypes.DmeUpdateArea).replace(" ", "") + ".shp", "utf-8", constructionLayer.crs())
            # constructionLayer = QgsVectorLayer(shpPath + "/" + QString(SurfaceTypes.DmeUpdateArea).replace(" ", "") + ".shp", SurfaceTypes.DmeUpdateArea, "ogr")

            point3d = self.parametersPanel.pnlDme1.Point3d
            point3d1 = self.parametersPanel.pnlDme2.Point3d
            num = MathHelper.calcDistance(point3d, point3d1)
            num1 = num * 0.5
            num2 = math.sqrt(num * num - num1 * num1)
            num3 = MathHelper.getBearing(point3d, point3d1)
            point3d2 = MathHelper.distanceBearingPoint(point3d, num3, 0.5 * num)
            point3d3 = MathHelper.distanceBearingPoint(point3d2, num3 - 1.5707963267949, num2)
            point3d4 = MathHelper.distanceBearingPoint(point3d2, num3 + 1.5707963267949, num2)
            distance = Distance(float(self.parametersPanel.txtDoc1.text()), DistanceUnits.NM)
            metres = distance.Metres
            distance1 = Distance(float(self.parametersPanel.txtDoc2.text()), DistanceUnits.NM)
            metres1 = distance1.Metres
            
            circlePointList = MathHelper.constructCircle(point3d, metres, 100)
            circlePointList1 = MathHelper.constructCircle(point3d1, metres1, 100)
            
            
            circlePointList2 = MathHelper.constructCircle(point3d3, num, 100)
            circlePointList3 = MathHelper.constructCircle(point3d4, num, 100)
            circlePointList4 = MathHelper.constructCircle(point3d, 1900, 100)
            circlePointList5 = MathHelper.constructCircle(point3d1, 1900, 100)
            
            # constructionLayer.startEditing()
            
            polygon = QgsGeometry.fromPolygon([circlePointList])
    #         feature0 = QgsFeature()
    #         feature0.setGeometry(polygon)
    #         constructionLayer.addFeature(feature0)
            polygon = QgsGeometry.fromPolygon([circlePointList])
            polygon1 = QgsGeometry.fromPolygon([circlePointList1])
            polygon2 = QgsGeometry.fromPolygon([circlePointList2])
            polygon3 = QgsGeometry.fromPolygon([circlePointList3])
            polygon4 = QgsGeometry.fromPolygon([circlePointList4])
            polygon5 = QgsGeometry.fromPolygon([circlePointList5])
            
            polygon0 = polygon.intersection(polygon1)
            polygon0 = polygon0.intersection(polygon2)
            polygon0 = polygon0.difference(polygon3)
            polygon0 = polygon0.difference(polygon4)
            polygon0 = polygon0.difference(polygon5)
            # feature1 = QgsFeature()
            # feature1.setGeometry(polygon0)
            # constructionLayer.addFeature(feature1)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polygon0.asPolygon()[0])

            
            polygon0 = polygon.intersection(polygon1)
            polygon0 = polygon0.intersection(polygon3)
            polygon0 = polygon0.difference(polygon2)
            polygon0 = polygon0.difference(polygon4)
            polygon0 = polygon0.difference(polygon5)
            # feature2 = QgsFeature()
            # feature2.setGeometry(polygon0)
            # constructionLayer.addFeature(feature2)

            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polygon0.asPolygon()[0])
            
            
            
            # constructionLayer.commitChanges()
        
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.DmeUpdateArea)
        self.resultLayerList = [constructionLayer]
        QgisHelper.zoomToLayers([constructionLayer])

    def initParametersPan(self):
        ui = Ui_RnavDmeUpdateAreaDlg()
        self.parametersPanel = ui
        FlightPlanBaseSimpleDlg.initParametersPan(self)
        
        '''init panel'''
        self.parametersPanel.pnlDme1 = PositionPanel(ui.gbDme1)
#         self.parametersPanel.pnlDme1.groupBox.setTitle("DME Position")
        self.parametersPanel.pnlDme1.btnCalculater.hide()
        self.parametersPanel.pnlDme1.hideframe_Altitude()
        self.parametersPanel.pnlDme1.setObjectName("positionDme1")        
        ui.vl_Dme1.insertWidget(1, self.parametersPanel.pnlDme1)
        
        self.parametersPanel.pnlDme2 = PositionPanel(ui.gbDme2)
#         self.parametersPanel.pnlDme1.groupBox.setTitle("DME Position")
        self.parametersPanel.pnlDme2.btnCalculater.hide()
        self.parametersPanel.pnlDme2.hideframe_Altitude()
        self.parametersPanel.pnlDme2.setObjectName("positionDme2")        
        ui.vl_Dme2.insertWidget(1, self.parametersPanel.pnlDme2)
        
        
        self.parametersPanel.cmbConstructionType.addItems(["2D", "3D"])
        '''signal and slost'''
        self.parametersPanel.btnMesureDoc1.clicked.connect(self.measureToolDoc1)
        self.parametersPanel.btnMesureDoc2.clicked.connect(self.measureToolDoc2)
        
    def measureToolDoc1(self):
        measureThrFaf = MeasureTool(define._canvas, self.parametersPanel.txtDoc1, DistanceUnits.NM)
        define._canvas.setMapTool(measureThrFaf)
        
    def measureToolDoc2(self):
        measureThrFaf = MeasureTool(define._canvas, self.parametersPanel.txtDoc2, DistanceUnits.NM)
        define._canvas.setMapTool(measureThrFaf)