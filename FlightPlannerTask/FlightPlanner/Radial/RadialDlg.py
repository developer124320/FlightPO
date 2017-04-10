# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication, Qt, QString
from PyQt4.QtGui import QColor, QMessageBox, QStandardItem, QFileDialog
from qgis.core import QGis, QgsVectorLayer
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapToolPan
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import ObstacleTableColumnType, SurfaceTypes, \
                 DistanceUnits,AltitudeUnits, Point3D, \
                 ObstacleAreaResult, ConstructionType
from FlightPlanner.Radial.ui_RadialNew import Ui_Radial
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.polylineArea import PolylineArea
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, ComplexObstacleArea, SecondaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.Captions import Captions
from FlightPlanner.AcadHelper import AcadHelper

import define, math

class RadialDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)

        self.currentLayer = define._canvas.currentLayer()
        self.setObjectName("RadialDlg")
        self.surfaceType = SurfaceTypes.Radial
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.Radial)
        self.resize(540, 550)
        QgisHelper.matchingDialogSize(self, 720, 550)
        self.surfaceList = None
        self.complexObstacleArea = ComplexObstacleArea()

        self.vorDmeFeatureArray = []

        self.initBasedOnCmb()
    def initBasedOnCmb(self):

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
                for feat in vorDmeFeatureList:
                    typeValue = feat.attributes()[idx].toString()
                    nameValue = feat.attributes()[idxName].toString()
                    basedOnCmbObjItems.append(typeValue + " " + nameValue)
                basedOnCmbObjItems.sort()
                basedOnCmbObj.Items = basedOnCmbObjItems
                basedOnCmbObj.SelectedIndex = 0

                # if idxAttributes
                feat = vorDmeFeatureList[0]
                attrValue = feat.attributes()[idxLat].toDouble()
                lat = attrValue[0]

                attrValue = feat.attributes()[idxLong].toDouble()
                long = attrValue[0]

                attrValue = feat.attributes()[idxAltitude].toDouble()
                alt = attrValue[0]

                vorDmePositionPanelObj.Point3d = Point3D(long, lat, alt)
                self.connect(basedOnCmbObj, SIGNAL("Event_0"), self.basedOnCmbObj_Event_0)

        return vorDmeFeatureList
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

        feat = self.vorDmeFeatureArray[self.parametersPanel.cmbBasedOn.SelectedIndex]
        attrValue = feat.attributes()[idxLat].toDouble()
        lat = attrValue[0]

        attrValue = feat.attributes()[idxLong].toDouble()
        long = attrValue[0]

        attrValue = feat.attributes()[idxAltitude].toDouble()
        alt = attrValue[0]

        self.parametersPanel.pnlNavAid.Point3d = Point3D(long, lat, alt)

    def initObstaclesModel(self):
        self.obstaclesModel.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        return FlightPlanBaseDlg.initObstaclesModel(self)

    
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
        parameterList.append(("general", "group"))
        parameterList.append(("Navigational Aid", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlNavAid.txtPointX.text()), float(self.parametersPanel.pnlNavAid.txtPointY.text()))

        parameterList.append(("Type", self.parametersPanel.cmbNavAidType.SelectedItem))

        parameterList.append(("Lat", self.parametersPanel.pnlNavAid.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlNavAid.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlNavAid.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlNavAid.txtPointY.text()))

        
        parameterList.append(("Parameters", "group"))

        parameterList.append(("Radial", "Plan : " + str(self.parametersPanel.txtTrackRadial.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtTrackRadial.txtRadialGeodetic.Value) + define._degreeStr))

        # parameterList.append(("Radial", self.parametersPanel.txtTrackRadial.Value))
        parameterList.append(("Distance to Start", self.parametersPanel.txtDistStart.text() + "nm"))
        parameterList.append(("Distance to Finish", self.parametersPanel.txtDistFinish.text() + "nm"))
        parameterList.append(("Tolerance Type", self.parametersPanel.cmbToleranceType.currentText()))
        parameterList.append(("MOCmultipiler", self.parametersPanel.mocSpinBox.text()))

        if self.parametersPanel.cmbToleranceType.currentIndex() == 2:
            parameterList.append(("Selection Mode", self.parametersPanel.cmbSelectionMode.currentText()))
            parameterList.append(("Construction Type", self.parametersPanel.cmbConstructionType.currentText()))
            parameterList.append(("Primary Moc", self.parametersPanel.txtPrimaryMOC.text() + "m"))
            parameterList.append(("", self.parametersPanel.txtPrimaryMOCFt.text() + "ft"))
            parameterList.append(("2nm over-head the VOR", str(self.parametersPanel.chbOverhead.isChecked())))


        parameterList.append(("Results / Checked Obstacles", "group"))
        parameterList.append(("Checked Obstacles", "group"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        
        
        return parameterList
    
    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        
        
        
#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)
    
        
    def btnPDTCheck_Click(self):
        pdtResultStr = MathHelper.pdtCheckResultToString(float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), float(self.parametersPanel.txtIas.text()), float(self.parametersPanel.txtTime.text()))
        
        QMessageBox.warning(self, "PDT Check", pdtResultStr)
    def btnEvaluate_Click(self):
        self.complexObstacleArea = ComplexObstacleArea()
        num = None;
        num1 = None;
        num2 = None;
        num3 = None;
        line = None;
#         if (!AcadHelper.Ready)
#         {
#             return;
#         }
#         if (!self.method_27(true))
#         {
#             return;
#         }
        constructionLayer = None;
        nominalTrackLayer = None;
        mapUnits = define._canvas.mapUnits()

        point3d = self.parametersPanel.pnlNavAid.Point3d;
        metres = Altitude(float(self.parametersPanel.txtStartAltitude.text())).Metres;
        metres1 = Altitude(float(self.parametersPanel.txtPrimaryMOC.text())).Metres;
        percent = float(self.parametersPanel.txtAltitudeChange.text());
        num4 = Unit.ConvertDegToRad(float(self.parametersPanel.txtTrackRadial.Value));
        metres2 = Distance(float(self.parametersPanel.txtDistStart.text()), DistanceUnits.NM).Metres;
        metres3 = Distance(float(self.parametersPanel.txtDistFinish.text()), DistanceUnits.NM).Metres;

        # if define._mapCrs == None:
        #     if mapUnits == QGis.Meters:
        #         nominalTrackLayer = QgsVectorLayer("linestring?crs=EPSG:32633", "NominalTrack", "memory")
        #     else:
        #         nominalTrackLayer = QgsVectorLayer("linestring?crs=EPSG:4326", "NominalTrack", "memory")
        # else:
        #     nominalTrackLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), "NominalTrack", "memory")
        # nominalTrackLayer.startEditing()
        # polyline = QgsGeometry.fromPolyline([MathHelper.distanceBearingPoint(point3d, num4, metres2), MathHelper.distanceBearingPoint(point3d, num4, metres3)])
        # feature = QgsFeature()
        # feature.setGeometry(polyline)
        # nominalTrackLayer.addFeature(feature)
        # nominalTrackLayer.commitChanges()


        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 0):
            num = Unit.ConvertDegToRad(6.2);
            num1 = Unit.ConvertDegToRad(6.9);
            num2 = Unit.ConvertDegToRad(10.3);
        else:
            num = Unit.ConvertDegToRad(4.5);
            num1 = Unit.ConvertDegToRad(5.2);
            num2 = Unit.ConvertDegToRad(7.8);
        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 0):
            num3 = 2315 if(self.parametersPanel.cmbToleranceType.currentIndex() != 2 or not self.parametersPanel.chbOverhead.isChecked()) else 4630;
        else:
            num3 = 1900 if(self.parametersPanel.cmbToleranceType.currentIndex() != 2 or not self.parametersPanel.chbOverhead.isChecked()) else 3704;
        num5 = num4 + num;
        num6 = num4 - num;
        num7 = num4 + num1;
        num8 = num4 - num1;
        num9 = num4 + num2;
        num10 = num4 - num2;
        num11 = num4 + Unit.ConvertDegToRad(90);
        num12 = num4 - Unit.ConvertDegToRad(90);
        num13 = metres2 / math.cos(num);
        num14 = metres2 / math.cos(num1);
        num15 = metres2 / math.cos(num2);
        num16 = metres3 / math.cos(num);
        num17 = metres3 / math.cos(num1);
        num18 = metres3 / math.cos(num2);
        point3d1 = MathHelper.distanceBearingPoint(point3d, num4, metres2);
        point3d2 = MathHelper.distanceBearingPoint(point3d, num4, metres3);
        point3d3 = MathHelper.distanceBearingPoint(point3d, num12, num3);
        point3d4 = MathHelper.distanceBearingPoint(point3d, num11, num3);
        point3d5 = MathHelper.distanceBearingPoint(point3d4, num9, num15);
        point3d6 = MathHelper.distanceBearingPoint(point3d3, num10, num15);
        num19 = MathHelper.calcDistance(point3d1, point3d5) / 2;
        point3d7 = MathHelper.distanceBearingPoint(point3d1, num12, num19);
        point3d8 = MathHelper.distanceBearingPoint(point3d1, num11, num19);
        point3d9 = MathHelper.distanceBearingPoint(point3d3, num10, num18);
        point3d10 = MathHelper.distanceBearingPoint(point3d4, num9, num18);
        num20 = MathHelper.calcDistance(point3d2, point3d10) / 2;
        point3d11 = MathHelper.distanceBearingPoint(point3d2, num12, num20);
        point3d12 = MathHelper.distanceBearingPoint(point3d2, num11, num20);

        resultPoint3dArrayList = []


        if (self.parametersPanel.cmbToleranceType.currentIndex() == 0):
            resultPoint3dArrayList.append([point3d1, point3d2])
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num5, num16), MathHelper.distanceBearingPoint(point3d, num5, num13)])
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num5, num13), MathHelper.distanceBearingPoint(point3d, num6, num13)]);
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num6, num13), MathHelper.distanceBearingPoint(point3d, num6, num16)]);
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num6, num16), MathHelper.distanceBearingPoint(point3d, num5, num16)]);

            polylineArea0 = PolylineArea([MathHelper.distanceBearingPoint(point3d, num5, num16), MathHelper.distanceBearingPoint(point3d, num5, num13), MathHelper.distanceBearingPoint(point3d, num6, num13), MathHelper.distanceBearingPoint(point3d, num6, num16), MathHelper.distanceBearingPoint(point3d, num6, num16), MathHelper.distanceBearingPoint(point3d, num5, num16)])
            self.complexObstacleArea.Add(PrimaryObstacleArea(polylineArea0))
        elif (self.parametersPanel.cmbToleranceType.currentIndex() == 1):
            resultPoint3dArrayList.append([point3d1, point3d2]);
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num7, num17), MathHelper.distanceBearingPoint(point3d, num7, num14)]);
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num7, num14), MathHelper.distanceBearingPoint(point3d, num8, num14)]);
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num8, num14), MathHelper.distanceBearingPoint(point3d, num8, num17)]);
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num8, num17), MathHelper.distanceBearingPoint(point3d, num7, num17)]);
            polylineArea0 = PolylineArea([MathHelper.distanceBearingPoint(point3d, num7, num17), MathHelper.distanceBearingPoint(point3d, num7, num14), MathHelper.distanceBearingPoint(point3d, num8, num14), MathHelper.distanceBearingPoint(point3d, num8, num17), MathHelper.distanceBearingPoint(point3d, num8, num17), MathHelper.distanceBearingPoint(point3d, num7, num17)])
            self.complexObstacleArea.Add(PrimaryObstacleArea(polylineArea0))
        elif (self.parametersPanel.cmbToleranceType.currentIndex() == 2):
            if (self.parametersPanel.cmbConstructionType.currentText() != ConstructionType.Construct2D):
                num21 = metres - metres1;
                num22 = percent / 100;
                num23 = num21 + (metres3 - metres2) * num22;
                num24 = metres + (metres3 - metres2) * num22;
                point3d5 = point3d5.smethod_167(metres);
                point3d6 = point3d6.smethod_167(metres);
                point3d9 = point3d9.smethod_167(num24);
                point3d10 = point3d10.smethod_167(num24);
                point3d8 = point3d8.smethod_167(num21);
                point3d12 = point3d12.smethod_167(num23);
                point3d7 = point3d7.smethod_167(num21);
                point3d11 = point3d11.smethod_167(num23);
                point3d1 = point3d1.smethod_167(metres);
                point3d2 = point3d2.smethod_167(num24);
                # resultPoint3dArrayList.append([point3d8, point3d5, point3d10, point3d12]);
                resultPoint3dArrayList.append([point3d8, point3d12, point3d11, point3d7]);
                resultPoint3dArrayList.append([point3d7, point3d11, point3d9, point3d6]);

                self.complexObstacleArea.Add(PrimaryObstacleArea(PolylineArea([point3d8, point3d12, point3d11, point3d7, point3d8])))
                self.complexObstacleArea.Add(SecondaryObstacleArea(point3d8, point3d12, point3d5, point3d10, MathHelper.getBearing(point3d8, point3d12)))
                self.complexObstacleArea.Add(SecondaryObstacleArea(point3d7, point3d11, point3d6, point3d9, MathHelper.getBearing(point3d7, point3d11)))
            else:
                resultPoint3dArrayList.append([point3d1, point3d2]);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                resultPoint3dArrayList.append([point3d6, point3d5]);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                resultPoint3dArrayList.append([point3d5, point3d10]);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                resultPoint3dArrayList.append([point3d10, point3d9]);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                resultPoint3dArrayList.append([point3d9, point3d6]);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                resultPoint3dArrayList.append([point3d7, point3d11]);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                resultPoint3dArrayList.append([point3d8, point3d12]);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
