# -*- coding: UTF-8 -*-
'''
Created on 30 Jun 2015

@author: Administrator
'''
from qgis.core import QGis, QgsVectorLayer, QgsGeometry, QgsFeature, QgsVectorFileWriter
from PyQt4.QtGui import QFileDialog, QStandardItem, QMessageBox
from PyQt4.QtCore import SIGNAL,Qt, QCoreApplication, QString
from FlightPlanner.types import ConstructionType, CriticalObstacleType, ObstacleTableColumnType,\
     TurnDirection, ObstacleAreaResult
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, ComplexObstacleArea, SecondaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.Enroute.EnrouteStraight.ui_EnrouteStraight import Ui_EnrouteStraight
from FlightPlanner.DataHelper import DataHelper

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import Point3D, SurfaceTypes
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.helpers import MathHelper, Unit
import define
import math

class EnrouteStraightDlg(FlightPlanBaseDlg):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("HoldingRnp")
        self.surfaceType = SurfaceTypes.EnrouteStraight
        self.copApplicable = True
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.EnrouteStraight)
                
        self.resize(540, 550)
        QgisHelper.matchingDialogSize(self, 670, 700)

        self.vorDmeFeatureArray1 = dict()
        self.currentLayer = define._canvas.currentLayer()
        self.resultLayerList = []
        self.initBasedOnCmb1()

        self.vorDmeFeatureArray = dict()
        self.initBasedOnCmb()

    def initBasedOnCmb1(self):
        # self.currentLayer = define._canvas.currentLayer()
        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.vorDmeFeatureArray1 = self.basedOnCmbFill1(self.currentLayer, self.parametersPanel.cmbBasedOn1, self.parametersPanel.pnlNavAid1)
    def basedOnCmbFill1(self, layer, basedOnCmbObj, vorDmePositionPanelObj):
        basedOnCmbObj.Clear()
        vorDmePositionPanelObj.Point3d = None
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
                if self.parametersPanel.cmbNavAidType1.SelectedIndex == 0:
                    if attrValue == "VOR" or attrValue == "VORDME" or attrValue == "VORTAC" or attrValue == "TACAN":
                        vorDmeList.append(attrValue)
                        vorDmeFeatureList.append(feat)
                else:
                    if attrValue == "NDB" or attrValue == "NDBDME":
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
                try:
                    feat = resultfeatDict.__getitem__(basedOnCmbObjItems[0])
                except:
                    return dict()
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
        if len(self.vorDmeFeatureArray) == 0:
            return
        layer = self.currentLayer
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')
        try:
            feat = self.vorDmeFeatureArray.__getitem__(self.parametersPanel.cmbBasedOn1.SelectedItem)
        except:
            return
        attrValue = feat.attributes()[idxLat].toDouble()
        lat = attrValue[0]

        attrValue = feat.attributes()[idxLong].toDouble()
        long = attrValue[0]

        attrValue = feat.attributes()[idxAltitude].toDouble()
        alt = attrValue[0]

        self.parametersPanel.pnlNavAid1.Point3d = Point3D(long, lat, alt)

    def initBasedOnCmb(self):
        # self.currentLayer = define._canvas.currentLayer()
        if self.currentLayer != None and self.currentLayer.isValid():
            self.vorDmeFeatureArray = self.basedOnCmbFill(self.currentLayer, self.parametersPanel.cmbBasedOn2, self.parametersPanel.pnlNavAid2)
    def basedOnCmbFill(self, layer, basedOnCmbObj, vorDmePositionPanelObj):
        basedOnCmbObj.Clear()
        vorDmePositionPanelObj.Point3d = None
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
                if self.parametersPanel.cmbNavAidType2.SelectedIndex == 0:
                    if attrValue == "VOR" or attrValue == "VORDME" or attrValue == "VORTAC" or attrValue == "TACAN":
                        vorDmeList.append(attrValue)
                        vorDmeFeatureList.append(feat)
                else:
                    if attrValue == "NDB" or attrValue == "NDBDME":
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
                try:
                    feat = resultfeatDict.__getitem__(basedOnCmbObjItems[0])
                except:
                    return dict()
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
        if len(self.vorDmeFeatureArray) == 0:
            return
        layer = self.currentLayer
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')
        try:
            feat = self.vorDmeFeatureArray.__getitem__(self.parametersPanel.cmbBasedOn2.SelectedItem)
        except:
            return
        attrValue = feat.attributes()[idxLat].toDouble()
        lat = attrValue[0]

        attrValue = feat.attributes()[idxLong].toDouble()
        long = attrValue[0]

        attrValue = feat.attributes()[idxAltitude].toDouble()
        alt = attrValue[0]

        self.parametersPanel.pnlNavAid2.Point3d = Point3D(long, lat, alt)

        
    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return  
