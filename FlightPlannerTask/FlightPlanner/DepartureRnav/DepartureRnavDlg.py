# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QString, Qt
from PyQt4.QtGui import QCheckBox, QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsVectorFileWriter,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import AngleUnits, TurnDirection, CriticalObstacleType, \
                    ObstacleTableColumnType, SurfaceTypes, DistanceUnits,AircraftSpeedCategory, \
                    OrientationType, AltitudeUnits, ObstacleAreaResult, RnavDmeDmeFlightPhase, \
                    RnavDmeDmeCriteria, RnavSpecification, RnavGnssFlightPhase , ConstructionType, \
                    CloseInObstacleType
from FlightPlanner.DepartureRnav.ui_DepartureRnav import Ui_DepartureRnav
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
from FlightPlanner.Holding.RnavDmeDme.RnavDmeDmeDlg import RnavDmeDmeTolerance
from FlightPlanner.RnavTolerance.RnavGnssTolerance import RnavGnssTolerance
from FlightPlanner.types import Point3D
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, ComplexObstacleArea, SecondaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.Captions import Captions
from FlightPlanner.messages import Messages

from FlightPlanner.Holding.RnavVorDme.RnavVorDmeDlg import RnavVorDme
from FlightPlanner.Holding.RnavDmeDme.RnavDmeDmeDlg import RnavDmeDme

# from FlightPlanner.IasHelp.IasHelpDlg import IasHelpDlg
import define, math

class DepartureRnavDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("DepartureRnavDlg")
        self.surfaceType = SurfaceTypes.DepartureRnav
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.DepartureRnav)
        self.resize(540, 200)
        QgisHelper.matchingDialogSize(self, 750, 700)
        self.surfaceList = None

        self.resultRnavTolerance = None

        self.isSelectedGnss = True
        self.bearingDirBetweenFirst = 0.0
        self.defaultBearing = 0.0
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
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlRwyDir.txtPointX.text()), float(self.parametersPanel.pnlRwyDir.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlRwyDir.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlRwyDir.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlRwyDir.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlRwyDir.txtPointY.text()))
        parameterList.append(("Altitude", self.parametersPanel.pnlRwyDir.txtAltitudeM.text() + "m"))
        parameterList.append(("", self.parametersPanel.pnlRwyDir.txtAltitudeFt.text() + "ft"))

        parameterList.append(("Start of RWY/FATO Position", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlRwyStart.txtPointX.text()), float(self.parametersPanel.pnlRwyStart.txtPointY.text()))

        parameterList.append(("Lat", self.parametersPanel.pnlRwyStart.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlRwyStart.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlRwyStart.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlRwyStart.txtPointY.text()))

        parameterList.append(("Direction", "Plan : " + str(self.parametersPanel.txtDer.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtDer.txtRadialGeodetic.Value) + define._degreeStr))

        # parameterList.append(("Direction()", self.parametersPanel.txtDer.Value))
        
        parameterList.append(("Parameters", "group"))

        parameterList.append(("Aerodrome Reference Point(ARP)", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlFirstWPt.txtPointX.text()), float(self.parametersPanel.pnlFirstWPt.txtPointY.text()))

        parameterList.append(("Lat", self.parametersPanel.pnlFirstWPt.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlFirstWPt.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlFirstWPt.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlFirstWPt.txtPointY.text()))


        parameterList.append(("First Waypoint Psition", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlARP.txtPointX.text()), float(self.parametersPanel.pnlARP.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlARP.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlARP.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlARP.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlARP.txtPointY.text()))
        
        parameterList.append(("Distance", self.parametersPanel.txtDistance.text() +"nm"))
        parameterList.append(("Altitude", self.parametersPanel.txtAltitudeM.text() +"m"))
        parameterList.append(("", self.parametersPanel.txtAltitudeFt.text() +"ft"))

        parameterList.append(("Sensor Type", self.parametersPanel.cmbSensorType.currentText()))
        parameterList.append(("Rnav Specification", self.parametersPanel.cmbSpecification.currentText()))
        if self.parametersPanel.cmbSensorType.currentIndex() != 0:            
            parameterList.append(("Number of DMEs used", self.parametersPanel.cmbDmeCount.currentText()))
        if self.parametersPanel.chbCatH.isChecked():            
            parameterList.append(("Cat. H", "True"))
        else:
            parameterList.append(("Cat. H", "False"))
        
        parameterList.append(("MOC", self.parametersPanel.txtMoc.text() + "%"))
        parameterList.append(("PDG", self.parametersPanel.txtPdg.text() + "%"))
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstruct.currentText()))
        parameterList.append(("MOCmultipiler", str(self.parametersPanel.mocSpinBox.value())))

        parameterList.append(("Results", "group"))
        parameterList.append(("Waypoint 1", "group"))
        parameterList.append(("XTT", self.parametersPanel.txtXtt1D.text()))
        parameterList.append(("ATT", self.parametersPanel.txtAtt1D.text()))
        parameterList.append(("1/2 A/w", self.parametersPanel.txtAsw1D.text()))

        parameterList.append(("Waypoint 2", "group"))
        parameterList.append(("XTT", self.parametersPanel.txtXtt2D.text()))
        parameterList.append(("ATT", self.parametersPanel.txtAtt2D.text()))
        parameterList.append(("1/2 A/w", self.parametersPanel.txtAsw2D.text()))


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
        point3dCollection = [];
        point3dCollection1 = [];
        point3dCollection2 = [];
        point3dCollection3 = [];
        point3dCollection4 = [];
#         point3dCollection5 = [];
#         if (!AcadHelper.Ready)
#         {
#             return;
#         }
#         if (!self.method_27(false))
#         {
#             return;
#         }
        result, point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, point3dCollection4, point3dCollection5 = self.method_37() 
        if (not result ):
            return;
        complexObstacleArea = ComplexObstacleArea();
        point3dCollection6 = [];
        point3dCollection6.extend(point3dCollection2);
        point3dCollection3.reverse()
        point3dCollection6.extend(point3dCollection3);
        complexObstacleArea.Add(PrimaryObstacleArea(PolylineArea(point3dCollection6)));
        for i in range(1, len(point3dCollection2)):
            if (not point3dCollection2[i - 1].smethod_170(point3dCollection1[i - 1]) or not point3dCollection2[i].smethod_170(point3dCollection1[i])):
                complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection2[i - 1], point3dCollection2[i], point3dCollection1[i - 1], point3dCollection1[i], MathHelper.getBearing(point3dCollection2[i - 1], point3dCollection2[i])));
        for j in range(1, len(point3dCollection3)):
            if (not point3dCollection3[j - 1].smethod_170(point3dCollection4[j - 1]) or not point3dCollection3[j].smethod_170(point3dCollection4[j])):
                complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection3[j - 1], point3dCollection3[j], point3dCollection4[j - 1], point3dCollection4[j], MathHelper.getBearing(point3dCollection3[j - 1], point3dCollection3[j])));
        point3d = self.parametersPanel.pnlRwyDir.Point3d;
        point3d1 = self.parametersPanel.pnlFirstWPt.Point3d;
        percent = float(self.parametersPanel.txtMoc.text());
        num = float(self.parametersPanel.txtPdg.text());
        num1 = Unit.ConvertDegToRad(float(self.parametersPanel.txtDer.Value));
        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        self.obstaclesModel = DepartureRnavObstacles(point3d, num1, percent, num, complexObstacleArea);
            
        return FlightPlanBaseDlg.btnEvaluate_Click(self)

    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        if (math.fabs(Unit.ConvertRadToDeg(self.defaultBearing) - float(self.parametersPanel.txtDer.Value))) > 15.05:
            QMessageBox.warning(self, "Warning", Messages.ERR_COURSE_CHANGES_GREATER_THAN_15_NOT_ALLOWED + "\nThe bearing between the Start RWY and DER position is " +str(round(Unit.ConvertRadToDeg(self.defaultBearing), 4)) + ".")
            self.parametersPanel.txtDer.Value = round(Unit.ConvertRadToDeg(self.defaultBearing), 4)
            return


        point3dCollection = None;
        point3dCollection1 = None;
        point3dCollection2 = None;
        point3dCollection3 = None;
        point3dCollection4 = None;
        point3dCollection5 = None;
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        point3d3 = None;

        
        mapUnits = define._canvas.mapUnits()
        constructionLayer = None
        
        result, point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, point3dCollection4, point3dCollection5 = self.method_37()
        if not result:
            return
        point3dArrayResult = []
        if (self.parametersPanel.cmbConstruct.currentText() != ConstructionType.Construct2D):
#             point3dArrayResult = []
            point3d4 = self.parametersPanel.pnlRwyDir.Point3d;
            point3d5 = self.parametersPanel.pnlFirstWPt.Point3d;
            percent = float(self.parametersPanel.txtPdg.text()) / 100;
            num = float(self.parametersPanel.txtMoc.text()) / 100;
            num1 = Unit.ConvertDegToRad(float(self.parametersPanel.txtDer.Value));
            num2 = MathHelper.getBearing(point3d4, point3d5) + 1.5707963267949;
            for i in range(1, len(point3dCollection2)):
                if (not point3dCollection2[i - 1].smethod_170(point3dCollection1[i - 1]) or not point3dCollection2[i].smethod_170(point3dCollection1[i])):
                    point3dArrayResult.append([point3dCollection2[i - 1], point3dCollection2[i], point3dCollection1[i], point3dCollection1[i - 1]])