#                 num21 = metres - metres1;
#                 num22 = percent / 100;
#                 num23 = num21 + (metres3 - metres2) * num22;
#                 num24 = metres + (metres3 - metres2) * num22;
#                 point3d5 = point3d5.smethod_167(0);
#                 point3d6 = point3d6.smethod_167(0);
#                 point3d9 = point3d9.smethod_167(0);
#                 point3d10 = point3d10.smethod_167(0);
#                 point3d8 = point3d8.smethod_167(0);
#                 point3d12 = point3d12.smethod_167(0);
#                 point3d7 = point3d7.smethod_167(0);
#                 point3d11 = point3d11.smethod_167(0);
#                 point3d1 = point3d1.smethod_167(0);
#                 point3d2 = point3d2.smethod_167(0);
                # resultPoint3dArrayList.append([point3d8, point3d5, point3d10, point3d12]);
                # resultPoint3dArrayList.append([point3d8, point3d12, point3d11, point3d7]);
                # resultPoint3dArrayList.append([point3d7, point3d11, point3d9, point3d6]);

                self.complexObstacleArea.Add(PrimaryObstacleArea(PolylineArea([point3d8, point3d12, point3d11, point3d7, point3d8])))
                self.complexObstacleArea.Add(SecondaryObstacleArea(point3d8, point3d12, point3d5, point3d10, MathHelper.getBearing(point3d8, point3d12)))
                self.complexObstacleArea.Add(SecondaryObstacleArea(point3d7, point3d11, point3d6, point3d9, MathHelper.getBearing(point3d7, point3d11)))

        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        self.obstaclesModel = RadialObstacles(self.complexObstacleArea, Altitude(float(self.parametersPanel.txtPrimaryMOC.text())), self.manualPolygon );

        return FlightPlanBaseDlg.btnEvaluate_Click(self)

    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        self.complexObstacleArea = ComplexObstacleArea()
        num = None;
        num1 = None;
        num2 = None;
        num3 = None;
        line = None;
