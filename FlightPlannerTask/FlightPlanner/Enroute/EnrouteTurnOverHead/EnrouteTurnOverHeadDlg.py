# -*- coding: UTF-8 -*-
'''
Created on 30 Jun 2015

@author: Administrator
'''
from qgis.core import QGis, QgsVectorLayer, QgsGeometry, QgsFeature, QgsVectorFileWriter
from PyQt4.QtGui import QFileDialog, QStandardItem, QMessageBox
from PyQt4.QtCore import SIGNAL,Qt, QCoreApplication, QString
from FlightPlanner.types import ConstructionType, CriticalObstacleType, ObstacleTableColumnType, OrientationType, DistanceUnits, AltitudeUnits, TurnDirection
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.WindPanel import WindPanel
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, ComplexObstacleArea, SecondaryObstacleArea, ObstacleAreaResult
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
# 
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Enroute.EnrouteTurnOverHead.ui_EnrouteTurnOverHead import Ui_EnrouteTurnOverHead
from FlightPlanner.DataHelper import DataHelper

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import AltitudeUnits, Point3D, AngleUnits, SurfaceTypes
from FlightPlanner.polylineArea import PolylineArea
from FlightPlanner.helpers import Speed, Altitude, MathHelper, Unit
import define
import math

class EnrouteTurnOverHeadDlg(FlightPlanBaseDlg):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("HoldingRnp")
        self.surfaceType = SurfaceTypes.EnrouteTurnOverHead
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.EnrouteTurnOverHead)
                
        self.resize(540, 550)
        QgisHelper.matchingDialogSize(self, 670, 700)

        self.vorDmeFeatureArray = dict()
        self.currentLayer = define._canvas.currentLayer()
        self.initBasedOnCmb()
    def initBasedOnCmb(self):
        # self.currentLayer = define._canvas.currentLayer()
        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.vorDmeFeatureArray = self.basedOnCmbFill(self.currentLayer, self.parametersPanel.cmbBasedOn, self.parametersPanel.pnlNavAid)
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
                if self.parametersPanel.cmbNavAidType.SelectedIndex == 0:
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
            feat = self.vorDmeFeatureArray.__getitem__(self.parametersPanel.cmbBasedOn.SelectedItem)
        except:
            return
        attrValue = feat.attributes()[idxLat].toDouble()
        lat = attrValue[0]

        attrValue = feat.attributes()[idxLong].toDouble()
        long = attrValue[0]

        attrValue = feat.attributes()[idxAltitude].toDouble()
        alt = attrValue[0]

        self.parametersPanel.pnlNavAid.Point3d = Point3D(long, lat, alt)

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
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.EnrouteTurnOverHead, self.ui.tblObstacles, None, parameterList, resultHideColumnNames)
#         self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
    
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("Waypoint Position", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlNavAid.txtPointX.text()), float(self.parametersPanel.pnlNavAid.txtPointY.text()))
        
        parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
        parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
        parameterList.append(("X", self.parametersPanel.pnlNavAid.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlNavAid.txtPointY.text()))
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("In-bound Track", self.parametersPanel.txtInBound.text()))
        parameterList.append(("Out-bound Track", self.parametersPanel.txtOutBound.text()))
        parameterList.append(("IAS", self.parametersPanel.txtIas.text() + "kts"))
        parameterList.append(("ISA", self.parametersPanel.txtIsa.text()))
        parameterList.append(("Bank Angle", self.parametersPanel.txtBankAngle.text()))
        parameterList.append(("Wind", self.parametersPanel.pnlWind.speedBox.text() + "kts"))
        parameterList.append(("Pilot Reaction Time", self.parametersPanel.txtPilotTime.text() + "sec"))
        parameterList.append(("Bank Establishment Time", self.parametersPanel.txtBankEstTime.text() + "sec"))
        parameterList.append(("Primary MOC", self.parametersPanel.txtPrimaryMoc.text() + "m"))
        parameterList.append(("Enroute Altitude", self.parametersPanel.txtEnrouteAltitude.text() + "ft"))
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstruction.currentText()))
        parameterList.append(("4nm overhead the VOR", str(self.parametersPanel.chbOverhead.isChecked())))
        
        parameterList.append(("Results / Checked Obstacles", "group"))   
        parameterList.append(("Checked Obstacles", "group"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        return parameterList
    def initObstaclesModel(self):
        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        
        return FlightPlanBaseDlg.initObstaclesModel(self)
    def btnEvaluate_Click(self):
        turnDirection = None;
        point3ds = [];
        nums = [];
        point3d = None;
        if (not self.method_27()):
            return;
        turnDirectionList = []
        num = MathHelper.smethod_77(float(self.parametersPanel.txtInBound.text()), float(self.parametersPanel.txtOutBound.text()), AngleUnits.Degrees, turnDirectionList);
        turnDirection = turnDirectionList[0]
        point3dCollection, point3ds, nums = self.method_39();
        complexObstacleArea = ComplexObstacleArea();
        item = [point3dCollection[3], point3dCollection[4], point3dCollection[5], point3dCollection[6], point3dCollection[7]];
        polylineArea = PolylineArea(item);
        if (num < 60):
            polylineArea.method_3(point3dCollection[7], MathHelper.smethod_57(turnDirection, point3dCollection[7], point3dCollection[30], point3ds[0]));
            polylineArea.method_1(point3dCollection[30]);
        elif (num > 150):
            polylineArea.method_3(point3dCollection[7], MathHelper.smethod_57(turnDirection, point3dCollection[7], point3dCollection[9], point3ds[0]));
            polylineArea.method_1(point3dCollection[9]);
            polylineArea.method_3(point3dCollection[10], MathHelper.smethod_57(turnDirection, point3dCollection[10], point3dCollection[12], point3ds[1]));
            polylineArea.method_3(point3dCollection[12], MathHelper.smethod_57(turnDirection, point3dCollection[12], point3dCollection[14], point3ds[2]));
            polylineArea.method_1(point3dCollection[14]);
        else:
            polylineArea.method_3(point3dCollection[7], MathHelper.smethod_57(turnDirection, point3dCollection[7], point3dCollection[9], point3ds[0]));
            polylineArea.method_1(point3dCollection[9]);
            polylineArea.method_3(point3dCollection[10], MathHelper.smethod_57(turnDirection, point3dCollection[10], point3dCollection[30], point3ds[1]));
            polylineArea.method_1(point3dCollection[30]);
        point3dArray = [point3dCollection[15], point3dCollection[16], point3dCollection[3]];
        polylineArea.method_7(point3dArray);
        complexObstacleArea.Add(PrimaryObstacleArea(polylineArea));
        complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection[5], point3dCollection[4], point3dCollection[20], point3dCollection[19]));
        complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection[4], point3dCollection[3], point3dCollection[19], point3dCollection[18]));
        complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection[7], point3dCollection[6], point3dCollection[22], point3dCollection[21]));
        complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection[16], point3dCollection[15], point3dCollection[17], point3dCollection[29]));
        if (num > 60):
            complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection[10], point3dCollection[9], point3dCollection[25], point3dCollection[24]));
        if (num <= 150):
            complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection[15], point3dCollection[30], point3dCollection[29], point3dCollection[28]));
        else:
            complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection[15], point3dCollection[14], point3dCollection[29], point3dCollection[28]));
        if (num <= 60):
            point3d1 = MathHelper.smethod_93(turnDirection, point3dCollection[7], point3dCollection[30], point3ds[0]);
            point3d2 = MathHelper.smethod_93(turnDirection, point3dCollection[22], point3dCollection[28], point3ds[0]);
            complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection[7], point3d1, point3dCollection[30], point3dCollection[22], None, point3d2, point3dCollection[28]));
        else:
            point3d3 = MathHelper.smethod_93(turnDirection, point3dCollection[7], point3dCollection[9], point3ds[0]);
            point3d4 = MathHelper.smethod_93(turnDirection, point3dCollection[22], point3dCollection[24], point3ds[0]);
            complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection[7], point3d3, point3dCollection[9], point3dCollection[22], None, point3d4, point3dCollection[24]));
        if (num > 60):
            if (num > 150):
                point3d5 = MathHelper.smethod_93(turnDirection, point3dCollection[10], point3dCollection[12], point3ds[1]);
                point3d6 = MathHelper.smethod_93(turnDirection, point3dCollection[25], point3dCollection[27], point3ds[1]);
                complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection[10], point3d5, point3dCollection[12], point3dCollection[25], None, point3d6, point3dCollection[27]));
            else:
                point3d7 = MathHelper.smethod_93(turnDirection, point3dCollection[10], point3dCollection[30], point3ds[1]);
                point3d8 = MathHelper.smethod_93(turnDirection, point3dCollection[25], point3dCollection[28], point3ds[1]);
                complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection[10], point3d7, point3dCollection[30], point3dCollection[25], None, point3d8, point3dCollection[28]));
        if (num > 150):
            point3d9 = MathHelper.smethod_93(turnDirection, point3dCollection[12], point3dCollection[14], point3ds[2]);
            point3d10 = MathHelper.smethod_93(turnDirection, point3dCollection[27], point3dCollection[28], point3ds[2]);
            complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection[12], point3d9, point3dCollection[14], point3dCollection[27], None, point3d10, point3dCollection[28]));
        polylineArea1 = PolylineArea();
        if (num <= 60):
            item1 = [point3dCollection[21], point3dCollection[22], point3dCollection[28], point3dCollection[29], point3dCollection[17]];
            polylineArea1.method_7(item1);
            polylineArea1.method_19(1, MathHelper.smethod_60(point3dCollection[22], point3dCollection[23], point3dCollection[28]));
        elif (num > 150):
            point3d = MathHelper.smethod_68(point3dCollection[25], point3dCollection[26], point3dCollection[27]);
            num1 = MathHelper.getBearing(point3d, point3dCollection[27]) + Unit.ConvertDegToRad(90);
            if (not MathHelper.smethod_130(MathHelper.getBearing(point3d, point3dCollection[25]), MathHelper.getBearing(point3d, point3dCollection[27]))):
                num1 = num1 - Unit.ConvertDegToRad(180);
            point3dArray1 = [point3dCollection[21], point3dCollection[22], point3dCollection[24], point3dCollection[25], point3dCollection[27], point3dCollection[28], point3dCollection[29], point3dCollection[17]];
            polylineArea1.method_7(point3dArray1);
            polylineArea1.method_19(1, MathHelper.smethod_60(point3dCollection[22], point3dCollection[23], point3dCollection[24]));
            polylineArea1.method_19(3, MathHelper.smethod_60(point3dCollection[25], point3dCollection[26], point3dCollection[27]));
            polylineArea1.method_19(4, MathHelper.smethod_59(num1, point3dCollection[27], point3dCollection[28]));
        else:
            item2 = [point3dCollection[21], point3dCollection[22], point3dCollection[24], point3dCollection[25], point3dCollection[28], point3dCollection[29], point3dCollection[17]];
            polylineArea1.method_7(item2);
            polylineArea1.method_19(1, MathHelper.smethod_60(point3dCollection[22], point3dCollection[23], point3dCollection[24]));
            polylineArea1.method_19(3, MathHelper.smethod_60(point3dCollection[25], point3dCollection[26], point3dCollection[28]));
        point3dArray2 = [point3dCollection[18], point3dCollection[19], point3dCollection[20]];
        polylineArea1.method_7(point3dArray2);
        primaryObstacleArea = PrimaryObstacleArea(polylineArea1);
        
        self.obstaclesModel = EnrouteTurnOverheadObstacles(complexObstacleArea,  Altitude(float(self.parametersPanel.txtPrimaryMoc.text())), Altitude(float(self.parametersPanel.txtEnrouteAltitude.text()), AltitudeUnits.FT))
        
        return FlightPlanBaseDlg.btnEvaluate_Click(self)


    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        if not self.method_27():
            return 
        
        turnDirection = None;
        point3ds = [];
        nums = [];
        point3d = None;
        polyline = PolylineArea();
        point3d1 = None;
        item = None;
        turnDirectionList = []
        num = MathHelper.smethod_77(float(self.parametersPanel.txtInBound.text()), float(self.parametersPanel.txtOutBound.text()), AngleUnits.Degrees, turnDirectionList);
        turnDirection = turnDirectionList[0]
        point3dCollection, point3ds, nums = self.method_39();
        
        mapUnits = define._canvas.mapUnits()
        constructionLayer = None
                
        if (self.parametersPanel.cmbConstruction.currentText() != ConstructionType.Construct3D):
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)
            resultPoint3dArrayList = []
            resultPolylineAreaList = []
            item = [point3dCollection[18], point3dCollection[19], point3dCollection[20]];
            resultPoint3dArrayList.append(item)
