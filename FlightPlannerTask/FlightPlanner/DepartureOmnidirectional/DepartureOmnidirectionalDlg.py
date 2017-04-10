# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QSize, Qt
from PyQt4.QtGui import QCheckBox, QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsCoordinateReferenceSystem,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2

from PyQt4.QtCore import SIGNAL, QCoreApplication,QSize, Qt
from PyQt4.QtGui import QColor, QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsCoordinateReferenceSystem,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, \
                QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, \
                QgsSymbolV2, QgsRendererCategoryV2, QgsGeometry
from qgis.core import QGis, QgsRectangle, QgsGeometry, QgsCsException, QgsPoint,\
        QgsFeatureRequest, QgsCoordinateTransform, QgsFeature, QgsVectorLayer
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapToolPan

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import AngleUnits, TurnDirection, CriticalObstacleType, \
                    ObstacleTableColumnType, SurfaceTypes, DistanceUnits,AircraftSpeedCategory, \
                    OrientationType, AltitudeUnits, ObstacleAreaResult, RnavDmeDmeFlightPhase, \
                    RnavDmeDmeCriteria, RnavSpecification, RnavGnssFlightPhase , ConstructionType, \
                    CloseInObstacleType
from FlightPlanner.DepartureOmnidirectional.ui_DepartureOmnidirectional import Ui_DepartureOmnidirectional
from FlightPlanner.Panels.PositionPanel import PositionPanel
# from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, ComplexObstacleArea, SecondaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.messages import Messages
from FlightPlanner.AcadHelper import AcadHelper
import define, math

class DepartureOmnidirectionalDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("DepartureOmnidirectionalDlg")
        self.surfaceType = SurfaceTypes.DepartureOmnidirectional
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.DepartureOmnidirectional)
        self.resize(540, 700)
        QgisHelper.matchingDialogSize(self, 600, 700)
        self.surfaceList = None
        self.manualPolygon = None
        self.area123 = []
        self.circleArea = None
        self.resultLayerList = []
    def initObstaclesModel(self):
        self.obstaclesModel.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        return FlightPlanBaseDlg.initObstaclesModel(self)
    def openData(self):
        return FlightPlanBaseDlg.openData(self)
        self.calcRadiusArea3()

    
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
        # longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlDer.txtPointX.text()), float(self.parametersPanel.pnlDer.txtPointY.text()))

        parameterList.append(("DER Position", "group"))
        parameterList.append(("Lat", self.parametersPanel.pnlDer.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlDer.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlDer.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlDer.txtPointY.text()))
        parameterList.append(("Altitude", self.parametersPanel.pnlDer.txtAltitudeM.text() + "m"))
        parameterList.append(("", self.parametersPanel.pnlDer.txtAltitudeFt.text() + "ft"))
        
        
        parameterList.append(("Start of RWY/FATO Psition", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlRwyStart.txtPointX.text()), float(self.parametersPanel.pnlRwyStart.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlRwyStart.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlRwyStart.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlRwyStart.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlRwyStart.txtPointY.text()))
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Selection Mode", self.parametersPanel.cmbSelectionMode.currentText()))
        
        if self.parametersPanel.chbCatH.isChecked():            
            parameterList.append(("Minimum Turn Height", self.parametersPanel.txtMinTurnHeight.text() + "m"))
        else:
            parameterList.append(("Minimum Turn Height", self.parametersPanel.txtMinTurnHeight_CATH.text() + "m"))
        parameterList.append(("Turning Altitude", self.parametersPanel.txtTurningAltitude.text() + "ft"))
        parameterList.append(("Next Segment Altitude/MSA", self.parametersPanel.txtNextSegmentAltitude.text() + "ft"))
        parameterList.append(("MOC", self.parametersPanel.txtMoc.text() + "%"))
        parameterList.append(("PDG", self.parametersPanel.txtPdg.text() + "%"))
        parameterList.append(("MOCmultipiler", str(self.parametersPanel.mocSpinBox.value())))
        if self.parametersPanel.chbTurnsBeforeDer.isChecked():            
            parameterList.append(("Allow turns before DER", "True"))
        else:
            parameterList.append(("Allow turns before DER", "False"))
        if self.parametersPanel.chbCatH.isChecked():            
            parameterList.append(("Cat. H", "True"))
        else:
            parameterList.append(("Cat. H", "False"))
        
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
        polylineArea = None;
        polylineArea1 = None;
        polylineArea2 = None;
        primaryObstacleArea = None;