#                     AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3dCollection2.get_Item(i - 1), point3dCollection2.get_Item(i), point3dCollection1.get_Item(i), point3dCollection1.get_Item(i - 1), true, true, true, true), constructionLayer);
            for j in range(1, len(point3dCollection3)):
                if (not point3dCollection3[j - 1].smethod_170(point3dCollection4[j - 1]) or not point3dCollection3[j].smethod_170(point3dCollection4[j])):
                    point3dArrayResult.append([point3dCollection3[j - 1], point3dCollection3[j], point3dCollection4[j], point3dCollection4[j - 1]])
#                     AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3dCollection3.get_Item(j - 1), point3dCollection3.get_Item(j), point3dCollection4.get_Item(j), point3dCollection4.get_Item(j - 1), true, true, true, true), constructionLayer);
            for k in range(1, len(point3dCollection2)):
                item = point3dCollection2[k - 1];
                item1 = point3dCollection2[k];
                if (not item.smethod_170(item1)):
                    if (k != 1):
                        point3d = MathHelper.getIntersectionPoint(point3d4, point3d5, item, MathHelper.distanceBearingPoint(item, num2, 1000));
                    else:
                        point3d = point3d4.smethod_167(item.get_Z());
                    point3d1 = MathHelper.getIntersectionPoint(point3d4, point3d5, item1, MathHelper.distanceBearingPoint(item1, num2, 1000));
                    point3d = point3d.smethod_167(self.method_38(point3d4, num1, point3d, percent, num, True));
                    point3d1 = point3d1.smethod_167(self.method_38(point3d4, num1, point3d1, percent, num, True));
                    point3dArrayResult.append([item, item1, point3d1, point3d])
#                     AcadHelper.smethod_18(transaction, blockTableRecord, new Face(item, item1, point3d1, point3d, true, true, true, true), constructionLayer);
            for l in range(1, len(point3dCollection3)):
                item2 = point3dCollection3[l - 1];
                item3 = point3dCollection3[l];
                if (not item2.smethod_170(item3)):
                    if (l != 1):
                        point3d2 = MathHelper.getIntersectionPoint(point3d4, point3d5, item2, MathHelper.distanceBearingPoint(item2, num2, 1000));
                    else:
                        point3d2 = point3d4.smethod_167(item2.get_Z());
                    point3d3 = MathHelper.getIntersectionPoint(point3d4, point3d5, item3, MathHelper.distanceBearingPoint(item3, num2, 1000));
                    point3d2 = point3d2.smethod_167(self.method_38(point3d4, num1, point3d2, percent, num, True));
                    point3d3 = point3d3.smethod_167(self.method_38(point3d4, num1, point3d3, percent, num, True));
                    point3dArrayResult.append([item2, item3, point3d3, point3d2])
#                     AcadHelper.smethod_18(transaction, blockTableRecord, new Face(item2, item3, point3d3, point3d2, true, true, true, true), constructionLayer);
            point3dArrayResult.append([point3dCollection5[0], point3dCollection5[1], point3dCollection5[2], point3dCollection5[3]])   
#             AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3dCollection5.get_Item(0), point3dCollection5.get_Item(1), point3dCollection5.get_Item(2), point3dCollection5.get_Item(3), true, true, true, true), constructionLayer);
            if define._mapCrs == None:
                if mapUnits == QGis.Meters:
                    constructionLayer = QgsVectorLayer("polygon?crs=EPSG:32633", self.surfaceType, "memory")
                else:
                    constructionLayer = QgsVectorLayer("polygon?crs=EPSG:4326", self.surfaceType, "memory")
            else:
                constructionLayer = QgsVectorLayer("polygon?crs=%s"%define._mapCrs.authid (), self.surfaceType, "memory")

            shpPath = ""
            if define.obstaclePath != None:
                shpPath = define.obstaclePath
            elif define.xmlPath != None:
                shpPath = define.xmlPath
            else:
                shpPath = define.appPath
            er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + QString(self.surfaceType).replace(" ", "") + ".shp", "utf-8", constructionLayer.crs())
            constructionLayer = QgsVectorLayer(shpPath + "/" + QString(self.surfaceType).replace(" ", "") + ".shp", self.surfaceType, "ogr")


            constructionLayer.startEditing()
            for point3dArray in point3dArrayResult:
                polygon = QgsGeometry.fromPolygon([point3dArray])
                feature = QgsFeature()
                feature.setGeometry(polygon)
                pr = constructionLayer.dataProvider()
                pr.addFeatures([feature])
                # constructionLayer.addFeature(feature)
            constructionLayer.commitChanges()
            QgisHelper.appendToCanvas(define._canvas, [constructionLayer], self.surfaceType)
            self.resultLayerList = [constructionLayer]
        else:
            num3 = 0;
            for m in range(1, len(point3dCollection2)):
                if point3dCollection2[m - 1].smethod_170(point3dCollection1[m - 1]) and point3dCollection2[m].smethod_170(point3dCollection1[m]):
                    num3 += 1;
                else:
                    break
                
            for n in range(num3):
                point3dCollection2.remove(point3dCollection2[0]);
            num3 = 0;
            for o in range(1, len(point3dCollection3)):
                if point3dCollection3[o - 1].smethod_170(point3dCollection4[o - 1]) and point3dCollection3[o].smethod_170(point3dCollection4[o]):
                    num3 += 1;
                else:
                    break
            for p in range(num3):
                point3dCollection3.remove(point3dCollection3[0]);
            point3dArrayResult.append(point3dCollection1)
#             AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_128(point3dCollection1), constructionLayer);
            if (len(point3dCollection2) > 1):
                point3dArrayResult.append(point3dCollection2)
#                 AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_128(point3dCollection2), constructionLayer);
#             }
            if (len(point3dCollection3) > 1):
                point3dArrayResult.append(point3dCollection3)
#                 AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_128(point3dCollection3), constructionLayer);
#             }
            point3dArrayResult.append(point3dCollection4)
#             AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_128(point3dCollection4), constructionLayer);
            point3dArray = [point3dCollection1[0], point3dCollection4[0]]
            point3dArrayResult.append(point3dArray)
#             AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(point3dArray), constructionLayer);
            point3dArray1 = [point3dCollection1[len(point3dCollection1) - 1], point3dCollection4[len(point3dCollection4) - 1]]
            point3dArrayResult.append(point3dArray1)
#             AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(point3dArray1), constructionLayer);

            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)
            for point3dArray in point3dArrayResult:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, point3dArray)
            nominalTrackLayer = self.nominal2Layer()
            QgisHelper.appendToCanvas(define._canvas, [constructionLayer, nominalTrackLayer], self.surfaceType)
            self.resultLayerList = [constructionLayer, nominalTrackLayer]
        QgisHelper.zoomToLayers(self.resultLayerList)
        self.ui.btnEvaluate.setEnabled(True)
    def initParametersPan(self):
        ui = Ui_DepartureRnav()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.gbResultsDME.setEnabled(False)
        self.parametersPanel.gbResultsVOR.setVisible(False)
        # self.parametersPanel.btnCaptureDer.setVisible(False)
        self.parametersPanel.btnCaptureDistance.setVisible(False)

        self.parametersPanel.gbResultsDME.setTitle("Results")


        self.parametersPanel.chbHideCloseInObst = QCheckBox(self.ui.grbResult)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.parametersPanel.chbHideCloseInObst.setFont(font)
        self.parametersPanel.chbHideCloseInObst.setObjectName("chbHideCloseInObst")
        self.ui.vlResultGroup.addWidget(self.parametersPanel.chbHideCloseInObst)
        self.parametersPanel.chbHideCloseInObst.setText("Hide close-in obstacles")
        
        
        self.parametersPanel.frame_63.setVisible(False)
        
        self.parametersPanel.pnlRwyDir = PositionPanel(self.parametersPanel.gbRunway)
        self.parametersPanel.pnlRwyDir.groupBox.setTitle("DER Position")
        self.parametersPanel.pnlRwyDir.btnCalculater.hide()