#         if (!AcadHelper.Ready)
#         {
#             return;
#         }
#         if (!self.method_27(true))
#         {
#             return;
#         }
        constructionLayer = None;
        nominalTrackLayer = None;
        mapUnits = define._canvas.mapUnits()
        
        point3d = self.parametersPanel.pnlNavAid.Point3d;
        metres = Altitude(float(self.parametersPanel.txtStartAltitude.text())).Metres;
        metres1 = Altitude(float(self.parametersPanel.txtPrimaryMOC.text())).Metres;
        percent = float(self.parametersPanel.txtAltitudeChange.text());
        num4 = Unit.ConvertDegToRad(float(self.parametersPanel.txtTrackRadial.Value));
        metres2 = Distance(float(self.parametersPanel.txtDistStart.text()), DistanceUnits.NM).Metres;
        metres3 = Distance(float(self.parametersPanel.txtDistFinish.text()), DistanceUnits.NM).Metres;

        nominalTrackLayer = AcadHelper.createNominalTrackLayer([MathHelper.distanceBearingPoint(point3d, num4, metres2), MathHelper.distanceBearingPoint(point3d, num4, metres3)], None, "memory", "NominalTrack_" + self.surfaceType.replace(" ", "_").replace("-", "_"))

        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 0):
            num = Unit.ConvertDegToRad(6.2);
            num1 = Unit.ConvertDegToRad(6.9);
            num2 = Unit.ConvertDegToRad(10.3);
        else:
            num = Unit.ConvertDegToRad(4.5);
            num1 = Unit.ConvertDegToRad(5.2);
            num2 = Unit.ConvertDegToRad(7.8);
        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 0):
            num3 = 2315 if(self.parametersPanel.cmbToleranceType.currentIndex() != 2 or not self.parametersPanel.chbOverhead.isChecked()) else 4630;
        else:
            num3 = 1900 if(self.parametersPanel.cmbToleranceType.currentIndex() != 2 or not self.parametersPanel.chbOverhead.isChecked()) else 3704;
        num5 = num4 + num;
        num6 = num4 - num;
        num7 = num4 + num1;
        num8 = num4 - num1;
        num9 = num4 + num2;
        num10 = num4 - num2;
        num11 = num4 + Unit.ConvertDegToRad(90);
        num12 = num4 - Unit.ConvertDegToRad(90);
        num13 = metres2 / math.cos(num);
        num14 = metres2 / math.cos(num1);
        num15 = metres2 / math.cos(num2);
        num16 = metres3 / math.cos(num);
        num17 = metres3 / math.cos(num1);
        num18 = metres3 / math.cos(num2);
        point3d1 = MathHelper.distanceBearingPoint(point3d, num4, metres2);
        point3d2 = MathHelper.distanceBearingPoint(point3d, num4, metres3);
        point3d3 = MathHelper.distanceBearingPoint(point3d, num12, num3);
        point3d4 = MathHelper.distanceBearingPoint(point3d, num11, num3);
        point3d5 = MathHelper.distanceBearingPoint(point3d4, num9, num15);
        point3d6 = MathHelper.distanceBearingPoint(point3d3, num10, num15);
        num19 = MathHelper.calcDistance(point3d1, point3d5) / 2;
        point3d7 = MathHelper.distanceBearingPoint(point3d1, num12, num19);
        point3d8 = MathHelper.distanceBearingPoint(point3d1, num11, num19);
        point3d9 = MathHelper.distanceBearingPoint(point3d3, num10, num18);
        point3d10 = MathHelper.distanceBearingPoint(point3d4, num9, num18);
        num20 = MathHelper.calcDistance(point3d2, point3d10) / 2;
        point3d11 = MathHelper.distanceBearingPoint(point3d2, num12, num20);
        point3d12 = MathHelper.distanceBearingPoint(point3d2, num11, num20);
        
        resultPoint3dArrayList = []
        
        
        if (self.parametersPanel.cmbToleranceType.currentIndex() == 0):
            resultPoint3dArrayList.append([point3d1, point3d2])
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num5, num16), MathHelper.distanceBearingPoint(point3d, num5, num13)])
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num5, num13), MathHelper.distanceBearingPoint(point3d, num6, num13)]);
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num6, num13), MathHelper.distanceBearingPoint(point3d, num6, num16)]);
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num6, num16), MathHelper.distanceBearingPoint(point3d, num5, num16)]);

            polylineArea0 = PolylineArea([MathHelper.distanceBearingPoint(point3d, num5, num16), MathHelper.distanceBearingPoint(point3d, num5, num13), MathHelper.distanceBearingPoint(point3d, num6, num13), MathHelper.distanceBearingPoint(point3d, num6, num16), MathHelper.distanceBearingPoint(point3d, num6, num16), MathHelper.distanceBearingPoint(point3d, num5, num16)])
            self.complexObstacleArea.Add(PrimaryObstacleArea(polylineArea0))
        elif (self.parametersPanel.cmbToleranceType.currentIndex() == 1):
            resultPoint3dArrayList.append([point3d1, point3d2]);
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num7, num17), MathHelper.distanceBearingPoint(point3d, num7, num14)]);
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num7, num14), MathHelper.distanceBearingPoint(point3d, num8, num14)]);
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num8, num14), MathHelper.distanceBearingPoint(point3d, num8, num17)]);
            resultPoint3dArrayList.append([MathHelper.distanceBearingPoint(point3d, num8, num17), MathHelper.distanceBearingPoint(point3d, num7, num17)]);
            polylineArea0 = PolylineArea([MathHelper.distanceBearingPoint(point3d, num7, num17), MathHelper.distanceBearingPoint(point3d, num7, num14), MathHelper.distanceBearingPoint(point3d, num8, num14), MathHelper.distanceBearingPoint(point3d, num8, num17), MathHelper.distanceBearingPoint(point3d, num8, num17), MathHelper.distanceBearingPoint(point3d, num7, num17)])
            self.complexObstacleArea.Add(PrimaryObstacleArea(polylineArea0))
        elif (self.parametersPanel.cmbToleranceType.currentIndex() == 2):
            if (self.parametersPanel.cmbConstructionType.currentText() != ConstructionType.Construct2D):
                num21 = metres - metres1;
                num22 = percent / 100;
                num23 = num21 + (metres3 - metres2) * num22;
                num24 = metres + (metres3 - metres2) * num22;
                point3d5 = point3d5.smethod_167(metres);
                point3d6 = point3d6.smethod_167(metres);
                point3d9 = point3d9.smethod_167(num24);
                point3d10 = point3d10.smethod_167(num24);
                point3d8 = point3d8.smethod_167(num21);
                point3d12 = point3d12.smethod_167(num23);
                point3d7 = point3d7.smethod_167(num21);
                point3d11 = point3d11.smethod_167(num23);
                point3d1 = point3d1.smethod_167(metres);
                point3d2 = point3d2.smethod_167(num24);
                resultPoint3dArrayList.append([point3d8, point3d5, point3d10, point3d12]);
                resultPoint3dArrayList.append([point3d8, point3d12, point3d11, point3d7]);
                resultPoint3dArrayList.append([point3d7, point3d11, point3d9, point3d6]);

                self.complexObstacleArea.Add(PrimaryObstacleArea(PolylineArea([point3d8, point3d12, point3d11, point3d7, point3d8])))
                self.complexObstacleArea.Add(SecondaryObstacleArea(point3d8, point3d5, point3d10, point3d12))
                self.complexObstacleArea.Add(SecondaryObstacleArea(point3d7, point3d11, point3d9, point3d6))
            else:
                resultPoint3dArrayList.append([point3d1, point3d2]);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                resultPoint3dArrayList.append([point3d6, point3d5]);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                resultPoint3dArrayList.append([point3d5, point3d10]);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                resultPoint3dArrayList.append([point3d10, point3d9]);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                resultPoint3dArrayList.append([point3d9, point3d6]);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                resultPoint3dArrayList.append([point3d7, point3d11]);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                resultPoint3dArrayList.append([point3d8, point3d12]);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                num21 = metres - metres1;
                num22 = percent / 100;
                num23 = num21 + (metres3 - metres2) * num22;
                num24 = metres + (metres3 - metres2) * num22;
                point3d5 = point3d5.smethod_167(0);
                point3d6 = point3d6.smethod_167(0);
                point3d9 = point3d9.smethod_167(0);
                point3d10 = point3d10.smethod_167(0);
                point3d8 = point3d8.smethod_167(0);
                point3d12 = point3d12.smethod_167(0);
                point3d7 = point3d7.smethod_167(0);
                point3d11 = point3d11.smethod_167(0);
                point3d1 = point3d1.smethod_167(0);
                point3d2 = point3d2.smethod_167(0);
                # resultPoint3dArrayList.append([point3d8, point3d5, point3d10, point3d12]);
                # resultPoint3dArrayList.append([point3d8, point3d12, point3d11, point3d7]);
                # resultPoint3dArrayList.append([point3d7, point3d11, point3d9, point3d6]);

                self.complexObstacleArea.Add(PrimaryObstacleArea(PolylineArea([point3d8, point3d12, point3d11, point3d7, point3d8])))
                self.complexObstacleArea.Add(SecondaryObstacleArea(point3d12, point3d8, point3d10, point3d5, MathHelper.getBearing(point3d8, point3d12)))
                self.complexObstacleArea.Add(SecondaryObstacleArea(point3d11, point3d7, point3d9, point3d6, MathHelper.getBearing(point3d7, point3d11)))
        if self.parametersPanel.cmbConstructionType.currentText() == ConstructionType.Construct2D:
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType)
            for point3dArray in resultPoint3dArrayList:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, point3dArray)
        else:
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Polygon)
            # if define._mapCrs == None:
            #     if mapUnits == QGis.Meters:
            #         constructionLayer = QgsVectorLayer("polygon?crs=EPSG:32633", self.surfaceType, "memory")
            #     else:
            #         constructionLayer = QgsVectorLayer("polygon?crs=EPSG:4326", self.surfaceType, "memory")
            # else:
            #     constructionLayer = QgsVectorLayer("polygon?crs=%s"%define._mapCrs.authid (), self.surfaceType, "memory")
            # constructionLayer.startEditing()
            for point3dArray in resultPoint3dArrayList:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, PolylineArea(point3dArray).method_14_closed())
            #     polygon = QgsGeometry.fromPolygon([point3dArray])
            #     feature = QgsFeature()
            #     feature.setGeometry(polygon)
            #     constructionLayer.addFeature(feature)
            # constructionLayer.commitChanges()
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer, nominalTrackLayer], self.surfaceType)
        self.resultLayerList = [constructionLayer, nominalTrackLayer]
        QgisHelper.zoomToLayers(self.resultLayerList)
        self.ui.btnEvaluate.setEnabled(True)
        self.manualEvent(self.parametersPanel.cmbSelectionMode.currentIndex())
        

    def initParametersPan(self):
        ui = Ui_Radial()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)
        
        self.parametersPanel.pnlNavAid = PositionPanel(self.parametersPanel.gbNavAid)
