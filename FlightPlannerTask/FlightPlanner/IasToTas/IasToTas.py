# -*- coding: utf-8 -*-
'''
Created on 18 May 2014

@author: Administrator
'''
from PyQt4.QtGui import QDialog, QIcon, QMessageBox, QStandardItemModel, QPixmap, QStandardItem, QTextDocument, QPushButton, QAbstractItemView, QComboBox, QFileDialog
# from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL, Qt, QVariant, QSizeF, QCoreApplication, QObject
from PyQt4.QtGui import QFont, QLineEdit
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.BasicGNSS.ParameterDlgs.DlgCaculateWaypoint import CalcDlg
from FlightPlanner.BasicGNSS.gnssSegments import FinalApproachSegment, MissedApproachSegment, IntermediateSegment,\
                InitialSegment1, InitialSegment2, InitialSegment3
from FlightPlanner.BasicGNSS.GnssSegmentObstacles import GnssSegmentObstacles
from FlightPlanner.types import RnavSegmentType, AircraftSpeedCategory, AltitudeUnits, SpeedUnits, AngleGradientSlopeUnits,\
                Point3D, RnavCommonWaypoint, WindType, AngleUnits, SurfaceTypes
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.helpers import Speed, Altitude, AngleGradientSlope, MathHelper, Unit, Distance
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from qgis.gui import QgsTextAnnotationItem, QgsAnnotationItem, QgsRubberBand
from qgis.core import QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsPalLayerSettings, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.expressions import Expressions
from FlightPlanner.Captions import Captions
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.FlightPlanBaseSimpleDlg import FlightPlanBaseSimpleDlg
from FlightPlanner.IasToTas.ui_IasToTas import Ui_IasToTas
from FlightPlanner.messages import Messages
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.Panels.WindPanel import WindPanel
from map.tools import SelectedFeatureByRectTasDraw
import define
import math

class IasToTasDlg(FlightPlanBaseSimpleDlg):
    def __init__(self, parent):
        FlightPlanBaseSimpleDlg.__init__(self, parent)
        self.setObjectName("IasToTas")
        self.surfaceType = SurfaceTypes.IasToTas
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.IasToTas)
        QgisHelper.matchingDialogSize(self, 650, 600)

    def btnConstruct_Click(self):
        pass
    def uiStateInit(self):
        # self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnConstruct.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)
        self.ui.btnExportResult.setVisible(False)
