# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QSize, Qt
from PyQt4.QtGui import QColor, QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsCoordinateReferenceSystem,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, \
                QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, \
                QgsSymbolV2, QgsRendererCategoryV2, QgsGeometry
from qgis.core import QGis, QgsRectangle, QgsGeometry, QgsCsException, QgsPoint,\
        QgsFeatureRequest, QgsCoordinateTransform, QgsFeature, QgsVectorLayer
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapToolPan, QgsEllipseSymbolLayerV2Widget
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType, SurfaceTypes, \
                 DistanceUnits,AircraftSpeedCategory, OrientationType, AltitudeUnits, \
                 ObstacleAreaResult, RnavFlightPhase, ConstructionType, RnavSpecification, IntersectionStatus,\
                 TurnDirection,RnavDmeDmeFlightPhase, \
                    RnavDmeDmeCriteria, RnavSpecification, RnavGnssFlightPhase , ConstructionType, \
                    CloseInObstacleType
from FlightPlanner.RnavStraightSegmentAnalyser.ui_RnavStraightSegmentAnalyser import Ui_RnavStraightSegmentAnalyser
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.ProtectionAreaPanel import ProtectionAreaPanel
from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Holding.HoldingRnav.HoldingTemplateRnav import HoldingTemplateRnav
from FlightPlanner.Holding.HoldingTemplate import HoldingTemplate
from FlightPlanner.Panels.WindPanel import WindPanel
from FlightPlanner.Holding.HoldingTemplateBase import HoldingTemplateBase
from FlightPlanner.types import Point3D, Point3dCollection
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, ComplexObstacleArea, SecondaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.IasHelp.IasHelpDlg import IasHelpDlg
from FlightPlanner.messages import Messages
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.Holding.RnavVorDme.RnavVorDmeDlg import RnavVorDme
from FlightPlanner.Holding.RnavDmeDme.RnavDmeDmeDlg import RnavDmeDme
from FlightPlanner.RnavTolerance.RnavDmeDmeTolerance import RnavDmeDmeTolerance
from FlightPlanner.RnavTolerance.RnavGnssTolerance import RnavGnssTolerance

import define, math

class RnavStraightSegmentAnalyserDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("RnavStraightSegmentAnalyserDlg")
        self.surfaceType = SurfaceTypes.RnavStraightSegmentAnalyser
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.RnavStraightSegmentAnalyser)
        self.resize(600, 600)
        QgisHelper.matchingDialogSize(self, 600, 700)
        self.surfaceList = None
        self.manualPolygon = None
        self.mapToolPan = None
        self.toolSelectByPolygon = None
        self.lineBand = None
        
        self.accepted.connect(self.closed)
        self.rejected.connect(self.closed)
        
    def closed(self):
        if self.mapToolPan != None:
            self.mapToolPan.deactivate()
        if self.toolSelectByPolygon != None:
            self.toolSelectByPolygon.deactivate()
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
        parameterList.append(("RNAV Specification", self.parametersPanel.cmbRnavSpecification.currentText()))
        if self.parametersPanel.cmbRnavSpecification.currentIndex() == 0:
            parameterList.append(("ATT", self.parametersPanel.pnlTolerances.txtAtt.text() + "nm"))
            parameterList.append(("XTT", self.parametersPanel.pnlTolerances.txtXtt.text() + "nm"))
            parameterList.append(("1/2 A/W", self.parametersPanel.pnlTolerances.txtAsw.text() + "nm"))
        else:
            if self.parametersPanel.cmbPhaseOfFlight.currentIndex() == 0:
                parameterList.append(("Cat.H", str(self.parametersPanel.chbCatH.isChecked())))
            else:
                parameterList.append(("Cat.H", str(self.parametersPanel.chbCatH.isChecked())))
                parameterList.append(("Aerodrome Reference Point(ARP)", "group"))
                longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlArp.txtPointX.text()), float(self.parametersPanel.pnlArp.txtPointY.text()))
        
                parameterList.append(("Lat", self.parametersPanel.pnlArp.txtLat.Value))
                parameterList.append(("Lon", self.parametersPanel.pnlArp.txtLong.Value))
                parameterList.append(("X", self.parametersPanel.pnlArp.txtPointX.text()))
                parameterList.append(("Y", self.parametersPanel.pnlArp.txtPointY.text()))                                     
            
        parameterList.append(("Waypoint 1 Position", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlWaypoint1.txtPointX.text()), float(self.parametersPanel.pnlWaypoint1.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlWaypoint1.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlWaypoint1.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlWaypoint1.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlWaypoint1.txtPointY.text()))
        
        parameterList.append(("Waypoint 2 Position", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlWaypoint2.txtPointX.text()), float(self.parametersPanel.pnlWaypoint2.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlWaypoint2.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlWaypoint2.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlWaypoint2.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlWaypoint2.txtPointY.text()))
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Selection Mode", self.parametersPanel.cmbSelectionMode.currentText()))
        parameterList.append(("Altitude", self.parametersPanel.txtAltitude.text() + "ft"))
        parameterList.append(("Primary Moc", self.parametersPanel.txtPrimaryMoc.text() + "m"))
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstruct.currentText()))
        parameterList.append(("MOCmultipiler", str(self.parametersPanel.mocSpinBox.value())))
        if self.parametersPanel.cmbConstruct.currentIndex() == 0:            
            parameterList.append(("Draw Waypoint Tolerance", str(self.parametersPanel.chbDrawTolerance.isChecked())))

        parameterList.append(("Results", "group"))
        parameterList.append(("Waypoint 1", "group"))
        parameterList.append(("XTT", self.parametersPanel.txtXtt1D.text()))
        parameterList.append(("ATT", self.parametersPanel.txtAtt1D.text()))
        parameterList.append(("1/2 A/W", self.parametersPanel.txtAsw1D.text()))
        parameterList.append(("Waypoint 2", "group"))
        parameterList.append(("XTT", self.parametersPanel.txtXtt2D.text()))
        parameterList.append(("ATT", self.parametersPanel.txtAtt2D.text()))
        parameterList.append(("1/2 A/W", self.parametersPanel.txtAsw2D.text()))


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
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
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
        point3dCollection6 = None;
        selectedArea = None;