#         self.filterList = []
#         for taaArea in self.taaCalculationAreas:
#             self.filterList.append(taaArea.title)
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, self.surfaceType, self.ui.tblObstacles, None, parameterList, resultHideColumnNames)
#         self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
    
    def getParameterList(self):
        parameterList = []
        parameterList.append(("General", "group"))
        parameterList.append(("Navigational Aid 1", "group"))
        parameterList.append(("Type", self.parametersPanel.cmbNavAidType1.SelectedItem))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlNavAid1.txtPointX.text()), float(self.parametersPanel.pnlNavAid1.txtPointY.text()))
        
        parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
        parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
        parameterList.append(("X", self.parametersPanel.pnlNavAid1.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlNavAid1.txtPointY.text()))
        
        parameterList.append(("Navigational Aid 2", "group"))
        parameterList.append(("Type", self.parametersPanel.cmbNavAidType2.SelectedItem))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlNavAid2.txtPointX.text()), float(self.parametersPanel.pnlNavAid2.txtPointY.text()))
        
        parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
        parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
        parameterList.append(("X", self.parametersPanel.pnlNavAid2.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlNavAid2.txtPointY.text()))
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Change Over Point", "group"))
        if self.parametersPanel.frameCOP.isVisible():
            parameterList.append(("Left", self.parametersPanel.lblLeft.text()))
            parameterList.append(("Left", self.parametersPanel.lblRight.text()))
        else:
            parameterList.append(("", self.parametersPanel.lblNA.text()))
        parameterList.append(("Primary Moc", str(self.parametersPanel.txtPrimaryMoc.Value.Metres) + "m"))
        parameterList.append(("Enroute Altitude", str(self.parametersPanel.txtEnrouteAltitude.Value.Feet) + "ft"))
        parameterList.append(("MOCmultipiler", str(self.parametersPanel.mocSpinBox.value())))
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstruction.currentText()))
        
       
        parameterList.append(("Results / Checked Obstacles", "group"))   
        parameterList.append(("Checked Obstacles", "group"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        return parameterList
    def initObstaclesModel(self):
        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
#         self.obstaclesModel = EnrouteStraightObstacles(self.surfaceArea)
        
        return FlightPlanBaseDlg.initObstaclesModel(self)
    def btnEvaluate_Click(self):
        num = None;
        num1 = None;
        num2 = None;
        num3 = None;
#         if (!AcadHelper.Ready)
#         {
#             return;
#         }
#         if (!self.method_27(false))
#         {
#             return;
#         }
        point3d = self.parametersPanel.pnlNavAid1.Point3d;
        point3d1 = self.parametersPanel.pnlNavAid2.Point3d;
        num4 = MathHelper.getBearing(point3d, point3d1);
        num5 = MathHelper.getBearing(point3d1, point3d);
        point3dCollection, num, num1, num2, num3 = self.method_37(point3d, point3d1);
        complexObstacleArea = ComplexObstacleArea();
        polylineArea = PolylineArea()
        polylineArea.Add(PolylineAreaPoint(point3dCollection[1]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[19]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[17]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[21]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[23]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[5], MathHelper.smethod_57(TurnDirection.Left, point3dCollection[5], point3dCollection[7], point3d1)))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[7]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[24]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[22]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[18]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[20]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[3], MathHelper.smethod_57(TurnDirection.Left, point3dCollection[3], point3dCollection[1], point3d)))
        primaryObstacleArea = PrimaryObstacleArea(polylineArea);
        polylineArea = PolylineArea()
        polylineArea.Add(PolylineAreaPoint(point3dCollection[0]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[13]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[11]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[12]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[15]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[4], MathHelper.smethod_57(TurnDirection.Left, point3dCollection[4], point3dCollection[6], point3d1)))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[6]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[16]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[10]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[9]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[14]))
        polylineArea.Add(PolylineAreaPoint(point3dCollection[2], MathHelper.smethod_57(TurnDirection.Left, point3dCollection[2], point3dCollection[0], point3d)))
        complexObstacleArea.method_0(PrimaryObstacleArea(polylineArea), num4);
        point3d2 = MathHelper.distanceBearingPoint(point3d, num5, MathHelper.calcDistance(point3d, point3dCollection[0]));
        point3d3 = MathHelper.distanceBearingPoint(point3d, num5, MathHelper.calcDistance(point3d, point3dCollection[1]));
        complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection[0], point3d2, point3dCollection[2], point3dCollection[1], None, point3d3, point3dCollection[3]));
        point3d2 = MathHelper.distanceBearingPoint(point3d1, num4, MathHelper.calcDistance(point3d1, point3dCollection[6]));
        point3d3 = MathHelper.distanceBearingPoint(point3d1, num4, MathHelper.calcDistance(point3d1, point3dCollection[7]));
        complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection[6], point3d2, point3dCollection[4], point3dCollection[7], None, point3d3, point3dCollection[5]));
        complexObstacleArea.method_0(SecondaryObstacleArea(point3dCollection[0], point3dCollection[13], point3dCollection[1], point3dCollection[19]), num4);
        complexObstacleArea.method_0(SecondaryObstacleArea(point3dCollection[13], point3dCollection[11], point3dCollection[19], point3dCollection[17]), num4);
        complexObstacleArea.method_0(SecondaryObstacleArea(point3dCollection[11], point3dCollection[15], point3dCollection[17], point3dCollection[23]), num4);
        complexObstacleArea.method_0(SecondaryObstacleArea(point3dCollection[15], point3dCollection[4], point3dCollection[23], point3dCollection[5]), num4);
        complexObstacleArea.method_0(SecondaryObstacleArea(point3dCollection[2], point3dCollection[14], point3dCollection[3], point3dCollection[20]), num4);
        complexObstacleArea.method_0(SecondaryObstacleArea(point3dCollection[14], point3dCollection[9], point3dCollection[20], point3dCollection[18]), num4);
        complexObstacleArea.method_0(SecondaryObstacleArea(point3dCollection[9], point3dCollection[16], point3dCollection[18], point3dCollection[24]), num4);
        complexObstacleArea.method_0(SecondaryObstacleArea(point3dCollection[16], point3dCollection[6], point3dCollection[24], point3dCollection[7]), num4);
        
        self.obstaclesModel = EnrouteStraightObstacles(complexObstacleArea, self.parametersPanel.txtPrimaryMoc.Value, self.parametersPanel.txtEnrouteAltitude.Value)
