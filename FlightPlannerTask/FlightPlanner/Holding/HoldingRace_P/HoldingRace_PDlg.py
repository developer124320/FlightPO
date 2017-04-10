# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QSize, Qt
from PyQt4.QtGui import QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsCoordinateReferenceSystem,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType, SurfaceTypes, DistanceUnits,AircraftSpeedCategory, OrientationType, AltitudeUnits, ObstacleAreaResult
from FlightPlanner.Holding.HoldingRace_P.ui_HoldingRace_P import Ui_HoldingRace_P
from FlightPlanner.Panels.PositionPanel import PositionPanel
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
from FlightPlanner.types import Point3D
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.IasHelp.IasHelpDlg import IasHelpDlg
import define

class HoldingRace_PDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("HoldingRace_PDlg")
        self.surfaceType = SurfaceTypes.HoldingRace_P
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.HoldingRace_P)
        self.resize(540, 500)
        self.surfaceList = None
        
    
    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(1)
        self.ui.tabCtrlGeneral.removeTab(2)
        return FlightPlanBaseDlg.uiStateInit(self)
        
    def initParametersPan(self):
        ui = Ui_HoldingRace_P()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)
        
        self.parametersPanel.txtTas.setEnabled(False)
        self.parametersPanel.pnlInsPos = PositionPanel(self.parametersPanel.gbVorDmePosition)
#         self.parametersPanel.pnlInsPos.groupBox.setTitle("FAWP")
        self.parametersPanel.pnlInsPos.btnCalculater.hide()
        self.parametersPanel.pnlInsPos.hideframe_Altitude()
        self.parametersPanel.pnlInsPos.setObjectName("pnlInsPos")
        ui.vl_VorDmePosition.addWidget(self.parametersPanel.pnlInsPos)
        
        self.parametersPanel.pnlWind = WindPanel(self.parametersPanel.gbParameters)
        self.parametersPanel.pnlWind.lblIA.setMinimumSize(250, 0)
        self.parametersPanel.vl_gbParameters.insertWidget(6, self.parametersPanel.pnlWind)
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
               
        
        self.parametersPanel.cmbAircraftCategory.addItems(["A", "B", "C", "D", "E", "H", "Custom"])
#         self.parametersPanel.cmbOutboundLimit.addItems(["Time", "Distance From Waypoint"])
#         self.parametersPanel.cmbConstruction.addItems(["2D", "3D"])
        self.parametersPanel.cmbOrientation.addItems(["Right", "Left"])
        
        self.parametersPanel.cmbAircraftCategory.setCurrentIndex(3)
        self.parametersPanel.frameAircraftCategory.hide()
        self.parametersPanel.frameMoc.hide()
                
#         self.parametersPanel.cmbHoldingFunctionality.currentIndexChanged.connect(self.cmbHoldingFunctionalityCurrentIndexChanged)
#         self.parametersPanel.cmbOutboundLimit.currentIndexChanged.connect(self.cmbOutboundLimitCurrentIndexChanged)
#         self.parametersPanel.btnCaptureTrack.clicked.connect(self.captureBearing)
#         self.parametersPanel.btnCaptureDistance.clicked.connect(self.measureDistance)
#         self.parametersPanel.btnCaptureLength.clicked.connect(self.measureLength)        
        self.parametersPanel.txtAltitude.textChanged.connect(self.altitudeChanged)