#         if (!AcadHelper.Ready)
#         {
#             return;
#         }
#         if (!self.method_27(false))
#         {
#             return;
#         }
#         if (self.pnlSelectionMode.Value == SelectionModeType.Manual && !self.pnlSelectionMode.method_0())
#         {
#             return;
#         }
#         try
#         {
        num = MathHelper.getBearing(self.parametersPanel.pnlWaypoint1.Point3d, self.parametersPanel.pnlWaypoint2.Point3d);
        result, point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, point3dCollection4, point3dCollection5, point3dCollection6 = self.method_38()
        if (result):
            flag = False if (self.parametersPanel.cmbRnavSpecification.currentIndex() <= 0 or self.parametersPanel.cmbPhaseOfFlight.currentIndex()) else self.phaseOfFlight == RnavFlightPhase.Enroute;
            complexObstacleArea = ComplexObstacleArea();
            polylineArea = PolylineArea();
            polylineArea1 = PolylineArea();
            polylineArea.method_5(point3dCollection);
            polylineArea1.method_5(point3dCollection1);
            if (flag):
                count = polylineArea.Count - 1;
                polylineArea[count].Bulge = MathHelper.smethod_57(TurnDirection.Right, point3dCollection.get_Item(count), point3dCollection3.get_Item(count), point3dCollection4.get_Item(1));
                polylineArea1[count].Bulge = MathHelper.smethod_57(TurnDirection.Right, point3dCollection1.get_Item(count), point3dCollection2.get_Item(count), point3dCollection4.get_Item(1));
            point3dCollection3.reverse()    
            polylineArea.method_5(point3dCollection3);
            point3dCollection2.reverse()
            polylineArea1.method_5(point3dCollection2);
            if (flag):
                count1 = polylineArea.Count - 1;
                polylineArea[count1].Bulge = MathHelper.smethod_57(TurnDirection.Right, point3dCollection3.get_Item(0), point3dCollection.get_Item(0), point3dCollection4.get_Item(0));
                polylineArea.method_1(point3dCollection.get_Item(0));
                polylineArea1[count1].Bulge = MathHelper.smethod_57(TurnDirection.Right, point3dCollection2.get_Item(0), point3dCollection1.get_Item(0), point3dCollection4.get_Item(0));
                polylineArea1.method_1(point3dCollection1.get_Item(0));
            complexObstacleArea.Add(PrimaryObstacleArea(polylineArea1));
            for i in range(1, point3dCollection1.get_Count()):
                if (not point3dCollection1.get_Item(i - 1).smethod_170(point3dCollection.get_Item(i - 1)) or not point3dCollection1.get_Item(i).smethod_170(point3dCollection.get_Item(i))):
                    complexObstacleArea.method_0(SecondaryObstacleArea(point3dCollection1.get_Item(i - 1), point3dCollection1.get_Item(i), point3dCollection.get_Item(i - 1), point3dCollection.get_Item(i)), num);
            for j in range(1, point3dCollection2.get_Count()):
                if (not point3dCollection2.get_Item(j - 1).smethod_170(point3dCollection3.get_Item(j - 1)) or not point3dCollection2.get_Item(j).smethod_170(point3dCollection3.get_Item(j))):
                    complexObstacleArea.method_0(SecondaryObstacleArea(point3dCollection2.get_Item(j - 1), point3dCollection2.get_Item(j), point3dCollection3.get_Item(j - 1), point3dCollection3.get_Item(j)), num);
            if (flag):
                num1 = MathHelper.calcDistance(point3dCollection4.get_Item(0), point3dCollection1.get_Item(0));
                num2 = MathHelper.calcDistance(point3dCollection4.get_Item(0), point3dCollection.get_Item(0));
                point3d = MathHelper.distanceBearingPoint(point3dCollection4.get_Item(0), num + 3.14159265358979, num1);
                point3d1 = MathHelper.distanceBearingPoint(point3dCollection4.get_Item(0), num + 3.14159265358979, num2);
                complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection2.get_Item(0), point3d, point3dCollection1.get_Item(0), point3dCollection3.get_Item(0), None, point3d1, point3dCollection.get_Item(0)));
                count2 = point3dCollection1.get_Count() - 1;
                point3d = MathHelper.distanceBearingPoint(point3dCollection4.get_Item(1), num, num1);
                point3d1 = MathHelper.distanceBearingPoint(point3dCollection4.get_Item(1), num, num2);
                complexObstacleArea.Add(SecondaryObstacleArea(point3dCollection1.get_Item(count2), point3d, point3dCollection2.get_Item(count2), point3dCollection.get_Item(count2), None, point3d1, point3dCollection3.get_Item(count2)));
                
            selectedArea = PrimaryObstacleArea(polylineArea);
            
            ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
            self.obstaclesModel = RnavStraightObstacles(complexObstacleArea, Altitude(float(self.parametersPanel.txtPrimaryMoc.text())), Altitude(float(self.parametersPanel.txtAltitude.text()),AltitudeUnits.FT), self.manualPolygon );
            
#             self.parametersPanel.frameAltitude.setE
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
        point3dCollection6 = None;
#         if (!AcadHelper.Ready)
#         {
#             return;
#         }
#         if (!self.method_27(true))
#         {
#             return;
#         }
        mapUnits = define._canvas.mapUnits()
        constructionLayer = None
        point3d = self.parametersPanel.pnlWaypoint1.Point3d;
        point3d1 = self.parametersPanel.pnlWaypoint2.Point3d;
        result, point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, point3dCollection4, point3dCollection5, point3dCollection6 = self.method_38()
        resultPoint3dArrayList = []
        if (result):
            flag = False if (self.parametersPanel.cmbRnavSpecification.currentIndex() <= 0 or self.parametersPanel.cmbPhaseOfFlight.currentIndex() < 0) else self.phaseOfFlight == 0;
