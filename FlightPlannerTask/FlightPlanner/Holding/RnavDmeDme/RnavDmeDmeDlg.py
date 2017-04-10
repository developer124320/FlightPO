# -*- coding: UTF-8 -*-
'''
Created on 30 Jun 2015

@author: Administrator
'''

from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType,\
      DistanceUnits, RnavSpecification, RnavDmeDmeFlightPhase, RnavDmeDmeCriteria, ObstacleAreaResult
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, SecondaryObstacleArea, ComplexObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.Holding.RnavDmeDme.ui_RnavDmeDme import Ui_RnavDmeDme
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import AltitudeUnits, Point3D, SurfaceTypes
from FlightPlanner.polylineArea import PolylineArea
from FlightPlanner.helpers import Distance, Altitude, MathHelper, Unit
from FlightPlanner.SelectFly.SelectFlyDlg import SelectFlyDlg
from qgis.gui import QgsMapTool, QgsMapToolPan
from qgis.gui import QgsRubberBand
from qgis.core import QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsVectorFileWriter, QgsSymbolV2, QgsRendererCategoryV2

from PyQt4.QtCore import SIGNAL, QCoreApplication,Qt, QVariant
from PyQt4.QtGui import QColor, QStandardItem, QFileDialog
import define
import math

class RnavDmeDme(FlightPlanBaseDlg):
    '''
    classdocs
    '''
    Result1 = None
    Result2 = None
