# -*- coding: utf-8 -*-
'''
Created on Apr 22, 2015

@author: Administrator
'''
from PyQt4.QtGui import QDialog, QMessageBox, QStandardItem, QFileDialog
from PyQt4.QtCore import QVariant, QCoreApplication, SIGNAL
from qgis.core import QGis, QgsField, QgsRectangle

# from FlightPlanner.PinSVisualSegment.ui_PinSVisualSegmentDepDlg import ui_PinSVisualSegmentDepDlg

from FlightPlanner.types import PinsVisualSegmentType, DistanceUnits, AltitudeUnits, PinsOperationType,\
        OCAHType, TurnDirection, ConstructionType, \
        SurfaceTypes, Point3D, CriticalObstacleType, ObstacleTableColumnType, PinsSurfaceType,\
        AngleUnits
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, AngleGradientSlope
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.MCAHPanel import MCAHPanel
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.messages import Messages
from FlightPlanner.polylineArea import PolylineArea
from FlightPlanner.Polyline import Polyline
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.PinSVisualSegment.ui_PinsApp import Ui_PinsApp
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
import define
import math

class PinSVisualSegmentAppDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("PinSVisualSegmentAppDlg")
        self.surfaceType = SurfaceTypes.PinSVisualSegmentApp
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.PinSVisualSegmentApp)
        QgisHelper.matchingDialogSize(self, 670, 700)
    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)  
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False) 
        self.ui.tabCtrlGeneral.removeTab(2)
        return FlightPlanBaseDlg.uiStateInit(self)
        

    def initParametersPan(self):
        ui = Ui_PinsApp()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)
        
        self.pnlOCAH = MCAHPanel(ui.groupBox_20)
        self.pnlOCAH.lblMCAH.setText("Minimum (ft):")
        self.pnlOCAH.setValue(Altitude(500, AltitudeUnits.FT))
        self.pnlOCAH.cmbMCAH.clear()
        self.pnlOCAH.cmbMCAH.addItems([OCAHType.OCA, OCAHType.OCH])
        ui.verticalLayout_5.insertWidget(4, self.pnlOCAH)
        ui.cmbSegmentType.Items = [PinsVisualSegmentType.Direct, PinsVisualSegmentType.Manoeuvring]
        ui.cmbApproachType.Items = [PinsOperationType.DayOnly, PinsOperationType.DayNight]
        ui.cmbApproachType.SelectedIndex = 1
        ui.cmbConstructionType.Items = [ConstructionType.Construct2D, ConstructionType.Construct3D]
        ui.txtApproachSurfaceTrack.Visible = False
        ui.frame_Limitation.hide()        
        
        self.pnlHRP = PositionPanel(ui.grbIDF)
        self.pnlHRP.groupBox.setTitle("Heliport Reference point (HRP)")
        self.pnlHRP.btnCalculater.hide()
        self.pnlHRP.setObjectName("positionHRP")
        ui.verticalLayout_HRP.insertWidget(0, self.pnlHRP)
        self.connect(self.pnlHRP, SIGNAL("positionChanged"), self.initResultPanel)
        
        self.pnlMAPt = PositionPanel(ui.grbIDF)
        self.pnlMAPt.groupBox.setTitle("")
        self.pnlMAPt.hideframe_Altitude()
        self.pnlMAPt.setObjectName("positionMAPt")
        self.pnlMAPt.btnCalculater.hide()
        ui.verticalLayout_IDF.insertWidget(0, self.pnlMAPt)
        self.connect(self.pnlMAPt, SIGNAL("positionChanged"), self.initResultPanel)
        
        ui.frame_Tolerance.hide()
        self.pnlTolerance = RnavTolerancesPanel(ui.grbIDF)
        self.pnlTolerance.set_HasXTT(False)        
        self.pnlTolerance.set_Att(Distance(0.24, DistanceUnits.NM))
        self.pnlTolerance.set_Asw(Distance(0.8, DistanceUnits.NM))
        ui.verticalLayout_IDF.addWidget(self.pnlTolerance)        
        
        '''Event Handlers Connect'''
#         ui.btnOpenData.clicked.connect(self.openData)
#         ui.btnSaveData.clicked.connect(self.saveData)
        self.connect(ui.cmbSegmentType, SIGNAL("Event_0"), self.chbLeftTurnProhibited_Click)
        self.connect(ui.cmbApproachType, SIGNAL("Event_0"), self.chbLeftTurnProhibited_Click)
        self.connect(ui.txtVSDG, SIGNAL("Event_0"), self.chbLeftTurnProhibited_Click)
        self.connect(ui.txtApproachSurfaceTrack, SIGNAL("Event_0"), self.chbLeftTurnProhibited_Click)
        # ui.btnCaptureSurfaceTrack.clicked.connect(self.method_39)
        self.connect(ui.chbLeftFlyOverProhibited, SIGNAL("Event_0"), self.chbLeftTurnProhibited_Click)
        self.connect(ui.chbRightFlyOverProhibited, SIGNAL("Event_0"), self.chbLeftTurnProhibited_Click)
        # ui.btnCaptureTrackTo.clicked.connect(self.method_37)
        self.pnlMAPt.txtPointX.textChanged.connect(self.chbLeftTurnProhibited_Click)
        self.pnlMAPt.txtPointY.textChanged.connect(self.chbLeftTurnProhibited_Click)
        self.pnlHRP.txtPointX.textChanged.connect(self.chbLeftTurnProhibited_Click)
        self.pnlHRP.txtPointY.textChanged.connect(self.chbLeftTurnProhibited_Click)
        self.pnlHRP.txtAltitudeM.textChanged.connect(self.chbLeftTurnProhibited_Click)

    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        try:
            self.method_27(True)
            if (self.parametersPanel.cmbSegmentType.SelectedIndex != 0):
                self.pinSVisualSegmentDepManouvering = PinSVisualSegmentAppManouvering(self)
            else:
                self.pinSVisualSegmentDepManouvering = PinSVisualSegmentAppDirect(self)
        
            layersList = []
            if self.parametersPanel.cmbConstructionType.SelectedItem != ConstructionType.Construct2D:
                self.pinSVisualSegmentDepManouvering.imethod_2(layersList)
            else:
                self.pinSVisualSegmentDepManouvering.imethod_1(layersList)
                
            QgisHelper.appendToCanvas(define._canvas, layersList, SurfaceTypes.PinSVisualSegmentApp)
            QgisHelper.zoomToLayers(layersList)
            self.resultLayerList = layersList
            self.ui.btnEvaluate.setEnabled(True)
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
        

    def initObstaclesModel(self):
        self.obstaclesModel = PinSVisualSegmentAppObstacles([self.pinSVisualSegmentDepManouvering])
        return FlightPlanBaseDlg.initObstaclesModel(self)


    def initSurfaceCombo(self):
        if self.parametersPanel.cmbSegmentType.SelectedIndex == 0:
            self.ui.cmbObstSurface.addItems(["All", PinsSurfaceType.PinsSurfaceType_OCS, PinsSurfaceType.PinsSurfaceType_OIS, PinsSurfaceType.PinsSurfaceType_LevelOCS, PinsSurfaceType.PinsSurfaceType_LevelOIS])
        else:
            self.ui.cmbObstSurface.addItems(["All", PinsSurfaceType.PinsSurfaceType_OCS, PinsSurfaceType.PinsSurfaceType_OIS, PinsSurfaceType.PinsSurfaceType_LevelOCS])
            
        return FlightPlanBaseDlg.initSurfaceCombo(self)
    
    def method_27(self, bool_0):
        try:
            if not self.pnlMAPt.IsValid():
                raise UserWarning ,"IDF poisition value is incorrect. "
            if not self.pnlHRP.IsValid():
                raise UserWarning ,"HRP poisition value is incorrect."

            if (self.parametersPanel.cmbSegmentType.SelectedIndex == 1):
                self.valueValidate(self.parametersPanel.txtApproachSurfaceTrack, "ApproachSurfaceTrack")
            self.valueValidate(self.pnlOCAH.txtMCAH, "Minimum")
            return True
 
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
    
    def method_29(self):
        self.ui.cmbObstSurface.clear()
    
    def method_32(self):
        self.parametersPanel.txtApproachSurfaceTrack.Visible = self.parametersPanel.cmbSegmentType.SelectedIndex == 1
        self.pnlTolerance.setVisible(self.parametersPanel.cmbSegmentType.SelectedIndex == 0)
        self.parametersPanel.frame_Limitation.setVisible(self.parametersPanel.cmbSegmentType.SelectedIndex == 1)
    
    def method_33(self):
        turnDirection = []   
        try:     
            if (self.parametersPanel.cmbSegmentType.SelectedIndex== 1):
                point3d = self.pnlMAPt.getPoint3D()
                point3d1 = self.pnlHRP.getPoint3D()
                num = Unit.smethod_1(MathHelper.getBearing(point3d, point3d1))
                num1 = MathHelper.smethod_3(self.smethod_17(self.parametersPanel.txtApproachSurfaceTrack) +180)
                MathHelper.smethod_77(num, num1, AngleUnits.Degrees, turnDirection)
                
                if (turnDirection[0] == TurnDirection.Left):
                    pass
                elif (turnDirection[0] != TurnDirection.Right):
                    if (self.parametersPanel.chbLeftFlyOverProhibited.Checked and self.parametersPanel.chbRightFlyOverProhibited.Checked):
                        self.parametersPanel.chbRightFlyOverProhibited.Checked = False
                else:
                    pass
        except:
            pass 
    def method_39(self):
        CaptureBearingSurfaceTrack = CaptureBearingTool(define._canvas, self.parametersPanel.txtApproachSurfaceTrack)
        define._canvas.setMapTool(CaptureBearingSurfaceTrack) 
    def smethod_17(self, txtBox):
        try:
            value1 = float(txtBox.text())
            return value1
        except:
            return 0         
    def chbLeftTurnProhibited_Click(self):
        sender = self.sender() 
        if sender == self.parametersPanel.cmbSegmentType:
            self.method_32()
        elif (sender == self.pnlMAPt.txtPointX or sender == self.pnlMAPt.txtPointY):
            self.method_33()
        elif (sender == self.pnlHRP.txtPointX or sender == self.pnlHRP.txtPointY or sender == self.pnlHRP.txtAltitudeM):
            self.method_33()
        elif (sender == self.parametersPanel.txtApproachSurfaceTrack):
            self.method_33()
        elif ((sender == self.parametersPanel.chbLeftFlyOverProhibited or sender == self.parametersPanel.chbRightFlyOverProhibited) and self.parametersPanel.cmbSegmentType.SelectedIndex== 1):
            if (sender == self.parametersPanel.chbLeftFlyOverProhibited):
                if (self.parametersPanel.chbRightFlyOverProhibited.Visible):
                    self.parametersPanel.chbRightFlyOverProhibited.Checked = False
            elif (sender == self.parametersPanel.chbRightFlyOverProhibited and self.parametersPanel.chbLeftFlyOverProhibited.Visible):
                self.parametersPanel.chbLeftFlyOverProhibited.Checked = False
        self.method_29()
    
    def valueValidate(self, txtBox, title):
        try:
            value = float(txtBox.text())
            return True
        except ValueError:
            raise UserWarning ,"%s Value is not correct "%title
    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return
        self.filterList = []
        if self.parametersPanel.cmbSegmentType.SelectedIndex != 0:
            self.filterList = ["", PinsSurfaceType.PinsSurfaceType_OCS, PinsSurfaceType.PinsSurfaceType_OIS, PinsSurfaceType.PinsSurfaceType_LevelOCS]
        else:
            self.filterList = ["", PinsSurfaceType.PinsSurfaceType_OCS, PinsSurfaceType.PinsSurfaceType_OIS, PinsSurfaceType.PinsSurfaceType_LevelOCS, PinsSurfaceType.PinsSurfaceType_LevelOIS]