#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseSimpleDlg.uiStateInit(self)

    def initParametersPan(self):
        ui = Ui_IasToTas()
        self.parametersPanel = ui
        FlightPlanBaseSimpleDlg.initParametersPan(self)

        self.parametersPanel.pnlWind = WindPanel(self.parametersPanel.gbNonStandard)
        self.parametersPanel.pnlWind.lblIA.setMinimumSize(180, 0)
        self.parametersPanel.pnlWind.speedBox.setEnabled(False)
        self.parametersPanel.vLayoutNonStandard.insertWidget(0, self.parametersPanel.pnlWind)
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))

        self.parametersPanel.txtAltitude.textChanged.connect(self.txtAltitudeChanged)
        self.parametersPanel.cmbType.addItems([IasTasSegmentType.Departure, IasTasSegmentType.Enroute, IasTasSegmentType.Holding, IasTasSegmentType.InitialRR, IasTasSegmentType.InitialDR, IasTasSegmentType.IafIfFaf, IasTasSegmentType.MissedApproach])
        self.parametersPanel.cmbType.currentIndexChanged.connect(self.method_29)
        self.parametersPanel.txtIAS.textChanged.connect(self.method_29)
        self.parametersPanel.txtAltitude.textChanged.connect(self.method_29)
        self.parametersPanel.txtTime.textChanged.connect(self.method_29)
        self.parametersPanel.txtISA.textChanged.connect(self.method_29)

        self.parametersPanel.btnEST.clicked.connect(self.btnESTClicked)
        self.parametersPanel.btnREA.clicked.connect(self.btnREAClicked)
        self.parametersPanel.btnC.clicked.connect(self.btnCClicked)
        self.parametersPanel.btnD.clicked.connect(self.btnDClicked)
        self.parametersPanel.btnX.clicked.connect(self.btnXClicked)
        self.parametersPanel.btnNonStd.clicked.connect(self.btnNonStdClicked)

        self.parametersPanel.txtAltitudeM.textChanged.connect(self.txtAltitudeMChanged)
        self.parametersPanel.txtAltitude.textChanged.connect(self.txtAltitudeFtChanged)

        self.flag = 0
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtAltitudeM.setText(str(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude.text()))))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")

        self.method_29()
    def txtAltitudeMChanged(self):
        if self.flag==0:
            self.flag=1;
        if self.flag==2:
            self.flag=0;
        if self.flag==1:
            try:
                self.parametersPanel.txtAltitude.setText(str(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAltitudeM.text()))))
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
    def btnESTClicked(self):
        selectTool = SelectedFeatureByRectTasDraw(define._canvas, self.est.Metres)
        define._canvas.setMapTool(selectTool)
        QObject.connect(selectTool, SIGNAL("resultSelectedFeatureByRectTasDraw"), self.resultSelectedFeatureByRectTasDraw)
        pass
    def btnREAClicked(self):
        selectTool = SelectedFeatureByRectTasDraw(define._canvas, self.rea.Metres)
        define._canvas.setMapTool(selectTool)
        QObject.connect(selectTool, SIGNAL("resultSelectedFeatureByRectTasDraw"), self.resultSelectedFeatureByRectTasDraw)

    def btnCClicked(self):
        selectTool = SelectedFeatureByRectTasDraw(define._canvas, self.c.Metres)
        define._canvas.setMapTool(selectTool)
        QObject.connect(selectTool, SIGNAL("resultSelectedFeatureByRectTasDraw"), self.resultSelectedFeatureByRectTasDraw)

    def btnDClicked(self):
        selectTool = SelectedFeatureByRectTasDraw(define._canvas, self.d.Metres)
        define._canvas.setMapTool(selectTool)
        QObject.connect(selectTool, SIGNAL("resultSelectedFeatureByRectTasDraw"), self.resultSelectedFeatureByRectTasDraw)

    def btnXClicked(self):
        selectTool = SelectedFeatureByRectTasDraw(define._canvas, self.x.Metres)
        define._canvas.setMapTool(selectTool)
        QObject.connect(selectTool, SIGNAL("resultSelectedFeatureByRectTasDraw"), self.resultSelectedFeatureByRectTasDraw)
    def btnNonStdClicked(self):
        selectTool = SelectedFeatureByRectTasDraw(define._canvas, self.custom.Metres)
        define._canvas.setMapTool(selectTool)
        QObject.connect(selectTool, SIGNAL("resultSelectedFeatureByRectTasDraw"), self.resultSelectedFeatureByRectTasDraw)

    def resultSelectedFeatureByRectTasDraw(self, geom, distance, direction_bearing):
        # flag = FlightPlanBaseSimpleDlg.btnConstruct_Click(self)
        # if not flag:
        #     return
        if define._userLayers == None:
            mapUnits = define._canvas.mapUnits()
            constructionLayer = AcadHelper.createVectorLayer("Lines", QGis.Line)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, geom.asPolyline(), False, {"Caption":str(round(distance, 4)) + "m"})


            define._userLayers = constructionLayer
            palSetting = QgsPalLayerSettings()
            palSetting.readFromLayer(constructionLayer)
            palSetting.enabled = True
            palSetting.fieldName = "Caption"
            palSetting.isExpression = True
            palSetting.placement = QgsPalLayerSettings.Line
            palSetting.placementFlags = QgsPalLayerSettings.AboveLine
            palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '8', "")
            palSetting.writeToLayer(constructionLayer)
            QgisHelper.appendToCanvas(define._canvas,[constructionLayer], "Users layer", True)
            # self.resultLayerList = [constructionLayer]
        else:


            # constructionLayer = AcadHelper.createVectorLayer("Lines", QGis.Line)
            constructionLayer = define._userLayers
            iter = define._userLayers. getFeatures()
            equalFlag = 0
            for feat in iter:
                # AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, feat)
                if geom.equals(feat.geometry()):
                    equalFlag += 1
            if equalFlag <= 0:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, geom.asPolyline(), False, {"Caption":str(round(distance, 4)) + "m"})




            palSetting = QgsPalLayerSettings()
            palSetting.readFromLayer(constructionLayer)
            palSetting.enabled = True
            palSetting.fieldName = "Caption"
            palSetting.isExpression = True
            palSetting.placement = QgsPalLayerSettings.Line
            palSetting.placementFlags = QgsPalLayerSettings.AboveLine
            palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '8', "")
            palSetting.writeToLayer(constructionLayer)
            # QgisHelper.appendToCanvas(define._canvas,[constructionLayer], "Users layer", True)
            # self.resultLayerList = [constructionLayer]
            QgisHelper.zoomToLayers([constructionLayer])
            define._userLayers = constructionLayer
        pass
    def txtAltitudeChanged(self):
        try:
            self.method_29()
            self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
        except:
            pass
    def method_27(self, speed_0, speed_1, double_0):
        return Distance((speed_0 + speed_1).MetresPerSecond * double_0);
    
    def method_29(self):
        speed = None;
        speed1 = None;
        num = None;
        num1 = None;
        # Validator validator = new Validator(ValidationFlags.None);
        flag = True;
        flag1 = True;
        # self.errorProvider.method_1();
        # if (!self.cmbType.method_1(validator))
        # {
        #     flag = false;
        # }
        # if (!self.pnlAltitude.method_1(validator))
        # {
        #     flag = false;
        # }
        # if (!self.pnlISA.method_2(validator))
        # {
        #     flag = false;
        # }
        # validator.Flags = ValidationFlags.Positive;
        # if (!self.pnlIAS.method_1(validator))
        # {
        #     flag = false;
        # }
        # validator.Flags = ValidationFlags.AllowEmpty | ValidationFlags.NonNegative;
        # if (!self.pnlWind.method_1(validator))
        # {
        #     flag1 = false;
        # }
        # if (!self.pnlTime.method_1(validator))
        # {
        #     flag1 = false;
        # }
        if (flag1):
            if self.parametersPanel.pnlWind.Value == None:
                flag1 = False
            else:
                try:
                    time = float(self.parametersPanel.txtTime.text())
                    flag1 = True
                except:
                    flag1 = False
            # flag1 = False if(self.pnlWind.Value.IsNaN) else not double.IsNaN(self.pnlTime.Value));
        # }
        # self.panelEx.SuspendLayout();
        # self.gbResults.SuspendLayout();
        # try:
        tAS = Captions.TAS;
        eST = Captions.EST;
        pILOTREACTION = Captions.PILOT_REACTION;
        str0 = Captions.c;
        str1 = "";
        self.est = Distance.NaN();
        self.rea = Distance.NaN();
        self.c = Distance.NaN();
        self.x = Distance.NaN();
        self.d = Distance.NaN();
        self.custom = Distance.NaN();
        if (not flag):
            self.parametersPanel.txtTAS.setText(Captions.NOT_APPLICABLE);
            self.parametersPanel.txtEST.setText(Captions.NOT_APPLICABLE);
            self.parametersPanel.txtREA.setText(Captions.NOT_APPLICABLE);
            self.parametersPanel.txtC.setText(Captions.NOT_APPLICABLE);
            self.parametersPanel.txtX.setText(Captions.NOT_APPLICABLE);
            self.parametersPanel.txtD.setText(Captions.NOT_APPLICABLE);
            self.parametersPanel.txtNonStandardResult.setText(Captions.NOT_APPLICABLE);
        else:
            value = Speed(float(self.parametersPanel.txtIAS.text()), SpeedUnits.KTS);
            altitude = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT);
            value1 = float(self.parametersPanel.txtISA.text());
            selectedIndex = self.parametersPanel.cmbType.currentText();
            if selectedIndex == IasTasSegmentType.Departure or selectedIndex == IasTasSegmentType.MissedApproach:
                speed = Speed(30);
                num = 3;
                speed1 = Speed(30);
                num1 = 3;
            elif selectedIndex == IasTasSegmentType.Enroute:
                speed = Speed.smethod_1(altitude);
                num = 5;
                speed1 = Speed.smethod_1(altitude);
                num1 = 10;
            elif selectedIndex == IasTasSegmentType.Holding or selectedIndex == IasTasSegmentType.InitialRR:
                speed = Speed.smethod_1(altitude);
                num = 5;
                speed1 = Speed.smethod_1(altitude);
                num1 = 6;
            elif selectedIndex == IasTasSegmentType.InitialDR or selectedIndex == IasTasSegmentType.IafIfFaf:
                speed = Speed(30);
                num = 5;
                speed1 = Speed(30);
                num1 = 6;
            else:
                pass
    #                 throw new Exception(Messages.ERR_UNSUPPORTED_PROCEDURE_SEGMENT_TYPE);
            if (selectedIndex == IasTasSegmentType.Departure):
                m = value
                n = (value / 10)
                value = m + n;
                tAS = tAS + " (" + Captions.IAS + "+ 10%)";
            speed2 = Speed.smethod_0(value, value1, altitude);
            self.est = self.method_27(speed2, speed, num);
            self.rea = self.method_27(speed2, speed1, num1);
            self.c = self.est + self.rea;
            self.x = self.method_27(speed2, Speed(10), 15);
            self.d = self.method_27(speed2, Speed(10), 3);
            eST = eST + " (%i kts / %i s)"%(speed.Knots, num);
            pILOTREACTION = pILOTREACTION + " (%i kts / %i s)"%(speed1.Knots, num1);
            str0 = str0 + " (%i kts / %i + %i s)"%(speed.Knots, num, num1);
            self.parametersPanel.label_10.setText(tAS);
            self.parametersPanel.txtTAS.setText(str(speed2.Knots) + "kts");
            self.parametersPanel.label_73.setText(eST);
            self.parametersPanel.txtEST.setText(str(self.est.Metres) + "m");
            self.parametersPanel.label_74.setText(pILOTREACTION);
            self.parametersPanel.txtREA.setText(str(self.rea.Metres) + "m");
            self.parametersPanel.label_75.setText(str0);
            self.parametersPanel.txtC.setText(str(self.c.Metres) + "m");
            self.parametersPanel.txtX.setText(str(self.x.Metres) + "m");
            self.parametersPanel.txtD.setText(str(self.d.Metres) + "m");
            if (not flag1):
                self.parametersPanel.txtNonStandardResult.setText(Captions.NOT_APPLICABLE);
            else:
                self.custom = self.method_27(speed2, self.parametersPanel.pnlWind.Value, float(self.parametersPanel.txtTime.text()));
                str2 = str(self.parametersPanel.pnlWind.Value.Knots) + "kts";
                value2 = float(self.parametersPanel.txtTime.text());
                str1 = "%s / %i s"%(str2, value2);
                self.parametersPanel.txtNonStandardResult.setText(str(self.custom.Metres) + "m");
        self.parametersPanel.label_10.setText(tAS);
        self.parametersPanel.label_73.setText(eST);
        self.parametersPanel.label_74.setText(pILOTREACTION);
        self.parametersPanel.label_75.setText(str0);
        self.parametersPanel.label_11.setText(str1);
    #     self.method_28(self.pnlEST);
    #     self.method_28(self.pnlREA);
    #     self.method_28(self.pnlC);
    #     self.method_28(self.pnlX);
    #     self.method_28(self.pnlD);
    #     self.method_28(self.pnlNonStandardResult);
        self.parametersPanel.frame_X.setVisible(self.parametersPanel.cmbType.currentIndex() == 6);
        self.parametersPanel.frame_D.setVisible(self.parametersPanel.cmbType.currentIndex() == 6);
        self.parametersPanel.gbNonStandardResult.setVisible(self.parametersPanel.txtNonStandardResult.text() != Captions.NOT_APPLICABLE);
        # except:
        #     pass
class IasTasSegmentType:
    Departure = "Departure"
    Enroute = "En-route"
    Holding = "Holding"
    InitialRR = "Initial approach - reversal and racetrack procedures"
    InitialDR = "Initial approach - DR track procedures"
    IafIfFaf = "IAF, IF, FAF"
    MissedApproach = "Missed Approach"
        