#         if (self.parametersPanel.cmbSelectionMode.currentText() == "Manual" and not self.pnlSelectionMode.method_0()):
#             return;
        result, point3dCollection, point3dCollection1, polylineArea, polylineArea1, polylineArea2= self.method_34()
        if (not result):
            return;
        point3d = self.parametersPanel.pnlDer.Point3d;
        num = MathHelper.getBearing(self.parametersPanel.pnlRwyStart.Point3d, point3d);
        percent = float(self.parametersPanel.txtMoc.text());
        percent1 = float(self.parametersPanel.txtPdg.text());
        
        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        self.obstaclesModel = DepartureOmnidirectionalObstacles(point3d, num, Altitude(float(self.parametersPanel.txtTurningAltitude.text()), AltitudeUnits.FT), percent, percent1, self.parametersPanel.chbCatH.isChecked(), point3dCollection, point3dCollection1, polylineArea1, polylineArea2, self.manualPolygon);
        
#                     
        return FlightPlanBaseDlg.btnEvaluate_Click(self)
    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        # self.parametersPanel.txtRadius.setText("")

        point3dCollection = None;
        point3dCollection1 = None;
        polylineArea = None;
        polylineArea1 = None;
        polylineArea2 = None;

        point3dArrayResult = []

        mapUnits = define._canvas.mapUnits()
        constructionLayer = None


        result, point3dCollection, point3dCollection1, polylineArea, polylineArea1, polylineArea2 = self.method_34()
        if result:
            point3dCollection2 = [];
            if (point3dCollection != None and len(point3dCollection) > 0):
                point3dCollection2.append(point3dCollection[0]);
            for point3d in point3dCollection1:
                point3dCollection2.append(point3d);
            if (point3dCollection != None and len(point3dCollection) > 0):
                point3dCollection2.append(point3dCollection[3]);
            # point3dCollection2.pop(3)
            # point3dCollection2.pop(3)
            # point3dArrayResult.append(polylineArea1.method_14_closed())
            # point3dArrayResult.append(polylineArea2.method_14_closed())
            point3dArrayResult.append(PolylineArea(point3dCollection2))

            self.area123 = point3dCollection2
            self.circleArea = polylineArea

            nominalPointTest1 = point3dCollection2[2]
            nominalPointTest2 = point3dCollection2[3]
            self.nominalPoint = MathHelper.distanceBearingPoint(nominalPointTest1, MathHelper.getBearing(nominalPointTest1, nominalPointTest2), MathHelper.calcDistance(nominalPointTest1, nominalPointTest2) / 2)
            # if polylineArea.isCircle:
            #     self.parametersPanel.txtRadius.setText(str(polylineArea.Radius()))
            point3dArrayResult.append(polylineArea)

        if not len(point3dArrayResult) > 0 :
            return
        constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)
        for point3dArray in point3dArrayResult:
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, point3dArray, True)
        nominalTrackLayer = self.nominal2Layer()
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer, nominalTrackLayer], self.surfaceType)
        self.resultLayerList = [constructionLayer, nominalTrackLayer]
        QgisHelper.zoomToLayers(self.resultLayerList)
        self.ui.btnEvaluate.setEnabled(True)
        # return FlightPlanBaseDlg.btnConstruct_Click(self)
        
    def initParametersPan(self):
        ui = Ui_DepartureOmnidirectional()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)
        
        self.parametersPanel.chbHideCloseInObst = QCheckBox(self.ui.grbResult)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.parametersPanel.chbHideCloseInObst.setFont(font)
        self.parametersPanel.chbHideCloseInObst.setObjectName("chbHideCloseInObst")
        self.ui.vlResultGroup.addWidget(self.parametersPanel.chbHideCloseInObst)
        self.parametersPanel.chbHideCloseInObst.setText("Hide close-in obstacles")
        self.parametersPanel.txtRadiusFt.setEnabled(False)
        self.parametersPanel.txtRadius.setEnabled(False)
        
        self.parametersPanel.frameMinTurnHeight_CATH.setVisible(False)
        
        self.parametersPanel.pnlDer = PositionPanel(self.parametersPanel.gbRunway)
        self.parametersPanel.pnlDer.groupBox.setTitle("DER Position")
        self.parametersPanel.pnlDer.btnCalculater.hide()