#         self.ui.btnExportResult.setEnabled(True)     
        
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, "PinS Visual Segment for Approaches", self.ui.tblObstacles, self.filterList, parameterList, resultHideColumnNames)
        self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
        # return FlightPlanBaseDlg.exportResult(self)
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Visual Segment Type", self.parametersPanel.cmbSegmentType.SelectedItem))
        parameterList.append(("Approach Type", self.parametersPanel.cmbApproachType.SelectedItem))
        parameterList.append(("VSDG", str(self.parametersPanel.txtVSDG.Value.Degrees) + unicode(" °", "utf-8")))
        parameterList.append(("Minimum(%s)"%self.pnlOCAH.cmbMCAH.currentText(), self.pnlOCAH.txtMCAH.text() + " ft"))
        parameterList.append(("MOC", str(self.parametersPanel.txtMOC.Value.Metres) + " m"))
        parameterList.append(("", str(self.parametersPanel.txtMOC.Value.Feet) + " ft"))

        parameterList.append(("Construction Type", self.parametersPanel.cmbConstructionType.SelectedItem))
        
        if self.parametersPanel.cmbSegmentType.SelectedIndex != 0:
            parameterList.append(("In-bound Approach Surface Track", "Plan : " + str(self.parametersPanel.txtApproachSurfaceTrack.txtRadialPlan.Value) + define._degreeStr))
            parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtApproachSurfaceTrack.txtRadialGeodetic.Value) + define._degreeStr))

            # parameterList.append(("In-bound Approach Surface Track", self.parametersPanel.txtApproachSurfaceTrack.Value + unicode(" °", "utf-8")))
            if self.parametersPanel.chbRightFlyOverProhibited.Checked:
                parameterList.append(("Limitation", "Right turn prohibited"))
            else:
                parameterList.append(("Limitation", "Left turn prohibited"))
                                
        parameterList.append(("Missed Approach Point(MAPt)", "group"))
#         parameterList.append(("X", self.pnlMAPt.txtPointX.text()))
#         parameterList.append(("Y", self.pnlMAPt.txtPointY.text()))
        DataHelper.pnlPositionParameter(self.pnlMAPt, parameterList)
        parameterList.append(("Track From", "Plan : " + str(self.parametersPanel.txtTrackTo.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtTrackTo.txtRadialGeodetic.Value) + define._degreeStr))

        # parameterList.append(("Track From", self.parametersPanel.txtTrackTo.Value + unicode(" °", "utf-8")))
        if self.parametersPanel.cmbSegmentType.SelectedIndex == 0:
            parameterList.append(("ATT", self.pnlTolerance.txtAtt.text() + " nm"))
            parameterList.append(("1/2 A/W", self.pnlTolerance.txtAsw.text() + " nm"))
                
        parameterList.append(("Heliport", "group"))
#         parameterList.append(("X", self.pnlHRP.txtPointX.text()))
#         parameterList.append(("Y", self.pnlHRP.txtPointY.text()))
#         parameterList.append(("Altitude", self.pnlHRP.txtAltitudeM.text() + " m/" + self.pnlHRP.txtAltitudeFt.text() + " ft"))
        DataHelper.pnlPositionParameter(self.pnlHRP, parameterList)
        parameterList.append(("Crossing Height [HCH]", str(self.parametersPanel.txtHCH.Value) + " m"))
        parameterList.append(("Safety Area Length", str(self.parametersPanel.txtHSAL.Value.Metres) + " m"))
        parameterList.append(("Safety Area Width", str(self.parametersPanel.txtHSAW.Value.Metres) + " m"))
                
        parameterList.append(("Results / Checked Obstacles", "group"))        
#  
        parameterList.append(("Checked Obstacles", "group"))
        
        for strFilter in self.filterList:
            self.obstaclesModel.setFilterFixedString(strFilter)
            c = self.obstaclesModel.rowCount()
            parameterList.append(("Number of Checked Obstacles(%s)"%strFilter, str(c)))  
        return parameterList

class IPinSVisualSegmentApp:

    def get_Cancelled(self):
        pass
    Cancelled = property(get_Cancelled, None, None, None)
    
    def get_SelectionArea(self):
        pass
    SelectionArea = property(get_SelectionArea, None, None, None)

    def imethod_1(self):
        pass
    
    def imethod_2(self):
        pass