#         self.parametersPanel.pnlNavAid.groupBox.setTitle("Aerodrome Reference Point(ARP)")
        self.parametersPanel.pnlNavAid.btnCalculater.hide()
        self.parametersPanel.pnlNavAid.hideframe_Altitude()
        self.parametersPanel.pnlNavAid.setObjectName("pnlNavAid")
        ui.vl_gbNavAid.addWidget(self.parametersPanel.pnlNavAid)
        
        self.parametersPanel.cmbNavAidType.Items = ["VOR", "NDB"]
        self.parametersPanel.cmbSelectionMode.addItems(["Automatic", "Manual"])
#         self.parametersPanel.cmbSensorType.currentIndexChanged.connect(self.cmbSensorTypeChanged)
        self.parametersPanel.cmbToleranceType.addItems(["Intersecting", "Tracking", "Area Splay"])
        self.parametersPanel.cmbConstructionType.addItems(["2D", "3D"])
        
        
                
        self.parametersPanel.cmbConstructionType.currentIndexChanged.connect(self.method_28)
        self.connect(self.parametersPanel.cmbNavAidType, SIGNAL("Event_0"), self.method_28)
        # self.parametersPanel.btnCaptureTrackRadial.clicked.connect(self.captureTrackRadial)
#         self.parametersPanel.chbHideCloseInObst.stateChanged.connect(self.chbHideCloseInObstStateChanged)
        self.parametersPanel.btnCaptureDistFinish.clicked.connect(self.measureDistFinish)
        self.parametersPanel.btnCaptureDistStart.clicked.connect(self.measureDistStart)        
