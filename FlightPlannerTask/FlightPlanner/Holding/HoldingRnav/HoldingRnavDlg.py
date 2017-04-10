# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QSize, Qt
from PyQt4.QtGui import QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsMapLayerRegistry,QgsCoordinateReferenceSystem,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType, SurfaceTypes, DistanceUnits,AircraftSpeedCategory, OrientationType, AltitudeUnits, ObstacleAreaResult
from FlightPlanner.Holding.HoldingRnav.ui_HoldingRnav import Ui_Form_HoldingRnav
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
from FlightPlanner.messages import Messages
from FlightPlanner.AcadHelper import AcadHelper
import define

class HoldingRnavDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("HoldingRnavDlg")
        self.surfaceType = SurfaceTypes.HoldingRnav
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.HoldingRnav)
        self.resize(540, 550)
        QgisHelper.matchingDialogSize(self, 720, 700)
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
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.HoldingRnav, self.ui.tblObstacles, None, parameterList, resultHideColumnNames)
#         self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
    
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("Waypoint", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlWaypoint.txtPointX.text()), float(self.parametersPanel.pnlWaypoint.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlWaypoint.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlWaypoint.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlWaypoint.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlWaypoint.txtPointY.text()))
        parameterList.append(("ATT", self.parametersPanel.pnlTolerances.txtAtt.text() + "nm"))
        parameterList.append(("XTT", self.parametersPanel.pnlTolerances.txtXtt.text() + "nm"))
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Holding Functionality Required", self.parametersPanel.cmbHoldingFunctionality.currentText()))
        if self.parametersPanel.cmbHoldingFunctionality.currentIndex() != 0:            
            parameterList.append(("Out-bound Red Limitation", self.parametersPanel.cmbOutboundLimit.currentText()))
        # parameterList.append(("Aircraft Category", self.parametersPanel.cmbAircraftCategory.currentText()))
        parameterList.append(("IAS", self.parametersPanel.txtIas.text() + "kts"))
        parameterList.append(("Altitude", self.parametersPanel.txtAltitudeM.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtAltitude.text() + "ft"))
        parameterList.append(("ISA", self.parametersPanel.txtIsa.text() + unicode("°C", "utf-8")))
        if self.parametersPanel.cmbHoldingFunctionality.currentIndex() == 0:
            parameterList.append(("Length", self.parametersPanel.txtLength.text() + "nm"))
        else:
            if self.parametersPanel.cmbOutboundLimit.currentIndex() == 0:
                parameterList.append(("Time", self.parametersPanel.txtTime.text() + "min"))
            else:
                parameterList.append(("Distance", self.parametersPanel.txtDistance.text() + "nm"))
        parameterList.append(("Wind", self.parametersPanel.pnlWind.speedBox.text() + "kts"))
        parameterList.append(("MOC", self.parametersPanel.txtMoc.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtMocFt.text() + "ft"))
        if self.parametersPanel.chbCatH.isChecked():
            parameterList.append(("Cat.H(linear MOC reduction up to 2NM", "Checked"))
        else:
            parameterList.append(("Cat.H(linear MOC reduction up to 2NM", "Unchecked"))        
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstruction.currentText()))
        
        parameterList.append(("Entry Areas", "group"))
        if self.parametersPanel.cmbHoldingFunctionality.currentIndex() != 0 and self.parametersPanel.cmbOutboundLimit.currentIndex() != 0:
            if self.parametersPanel.chbSector1.isChecked():
                parameterList.append(("Sector 1", "Checked"))
            else:
                parameterList.append(("Sector 1", "Unchecked")) 
            
            if self.parametersPanel.chbSector2.isChecked():
                parameterList.append(("Sector 2", "Checked"))
            else:
                parameterList.append(("Sector 2", "Unchecked")) 
            
            if self.parametersPanel.chbSector3.isChecked():
                parameterList.append(("Sector 3", "Checked"))
            else:
                parameterList.append(("Sector 3", "Unchecked")) 
        else:
            if self.parametersPanel.chbIntercept.isChecked():
                parameterList.append(("70 Intercept", "Checked"))
            else:
                parameterList.append(("70 Intercept", "Unchecked")) 
            
            if self.parametersPanel.chbSectors12.isChecked():
                parameterList.append(("Sector 1_2", "Checked"))
            else:
                parameterList.append(("Sector 1_2", "Unchecked")) 
        
        parameterList.append(("Orientation", "group"))
        parameterList.append(("In-bound Track", "Plan : " + str(self.parametersPanel.txtTrack.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtTrack.txtRadialGeodetic.Value) + define._degreeStr))

        # parameterList.append(("In-bound Trak", self.parametersPanel.txtTrack.Value + unicode("°", "utf-8")))
        parameterList.append(("Turns", self.parametersPanel.cmbOrientation.currentText()))
        
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
        self.ui.tabCtrlGeneral.removeTab(2)
