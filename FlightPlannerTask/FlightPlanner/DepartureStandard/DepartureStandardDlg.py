# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication, QString, Qt
from PyQt4.QtGui import QCheckBox, QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsVectorFileWriter,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import AngleUnits, TurnDirection, CriticalObstacleType, \
                    ObstacleTableColumnType, SurfaceTypes, DistanceUnits,AircraftSpeedCategory, \
                    OrientationType, AltitudeUnits, ObstacleAreaResult, RnavDmeDmeFlightPhase, \
                    RnavDmeDmeCriteria, RnavSpecification, RnavGnssFlightPhase , ConstructionType, \
                    CloseInObstacleType
from FlightPlanner.DepartureStandard.ui_DepartureStandard import Ui_DepartureStandard
from FlightPlanner.Panels.PositionPanel import PositionPanel
# from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.AcadHelper import AcadHelper
# from FlightPlanner.Holding.HoldingTemplate import HoldingTemplate
# from FlightPlanner.Panels.WindPanel import WindPanel
from FlightPlanner.RnavTolerance.RnavDmeDmeTolerance import RnavDmeDmeTolerance
from FlightPlanner.RnavTolerance.RnavGnssTolerance import RnavGnssTolerance
from FlightPlanner.types import Point3D, Point3dCollection, StandardDepartureType
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, ComplexObstacleArea, SecondaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.Captions import Captions
from FlightPlanner.messages import Messages
# from FlightPlanner.IasHelp.IasHelpDlg import IasHelpDlg
import define, math

class DepartureStandardDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("DepartureStandardDlg")
        self.surfaceType = SurfaceTypes.DepartureStandard
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.DepartureStandard)
        self.resize(540, 200)
        QgisHelper.matchingDialogSize(self, 670, 700)
        self.surfaceList = None
        self.resultLayerList = []

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
        parameterList.append(("Runway", "group"))
        parameterList.append(("DER Position", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlDer.txtPointX.text()), float(self.parametersPanel.pnlDer.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlDer.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlDer.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlDer.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlDer.txtPointY.text()))
        parameterList.append(("Altitude", self.parametersPanel.pnlDer.txtAltitudeM.text() + "m"))
        parameterList.append(("", self.parametersPanel.pnlDer.txtAltitudeFt.text() + "ft"))

        parameterList.append(("Direction", "Plan : " + str(self.parametersPanel.txtRwyDir.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtRwyDir.txtRadialGeodetic.Value) + define._degreeStr))

        # parameterList.append(("Direction", self.parametersPanel.txtRwyDir.Value))
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Type", self.parametersPanel.cmbType.currentText()))
        
        if self.parametersPanel.cmbType.currentText() == "VOR" or self.parametersPanel.cmbType.currentText() == "NDB":
            if self.parametersPanel.cmbType.currentText() == "VOR":
                parameterList.append(("VOR Position", "group"))
            else:
                parameterList.append(("NDB Position", "group"))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlNavAid.txtPointX.text()), float(self.parametersPanel.pnlNavAid.txtPointY.text()))
            
            parameterList.append(("Lat", self.parametersPanel.pnlNavAid.txtLat.Value))
            parameterList.append(("Lon", self.parametersPanel.pnlNavAid.txtLong.Value))
            parameterList.append(("X", self.parametersPanel.pnlNavAid.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlNavAid.txtPointY.text()))
        
        if self.parametersPanel.cmbType.currentIndex() != 0:
            parameterList.append(("Track", "Plan : " + str(self.parametersPanel.txtTrack.txtRadialPlan.Value) + define._degreeStr))
            parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtTrack.txtRadialGeodetic.Value) + define._degreeStr))

            # parameterList.append(("Track", self.parametersPanel.txtTrack.Value))
            
        parameterList.append(("Distance", self.parametersPanel.txtDistance.text() + "nm"))
        if self.parametersPanel.chbCatH.isChecked():            
            parameterList.append(("Cat. H", "True"))
        else:
            parameterList.append(("Cat. H", "False"))
        
        parameterList.append(("MOC", self.parametersPanel.txtMoc.text() + "%"))
        parameterList.append(("PDG", self.parametersPanel.txtPdg.text() + "%"))
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstruct.currentText()))
        parameterList.append(("MOCmultipiler", str(self.parametersPanel.mocSpinBox.value())))
        
        parameterList.append(("Results / Checked Obstacles", "group"))   
        parameterList.append(("Checked Obstacles", "group"))
        if self.parametersPanel.chbHideCloseInObst.isChecked():
            parameterList.append(("Hide close-in obstacles", "True"))
        else:
            parameterList.append(("Hide close-in obstacles", "False"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        
        
        return parameterList
    
    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        self.ui.frm_cmbObstSurface.setVisible(False)
        
        
        
#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)
    
        
    def btnPDTCheck_Click(self):
        pdtResultStr = MathHelper.pdtCheckResultToString(float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), float(self.parametersPanel.txtIas.text()), float(self.parametersPanel.txtTime.text()))
        
        QMessageBox.warning(self, "PDT Check", pdtResultStr)
    def btnEvaluate_Click(self):
        point3dCollection = None;
        point3dCollection1 = None;
        point3dCollection2 = None;
        point3dCollection3 = None;
        point3dCollection4 = None;
        point3dCollection5 = None;
#         if (!AcadHelper.Ready)
#         {
#             return;
#         }
#         if (!this.method_27(false))
#         {
#             return;
#         }
        result, point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, point3dCollection4, point3dCollection5 = self.method_38()
        if (not result):
            return;
        complexObstacleArea = ComplexObstacleArea();
        point3dCollection6 = Point3dCollection();
        point3dCollection6.appendList(point3dCollection2);
        point3dCollection3.reverse()
        point3dCollection6.appendList(point3dCollection3);
        complexObstacleArea.Add(PrimaryObstacleArea(PolylineArea(PolylineArea(point3dCollection6).method_14_closed())));
        if (point3dCollection1 != None):
            for i in range(1, point3dCollection2.get_Count()):
                if (not point3dCollection2.get_Item(i - 1).smethod_170(point3dCollection1.get_Item(i - 1)) or not point3dCollection2.get_Item(i).smethod_170(point3dCollection1.get_Item(i))):
                    complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection2.get_Item(i - 1), point3dCollection2.get_Item(i), point3dCollection1.get_Item(i - 1), point3dCollection1.get_Item(i)));
        if (point3dCollection4 != None):
            for j in range(1, point3dCollection3.get_Count()):
                if (not point3dCollection3.get_Item(j - 1).smethod_170(point3dCollection4.get_Item(j - 1)) or not point3dCollection3.get_Item(j).smethod_170(point3dCollection4.get_Item(j))):
                    complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection3.get_Item(j - 1), point3dCollection3.get_Item(j), point3dCollection4.get_Item(j - 1), point3dCollection4.get_Item(j)));
        point3d = self.parametersPanel.pnlDer.Point3d;
        percent = float(self.parametersPanel.txtMoc.text());
        num = float(self.parametersPanel.txtPdg.text());
        num1 = Unit.ConvertDegToRad(float(self.parametersPanel.txtRwyDir.Value));
        
        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        self.obstaclesModel = DepartureStandardObstacles(point3d, num1, percent, num, complexObstacleArea);
          
        return FlightPlanBaseDlg.btnEvaluate_Click(self)

    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        point3dCollection = None;
        point3dCollection1 = None;
        point3dCollection2 = None;
        point3dCollection3 = None;
        point3dCollection4 = None;
        point3dCollection5 = None;
        num = None;
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        point3d3 = None;
#         if (!AcadHelper.Ready)
#         {
#             return;
#         }
#         if (!self.method_27(true))
#         {
#             return;
#         }
        constructionLayer = None;

        mapUnits = define._canvas.mapUnits()
        
        result, point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, point3dCollection4, point3dCollection5 = self.method_38()
        resultPoint3dArrayList = []
        if (result):
            if (self.parametersPanel.cmbConstruct.currentText() != ConstructionType.Construct2D):
                point3d4 = self.parametersPanel.pnlDer.Point3d;
                item = point3dCollection5.get_Item(0);
                item1 = point3dCollection5.get_Item(1);
                percent = float(self.parametersPanel.txtPdg.text()) / 100;
                percent1 = float(self.parametersPanel.txtMoc.text()) / 100;
                num1 = Unit.ConvertDegToRad(float(self.parametersPanel.txtRwyDir.Value));
                num2 = MathHelper.getBearing(item, item1) + 1.5707963267949;
                if (point3dCollection1 != None):
                    for i in range(1, point3dCollection2.get_Count()):
                        if (not point3dCollection2.get_Item(i - 1).smethod_170(point3dCollection1.get_Item(i - 1)) or not point3dCollection2.get_Item(i).smethod_170(point3dCollection1.get_Item(i))):
                            resultPoint3dArrayList.append([point3dCollection2.get_Item(i - 1), point3dCollection2.get_Item(i), point3dCollection1.get_Item(i), point3dCollection1.get_Item(i - 1)])