#         self.parametersPanel.txtAltitude.textChanged.connect(self.altitudeChanged)
        self.parametersPanel.cmbToleranceType.currentIndexChanged.connect(self.method_28)
#         self.parametersPanel.btnIasHelp.clicked.connect(self.iasHelpShow)
#         self.parametersPanel.txtIas.textChanged.connect(self.iasChanged)
#         self.parametersPanel.txtIsa.textChanged.connect(self.isaChanged)
#
        self.parametersPanel.txtPrimaryMOC.textChanged.connect(self.txtMocMChanged)
        self.parametersPanel.txtPrimaryMOCFt.textChanged.connect(self.txtMocFtChanged)
        self.flag1 = 0
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtPrimaryMOCFt.setText(str(round(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtPrimaryMOC.text())), 4), 4)))
            except:
                self.parametersPanel.txtPrimaryMOCFt.setText("0.0")


        self.method_28()
    def txtMocMChanged(self):
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtPrimaryMOCFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtPrimaryMOC.text())), 4)))
            except:
                self.parametersPanel.txtPrimaryMOCcFt.setText("0.0")
    def txtMocFtChanged(self):
        if self.flag1==0:
            self.flag1=2;
        if self.flag1==1:
            self.flag1=0;
        if self.flag1==2:
            try:
                self.parametersPanel.txtPrimaryMOC.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtPrimaryMOCFt.text())), 4)))
            except:
                self.parametersPanel.txtPrimaryMOC.setText("0.0")
    def outputResultMethod(self):
        self.manualPolygon = self.toolSelectByPolygon.polygonGeom
    def manualEvent(self, index):
        QgisHelper.ClearRubberBandInCanvas(define._canvas)
        self.manualPolygon = None
        if index != 0:
            self.toolSelectByPolygon = RubberBandPolygon(define._canvas)
            define._canvas.setMapTool(self.toolSelectByPolygon)
            self.connect(self.toolSelectByPolygon, SIGNAL("outputResult"), self.outputResultMethod)
        else:
            self.mapToolPan = QgsMapToolPan(define._canvas)
            define._canvas.setMapTool(self.mapToolPan )
    def method_28(self):
        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 0):
            self.parametersPanel.txtTrackRadial.Caption = Captions.TRACK
            self.parametersPanel.chbOverhead.setText(Captions.EXTRA_OVERHEAD_NDB);
        else:
            self.parametersPanel.txtTrackRadial.Caption = Captions.RADIAL
            self.parametersPanel.chbOverhead.setText(Captions.EXTRA_OVERHEAD_VOR);