#             if (self.parametersPanel.cmbConstruct.currentText() != ConstructionType.Construct2D):
#                 metres = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT).Metres - Altitude(float(self.parametersPanel.txtPrimaryMoc.text())).Metres;
#                 num = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT).Metres;
#                 for i in range(1, point3dCollection1.get_Count()):
#                     resultPoint3dArrayList.append([point3dCollection1.get_Item(i - 1).smethod_167(metres), point3dCollection1.get_Item(i).smethod_167(metres), point3dCollection2.get_Item(i).smethod_167(metres), point3dCollection2.get_Item(i - 1).smethod_167(metres)])
# #                     AcadHelper.method_18(transaction, blockTableRecord, new Face(point3dCollection1.get_Item(i - 1).smethod_167(metres), point3dCollection1.get_Item(i).smethod_167(metres), point3dCollection2.get_Item(i).smethod_167(metres), point3dCollection2.get_Item(i - 1).smethod_167(metres), true, true, true, true), constructionLayer);
#                 for j in range(1, point3dCollection1.get_Count()):
#                     resultPoint3dArrayList.append([point3dCollection1.get_Item(j - 1).smethod_167(metres), point3dCollection1.get_Item(j).smethod_167(metres), point3dCollection.get_Item(j).smethod_167(num), point3dCollection.get_Item(j - 1).smethod_167(num)])
# #                     AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3dCollection1.get_Item(j - 1).smethod_167(metres), point3dCollection1.get_Item(j).smethod_167(metres), point3dCollection.get_Item(j).smethod_167(num), point3dCollection.get_Item(j - 1).smethod_167(num), true, true, true, true), constructionLayer);
#                 for k in range(1, point3dCollection2.get_Count()):
#                     resultPoint3dArrayList.append([point3dCollection2.get_Item(k - 1).smethod_167(metres), point3dCollection2.get_Item(k).smethod_167(metres), point3dCollection3.get_Item(k).smethod_167(num), point3dCollection3.get_Item(k - 1).smethod_167(num)])
# #                     AcadHelper.smethod_18(transaction, blockTableRecord, new Face(point3dCollection2.get_Item(k - 1).smethod_167(metres), point3dCollection2.get_Item(k).smethod_167(metres), point3dCollection3.get_Item(k).smethod_167(num), point3dCollection3.get_Item(k - 1).smethod_167(num), true, true, true, true), constructionLayer);
#                 polyline = PolylineArea(point3dCollection4);
#                 resultPoint3dArrayList.append(point3dCollection4)
# #                 polyline.set_Elevation(num);
# #                 polyline.set_Thickness(-self.pnlPrimaryMoc.Value.Metres);
# #                 AcadHelper.smethod_18(transaction, blockTableRecord, polyline, constructionLayer);
#                 if (flag):
#                     num1 = MathHelper.calcDistance(point3dCollection4.get_Item(0), point3dCollection1.get_Item(0));
#                     num2 = MathHelper.calcDistance(point3dCollection4.get_Item(0), point3dCollection.get_Item(0));
#                     point3dCollection7 = MathHelper.smethod_137(point3dCollection2.get_Item(0), point3dCollection4.get_Item(0), num1, 3.14159265358979, 50, TurnDirection.Right);
#                     point3dCollection7.append(point3dCollection1.get_Item(0));
#                     point3dCollection8 = MathHelper.smethod_137(point3dCollection3.get_Item(0), point3dCollection4.get_Item(0), num2, 3.14159265358979, 50, TurnDirection.Right);
#                     point3dCollection8.Add(point3dCollection.get_Item(0));
#                     for l in range(point3dCollection7.get_Count()):
#                         point3dCollection7.set_Item(l, point3dCollection7.get_Item(l).smethod_167(metres));
#                     for m in range(point3dCollection8.get_Count()):
#                         point3dCollection8.set_Item(m, point3dCollection8.get_Item(m).smethod_167(num));
#                     polygon0, polygon1 = QgisHelper.smethod_147(point3dCollection7, point3dCollection8)
#                     pointArray = QgsGeometry.asPolygon(polygon0)
#                     resultPoint3dArrayList.append(pointArray[0])
#
#                     pointArray = QgsGeometry.asPolygon(polygon1)
#                     resultPoint3dArrayList.append(pointArray[0])
#
# #                     AcadHelper.smethod_147(transaction, blockTableRecord, point3dCollection7, point3dCollection8, constructionLayer);
#                     count = point3dCollection1.get_Count() - 1;
#                     point3dCollection7 = MathHelper.smethod_137(point3dCollection1.get_Item(count), point3dCollection4.get_Item(1), num1, 3.14159265358979, 50, TurnDirection.Right);
#                     point3dCollection7.Add(point3dCollection2.get_Item(count));
#                     point3dCollection8 = MathHelper.smethod_137(point3dCollection.get_Item(count), point3dCollection4.get_Item(1), num2, 3.14159265358979, 50, TurnDirection.Right);
#                     point3dCollection8.Add(point3dCollection3.get_Item(count));
#                     for n in range(point3dCollection7.get_Count()):
#                         point3dCollection7.set_Item(n, point3dCollection7.get_Item(n).smethod_167(metres));
#                     for o in range(point3dCollection8.get_Count()):
#                         point3dCollection8.set_Item(o, point3dCollection8.get_Item(o).smethod_167(num));
#                     polygon0, polygon1 = QgisHelper.smethod_147(point3dCollection7, point3dCollection8)
#                     pointArray = QgsGeometry.asPolygon(polygon0)
#                     resultPoint3dArrayList.append(pointArray[0])
#
#                     pointArray = QgsGeometry.asPolygon(polygon1)
#                     resultPoint3dArrayList.append(pointArray[0])
#
# #                     AcadHelper.smethod_147(transaction, blockTableRecord, point3dCollection7, point3dCollection8, constructionLayer);
#             else:
            count1 = point3dCollection1.get_Count() - 1;
            resultPoint3dArrayList.append(point3dCollection)
            resultPoint3dArrayList.append(point3dCollection1)
            resultPoint3dArrayList.append(point3dCollection2)
            resultPoint3dArrayList.append(point3dCollection3)
#                 AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_128(point3dCollection), constructionLayer);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_128(point3dCollection1), constructionLayer);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_128(point3dCollection2), constructionLayer);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_128(point3dCollection3), constructionLayer);
            if (not flag):
                item = [point3dCollection.get_Item(0), point3dCollection3.get_Item(0)];
                resultPoint3dArrayList.append(item)
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(item), constructionLayer);
                point3dArray = [point3dCollection.get_Item(count1), point3dCollection3.get_Item(count1)];
                resultPoint3dArrayList.append(point3dArray)
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(point3dArray), constructionLayer);
            else:
                polylineArea = PolylineArea();
                polylineArea.method_3(point3dCollection2.get_Item(0), -1)# MathHelper.smethod_57(TurnDirection.Right, point3dCollection2.get_Item(0), point3dCollection1.get_Item(0), point3dCollection4.get_Item(0)));
                polylineArea.method_1(point3dCollection1.get_Item(0));
                resultPoint3dArrayList.append(PolylineArea.smethod_131(polylineArea).method_14())
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_131(polylineArea), constructionLayer);
                polylineArea = PolylineArea();
                polylineArea.method_3(point3dCollection3.get_Item(0),-1)# MathHelper.smethod_57(TurnDirection.Right, point3dCollection3.get_Item(0), point3dCollection.get_Item(0), point3dCollection4.get_Item(0)));
                polylineArea.method_1(point3dCollection.get_Item(0));
                resultPoint3dArrayList.append(PolylineArea.smethod_131(polylineArea).method_14())
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_131(polylineArea), constructionLayer);
                polylineArea = PolylineArea();
                polylineArea.method_3(point3dCollection1.get_Item(count1), -1)#MathHelper.smethod_57(TurnDirection.Right, point3dCollection1.get_Item(count1), point3dCollection2.get_Item(count1), point3dCollection4.get_Item(1)));
                polylineArea.method_1(point3dCollection2.get_Item(count1));
                resultPoint3dArrayList.append(PolylineArea.smethod_131(polylineArea).method_14())
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_131(polylineArea), constructionLayer);
                polylineArea = PolylineArea();
                polylineArea.method_3(point3dCollection.get_Item(count1), -1)#MathHelper.smethod_57(TurnDirection.Right, point3dCollection.get_Item(count1), point3dCollection3.get_Item(count1), point3dCollection4.get_Item(1)));
                polylineArea.method_1(point3dCollection3.get_Item(count1));
                resultPoint3dArrayList.append(PolylineArea.smethod_131(polylineArea).method_14())
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_131(polylineArea), constructionLayer);
            resultPoint3dArrayList.append(point3dCollection4)
