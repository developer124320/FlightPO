# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QSize, Qt,  QVariant
from PyQt4.QtGui import QColor,QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsCoordinateReferenceSystem,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, \
                QgsVectorFileWriter, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, \
                QgsSymbolV2, QgsRendererCategoryV2, QgsGeometry
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapToolPan
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType, SurfaceTypes, \
                 DistanceUnits,AircraftSpeedCategory, OrientationType, AltitudeUnits, \
                 ObstacleAreaResult, RnavFlightPhase, ConstructionType, RnavSpecification, IntersectionStatus,\
                 TurnDirection,RnavWaypointType, AngleUnits, OffsetGapType
from FlightPlanner.RnavTurningSegmentAnalyser.ui_RnavTurningSegmentAnalyser import Ui_RnavTurningSegmentAnalyser
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.BasicGNSS.rnavWaypoints import RnavWaypoints
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.AcadHelper import AcadHelper
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
from FlightPlanner.RnavTolerance0 import RnavGnssTolerance
from FlightPlanner.Captions import Captions
from FlightPlanner.BasicGNSS.windSpiral import WindSpiral
from qgis.core import QGis, QgsRectangle, QgsGeometry, QgsCsException, QgsPoint,\
        QgsFeatureRequest, QgsCoordinateTransform, QgsFeature, QgsVectorLayer


import define, math

class RnavTurningSegmentAnalyserDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("RnavTurningSegmentAnalyserDlg")
        self.surfaceType = SurfaceTypes.RnavTurningSegmentAnalyser
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.RnavTurningSegmentAnalyser)
        self.resize(540, 600)
        QgisHelper.matchingDialogSize(self, 720, 700)
        self.surfaceList = None
        self.manualPolygon = None

        self.mapToolPan = None
        self.toolSelectByPolygon = None

        self.accepted.connect(self.closed)
        self.rejected.connect(self.closed)

        self.wptLayer = None
        
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
            if self.parametersPanel.cmbPhaseOfFlight.currentIndex() != 0:
                parameterList.append(("Aerodrome Reference Point(ARP)", "group"))
                longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlArp.txtPointX.text()), float(self.parametersPanel.pnlArp.txtPointY.text()))
        
                parameterList.append(("Lat", self.parametersPanel.pnlArp.txtLat.Value))
                parameterList.append(("Lon", self.parametersPanel.pnlArp.txtLong.Value))
                parameterList.append(("X", self.parametersPanel.pnlArp.txtPointX.text()))
                parameterList.append(("Y", self.parametersPanel.pnlArp.txtPointY.text()))                                     
            
        parameterList.append(("Waypoint", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlWaypoint.txtPointX.text()), float(self.parametersPanel.pnlWaypoint.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlWaypoint.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlWaypoint.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlWaypoint.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlWaypoint.txtPointY.text()))
        
        parameterList.append(("Cat.H", str(self.parametersPanel.chbCatH.isChecked())))
        parameterList.append((self.parametersPanel.chbCircularArcs.text(), str(self.parametersPanel.chbCircularArcs.isChecked())))
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Selection Mode", self.parametersPanel.cmbSelectionMode.currentText()))
        parameterList.append(("In-bound Track", "Plan : " + str(self.parametersPanel.txtInbound.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtInbound.txtRadialGeodetic.Value) + define._degreeStr))

        # parameterList.append(("In-bound Track", self.parametersPanel.txtInbound.Value))
        parameterList.append(("Out-bound Track", "Plan : " + str(self.parametersPanel.txtOutbound.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtOutbound.txtRadialGeodetic.Value) + define._degreeStr))

        # parameterList.append(("Out-bound Track", self.parametersPanel.txtOutbound.Value))
        parameterList.append(("IAS", self.parametersPanel.txtIas.text() + "kts"))
        parameterList.append(("Altitude", self.parametersPanel.txtAltitude.text() + "ft"))
        parameterList.append(("ISA", self.parametersPanel.txtIsa.text()))
        parameterList.append(("Bank Angle", self.parametersPanel.txtBankAngle.text()))
        parameterList.append(("Wind", self.parametersPanel.pnlWind.speedBox.text() + "kts"))
        parameterList.append(("Primary Moc", self.parametersPanel.txtPrimaryMoc.text() + "m"))
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstructionType.currentText()))
        parameterList.append(("MOCmultipiler", str(self.parametersPanel.mocSpinBox.value())))
        if self.parametersPanel.cmbConstructionType.currentIndex() == 0:            
            parameterList.append(("Draw Waypoint Tolerance", str(self.parametersPanel.chbDrawTolerance.isChecked())))
        
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
        polylineArea = None;
        polylineArea1 = None;
        polylineArea2 = None;
        polylineArea3 = None;
        polylineArea4 = None;
        turnDirection = None;
        turnConstructionMethod = None;
        selectedArea = None;
        
        polylineAreaAAA, complexObstacleArea, turnDirection, turnConstructionMethod, polylineArea, polylineArea1, polylineArea2, polylineArea3, polylineArea4, point3dCollection = self.method_40();
        obstacleArea = complexObstacleArea.ObstacleArea;
        complexObstacleArea.ObstacleArea = None;
        
        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        self.obstaclesModel = RnavTurningSegmentObstacles(complexObstacleArea, Altitude(float(self.parametersPanel.txtPrimaryMoc.text())), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), self.manualPolygon );
            

        return FlightPlanBaseDlg.btnEvaluate_Click(self)

            
    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        point3dCollection = None;
        polylineArea = None;
        polylineArea1 = None;
        polylineArea2 = None;
        polylineArea3 = None;
        polylineArea4 = None;
        turnDirection = None;
        turnConstructionMethod = None;
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
        
        polylineAreaAAA, complexObstacleArea, turnDirection, turnConstructionMethod, polylineArea, polylineArea1, polylineArea2, polylineArea3, polylineArea4, point3dCollection = self.method_40()
        
        resultPointArrayList = []
        count = polylineArea1.Count;
        resultPointArrayList.append(PolylineArea.smethod_131(polylineArea1))
        resultPointArrayList.append(PolylineArea.smethod_131(polylineArea2))
        resultPointArrayList.append(PolylineArea.smethod_136(complexObstacleArea.ObstacleArea.previewArea, True))
        resultPointArrayList.append(PolylineArea.smethod_131(polylineArea4))
        if (self.parametersPanel.chbDrawTolerance.isChecked()):
            resultPointArrayList.append(PolylineArea.smethod_133(point3dCollection, True))
        constructionLayer = AcadHelper.createVectorLayer(self.surfaceType)
        for pointArray in resultPointArrayList:
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, pointArray)
        # if self.wptLayer != None:
        #     QgisHelper.removeFromCanvas(define._canvas, [self.wptLayer])
        self.wptLayer = self.WPT2Layer()
        if self.parametersPanel.cmbType.currentIndex() == 2:
            QgisHelper.appendToCanvas(define._canvas, [constructionLayer], self.surfaceType)
            self.resultLayerList = [constructionLayer]
        else:
            self.resultLayerList = [constructionLayer, self.wptLayer]
            QgisHelper.appendToCanvas(define._canvas, [constructionLayer, self.wptLayer], self.surfaceType)
        QgisHelper.zoomToLayers([constructionLayer])
        self.ui.btnEvaluate.setEnabled(True)
        self.manualEvent(self.parametersPanel.cmbSelectionMode.currentIndex())
        

    def outputResultMethod(self):
        self.manualPolygon = self.toolSelectByPolygon.polygonGeom
    def manualEvent(self, index):
        QgisHelper.ClearRubberBandInCanvas(define._canvas)
        self.manualPolygon  = None

        if index != 0:
            self.toolSelectByPolygon = RubberBandPolygon(define._canvas)
            define._canvas.setMapTool(self.toolSelectByPolygon)
            self.connect(self.toolSelectByPolygon, SIGNAL("outputResult"), self.outputResultMethod)
        else:
            self.mapToolPan = QgsMapToolPan(define._canvas)
            define._canvas.setMapTool(self.mapToolPan )
    
        
    def initParametersPan(self):
        ui = Ui_RnavTurningSegmentAnalyser()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)
        
        self.parametersPanel.pnlArp= PositionPanel(self.parametersPanel.gbGeneral)
        self.parametersPanel.pnlArp.groupBox.setTitle("Aerodrome Reference Point(ARP)")
        self.parametersPanel.pnlArp.btnCalculater.hide()
        self.parametersPanel.pnlArp.hideframe_Altitude()
        self.parametersPanel.pnlArp.setObjectName("pnlArp")
        ui.vl_gbGeneral.insertWidget(2, self.parametersPanel.pnlArp)
        
        self.parametersPanel.pnlWaypoint = PositionPanel(self.parametersPanel.gbWaypoint)
#         self.parametersPanel.pnlWaypoint.groupBox.setTitle("Waypoint 1")
        self.parametersPanel.pnlWaypoint.btnCalculater.hide()
        self.parametersPanel.pnlWaypoint.hideframe_Altitude()
        self.parametersPanel.pnlWaypoint.setObjectName("pnlWaypoint")
        ui.vLayoutGbWaypoint.addWidget(self.parametersPanel.pnlWaypoint)
#         self.connect(self.parametersPanel.pnlWaypoint, SIGNAL("positionChanged"), self.initResultPanel)
        
        self.parametersPanel.pnlTolerances = RnavTolerancesPanel(ui.gbGeneral)
        self.parametersPanel.pnlTolerances.set_Att(Distance(0.8, DistanceUnits.NM))
        self.parametersPanel.pnlTolerances.set_Xtt(Distance(1, DistanceUnits.NM))
        self.parametersPanel.pnlTolerances.set_Asw(Distance(2, DistanceUnits.NM))
        ui.vl_gbGeneral.insertWidget(2, self.parametersPanel.pnlTolerances)
        
        self.parametersPanel.pnlWind = WindPanel(self.parametersPanel.gbParameters)
        self.parametersPanel.vl_gbParameters.insertWidget(9, self.parametersPanel.pnlWind)
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
        
               
        self.parametersPanel.cmbSelectionMode.addItems(["Automatic", "Manual"])
        self.parametersPanel.cmbSelectionMode.currentIndexChanged.connect(self.manualEvent)
        self.parametersPanel.cmbConstructionType.addItems(["2D", "3D"])
        self.parametersPanel.cmbType.addItems(["Fly-By", "Fly-Over", "RF"])
        
#         self.parametersPanel.cmbRnavSpecification.currentIndexChanged.connect(self.method_33)
#         self.parametersPanel.cmbPhaseOfFlight.currentIndexChanged.connect(self.method_31)
#         self.parametersPanel.cmbConstructionType.currentIndexChanged.connect(self.method_31)
        
        self.parametersPanel.cmbRnavSpecification.addItems(["", "Rnav5", "Rnav2", "Rnav1", "Rnp4", "Rnp2", "Rnp1", "ARnp2", "ARnp1", "ARnp09", "ARnp08", "ARnp07", "ARnp06", "ARnp05", "ARnp04", "ARnp03", "RnpApch"])
        self.parametersPanel.txtAltitude.textChanged.connect(self.altitudeChanged)
        # self.parametersPanel.btnCaptureInboundTrack.clicked.connect(self.captureInboundTrack)
        # self.parametersPanel.btnCaptureOutboundTrack.clicked.connect(self.captureOutboundTrack)
        
        self.parametersPanel.cmbConstructionType.currentIndexChanged.connect(self.method_31)
        self.parametersPanel.cmbRnavSpecification.currentIndexChanged.connect(self.cmbRnavSpecificationChangeed)
        self.parametersPanel.cmbPhaseOfFlight.currentIndexChanged.connect(self.cmbPhaseOfFlightChanged)
        self.parametersPanel.chbCatH.clicked.connect(self.method_31)
        self.parametersPanel.cmbType.currentIndexChanged.connect(self.method_31)
        self.parametersPanel.txtAltitude.textChanged.connect(self.altitudeChanged)
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
                self.parametersPanel.txtPrimaryMocFt.setText(str(round(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtPrimaryMoc.text())), 4), 4)))
            except:
                self.parametersPanel.txtPrimaryMocFt.setText("0.0")


        self.method_31()

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

    def cmbRnavSpecificationChangeed(self):
        self.method_34(-1)
        self.method_35(-1)
        self.method_31()
    def cmbPhaseOfFlightChanged(self):
        self.method_35(-1)
        self.method_31()
    # def captureInboundTrack(self):
    #     captureInboundTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtInbound)
    #     define._canvas.setMapTool(captureInboundTrackTool)
    # def captureOutboundTrack(self):
    #     captureOutboundTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtOutbound)
    #     define._canvas.setMapTool(captureOutboundTrackTool)
    
    def altitudeChanged(self):
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
#         try:
#             self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots))
#         except:
#             raise ValueError("Value Invalid")
    def method_31(self):
        self.parametersPanel.framePhaseOfFlight.setVisible(self.parametersPanel.cmbRnavSpecification.currentIndex() > 0);
        self.parametersPanel.pnlArp.setVisible(False if (self.parametersPanel.cmbRnavSpecification.currentIndex() <= 0 or self.parametersPanel.cmbPhaseOfFlight.currentIndex() < 0) else self.phaseOfFlight != RnavFlightPhase.Enroute);
        self.parametersPanel.pnlTolerances.setVisible(self.parametersPanel.cmbRnavSpecification.currentIndex() < 1);
        self.parametersPanel.chbDrawTolerance.setVisible(self.parametersPanel.cmbConstructionType.currentText() == ConstructionType.Construct2D);
        self.parametersPanel.frameMoc_4.setVisible(False if (self.parametersPanel.cmbRnavSpecification.currentIndex() >= 1) else self.parametersPanel.cmbType.currentIndex() != 2);
        self.parametersPanel.frameMoc_3.setVisible(False if (self.parametersPanel.cmbRnavSpecification.currentIndex() >= 1) else self.parametersPanel.cmbType.currentIndex() != 2);
        if (not self.parametersPanel.chbCatH.isChecked()):
            self.parametersPanel.chbCircularArcs.setText(Captions.USE_CIRC_ARC_METHOD_30);
        else:
            self.parametersPanel.chbCircularArcs.setText(Captions.USE_CIRC_ARC_METHOD_60);