#                             AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3dCollection2.get_Item(i - 1), point3dCollection2.get_Item(i), point3dCollection1.get_Item(i), point3dCollection1.get_Item(i - 1), true, true, true, true), constructionLayer);
                if (point3dCollection4 != None):
                    for j in range(1, point3dCollection3.get_Count()):
                        if (not point3dCollection3.get_Item(j - 1).smethod_170(point3dCollection4.get_Item(j - 1)) or not point3dCollection3.get_Item(j).smethod_170(point3dCollection4.get_Item(j))):
                            resultPoint3dArrayList.append([point3dCollection3.get_Item(j - 1), point3dCollection3.get_Item(j), point3dCollection4.get_Item(j), point3dCollection4.get_Item(j - 1)])
#                             AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3dCollection3.get_Item(j - 1), point3dCollection3.get_Item(j), point3dCollection4.get_Item(j), point3dCollection4.get_Item(j - 1), true, true, true, true), constructionLayer);
                for k in range(1, point3dCollection2.get_Count()):
                    item2 = point3dCollection2.get_Item(k - 1);
                    item3 = point3dCollection2.get_Item(k);
                    if (not item2.smethod_170(item3)):
                        if (k != 1):
                            point3d = MathHelper.getIntersectionPoint(item, item1, item2, MathHelper.distanceBearingPoint(item2, num2, 1000));
                        else:
                            point3d = item.smethod_167(item2.get_Z());
                        point3d1 = MathHelper.getIntersectionPoint(item, item1, item3, MathHelper.distanceBearingPoint(item3, num2, 1000));
                        point3d = point3d.smethod_167(self.method_39(point3d4, num1, point3d, percent, percent1, True));
                        point3d1 = point3d1.smethod_167(self.method_39(point3d4, num1, point3d1, percent, percent1, True));
                        resultPoint3dArrayList.append([item2, item3, point3d1, point3d])
#                         AcadHelper.smethod_18(transaction, blockTableRecord, new Face(item2, item3, point3d1, point3d, true, true, true, true), constructionLayer);
                for l in range(1, point3dCollection3.get_Count()):
                    item4 = point3dCollection3.get_Item(l - 1);
                    item5 = point3dCollection3.get_Item(l);
                    if (not item4.smethod_170(item5)):
                        if (l != 1):
                            point3d2 = MathHelper.getIntersectionPoint(item, item1, item4, MathHelper.distanceBearingPoint(item4, num2, 1000));
                        else:
                            point3d2 = item.smethod_167(item4.get_Z());
                        point3d3 = MathHelper.getIntersectionPoint(item, item1, item5, MathHelper.distanceBearingPoint(item5, num2, 1000));
                        point3d2 = point3d2.smethod_167(self.method_39(point3d4, num1, point3d2, percent, percent1, True));
                        point3d3 = point3d3.smethod_167(self.method_39(point3d4, num1, point3d3, percent, percent1, True));
                        resultPoint3dArrayList.append([item4, item5, point3d3, point3d2])
#                         AcadHelper.smethod_18(transaction, blockTableRecord, new Face(item4, item5, point3d3, point3d2, true, true, true, true), constructionLayer);
                resultPoint3dArrayList.append([point3dCollection5.get_Item(0), point3dCollection5.get_Item(1), point3dCollection5.get_Item(2), point3dCollection5.get_Item(3)])
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
                #
                #
                # constructionLayer.startEditing()
                for point3dArray in resultPoint3dArrayList:
                    AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, point3dArray)
                #     polygon = QgsGeometry.fromPolygon([point3dArray])
                #     feature = QgsFeature()
                #     feature.setGeometry(polygon)
                #     constructionLayer.addFeature(feature)
                # constructionLayer.commitChanges()
                QgisHelper.appendToCanvas(define._canvas, [constructionLayer], self.surfaceType)
                self.resultLayerList = [constructionLayer]