#                 AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_128(point3dCollection4), constructionLayer);
            if (self.parametersPanel.chbDrawTolerance.isChecked()):
                resultPoint3dArrayList.append(PolylineArea.smethod_133(point3dCollection5, True).method_14())
                resultPoint3dArrayList.append(PolylineArea.smethod_133(point3dCollection6, True).method_14())
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_133(point3dCollection5, true), constructionLayer);
#                     AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_133(point3dCollection6, true), constructionLayer);
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType)
            for pointArray in resultPoint3dArrayList:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, pointArray)

            wptLayer = AcadHelper.WPT2Layer(self.parametersPanel.pnlWaypoint1.Point3d, self.parametersPanel.pnlWaypoint2.Point3d, "WPT_" + self.surfaceType.replace(" ", "_").replace("-", "_"))
            resultLayers = [constructionLayer, wptLayer, self.nominal2Layer()]
            QgisHelper.appendToCanvas(define._canvas, resultLayers, self.surfaceType)
            QgisHelper.zoomToLayers(resultLayers)
            self.resultLayerList = resultLayers
            self.ui.btnEvaluate.setEnabled(True)
            self.manualEvent(self.parametersPanel.cmbSelectionMode.currentIndex())


    def initParametersPan(self):
        ui = Ui_RnavStraightSegmentAnalyser()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.gbResultsDME.setEnabled(False)
        self.parametersPanel.gbResultsVOR.setVisible(False)

        # self.parametersPanel.pnlProtect = ProtectionAreaPanel()
        # ui.vl_gbGeneral.addWidget(self.parametersPanel.pnlProtect)

        self.parametersPanel.pnlArp= PositionPanel(self.parametersPanel.gbGeneral)
        self.parametersPanel.pnlArp.groupBox.setTitle("Aerodrome Reference Point(ARP)")
        self.parametersPanel.pnlArp.btnCalculater.hide()
        self.parametersPanel.pnlArp.hideframe_Altitude()
        self.parametersPanel.pnlArp.setObjectName("pnlArp")
        ui.vl_gbGeneral.addWidget(self.parametersPanel.pnlArp)
        
        self.parametersPanel.pnlWaypoint1 = PositionPanel(self.parametersPanel.gbGeneral)
        self.parametersPanel.pnlWaypoint1.groupBox.setTitle("Waypoint 1")
        self.parametersPanel.pnlWaypoint1.btnCalculater.hide()
        self.parametersPanel.pnlWaypoint1.hideframe_Altitude()
        self.parametersPanel.pnlWaypoint1.setObjectName("pnlWaypoint1")
        ui.vl_gbGeneral.addWidget(self.parametersPanel.pnlWaypoint1)
        self.connect(self.parametersPanel.pnlWaypoint1, SIGNAL("positionChanged"), self.drawLineBand)
        
        self.parametersPanel.pnlWaypoint2 = PositionPanel(self.parametersPanel.gbGeneral)
        self.parametersPanel.pnlWaypoint2.groupBox.setTitle("Waypoint 2")
        self.parametersPanel.pnlWaypoint2.btnCalculater.hide()
        self.parametersPanel.pnlWaypoint2.hideframe_Altitude()
        self.parametersPanel.pnlWaypoint2.setObjectName("pnlWaypoint2")
        ui.vl_gbGeneral.addWidget(self.parametersPanel.pnlWaypoint2)
        self.connect(self.parametersPanel.pnlWaypoint2, SIGNAL("positionChanged"), self.drawLineBand)

        
        self.parametersPanel.pnlTolerances = RnavTolerancesPanel(self.parametersPanel.gbGeneral)
        self.parametersPanel.pnlTolerances.set_Att(Distance(0.8, DistanceUnits.NM))
        self.parametersPanel.pnlTolerances.set_Xtt(Distance(1, DistanceUnits.NM))
        self.parametersPanel.pnlTolerances.set_Asw(Distance(2, DistanceUnits.NM))
        ui.vl_gbGeneral.insertWidget(2, self.parametersPanel.pnlTolerances)
        self.connect(self.parametersPanel.pnlTolerances, SIGNAL("valueChanged()"), self.VorDmeShow)
               
        self.parametersPanel.cmbSelectionMode.addItems(["Automatic", "Manual"])
        self.parametersPanel.cmbSelectionMode.currentIndexChanged.connect(self.manualEvent)
        self.parametersPanel.cmbConstruct.addItems(["2D", "3D"])
        
        self.parametersPanel.cmbRnavSpecification.currentIndexChanged.connect(self.method_33)
        self.parametersPanel.cmbRnavSpecification.currentIndexChanged.connect(self.VorDmeShow)
        self.parametersPanel.cmbPhaseOfFlight.currentIndexChanged.connect(self.method_31)
        self.parametersPanel.cmbPhaseOfFlight.currentIndexChanged.connect(self.VorDmeShow)
        self.parametersPanel.cmbConstruct.currentIndexChanged.connect(self.method_31)

        self.parametersPanel.txtAltitude.textChanged.connect(self.VorDmeShow)

        self.parametersPanel.cmbRnavSpecification.addItems(["", "Rnav5", "Rnav2", "Rnav1", "Rnp4", "Rnp2", "Rnp1", "ARnp2", "ARnp1", "ARnp09", "ARnp08", "ARnp07", "ARnp06", "ARnp05", "ARnp04", "ARnp03", "RnpApch"])