#         EnrouteStraight.EnrouteStraightEvaluator enrouteStraightEvaluator = new EnrouteStraight.EnrouteStraightEvaluator(complexObstacleArea, self.pnlPrimaryMoc.Value, self.pnlEnrouteAltitude.Value);
#         self.method_29();
        return FlightPlanBaseDlg.btnEvaluate_Click(self)


    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        
        num = None;
        num1 = None;
        num2 = None;
        num3 = None;
        
        
        
        mapUnits = define._canvas.mapUnits()
        constructionLayer = None
        
        point3d = self.parametersPanel.pnlNavAid1.Point3d;
        point3d1 = self.parametersPanel.pnlNavAid2.Point3d;
        point3dCollection, num, num1, num2, num3 = self.method_37(point3d, point3d1);
        
        if (self.parametersPanel.cmbConstruction.currentText() != ConstructionType.Construct3D):
            resultPoint3dArrayList = []
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)

            point3dArray = [point3dCollection[1], point3dCollection[19], point3dCollection[17],\
                             point3dCollection[21], point3dCollection[23], point3dCollection[5],\
                              point3dCollection[7], point3dCollection[24], point3dCollection[22],\
                               point3dCollection[18], point3dCollection[20], point3dCollection[3]]
            polyline1 = PolylineArea(point3dArray);
            polyline1[5].set_Bulge(MathHelper.smethod_57(TurnDirection.Left, point3dCollection[5], point3dCollection[7], point3d1));
            polyline1[11].set_Bulge(MathHelper.smethod_57(TurnDirection.Left, point3dCollection[3], point3dCollection[1], point3d));
#             polyline1.smethod_158();
#             polyline1.set_Closed(True);
            resultPoint3dArrayList.append(polyline1)
#             AcadHelper.smethod_18(transaction, blockTableRecord, polyline1, constructionLayer);
            item1 = [point3dCollection[0], point3dCollection[13], point3dCollection[11],\
                      point3dCollection[12], point3dCollection[15], point3dCollection[4],\
                       point3dCollection[6], point3dCollection[16], point3dCollection[10],\
                        point3dCollection[9], point3dCollection[14], point3dCollection[2]]
            polyline1 = PolylineArea(item1);
            polyline1[5].set_Bulge(MathHelper.smethod_57(TurnDirection.Left, point3dCollection[4], point3dCollection[6], point3d1));
            polyline1[11].set_Bulge(MathHelper.smethod_57(TurnDirection.Left, point3dCollection[2], point3dCollection[0], point3d));
#             polyline1.smethod_158();
#             polyline1.set_Closed(True);
#             resultPolylineAreaList.append(polyline1)
            resultPoint3dArrayList.append(polyline1)
            resultPoint3dArray = [point3d, point3d1]
#             resultPolylineAreaList.append(PolylineArea([point3d, point3d1]))
#             AcadHelper.smethod_18(transaction, blockTableRecord, polyline1, constructionLayer);
#             AcadHelper.smethod_18(transaction, blockTableRecord, new Line(point3d, point3d1), constructionLayer);
#             AcadHelper.smethod_18(transaction, blockTableRecord, new DBPoint(point3dCollection[8)), constructionLayer);

            for polylineArea in resultPoint3dArrayList:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea, True)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, resultPoint3dArray)
        else:
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Polygon)
            resultPoint3dArrayList = []
            # if define._mapCrs == None:
            #     if mapUnits == QGis.Meters:
            #         constructionLayer = QgsVectorLayer("polygon?crs=EPSG:32633", self.surfaceType, "memory")
            #     else:
            #         constructionLayer = QgsVectorLayer("polygon?crs=EPSG:4326", self.surfaceType, "memory")
            # else:
            #     constructionLayer = QgsVectorLayer("polygon?crs=%s"%define._mapCrs.authid (), self.surfaceType, "memory")
            #
            # shpPath = ""
            # if define.obstaclePath != None:
            #     shpPath = define.obstaclePath
            # elif define.xmlPath != None:
            #     shpPath = define.xmlPath
            # else:
            #     shpPath = define.appPath
            # er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + QString(self.surfaceType).replace(" ", "") + ".shp", "utf-8", constructionLayer.crs())
            # constructionLayer = QgsVectorLayer(shpPath + "/" + QString(self.surfaceType).replace(" ", "") + ".shp", self.surfaceType, "ogr")

                
            metres = self.parametersPanel.txtPrimaryMoc.Value.Metres;
            metres1 = self.parametersPanel.txtEnrouteAltitude.Value.Metres;
            num4 = metres1 - metres;
            point3d2 = Point3D(point3d1.get_X() + 1, point3d1.get_Y() + 1)
            point3d3 = Point3D(point3d.get_X() + 1, point3d.get_Y() + 1)
            line = [point3d.smethod_167(metres1), point3d1.smethod_167(metres1), point3d2.smethod_167(metres1), point3d3.smethod_167(metres1), point3d.smethod_167(metres1)];
            resultPoint3dArrayList.append(line)