#                 AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3dCollection5.get_Item(0), point3dCollection5.get_Item(1), point3dCollection5.get_Item(2), point3dCollection5.get_Item(3), true, true, true, true), constructionLayer);
            else:
                resultPoint3dArrayList = []
                if (point3dCollection1 != None):
                    num = 0;
                    for m in range(1, point3dCollection2.get_Count()):
                        if point3dCollection2.get_Item(m - 1).smethod_170(point3dCollection1.get_Item(m - 1)) and point3dCollection2.get_Item(m).smethod_170(point3dCollection1.get_Item(m)):
                            break
                        num += 1;
                    for n in range(num):
                        point3dCollection2.RemoveAt(0);
                if (point3dCollection4 != None):
                    num = 0;
                    for o in range(1, point3dCollection3.get_Count()):
                        if point3dCollection3.get_Item(o - 1).smethod_170(point3dCollection4.get_Item(o - 1)) and point3dCollection3.get_Item(o).smethod_170(point3dCollection4.get_Item(o)):
                            break
                        num += 1;
                    for p in range(num):
                        point3dCollection3.RemoveAt(0);
                if (point3dCollection1 != None and point3dCollection1.get_Count() > 0):
                    resultPoint3dArrayList.append(point3dCollection1)
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_128(point3dCollection1), constructionLayer);
                if (point3dCollection2.get_Count() > 1):
                    resultPoint3dArrayList.append(point3dCollection2)
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_128(point3dCollection2), constructionLayer);
                if (point3dCollection3.get_Count() > 1):
                    resultPoint3dArrayList.append(point3dCollection3)
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_128(point3dCollection3), constructionLayer);
                if (point3dCollection4 != None):
                    resultPoint3dArrayList.append(point3dCollection4)
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_128(point3dCollection4), constructionLayer);:
                if (not (point3dCollection1 != None) or not (point3dCollection4 != None)):
                    point3dArray = [point3dCollection2.get_Item(0), point3dCollection3.get_Item(0)];
                    resultPoint3dArrayList.append(point3dArray)
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(point3dArray), constructionLayer);
                    point3dArray1 = [point3dCollection2.get_Item(point3dCollection2.get_Count() - 1), point3dCollection3.get_Item(point3dCollection3.get_Count() - 1)];
                    resultPoint3dArrayList.append(point3dArray1)
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(point3dArray1), constructionLayer);
                else:
                    point3dArray2 = [point3dCollection1.get_Item(0), point3dCollection4.get_Item(0)];
                    resultPoint3dArrayList.append(point3dArray2)
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(point3dArray2), constructionLayer);
                    point3dArray3 = [point3dCollection1.get_Item(point3dCollection1.get_Count() - 1), point3dCollection4.get_Item(point3dCollection4.get_Count() - 1)];
                    resultPoint3dArrayList.append(point3dArray3)

                constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)
                nominalPointTest1 = resultPoint3dArrayList[3][0]
                nominalPointTest2 = resultPoint3dArrayList[3][1]
                self.nominalPoint = MathHelper.distanceBearingPoint(nominalPointTest1, MathHelper.getBearing(nominalPointTest1, nominalPointTest2), MathHelper.calcDistance(nominalPointTest1, nominalPointTest2) / 2)

                for point3dArray in resultPoint3dArrayList:
                    AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, point3dArray)
                nominalTrackLayer = self.nominal2Layer()
                QgisHelper.appendToCanvas(define._canvas, [constructionLayer, nominalTrackLayer], self.surfaceType)
                self.resultLayerList = [constructionLayer, nominalTrackLayer]
            QgisHelper.zoomToLayers(self.resultLayerList)
            self.ui.btnEvaluate.setEnabled(True)
    def initParametersPan(self):
        ui = Ui_DepartureStandard()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.btnCaptureDistance.setVisible(False)
        self.parametersPanel.txtRwyDir.btnCaptureRadial.setVisible(False)

        # self.parametersPanel.txtDistance.setEnabled(False)
        # self.parametersPanel.txtAltitudeM.setEnabled(False)
        # self.parametersPanel.txtAltitudeFt.setEnabled(False)
        self.parametersPanel.chbHideCloseInObst = self.chbHideCloseInObst
        self.parametersPanel.chbHideCloseInObst.setVisible(True)
        # self.parametersPanel.chbHideCloseInObst = QCheckBox(self.ui.grbResult)
        # font = QFont()
        # font.setBold(False)
        # font.setWeight(50)
        # self.parametersPanel.chbHideCloseInObst.setFont(font)
        # self.parametersPanel.chbHideCloseInObst.setObjectName("chbHideCloseInObst")
        # self.ui.vlResultGroup.addWidget(self.parametersPanel.chbHideCloseInObst)
        # self.parametersPanel.chbHideCloseInObst.setText("Hide close-in obstacles")
        
        self.parametersPanel.pnlDer = PositionPanel(self.parametersPanel.gbRunway)
        self.parametersPanel.pnlDer.groupBox.setTitle("DER Position")
        self.parametersPanel.pnlDer.btnCalculater.hide()