#         self.parametersPanel.cmbRnavSpecification.addItems(["sdfa"])

        self.parametersPanel.txtAltitudeM.textChanged.connect(self.txtAltitudeMChanged)
        self.parametersPanel.txtAltitude.textChanged.connect(self.txtAltitudeFtChanged)

        self.flag = 0
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")


        self.parametersPanel.txtPrimaryMoc.textChanged.connect(self.txtMocMChanged)
        self.parametersPanel.txtPrimaryMocFt.textChanged.connect(self.txtMocFtChanged)
        self.flag1 = 0
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtPrimaryMocFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtPrimaryMoc.text())), 4)))
            except:
                self.parametersPanel.txtPrimaryMocFt.setText("0.0")
        self.method_31()

        self.VorDmeShow()
    def txtAltitudeMChanged(self):
        if self.flag==0:
            self.flag=1;
        if self.flag==2:
            self.flag=0;
        if self.flag==1:
            try:
                self.parametersPanel.txtAltitude.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAltitudeM.text())), 4)))
            except:
                self.parametersPanel.txtAltitude.setText("0.0")

    def txtAltitudeFtChanged(self):
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtAltitudeM.setText(str(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude.text()))))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")
    def txtMocMChanged(self):
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtPrimaryMocFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtPrimaryMoc.text())), 4)))
            except:
                self.parametersPanel.txtPrimaryMocFt.setText("0.0")
    def txtMocFtChanged(self):
        if self.flag1==0:
            self.flag1=2;
        if self.flag1==1:
            self.flag1=0;
        if self.flag1==2:
            try:
                self.parametersPanel.txtPrimaryMoc.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtPrimaryMocFt.text())), 4)))
            except:
                self.parametersPanel.txtPrimaryMoc.setText("0.0")

    def VorDmeShow(self):
        if self.parametersPanel.cmbRnavSpecification.currentIndex() == 0:
            try:
                self.parametersPanel.txtAsw1D.setText(str(round(self.parametersPanel.pnlTolerances.ASW.NauticalMiles, 4)))
                self.parametersPanel.txtXtt1D.setText(str(round(self.parametersPanel.pnlTolerances.XTT.NauticalMiles, 4)))
                self.parametersPanel.txtAtt1D.setText(str(round(self.parametersPanel.pnlTolerances.ATT.NauticalMiles, 4)))

                self.parametersPanel.txtAsw2D.setText(str(round(self.parametersPanel.pnlTolerances.ASW.NauticalMiles, 4)))
                self.parametersPanel.txtXtt2D.setText(str(round(self.parametersPanel.pnlTolerances.XTT.NauticalMiles, 4)))
                self.parametersPanel.txtAtt2D.setText(str(round(self.parametersPanel.pnlTolerances.ATT.NauticalMiles, 4)))
            except:
                pass
            return
        rnavSpecification_0 = self.parametersPanel.cmbRnavSpecification.currentText()
        rnavSpecification = self.parametersPanel.cmbPhaseOfFlight.currentText()
        rnavGnssFlightPhase = None
        if rnavSpecification == "Enroute":
            rnavGnssFlightPhase = RnavGnssFlightPhase.Enroute
        elif rnavSpecification == "StarSid":
            rnavGnssFlightPhase = RnavGnssFlightPhase.StarSid
        elif rnavSpecification == "Star30Sid30IfIafMa30":
            rnavGnssFlightPhase = RnavGnssFlightPhase.Star30Sid30IfIafMa30
        elif rnavSpecification == "Sid15":
            rnavGnssFlightPhase = RnavGnssFlightPhase.Sid15
        elif rnavSpecification == "Ma15":
            rnavGnssFlightPhase = RnavGnssFlightPhase.Ma15
        elif rnavSpecification == "Mapt":
            rnavGnssFlightPhase = RnavGnssFlightPhase.Mapt
        elif rnavSpecification == "Faf":
            rnavGnssFlightPhase = RnavGnssFlightPhase.Faf
        rnavGnssTolerance = RnavGnssTolerance(rnavSpecification_0, rnavGnssFlightPhase, None, None)
        # if rnavSpecification == "":
        #     return
        # rnavDmeDmeCriterium = 0 #self.parametersPanel.cmbDmeCount.currentIndex()
        # flag = True;
        # rnavDmeDmeFlightPhase = RnavDmeDmeFlightPhase.EnrouteStarSid #self.parametersPanel.cmbFlightPhase1.currentIndex() if(rnavSpecification != RnavSpecification.Rnav5) else RnavDmeDmeFlightPhase.EnrouteStarSid
        # result1 = RnavDmeDmeTolerance(rnavSpecification, rnavDmeDmeFlightPhase, rnavDmeDmeCriterium, Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT));
        # # if (self.parametersPanel.chbUse2Waypoints.isChecked()):
        # rnavSpecification = self.parametersPanel.cmbRnavSpecification.currentText()
        # rnavDmeDmeCriterium = 0 #self.parametersPanel.cmbDmeCount.currentIndex()
        # rnavDmeDmeFlightPhase = RnavDmeDmeFlightPhase.EnrouteStarSid #self.parametersPanel.cmbFlightPhase2.currentIndex() if(rnavSpecification != RnavSpecification.Rnav5) else RnavDmeDmeFlightPhase.EnrouteStarSid
        # result2 = RnavDmeDmeTolerance(rnavSpecification, rnavDmeDmeFlightPhase, rnavDmeDmeCriterium, Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT));

        # if result1 != None:
        if rnavGnssTolerance.ASW != None:
            try:
                self.parametersPanel.txtAsw1D.setText(str(round(rnavGnssTolerance.ASW.NauticalMiles, 2)))
                self.parametersPanel.txtXtt1D.setText(str(round(rnavGnssTolerance.XTT.NauticalMiles, 2)))
                self.parametersPanel.txtAtt1D.setText(str(round(rnavGnssTolerance.ATT.NauticalMiles, 2)))

                self.parametersPanel.txtAsw2D.setText(str(round(rnavGnssTolerance.ASW.NauticalMiles, 2)))
                self.parametersPanel.txtXtt2D.setText(str(round(rnavGnssTolerance.XTT.NauticalMiles, 2)))
                self.parametersPanel.txtAtt2D.setText(str(round(rnavGnssTolerance.ATT.NauticalMiles, 2)))
            except:
                pass


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
    
    
    def altitudeChanged(self):
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
        try:
            self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots))
        except:
            raise ValueError("Value Invalid")
    def method_31(self):
        self.parametersPanel.framePhaseOfFlight.setVisible(self.parametersPanel.cmbRnavSpecification.currentIndex() > 0);
        self.parametersPanel.pnlArp.setVisible(False if (self.parametersPanel.cmbRnavSpecification.currentIndex() <= 0 or self.parametersPanel.cmbPhaseOfFlight.currentIndex() < 0) else self.phaseOfFlight != 0);
        self.parametersPanel.chbCatH.setVisible(False if (self.parametersPanel.cmbRnavSpecification.currentIndex() <= 0) else self.parametersPanel.cmbPhaseOfFlight.currentIndex() >= 0);
        self.parametersPanel.pnlTolerances.setVisible(self.parametersPanel.cmbRnavSpecification.currentIndex() < 1);
        self.parametersPanel.chbDrawTolerance.setVisible(self.parametersPanel.cmbConstruct.currentText() == ConstructionType.Construct2D);
    def method_32(self, int_0):
        self.parametersPanel.cmbPhaseOfFlight.clear();
        if (self.parametersPanel.cmbRnavSpecification.currentIndex() > 0):
            rnavSpec = self.parametersPanel.cmbRnavSpecification.currentText()
            if rnavSpec == RnavSpecification.Rnav5 or rnavSpec == RnavSpecification.Rnav2 or rnavSpec == RnavSpecification.Rnp4 or rnavSpec == RnavSpecification.Rnp2:
                self.parametersPanel.cmbPhaseOfFlight.addItems(["Enroute", "StarSid"])
            elif rnavSpec == RnavSpecification.Rnav1 or rnavSpec == RnavSpecification.Rnp1 or rnavSpec == RnavSpecification.ARnp1:
                self.parametersPanel.cmbPhaseOfFlight.addItems(["Enroute", "StarSid", "Star30Sid30IfIafMa30", "Sid15", "Ma15"])
            elif rnavSpec == RnavSpecification.ARnp2:
                self.parametersPanel.cmbPhaseOfFlight.addItems(["Enroute"])
            elif rnavSpec == RnavSpecification.ARnp03 or rnavSpec == RnavSpecification.ARnp04 or rnavSpec == RnavSpecification.ARnp05 or rnavSpec == RnavSpecification.ARnp06 or rnavSpec == RnavSpecification.ARnp07 or rnavSpec == RnavSpecification.ARnp08 or rnavSpec == RnavSpecification.ARnp09:
                self.parametersPanel.cmbPhaseOfFlight.addItems(["StarSid", "Star30Sid30IfIafMa30", "Sid15", "Ma15"])
            elif rnavSpec == RnavSpecification.RnpApch:
                self.parametersPanel.cmbPhaseOfFlight.addItems(["Star30Sid30IfIafMa30", "Faf", "Mapt", "Ma15"])