#         self.parametersPanel.cmbAircraftCategory.currentIndexChanged.connect(self.changeCategory)
#         self.parametersPanel.btnIasHelp.clicked.connect(self.iasHelpShow)
        self.parametersPanel.txtIas.textChanged.connect(self.iasChanged)
        self.parametersPanel.txtIsa.textChanged.connect(self.isaChanged)
        
        self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots))
    def iasChanged(self):
        try:
            self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots))
        except:
            raise ValueError("Value Invalid")
    def isaChanged(self):
        try:
            self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots))
        except:
            raise ValueError("Value Invalid")    
    def iasHelpShow(self):
        dlg = IasHelpDlg()
        dlg.exec_()
    def altitudeChanged(self):
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
        try:
            self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots))
        except:
            raise ValueError("Value Invalid")
    def method_27(self):
        try:
            if (not self.isHoldingFunctionalityRequired):
                if (float(self.parametersPanel.txtTime.text())< 1):
                    QMessageBox.warning(self, "Warning", "Time's value can not be smaller than 1.")
        except:
            QMessageBox.warning(self, "Warning", "Time's value must be type of number.")
    
    def method_38(self):
        point3d = self.parametersPanel.pnlWaypoint.Point3d
        num = 1
        if (self.parametersPanel.cmbOrientation.currentText() == OrientationType.Left):
            num = -1
        num1 = MathHelper.smethod_4(Unit.ConvertDegToRad(float(self.parametersPanel.txtTrack.Value)))
        aTT = Distance(float(self.parametersPanel.pnlTolerances.txtAtt.text()), DistanceUnits.NM)
        point3d1 = MathHelper.distanceBearingPoint(point3d, num1, aTT.Metres)
        xTT = Distance(float(self.parametersPanel.pnlTolerances.txtXtt.text()), DistanceUnits.NM)
        point3d2 = MathHelper.distanceBearingPoint(point3d1, num1 + num * 1.5707963267949, xTT.Metres)
        distance = Distance(float(self.parametersPanel.pnlTolerances.txtAtt.text()), DistanceUnits.NM)
        point3d3 = MathHelper.distanceBearingPoint(point3d2, num1 + 3.14159265358979, distance.Metres * 2)
        aTT1 = Distance(float(self.parametersPanel.pnlTolerances.txtAtt.text()), DistanceUnits.NM)
        point3d4 = MathHelper.distanceBearingPoint(point3d, num1, aTT1.Metres)
        xTT1 = Distance(float(self.parametersPanel.pnlTolerances.txtXtt.text()), DistanceUnits.NM)
        point3d5 = MathHelper.distanceBearingPoint(point3d4, num1 - num * 1.5707963267949, xTT1.Metres)
        distance1 = Distance(float(self.parametersPanel.pnlTolerances.txtAtt.text()), DistanceUnits.NM)
        point3d6 = MathHelper.distanceBearingPoint(point3d5, num1 + 3.14159265358979, distance1.Metres * 2)
        point3dArray = [point3d2, point3d3, point3d6, point3d5]
        return PolylineArea(point3dArray)
    