#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)
    
        
    def btnPDTCheck_Click(self):
        pdtResultStr = MathHelper.pdtCheckResultToString(float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), float(self.parametersPanel.txtIas.text()), float(self.parametersPanel.txtTime.text()))
#         pdtResultStr = ""
#         K = round(171233 * math.pow(288 + float(self.parametersPanel.txtIsa.text()) - 0.00198 * Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT).Feet, 0.5)/(math.pow(288 - 0.00198 * Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT).Feet, 2.628)), 4)
#         pdtResultStr = "1. K = \t" + str(K) + "\n"
#         
#         V = K * float(self.parametersPanel.txtIas.text())
#         pdtResultStr += "2. V = \t" + str(V) + "kt\n"
#         
#         v = V / 3600
#         pdtResultStr += "3. v = \t" + str(v) + "NM/s\n"
#         
#         R = 509.26 / V
#         pdtResultStr += "4. R = \t" + str(R)  + unicode("°/s", "utf-8") + "\n"     
#         
#         r = V / (62.83 * R) 
#         pdtResultStr += "5. r = \t" + str(r) + "NM\n" 
#         
#         h = float(self.parametersPanel.txtAltitude.text()) / 1000
#         pdtResultStr += "6. h = \t" + str(h) + "\n" 
#         
#         w = 2 * h + 47
#         pdtResultStr += "7. w = \t" + str(w) + "kt\n" 
#         
#         wd = w / 3600
#         pdtResultStr += "8. w' = \t" + str(wd) + "NM/s\n" 
#         
#         E45 = 45 * wd / R
#         pdtResultStr += "9. E45' = \t" + str(E45) + "NM\n" 
#         
#         t = 60 * float(self.parametersPanel.txtTime.text())
#         pdtResultStr += "10. t = \t" + str(t) + "s\n" 
#         
#         L = v * t
#         pdtResultStr += "11. L = \t" + str(L) + "NM\n"
#         
#         ab = 5 * v
#         pdtResultStr += "12. ab = \t" + str(ab) + "NM\n"
#         
#         ac = 11 * v
#         pdtResultStr += "13. ac = \t" + str(ac) + "NM\n"
#         
#         gi1 = (t - 5) * v
#         pdtResultStr += "14. gi1 = gi3 = \t" + str(gi1) + "NM\n"
#         
#         gi2 = (t + 21) * v
#         pdtResultStr += "15. gi2 = gi4 = \t" + str(gi2) + "NM\n"
#         
#         Wb = 5 * wd
#         pdtResultStr += "16. Wb = \t" + str(Wb) + "NM\n"
#         
#         Wc = 11 * wd
#         pdtResultStr += "17. Wc = \t" + str(Wc) + "NM\n"
#         
#         Wd = Wc + E45
#         pdtResultStr += "18. Wd = \t" + str(Wd) + "NM\n"
#         
#         We = Wc + 2 * E45
#         pdtResultStr += "19. We = \t" + str(We) + "NM\n"
#         
#         Wf = Wc + 3 * E45
#         pdtResultStr += "20. Wf = \t" + str(Wf) + "NM\n"
#         
#         Wg = Wc + 4 * E45
#         pdtResultStr += "21. Wg = \t" + str(Wg) + "NM\n"
#         
#         Wh = Wb + 4 * E45
#         pdtResultStr += "22. Wh = \t" + str(Wh) + "NM\n"
#         
#         Wo = Wb + 5 * E45
#         pdtResultStr += "23. Wo = \t" + str(Wo) + "NM\n"
#         
#         Wp = Wb + 6 * E45
#         pdtResultStr += "24. Wp = \t" + str(Wp) + "NM\n"
#         
#         Wi1 = (t + 6) * wd + 4 * E45
#         pdtResultStr += "25. Wi1 = Wi3 = \t" + str(Wi1) + "NM\n"
#         
#         Wi2 = Wi1 + 14 * wd
#         pdtResultStr += "26. Wi2 = Wi4 = \t" + str(Wi2) + "NM\n"
#         
#         Wj = Wi2 + E45
#         pdtResultStr += "27. Wj = \t" + str(Wj) + "NM\n"
#         
#         Wk = Wi2 + 2 * E45        
#         pdtResultStr += "28. Wk = Wi = \t" + str(Wk) + "NM\n"
#         
#         Wm = Wi2 + 3 * E45
#         pdtResultStr += "29. Wm = \t" + str(Wm) + "NM\n"
#         
#         Wn3 = Wi1 + 4 * E45
#         pdtResultStr += "30. Wn3 = \t" + str(Wn3) + "NM\n"
#         
#         Wn4 = Wi2 + 4 * E45
#         pdtResultStr += "31. Wn4 = \t" + str(Wn4) + "NM\n"
#         
#         XE = 2 * r + (t + 15) * v + (t + 26 + 195 / R) * wd
#         pdtResultStr += "32. XE = \t" + str(XE) + "NM\n"
#         
#         YE = 11 * v * math.cos(math.pi * 20 / 180) + r * (1 + math.sin(math.pi * 20 / 180)) + (t + 15) * v * math.tan(math.pi * 5 / 180) + (t + 26 + 125 / R) * wd
#         pdtResultStr += "33. YE = \t" + str(YE) + "NM"
        
        
        
        QMessageBox.warning(self, "PDT Check", pdtResultStr)
    def btnEvaluate_Click(self):
        
        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        polylineArea1 = self.method_38();
        
        if (self.isHoldingFunctionalityRequired):
            holdingTemplateRnav = HoldingTemplateRnav(self.parametersPanel.pnlWaypoint.Point3d, float(self.parametersPanel.txtTrack.Value), Speed(float(self.parametersPanel.txtIas.text())), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), Speed(float(self.parametersPanel.pnlWind.speedBox.text())), float(self.parametersPanel.txtIsa.text()), Distance(float(self.parametersPanel.txtLength.text()), DistanceUnits.NM), self.parametersPanel.cmbOrientation.currentText());
            self.parametersPanel.txtLength.setText(str(holdingTemplateRnav.D.NauticalMiles))
            polyLineAreaList = holdingTemplateRnav.vmethod_0(polylineArea1, self.parametersPanel.chbIntercept.isChecked(), self.parametersPanel.chbSectors12.isChecked());
        
        elif (self.parametersPanel.cmbOutboundLimit.currentIndex() != 0):
            holdingTemplateRnav = HoldingTemplateRnav(self.parametersPanel.pnlWaypoint.Point3d, float(self.parametersPanel.txtTrack.Value), Speed(float(self.parametersPanel.txtIas.text())), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), Speed(float(self.parametersPanel.pnlWind.speedBox.text())), float(self.parametersPanel.txtIsa.text()), Distance(float(self.parametersPanel.txtDistance.text()), DistanceUnits.NM), self.parametersPanel.cmbOrientation.currentText(), self.parametersPanel.pnlTolerances.XTT, self.parametersPanel.pnlTolerances.ATT);
            self.parametersPanel.txtDistance.setText(str(holdingTemplateRnav.WD.NauticalMiles))
            polyLineAreaList = holdingTemplateRnav.vmethod_1(polylineArea1, self.parametersPanel.chbSector1.isChecked(), self.parametersPanel.chbSector2.isChecked(), self.parametersPanel.chbSector3.isChecked());
        else:
            holdingTemplateRnav = HoldingTemplate(self.parametersPanel.pnlWaypoint.Point3d, float(self.parametersPanel.txtTrack.Value), Speed(float(self.parametersPanel.txtIas.text())), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), Speed(float(self.parametersPanel.pnlWind.speedBox.text())), float(self.parametersPanel.txtIsa.text()), float(self.parametersPanel.txtTime.text()), self.parametersPanel.cmbOrientation.currentText());
            polyLineAreaList = holdingTemplateRnav.vmethod_0(polylineArea1, self.parametersPanel.chbIntercept.isChecked(), self.parametersPanel.chbSectors12.isChecked());
        
        altitude_0 = Distance(float(self.parametersPanel.txtAltitude.text()), DistanceUnits.FT)
        altitude_1 = Distance(float(self.parametersPanel.txtMoc.text()), DistanceUnits.M)
        distance_0 = Distance(2, DistanceUnits.NM)
        if not self.parametersPanel.chbCatH.isChecked():
            self.surfaceList = self.createHoldingRnavAreaList_Buffer(polyLineAreaList[0], Distance(float(self.parametersPanel.txtAltitude.text()), DistanceUnits.FT), Distance(float(self.parametersPanel.txtMoc.text()), DistanceUnits.M))
