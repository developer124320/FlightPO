# -*- coding: UTF-8 -*-
'''
Created on 30 Jun 2015

@author: Administrator
'''
from qgis.core import QGis, QgsVectorLayer, QgsGeometry, QgsFeature, QgsVectorFileWriter
from PyQt4.QtGui import QSizePolicy, QSpinBox, QLabel, QFileDialog, QFrame, QLineEdit, QHBoxLayout, QFont, QStandardItem, QMessageBox
from PyQt4.QtCore import QString,Qt, QCoreApplication, QSize

# 
# from FlightPlanner.PinSVisualSegment.ui_PinSVisualSegmentDepDlg import ui_PinSVisualSegmentDepDlg
# 
# from FlightPlanner.types import DistanceUnits, AltitudeUnits, PinsOperationType, \
#         OCAHType, TurnDirection, AngleUnits, ConstructionType, AngleGradientSlopeUnits, \
#         SurfaceTypes, Point3D, CriticalObstacleType, ObstacleTableColumnType, PinsSurfaceType,\
#         AngleUnits, DisregardableObstacleType
from FlightPlanner.helpers import Altitude 
from FlightPlanner.types import ConstructionType, CriticalObstacleType, ObstacleTableColumnType, OrientationType, DistanceUnits, AltitudeUnits, TurnDirection
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.WindPanel import WindPanel
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
# 
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Polyline import Polyline
from FlightPlanner.polylineArea import PolylineArea
# 
# 
# from FlightPlanner.QgisHelper import QgisHelper
# from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.types import SurfaceTypes, AltitudeUnits
from FlightPlanner.Enroute.EnrouteStraight.ui_EnrouteStraight import Ui_EnrouteStraight
from FlightPlanner.DataHelper import DataHelper

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import RnavSegmentType, AircraftSpeedCategory, AltitudeUnits, SpeedUnits, AngleGradientSlopeUnits,\
                Point3D, RnavCommonWaypoint, WindType, AngleUnits, SurfaceTypes
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.helpers import Distance, Speed, Altitude, AngleGradientSlope, MathHelper, Unit
from FlightPlanner.IasHelp.IasHelpDlg import IasHelpDlg
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
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.EnrouteStraight)
        self.resultLayerList = []
        self.resize(540, 550)

    def exportResult(self):
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return  
#         self.filterList = []
#         for taaArea in self.taaCalculationAreas:
#             self.filterList.append(taaArea.title)
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.HoldingRnp, self.ui.tblObstacles, None, parameterList)
#         self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
        return FlightPlanBaseDlg.exportResult(self)
    
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("Waypoint Position", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlWaypoint.txtPointX.text()), float(self.parametersPanel.pnlWaypoint.txtPointY.text()))
        
        parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
        parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
        parameterList.append(("X", self.parametersPanel.pnlWaypoint.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlWaypoint.txtPointY.text()))
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("RNP Value", self.parametersPanel.txtRnpValue.text()))
        parameterList.append(("Aircraft Category", self.parametersPanel.cmbAircraftCategory_2.currentText()))
        parameterList.append(("IAS", self.parametersPanel.txtIas.text() + "kts"))
        parameterList.append(("Altitude", self.parametersPanel.txtAltitude.text() + "ft"))
        parameterList.append(("ISA", self.parametersPanel.txtIsa.text() + unicode("°C", "utf-8")))
        parameterList.append(("Wind", self.parametersPanel.pnlWind.speedBox.text() + "kts"))
        parameterList.append(("Time", self.parametersPanel.txtTime.text() + "min"))
        parameterList.append(("MOC", self.parametersPanel.txtMoc.text() + "m"))
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstruction.currentText()))
        
        
        parameterList.append(("Orientation", "group"))
        parameterList.append(("In-bound Trak", self.parametersPanel.txtTrack.text() + unicode("°", "utf-8")))
        parameterList.append(("Turns", self.parametersPanel.cmbOrientation.currentText()))
        
        parameterList.append(("Results / Checked Obstacles", "group"))   
        parameterList.append(("Checked Obstacles", "group"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        return parameterList
    def initObstaclesModel(self):
        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        self.obstaclesModel = HoldingRnpObstacles(self.surfaceList)
        
        return FlightPlanBaseDlg.initObstaclesModel(self)
    def btnEvaluate_Click(self):
        return FlightPlanBaseDlg.btnEvaluate_Click(self)


    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        mapUnits = define._canvas.mapUnits()
        constructionLayer = None
        
        polylines = self.method_36(True)
        
        if (self.parametersPanel.cmbConstruction.currentText() != ConstructionType.Construct3D):
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)
            for polylineArea1 in polylines:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea1, True)
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
            #
            # constructionLayer.startEditing()
            count = len(polylines)
            num = 0.1 * count
            altitude = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)
            value = Altitude(float(self.parametersPanel.txtMoc.text()), AltitudeUnits.M)
            metres = altitude.Metres - value.Metres
            for i in range(count):
                polygon1 = QgsGeometry.fromPolygon([polylines[i].method_14_closed()])
                polygonNew = polygon1
                if (i > 0):
                    metres1 = altitude.Metres