#             foreach (RnavFlightPhase rnavFlightPhase in RnavGnssTolerance.smethod_1(self.rnavSpecification))
#             {
#                 if (rnavFlightPhase != RnavFlightPhase.Enroute && rnavFlightPhase != RnavFlightPhase.STAR)
#                 {
#                     continue;
#                 }
#                 self.pnlPhaseOfFlight.Items.Add(EnumHelper.smethod_0(rnavFlightPhase));
#             }
#         }
        if (int_0 > -1 and int_0 < self.parametersPanel.cmbPhaseOfFlight.count()):
            self.parametersPanel.cmbPhaseOfFlight.setCurrentIndex(int_0);
            return
        self.parametersPanel.cmbPhaseOfFlight.setCurrentIndex(-1)
    def method_37(self, point3d_0, rnavGnssTolerance_0, double_0):
        aTT = rnavGnssTolerance_0.ATT;
        point3d = MathHelper.distanceBearingPoint(point3d_0, double_0, aTT.Metres);
        xTT = rnavGnssTolerance_0.XTT;
        point3d1 = MathHelper.distanceBearingPoint(point3d, double_0 + 1.5707963267949, xTT.Metres);
        distance = rnavGnssTolerance_0.ATT;
        point3d2 = MathHelper.distanceBearingPoint(point3d1, double_0 + 3.14159265358979, distance.Metres * 2);
        aTT1 = rnavGnssTolerance_0.ATT;
        point3d3 = MathHelper.distanceBearingPoint(point3d_0, double_0, aTT1.Metres);
        xTT1 = rnavGnssTolerance_0.XTT;
        point3d4 = MathHelper.distanceBearingPoint(point3d3, double_0 - 1.5707963267949, xTT1.Metres);
        distance1 = rnavGnssTolerance_0.ATT;
        point3d5 = MathHelper.distanceBearingPoint(point3d4, double_0 + 3.14159265358979, distance1.Metres * 2);
        point3dArray = [point3d1, point3d2, point3d5, point3d4];
        return Point3dCollection(point3dArray);
    def method_33(self):
        self.method_32(-1)
        self.method_31()
    
    def method_38(self):
        aTT = None;
        point3d = None;
        point3d1 = None;
        point3d2 = self.parametersPanel.pnlWaypoint1.Point3d;
        point3d3 = self.parametersPanel.pnlWaypoint2.Point3d;
        if (MathHelper.calcDistance(point3d2, point3d3) < 1000):
            QMessageBox.warning(self, "Warning", Messages.ERR_POSITIONS_TOO_CLOSE)
        num = MathHelper.getBearing(point3d2, point3d3);
        num1 = MathHelper.smethod_4(num - 1.5707963267949);
        num2 = MathHelper.smethod_4(num + 1.5707963267949);
        num3 = MathHelper.smethod_4(num + 3.14159265358979);
        point3dCollection_0 = Point3dCollection();
        point3dCollection_3 = Point3dCollection();
        point3dCollection_1 = Point3dCollection();
        point3dCollection_2 = Point3dCollection();
        point3dCollection_4 = Point3dCollection();
        point3dArray = [point3d2, point3d3];
        point3dCollection_4.smethod_145(point3dArray);
        if (self.parametersPanel.cmbRnavSpecification.currentIndex() >= 1):
            rnavSpecification = self.rnavSpecification;
            rnavFlightPhase = self.phaseOfFlight;
            aircraftSpeedCategory = AircraftSpeedCategory.H if (self.parametersPanel.chbCatH.isChecked()) else AircraftSpeedCategory.C;
            if (rnavFlightPhase != 0):
                point3d4 = self.parametersPanel.pnlArp.Point3d;
                distance = Distance(MathHelper.calcDistance(point3d4, point3d2));
                distance1 = Distance(MathHelper.calcDistance(point3d4, point3d3));
                num4 = Unit.ConvertNMToMeter(30);
                point3d0_1 = []
                intersectionStatu = MathHelper.smethod_34(point3d2, point3d3, point3d4, num4, point3d0_1);
                point3d = point3d0_1[0]
                point3d1 = point3d0_1[1]
                # rnavGnssTolerance = RnavGnssTolerance(rnavSpecification, None, rnavFlightPhase, aircraftSpeedCategory, distance);
                rnavGnssTolerance = RnavGnssTolerance(rnavSpecification, rnavFlightPhase, None, None);
                # rnavGnssTolerance1 = RnavGnssTolerance(rnavSpecification, None, rnavFlightPhase, aircraftSpeedCategory, distance1);
                rnavGnssTolerance1 = RnavGnssTolerance(rnavSpecification, rnavFlightPhase, None, None);
                if (False if (not (rnavGnssTolerance.XTT == rnavGnssTolerance1.XTT) or not (rnavGnssTolerance.ATT == rnavGnssTolerance1.ATT)) else rnavGnssTolerance.ASW == rnavGnssTolerance1.ASW or intersectionStatu == IntersectionStatus.Nothing or intersectionStatu == IntersectionStatus.Tangent or distance.Metres >= num4 and distance1.Metres >= num4):
                    # rnavGnssTolerance2 = RnavGnssTolerance(rnavSpecification, None,  rnavFlightPhase, aircraftSpeedCategory, Distance(50, DistanceUnits.NM));
                    rnavGnssTolerance2 = RnavGnssTolerance(rnavSpecification, rnavFlightPhase, None, None);
                    aTT1 = rnavGnssTolerance2.ATT;
                    point3d5 = MathHelper.distanceBearingPoint(point3d2, num3, aTT1.Metres);
                    aSW = rnavGnssTolerance2.ASW;
                    point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d5, num1, aSW.Metres / 2));
                    aSW1 = rnavGnssTolerance2.ASW;
                    point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d5, num1, aSW1.Metres));
                    aSW2 = rnavGnssTolerance2.ASW;
                    point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d5, num2, aSW2.Metres / 2));
                    distance2 = rnavGnssTolerance2.ASW;
                    point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d5, num2, distance2.Metres));
                    aSW3 = rnavGnssTolerance2.ASW;
                    point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d3, num1, aSW3.Metres / 2));
                    distance3 = rnavGnssTolerance2.ASW;
                    point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d3, num1, distance3.Metres));
                    aSW4 = rnavGnssTolerance2.ASW;
                    point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d3, num2, aSW4.Metres / 2));
                    distance4 = rnavGnssTolerance2.ASW;
                    point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d3, num2, distance4.Metres));
                    point3dCollection_5 = self.method_37(point3d2, rnavGnssTolerance2, num);
                    point3dCollection_6 = self.method_37(point3d3, rnavGnssTolerance2, num);
                elif (distance.Metres > num4 or distance1.Metres > num4):
                    point3dCollection_5 = self.method_37(point3d2, rnavGnssTolerance, num);
                    point3dCollection_6 = self.method_37(point3d3, rnavGnssTolerance1, num);
                    aTT = rnavGnssTolerance.ATT;
                    point3d6 = MathHelper.distanceBearingPoint(point3d2, num3, aTT.Metres);
                    if (distance.Metres <= num4):
                        num5 = math.tan(Unit.ConvertDegToRad(15));
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d6, num1, aTT.Metres / 2));
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d6, num1, aTT.Metres));
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d6, num2, aTT.Metres / 2));
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d6, num2, aTT.Metres));
                        aTT = rnavGnssTolerance.ATT;
                        point3d7 = MathHelper.distanceBearingPoint(point3d1, num3, aTT.Metres);
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d7, num1, aTT.Metres / 2));
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d7, num1, aTT.Metres));
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d7, num2, aTT.Metres / 2));
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d7, num2, aTT.Metres));
                        metres = rnavGnssTolerance1.ASW.Metres;
                        aTT = rnavGnssTolerance.ASW;
                        point3d7 = MathHelper.distanceBearingPoint(point3d7, num, math.fabs(metres - aTT.Metres) / num5);
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d7, num1, aTT.Metres / 2));
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d7, num1, aTT.Metres));
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d7, num2, aTT.Metres / 2));
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d7, num2, aTT.Metres));
                        point3d7 = MathHelper.distanceBearingPoint(point3d7, num, 100) if (MathHelper.calcDistance(point3d6, point3d7) > MathHelper.calcDistance(point3d6, point3d3)) else  point3d3;
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d7, num1, aTT.Metres / 2));
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d7, num1, aTT.Metres));
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d7, num2, aTT.Metres / 2));
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d7, num2, aTT.Metres));
                    else:
                        num6 = math.tan(Unit.ConvertDegToRad(30));
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d6, num1, aTT.Metres / 2));
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d6, num1, aTT.Metres));
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d6, num2, aTT.Metres / 2));
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d6, num2, aTT.Metres));
                        aTT = rnavGnssTolerance.ATT;
                        point3d8 = MathHelper.distanceBearingPoint(point3d, num, aTT.Metres);
                        metres1 = rnavGnssTolerance.ASW.Metres;
                        aTT = rnavGnssTolerance1.ASW;
                        point3d8 = MathHelper.distanceBearingPoint(point3d8, num3, math.fabs(metres1 - aTT.Metres) / num6);
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d8, num1, aTT.Metres / 2));
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d8, num1, aTT.Metres));
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d8, num2, aTT.Metres / 2));
                        aTT = rnavGnssTolerance.ASW;
                        point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d8, num2, aTT.Metres));
                        aTT = rnavGnssTolerance.ATT;
                        point3d8 = MathHelper.distanceBearingPoint(point3d, num, aTT.Metres);
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d8, num1, aTT.Metres / 2));
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d8, num1, aTT.Metres));
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d8, num2, aTT.Metres / 2));
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d8, num2, aTT.Metres));
                        point3d8 = MathHelper.distanceBearingPoint(point3d8, num, 100) if (MathHelper.calcDistance(point3d6, point3d8) > MathHelper.calcDistance(point3d6, point3d3)) else point3d3;
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d8, num1, aTT.Metres / 2));
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d8, num1, aTT.Metres));
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d8, num2, aTT.Metres / 2));
                        aTT = rnavGnssTolerance1.ASW;
                        point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d8, num2, aTT.Metres));
                    self.method_39(point3dCollection_1, point3d6, point3d3, num);
                    self.method_39(point3dCollection_2, point3d6, point3d3, num);
                    self.method_39(point3dCollection_0, point3d6, point3d3, num);
                    self.method_39(point3dCollection_3, point3d6, point3d3, num);
                else:
                    # rnavGnssTolerance3 = RnavGnssTolerance(rnavSpecification, None, rnavFlightPhase, aircraftSpeedCategory, Distance(10, DistanceUnits.NM));
                    rnavGnssTolerance3 = RnavGnssTolerance(rnavSpecification, rnavFlightPhase, None, None);
                    aTT2 = rnavGnssTolerance3.ATT;
                    point3d9 = MathHelper.distanceBearingPoint(point3d2, num3, aTT2.Metres);
                    aSW5 = rnavGnssTolerance3.ASW;
                    point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d9, num1, aSW5.Metres / 2));
                    aTT = rnavGnssTolerance3.ASW;
                    point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d9, num1, aTT.Metres));
                    aTT = rnavGnssTolerance3.ASW;
                    point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d9, num2, aTT.Metres / 2));
                    aTT = rnavGnssTolerance3.ASW;
                    point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d9, num2, aTT.Metres));
                    aTT = rnavGnssTolerance3.ASW;
                    point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d3, num1, aTT.Metres / 2));
                    aTT = rnavGnssTolerance3.ASW;
                    point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d3, num1, aTT.Metres));
                    aTT = rnavGnssTolerance3.ASW;
                    point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d3, num2, aTT.Metres / 2));
                    aTT = rnavGnssTolerance3.ASW;
                    point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d3, num2, aTT.Metres));
                    point3dCollection_5 = self.method_37(point3d2, rnavGnssTolerance3, num);
                    point3dCollection_6 = self.method_37(point3d3, rnavGnssTolerance3, num);
            else:
                # rnavGnssTolerance4 = RnavGnssTolerance(rnavSpecification, None, rnavFlightPhase, aircraftSpeedCategory, Distance(50, DistanceUnits.NM));
                rnavGnssTolerance4 = RnavGnssTolerance(rnavSpecification, rnavFlightPhase, None, None);
                distance5 = rnavGnssTolerance4.ASW;
                point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d2, num1, distance5.Metres / 2));
                aSW6 = rnavGnssTolerance4.ASW;
                point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d2, num1, aSW6.Metres));
                distance6 = rnavGnssTolerance4.ASW;
                point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d2, num2, distance6.Metres / 2));
                aSW7 = rnavGnssTolerance4.ASW;
                point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d2, num2, aSW7.Metres));
                distance7 = rnavGnssTolerance4.ASW;
                point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d3, num1, distance7.Metres / 2));
                aSW8 = rnavGnssTolerance4.ASW;
                point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d3, num1, aSW8.Metres));
                distance8 = rnavGnssTolerance4.ASW;
                point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d3, num2, distance8.Metres / 2));
                aSW9 = rnavGnssTolerance4.ASW;
                point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d3, num2, aSW9.Metres));
                point3dCollection_5 = self.method_37(point3d2, rnavGnssTolerance4, num);
                point3dCollection_6 = self.method_37(point3d3, rnavGnssTolerance4, num);
        else:
            rnavGnssTolerance5 = RnavGnssTolerance(None, None, None, None, self.parametersPanel.pnlTolerances.XTT, self.parametersPanel.pnlTolerances.ATT, self.parametersPanel.pnlTolerances.ASW);
            aTT = rnavGnssTolerance5.ATT;
            point3d10 = MathHelper.distanceBearingPoint(point3d2, num3, aTT.Metres);
            distance9 = rnavGnssTolerance5.ASW;
            point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d10, num1, distance9.Metres / 2));
            aSW10 = rnavGnssTolerance5.ASW;
            point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d10, num1, aSW10.Metres));
            distance10 = rnavGnssTolerance5.ASW;
            point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d10, num2, distance10.Metres / 2));
            aSW11 = rnavGnssTolerance5.ASW;
            point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d10, num2, aSW11.Metres));
            distance11 = rnavGnssTolerance5.ASW;
            point3dCollection_1.Add(MathHelper.distanceBearingPoint(point3d3, num1, distance11.Metres / 2));
            aSW12 = rnavGnssTolerance5.ASW;
            point3dCollection_0.Add(MathHelper.distanceBearingPoint(point3d3, num1, aSW12.Metres));
            distance12 = rnavGnssTolerance5.ASW;
            point3dCollection_2.Add(MathHelper.distanceBearingPoint(point3d3, num2, distance12.Metres / 2));
            aSW13 = rnavGnssTolerance5.ASW;
            point3dCollection_3.Add(MathHelper.distanceBearingPoint(point3d3, num2, aSW13.Metres));
            point3dCollection_5 = self.method_37(point3d2, rnavGnssTolerance5, num);
            point3dCollection_6 = self.method_37(point3d3, rnavGnssTolerance5, num);
        return (True, point3dCollection_0, point3dCollection_1, point3dCollection_2, point3dCollection_3, point3dCollection_4, point3dCollection_5, point3dCollection_6);
    def drawLineBand(self):
        if self.lineBand != None:
            QgisHelper.ClearRubberBandInCanvas(define._canvas, [self.lineBand])
            self.lineBand = None
        try:
            pointList = []
            self.lineBand = QgsRubberBand(define._canvas, QGis.Line)
            self.lineBand.setColor(Qt.red)
            self.lineBand.setWidth(1.5)
            self.lineBand.reset(QGis.Line)
            try:
                pointWpt1 = self.parametersPanel.pnlWaypoint1.Point3d
                pointList.append(pointWpt1)
            except UserWarning:
                pass
            try:
                pointWpt2 = self.parametersPanel.pnlWaypoint2.Point3d
                pointList.append(pointWpt2)
            except:
                pass

            if len(pointList) > 1:
                self.lineBand.addGeometry(QgsGeometry.fromPolyline(pointList),None)

        except UnboundLocalError:
            pass

        finally:
            self.lineBand.show()
    def method_39(self, point3dCollection_0, point3d_0, point3d_1, double_0):
        point3d = None;
        num = 0;
        num1 = 1;
        double0 = double_0 - 1.5707963267949;
        num2 = MathHelper.calcDistance(point3d_0, point3d_1);
        for i in range(1, point3dCollection_0.get_Count()):
            num = i - 1;
            num1 = i;
            point3d = MathHelper.getIntersectionPoint(point3d_0, point3d_1, point3dCollection_0.get_Item(num1), MathHelper.distanceBearingPoint(point3dCollection_0.get_Item(num1), double0, 1000));
            num3 = MathHelper.calcDistance(point3d_0, point3d);
            if (MathHelper.smethod_99(num2, num3, 0.0001) or num2 < num3):
                point3d = MathHelper.getIntersectionPoint(point3dCollection_0.get_Item(num), point3dCollection_0.get_Item(num1), point3d_1, MathHelper.distanceBearingPoint(point3d_1, double0, 1000));
                point3dCollection_0.Insert(num1, point3d);
                num4 = num1 + 1;
                while (point3dCollection_0.get_Count() > num4):
                    point3dCollection_0.RemoveAt(num4);
                return;
        point3d = MathHelper.getIntersectionPoint(point3dCollection_0.get_Item(num), point3dCollection_0.get_Item(num1), point3d_1, MathHelper.distanceBearingPoint(point3d_1, double0, 1000));
        point3dCollection_0.Add(point3d);
    def nominal2Layer(self):
        return AcadHelper.createNominalTrackLayer([self.parametersPanel.pnlWaypoint1.Point3d, self.parametersPanel.pnlWaypoint2.Point3d], None, "memory", "NominalTrack_" + self.surfaceType.replace(" ", "_").replace("-", "_"))
    def get_phaseOfFlight(self):
        if self.parametersPanel.cmbPhaseOfFlight.currentText() == "Enroute":
            return 0
        elif self.parametersPanel.cmbPhaseOfFlight.currentText() == "StarSid":
            return 1
        elif self.parametersPanel.cmbPhaseOfFlight.currentText() == "Star30Sid30IfIafMa30":
            return 2
        elif self.parametersPanel.cmbPhaseOfFlight.currentText() == "Sid15":
            return 3
        elif self.parametersPanel.cmbPhaseOfFlight.currentText() == "Ma15":
            return 4
        elif self.parametersPanel.cmbPhaseOfFlight.currentText() == "Faf":
            return 5
        elif self.parametersPanel.cmbPhaseOfFlight.currentText() == "Mapt":
            return 6
        return -1
    
    phaseOfFlight = property(get_phaseOfFlight, None, None, None)
    
    def get_rnavSpecification(self):
        return self.parametersPanel.cmbRnavSpecification.currentText()
    rnavSpecification = property(get_rnavSpecification, None, None, None)
