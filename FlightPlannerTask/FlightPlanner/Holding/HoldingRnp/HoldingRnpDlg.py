# -*- coding: UTF-8 -*-
'''
Created on 30 Jun 2015

@author: Administrator
'''
from qgis.core import QGis, QgsVectorLayer, QgsGeometry, QgsFeature
from PyQt4.QtGui import QSizePolicy, QSpinBox, QLabel, QFileDialog, QFrame, QHBoxLayout, QFont, QStandardItem, QMessageBox
from PyQt4.QtCore import Qt, QCoreApplication, QSize


from FlightPlanner.types import Point3D, ConstructionType, CriticalObstacleType, ObstacleTableColumnType, OrientationType, TurnDirection
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.WindPanel import WindPanel
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.Holding.HoldingRnp.ui_HoldingRnpGeneral import Ui_HoldingRnpGeneral
from FlightPlanner.DataHelper import DataHelper

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import AircraftSpeedCategory, AltitudeUnits, SurfaceTypes
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.helpers import Speed, Altitude, MathHelper, Unit
from FlightPlanner.IasHelp.IasHelpDlg import IasHelpDlg
import define
import math

class HoldingRnpDlg(FlightPlanBaseDlg):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("HoldingRnp")
        self.surfaceType = SurfaceTypes.HoldingRnp
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.HoldingRnp)
                
        self.resize(540, 550)
        QgisHelper.matchingDialogSize(self, 710, 700)


        # point1 = Point3D(670765.834204, 6624159.01137)
        # point2 = Point3D(658888.622249, 6631328.51407)
        # point3 = Point3D(648258.512784, 6624159.01137)
        # b = MathHelper.smethod_60(point1, point2, point3)
        # pass

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
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.HoldingRnp, self.ui.tblObstacles, None, parameterList, resultHideColumnNames)
#         self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
    
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("Waypoint Position", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlWaypoint.txtPointX.text()), float(self.parametersPanel.pnlWaypoint.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlWaypoint.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlWaypoint.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlWaypoint.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlWaypoint.txtPointY.text()))
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("RNP Value", self.parametersPanel.txtRnpValue.text()))
        # parameterList.append(("Aircraft Category", self.parametersPanel.cmbAircraftCategory_2.currentText()))
        parameterList.append(("IAS", self.parametersPanel.txtIas.text() + "kts"))
        parameterList.append(("TAS", self.parametersPanel.txtTas.text() + "kts"))
        parameterList.append(("Altitude", self.parametersPanel.txtAltitudeM.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtAltitude.text() + "ft"))
        parameterList.append(("ISA", self.parametersPanel.txtIsa.text() + unicode("°C", "utf-8")))
        parameterList.append(("Wind", self.parametersPanel.pnlWind.speedBox.text() + "kts"))
        parameterList.append(("Time", self.parametersPanel.txtTime.text() + "min"))
        parameterList.append(("MOC", self.parametersPanel.txtMoc.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtMocFt.text() + "ft"))
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstruction.currentText()))
        
        
        parameterList.append(("Orientation", "group"))
        parameterList.append(("In-bound Trak", "Plan : " + str(self.parametersPanel.txtTrack.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtTrack.txtRadialGeodetic.Value) + define._degreeStr))

        # parameterList.append(("In-bound Trak", self.parametersPanel.txtTrack.Value + unicode("°", "utf-8")))
        parameterList.append(("Turns", self.parametersPanel.cmbOrientation.currentText()))
        
        parameterList.append(("Results / Checked Obstacles", "group"))   
        parameterList.append(("Checked Obstacles", "group"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        return parameterList
    def initObstaclesModel(self):
        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        self.obstaclesModel = HoldingRnpObstacles(self.surfaceList, Altitude(float(self.parametersPanel.txtMoc.text())), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
        
        return FlightPlanBaseDlg.initObstaclesModel(self)
    def btnEvaluate_Click(self):
        polylines = self.method_36(False)
#         polylines[0].Dispose();
#         polylines.RemoveAt(0);
        count = len(polylines)
        num = 0.1 * count
        altitudeMoc = Altitude(float(self.parametersPanel.txtMoc.text()), AltitudeUnits.M)
        metres = altitudeMoc.Metres
        holdingRnpAreas = []
        for i in range(count):
            if (i > 0):
                metres = num * altitudeMoc.Metres
                num = num - 0.1
            point3dCollection = polylines[i].method_14_closed(6)
            polylineArea0 = PolylineArea(point3dCollection)
            holdingRnpAreas.append(HoldingRnpArea(polylineArea0, Altitude(metres)))
        self.surfaceList = holdingRnpAreas
        return FlightPlanBaseDlg.btnEvaluate_Click(self)


    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        mapUnits = define._canvas.mapUnits()
        constructionLayer = None
        
        polylines = self.method_36(True)
        pollineAreaLineList, polylineAreaArcList, centerPolylineArea = self.method_36_Construct(True)
        if (self.parametersPanel.cmbConstruction.currentText() != ConstructionType.Construct3D):
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, centerPolylineArea, True)
            for polrlineArea in pollineAreaLineList:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polrlineArea)
            for polrlineArea in polylineAreaArcList:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polrlineArea)

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
            count = len(polylines)
            num = 0.1 * count
            altitude = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)
            value = Altitude(float(self.parametersPanel.txtMoc.text()), AltitudeUnits.M)
            metres = altitude.Metres - value.Metres
            for i in range(count):
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylines[len(polylines) - 1 - i], True)