#             polyline2 = PolylineArea(item);
#             AcadHelper.smethod_18(transaction, blockTableRecord, polyline2, constructionLayer);
            item9 = [point3dCollection[3], point3dCollection[4], point3dCollection[5]];
            resultPoint3dArrayList.append(item9)
#             polyline2 = AcadHelper.smethod_126(item9);
#             AcadHelper.smethod_18(transaction, blockTableRecord, polyline2, constructionLayer);
            if (num <= 60):
                point3dArray9 = [point3dCollection[21], point3dCollection[22], point3dCollection[28], point3dCollection[29], point3dCollection[17]];
                polyline2 = PolylineArea(point3dArray9);
                polyline2[1].set_Bulge(MathHelper.smethod_60(point3dCollection[22], point3dCollection[23], point3dCollection[28]));
                resultPolylineAreaList.append(polyline2)
#                 AcadHelper.smethod_18(transaction, blockTableRecord, polyline2, constructionLayer);
                item10 = [point3dCollection[6], point3dCollection[7], point3dCollection[30], point3dCollection[15], point3dCollection[16]];
                polyline2 = PolylineArea(item10);
                polyline2[1].set_Bulge(MathHelper.smethod_60(point3dCollection[7], point3dCollection[8], point3dCollection[30]));
                resultPolylineAreaList.append(polyline2)