class RnavStraightObstacles(ObstacleTable):
    def __init__(self, complexObstacleArea_0, altitude_0, altitude_1, manualPoly):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, None)
        self.manualPolygon = manualPoly
        self.surfaceType = SurfaceTypes.RnavStraightSegmentAnalyser
        self.area = complexObstacleArea_0;
        self.primaryMoc = altitude_0.Metres;
        self.enrouteAltitude = altitude_1.Metres;
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
        if self.manualPolygon != None:
            if not self.manualPolygon.contains(obstacle_0.Position):
                return
        obstacleAreaResult = ObstacleAreaResult.Outside;
        num = None;
        num1 = None;
        mocMultiplier = self.primaryMoc * obstacle_0.MocMultiplier;
        resultList = []
        obstacleAreaResult = self.area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier, resultList);
        if len(resultList) == None:
            return
        num = resultList[0]
        num1 = resultList[1]
        if (obstacleAreaResult != ObstacleAreaResult.Outside and num != None):
            position = obstacle_0.Position;
            z = position.get_Z() + obstacle_0.Trees + num;
            criticalObstacleType = CriticalObstacleType.No;
            if (z > self.enrouteAltitude):
                criticalObstacleType = CriticalObstacleType.Yes;
            checkResult = [obstacleAreaResult, num1, num, z, criticalObstacleType];
            self.addObstacleToModel(obstacle_0, checkResult)
#             RnavStraightSegmentAnalyser.obstacles.method_11(obstacle_0, obstacleAreaResult, num1, num, z, criticalObstacleType);
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