#     Count = 0
    def __init__(self, parent):
        '''
        Constructor
        '''
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("RnavVorDme")
        self.surfaceType = SurfaceTypes.RnavDmeDme
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.RnavDmeDme)
                
        self.resize(600, 550)
        QgisHelper.matchingDialogSize(self, 720, 700)
        
        self.result1 = None
        self.result2 = None
        self.manualPolygon = None
        self.complexObstacleArea = None
        self.lineBand = None
        self.resultLayers = []
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
        parameterList.append(("Parameters", "group"))
        parameterList.append(("RNAV Specification", self.parametersPanel.cmbRnavSpecification.currentText()))
        parameterList.append(("Number of DMEs Used", self.parametersPanel.cmbDmeCount.currentText()))
        parameterList.append(("Use 2 Waypoints", str(self.parametersPanel.chbUse2Waypoints.isChecked())))

        if not self.parametersPanel.chbUse2Waypoints.isChecked():
            parameterList.append(("Waypoint Position", "group"))
            parameterList.append(("Phase of Flight", self.parametersPanel.cmbFlightPhase1.currentText()))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlPosWpt1.txtPointX.text()), float(self.parametersPanel.pnlPosWpt1.txtPointY.text()))

            parameterList.append(("Lat", self.parametersPanel.pnlPosWpt1.txtLat.Value))
            parameterList.append(("Lon", self.parametersPanel.pnlPosWpt1.txtLong.Value))
            parameterList.append(("X", self.parametersPanel.pnlPosWpt1.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlPosWpt1.txtPointY.text()))

            parameterList.append(("Aircraft Altitude", self.parametersPanel.txtAltitude1.text() + "ft"))
        else:
            parameterList.append(("Waypoint 1 Position", "group"))
            parameterList.append(("Phase of Flight", self.parametersPanel.cmbFlightPhase1.currentText()))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlPosWpt1.txtPointX.text()), float(self.parametersPanel.pnlPosWpt1.txtPointY.text()))

            parameterList.append(("Lat", self.parametersPanel.pnlPosWpt1.txtLat.Value))
            parameterList.append(("Lon", self.parametersPanel.pnlPosWpt1.txtLong.Value))
            parameterList.append(("X", self.parametersPanel.pnlPosWpt1.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlPosWpt1.txtPointY.text()))
            parameterList.append(("Aircraft Altitude", self.parametersPanel.txtAltitude1.text() + "ft"))

            parameterList.append(("Waypoint 2 Position", "group"))
            parameterList.append(("Phase of Flight", self.parametersPanel.cmbFlightPhase2.currentText()))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlPosWpt2.txtPointX.text()), float(self.parametersPanel.pnlPosWpt2.txtPointY.text()))

            parameterList.append(("Lat", self.parametersPanel.pnlPosWpt2.txtLat.Value))
            parameterList.append(("Lon", self.parametersPanel.pnlPosWpt2.txtLong.Value))
            parameterList.append(("X", self.parametersPanel.pnlPosWpt2.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlPosWpt2.txtPointY.text()))
            parameterList.append(("Aircraft Altitude", self.parametersPanel.txtAltitude2.text() + "ft"))

        if not self.parametersPanel.chbUse2Waypoints.isChecked():
            parameterList.append(("Nominal Track", "Plan : " + str(self.parametersPanel.txtTrack.txtRadialPlan.Value) + define._degreeStr))
            parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtTrack.txtRadialGeodetic.Value) + define._degreeStr))

            # parameterList.append(("Nominal Track", self.parametersPanel.txtTrack.Value))
        parameterList.append(("Selection Mode", self.parametersPanel.cmbSelectionMode.currentText()))
        parameterList.append(("Altitude", self.parametersPanel.txtAltitude.text() + "ft"))
        parameterList.append(("Primary Moc", self.parametersPanel.txtPrimaryMoc.text() + "m"))
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstruct.currentText()))
        parameterList.append(("MOCmultipiler", str(self.parametersPanel.mocSpinBox.value())))

        parameterList.append(("Draw Waypoint Tolerance", str(self.parametersPanel.chbDrawTolerance.isChecked())))

        parameterList.append(("Results", "group"))
        parameterList.append(("Waypoint1", "group"))
        parameterList.append(("XTT", self.parametersPanel.txtXtt1.text() + "nm"))
        parameterList.append(("Att", self.parametersPanel.txtAtt1.text() + "nm"))
        parameterList.append(("1/2 A/W", self.parametersPanel.txtAsw1.text() + "nm"))

        parameterList.append(("Waypoint2", "group"))
        parameterList.append(("XTT", self.parametersPanel.txtXtt2.text() + "nm"))
        parameterList.append(("Att", self.parametersPanel.txtAtt2.text() + "nm"))
        parameterList.append(("1/2 A/W", self.parametersPanel.txtAsw2.text() + "nm"))


        parameterList.append(("Results / Checked Obstacles", "group"))
        parameterList.append(("Checked Obstacles", "group"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        return parameterList

    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        if self.lineBand != None:
            QgisHelper.ClearRubberBandInCanvas(define._canvas, [self.lineBand])
            self.lineBand = None
        if not self.method_28():
            return
        self.complexObstacleArea = ComplexObstacleArea()
        resultPolylineAreaList = []
        num = 0.0
        point3d = self.parametersPanel.pnlPosWpt1.Point3d;
        origin = Point3D.get_Origin();
        if (not self.parametersPanel.chbUse2Waypoints.isChecked()):
            origin = Point3D.get_Origin();
            num = Unit.ConvertDegToRad(float(self.parametersPanel.txtTrack.Value));
        else:
            origin = self.parametersPanel.pnlPosWpt2.Point3d;
            num = MathHelper.getBearing(point3d, origin);
#         Document activeDocument = AcadHelper.ActiveDocument;
#         using (DocumentLock documentLock = activeDocument.LockDocument())
#         {
#             using (Transaction transaction = activeDocument.get_Database().get_TransactionManager().StartTransaction())
#             {
#                 BlockTableRecord blockTableRecord = AcadHelper.smethod_32(1, transaction, activeDocument.get_Database());
        aTT = RnavDmeDme.Result1.ATT;
        point3d1 = MathHelper.distanceBearingPoint(point3d, num - 3.14159265358979, aTT.Metres);
        xTT = RnavDmeDme.Result1.XTT;
        point3d2 = MathHelper.distanceBearingPoint(point3d1, num - 1.5707963267949, xTT.Metres);
        distance = RnavDmeDme.Result1.ATT;
        point3d3 = MathHelper.distanceBearingPoint(point3d2, num, distance.Metres * 2);
        xTT1 = RnavDmeDme.Result1.XTT;
        point3d4 = MathHelper.distanceBearingPoint(point3d3, num + 1.5707963267949, xTT1.Metres * 2);
        aTT1 = RnavDmeDme.Result1.ATT;
        point3d5 = MathHelper.distanceBearingPoint(point3d4, num - 3.14159265358979, aTT1.Metres * 2);
        point3dArray = [point3d2, point3d3, point3d4, point3d5, point3d2]

        if self.parametersPanel.chbDrawTolerance.isChecked():
            resultPolylineAreaList.append(PolylineArea(point3dArray))

        # self.complexObstacleArea.Add(PrimaryObstacleArea(PolylineArea(point3dArray)))
#         AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(point3dArray), constructionLayer);
        aSW = RnavDmeDme.Result1.ASW;
        point3d6 = MathHelper.distanceBearingPoint(point3d, num - 1.5707963267949, aSW.Metres);
        aSW1 = RnavDmeDme.Result1.ASW;
        point3d7 = MathHelper.distanceBearingPoint(point3d, num + 1.5707963267949, aSW1.Metres);
        point3dArray1 = [point3d6, point3d7]
        resultPolylineAreaList.append(PolylineArea(point3dArray1))

        self.complexObstacleArea.NominalTrack = Unit.ConvertDegToRad(float(self.parametersPanel.txtTrack.Value))
#         AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(point3dArray1), constructionLayer);
        if (self.parametersPanel.chbUse2Waypoints.isChecked()):
            distance1 = RnavDmeDme.Result2.ATT;
            point3d1 = MathHelper.distanceBearingPoint(origin, num - 3.14159265358979, distance1.Metres);
            xTT2 = RnavDmeDme.Result2.XTT;
            point3d2 = MathHelper.distanceBearingPoint(point3d1, num - 1.5707963267949, xTT2.Metres);
            aTT2 = RnavDmeDme.Result2.ATT;
            point3d3 = MathHelper.distanceBearingPoint(point3d2, num, aTT2.Metres * 2);
            distance2 = RnavDmeDme.Result2.XTT;
            point3d4 = MathHelper.distanceBearingPoint(point3d3, num + 1.5707963267949, distance2.Metres * 2);
            aTT3 = RnavDmeDme.Result2.ATT;
            point3d5 = MathHelper.distanceBearingPoint(point3d4, num - 3.14159265358979, aTT3.Metres * 2);
            point3dArray2 = [point3d2, point3d3, point3d4, point3d5, point3d2]
            if self.parametersPanel.chbDrawTolerance.isChecked():
                resultPolylineAreaList.append(PolylineArea(point3dArray2))

            # self.complexObstacleArea.Add(PrimaryObstacleArea(PolylineArea(point3dArray2)))
#             AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(point3dArray2), constructionLayer);
            aSW2 = RnavDmeDme.Result2.ASW;
            point3d8 = MathHelper.distanceBearingPoint(origin, num - 1.5707963267949, aSW2.Metres);
            aSW3 = RnavDmeDme.Result2.ASW;
            point3d9 = MathHelper.distanceBearingPoint(origin, num + 1.5707963267949, aSW3.Metres);
            point3dArray3 = [point3d8, point3d9]
            resultPolylineAreaList.append(PolylineArea(point3dArray3))
#             AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(point3dArray3), constructionLayer);
            point3dArray4 = [point3d6, point3d8]
            resultPolylineAreaList.append(PolylineArea(point3dArray4))
#             AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(point3dArray4), constructionLayer);
            point3dArray5 = [point3d7, point3d9]
            resultPolylineAreaList.append(PolylineArea(point3dArray5))
#             AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(point3dArray5), constructionLayer);
            distance3 = RnavDmeDme.Result1.ASW;
            point3d6 = MathHelper.distanceBearingPoint(point3d, num - 1.5707963267949, distance3.Metres / 2);
            aSW4 = RnavDmeDme.Result1.ASW;
            point3d7 = MathHelper.distanceBearingPoint(point3d, num + 1.5707963267949, aSW4.Metres / 2);
            distance4 = RnavDmeDme.Result2.ASW;
            point3d8 = MathHelper.distanceBearingPoint(origin, num - 1.5707963267949, distance4.Metres / 2);
            aSW5 = RnavDmeDme.Result2.ASW;
            point3d9 = MathHelper.distanceBearingPoint(origin, num + 1.5707963267949, aSW5.Metres / 2);
            point3dArray6 = [point3d6, point3d8]
            resultPolylineAreaList.append(PolylineArea(point3dArray6))
#             AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(point3dArray6), constructionLayer);
            point3dArray7 = [point3d7, point3d9]
            resultPolylineAreaList.append(PolylineArea(point3dArray7))

            if MathHelper.calcDistance(point3dArray6[0], point3dArray7[0]) < MathHelper.calcDistance(point3dArray6[0], point3dArray7[1]):
                pointArray = [point3dArray6[0], point3dArray7[0], point3dArray7[1], point3dArray6[1]]
            else:
                pointArray = [point3dArray6[0], point3dArray7[1], point3dArray7[0], point3dArray6[1]]

            self.complexObstacleArea.Add(PrimaryObstacleArea(PolylineArea(pointArray)))

            if MathHelper.calcDistance(point3dArray4[0], point3dArray6[0]) < MathHelper.calcDistance(point3dArray4[0], point3dArray6[1]):
                pointArray = [point3dArray4[0], point3dArray6[0], point3dArray6[1], point3dArray4[1]]
            else:
                pointArray = [point3dArray4[0], point3dArray6[1], point3dArray6[0], point3dArray4[1]]

            self.complexObstacleArea.Add(SecondaryObstacleArea(pointArray[1], pointArray[2], pointArray[0], pointArray[3], MathHelper.getBearing(pointArray[1], pointArray[2])))

            if MathHelper.calcDistance(point3dArray5[0], point3dArray7[0]) < MathHelper.calcDistance(point3dArray5[0], point3dArray7[1]):
                pointArray = [point3dArray5[0], point3dArray7[0], point3dArray7[1], point3dArray5[1]]
            else:
                pointArray = [point3dArray5[0], point3dArray7[1], point3dArray7[0], point3dArray5[1]]

            self.complexObstacleArea.Add(SecondaryObstacleArea(pointArray[1], pointArray[2], pointArray[0], pointArray[3], MathHelper.getBearing(pointArray[1], pointArray[2])))

#             AcadHelper.smethod_18(transaction, blockTableRecord, AcadHelper.smethod_126(point3dArray7), constructionLayer);
#                 }
#         resultPolylineAreaList.append(PolylineArea([self.parametersPanel.pnlPosWpt1.Point3d, self.parametersPanel.pnlPosWpt2.Point3d]))
        mapUnits = define._canvas.mapUnits()
        constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)
        for polylineArea in resultPolylineAreaList:
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea)

        selctFlyDlg = SelectFlyDlg()
        selctFlyDlg.ui_SelectFly.groupBoxWaypoint2.setVisible(self.parametersPanel.chbUse2Waypoints.isChecked())

        selctFlyDlg.exec_()
        # if len(self.resultLayers) != 0:
        #     QgisHelper.removeFromCanvas(define._canvas, self.resultLayers)
        if self.parametersPanel.chbUse2Waypoints.isChecked():
            wptLayer = self.WPT2Layer(selctFlyDlg.FlyWpt1, selctFlyDlg.FlyWpt2)
            self.resultLayers = [constructionLayer, wptLayer, self.nominal2Layer()]
        else:
            wptLayer = self.WPT2Layer(selctFlyDlg.FlyWpt1)
            self.resultLayers = [constructionLayer, wptLayer]

        QgisHelper.appendToCanvas(define._canvas, self.resultLayers, SurfaceTypes.RnavDmeDme)
        self.resultLayerList = self.resultLayers
        QgisHelper.zoomToLayers([constructionLayer])
        self.ui.btnEvaluate.setEnabled(True)

    def initParametersPan(self):
        ui = Ui_RnavDmeDme()
        self.parametersPanel = ui
        
        
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.gbVorDmePosition.setVisible(False)

        self.parametersPanel.pnlPosWpt1 = PositionPanel(self.parametersPanel.gbWaypoint1)
        self.parametersPanel.pnlPosWpt1.groupBox.setTitle("Position")