#                 AcadHelper.smethod_18(transaction, blockTableRecord, polyline2, constructionLayer);
            elif (num > 150):
                point3d = MathHelper.smethod_68(point3dCollection[25], point3dCollection[26], point3dCollection[27]);
                num5 = MathHelper.getBearing(point3d, point3dCollection[27]) + Unit.ConvertDegToRad(90);
                if (not MathHelper.smethod_130(MathHelper.getBearing(point3d, point3dCollection[25]), MathHelper.getBearing(point3d, point3dCollection[27]))):
                    num5 = num5 - Unit.ConvertDegToRad(180);
                point3dArray10 = [point3dCollection[21], point3dCollection[22], point3dCollection[24], point3dCollection[25], point3dCollection[27], point3dCollection[28], point3dCollection[29], point3dCollection[17]];
                polyline2 = PolylineArea(point3dArray10);
                polyline2[1].set_Bulge(MathHelper.smethod_60(point3dCollection[22], point3dCollection[23], point3dCollection[24]));
                polyline2[3].set_Bulge(MathHelper.smethod_60(point3dCollection[25], point3dCollection[26], point3dCollection[27]));
                polyline2[4].set_Bulge(MathHelper.smethod_59(num5, point3dCollection[27], point3dCollection[28]));
                resultPolylineAreaList.append(polyline2)
#                 AcadHelper.smethod_18(transaction, blockTableRecord, polyline2, constructionLayer);
                item11 = [point3dCollection[6], point3dCollection[7], point3dCollection[9], point3dCollection[10], point3dCollection[12], point3dCollection[14], point3dCollection[15], point3dCollection[16]];
                polyline2 = PolylineArea(item11);
                polyline2[1].set_Bulge(MathHelper.smethod_60(point3dCollection[7], point3dCollection[8], point3dCollection[9]));
                polyline2[3].set_Bulge(MathHelper.smethod_60(point3dCollection[10], point3dCollection[11], point3dCollection[12]));
                polyline2[4].set_Bulge(MathHelper.smethod_59(num5, point3dCollection[12], point3dCollection[14]));
                resultPolylineAreaList.append(polyline2)
#                 AcadHelper.smethod_18(transaction, blockTableRecord, polyline2, constructionLayer);
            else:
                point3dArray11 = [point3dCollection[21], point3dCollection[22], point3dCollection[24], point3dCollection[25], point3dCollection[28], point3dCollection[29], point3dCollection[17]];
                polyline2 = PolylineArea(point3dArray11);
                polyline2[1].set_Bulge(MathHelper.smethod_60(point3dCollection[22], point3dCollection[23], point3dCollection[24]));
                polyline2[3].set_Bulge(MathHelper.smethod_60(point3dCollection[25], point3dCollection[26], point3dCollection[28]));
                resultPolylineAreaList.append(polyline2)
#                 AcadHelper.smethod_18(transaction, blockTableRecord, polyline2, constructionLayer);
                item12 = [point3dCollection[6], point3dCollection[7], point3dCollection[9], point3dCollection[10], point3dCollection[30], point3dCollection[15], point3dCollection[16]];
                polyline2 = PolylineArea(item12);
                polyline2[1].set_Bulge(MathHelper.smethod_60(point3dCollection[7], point3dCollection[8], point3dCollection[9]));
                polyline2[3].set_Bulge(MathHelper.smethod_60(point3dCollection[10], point3dCollection[11], point3dCollection[30]));
                resultPoint3dArrayList.append(polyline2.method_14())
#                 AcadHelper.smethod_18(transaction, blockTableRecord, polyline2, constructionLayer);
            point3dArray12 = [point3dCollection[0], point3dCollection[1], point3dCollection[2]];
#             polyline2 = PolylineArea(point3dArray12);
            resultPoint3dArrayList.append(point3dArray12)
#             AcadHelper.smethod_18(transaction, blockTableRecord, polyline2, constructionLayer);
            item13 = [point3dCollection[20], point3dCollection[5], point3dCollection[21]];
            resultPoint3dArrayList.append(item13)
#             polyline2 = PolylineArea(item13);
#             AcadHelper.smethod_18(transaction, blockTableRecord, polyline2, constructionLayer);
            point3dArray13 = [point3dCollection[17], point3dCollection[18]];
            resultPoint3dArrayList.append(point3dArray13)