class PinSVisualSegmentAppDirect(IPinSVisualSegmentApp):#, IObstacleEvaluator
    
    def __init__(self, pinSVisualSegmentApp_0):
        
        self.RADIUS = 750

        self.MAX_WIDTH = 120
 
        self.OCS = 0
 
        self.OIS = 1
 
        self.LEVEL_OCS = 2
 
        self.LEVEL_OIS = 3
 
        self.ptsOCSL = []
 
        self.ptsOCSR = []
 
        self.ptsOISL = []
 
        self.ptsOISR = []
 
        self.ptsLevelOCSL = []
 
        self.ptsLevelOCSR = []
 
        self.ptsLevelOISL = []
 
        self.ptsLevelOISR = []
 
        self.ptsOIS = []
 
        self.ptsOCS = []
 
        self.ptsLevelOIS = []
 
        self.ptsLevelOCS = []
 
        self.selectionArea = []
 
        self.ptHRP = None
     
        self.ptMAPt = None
     
        self.ptStart = None
     
        self.track = 0.0
     
        self.tang = 0.0
     
        self.cancelled = False
 
        turnDirection = "Nothing"
        self.ptMAPt = pinSVisualSegmentApp_0.pnlMAPt.Point3d;
        self.ptHRP = pinSVisualSegmentApp_0.pnlHRP.Point3d;
        point3d13 = self.ptHRP
        num = MathHelper.getBearing(self.ptHRP, self.ptMAPt)
        try:
            value = pinSVisualSegmentApp_0.parametersPanel.txtHSAL.Value
        except ValueError:
            raise UserWarning, "HSAL Value is invalid!"
        self.ptStart = MathHelper.distanceBearingPoint(point3d13, num, value.Metres / 2);
        num1 = MathHelper.getBearing(self.ptMAPt, self.ptHRP);
        num2 = MathHelper.smethod_4(num1 + 3.14159265358979);
        try:
            num3 = Unit.ConvertDegToRad(float(pinSVisualSegmentApp_0.parametersPanel.txtTrackTo.Value));
        except ValueError:
            raise UserWarning, "Track To is invalid!"
        self.track = num1
        altitude = pinSVisualSegmentApp_0.pnlOCAH.method_3(Altitude(self.ptHRP.get_Z()));
        metres = altitude.Metres
        try:
            metres1 = pinSVisualSegmentApp_0.parametersPanel.txtMOC.Value.Metres
        except ValueError:
            raise UserWarning, "MOC is invalid!"
        turnDirList = []
        if (MathHelper.smethod_77(Unit.smethod_1(num3), Unit.smethod_1(num1), AngleUnits.Degrees, turnDirList ) > 30.9):
            raise UserWarning, Messages.ERR_COURSE_CHANGES_GREATER_THAN_30_NOT_ALLOWED
        turnDirection = turnDirList[0]
        if (MathHelper.calcDistance(self.ptHRP, self.ptMAPt) > 3000):
            raise UserWarning, Messages.ERR_VISUAL_SEGMENT_EXCEEDS_MAX_LENGTH
        try:
            metres2 = float(pinSVisualSegmentApp_0.parametersPanel.txtHCH.Value)
        except ValueError:
            raise UserWarning, "Crossing Height [HCH] is invalid!"
        if (metres - metres1 <= 0 or metres - metres2 <= 0):
            raise UserWarning, Messages.ERR_INSUFFICIENT_MINIMUM_ALTITUDE
        angleGradientSlope = pinSVisualSegmentApp_0.parametersPanel.txtVSDG.Value
        num4 = (metres - metres2) / math.tan(Unit.ConvertDegToRad(angleGradientSlope.Degrees));
        value1 = angleGradientSlope
        self.tang = math.tan(Unit.ConvertDegToRad(value1.Degrees - 1.12));
        
        try:
            metres3 = pinSVisualSegmentApp_0.parametersPanel.txtHSAL.Value.Metres
        except ValueError:
            raise UserWarning, "Safety Area Length is invalid!"
        try:
            metres4 = pinSVisualSegmentApp_0.parametersPanel.txtHSAW.Value.Metres
        except ValueError:
            raise UserWarning, "Safety Area Width is invalid!"
        metres5 = pinSVisualSegmentApp_0.pnlTolerance.ASW.Metres;
        num5 = pinSVisualSegmentApp_0.pnlTolerance.ATT.Metres;
        point3d14 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(self.ptHRP, num2, metres3 / 2), num2, num4);
        if (MathHelper.calcDistance(self.ptHRP, point3d14) > MathHelper.calcDistance(self.ptHRP, self.ptMAPt)):
            raise UserWarning, Messages.ERR_INSUFFICIENT_SEGMENT_LENGTH
        point3d15 = MathHelper.distanceBearingPoint(self.ptMAPt, num3 - 1.5707963267949, metres5 / 2);
        point3d15 = MathHelper.distanceBearingPoint(point3d15, num3, num5);
        point3d16 = MathHelper.distanceBearingPoint(self.ptMAPt, num3 + 1.5707963267949, metres5 / 2);
        point3d16 = MathHelper.distanceBearingPoint(point3d16, num3, num5);
        point3d2 = MathHelper.getIntersectionPoint(point3d15, point3d16, self.ptHRP, self.ptMAPt);
        if (MathHelper.calcDistance(self.ptHRP, point3d14) > MathHelper.calcDistance(self.ptHRP, point3d2)):
            point3d14 = self.ptMAPt;
        num6 = (240 - metres4) / 2 / 0.1 if (pinSVisualSegmentApp_0.parametersPanel.cmbApproachType.SelectedIndex == 0) else (240 - metres4) / 2 / 0.15
        num7 = (metres - metres1) / self.tang
        if (num6 >= num7):
            point3d = MathHelper.distanceBearingPoint(self.ptHRP, num2, metres3 / 2);
            point3d = MathHelper.distanceBearingPoint(point3d, num2 + 1.5707963267949, metres4 / 2);
            self.ptsOCSL.append(Point3D(point3d.get_X(), point3d.get_Y(), self.ptHRP.get_Z()));
            point3d = MathHelper.distanceBearingPoint(self.ptHRP, num2, metres3 / 2 + num7);
            point3d = MathHelper.distanceBearingPoint(point3d, num2 + 1.5707963267949, 120);
            self.ptsOCSL.append(Point3D(point3d.get_X(), point3d.get_Y(), self.ptHRP.get_Z() + self.tang * num7));
            point3d = MathHelper.distanceBearingPoint(self.ptHRP, num2, metres3 / 2);
            point3d = MathHelper.distanceBearingPoint(point3d, num2 - 1.5707963267949, metres4 / 2);
            self.ptsOCSR.append(Point3D(point3d.get_X(), point3d.get_Y(), self.ptHRP.get_Z()));
            point3d = MathHelper.distanceBearingPoint(self.ptHRP, num2, metres3 / 2 + num7);
            point3d = MathHelper.distanceBearingPoint(point3d, num2 - 1.5707963267949, 120);
            self.ptsOCSR.append(Point3D(point3d.get_X(), point3d.get_Y(), self.ptHRP.get_Z() + self.tang * num7));
        else:
            point3d = MathHelper.distanceBearingPoint(self.ptHRP, num2, metres3 / 2);
            point3d = MathHelper.distanceBearingPoint(point3d, num2 + 1.5707963267949, metres4 / 2);
            self.ptsOCSL.append(Point3D(point3d.get_X(), point3d.get_Y(), self.ptHRP.get_Z()));
            point3d = MathHelper.distanceBearingPoint(self.ptHRP, num2, metres3 / 2 + num6);
            point3d = MathHelper.distanceBearingPoint(point3d, num2 + 1.5707963267949, 120);
            self.ptsOCSL.append(Point3D(point3d.get_X(), point3d.get_Y(), self.ptHRP.get_Z() + self.tang * num6));
            point3d = MathHelper.distanceBearingPoint(self.ptHRP, num2, metres3 / 2 + num7);
            point3d = MathHelper.distanceBearingPoint(point3d, num2 + 1.5707963267949, 120);
            self.ptsOCSL.append(Point3D(point3d.get_X(), point3d.get_Y(), self.ptHRP.get_Z() + self.tang * num7));
            point3d = MathHelper.distanceBearingPoint(self.ptHRP, num2, metres3 / 2);
            point3d = MathHelper.distanceBearingPoint(point3d, num2 - 1.5707963267949, metres4 / 2);
            self.ptsOCSR.append(Point3D(point3d.get_X(), point3d.get_Y(), self.ptHRP.get_Z()));
            point3d = MathHelper.distanceBearingPoint(self.ptHRP, num2, metres3 / 2 + num6);
            point3d = MathHelper.distanceBearingPoint(point3d, num2 - 1.5707963267949, 120);
            self.ptsOCSR.append(Point3D(point3d.get_X(), point3d.get_Y(), self.ptHRP.get_Z() + self.tang * num6));
            point3d = MathHelper.distanceBearingPoint(self.ptHRP, num2, metres3 / 2 + num7);
            point3d = MathHelper.distanceBearingPoint(point3d, num2 - 1.5707963267949, 120);
            self.ptsOCSR.append(Point3D(point3d.get_X(), point3d.get_Y(), self.ptHRP.get_Z() + self.tang * num7));
        point3d17 = MathHelper.distanceBearingPoint(self.ptMAPt, num3 - 1.5707963267949, metres5 / 2);
        point3d18 = MathHelper.distanceBearingPoint(self.ptMAPt, num3 + 1.5707963267949, metres5 / 2);
        point3d19 = MathHelper.distanceBearingPoint(point3d17, num3 + 3.14159265358979, num5);
        point3d20 = MathHelper.distanceBearingPoint(point3d18, num3 + 3.14159265358979, num5);
        if (not point3d14.smethod_170(self.ptMAPt)):
            point3d7 = MathHelper.distanceBearingPoint(point3d14, num1 - 1.5707963267949, metres5 / 2);
            point3d8 = MathHelper.distanceBearingPoint(point3d14, num1 + 1.5707963267949, metres5 / 2);
            point3d11 = MathHelper.distanceBearingPoint(point3d7, num1, 100)
            point3d12 = MathHelper.distanceBearingPoint(point3d8, num1, 100)
            point3d9 = MathHelper.getIntersectionPoint(point3d19, point3d17, point3d7, point3d11)
            if (point3d9 == None):
                point3d9 = point3d17;
            point3d10 = MathHelper.getIntersectionPoint(point3d20, point3d18, point3d8, point3d12)
            if (point3d10 == None):
                point3d10 = point3d18;
        else:
            point3d7 = point3d17;
            point3d8 = point3d18;
            point3d9 = point3d17;
            point3d10 = point3d18;
            point3d11 = point3d17;
            point3d12 = point3d18;
        point3d = MathHelper.distanceBearingPoint(self.ptHRP, num2, metres3 / 2);
        self.ptsOISL.append(self.ptsOCSL[0]);
        self.ptsOISL.append(point3d7.smethod_167(self.ptHRP.get_Z() + self.tang * MathHelper.calcDistance(point3d, point3d14)));
        self.ptsOISR.append(self.ptsOCSR[0]);
        self.ptsOISR.append(point3d8.smethod_167(self.ptHRP.get_Z() + self.tang * MathHelper.calcDistance(point3d, point3d14)));
        self.ptsLevelOCSL.append(point3d19.smethod_167(self.ptHRP.get_Z() + (metres - metres1)));
        self.ptsLevelOCSL.append(point3d9.smethod_167(self.ptHRP.get_Z() + (metres - metres1)));
        self.ptsLevelOCSR.append(point3d20.smethod_167(self.ptHRP.get_Z() + (metres - metres1)));
        self.ptsLevelOCSR.append(point3d10.smethod_167(self.ptHRP.get_Z() + (metres - metres1)));
        z = self.ptHRP.get_Z() + metres - 30;
        point3d21 = MathHelper.distanceBearingPoint(self.ptHRP, num1, 750);
        point3d22 = MathHelper.distanceBearingPoint(self.ptMAPt, num3 - 1.5707963267949, metres5);
        point3d3, point3d4, point3d5, point3d16 = MathHelper.smethod_89(point3d22, 0, self.ptHRP, 750);
        point3d15 = MathHelper.getIntersectionPoint(point3d22, point3d16, point3d21, MathHelper.distanceBearingPoint(point3d21, num1 - 1.5707963267949, 100));
        self.ptsLevelOISL.append(point3d21.smethod_167(z));
        self.ptsLevelOISL.append(point3d15.smethod_167(z));
        self.ptsLevelOISL.append(point3d16.smethod_167(z));
        self.ptsLevelOISL.append(point3d22.smethod_167(z));
        if (point3d9 == point3d17):
            self.ptsLevelOISL.append(point3d17.smethod_167(z));
        elif (not MathHelper.smethod_119(point3d9, point3d18, point3d17)):
            point3d1 = MathHelper.getIntersectionPoint(point3d18, point3d17, point3d7, point3d11);
            self.ptsLevelOISL.append(point3d1.smethod_167(z))
        else:
            self.ptsLevelOISL.append(point3d17.smethod_167(z));
            self.ptsLevelOISL.append(point3d9.smethod_167(z));
        point3d21 = MathHelper.distanceBearingPoint(self.ptHRP, num1, 750);
        point3d22 = MathHelper.distanceBearingPoint(self.ptMAPt, num3 + 1.5707963267949, metres5);
        point3d3, point3d16, point3d5, point3d6 = MathHelper.smethod_89(point3d22, 0, self.ptHRP, 750);
        point3d15 = MathHelper.getIntersectionPoint(point3d22, point3d16, point3d21, MathHelper.distanceBearingPoint(point3d21, num1 - 1.5707963267949, 100));
        self.ptsLevelOISR.append(point3d21.smethod_167(z));
        self.ptsLevelOISR.append(point3d15.smethod_167(z));
        self.ptsLevelOISR.append(point3d16.smethod_167(z));
        self.ptsLevelOISR.append(point3d22.smethod_167(z));
        if (point3d10 == point3d18):
            self.ptsLevelOISR.append(point3d18.smethod_167(z));
        elif (not MathHelper.smethod_119(point3d10, point3d18, point3d17)):
            point3d1 = MathHelper.getIntersectionPoint(point3d18, point3d17, point3d8, point3d12);
            self.ptsLevelOISR.append(point3d1.smethod_167(z));
        else:
            self.ptsLevelOISR.append(point3d18.smethod_167(z));
            self.ptsLevelOISR.append(point3d10.smethod_167(z));
        self.selectionArea.append(self.ptsLevelOCSL[0]);
        if (MathHelper.smethod_115(self.ptsLevelOCSL[1], self.ptsLevelOISR[3], self.ptsLevelOISL[3])):
            self.selectionArea.append(self.ptsLevelOCSL[1]);
        self.selectionArea.append(self.ptsLevelOISL[4]);
        self.selectionArea.append(self.ptsLevelOISL[3]);
        self.selectionArea.append(self.ptsLevelOISL[2]);
        self.selectionArea.append(self.ptsLevelOISL[1]);
        self.selectionArea.append(self.ptsLevelOISR[1]);
        self.selectionArea.append(self.ptsLevelOISR[2]);
        self.selectionArea.append(self.ptsLevelOISR[3]);
        self.selectionArea.append(self.ptsLevelOISR[4]);
        if (MathHelper.smethod_115(self.ptsLevelOCSR[1], self.ptsLevelOISR[3], self.ptsLevelOISL[3])):
            self.selectionArea.append(self.ptsLevelOCSR[1]);
        self.selectionArea.append(self.ptsLevelOCSR[0]);