#         self.parametersPanel.pnlRwyDir.hideframe_Altitude()
        self.parametersPanel.pnlRwyDir.setObjectName("pnlRwyDir")
        ui.vl_gbRunway.insertWidget(0, self.parametersPanel.pnlRwyDir)
        # self.parametersPanel.pnlRwyDir.txtPointY.textChanged.connect(self.CalcDistance)
        self.connect(self.parametersPanel.pnlRwyDir, SIGNAL("positionChanged"), self.CalcDistance)
        self.connect(self.parametersPanel.pnlRwyDir, SIGNAL("positionChanged"), self.CalcDirection)
        self.connect(self.parametersPanel.pnlRwyDir, SIGNAL("positionChanged"), self.DistanceChanged)
        self.connect(self.parametersPanel.pnlRwyDir, SIGNAL("positionChanged"), self.VorDmeShow)

        self.parametersPanel.pnlRwyDir.txtAltitudeM.textChanged.connect(self.dirAltitudeMChanged)


        self.parametersPanel.pnlRwyStart = PositionPanel(self.parametersPanel.gbRunway)
        self.parametersPanel.pnlRwyStart.groupBox.setTitle("Start of RWY/FATO Position")
        self.parametersPanel.pnlRwyStart.btnCalculater.hide()
        self.parametersPanel.pnlRwyStart.hideframe_Altitude()
        self.parametersPanel.pnlRwyStart.setObjectName("pnlRwyStart")
        ui.vl_gbRunway.insertWidget(1, self.parametersPanel.pnlRwyStart)
        self.connect(self.parametersPanel.pnlRwyStart, SIGNAL("positionChanged"), self.CalcDirection)
        self.connect(self.parametersPanel.pnlRwyStart, SIGNAL("positionChanged"), self.VorDmeShow)
        # self.parametersPanel.pnlRwyStart.txtPointY.textChanged.connect(self.CalcDirection)

        self.parametersPanel.pnlARP = PositionPanel(self.parametersPanel.gbParameters)
        self.parametersPanel.pnlARP.groupBox.setTitle("Aerodrome Reference Point(ARP)")
        self.parametersPanel.pnlARP.btnCalculater.hide()
        self.parametersPanel.pnlARP.hideframe_Altitude()
        self.parametersPanel.pnlARP.setObjectName("pnlARP")
        ui.vl_gbParameters.insertWidget(0, self.parametersPanel.pnlARP)
        self.connect(self.parametersPanel.pnlARP, SIGNAL("positionChanged"), self.VorDmeShow)
        
        self.parametersPanel.pnlFirstWPt = PositionPanel(self.parametersPanel.gbParameters)
        self.parametersPanel.pnlFirstWPt.groupBox.setTitle("First Waypoint Position")
        self.parametersPanel.pnlFirstWPt.btnCalculater.hide()
        self.parametersPanel.pnlFirstWPt.hideframe_Altitude()
        self.parametersPanel.pnlFirstWPt.setObjectName("pnlFirstWPt")
        ui.vl_gbParameters.insertWidget(1, self.parametersPanel.pnlFirstWPt)
        self.connect(self.parametersPanel.pnlFirstWPt, SIGNAL("positionChanged"), self.CalcDistance)
        self.connect(self.parametersPanel.pnlFirstWPt, SIGNAL("positionChanged"), self.VorDmeShow)

        # self.parametersPanel.pnlFirstWPt.txtPointY.textChanged.connect(self.CalcDistance)

        self.parametersPanel.cmbSensorType.addItems(["GNSS", "DME/DME"])
        self.parametersPanel.cmbSensorType.currentIndexChanged.connect(self.cmbSensorTypeChanged)
        self.parametersPanel.cmbSpecification.addItems(["Rnav1", "Rnav2", "Rnp1", "ARnp1", "ARnp09", "ARnp08", "ARnp07", "ARnp06", "ARnp05", "ARnp04", "ARnp03"])

        self.parametersPanel.cmbDmeCount.addItems(["2", "More than 2"])
        self.parametersPanel.cmbConstruct.addItems(["2D", "3D"])
        
        self.flag = 0
        self.flag1 = 0
        self.parametersPanel.txtAltitudeFt.textChanged.connect(self.txtAltitudeFtChanged)
        self.parametersPanel.txtAltitudeM.textChanged.connect(self.txtAltitudeMChanged)
        self.parametersPanel.txtAltitudeM.textChanged.connect(self.VorDmeShow)
        self.parametersPanel.cmbSpecification.currentIndexChanged.connect(self.VorDmeShow)
        self.parametersPanel.cmbSensorType.currentIndexChanged.connect(self.VorDmeShow)
        self.parametersPanel.cmbDmeCount.currentIndexChanged.connect(self.VorDmeShow)
        self.parametersPanel.txtDistance.textChanged.connect(self.DistanceChanged)
        self.connect(self.parametersPanel.txtDer, SIGNAL("Event_0"), self.DistanceChanged)
#         self.parametersPanel.cmbHoldingFunctionality.currentIndexChanged.connect(self.cmbHoldingFunctionalityCurrentIndexChanged)
#         self.parametersPanel.cmbOutboundLimit.currentIndexChanged.connect(self.cmbOutboundLimitCurrentIndexChanged)
#         self.parametersPanel.btnCaptureDer.clicked.connect(self.captureBearing)
        self.parametersPanel.chbHideCloseInObst.stateChanged.connect(self.chbHideCloseInObstStateChanged)

#         self.parametersPanel.btnCaptureDistance.clicked.connect(self.measureDistance)
#         self.parametersPanel.btnCaptureLength.clicked.connect(self.measureLength)        
        self.parametersPanel.txtPdg.textChanged.connect(self.pdgChanged)