#             self.para.pnlTrackRadial.Caption = Captions.RADIAL;
#             self.chbOverhead.Text = Captions.EXTRA_OVERHEAD_VOR;
#         self.parametersPanel.frameConstructionType.setVisible(self.parametersPanel.cmbToleranceType.currentIndex() == 2);
        flag = False if(self.parametersPanel.cmbToleranceType.currentIndex() != 2) else self.parametersPanel.cmbConstructionType.currentText() == ConstructionType.Construct3D;
        self.parametersPanel.frameStartAltitude.setVisible(flag);
        self.parametersPanel.framePrimaryMoc.setVisible(self.parametersPanel.cmbToleranceType.currentIndex() == 2)
        self.parametersPanel.frameAltitudeChange.setVisible(flag);
        self.parametersPanel.frameSelectionMode.setVisible(self.parametersPanel.cmbToleranceType.currentIndex() == 2)
        self.parametersPanel.chbOverhead.setVisible(self.parametersPanel.cmbToleranceType.currentIndex() == 2);

        self.initBasedOnCmb()
    # def captureTrackRadial(self):
    #     captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrackRadial)
    #     define._canvas.setMapTool(captureTrackTool)
    def measureDistStart(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtDistStart, DistanceUnits.NM)
        define._canvas.setMapTool(measureDistanceTool)
    def measureDistFinish(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtDistFinish, DistanceUnits.NM)
        define._canvas.setMapTool(measureDistanceTool)
    
    
    
    