#         self.parametersPanel.pnlRwyDir.hideframe_Altitude()
        self.parametersPanel.pnlDer.setObjectName("pnlDer")
        ui.vl_gbRunway.insertWidget(0, self.parametersPanel.pnlDer)
        self.parametersPanel.pnlDer.txtPointX.textChanged.connect(self.CalcParam)
        self.parametersPanel.pnlDer.txtAltitudeM.textChanged.connect(self.derAltitudeChanged)
        self.connect(self.parametersPanel.pnlDer, SIGNAL("positionChanged"), self.CalcParam)

        self.parametersPanel.pnlRwyStart = PositionPanel(self.parametersPanel.gbRunway)
        self.parametersPanel.pnlRwyStart.groupBox.setTitle("Start of RWY/FATO Position")
        self.parametersPanel.pnlRwyStart.btnCalculater.hide()
        self.parametersPanel.pnlRwyStart.hideframe_Altitude()
        self.parametersPanel.pnlRwyStart.setObjectName("pnlRwyStart")
        ui.vl_gbRunway.insertWidget(1, self.parametersPanel.pnlRwyStart)
        self.connect(self.parametersPanel.pnlRwyStart, SIGNAL("positionChanged"), self.CalcParam)
        # self.parametersPanel.pnlRwyStart.txtPointX.textChanged.connect(self.CalcParam)


        self.parametersPanel.pnlNavAid = PositionPanel(self.parametersPanel.gbParameters)
        self.parametersPanel.pnlNavAid.groupBox.setTitle("VOR Position")
        self.parametersPanel.pnlNavAid.btnCalculater.hide()
        self.parametersPanel.pnlNavAid.hideframe_Altitude()
        self.parametersPanel.pnlNavAid.setObjectName("pnlNavAid")
        ui.vl_gbParameters.insertWidget(1, self.parametersPanel.pnlNavAid)
        self.parametersPanel.pnlNavAid.setVisible(False)
               
        self.parametersPanel.cmbType.addItems(["Straight", "With Track Adjustment", "VOR", "NDB"])
        self.parametersPanel.cmbType.currentIndexChanged.connect(self.cmbTypeChanged)
        self.parametersPanel.cmbConstruct.addItems(["2D", "3D"])
        
        self.parametersPanel.txtTrack.Visible = False
        
                
        self.parametersPanel.chbHideCloseInObst.stateChanged.connect(self.chbHideCloseInObstStateChanged)
        self.parametersPanel.btnCaptureDistance.clicked.connect(self.measureDistance)
        self.parametersPanel.txtAltitudeM.textChanged.connect(self.altitudeMChanged)
        self.parametersPanel.txtAltitudeFt.textChanged.connect(self.altitudeFtChanged)
        self.parametersPanel.txtDistance.textChanged.connect(self.distanceChanged)

        self.flag = 0
        self.flag1 = 0

        try:
            altitudeValueMetre = Distance(float(self.parametersPanel.txtDistance.text()),DistanceUnits.NM).Metres * float(self.parametersPanel.txtPdg.text()) / 100.0 + (float(self.parametersPanel.pnlDer.txtAltitudeM.text()) + 5.0)
            self.parametersPanel.txtAltitudeM.setText(str(round(altitudeValueMetre, 4)))
        except:
            pass
        self.CalcParam()
    def derAltitudeChanged(self):
        altitudeValueMetre = Distance(float(self.parametersPanel.txtDistance.text()),DistanceUnits.NM).Metres * float(self.parametersPanel.txtPdg.text()) / 100.0 + (float(self.parametersPanel.pnlDer.txtAltitudeM.text()) + 5.0)
        self.parametersPanel.txtAltitudeM.setText(str(round(altitudeValueMetre, 4)))
        # diatanceMetre = (float(self.parametersPanel.txtAltitudeM.text()) - (float(self.parametersPanel.pnlDer.txtAltitudeM.text())+ 5.0)) / (float(self.parametersPanel.txtPdg.text()) / 100)
        # self.parametersPanel.txtDistance.setText(str(round(Unit.ConvertMeterToNM(diatanceMetre), 2)))

    def altitudeMChanged(self):
        if self.flag==0:
            self.flag=1;
        if self.flag==2:
            self.flag=0;
        if self.flag==1:
            try:
                self.parametersPanel.txtAltitudeFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAltitudeM.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeFt.setText("0.0")

        # Calculate Distance
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                ss = self.parametersPanel.txtAltitudeM.text()
                diatanceMetre = (float(self.parametersPanel.txtAltitudeM.text()) - (float(self.parametersPanel.pnlDer.txtAltitudeM.text())+ 5.0)) / (float(self.parametersPanel.txtPdg.text()) / 100)
                self.parametersPanel.txtDistance.setText(str(round(Unit.ConvertMeterToNM(diatanceMetre), 4)))
            except:
                self.parametersPanel.txtDistance.setText("0.0")
    def altitudeFtChanged(self):
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitudeFt.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")
    def distanceChanged(self):
        if self.flag1==0:
            self.flag1=2;
        if self.flag1==1:
            self.flag1=0;
        if self.flag1==2:
            try:
                altitudeValueMetre = Distance(float(self.parametersPanel.txtDistance.text()),DistanceUnits.NM).Metres * float(self.parametersPanel.txtPdg.text()) / 100.0 + (float(self.parametersPanel.pnlDer.txtAltitudeM.text()) + 5.0)
                self.parametersPanel.txtAltitudeM.setText(str(round(altitudeValueMetre, 4)))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")
    def CalcParam(self):
        try:
            pointDer = self.parametersPanel.pnlDer.Point3d
            pointStart = self.parametersPanel.pnlRwyStart.Point3d
            self.parametersPanel.txtRwyDir.Value = round(Unit.ConvertRadToDeg(MathHelper.getBearing(pointStart, pointDer)), 4)
            self.parametersPanel.txtDistance.setText(str(round(Distance(MathHelper.calcDistance(pointDer, pointStart)).NauticalMiles, 4)))
            self.parametersPanel.txtAltitudeM.setText(self.parametersPanel.pnlRwyStart.txtAltitudeM.text())
            self.parametersPanel.txtAltitudeFt.setText(self.parametersPanel.pnlRwyStart.txtAltitudeFt.text())
        except:
            pass
        try:
            distanceBetweenDerAndStart = MathHelper.calcDistance(self.parametersPanel.pnlDer.Point3d, self.parametersPanel.pnlRwyStart.Point3d)
            self.parametersPanel.txtDistance.setText(str(round(Unit.ConvertMeterToNM(distanceBetweenDerAndStart), 4)))
        except:
            pass

    def chbHideCloseInObstStateChanged(self, state):
        if state:
            self.obstaclesModel.setFilterKeyColumn(self.obstaclesModel.IndexCloseIn)
            self.obstaclesModel.setFilterFixedString("No")
#             self.obstaclesModel.setFilterKeyColumn(self.obstaclesModel.IndexSurface)
        else:
            self.obstaclesModel.setFilterKeyColumn(self.obstaclesModel.IndexCloseIn)
            self.obstaclesModel.setFilterFixedString("")
    
    def cmbTypeChanged(self, index):
        if index == 0:
            self.parametersPanel.pnlNavAid.setVisible(False)
            self.parametersPanel.txtTrack.Visible = False
        elif index == 1:
            self.parametersPanel.pnlNavAid.setVisible(False)
            self.parametersPanel.txtTrack.Visible = True
        elif index == 2:
            self.parametersPanel.pnlNavAid.groupBox.setTitle("VOR Position")
            self.parametersPanel.pnlNavAid.setVisible(True)
            self.parametersPanel.txtTrack.Visible = True
        elif index == 3:
            self.parametersPanel.pnlNavAid.groupBox.setTitle("NDB Position")
            self.parametersPanel.pnlNavAid.setVisible(True)
            self.parametersPanel.txtTrack.Visible = True
    
    # def captureBearing(self):
    #     captureRwyDerTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtRwyDir)
    #     define._canvas.setMapTool(captureRwyDerTool)
    def captureTrack(self):
        captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrack)
        define._canvas.setMapTool(captureTrackTool)
    def measureDistance(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtDistance, DistanceUnits.NM)
        define._canvas.setMapTool(measureDistanceTool)
    
    def method_38(self):
        turnDirection = None;
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        point3d3 = None;
        point3d4 = None;
        point3d5 = None;
        point3d6 = None;
        point3dCollection_0 = Point3dCollection();
        point3dCollection_1 = None;
        point3dCollection_2 = Point3dCollection();
        point3dCollection_3 = Point3dCollection();
        point3dCollection_4 = None;
        point3dCollection_5 = Point3dCollection();
        point3d7 = self.parametersPanel.pnlDer.Point3d;
        num = Unit.ConvertDegToRad(float(self.parametersPanel.txtRwyDir.Value));
        standardDepartureType = self.parametersPanel.cmbType.currentText();
        metres = Distance(float(self.parametersPanel.txtDistance.text()), DistanceUnits.NM).Metres;
        percent = float(self.parametersPanel.txtMoc.text()) / 100;
        percent1 = float(self.parametersPanel.txtPdg.text()) / 100;
        num1 = 90 / percent1 if (self.parametersPanel.chbCatH.isChecked()) else 120 / percent1;
        num2 = 45 if (self.parametersPanel.chbCatH.isChecked()) else 150;
        num3 = Unit.ConvertDegToRad(15);
        if (standardDepartureType != StandardDepartureType.Straight):
            num4 = Unit.ConvertDegToRad(float(self.parametersPanel.txtTrack.Value));
            turnDirectionList = []
            num5 = MathHelper.smethod_77(num, num4, AngleUnits.Radians, turnDirectionList);
            turnDirection = turnDirectionList[0]
            if (turnDirection != TurnDirection.Nothing and num5 > Unit.ConvertDegToRad(15.05)):
                QMessageBox.warning(self, "Warning", Messages.ERR_COURSE_CHANGES_GREATER_THAN_15_NOT_ALLOWED)