#         self.parametersPanel.cmbAircraftCategory.currentIndexChanged.connect(self.changeCategory)
#         self.parametersPanel.btnIasHelp.clicked.connect(self.iasHelpShow)
#         self.parametersPanel.txtIas.textChanged.connect(self.iasChanged)
#         self.parametersPanel.txtIsa.textChanged.connect(self.isaChanged)
#     ]
        self.VorDmeShow()
        self.flag2 = 0
        self.flag3 = 0
        self.trackRadialPanelSetEnabled()
    def dirAltitudeMChanged(self):
        try:
            distM = Distance(float(self.parametersPanel.txtDistance.text()), DistanceUnits.NM).Metres
            if self.flag3==0:
                self.flag3=2;
            if self.flag3==1:
                self.flag3=0;
            if self.flag3==2:
                try:

                    altitudeMValue = (distM * (float(self.parametersPanel.txtPdg.text()) / 100)) + (float(self.parametersPanel.pnlRwyDir.txtAltitudeM.text()) + 5.0)
                    self.parametersPanel.txtAltitudeM.setText(str(round(altitudeMValue, 4)))
                except:
                    pass
        except:
            pass
    def DistanceChanged(self):
        try:

            distM = Distance(float(self.parametersPanel.txtDistance.text()), DistanceUnits.NM).Metres
            altitudeMValue = (distM * (float(self.parametersPanel.txtPdg.text()) / 100)) + (float(self.parametersPanel.pnlRwyDir.txtAltitudeM.text()) + 5.0)

            # pointDer = self.parametersPanel.pnlRwyDir.Point3d
            # pointStart = self.parametersPanel.pnlRwyStart.Point3d
            # bearingDirection = MathHelper.getBearing(pointStart, pointDer)
            bearingDirection = Unit.ConvertDegToRad(float(self.parametersPanel.txtDer.Value))

            pointFirst = MathHelper.distanceBearingPoint(self.parametersPanel.pnlRwyDir.Point3d, bearingDirection, distM)
            self.parametersPanel.txtAltitudeM.setText(str(round(altitudeMValue, 4)))
            if self.flag2==0:
                self.flag2=1;
            if self.flag2==2:
                self.flag2=0;
            if self.flag2==1:
                try:



                    #Calculate First Waypoint

                    self.parametersPanel.pnlFirstWPt.Point3d = pointFirst

                except:
                    pass
        except:
            pass

    def pdgChanged(self):
        if self.flag1==0:
            self.flag1=2;
        if self.flag1==1:
            self.flag1=0;
        if self.flag1==2:
            try:
                distM = Distance(float(self.parametersPanel.txtDistance.text()), DistanceUnits.NM).Metres
                altitudeMValue = (distM * (float(self.parametersPanel.txtPdg.text())) / 100) + (float(self.parametersPanel.pnlRwyDir.txtAltitudeM.text()) + 5.0)
                self.parametersPanel.txtAltitudeM.setText(str(round(altitudeMValue, 4)))
            except:
                pass
    def txtAltitudeMChanged(self):
        if self.flag==0:
            self.flag=1;
        if self.flag==2:
            self.flag=0;
        if self.flag==1:
            try:
                self.parametersPanel.txtAltitudeFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAltitudeM.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeFt.setText("0.0")

        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                distM = Distance(float(self.parametersPanel.txtDistance.text()), DistanceUnits.NM).Metres
                pdgValue = ((float(self.parametersPanel.txtAltitudeM.text()) - (float(self.parametersPanel.pnlRwyDir.txtAltitudeM.text()) + 5.0)) / distM) * 100
                self.parametersPanel.txtPdg.setText(str(pdgValue))
            except:
                pass
    def txtAltitudeFtChanged(self):
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitudeFt.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")

    def method_RnavToleranceCalc(self):
        rnavDmeDmeFlightPhase = RnavDmeDmeFlightPhase.Sid15;
        num8 = Unit.ConvertNMToMeter(15);
        num9 = Unit.ConvertNMToMeter(30);
        percent = float(self.parametersPanel.txtMoc.text()) / 100;
        percent1 = float(self.parametersPanel.txtPdg.text()) / 100;

        try:
            point3d9 = self.parametersPanel.pnlRwyDir.Point3d
            point3d10 = self.parametersPanel.pnlARP.Point3d;
            point3d11 = self.parametersPanel.pnlFirstWPt.Point3d;

            num11 = MathHelper.calcDistance(point3d10, point3d11);

            if (num11 >= num8 and num11 < num9):
                rnavDmeDmeFlightPhase = RnavDmeDmeFlightPhase.Star30Sid30IfIaf;
            elif (num11 >= num9):
                rnavDmeDmeFlightPhase = RnavDmeDmeFlightPhase.EnrouteStarSid;
        except:
            pass
        aircraftSpeedCategory = AircraftSpeedCategory.H if (self.parametersPanel.chbCatH.isChecked()) else AircraftSpeedCategory.D;
        rnavSpecification = self.parametersPanel.cmbSpecification.currentText()#(RnavSpecification)EnumHelper.smethod_1((string)self.pnlSpecification.SelectedItem, typeof(RnavSpecification));
        rnavSensorType = self.parametersPanel.cmbSensorType.currentText()#(RnavSensorType)EnumHelper.smethod_1((string)self.pnlSensorType.SelectedItem, typeof(RnavSensorType));



        if (rnavSensorType != "GNSS"):
            rnavDmeDmeCriterium = self.parametersPanel.cmbDmeCount.currentIndex()#(RnavDmeDmeCriteria)EnumHelper.smethod_1((string)self.pnlDmeCount.SelectedItem, typeof(RnavDmeDmeCriteria));
            self.resultRnavTolerance = RnavDmeDmeTolerance(rnavSpecification, rnavDmeDmeFlightPhase, rnavDmeDmeCriterium, Altitude(float(self.parametersPanel.txtAltitudeM.text())))
        else:
            self.resultRnavTolerance = RnavGnssTolerance(rnavSpecification, RnavGnssFlightPhase.Sid15, None, aircraftSpeedCategory)


    def VorDmeShow(self):
        try:
            self.method_RnavToleranceCalc()
        except:
            pass
        try:
            self.parametersPanel.txtAsw1D.setText(str(round(self.resultRnavTolerance.ASW.NauticalMiles, 2)))
            self.parametersPanel.txtXtt1D.setText(str(round(self.resultRnavTolerance.XTT.NauticalMiles, 2)))
            self.parametersPanel.txtAtt1D.setText(str(round(self.resultRnavTolerance.ATT.NauticalMiles, 2)))
        except:
            pass
    def CalcDirection(self):
        try:
            pointDer = self.parametersPanel.pnlRwyDir.Point3d
            pointStart = self.parametersPanel.pnlRwyStart.Point3d
            self.trackRadialPanelSetEnabled()
            self.defaultBearing = MathHelper.getBearing(pointStart, pointDer)
            self.parametersPanel.txtDer.Value = round(Unit.ConvertRadToDeg(MathHelper.getBearing(pointStart, pointDer)),4)
        except:
            pass
    def CalcDistance(self):
        pointFirst = None
        pointDer = None
        try:
            pointDer = self.parametersPanel.pnlRwyDir.Point3d
            pointFirst = self.parametersPanel.pnlFirstWPt.Point3d
        except:
            return
        if self.flag2==0:
            self.flag2=2;
        if self.flag2==1:
            self.flag2=0;
        if self.flag2==2:
            try:
                # pointDer = self.parametersPanel.pnlRwyDir.Point3d
                # pointFirst = self.parametersPanel.pnlFirstWPt.Point3d
                # self.bearingDirBetweenFirst = Unit.ConvertDegToRad(float(self.parametersPanel.txtDer.Value))#MathHelper.getBearing(pointDer, pointFirst)
                self.parametersPanel.txtDistance.setText(str(round(Distance(MathHelper.calcDistance(pointDer, pointFirst)).NauticalMiles, 4)))
            # self.parametersPanel.txtAltitudeM.setText(self.parametersPanel.pnlFirstWPt.txtAltitudeM.text())
            # self.parametersPanel.txtAltitudeFt.setText(self.parametersPanel.pnlFirstWPt.txtAltitudeFt.text())
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
    
    def cmbSensorTypeChanged(self, index):
        self.parametersPanel.cmbSpecification.clear()
        if index == 0:
            self.parametersPanel.frame_63.setVisible(False)
            self.parametersPanel.cmbSpecification.addItems(["Rnav1", "Rnav2", "Rnp1", "ARnp1", "ARnp09", "ARnp08", "ARnp07", "ARnp06", "ARnp05", "ARnp04", "ARnp03"])
            self.isSelectedGnss = True

        else:
            self.parametersPanel.frame_63.setVisible(True)
            self.parametersPanel.cmbSpecification.addItems(["Rnav1", "Rnav2"])
            self.isSelectedGnss = False
        self.VorDmeShow()
    
    # def captureBearing(self):
    #     self.captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtDer)
    #     define._canvas.setMapTool(self.captureTrackTool)
    def method_37(self):
        turnDirection = None
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        point3d3 = None;
        point3d4 = None;
        point3d5 = None;
        point3d6 = None;
        point3d7 = None;
        point3d8 = None;
        distance = None;
        num = None;
        num1 = None;
        num2 = None;
        num3 = None;
        point3dCollection_0 = [];
        point3dCollection_1 = [];
        point3dCollection_2 = [];
        point3dCollection_3 = [];
        point3dCollection_4 = [];
        point3dCollection_5 = [];
        point3d9 = self.parametersPanel.pnlRwyDir.Point3d
        point3d10 = self.parametersPanel.pnlARP.Point3d;
        point3d11 = self.parametersPanel.pnlFirstWPt.Point3d;
        percent = float(self.parametersPanel.txtMoc.text()) / 100;
        percent1 = float(self.parametersPanel.txtPdg.text()) / 100;
        aircraftSpeedCategory = AircraftSpeedCategory.H if (self.parametersPanel.chbCatH.isChecked()) else AircraftSpeedCategory.D;
        rnavSpecification = self.parametersPanel.cmbSpecification.currentText()#(RnavSpecification)EnumHelper.smethod_1((string)self.pnlSpecification.SelectedItem, typeof(RnavSpecification));
        rnavSensorType = self.parametersPanel.cmbSensorType.currentText()#(RnavSensorType)EnumHelper.smethod_1((string)self.pnlSensorType.SelectedItem, typeof(RnavSensorType));
        num4 = 90 / percent1 if (self.parametersPanel.chbCatH.isChecked()) else 120 / percent1;
        num5 = 45 if (self.parametersPanel.chbCatH.isChecked()) else 150;
        num6 = Unit.ConvertDegToRad(float(self.parametersPanel.txtDer.Value));
        num7 = MathHelper.getBearing(point3d9, point3d11);
        distance1 = Distance(MathHelper.calcDistance(point3d9, point3d11));
        num8 = Unit.ConvertNMToMeter(15);
        num9 = Unit.ConvertNMToMeter(30);
        if (MathHelper.calcDistance(point3d9, point3d10) > Unit.ConvertNMToMeter(10)):
            QMessageBox.warning(self, Captions.DER, Messages.ERR_DISTANCE_BETWEEN_X_AND_ARP_EXCEEDS_10_NM)
#             ErrorMessageBox.smethod_0(self, string.Format(Messages.ERR_DISTANCE_BETWEEN_X_AND_ARP_EXCEEDS_10_NM, Captions.DER));
            return (False, None, None, None, None, None, None);
        turnDirectionList = []
        num10 = MathHelper.smethod_77(num6, num7, AngleUnits.Radians, turnDirectionList);
        turnDirection = turnDirectionList[0]
        if (turnDirection != TurnDirection.Nothing and num10 > Unit.ConvertDegToRad(15.05)):
            QMessageBox.warning(self, "Warning", Messages.ERR_COURSE_CHANGES_GREATER_THAN_15_NOT_ALLOWED)
#             ErrorMessageBox.smethod_0(self, Messages.ERR_COURSE_CHANGES_GREATER_THAN_15_NOT_ALLOWED);
            return (False, None, None, None, None, None, None);
        num11 = num4 / math.cos(num10);
        if (MathHelper.calcDistance(point3d9, point3d11) <= num11):
            eRRINSUFFICIENTDISTANCEFIRSTWPTDER = Messages.ERR_INSUFFICIENT_DISTANCE_FIRST_WPT_DER;
            distance = Distance(num4);
            QMessageBox.warning(self, "Warning", eRRINSUFFICIENTDISTANCEFIRSTWPTDER%distance.NauticalMiles)