#         self.chbDrawTolerance.Visible = self.pnlConstructionType.Value == ConstructionType.Construct2D;
    def method_34(self, int_0):
        self.parametersPanel.cmbPhaseOfFlight.clear();
        if (self.parametersPanel.cmbRnavSpecification.currentIndex() > 0):
            self.parametersPanel.cmbPhaseOfFlight.addItems(["Enroute", "STAR"])
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
    def method_35(self, int_0):
        if (int_0 < 0):
            int_0 = self.parametersPanel.cmbType.currentIndex();
        self.parametersPanel.cmbType.clear();
        if (self.parametersPanel.cmbRnavSpecification.currentIndex() < 1):
            self.parametersPanel.cmbType.addItems(["Fly-By", "Fly-Over", "RF"]);
        elif (self.parametersPanel.cmbPhaseOfFlight.currentIndex() >= 0):
            if self.phaseOfFlight == RnavFlightPhase.Enroute:
                self.parametersPanel.cmbType.addItems(["Fly-By"])
            elif self.phaseOfFlight == RnavFlightPhase.STAR:
                self.parametersPanel.cmbType.addItems(["Fly-By", "Fly-Over", "RF"]);
        self.parametersPanel.cmbType.setCurrentIndex(max([0, min([int_0, self.parametersPanel.cmbType.count() - 1])]));
    def method_37(self, point3d_0, rnavGnssTolerance_0, double_0):
        aTT = rnavGnssTolerance_0.ATT;
        point3d = MathHelper.distanceBearingPoint(point3d_0, double_0, aTT.Metres);
        xTT = rnavGnssTolerance_0.XTT;
        point3d1 = MathHelper.distanceBearingPoint(point3d, double_0 + math.pi / 2, xTT.Metres);
        distance = rnavGnssTolerance_0.ATT;
        point3d2 = MathHelper.distanceBearingPoint(point3d1, double_0 + math.pi, distance.Metres * 2);
        aTT1 = rnavGnssTolerance_0.ATT;
        point3d3 = MathHelper.distanceBearingPoint(point3d_0, double_0, aTT1.Metres);
        xTT1 = rnavGnssTolerance_0.XTT;
        point3d4 = MathHelper.distanceBearingPoint(point3d3, double_0 - math.pi / 2, xTT1.Metres);
        distance1 = rnavGnssTolerance_0.ATT;
        point3d5 = MathHelper.distanceBearingPoint(point3d4, double_0 + math.pi, distance1.Metres * 2);
        point3dArray = [point3d1, point3d2, point3d5, point3d4];
        return Point3dCollection(point3dArray);
    def method_33(self):
        return self.parametersPanel.cmbType.currentIndex()
    
    
    def method_39(self, point3d_0, rnavGnssTolerance_0, double_0):
        aTT = rnavGnssTolerance_0.ATT;
        point3d = MathHelper.distanceBearingPoint(point3d_0, double_0, aTT.Metres);
        xTT = rnavGnssTolerance_0.XTT;
        point3d1 = MathHelper.distanceBearingPoint(point3d, double_0 + math.pi / 2, xTT.Metres);
        distance = rnavGnssTolerance_0.ATT;
        point3d2 = MathHelper.distanceBearingPoint(point3d1, double_0 + math.pi, distance.Metres * 2);
        aTT1 = rnavGnssTolerance_0.ATT;
        point3d3 = MathHelper.distanceBearingPoint(point3d_0, double_0, aTT1.Metres);
        xTT1 = rnavGnssTolerance_0.XTT;
        point3d4 = MathHelper.distanceBearingPoint(point3d3, double_0 - math.pi / 2, xTT1.Metres);
        distance1 = rnavGnssTolerance_0.ATT;
        point3d5 = MathHelper.distanceBearingPoint(point3d4, double_0 + math.pi, distance1.Metres * 2);
        point3dArray = [point3d1, point3d2, point3d5, point3d4];
        return Point3dCollection(point3dArray);
    
    def method_40(self):
        rnavGnssTolerance = None;
        point3d = self.parametersPanel.pnlWaypoint.Point3d;
        Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT));
        num = MathHelper.smethod_3(float(self.parametersPanel.txtInbound.Value));
        num1 = MathHelper.smethod_3(float(self.parametersPanel.txtOutbound.Value));
        rnavWaypointType = self.method_33();
        turnDirectionList = []
        polylineAreaAAA = PolylineArea()
        num2 = MathHelper.smethod_77(num, num1, AngleUnits.Degrees, turnDirectionList);
        turnDirection_0 = turnDirectionList[0];
        if (num2 > 120 and self.parametersPanel.cmbType.currentIndex() == 0):
            QMessageBox.warning(self, "Warning", Messages.ERR_COURSE_CHANGES_GREATER_THAN_120_NOT_ALLOWED)
#             throw new Exception(Messages.ERR_COURSE_CHANGES_GREATER_THAN_120_NOT_ALLOWED);
        num = MathHelper.smethod_4(Unit.ConvertDegToRad(num));
        num1 = MathHelper.smethod_4(Unit.ConvertDegToRad(num1));
        aircraftSpeedCategory = AircraftSpeedCategory.H if (self.parametersPanel.chbCatH.isChecked()) else AircraftSpeedCategory.C;
        if (self.parametersPanel.cmbRnavSpecification.currentIndex() <= 0):
            rnavGnssTolerance = RnavGnssTolerance(None, None, None, None, self.parametersPanel.pnlTolerances.XTT, self.parametersPanel.pnlTolerances.ATT, self.parametersPanel.pnlTolerances.ASW);
        else:
            rnavSpecification = self.rnavSpecification;
            rnavFlightPhase = self.phaseOfFlight;
            rnavGnssTolerance = RnavGnssTolerance(rnavSpecification, None, aircraftSpeedCategory,  rnavFlightPhase, Distance(MathHelper.calcDistance(point3d, self.parametersPanel.pnlArp.Point3d))) if (rnavFlightPhase != RnavFlightPhase.Enroute) else RnavGnssTolerance(rnavSpecification, None, aircraftSpeedCategory, rnavFlightPhase, Distance(50, DistanceUnits.NM));
        point3dCollection_0 = self.method_39(point3d, rnavGnssTolerance, num);
        if (num2 <= (60 if (aircraftSpeedCategory == AircraftSpeedCategory.H) else 30) and self.parametersPanel.chbCircularArcs.isChecked()):
            turnConstructionMethod_0 = TurnConstructionMethod.CircularArcs;
            
            complexObstacleArea, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4 = self.method_41(point3d, num, num1, rnavGnssTolerance, turnDirection_0)
            return (polylineAreaAAA, complexObstacleArea, turnDirection_0, turnConstructionMethod_0, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4, point3dCollection_0)
#             return self.method_41(point3d, num, num1, rnavGnssTolerance, (TurnDirection)((int)turnDirection_0), out polylineArea_0, out polylineArea_1, out polylineArea_2, out polylineArea_3, out polylineArea_4);
        if (rnavWaypointType == RnavWaypointType.RF):
            turnConstructionMethod_0 = TurnConstructionMethod.FixedRadius;
            complexObstacleArea, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4 = self.method_42(point3d, num, num1, rnavGnssTolerance, turnDirection_0)
            return (polylineAreaAAA, complexObstacleArea, turnDirection_0, turnConstructionMethod_0, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4, point3dCollection_0)
#             return self.method_42(point3d, num, num1, rnavGnssTolerance, (TurnDirection)((int)turnDirection_0), out polylineArea_0, out polylineArea_1, out polylineArea_2, out polylineArea_3, out polylineArea_4);
        turnConstructionMethod_0 = TurnConstructionMethod.BoundingCircles;
        polylineAreaAAA, complexObstacleArea, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4 = self.method_43(point3d, num, num1, rnavGnssTolerance, turnDirection_0)
        return (polylineAreaAAA, complexObstacleArea, turnDirection_0, turnConstructionMethod_0, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4, point3dCollection_0)