#             polyline2 = AcadHelper.smethod_126(point3dArray13);
#             AcadHelper.smethod_18(transaction, blockTableRecord, polyline2, constructionLayer);

            for point3dArray in resultPoint3dArrayList:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, point3dArray)
            for polylineArea in resultPolylineAreaList:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea)
        else:
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Polygon)
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

                
            num1 = -1;
            num2 = -1;
            num3 = -1;
            point3dCollection1 = [];
            point3dCollection2 = [];
            point3dCollection3 = [];
            point3dCollection4 = [];
            polyline = None
            if (num <= 60):
                point3dArray = [point3dCollection[18], point3dCollection[19], point3dCollection[20]];
                point3dCollection1.extend(point3dArray);
                item1 = [point3dCollection[21], point3dCollection[22]];
                point3dCollection2.extend(item1);
                point3dArray, num1 = MathHelper.smethod_139(point3dCollection[22], point3dCollection[23], point3dCollection[28], num1)
                point3dCollection2.extend(point3dArray);
                point3dArray1 = [point3dCollection[28], point3dCollection[29], point3dCollection[17]];
                point3dCollection2.extend(point3dArray1);
                item2 = [point3dCollection[3], point3dCollection[4], point3dCollection[5], point3dCollection[6], point3dCollection[7], point3dCollection[30], point3dCollection[15], point3dCollection[16]];
                polyline = PolylineArea(item2);
                polyline[4].set_Bulge(MathHelper.smethod_60(point3dCollection[7], point3dCollection[8], point3dCollection[30]));
                point3dArray2 = [point3dCollection[3], point3dCollection[4], point3dCollection[5]];
                point3dCollection3.extend(point3dArray2);
                item3 = [point3dCollection[6], point3dCollection[7]];
                point3dCollection4.extend(item3);
                pointArray, num1 = MathHelper.smethod_139(point3dCollection[7], point3dCollection[8], point3dCollection[30], num1)
                point3dCollection4.extend(pointArray);
                point3dArray3 = [point3dCollection[30], point3dCollection[15], point3dCollection[16]];
                point3dCollection4.extend(point3dArray3);
            elif (num > 150):
                item4 = [point3dCollection[18], point3dCollection[19], point3dCollection[20]];
                point3dCollection1.extend(item4);
                point3d1 = MathHelper.smethod_68(point3dCollection[25], point3dCollection[26], point3dCollection[27]);
                num4 = MathHelper.getBearing(point3d1, point3dCollection[27]) + Unit.ConvertDegToRad(90);
                if (not MathHelper.smethod_130(MathHelper.getBearing(point3d1, point3dCollection[25]), MathHelper.getBearing(point3d1, point3dCollection[27]))):
                    num4 = num4 - Unit.ConvertDegToRad(180);
                item = [point3dCollection[21], point3dCollection[22]];
                point3dCollection2.extend(item);
                pointArray, num1 = MathHelper.smethod_139(point3dCollection[22], point3dCollection[23], point3dCollection[24], num1)
                point3dCollection2.extend(pointArray);
                item = [point3dCollection[24], point3dCollection[25]];
                point3dCollection2.extend(item);
                pointArray, num2 = MathHelper.smethod_139(point3dCollection[25], point3dCollection[26], point3dCollection[27], num2)
                point3dCollection2.extend(pointArray);
                point3dCollection2.append(point3dCollection[27]);
                pointArray, num3 = MathHelper.smethod_140(num4, point3dCollection[27], point3dCollection[28], num3)
                point3dCollection2.extend(pointArray);
                item = [point3dCollection[28], point3dCollection[29], point3dCollection[17]];
                point3dCollection2.extend(item);
                point3d1 = MathHelper.smethod_68(point3dCollection[10], point3dCollection[11], point3dCollection[12]);
                num4 = MathHelper.getBearing(point3d1, point3dCollection[12]) + Unit.ConvertDegToRad(90);
                if (not MathHelper.smethod_130(MathHelper.getBearing(point3d1, point3dCollection[10]), MathHelper.getBearing(point3d1, point3dCollection[12]))):
                    num4 = num4 - Unit.ConvertDegToRad(180);
                item = [point3dCollection[3], point3dCollection[4], point3dCollection[5], point3dCollection[6], point3dCollection[7], point3dCollection[9], point3dCollection[10], point3dCollection[12], point3dCollection[14], point3dCollection[15], point3dCollection[16]];
                polyline = PolylineArea(item);
                polyline[4].set_Bulge(MathHelper.smethod_60(point3dCollection[7], point3dCollection[8], point3dCollection[9]));
                polyline[6].set_Bulge(MathHelper.smethod_60(point3dCollection[10], point3dCollection[11], point3dCollection[12]));
                polyline[7].set_Bulge(MathHelper.smethod_59(num4, point3dCollection[12], point3dCollection[14]));
                item = [point3dCollection[3], point3dCollection[4], point3dCollection[5]];
                point3dCollection3.extend(item);
                item = [point3dCollection[6], point3dCollection[7]];
                point3dCollection4.extend(item);
                pointArray, num1 = MathHelper.smethod_139(point3dCollection[7], point3dCollection[8], point3dCollection[9], num1)
                point3dCollection4.extend(pointArray);
                item = [point3dCollection[9], point3dCollection[10]];
                point3dCollection4.extend(item);
                pointArray, num2 = MathHelper.smethod_139(point3dCollection[10], point3dCollection[11], point3dCollection[12], num2)
                point3dCollection4.extend(pointArray);
                point3dCollection4.append(point3dCollection[12]);
                pointArray, num3 = MathHelper.smethod_140(num4, point3dCollection[12], point3dCollection[14], num3)
                point3dCollection4.extend(pointArray);
                item = [point3dCollection[14], point3dCollection[15], point3dCollection[16]];
                point3dCollection4.extend(item);
            else:
                point3dArray4 = [point3dCollection[18], point3dCollection[19], point3dCollection[20]];
                point3dCollection1.extend(point3dArray4);
                item5 = [point3dCollection[21], point3dCollection[22]];
                point3dCollection2.extend(item5);
                pointArray ,num1 = MathHelper.smethod_139(point3dCollection[22], point3dCollection[23], point3dCollection[24], num1)
                point3dCollection2.extend(pointArray);
                point3dArray5 = [point3dCollection[24], point3dCollection[25]];
                point3dCollection2.extend(point3dArray5);
                pointArray, num2 = MathHelper.smethod_139(point3dCollection[25], point3dCollection[26], point3dCollection[28], num2)
                point3dCollection2.extend(pointArray);
                item6 = [point3dCollection[28], point3dCollection[29], point3dCollection[17]];
                point3dCollection2.extend(item6);
                point3dArray6 = [point3dCollection[3], point3dCollection[4], point3dCollection[5], point3dCollection[6], point3dCollection[7], point3dCollection[9], point3dCollection[10], point3dCollection[30], point3dCollection[15], point3dCollection[16]];
                polyline = PolylineArea(point3dArray6);
                polyline[4].set_Bulge(MathHelper.smethod_60(point3dCollection[7], point3dCollection[8], point3dCollection[9]));
                polyline[6].set_Bulge(MathHelper.smethod_60(point3dCollection[10], point3dCollection[11], point3dCollection[30]));
                item7 = [point3dCollection[3], point3dCollection[4], point3dCollection[5]];
                point3dCollection3.extend(item7);
                point3dArray7 = [point3dCollection[6], point3dCollection[7]];
                point3dCollection4.extend(point3dArray7);
                pointArray, num1 = MathHelper.smethod_139(point3dCollection[7], point3dCollection[8], point3dCollection[9], num1)
                point3dCollection4.extend(pointArray);
                item8 = [point3dCollection[9], point3dCollection[10]];
                point3dCollection4.extend(item8);
                pointArray, num2 = MathHelper.smethod_139(point3dCollection[10], point3dCollection[11], point3dCollection[30], num2)
                point3dCollection4.extend(pointArray);
                point3dArray8 = [point3dCollection[30], point3dCollection[15], point3dCollection[16]];
                point3dCollection4.extend(point3dArray8);
            metres = Altitude(float(self.parametersPanel.txtPrimaryMoc.text())).Metres;
            metres1 = Altitude(float(self.parametersPanel.txtEnrouteAltitude.text()), AltitudeUnits.FT).Metres;