#         self.selectionArea.smethod_146();
        self.ptsOIS.append(self.ptsOISL[0]);
        self.ptsOIS.append(self.ptsOISL[1]);
        self.ptsOIS.append(self.ptsOCSL[len(self.ptsOCSL) - 1]);
        self.ptsOIS.append(self.ptsOCSR[len(self.ptsOCSR) - 1]);
        self.ptsOIS.append(self.ptsOISR[1]);
        self.ptsOIS.append(self.ptsOISR[0]);
#         self.ptsOIS.smethod_146();
        for point in self.ptsOCSL:
            self.ptsOCS.append(point)
        for j in range(len(self.ptsOCSR) - 1, -1, -1):
            self.ptsOCS.append(self.ptsOCSR[j])
#         self.ptsOCS.smethod_146();
        self.ptsLevelOCS.append(self.ptsLevelOCSL[0]);
        self.ptsLevelOCS.append(self.ptsLevelOCSL[1]);
        self.ptsLevelOCS.append(self.ptsOISL[1]);
        self.ptsLevelOCS.append(self.ptsOCSL[len(self.ptsOCSL) - 1]);
        self.ptsLevelOCS.append(self.ptsOCSR[len(self.ptsOCSL) - 1]);
        self.ptsLevelOCS.append(self.ptsOISR[1]);
        self.ptsLevelOCS.append(self.ptsLevelOCSR[1]);
        self.ptsLevelOCS.append(self.ptsLevelOCSR[0]);