#         return self.method_43(point3d, num, num1, rnavGnssTolerance, (TurnDirection)((int)turnDirection_0), out polylineArea_0, out polylineArea_1, out polylineArea_2, out polylineArea_3, out polylineArea_4);

    def method_41(self, point3d_0, double_0, double_1, rnavGnssTolerance_0, turnDirection_0):
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        point3d3 = None;
        point3d4 = None;
        point3d5 = None;
        point3d6 = None;
        point3d7 = None;
        point3d8 = None;
        point3d9 = None;
        point3d10 = None;
        point3d11 = None;
        point3d12 = None;
        point3d13 = None;
        point3d14 = None;
        point3d15 = None;
        point3d16 = None;
        point3d17 = None;
        point3d18 = None;
        point3d19 = None;
        aTT = None;
        point3d0 = [];
        double0 = double_0;
        num = MathHelper.smethod_4(double0 - math.pi / 2);
        num1 = MathHelper.smethod_4(double0 + math.pi / 2);
        num2 = MathHelper.smethod_4(double0 + math.pi);
        double1 = double_1;
        num3 = MathHelper.smethod_4(double1 - math.pi / 2);
        num4 = MathHelper.smethod_4(double1 + math.pi / 2);
        num5 = MathHelper.smethod_4(double1 + math.pi);
        complexObstacleArea = ComplexObstacleArea();
        polylineArea_0 = PolylineArea();
        polylineArea_1 = PolylineArea();
        polylineArea_2 = PolylineArea();
        polylineArea_3 = PolylineArea();
        polylineArea_4 = PolylineArea();
        if (turnDirection_0 != TurnDirection.Right):
            aSW = rnavGnssTolerance_0.ASW;
            point3d9 = MathHelper.distanceBearingPoint(point3d_0, num1, aSW.Metres / 2);
            aTT = rnavGnssTolerance_0.ATT;
            point3d8 = MathHelper.distanceBearingPoint(point3d9, num2, aTT.Metres);
            aTT = rnavGnssTolerance_0.ASW;
            point3d10 = MathHelper.distanceBearingPoint(point3d_0, num4, aTT.Metres / 2);
            aTT = rnavGnssTolerance_0.ATT;
            point3d11 = MathHelper.distanceBearingPoint(point3d10, double1, aTT.Metres);
            aTT = rnavGnssTolerance_0.ASW;
            point3d13 = MathHelper.distanceBearingPoint(point3d_0, num1, aTT.Metres);
            aTT = rnavGnssTolerance_0.ATT;
            point3d12 = MathHelper.distanceBearingPoint(point3d13, num2, aTT.Metres);
            aTT = rnavGnssTolerance_0.ASW;
            point3d14 = MathHelper.distanceBearingPoint(point3d_0, num4, aTT.Metres);
            aTT = rnavGnssTolerance_0.ATT;
            point3d15 = MathHelper.distanceBearingPoint(point3d14, double1, aTT.Metres);
            aTT = rnavGnssTolerance_0.ATT;
            point3d20 = MathHelper.distanceBearingPoint(point3d10, num5, aTT.Metres);
            aTT = rnavGnssTolerance_0.ATT;
            point3d21 = MathHelper.distanceBearingPoint(point3d14, num5, aTT.Metres);
            point3d18 = MathHelper.getIntersectionPoint(point3d20, point3d21, point3d8, point3d12);
            aTT = rnavGnssTolerance_0.ASW;
            point3d22 = MathHelper.distanceBearingPoint(point3d_0, num, aTT.Metres / 2);
            aTT = rnavGnssTolerance_0.ASW;
            point3d23 = MathHelper.distanceBearingPoint(point3d_0, num, aTT.Metres);
            point3d = MathHelper.getIntersectionPoint(point3d20, point3d21, point3d22, MathHelper.distanceBearingPoint(point3d22, double0, 100));
            point3d4 = MathHelper.getIntersectionPoint(point3d20, point3d21, point3d23, MathHelper.distanceBearingPoint(point3d23, double0, 100));
            point3d1 = MathHelper.getIntersectionPoint(point3d10, point3d14, point3d22, MathHelper.distanceBearingPoint(point3d22, double0, 100));
            point3d5 = MathHelper.getIntersectionPoint(point3d10, point3d14, point3d23, MathHelper.distanceBearingPoint(point3d23, double0, 100));
            aTT = rnavGnssTolerance_0.ASW;
            point3d22 = MathHelper.distanceBearingPoint(point3d_0, num3, aTT.Metres / 2);
            aTT = rnavGnssTolerance_0.ASW;
            point3d23 = MathHelper.distanceBearingPoint(point3d_0, num3, aTT.Metres);
            point3d2 = MathHelper.getIntersectionPoint(point3d9, point3d13, point3d22, MathHelper.distanceBearingPoint(point3d22, double1, 100));
            point3d6 = MathHelper.getIntersectionPoint(point3d9, point3d13, point3d23, MathHelper.distanceBearingPoint(point3d23, double1, 100));
            aTT = rnavGnssTolerance_0.ATT;
            point3d20 = MathHelper.distanceBearingPoint(point3d9, double0, aTT.Metres);
            aTT = rnavGnssTolerance_0.ATT;
            point3d21 = MathHelper.distanceBearingPoint(point3d13, double0, aTT.Metres);
            point3d19 = MathHelper.getIntersectionPoint(point3d20, point3d21, point3d11, point3d15);
            point3d3 = MathHelper.getIntersectionPoint(point3d20, point3d21, point3d22, MathHelper.distanceBearingPoint(point3d22, double1, 100));
            point3d7 = MathHelper.getIntersectionPoint(point3d20, point3d21, point3d23, MathHelper.distanceBearingPoint(point3d23, double1, 100));
            point3d0 = [point3d12, point3d13, point3d14, point3d15];
            polylineArea_3.method_7(point3d0);
            polylineArea_3[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d13, point3d14, point3d_0);
            point3d0 = [point3d8, point3d9, point3d10, point3d11];
            polylineArea_2.method_7(point3d0);
            polylineArea_2[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d9, point3d10, point3d_0);
            point3d0 = [point3d4, point3d5, point3d6, point3d7];
            polylineArea_0.method_7(point3d0);
            point3d0 = [point3d, point3d1, point3d2, point3d3];
            polylineArea_1.method_7(point3d0);
            point3d20 = MathHelper.getIntersectionPoint(point3d, point3d4, point3d_0, MathHelper.distanceBearingPoint(point3d_0, num2, 100));
            point3d21 = MathHelper.getIntersectionPoint(point3d3, point3d7, point3d_0, MathHelper.distanceBearingPoint(point3d_0, double1, 100));
            point3d0 = [point3d20, point3d_0, point3d21];
            polylineArea_4.method_7(point3d0);
            polylineArea = PolylineArea();
            polylineArea.method_1(point3d18);
            polylineArea.method_8(polylineArea_3);
            polylineArea.method_1(point3d19);
            polylineArea.method_8(polylineArea_0.method_17());
            complexObstacleArea.ObstacleArea = PrimaryObstacleArea(polylineArea);
            polylineArea.clear();
            polylineArea.method_1(point3d18);
            polylineArea.method_8(polylineArea_2);
            polylineArea.method_1(point3d19);
            polylineArea.method_8(polylineArea_1.method_17());
            complexObstacleArea.Add(PrimaryObstacleArea(polylineArea));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d8, point3d9, point3d12, point3d13));
            point3d20 = MathHelper.smethod_93(turnDirection_0, point3d9, point3d10, point3d_0);
            point3d21 = MathHelper.smethod_93(turnDirection_0, point3d13, point3d14, point3d_0);
            complexObstacleArea.Add(SecondaryObstacleArea(point3d9, point3d20, point3d10, point3d13, None, point3d21, point3d14));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d10, point3d11, point3d14, point3d15));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d, point3d1, point3d4, point3d5));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d1, point3d2, point3d5, point3d6));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d2, point3d3, point3d6, point3d7));
        else:
            aTT = rnavGnssTolerance_0.ASW;
            point3d1 = MathHelper.distanceBearingPoint(point3d_0, num, aTT.Metres / 2);
            distance = rnavGnssTolerance_0.ATT;
            point3d = MathHelper.distanceBearingPoint(point3d1, num2, distance.Metres);
            aSW1 = rnavGnssTolerance_0.ASW;
            point3d2 = MathHelper.distanceBearingPoint(point3d_0, num3, aSW1.Metres / 2);
            aTT1 = rnavGnssTolerance_0.ATT;
            point3d3 = MathHelper.distanceBearingPoint(point3d2, double1, aTT1.Metres);
            distance1 = rnavGnssTolerance_0.ASW;
            point3d5 = MathHelper.distanceBearingPoint(point3d_0, num, distance1.Metres);
            aTT2 = rnavGnssTolerance_0.ATT;
            point3d4 = MathHelper.distanceBearingPoint(point3d5, num2, aTT2.Metres);
            aSW2 = rnavGnssTolerance_0.ASW;
            point3d6 = MathHelper.distanceBearingPoint(point3d_0, num3, aSW2.Metres);
            distance2 = rnavGnssTolerance_0.ATT;
            point3d7 = MathHelper.distanceBearingPoint(point3d6, double1, distance2.Metres);
            aTT3 = rnavGnssTolerance_0.ATT;
            point3d24 = MathHelper.distanceBearingPoint(point3d2, num5, aTT3.Metres);
            distance3 = rnavGnssTolerance_0.ATT;
            point3d25 = MathHelper.distanceBearingPoint(point3d6, num5, distance3.Metres);
            point3d16 = MathHelper.getIntersectionPoint(point3d24, point3d25, point3d, point3d4);
            aSW3 = rnavGnssTolerance_0.ASW;
            point3d26 = MathHelper.distanceBearingPoint(point3d_0, num1, aSW3.Metres / 2);
            aSW4 = rnavGnssTolerance_0.ASW;
            point3d27 = MathHelper.distanceBearingPoint(point3d_0, num1, aSW4.Metres);
            point3d8 = MathHelper.getIntersectionPoint(point3d24, point3d25, point3d26, MathHelper.distanceBearingPoint(point3d26, double0, 100));
            point3d12 = MathHelper.getIntersectionPoint(point3d24, point3d25, point3d27, MathHelper.distanceBearingPoint(point3d27, double0, 100));
            point3d9 = MathHelper.getIntersectionPoint(point3d2, point3d6, point3d26, MathHelper.distanceBearingPoint(point3d26, double0, 100));
            point3d13 = MathHelper.getIntersectionPoint(point3d2, point3d6, point3d27, MathHelper.distanceBearingPoint(point3d27, double0, 100));
            distance4 = rnavGnssTolerance_0.ASW;
            point3d26 = MathHelper.distanceBearingPoint(point3d_0, num4, distance4.Metres / 2);
            aSW5 = rnavGnssTolerance_0.ASW;
            point3d27 = MathHelper.distanceBearingPoint(point3d_0, num4, aSW5.Metres);
            point3d10 = MathHelper.getIntersectionPoint(point3d1, point3d5, point3d26, MathHelper.distanceBearingPoint(point3d26, double1, 100));
            point3d14 = MathHelper.getIntersectionPoint(point3d1, point3d5, point3d27, MathHelper.distanceBearingPoint(point3d27, double1, 100));
            aTT4 = rnavGnssTolerance_0.ATT;
            point3d24 = MathHelper.distanceBearingPoint(point3d1, double0, aTT4.Metres);
            aTT5 = rnavGnssTolerance_0.ATT;
            point3d25 = MathHelper.distanceBearingPoint(point3d5, double0, aTT5.Metres);
            point3d17 = MathHelper.getIntersectionPoint(point3d24, point3d25, point3d3, point3d7);
            point3d11 = MathHelper.getIntersectionPoint(point3d24, point3d25, point3d26, MathHelper.distanceBearingPoint(point3d26, double1, 100));
            point3d15 = MathHelper.getIntersectionPoint(point3d24, point3d25, point3d27, MathHelper.distanceBearingPoint(point3d27, double1, 100));
            point3d0 = [point3d4, point3d5, point3d6, point3d7 ];
            polylineArea_0.method_7(point3d0);
            polylineArea_0[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d5, point3d6, point3d_0);
            point3dArray = [point3d, point3d1, point3d2, point3d3];
            polylineArea_1.method_7(point3dArray);
            polylineArea_1[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d1, point3d2, point3d_0);
            point3dArray1 = [point3d12, point3d13, point3d14, point3d15];
            polylineArea_3.method_7(point3dArray1);
            point3dArray2 = [point3d8, point3d9, point3d10, point3d11];
            polylineArea_2.method_7(point3dArray2);
            point3d24 = MathHelper.getIntersectionPoint(point3d8, point3d12, point3d_0, MathHelper.distanceBearingPoint(point3d_0, num2, 100));
            point3d25 = MathHelper.getIntersectionPoint(point3d11, point3d15, point3d_0, MathHelper.distanceBearingPoint(point3d_0, double1, 100));
            point3d01 = [point3d24, point3d_0, point3d25];
            polylineArea_4.method_7(point3d01);
            polylineArea1 = PolylineArea();
            polylineArea1.method_1(point3d16);
            polylineArea1.method_8(polylineArea_0);
            polylineArea1.method_1(point3d17);
            polylineArea1.method_8(polylineArea_3.method_17());
            complexObstacleArea.ObstacleArea = PrimaryObstacleArea(polylineArea1);
            polylineArea1.clear();
            polylineArea1.method_1(point3d16);
            polylineArea1.method_8(polylineArea_1);
            polylineArea1.method_1(point3d17);
            polylineArea1.method_8(polylineArea_2.method_17());
            complexObstacleArea.Add(PrimaryObstacleArea(polylineArea1));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d, point3d1, point3d4, point3d5));
            point3d24 = MathHelper.smethod_93(turnDirection_0, point3d1, point3d2, point3d_0);
            point3d25 = MathHelper.smethod_93(turnDirection_0, point3d5, point3d6, point3d_0);
            complexObstacleArea.Add(SecondaryObstacleArea(point3d1, point3d24, point3d2, point3d5, None,  point3d25, point3d6));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d2, point3d3, point3d6, point3d7));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d8, point3d9, point3d12, point3d13));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d9, point3d10, point3d13, point3d14));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d10, point3d11, point3d14, point3d15));
        return (complexObstacleArea, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4);
    
    def method_42(self, point3d_0, double_0, double_1, rnavGnssTolerance_0, turnDirection_0):
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        point3d3 = None;
        point3d4 = None;
        point3d5 = None;
        point3d6 = None;
        point3d7 = None;
        point3d8 = None;
        point3d9 = None;
        aSW = None;
        point3d0 = None;
        double0 = double_0;
        num = MathHelper.smethod_4(double0 - math.pi / 2);
        num1 = MathHelper.smethod_4(double0 + math.pi / 2);
        num2 = MathHelper.smethod_4(double0 + math.pi);
        double1 = double_1;
        num3 = MathHelper.smethod_4(double1 - math.pi / 2);
        num4 = MathHelper.smethod_4(double1 + math.pi / 2);
        MathHelper.smethod_4(double1 + math.pi);
        speed = Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT));
        value = float(self.parametersPanel.txtBankAngle.text());
        knots = speed.Knots;
        value1 = self.parametersPanel.pnlWind.Value;
        num5 = Unit.ConvertNMToMeter(math.pow(knots + value1.Knots, 2) / (68626 * math.tan(Unit.ConvertDegToRad(value))));
        if (num5 < rnavGnssTolerance_0.ASW.Metres):
            obj = num5;
            aSW = rnavGnssTolerance_0.ASW;
            sss = str(aSW.Meters) + "m"
            QMessageBox.warning(self, "Warning", "The calculated radius of %f m cannot be smaller than 1/2 AW (%s)"%obj%sss)
