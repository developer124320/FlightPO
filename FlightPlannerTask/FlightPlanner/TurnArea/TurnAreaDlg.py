# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QSize, Qt
from PyQt4.QtGui import QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsCoordinateReferenceSystem,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType, SurfaceTypes, DistanceUnits, SpeedUnits,AircraftSpeedCategory, OrientationType, AltitudeUnits, ObstacleAreaResult
from FlightPlanner.TurnArea.ui_TurnArea import Ui_TurnArea
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.Panels.WindPanel import WindPanel
from FlightPlanner.Holding.HoldingTemplateBase import HoldingTemplateBase
from FlightPlanner.types import Point3D
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.Prompts import Prompts
from FlightPlanner.captureCoordinateTool import CaptureCoordinateToolUpdate

import define

class TurnAreaDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.resize(600, 500)
        self.setObjectName("TurnAreaDlg")
        self.surfaceType = SurfaceTypes.TurnArea
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.TurnArea)
        self.resize(600, 500)
        QgisHelper.matchingDialogSize(self, 700, 500)
        self.surfaceList = None
        
    
    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(1)
        self.ui.tabCtrlGeneral.removeTab(1)
        self.ui.btnEvaluate.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)
        return FlightPlanBaseDlg.uiStateInit(self)
    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        value = Speed(float(self.parametersPanel.txtIas.text()),SpeedUnits.KTS);
        if (self.parametersPanel.chbDeparture.isChecked()):
            value = value + (value / 10);
        altitude = Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT);
        value1 = float(self.parametersPanel.txtIsa.text());
        num1 = float (self.parametersPanel.txtBankAngle.text());
        self.speedP = self.parametersPanel.pnlWind.Value;
        self.num2P = Unit.ConvertDegToRad(float(self.parametersPanel.txtTrackRadial.Value));
        self.orientationTypeP = self.parametersPanel.cmbOrientation.currentText();
        speed1 = Speed.smethod_0(value, value1, altitude);
        numList = []
        distance = Distance.smethod_1(speed1, num1, numList);
        self.numP = numList[0]
        self.metresP = distance.Metres;

        self.originP = Point3D.get_Origin();
        self.point3dP = Point3D.get_Origin();
        self.origin1P = Point3D.get_Origin();
        self.polylineP = PolylineArea();
        self.flagP = True;


        define._canvas.setMapTool(self.CaptureCoordTool)

    def resultPointValueListMethod(self, resultValueList):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        point  = Point3D()
        try:
            point = Point3D(float(resultValueList[1]), float(resultValueList[2]), float(resultValueList[3]))
        except:
            return
        if (not self.flagP):
            mapUnits = define._canvas.mapUnits()
            self.constructionLayer = AcadHelper.createVectorLayer(self.surfaceType)

            self.point3dP = point.smethod_167(0);
            self.origin1P = self.method_31(self.polylineP, self.originP, self.point3dP, self.numP, self.metresP, self.speedP, self.num2P, self.orientationTypeP);
            AcadHelper.setGeometryAndAttributesInLayer(self.constructionLayer, self.polylineP)
            QgisHelper.appendToCanvas(define._canvas, [self.constructionLayer], self.surfaceType)

            # polyline.Draw();
        else:

            mapUnits = define._canvas.mapUnits()
            self.constructionLayer = AcadHelper.createVectorLayer(self.surfaceType)
            self.originP = point.smethod_167(0);
            self.polylineP, self.origin1P = self.method_30(self.originP, self.numP, self.metresP, self.speedP, self.num2P, self.orientationTypeP);
            AcadHelper.setGeometryAndAttributesInLayer(self.constructionLayer, self.polylineP)
            QgisHelper.appendToCanvas(define._canvas, [self.constructionLayer], self.surfaceType)
            # AcadHelper.smethod_18(transaction, blockTableRecord, polyline, constructionLayer);
        self.flagP = not self.flagP;
        self.resultLayerList = [self.constructionLayer]
        if (not self.flagP):
            define._messageLabel.setText(Prompts.SECOND_POSITION_FINISH);
        else:
            define._messageLabel.setText(Prompts.POSITION_FINISH)
        pass
    def initParametersPan(self):
        ui = Ui_TurnArea()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)
        
        self.parametersPanel.txtTas.setEnabled(False)
        self.CaptureCoordTool = CaptureCoordinateToolUpdate(define._canvas)
        self.connect(self.CaptureCoordTool, SIGNAL("resultPointValueList"), self.resultPointValueListMethod)
        self.parametersPanel.pnlWind = WindPanel(self.parametersPanel.gbParameters)
        self.parametersPanel.pnlWind.lblIA.setMinimumSize(100, 0)
        self.parametersPanel.pnlWind.lblIA.setMaximumSize(100, 10000)
        self.parametersPanel.vl_gbParameters.insertWidget(6, self.parametersPanel.pnlWind)
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT))

        self.parametersPanel.cmbOrientation.addItems(["Right", "Left"])
                