#         self.ptsLevelOCS.smethod_146();
        self.ptsLevelOIS.append(self.ptsLevelOISL[3]);
        self.ptsLevelOIS.append(self.ptsLevelOISL[2]);
        self.ptsLevelOIS.append(self.ptHRP);
        self.ptsLevelOIS.append(self.ptsLevelOISR[2]);
        self.ptsLevelOIS.append(self.ptsLevelOISR[3]);

    def get_Cancelled(self):
        return self.cancelled
    Canceled = property(get_Cancelled, None, None, None)
 
    def get_SelectionArea(self):
        return self.selectionArea;
    SelectionArea = property(get_SelectionArea, None, None, None)
 
 
    def imethod_0(self, obstacle_0):
        criticalObstacleType = CriticalObstacleType.No
        if (MathHelper.pointInPolygon(self.ptsOIS, obstacle_0.Position, obstacle_0.Tolerance)):
            point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.track + 1.5707963267949, 100);
            point3d = MathHelper.getIntersectionPoint(obstacle_0.Position, point3d1, self.ptMAPt, self.ptHRP);
            num1 = MathHelper.calcDistance(self.ptStart, obstacle_0.Position);
            num1 = 0.0001 if num1 <= obstacle_0.Tolerance else num1 - obstacle_0.Tolerance
            z = num1 * self.tang + self.ptHRP.get_Z()
            num = PinsSurfaceType.PinsSurfaceType_OIS if not MathHelper.pointInPolygon(self.ptsOCS, obstacle_0.Position, obstacle_0.Tolerance) else PinsSurfaceType.PinsSurfaceType_OCS
        elif (not MathHelper.pointInPolygon(self.ptsLevelOCS, obstacle_0.Position, obstacle_0.Tolerance)):
            z = self.ptsLevelOIS[0].get_Z();
            num = PinsSurfaceType.PinsSurfaceType_LevelOIS
            if (not MathHelper.pointInPolygon(self.ptsLevelOIS, obstacle_0.Position, obstacle_0.Tolerance) and MathHelper.calcDistance(self.ptHRP, obstacle_0.Position) - obstacle_0.Tolerance > 750):
                return;
        else:
            z = self.ptsLevelOCS[0].get_Z();
            num = PinsSurfaceType.PinsSurfaceType_LevelOCS
        position = obstacle_0.Position;
        z1 = position.get_Z() + obstacle_0.Trees - z;
        if (z1 > 0):
            criticalObstacleType = CriticalObstacleType.Yes;
        return [z, z1, criticalObstacleType, num]
 
    def imethod_1(self, layers):
        resultLayer = AcadHelper.createVectorLayer("Pins Visual Segment Approach Direct 2D")
        linesList = []
        point3dCollection = []
        for point in self.ptsOCSL:
            point3dCollection.append(point)
        for j in range(len(self.ptsOCSR) - 1, -1, -1):
            point3dCollection.append(self.ptsOCSR[j]);
        point3dCollection.append(self.ptsOCSL[0])
        polylineOCS = (point3dCollection, [("surface", PinsSurfaceType.PinsSurfaceType_OCS)]);
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, point3dCollection, False, {"Surface":PinsSurfaceType.PinsSurfaceType_OCS})

        linesList.append(polylineOCS)
         
        ocsPoints = []
        for point in self.ptsOCSL:
            ocsPoints.append(point)
        ocsPoints.append(self.ptsOISL[1])
        ocsPoints.append(self.ptsOISL[0])
        polylineOCS1 = (ocsPoints, [("surface", PinsSurfaceType.PinsSurfaceType_OIS)])
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, ocsPoints, False, {"Surface":PinsSurfaceType.PinsSurfaceType_OIS})

        linesList.append(polylineOCS1)
         
        oCSRPoints = []
        for point in self.ptsOCSR:
            oCSRPoints.append(point)
        oCSRPoints.append(self.ptsOISR[1])
        oCSRPoints.append(self.ptsOISR[0])
        polyline = (oCSRPoints, [("surface", PinsSurfaceType.PinsSurfaceType_OIS)])
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, oCSRPoints, False, {"Surface":PinsSurfaceType.PinsSurfaceType_OIS})

        linesList.append(polyline)
         
        point3dCollection = Polyline()
        if (len(self.ptsLevelOISL) == 6):
            point3dCollection.Add(self.ptsLevelOISL[5])
        point3dCollection.Add(self.ptsLevelOISL[4])
        point3dCollection.Add(self.ptsLevelOISL[3]);
        point3dCollection.Add(self.ptsLevelOISL[2]);
        point3dCollection.Add(self.ptsLevelOISR[2]);
        point3dCollection.Add(self.ptsLevelOISR[3]);
        point3dCollection.Add(self.ptsLevelOISR[4]);
        if (len(self.ptsLevelOISR) == 6):
            point3dCollection.Add(self.ptsLevelOISR[5]);
        point3dCollection.Add(self.ptsOISR[1])
        point3dCollection.Add(self.ptsOISR[0])
        point3dCollection.Add(self.ptsOISL[0])
        point3dCollection.Add(self.ptsOISL[1])
        point3dCollection.Closed = True
        if (len(self.ptsLevelOISL) != 6):
            point3dCollection.SetBulgeAt(2, MathHelper.smethod_60(self.ptsLevelOISL[2], self.ptsLevelOISL[0], self.ptsLevelOISR[2]))
        else:
            point3dCollection.SetBulgeAt(3, MathHelper.smethod_60(self.ptsLevelOISL[2], self.ptsLevelOISL[0], self.ptsLevelOISR[2]))
        pointList = point3dCollection.getQgsPointList()
        polyline = (pointList, [("surface", PinsSurfaceType.PinsSurfaceType_LevelOIS)])
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, pointList, False, {"Surface":PinsSurfaceType.PinsSurfaceType_LevelOIS})

        linesList.append(polyline)
 
        point3dCollection = []
        point3dCollection.append(self.ptsLevelOCSL[0])
        point3dCollection.append(self.ptsLevelOCSL[1])
        point3dCollection.append(self.ptsOISL[1])
        point3dCollection.append(self.ptsOCSL[len(self.ptsOCSL) - 1])
        point3dCollection.append(self.ptsOCSR[len(self.ptsOCSR) - 1])
        point3dCollection.append(self.ptsOISR[1])
        point3dCollection.append(self.ptsLevelOCSR[1])
        point3dCollection.append(self.ptsLevelOCSR[0])
        point3dCollection.append(self.ptsLevelOCSL[0])
        polyline = (point3dCollection, [("surface", PinsSurfaceType.PinsSurfaceType_LevelOCS)])
        linesList.append(polyline)
        