#                     value = self.pnlMoc.Value;
                    metres = metres1 - num * value.Metres
                    num = num - 0.1
# #                 polylines[i].set_Elevation(metres);
#                 DBObjectCollection dBObjectCollection = new DBObjectCollection();
# #                 dBObjectCollection.Add(polylines[i]);
#                 Autodesk.AutoCAD.DatabaseServices.Region item = Autodesk.AutoCAD.DatabaseServices.Region.CreateFromCurves(dBObjectCollection).get_Item(0) as Autodesk.AutoCAD.DatabaseServices.Region;
#                 item.SetDatabaseDefaults();
                if (i > 0):
                    polygon0 = QgsGeometry.fromPolygon([polylines[i - 1].method_14_closed()])
                    polygonNew = polygon1.difference(polygon0)
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, PolylineArea(polygonNew.asPolygon()[0]))
            #     feature = QgsFeature()
            #     feature.setGeometry(polygonNew)
            #     constructionLayer.addFeature(feature)
            # constructionLayer.commitChanges()
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.HoldingRnp)
        self.resultLayerList = [constructionLayer]
        self.ui.btnEvaluate.setEnabled(True)

    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)
        
        return FlightPlanBaseDlg.uiStateInit(self)
    def initParametersPan(self):
        ui = Ui_EnrouteStraight()
        self.parametersPanel = ui
        
        
        FlightPlanBaseDlg.initParametersPan(self)        
        
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
        self.parametersPanel.cmbNavAidType1.addItems(["VOR", "NDB"])
        self.parametersPanel.cmbNavAidType2.addItems(["VOR", "NDB"])

    def iasChanged(self):
        try:
            self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots))
        except:
            raise ValueError("Value Invalid")
    def iasHelpShow(self):
        dlg = IasHelpDlg()
        dlg.exec_()
    def changeCategory(self):
        if self.parametersPanel.cmbAircraftCategory_2.currentIndex() == AircraftSpeedCategory.A:
            self.parametersPanel.txtIas.setText(str(Speed(150).Knots))
            return
        elif self.parametersPanel.cmbAircraftCategory_2.currentIndex() == AircraftSpeedCategory.B:
            self.parametersPanel.txtIas.setText(str(Speed(180).Knots))
            return
        elif self.parametersPanel.cmbAircraftCategory_2.currentIndex() == AircraftSpeedCategory.C:
            self.parametersPanel.txtIas.setText(str(Speed(240).Knots))
            return
        elif self.parametersPanel.cmbAircraftCategory_2.currentIndex() == AircraftSpeedCategory.D:
            self.parametersPanel.txtIas.setText(str(Speed(250).Knots))
            return
        elif self.parametersPanel.cmbAircraftCategory_2.currentIndex() == AircraftSpeedCategory.E:
            self.parametersPanel.txtIas.setText(str(Speed(250).Knots))
            return
        elif self.parametersPanel.cmbAircraftCategory_2.currentIndex() == AircraftSpeedCategory.H:
            self.parametersPanel.txtIas.setText(str(Speed(250).Knots))
            return
    
    def method_31(self):
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
    def captureBearing(self):
        self.captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrack)
        define._canvas.setMapTool(self.captureTrackTool)
    def method_36(self, bool_0):