#             line.set_Thickness(-metres);
#             AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
            item = [point3dCollection[0], point3dCollection[13], point3dCollection[11],\
                     point3dCollection[12], point3dCollection[15], point3dCollection[4],\
                      point3dCollection[6], point3dCollection[16], point3dCollection[10],\
                       point3dCollection[9], point3dCollection[14], point3dCollection[2]];
            polyline = PolylineArea(item);
            polyline[5].set_Bulge(MathHelper.smethod_57(TurnDirection.Left, point3dCollection[4], point3dCollection[6], point3d1));
            polyline[11].set_Bulge(MathHelper.smethod_57(TurnDirection.Left, point3dCollection[2], point3dCollection[0], point3d));
            resultPoint3dArrayList.append(polyline.method_14_closed())
#             polyline.set_Elevation(num4);
#             polyline.smethod_158();
#             polyline.set_Closed(true);
#             DBObjectCollection dBObjectCollection = new DBObjectCollection();
#             dBObjectCollection.Add(polyline);
#             foreach (Entity entity in Autodesk.AutoCAD.DatabaseServices.Region.CreateFromCurves(dBObjectCollection))
#             {
#                 AcadHelper.smethod_18(transaction, blockTableRecord, entity, constructionLayer);
#             }
#             polyline.Dispose();
            point3d2 = point3dCollection[0].smethod_167(num4);
            point3d3 = point3dCollection[1].smethod_167(metres1);
            point3d4 = point3dCollection[19].smethod_167(metres1);
            point3d5 = point3dCollection[13].smethod_167(num4);
            resultPoint3dArrayList.append([point3d2, point3d3, point3d4, point3d5, point3d2])
#             AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3d2, point3d3, point3d4, point3d5, true, true, true, true), constructionLayer);
            point3d2 = point3dCollection[19].smethod_167(metres1);
            point3d3 = point3dCollection[13].smethod_167(num4);
            point3d4 = point3dCollection[11].smethod_167(num4);
            point3d5 = point3dCollection[17].smethod_167(metres1);
            resultPoint3dArrayList.append([point3d2, point3d3, point3d4, point3d5, point3d2])
#             AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3d2, point3d3, point3d4, point3d5, true, true, true, true), constructionLayer);
            point3d2 = point3dCollection[11].smethod_167(num4);
            point3d3 = point3dCollection[17].smethod_167(metres1);
            point3d4 = point3dCollection[23].smethod_167(metres1);
            point3d5 = point3dCollection[15].smethod_167(num4);
            resultPoint3dArrayList.append([point3d2, point3d3, point3d4, point3d5, point3d2])
#             AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3d2, point3d3, point3d4, point3d5, true, true, true, true), constructionLayer);
            point3d2 = point3dCollection[23].smethod_167(metres1);
            point3d3 = point3dCollection[15].smethod_167(num4);
            point3d4 = point3dCollection[4].smethod_167(num4);
            point3d5 = point3dCollection[5].smethod_167(metres1);
            resultPoint3dArrayList.append([point3d2, point3d3, point3d4, point3d5, point3d2])
#             AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3d2, point3d3, point3d4, point3d5, true, true, true, true), constructionLayer);
            point3d2 = point3dCollection[2].smethod_167(num4);
            point3d3 = point3dCollection[3].smethod_167(metres1);
            point3d4 = point3dCollection[20].smethod_167(metres1);
            point3d5 = point3dCollection[14].smethod_167(num4);
            resultPoint3dArrayList.append([point3d2, point3d3, point3d4, point3d5, point3d2])
#             AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3d2, point3d3, point3d4, point3d5, true, true, true, true), constructionLayer);
            point3d2 = point3dCollection[20].smethod_167(metres1);
            point3d3 = point3dCollection[14].smethod_167(num4);
            point3d4 = point3dCollection[9].smethod_167(num4);
            point3d5 = point3dCollection[22].smethod_167(metres1);
            resultPoint3dArrayList.append([point3d2, point3d3, point3d4, point3d5, point3d2])
#             AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3d2, point3d3, point3d4, point3d5, true, true, true, true), constructionLayer);
            point3d2 = point3dCollection[9].smethod_167(num4);
            point3d3 = point3dCollection[22].smethod_167(metres1);
            point3d4 = point3dCollection[24].smethod_167(metres1);
            point3d5 = point3dCollection[16].smethod_167(num4);
            resultPoint3dArrayList.append([point3d2, point3d3, point3d4, point3d5, point3d2])
#             AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3d2, point3d3, point3d4, point3d5, true, true, true, true), constructionLayer);
            point3d2 = point3dCollection[24].smethod_167(metres1);
            point3d3 = point3dCollection[16].smethod_167(num4);
            point3d4 = point3dCollection[6].smethod_167(num4);
            point3d5 = point3dCollection[7].smethod_167(metres1);
            resultPoint3dArrayList.append([point3d2, point3d3, point3d4, point3d5, point3d2])