#         polyline = (self.ptsOIS, [("surface", PinsSurfaceType.PinsSurfaceType_OIS)])
#         linesList.append(polyline)
# 
#         polyline = (self.ptsOCS, [("surface", PinsSurfaceType.PinsSurfaceType_OCS)])
#         linesList.append(polyline)
#         polyline = (self.ptsLevelOIS, [("surface", PinsSurfaceType.PinsSurfaceType_LevelOIS)])
#         linesList.append(polyline)
#         polyline = (self.ptsLevelOCS, [("surface", PinsSurfaceType.PinsSurfaceType_LevelOCS)])
#         linesList.append(polyline)

        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, point3dCollection, False, {"Surface":PinsSurfaceType.PinsSurfaceType_LevelOCS})
        layers.append(resultLayer)#QgisHelper.createPolylineLayer("Pins Visual Segment Approach Direct 2D", linesList, [QgsField("surface", QVariant.String)]))
  
    def imethod_2(self, layers):
        resultLayer = AcadHelper.createVectorLayer("Pins Visual Segment Approach Direct 3D")
        linesList = []
        if (len(self.ptsOCSL) != 2):
            face = [self.ptsOCSL[0], self.ptsOCSL[1], self.ptsOCSR[1], self.ptsOCSR[0], self.ptsOCSL[0]]
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, face)

            linesList.append((face, []))
            face = [self.ptsOCSL[1], self.ptsOCSL[2], self.ptsOCSR[2], self.ptsOCSR[1], self.ptsOCSL[1]]
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, face)
            linesList.append((face, []))
            face = [self.ptsOCSL[0], self.ptsOCSL[1], self.ptsOCSL[2], self.ptsOISL[1], self.ptsOCSL[0]]
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, face)
            linesList.append((face, []))
            face = [self.ptsOCSR[0], self.ptsOCSR[1], self.ptsOCSR[2], self.ptsOISR[1], self.ptsOCSR[0]]
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, face)
            linesList.append((face, []))
        else:
            face = [self.ptsOCSL[0], self.ptsOCSL[1], self.ptsOCSR[1], self.ptsOCSR[0], self.ptsOCSL[0]]
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, face)
            linesList.append((face, []))
            face = [self.ptsOCSL[0], self.ptsOCSL[1], self.ptsOISL[1], self.ptsOISL[0], self.ptsOCSL[0]]
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, face)
            linesList.append((face, []))
            face = [self.ptsOCSR[0], self.ptsOCSR[1], self.ptsOISR[1], self.ptsOISR[0], self.ptsOCSR[0]]
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, face)
            linesList.append((face, []))
        point3dCollection = Polyline()
        if (len(self.ptsLevelOISL) == 6):
            point3dCollection.Add(self.ptsLevelOISL[5]);
        point3dCollection.Add(self.ptsLevelOISL[4]);
        point3dCollection.Add(self.ptsLevelOISL[3]);
        point3dCollection.Add(self.ptsLevelOISL[2]);
        point3dCollection.Add(self.ptsLevelOISR[2]);
        point3dCollection.Add(self.ptsLevelOISR[3]);
        point3dCollection.Add(self.ptsLevelOISR[4]);
        if (len(self.ptsLevelOISR) == 6):
            point3dCollection.Add(self.ptsLevelOISR[5])
        point3dCollection.Add(self.ptsOISR[1]);
        point3dCollection.Add(self.ptsOISR[0]);
        point3dCollection.Add(self.ptsOISL[0]);
        point3dCollection.Add(self.ptsOISL[1]);
        point3dCollection.Closed = True
        if (len(self.ptsLevelOISL) != 6):
            point3dCollection.SetBulgeAt(2, MathHelper.smethod_60(self.ptsLevelOISL[2], self.ptsLevelOISL[0], self.ptsLevelOISR[2]));
        else:
            point3dCollection.SetBulgeAt(3, MathHelper.smethod_60(self.ptsLevelOISL[2], self.ptsLevelOISL[0], self.ptsLevelOISR[2]));
        pointList = point3dCollection.getQgsPointList()
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, PolylineArea(pointList))
        linesList.append((pointList, []))
        #item = self.ptsLevelOISL[0];
        #polyline.set_Elevation(item.get_Z());
        point3dCollection = []
        point3dCollection.append(self.ptsLevelOCSL[0]);
        point3dCollection.append(self.ptsLevelOCSL[1]);
        point3dCollection.append(self.ptsOISL[1]);
        point3dCollection.append(self.ptsOCSL[len(self.ptsOCSL) - 1])
        point3dCollection.append(self.ptsOCSR[len(self.ptsOCSR) - 1]);
        point3dCollection.append(self.ptsOISR[1])
        point3dCollection.append(self.ptsLevelOCSR[1]);
        point3dCollection.append(self.ptsLevelOCSR[0]);
        point3dCollection.append(self.ptsLevelOCSL[0]);
        linesList.append((point3dCollection, []))


        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, point3dCollection, False, {"Surface":PinsSurfaceType.PinsSurfaceType_LevelOCS})

        layers.append(resultLayer)#QgisHelper.createPolylineLayer("Pins Visual Segment Approach Direct 3D", linesList, []))

  
class PinSVisualSegmentAppManouvering(IPinSVisualSegmentApp):
    
    def __init__(self, pinSVisualSegmentApp_0):
        self.RADIUS = 750;
      
        self.OCS = 0
      
        self.OIS = 1
      
        self.LEVEL_OCS = 2
      
        self.poaLevelOCS = PrimaryObstacleArea()
      
        self.poaOIS = PrimaryObstacleArea()
      
        self.poaOCS = PrimaryObstacleArea()
      
        self.paLevelOCS = PolylineArea()
      
        self.paOIS = PolylineArea()
      
        self.paOCS = PolylineArea()
      
        self.selectionArea = []
      
        self.ptsOCSL = []
      
        self.ptsOCSR = []
      
        self.ptHRP = Point3D()
      
        self.ptMAPt = Point3D()
      
        self.track = 0.0
      
        self.tang = 0.0
      
        self.elevOIS = 0.0
      
        self.elevLevelOCS = 0.0
      
        self.cancelled = False

        #pinSVisualSegmentApp_0 = PinSVisualSegmentAppDlg()
        
        self.ptMAPt = pinSVisualSegmentApp_0.pnlMAPt.getPoint3D()
        self.ptHRP = pinSVisualSegmentApp_0.pnlHRP.getPoint3D()
        try:
            self.track = MathHelper.smethod_4(Unit.ConvertDegToRad(float(pinSVisualSegmentApp_0.parametersPanel.txtApproachSurfaceTrack.Value) + 180))
        except ValueError:
            raise UserWarning, "Approach Surface Track is invalid!"
        num = MathHelper.getBearing(self.ptMAPt, self.ptHRP);
        num1 = num - 1.5707963267949
        num2 = num + 1.5707963267949
        num3 = MathHelper.getBearing(self.ptHRP, self.ptMAPt)
        try:
            metres = pinSVisualSegmentApp_0.parametersPanel.txtMOC.Value.Metres
        except ValueError:
            raise UserWarning, "MOC is invalid!"
        try:
            metres1 = float(pinSVisualSegmentApp_0.parametersPanel.txtHCH.Value)
        except ValueError:
            raise UserWarning, "Crossing Height [HCH] is invalid!"
        altitude = pinSVisualSegmentApp_0.pnlOCAH.method_3(Altitude(self.ptHRP.get_Z()))
        metres2 = altitude.Metres
        if (metres2 < 90):
            raise UserWarning, Messages.ERR_INSUFFICIENT_MINIMUM_ALTITUDE
        if (metres2 < metres):
            raise UserWarning, Messages.ERR_INSUFFICIENT_MINIMUM_ALTITUDE
        altitude1 = pinSVisualSegmentApp_0.pnlOCAH.method_2(Altitude(self.ptHRP.get_Z()))
        metres3 = altitude1.Metres;
        try:
            value = pinSVisualSegmentApp_0.parametersPanel.txtVSDG.Value
        except ValueError:
            raise UserWarning, "Visual Segment Design Gradient [VSDG] is invalid!"
        num4 = (metres2 - metres1) / math.tan(Unit.ConvertDegToRad(value.Degrees));
        self.tang = (metres2 - metres) / num4;
        num5 = 741;
        num6 = 1482;
        if (metres2 > 183):
            num7 = math.trunc((metres2 - 183) / 30)
            if ((metres2 - 183) % 30 > 0):
                num7 = num7 + 1;
            num6 = num6 + num7 * 185;
        num8 = 50;
        if (metres2 > 183 and metres2 <= 304):
            num9 = math.trunc((metres2 - 183) / 30);
            if ((metres2 - 183) % 30 > 0):
                num9 = num9 + 1;
            num8 = num8 - num9 * 5;
            if (num8 < 30):
                num8 = 30;
        elif (metres2 > 304):
            num8 = 30;
        num10 = Unit.ConvertDegToRad(num8);
        num11 = MathHelper.calcDistance(self.ptMAPt, self.ptHRP);
        if (num11 < 1000):
            eRRINSUFFICIENTSEGMENTLENGTHMAPTHRP = Messages.ERR_INSUFFICIENT_SEGMENT_LENGTH_MAPT_HRP
            distance = Distance(num6)
            raise UserWarning, eRRINSUFFICIENTSEGMENTLENGTHMAPTHRP % distance.Metres
        listTurn = []
        num12 = MathHelper.smethod_77(num, self.track, AngleUnits.Radians, listTurn)
        turnDirection = listTurn[0]
        if (num12 + num10 >= 3.14159265358979):
            eRRPINSCCHGLARGEUSEDIRECT = unicode(Messages.ERR_PINS_CCHG_LARGE_USE_DIRECT, "utf-8")
            num13 = Unit.smethod_1(3.14159265358979 - num10);
            raise UserWarning, eRRPINSCCHGLARGEUSEDIRECT % num13