#         
        self.parametersPanel.pnlPosWpt1.hideframe_Altitude()
        self.parametersPanel.pnlPosWpt1.setObjectName("posiWaypoint1")
        self.parametersPanel.pnlPosWpt1.btnCalculater.hide()
        self.parametersPanel.verticalLayoutWaypoint1.insertWidget(1, self.parametersPanel.pnlPosWpt1)
        self.connect(self.parametersPanel.pnlPosWpt1, SIGNAL("positionChanged"), self.drawLineBand)

        self.parametersPanel.pnlPosWpt2 = PositionPanel(self.parametersPanel.gbWaypoint2)
        self.parametersPanel.pnlPosWpt2.groupBox.setTitle("Position")
#         
        self.parametersPanel.pnlPosWpt2.hideframe_Altitude()
        self.parametersPanel.pnlPosWpt2.setObjectName("posiWaypoint2")
        self.parametersPanel.pnlPosWpt2.btnCalculater.hide()
        self.parametersPanel.verticalLayoutWaypoint2.insertWidget(1, self.parametersPanel.pnlPosWpt2)
        self.connect(self.parametersPanel.pnlPosWpt2, SIGNAL("positionChanged"), self.drawLineBand)

        self.parametersPanel.chbUse2Waypoints.setChecked(True)
        self.parametersPanel.txtTrack.Visible = False
        self.parametersPanel.cmbRnavSpecification.addItems(["Rnav5", "Rnav2", "Rnav1"])
        self.parametersPanel.cmbRnavSpecification.setCurrentIndex(2)
        
        self.parametersPanel.cmbDmeCount.addItems(["2", "More than 2"])
        self.parametersPanel.cmbFlightPhase1.addItems(["En-route/STAR/SID(>30nm ARP)", "STAR/SID/IF/IAF(<30nm ARP)", "SID(<15nm ARP)"])
        self.parametersPanel.cmbFlightPhase2.addItems(["En-route/STAR/SID(>30nm ARP)", "STAR/SID/IF/IAF(<30nm ARP)", "SID(<15nm ARP)"])
        
        self.parametersPanel.chbUse2Waypoints.clicked.connect(self.chbUse2Waypoints_clicked)
        # self.parametersPanel.btnCaptureTrack.clicked.connect(self.captureBearing)
        self.parametersPanel.pnlPosWpt1.txtPointX.textChanged.connect(self.method_28)
        self.parametersPanel.pnlPosWpt1.txtPointY.textChanged.connect(self.method_28)
        self.parametersPanel.pnlPosWpt2.txtPointX.textChanged.connect(self.method_28)
        self.parametersPanel.pnlPosWpt2.txtPointY.textChanged.connect(self.method_28)
        self.parametersPanel.cmbDmeCount.currentIndexChanged.connect(self.method_28)
        self.parametersPanel.cmbFlightPhase1.currentIndexChanged.connect(self.method_28)
        self.parametersPanel.cmbFlightPhase2.currentIndexChanged.connect(self.method_28)
        self.parametersPanel.cmbRnavSpecification.currentIndexChanged.connect(self.chbUse2Waypoints_clicked)
        self.parametersPanel.txtAltitude1.textChanged.connect(self.method_28)
        self.parametersPanel.txtAltitude2.textChanged.connect(self.method_28)

        self.parametersPanel.cmbSelectionMode.addItems(["Automatic", "Manual"])
        self.parametersPanel.cmbSelectionMode.currentIndexChanged.connect(self.manualEvent)
        self.parametersPanel.cmbConstruct.addItems(["2D", "3D"])

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

        self.parametersPanel.txtAltitudeM1.textChanged.connect(self.txtAltitudeM1Changed)
        self.parametersPanel.txtAltitude1.textChanged.connect(self.txtAltitudeFt1Changed)

        self.flag1 = 0
        if self.flag1==0:
            self.flag1=2;
        if self.flag1==1:
            self.flag1=0;
        if self.flag1==2:
            try:
                self.parametersPanel.txtAltitudeM1.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude1.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM1.setText("0.0")

        self.parametersPanel.txtAltitudeM2.textChanged.connect(self.txtAltitudeM2Changed)
        self.parametersPanel.txtAltitude2.textChanged.connect(self.txtAltitudeFt2Changed)

        self.flag2 = 0
        if self.flag2==0:
            self.flag2=2;
        if self.flag2==1:
            self.flag2=0;
        if self.flag2==2:
            try:
                self.parametersPanel.txtAltitudeM2.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude2.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM2.setText("0.0")

        self.parametersPanel.txtPrimaryMoc.textChanged.connect(self.txtMocMChanged)
        self.parametersPanel.txtPrimaryMocFt.textChanged.connect(self.txtMocFtChanged)

        self.flag3 = 0
        if self.flag3==0:
            self.flag3=1;
        if self.flag3==2:
            self.flag3=0;
        if self.flag3==1:
            try:
                self.parametersPanel.txtPrimaryMocFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtPrimaryMoc.text())), 4)))
            except:
                self.parametersPanel.txtPrimaryMocFt.setText("0.0")


        self.chbUse2Waypoints_clicked()
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

    def txtAltitudeM1Changed(self):
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtAltitude1.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAltitudeM1.text())), 4)))
            except:
                self.parametersPanel.txtAltitude1.setText("0.0")
    def txtAltitudeFt1Changed(self):
        if self.flag1==0:
            self.flag1=2;
        if self.flag1==1:
            self.flag1=0;
        if self.flag1==2:
            try:
                self.parametersPanel.txtAltitudeM1.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude1.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM1.setText("0.0")
    def txtAltitudeM2Changed(self):
        if self.flag2==0:
            self.flag2=1;
        if self.flag2==2:
            self.flag2=0;
        if self.flag2==1:
            try:
                self.parametersPanel.txtAltitude2.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAltitudeM2.text())), 4)))
            except:
                self.parametersPanel.txtAltitude2.setText("0.0")
    def txtAltitudeFt2Changed(self):
        if self.flag2==0:
            self.flag2=2;
        if self.flag2==1:
            self.flag2=0;
        if self.flag2==2:
            try:
                self.parametersPanel.txtAltitudeM2.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude2.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM2.setText("0.0")

    def txtMocMChanged(self):
        if self.flag3==0:
            self.flag3=1;
        if self.flag3==2:
            self.flag3=0;
        if self.flag3==1:
            try:
                self.parametersPanel.txtPrimaryMocFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtPrimaryMoc.text())), 4)))
            except:
                self.parametersPanel.txtPrimaryMocFt.setText("0.0")
    def txtMocFtChanged(self):
        if self.flag3==0:
            self.flag3=2;
        if self.flag3==1:
            self.flag3=0;
        if self.flag3==2:
            try:
                self.parametersPanel.txtPrimaryMoc.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtPrimaryMocFt.text())), 4)))
            except:
                self.parametersPanel.txtPrimaryMoc.setText("0.0")
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
    def outputResultMethod(self):
        self.manualPolygon = self.toolSelectByPolygon.polygonGeom
    def btnEvaluate_Click(self):
        if self.complexObstacleArea == None:
            return
        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        self.obstaclesModel = RnavDmeDmeObstacles(self.complexObstacleArea, Altitude(float(self.parametersPanel.txtPrimaryMoc.text())), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), self.manualPolygon );