#             throw new Exception(string.Format("The calculated radius of {0} m cannot be smaller than 1/2 AW ({1})", obj, aSW.method_0(":m")));
        num6 = MathHelper.smethod_76(double0, double1, AngleUnits.Radians);
        complexObstacleArea = ComplexObstacleArea();
        polylineArea_0 = PolylineArea();
        polylineArea_1 = PolylineArea();
        polylineArea_2 = PolylineArea();
        polylineArea_3 = PolylineArea();
        polylineArea_4 = PolylineArea();
        metres = rnavGnssTolerance_0.BV.Metres;
        aSW = rnavGnssTolerance_0.XTT;
        metres1 = num5 - (1.5 * aSW.Metres + metres);
        aSW = rnavGnssTolerance_0.XTT;
        metres2 = num5 - (0.75 * aSW.Metres + metres / 2);
        aSW = rnavGnssTolerance_0.XTT;
        metres3 = num5 + (0.75 * aSW.Metres + metres / 2 + 93);
        aSW = rnavGnssTolerance_0.XTT;
        metres4 = num5 + (1.5 * aSW.Metres + metres + 186);
        if (turnDirection_0 != TurnDirection.Right):
            point3d10 = MathHelper.distanceBearingPoint(point3d_0, num, num5);
            point3d11 = MathHelper.distanceBearingPoint(point3d10, num4, num5);
            aSW = rnavGnssTolerance_0.ATT;
            point3d12 = MathHelper.distanceBearingPoint(point3d_0, num2, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            point3d13 = MathHelper.distanceBearingPoint(point3d12, num, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            point3d14 = MathHelper.distanceBearingPoint(point3d12, num, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d15 = MathHelper.distanceBearingPoint(point3d12, num1, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d16 = MathHelper.distanceBearingPoint(point3d12, num1, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            point3d17 = MathHelper.distanceBearingPoint(point3d_0, num, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            point3d18 = MathHelper.distanceBearingPoint(point3d_0, num, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d19 = MathHelper.distanceBearingPoint(point3d_0, num1, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d20 = MathHelper.distanceBearingPoint(point3d_0, num1, aSW.Metres);
            point3d21 = point3d17;
            point3d22 = point3d18;
            point3d5_6 = []
            MathHelper.smethod_34(point3d15, point3d19, point3d10, metres3, point3d5_6);
            point3d5 = point3d5_6[0];
            point3d6 = point3d5_6[1];
            point3d5_7 = []
            MathHelper.smethod_34(point3d16, point3d20, point3d10, metres4, point3d5_7);
            point3d5 = point3d5_7[0]
            point3d7 = point3d5_7[1];
            aSW = rnavGnssTolerance_0.ASW;
            point3d23 = MathHelper.distanceBearingPoint(point3d11, num3, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            point3d24 = MathHelper.distanceBearingPoint(point3d11, num3, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d25 = MathHelper.distanceBearingPoint(point3d11, num4, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d26 = MathHelper.distanceBearingPoint(point3d11, num4, aSW.Metres);
            point3d12 = MathHelper.distanceBearingPoint(point3d11, double1, 500);
            aSW = rnavGnssTolerance_0.ASW;
            MathHelper.distanceBearingPoint(point3d12, num3, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            MathHelper.distanceBearingPoint(point3d12, num3, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d27 = MathHelper.distanceBearingPoint(point3d12, num4, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d28 = MathHelper.distanceBearingPoint(point3d12, num4, aSW.Metres);
            point3d29 = point3d23;
            point3d30 = point3d24;
            point3d5_8 = []
            MathHelper.smethod_34(point3d25, point3d27, point3d10, metres3, point3d5_8);
            point3d5 = point3d5_8[0]
            point3d8 = point3d5_8[1];
            point3d5_9 = []
            MathHelper.smethod_34(point3d26, point3d28, point3d10, metres4, point3d5_9)
            point3d5 = point3d5_9[0]
            point3d9 = point3d5_9[1];
            aSW = rnavGnssTolerance_0.ASW;
            point3d12 = MathHelper.distanceBearingPoint(point3d9, num3, aSW.Metres);
            aSW = rnavGnssTolerance_0.ATT;
            point3d12 = MathHelper.distanceBearingPoint(point3d12, double1, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            point3d31 = MathHelper.distanceBearingPoint(point3d12, num3, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            point3d32 = MathHelper.distanceBearingPoint(point3d12, num3, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d33 = MathHelper.distanceBearingPoint(point3d12, num4, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d34 = MathHelper.distanceBearingPoint(point3d12, num4, aSW.Metres);
            point3d0 = [point3d16, point3d7, point3d9, point3d34];
            polylineArea_0.method_7(point3d0);
            polylineArea_0[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d7, point3d9, point3d10);
            point3d0 = [point3d15, point3d6, point3d8, point3d33];
            polylineArea_1.method_7(point3d0);
            polylineArea_1[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d6, point3d8, point3d10);
            point3d0 = [point3d14, point3d22, point3d30, point3d32];
            polylineArea_2.method_7(point3d0);
            polylineArea_2[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d22, point3d30, point3d10);
            point3d0 = [point3d13, point3d21, point3d29, point3d31];
            polylineArea_3.method_7(point3d0);
            polylineArea_3[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d21, point3d29, point3d10);
            point3d0 = [point3d_0, point3d11];
            polylineArea_4.method_7(point3d0);
            polylineArea_4[0].Bulge = MathHelper.smethod_57(turnDirection_0, point3d_0, point3d11, point3d10);
            polylineArea = PolylineArea();
            point3d0 = [point3d16, point3d7, point3d9, point3d34, point3d31, point3d29, point3d21, point3d13];
            polylineArea.method_7(point3d0);
            polylineArea[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d7, point3d9, point3d10);
            polylineArea[5].Bulge = MathHelper.smethod_57(MathHelper.smethod_67(turnDirection_0), point3d29, point3d21, point3d10);
            complexObstacleArea.ObstacleArea = PrimaryObstacleArea(polylineArea);
            polylineArea = PolylineArea();
            point3d0 = [point3d15, point3d6, point3d8, point3d33, point3d32, point3d30, point3d22, point3d14];
            polylineArea.method_7(point3d0);
            polylineArea[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d6, point3d8, point3d10);
            polylineArea[5].Bulge = MathHelper.smethod_57(MathHelper.smethod_67(turnDirection_0), point3d30, point3d22, point3d10);
            complexObstacleArea.Add(PrimaryObstacleArea(polylineArea));
            point3d35 = MathHelper.distanceBearingPoint(point3d10, MathHelper.getBearing(point3d10, point3d_0) - num6 / 2, metres1);
            point3d36 = MathHelper.distanceBearingPoint(point3d10, MathHelper.getBearing(point3d10, point3d_0) - num6 / 2, metres2);
            point3d37 = MathHelper.distanceBearingPoint(point3d10, MathHelper.getBearing(point3d10, MathHelper.distanceBearingPoint(point3d8, MathHelper.getBearing(point3d8, point3d6), MathHelper.calcDistance(point3d8, point3d6) / 2)), metres3);
            point3d38 = MathHelper.distanceBearingPoint(point3d10, MathHelper.getBearing(point3d10, MathHelper.distanceBearingPoint(point3d9, MathHelper.getBearing(point3d9, point3d7), MathHelper.calcDistance(point3d9, point3d7) / 2)), metres4);
            complexObstacleArea.Add(SecondaryObstacleArea(point3d15, point3d6, point3d16, point3d7));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d14, point3d22, point3d13, point3d21));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d8, point3d33, point3d9, point3d34));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d30, point3d32, point3d29, point3d31));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d22, point3d36, point3d30, point3d21,None, point3d35, point3d29));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d6, point3d37, point3d8, point3d7, None, point3d38, point3d9));
        else:
            point3d39 = MathHelper.distanceBearingPoint(point3d_0, num1, num5);
            point3d40 = MathHelper.distanceBearingPoint(point3d39, num3, num5);
            aSW = rnavGnssTolerance_0.ATT;
            point3d41 = MathHelper.distanceBearingPoint(point3d_0, num2, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            point3d42 = MathHelper.distanceBearingPoint(point3d41, num1, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            point3d43 = MathHelper.distanceBearingPoint(point3d41, num1, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d44 = MathHelper.distanceBearingPoint(point3d41, num, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d45 = MathHelper.distanceBearingPoint(point3d41, num, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            point3d46 = MathHelper.distanceBearingPoint(point3d_0, num1, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            point3d47 = MathHelper.distanceBearingPoint(point3d_0, num1, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d48 = MathHelper.distanceBearingPoint(point3d_0, num, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d49 = MathHelper.distanceBearingPoint(point3d_0, num, aSW.Metres);
            point3d50 = point3d46;
            point3d51 = point3d47;
            point3d0_1 = []
            MathHelper.smethod_34(point3d44, point3d48, point3d39, metres3, point3d0_1)
            point3d = point3d0_1[0]
            point3d1 = point3d0_1[1];
            point3d0_2 = []
            MathHelper.smethod_34(point3d45, point3d49, point3d39, metres4, point3d0_2)
            point3d = point3d0_2[0]
            point3d2 = point3d0_2[1];
            aSW = rnavGnssTolerance_0.ASW;
            point3d52 = MathHelper.distanceBearingPoint(point3d40, num4, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            point3d53 = MathHelper.distanceBearingPoint(point3d40, num4, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d54 = MathHelper.distanceBearingPoint(point3d40, num3, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d55 = MathHelper.distanceBearingPoint(point3d40, num3, aSW.Metres);
            point3d41 = MathHelper.distanceBearingPoint(point3d40, double1, 500);
            aSW = rnavGnssTolerance_0.ASW;
            MathHelper.distanceBearingPoint(point3d41, num4, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            MathHelper.distanceBearingPoint(point3d41, num4, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d56 = MathHelper.distanceBearingPoint(point3d41, num3, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d57 = MathHelper.distanceBearingPoint(point3d41, num3, aSW.Metres);
            point3d58 = point3d52;
            point3d59 = point3d53;
            point3d0_3 = []
            MathHelper.smethod_34(point3d54, point3d56, point3d39, metres3, point3d0_3)
            point3d = point3d0_3[0]
            point3d3 = point3d0_3[1];
            point3d0_4 = []
            MathHelper.smethod_34(point3d55, point3d57, point3d39, metres4, point3d0_4)
            point3d = point3d0_4[0]
            point3d4 = point3d0_4[1];
            aSW = rnavGnssTolerance_0.ASW;
            point3d41 = MathHelper.distanceBearingPoint(point3d4, num4, aSW.Metres);
            aSW = rnavGnssTolerance_0.ATT;
            point3d41 = MathHelper.distanceBearingPoint(point3d41, double1, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            point3d60 = MathHelper.distanceBearingPoint(point3d41, num4, aSW.Metres);
            aSW = rnavGnssTolerance_0.ASW;
            point3d61 = MathHelper.distanceBearingPoint(point3d41, num4, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d62 = MathHelper.distanceBearingPoint(point3d41, num3, aSW.Metres / 2);
            aSW = rnavGnssTolerance_0.ASW;
            point3d63 = MathHelper.distanceBearingPoint(point3d41, num3, aSW.Metres);
            point3d0 = [point3d45, point3d2, point3d4, point3d63];
            polylineArea_0.method_7(point3d0);
            polylineArea_0[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d2, point3d4, point3d39);
            point3d0 = [point3d44, point3d1, point3d3, point3d62];
            polylineArea_1.method_7(point3d0);
            polylineArea_1[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d1, point3d3, point3d39);
            point3d0 = [point3d43, point3d51, point3d59, point3d61];
            polylineArea_2.method_7(point3d0);
            polylineArea_2[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d51, point3d59, point3d39);
            point3d0 = [point3d42, point3d50, point3d58, point3d60];
            polylineArea_3.method_7(point3d0);
            polylineArea_3[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d50, point3d58, point3d39);
            point3d0 = [point3d_0, point3d40 ];
            polylineArea_4.method_7(point3d0);
            polylineArea_4[0].Bulge = MathHelper.smethod_57(turnDirection_0, point3d_0, point3d40, point3d39);
            polylineArea1 = PolylineArea();
            point3d0 = [point3d45, point3d2, point3d4, point3d63, point3d60, point3d58, point3d50, point3d42];
            polylineArea1.method_7(point3d0);
            polylineArea1[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d2, point3d4, point3d39);
            polylineArea1[5].Bulge = MathHelper.smethod_57(MathHelper.smethod_67(turnDirection_0), point3d58, point3d50, point3d39);
            complexObstacleArea.ObstacleArea = PrimaryObstacleArea(polylineArea1);
            polylineArea1 = PolylineArea();
            point3d0 = [point3d44, point3d1, point3d3, point3d62, point3d61, point3d59, point3d51, point3d43];
            polylineArea1.method_7(point3d0);
            polylineArea1[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d1, point3d3, point3d39);
            polylineArea1[5].Bulge = MathHelper.smethod_57(MathHelper.smethod_67(turnDirection_0), point3d59, point3d51, point3d39);
            complexObstacleArea.Add(PrimaryObstacleArea(polylineArea1));
            point3d64 = MathHelper.distanceBearingPoint(point3d39, MathHelper.getBearing(point3d39, point3d_0) + num6 / 2, metres1);
            point3d65 = MathHelper.distanceBearingPoint(point3d39, MathHelper.getBearing(point3d39, point3d_0) + num6 / 2, metres2);
            point3d66 = MathHelper.distanceBearingPoint(point3d39, MathHelper.getBearing(point3d39, MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d3, point3d1), MathHelper.calcDistance(point3d3, point3d1) / 2)), metres3);
            point3d67 = MathHelper.distanceBearingPoint(point3d39, MathHelper.getBearing(point3d39, MathHelper.distanceBearingPoint(point3d4, MathHelper.getBearing(point3d4, point3d2), MathHelper.calcDistance(point3d4, point3d2) / 2)), metres4);
            complexObstacleArea.Add(SecondaryObstacleArea(point3d44, point3d1, point3d45, point3d2));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d43, point3d51, point3d42, point3d50));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d3, point3d62, point3d4, point3d63));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d59, point3d61, point3d58, point3d60));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d51, point3d65, point3d59, point3d50,None,  point3d64, point3d58));
            complexObstacleArea.Add(SecondaryObstacleArea(point3d1, point3d66, point3d3, point3d2,None, point3d67, point3d4));
        return (complexObstacleArea, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4);
    
    def method_43(self, point3d_0, double_0, double_1, rnavGnssTolerance_0, turnDirection_0):
        point3d = None;
        point3d1 = None;
        num = None;
        point3d2 = None;
        num1 = None;
        num2 = None;
        point3d3 = None;
        point3d4 = None;
        point3d5 = None;
        point3d6 = None;
        point3d7 = None;
        point3d8 = None;
        point3d9 = None;
        point3d10 = None;
        point3d11 = None;
        point3d12 = None;
        point3d13 = None;
        point3d14 = None;
        point3d15 = None;
        point3d16 = None;
        point3d17 = None;
        point3d18 = None;
        point3d19 = None;
        point3d20 = None;
        point3d21 = None;
        point3d22 = None;
        point3d23 = None;
        point3d24 = None;
        point3d25 = None;
        point3d26 = None;
        point3d27 = None;
        point3d28 = None;
        point3d29 = None;
        point3d30 = None;
        point3dArray = None;
        num3 = None;
        metresPerSecond = None;
        metresPerSecond1 = None;
        complexObstacleArea = ComplexObstacleArea();
        polylineArea_0 = PolylineArea();
        polylineArea_1 = PolylineArea();
        polylineArea_2 = PolylineArea();
        polylineArea_3 = PolylineArea();
        polylineArea_4 = PolylineArea();

        polylineAreaAAA = PolylineArea()
        rnavWaypointType = self.method_33();
        num4 = MathHelper.smethod_4(double_0);
        num5 = MathHelper.smethod_4(num4 + math.pi / 2);
        num6 = MathHelper.smethod_4(num4 - math.pi / 2);
        num7 = MathHelper.smethod_4(num4 + math.pi);
        num8 = MathHelper.smethod_4(double_1);
        num9 = MathHelper.smethod_4(num8 + math.pi / 2);
        num10 = MathHelper.smethod_4(num8 - math.pi / 2);
        num11 = MathHelper.smethod_4(num8 + math.pi);
        metres = rnavGnssTolerance_0.ASW.Metres;
        metres1 = rnavGnssTolerance_0.ATT.Metres;
        metres2 = rnavGnssTolerance_0.XTT.Metres;
        num12 = MathHelper.smethod_76(Unit.smethod_1(num4), Unit.smethod_1(num8), AngleUnits.Degrees);
        num13 = Unit.ConvertDegToRad(30);
        speed = Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT));
        value = self.parametersPanel.pnlWind.Value;
        value1 = float(self.parametersPanel.txtBankAngle.text());
        distance = Distance.smethod_0(speed, value1);
        metres3 = distance.Metres;
        distance = RnavWaypoints.getDistanceFromWaypointToEarliestTurningPoint(rnavWaypointType, Distance(metres1), Distance(metres3), num12, AngleUnits.Degrees);
        metres4 = distance.Metres;
        point3d = MathHelper.distanceBearingPoint(point3d_0, num7, math.fabs(metres4)) if (metres4 >= 0) else MathHelper.distanceBearingPoint(point3d_0, num4, math.fabs(metres4));
        distance = RnavWaypoints.getDistanceFromWaypointToLatestTurningPoint(rnavWaypointType, speed, value, float(self.parametersPanel.txtPilotTime.text()), float(self.parametersPanel.txtBankEstTime.text()), Distance(metres1), Distance(metres3), num12, AngleUnits.Degrees);
        metres5 = distance.Metres;
        point3d1 = MathHelper.distanceBearingPoint(point3d_0, num7, math.fabs(metres5)) if (metres5 >= 0) else MathHelper.distanceBearingPoint(point3d_0, num4, math.fabs(metres5));
        if (rnavWaypointType != RnavWaypointType.FlyBy):
            num14 = 0.6 * num12 if (num12 < 50) else 30;
            if (num12 < 50):
                num3 = 90 - num14;
                num1 = num3;
            else:
                num3 = 60;
            num1 = num3;
            distance = Distance.smethod_0(speed, 15);
            metres6 = distance.Metres;
            num15 = metres3 * math.sin(Unit.ConvertDegToRad(num12));
            num16 = metres3 * math.cos(Unit.ConvertDegToRad(num12)) * math.tan(Unit.ConvertDegToRad(num14));
            num17 = metres3 * ((1 - math.cos(Unit.ConvertDegToRad(num12)) / math.cos(Unit.ConvertDegToRad(num14))) / math.sin(Unit.ConvertDegToRad(num14)));
            num18 = metres6 * math.tan(Unit.ConvertDegToRad(num14 / 2));
            if (self.parametersPanel.chbCatH.isChecked()):
                metresPerSecond = 5 * speed.MetresPerSecond;
            else:
                metresPerSecond = 10 * speed.MetresPerSecond;
                num2 = metresPerSecond;
            num2 = metresPerSecond;
            point3d31 = MathHelper.distanceBearingPoint(point3d_0, num8, num15 + num16 + num17 + num18);
            if (turnDirection_0 != TurnDirection.Left):
                point3d3 = MathHelper.distanceBearingPoint(point3d_0, num4 + Unit.ConvertDegToRad(90), metres3);
                point3d5 = MathHelper.distanceBearingPoint(point3d3, num8 - Unit.ConvertDegToRad(num1), metres3);
                point3d4 = MathHelper.distanceBearingPoint(point3d31, num8 - Unit.ConvertDegToRad(90), metres6);
                point3d6 = MathHelper.distanceBearingPoint(point3d4, MathHelper.getBearing(point3d4, point3d31) + Unit.ConvertDegToRad(num14), metres6);
            else:
                point3d3 = MathHelper.distanceBearingPoint(point3d_0, num4 - Unit.ConvertDegToRad(90), metres3);
                point3d5 = MathHelper.distanceBearingPoint(point3d3, num8 + Unit.ConvertDegToRad(num1), metres3);
                point3d4 = MathHelper.distanceBearingPoint(point3d31, num8 + Unit.ConvertDegToRad(90), metres6);
                point3d6 = MathHelper.distanceBearingPoint(point3d4, MathHelper.getBearing(point3d4, point3d31) - Unit.ConvertDegToRad(num14), metres6);
            point3d32 = MathHelper.distanceBearingPoint(point3d31, num8, num2);
            polylineArea_4.Add(PolylineAreaPoint(point3d_0, MathHelper.smethod_57(turnDirection_0, point3d_0, point3d5, point3d3)));
            polylineArea_4.method_1(point3d5);
            if (turnDirection_0 == TurnDirection.Left):
                polylineArea_4.Add(PolylineAreaPoint(point3d6, MathHelper.smethod_57(TurnDirection.Right, point3d6, point3d31, point3d4)));
            elif (turnDirection_0 != TurnDirection.Right):
                polylineArea_4.method_1(point3d6);
            else:
                polylineArea_4.Add(PolylineAreaPoint(point3d6, MathHelper.smethod_57(TurnDirection.Left, point3d6, point3d31, point3d4)));
            polylineArea_4.method_1(point3d31);
            polylineArea_4.method_1(point3d32);
        else:
            num19 = metres3 * math.tan(Unit.ConvertDegToRad(num12 / 2));
            if (self.parametersPanel.chbCatH.isChecked()):
                metresPerSecond1 = 3 * speed.MetresPerSecond;
                num = metresPerSecond1;
            else:
                metresPerSecond1 = 5 * speed.MetresPerSecond;
                num = metresPerSecond1;
            num = metresPerSecond1;
            point3d33 = MathHelper.distanceBearingPoint(point3d_0, num7, num19);
            point3d34 = MathHelper.distanceBearingPoint(point3d33, num5, 100);
            point3d35 = MathHelper.distanceBearingPoint(point3d_0, num8, num19);
            point3d36 = MathHelper.distanceBearingPoint(point3d35, num9, 100);
            point3d2 = MathHelper.getIntersectionPoint(point3d33, point3d34, point3d35, point3d36);
            point3d33 = MathHelper.distanceBearingPoint(point3d_0, num7, num19 + num);
            point3d34 = MathHelper.distanceBearingPoint(point3d_0, num7, num19);
            point3d35 = MathHelper.distanceBearingPoint(point3d_0, num8, num19);
            point3d36 = MathHelper.distanceBearingPoint(point3d_0, num8, num19 + num);
            polylineArea_4.method_1(point3d33);
            polylineArea_4.Add(PolylineAreaPoint(point3d34, MathHelper.smethod_57(turnDirection_0, point3d34, point3d35, point3d2)));
            polylineArea_4.method_1(point3d35);
            polylineArea_4.method_1(point3d36);
        if (turnDirection_0 != TurnDirection.Right):
            windSpiral = WindSpiral(MathHelper.distanceBearingPoint(point3d1, num5, metres / 2), num4, speed, value, value1, TurnDirection.Left);
            windSpiral1 = WindSpiral(MathHelper.distanceBearingPoint(point3d1, num6, metres / 2), num4, speed, value, value1, TurnDirection.Left);
            polylineArea_2.method_1(MathHelper.distanceBearingPoint(point3d, num5, metres / 2));
            polylineArea_2.method_1(MathHelper.distanceBearingPoint(point3d1, num5, metres / 2));
            num20 = num8 - num13;
            point3d37 = windSpiral.method_0(num20, AngleUnits.Radians);
            point3d38 = windSpiral1.method_0(num20, AngleUnits.Radians);
            point3d39 = MathHelper.distanceBearingPoint(point3d_0, num9, metres / 2);
            point3d40 = MathHelper.distanceBearingPoint(point3d39, num8, 10000);
            if (windSpiral.method_1(point3d39, point3d40, True) or windSpiral1.method_1(point3d39, point3d40, True)):
                num21 = num6 if (num12 >= 90) else num8;
                if (not MathHelper.smethod_119(point3d38, point3d37, MathHelper.distanceBearingPoint(point3d37, num20, 1000))):
                    if (rnavWaypointType == RnavWaypointType.FlyBy):
                        point3d19 = MathHelper.distanceBearingPoint(windSpiral.Center[0], num5, windSpiral.Radius[0]);
                        polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, point3d19, windSpiral.Center[0]);
                        polylineArea_2.method_1(point3d19);
                        point3d41 = windSpiral.method_0(num21, AngleUnits.Radians);
                        point3d22 = MathHelper.getIntersectionPoint(point3d41, MathHelper.distanceBearingPoint(point3d41, num21, 100), point3d19, MathHelper.distanceBearingPoint(point3d19, num4, 100));
                        polylineArea_2.method_1(point3d22);
                        if (not MathHelper.smethod_117(point3d37, windSpiral.Center[0], windSpiral.Finish[0], False)):
                            polylineArea_2.method_3(point3d41, MathHelper.smethod_57(turnDirection_0, point3d41, point3d37, windSpiral.Center[0]));
                        else:
                            polylineArea_2.method_3(point3d41, MathHelper.smethod_57(turnDirection_0, point3d41, windSpiral.Finish[0], windSpiral.Center[0]));
                            polylineArea_2.method_3(windSpiral.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral.Start[1], point3d37, windSpiral.Center[1]));
                    elif (not MathHelper.smethod_117(point3d37, windSpiral.Center[0], windSpiral.Finish[0], False)):
                        polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, point3d37, windSpiral.Center[0]);
                    else:
                        polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, windSpiral.Finish[0], windSpiral.Center[0]);
                        polylineArea_2.method_3(windSpiral.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral.Start[1], point3d37, windSpiral.Center[1]));
                    polylineArea_2.method_1(point3d37);
                    point3d19 = MathHelper.getIntersectionPoint(point3d37, MathHelper.distanceBearingPoint(point3d37, num20, 100), point3d_0, MathHelper.distanceBearingPoint(point3d_0, num8, 100));
                    polylineArea_2.method_1(point3d19);
                else:
                    point3d42 = windSpiral.method_0(num6, AngleUnits.Radians);
                    point3d43 = windSpiral1.method_0(num6, AngleUnits.Radians);
                    if (rnavWaypointType != RnavWaypointType.FlyBy):
                        polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, windSpiral.Finish[0], windSpiral.Center[0]);
                        polylineArea_2.method_3(windSpiral.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral.Start[1], point3d42, windSpiral.Center[1]));
                        polylineArea_2.method_1(point3d42);
                    else:
                        point3d19 = MathHelper.distanceBearingPoint(windSpiral.Center[0], num5, windSpiral.Radius[0]);
                        polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, point3d19, windSpiral.Center[0]);
                        polylineArea_2.method_1(point3d19);
                        point3d44 = windSpiral.method_0(num21, AngleUnits.Radians);
                        point3d21 = MathHelper.getIntersectionPoint(point3d44, MathHelper.distanceBearingPoint(point3d44, num21, 100), point3d19, MathHelper.distanceBearingPoint(point3d19, num4, 100));
                        polylineArea_2.method_1(point3d21);
                        if (not MathHelper.smethod_117(point3d44, windSpiral.Center[0], windSpiral.Finish[0], False)):
                            polylineArea_2.method_3(point3d44, MathHelper.smethod_57(turnDirection_0, point3d44, windSpiral.Finish[0], windSpiral.Center[0]));
                            polylineArea_2.method_3(windSpiral.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral.Start[1], point3d42, windSpiral.Center[1]));
                            polylineArea_2.method_1(point3d42);
                        else:
                            polylineArea_2.method_3(point3d44, MathHelper.smethod_57(turnDirection_0, point3d44, point3d42, windSpiral.Center[1]));
                            polylineArea_2.method_1(point3d42);
                    point3d19 = MathHelper.getIntersectionPoint(point3d38, MathHelper.distanceBearingPoint(point3d38, num20, 100), point3d_0, MathHelper.distanceBearingPoint(point3d_0, num8, 100));
                    polylineArea_2.method_3(point3d43, MathHelper.smethod_57(turnDirection_0, point3d43, point3d38, windSpiral1.Center[1]));
                    polylineArea_2.method_1(point3d38);
                    polylineArea_2.method_1(point3d19);
            else:
                num22 = num8 + Unit.ConvertDegToRad(15);
                point3d45 = windSpiral.method_0(num22, AngleUnits.Radians);
                if (rnavWaypointType != RnavWaypointType.FlyBy):
                    if (not MathHelper.smethod_115(point3d45, windSpiral.Center[0], windSpiral.Finish[0])):
                        polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, point3d45, windSpiral.Center[0]);
                    else:
                        polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, windSpiral.Finish[0], windSpiral.Center[0]);
                        polylineArea_2.method_3(windSpiral.Finish[0], MathHelper.smethod_57(turnDirection_0, windSpiral.Finish[0], point3d45, windSpiral.Center[1]));
                    polylineArea_2.method_1(point3d45);
                    polylineArea_2.method_1(MathHelper.distanceBearingPoint(point3d45, num22, 10000));
                else:
                    point3d19 = MathHelper.distanceBearingPoint(windSpiral.Center[0], num5, windSpiral.Radius[0]);
                    polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, point3d19, windSpiral.Center[0]);
                    polylineArea_2.method_1(point3d19);
                    point3d46 = windSpiral.method_0(num8, AngleUnits.Radians);
                    point3d20 = MathHelper.getIntersectionPoint(point3d19, MathHelper.distanceBearingPoint(point3d19, num4, 100), point3d46, MathHelper.distanceBearingPoint(point3d46, num11, 100));
                    polylineArea_2.method_1(point3d20);
                    point3d19 = MathHelper.distanceBearingPoint(point3d45, num22, 10000);
                    point3d20 = MathHelper.getIntersectionPoint(point3d20, point3d46, point3d45, point3d19);
                    point3dArray = [point3d20, point3d19];
                    polylineArea_2.method_7(point3dArray);
            polylineArea_2.method_16();
            # polylineArea_2.reverse()
            polylineArea_2 = self.method_44(polylineArea_2, point3d39, point3d40);

            count = polylineArea_2.Count
            for i in range(count):
                if i + 1 == count:break
                if i != 0 and i + 1 != count:
                    if polylineArea_2[i].Position.get_X() == polylineArea_2[i-1].Position.get_X() and polylineArea_2[i].Position.get_X() == polylineArea_2[i+1].Position.get_X():
                        polylineArea_2.pop(i)
                        count -= 1

                        continue
                    if polylineArea_2[i].Position.get_Y() == polylineArea_2[i-1].Position.get_Y() and polylineArea_2[i].Position.get_Y() == polylineArea_2[i+1].Position.get_Y():
                        polylineArea_2.pop(i)
                        count -= 1
                        continue
            polylineArea_3 = polylineArea_2.method_23(-(metres / 2), OffsetGapType.Fillet, 0, 2, 2);
            # polylineArea_3333 = PolylineArea()
            # i = polylineArea_3.Count - 1
            # for polylineAreaPoint000 in polylineArea_3:
            #     polylineArea_3333.Add(polylineArea_3[i])
            #     i -=1
            # polylineArea_3 = polylineArea_3333
            #
            #
            # polylineArea_3333 = PolylineArea()
            # i = polylineArea_2.Count - 1
            # for polylineAreaPoint000 in polylineArea_2:
            #     polylineArea_3333.Add(polylineArea_2[i])
            #     i -=1
            # polylineArea_2 = polylineArea_3333
            # i=0
            # for item in polylineArea_2:
            #     polylineArea_3[i].set_Bulge(item.Bulge)
            #     i += 1


            polylineAreaAAA = PolylineArea([point3d39, point3d40])
            # for i in range(len(polylineArea_3_0), 0):
            #     polylineArea_3.Add(polylineArea_3_0[i])
            self.method_45(complexObstacleArea, polylineArea_2, polylineArea_3);
            polylineArea_3 = self.method_44(polylineArea_3, MathHelper.distanceBearingPoint(point3d39, num9, metres / 2), MathHelper.distanceBearingPoint(point3d40, num9, -metres / 2));
            point3d39 = MathHelper.distanceBearingPoint(point3d_0, num10, metres / 2);
            point3d40 = MathHelper.distanceBearingPoint(point3d39, num8, 1000);
            point3d47 = MathHelper.distanceBearingPoint(point3d_0, num10, metres);
            point3d48 = MathHelper.distanceBearingPoint(point3d47, num8, 1000);
            position = MathHelper.distanceBearingPoint(point3d, num6, metres / 2);
            position1 = MathHelper.distanceBearingPoint(point3d, num6, metres);
            if (MathHelper.smethod_119(position, point3d39, point3d40) and MathHelper.smethod_119(position1, point3d39, point3d40)):
                point3d49 = MathHelper.distanceBearingPoint(position1, num8 - Unit.ConvertDegToRad(15), 100);
                point3d23 = MathHelper.getIntersectionPoint(point3d39, point3d40, position1, point3d49);
                point3d24 = MathHelper.getIntersectionPoint(point3d47, point3d48, position1, point3d49);
                point3d50 = point3d23;
                point3d51 = MathHelper.distanceBearingPoint(point3d24, num9, metres / 2);
                complexObstacleArea.Add(SecondaryObstacleArea(point3d23, point3d51, point3d50, point3d24));
                point3dArray = [position1, point3d23, point3d51];
                polylineArea_1.method_7(point3dArray);
                point3dArray = [position1, point3d50, point3d24];
                polylineArea_0.method_7(point3dArray);
            elif (not MathHelper.smethod_115(position, point3d39, point3d40) or not MathHelper.smethod_119(position1, point3d47, point3d48)):
                num23 = num4 - Unit.ConvertDegToRad(num12 / 2);
                point3d52 = MathHelper.distanceBearingPoint(position, num23, 100);
                point3d53 = MathHelper.distanceBearingPoint(position1, num23, 100);
                point3d27 = MathHelper.getIntersectionPoint(point3d39, point3d40, position, point3d52);
                point3d28 = MathHelper.getIntersectionPoint(point3d47, point3d48, position1, point3d53);
                complexObstacleArea.Add(SecondaryObstacleArea(position, point3d27, position1, point3d28));
                point3dArray = [position, point3d27 ];
                polylineArea_1.method_7(point3dArray);
                point3dArray = [position1, point3d28];
                polylineArea_0.method_7(point3dArray);
            else:
                num24 = num4 - Unit.ConvertDegToRad(num12 / 2);
                point3d54 = MathHelper.distanceBearingPoint(position, num24, 100);
                point3d55 = MathHelper.distanceBearingPoint(position1, num8 - Unit.ConvertDegToRad(15), 100);
                point3d25 = MathHelper.getIntersectionPoint(point3d39, point3d40, position, point3d54);
                point3d26 = MathHelper.getIntersectionPoint(point3d47, point3d48, position1, point3d55);
                point3d56 = point3d26;
                point3d57 = MathHelper.distanceBearingPoint(point3d56, num9, -metres / 2);
                complexObstacleArea.Add(SecondaryObstacleArea(position, point3d25, position1, position1));
                complexObstacleArea.Add(SecondaryObstacleArea(point3d25, point3d57, position1, point3d26));
                point3dArray = [position, point3d25, point3d57];
                polylineArea_1.method_7(point3dArray);
                point3dArray = [position1, point3d26, point3d56];
                polylineArea_0.method_7(point3dArray);
            position2 = polylineArea_2[polylineArea_2.Count - 1].Position;
            point3d29 = MathHelper.getIntersectionPoint(position2, MathHelper.distanceBearingPoint(position2, num10, 1000), point3d39, point3d40);
            point3d30 = MathHelper.getIntersectionPoint(position2, MathHelper.distanceBearingPoint(position2, num10, 1000), point3d47, point3d48);
            position = polylineArea_1[polylineArea_1.Count - 1].Position;
            position1 = polylineArea_0[polylineArea_0.Count - 1].Position;
            if (MathHelper.smethod_121(position, point3d30, position2, False) and MathHelper.smethod_121(position1, point3d30, position2, False)):
                complexObstacleArea.Add(SecondaryObstacleArea(position, point3d29, position1, point3d30));
                polylineArea_1.method_1(point3d29);
                polylineArea_0.method_1(point3d30);
            polylineArea = PolylineArea();
            polylineArea.method_8(polylineArea_3);
            polylineArea.method_1(polylineArea_2[polylineArea_2.Count - 1].Position);
            polylineArea.method_1(polylineArea_1[polylineArea_1.Count - 1].Position);
            polylineArea.method_8(polylineArea_0.method_17());
            complexObstacleArea.ObstacleArea = PrimaryObstacleArea(polylineArea);
            polylineArea = PolylineArea();
            polylineArea.method_8(polylineArea_2);
            polylineArea.method_8(polylineArea_1.method_17());
            complexObstacleArea.Insert(0, PrimaryObstacleArea(polylineArea));
        else:
            windSpiral2 = WindSpiral(MathHelper.distanceBearingPoint(point3d1, num6, metres / 2), num4, speed, value, value1, TurnDirection.Right);
            windSpiral3 = WindSpiral(MathHelper.distanceBearingPoint(point3d1, num5, metres / 2), num4, speed, value, value1, TurnDirection.Right);
            polylineArea_1.method_1(MathHelper.distanceBearingPoint(point3d, num6, metres / 2));
            polylineArea_1.method_1(MathHelper.distanceBearingPoint(point3d1, num6, metres / 2));
            num25 = num8 + num13;
            point3d58 = windSpiral2.method_0(num25, AngleUnits.Radians);
            point3d59 = windSpiral3.method_0(num25, AngleUnits.Radians);
            point3d60 = MathHelper.distanceBearingPoint(point3d_0, num10, metres / 2);
            point3d61 = MathHelper.distanceBearingPoint(point3d60, num8, 10000);
            if (windSpiral2.method_1(point3d60, point3d61, True) or windSpiral3.method_1(point3d60, point3d61, True)):
                num26 = num5 if (num12 >= 90) else num8;
                if (not MathHelper.smethod_115(point3d59, point3d58, MathHelper.distanceBearingPoint(point3d58, num25, 1000))):
                    if (rnavWaypointType == RnavWaypointType.FlyBy):
                        point3d7 = MathHelper.distanceBearingPoint(windSpiral2.Center[0], num6, windSpiral2.Radius[0]);
                        polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, point3d7, windSpiral2.Center[0]);
                        polylineArea_1.method_1(point3d7);
                        point3d62 = windSpiral2.method_0(num26, AngleUnits.Radians);
                        point3d10 = MathHelper.getIntersectionPoint(point3d62, MathHelper.distanceBearingPoint(point3d62, num26, 100), point3d7, MathHelper.distanceBearingPoint(point3d7, num4, 100));
                        polylineArea_1.method_1(point3d10);
                        if (not MathHelper.smethod_121(point3d58, windSpiral2.Center[0], windSpiral2.Finish[0], False)):
                            polylineArea_1.method_3(point3d62, MathHelper.smethod_57(turnDirection_0, point3d62, point3d58, windSpiral2.Center[0]));
                        else:
                            polylineArea_1.method_3(point3d62, MathHelper.smethod_57(turnDirection_0, point3d62, windSpiral2.Finish[0], windSpiral2.Center[0]));
                            polylineArea_1.method_3(windSpiral2.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral2.Start[1], point3d58, windSpiral2.Center[1]));
                    elif (not MathHelper.smethod_121(point3d58, windSpiral2.Center[0], windSpiral2.Finish[0], False)):
                        polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, point3d58, windSpiral2.Center[0]);
                    else:
                        polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, windSpiral2.Finish[0], windSpiral2.Center[0]);
                        polylineArea_1.method_3(windSpiral2.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral2.Start[1], point3d58, windSpiral2.Center[1]));
                    polylineArea_1.method_1(point3d58);
                    point3d7 = MathHelper.getIntersectionPoint(point3d58, MathHelper.distanceBearingPoint(point3d58, num25, 100), point3d_0, MathHelper.distanceBearingPoint(point3d_0, num8, 100));
                    polylineArea_1.method_1(point3d7);
                else:
                    point3d63 = windSpiral2.method_0(num5, AngleUnits.Radians);
                    point3d64 = windSpiral3.method_0(num5, AngleUnits.Radians);
                    if (rnavWaypointType != RnavWaypointType.FlyBy):
                        polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, windSpiral2.Finish[0], windSpiral2.Center[0]);
                        polylineArea_1.method_3(windSpiral2.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral2.Start[1], point3d63, windSpiral2.Center[1]));
                        polylineArea_1.method_1(point3d63);
                    else:
                        point3d7 = MathHelper.distanceBearingPoint(windSpiral2.Center[0], num6, windSpiral2.Radius[0]);
                        polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, point3d7, windSpiral2.Center[0]);
                        polylineArea_1.method_1(point3d7);
                        point3d65 = windSpiral2.method_0(num26, AngleUnits.Radians);
                        point3d9 = MathHelper.getIntersectionPoint(point3d65, MathHelper.distanceBearingPoint(point3d65, num26, 100), point3d7, MathHelper.distanceBearingPoint(point3d7, num4, 100));
                        polylineArea_1.method_1(point3d9);
                        if (not MathHelper.smethod_121(point3d65, windSpiral2.Center[0], windSpiral2.Finish[0], False)):
                            polylineArea_1.method_3(point3d65, MathHelper.smethod_57(turnDirection_0, point3d65, windSpiral2.Finish[0], windSpiral2.Center[0]));
                            polylineArea_1.method_3(windSpiral2.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral2.Start[1], point3d63, windSpiral2.Center[1]));
                            polylineArea_1.method_1(point3d63);
                        else:
                            polylineArea_1.method_3(point3d65, MathHelper.smethod_57(turnDirection_0, point3d65, point3d63, windSpiral2.Center[1]));
                            polylineArea_1.method_1(point3d63);
                    point3d7 = MathHelper.getIntersectionPoint(point3d59, MathHelper.distanceBearingPoint(point3d59, num25, 100), point3d_0, MathHelper.distanceBearingPoint(point3d_0, num8, 100));
                    polylineArea_1.method_3(point3d64, MathHelper.smethod_57(turnDirection_0, point3d64, point3d59, windSpiral3.Center[1]));
                    polylineArea_1.method_1(point3d59);
                    polylineArea_1.method_1(point3d7);
            else:
                num27 = num8 - Unit.ConvertDegToRad(15);
                point3d66 = windSpiral2.method_0(num27, AngleUnits.Radians);
                if (rnavWaypointType != RnavWaypointType.FlyBy):
                    if (not MathHelper.smethod_119(point3d66, windSpiral2.Center[0], windSpiral2.Finish[0])):
                        polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, point3d66, windSpiral2.Center[0]);
                    else:
                        polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, windSpiral2.Finish[0], windSpiral2.Center[0]);
                        polylineArea_1.method_3(windSpiral2.Finish[0], MathHelper.smethod_57(turnDirection_0, windSpiral2.Finish[0], point3d66, windSpiral2.Center[1]));
                    polylineArea_1.method_1(point3d66);
                    polylineArea_1.method_1(MathHelper.distanceBearingPoint(point3d66, num27, 10000));
                else:
                    point3d7 = MathHelper.distanceBearingPoint(windSpiral2.Center[0], num6, windSpiral2.Radius[0]);
                    polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, point3d7, windSpiral2.Center[0]);
                    polylineArea_1.method_1(point3d7);
                    point3d67 = windSpiral2.method_0(num8, AngleUnits.Radians);
                    point3d8 = MathHelper.getIntersectionPoint(point3d7, MathHelper.distanceBearingPoint(point3d7, num4, 100), point3d67, MathHelper.distanceBearingPoint(point3d67, num11, 100));
                    polylineArea_1.method_1(point3d8);
                    point3d7 = MathHelper.distanceBearingPoint(point3d66, num27, 10000);
                    point3d8 = MathHelper.getIntersectionPoint(point3d8, point3d67, point3d66, point3d7);
                    point3dArray = [point3d8, point3d7];
                    polylineArea_1.method_7(point3dArray);
            polylineArea_1.method_16();
            polylineArea_1 = self.method_44(polylineArea_1, point3d60, point3d61);

            polylineAreaAAA = PolylineArea([point3d60, point3d61])

            polylineArea_0 = polylineArea_1.method_23(metres / 2, OffsetGapType.Fillet, 0, 2, 2);
            self.method_45(complexObstacleArea, polylineArea_1, polylineArea_0);
            polylineArea_0 = self.method_44(polylineArea_0, MathHelper.distanceBearingPoint(point3d60, num10, metres / 2), MathHelper.distanceBearingPoint(point3d61, num10, metres / 2));
            point3d60 = MathHelper.distanceBearingPoint(point3d_0, num9, metres / 2);
            point3d61 = MathHelper.distanceBearingPoint(point3d60, num8, 1000);
            point3d68 = MathHelper.distanceBearingPoint(point3d_0, num9, metres);
            point3d69 = MathHelper.distanceBearingPoint(point3d68, num8, 1000);
            position3 = MathHelper.distanceBearingPoint(point3d, num5, metres / 2);
            position4 = MathHelper.distanceBearingPoint(point3d, num5, metres);
            if (MathHelper.smethod_115(position3, point3d60, point3d61) and MathHelper.smethod_115(position4, point3d60, point3d61)):
                point3d70 = MathHelper.distanceBearingPoint(position4, num8 + Unit.ConvertDegToRad(15), 100);
                point3d11 = MathHelper.getIntersectionPoint(point3d60, point3d61, position4, point3d70);
                point3d12 = MathHelper.getIntersectionPoint(point3d68, point3d69, position4, point3d70);
                point3d71 = point3d11;
                point3d72 = MathHelper.distanceBearingPoint(point3d12, num10, metres / 2);
                complexObstacleArea.Add(SecondaryObstacleArea(point3d11, point3d72, point3d71, point3d12));
                point3dArray = [position4, point3d11, point3d72];
                polylineArea_2.method_7(point3dArray);
                point3dArray = [position4, point3d71, point3d12];
                polylineArea_3.method_7(point3dArray);
            elif (not MathHelper.smethod_119(position3, point3d60, point3d61) or not MathHelper.smethod_115(position4, point3d68, point3d69)):
                num28 = num4 + Unit.ConvertDegToRad(num12 / 2);
                point3d73 = MathHelper.distanceBearingPoint(position3, num28, 100);
                point3d74 = MathHelper.distanceBearingPoint(position4, num28, 100);
                point3d15 = MathHelper.getIntersectionPoint(point3d60, point3d61, position3, point3d73);
                point3d16 = MathHelper.getIntersectionPoint(point3d68, point3d69, position4, point3d74);
                complexObstacleArea.Add(SecondaryObstacleArea(position3, point3d15, position4, point3d16));
                point3dArray = [position3, point3d15 ];
                polylineArea_2.method_7(point3dArray);
                point3dArray = [position4, point3d16 ];
                polylineArea_3.method_7(point3dArray);
            else:
                num29 = num4 + Unit.ConvertDegToRad(num12 / 2);
                point3d75 = MathHelper.distanceBearingPoint(position3, num29, 100);
                point3d76 = MathHelper.distanceBearingPoint(position4, num8 + Unit.ConvertDegToRad(15), 100);
                point3d13 = MathHelper.getIntersectionPoint(point3d60, point3d61, position3, point3d75);
                point3d14 = MathHelper.getIntersectionPoint(point3d68, point3d69, position4, point3d76);
                point3d77 = point3d14;
                point3d78 = MathHelper.distanceBearingPoint(point3d77, num10, metres / 2);
                complexObstacleArea.Add(SecondaryObstacleArea(position3, point3d13, position4, position4));
                complexObstacleArea.Add(SecondaryObstacleArea(point3d13, point3d78, position4, point3d14));
                point3dArray = [position3, point3d13, point3d78 ];
                polylineArea_2.method_7(point3dArray);
                point3dArray = [position4, point3d14, point3d77 ];
                polylineArea_3.method_7(point3dArray);
            position5 = polylineArea_1[polylineArea_1.Count - 1].Position;
            point3d17 = MathHelper.getIntersectionPoint(position5, MathHelper.distanceBearingPoint(position5, num9, 1000), point3d60, point3d61);
            point3d18 = MathHelper.getIntersectionPoint(position5, MathHelper.distanceBearingPoint(position5, num9, 1000), point3d68, point3d69);
            position3 = polylineArea_2[polylineArea_2.Count - 1].Position;
            position4 = polylineArea_3[polylineArea_3.Count - 1].Position;
            if (MathHelper.smethod_117(position3, point3d18, position5, False) and MathHelper.smethod_117(position4, point3d18, position5, False)):
                complexObstacleArea.Add(SecondaryObstacleArea(position3, point3d17, position4, point3d18));
                polylineArea_2.method_1(point3d17);
                polylineArea_3.method_1(point3d18);
            polylineArea1 = PolylineArea();
            polylineArea1.method_8(polylineArea_0);
            polylineArea1.method_1(polylineArea_1[polylineArea_1.Count - 1].Position);
            polylineArea1.method_1(polylineArea_2[polylineArea_2.Count - 1].Position);
            polylineArea1.method_8(polylineArea_3.method_17());
            complexObstacleArea.ObstacleArea = PrimaryObstacleArea(polylineArea1);
            polylineArea1 = PolylineArea();
            polylineArea1.method_8(polylineArea_1);
            polylineArea1.method_8(polylineArea_2.method_17());
            complexObstacleArea.Insert(0, PrimaryObstacleArea(polylineArea1));
        return (polylineAreaAAA, complexObstacleArea, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4);
    
    def method_44(self, polylineArea_0, point3d_0, point3d_1):
        # point3dArray = polylineArea_0.method_14()
        # polyline = QgsGeometry.fromPolyline(point3dArray)
        # line = QgsGeometry.fromPolyline([point3d_0.smethod_167(0), point3d_1.smethod_167(0)])
        # if polyline.intersects(line):
        #     point3dAt = point3dArray[0]
        #     point3d = point3dAt
        #     geom = polyline.intersection(line)
        #     # for point3d1 in geom.asPoint():
        #     point3d1 = geom.asPoint()
        #     if (MathHelper.calcDistance(point3dAt, point3d1) <= MathHelper.calcDistance(point3dAt, point3d)):
        #         return polylineArea_0;
        #     point3d = point3dArray[2]
        #     splitCurves = polyline.splitGeometry([point3d_0.smethod_167(0), point3d_1.smethod_167(0)], False);
        #     if len(splitCurves) > 0 :
        #         item = splitCurves[1][0]
        #         polylineArea = PolylineArea.smethod_1(item)
        #         # return polylineArea
        return polylineArea_0