#             altitude = altitude_0.Metres;
            self.obstaclesModel = HoldingRnavObstacles(self.parametersPanel.chbCatH.isChecked(), "buffer", self.surfaceList, altitude_0)
        else:
            
            self.inner = PrimaryObstacleArea(polyLineAreaList[0]);
            self.outer = PrimaryObstacleArea(HoldingTemplateBase.smethod_5(polyLineAreaList[0], distance_0));
            
            polylineArea_0 = self.inner.previewArea
            polylineArea_1 = PolylineArea()
            if (not polylineArea_0.isCircle):
                for i in range(len(polylineArea_0)):
                    item = polylineArea_0[i];
                    x = item.Position.get_X();
                    position = item.Position;
                    polylineArea_1.Add(PolylineAreaPoint(Point3D(x, position.get_Y()), item.Bulge))
            else:
                point3d = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 0, polylineArea_0.Radius);
                point3d1 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 1.5707963267949, polylineArea_0.Radius);
                point3d2 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 3.14159265358979, polylineArea_0.Radius);
                point3d3 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 4.71238898038469, polylineArea_0.Radius);
                polylineArea_1.Add(PolylineAreaPoint(Point3D(point3d.get_X(), point3d.get_Y()), MathHelper.smethod_60(point3d, point3d1, point3d2)))
                polylineArea_1.Add(PolylineAreaPoint(Point3D(point3d2.get_X(), point3d2.get_Y()), MathHelper.smethod_60(point3d2, point3d3, point3d)))
                polylineArea_1.Add(PolylineAreaPoint(Point3D(point3d.get_X(), point3d.get_Y()), 0))
                
            self.poly = polylineArea_1