#                 ErrorMessageBox.smethod_0(self, Messages.ERR_COURSE_CHANGES_GREATER_THAN_15_NOT_ALLOWED);
                return (False, None, None, None, None, None, None);
            if (standardDepartureType != StandardDepartureType.WithTrackAdjustment):
                point3d8 = self.parametersPanel.pnlNavAid.Point3d;
                point3d2 = MathHelper.getIntersectionPoint(point3d7, MathHelper.distanceBearingPoint(point3d7, num + 1.5707963267949, 100), point3d8, MathHelper.distanceBearingPoint(point3d8, num4, 100));
                num6 = 90 if (self.parametersPanel.chbCatH.isChecked()) else 300;
                if (MathHelper.calcDistance(point3d7, point3d2) > num6):
                    eRRDEPARTURETRACKCROSSING = Messages.ERR_DEPARTURE_TRACK_CROSSING;
                    distance = Distance(num6);
                    QMessageBox.warning(self, "Warning", eRRDEPARTURETRACKCROSSING%distance.NauticalMiles)
#                     ErrorMessageBox.smethod_0(self, string.Format(eRRDEPARTURETRACKCROSSING, distance.method_0(":u")));
                    return (False, None, None, None, None, None, None);
                num7 = 1900 if (standardDepartureType == StandardDepartureType.VOR) else 2315;
                num8 = Unit.ConvertNMToMeter(10);
                num9 = Unit.ConvertDegToRad(7.8) if (standardDepartureType == StandardDepartureType.VOR) else Unit.ConvertDegToRad(10.3);
                point3dCollection_1 = Point3dCollection();
                point3dCollection_4 = Point3dCollection();
                point3d9 = MathHelper.distanceBearingPoint(point3d8, num4 + 3.14159265358979, Unit.ConvertNMToMeter(100));
                point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d9, num4 - 1.5707963267949, num8));
                point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d9, num4 - 1.5707963267949, num8 / 2));
                point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d9, num4 + 1.5707963267949, num8 / 2));
                point3dCollection_4.Add(MathHelper.distanceBearingPoint(point3d9, num4 + 1.5707963267949, num8));
                point3d9 = MathHelper.distanceBearingPoint(point3d8, num4 + 3.14159265358979, (num8 - num7) / math.tan(num9));
                point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d9, num4 - 1.5707963267949, num8));
                point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d9, num4 - 1.5707963267949, num8 / 2));
                point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d9, num4 + 1.5707963267949, num8 / 2));
                point3dCollection_4.Add(MathHelper.distanceBearingPoint(point3d9, num4 + 1.5707963267949, num8));
                point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d8, num4 - 1.5707963267949, num7));
                point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d8, num4 - 1.5707963267949, num7 / 2));
                point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d8, num4 + 1.5707963267949, num7 / 2));
                point3dCollection_4.Add(MathHelper.distanceBearingPoint(point3d8, num4 + 1.5707963267949, num7));
                point3d9 = MathHelper.distanceBearingPoint(point3d8, num4, (num8 - num7) / math.tan(num9));
                point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d9, num4 - 1.5707963267949, num8));
                point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d9, num4 - 1.5707963267949, num8 / 2));
                point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d9, num4 + 1.5707963267949, num8 / 2));
                point3dCollection_4.Add(MathHelper.distanceBearingPoint(point3d9, num4 + 1.5707963267949, num8));
                point3d9 = MathHelper.distanceBearingPoint(point3d8, num4, Unit.ConvertNMToMeter(100));
                point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d9, num4 - 1.5707963267949, num8));
                point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d9, num4 - 1.5707963267949, num8 / 2));
                point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d9, num4 + 1.5707963267949, num8 / 2));
                point3dCollection_4.Add(MathHelper.distanceBearingPoint(point3d9, num4 + 1.5707963267949, num8));
                self.method_41(point3dCollection_1, point3d7, MathHelper.distanceBearingPoint(point3d7, num - 1.5707963267949, 100));
                self.method_41(point3dCollection_2, point3d7, MathHelper.distanceBearingPoint(point3d7, num - 1.5707963267949, 100));
                self.method_42(point3dCollection_3, point3d7, MathHelper.distanceBearingPoint(point3d7, num + 1.5707963267949, 100));
                self.method_42(point3dCollection_4, point3d7, MathHelper.distanceBearingPoint(point3d7, num + 1.5707963267949, 100));
                if (not MathHelper.smethod_115(point3d2, point3d7, MathHelper.distanceBearingPoint(point3d7, num, 1000))):
                    point3d3 = MathHelper.distanceBearingPoint(point3d7, num - 1.5707963267949, num2);
                    point3d5 = MathHelper.distanceBearingPoint(point3d2, num + 1.5707963267949, num2);
                else:
                    point3d3 = MathHelper.distanceBearingPoint(point3d2, num - 1.5707963267949, num2);
                    point3d5 = MathHelper.distanceBearingPoint(point3d7, num + 1.5707963267949, num2);
                if (turnDirection == TurnDirection.Left or turnDirection == TurnDirection.Nothing):
                    point3d4 = MathHelper.distanceBearingPoint(point3d3, num4 - num3, 500);
                    point3d6 = MathHelper.distanceBearingPoint(point3d5, num + num3, 500);
                else:
                    point3d4 = MathHelper.distanceBearingPoint(point3d3, num - num3, 500);
                    point3d6 = MathHelper.distanceBearingPoint(point3d5, num4 + num3, 500);
                self.method_41(point3dCollection_1, point3d3, point3d4);
                self.method_41(point3dCollection_2, point3d3, point3d4);
                self.method_42(point3dCollection_3, point3d5, point3d6);
                self.method_42(point3dCollection_4, point3d5, point3d6);
                self.method_43(point3dCollection_2, point3dCollection_1, point3d8, num4);
                self.method_43(point3dCollection_3, point3dCollection_4, point3d8, num4);
                for i in range(len(point3dCollection_1)):
                    point3dCollection_1.set_Item(i, point3dCollection_1.get_Item(i).smethod_167(self.method_39(point3d7, num, point3dCollection_1.get_Item(i), percent1, percent, False)));
                for j in range(point3dCollection_2.get_Count()):
                    point3dCollection_2.set_Item(j, point3dCollection_2.get_Item(j).smethod_167(self.method_39(point3d7, num, point3dCollection_2.get_Item(j), percent1, percent, True)));
                for k in range(point3dCollection_3.get_Count()):
                    point3dCollection_3.set_Item(k, point3dCollection_3.get_Item(k).smethod_167(self.method_39(point3d7, num, point3dCollection_3.get_Item(k), percent1, percent, True)));
                for l in range(point3dCollection_4.get_Count()):
                    point3dCollection_4.set_Item(l, point3dCollection_4.get_Item(l).smethod_167(self.method_39(point3d7, num, point3dCollection_4.get_Item(l), percent1, percent, False)));
                point3dCollection_2.Insert(0, point3d3.smethod_167(point3d7.get_Z() + 5));
                point3dCollection_1.Insert(0, point3d3.smethod_167(point3d7.get_Z() + 5));
                point3dCollection_1.Insert(1, point3dCollection_2.get_Item(1));
                point3dCollection_3.Insert(0, point3d5.smethod_167(point3d7.get_Z() + 5));
                point3dCollection_4.Insert(0, point3d5.smethod_167(point3d7.get_Z() + 5));
                point3dCollection_4.Insert(1, point3dCollection_3.get_Item(1));
                point3d10 = MathHelper.distanceBearingPoint(point3d2, num4, metres);
                self.method_40(point3dCollection_1, point3d7, point3d10, num, percent1, percent, False);
                self.method_40(point3dCollection_2, point3d7, point3d10, num, percent1, percent, True);
                self.method_40(point3dCollection_3, point3d7, point3d10, num, percent1, percent, True);
                self.method_40(point3dCollection_4, point3d7, point3d10, num, percent1, percent, False);
                point3dCollection_0.appendList(point3dCollection_1);