#         MathHelper.smethod_76(Unit.smethod_1(num3), MathHelper.smethod_3(pinSVisualSegmentApp_0.pnlTrackTo.Value + 180), AngleUnits.Degrees);
        if (num12 > 30):
            raise UserWarning, Messages.ERR_PINS_CCHG_MAPT_GREATER_THAN_30
        num14 = MathHelper.smethod_62(TurnDirection.Right, 3.14159265358979, AngleUnits.Radians);
        self.paLevelOCS.method_3(MathHelper.distanceBearingPoint(self.ptHRP, num1, num5), num14);
        self.paLevelOCS.method_1(MathHelper.distanceBearingPoint(self.ptHRP, num2, num5));
        self.paLevelOCS.method_3(MathHelper.distanceBearingPoint(self.ptMAPt, num2, num5), num14);
        self.paLevelOCS.method_1(MathHelper.distanceBearingPoint(self.ptMAPt, num1, num5));
        self.poaLevelOCS = PrimaryObstacleArea(self.paLevelOCS)
        self.elevLevelOCS = metres3 - 76;
        self.paOIS.method_1(self.ptMAPt);
        if (turnDirection == TurnDirection.Nothing or MathHelper.smethod_99(num12, 0, 0.1)):
            point3d = MathHelper.distanceBearingPoint(self.ptHRP, num - num10, num6);
            point3d1 = MathHelper.distanceBearingPoint(self.ptHRP, num + num10, num6);
            if (pinSVisualSegmentApp_0.parametersPanel.chbLeftFlyOverProhibited.Checked):
                point3d = MathHelper.distanceBearingPoint(self.ptHRP, num, num6);
            elif (pinSVisualSegmentApp_0.parametersPanel.chbRightFlyOverProhibited.Checked):
                point3d1 = MathHelper.distanceBearingPoint(self.ptHRP, num, num6);
            self.paOIS.method_3(point3d, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, self.ptHRP));
            self.paOIS.method_1(point3d1);
        else:
            if num6 > num11:
                point3d2 = None
                point3d3 = None
            else:  
                point3d2 = MathHelper.distanceBearingPoint(self.ptHRP, num - math.fabs(math.asin(num6 / num11)) - 1.5707963267949, num6);
                point3d3 = MathHelper.distanceBearingPoint(self.ptHRP, num + math.fabs(math.asin(num6 / num11)) + 1.5707963267949, num6);
            if (num12 < num10 and not pinSVisualSegmentApp_0.parametersPanel.chbLeftFlyOverProhibited.Checked and not pinSVisualSegmentApp_0.parametersPanel.chbRightFlyOverProhibited.Checked):
                point3d = MathHelper.distanceBearingPoint(self.ptHRP, self.track - num10, num6);
                point3d1 = MathHelper.distanceBearingPoint(self.ptHRP, self.track + num10, num6);
                if (MathHelper.smethod_119(point3d2, self.ptHRP, point3d)):
                    point3d = point3d2;
                if (MathHelper.smethod_115(point3d3, self.ptHRP, point3d1)):
                    point3d1 = point3d3;
                self.paOIS.method_3(point3d, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, self.ptHRP));
                self.paOIS.method_1(point3d1);
                self.paOIS.method_1(self.ptMAPt);
            elif (turnDirection != TurnDirection.Left):
                point3d1 = MathHelper.distanceBearingPoint(self.ptHRP, self.track + num10, num6);
                if (MathHelper.smethod_115(point3d3, self.ptHRP, point3d1)):
                    point3d1 = point3d3;
                if (not pinSVisualSegmentApp_0.parametersPanel.chbRightFlyOverProhibited.Checked):
                    num15 = Unit.ConvertDegToRad(30);
                    point3d = MathHelper.distanceBearingPoint(self.ptHRP, self.track - num10, num6) if num12 - num10 <= num15 else MathHelper.distanceBearingPoint(self.ptHRP, num + num15, num6)
                    if (MathHelper.smethod_119(point3d, self.ptMAPt, self.ptHRP)):
                        self.paOIS.method_1(self.ptHRP);
                    self.paOIS.method_3(point3d, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, self.ptHRP));
                    self.paOIS.method_1(point3d1);
                    self.paOIS.method_1(self.ptMAPt);
                else:
                    point3d = MathHelper.distanceBearingPoint(self.ptHRP, self.track, num6);
                    self.paOIS.method_1(self.ptHRP);
                    if (not MathHelper.smethod_119(point3d3, self.ptHRP, point3d)):
                        self.paOIS.method_1(point3d);
                    else:
                        self.paOIS.method_3(point3d, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, self.ptHRP));
                        self.paOIS.method_1(point3d1);
                    self.paOIS.method_1(self.ptMAPt);
            else:
                point3d = MathHelper.distanceBearingPoint(self.ptHRP, self.track - num10, num6);
                if (MathHelper.smethod_119(point3d2, self.ptHRP, point3d)):
                    point3d = point3d2;
                if (not pinSVisualSegmentApp_0.parametersPanel.chbLeftFlyOverProhibited.Checked):
                    num16 = Unit.ConvertDegToRad(30)
                    point3d1 = MathHelper.distanceBearingPoint(self.ptHRP, self.track + num10, num6) if num12 - num10 <= num16 else MathHelper.distanceBearingPoint(self.ptHRP, num - num16, num6)
                    self.paOIS.method_3(point3d, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, self.ptHRP));
                    self.paOIS.method_1(point3d1);
                    if (MathHelper.smethod_115(point3d1, self.ptMAPt, self.ptHRP)):
                        self.paOIS.method_1(self.ptHRP);
                    self.paOIS.method_1(self.ptMAPt);
                else:
                    point3d1 = MathHelper.distanceBearingPoint(self.ptHRP, self.track, num6);
                    if (MathHelper.smethod_115(point3d2, self.ptHRP, point3d1)):
                        self.paOIS.method_3(point3d, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, self.ptHRP));
                    self.paOIS.method_1(point3d1);
                    self.paOIS.method_1(self.ptHRP);
                    self.paOIS.method_1(self.ptMAPt);

        self.paOIS.offsetCurve(num5)
        self.poaOIS = PrimaryObstacleArea(self.paOIS)
        self.elevOIS = self.ptHRP.get_Z() + max([metres2 / 2 - 46, 46]);
        try:
            metres5 = pinSVisualSegmentApp_0.parametersPanel.txtHSAL.Value.Metres
        except ValueError:
            raise UserWarning, "Safety Area Length is invalid!"
        try:
            metres4 = pinSVisualSegmentApp_0.parametersPanel.txtHSAW.Value.Metres
        except ValueError:
            raise UserWarning, "Safety Area Width is invalid!"
        num = self.track
        point3d4 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(self.ptHRP, num, metres5 / 2), num - 1.5707963267949, metres4 / 2);
        point3d5 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(self.ptHRP, num, metres5 / 2), num + 1.5707963267949, metres4 / 2);
        num17 = math.atan(0.1) if pinSVisualSegmentApp_0.parametersPanel.cmbApproachType.SelectedIndex == 0 else math.atan(0.15)
        num18 = 152 / self.tang;
        num19 = (120 - metres4 / 2) / math.tan(num17);
        self.ptsOCSL.append(point3d4);
        self.ptsOCSL.append(MathHelper.distanceBearingPoint(point3d4, num - num17, num19 * math.cos(num17)).smethod_167(self.ptHRP.get_Z() + num19 * self.tang));
        self.ptsOCSL.append(MathHelper.distanceBearingPoint(self.ptsOCSL[1], num, num18 - num19).smethod_167(self.ptHRP.get_Z() + 152));
        self.ptsOCSR.append(point3d5);
        self.ptsOCSR.append(MathHelper.distanceBearingPoint(point3d5, num + num17, num19 * math.cos(num17)).smethod_167(self.ptHRP.get_Z() + num19 * self.tang));
        self.ptsOCSR.append(MathHelper.distanceBearingPoint(self.ptsOCSR[1], num, num18 - num19).smethod_167(self.ptHRP.get_Z() + 152));
        for point in self.ptsOCSL:
            self.paOCS.method_1(point)
        for j in range(len(self.ptsOCSR) - 1, -1, -1):
            self.paOCS.method_1(self.ptsOCSR[j])
        self.paOCS.method_10();
        self.poaOCS = PrimaryObstacleArea(self.paOCS)
        self.selectionArea = (PrimaryObstacleArea(self.paOIS)).SelectionArea
   
    def get_Cancelled(self):
        return self.cancelled
    Cancelled = property(get_Cancelled, None, None, None)
   
    def get_SelectionArea(self):
        return self.selectionArea;
    SelectionArea = property(get_SelectionArea, None, None, None)
    
   
    def imethod_0(self, obstacle_0):
        criticalObstacleType = CriticalObstacleType.No;
        if (self.poaOIS.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
            z = self.elevOIS;
            num = PinsSurfaceType.PinsSurfaceType_OIS
            if (self.poaOCS.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
                point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.track, 100);
                point3d = MathHelper.getIntersectionPoint(obstacle_0.Position, point3d1, self.ptsOCSL[0], self.ptsOCSR[0])
                num1 = max([MathHelper.calcDistance(point3d, obstacle_0.Position) - obstacle_0.Tolerance, 0])
                z = num1 * self.tang + self.ptHRP.get_Z()
                num = PinsSurfaceType.PinsSurfaceType_OCS
            elif (self.poaLevelOCS.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
                z = self.elevLevelOCS
                num = PinsSurfaceType.PinsSurfaceType_LevelOCS
            position = obstacle_0.Position
            z1 = position.get_Z() + obstacle_0.Trees - z
            if (z1 > 0):
                criticalObstacleType = CriticalObstacleType.Yes;
            return [z, z1, criticalObstacleType, num]
   
    def imethod_1(self, layers):
        resultLayer = AcadHelper.createVectorLayer("Pins Visual Segment Approach Manouvering 2D")
        linesList = []
        pointList = self.paLevelOCS.method_14_closed()
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.paLevelOCS, True, {"Surface":PinsSurfaceType.PinsSurfaceType_LevelOCS})

        polyline = (pointList, [("surface", PinsSurfaceType.PinsSurfaceType_LevelOCS)])
        linesList.append(polyline)
        pointList = self.paOIS.method_14_closed()
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.paOIS, True, {"Surface":PinsSurfaceType.PinsSurfaceType_OIS})

        polyline = (pointList, [("surface", PinsSurfaceType.PinsSurfaceType_OIS)])
        linesList.append(polyline)
        pointList = self.paOCS.method_14_closed()
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.paOCS, True, {"Surface":PinsSurfaceType.PinsSurfaceType_OCS})

        polyline = (pointList, [("surface", PinsSurfaceType.PinsSurfaceType_OCS)])
        linesList.append(polyline)
        layers.append(resultLayer)#QgisHelper.createPolylineLayer("Pins Visual Segment Approach Manouvering 2D", linesList, [QgsField("surface", QVariant.String)]))
   
    def imethod_2(self, layers):
        resultLayer = AcadHelper.createVectorLayer("Pins Visual Segment Approach Manouvering 3D")
        linesList = []
        pointList = self.paLevelOCS.method_14_closed()
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.paLevelOCS, True, {"Surface":PinsSurfaceType.PinsSurfaceType_LevelOCS})

        polyline = (pointList, [("surface", PinsSurfaceType.PinsSurfaceType_LevelOCS)])
        linesList.append(polyline)
        pointList = self.paOIS.method_14_closed()
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.paOIS, True, {"Surface":PinsSurfaceType.PinsSurfaceType_OIS})

        polyline = (pointList, [("surface", PinsSurfaceType.PinsSurfaceType_OIS)])
        linesList.append(polyline)
        pointList = self.paOCS.method_14_closed()
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.paOCS, True, {"Surface":PinsSurfaceType.PinsSurfaceType_OCS})

        polyline = (pointList, [("surface", PinsSurfaceType.PinsSurfaceType_OCS)])
        linesList.append(polyline)
        layers.append(resultLayer)#QgisHelper.createPolylineLayer("Pins Visual Segment Approach Manouvering 3D", linesList, [QgsField("surface", QVariant.String)]))