#         self.parametersPanel.cmbHoldingFunctionality.currentIndexChanged.connect(self.cmbHoldingFunctionalityCurrentIndexChanged)
#         self.parametersPanel.cmbOutboundLimit.currentIndexChanged.connect(self.cmbOutboundLimitCurrentIndexChanged)
#         self.parametersPanel.btnCaptureTrack.clicked.connect(self.captureBearing)
#         self.parametersPanel.btnCaptureDistance.clicked.connect(self.measureDistance)
#         self.parametersPanel.btnCaptureLength.clicked.connect(self.measureLength)        
        self.parametersPanel.txtAltitudeFt.textChanged.connect(self.altitudeFtChanged)
        self.parametersPanel.txtAltitudeM.textChanged.connect(self.altitudeMChanged)
#         self.parametersPanel.cmbAircraftCategory.currentIndexChanged.connect(self.changeCategory)
#         self.parametersPanel.btnIasHelp.clicked.connect(self.iasHelpShow)
        self.parametersPanel.txtIas.textChanged.connect(self.iasChanged)
        self.parametersPanel.txtIsa.textChanged.connect(self.isaChanged)
        
        self.parametersPanel.txtTas.setText(str(round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT)).Knots, 4)))

        self.flag = 0
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitudeFt.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")
    def iasChanged(self):
        try:
            self.parametersPanel.txtTas.setText(str(round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT)).Knots, 4)))
        except:
            raise ValueError("Value Invalid")
    def isaChanged(self):
        try:
            self.parametersPanel.txtTas.setText(str(round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT)).Knots, 4)))
        except:
            raise ValueError("Value Invalid")    
    # def iasHelpShow(self):
    #     dlg = IasHelpDlg()
    #     dlg.exec_()
    def altitudeFtChanged(self):
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtAltitudeM.setText(str(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitudeFt.text()))))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")

        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT))
        try:
            self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT)).Knots))
        except:
            raise ValueError("Value Invalid")
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

        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT))
        try:
            self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT)).Knots))
        except:
            raise ValueError("Value Invalid")

    def captureBearing(self):
        self.captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrackRadial)
        define._canvas.setMapTool(self.captureTrackTool)
    # def measureDistance(self):
    #     measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtDistance, DistanceUnits.NM)
    #     define._canvas.setMapTool(measureDistanceTool)
    # def measureLength(self):
    #     measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtLength, DistanceUnits.NM)
    #     define._canvas.setMapTool(measureDistanceTool)
    def method_30(self, point3d_0, double_0, double_1, speed_0, double_2, orientationType_0):
        double0 = 45 / double_0 * speed_0.MetresPerSecond;
        num = 90 / double_0 * speed_0.MetresPerSecond;
        double01 = 135 / double_0 * speed_0.MetresPerSecond;
        num1 = 180 / double_0 * speed_0.MetresPerSecond;
        double02 = 225 / double_0 * speed_0.MetresPerSecond;
        num2 = 270 / double_0 * speed_0.MetresPerSecond;
        num3 = 1;
        if (orientationType_0 == OrientationType.Left):
            num3 = -1;
        point3d = MathHelper.distanceBearingPoint(point3d_0, num3 * 1.5707963267949 + double_2, double_1);
        point3d_1 = point3d;
        point3d1 = MathHelper.distanceBearingPoint(point3d, -1 * num3 * 0.785398163397448 + double_2, double_1 + double0);
        point3d2 = MathHelper.distanceBearingPoint(point3d, double_2, double_1 + num);
        point3d3 = MathHelper.distanceBearingPoint(point3d, num3 * 0.785398163397448 + double_2, double_1 + double01);
        point3d4 = MathHelper.distanceBearingPoint(point3d, num3 * 1.5707963267949 + double_2, double_1 + num1);
        point3d5 = MathHelper.distanceBearingPoint(point3d, num3 * 2.35619449019234 + double_2, double_1 + double02);
        point3d6 = MathHelper.distanceBearingPoint(point3d, num3 * 3.14159265358979 + double_2, double_1 + num2);
        point3d0 = [point3d_0, point3d2, point3d4, point3d6];
        polyline = AcadHelper.smethod_126(point3d0);
        polyline.SetBulgeAt(0, MathHelper.smethod_60(point3d_0, point3d1, point3d2));
        polyline.SetBulgeAt(1, MathHelper.smethod_60(point3d2, point3d3, point3d4));
        polyline.SetBulgeAt(2, MathHelper.smethod_60(point3d4, point3d5, point3d6));
        return (polyline, point3d_1);
    def method_31(self, polyline_0, point3d_0, point3d_1, double_0, double_1, speed_0, double_2, orientationType_0):
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        point3d3 = None;
        point3d4 = None;
        point3d5 = None;
        num = None;
        double0 = 45 / double_0 * speed_0.MetresPerSecond;
        double01 = 90 / double_0 * speed_0.MetresPerSecond;
        num1 = 135 / double_0 * speed_0.MetresPerSecond;
        double02 = 180 / double_0 * speed_0.MetresPerSecond;
        num2 = 225 / double_0 * speed_0.MetresPerSecond;
        double03 = 270 / double_0 * speed_0.MetresPerSecond;
        num3 = MathHelper.getBearing(point3d_0, point3d_1);
        num4 = 1;
        if (orientationType_0 == OrientationType.Left):
            num4 = -1;
        point3d0 = point3d_0;
        point3d11 = point3d_1;
        if (MathHelper.smethod_130(double_2, num3)):
            if (orientationType_0 == OrientationType.Left):
                point3d0 = point3d_1;
                point3d11 = point3d_0;
        elif (orientationType_0 == OrientationType.Right):
            point3d0 = point3d_1;
            point3d11 = point3d_0;
        point3d6 = MathHelper.distanceBearingPoint(point3d0, num4 * 1.5707963267949 + double_2, double_1);
        point3d7 = MathHelper.distanceBearingPoint(point3d6, -1 * num4 * 0.785398163397448 + double_2, double_1 + double0);
        point3d8 = MathHelper.distanceBearingPoint(point3d6, double_2, double_1 + double01);
        point3d9 = MathHelper.distanceBearingPoint(point3d6, num4 * 0.785398163397448 + double_2, double_1 + num1);
        point3d10 = MathHelper.distanceBearingPoint(point3d6, num4 * 1.5707963267949 + double_2, double_1 + double02);
        point3d12 = MathHelper.distanceBearingPoint(point3d6, num4 * 2.35619449019234 + double_2, double_1 + num2);
        point3d13 = MathHelper.distanceBearingPoint(point3d6, num4 * 3.14159265358979 + double_2, double_1 + double03);
        point3d14 = MathHelper.distanceBearingPoint(point3d11, num4 * 1.5707963267949 + double_2, double_1);
        point3d15 = MathHelper.distanceBearingPoint(point3d14, -1 * num4 * 0.785398163397448 + double_2, double_1 + double0);
        point3d16 = MathHelper.distanceBearingPoint(point3d14, double_2, double_1 + double01);
        point3d17 = MathHelper.distanceBearingPoint(point3d14, num4 * 0.785398163397448 + double_2, double_1 + num1);
        point3d18 = MathHelper.distanceBearingPoint(point3d14, num4 * 1.5707963267949 + double_2, double_1 + double02);
        point3d19 = MathHelper.distanceBearingPoint(point3d14, num4 * 2.35619449019234 + double_2, double_1 + num2);
        point3d20 = MathHelper.distanceBearingPoint(point3d14, num4 * 3.14159265358979 + double_2, double_1 + double03);
        point3d_2 = point3d14;
        point3d = MathHelper.smethod_68(point3d0, point3d7, point3d8);
        point3d1 = MathHelper.smethod_68(point3d11, point3d15, point3d16);
        num5 = MathHelper.calcDistance(point3d, point3d8);
        point3d2 = MathHelper.smethod_68(point3d8, point3d9, point3d10);
        point3d3 = MathHelper.smethod_68(point3d16, point3d17, point3d18);
        num6 = MathHelper.calcDistance(point3d2, point3d10);
        point3d4 = MathHelper.smethod_68(point3d10, point3d12, point3d13);
        point3d5 = MathHelper.smethod_68(point3d18, point3d19, point3d20);
        num7 = MathHelper.calcDistance(point3d4, point3d13);
        num3 = MathHelper.getBearing(point3d6, point3d14);
        num3 = num3 - 1.5707963267949 if(orientationType_0 != OrientationType.Left) else num3 + 1.5707963267949;
        num8 = MathHelper.getBearing(point3d, point3d8);
        if (orientationType_0 != OrientationType.Left):
            num = 1 if(not MathHelper.smethod_130(num8, num3)) else 2;
        else:
            num = 2 if(not MathHelper.smethod_130(num8, num3)) else 1;
        if (num == 2):
            num9 = MathHelper.getBearing(point3d, point3d10);
            if (orientationType_0 != OrientationType.Left):
                num = 2 if(not MathHelper.smethod_130(num9, num3)) else 3;
            else:
                num = 3 if(not MathHelper.smethod_130(num9, num3)) else 2;
        if (num == 1):
            num10 = MathHelper.smethod_52(double_2 - num4 * 1.5707963267949, num3, True);
            point3d21 = MathHelper.distanceBearingPoint(point3d, num10, num5);
            point3d22 = MathHelper.distanceBearingPoint(point3d, num3, num5);
            point3d23 = MathHelper.distanceBearingPoint(point3d1, num3, num5);
            num8 = MathHelper.getBearing(point3d1, point3d16);
            num10 = MathHelper.smethod_52(num8, num3, True);
            point3d24 = MathHelper.distanceBearingPoint(point3d1, num10, num5);
            point3dArray = [point3d0, point3d22, point3d23, point3d16, point3d18, point3d20];
            AcadHelper.smethod_121(polyline_0, point3dArray);
            polyline_0.SetBulgeAt(0, MathHelper.smethod_60(point3d0, point3d21, point3d22));
            polyline_0.SetBulgeAt(2, MathHelper.smethod_60(point3d23, point3d24, point3d16));
            polyline_0.SetBulgeAt(3, MathHelper.smethod_60(point3d16, point3d17, point3d18));
            polyline_0.SetBulgeAt(4, MathHelper.smethod_60(point3d18, point3d19, point3d20));
            return point3d_2;
        if (num == 2):
            num8 = MathHelper.getBearing(point3d2, point3d8);
            num11 = MathHelper.smethod_52(num8, num3, True);
            point3d25 = MathHelper.distanceBearingPoint(point3d2, num11, num6);
            point3d26 = MathHelper.distanceBearingPoint(point3d2, num3, num6);
            point3d27 = MathHelper.distanceBearingPoint(point3d3, num3, num6);
            num8 = MathHelper.getBearing(point3d3, point3d18);
            num11 = MathHelper.smethod_52(num3, num8, True);
            point3d28 = MathHelper.distanceBearingPoint(point3d3, num11, num6);
            point3dArray1 = [point3d0, point3d8, point3d26, point3d27, point3d18, point3d20 ];
            AcadHelper.smethod_121(polyline_0, point3dArray1);
            polyline_0.SetBulgeAt(0, MathHelper.smethod_60(point3d0, point3d7, point3d8));
            polyline_0.SetBulgeAt(1, MathHelper.smethod_60(point3d8, point3d25, point3d26));
            polyline_0.SetBulgeAt(3, MathHelper.smethod_60(point3d27, point3d28, point3d18));
            polyline_0.SetBulgeAt(4, MathHelper.smethod_60(point3d18, point3d19, point3d20));
            return point3d_2;
        num8 = MathHelper.getBearing(point3d4, point3d10);
        num12 = MathHelper.smethod_52(num8, num3, True);
        point3d29 = MathHelper.distanceBearingPoint(point3d4, num12, num7);
        point3d30 = MathHelper.distanceBearingPoint(point3d4, num3, num7);
        point3d31 = MathHelper.distanceBearingPoint(point3d5, num3, num7);
        num8 = MathHelper.getBearing(point3d5, point3d20);
        num12 = MathHelper.smethod_52(num3, num8, True);
        point3d32 = MathHelper.distanceBearingPoint(point3d5, num12, num7);
        point3dArray2 = [point3d0, point3d8, point3d10, point3d30, point3d31, point3d20 ];
        AcadHelper.smethod_121(polyline_0, point3dArray2);
        polyline_0.SetBulgeAt(0, MathHelper.smethod_60(point3d0, point3d7, point3d8));
        polyline_0.SetBulgeAt(1, MathHelper.smethod_60(point3d8, point3d9, point3d10));
        polyline_0.SetBulgeAt(2, MathHelper.smethod_60(point3d10, point3d29, point3d30));
        polyline_0.SetBulgeAt(4, MathHelper.smethod_60(point3d31, point3d32, point3d20));
        return point3d_2