#                 point3dCollection_4.reverse()
                point3dCollection_0.appendList(point3dCollection_4);
                point3dCollection_5.Add(point3d2.smethod_167(point3d7.get_Z() + 5));
                point3dCollection_5.Add(point3d10.smethod_167(self.method_39(point3d7, num, point3d10, percent1, percent, False)));
                point3dCollection_5.Add(point3d10.smethod_167(self.method_39(point3d7, num, point3d10, percent1, percent, True)));
                point3dCollection_5.Add(point3d2.smethod_167(point3d7.get_Z() + 5));
            else:
                if (metres <= num1 / math.cos(num5)):
                    eRRINSUFFICIENTDEPARTUREDISTANCE = Messages.ERR_INSUFFICIENT_DEPARTURE_DISTANCE;
                    distance1 = Distance(num1);
                    QMessageBox.warning(self, "Warning", eRRINSUFFICIENTDEPARTUREDISTANCE%distance1.NauticalMiles)
#                     ErrorMessageBox.smethod_0(self, string.Format(eRRINSUFFICIENTDEPARTUREDISTANCE, distance1.method_0(":nm")));
                    return (False, None, None, None, None, None, None);
                point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d7, num - 1.5707963267949, num2).smethod_167(point3d7.get_Z() + 5));
                point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d7, num + 1.5707963267949, num2).smethod_167(point3d7.get_Z() + 5));
                point3d11 = MathHelper.distanceBearingPoint(point3d7, num4, metres);
                if (turnDirection == TurnDirection.Nothing):
                    point3d12 = MathHelper.distanceBearingPoint(point3dCollection_2.get_Item(0), num - num3, metres / math.cos(num3));
                    point3d13 = MathHelper.distanceBearingPoint(point3dCollection_3.get_Item(0), num + num3, metres / math.cos(num3));
                    point3dCollection_2.Add(point3d12.smethod_167(self.method_39(point3d7, num, point3d12, percent1, percent, True)));
                    point3dCollection_3.Add(point3d13.smethod_167(self.method_39(point3d7, num, point3d13, percent1, percent, True)));
                elif (turnDirection != TurnDirection.Left):
                    point3d1 = MathHelper.getIntersectionPoint(point3dCollection_3.get_Item(0), MathHelper.distanceBearingPoint(point3dCollection_3.get_Item(0), num4 + num3, 100), point3d11, MathHelper.distanceBearingPoint(point3d11, num4 + 1.5707963267949, 100));
                    point3dCollection_3.Add(point3d1.smethod_167(self.method_39(point3d7, num, point3d1, percent1, percent, True)));
                    point3d14 = MathHelper.distanceBearingPoint(point3dCollection_2.get_Item(0), num - num3, num1 / math.cos(num3));
                    point3dCollection_2.Add(point3d14.smethod_167(self.method_39(point3d7, num, point3d14, percent1, percent, True)));
                    point3d14 = MathHelper.getIntersectionPoint(point3d14, MathHelper.distanceBearingPoint(point3d14, num4 - num3, 100), point3d11, MathHelper.distanceBearingPoint(point3d11, num4 + 1.5707963267949, 100));
                    point3dCollection_2.Add(point3d14.smethod_167(self.method_39(point3d7, num, point3d14, percent1, percent, True)));
                else:
                    point3d = MathHelper.getIntersectionPoint(point3dCollection_2.get_Item(0), MathHelper.distanceBearingPoint(point3dCollection_2.get_Item(0), num4 - num3, 100), point3d11, MathHelper.distanceBearingPoint(point3d11, num4 + 1.5707963267949, 100));
                    point3dCollection_2.Add(point3d.smethod_167(self.method_39(point3d7, num, point3d, percent1, percent, True)));
                    point3d15 = MathHelper.distanceBearingPoint(point3dCollection_3.get_Item(0), num + num3, num1 / math.cos(num3));
                    point3dCollection_3.Add(point3d15.smethod_167(self.method_39(point3d7, num, point3d15, percent1, percent, True)));
                    point3d15 = MathHelper.getIntersectionPoint(point3d15, MathHelper.distanceBearingPoint(point3d15, num4 + num3, 100), point3d11, MathHelper.distanceBearingPoint(point3d11, num4 + 1.5707963267949, 100));
                    point3dCollection_3.Add(point3d15.smethod_167(self.method_39(point3d7, num, point3d15, percent1, percent, True)));
                point3dCollection_0.appendList(point3dCollection_2);
#                 point3dCollection_3.reverse()
                point3dCollection_0.appendList(point3dCollection_3);
                point3dCollection_5.Add(point3d7.smethod_167(point3d7.get_Z() + 5));
                point3dCollection_5.Add(point3d11.smethod_167(self.method_39(point3d7, num, point3d11, percent1, percent, False)));
                point3dCollection_5.Add(point3d11.smethod_167(self.method_39(point3d7, num, point3d11, percent1, percent, True)));
                point3dCollection_5.Add(point3d7.smethod_167(point3d7.get_Z() + 5));
        else:
            point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d7, num - 1.5707963267949, num2).smethod_167(point3d7.get_Z() + 5));
            point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d7, num + 1.5707963267949, num2).smethod_167(point3d7.get_Z() + 5));
            point3d16 = MathHelper.distanceBearingPoint(point3dCollection_2.get_Item(0), num - num3, metres / math.cos(num3));
            point3d17 = MathHelper.distanceBearingPoint(point3dCollection_3.get_Item(0), num + num3, metres / math.cos(num3));
            point3dCollection_2.Add(point3d16.smethod_167(self.method_39(point3d7, num, point3d16, percent1, percent, True)));
            point3dCollection_3.Add(point3d17.smethod_167(self.method_39(point3d7, num, point3d17, percent1, percent, True)));
            point3dCollection_0.appendList(point3dCollection_2);