#                 Point3dCollection point3dCollection = new Point3dCollection();
#                 if (polyline.IntersectWith(line, 2, point3dCollection) > 0)
#                 {
#                     Point3d point3dAt = polyline.GetPoint3dAt(0);
#                     Point3d point3d = point3dAt;
#                     foreach (Point3d point3d1 in point3dCollection)
#                     {
#                         if (MathHelper.calcDistance(point3dAt, point3d1) <= MathHelper.calcDistance(point3dAt, point3d))
#                         {
#                             continue;
#                         }
#                         point3d = point3d1;
#                     }
#                     point3dCollection.Clear();
#                     point3dCollection.Add(point3d);
#                     DBObjectCollection splitCurves = polyline.GetSplitCurves(point3dCollection);
#                     try
#                     {
#                         if (splitCurves.get_Count() > 0)
#                         {
#                             Polyline item = splitCurves.get_Item(0) as Polyline;
#                             if (item != null)
#                             {
#                                 polylineArea = PolylineArea.smethod_1(item);
#                                 return polylineArea;
#                             }
#                         }
#                     }
#                     finally
#                     {
#                         AcadHelper.smethod_25(splitCurves);
#                     }
#                 }
#             }
#             return polylineArea_0;
#         }
#         return polylineArea;
#     }
    def method_45(self, complexObstacleArea_0, polylineArea_0, polylineArea_1):
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        point3d3 = None;
        num = 0;
        num1 = 0;
        while (num < polylineArea_0.Count):
            if (num1 >= polylineArea_1.Count):
                break;
            if (polylineArea_0[num].Bulge == 0 and polylineArea_1[num1].Bulge == 0):
                if (num != polylineArea_0.Count - 1):
                    if (num1 != polylineArea_1.Count - 1):
                        complexObstacleArea_0.Add(SecondaryObstacleArea(polylineArea_0[num].Position, polylineArea_0[num + 1].Position, polylineArea_1[num1].Position, polylineArea_1[num1 + 1].Position, MathHelper.getBearing(polylineArea_0[num + 1].Position, polylineArea_0[num].Position)));
                        num += 1
                        num1 += 1;
                        continue;
                return;
            elif (polylineArea_0[num].Bulge != 0 and polylineArea_1[num1].Bulge != 0):
                if (num != polylineArea_0.Count - 1):
                    if (num1 != polylineArea_1.Count - 1):
                        position = polylineArea_0[num].Position;
                        position1 = polylineArea_0[num + 1].Position;
                        position2 = polylineArea_1[num1].Position;
                        position3 = polylineArea_1[num1 + 1].Position;
                        point3d = MathHelper.smethod_71(position, position1, polylineArea_0[num].Bulge);
                        point3d1 = MathHelper.smethod_71(position2, position3, polylineArea_1[num1].Bulge);
                        point3d4 = MathHelper.smethod_93(MathHelper.smethod_66(polylineArea_0[num].Bulge), position, position1, point3d);
                        point3d5 = MathHelper.smethod_93(MathHelper.smethod_66(polylineArea_1[num1].Bulge), position2, position3, point3d1);
                        complexObstacleArea_0.Add(SecondaryObstacleArea(position, point3d4, position1, position2, None, point3d5, position3, polylineArea_0[num].Bulge, polylineArea_1[num].Bulge));
                        num += 1;
                        num1 += 1;
                        continue;
                return;
            elif (polylineArea_1[num1].Bulge == 0):
                if (num == polylineArea_0.Count - 1):
                    return;
                position4 = polylineArea_0[num].Position;
                position5 = polylineArea_0[num + 1].Position;
                point3d3 = MathHelper.smethod_71(position4, position5, polylineArea_0[num1].Bulge);
                point3d6 = MathHelper.smethod_93(MathHelper.smethod_66(polylineArea_0[num].Bulge), position4, position5, point3d3);
                num2 = MathHelper.calcDistance(point3d3, polylineArea_1[num1].Position);
                point3d7 = MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d3, position4), num2);
                point3d8 = MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d3, point3d6), num2);
                point3d9 = MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d3, position5), num2);
                complexObstacleArea_0.Add(SecondaryObstacleArea(position4, point3d6, position5, point3d7, None, point3d8, point3d9));
                num += 1;
            else:
                if (num1 == polylineArea_1.Count - 1):
                    return;
                position6 = polylineArea_1[num1].Position;
                position7 = polylineArea_1[num1 + 1].Position;
                point3d2 = MathHelper.smethod_71(position6, position7, polylineArea_1[num1].Bulge);
                point3d10 = MathHelper.smethod_93(MathHelper.smethod_66(polylineArea_1[num1].Bulge), position6, position7, point3d2);
                complexObstacleArea_0.Add(SecondaryObstacleArea(position6, point3d10, position7));
                num1 += 1;
    def WPT2Layer(self):
        mapUnits = define._canvas.mapUnits()
        if define._mapCrs == None:
            if mapUnits == QGis.Meters:
                resultLayer = QgsVectorLayer("Point?crs=EPSG:32633", "WPT_" + self.surfaceType.replace(" ", "_").replace("-", "_"), "memory")
            else:
                resultLayer = QgsVectorLayer("Point?crs=EPSG:4326", "WPT_" + self.surfaceType.replace(" ", "_").replace("-", "_"), "memory")
        else:
            resultLayer = QgsVectorLayer("Point?crs=%s"%define._mapCrs.authid (), "WPT_" + self.surfaceType.replace(" ", "_").replace("-", "_"), "memory")
        shpPath = ""
        if define.obstaclePath != None:
            shpPath = define.obstaclePath
        elif define.xmlPath != None:
            shpPath = define.xmlPath
        else:
            shpPath = define.appPath
        er = QgsVectorFileWriter.writeAsVectorFormat(resultLayer, shpPath + "/" + "RnavTurningSegmentAnalyserWpt" + ".shp", "utf-8", resultLayer.crs())
        resultLayer = QgsVectorLayer(shpPath + "/" + "RnavTurningSegmentAnalyserWpt" + ".shp", "WPT_RnavTurningSegmentAnalyser", "ogr")