#             self.parametersPanel.frameAltitude.setE
        return FlightPlanBaseDlg.btnEvaluate_Click(self)

    def chbUse2Waypoints_clicked(self):
        self.parametersPanel.cmbFlightPhase1.clear()
        self.parametersPanel.cmbFlightPhase2.clear()
        self.parametersPanel.frame_60.setEnabled(self.parametersPanel.cmbRnavSpecification.currentIndex() > 0)
        self.parametersPanel.frame_61.setEnabled(self.parametersPanel.cmbRnavSpecification.currentIndex() > 0)
        if (self.parametersPanel.cmbRnavSpecification.currentIndex() == 0):
            self.parametersPanel.cmbFlightPhase1.addItems(["En-route/STAR/SID(>30nm ARP)", "STAR/SID/IF/IAF(<30nm ARP)", "SID(<15nm ARP)"])
            self.parametersPanel.cmbFlightPhase2.addItems(["En-route/STAR/SID(>30nm ARP)", "STAR/SID/IF/IAF(<30nm ARP)", "SID(<15nm ARP)"])

            self.parametersPanel.cmbFlightPhase1.setCurrentIndex(0);
            self.parametersPanel.cmbFlightPhase2.setCurrentIndex(0)
        else:
            self.parametersPanel.cmbFlightPhase1.addItems(["En-route/STAR/SID(>30nm ARP)", "STAR/SID/IF/IAF(<30nm ARP)", "SID(<15nm ARP)", "Faf"])
            self.parametersPanel.cmbFlightPhase2.addItems(["En-route/STAR/SID(>30nm ARP)", "STAR/SID/IF/IAF(<30nm ARP)", "SID(<15nm ARP)", "Faf"])

        self.parametersPanel.txtTrack.Visible = not self.parametersPanel.chbUse2Waypoints.isChecked()
        self.parametersPanel.gbWaypoint2.setVisible(self.parametersPanel.chbUse2Waypoints.isChecked());
        self.parametersPanel.gbResultsWaypoint2.setVisible(self.parametersPanel.chbUse2Waypoints.isChecked());

        if not self.parametersPanel.chbUse2Waypoints.isChecked():
            self.parametersPanel.gbWaypoint1.setTitle("Waypoint")
            self.parametersPanel.gbResultsWaypoint1.setTitle("Waypoint")
        else:
            self.parametersPanel.gbWaypoint1.setTitle("Waypoint1")
            self.parametersPanel.gbResultsWaypoint1.setTitle("Waypoint1")
        self.method_28()
        # self.parametersPanel.gbWaypoint2.setVisible(bool_0)
        # self.parametersPanel.frame_TrackFrom.setVisible(not bool_0)

    
    # def captureBearing(self):
    #     self.captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrack)
    #     define._canvas.setMapTool(self.captureTrackTool)
    def nominal2Layer(self):
        return AcadHelper.createNominalTrackLayer([self.parametersPanel.pnlPosWpt1.Point3d, self.parametersPanel.pnlPosWpt2.Point3d], None, "memory", "NominalTrack_" + self.surfaceType.replace(" ", "_"))
    def WPT2Layer(self,flyWpt1, flyWpt2 = None):
        mapUnits = define._canvas.mapUnits()
        if define._mapCrs == None:
            if mapUnits == QGis.Meters:
                resultLayer = QgsVectorLayer("Point?crs=EPSG:32633", "WPT_RnavDmeDme", "memory")
            else:
                resultLayer = QgsVectorLayer("Point?crs=EPSG:4326", "WPT_RnavDmeDme", "memory")
        else:
            resultLayer = QgsVectorLayer("Point?crs=%s"%define._mapCrs.authid (), "WPT_RnavDmeDme", "memory")
        shpPath = ""
        if define.obstaclePath != None:
            shpPath = define.obstaclePath
        elif define.xmlPath != None:
            shpPath = define.xmlPath
        else:
            shpPath = define.appPath
        er = QgsVectorFileWriter.writeAsVectorFormat(resultLayer, shpPath + "/" + "WPT_RnavDmeDme" + ".shp", "utf-8", resultLayer.crs())
        resultLayer = QgsVectorLayer(shpPath + "/" + "WPT_RnavDmeDme" + ".shp", "WPT_RnavDmeDme", "ogr")

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

        if flyWpt2 != None:
            feature.setGeometry(QgsGeometry.fromPoint (self.parametersPanel.pnlPosWpt1.Point3d))
            feature.setAttribute(fieldName, "Waypoint1")
            pr = resultLayer.dataProvider()
            pr.addFeatures([feature])
            # resultLayer.addFeature(feature)
            feature.setGeometry(QgsGeometry.fromPoint (self.parametersPanel.pnlPosWpt2.Point3d))
            feature.setAttribute(fieldName, "Waypoint2")
            pr = resultLayer.dataProvider()
            pr.addFeatures([feature])
            # resultLayer.addFeature(feature)
        else:
            feature.setGeometry(QgsGeometry.fromPoint (self.parametersPanel.pnlPosWpt1.Point3d))
            feature.setAttribute(fieldName, "Waypoint1")
            pr = resultLayer.dataProvider()
            pr.addFeatures([feature])
            # resultLayer.addFeature(feature)

        resultLayer.commitChanges()

        '''FlyOver'''
        mawpBearing = MathHelper.getBearing(self.parametersPanel.pnlPosWpt1.Point3d, self.parametersPanel.pnlPosWpt2.Point3d)
        symbolFlyOver = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
        symbolFlyOver.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyover.svg", 10.0, 0.0)
        symbolFlyOver.appendSymbolLayer(svgSymLayer)
        renderCatFlyOver = QgsRendererCategoryV2(1, symbolFlyOver,"Fly Over")

        '''FlyBy'''
        symbolFlyBy = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
        symbolFlyBy.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyby.svg", 10.0, 0.0)
        symbolFlyBy.appendSymbolLayer(svgSymLayer)
        renderCatFlyBy = QgsRendererCategoryV2(0, symbolFlyBy,"Fly By")

        symRenderer = None
        if flyWpt1 == flyWpt2:
            if flyWpt1 == 0:
                VORDME_WPT_EXPRESION = "CASE WHEN  \"CATEGORY\" = 'Waypoint1'  THEN 0 " + \
                                        "WHEN \"CATEGORY\" = 'Waypoint2' THEN 0 " + \
                                        "END"
                symRenderer = QgsCategorizedSymbolRendererV2(VORDME_WPT_EXPRESION, [renderCatFlyBy])
            else:
                VORDME_WPT_EXPRESION = "CASE WHEN  \"CATEGORY\" = 'Waypoint1'  THEN 1 " + \
                                        "WHEN \"CATEGORY\" = 'Waypoint2' THEN 1 " + \
                                        "END"
                symRenderer = QgsCategorizedSymbolRendererV2(VORDME_WPT_EXPRESION, [renderCatFlyOver])
        else:
            if flyWpt1 == 0:
                VORDME_WPT_EXPRESION = "CASE WHEN  \"CATEGORY\" = 'Waypoint1'  THEN 0 " + \
                                        "WHEN \"CATEGORY\" = 'Waypoint2' THEN 1 " + \
                                        "END"
                symRenderer = QgsCategorizedSymbolRendererV2(VORDME_WPT_EXPRESION, [renderCatFlyBy, renderCatFlyOver])
            else:
                VORDME_WPT_EXPRESION = "CASE WHEN  \"CATEGORY\" = 'Waypoint1'  THEN 1 " + \
                                        "WHEN \"CATEGORY\" = 'Waypoint2' THEN 0 " + \
                                        "END"
                symRenderer = QgsCategorizedSymbolRendererV2(VORDME_WPT_EXPRESION, [renderCatFlyBy, renderCatFlyOver])


        resultLayer.setRendererV2(symRenderer)
        return resultLayer
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
                pointWpt1 = self.parametersPanel.pnlPosWpt1.Point3d
                pointList.append(pointWpt1)
            except UserWarning:
                pass
            try:
                pointWpt2 = self.parametersPanel.pnlPosWpt2.Point3d
                pointList.append(pointWpt2)
            except:
                pass

            if len(pointList) > 1:
                for pt in pointList:
                    if pt == None:
                        return
                self.lineBand.addGeometry(QgsGeometry.fromPolyline(pointList),None)

        except UnboundLocalError:
            return

        finally:
            try:
                self.lineBand.show()
            except:
                pass
    def method_28(self):