#             for i in range(len(point3dCollection1)):
#                 point3dCollection1.set_Item(i, point3dCollection1[i).smethod_167(metres1));
#             for (int j = 0; j < point3dCollection2.get_Count(); j++)
#             {
#                 point3dCollection2.set_Item(j, point3dCollection2[j).smethod_167(metres1));
#             }
#             for (int k = 0; k < point3dCollection3.get_Count(); k++)
#             {
#                 point3dCollection3.set_Item(k, point3dCollection3[k).smethod_167(metres1 - metres));
#             }
#             for (int l = 0; l < point3dCollection4.get_Count(); l++)
#             {
#                 point3dCollection4.set_Item(l, point3dCollection4[l).smethod_167(metres1 - metres));
#             }
#             polyline.set_Elevation(metres1 - metres);
            
            # constructionLayer.startEditing()
            
            polygon3_1 = QgisHelper.smethod_147(point3dCollection3, point3dCollection1)
            polygon4_2 = QgisHelper.smethod_147(point3dCollection4, point3dCollection2)
            
            feature = QgsFeature()
#             feature.setGeometry(polygon3_1[0])
#             constructionLayer.addFeature(feature)
#             
#             feature.setGeometry(polygon3_1[1])
#             constructionLayer.addFeature(feature)
#             
#             feature.setGeometry(polygon4_2[0])
#             constructionLayer.addFeature(feature)
#             
#             feature.setGeometry(polygon4_2[1])
#             constructionLayer.addFeature(feature)
#             AcadHelper.smethod_147(transaction, blockTableRecord, point3dCollection3, point3dCollection1, constructionLayer);
#             AcadHelper.smethod_147(transaction, blockTableRecord, point3dCollection4, point3dCollection2, constructionLayer);
#             polyline.SetDatabaseDefaults();
#             polyline.set_Closed(true);
#             DBObjectCollection dBObjectCollection = new DBObjectCollection();
#             dBObjectCollection.Add(polyline);
#             DBObjectCollection dBObjectCollection1 = Autodesk.AutoCAD.DatabaseServices.Region.CreateFromCurves(dBObjectCollection);
#             AcadHelper.smethod_25(dBObjectCollection);
#             foreach (Entity entity in dBObjectCollection1)
#             {
#                 AcadHelper.smethod_18(transaction, blockTableRecord, entity, constructionLayer);
#             }
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polyline.method_14())
            # feature.setGeometry(QgsGeometry.fromPolygon([polyline.method_14()]))
            # constructionLayer.addFeature(feature)
            
            item = [point3dCollection[0], point3dCollection[1], point3dCollection[2]];
            polyline1 = PolylineArea(item);
            
#             feature.setGeometry(QgsGeometry.fromPolygon([polyline1.method_14_closed()]))
#             constructionLayer.addFeature(feature)
#             polyline1.set_Elevation(metres1);
#             polyline1.set_Thickness(-metres);
#             AcadHelper.smethod_18(transaction, blockTableRecord, polyline1, constructionLayer);    
            
#             count = len(polylines)
#             num = 0.1 * count
#             altitude = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)
#             value = Altitude(float(self.parametersPanel.txtMoc.text()), AltitudeUnits.M)
#             metres = altitude.Metres - value.Metres
#             for i in range(count):
#                 polygon1 = QgsGeometry.fromPolygon([polylines[i].method_14_closed()])
#                 polygonNew = polygon1
#                 if (i > 0):
#                     metres1 = altitude.Metres
# #                     value = self.pnlMoc.Value;
#                     metres = metres1 - num * value.Metres
#                     num = num - 0.1
# # #                 polylines[i].set_Elevation(metres);
# #                 DBObjectCollection dBObjectCollection = new DBObjectCollection();
# # #                 dBObjectCollection.Add(polylines[i]);
# #                 Autodesk.AutoCAD.DatabaseServices.Region item = Autodesk.AutoCAD.DatabaseServices.Region.CreateFromCurves(dBObjectCollection)[0) as Autodesk.AutoCAD.DatabaseServices.Region;
# #                 item.SetDatabaseDefaults();
#                 if (i > 0):
#                     polygon0 = QgsGeometry.fromPolygon([polylines[i - 1].method_14_closed()])
#                     polygonNew = polygon1.difference(polygon0)
#                 feature = QgsFeature()
#                 feature.setGeometry(polygonNew)
#                 constructionLayer.addFeature(feature) 
#             constructionLayer.commitChanges()
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.EnrouteTurnOverHead)
        self.resultLayerList = [constructionLayer]
        self.ui.btnEvaluate.setEnabled(True)
        # return FlightPlanBaseDlg.btnConstruct_Click(self)

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
        ui = Ui_EnrouteTurnOverHead()
        self.parametersPanel = ui
        
        
        FlightPlanBaseDlg.initParametersPan(self)        
        
        self.parametersPanel.frameAircraftCategory.setVisible(False)
        
        self.parametersPanel.pnlNavAid = PositionPanel(self.parametersPanel.gbNavAid)
#         self.parametersPanel.pnlNavAid.hideframe_Altitude()
        self.parametersPanel.pnlNavAid.setObjectName("pnlNavAid")
        self.parametersPanel.pnlNavAid.btnCalculater.hide()
        self.parametersPanel.verticalLayoutNavAid.addWidget(self.parametersPanel.pnlNavAid)
        self.connect(self.parametersPanel.pnlNavAid, SIGNAL("positionChanged"), self.iasChanged)

        
        self.parametersPanel.pnlWind = WindPanel(self.parametersPanel.gbParameters)
        self.parametersPanel.vl_gbParameters.insertWidget(7, self.parametersPanel.pnlWind)
        self.parametersPanel.pnlWind.LabelWidth = 192
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtEnrouteAltitude.text()), AltitudeUnits.FT))
        