#             self.altitude = altitude_0.Metres;
#             self.moc = altitude_1.Metres;
#             self.offset = distance_0; 
            self.obstaclesModel = HoldingRnavObstacles(self.parametersPanel.chbCatH.isChecked(), "second", None, altitude_0, self.inner, self.outer, self.poly, altitude_1, distance_0)                     
        
        return FlightPlanBaseDlg.btnEvaluate_Click(self)

    def createHoldingRnavAreaList_Buffer(self, polylineArea_0, altitude_0, altitude_1):
        polylineAreaList = HoldingTemplateBase.smethod_1(polylineArea_0, False);
        areas = []
        count = len(polylineAreaList)
        num = 0.1 * count;
        metres = altitude_1.Metres;
        for i in range(count):
            if (i > 0):
                metres = num * altitude_1.Metres;
                num = num - 0.1;
            areas.append(HoldingRnavArea(polylineAreaList[i], Altitude(metres)))
        return areas
#         self.selectionArea = self.areas[self.areas.Count - 1].Area;
#         self.altitude = altitude_0.Metres;
            
    def btnConstruct_Click(self):
        # point3dNew0 = self.parametersPanel.pnlWaypoint.Point3d
        # pointNew1 = MathHelper.distanceBearingPoint(point3dNew0, Unit.ConvertDegToRad(float(self.parametersPanel.txtTrack.Value) + 90), 1000)
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        self.method_27()
        
        polylineArea3 = self.method_38();
        mapUnits = define._canvas.mapUnits()
        constructionLayer = None
        
        polyLineAreaList = []
        if (self.isHoldingFunctionalityRequired):
            holdingTemplateRnav = HoldingTemplateRnav(self.parametersPanel.pnlWaypoint.Point3d, float(self.parametersPanel.txtTrack.Value), Speed(float(self.parametersPanel.txtIas.text())), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), Speed(float(self.parametersPanel.pnlWind.speedBox.text())), float(self.parametersPanel.txtIsa.text()), Distance(float(self.parametersPanel.txtLength.text()), DistanceUnits.NM), self.parametersPanel.cmbOrientation.currentText());
            if holdingTemplateRnav.D.NauticalMiles != float(self.parametersPanel.txtLength.text()):
                if QMessageBox.warning(self,"Warning", Messages.INSUFFICIENT_LENGTH_OF_OUTBOUND_LEG%holdingTemplateRnav.D.NauticalMiles, QMessageBox.Ok | QMessageBox.Cancel) != QMessageBox.Ok:
                    return
            self.parametersPanel.txtLength.setText(str(holdingTemplateRnav.D.NauticalMiles))
            polyLineAreaList = holdingTemplateRnav.vmethod_0(polylineArea3, self.parametersPanel.chbIntercept.isChecked(), self.parametersPanel.chbSectors12.isChecked());
        
        elif (self.parametersPanel.cmbOutboundLimit.currentIndex() != 0):
            holdingTemplateRnav = HoldingTemplateRnav(self.parametersPanel.pnlWaypoint.Point3d, float(self.parametersPanel.txtTrack.Value), Speed(float(self.parametersPanel.txtIas.text())), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), Speed(float(self.parametersPanel.pnlWind.speedBox.text())), float(self.parametersPanel.txtIsa.text()), Distance(float(self.parametersPanel.txtDistance.text()), DistanceUnits.NM), self.parametersPanel.cmbOrientation.currentText(), self.parametersPanel.pnlTolerances.XTT, self.parametersPanel.pnlTolerances.ATT);
            if holdingTemplateRnav.WD.NauticalMiles != float(self.parametersPanel.txtDistance.text()):
                if QMessageBox.warning(self,"Warning", Messages.INSUFFICIENT_DISTANCE_FROM_WPT_TO_OUTBOUND_LEG%holdingTemplateRnav.WD.NauticalMiles, QMessageBox.Ok | QMessageBox.Cancel) != QMessageBox.Ok:
                    return
            self.parametersPanel.txtDistance.setText(str(holdingTemplateRnav.WD.NauticalMiles))
            polyLineAreaList = holdingTemplateRnav.vmethod_1(polylineArea3, self.parametersPanel.chbSector1.isChecked(), self.parametersPanel.chbSector2.isChecked(), self.parametersPanel.chbSector3.isChecked());
        else:
            holdingTemplateRnav = HoldingTemplate(self.parametersPanel.pnlWaypoint.Point3d, float(self.parametersPanel.txtTrack.Value), Speed(float(self.parametersPanel.txtIas.text())), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), Speed(float(self.parametersPanel.pnlWind.speedBox.text())), float(self.parametersPanel.txtIsa.text()), float(self.parametersPanel.txtTime.text()), self.parametersPanel.cmbOrientation.currentText());
            polyLineAreaList = holdingTemplateRnav.vmethod_0(polylineArea3, self.parametersPanel.chbIntercept.isChecked(), self.parametersPanel.chbSectors12.isChecked());
        
        if not self.parametersPanel.chbCatH.isChecked():
            polyLineAreaList.extend(HoldingTemplateBase.smethod_1(polyLineAreaList[0], True))
        else:
            polyLineAreaList.extend(HoldingTemplateBase.smethod_2(polyLineAreaList[0], Distance(2, DistanceUnits.NM)))
        if self.parametersPanel.cmbConstruction.currentIndex() != 0:
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Polygon)
            # if define._mapCrs == None:
            #     if mapUnits == QGis.Meters:
            #         constructionLayer = QgsVectorLayer("polygon?crs=EPSG:32633", self.surfaceType, "memory")
            #     else:
            #         constructionLayer = QgsVectorLayer("polygon?crs=EPSG:4326", self.surfaceType, "memory")
            # else:
            #     constructionLayer = QgsVectorLayer("polygon?crs=%s"%define._mapCrs.authid (), self.surfaceType, "memory")
            #
            # constructionLayer.startEditing()
            
            polylineArea_0 = holdingTemplateRnav.Nominal
            polylineArea_1 = PolylineArea()
            if (not polylineArea_0.isCircle):
                for i in range(len(polylineArea_0)):
                    item = polylineArea_0[i];
                    x = item.Position.get_X();
                    position = item.Position;
                    polylineArea_1.Add(PolylineAreaPoint(Point3D(x, position.get_Y()), item.Bulge))
            else:
                point3d = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 0, polylineArea_0.Radius);
                point3d1 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 1.5707963267949, polylineArea_0.Radius);
                point3d2 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 3.14159265358979, polylineArea_0.Radius);
                point3d3 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 4.71238898038469, polylineArea_0.Radius);
                polylineArea_1.Add(PolylineAreaPoint(Point3D(point3d.get_X(), point3d.get_Y()), MathHelper.smethod_60(point3d, point3d1, point3d2)))
                polylineArea_1.Add(PolylineAreaPoint(Point3D(point3d2.get_X(), point3d2.get_Y()), MathHelper.smethod_60(point3d2, point3d3, point3d)))
                polylineArea_1.Add(PolylineAreaPoint(Point3D(point3d.get_X(), point3d.get_Y()), 0))
                
            bulgeTemp = -1#(polylineArea_1[0].bulge + polylineArea_1[2].bulge) / 2
            polylineArea_1[0].bulge = bulgeTemp
            polylineArea_1[2].bulge = bulgeTemp
            # polyLineAreaList.insert(0, polylineArea_1)

            count = len(polyLineAreaList)
            
            # polyline1 = QgsGeometry.fromPolygon([polylineArea3.method_14_closed(4)])
            # feature = QgsFeature()
            # feature.setGeometry(polyline1)
            # constructionLayer.addFeature(feature)

            polygonList = []
            for i in range(count):
                polygonList.append(QgsGeometry.fromPolygon([polyLineAreaList[i].method_14_closed(4)]))
            for i in range(count):
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polyLineAreaList[len(polyLineAreaList) - 1 - i])
            if polylineArea_0.isCircle:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea_0)
            else:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea_1, True)

            #     polygon1 = polygonList[len(polygonList) - 1 - i]
            #     feature = QgsFeature()
            #     feature.setGeometry(polygon1)
            #     constructionLayer.addFeature(feature)
            #
            # constructionLayer.commitChanges()
        else:
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType)
            # if define._mapCrs == None:
            #     if mapUnits == QGis.Meters:
            #         constructionLayer = QgsVectorLayer("linestring?crs=EPSG:32633", self.surfaceType, "memory")
            #     else:
            #         constructionLayer = QgsVectorLayer("linestring?crs=EPSG:4326", self.surfaceType, "memory")
            # else:
            #     constructionLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), self.surfaceType, "memory")

            polylineArea_0 = holdingTemplateRnav.Nominal
            polylineArea_1 = PolylineArea()
            if (not polylineArea_0.isCircle):
                for i in range(len(polylineArea_0)):
                    item = polylineArea_0[i];
                    x = item.Position.get_X();
                    position = item.Position;
                    polylineArea_1.Add(PolylineAreaPoint(Point3D(x, position.get_Y()), item.Bulge))
            else:
                point3d = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 0, polylineArea_0.Radius);
                point3d1 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 1.5707963267949, polylineArea_0.Radius);
                point3d2 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 3.14159265358979, polylineArea_0.Radius);
                point3d3 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 4.71238898038469, polylineArea_0.Radius);
                polylineArea_1.Add(PolylineAreaPoint(Point3D(point3d.get_X(), point3d.get_Y()), MathHelper.smethod_60(point3d, point3d1, point3d2)))
                polylineArea_1.Add(PolylineAreaPoint(Point3D(point3d2.get_X(), point3d2.get_Y()), MathHelper.smethod_60(point3d2, point3d3, point3d)))
                polylineArea_1.Add(PolylineAreaPoint(Point3D(point3d.get_X(), point3d.get_Y()), 0))

            bulgeTemp = -1#(polylineArea_1[0].bulge + polylineArea_1[2].bulge) / 2
            polylineArea_1[0].bulge = bulgeTemp
            polylineArea_1[2].bulge = bulgeTemp
            # polyLineAreaList.append(polylineArea_1)
            if polylineArea_0.isCircle:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea_0)
            else:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea_1, True)


            polyLineAreaList.append(polylineArea3)
            constructionLayer.startEditing()
            for polylineArea in polyLineAreaList:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea, True)

                # polyline1 = QgsGeometry.fromPolyline(polylineArea.method_14_closed(4))
                # feature = QgsFeature()
                # feature.setGeometry(polyline1)
                # constructionLayer.addFeature(feature)
            # feature = QgsFeature()
            # feature.setGeometry(QgsGeometry.fromPolyline([pointNew1, point3dNew0]))
            # constructionLayer.addFeature(feature)
            # constructionLayer.commitChanges()
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.HoldingRnav)
        self.resultLayerList = [constructionLayer]
        # QgisHelper.zoomToLayers([constructionLayer])
        self.ui.btnEvaluate.setEnabled(True)

        
    def initParametersPan(self):
        ui = Ui_Form_HoldingRnav()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)
        
        self.parametersPanel.txtTas.setEnabled(False)
        self.parametersPanel.pnlWaypoint = PositionPanel(self.parametersPanel.gbWaypoint)