#             AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3d2, point3d3, point3d4, point3d5, true, true, true, true), constructionLayer);
            point3dCollection1 = []
            point3dCollection2 = []
            num5 = MathHelper.getBearing(point3d, point3dCollection[1]);
            num6 = MathHelper.calcDistance(point3d, point3dCollection[0]);
            num7 = MathHelper.calcDistance(point3d, point3dCollection[1]);
            num8 = int((num7 * 3.14159265358979 / 100) + 1);
            for i in range(num8):
                num9 = 3.14159265358979 * (float(i) / float(num8));
                point3dCollection1.append(MathHelper.distanceBearingPoint(point3d, num5 + num9, num6).smethod_167(num4));
                point3dCollection2.append(MathHelper.distanceBearingPoint(point3d, num5 + num9, num7).smethod_167(metres1));
            point3dCollection1.append(point3dCollection2[0])
            point3dCollection2.append(point3dCollection2[0])
            polygonGeom1, polygonGeom2 = QgisHelper.smethod_146(point3dCollection1, point3dCollection2);
            resultPoint3dArrayList.append(polygonGeom1.asPolygon()[0])
            resultPoint3dArrayList.append(polygonGeom2.asPolygon()[0])
            point3dCollection1 = []
            point3dCollection2 = []
            num5 = MathHelper.getBearing(point3d1, point3dCollection[5]);
            num6 = MathHelper.calcDistance(point3d1, point3dCollection[4]);
            num7 = MathHelper.calcDistance(point3d1, point3dCollection[5]);
            num8 = int((num7 * 3.14159265358979 / 100) + 1);
            for j in range(num8):
                num10 = 3.14159265358979 * (float(j) / float(num8));
                point3dCollection1.append(MathHelper.distanceBearingPoint(point3d1, num5 - num10, num6).smethod_167(num4));
                point3dCollection2.append(MathHelper.distanceBearingPoint(point3d1, num5 - num10, num7).smethod_167(metres1));
            polygonGeom1, polygonGeom2 = QgisHelper.smethod_146(point3dCollection1, point3dCollection2);
            resultPoint3dArrayList.append(polygonGeom1.asPolygon()[0])
            resultPoint3dArrayList.append(polygonGeom2.asPolygon()[0])
            
            # constructionLayer.startEditing()
            
            for pointArray in resultPoint3dArrayList:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, PolylineArea(pointArray))
            #     feature = QgsFeature()
            #     feature.setGeometry(QgsGeometry.fromPolygon([pointArray]))
            #     constructionLayer.addFeature(feature)
            # constructionLayer.commitChanges()
            
#             AcadHelper.smethod_147(transaction, blockTableRecord, point3dCollection1, point3dCollection2, constructionLayer);
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.EnrouteStraight)
        self.resultLayerList = [constructionLayer]
        QgisHelper.zoomToLayers(self.resultLayerList)
        self.ui.btnEvaluate.setEnabled(True)

    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        
        return FlightPlanBaseDlg.uiStateInit(self)
    def initParametersPan(self):
        ui = Ui_EnrouteStraight()
        self.parametersPanel = ui
        
        
        FlightPlanBaseDlg.initParametersPan(self)        
        
        self.parametersPanel.lblNA.setText("Not applicable. positions too close")
        
        self.parametersPanel.pnlNavAid1 = PositionPanel(self.parametersPanel.gbNavAid1)
#         self.parametersPanel.pnlWaypoint.groupBox.setTitle("Waypoint Position")
        
        self.parametersPanel.pnlNavAid1.hideframe_Altitude()
        self.parametersPanel.pnlNavAid1.setObjectName("pnlNavAid1")
        self.parametersPanel.pnlNavAid1.btnCalculater.hide()
        self.parametersPanel.verticalLayoutNavAid1.addWidget(self.parametersPanel.pnlNavAid1)
        
        self.parametersPanel.pnlNavAid2 = PositionPanel(self.parametersPanel.gbNavAid12)
        self.parametersPanel.pnlNavAid2.hideframe_Altitude()
        self.parametersPanel.pnlNavAid2.setObjectName("pnlNavAid2")
        self.parametersPanel.pnlNavAid2.btnCalculater.hide()
        self.parametersPanel.verticalLayoutNavAid2.addWidget(self.parametersPanel.pnlNavAid2)
        
#         self.parametersPanel.pnlWind = WindPanel(self.parametersPanel.grbParameters)
#         self.parametersPanel.vLayout_grbParameters.insertWidget(5, self.parametersPanel.pnlWind)
#         self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
        