#         Point3d point3d;
#         Point3d point3d1;
#         Point3d point3d2;
#         Point3d point3d3;
#         Point3d point3d4;
#         double num;
        polylines = []
        point3d5 = self.parametersPanel.pnlWaypoint.Point3d
        value = float(self.parametersPanel.txtTrack.text())
        value1 = float(self.parametersPanel.txtRnpValue.text())
        speed = Speed(float(self.parametersPanel.txtIas.text()))
        altitude = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)
        num1 = float(self.parametersPanel.txtIsa.text())
        value2 = float(self.parametersPanel.txtTime.text())
        speed1 = Speed(float(self.parametersPanel.pnlWind.speedBox.text()))
        num = 15 if (altitude.Feet >= 24500) else 23
        speed2 = Speed.smethod_0(speed, num1, altitude)
        metresPerSecond = value2 * 60 * speed2.MetresPerSecond
        num2 = math.pow(speed2.Knots + speed1.Knots, 2) / (34313 * math.tan(Unit.ConvertDegToRad(num))) * 1852
        num3 = value1 * 1852
        num4 = num2 * (1 - math.sin(Unit.ConvertDegToRad(20))) / (2 * math.cos(Unit.ConvertDegToRad(20)))
        num5 = value1 * 1852 + 3704
        if (num5 < 9260):
            num5 = 9260
        point3d4 = MathHelper.distanceBearingPoint(point3d5, Unit.ConvertDegToRad(value + 90), num2 / 2) if (self.parametersPanel.cmbOrientation.currentText() != OrientationType.Left) else MathHelper.distanceBearingPoint(point3d5, Unit.ConvertDegToRad(value - 90), num2 / 2)
        point3d6 = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(value), num4)
        point3d7 = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(value + 180), metresPerSecond)
        num6 = num2 / 2 + 1.414 * num3
        num7 = num2 / 2 + num3
        point3d8 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(value), num6)
        point3d9 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(value + 90) - math.acos(num7 / num6), num6)
        point3d10 = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value + 90) + math.acos(num7 / num6), num6)
        point3d11 = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value + 180), num6);
        point3d12 = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value - 90) - math.acos(num7 / num6), num6)
        point3d13 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(value - 90) + math.acos(num7 / num6), num6)
        point3d = MathHelper.getIntersectionPoint(point3d9, MathHelper.distanceBearingPoint(point3d9, MathHelper.getBearing(point3d6, point3d9) - Unit.ConvertDegToRad(90), 100), point3d8, MathHelper.distanceBearingPoint(point3d8, Unit.ConvertDegToRad(value + 90), 100))
        point3d1 = MathHelper.getIntersectionPoint(point3d10, MathHelper.distanceBearingPoint(point3d10, MathHelper.getBearing(point3d7, point3d10) + Unit.ConvertDegToRad(90), 100), point3d11, MathHelper.distanceBearingPoint(point3d11, Unit.ConvertDegToRad(value + 90), 100))
        point3d2 = MathHelper.getIntersectionPoint(point3d12, MathHelper.distanceBearingPoint(point3d12, MathHelper.getBearing(point3d7, point3d12) - Unit.ConvertDegToRad(90), 100), point3d11, MathHelper.distanceBearingPoint(point3d11, Unit.ConvertDegToRad(value - 90), 100))
        point3d3 = MathHelper.getIntersectionPoint(point3d13, MathHelper.distanceBearingPoint(point3d13, MathHelper.getBearing(point3d6, point3d13) + Unit.ConvertDegToRad(90), 100), point3d8, MathHelper.distanceBearingPoint(point3d8, Unit.ConvertDegToRad(value - 90), 100))
        polylines1 = []
        if (bool_0):
            num8 = num2 / 2
            point3d14 = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(value + 90), num8)
            point3d15 = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value + 90), num8)
            point3d16 = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value - 90), num8)
            point3d17 = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(value - 90), num8)
            point3dArray = [point3d14, point3d15, point3d16, point3d17]
            polylineArea = PolylineArea(point3dArray)
#             for point3d0 in point3dArray:
#                 polyline.Add(point3d0)            
            polylineArea.method_19(1, MathHelper.smethod_57(TurnDirection.Right, point3d15, point3d16, point3d7))
            polylineArea.method_19(3, MathHelper.smethod_57(TurnDirection.Right, point3d17, point3d14, point3d4))
#             polyline.set_closed(True)
#             polyline.SetDatabaseDefaults()
            polylines1.append(polylineArea)
        point3dArray1 = [point3d9, point3d10, point3d12, point3d13]
        polylineArea1 = PolylineArea(point3dArray1)
