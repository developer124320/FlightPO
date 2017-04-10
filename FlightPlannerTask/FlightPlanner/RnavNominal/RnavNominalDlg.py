# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QSize, Qt, QVariant
from PyQt4.QtGui import QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsPalLayerSettings,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType, SurfaceTypes, DistanceUnits, SpeedUnits,AircraftSpeedCategory, OrientationType, AltitudeUnits, ObstacleAreaResult
from FlightPlanner.types import RnavFlightPhase, RnavWaypointType, AngleUnits, TurnDirection
from FlightPlanner.RnavNominal.ui_RnavNominal import Ui_RnavNominal
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.messages import Messages

from FlightPlanner.Confirmations import Confirmations
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.Panels.WindPanel import WindPanel
from FlightPlanner.Captions import Captions
from FlightPlanner.types import Point3D
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.captureCoordinateTool import CaptureCoordinateToolUpdate
from FlightPlanner.QtObjectMethods import ComboBox, LineEdit,AltitudeObject
from FlightPlanner.BasicGNSS.rnavWaypoints import RnavWaypoints
from FlightPlanner.expressions import Expressions


import define, math

class RnavNominalDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("RnavNominalDlg")
        self.surfaceType = SurfaceTypes.RnavNominal
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.RnavNominal)
        self.resize(550, 700)
        QgisHelper.matchingDialogSize(self, 720, 700)
        self.surfaceList = None
        
    
    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(1)
        self.ui.btnEvaluate.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(1)

        return FlightPlanBaseDlg.uiStateInit(self)


    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        self.method_34(True)
        pass


    def initParametersPan(self):
        ui = Ui_RnavNominal()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.frame_Tas.setVisible(False)
        self.parametersPanel.frame_Tas1.setVisible(False)
        self.parametersPanel.frame_Tas2.setVisible(False)

        self.parametersPanel.chbFirstWaypoint2.setVisible(False)

        self.parametersPanel.pnlPosWpt1 = PositionPanel(ui.gbWaypoint1)
        self.parametersPanel.pnlPosWpt1.groupBox.setTitle("Position")
        self.parametersPanel.pnlPosWpt1.btnCalculater.hide()
        self.parametersPanel.pnlPosWpt1.hideframe_Altitude()
        self.parametersPanel.pnlPosWpt1.setObjectName("pnlPosWpt1")
        ui.vl_gbWaypoint1.insertWidget(1, self.parametersPanel.pnlPosWpt1)

        self.parametersPanel.pnlPosWpt2 = PositionPanel(ui.gbWaypoint2)
        self.parametersPanel.pnlPosWpt2.groupBox.setTitle("Position")
        self.parametersPanel.pnlPosWpt2.btnCalculater.hide()
        self.parametersPanel.pnlPosWpt2.hideframe_Altitude()
        self.parametersPanel.pnlPosWpt2.setObjectName("pnlPosWpt2")
        ui.vl_gbWaypoint2.insertWidget(1, self.parametersPanel.pnlPosWpt2)

        self.parametersPanel.pnlWind1 = WindPanel(self.parametersPanel.pnlAttR1)
        self.parametersPanel.pnlWind1.lblIA.setMinimumSize(100, 0)
        self.parametersPanel.pnlWind1.lblIA.setMaximumSize(100, 10000)
        self.parametersPanel.vl_pnlAttR1.addWidget(self.parametersPanel.pnlWind1)
        self.parametersPanel.pnlWind1.setAltitude(Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT))

        self.parametersPanel.pnlWind2 = WindPanel(self.parametersPanel.pnlAttR2)
        self.parametersPanel.pnlWind2.lblIA.setMinimumSize(100, 0)
        self.parametersPanel.pnlWind2.lblIA.setMaximumSize(100, 10000)
        self.parametersPanel.vl_pnlAttR2.addWidget(self.parametersPanel.pnlWind2)
        self.parametersPanel.pnlWind2.setAltitude(Altitude(float(self.parametersPanel.txtAltitude2.text()), AltitudeUnits.FT))

        self.parametersPanel.pnlAtt1 = RnavTolerancesPanel(self)
        self.parametersPanel.pnlAtt1.set_Att(Distance(0.8, DistanceUnits.NM))
        self.parametersPanel.pnlAtt1.HasASW = False
        self.parametersPanel.pnlAtt1.HasXTT = False
        self.parametersPanel.pnlAtt1.btnDropDown.setMaximumHeight(23)
        self.parametersPanel.pnlAtt1.LabelWidth = 100
        ui.vl_pnlAttR1.addWidget(self.parametersPanel.pnlAtt1)
        self.connect(self.parametersPanel.pnlAtt1, SIGNAL("valueChanged()"), self.method_28)

        self.parametersPanel.pnlAtt2 = RnavTolerancesPanel(self)
        self.parametersPanel.pnlAtt2.set_Att(Distance(0.8, DistanceUnits.NM))
        self.parametersPanel.pnlAtt2.HasASW = False
        self.parametersPanel.pnlAtt2.HasXTT = False
        self.parametersPanel.pnlAtt2.btnDropDown.setMaximumHeight(23)
        self.parametersPanel.pnlAtt2.LabelWidth = 100
        ui.vl_pnlAttR2.addWidget(self.parametersPanel.pnlAtt2)
        self.connect(self.parametersPanel.pnlAtt2, SIGNAL("valueChanged()"), self.method_28)


        self.parametersPanel.cmbPhaseOfFlight.addItems(["Enroute", "SID", "IafIf", "Faf", "MissedApproach"])
        self.parametersPanel.cmbType1.addItems(["FlyBy", "FlyOver"])
        self.parametersPanel.cmbType2.addItems(["FlyBy", "FlyOver"])