#                 polygon1 = QgsGeometry.fromPolygon([polylines[i].method_14_closed(6)])
#                 polygonNew = polygon1
#                 if (i > 0):
#                     metres1 = altitude.Metres
# #                     value = self.pnlMoc.Value;
#                     metres = metres1 - num * value.Metres
#                     num = num - 0.1
#                 if (i > 0):
#                     polygon0 = QgsGeometry.fromPolygon([polylines[i - 1].method_14_closed(6)])
#                     polygonNew = polygon1.difference(polygon0)
#                 feature = QgsFeature()
#                 feature.setGeometry(polygonNew)
#                 constructionLayer.addFeature(feature)
#             constructionLayer.commitChanges()
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.HoldingRnp)
        self.resultLayerList = [constructionLayer]
        self.ui.btnEvaluate.setEnabled(True)

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
        pdtResultStr = ""
        K = round(171233 * math.pow(288 + float(self.parametersPanel.txtIsa.text()) - 0.00198 * Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT).Feet, 0.5)/(math.pow(288 - 0.00198 * Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT).Feet, 2.628)), 4)
        pdtResultStr = "1. K = \t" + str(K) + "\n"
        
        V = Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots
        pdtResultStr += "2. V = \t" + str(V) + "kt\n"
        
        v = V / 3600
        pdtResultStr += "3. v = \t" + str(v) + "NM/s\n"
        
        R = 509.26 / V
        pdtResultStr += "4. R = \t" + str(R)  + unicode("°/s", "utf-8") + "\n"     
        
        r = V / (62.83 * R) 
        pdtResultStr += "5. r = \t" + str(r) + "NM\n" 
        
        h = float(self.parametersPanel.txtAltitude.text()) / 1000
        pdtResultStr += "6. h = \t" + str(h) + "\n" 
        
        w = 2 * h + 47
        pdtResultStr += "7. w = \t" + str(w) + "kt\n" 
        
        wd = w / 3600
        pdtResultStr += "8. w' = \t" + str(wd) + "NM/s\n" 
        
        E45 = 45 * wd / R
        pdtResultStr += "9. E45' = \t" + str(E45) + "NM\n" 
        
        t = 60 * float(self.parametersPanel.txtTime.text())
        pdtResultStr += "10. t = \t" + str(t) + "s\n" 
        
        L = v * t
        pdtResultStr += "11. L = \t" + str(L) + "NM\n"
        
        ab = 5 * v
        pdtResultStr += "12. ab = \t" + str(ab) + "NM\n"
        
        ac = 11 * v
        pdtResultStr += "13. ac = \t" + str(ac) + "NM\n"
        
        gi1 = (t - 5) * v
        pdtResultStr += "14. gi1 = gi3 = \t" + str(gi1) + "NM\n"
        
        gi2 = (t + 21) * v
        pdtResultStr += "15. gi2 = gi4 = \t" + str(gi2) + "NM\n"
        
        Wb = 5 * wd
        pdtResultStr += "16. Wb = \t" + str(Wb) + "NM\n"
        
        Wc = 11 * wd
        pdtResultStr += "17. Wc = \t" + str(Wc) + "NM\n"
        
        Wd = Wc + E45
        pdtResultStr += "18. Wd = \t" + str(Wd) + "NM\n"
        
        We = Wc + 2 * E45
        pdtResultStr += "19. We = \t" + str(We) + "NM\n"
        
        Wf = Wc + 3 * E45
        pdtResultStr += "20. Wf = \t" + str(Wf) + "NM\n"
        
        Wg = Wc + 4 * E45
        pdtResultStr += "21. Wg = \t" + str(Wg) + "NM\n"
        
        Wh = Wb + 4 * E45
        pdtResultStr += "22. Wh = \t" + str(Wh) + "NM\n"
        
        Wo = Wb + 5 * E45
        pdtResultStr += "23. Wo = \t" + str(Wo) + "NM\n"
        
        Wp = Wb + 6 * E45
        pdtResultStr += "24. Wp = \t" + str(Wp) + "NM\n"
        
        Wi1 = (t + 6) * wd + 4 * E45
        pdtResultStr += "25. Wi1 = Wi3 = \t" + str(Wi1) + "NM\n"
        
        Wi2 = Wi1 + 14 * wd
        pdtResultStr += "26. Wi2 = Wi4 = \t" + str(Wi2) + "NM\n"
        
        Wj = Wi2 + E45
        pdtResultStr += "27. Wj = \t" + str(Wj) + "NM\n"
        
        Wk = Wi2 + 2 * E45        
        pdtResultStr += "28. Wk = Wi = \t" + str(Wk) + "NM\n"
        
        Wm = Wi2 + 3 * E45
        pdtResultStr += "29. Wm = \t" + str(Wm) + "NM\n"
        
        Wn3 = Wi1 + 4 * E45
        pdtResultStr += "30. Wn3 = \t" + str(Wn3) + "NM\n"
        
        Wn4 = Wi2 + 4 * E45
        pdtResultStr += "31. Wn4 = \t" + str(Wn4) + "NM\n"
        
        XE = 2 * r + (t + 15) * v + (t + 26 + 195 / R) * wd
        pdtResultStr += "32. XE = \t" + str(XE) + "NM\n"
        
        YE = 11 * v * math.cos(math.pi * 20 / 180) + r * (1 + math.sin(math.pi * 20 / 180)) + (t + 15) * v * math.tan(math.pi * 5 / 180) + (t + 26 + 125 / R) * wd
        pdtResultStr += "33. YE = \t" + str(YE) + "NM"
        
        
        
        QMessageBox.warning(self, "PDT Check", pdtResultStr)
    def initParametersPan(self):
        ui = Ui_HoldingRnpGeneral()
        self.parametersPanel = ui
        
        
        FlightPlanBaseDlg.initParametersPan(self)        
        self.parametersPanel.txtTas.setEnabled(False)
        self.parametersPanel.pnlWaypoint = PositionPanel(self.parametersPanel.holding)
        self.parametersPanel.pnlWaypoint.groupBox.setTitle("Waypoint Position")
        
        self.parametersPanel.pnlWaypoint.hideframe_Altitude()
        self.parametersPanel.pnlWaypoint.setObjectName("positionWaypoint")
        self.parametersPanel.pnlWaypoint.btnCalculater.hide()
        self.parametersPanel.verticalLayout.insertWidget(0,self.parametersPanel.pnlWaypoint)
        
        self.parametersPanel.pnlWind = WindPanel(self.parametersPanel.grbParameters)
        self.parametersPanel.vLayout_grbParameters.insertWidget(5, self.parametersPanel.pnlWind)
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
        