class RadialObstacles(ObstacleTable):
    def __init__(self, complexObstacleArea_0, altitude_0, manualPoly):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, None)
        self.manualPolygon = manualPoly
        self.surfaceType = SurfaceTypes.RnavStraightSegmentAnalyser
        self.area = complexObstacleArea_0;
        self.primaryMoc = altitude_0.Metres;
        # self.surfaceType = SurfaceTypes.RnavStraightSegmentAnalyser
    def setHiddenColumns(self, tableView):
#         tableView.hideColumn(self.IndexObstArea)
#         tableView.hideColumn(self.IndexDistInSecM)
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

        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DistInSecM,
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt
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



    def checkObstacle(self, obstacle_0):
        if self.manualPolygon != None:
            if not self.manualPolygon.contains(obstacle_0.Position):
                return
        obstacleAreaResult = ObstacleAreaResult.Outside;
        num = None;
        num1 = None;
        mocMultiplier = self.primaryMoc * obstacle_0.MocMultiplier;
        obstacleAreaResult, num, num1 = self.area.pointInArea(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier);
        if (obstacleAreaResult != ObstacleAreaResult.Outside and num != None):
            position = obstacle_0.Position;
            z = position.get_Z() + obstacle_0.Trees + num;
            # criticalObstacleType = CriticalObstacleType.No;
            # if (z > self.enrouteAltitude):
            #     criticalObstacleType = CriticalObstacleType.Yes;
            checkResult = [obstacleAreaResult, num1, num, z];
            self.addObstacleToModel(obstacle_0, checkResult)