#             point3dCollection_3.reverse()
            point3dCollection_0.appendList(point3dCollection_3);
            point3d18 = MathHelper.distanceBearingPoint(point3d7, num, metres);
            point3dCollection_5.Add(point3d7.smethod_167(point3d7.get_Z() + 5));
            point3dCollection_5.Add(point3d18.smethod_167(self.method_39(point3d7, num, point3d18, percent1, percent, False)));
            point3dCollection_5.Add(point3d18.smethod_167(self.method_39(point3d7, num, point3d18, percent1, percent, True)));
            point3dCollection_5.Add(point3d7.smethod_167(point3d7.get_Z() + 5));
        return (True, point3dCollection_0, point3dCollection_1, point3dCollection_2, point3dCollection_3, point3dCollection_4, point3dCollection_5);
    def method_39(self, point3d_0, double_0, point3d_1, double_1, double_2, bool_0):
        point3d = None;
        point3d = MathHelper.getIntersectionPoint(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_0, 1000), point3d_1, MathHelper.distanceBearingPoint(point3d_1, double_0 + 1.5707963267949, 1000));
        num = MathHelper.calcDistance(point3d_0, point3d);
        if (not bool_0):
            return point3d_0.get_Z() + 5 + num * double_1;
        return point3d_0.get_Z() + 5 + num * (double_1 - double_2);
    def method_40(self, point3dCollection_0, point3d_0, point3d_1, double_0, double_1, double_2, bool_0):
        point3d = None;
        num = 0;
        num1 = 1;
        num2 = MathHelper.getBearing(point3d_0, point3d_1) - 1.5707963267949;
        num3 = MathHelper.calcDistance(point3d_0, point3d_1);
        for i in range(1, point3dCollection_0.get_Count()):
            num = i - 1;
            num1 = i;
            point3d = MathHelper.getIntersectionPoint(point3d_0, point3d_1, point3dCollection_0.get_Item(num1), MathHelper.distanceBearingPoint(point3dCollection_0.get_Item(num1), num2, 1000));
            num4 = MathHelper.calcDistance(point3d_0, point3d);
            if (MathHelper.smethod_99(num3, num4, 0.0001) or num3 < num4):
                point3d = MathHelper.getIntersectionPoint(point3dCollection_0.get_Item(num), point3dCollection_0.get_Item(num1), point3d_1, MathHelper.distanceBearingPoint(point3d_1, num2, 1000));
                point3dCollection_0.Insert(num1, point3d.smethod_167(self.method_39(point3d_0, double_0, point3d, double_1, double_2, bool_0)));
                num5 = num1 + 1;
                while (point3dCollection_0.get_Count() > num5):
                    point3dCollection_0.RemoveAt(num5);
                return;
        point3d = MathHelper.getIntersectionPoint(point3dCollection_0.get_Item(num), point3dCollection_0.get_Item(num1), point3d_1, MathHelper.distanceBearingPoint(point3d_1, num2, 1000));
        point3dCollection_0.Add(point3d.smethod_167(self.method_39(point3d_0, double_0, point3d, double_1, double_2, bool_0)));
    
    def method_41(self, point3dCollection_0, point3d_0, point3d_1):
        point3d = None;
        num = 1;
        while (True):
            if (num < point3dCollection_0.get_Count()):
                item = point3dCollection_0.get_Item(num - 1);
                item1 = point3dCollection_0.get_Item(num);
                if (not MathHelper.smethod_115(item, point3d_0, point3d_1)):
                    break;
                if (not MathHelper.smethod_115(item1, point3d_0, point3d_1)):
                    point3d = MathHelper.getIntersectionPoint(point3d_0, point3d_1, item, item1);
                    point3dCollection_0.set_Item(0, point3d);
                    return;
                point3dCollection_0.RemoveAt(0);
            else:
                break;
    
    def method_42(self, point3dCollection_0, point3d_0, point3d_1):
        point3d = None;
        num = 1;
        while (True):
            if (num < point3dCollection_0.get_Count()):
                item = point3dCollection_0.get_Item(num - 1);
                item1 = point3dCollection_0.get_Item(num);
                if (not MathHelper.smethod_119(item, point3d_0, point3d_1)):
                    break;
                if (not MathHelper.smethod_119(item1, point3d_0, point3d_1)):
                    point3d = MathHelper.getIntersectionPoint(point3d_0, point3d_1, item, item1);
                    point3dCollection_0.set_Item(0, point3d);
                    return;
                point3dCollection_0.RemoveAt(0);
            else:
                break;
    def method_43(self, point3dCollection_0, point3dCollection_1, point3d_0, double_0):
        point3d = None;
        point3d1 = None;
        point3d2 = MathHelper.distanceBearingPoint(point3d_0, double_0 - 1.5707963267949, 100);
        if (MathHelper.smethod_115(point3dCollection_0.get_Item(0), point3d_0, point3d2) and MathHelper.smethod_115(point3dCollection_1.get_Item(0), point3d_0, point3d2)) or (MathHelper.smethod_119(point3dCollection_0.get_Item(0), point3d_0, point3d2) and MathHelper.smethod_119(point3dCollection_1.get_Item(0), point3d_0, point3d2)):
            point3d = MathHelper.getIntersectionPoint(point3dCollection_1.get_Item(0), MathHelper.distanceBearingPoint(point3dCollection_1.get_Item(0), double_0 - 1.5707963267949, 100), point3dCollection_0.get_Item(0), point3dCollection_0.get_Item(1));
            point3dCollection_0.Insert(1, point3d);
            return;
        point3d1 = MathHelper.getIntersectionPoint(point3dCollection_0.get_Item(1), MathHelper.distanceBearingPoint(point3dCollection_0.get_Item(1), double_0 - 1.5707963267949, 100), point3dCollection_0.get_Item(0), point3dCollection_1.get_Item(0));
        point3dCollection_1.Insert(0, point3d1);
        point3d1 = MathHelper.getIntersectionPoint(point3dCollection_1.get_Item(1), MathHelper.distanceBearingPoint(point3dCollection_1.get_Item(1), double_0 - 1.5707963267949, 100), point3dCollection_0.get_Item(1), point3dCollection_0.get_Item(2));
        point3dCollection_0.Insert(2, point3d1);

    def nominal2Layer(self):
        return AcadHelper.createNominalTrackLayer([self.parametersPanel.pnlDer.Point3d, self.nominalPoint], None, "memory", "NominalTrack_" + self.surfaceType.replace(" ", "_"))