#         self.parametersPanel.pnlRwyDir.hideframe_Altitude()
        self.parametersPanel.pnlDer.setObjectName("pnlDer")
        ui.vl_gbRunway.addWidget(self.parametersPanel.pnlDer)
#         self.connect(self.parametersPanel.pnlRwyDir, SIGNAL("positionChanged"), self.initResultPanel)

        self.parametersPanel.pnlRwyStart = PositionPanel(self.parametersPanel.gbRunway)
        self.parametersPanel.pnlRwyStart.groupBox.setTitle("Start of RWY/FATO Position")
        self.parametersPanel.pnlRwyStart.btnCalculater.hide()
        self.parametersPanel.pnlRwyStart.hideframe_Altitude()
        self.parametersPanel.pnlRwyStart.setObjectName("pnlRwyStart")
        ui.vl_gbRunway.insertWidget(1, self.parametersPanel.pnlRwyStart)
        self.calcRadiusArea3()
        self.parametersPanel.cmbSelectionMode.addItems(["Automatic", "Manual"])
        self.parametersPanel.cmbSelectionMode.currentIndexChanged.connect(self.manualEvent)
#         self.parametersPanel.cmbHoldingFunctionality.currentIndexChanged.connect(self.cmbHoldingFunctionalityCurrentIndexChanged)
#         self.parametersPanel.cmbOutboundLimit.currentIndexChanged.connect(self.cmbOutboundLimitCurrentIndexChanged)
#         self.parametersPanel.btnCaptureDer.clicked.connect(self.captureBearing)
        self.parametersPanel.chbHideCloseInObst.stateChanged.connect(self.chbHideCloseInObstStateChanged)
        self.parametersPanel.chbCatH.stateChanged.connect(self.chbCATHStateChanged)
        self.parametersPanel.txtPdg.textChanged.connect(self.calcRadiusArea3)
        self.parametersPanel.pnlDer.txtPointX.textChanged.connect(self.calcRadiusArea3)
        self.parametersPanel.pnlDer.txtAltitudeM.textChanged.connect(self.calcRadiusArea3)
        self.parametersPanel.txtNextSegmentAltitude.textChanged.connect(self.txtNextSegmentAltitudeChanged)
        self.parametersPanel.txtTurningAltitude.textChanged.connect(self.txtTurningAltitudeChanged)
        self.parametersPanel.txtNextSegmentAltitudeM.textChanged.connect(self.txtNextSegmentAltitudeMChanged)
        self.parametersPanel.txtTurningAltitudeM.textChanged.connect(self.txtTurningAltitudeMChanged)


        self.parametersPanel.txtMinTurnHeight.textChanged.connect(self.txtMinTurnHeightChanged)
        self.parametersPanel.txtMinTurnHeightFt.textChanged.connect(self.txtMinTurnHeightFtChanged)
        self.parametersPanel.txtMinTurnHeight_CATH.textChanged.connect(self.txtMinTurnHeight_CATHChanged)
        self.parametersPanel.txtMinTurnHeight_CATH_2.textChanged.connect(self.txtMinTurnHeight_CATH_2Changed)