class RubberBandPolygon(QgsMapTool):
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.mCanvas = canvas
        self.mRubberBand = None
        self.mRubberBand0 = QgsRubberBand( self.mCanvas, QGis.Polygon )
        self.mCursor = Qt.ArrowCursor
        self.mFillColor = QColor( 254, 178, 76, 63 )
        self.mBorderColour = QColor( 254, 58, 29, 100 )
        self.mRubberBand0.setBorderColor( self.mBorderColour )
        self.polygonGeom = None
        self.drawFlag = False
#         self.constructionLayer = constructionLayer
    def canvasPressEvent( self, e ):
        if ( self.mRubberBand == None ):
            self.mRubberBand0.reset( QGis.Polygon )
#             define._canvas.clearCache ()
            self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
            self.mRubberBand0 = QgsRubberBand( self.mCanvas, QGis.Polygon )
            self.mRubberBand.setFillColor( self.mFillColor )
            self.mRubberBand.setBorderColor( self.mBorderColour )
            self.mRubberBand0.setFillColor( self.mFillColor )
            self.mRubberBand0.setBorderColor( self.mBorderColour )
        if ( e.button() == Qt.LeftButton ):
            self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )
        else:
            if ( self.mRubberBand.numberOfVertices() > 2 ):
                self.polygonGeom = self.mRubberBand.asGeometry()
            else:
                return
#                 QgsMapToolSelectUtils.setSelectFeatures( self.mCanvas, polygonGeom, e )
            self.mRubberBand.reset( QGis.Polygon )
            self.mRubberBand0.addGeometry(self.polygonGeom, None)
            self.mRubberBand0.show()
            self.mRubberBand = None
            self.emit(SIGNAL("outputResult"), self.polygonGeom)

    def canvasMoveEvent( self, e ):
        pass
        if ( self.mRubberBand == None ):
            return
        if ( self.mRubberBand.numberOfVertices() > 0 ):
            self.mRubberBand.removeLastPoint( 0 )
            self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )
    def deactivate(self):
#         self.rubberBand.reset(QGis.Point)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))