#             ErrorMessageBox.smethod_0(self, string.Format(eRRINSUFFICIENTDISTANCEFIRSTWPTDER, distance.method_0(":nm")));
            return (False, None, None, None, None, None, None);
        num12 = num7 - 1.5707963267949;
        num13 = num7 + 1.5707963267949;
        num14 = num7 + 3.14159265358979;
        num15 = num6 - 1.5707963267949;
        num16 = num6 + 1.5707963267949;
        num17 = Unit.ConvertDegToRad(15);
        point3dCollection_1.append(MathHelper.distanceBearingPoint(point3d9, num15, num5).smethod_167(point3d9.get_Z() + 5));
        point3dCollection_2.append(MathHelper.distanceBearingPoint(point3d9, num15, num5).smethod_167(point3d9.get_Z() + 5));
        point3dCollection_3.append(MathHelper.distanceBearingPoint(point3d9, num16, num5).smethod_167(point3d9.get_Z() + 5));
        point3dCollection_4.append(MathHelper.distanceBearingPoint(point3d9, num16, num5).smethod_167(point3d9.get_Z() + 5));
        num18 = num5 * math.cos(num10);
        if (rnavSensorType != "GNSS"):
            rnavDmeDmeCriterium = self.parametersPanel.cmbDmeCount.currentIndex()#(RnavDmeDmeCriteria)EnumHelper.smethod_1((string)self.pnlDmeCount.SelectedItem, typeof(RnavDmeDmeCriteria));
            
            num11 = MathHelper.calcDistance(point3d10, point3d11);
            rnavDmeDmeFlightPhase = RnavDmeDmeFlightPhase.Sid15;
            if (num11 >= num8 and num11 < num9):
                rnavDmeDmeFlightPhase = RnavDmeDmeFlightPhase.Star30Sid30IfIaf;
            elif (num11 >= num9):
                rnavDmeDmeFlightPhase = RnavDmeDmeFlightPhase.EnrouteStarSid;
            altitude = Altitude(MathHelper.smethod_0(point3d9.get_Z() + percent1 * MathHelper.calcDistance(point3d9, point3d11) + 5, -2), AltitudeUnits.M);
            num19 = Unit.ConvertNMToMeter(2);
            if (rnavDmeDmeCriterium == RnavDmeDmeCriteria.MoreThanTwo and rnavSpecification == "RNAV2"):
                num19 = Unit.ConvertNMToMeter(2.26);
            elif (rnavDmeDmeCriterium == RnavDmeDmeCriteria.MoreThanTwo and rnavSpecification == "RNAV1"):
                num19 = Unit.ConvertNMToMeter(1.68);
            distance = RnavDmeDmeTolerance(rnavSpecification, rnavDmeDmeFlightPhase, rnavDmeDmeCriterium, altitude).ASW;
            self.resultRnavTolerance = RnavDmeDmeTolerance(rnavSpecification, rnavDmeDmeFlightPhase, rnavDmeDmeCriterium, Altitude(float(self.parametersPanel.txtAltitudeM.text())))
            num20 = max([distance.Metres, num19]);
            point3d12 = MathHelper.distanceBearingPoint(point3d9, num12, num19 / 2);
            point3d13 = MathHelper.distanceBearingPoint(point3d11, num12, num20 / 2);
            point3d14 = MathHelper.distanceBearingPoint(point3d9, num12, num19);
            point3d15 = MathHelper.distanceBearingPoint(point3d11, num12, num20);
            point3d16 = MathHelper.distanceBearingPoint(point3d9, num13, num19 / 2);
            point3d17 = MathHelper.distanceBearingPoint(point3d11, num13, num20 / 2);
            point3d18 = MathHelper.distanceBearingPoint(point3d9, num13, num19);
            point3d19 = MathHelper.distanceBearingPoint(point3d11, num13, num20);
            if (turnDirection != TurnDirection.Nothing):
                if (turnDirection == TurnDirection.Left):
                    point3d6 = MathHelper.distanceBearingPoint(point3dCollection_1[0], num7 - num17, 100);
                    point3d7 = MathHelper.getIntersectionPoint(point3dCollection_1[0], point3d6, point3d12, point3d13);
                    point3d8 = MathHelper.getIntersectionPoint(point3dCollection_1[0], point3d6, point3d14, point3d15);
                    point3dCollection_1.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                    point3dCollection_2.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                    point3d7 = MathHelper.getIntersectionPoint(point3d8, MathHelper.distanceBearingPoint(point3d8, num7 + 1.5707963267949, 100), point3d12, point3d13);
                    point3dCollection_1.append(point3d8.smethod_167(self.method_38(point3d9, num6, point3d8, percent1, percent, False)));
                    point3dCollection_2.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                    if (turnDirection != TurnDirection.Nothing):
                        point3d6 = MathHelper.distanceBearingPoint(point3dCollection_4[0], num6 + num17, num4 / math.cos(num17));
                        point3d7 = MathHelper.getIntersectionPoint(point3dCollection_4[0], point3d6, point3d16, point3d17);
                        if (MathHelper.calcDistance(point3dCollection_4[0], point3d6) <= MathHelper.calcDistance(point3dCollection_4[0], point3d7)):
                            point3dCollection_4.append(point3d6.smethod_167(self.method_38(point3d9, num6, point3d6, percent1, percent, True)));
                            point3dCollection_3.append(point3d6.smethod_167(self.method_38(point3d9, num6, point3d6, percent1, percent, True)));
                            point3d7 = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, num7 + num17, 100), point3d16, point3d17);
                            point3dCollection_4.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                            point3dCollection_3.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                        else:
                            point3dCollection_4.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                            point3dCollection_3.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                            point3d7 = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, num7 + 1.5707963267949, 100), point3d16, point3d17);
                            point3dCollection_4.append(point3d6.smethod_167(self.method_38(point3d9, num6, point3d6, percent1, percent, False)));
                            point3dCollection_3.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                        point3d7 = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, num7 + num17, 100), point3d18, point3d19);
                        point3dCollection_4.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, False)));
                        point3d7 = MathHelper.getIntersectionPoint(point3d7, MathHelper.distanceBearingPoint(point3d7, num7 + 1.5707963267949, 100), point3d16, point3d17);
                        point3dCollection_3.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                    else:
                        point3d6 = MathHelper.distanceBearingPoint(point3dCollection_4[0], num7 + num17, 100);
                        point3d7 = MathHelper.getIntersectionPoint(point3dCollection_4[0], point3d6, point3d16, point3d17);
                        point3d8 = MathHelper.getIntersectionPoint(point3dCollection_4[0], point3d6, point3d18, point3d19);
                        point3dCollection_4.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                        point3dCollection_3.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                        point3d7 = MathHelper.getIntersectionPoint(point3d8, MathHelper.distanceBearingPoint(point3d8, num7 + 1.5707963267949, 100), point3d16, point3d17);
                        point3dCollection_4.append(point3d8.smethod_167(self.method_38(point3d9, num6, point3d8, percent1, percent, False)));
                        point3dCollection_3.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));

                else:
                    point3d6 = MathHelper.distanceBearingPoint(point3dCollection_4[0], num7 + num17, 100);
                    point3d7 = MathHelper.getIntersectionPoint(point3dCollection_4[0], point3d6, point3d16, point3d17);
                    point3d8 = MathHelper.getIntersectionPoint(point3dCollection_4[0], point3d6, point3d18, point3d19);
                    point3dCollection_4.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                    point3dCollection_3.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                    point3d7 = MathHelper.getIntersectionPoint(point3d8, MathHelper.distanceBearingPoint(point3d8, num7 - 1.5707963267949, 100), point3d16, point3d17);
                    point3dCollection_4.append(point3d8.smethod_167(self.method_38(point3d9, num6, point3d8, percent1, percent, False)));
                    point3dCollection_3.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                    point3d6 = MathHelper.distanceBearingPoint(point3dCollection_1[0], num6 - num17, num4 / math.cos(num17));
                    point3d7 = MathHelper.getIntersectionPoint(point3dCollection_1[0], point3d6, point3d12, point3d13);
                    if (MathHelper.calcDistance(point3dCollection_1[0], point3d6) <= MathHelper.calcDistance(point3dCollection_1[0], point3d7)):
                        point3dCollection_1.Add(point3d6.smethod_167(self.method_38(point3d9, num6, point3d6, percent1, percent, True)));
                        point3dCollection_2.Add(point3d6.smethod_167(self.method_38(point3d9, num6, point3d6, percent1, percent, True)));
                        point3d7 = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, num7 - num17, 100), point3d12, point3d13);
                        point3dCollection_1.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                        point3dCollection_2.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                    else:
                        point3dCollection_1.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                        point3dCollection_2.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                        point3d7 = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, num7 - 1.5707963267949, 100), point3d12, point3d13);
                        point3dCollection_1.append(point3d6.smethod_167(self.method_38(point3d9, num6, point3d6, percent1, percent, False)));
                        point3dCollection_2.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                    point3d7 = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, num7 - num17, 100), point3d14, point3d15);
                    point3dCollection_1.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, False)));
                    point3d7 = MathHelper.getIntersectionPoint(point3d7, MathHelper.distanceBearingPoint(point3d7, num7 - 1.5707963267949, 100), point3d12, point3d13);
                    point3dCollection_2.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
            else:
                point3d6 = MathHelper.distanceBearingPoint(point3dCollection_1[0], num7 - num17, 100);
                point3d7 = MathHelper.getIntersectionPoint(point3dCollection_1[0], point3d6, point3d12, point3d13);
                point3d8 = MathHelper.getIntersectionPoint(point3dCollection_1[0], point3d6, point3d14, point3d15);
                point3dCollection_1.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                point3dCollection_2.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                point3d7 = MathHelper.getIntersectionPoint(point3d8, MathHelper.distanceBearingPoint(point3d8, num7 + 1.5707963267949, 100), point3d12, point3d13);
                point3dCollection_1.append(point3d8.smethod_167(self.method_38(point3d9, num6, point3d8, percent1, percent, False)));
                point3dCollection_2.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                if (turnDirection != TurnDirection.Nothing):
                    point3d6 = MathHelper.distanceBearingPoint(point3dCollection_4[0], num6 + num17, num4 / math.cos(num17));
                    point3d7 = MathHelper.getIntersectionPoint(point3dCollection_4[0], point3d6, point3d16, point3d17);
                    if (MathHelper.calcDistance(point3dCollection_4[0], point3d6) <= MathHelper.calcDistance(point3dCollection_4[0], point3d7)):
                        point3dCollection_4.append(point3d6.smethod_167(self.method_38(point3d9, num6, point3d6, percent1, percent, True)));
                        point3dCollection_3.append(point3d6.smethod_167(self.method_38(point3d9, num6, point3d6, percent1, percent, True)));
                        point3d7 = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, num7 + num17, 100), point3d16, point3d17);
                        point3dCollection_4.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                        point3dCollection_3.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                    else:
                        point3dCollection_4.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                        point3dCollection_3.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                        point3d7 = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, num7 + 1.5707963267949, 100), point3d16, point3d17);
                        point3dCollection_4.append(point3d6.smethod_167(self.method_38(point3d9, num6, point3d6, percent1, percent, False)));
                        point3dCollection_3.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                    point3d7 = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, num7 + num17, 100), point3d18, point3d19);
                    point3dCollection_4.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, False)));
                    point3d7 = MathHelper.getIntersectionPoint(point3d7, MathHelper.distanceBearingPoint(point3d7, num7 + 1.5707963267949, 100), point3d16, point3d17);
                    point3dCollection_3.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                else:
                    point3d6 = MathHelper.distanceBearingPoint(point3dCollection_4[0], num7 + num17, 100);
                    point3d7 = MathHelper.getIntersectionPoint(point3dCollection_4[0], point3d6, point3d16, point3d17);
                    point3d8 = MathHelper.getIntersectionPoint(point3dCollection_4[0], point3d6, point3d18, point3d19);
                    point3dCollection_4.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                    point3dCollection_3.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));
                    point3d7 = MathHelper.getIntersectionPoint(point3d8, MathHelper.distanceBearingPoint(point3d8, num7 + 1.5707963267949, 100), point3d16, point3d17);
                    point3dCollection_4.append(point3d8.smethod_167(self.method_38(point3d9, num6, point3d8, percent1, percent, False)));
                    point3dCollection_3.append(point3d7.smethod_167(self.method_38(point3d9, num6, point3d7, percent1, percent, True)));