#
        self.parametersPanel.cmbType2.currentIndexChanged.connect(self.method_28)
        self.parametersPanel.chbFirstWaypoint.clicked.connect(self.chbFirstWaypointClicked)
        self.parametersPanel.chbUse2Waypoints.clicked.connect(self.method_28)
        self.parametersPanel.txtAltitude1.textChanged.connect(self.altitude1Changed)
        self.parametersPanel.txtAltitudeM1.textChanged.connect(self.altitudeM1Changed)

        self.parametersPanel.txtAltitude2.textChanged.connect(self.altitude2Changed)
        self.parametersPanel.txtAltitudeM2.textChanged.connect(self.altitudeM2Changed)

        self.parametersPanel.txtDerAltitude.textChanged.connect(self.altitudeMChanged)
        self.parametersPanel.txtDerAltitudeFt.textChanged.connect(self.altitudeChanged)
        self.parametersPanel.cmbPhaseOfFlight.currentIndexChanged.connect(self.cmbPhaseOfFlightChanged)

        self.flag = 0
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtDerAltitude.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtDerAltitudeFt.text())), 4)))
            except:
                self.parametersPanel.txtDerAltitude.setText("0.0")

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

        self.parametersPanel.pnlWind1.setAltitude(Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT))
        self.parametersPanel.pnlWind2.setAltitude(Altitude(float(self.parametersPanel.txtAltitude2.text()), AltitudeUnits.FT))
        self.method_28()
    def cmbPhaseOfFlightChanged(self):
        self.method_28()
        self.chbFirstWaypointClicked()
    def chbFirstWaypointClicked(self):
        self.parametersPanel.txtBank1.setText(str(self.method_29(Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT), self.isDepartureSelected, self.isMissedApproachSelected, self.isEnrouteSelected, self.parametersPanel.chbFirstWaypoint.isChecked())));
        self.parametersPanel.txtBank2.setText(str(self.method_29(Altitude(float(self.parametersPanel.txtAltitude2.text()), AltitudeUnits.FT), self.isDepartureSelected, self.isMissedApproachSelected, self.isEnrouteSelected, False)));

    def iasChanged(self):
        try:
            self.parametersPanel.txtTas.setText(str(round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT)).Knots, 4)))
        except:
            raise ValueError("Value Invalid")
    def isaChanged(self):
        try:
            self.parametersPanel.txtTas.setText(str(round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT)).Knots, 4)))
        except:
            raise ValueError("Value Invalid")    
    # def iasHelpShow(self):
    #     dlg = IasHelpDlg()
    #     dlg.exec_()
    def altitudeChanged(self):
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtDerAltitude.setText(str(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtDerAltitudeFt.text()))))
            except:
                self.parametersPanel.txtDerAltitude.setText("0.0")

        self.parametersPanel.txtBank1.setText(str(self.method_29(Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT), self.isDepartureSelected, self.isMissedApproachSelected, self.isEnrouteSelected, self.parametersPanel.chbFirstWaypoint.isChecked())));
        self.parametersPanel.txtBank2.setText(str(self.method_29(Altitude(float(self.parametersPanel.txtAltitude2.text()), AltitudeUnits.FT), self.isDepartureSelected, self.isMissedApproachSelected, self.isEnrouteSelected, False)));

        # self.parametersPanel.pnlWind1.setAltitude(Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT))
        # try:
        #     self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT)).Knots))
        # except:
        #     raise ValueError("Value Invalid")
    def altitudeMChanged(self):
        if self.flag==0:
            self.flag=1;
        if self.flag==2:
            self.flag=0;
        if self.flag==1:
            try:
                self.parametersPanel.txtDerAltitudeFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtDerAltitude.text())), 4)))
            except:
                self.parametersPanel.txtDerAltitudeFt.setText("0.0")
        self.parametersPanel.txtBank1.setText(str(self.method_29(Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT), self.isDepartureSelected, self.isMissedApproachSelected, self.isEnrouteSelected, self.parametersPanel.chbFirstWaypoint.isChecked())));
        self.parametersPanel.txtBank2.setText(str(self.method_29(Altitude(float(self.parametersPanel.txtAltitude2.text()), AltitudeUnits.FT), self.isDepartureSelected, self.isMissedApproachSelected, self.isEnrouteSelected, False)));

        # self.parametersPanel.pnlWind1.setAltitude(Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT))
        # try:
        #     self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT)).Knots))
        # except:
        #     raise ValueError("Value Invalid")


    def altitude1Changed(self):
        if self.flag1==0:
            self.flag1=2;
        if self.flag1==1:
            self.flag1=0;
        if self.flag1==2:
            try:
                self.parametersPanel.txtAltitudeM1.setText(str(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude1.text()))))
            except:
                self.parametersPanel.txtAltitudeM1.setText("0.0")
        self.parametersPanel.txtBank1.setText(str(self.method_29(Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT), self.isDepartureSelected, self.isMissedApproachSelected, self.isEnrouteSelected, self.parametersPanel.chbFirstWaypoint.isChecked())));
        self.parametersPanel.pnlWind1.setAltitude(Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT));

        # self.pnlBank1.Value = self.method_29(self.pnlAltitude1.Value, self.isDepartureSelected, self.isMissedApproachSelected, self.isEnrouteSelected, self.chbFirstWaypoint.Checked);
		# self.pnlWind1.Altitude = self.pnlAltitude1.Value;
        self.parametersPanel.pnlWind1.setAltitude(Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT))
        # try:
        #     self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT)).Knots))
        # except:
        #     raise ValueError("Value Invalid")
    def altitudeM1Changed(self):
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtAltitude1.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAltitudeM1.text())), 4)))
            except:
                self.parametersPanel.txtAltitude1.setText("0.0")
        self.parametersPanel.txtBank1.setText(str(self.method_29(Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT), self.isDepartureSelected, self.isMissedApproachSelected, self.isEnrouteSelected, self.parametersPanel.chbFirstWaypoint.isChecked())));
        self.parametersPanel.pnlWind1.setAltitude(Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT));

        self.parametersPanel.pnlWind1.setAltitude(Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT))
        # try:
        #     self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT)).Knots))
        # except:
        #     raise ValueError("Value Invalid")

    def altitude2Changed(self):
        if self.flag2==0:
            self.flag2=2;
        if self.flag2==1:
            self.flag2=0;
        if self.flag2==2:
            try:
                self.parametersPanel.txtAltitudeM2.setText(str(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude2.text()))))
            except:
                self.parametersPanel.txtAltitudeM2.setText("0.0")

        self.parametersPanel.txtBank2.setText(str(self.method_29(Altitude(float(self.parametersPanel.txtAltitude2.text()), AltitudeUnits.FT), self.isDepartureSelected, self.isMissedApproachSelected, self.isEnrouteSelected, False)));
        self.parametersPanel.pnlWind2.setAltitude(Altitude(float(self.parametersPanel.txtAltitude2.text()), AltitudeUnits.FT));

        self.parametersPanel.pnlWind2.setAltitude(Altitude(float(self.parametersPanel.txtAltitude2.text()), AltitudeUnits.FT))
        # try:
        #     self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT)).Knots))
        # except:
        #     raise ValueError("Value Invalid")
    def altitudeM2Changed(self):
        if self.flag2==0:
            self.flag2=1;
        if self.flag2==2:
            self.flag2=0;
        if self.flag2==1:
            try:
                self.parametersPanel.txtAltitude2.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAltitudeM2.text())), 4)))
            except:
                self.parametersPanel.txtAltitude2.setText("0.0")

        self.parametersPanel.txtBank2.setText(str(self.method_29(Altitude(float(self.parametersPanel.txtAltitude2.text()), AltitudeUnits.FT), self.isDepartureSelected, self.isMissedApproachSelected, self.isEnrouteSelected, False)));
        self.parametersPanel.pnlWind2.setAltitude(Altitude(float(self.parametersPanel.txtAltitude2.text()), AltitudeUnits.FT));
        

        self.parametersPanel.pnlWind2.setAltitude(Altitude(float(self.parametersPanel.txtAltitude2.text()), AltitudeUnits.FT))
        # try:
        #     self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitudeFt.text()), AltitudeUnits.FT)).Knots))
        # except:
        #     raise ValueError("Value Invalid")

    def captureTrackFrom(self):
        captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrackFrom)
        define._canvas.setMapTool(captureTrackTool)
    def captureTrackTo(self):
        captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrackTo)
        define._canvas.setMapTool(captureTrackTool)
    def chbUse2Waypoints_Click(self):
        pass

    def method_28(self):
        flag = self.isDepartureSelected;
        self.parametersPanel.frame_DerAltitude.setVisible(flag);
        self.parametersPanel.frame_DerAltitude.setEnabled(flag);
        self.parametersPanel.chbFirstWaypoint.setVisible(flag);
        self.parametersPanel.chbIAS.setVisible(flag);
        # if (not flag):
        #     self.pnlOptions.ColumnStyles[0].Width = 50f;
        #     self.pnlOptions.ColumnStyles[1].Width = 50f;
        #     self.pnlOptions.ColumnStyles[2].Width = 0f;
        # }
        # else
        # {
        #     self.pnlOptions.ColumnStyles[0].Width = 35f;
        #     self.pnlOptions.ColumnStyles[1].Width = 35f;
        #     self.pnlOptions.ColumnStyles[2].Width = 30f;
        # }
        self.parametersPanel.gbWaypoint2.setVisible(self.parametersPanel.chbUse2Waypoints.isChecked());
        if (not self.parametersPanel.chbUse2Waypoints.isChecked()):
            if (self.parametersPanel.cmbType1.count() == 3):
                if (self.parametersPanel.cmbType1.currentIndex() == 2):
                    self.parametersPanel.cmbType1.setCurrentIndex(0);
                self.parametersPanel.cmbType1.removeItem(2);
            self.parametersPanel.gbWaypoint1.setTitle(Captions.WAYPOINT);
            self.parametersPanel.txtTrackTo.Caption = Captions.TRACK_TO_WAYPOINT
            self.parametersPanel.txtTrackFrom.Value = Captions.TRACK_FROM_WAYPOINT
        else:
            if (self.parametersPanel.cmbType1.count() == 2):
                self.parametersPanel.cmbType1.addItem(Captions.FIXED_RADIUS);
            self.parametersPanel.gbWaypoint1.setTitle(Captions.WAYPOINT_1);
            self.parametersPanel.txtTrackTo.Caption = Captions.TRACK_TO_WAYPOINT_1
            self.parametersPanel.txtTrackFrom.Caption = Captions.TRACK_FROM_WAYPOINT_2
        # self.parametersPanel.pnlWind1.setEnabled(self.parametersPanel.pnlAtt1.ATT.IsValid;
        # self.pnlWind2.Enabled = self.pnlAtt2.ATT.IsValid;
    def method_29(self, altitude_0, bool_0, bool_1, bool_2, bool_3):
        if (bool_0 and bool_3):
            return 15;
        if (not bool_0):
            if (not bool_1 and not bool_2):
                return 25;
            return 15;
        num = altitude_0.Feet;
        num1 = Altitude(float(self.parametersPanel.txtDerAltitude.text())).Feet;
        if (num - num1 > 3000):
            return 25;
        if (num - num1 > 1000):
            return 20;
        return 15;
    def method_34(self, bool_0):
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        point3d3 = None;
        point3d4 = None;
        point3d5 = None;
        value = None;
        num = None;
        num1 = None;
        num2 = None;
        num3 = None;
        value1 = None;
        num4 = None;
        num5 = None;
        num6 = None;
        metres = None;
        metres1 = None;
        num7 = None;
        num8 = None;
        num9 = None;
        num10 = None;
        num11 = None;
        metres2 = None;
        metres3 = None;
        turnDirection = None;
        speed = None;
        speed1 = None;
        degree = None;
        degree1 = None;
        degree2 = None;
        degree3 = None;
        distance = None;
        num12 = None;
        num13 = None;
        metres4 = None;
        symbol = None;
        symbol1 = None;
        distance1 = None;
        value2 = None;
        point3dArray = [];
        num14 = 0;
        point3d6 = self.parametersPanel.pnlPosWpt1.Point3d;
        point3d7 = point3d6;
        if (self.parametersPanel.chbUse2Waypoints.isChecked()):
            point3d7 = self.parametersPanel.pnlPosWpt2.Point3d;
            if (MathHelper.calcDistance(point3d6, point3d7) < 1):
                QMessageBox.warning(self,"Error", Messages.ERR_POSITIONS_CANNOT_BE_EQUAL)
                # ErrorMessageBox.smethod_0(self, Messages.ERR_POSITIONS_CANNOT_BE_EQUAL);
                return None;
        polylineArea = PolylineArea();
        polylineArea1 = PolylineArea();
        polylineArea2 = PolylineArea();
        polylineArea3 = PolylineArea();
        polylineArea4 = PolylineArea();
        polylineArea5 = PolylineArea();
        stringBuilder = "";
        stringBuilder += self.parametersPanel.gbGeneral.title() + "\n";
        stringBuilder += ComboBox.method_11(self.parametersPanel.cmbPhaseOfFlight, self.parametersPanel.label_13, "    ") + "\n";
        stringBuilder += LineEdit.method_7(self.parametersPanel.txtIsa, self.parametersPanel.label_21, "    ") + "\n";
        stringBuilder += "%s%s\t%s"%("    ", self.parametersPanel.chbCatH.text(), self.parametersPanel.chbCatH.isChecked()) + "\n";
        stringBuilder += self.parametersPanel.gbWaypoint1.title() + "\n";
        stringBuilder += ComboBox.method_11(self.parametersPanel.cmbType1, self.parametersPanel.label_11, "    ") + "\n";
        stringBuilder += "    " + self.parametersPanel.pnlPosWpt1.groupBox.title() + "\n";
        stringBuilder += self.parametersPanel.pnlPosWpt1.method_8("        ") + "\n";
        num15 = 0;
        num16 = 0;
        num17 = 0;
        num18 = 0;
        num19 = 0;
        num20 = 0;
        flag = self.isDepartureSelected;
        rnavFlightPhase = self.get_FlightPhase()#(RnavFlightPhase)EnumHelper.smethod_1((string)self.pnlPhaseOfFlight.SelectedItem, typeof(RnavFlightPhase));
        if (self.parametersPanel.cmbType1.currentIndex() < 2):
            rnavWaypointType = self.parametersPanel.cmbType1.currentIndex()#(RnavWaypointType)EnumHelper.smethod_1((string)self.pnlType1.SelectedItem, typeof(RnavWaypointType));
            value = MathHelper.smethod_3(float(self.parametersPanel.txtTrackTo.Value));
            num = MathHelper.smethod_3(float(self.parametersPanel.txtTrackFrom.Value)) if(not self.parametersPanel.chbUse2Waypoints.isChecked()) else MathHelper.smethod_3(Unit.smethod_1(MathHelper.getBearing(point3d6, point3d7)));
            turnDirectionList = []
            num1 = MathHelper.smethod_77(value, num, AngleUnits.Degrees, turnDirectionList)
            turnDirection = turnDirectionList[0];
            num19 = Unit.ConvertDegToRad(num1);
            if (turnDirection == TurnDirection.Nothing):
                QMessageBox.warning(self, "Error", Messages.ERR_COURSE_CHANGE_OF_0_NOT_ALLOWED)
                # ErrorMessageBox.smethod_0(self, Messages.ERR_COURSE_CHANGE_OF_0_NOT_ALLOWED);
                return None;
            if (num1 > 120 and self.parametersPanel.cmbType1.currentIndex() == 0 and QMessageBox.warning(self, "Warning", Confirmations.CONTINUE_CONSTRUCTING_FMS_120, QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
                return None;
            value1 = float(self.parametersPanel.txtBank1.text());
            num4 = 15;
            speed = Speed(float(self.parametersPanel.txtIas1.text()));
            if (flag and self.parametersPanel.chbIAS.isChecked()):
                speed = speed + (speed / 10);
            speed1 = Speed.smethod_0(speed, float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT));
            num5_0 = []
            distance1 = Distance.smethod_1(speed1, value1, num5_0)
            num5 = num5_0[0];
            metres = distance1.Metres;
            num6_0 = []
            distance1 = Distance.smethod_1(speed1, num4, num6_0)
            num6 = num6_0[0];
            metres1 = distance1.Metres;
            num17 = metres;
            caption = "IAS:"#self.pnlIas1.Caption;
            value2 = self.parametersPanel.txtIas1.text();
            stringBuilder += "%s%s\t%s"%("    ", caption, value2) + "kts\n";
            if (flag and self.parametersPanel.chbIAS.isChecked()):
                stringBuilder += "%s%s\t%f"%("    ", Captions.DEPARTURE_IAS, round(speed.Knots, 4)) + "kts\n";
            stringBuilder += "%s%s\t%f"%("    ", Captions.TAS, round(speed1.Knots,4)) + "kts\n";
            stringBuilder += AltitudeObject.method_8(self.parametersPanel.txtAltitude1, self.parametersPanel.label_4, "    ", "ft") + "\n";
            if (self.parametersPanel.cmbType1.currentIndex() == 0):
                num7 = metres * math.tan(Unit.ConvertDegToRad(0.5 * num1));
                num8 = 5 * speed1.MetresPerSecond if(not self.parametersPanel.chbCatH.isChecked()) else 3 * speed1.MetresPerSecond;
                point3d = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(value + 180), num7);
                point3d1 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(value + 90), 100);
                point3d2 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(num), num7);
                point3d3 = MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(num + 90), 100);
                point3d4 = MathHelper.getIntersectionPoint(point3d, point3d1, point3d2, point3d3);
                point3d = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(value + 180), num7 + num8);
                point3d1 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(value + 180), num7);
                point3d2 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(num), num7);
                point3d3 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(num), num7 + num8);
                polylineArea.method_1(point3d);
                polylineArea.Add(PolylineAreaPoint(point3d1, MathHelper.smethod_57(turnDirection, point3d1, point3d2, point3d4)));
                polylineArea.method_1(point3d2);
                polylineArea.method_1(point3d3);
                num14 = num7 + num8;
                stringBuilder += "%s%s\t%f °"%("    ", Captions.TRACK_TO, round(value, 4)) + "\n";
                stringBuilder += "%s%s\t%f °"%("    ", Captions.TRACK_FROM, round(num, 4)) + "\n";
                stringBuilder += "%s%s\t%f °"%("    ", Captions.COURSE_CHANGE, round(num1, 4)) + "\n";
                stringBuilder += "%s%s\t%f °"%("    ", Captions.BANK_ANGLE, round(value1, 4)) + "\n";
                tURNRADIUS = Captions.TURN_RADIUS;
                stringBuilder += "%s%s\t%f"%("    ", tURNRADIUS, round(distance1.Metres, 4))+ "m\n";
                distance1 = Distance(metres);
                rOLLINDISTANCE = Captions.ROLL_IN_DISTANCE;
                distance1 = Distance(num8);
                stringBuilder += "%s%s\t%f"%("    ", rOLLINDISTANCE, round(distance1.Metres, 4)) + "\n";
                tURNINITIATIONDISTANCE = Captions.TURN_INITIATION_DISTANCE;
                distance1 = Distance(num7);
                stringBuilder += "%s%s\t%f"%("    ", tURNINITIATIONDISTANCE, round(distance1.Metres, 4)) + "\n";
                rOLLOUTDISTANCE = Captions.ROLL_OUT_DISTANCE;
                distance1 = Distance(num8);
                stringBuilder += "%s%s\t%f"%("    ", rOLLOUTDISTANCE, round(distance1.Metres, 4)) + "\n";
                num15 = num7;
            elif (self.parametersPanel.cmbType1.currentIndex() == 1):
                num2 = 30;
                num3 = 60;
                if (num1 < 50):
                    num2 = 0.6 * num1;
                    num3 = 90 - num2;
                num7 = metres * math.sin(Unit.ConvertDegToRad(num1));
                num8 = metres * math.cos(Unit.ConvertDegToRad(num1)) * math.tan(Unit.ConvertDegToRad(num2));
                num9 = metres * ((1 - math.cos(Unit.ConvertDegToRad(num1)) / math.cos(Unit.ConvertDegToRad(num2))) / math.sin(Unit.ConvertDegToRad(num2)));
                num10 = metres1 * math.tan(Unit.ConvertDegToRad(num2 / 2));
                num11 = 10 * speed1.MetresPerSecond if(not self.parametersPanel.chbCatH.isChecked) else 5 * speed1.MetresPerSecond;
                point3d2 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(num), num7 + num8 + num9 + num10);
                if (turnDirection != TurnDirection.Left):
                    point3d4 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(value + 90), metres);
                    point3d = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(num - num3), metres);
                    point3d5 = MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(num - 90), metres1);
                    point3d1 = MathHelper.distanceBearingPoint(point3d5, MathHelper.getBearing(point3d5, point3d2) + Unit.ConvertDegToRad(num2), metres1);
                else:
                    point3d4 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(value - 90), metres);
                    point3d = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(num + num3), metres);
                    point3d5 = MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(num + 90), metres1);
                    point3d1 = MathHelper.distanceBearingPoint(point3d5, MathHelper.getBearing(point3d5, point3d2) - Unit.ConvertDegToRad(num2), metres1);
                point3d3 = MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(num), num11);
                polylineArea.Add(PolylineAreaPoint(point3d6, MathHelper.smethod_57(turnDirection, point3d6, point3d, point3d4)));
                polylineArea.method_1(point3d);
                if (turnDirection == TurnDirection.Left):
                    polylineArea.Add(PolylineAreaPoint(point3d1, MathHelper.smethod_57(TurnDirection.Right, point3d1, point3d2, point3d5)));
                elif (turnDirection != TurnDirection.Right):
                    polylineArea.method_1(point3d1);
                else:
                    polylineArea.Add(PolylineAreaPoint(point3d1, MathHelper.smethod_57(TurnDirection.Left, point3d1, point3d2, point3d5)));
                polylineArea.method_1(point3d2);
                polylineArea.method_1(point3d3);
                num14 = num7 + num8 + num9 + num10 + num11;
                stringBuilder += "%s%s\t%f °"%("    ", Captions.TRACK_TO, round(value, 4)) + "\n";
                stringBuilder += "%s%s\{%f °"%("    ", Captions.TRACK_FROM, round(num, 4)) + "\n";
                stringBuilder += "%s%s\t%f °"%("    ", Captions.COURSE_CHANGE, round(num1, 4)) + "\n";
                stringBuilder += "%s%s\t%f °"%("    ", Captions.BANK_ANGLE_1, round(value1, 4)) + "\n";
                tURNRADIUS1 = Captions.TURN_RADIUS_1;
                distance1 = Distance(metres);
                stringBuilder += "%s%s\t%f"%("    ", tURNRADIUS1, round(distance1.Metres, 4)) + "m\n";
                stringBuilder += "%s%s\t%f °"%("    ", Captions.BANK_ANGLE_2, round(num4, 4)) + "\n";
                tURNRADIUS2 = Captions.TURN_RADIUS_2;
                distance1 = Distance(metres1);
                stringBuilder += "%s%s\t%f"%("    ", tURNRADIUS2, round(distance1.Metres, 4)) + "m\n";
                stringBuilder += "%s%s\t%f °"%("    ", Captions.INTERCEPT_ANGLE, round(num2, 4)) + "\n";
                l1 = Captions.L1;
                distance1 = Distance(num7);
                stringBuilder += "%s%s\t%f"%("    ", l1, round(distance1.Metres, 4)) + "m\n";
                l2 = Captions.L2;
                distance1 = Distance(num8);
                stringBuilder += "%s%s\t%f"%("    ", l2, round(distance1.Metres,4)) + "m\n";
                l3 = Captions.L3;
                distance1 = Distance(num9);
                stringBuilder += "%s%s\t%f"%("    ", l3, round(distance1.Metres, 4)) + "m\n";
                l4 = Captions.L4;
                distance1 = Distance(num10);
                stringBuilder += "%s%s\t%s"%("    ", l4, round(distance1.Metres, 4)) + "m\n";
                l5 = Captions.L5;
                distance1 = Distance(num11);
                stringBuilder += "%s%s\t%f"%("    ", l5, round(distance1.Metres, 4)) + "m\n";
                mINIMUMTURNDISTANCE = Captions.MINIMUM_TURN_DISTANCE;
                distance1 = Distance(num7 + num8 + num9 + num10 + num11);
                stringBuilder += "%s%s\t%f"%("    ", mINIMUMTURNDISTANCE, round(distance1.Metres, 4)) +"m\n";
            if (self.parametersPanel.pnlAtt1.ATT.IsValid()):
                distance1 = RnavWaypoints.getDistanceFromWaypointToEarliestTurningPoint(rnavWaypointType, self.parametersPanel.pnlAtt1.ATT, Distance(metres), num1, AngleUnits.Degrees);
                metres2 = distance1.Metres;
                distance1 = RnavWaypoints.smethod_13(rnavFlightPhase, rnavWaypointType, speed1, self.parametersPanel.pnlWind1.Value, self.parametersPanel.pnlAtt1.ATT, Distance(metres), num1, AngleUnits.Degrees);
                metres3 = distance1.Metres;
                point3d = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(value + 180), math.fabs(metres2)) if(metres2 >= 0) else MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(value), math.fabs(metres2));
                point3d1 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(value + 90), 400);
                point3d2 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(value - 90), 400);
                point3dArray = [point3d1, point3d2 ];
                polylineArea2.method_7(point3dArray);
                point3d = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(value + 180), math.fabs(metres3)) if(metres3 >= 0) else MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(value), math.fabs(metres3));
                point3d1 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(value + 90), 400);
                point3d2 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(value - 90), 400);
                point3dArray = [point3d1, point3d2 ];
                polylineArea3.method_7(point3dArray);
                stringBuilder += self.parametersPanel.pnlAtt1.method_3("    ") + "\n";
                if (self.parametersPanel.pnlWind1.Value.IsValid()):
                    stringBuilder += self.parametersPanel.pnlWind1.method_7("    ") +"\n";
                kKLINE = Captions.K_K_LINE;
                distance1 = Distance(metres2);
                stringBuilder += "%s%s\t%f"%("    ", kKLINE, round(distance1.Metres, 4)) + "m\n";
                wINDSPIRALLINE = Captions.WIND_SPIRAL_LINE;
                distance1 = Distance(metres3);
                stringBuilder += "%s%s\t%f"%("    ", wINDSPIRALLINE, round(distance1.Metres, 4)) + "m\n";
        elif (self.parametersPanel.chbUse2Waypoints.isChecked()):
            value = float(self.parametersPanel.txtTrackTo.Value);
            num = float(self.parametersPanel.txtTrackFrom.Value);
            turnDirection_000 = []
            num1 = MathHelper.smethod_77(value, num, AngleUnits.Degrees, turnDirection_000)
            turnDirection = turnDirection_000[0];
            if (turnDirection == TurnDirection.Nothing):
                QMessageBox.warning(self, "Error", Messages.ERR_COURSE_CHANGE_OF_0_NOT_ALLOWED)
                # ErrorMessageBox.smethod_0(self, Messages.ERR_COURSE_CHANGE_OF_0_NOT_ALLOWED);
                return None;
            if (num1 > 120 and self.parametersPanel.cmbType1.currentIndex() == 0 and QMessageBox.warning(self, "Warning" , Confirmations.CONTINUE_CONSTRUCTING_FMS_120, QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
                return None;
            value1 = float(self.parametersPanel.txtBank1.text());
            speed = Speed(float(self.parametersPanel.txtIas1.text()));
            if (flag and self.parametersPanel.chbIAS.isChecked()):
                speed = speed + (speed / 10);
            speed1 = Speed.smethod_0(speed, float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude1.text()), AltitudeUnits.FT));
            num5_0 = []
            distance1 = Distance.smethod_1(speed1, value1, num5_0)
            num5 = num5_0[0];
            metres = distance1.Metres;
            if (turnDirection != TurnDirection.Left):
                point3d4 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(value + 90), metres);
                point3d = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(num - 90), metres);
            else:
                point3d4 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(value - 90), metres);
                point3d = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(num + 90), metres);
            polylineArea.method_1(point3d6);
            num14 = 0;
            stringBuilder += "%s%s\t%f °"%("    ", Captions.TRACK_TO, round(value, 4)) + "\n";
            stringBuilder += "%s%s\t%f °"%("    ", Captions.TRACK_FROM, round(num, 4)) + "\n";
            stringBuilder += "%s%s\t%f °"%("    ", Captions.COURSE_CHANGE, round(num1, 4)) + "\n";
            stringBuilder += "%s%s\t%f °"%("    ", Captions.BANK_ANGLE, round(value1, 4)) + "\n";
            str0 = Captions.TURN_RADIUS;
            distance1 = Distance(metres);
            stringBuilder += "%s%s\t%f"%("    ", str0, round(distance1.Metres, 4)) + "m\n";
            aLONGTRACKDISTANCE = Captions.ALONG_TRACK_DISTANCE;
            distance1 = Distance(Unit.ConvertDegToRad(num1) * num5);
            stringBuilder += "%s%s\t%f"%("    ", aLONGTRACKDISTANCE, round(distance1.Metres, 4)) + "m\n";
        if (not self.parametersPanel.chbUse2Waypoints.isChecked()):
            if (bool_0):
                self.constructionLineLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)
                resultPolylineArea = PolylineArea.smethod_131(polylineArea)
                AcadHelper.setGeometryAndAttributesInLayer(self.constructionLineLayer, resultPolylineArea)
                self.constructionTextLayer = None
                mapUnits = define._canvas.mapUnits()
                if define._mapCrs == None:
                    if mapUnits == QGis.Meters:
                        self.constructionTextLayer = QgsVectorLayer("Point?crs=EPSG:32633", "Text", "memory")
                    else:
                        self.constructionTextLayer = QgsVectorLayer("Point?crs=EPSG:4326", "Text", "memory")
                else:
                    self.constructionTextLayer = QgsVectorLayer("Point?crs=%s"%define._mapCrs.authid (), "Text", "memory")

                if polylineArea2.Count == 2:
                    self.method_35(polylineArea2, Captions.K_K_LINE_WPT1, self.constructionLineLayer);
                if polylineArea3.Count == 2:
                    self.method_35(polylineArea3, Captions.WIND_SPIRAL_LINE_WPT1, self.constructionLineLayer);


                if (self.parametersPanel.chbInsertSymbols.isChecked()):
                    symbol = self.parametersPanel.cmbType1.currentText() 

                    QgisHelper.appendToCanvas(define._canvas, [self.constructionLineLayer, self.WPT2Layer(symbol, point3d6)], self.surfaceType, True)
                    self.resultLayerList = [self.constructionLineLayer, self.WPT2Layer(symbol, point3d6)]

                else:
                    QgisHelper.appendToCanvas(define._canvas, [self.constructionLineLayer], self.surfaceType, True)
                    self.resultLayerList = [self.constructionLineLayer]
            return stringBuilder
        stringBuilder += self.parametersPanel.gbWaypoint2.title();
        stringBuilder += ComboBox.method_11(self.parametersPanel.cmbType1, self.parametersPanel.label_11, "    ") + "\n";
        stringBuilder += "    " + self.parametersPanel.pnlPosWpt2.groupBox.title() + "\n";
        stringBuilder += self.parametersPanel.pnlPosWpt2.method_8("        ") + "\n";
        rnavWaypointType1 = self.parametersPanel.cmbType2.currentIndex()#(RnavWaypointType)EnumHelper.smethod_1((string)self.pnlType2.SelectedItem, typeof(RnavWaypointType));
        value = Unit.smethod_1(MathHelper.getBearing(point3d6, point3d7));
        num = float(self.parametersPanel.txtTrackFrom.Value);
        turnDirectionList = []
        num1 = MathHelper.smethod_77(value, num, AngleUnits.Degrees, turnDirectionList )
        turnDirection = turnDirectionList[0];
        num20 = Unit.ConvertDegToRad(num1);
        if (turnDirection == TurnDirection.Nothing):
            QMessageBox.warning(self, "Error", Messages.ERR_COURSE_CHANGE_OF_0_NOT_ALLOWED)
            # ErrorMessageBox.smethod_0(self, Messages.ERR_COURSE_CHANGE_OF_0_NOT_ALLOWED);
            return None;
        if (num1 > 120 and self.parametersPanel.cmbType2.currentIndex() == 0 and QMessageBox.warning(self, "Warning", Confirmations.CONTINUE_CONSTRUCTING_FMS_120, QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
            return None;
        value1 = float(self.parametersPanel.txtBank2.text());
        num4 = 15;
        speed = Speed(float(self.parametersPanel.txtIas2.text()));
        if (flag and self.parametersPanel.chbIAS.isChecked()):
            speed = speed + (speed / 10);
        speed1 = Speed.smethod_0(speed, float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitudeM2.text())));
        num5_0 = []
        distance1 = Distance.smethod_1(speed1, value1, num5_0)
        num5 = num5_0[0];
        metres = distance1.Metres;
        num6_0 = []
        distance1 = Distance.smethod_1(speed1, num4, num6_0)
        num6 = num6_0[0];
        metres1 = distance1.Metres;
        num18 = metres;
        caption1 = "IAS:"#self.pnlIas2.Caption;
        value2 = Speed(float(self.parametersPanel.txtIas2.text()));
        stringBuilder += "%s%s\t%f"%("    ", caption1, round(value2.Knots, 4)) + "kts\n";
        if (flag and self.parametersPanel.chbIAS.isChecked()):
            stringBuilder += "%s%s\t%f"%("    ", Captions.DEPARTURE_IAS, round(speed.Knots, 4)) + "kts\n";
        stringBuilder += "%s%s\t%f"%("    ", Captions.TAS, round(speed1.Knots, 4)) + "kts\n";
        stringBuilder += AltitudeObject.method_8(self.parametersPanel.txtAltitude2, self.parametersPanel.label_17, "    ", "ft") + "\n";
        if (self.parametersPanel.cmbType2.currentIndex() != 0):
            num2 = 30;
            num3 = 60;
            if (num1 < 50):
                num2 = 0.6 * num1;
                num3 = 90 - num2;
            num7 = metres * math.sin(Unit.ConvertDegToRad(num1));
            num8 = metres * math.cos(Unit.ConvertDegToRad(num1)) * math.tan(Unit.ConvertDegToRad(num2));
            num9 = metres * ((1 - math.cos(Unit.ConvertDegToRad(num1)) / math.cos(Unit.ConvertDegToRad(num2))) / math.sin(Unit.ConvertDegToRad(num2)));
            num10 = metres1 * math.tan(Unit.ConvertDegToRad(num2 / 2));
            num11 = 10 * speed1.MetresPerSecond if(not self.parametersPanel.chbCatH.isChecked()) else 5 * speed1.MetresPerSecond;
            point3d2 = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(num), num7 + num8 + num9 + num10);
            if (turnDirection != TurnDirection.Left):
                point3d4 = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value + 90), metres);
                point3d = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(num - num3), metres);
                point3d5 = MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(num - 90), metres1);
                point3d1 = MathHelper.distanceBearingPoint(point3d5, MathHelper.getBearing(point3d5, point3d2) + Unit.ConvertDegToRad(num2), metres1);
            else:
                point3d4 = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value - 90), metres);
                point3d = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(num + num3), metres);
                point3d5 = MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(num + 90), metres1);
                point3d1 = MathHelper.distanceBearingPoint(point3d5, MathHelper.getBearing(point3d5, point3d2) - Unit.ConvertDegToRad(num2), metres1);
            point3d3 = MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(num), num11);
            polylineArea1.Add(PolylineAreaPoint(point3d7, MathHelper.smethod_57(turnDirection, point3d7, point3d, point3d4)));
            polylineArea1.method_1(point3d);
            if (turnDirection == TurnDirection.Left):
                polylineArea1.Add(PolylineAreaPoint(point3d1, MathHelper.smethod_57(TurnDirection.Right, point3d1, point3d2, point3d5)));
            elif (turnDirection != TurnDirection.Right):
                polylineArea1.method_1(point3d1);
            else:
                polylineArea1.Add(PolylineAreaPoint(point3d1, MathHelper.smethod_57(TurnDirection.Left, point3d1, point3d2, point3d5)));
            polylineArea1.method_1(point3d2);
            polylineArea1.method_1(point3d3);
            stringBuilder += "%s%s\t%f °"%("    ", Captions.TRACK_TO, round(value,4)) + "\n";
            stringBuilder += "%s%s\t%f °"%("    ", Captions.TRACK_FROM, round(num, 4)) + "\n";
            stringBuilder += "%s%s\t%f °"%("    ", Captions.COURSE_CHANGE, round(num1, 4)) + "\n";
            stringBuilder += "%s%s\t%f °"%("    ", Captions.BANK_ANGLE_1, round(value1, 4)) + "\n";
            tURNRADIUS11 = Captions.TURN_RADIUS_1;
            distance1 = Distance(metres);
            stringBuilder += "%s%s\t%f"%("    ", tURNRADIUS11, round(distance1.Metres, 4)) + "m\n";
            stringBuilder += "%s%s\t%f °"%("    ", Captions.BANK_ANGLE_2, round(num4, 4)) + "\n";
            tURNRADIUS21 = Captions.TURN_RADIUS_2;
            distance1 = Distance(metres1);
            stringBuilder += "%s%s\t%f"%("    ", tURNRADIUS21, round(distance1.Metres, 4)) + "m\n";
            stringBuilder += "%s%s\t%f °"%("    ", Captions.INTERCEPT_ANGLE, round(num2, 4)) + "\n";
            l11 = Captions.L1;
            distance1 = Distance(num7);
            stringBuilder += "%s%s\t%f"%("    ", l11, round(distance1.Metres, 4)) + "m\n";
            l21 = Captions.L2;
            distance1 = Distance(num8);
            stringBuilder += "%s%s\t%f"%("    ", l21, round(distance1.Metres, 4)) + "m\n";
            l31 = Captions.L3;
            distance1 = Distance(num9);
            stringBuilder += "%s%s\t%f"%("    ", l31, round(distance1.Metres, 4)) + "m\n";
            l41 = Captions.L4;
            distance1 = Distance(num10);
            stringBuilder += "%s%s\t%f"%("    ", l41, round(distance1.Metres, 4)) + "m\n";
            l51 = Captions.L5;
            distance1 = Distance(num11);
            stringBuilder += "%s%s\t%f"%("    ", l51, round(distance1.Metres, 4)) + "m\n";
            mINIMUMTURNDISTANCE1 = Captions.MINIMUM_TURN_DISTANCE;
            distance1 = Distance(num7 + num8 + num9 + num10 + num11);
            stringBuilder += "%s%s\t%f"%("    ", mINIMUMTURNDISTANCE1, round(distance1.Metres, 4)) + "m\n";
        else:
            num7 = metres * math.tan(Unit.ConvertDegToRad(0.5 * num1));
            num8 = 5 * speed1.MetresPerSecond if(not self.parametersPanel.chbCatH.isChecked()) else 3 * speed1.MetresPerSecond;
            point3d = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value + 180), num7);
            point3d1 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(value + 90), 100);
            point3d2 = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(num), num7);
            point3d3 = MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(num + 90), 100);
            point3d4 = MathHelper.getIntersectionPoint(point3d, point3d1, point3d2, point3d3);
            point3d = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value + 180), num7 + num8);
            point3d1 = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value + 180), num7);
            point3d2 = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(num), num7);
            point3d3 = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(num), num7 + num8);
            polylineArea1.method_1(point3d);
            polylineArea1.Add(PolylineAreaPoint(point3d1, MathHelper.smethod_57(turnDirection, point3d1, point3d2, point3d4)));
            polylineArea1.method_1(point3d2);
            polylineArea1.method_1(point3d3);
            num14 = num14 + num7 + num8;
            stringBuilder += "%s%s\t%f °"%("    ", Captions.TRACK_TO, round(value, 4)) + "\n";
            stringBuilder += "%s%s\t%f °"%("    ", Captions.TRACK_FROM, round(num, 4)) + "\n";
            stringBuilder += "%s%s\t%f °"%("    ", Captions.COURSE_CHANGE, round(num1, 4)) + "\n";
            stringBuilder += "%s%s\t%f °"%("    ", Captions.BANK_ANGLE, round(value1, 4)) + "\n";
            str1 = Captions.TURN_RADIUS;
            distance1 = Distance(metres);
            stringBuilder += "%s%s\t%f"%("    ", str1, round(distance1.Metres, 4)) + "m\n";
            rOLLINDISTANCE1 = Captions.ROLL_IN_DISTANCE;
            distance1 = Distance(num8);
            stringBuilder += "%s%s\t%f"%("    ", rOLLINDISTANCE1, round(distance1.Metres, 4)) + "m\n";
            tURNINITIATIONDISTANCE1 = Captions.TURN_INITIATION_DISTANCE;
            distance1 = Distance(num7);
            stringBuilder += "%s%s\t%f"%("    ", tURNINITIATIONDISTANCE1, round(distance1.Metres, 4)) + "m\n";
            rOLLOUTDISTANCE1 = Captions.ROLL_OUT_DISTANCE;
            distance1 = Distance(num8);
            stringBuilder += "%s%s\t%f"%("    ", rOLLOUTDISTANCE1, round(distance1.Metres, 4)) + "m\n";
            num16 = num7;
        if (self.parametersPanel.pnlAtt2.ATT.IsValid()):
            distance1 = RnavWaypoints.getDistanceFromWaypointToEarliestTurningPoint(rnavWaypointType1, self.parametersPanel.pnlAtt2.ATT, Distance(metres), num1, AngleUnits.Degrees);
            metres2 = distance1.Metres;
            distance1 = RnavWaypoints.smethod_13(rnavFlightPhase, rnavWaypointType1, speed1, self.parametersPanel.pnlWind2.Value, self.parametersPanel.pnlAtt2.ATT, Distance(metres), num1, AngleUnits.Degrees);
            metres3 = distance1.Metres;
            point3d = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value + 180), math.fabs(metres2)) if(metres2 >= 0) else MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value), math.fabs(metres2));
            point3d1 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(value + 90), 400);
            point3d2 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(value - 90), 400);
            point3dArray = [point3d1, point3d2 ];
            polylineArea4.method_7(point3dArray);
            point3d = MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value + 180), math.fabs(metres3)) if(metres3 >= 0) else MathHelper.distanceBearingPoint(point3d7, Unit.ConvertDegToRad(value), math.fabs(metres3));
            point3d1 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(value + 90), 400);
            point3d2 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(value - 90), 400);
            point3dArray = [point3d1, point3d2 ];
            polylineArea5.method_7(point3dArray);
            stringBuilder += self.parametersPanel.pnlAtt2.method_3("    ") + "\n";
            if (self.parametersPanel.pnlWind2.Value.IsValid()):
                stringBuilder += self.parametersPanel.pnlWind2.method_7("    ") + "\n";
            kKLINE1 = Captions.K_K_LINE;
            distance1 = Distance(metres2);
            stringBuilder += "%s%s\t%f"%("    ", kKLINE1, round(distance1.Metres, 4)) + "m\n";
            wINDSPIRALLINE1 = Captions.WIND_SPIRAL_LINE;
            distance1 = Distance(metres3);
            stringBuilder += "%s%s\t%f"%("    ", wINDSPIRALLINE1, round(distance1.Metres, 4)) + "m\n";

        if (MathHelper.calcDistance(point3d6, point3d7) < num14):
            eRRMSD = Messages.ERR_MSD;
            distance1 = Distance(num14);
            str2 = eRRMSD%(round(distance1.NauticalMiles, 4)) + " nm."
            QMessageBox.warning(self, "Error", str2)
            # ErrorMessageBox.smethod_0(self, str2);
            return None;
        if (bool_0):
            self.constructionLineLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)
            polylineArea.method_8(polylineArea1)
            resultPolylineArea = PolylineArea.smethod_131(polylineArea)
            AcadHelper.setGeometryAndAttributesInLayer(self.constructionLineLayer, resultPolylineArea)
            if (polylineArea2.Count == 2):
                self.method_35(polylineArea2, Captions.K_K_LINE_WPT1, self.constructionLineLayer);
            if (polylineArea3.Count == 2):
                self.method_35(polylineArea3, Captions.WIND_SPIRAL_LINE_WPT1, self.constructionLineLayer);
            if (polylineArea4.Count == 2):
                self.method_35(polylineArea4, Captions.K_K_LINE_WPT2, self.constructionLineLayer);
            if (polylineArea5.Count == 2):
                self.method_35(polylineArea5, Captions.WIND_SPIRAL_LINE_WPT2, self.constructionLineLayer);

            mapUnits = define._canvas.mapUnits()
            self.wptLayer = AcadHelper.createVectorLayer("WPT_" + self.surfaceType.replace(" ", "_").replace("-", "_"), QGis.Point)
            # fieldName = "CATEGORY"
            # self.wptLayer.startEditing()
            # self.wptLayer.dataProvider().addAttributes( [QgsField(fieldName, QVariant.String)] )
            # # self.wptLayer.startEditing()
            #
            #
            # self.wptLayer.commitChanges()
            if (self.parametersPanel.chbInsertSymbols.isChecked()):
                symbol1 = self.parametersPanel.cmbType1.currentText()#(self.pnlType1.SelectedIndex != 0 ? new Symbol(SymbolType.Flyo) : new Symbol(SymbolType.Flyb));
                AcadHelper.smethod_57(symbol1, point3d6, self.wptLayer);
                symbol1 = self.parametersPanel.cmbType2.currentText()#(self.pnlType2.SelectedIndex != 0 ? new Symbol(SymbolType.Flyo) : new Symbol(SymbolType.Flyb));
                AcadHelper.smethod_57(symbol1, point3d7, self.wptLayer);
                QgisHelper.appendToCanvas(define._canvas, [self.constructionLineLayer, self.wptLayer], self.surfaceType, True)
                self.resultLayerList = [self.constructionLineLayer, self.wptLayer]
                return stringBuilder
            QgisHelper.appendToCanvas(define._canvas, [self.constructionLineLayer], self.surfaceType, True)
            self.resultLayerList = [self.constructionLineLayer]
        return stringBuilder;
    def method_35(self, polylineArea_0, string_0, layer):
        resultPolylineArea = PolylineArea.smethod_131(polylineArea_0)
    #     AcadHelper.smethod_18(transaction_0, blockTableRecord_0, AcadHelper.smethod_131(polylineArea_0), string_1);
        num = MathHelper.getBearing(polylineArea_0[0].Position, polylineArea_0[1].Position);
        point3d = MathHelper.distanceBearingPoint(polylineArea_0[0].Position, num, MathHelper.calcDistance(polylineArea_0[0].Position, polylineArea_0[1].Position) / 2);

        if (num > 3.14159265358979):
            num = num - 3.14159265358979;


        # layer.startEditing()
        # # fields = constructionLayer.pendingFields()
        # feature = QgsFeature()
        # # feature.setFields(fields)
        # layer.startEditing()
        AcadHelper.setGeometryAndAttributesInLayer(layer, resultPolylineArea, False, {"Caption":string_0})
        # feature.setGeometry(QgsGeometry.fromPolyline(resultPolylineArea.method_14()))
        # feature.setAttributes([string_0, "", ""])
        # layer.addFeature(feature)
        #
        # layer.commitChanges()

        palSetting = QgsPalLayerSettings()
        palSetting.readFromLayer(layer)
        palSetting.enabled = True
        palSetting.fieldName = "Caption"
        palSetting.isExpression = True
        palSetting.placement = QgsPalLayerSettings.Line
        palSetting.placementFlags = QgsPalLayerSettings.AboveLine
        # palSetting.Rotation = Unit.ConvertRadToDeg(7.85398163397448 - num)
        palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '8', "")
        palSetting.writeToLayer(layer)

    def WPT2Layer(self, symbol, point3d):
        resultLayer = AcadHelper.createVectorLayer("WPT", QGis.Point)
        # fieldName = "CATEGORY"
        # resultLayer.startEditing()
        if symbol == "FlyOver":
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, point3d, False, {"Category":"FlyOver"})
            # feature = Fea()
            # feature.setGeometry(QgsGeometry.fromPoint(point3d))
            # feature.setAttribute("", "FlyOver")
            # resultLayer.addFeature(feature)
        else:
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, point3d, False, {"Category":"FlyBy"})

        #     feature = QgsFeature()
        #     feature.setGeometry(QgsGeometry.fromPoint(point3d))
        #     feature.setAttribute(fieldName, "FlyBy")
        #     resultLayer.addFeature(feature)
        #
        # resultLayer.commitChanges()

        '''FlyOver'''
        # mawpBearing = MathHelper.getBearing(self.annotationMAHWP.mapPosition(), self.annotationMAWP.mapPosition())
        symbolFlyOver = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
        symbolFlyOver.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyover.svg", 9.0, 0.0)#Unit.ConvertRadToDeg(mawpBearing))
        symbolFlyOver.appendSymbolLayer(svgSymLayer)
        renderCatFlyOver = QgsRendererCategoryV2(1, symbolFlyOver,"FlyOver")

        '''FlyBy'''
        symbolFlyBy = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
        symbolFlyBy.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyby.svg", 9.0, 0.0)#Unit.ConvertRadToDeg(mawpBearing))
        symbolFlyBy.appendSymbolLayer(svgSymLayer)
        renderCatFlyBy = QgsRendererCategoryV2(0, symbolFlyBy,"FlyBy")

        symRenderer = QgsCategorizedSymbolRendererV2(Expressions.RNAVNOMINAL_EXPRESION, [renderCatFlyOver, renderCatFlyBy])

        resultLayer.setRendererV2(symRenderer)
        return resultLayer
    def get_isDepartureSelected(self):
        flag = False;
        try:
            # rnavFlightPhase = (RnavFlightPhase)EnumHelper.smethod_1((string)self.pnlPhaseOfFlight.SelectedItem, typeof(RnavFlightPhase));
            flag = self.parametersPanel.cmbPhaseOfFlight.currentText() == "SID";
        except:
            return False;
        return flag;
    isDepartureSelected = property(get_isDepartureSelected, None, None, None)

    def get_isEnrouteSelected(self):
        flag = False;
        try:
            # rnavFlightPhase = (RnavFlightPhase)EnumHelper.smethod_1((string)self.pnlPhaseOfFlight.SelectedItem, typeof(RnavFlightPhase));
            flag = self.parametersPanel.cmbPhaseOfFlight.currentText() == "Enroute";
        except:
            return False;
        return flag;
    isEnrouteSelected = property(get_isEnrouteSelected, None, None, None)

    def get_isMissedApproachSelected(self):
        flag = False;
        try:
            # rnavFlightPhase = (RnavFlightPhase)EnumHelper.smethod_1((string)self.pnlPhaseOfFlight.SelectedItem, typeof(RnavFlightPhase));
            flag = self.parametersPanel.cmbPhaseOfFlight.currentText() == "MissedApproach";
        except:
            return False;
        return flag;
    isMissedApproachSelected = property(get_isMissedApproachSelected, None, None, None)

    def get_FlightPhase(self):
        if self.parametersPanel.cmbPhaseOfFlight.currentText() == "Enroute":
            return 0
        elif self.parametersPanel.cmbPhaseOfFlight.currentText() == "SID":
            return 1
        elif self.parametersPanel.cmbPhaseOfFlight.currentText() == "STAR":
            return 2
        elif self.parametersPanel.cmbPhaseOfFlight.currentText() == "IafIf":
            return 3
        elif self.parametersPanel.cmbPhaseOfFlight.currentText() == "Faf":
            return 4
        elif self.parametersPanel.cmbPhaseOfFlight.currentText() == "MissedApproach":
            return 5