#         self.resize(460,600)
        self.parametersPanel.cmbConstruction.addItems(["2D", "3D"])
        self.parametersPanel.cmbNavAidType.Items = ["VOR", "NDB"]
        
        self.method_31()
        self.iasChanged()
        self.parametersPanel.txtEnrouteAltitude.textChanged.connect(self.method_31)
        self.parametersPanel.btnCaptureInBound.clicked.connect(self.captureBearingInBound)
        self.parametersPanel.btnCaptureOutBound.clicked.connect(self.captureBearingOutBound)
        self.parametersPanel.txtIas.textChanged.connect(self.iasChanged)
        self.parametersPanel.txtIsa.textChanged.connect(self.iasChanged)
        self.connect(self.parametersPanel.cmbNavAidType, SIGNAL("Event_0"), self.initBasedOnCmb)
    def iasChanged(self):
        try:
            self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtEnrouteAltitude.text()), AltitudeUnits.FT) - self.parametersPanel.pnlNavAid.Altitude()).Knots))
        except:
            raise ValueError("Value Invalid")
#     def iasHelpShow(self):
#         dlg = IasHelpDlg()
#         dlg.exec_()
    
    def method_27(self):
        if MathHelper.smethod_63(float(self.parametersPanel.txtInBound.text()), float(self.parametersPanel.txtOutBound.text()), AngleUnits.Degrees) == TurnDirection.Nothing:
            QMessageBox.warning(self, "Warning", "INBOUND_OUTBOUND_TRACK_CANNOT_BE_IDENTICAL")
            return False
        return True
    
    def method_31(self):
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtEnrouteAltitude.text()), AltitudeUnits.FT))
        self.iasChanged()
    def method_36(self, double_0, double_1, double_2, double_3, turnDirection_0, double_4, double_5, double_6, point3d_0):
        num = None;
        num = -1 if(turnDirection_0 != TurnDirection.Right) else 1;
        num1 = int(math.trunc((double_1 - double_0) / double_2));
        point3dCollection = [];
        for i in range(num1 + 1):
            double0 = double_0 / double_5;
            double4 = double_4 / 3600;
            double6 = double_6 + double0 * double4 * 1000;
            double3 = double_3 + Unit.ConvertDegToRad(-90 * num + double_0 * num);
            point3dCollection.append(MathHelper.distanceBearingPoint(point3d_0, double3, double6));
            double_0 = double_0 + double_2;
        return point3dCollection;
    
    def method_37(self, point3d_0, point3d_1, point3d_2, turnDirection_0):
        num = None;
        num1 = MathHelper.calcDistance(point3d_1, point3d_2);
        num2 = MathHelper.getBearing(point3d_0, point3d_1);
        num3 = MathHelper.getBearing(point3d_0, point3d_2);
        num4 = max([num2, num3]) - min([num2, num3]);
        if (num4 > 3.14159265358979):
            num4 = 6.28318530717959 - num4;
        num5 = MathHelper.calcDistance(point3d_0, point3d_1);
        double_0 = num1 / (2 * math.sin(num4));
        point3d = MathHelper.distanceBearingPoint(point3d_0, num2, num5 / 2);
        num = num2 - 1.570796327 if(turnDirection_0 != TurnDirection.Right) else num2 + 1.570796327;
        num6 = math.sqrt(double_0 * double_0 - num5 / 2 * (num5 / 2));
        return (MathHelper.distanceBearingPoint(point3d, num, num6), double_0);
    
    def  method_38(self, point3d_0, point3d_1, point3d_2, double_0, double_1, double_2, point3d_3, point3d_4, point3d_5):
        point3d = None;
        point3d1 = None;
        point3d = MathHelper.getIntersectionPoint(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_0, 0.1), point3d_1, point3d_2) 
        point3d1 = MathHelper.getIntersectionPoint(point3d_3, MathHelper.distanceBearingPoint(point3d_3, double_0, 0.1), point3d_4, point3d_5)
        if (point3d == None or MathHelper.calcDistance(point3d_0, point3d) >= double_2 or point3d1 == None):
            double_3 = None;
            return (False, double_3);
        num = MathHelper.calcDistance(point3d_3, point3d1);
        double_3 = math.acos(num / double_1);
        return (True, double_3);
    
    def method_39(self):
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        num =  None;
        num1 =  None;
        num2 =  None;
        num3 =  None;
        num4 =  None;
        num5 =  None;
        num6 =  None;
        num7 =  None;
        num8 =  None;
        num9 =  None
        num10 =  None;
        num11 =  None;
        num12 =  None;
        num13 =  None;
        num14 =  None;
        num15 =  None;
        num16 =  None;
        turnDirection = None;
        list_0 = [];
        list_1 = [];
        point3d3 = self.parametersPanel.pnlNavAid.Point3d;
        point3d4 = point3d3;
        point3d5 = point3d4;
        point3d6 = point3d4;
        point3d7 = point3d4;
        point3d8 = point3d4;
        point3d9 = point3d4;
        point3d10 = point3d4;
        point3d11 = point3d4;
        point3d12 = point3d4;
        point3d13 = point3d4;
        point3d14 = point3d4;
        point3d15 = point3d4;
        point3d16 = point3d4;
        point3d17 = point3d4;
        point3d18 = point3d4;
        point3d19 = point3d4;
        point3d20 = point3d4;
        point3d21 = point3d4;
        item = point3d4;
        item1 = point3d4;
        item2 = point3d4;
        item3 = point3d4;
        item4 = point3d4;
        item5 = point3d4;
        point3d22 = point3d4;
        point3d23 = point3d4;
        point3d24 = point3d4;
        point3d25 = point3d4;
        point3d26 = point3d4;
        point3d27 = point3d4;
        point3d28 = point3d4;
        enrouteAltitude = Altitude(float(self.parametersPanel.txtEnrouteAltitude.text()), AltitudeUnits.FT)