#         self.parametersPanel.btnCaptureDistance.clicked.connect(self.measureDistance)
#         self.parametersPanel.btnCaptureLength.clicked.connect(self.measureLength)        
#         self.parametersPanel.txtAltitude.textChanged.connect(self.altitudeChanged)
#         self.parametersPanel.cmbAircraftCategory.currentIndexChanged.connect(self.changeCategory)
#         self.parametersPanel.btnIasHelp.clicked.connect(self.iasHelpShow)
#         self.parametersPanel.txtIas.textChanged.connect(self.iasChanged)
#         self.parametersPanel.txtIsa.textChanged.connect(self.isaChanged)
#
        self.txtTFlag = True
        self.txtNFlag = True
        self.txtTMFlag = False
        self.txtNMFlag = False

        self.flag = 0
        self.flag1 = 0
        self.flag2 = 0
        self.flag3 = 0
        try:
            self.parametersPanel.txtNextSegmentAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtNextSegmentAltitude.text())), 4)))
        except:
            self.parametersPanel.txtNextSegmentAltitudeM.setText("0.0")
        try:
            self.parametersPanel.txtTurningAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtTurningAltitude.text())), 4)))
        except:
            self.parametersPanel.txtTurningAltitudeM.setText("0.0")


        try:
            self.parametersPanel.txtMinTurnHeightFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMinTurnHeight.text())), 4)))
        except:
            self.parametersPanel.txtMinTurnHeightFt.setText("0.0")
        try:
            self.parametersPanel.txtMinTurnHeight_CATH_2.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMinTurnHeight_CATH.text())), 4)))
        except:
            self.parametersPanel.txtMinTurnHeight_CATH_2.setText("0.0")

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


    def txtNextSegmentAltitudeMChanged(self):
        if self.flag==0:
            self.flag=1;
        if self.flag==2:
            self.flag=0;
        if self.flag==1:
            try:
                self.parametersPanel.txtNextSegmentAltitude.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtNextSegmentAltitudeM.text())), 4)))
            except:
                self.parametersPanel.txtNextSegmentAltitude.setText("0.0")
        self.calcRadiusArea3()

    def txtNextSegmentAltitudeChanged(self):
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtNextSegmentAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtNextSegmentAltitude.text())), 4)))
            except:
                self.parametersPanel.txtNextSegmentAltitudeM.setText("0.0")
        self.calcRadiusArea3()
    def txtTurningAltitudeChanged(self):
        if self.flag1==0:
            self.flag1=2;
        if self.flag1==1:
            self.flag1=0;
        if self.flag1==2:
            try:
                self.parametersPanel.txtTurningAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtTurningAltitude.text())), 4)))
            except:
                self.parametersPanel.txtTurningAltitudeM.setText("0.0")
        self.calcRadiusArea3()
    def txtTurningAltitudeMChanged(self):
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtTurningAltitude.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtTurningAltitudeM.text())), 4)))
            except:
                self.parametersPanel.txtTurningAltitude.setText("0.0")
        self.calcRadiusArea3()
    def calcRadiusArea3(self):
        try:
            pdg = 0.0
            try:
                pdg = float(self.parametersPanel.txtPdg.text())
            except:
                pass

            dist1 = math.fabs((Altitude(float(self.parametersPanel.txtTurningAltitude.text()), AltitudeUnits.FT).Metres - Altitude(float(self.parametersPanel.txtNextSegmentAltitude.text()), AltitudeUnits.FT).Metres ) / (3.3 / 100.0))
            dist2 = math.fabs((Altitude(float(self.parametersPanel.txtTurningAltitude.text()), AltitudeUnits.FT).Metres - float(self.parametersPanel.pnlDer.txtAltitudeM.text())- 5.0) / (pdg / 100.0))
            # print dist1, dist2
            self.parametersPanel.txtRadius.setText(str(round(dist1 + dist2, 4)))
            self.parametersPanel.txtRadiusFt.setText(str(round(Unit.ConvertMeterToNM(dist1 + dist2), 4)))
        except:
            pass
    def txtMinTurnHeightChanged(self):
        if self.flag2==0:
            self.flag2=1;
        if self.flag2==2:
            self.flag2=0;
        if self.flag2==1:
            try:
                self.parametersPanel.txtMinTurnHeightFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMinTurnHeight.text())), 4)))
            except:
                self.parametersPanel.txtMinTurnHeightFt.setText("0.0")
        self.calcRadiusArea3()

    def txtMinTurnHeightFtChanged(self):
        if self.flag2==0:
            self.flag2=2;
        if self.flag2==1:
            self.flag2=0;
        if self.flag2==2:
            try:
                self.parametersPanel.txtMinTurnHeight.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtMinTurnHeightFt.text())), 4)))
            except:
                self.parametersPanel.txtMinTurnHeight.setText("0.0")
        self.calcRadiusArea3()
    def txtMinTurnHeight_CATH_2Changed(self):
        if self.flag3==0:
            self.flag3=2;
        if self.flag3==1:
            self.flag3=0;
        if self.flag3==2:
            try:
                self.parametersPanel.txtMinTurnHeight_CATH.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtMinTurnHeight_CATH_2.text())), 4)))
            except:
                self.parametersPanel.txtMinTurnHeight_CATH.setText("0.0")
        self.calcRadiusArea3()
    def txtMinTurnHeight_CATHChanged(self):
        if self.flag3==0:
            self.flag3=1;
        if self.flag3==2:
            self.flag3=0;
        if self.flag3==1:
            try:
                self.parametersPanel.txtMinTurnHeight_CATH_2.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMinTurnHeight_CATH.text())), 4)))
            except:
                self.parametersPanel.txtMinTurnHeight_CATH_2.setText("0.0")
    def chbCATHStateChanged(self, state):
        self.parametersPanel.frameMinTurnHeight.setVisible(not self.parametersPanel.chbCatH.isChecked())
        self.parametersPanel.frameMinTurnHeight_CATH.setVisible(self.parametersPanel.chbCatH.isChecked())  
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
            self.parametersPanel.cmbSpecification.addItems(["Rnav1", "Rnav2", "Rnp1"])
        else:
            self.parametersPanel.frame_63.setVisible(True)
            self.parametersPanel.cmbSpecification.addItems(["Rnav1", "Rnav2"])
    
    def captureBearing(self):
        self.captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtDer)
        define._canvas.setMapTool(self.captureTrackTool)
    
    def method_34(self):
        point3dCollection_0 = None
        point3dCollection_1 = None
        polylineArea_0 = None
        polylineArea_1 = None
        polylineArea_2 = None
        
        point3d = self.parametersPanel.pnlRwyStart.Point3d;
        point3d1 = self.parametersPanel.pnlDer.Point3d;
        num = MathHelper.getBearing(point3d, point3d1);
        num1 = MathHelper.smethod_4(num + 3.14159265358979);
        num2 = MathHelper.smethod_4(num - 1.5707963267949);
        num3 = MathHelper.smethod_4(num + 1.5707963267949);
        percent = float(self.parametersPanel.txtPdg.text()) / 100;
        metres = Altitude(float(self.parametersPanel.txtTurningAltitude.text()), AltitudeUnits.FT).Metres;
        metres1 = Altitude(float(self.parametersPanel.txtNextSegmentAltitude.text()), AltitudeUnits.FT).Metres;
        num4 = 45 if (self.parametersPanel.chbCatH.isChecked()) else 150;
        num5 = MathHelper.calcDistance(point3d, point3d1);
        if (num5 < 10):
            QMessageBox.warning(self, "Warning", Messages.ERR_POSITIONS_TOO_CLOSE);
            return (False, None, None, None, None, None)
        if (not self.parametersPanel.chbTurnsBeforeDer.isChecked()):
            point3dCollection_0 = None;
        else:
            point3d2 = point3d if (self.parametersPanel.chbCatH.isChecked()) else MathHelper.distanceBearingPoint(point3d, num, min([600, num5]));
            if (MathHelper.smethod_103(point3d2, point3d1, 0.1)):
                point3dCollection_0 = None;
            else:
                point3dCollection_0 = [];
                point3dCollection_0.append(MathHelper.distanceBearingPoint(point3d2, num2, num4));
                point3dCollection_0.append(MathHelper.distanceBearingPoint(point3d1, num2, num4));
                point3dCollection_0.append(MathHelper.distanceBearingPoint(point3d1, num3, num4));
                point3dCollection_0.append(MathHelper.distanceBearingPoint(point3d2, num3, num4));
        num6 = ((Altitude(float(self.parametersPanel.txtMinTurnHeight_CATH.text())).Metres if (self.parametersPanel.chbCatH.isChecked()) else Altitude(float(self.parametersPanel.txtMinTurnHeight.text())).Metres) - 5) / percent;
        z = (metres - point3d1.get_Z() - 5) / percent;
        num7 = Unit.ConvertDegToRad(15);
        num8 = Unit.ConvertDegToRad(30);
        point3d3 = MathHelper.distanceBearingPoint(point3d1, num2, num4);
        point3d4 = MathHelper.distanceBearingPoint(point3d1, num3, num4);
        point3d5 = MathHelper.distanceBearingPoint(point3d3, num - num7, num6 / math.cos(num7));
        point3d6 = MathHelper.distanceBearingPoint(point3d4, num + num7, num6 / math.cos(num7));
        point3d7 = MathHelper.distanceBearingPoint(point3d5, num - num8, (z - num6) / math.cos(num8));
        point3d8 = MathHelper.distanceBearingPoint(point3d6, num + num8, (z - num6) / math.cos(num8));
        point3dCollection_1 = [];
        point3dArray = [point3d3, point3d5, point3d7, point3d8, point3d6, point3d4];
        point3dCollection_1.extend(point3dArray);
        z1 = (metres1 - point3d1.get_Z() - 5) / percent;
        point3d9 = point3d if (self.parametersPanel.chbCatH.isChecked()) else MathHelper.distanceBearingPoint(point3d, num, min([600, num5]));
        polylineArea_0 = PolylineArea(None, point3d9.smethod_167(0), z1);
        point3d10 = MathHelper.distanceBearingPoint(point3d9, num1, z1);
        point3d11 = MathHelper.distanceBearingPoint(point3d9, num, z1);
        polylineArea_1 = PolylineArea();
        polylineArea_1.method_3(point3d10, MathHelper.smethod_57(TurnDirection.Right, point3d10, point3d11, point3d9));
        polylineArea_1.method_1(point3d11);
        if (point3dCollection_0 != None):
            item = [point3d1, point3dCollection_0[1], point3dCollection_0[0], point3d9];
            polylineArea_1.method_7(item);
        polylineArea_2 = PolylineArea();
        polylineArea_2.method_3(point3d10, MathHelper.smethod_57(TurnDirection.Left, point3d10, point3d11, point3d9));
        polylineArea_2.method_1(point3d11);
        if (point3dCollection_0 != None):
            item1 = [point3d1, point3dCollection_0[2], point3dCollection_0[3], point3d9];
            polylineArea_2.method_7(item1);
        return (True, point3dCollection_0, point3dCollection_1, polylineArea_0, polylineArea_1, polylineArea_2);
    def nominal2Layer(self):
        resultLayer = AcadHelper.createVectorLayer("NominalTrack_" + self.surfaceType.replace(" ", "_").replace("-", "_"), QGis.Line)
        startPoint3d = self.parametersPanel.pnlRwyStart.Point3d
        derPoint3d =self.parametersPanel.pnlDer.Point3d
        bearing = MathHelper.getBearing(startPoint3d, derPoint3d)
        derPoint3d1 = MathHelper.distanceBearingPoint(derPoint3d, bearing, 100)
        derPoint3d2 = MathHelper.distanceBearingPoint(derPoint3d, bearing, self.circleArea[0].bulge)
        geom = QgsGeometry.fromPolyline(self.area123).intersection(QgsGeometry.fromPolyline([derPoint3d1, derPoint3d2]))
        intersectionPoint1 = geom.asPoint()

        derPoint3d1 = MathHelper.distanceBearingPoint(derPoint3d, bearing, 100)
        bearing = MathHelper.smethod_4(bearing + math.pi)
        derPoint3d2 = MathHelper.distanceBearingPoint(derPoint3d, bearing, MathHelper.calcDistance(derPoint3d, startPoint3d) + 200)
        geom = QgsGeometry.fromPolyline(PolylineArea(self.area123).method_14_closed()).intersection(QgsGeometry.fromPolyline([derPoint3d1, derPoint3d2]))
        intersectionPoint2 = geom.asPoint()
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [intersectionPoint1, derPoint3d])

        return resultLayer