#         Label4:
#         Label0:
            point3d6 = MathHelper.distanceBearingPoint(point3dCollection_1[len(point3dCollection_1) - 1], MathHelper.getBearing(point3d14, point3d15), MathHelper.calcDistance(point3d14, point3d15));
            point3dCollection_1.append(point3d6.smethod_167(self.method_38(point3d9, num6, point3d6, percent1, percent, False)));
            point3d6 = MathHelper.distanceBearingPoint(point3dCollection_2[len(point3dCollection_2) - 1], MathHelper.getBearing(point3d12, point3d13), MathHelper.calcDistance(point3d12, point3d13));
            point3dCollection_2.append(point3d6.smethod_167(self.method_38(point3d9, num6, point3d6, percent1, percent, True)));
            point3d6 = MathHelper.distanceBearingPoint(point3dCollection_4[len(point3dCollection_4) - 1], MathHelper.getBearing(point3d18, point3d19), MathHelper.calcDistance(point3d18, point3d19));
            point3dCollection_4.append(point3d6.smethod_167(self.method_38(point3d9, num6, point3d6, percent1, percent, False)));
            point3d6 = MathHelper.distanceBearingPoint(point3dCollection_3[len(point3dCollection_3) - 1], MathHelper.getBearing(point3d16, point3d17), MathHelper.calcDistance(point3d16, point3d17));
            point3dCollection_3.append(point3d6.smethod_167(self.method_38(point3d9, num6, point3d6, percent1, percent, True)));
        else:
            # if rnavSpecification == RnavSpecification.Rnav5:
            #     rnavSpecification = RnavSpecification.Rnav2
            rnavGnssTolerance = RnavGnssTolerance(rnavSpecification, RnavGnssFlightPhase.Sid15, None, aircraftSpeedCategory);
            self.resultRnavTolerance = RnavGnssTolerance(rnavSpecification, RnavGnssFlightPhase.Sid15, None, aircraftSpeedCategory)
            metres = rnavGnssTolerance.ASW.Metres;
            metres1 = rnavGnssTolerance.ATT.Metres;
            rnavGnssTolerance = RnavGnssTolerance(rnavSpecification, RnavGnssFlightPhase.Star30Sid30IfIafMa30, None, aircraftSpeedCategory);
            metres2 = rnavGnssTolerance.ASW.Metres;
            metres3 = rnavGnssTolerance.ATT.Metres;
            rnavGnssTolerance = RnavGnssTolerance(rnavSpecification, RnavGnssFlightPhase.StarSid, None, aircraftSpeedCategory);
            metres4 = rnavGnssTolerance.ASW.Metres;
            metres5 = rnavGnssTolerance.ATT.Metres;
            point3d0_1 = []
            MathHelper.smethod_34(point3d9, point3d11, point3d10, num8, point3d0_1);
            point3d = point3d0_1[0]
            point3d1 = point3d0_1[1]
            point3d2 = point3d1  if (not MathHelper.smethod_135(num7, MathHelper.getBearing(point3d9, point3d), Unit.ConvertDegToRad(5), AngleUnits.Radians)) else point3d;
            point3d0_1 = []
            MathHelper.smethod_34(point3d9, point3d11, point3d10, num9, point3d0_1);
            point3d = point3d0_1[0]
            point3d1 = point3d0_1[1]
            point3d3 = point3d1 if (not MathHelper.smethod_135(num7, MathHelper.getBearing(point3d9, point3d), Unit.ConvertDegToRad(5), AngleUnits.Radians)) else point3d;
            if (turnDirection != TurnDirection.Nothing):
                if (turnDirection == TurnDirection.Left):
                    pass
#                     goto Label5;
#                 }
                else:
                    point3d20 = MathHelper.distanceBearingPoint(point3dCollection_1[0], num6 - num17, num4 / math.cos(num17));
                    point3d21 = MathHelper.distanceBearingPoint(point3d9, num12, metres / 2);
                    point3d22 = MathHelper.distanceBearingPoint(point3d11, num12, metres / 2);
                    point3d5 = MathHelper.getIntersectionPoint(point3dCollection_1[0], point3d20, point3d21, point3d22);
                    if (MathHelper.calcDistance(point3dCollection_1[0], point3d20) <= MathHelper.calcDistance(point3dCollection_1[0], point3d5)):
                        point3dCollection_1.append(point3d20.smethod_167(self.method_38(point3d9, num6, point3d20, percent1, percent, False)));
                        point3dCollection_2.append(point3d20.smethod_167(self.method_38(point3d9, num6, point3d20, percent1, percent, True)));
                        point3d5 = MathHelper.getIntersectionPoint(point3d20, MathHelper.distanceBearingPoint(point3d20, num7 - num17, 1000), point3d21, point3d22);
                        if (not point3d20.smethod_170(point3d5)):
                            point3dCollection_1.append(point3d5.smethod_167(self.method_38(point3d9, num6, point3d5, percent1, percent, True)));
                            point3dCollection_2.append(point3d5.smethod_167(self.method_38(point3d9, num6, point3d5, percent1, percent, True)));
                    else:
                        point3dCollection_1.append(point3d5.smethod_167(self.method_38(point3d9, num6, point3d5, percent1, percent, True)));
                        point3dCollection_2.append(point3d5.smethod_167(self.method_38(point3d9, num6, point3d5, percent1, percent, True)));
                        point3d5 = MathHelper.getIntersectionPoint(point3d21, point3d22, point3d20, MathHelper.distanceBearingPoint(point3d20, num13, 100));
                        point3dCollection_1.append(point3d20.smethod_167(self.method_38(point3d9, num6, point3d20, percent1, percent, False)));
                        point3dCollection_2.append(point3d5.smethod_167(self.method_38(point3d9, num6, point3d5, percent1, percent, True)));
                    point3d21 = MathHelper.distanceBearingPoint(point3d9, num12, metres);
                    point3d22 = MathHelper.distanceBearingPoint(point3d11, num12, metres);
                    point3d5 = MathHelper.getIntersectionPoint(point3d20, MathHelper.distanceBearingPoint(point3d20, num7 - num17, 1000), point3d21, point3d22);
                    point3dCollection_1.append(point3d5.smethod_167(self.method_38(point3d9, num6, point3d5, percent1, percent, False)));
                    point3d20 = MathHelper.distanceBearingPoint(point3d5, num13, metres / 2);
                    point3dCollection_2.append(point3d20.smethod_167(self.method_38(point3d9, num6, point3d20, percent1, percent, True)));
                    point3d20 = MathHelper.distanceBearingPoint(point3d2, num14, metres1);
                    point3d21 = MathHelper.distanceBearingPoint(point3d20, num12, metres);
                    point3d22 = MathHelper.distanceBearingPoint(point3d20, num12, metres / 2);
                    point3dCollection_1.append(point3d21.smethod_167(self.method_38(point3d9, num6, point3d21, percent1, percent, False)));
                    point3dCollection_2.append(point3d22.smethod_167(self.method_38(point3d9, num6, point3d22, percent1, percent, True)));
                    point3d21 = MathHelper.distanceBearingPoint(point3d21, num7 - num17, (metres2 - metres) / math.sin(num17));
                    point3d22 = MathHelper.distanceBearingPoint(point3d21, num13, metres2 / 2);
                    point3dCollection_1.append(point3d21.smethod_167(self.method_38(point3d9, num6, point3d21, percent1, percent, False)));
                    point3dCollection_2.append(point3d22.smethod_167(self.method_38(point3d9, num6, point3d22, percent1, percent, True)));
                    point3d20 = MathHelper.distanceBearingPoint(point3d3, num14, metres3);
                    point3d21 = MathHelper.distanceBearingPoint(point3d20, num12, metres2);
                    point3d22 = MathHelper.distanceBearingPoint(point3d20, num12, metres2 / 2);
                    point3dCollection_1.append(point3d21.smethod_167(self.method_38(point3d9, num6, point3d21, percent1, percent, False)));
                    point3dCollection_2.append(point3d22.smethod_167(self.method_38(point3d9, num6, point3d22, percent1, percent, True)));
                    point3d21 = MathHelper.distanceBearingPoint(point3d21, num7 - num17, (metres4 - metres2) / math.sin(num17));
                    point3d22 = MathHelper.distanceBearingPoint(point3d21, num13, metres4 / 2);
                    point3dCollection_1.append(point3d21.smethod_167(self.method_38(point3d9, num6, point3d21, percent1, percent, False)));
                    point3dCollection_2.append(point3d22.smethod_167(self.method_38(point3d9, num6, point3d22, percent1, percent, True)));
                    point3d21 = MathHelper.distanceBearingPoint(point3d21, num7, 5000);
                    point3d22 = MathHelper.distanceBearingPoint(point3d22, num7, 5000);
                    point3dCollection_1.append(point3d21.smethod_167(self.method_38(point3d9, num6, point3d21, percent1, percent, False)));
                    point3dCollection_2.append(point3d22.smethod_167(self.method_38(point3d9, num6, point3d22, percent1, percent, True)));
                    point3d23 = MathHelper.distanceBearingPoint(point3dCollection_4[0], num7 + num17, (metres / 2 - num18) / math.sin(num17));
                    point3d22 = point3d23;
                    point3d21 = point3d23;
                    point3dCollection_4.append(point3d21.smethod_167(self.method_38(point3d9, num6, point3d21, percent1, percent, True)));
                    point3dCollection_3.append(point3d22.smethod_167(self.method_38(point3d9, num6, point3d22, percent1, percent, True)));
                    point3d21 = MathHelper.distanceBearingPoint(point3dCollection_4[0], num7 + num17, (metres - num18) / math.sin(num17));
                    point3d22 = MathHelper.distanceBearingPoint(point3d21, num12, metres / 2);
                    point3dCollection_4.append(point3d21.smethod_167(self.method_38(point3d9, num6, point3d21, percent1, percent, False)));
                    point3dCollection_3.append(point3d22.smethod_167(self.method_38(point3d9, num6, point3d22, percent1, percent, True)));
                    point3d20 = MathHelper.distanceBearingPoint(point3d2, num14, metres1);
                    point3d21 = MathHelper.distanceBearingPoint(point3d20, num13, metres);
                    point3d22 = MathHelper.distanceBearingPoint(point3d20, num13, metres / 2);
                    point3dCollection_4.append(point3d21.smethod_167(self.method_38(point3d9, num6, point3d21, percent1, percent, False)));
                    point3dCollection_3.append(point3d22.smethod_167(self.method_38(point3d9, num6, point3d22, percent1, percent, True)));
                    point3d21 = MathHelper.distanceBearingPoint(point3d21, num7 + num17, (metres2 - metres) / math.sin(num17));
                    point3d22 = MathHelper.distanceBearingPoint(point3d21, num12, metres2 / 2);
                    point3dCollection_4.append(point3d21.smethod_167(self.method_38(point3d9, num6, point3d21, percent1, percent, False)));
                    point3dCollection_3.append(point3d22.smethod_167(self.method_38(point3d9, num6, point3d22, percent1, percent, True)));
                    point3d20 = MathHelper.distanceBearingPoint(point3d3, num14, metres3);
                    point3d21 = MathHelper.distanceBearingPoint(point3d20, num13, metres2);
                    point3d22 = MathHelper.distanceBearingPoint(point3d20, num13, metres2 / 2);
                    point3dCollection_4.append(point3d21.smethod_167(self.method_38(point3d9, num6, point3d21, percent1, percent, False)));
                    point3dCollection_3.append(point3d22.smethod_167(self.method_38(point3d9, num6, point3d22, percent1, percent, True)));
                    point3d21 = MathHelper.distanceBearingPoint(point3d21, num7 + num17, (metres4 - metres2) / math.sin(num17));
                    point3d22 = MathHelper.distanceBearingPoint(point3d21, num12, metres4 / 2);
                    point3dCollection_4.append(point3d21.smethod_167(self.method_38(point3d9, num6, point3d21, percent1, percent, False)));
                    point3dCollection_3.append(point3d22.smethod_167(self.method_38(point3d9, num6, point3d22, percent1, percent, True)));
                    point3d21 = MathHelper.distanceBearingPoint(point3d21, num7, 5000);
                    point3d22 = MathHelper.distanceBearingPoint(point3d22, num7, 5000);
                    point3dCollection_4.append(point3d21.smethod_167(self.method_38(point3d9, num6, point3d21, percent1, percent, False)));
                    point3dCollection_3.append(point3d22.smethod_167(self.method_38(point3d9, num6, point3d22, percent1, percent, True)));
                    self.method_39(point3dCollection_1, point3d9, point3d11, num6, percent1, percent, False);
                    self.method_39(point3dCollection_2, point3d9, point3d11, num6, percent1, percent, True);
                    self.method_39(point3dCollection_3, point3d9, point3d11, num6, percent1, percent, True);
                    self.method_39(point3dCollection_4, point3d9, point3d11, num6, percent1, percent, False);
                    point3dCollection_0.extend(point3dCollection_1);