#         RnavDmeDmeFlightPhase rnavDmeDmeFlightPhase;
        RnavDmeDme.Result1 = None;
        RnavDmeDme.Result2 = None;
        try:
            try:
                rnavSpecification = self.parametersPanel.cmbRnavSpecification.currentText()
                rnavDmeDmeCriterium = self.parametersPanel.cmbDmeCount.currentIndex()
                flag = True;
                rnavDmeDmeFlightPhase = self.parametersPanel.cmbFlightPhase1.currentIndex() if(rnavSpecification != RnavSpecification.Rnav5) else RnavDmeDmeFlightPhase.EnrouteStarSid
                RnavDmeDme.Result1 = RnavDmeDmeTolerance(rnavSpecification, rnavDmeDmeFlightPhase, rnavDmeDmeCriterium, Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT));
                if (self.parametersPanel.chbUse2Waypoints.isChecked()):
                    rnavSpecification = self.parametersPanel.cmbRnavSpecification.currentText()
                    rnavDmeDmeCriterium = self.parametersPanel.cmbDmeCount.currentIndex()
                    rnavDmeDmeFlightPhase = self.parametersPanel.cmbFlightPhase2.currentIndex() if(rnavSpecification != RnavSpecification.Rnav5) else RnavDmeDmeFlightPhase.EnrouteStarSid
                    RnavDmeDme.Result2 = RnavDmeDmeTolerance(rnavSpecification, rnavDmeDmeFlightPhase, rnavDmeDmeCriterium, Altitude(float(self.parametersPanel.txtAltitude2.text()), AltitudeUnits.FT));
                    # RnavDmeDme.Result2 = RnavGnssTolerance(rnavSpecification, RnavGnssFlightPhase.Faf, None, None)
            finally:
                self.parametersPanel.txtXtt1.setText(str(round(RnavDmeDme.Result1.XTT.NauticalMiles, 2)) if(RnavDmeDme.Result1 != None) else "0")
                self.parametersPanel.txtAtt1.setText(str(round(RnavDmeDme.Result1.ATT.NauticalMiles, 2)) if(RnavDmeDme.Result1 != None) else "0")
                self.parametersPanel.txtAsw1.setText(str(round(RnavDmeDme.Result1.ASW.NauticalMiles, 2)) if(RnavDmeDme.Result1 != None) else "0")
                self.parametersPanel.txtXtt2.setText(str(round(RnavDmeDme.Result2.XTT.NauticalMiles, 2)) if(RnavDmeDme.Result2 != None) else "0")
                self.parametersPanel.txtAtt2.setText(str(round(RnavDmeDme.Result2.ATT.NauticalMiles, 2)) if(RnavDmeDme.Result2 != None) else "0")
                self.parametersPanel.txtAsw2.setText(str(round(RnavDmeDme.Result2.ASW.NauticalMiles, 2)) if(RnavDmeDme.Result2 != None) else "0")
        except:
            pass
        if (not self.parametersPanel.chbUse2Waypoints.isChecked()):
            return RnavDmeDme.Result1 != None;
        if (RnavDmeDme.Result1 == None):
            return False;
        return RnavDmeDme.Result2 != None;    