#         navAidAltitude = Altitude(float(self.parametersPanel.txtEnrouteAltitude.text()), AltitudeUnits.FT)
        speed = Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtEnrouteAltitude.text()), AltitudeUnits.FT));
        metres = enrouteAltitude.Metres - self.parametersPanel.pnlNavAid.Altitude().Metres;
        num16 = metres * 0.839099631 if(self.parametersPanel.cmbNavAidType.SelectedIndex != 0) else metres * 1.191753593;
        num17 = Unit.ConvertDegToRad(float(self.parametersPanel.txtBankAngle.text()));
        num18 = math.sin(num17) / math.cos(num17);
        num19 = min([3431 * num18 / (3.14159265358979 * speed.Knots), 3]);
        num20 = Unit.ConvertNMToMeter(speed.Knots / (3.14159265358979 * num19 * 20));
        metresPerSecond = speed.MetresPerSecond;
        value = self.parametersPanel.pnlWind.Value;
        metresPerSecond1 = (metresPerSecond + value.MetresPerSecond) * (float(self.parametersPanel.txtPilotTime.text()) + float(self.parametersPanel.txtBankEstTime.text()));
        value1 = float(self.parametersPanel.txtInBound.text())
        value2 = float(self.parametersPanel.txtOutBound.text());
        turnDirectionList = []
        num21 = MathHelper.smethod_77(value1, value2, AngleUnits.Degrees, turnDirectionList);
        turnDirection =turnDirectionList[0]
        kilometresPerHour = self.parametersPanel.pnlWind.Value.KilometresPerHour;
        num22 = Unit.ConvertDegToRad(value1);
        num23 = num22 + 3.14159265358979;
        point3d29 = MathHelper.distanceBearingPoint(point3d3, num23, num16);
        num24 = Unit.ConvertDegToRad(num21 / 2);
        num25 = num20 * (math.sin(num24) / math.cos(num24));
        point3d28 = MathHelper.distanceBearingPoint(point3d29, num23, num25);
        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 0):
            num = 9300;
        else:
            num = 9300 if(not self.parametersPanel.chbOverhead.isChecked()) else 7408;
        if (turnDirection != TurnDirection.Left):
            num1 = num22 - 1.570796327;
            num3 = num22 + 1.570796327;
            num4 = num22 + Unit.ConvertDegToRad(num21);
            num5 = num22 + Unit.ConvertDegToRad(num21 / 2);
            num6 = num4 + 3.14159265358979 + 0.523598776;
            num7 = num6 + 1.570796327;
            num8 = num4 - 1.570796327;
            num9 = num4 + 1.570796327;
        else:
            num1 = num22 + 1.570796327;
            num3 = num22 - 1.570796327;
            num4 = num22 - Unit.ConvertDegToRad(num21);
            num5 = num22 - Unit.ConvertDegToRad(num21 / 2);
            num6 = num4 + 3.14159265358979 - 0.523598776;
            num7 = num6 - 1.570796327;
            num8 = num4 + 1.570796327;
            num9 = num4 - 1.570796327;
        point3d23 = MathHelper.distanceBearingPoint(point3d28, num1, num);
        point3d24 = MathHelper.distanceBearingPoint(point3d28, num3, num);
        point3d14 = MathHelper.distanceBearingPoint(point3d23, num1, num);
        point3d15 = MathHelper.distanceBearingPoint(point3d24, num3, num);
        num26 = 2 * num16 + num25 + metresPerSecond1;
        point3d13 = MathHelper.distanceBearingPoint(point3d14, num22, num26);
        point3d22 = MathHelper.distanceBearingPoint(point3d13, num3, num);
        point3d30 = MathHelper.distanceBearingPoint(point3d22, num3, num20);
        point3d31 = MathHelper.distanceBearingPoint(point3d22, num3, 2 * num);
        point3d32 = MathHelper.distanceBearingPoint(point3d31, num3, num20);
        point3d33 = MathHelper.distanceBearingPoint(point3d24, num5, 1);
        point3d34 = MathHelper.distanceBearingPoint(point3d3, num4, 1);
        point3d = MathHelper.getIntersectionPoint(point3d24, point3d33, point3d3, point3d34);
        num27 = Unit.ConvertDegToRad(num21 / 2);
        num28 = num / math.sin(num27);
        point3d25 = MathHelper.distanceBearingPoint(point3d, num5 + 3.14159265358979, num28);
        num29 = num / (math.sin(num27) / math.cos(num27));
        point3d35 = MathHelper.distanceBearingPoint(point3d, num4 + 3.14159265358979, num29);
        point3d16 = MathHelper.distanceBearingPoint(point3d25, MathHelper.getBearing(point3d35, point3d25), num);
        point3dCollection = self.method_36(0, 96, 48, num22, turnDirection, kilometresPerHour, num19, num20, point3d30);
        item5 = point3dCollection[1];
        item4 = point3dCollection[2];
        point3d36, num10 = self.method_37(point3d22, item5, item4, turnDirection);
        list_0.append(point3d36);
        list_1.append(num10);
        item5 = MathHelper.distanceBearingPoint(point3d36, MathHelper.getBearing(point3d36, point3d22) - 0.001, num10) if(turnDirection != TurnDirection.Right) else  MathHelper.distanceBearingPoint(point3d36, MathHelper.getBearing(point3d36, point3d22) + 0.001, num10);
        point3d13 = MathHelper.distanceBearingPoint(point3d36, MathHelper.getBearing(point3d36, point3d13), num10 + num);
        point3d12 = MathHelper.distanceBearingPoint(point3d36, MathHelper.getBearing(point3d36, point3d13) - 0.01, num10 + num) if(turnDirection != TurnDirection.Right) else MathHelper.distanceBearingPoint(point3d36, MathHelper.getBearing(point3d36, point3d13) + 0.01, num10 + num);
        point3d7 = MathHelper.distanceBearingPoint(point3d36, MathHelper.getBearing(point3d36, item4), num10 + num);
        if (num21 <= 60):
            point3d5 = MathHelper.distanceBearingPoint(point3d36, num7, num10);
            point3d1 = MathHelper.distanceBearingPoint(point3d5, num6 + 3.14159265358979, 1);
            point3d27 = MathHelper.getIntersectionPoint(point3d5, point3d1, point3d3, point3d34);
            point3d7 = MathHelper.distanceBearingPoint(point3d36, MathHelper.getBearing(point3d36, point3d5), num10 + num);
        point3d11 = point3d7;
        if (num21 > 60):
            point3dCollection = self.method_36(96, 180, 42, num22, turnDirection, kilometresPerHour, num19, num20, point3d32);
            item2 = point3dCollection[1];
            item3 = point3dCollection[0];
            item1 = point3dCollection[2];
            point3d36, num10 = self.method_37(point3dCollection[0], item2, item1, turnDirection);
            list_0.append(point3d36);
            list_1.append(num10);
            point3d5 = MathHelper.distanceBearingPoint(point3d36, num7, num10);
            point3d1 = MathHelper.distanceBearingPoint(point3d5, num6 + 3.14159265358979, 1);
            point3d27 = MathHelper.getIntersectionPoint(point3d5, point3d1, point3d3, point3d34);
            item2 = MathHelper.distanceBearingPoint(point3d36, MathHelper.getBearing(point3d36, item3) - 0.001, num10) if(turnDirection != TurnDirection.Right) else MathHelper.distanceBearingPoint(point3d36, MathHelper.getBearing(point3d36, item3) + 0.001, num10);
            point3d10 = MathHelper.distanceBearingPoint(point3d36, MathHelper.getBearing(point3d36, item3), num10 + num);
            point3d9 = MathHelper.distanceBearingPoint(point3d36, MathHelper.getBearing(point3d36, item2), num10 + num);
            point3d7 = MathHelper.distanceBearingPoint(point3d36, MathHelper.getBearing(point3d36, point3d5), num10 + num);
        if (num21 > 150):
            point3dCollection1 = self.method_36(180, 270, 45, num22, turnDirection, kilometresPerHour, num19, num20, point3d32);
            item = point3dCollection1[1];
            item6 = point3dCollection1[0];
            item7 = point3dCollection1[2];
            point3d37, num11 = self.method_37(point3dCollection1[0], item, item7, turnDirection);
            list_0.append(point3d37);
            list_1.append(num11);
            point3d21 = MathHelper.distanceBearingPoint(point3d37, num7, num11);
            point3d38 = MathHelper.distanceBearingPoint(point3d21, num6 + 3.14159265358979, 1);
            point3d27 = MathHelper.getIntersectionPoint(point3d21, point3d38, point3d3, point3d34);
            item = MathHelper.distanceBearingPoint(point3d37, MathHelper.getBearing(point3d37, item6) - 0.001, num11) if(turnDirection != TurnDirection.Right) else MathHelper.distanceBearingPoint(point3d37, MathHelper.getBearing(point3d37, item6) + 0.001, num11);
            point3d7 = MathHelper.distanceBearingPoint(point3d37, MathHelper.getBearing(point3d37, point3d21), num11 + num);
            point3d8 = MathHelper.distanceBearingPoint(point3d37, MathHelper.getBearing(point3d37, item), num11 + num);
        point3d20 = MathHelper.distanceBearingPoint(point3d27, num6, num * 2);
        point3d26 = MathHelper.distanceBearingPoint(point3d27, num9, num);
        point3d17 = MathHelper.distanceBearingPoint(point3d27, num9, num * 2);
        point3d19 = MathHelper.distanceBearingPoint(point3d27, num8, num);
        point3d18 = MathHelper.distanceBearingPoint(point3d27, num8, num * 2);
        point3d39 = MathHelper.distanceBearingPoint(point3d7, num6 + 3.14159265358979, 1);
        point3d40 = MathHelper.distanceBearingPoint(point3d18, num4 + 3.14159265358979, 1);
        point3d6 = MathHelper.getIntersectionPoint(point3d7, point3d39, point3d18, point3d40);
        if (num21 <= 40):
            result, num2 =  self.method_38(point3d5, point3d27, point3d3, num8, num10, num, point3d36, point3d19, point3d20)
            if (result):
                point3d5 = MathHelper.distanceBearingPoint(point3d36, num8 + num2, num10) if(turnDirection != TurnDirection.Left) else MathHelper.distanceBearingPoint(point3d36, num8 - num2, num10);
            result, num15 = self.method_38(point3d7, point3d27, point3d3, num8, num10 + num, 2 * num, point3d36, point3d18, point3d6)
            if (result):
                point3d7 = MathHelper.distanceBearingPoint(point3d36, num8 + num15, num10 + num) if(turnDirection != TurnDirection.Left) else MathHelper.distanceBearingPoint(point3d36, num8 - num15, num10 + num);
        point3d41 = MathHelper.distanceBearingPoint(point3d15, num8, 0.1);
        point3d2 = MathHelper.getIntersectionPoint(point3d15, point3d41, point3d27, point3d3);
        num30 = MathHelper.calcDistance(point3d15, point3d2);
        if (num30 < 2 * num):
            num12 = 2 * num - num30;
            num13 = num12 / 0.267949192;
            num14 = math.sqrt(num12 * num12 + num13 * num13);
            point3d16 = MathHelper.distanceBearingPoint(point3d15, num4 + 0.261799388, num14) if(turnDirection != TurnDirection.Left) else MathHelper.distanceBearingPoint(point3d15, num4 - 0.261799388, num14);
        point3d41 = MathHelper.distanceBearingPoint(point3d24, num8, 0.1);
        point3d2 = MathHelper.getIntersectionPoint(point3d24, point3d41, point3d27, point3d3);
        num  = MathHelper.calcDistance(point3d24, point3d2);
        if (num30 < 2 * num and num21 > 75):
            num12 = 2 * num - num30;
            num13 = num12 / 0.267949192;
            num14 = math.sqrt(num12 * num12 + num13 * num13);
            point3d15 = MathHelper.distanceBearingPoint(point3d24, num4 + 0.261799388, num14) if(turnDirection != TurnDirection.Left) else MathHelper.distanceBearingPoint(point3d24, num4 - 0.261799388, num14);
            point3d16 = MathHelper.distanceBearingPoint(point3d15, MathHelper.getBearing(point3d15, point3d17), 0.1);
        point3dCollectionList = [];
        point3dArray = [point3d28, point3d3, point3d27];
        point3dCollectionList.extend(point3dArray)