#         self.resize(460,600)
        self.parametersPanel.cmbConstruction.addItems(["2D", "3D"])
        self.parametersPanel.cmbNavAidType1.Items = ["VOR", "NDB"]
        self.parametersPanel.cmbNavAidType2.Items = ["VOR", "NDB"]
        
        self.parametersPanel.scrollBar.valueChanged.connect(self.method_32)
        self.connect(self.parametersPanel.pnlNavAid1, SIGNAL("positionChanged"), self.method_34)
        self.connect(self.parametersPanel.pnlNavAid2, SIGNAL("positionChanged"), self.method_34)
        self.connect(self.parametersPanel.cmbNavAidType1, SIGNAL("Event_0"), self.initBasedOnCmb1)
        self.connect(self.parametersPanel.cmbNavAidType2, SIGNAL("Event_0"), self.initBasedOnCmb)

        self.method_31(-1);
        self.method_32();
    def method_31(self, int_0):
        try:
            if (self.parametersPanel.pnlNavAid1.IsValid() and self.parametersPanel.pnlNavAid2.IsValid()):
                num = int(round(Unit.ConvertMeterToNM(MathHelper.calcDistance(self.parametersPanel.pnlNavAid1.Point3d, self.parametersPanel.pnlNavAid2.Point3d))) - 10);
                if (num >= 10):
                    self.parametersPanel.scrollBar.setMinimum(0);
                    self.parametersPanel.scrollBar.setMaximum(num * 2);
                    if (int_0 < self.parametersPanel.scrollBar.minimum() or int_0 > self.parametersPanel.scrollBar.maximum()):
                        self.parametersPanel.scrollBar.setValue(int(self.parametersPanel.scrollBar.maximum() / 2));
                    else:
                        self.parametersPanel.scrollBar.setValue(int_0);
                    self.copApplicable = True;
                    return;
        except:
            pass
        self.copApplicable = False;
    
    def method_32(self):
        self.parametersPanel.lblNA.setVisible(not self.copApplicable);
        self.parametersPanel.frameCOP.setVisible(self.copApplicable);
        if (self.copApplicable):
            self.parametersPanel.lblLeft.setText(str(self.copFromLeft) + "nm");
            self.parametersPanel.lblRight.setText(str(self.copFromRight) + "nm")
        self.parametersPanel.chbOverhead.setVisible(True if(self.parametersPanel.cmbNavAidType1.SelectedIndex == 0) else self.parametersPanel.cmbNavAidType2.SelectedIndex == 0);
        pass
    def method_34(self):
        self.method_31(-1)
        self.method_32();
    
    def method_37(self, point3d_0, point3d_1):
        num = None
        num1 = None;
        num2 = None;
        num3 = None;
        num4 = None;
        num5 = None;
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        point3d3 = None;
        point3d4 = None;
        point3d5 = None;
        point3d6 = None;
        point3d7 = None;
        point3d8 = None;
        num6 = MathHelper.getBearing(point3d_0, point3d_1);
        double_0 = num6 - Unit.ConvertDegToRad(90);
        double_1 = num6 + Unit.ConvertDegToRad(90);
        num7 = num6 - Unit.ConvertDegToRad(180);
        if (self.parametersPanel.cmbNavAidType1.SelectedIndex != 0):
            double_2 = 9300;
            num = max([math.tan(Unit.ConvertDegToRad(7.95)), 0.14]);
            num1 = max([math.tan(Unit.ConvertDegToRad(13)), 0.23]);
            num2 = 4650;
        else:
            if (not self.parametersPanel.chbOverhead.isChecked()):
                double_2 = 9300;
                num2 = 4650;
            else:
                double_2 = 7408;
                num2 = 3704;
            num = max([math.tan(Unit.ConvertDegToRad(5.7)), 0.1]);
            num1 = max([math.tan(Unit.ConvertDegToRad(9.1)), 0.16]);
        if (self.parametersPanel.cmbNavAidType2.SelectedIndex != 0):
            double_3 = 9300;
            num3 = max(math.tan(Unit.ConvertDegToRad(7.95)), 0.14);
            num4 = max(math.tan(Unit.ConvertDegToRad(13)), 0.23);
            num5 = 4650;
        else:
            if (not self.parametersPanel.chbOverhead.isChecked()):
                double_3 = 9300;
                num5 = 4650;
            else:
                double_3 = 7408;
                num5 = 3704;
            num3 = max(math.tan(Unit.ConvertDegToRad(5.7)), 0.1);
            num4 = max(math.tan(Unit.ConvertDegToRad(9.1)), 0.16);
        point3d9 = MathHelper.distanceBearingPoint(point3d_0, double_1, double_2);
        point3d10 = MathHelper.distanceBearingPoint(point3d9, double_1, double_2);
        point3d11 = MathHelper.distanceBearingPoint(point3d_1, double_1, double_3);
        point3d12 = MathHelper.distanceBearingPoint(point3d11, double_1, double_3);
        point3d13 = MathHelper.distanceBearingPoint(point3d_0, double_0, double_2);
        point3d14 = MathHelper.distanceBearingPoint(point3d13, double_0, double_2);
        point3d15 = MathHelper.distanceBearingPoint(point3d_1, double_0, double_3);
        point3d16 = MathHelper.distanceBearingPoint(point3d15, double_0, double_3);
        num8 = 0;
        num9 = 0;
        if (self.copApplicable):
            num8 = self.copFromLeft;
            num9 = self.copFromRight;
        if (not MathHelper.smethod_99(num8, num9, 0.0001)):
            num10 = Unit.ConvertNMToMeter(num8);
            num11 = Unit.ConvertNMToMeter(num9);
            point3d = MathHelper.distanceBearingPoint(point3d_1, num7, num11) if(num10 <= num11) else MathHelper.distanceBearingPoint(point3d_0, num6, num10);
        else:
            point3d = MathHelper.distanceBearingPoint(point3d_0, num6, MathHelper.calcDistance(point3d_0, point3d_1) / 2);
        point3d17 = MathHelper.distanceBearingPoint(point3d, double_0, double_2);
        point3d18 = MathHelper.distanceBearingPoint(point3d, double_0, double_3);
        point3d19 = MathHelper.distanceBearingPoint(point3d, double_1, double_2);
        point3d20 = MathHelper.distanceBearingPoint(point3d, double_1, double_3);
        point3d21 = MathHelper.distanceBearingPoint(point3d9, num6, double_2 / num);
        point3d22 = MathHelper.distanceBearingPoint(point3d13, num6, double_2 / num);
        point3d23 = MathHelper.distanceBearingPoint(point3d11, num7, double_3 / num3);
        point3d24 = MathHelper.distanceBearingPoint(point3d15, num7, double_3 / num3);
        if (round(MathHelper.calcDistance(point3d9, point3d21), 4) <= round(MathHelper.calcDistance(point3d9, point3d19), 4)):
            point3d19 = MathHelper.distanceBearingPoint(point3d19, double_1, num * (MathHelper.calcDistance(point3d9, point3d19) - MathHelper.calcDistance(point3d9, point3d21)));
            point3d17 = MathHelper.distanceBearingPoint(point3d, double_0, MathHelper.calcDistance(point3d, point3d19));
        else:
            point3d21 = MathHelper.distanceBearingPoint(point3d9, num6, MathHelper.calcDistance(point3d9, point3d19) / 2);
            point3d22 = MathHelper.distanceBearingPoint(point3d13, num6, MathHelper.calcDistance(point3d13, point3d17) / 2);
        if (round(MathHelper.calcDistance(point3d11, point3d23), 4) <= round(MathHelper.calcDistance(point3d11, point3d20), 4)):
            point3d20 = MathHelper.distanceBearingPoint(point3d20, double_1, num3 * (MathHelper.calcDistance(point3d11, point3d20) - MathHelper.calcDistance(point3d11, point3d23)));
            point3d18 = MathHelper.distanceBearingPoint(point3d, double_0, MathHelper.calcDistance(point3d, point3d20));
        else:
            point3d23 = MathHelper.distanceBearingPoint(point3d11, num7, MathHelper.calcDistance(point3d11, point3d20) / 2);
            point3d24 = MathHelper.distanceBearingPoint(point3d15, num7, MathHelper.calcDistance(point3d15, point3d18) / 2);
        if (round(MathHelper.calcDistance(point3d, point3d19), 4) > round(MathHelper.calcDistance(point3d, point3d20), 4)):
            point3d20 = point3d19;
            num12 = MathHelper.calcDistance(point3d, point3d19) / MathHelper.calcDistance(point3d_1, point3d);
            num13 = (MathHelper.calcDistance(point3d, point3d19) - double_3) / math.sin(math.atan(num12));
            point3d23 = MathHelper.distanceBearingPoint(point3d19, MathHelper.getBearing(point3d19, point3d_1), num13);
            point3d18 = point3d17;
            point3d24 = MathHelper.distanceBearingPoint(point3d23, double_0, 2 * double_3);
        if (round(MathHelper.calcDistance(point3d, point3d20), 4) > round(MathHelper.calcDistance(point3d, point3d19), 4)):
            point3d19 = point3d20;
            num14 = MathHelper.calcDistance(point3d, point3d20) / MathHelper.calcDistance(point3d_0, point3d);
            num15 = (MathHelper.calcDistance(point3d, point3d20) - double_2) / math.sin(math.atan(num14));
            point3d21 = MathHelper.distanceBearingPoint(point3d20, MathHelper.getBearing(point3d20, point3d_0), num15);
            point3d17 = point3d18;
            point3d22 = MathHelper.distanceBearingPoint(point3d21, double_0, 2 * double_2);
        double2 = num2 + num1 * MathHelper.calcDistance(point3d_0, point3d);
        if (round(double2, 4) <= round(double_2 * 2, 4)):
            double2 = double_2 * 2;
            point3d1 = MathHelper.distanceBearingPoint(point3d, double_1, double_2 * 2);
            point3d2 = MathHelper.distanceBearingPoint(point3d, double_0, double_2 * 2);
            point3d3 = MathHelper.distanceBearingPoint(point3d10, num6, MathHelper.calcDistance(point3d_0, point3d) / 2);
            point3d4 = MathHelper.distanceBearingPoint(point3d14, num6, MathHelper.calcDistance(point3d_0, point3d) / 2);
        else:
            point3d1 = MathHelper.distanceBearingPoint(point3d, double_1, double2);
            point3d2 = MathHelper.distanceBearingPoint(point3d, double_0, double2);
            double21 = (double2 - double_2 * 2) / math.sin(math.atan(num1));
            point3d3 = MathHelper.distanceBearingPoint(point3d1, MathHelper.getBearing(point3d1, MathHelper.distanceBearingPoint(point3d_0, double_1, num2)), double21);
            point3d4 = MathHelper.distanceBearingPoint(point3d3, double_0, 4 * double_2);
        double3 = num5 + num4 * MathHelper.calcDistance(point3d_1, point3d);
        if (round(double3, 4) <= round(double_3 * 2, 4)):
            double3 = double_3 * 2;
            point3d5 = MathHelper.distanceBearingPoint(point3d, double_1, double_3 * 2);
            point3d6 = MathHelper.distanceBearingPoint(point3d, double_0, double_3 * 2);
            point3d7 = MathHelper.distanceBearingPoint(point3d12, num7, MathHelper.calcDistance(point3d_1, point3d) / 2);
            point3d8 = MathHelper.distanceBearingPoint(point3d16, num7, MathHelper.calcDistance(point3d_1, point3d) / 2);
        else:
            point3d5 = MathHelper.distanceBearingPoint(point3d, double_1, double3);
            point3d6 = MathHelper.distanceBearingPoint(point3d, double_0, double3);
            double31 = (double3 - double_3 * 2) / math.sin(math.atan(num4));
            point3d7 = MathHelper.distanceBearingPoint(point3d5, MathHelper.getBearing(point3d5, MathHelper.distanceBearingPoint(point3d_1, double_1, num5)), double31);
            point3d8 = MathHelper.distanceBearingPoint(point3d7, double_0, 4 * double_3);
        if (round(MathHelper.calcDistance(point3d, point3d1), 4) > round(MathHelper.calcDistance(point3d, point3d5), 4)):
            point3d5 = point3d1;
            point3d6 = point3d2;
            num16 = (double2 - num5) / MathHelper.calcDistance(point3d_1, point3d);
            double32 = (double2 - double_3 * 2) / math.sin(math.atan(num16));
            point3d7 = MathHelper.distanceBearingPoint(point3d1, MathHelper.getBearing(point3d1, MathHelper.distanceBearingPoint(point3d_1, double_1, num5)), double32);
            point3d8 = MathHelper.distanceBearingPoint(point3d7, double_0, 4 * double_3);
        if (round(MathHelper.calcDistance(point3d, point3d5), 4) > round(MathHelper.calcDistance(point3d, point3d1), 4)):
            point3d1 = point3d5;
            point3d2 = point3d6;
            num17 = (double3 - num2) / MathHelper.calcDistance(point3d_0, point3d);
            double22 = (double3 - double_2 * 2) / math.sin(math.atan(num17));
            point3d3 = MathHelper.distanceBearingPoint(point3d5, MathHelper.getBearing(point3d5, MathHelper.distanceBearingPoint(point3d_0, double_1, num2)), double22);
            point3d4 = MathHelper.distanceBearingPoint(point3d3, double_0, 4 * double_2);
        point3dCollection = []
        point3dCollection.append(point3d9);
        point3dCollection.append(point3d10);
        point3dCollection.append(point3d13);
        point3dCollection.append(point3d14);
        point3dCollection.append(point3d11);
        point3dCollection.append(point3d12);
        point3dCollection.append(point3d15);
        point3dCollection.append(point3d16);
        point3dCollection.append(point3d);
        point3dCollection.append(point3d17);
        point3dCollection.append(point3d18);
        point3dCollection.append(point3d19);
        point3dCollection.append(point3d20);
        point3dCollection.append(point3d21);
        point3dCollection.append(point3d22);
        point3dCollection.append(point3d23);
        point3dCollection.append(point3d24);
        point3dCollection.append(point3d1);
        point3dCollection.append(point3d2);
        point3dCollection.append(point3d3);
        point3dCollection.append(point3d4);
        point3dCollection.append(point3d5);
        point3dCollection.append(point3d6);
        point3dCollection.append(point3d7);
        point3dCollection.append(point3d8);
        point3dCollection.append(point3d);
        return (point3dCollection, double_0, double_1, double_2, double_3);
    
    def get_copFromLeft(self):
        return float(self.parametersPanel.scrollBar.value())/ 2 + 5
    copFromLeft = property(get_copFromLeft, None, None, None)
    
    def get_copFromRight(self):
        return float((self.parametersPanel.scrollBar.maximum() - self.parametersPanel.scrollBar.value())) / 2 + 5
    copFromRight = property(get_copFromRight, None, None, None)
    