#                     point3dCollection_4.reverse()
                    point3dCollection_0.extend(point3dCollection_4);
                    num = point3dCollection_5.append(point3d9.smethod_167(point3d9.get_Z() + 5));
                    num1 = point3dCollection_5.append(point3d11.smethod_167(self.method_38(point3d9, num6, point3d11, percent1, percent, False)));
                    num2 = point3dCollection_5.append(point3d11.smethod_167(self.method_38(point3d9, num6, point3d11, percent1, percent, True)));
                    num3 = point3dCollection_5.append(point3d9.smethod_167(point3d9.get_Z() + 5));
                    return (True, point3dCollection_0, point3dCollection_1, point3dCollection_2, point3dCollection_3, point3dCollection_4, point3dCollection_5);
#         Label5:
            point3d24 = MathHelper.distanceBearingPoint(point3dCollection_1[0], num7 - num17, (metres / 2 - num18) / math.sin(num17));
            point3d25 = point3d24;
            point3d26 = point3d24;
            point3dCollection_1.append(point3d26.smethod_167(self.method_38(point3d9, num6, point3d26, percent1, percent, True)));
            point3dCollection_2.append(point3d25.smethod_167(self.method_38(point3d9, num6, point3d25, percent1, percent, True)));
            point3d26 = MathHelper.distanceBearingPoint(point3dCollection_1[0], num7 - num17, (metres - num18) / math.sin(num17));
            point3d25 = MathHelper.distanceBearingPoint(point3d26, num13, metres / 2);
            point3dCollection_1.append(point3d26.smethod_167(self.method_38(point3d9, num6, point3d26, percent1, percent, False)));
            point3dCollection_2.append(point3d25.smethod_167(self.method_38(point3d9, num6, point3d25, percent1, percent, True)));
            point3d27 = MathHelper.distanceBearingPoint(point3d2, num14, metres1);
            point3d26 = MathHelper.distanceBearingPoint(point3d27, num12, metres);
            point3d25 = MathHelper.distanceBearingPoint(point3d27, num12, metres / 2);
            point3dCollection_1.append(point3d26.smethod_167(self.method_38(point3d9, num6, point3d26, percent1, percent, False)));
            point3dCollection_2.append(point3d25.smethod_167(self.method_38(point3d9, num6, point3d25, percent1, percent, True)));
            point3d26 = MathHelper.distanceBearingPoint(point3d26, num7 - num17, (metres2 - metres) / math.sin(num17));
            point3d25 = MathHelper.distanceBearingPoint(point3d26, num13, metres2 / 2);
            point3dCollection_1.append(point3d26.smethod_167(self.method_38(point3d9, num6, point3d26, percent1, percent, False)));
            point3dCollection_2.append(point3d25.smethod_167(self.method_38(point3d9, num6, point3d25, percent1, percent, True)));
            point3d27 = MathHelper.distanceBearingPoint(point3d3, num14, metres3);
            point3d26 = MathHelper.distanceBearingPoint(point3d27, num12, metres2);
            point3d25 = MathHelper.distanceBearingPoint(point3d27, num12, metres2 / 2);
            point3dCollection_1.append(point3d26.smethod_167(self.method_38(point3d9, num6, point3d26, percent1, percent, False)));
            point3dCollection_2.append(point3d25.smethod_167(self.method_38(point3d9, num6, point3d25, percent1, percent, True)));
            point3d26 = MathHelper.distanceBearingPoint(point3d26, num7 - num17, (metres4 - metres2) / math.sin(num17));
            point3d25 = MathHelper.distanceBearingPoint(point3d26, num13, metres4 / 2);
            point3dCollection_1.append(point3d26.smethod_167(self.method_38(point3d9, num6, point3d26, percent1, percent, False)));
            point3dCollection_2.append(point3d25.smethod_167(self.method_38(point3d9, num6, point3d25, percent1, percent, True)));
            point3d26 = MathHelper.distanceBearingPoint(point3d26, num7, 5000);
            point3d25 = MathHelper.distanceBearingPoint(point3d25, num7, 5000);
            point3dCollection_1.append(point3d26.smethod_167(self.method_38(point3d9, num6, point3d26, percent1, percent, False)));
            point3dCollection_2.append(point3d25.smethod_167(self.method_38(point3d9, num6, point3d25, percent1, percent, True)));
            if (turnDirection != TurnDirection.Nothing):
                point3d27 = MathHelper.distanceBearingPoint(point3dCollection_4[0], num6 + num17, num4 / math.cos(num17));
                point3d26 = MathHelper.distanceBearingPoint(point3d9, num13, metres / 2);
                point3d25 = MathHelper.distanceBearingPoint(point3d11, num13, metres / 2);
                point3d4 = MathHelper.getIntersectionPoint(point3dCollection_4[0], point3d27, point3d26, point3d25);
                if (MathHelper.calcDistance(point3dCollection_4[0], point3d27) <= MathHelper.calcDistance(point3dCollection_4[0], point3d4)):
                    point3dCollection_4.append(point3d27.smethod_167(self.method_38(point3d9, num6, point3d27, percent1, percent, False)));
                    point3dCollection_3.append(point3d27.smethod_167(self.method_38(point3d9, num6, point3d27, percent1, percent, True)));
                    point3d4 = MathHelper.getIntersectionPoint(point3d27, MathHelper.distanceBearingPoint(point3d27, num7 + num17, 1000), point3d26, point3d25);
                    if (not point3d27.smethod_170(point3d4)):
                        point3dCollection_4.append(point3d4.smethod_167(self.method_38(point3d9, num6, point3d4, percent1, percent, True)));
                        point3dCollection_3.append(point3d4.smethod_167(self.method_38(point3d9, num6, point3d4, percent1, percent, True)));
                else:
                    point3dCollection_4.append(point3d4.smethod_167(self.method_38(point3d9, num6, point3d4, percent1, percent, True)));
                    point3dCollection_3.append(point3d4.smethod_167(self.method_38(point3d9, num6, point3d4, percent1, percent, True)));
                    point3d4 = MathHelper.getIntersectionPoint(point3d26, point3d25, point3d27, MathHelper.distanceBearingPoint(point3d27, num12, 100));
                    point3dCollection_4.append(point3d27.smethod_167(self.method_38(point3d9, num6, point3d27, percent1, percent, False)));
                    point3dCollection_3.append(point3d4.smethod_167(self.method_38(point3d9, num6, point3d4, percent1, percent, True)));
                point3d26 = MathHelper.distanceBearingPoint(point3d9, num13, metres);
                point3d25 = MathHelper.distanceBearingPoint(point3d11, num13, metres);
                point3d4 = MathHelper.getIntersectionPoint(point3d27, MathHelper.distanceBearingPoint(point3d27, num7 + num17, 1000), point3d26, point3d25);
                point3dCollection_4.append(point3d4.smethod_167(self.method_38(point3d9, num6, point3d4, percent1, percent, False)));
                point3d27 = MathHelper.distanceBearingPoint(point3d4, num12, metres / 2);
                point3dCollection_3.append(point3d27.smethod_167(self.method_38(point3d9, num6, point3d27, percent1, percent, True)));
            else:
                point3d28 = MathHelper.distanceBearingPoint(point3dCollection_4[0], num7 + num17, (metres / 2 - num18) / math.sin(num17));
                point3d25 = point3d28;
                point3d26 = point3d28;
                point3dCollection_4.append(point3d26.smethod_167(self.method_38(point3d9, num6, point3d26, percent1, percent, True)));
                point3dCollection_3.append(point3d25.smethod_167(self.method_38(point3d9, num6, point3d25, percent1, percent, True)));
                point3d26 = MathHelper.distanceBearingPoint(point3dCollection_4[0], num7 + num17, (metres - num18) / math.sin(num17));
                point3d25 = MathHelper.distanceBearingPoint(point3d26, num12, metres / 2);
                point3dCollection_4.append(point3d26.smethod_167(self.method_38(point3d9, num6, point3d26, percent1, percent, False)));
                point3dCollection_3.append(point3d25.smethod_167(self.method_38(point3d9, num6, point3d25, percent1, percent, True)));
            point3d27 = MathHelper.distanceBearingPoint(point3d2, num14, metres1);
            point3d26 = MathHelper.distanceBearingPoint(point3d27, num13, metres);
            point3d25 = MathHelper.distanceBearingPoint(point3d27, num13, metres / 2);
            point3dCollection_4.append(point3d26.smethod_167(self.method_38(point3d9, num6, point3d26, percent1, percent, False)));
            point3dCollection_3.append(point3d25.smethod_167(self.method_38(point3d9, num6, point3d25, percent1, percent, True)));
            point3d26 = MathHelper.distanceBearingPoint(point3d26, num7 + num17, (metres2 - metres) / math.sin(num17));
            point3d25 = MathHelper.distanceBearingPoint(point3d26, num12, metres2 / 2);
            point3dCollection_4.append(point3d26.smethod_167(self.method_38(point3d9, num6, point3d26, percent1, percent, False)));
            point3dCollection_3.append(point3d25.smethod_167(self.method_38(point3d9, num6, point3d25, percent1, percent, True)));
            point3d27 = MathHelper.distanceBearingPoint(point3d3, num14, metres3);
            point3d26 = MathHelper.distanceBearingPoint(point3d27, num13, metres2);
            point3d25 = MathHelper.distanceBearingPoint(point3d27, num13, metres2 / 2);
            point3dCollection_4.append(point3d26.smethod_167(self.method_38(point3d9, num6, point3d26, percent1, percent, False)));
            point3dCollection_3.append(point3d25.smethod_167(self.method_38(point3d9, num6, point3d25, percent1, percent, True)));
            point3d26 = MathHelper.distanceBearingPoint(point3d26, num7 + num17, (metres4 - metres2) / math.sin(num17));
            point3d25 = MathHelper.distanceBearingPoint(point3d26, num12, metres4 / 2);
            point3dCollection_4.append(point3d26.smethod_167(self.method_38(point3d9, num6, point3d26, percent1, percent, False)));
            point3dCollection_3.append(point3d25.smethod_167(self.method_38(point3d9, num6, point3d25, percent1, percent, True)));
            point3d26 = MathHelper.distanceBearingPoint(point3d26, num7, 5000);
            point3d25 = MathHelper.distanceBearingPoint(point3d25, num7, 5000);
            point3dCollection_4.append(point3d26.smethod_167(self.method_38(point3d9, num6, point3d26, percent1, percent, False)));
            point3dCollection_3.append(point3d25.smethod_167(self.method_38(point3d9, num6, point3d25, percent1, percent, True)));
        self.method_39(point3dCollection_1, point3d9, point3d11, num6, percent1, percent, False);
        self.method_39(point3dCollection_2, point3d9, point3d11, num6, percent1, percent, True);
        self.method_39(point3dCollection_3, point3d9, point3d11, num6, percent1, percent, True);
        self.method_39(point3dCollection_4, point3d9, point3d11, num6, percent1, percent, False);
        point3dCollection_0.extend(point3dCollection_1);