#         Polyline polyline = AcadHelper.smethod_131(self.paLevelOCS);
#         polyline.set_Closed(true);
#         polyline.set_Elevation(self.elevLevelOCS);
#         dBObjectCollection.append(polyline);
#         polyline = AcadHelper.smethod_131(self.paOIS);
#         polyline.set_Closed(true);
#         polyline.set_Elevation(self.elevOIS);
#         dBObjectCollection.append(polyline);
#         for (int i = 1; i < self.ptsOCSL.get_Count(); i++):
#             Face face = new Face(self.ptsOCSL[i - 1), self.ptsOCSL[i), self.ptsOCSR[i), self.ptsOCSR[i - 1), true, true, true, true);
#             AcadHelper.smethod_18(transaction_0, blockTableRecord_0, face, string_0);

   
class PinSVisualSegmentAppObstacles(ObstacleTable):
    def __init__(self, surfacesList):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)
        self.surfaceType = SurfaceTypes.PinSVisualSegmentApp
         
#     private string title;
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        self.IndexSurfAltM = fixedColumnCount 
        self.IndexSurfAltFt = fixedColumnCount + 1
        self.IndexDifferenceM = fixedColumnCount + 2
        self.IndexDifferenceFt = fixedColumnCount + 3
        self.IndexCritical = fixedColumnCount + 4
        self.IndexSurface = fixedColumnCount + 5
         
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.SurfAltM,
                ObstacleTableColumnType.SurfAltFt,
                ObstacleTableColumnType.DifferenceM,
                ObstacleTableColumnType.DifferenceFt,
                ObstacleTableColumnType.Critical,
                ObstacleTableColumnType.Surface
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)
 
    def addObstacleToModel(self, obstacle, checkResult):
        ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
        row = self.source.rowCount() - 1
#         colCount = self.source.columnCount()
          
        item = QStandardItem(str(checkResult[0]))
        item.setData(checkResult[0])
        self.source.setItem(row, self.IndexSurfAltM, item)
          
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[0])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[0]))
        self.source.setItem(row, self.IndexSurfAltFt, item)
          
        item = QStandardItem(str(checkResult[1]))
        item.setData(checkResult[1])
        self.source.setItem(row, self.IndexDifferenceM, item)
          
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[1])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[1]))
        self.source.setItem(row, self.IndexDifferenceFt, item)
          
        item = QStandardItem(str(checkResult[2]))
        item.setData(checkResult[2])
        self.source.setItem(row, self.IndexCritical, item)
  
        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexSurface, item)
 
    def checkObstacle(self, obstacle_0):
        for surface in self.surfacesList:
            checkResult = surface.imethod_0(obstacle_0) 
            if checkResult != None:
                self.addObstacleToModel(obstacle_0, checkResult)
 
    def getExtentForLocate(self, sourceRow):
        surfaceType = self.source.item(sourceRow, self.IndexSurface).text()
        surfaceLayers = QgisHelper.getSurfaceLayers(self.surfaceType)
        rect = QgsRectangle()
        rect.setMinimal()
        for sfLayer in surfaceLayers:
            features = sfLayer.getFeatures()
            for feature in features:
                try:
                    surfaceString = feature.attribute("surface").toString()
                except KeyError:
                    break
                if surfaceString == surfaceType:
                    geom = feature.geometry()
                    rect.combineExtentWith(geom.boundingBox())
        return rect
    