class DepartureOmnidirectionalObstacles(ObstacleTable):
    def __init__(self, point3d_0, double_0, altitude_0, double_1, double_2, bool_0, point3dCollection_0, point3dCollection_1, polylineArea_0, polylineArea_1, manualPoly):
        ObstacleTable.__init__(self, None)
        self.manualPolygon = manualPoly
        self.surfaceType = SurfaceTypes.DepartureOmnidirectional
        self.track = double_0;
        self.ptDER = point3d_0;
        self.ptDER2 = MathHelper.distanceBearingPoint(point3d_0, double_0 - 1.5707963267949, 100);
        self.moc = double_1;
        self.minMoc = 80 if (bool_0) else 90;
        self.pdg = double_2;
        self.ta = altitude_0.Metres;
        point3dCollection = [];
        if (point3dCollection_0 != None and len(point3dCollection_0) > 0):
            point3dCollection.append(point3dCollection_0[0]);
        for point3d in point3dCollection_1:
            point3dCollection.append(point3d);
        if (point3dCollection_0 != None and len(point3dCollection_0) > 0):
            point3dCollection.append(point3dCollection_0[3]);
        self.area = PolylineArea.smethod_133(point3dCollection, True);
        self.area12 = PrimaryObstacleArea(PolylineArea(point3dCollection_1));
        self.area3a = PrimaryObstacleArea(polylineArea_0);
        self.area3b = PrimaryObstacleArea(polylineArea_1);
    def setHiddenColumns(self, tableView):