#         point3dCollection_4.reverse()
        point3dCollection_0.extend(point3dCollection_4);
        num = point3dCollection_5.append(point3d9.smethod_167(point3d9.get_Z() + 5));
        num1 = point3dCollection_5.append(point3d11.smethod_167(self.method_38(point3d9, num6, point3d11, percent1, percent, False)));
        num2 = point3dCollection_5.append(point3d11.smethod_167(self.method_38(point3d9, num6, point3d11, percent1, percent, True)));
        num3 = point3dCollection_5.append(point3d9.smethod_167(point3d9.get_Z() + 5));
        return (True, point3dCollection_0, point3dCollection_1, point3dCollection_2, point3dCollection_3, point3dCollection_4, point3dCollection_5);
    def method_38(self, point3d_0, double_0, point3d_1, double_1, double_2, bool_0):
        point3d = None;
        point3d = MathHelper.getIntersectionPoint(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_0, 1000), point3d_1, MathHelper.distanceBearingPoint(point3d_1, double_0 + 1.5707963267949, 1000));
        num = MathHelper.calcDistance(point3d_0, point3d);
        if (not bool_0):
            return point3d_0.get_Z() + 5 + num * double_1;
        return point3d_0.get_Z() + 5 + num * (double_1 - double_2);
    def method_39(self, point3dCollection_0, point3d_0, point3d_1, double_0, double_1, double_2, bool_0):
        point3d = None;
        num = 0;
        num1 = 1;
        num2 = MathHelper.getBearing(point3d_0, point3d_1) - 1.5707963267949;
        num3 = MathHelper.calcDistance(point3d_0, point3d_1);

        for i in range(1, len(point3dCollection_0)):
            num = i - 1;
            num1 = i;
            point3d = MathHelper.getIntersectionPoint(point3d_0, point3d_1, point3dCollection_0[num1], MathHelper.distanceBearingPoint(point3dCollection_0[num1], num2, 1000));
            num4 = MathHelper.calcDistance(point3d_0, point3d);
            if (MathHelper.smethod_99(num3, num4, 0.0001) or num3 < num4):
                point3d = MathHelper.getIntersectionPoint(point3dCollection_0[num], point3dCollection_0[num1], point3d_1, MathHelper.distanceBearingPoint(point3d_1, num2, 1000));
                point3dCollection_0.insert(num1, point3d.smethod_167(self.method_38(point3d_0, double_0, point3d, double_1, double_2, bool_0)));
                num5 = num1 + 1;
                while (len(point3dCollection_0) > num5):
                    point3dCollection_0.remove(point3dCollection_0[num5]);
                return;
        point3d = MathHelper.getIntersectionPoint(point3dCollection_0[num], point3dCollection_0[num1], point3d_1, MathHelper.distanceBearingPoint(point3d_1, num2, 1000));
        point3dCollection_0.append(point3d.smethod_167(self.method_38(point3d_0, double_0, point3d, double_1, double_2, bool_0)));
    def nominal2Layer(self):
        resultLayer = AcadHelper.createVectorLayer("NominalTrack_" + self.surfaceType.replace(" ", "_").replace("-", "_"), QGis.Line)
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [self.parametersPanel.pnlRwyDir.Point3d, self.parametersPanel.pnlFirstWPt.Point3d])

        resultLayer.commitChanges()
        return resultLayer
class DepartureRnavObstacles(ObstacleTable):
    def __init__(self, point3d_0, double_0, double_1, double_2, complexObstacleArea_0):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, None)
        
        self.surfaceType = SurfaceTypes.DepartureRnav
        self.obstaclesChecked = None
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
        num = 1E-08  if (not MathHelper.smethod_99(MathHelper.getBearing(self.ptDER, point3d), self.track, 5)) else MathHelper.calcDistance(self.ptDER, point3d);
        mocMultiplier = self.moc / 100 * num * obstacle_0.MocMultiplier;
        num1 = 0;
        num2 = None;
        obstacleAreaResult, num1, num2 = self.area.pointInArea(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier);
#         if num1 == None:
#             num1 = 0.0
#         if num2 == None:
#             num2 = 0.0
        if obstacleAreaResult == None:
            return
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
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