#         self.parametersPanel.pnlWaypoint.groupBox.setTitle("FAWP")
        self.parametersPanel.pnlWaypoint.btnCalculater.hide()
        self.parametersPanel.pnlWaypoint.hideframe_Altitude()
        self.parametersPanel.pnlWaypoint.setObjectName("pnlWaypoint")
        ui.vl_gbWaypoint.addWidget(self.parametersPanel.pnlWaypoint)
        self.connect(self.parametersPanel.pnlWaypoint, SIGNAL("positionChanged"), self.initResultPanel)
        
        self.parametersPanel.pnlTolerances = RnavTolerancesPanel(ui.gbWaypoint)
        self.parametersPanel.pnlTolerances.set_HasASW(False)        
        self.parametersPanel.pnlTolerances.set_Att(Distance(0.8, DistanceUnits.NM))
        self.parametersPanel.pnlTolerances.set_Xtt(Distance(1, DistanceUnits.NM))
        ui.vl_gbWaypoint.addWidget(self.parametersPanel.pnlTolerances)
        
        self.parametersPanel.pnlWind = WindPanel(self.parametersPanel.gbParameters)
        self.parametersPanel.pnlWind.lblIA.setMinimumSize(250, 0)
        self.parametersPanel.vl_gbParameters.insertWidget(7, self.parametersPanel.pnlWind)
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
               
        self.parametersPanel.cmbHoldingFunctionality.addItems([HoldingRnavFunctionalityRequiredType.Yes, HoldingRnavFunctionalityRequiredType.No])
        self.parametersPanel.cmbHoldingFunctionality.setCurrentIndex(1)
        self.parametersPanel.cmbAircraftCategory.addItems(["A", "B", "C", "D", "E", "H", "Custom"])
        self.parametersPanel.cmbOutboundLimit.addItems(["Time", "Distance From Waypoint"])
        self.parametersPanel.cmbConstruction.addItems(["2D", "3D"])
        self.parametersPanel.cmbOrientation.addItems(["Right", "Left"])
        
        self.parametersPanel.cmbAircraftCategory.setCurrentIndex(3)
        self.parametersPanel.frame_59.hide()
        
        self.frame_8_1 = QFrame(self)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.frame_8_1.setSizePolicy(sizePolicy)
        self.frame_8_1.setFrameShape(QFrame.StyledPanel)
        self.frame_8_1.setFrameShadow(QFrame.Raised)
        self.frame_8_1.setObjectName("frame_8")
        self.horizontalLayout_10_1 = QHBoxLayout(self.frame_8_1)
        self.horizontalLayout_10_1.setAlignment(Qt.AlignHCenter)
        self.horizontalLayout_10_1.setSpacing(0)
        self.horizontalLayout_10_1.setMargin(0)
        self.horizontalLayout_10_1.setObjectName("horizontalLayout_10")
        self.label_2_1 = QLabel(self.frame_8_1)
        self.label_2_1.setMinimumSize(QSize(250, 16777215))