#         point3dCollectionList.append(point3dArray);
        point3dArray = [point3d26, point3d25, point3d24, point3d23, point3d22, item5, item4, item3, item2, item1, item, point3d21, point3d20, point3d19];
        point3dCollectionList.extend(point3dArray)
#         point3dCollectionList.append(point3dArray);
        point3dArray = [point3d18, point3d17, point3d16, point3d15, point3d14, point3d13, point3d12, point3d11, point3d10, point3d9, point3d8, point3d7, point3d6, point3d5];
        point3dCollectionList.extend(point3dArray)
#         point3dCollectionList.append(point3dArray);
        return (point3dCollectionList, list_0, list_1);
    
    def captureBearingInBound(self):
        self.captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtInBound)
        define._canvas.setMapTool(self.captureTrackTool)
    def captureBearingOutBound(self):
        self.captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtOutBound)
        define._canvas.setMapTool(self.captureTrackTool)
        
class EnrouteTurnOverheadObstacles(ObstacleTable):
    def __init__(self, surfacesArea, altitude_0, altitude_1):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesArea)
        
        self.surfaceType = SurfaceTypes.EnrouteTurnOverHead
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
        mocMultiplier = self.primaryMoc * obstacle_0.MocMultiplier;
        obstacleAreaResult, num, num1 = self.area.pointInArea(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier);
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