#         if mapUnits == QGis.Meters:
#             resultLayer = QgsVectorLayer("Point?crs=EPSG:32633", "WPT", "memory")
#         else:
#             resultLayer = QgsVectorLayer("Point?crs=EPSG:4326", "WPT", "memory")
        fieldName = "CATEGORY"
        resultLayer.dataProvider().addAttributes( [QgsField(fieldName, QVariant.String)] )
        resultLayer.startEditing()
        fields = resultLayer.pendingFields()
        i = 1
        feature = QgsFeature()
        feature.setFields(fields)

        feature.setGeometry(QgsGeometry.fromPoint (self.parametersPanel.pnlWaypoint.Point3d))
        feature.setAttribute(fieldName, "Waypoint")
        pr = resultLayer.dataProvider()
        pr.addFeatures([feature])
        # resultLayer.addFeature(feature)
        # feature.setGeometry(QgsGeometry.fromPoint (self.parametersPanel.pnlPosWpt2.Point3d))
        # feature.setAttribute(fieldName, "Waypoint2")
        # resultLayer.addFeature(feature)
        resultLayer.commitChanges()

        renderCatFly = None
        if self.parametersPanel.cmbType.currentIndex() == 1:
            '''FlyOver'''

            symbolFlyOver = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
            symbolFlyOver.deleteSymbolLayer(0)
            svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyover.svg", 10.0, 0.0)
            symbolFlyOver.appendSymbolLayer(svgSymLayer)
            renderCatFly = QgsRendererCategoryV2(0, symbolFlyOver,"Fly Over")
        elif self.parametersPanel.cmbType.currentIndex() == 0:
            '''FlyBy'''
            symbolFlyBy = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
            symbolFlyBy.deleteSymbolLayer(0)
            svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyby.svg", 10.0, 0.0)
            symbolFlyBy.appendSymbolLayer(svgSymLayer)
            renderCatFly = QgsRendererCategoryV2(0, symbolFlyBy,"Fly By")
        else:
            return None
        WPT_EXPRESION = "CASE WHEN  \"CATEGORY\" = 'Waypoint'  THEN 0 " + \
                                        "END"
        symRenderer = QgsCategorizedSymbolRendererV2(WPT_EXPRESION, [renderCatFly])

        resultLayer.setRendererV2(symRenderer)
        return resultLayer
    def get_phaseOfFlight(self):
        if self.parametersPanel.cmbPhaseOfFlight.currentText() == "Enroute":
            return 0
        elif self.parametersPanel.cmbPhaseOfFlight.currentText() == "STAR":
            return 2
        return -1
        