#         self.label_2_1.setFixedWidth(100)
        self.label_2_1.setText("MOCmultiplier")
        
        font = QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.label_2_1.setFont(font)
        self.label_2_1.setObjectName("label_2_1")
        self.horizontalLayout_10_1.addWidget(self.label_2_1)
        
        self.parametersPanel.mocSpinBox = QSpinBox(self.frame_8_1)
        self.parametersPanel.mocSpinBox.setFont(font)
        self.parametersPanel.mocSpinBox.setObjectName("mocSpinBox")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parametersPanel.mocSpinBox.sizePolicy().hasHeightForWidth())
        self.parametersPanel.mocSpinBox.setSizePolicy(sizePolicy)
        self.parametersPanel.mocSpinBox.setMinimum(1)
        self.parametersPanel.mocSpinBox.setMinimumSize(QSize(159, 16777215))
        
#         self.parametersPanel.mocSpinBox.setFixedWidth(100)
        self.horizontalLayout_10_1.addWidget(self.parametersPanel.mocSpinBox)
#         self.verticalLayout_9.addWidget(self.frame_8_1)
        
        self.parametersPanel.vl_gbParameters.addWidget(self.frame_8_1)
        
        self.parametersPanel.frame_Length.hide()
        self.parametersPanel.frame_Time.show()
        self.parametersPanel.frame_OutBoundLimit.show()
        self.parametersPanel.frame_Distance.hide()
        self.parametersPanel.chbSector1.setVisible(False)
        self.parametersPanel.chbSector2.setVisible(False)
        self.parametersPanel.chbSector3.setVisible(False)
        
        self.parametersPanel.cmbHoldingFunctionality.currentIndexChanged.connect(self.cmbHoldingFunctionalityCurrentIndexChanged)
        self.parametersPanel.cmbOutboundLimit.currentIndexChanged.connect(self.cmbOutboundLimitCurrentIndexChanged)
        # self.parametersPanel.btnCaptureTrack.clicked.connect(self.captureBearing)
        self.parametersPanel.btnCaptureDistance.clicked.connect(self.measureDistance)
        self.parametersPanel.btnCaptureLength.clicked.connect(self.measureLength)        
        self.parametersPanel.txtAltitude.textChanged.connect(self.altitudeChanged)
        self.parametersPanel.cmbAircraftCategory.currentIndexChanged.connect(self.changeCategory)
        self.parametersPanel.btnIasHelp.clicked.connect(self.iasHelpShow)
        self.parametersPanel.txtIas.textChanged.connect(self.iasChanged)
        self.parametersPanel.txtIsa.textChanged.connect(self.isaChanged)
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

        self.parametersPanel.txtMoc.textChanged.connect(self.txtMocMChanged)
        self.parametersPanel.txtMocFt.textChanged.connect(self.txtMocFtChanged)

        self.flag1 = 0
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtMocFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMoc.text())), 4)))
            except:
                self.parametersPanel.txtMocFt.setText("0.0")

        self.parametersPanel.txtTas.setText(str(round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots, 4)))
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
                self.parametersPanel.txtAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")
    def txtMocMChanged(self):
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtMocFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMoc.text())), 4)))
            except:
                self.parametersPanel.txtMocFt.setText("0.0")
    def txtMocFtChanged(self):
        if self.flag1==0:
            self.flag1=2;
        if self.flag1==1:
            self.flag1=0;
        if self.flag1==2:
            try:
                self.parametersPanel.txtMoc.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtMocFt.text())), 4)))
            except:
                self.parametersPanel.txtMoc.setText("0.0")
    def iasChanged(self):
        try:
            self.parametersPanel.txtTas.setText(str(round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots, 4)))
        except:
            raise ValueError("Value Invalid")
    def isaChanged(self):
        try:
            self.parametersPanel.txtTas.setText(str(round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots, 4)))
        except:
            raise ValueError("Value Invalid")    
    def iasHelpShow(self):
        dlg = IasHelpDlg()
        dlg.exec_()
    def altitudeChanged(self):
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
        try:
            self.parametersPanel.txtTas.setText(str(round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots, 4)))
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
        
        self.surfaceType = SurfaceTypes.HoldingRnav
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
                result, num, num1 = current.method_0(obstacle_0)
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