class DepartureStandardObstacles(ObstacleTable):
    def __init__(self, point3d_0, double_0, double_1, double_2, complexObstacleArea_0):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, None)
        self.surfaceType = SurfaceTypes.DepartureStandard
        self.track = double_0;
        self.ptDER = point3d_0;
        self.ptDER2 = MathHelper.distanceBearingPoint(point3d_0, double_0, 100);
        self.moc = double_1;
        self.pdg = double_2;
        self.area = complexObstacleArea_0;
    def setHiddenColumns(self, tableView):
#         tableView.hideColumn(self.IndexObstArea)
#         tableView.hideColumn(self.IndexDistInSecM)
        return ObstacleTable.setHiddenColumns(self, tableView)
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        self.IndexObstArea = fixedColumnCount  
        self.IndexDistInSecM = fixedColumnCount + 1
        self.IndexDoM = fixedColumnCount + 2
        self.IndexMocReqM = fixedColumnCount + 3
        self.IndexMocReqFt = fixedColumnCount + 4
        self.IndexAcAltM = fixedColumnCount + 5
        self.IndexAcAltFt = fixedColumnCount + 6
        self.IndexAltReqM = fixedColumnCount + 7
        self.IndexAltReqFt = fixedColumnCount + 8
        self.IndexPDG = fixedColumnCount + 9
        self.IndexCritical = fixedColumnCount + 10
        self.IndexCloseIn = fixedColumnCount + 11
                 
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DistInSecM,
                ObstacleTableColumnType.DoM,
                ObstacleTableColumnType.MocReqM,
                ObstacleTableColumnType.MocReqFt, 
                ObstacleTableColumnType.AcAltM,
                ObstacleTableColumnType.AcAltFt,
                ObstacleTableColumnType.AltReqM,
                ObstacleTableColumnType.AltReqFt,
                ObstacleTableColumnType.PDG,
                ObstacleTableColumnType.Critical, 
                ObstacleTableColumnType.CloseIn               
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
        self.source.setItem(row, self.IndexDoM, item)
        
        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexMocReqM, item)
                      
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[3])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[3]))
        self.source.setItem(row, self.IndexMocReqFt, item)
        
        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4])
        self.source.setItem(row, self.IndexAcAltM, item)
                      
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[4])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[4]))
        self.source.setItem(row, self.IndexAcAltFt, item)
        
        item = QStandardItem(str(checkResult[5]))
        item.setData(checkResult[5])
        self.source.setItem(row, self.IndexAltReqM, item)
                      
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[5])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[5]))
        self.source.setItem(row, self.IndexAltReqFt, item)
        
        item = QStandardItem(str(checkResult[6]))
        item.setData(checkResult[6])
        self.source.setItem(row, self.IndexPDG, item)
        
        item = QStandardItem(str(checkResult[7]))
        item.setData(checkResult[7])
        self.source.setItem(row, self.IndexCritical, item)
        
        item = QStandardItem(str(checkResult[8]))
        item.setData(checkResult[8])
        self.source.setItem(row, self.IndexCloseIn, item)
    def checkObstacle(self, obstacle_0):
        num = None;
        point3d = None;
        point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.track + 3.14159265358979, obstacle_0.Tolerance);
        point3d2 = MathHelper.distanceBearingPoint(point3d1, self.track + 1.5707963267949, 100);
        point3d = MathHelper.getIntersectionPoint(self.ptDER, self.ptDER2, point3d1, point3d2);
        num = 1E-08 if (not MathHelper.smethod_99(MathHelper.getBearing(self.ptDER, point3d), self.track, 5)) else MathHelper.calcDistance(self.ptDER, point3d);
        mocMultiplier = self.moc / 100 * num * obstacle_0.MocMultiplier;
        num1 = 0;
        num2 = None;
        obstacleAreaResult, num1, num2 = self.area.pointInArea(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier);
        if (obstacleAreaResult != ObstacleAreaResult.Outside and num != None and num1 != None):
            z = self.ptDER.get_Z() + 5 + self.pdg / 100 * num;
            position = obstacle_0.Position;
            z1 = position.get_Z() + obstacle_0.Trees + num1;
            z2 = 100 * ((z1 - (self.ptDER.get_Z() + 5)) / num);
            criticalObstacleType = CriticalObstacleType.No;
            if (z2 > self.pdg):
                criticalObstacleType = CriticalObstacleType.Yes;
            closeInObstacleType = CloseInObstacleType.No;
            if (z1 <= self.ptDER.get_Z() + 60):
                closeInObstacleType = CloseInObstacleType.Yes;
            checkResult = [obstacleAreaResult, num2, num, num1, z, z1, z2, criticalObstacleType, closeInObstacleType];
            self.addObstacleToModel(obstacle_0, checkResult)
#         num = None;
#         point3d = None;
#         point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.track + 3.14159265358979, obstacle_0.Tolerance);
#         point3d2 = MathHelper.distanceBearingPoint(point3d1, self.track + 1.5707963267949, 100);
#         point3d = MathHelper.getIntersectionPoint(self.ptDER, self.ptDER2, point3d1, point3d2);
#         num = 1E-08  if (not MathHelper.smethod_99(MathHelper.getBearing(self.ptDER, point3d), self.track, 5)) else MathHelper.calcDistance(self.ptDER, point3d);
#         mocMultiplier = self.moc / 100 * num * obstacle_0.MocMultiplier;
#         num1 = 0;
#         num2 = None;
#         obstacleAreaResult, num1, num2 = self.area.pointInArea(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier);
# #         if num1 == None:
# #             num1 = 0.0
# #         if num2 == None:
# #             num2 = 0.0
#         if obstacleAreaResult == None:
#             return
#         if (obstacleAreaResult != ObstacleAreaResult.Outside):
#             z = self.ptDER.get_Z() + 5 + self.pdg / 100 * num;
#             position = obstacle_0.Position;
#             z1 = position.get_Z() + obstacle_0.Trees + num1;
#             z2 = 100 * ((z1 - (self.ptDER.get_Z() + 5)) / num);
#             criticalObstacleType = CriticalObstacleType.No;
#             if (z2 > self.pdg):
#                 criticalObstacleType = CriticalObstacleType.Yes;
#             closeInObstacleType = CloseInObstacleType.No;
#             if (z1 <= self.ptDER.get_Z() + 60):
#                 closeInObstacleType = CloseInObstacleType.Yes;
#             checkResult = [obstacleAreaResult, num2, num, num1, z, z1, z2, criticalObstacleType, closeInObstacleType];
#             self.addObstacleToModel(obstacle_0, checkResult)