#         tableView.hideColumn(self.IndexObstArea)
#         tableView.hideColumn(self.IndexDistInSecM)
        return ObstacleTable.setHiddenColumns(self, tableView)
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        self.IndexDrM = fixedColumnCount 
        self.IndexDoM = fixedColumnCount + 1
        self.IndexMocReqM = fixedColumnCount + 2
        self.IndexMocReqFt = fixedColumnCount + 3
        self.IndexAcAltM = fixedColumnCount + 4
        self.IndexAcAltFt = fixedColumnCount + 5
        self.IndexAltReqM = fixedColumnCount + 6
        self.IndexAltReqFt = fixedColumnCount + 7
        self.IndexPDG = fixedColumnCount + 8
        self.IndexCritical = fixedColumnCount + 9
        self.IndexCloseIn = fixedColumnCount + 10
                 
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.DrM,
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
        self.source.setItem(row, self.IndexDrM, item)
        
        item = QStandardItem(str(checkResult[1]))
        item.setData(checkResult[1])
        self.source.setItem(row, self.IndexDoM, item)
        
        item = QStandardItem(str(checkResult[2]))
        item.setData(checkResult[2])
        self.source.setItem(row, self.IndexMocReqM, item)
                      
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[2])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[2]))
        self.source.setItem(row, self.IndexMocReqFt, item)
        
        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexAcAltM, item)
                      
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[3])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[3]))
        self.source.setItem(row, self.IndexAcAltFt, item)
        
        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4])
        self.source.setItem(row, self.IndexAltReqM, item)
                      
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[4])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[4]))
        self.source.setItem(row, self.IndexAltReqFt, item)
        
        item = QStandardItem(str(checkResult[5]))
        item.setData(checkResult[5])
        self.source.setItem(row, self.IndexPDG, item)
        
        item = QStandardItem(str(checkResult[6]))
        item.setData(checkResult[6])
        self.source.setItem(row, self.IndexCritical, item)
        
        item = QStandardItem(str(checkResult[7]))
        item.setData(checkResult[7])
        self.source.setItem(row, self.IndexCloseIn, item)
    def checkObstacle(self, obstacle_0):
        if self.manualPolygon != None:
            if not self.manualPolygon.contains(obstacle_0.Position):
                return
        mocMultiplier = None;
        z = None;
        num = None;
        z1 = None;
        point3d = None;
        point3d1 = None;
        num1 = None;
        num2 = None;
        if (not self.area12.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
            if (not self.area3a.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance) and not self.area3b.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
                return;
            closestPointTo = self.area.getPointWithShortestDist(obstacle_0.Position);
            point = QgsGeometry.fromPolyline(self.area.method_14()).closestVertex(obstacle_0.Position)
            point3d1 = MathHelper.getIntersectionPoint(closestPointTo, MathHelper.distanceBearingPoint(closestPointTo, self.track, 100), self.ptDER, self.ptDER2);
            num1 = MathHelper.calcDistance(closestPointTo, point3d1) if (MathHelper.smethod_119(closestPointTo, self.ptDER, self.ptDER2)) else 1E-08;
            if num1 == 0:
                num1 = 1E-08
            num2 = max([1E-08, MathHelper.calcDistance(obstacle_0.Position, closestPointTo) - obstacle_0.Tolerance]);
            mocMultiplier = max([self.moc / 100 * (num1 + num2) * obstacle_0.MocMultiplier, self.minMoc]);
            z = self.ta + self.pdg / 100 * num2;
            position = obstacle_0.Position;
            num = position.get_Z() + obstacle_0.Trees + mocMultiplier;
            z1 = 100 * ((num - self.ta) / num2);

        else:
            point3d2 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.track + 3.14159265358979, obstacle_0.Tolerance);
            point3d3 = MathHelper.distanceBearingPoint(point3d2, self.track, 100);
            point3d = MathHelper.getIntersectionPoint(self.ptDER, self.ptDER2, point3d2, point3d3);
            num1 = 1E-08 if (not MathHelper.smethod_119(point3d2, self.ptDER, self.ptDER2)) else MathHelper.calcDistance(point3d, point3d2);
            if num1 == 0:
                num1 = 1E-08
            mocMultiplier = self.moc / 100 * num1 * obstacle_0.MocMultiplier;
            z = self.ptDER.get_Z() + 5 + self.pdg / 100 * num1;
            position1 = obstacle_0.Position;
            num = position1.get_Z() + obstacle_0.Trees + mocMultiplier;
            z1 = 100 * ((num - (self.ptDER.get_Z() + 5)) / num1);
        if num1 < 0.00001:
            num1 = None
        criticalObstacleType = CriticalObstacleType.No;
        if (z1 > self.pdg):
            criticalObstacleType = CriticalObstacleType.Yes;
        closeInObstacleType = CloseInObstacleType.No;
        if (num <= self.ptDER.get_Z() + 60):
            closeInObstacleType = CloseInObstacleType.Yes;
        checkResult = [num1, num2, mocMultiplier, z, num, z1, criticalObstacleType, closeInObstacleType];
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