class RnavDmeDmeTolerance:
    def __init__(self, rnavSpecification_0, rnavDmeDmeFlightPhase_0, rnavDmeDmeCriteria_0, altitude_0):
#         double num;
#         double num1;
        if rnavSpecification_0 == RnavSpecification.Rnav5:
            if (rnavDmeDmeFlightPhase_0 != RnavDmeDmeFlightPhase.EnrouteStarSid):
                self.xtt = Distance(0);
                self.att = Distance(0);
                self.asw = Distance(0);
                return
#                 throw new ArgumentException(string.Format(Validations.RNAV_FLIGHT_PHASE_NOT_SUPPORTED, EnumHelper.smethod_0(rnavDmeDmeFlightPhase_0)));
            num = 2.5;
        elif rnavSpecification_0 == RnavSpecification.Rnav2:
            if (rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.Faf):
                self.xtt = Distance(0);
                self.att = Distance(0);
                self.asw = Distance(0);
                return
            num = 1;
        elif rnavSpecification_0 == RnavSpecification.Rnav1:
            if (rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.Faf):
                num = 0.25;
            else:
                num = 0.5;
        else:
            self.xtt = Distance(0);
            self.att = Distance(0);
            self.asw = Distance(0);
            return
        if rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.EnrouteStarSid:
            num1 = 2;
        elif rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.Star30Sid30IfIaf:
            num1 = 1;
        elif rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.Sid15 or rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.Faf:
            num1 = 0.5;
        else:
            self.xtt = Distance(0);
            self.att = Distance(0);
            self.asw = Distance(0);
            return
        num2 = 0.25;
        num3 = Unit.ConvertDegToRad(90);
        if (rnavDmeDmeCriteria_0 == RnavDmeDmeCriteria.Two):
            num3 = Unit.ConvertDegToRad(30);
        num4 = 1.23 * math.sqrt(altitude_0.Feet);
        if (rnavSpecification_0 == RnavSpecification.Rnav5):
            num4 = 300;
        elif (rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.EnrouteStarSid):
            num4 = 1.23 * math.sqrt(15000);
        num5 = max([0.085, 0.00125 * num4]);
        num6 = 0.05;
        num7 = 2 * math.sqrt(2 * (num5 * num5 + num6 * num6)) / math.sin(num3);
        self.xtt = Distance(math.sqrt(num7 * num7 + num * num + num2 * num2), DistanceUnits.NM);
        self.att = Distance(math.sqrt(num7 * num7 + num2 * num2), DistanceUnits.NM);
        self.asw = Distance(1.5 * self.xtt.NauticalMiles + num1, DistanceUnits.NM);
    
    def get_asw(self):
        return self.asw
    ASW = property(get_asw, None, None, None)
    
    def get_xtt(self):
        return self.xtt
    XTT = property(get_xtt, None, None, None)
    
    def get_att(self):
        return self.att
    ATT = property(get_att, None, None, None)

class RnavDmeDmeObstacles(ObstacleTable):
    def __init__(self, complexObstacleArea_0, altitude_0, altitude_1, manualPoly):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, None)
        self.manualPolygon = manualPoly
        self.surfaceType = SurfaceTypes.RnavVorDme
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
        obstacleAreaResult, num, num1 = self.area.pointInArea(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier);
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