#         self.resize(460,600)
        self.parametersPanel.cmbConstruction.addItems(["2D", "3D"])
        self.parametersPanel.cmbAircraftCategory_2.addItems(["A", "B", "C", "D", "E", "H", "Custom"])
        self.parametersPanel.cmbOrientation.addItems([OrientationType.Left, OrientationType.Right])
#         self.parametersPanel.cmbOrientation.setCurrentIndex(1)
#         
#         '''Event Handlers Connect'''
#         
        self.parametersPanel.txtAltitude.textChanged.connect(self.method_31)
#         self.parametersPanel.cmbTurnLimitation.currentIndexChanged.connect(self.method_28)
#         self.parametersPanel.btnCaptureTrack.clicked.connect(self.captureBearing)
        self.parametersPanel.cmbAircraftCategory_2.currentIndexChanged.connect(self.changeCategory)
        self.parametersPanel.cmbAircraftCategory_2.setCurrentIndex(3)
        
        self.frame_8_1 = QFrame(self)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
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
        self.label_2_1.setMinimumSize(QSize(140, 16777215))
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
        self.parametersPanel.mocSpinBox.setMinimumSize(QSize(140, 16777215))
        
#         self.parametersPanel.mocSpinBox.setFixedWidth(100)
        self.horizontalLayout_10_1.addWidget(self.parametersPanel.mocSpinBox)