#     def method_136(self, polylineArea_0):
#         
#     
    def changeCategory(self):
        if self.parametersPanel.cmbAircraftCategory.currentIndex() == AircraftSpeedCategory.A:
            self.parametersPanel.txtIas.setText(str(Speed.smethod_0(Speed(150), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots))
            return
        elif self.parametersPanel.cmbAircraftCategory.currentIndex() == AircraftSpeedCategory.B:
            self.parametersPanel.txtIas.setText(str(Speed.smethod_0(Speed(180), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots))
            return
        elif self.parametersPanel.cmbAircraftCategory.currentIndex() == AircraftSpeedCategory.C:
            self.parametersPanel.txtIas.setText(str(Speed.smethod_0(Speed(240), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots))
            return
        elif self.parametersPanel.cmbAircraftCategory.currentIndex() == AircraftSpeedCategory.D:
            self.parametersPanel.txtIas.setText(str(Speed.smethod_0(Speed(250), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots))
            return
        elif self.parametersPanel.cmbAircraftCategory.currentIndex() == AircraftSpeedCategory.E:
            self.parametersPanel.txtIas.setText(str(Speed.smethod_0(Speed(250), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots))
            return
        elif self.parametersPanel.cmbAircraftCategory.currentIndex() == AircraftSpeedCategory.H:
            self.parametersPanel.txtIas.setText(str(Speed.smethod_0(Speed(70), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots))
            return
    
    # def captureBearing(self):
    #     self.captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrack)
    #     define._canvas.setMapTool(self.captureTrackTool)
    def measureDistance(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtDistance, DistanceUnits.NM)
        define._canvas.setMapTool(measureDistanceTool)
    def measureLength(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtLength, DistanceUnits.NM)
        define._canvas.setMapTool(measureDistanceTool)
    def cmbHoldingFunctionalityCurrentIndexChanged(self):
        if self.parametersPanel.cmbHoldingFunctionality.currentIndex() == 0:
            self.parametersPanel.frame_Length.show()
            self.parametersPanel.frame_OutBoundLimit.hide()
            self.parametersPanel.frame_Time.hide()
            self.parametersPanel.frame_Distance.hide()
            self.parametersPanel.chbSector1.setVisible(False)
            self.parametersPanel.chbSector2.setVisible(False)
            self.parametersPanel.chbSector3.setVisible(False)
            self.parametersPanel.chbIntercept.setVisible(True)
            self.parametersPanel.chbSectors12.setVisible(True)
        else:
            self.parametersPanel.frame_OutBoundLimit.show()
            self.parametersPanel.frame_Length.hide()
            if self.parametersPanel.cmbOutboundLimit.currentIndex() == 0:
                self.parametersPanel.frame_Time.show()
                self.parametersPanel.chbSector1.setVisible(False)
                self.parametersPanel.chbSector2.setVisible(False)
                self.parametersPanel.chbSector3.setVisible(False)
                self.parametersPanel.chbIntercept.setVisible(True)
                self.parametersPanel.chbSectors12.setVisible(True)
            else:
                self.parametersPanel.frame_Distance.show()
                self.parametersPanel.chbSector1.setVisible(True)
                self.parametersPanel.chbSector2.setVisible(True)
                self.parametersPanel.chbSector3.setVisible(True)
                self.parametersPanel.chbIntercept.setVisible(False)
                self.parametersPanel.chbSectors12.setVisible(False)
        
                
    def cmbOutboundLimitCurrentIndexChanged(self):
        if self.parametersPanel.cmbOutboundLimit.currentIndex() == 0:
            self.parametersPanel.frame_Time.show()
            self.parametersPanel.frame_Distance.hide()
            self.parametersPanel.chbSector1.setVisible(False)
            self.parametersPanel.chbSector2.setVisible(False)
            self.parametersPanel.chbSector3.setVisible(False)
            self.parametersPanel.chbIntercept.setVisible(True)
            self.parametersPanel.chbSectors12.setVisible(True)
        else:
            self.parametersPanel.frame_Time.hide()
            self.parametersPanel.frame_Distance.show()  
            self.parametersPanel.chbSector1.setVisible(True)
            self.parametersPanel.chbSector2.setVisible(True)
            self.parametersPanel.chbSector3.setVisible(True)
            self.parametersPanel.chbIntercept.setVisible(False)
            self.parametersPanel.chbSectors12.setVisible(False)                 
    def get_isHoldingFunctionalityRequired(self):
        return self.parametersPanel.cmbHoldingFunctionality.currentIndex() == 0
    isHoldingFunctionalityRequired = property(get_isHoldingFunctionalityRequired, None, None, None)            

class HoldingRnavArea:
#     private PrimaryObstacleArea area;
# 
#     private double moc;
    def get_area(self):
        return self.area
    Area = property(get_area, None, None, None)
    
    def get_moc(self):
        return self.moc
    Moc = property(get_moc, None, None, None)
    
    def __init__(self, polylineArea_0, altitude_0):
        self.area = PrimaryObstacleArea(polylineArea_0);
        self.moc = altitude_0.Metres;

    def method_0(self, obstacle_0):
        double_0 = self.moc * obstacle_0.MocMultiplier;
        double_1 = None
        if (not self.area.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
            return (False, double_0, double_1)
        position = obstacle_0.Position;
        double_1 = position.get_Z() + obstacle_0.Trees + double_0;
        return (True, double_0, double_1)
class HoldingRnavObstacles(ObstacleTable):
    def __init__(self, bool_0, typeStr, surfacesList = None, altitude = None, inner = None, outer = None, poly = None, altitude_1 = None, distance_0 = None):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)
        
        self.surfaceType = SurfaceTypes.HoldingRnp
        self.obstaclesChecked = None
        self.typeStr = typeStr
        self.altitude = altitude.Metres
        if self.typeStr == "buffer":            
            self.surfacesList = surfacesList
            
        else:
            self.inner = inner
            self.outer = outer
            self.poly = poly
            self.moc = altitude_1.Metres
            self.offset = distance_0
        self.bool = bool_0
    def setHiddenColumns(self, tableView):
        tableView.hideColumn(self.IndexObstArea)
        tableView.hideColumn(self.IndexDistInSecM)
        return ObstacleTable.setHiddenColumns(self, tableView)
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        newHeaderCount = 0
        if bool:
            self.IndexObstArea = fixedColumnCount 
            self.IndexDistInSecM = fixedColumnCount + 1
            self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DistInSecM
                ])
            newHeaderCount = 2
        self.IndexMocAppliedM = fixedColumnCount + newHeaderCount
        self.IndexMocAppliedFt = fixedColumnCount + 1 + newHeaderCount
        self.IndexMocMultiplier = fixedColumnCount + 2 + newHeaderCount
        self.IndexOcaM = fixedColumnCount + 3 + newHeaderCount
        self.IndexOcaFt = fixedColumnCount + 4 + newHeaderCount
        self.IndexCritical = fixedColumnCount + 5 + newHeaderCount
                 
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt,
                ObstacleTableColumnType.Critical            
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)
    
    def addObstacleToModel(self, obstacle, checkResult):
        if self.typeStr == "buffer":
            ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
            row = self.source.rowCount() - 1
        
            item = QStandardItem(str(checkResult[0]))
            item.setData(checkResult[0])
            self.source.setItem(row, self.IndexMocAppliedM, item)
              
            item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[0])))
            item.setData(Unit.ConvertMeterToFeet(checkResult[0]))
            self.source.setItem(row, self.IndexMocAppliedFt, item)
              
            item = QStandardItem(str(ObstacleTable.MocMultiplier))
            item.setData(ObstacleTable.MocMultiplier)
            self.source.setItem(row, self.IndexMocMultiplier, item)
              
            item = QStandardItem(str(checkResult[1]))
            item.setData(checkResult[1])
            self.source.setItem(row, self.IndexOcaM, item)
              
            item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[1])))
            item.setData(Unit.ConvertMeterToFeet(checkResult[1]))
            self.source.setItem(row, self.IndexOcaFt, item)
            
            item = QStandardItem(str(checkResult[2]))
            item.setData(checkResult[2])
            self.source.setItem(row, self.IndexCritical, item) 
        else:
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
        if self.typeStr == "buffer":
            criticalObstacleType = CriticalObstacleType.No;
            for current in self.surfacesList:
                result, num, num1 = current.method_0
                if (result):
                    if (num1 > self.altitude):
                        criticalObstacleType = CriticalObstacleType.Yes;
                    checkResult = []
                    checkResult.append(num)
                    checkResult.append(num1)
                    checkResult.append(criticalObstacleType)
                    self.addObstacleToModel(obstacle_0, checkResult)
                    break
        else:
            mocMultiplier = self.moc * obstacle_0.MocMultiplier;
            metres = None
            num = None
            obstacleAreaResult = ObstacleAreaResult.Outside;
            if (not self.inner.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
                num = MathHelper.calcDistance(self.poly.getClosestPointTo(obstacle_0.Position, False), obstacle_0.Position) - obstacle_0.Tolerance;
                if (num > self.offset.Metres):
                    return;
                metres = mocMultiplier * (1 - num / self.offset.Metres);
                obstacleAreaResult = ObstacleAreaResult.Secondary;
            else:
                metres = mocMultiplier;
                obstacleAreaResult = ObstacleAreaResult.Primary;
            position = obstacle_0.Position;
            z = position.get_Z() + obstacle_0.Trees + metres;
            criticalObstacleType = CriticalObstacleType.No;
            if (z > self.altitude):
                criticalObstacleType = CriticalObstacleType.Yes;
            checkResult = []
            checkResult.append(obstacleAreaResult)
            checkResult.append(num)
            checkResult.append(metres)
            checkResult.append(z)
            checkResult.append(criticalObstacleType)
            self.addObstacleToModel(obstacle_0, checkResult)
#             HoldingRnav.obstacles.method_12(obstacle_0, obstacleAreaResult, num, metres, z, criticalObstacleType);

#     def method_11(self, obstacle_0, double_0, double_1, criticalObstacleType_0):
#         double0 = []
#         double0.append(double_0)
#         double0[self.IndexMocAppliedFt] = Unit.ConvertMeterToFeet(double_0);
#         double0[self.IndexOcaM] = double_1;
#         double0[self.IndexOcaFt] = Unit.ConvertMeterToFeet(double_1);
#         double0[self.IndexCritical] = criticalObstacleType_0;
#         return base.method_1(double0)
        
class HoldingRnavFunctionalityRequiredType:
    Yes = "Yes"
    No = "No"        