#         for point3d0 in point3dArray1:
#             polyline1.Add(point3d0)
        polylineArea1.method_19(1, MathHelper.smethod_57(TurnDirection.Right, point3d10, point3d12, point3d7))
        polylineArea1.method_19(3, MathHelper.smethod_57(TurnDirection.Right, point3d13, point3d9, point3d6))
#         polylineArea1.set_closed(True)
#         polyline1.SetDatabaseDefaults();
        polylines1.append(polylineArea1)
        num9 = num5 / 5
        for i in range(1, 6):
            polylineArea0 = polylineArea1.getOffsetCurve(num9 * i )
            polylines1.append(polylineArea0)
            
#         try:
#             OffsetGapType offsetType = AcadHelper.OffsetType;
#             try
#             {
#                 AcadHelper.OffsetType = OffsetGapType.Extend;
#         num9 = num5 / 5
#         for i in range(4):
#             n = i + 1
#         point3dCollection = polyline1.GetOffsetCurves(5)
#         polyline0 = Polyline()
#         for point3d0 in point3dCollection:
#             polyline0.Add(point3d0)
#         polylines1.append(polyline0)
#         polylines = polylines1
#             }
#             finally
#             {
#                 AcadHelper.OffsetType = offsetType;
#             }
#         }
#         catch
#         {
#             foreach (Polyline polyline2 in polylines1)
#             {
#                 if (polyline2 == null)
#                 {
#                     continue;
#                 }
#                 polyline2.Dispose();
#             }
#             throw;
#         }
        return polylines1
class HoldingRnpArea:
    def __init__(self, polylineArea_0, altitude_0):
        self.area = PrimaryObstacleArea(polylineArea_0)
        self.moc = altitude_0.Metres
        self.altitude = altitude_0
    def method_0(self, obstacle_0):
        double_0 = self.moc * obstacle_0.MocMultiplier
        if (not self.area.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
            return (False, None, None)
        position = obstacle_0.Position
        double_1 = position.get_Z() + obstacle_0.Trees + double_0
        return (True, double_0, double_1)
class HoldingRnpObstacles(ObstacleTable):
    def __init__(self, surfacesList):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)
        
        self.surfaceType = SurfaceTypes.HoldingRnp
        self.obstaclesChecked = None
        self.surfacesList = surfacesList

    def setHiddenColumns(self, tableView):
        tableView.hideColumn(self.IndexObstArea)
        tableView.hideColumn(self.IndexDistInSecM)
        return ObstacleTable.setHiddenColumns(self, tableView)

    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        self.IndexMocAppliedM = fixedColumnCount 
        self.IndexMocAppliedFt = fixedColumnCount + 1
        self.IndexMocMultiplier = fixedColumnCount + 2
        self.IndexOcaM = fixedColumnCount + 3
        self.IndexOcaFt = fixedColumnCount + 4
        self.IndexCritical = fixedColumnCount + 5
                 
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
#     def method_11(self, obstacle_0, double_0, double_1, criticalObstacleType_0):
#         double0 = []
#         double0.append(double_0)#[self.IndexMocAppliedM] = double_0
# #         double0.append(Unit.ConvertMeterToFeet(double_0))#[self.IndexMocAppliedFt] = Unit.ConvertMeterToFeet(double_0)
# #         double0.append(ObstacleTable.method_1(double0))
#         double0.append(double_1)#[self.IndexOcaM] = double_1
# #         double0[self.IndexOcaFt] = Unit.ConvertMeterToFeet(double_1)
# #         double0[self.IndexCritical] = criticalObstacleType_0;
#         return ObstacleTable.method_1(double0)
    def checkObstacle(self, obstacle_0):
#         double num;
#         double num1;
        criticalObstacleType = CriticalObstacleType.No;
        for current in self.surfacesList:
            result, num, num1 = current.method_0
            if (result):
                if (num1 > current.altitude):
                    criticalObstacleType = CriticalObstacleType.Yes
                checkResult = []
                checkResult.append(num)
                checkResult.append(num1)
                checkResult.append(criticalObstacleType)
                self.addObstacleToModel(obstacle_0, checkResult)
                break
#                 self.method_11(obstacle_0, num, num1, criticalObstacleType)