#         return self.parametersPanel.cmbPhaseOfFlight.currentIndex()
    phaseOfFlight = property(get_phaseOfFlight, None, None, None)
    
    def get_rnavSpecification(self):
        return self.parametersPanel.cmbRnavSpecification.currentText()
    rnavSpecification = property(get_rnavSpecification, None, None, None)
class RnavTurningSegmentObstacles(ObstacleTable):
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
        obstacleAreaResult, num, num1 = self.area.pointInArea(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier);
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            position = obstacle_0.Position;
            if num == None:
                checkResult = [obstacleAreaResult, num1, num,  position.get_Z() + obstacle_0.Trees, CriticalObstacleType.No];
                self.addObstacleToModel(obstacle_0, checkResult)
                return

            z = position.get_Z() + obstacle_0.Trees + num;
            criticalObstacleType = CriticalObstacleType.No;
            if (z > self.enrouteAltitude):
                criticalObstacleType = CriticalObstacleType.Yes;
            checkResult = [obstacleAreaResult, num1, num, z, criticalObstacleType];
            self.addObstacleToModel(obstacle_0, checkResult)
        m = 0
#             RnavStraightSegmentAnalyser.obstacles.method_11(obstacle_0, obstacleAreaResult, num1, num, z, criticalObstacleType);
class TurnConstructionMethod:
    CircularArcs = "CircularArcs"
    FixedRadius = "FixedRadius"
    BoundingCircles = "BoundingCircles"
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