class EnrouteStraightObstacles(ObstacleTable):
    def __init__(self, surfacesArea, altitude_0, altitude_1):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesArea)
        
        self.surfaceType = SurfaceTypes.EnrouteStraight
        self.obstaclesChecked = None
        self.area = surfacesArea
        self.primaryMoc = altitude_0.Metres
        self.enrouteAltitude = altitude_1.Metres
    def setHiddenColumns(self, tableView):
        return ObstacleTable.setHiddenColumns(self, tableView)

    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        self.IndexObstArea = fixedColumnCount 
        self.IndexDistInSecM = fixedColumnCount + 1
        self.IndexMocAppliedM = fixedColumnCount + 2
        self.IndexMocAppliedFt = fixedColumnCount + 3
        self.IndexMocMultiplier = fixedColumnCount + 4
        self.IndexOcaM = fixedColumnCount + 5
        self.IndexOcaFt = fixedColumnCount + 6
        self.IndexCritical = fixedColumnCount + 7
                 
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DistInSecM,
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt,
                ObstacleTableColumnType.Critical            
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)
    def addObstacleToModel(self, obstacle, checkResult):
        ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
        row = self.source.rowCount() - 1

        item = QStandardItem(str(checkResult[0]))
        item.setData(checkResult[0])
        self.source.setItem(row, self.IndexObstArea, item)
        
        item = QStandardItem(str(checkResult[1]))
        item.setData(checkResult[1])
        self.source.setItem(row, self.IndexDistInSecM, item)
        
        item = QStandardItem(str(checkResult[2]))
        item.setData(checkResult[2])
        self.source.setItem(row, self.IndexMocAppliedM, item)
          
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[2])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[2]))
        self.source.setItem(row, self.IndexMocAppliedFt, item)
          
        item = QStandardItem(str(ObstacleTable.MocMultiplier))
        item.setData(ObstacleTable.MocMultiplier)
        self.source.setItem(row, self.IndexMocMultiplier, item)
          
        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexOcaM, item)
          
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[3])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[3]))
        self.source.setItem(row, self.IndexOcaFt, item)
        
        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4])
        self.source.setItem(row, self.IndexCritical, item) 
    def checkObstacle(self, obstacle_0):
        obstacleAreaResult = ObstacleAreaResult.Outside;
        num = None
        num1 = None
        z = None
        mocMultiplier = self.primaryMoc * obstacle_0.MocMultiplier;
        obstacleAreaResult, num, num1 = self.area.pointInArea(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier);
        if obstacleAreaResult == None:
            return
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            position = obstacle_0.Position;
            try:
                z = position.get_Z() + obstacle_0.Trees + num;
            except:
                pass
            criticalObstacleType = CriticalObstacleType.No;
            if (z > self.enrouteAltitude):
                criticalObstacleType = CriticalObstacleType.Yes;
            checkResult = [obstacleAreaResult, num1, num, z, criticalObstacleType]
            self.addObstacleToModel(obstacle_0, checkResult)
#             obstacles.method_11(obstacle_0, obstacleAreaResult, num1, num, z, criticalObstacleType);