#         self.verticalLayout_9.addWidget(self.frame_8_1)
        
        self.parametersPanel.vLayout_grbParameters.addWidget(self.frame_8_1)
        self.parametersPanel.btnIasHelp.clicked.connect(self.iasHelpShow)
        self.parametersPanel.frame_ConstructionType_2.hide()
        
        self.parametersPanel.txtIas.textChanged.connect(self.iasChanged)
        self.parametersPanel.txtIsa.textChanged.connect(self.isaChanged)
#         self.parametersPanel.txtIsa.textChanged.connect(self.isaChanged)
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
        try:
            speed = Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
            self.parametersPanel.txtTas.setText(str(round(speed.Knots, 4)))
        except:
            raise ValueError("Value Invalid")
    # def captureBearing(self):
    #     self.captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrack)
    #     define._canvas.setMapTool(self.captureTrackTool)
    def method_36(self, bool_0):
        polylines = []
        point3d5 = self.parametersPanel.pnlWaypoint.Point3d
        value = float(self.parametersPanel.txtTrack.Value)
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
            polylineArea.method_19(1, -1)#MathHelper.smethod_57(TurnDirection.Right, point3d15, point3d16, point3d7))
            polylineArea.method_19(3, -1)#MathHelper.smethod_57(TurnDirection.Right, point3d17, point3d14, point3d4))
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
            # polylineArea1.pop(len(polylineArea1) -1)
            polylineArea0 = polylineArea1.getOffsetCurve(num9 * i , 4)
            polylines1.append(polylineArea0)
        return polylines1


    def method_36_Construct(self, bool_0):
        polylines = []
        point3d5 = self.parametersPanel.pnlWaypoint.Point3d
        value = float(self.parametersPanel.txtTrack.Value)
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
        polylineArea = None
        if (bool_0):
            num8 = num2 / 2
            point3d14 = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(value + 90), num8)
            point3d15 = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value + 90), num8)
            point3d16 = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value - 90), num8)
            point3d17 = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(value - 90), num8)
            point3dArray = [point3d14, point3d15, point3d16, point3d17]
            polylineArea = PolylineArea(point3dArray)
            polylineArea.method_19(1, -1)#MathHelper.smethod_57(TurnDirection.Right, point3d15, point3d16, point3d7))
            polylineArea.method_19(3, -1)#MathHelper.smethod_57(TurnDirection.Right, point3d17, point3d14, point3d4))
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

        polylineAreaLineList = [PolylineArea([polylineArea1[0].Position, polylineArea1[1].Position]), PolylineArea([polylineArea1[2].Position, polylineArea1[3].Position])]
        polylineAreaArc0 = PolylineArea()
        polylineAreaArc0.Add( polylineArea1[1])
        polylineAreaArc0.Add( PolylineAreaPoint(polylineArea1[2].Position))
        polylineAreaArc1 = PolylineArea()
        polylineAreaArc1.Add( polylineArea1[3])
        polylineAreaArc1.Add( PolylineAreaPoint(polylineArea1[0].Position))
        polylineAreaArcList = [polylineAreaArc0, polylineAreaArc1]
        num9 = num5 / 5
        polylineAreaArcListResult = []
        polylineAreaLineListResult = []
        for i in range(1, 6):
            polylineAreaL0 = polylineAreaLineList[0].getOffsetCurveNo(num9 * i , 4)
            polylineAreaLineListResult.append(polylineAreaL0)

            polylineAreaA0 = polylineAreaArcList[0].getOffsetCurveNo(num9 * i , 4)
            polylineAreaT = PolylineArea()
            polylineAreaT.Add(PolylineAreaPoint(polylineAreaA0[0].Position, MathHelper.smethod_60(polylineAreaA0[0].Position, polylineAreaA0[int(len(polylineAreaA0)/2)].Position, polylineAreaA0[len(polylineAreaA0) - 1].Position)))
            polylineAreaT.Add(PolylineAreaPoint(polylineAreaA0[len(polylineAreaA0) - 1].Position))
            polylineAreaArcListResult.append(polylineAreaT)

            polylineAreaL1 = polylineAreaLineList[1].getOffsetCurveNo(num9 * i , 4)
            polylineAreaLineListResult.append(polylineAreaL1)

            polylineAreaA1 = polylineAreaArcList[1].getOffsetCurveNo(num9 * i , 4)
            polylineAreaT = PolylineArea()
            polylineAreaT.Add(PolylineAreaPoint(polylineAreaA1[0].Position, MathHelper.smethod_60(polylineAreaA1[0].Position, polylineAreaA1[int(len(polylineAreaA1)/2)].Position, polylineAreaA1[len(polylineAreaA1) - 1].Position)))
            polylineAreaT.Add(PolylineAreaPoint(polylineAreaA1[len(polylineAreaA1) - 1].Position))
            polylineAreaArcListResult.append(polylineAreaT)

            polylineAreaLineListResult.append(PolylineArea([polylineAreaL0[len(polylineAreaL0)-1].Position, polylineAreaA0[0].Position]))
            polylineAreaLineListResult.append(PolylineArea([polylineAreaA0[len(polylineAreaA0)-1].Position, polylineAreaL1[0].Position]))
            polylineAreaLineListResult.append(PolylineArea([polylineAreaL1[len(polylineAreaL1)-1].Position, polylineAreaA1[0].Position]))
            polylineAreaLineListResult.append(PolylineArea([polylineAreaA1[len(polylineAreaA1)-1].Position, polylineAreaL0[0].Position]))

        return polylineAreaLineListResult, polylineAreaArcListResult, polylineArea
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
    def __init__(self, surfacesArea, altitude_0, altitude_1):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesArea)
        
        self.surfaceType = SurfaceTypes.HoldingRnp
        self.obstaclesChecked = None
        self.area = surfacesArea
        self.primaryMoc = altitude_0.Metres;
        self.enrouteAltitude = altitude_1.Metres;
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
            result, num, num1 = current.method_0(obstacle_0)
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