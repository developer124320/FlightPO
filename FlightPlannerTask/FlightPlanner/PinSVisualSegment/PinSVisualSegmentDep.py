# -*- coding: utf-8 -*-
'''
Created on Apr 6, 2015

@author: jin
'''
from PyQt4.QtGui import QDialog, QMessageBox, QStandardItem, QAbstractItemView,\
     QLineEdit, QComboBox, QFileDialog
from PyQt4.QtCore import QVariant, QCoreApplication, SIGNAL
from qgis.core import QgsField, QgsRectangle
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.PinSVisualSegment.ui_PinSVisualSegmentDepDlg import ui_PinSVisualSegmentDepDlg

from FlightPlanner.types import PinsVisualSegmentType, AltitudeUnits, PinsOperationType,\
        TurnDirection, AngleUnits, ConstructionType, AngleGradientSlopeUnits, \
        SurfaceTypes, Point3D, CriticalObstacleType, ObstacleTableColumnType, PinsSurfaceType
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, AngleGradientSlope
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.MCAHPanel import MCAHPanel
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.validations import Validations
from FlightPlanner.messages import Messages
from FlightPlanner.polylineArea import PolylineArea
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
import define
import math
class PinSVisualSegmentDepDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.ui = ui_PinSVisualSegmentDepDlg()
        self.ui.setupUi(self)
        self.surfaceType = SurfaceTypes.PinSVisualSegmentDep
        QgisHelper.matchingDialogSize(self, 700, 650)
        ''' UI State Initialize '''
#         self.ui.btnOpenData.setDisabled(True)
#         self.ui.btnSaveData.setDisabled(True)
        self.ui.btnExportResult.setDisabled(True)
        self.ui.btnEvaluate.setEnabled(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        
        self.pnlMCAH = MCAHPanel(self.ui.groupBox_20)
        self.pnlMCAH.lblMCAH.setText("Minimum (ft):")
        self.pnlMCAH.setValue(Altitude(500, AltitudeUnits.FT))
        self.ui.verticalLayout_5.insertWidget(4, self.pnlMCAH)
        self.ui.cmbSegmentType.Items = [PinsVisualSegmentType.Direct, PinsVisualSegmentType.Manoeuvring]
        self.ui.cmbDepartureType.Items = [PinsOperationType.DayOnly, PinsOperationType.DayNight]
        self.ui.cmbDepartureType.SelectedIndex = 1
#         self.ui.cmbMCAH.addItems([MCAHType.MCA, MCAHType.MCH])
        self.ui.cmbDepartureType.Visible = False
        self.ui.txtTakeOffSurfaceTrack.Visible = False
        self.ui.frame_Limitation.hide()        
        
        self.pnlHRP = PositionPanel(self.ui.grbIDF)
        self.pnlHRP.groupBox.setTitle("Heliport Reference point (HRP)")
        self.pnlHRP.btnCalculater.hide()
        self.pnlHRP.setObjectName("positionHRP")
        self.ui.verticalLayout_HRP.insertWidget(0, self.pnlHRP)
        self.connect(self.pnlHRP, SIGNAL("positionChanged"), self.initResultPanel)
        
        self.pnlIDF = PositionPanel(self.ui.grbIDF)
        self.pnlIDF.groupBox.setTitle("")
        self.pnlIDF.hideframe_Altitude()
        self.pnlIDF.setObjectName("positionIDF")
        self.pnlIDF.btnCalculater.hide()
        self.ui.verticalLayout_IDF.insertWidget(0, self.pnlIDF)
        self.connect(self.pnlIDF, SIGNAL("positionChanged"), self.initResultPanel)
        
        self.ui.cmbConstructionType.Items = [ConstructionType.Construct2D, ConstructionType.Construct3D]
        self.ui.tblObstacles.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblObstacles.setSortingEnabled(True)
        
        '''Event Handlers Connect'''
        self.ui.btnOpenData.clicked.connect(self.openData)
        self.ui.btnSaveData.clicked.connect(self.saveData)
        self.connect(self.ui.cmbSegmentType, SIGNAL("Event_0"), self.chbLeftTurnProhibited_Click)
        self.connect(self.ui.cmbDepartureType, SIGNAL("Event_0"), self.chbLeftTurnProhibited_Click)
        self.connect(self.ui.txtVSDG, SIGNAL("Event_0"), self.chbLeftTurnProhibited_Click)
        self.connect(self.ui.txtTakeOffSurfaceTrack, SIGNAL("Event_0"), self.chbLeftTurnProhibited_Click)
        # self.ui.btnCaptureSurfaceTrack.clicked.connect(self.method_39)
        self.ui.chbLeftTurnProhibited.clicked.connect(self.chbLeftTurnProhibited_Click)
        self.ui.chbRightTurnProhibited.clicked.connect(self.chbLeftTurnProhibited_Click)
        # self.ui.btnCaptureTrackFrom.clicked.connect(self.method_37)
        self.pnlIDF.txtPointX.textChanged.connect(self.chbLeftTurnProhibited_Click)
        self.pnlIDF.txtPointY.textChanged.connect(self.chbLeftTurnProhibited_Click)
        self.pnlHRP.txtPointX.textChanged.connect(self.chbLeftTurnProhibited_Click)
        self.pnlHRP.txtPointY.textChanged.connect(self.chbLeftTurnProhibited_Click)
        self.pnlHRP.txtAltitudeM.textChanged.connect(self.chbLeftTurnProhibited_Click)
        self.ui.btnClose.clicked.connect(self.reject)
        self.ui.btnClose_2.clicked.connect(self.reject)
        self.ui.btnConstruct.clicked.connect(self.btnConstruct_Click)
        self.ui.btnEvaluate.clicked.connect(self.btnEvaluate_Click)
        self.ui.cmbSurface.currentIndexChanged.connect(self.cmbSurfaceChanged)
        self.ui.btnExportResult.clicked.connect(self.exportResult)
        self.obstaclesModel = None
        
        lstTextControls = self.ui.groupBox_20.findChildren(QLineEdit)
        for ctrl in lstTextControls:
            ctrl.textChanged.connect(self.initResultPanel)

        lstComboControls = self.ui.groupBox_20.findChildren(QComboBox)
        for ctrl in lstComboControls:
            ctrl.currentIndexChanged.connect(self.initResultPanel)

        
    def initResultPanel(self):
        self.ui.btnEvaluate.setEnabled(False)
        self.ui.btnExportResult.setEnabled(False)
        if self.obstaclesModel != None:
            self.obstaclesModel.clear()
        
    
    def cmbSurfaceChanged(self):
        if self.obstaclesModel == None:
            return
        if self.ui.cmbSurface.currentIndex() == 0 and self.ui.cmbSurface.currentText() == "All":
            self.obstaclesModel.setFilterFixedString("")
        else:
            self.obstaclesModel.setFilterFixedString(self.ui.cmbSurface.currentText())
        
    def btnEvaluate_Click(self):
        try:
            self.obstaclesModel = PinSVisualSegmentDepObstacles([self.pinSVisualSegmentDepManouvering])
            rnpArMapLayers = QgisHelper.getSurfaceLayers(SurfaceTypes.PinSVisualSegmentDep)
            self.obstaclesModel.loadObstacles(rnpArMapLayers)
            self.obstaclesModel.setLocateBtn(self.ui.btnLocate)
            self.ui.tblObstacles.setModel(self.obstaclesModel)
            self.obstaclesModel.setTableView(self.ui.tblObstacles)
            self.obstaclesModel.setHiddenColumns(self.ui.tblObstacles)
            self.ui.cmbSurface.setCurrentIndex(0)
            self.ui.tabControls.setCurrentIndex(1)
            
            self.ui.cmbSurface.clear()
            if self.ui.cmbSegmentType.SelectedIndex != 0:
                self.ui.cmbSurface.addItems(["All", PinsSurfaceType.PinsSurfaceType_LevelOIS, PinsSurfaceType.PinsSurfaceType_OCS])
            else:
                self.ui.cmbSurface.addItem("All")
                self.ui.cmbSurface.addItem(PinsSurfaceType.PinsSurfaceType_OIS)
            self.ui.btnExportResult.setEnabled(True)
#             raise ValueError, ""
        except UserWarning as e:
            QMessageBox.warning(self, "Information", e.message)
    def method_27(self, bool_0):
        if not self.pnlIDF.IsValid():
            raise UserWarning ,"IDF poisition value is incorrect. "
        # if (self.ui.cmbSegmentType.SelectedIndex == 0):
        #     self.valueValidate(self.ui.txtTrackFrom, "Track From")
            # self.valueValidate(self.ui.txtMOC, "Moc")
        if not self.pnlHRP.IsValid():
            raise UserWarning ,"HRP poisition value is incorrect."
        # self.valueValidate(self.ui.txtHSAL, "Safety Area Length")
        # self.valueValidate(self.ui.txtHSAW, "Safety Area Width")
        # if self.valueValidate(self.ui.txtVSDG, "VSDG") and float(self.ui.txtVSDG.text()) < 5:
        #     raise UserWarning ,Validations.VALUE_CANNOT_BE_SMALLER_THAN%5
        # if (self.ui.cmbSegmentType.SelectedIndex== 1):
        #     self.valueValidate(self.ui.txtTakeOffSurfaceTrack.txtRadialPlan, "TakeOffSurfaceTrack")
        self.valueValidate(self.pnlMCAH.txtMCAH, "Minimum")
        return True
 
    def method_29(self):
        self.ui.cmbSurface.clear()
    
    def method_32(self):
        self.ui.cmbDepartureType.Visible = self.ui.cmbSegmentType.SelectedIndex == 1
        self.ui.txtTakeOffSurfaceTrack.Visible = self.ui.cmbSegmentType.SelectedIndex == 1
        self.ui.txtTrackFrom.Visible = self.ui.cmbSegmentType.SelectedIndex == 0
        self.ui.txtMOC.Visible = self.ui.cmbSegmentType.SelectedIndex== 0
        self.ui.frame_Limitation.setVisible(self.ui.cmbSegmentType.SelectedIndex == 1)
    
    def method_33(self):
        turnDirection = []   
        try:     
            if (self.ui.cmbSegmentType.SelectedIndex== 1):
                point3d = self.pnlIDF.getPoint3D()
                point3d1 = self.pnlHRP.getPoint3D()
                num = Unit.smethod_1(MathHelper.getBearing(point3d, point3d1))
                num1 = self.smethod_17(self.ui.txtTakeOffSurfaceTrack.txtRadialPlan.numberBox)
                MathHelper.smethod_77(num, num1, AngleUnits.Degrees, turnDirection)
                
                if (turnDirection[0] == TurnDirection.Left):
                    pass
#                     self.ui.chbLeftTurnProhibited.setVisible(False)
#                     self.ui.chbRightTurnProhibited.setVisible(True)
                elif (turnDirection[0] != TurnDirection.Right):
#                     self.ui.chbLeftTurnProhibited.setVisible(True)
#                     self.ui.chbRightTurnProhibited.setVisible(True)
                    if (self.ui.chbLeftTurnProhibited.isChecked() and self.ui.chbRightTurnProhibited.isChecked()):
                        self.ui.chbRightTurnProhibited.setChecked(False)
                else:
                    pass
#                     self.ui.chbRightTurnProhibited.setVisible(False)
#                     self.ui.chbLeftTurnProhibited.setVisible(True)   
        except:
            pass          

    # def method_37(self):
    #     CaptureBearingTrackFrom = CaptureBearingTool(define._canvas, self.ui.txtTrackFrom)
    #     define._canvas.setMapTool(CaptureBearingTrackFrom)
    # def method_39(self):
    #     CaptureBearingSurfaceTrack = CaptureBearingTool(define._canvas, self.ui.txtTakeOffSurfaceTrack)
    #     define._canvas.setMapTool(CaptureBearingSurfaceTrack)
    def chbLeftTurnProhibited_Click(self):
        sender = self.sender() 
        if sender == self.ui.cmbSegmentType:
            self.method_32()
        elif (sender == self.pnlIDF.txtPointX or sender == self.pnlIDF.txtPointY):
            self.method_33()
        elif (sender == self.pnlHRP.txtPointX or sender == self.pnlHRP.txtPointY or sender == self.pnlHRP.txtAltitudeM):
            self.method_33()
        elif (sender == self.ui.txtTakeOffSurfaceTrack):
            self.method_33()
        elif ((sender == self.ui.chbLeftTurnProhibited or sender == self.ui.chbRightTurnProhibited) and self.ui.cmbSegmentType.SelectedIndex == 1):
            if (sender == self.ui.chbLeftTurnProhibited):
                if (self.ui.chbRightTurnProhibited.isVisible()):
                    self.ui.chbRightTurnProhibited.setChecked(False)
            elif (sender == self.ui.chbRightTurnProhibited and self.ui.chbLeftTurnProhibited.isVisible()):
                self.ui.chbLeftTurnProhibited.setChecked(False)
        self.method_29()
    def smethod_17(self, txtBox):
        try:
            value1 = float(txtBox.text())
            return value1
        except:
            return 0

    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        try:
            self.method_27(True)
            if (self.ui.cmbSegmentType.SelectedIndex != 0):
                self.pinSVisualSegmentDepManouvering = PinSVisualSegmentDepManouvering(self)
            else:
                self.pinSVisualSegmentDepManouvering = PinSVisualSegmentDepDirect(self)
        
            layersList = []
            if self.ui.cmbConstructionType.SelectedItem != ConstructionType.Construct2D:
                self.pinSVisualSegmentDepManouvering.imethod_2(layersList)
            else:
                self.pinSVisualSegmentDepManouvering.imethod_1(layersList)
                
            QgisHelper.appendToCanvas(define._canvas, layersList, SurfaceTypes.PinSVisualSegmentDep)
            QgisHelper.zoomToLayers(layersList)
            self.resultLayerList = layersList
            self.ui.btnEvaluate.setEnabled(True)
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
        
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
        if self.ui.cmbSegmentType.SelectedIndex != 0:
            self.filterList = ["", PinsSurfaceType.PinsSurfaceType_LevelOIS, PinsSurfaceType.PinsSurfaceType_OCS]
        else:
            self.filterList = ["", PinsSurfaceType.PinsSurfaceType_OIS]
#         self.ui.btnExportResult.setEnabled(True)     
        
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, "PinS Visual Segment for Departures", self.ui.tblObstacles, self.filterList, parameterList, resultHideColumnNames)
        self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbSurface.currentIndex()])
#         FlightPlanBaseDlg.exportResult()
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Visual Segment Type", self.ui.cmbSegmentType.SelectedItem))
        parameterList.append(("VSDG", str(self.ui.txtVSDG.Value.Percent) + " %"))
        parameterList.append(("Minimum(%s)"%self.pnlMCAH.cmbMCAH.currentText(), self.pnlMCAH.txtMCAH.text() + " ft"))
        parameterList.append(("Construction Type", self.ui.cmbConstructionType.SelectedItem))
        if self.ui.cmbSegmentType.SelectedIndex != 0:
            parameterList.append(("Departure Type", self.ui.cmbDepartureType.SelectedItem))
            parameterList.append(("Out-bound Take-off Surface Track", "Plan : " + str(self.parametersPanel.txtTakeOffSurfaceTrack.txtRadialPlan.Value) + define._degreeStr))
            parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtTakeOffSurfaceTrack.txtRadialGeodetic.Value) + define._degreeStr))

            # parameterList.append(("Out-bound Take-off Surface Track", self.ui.txtTakeOffSurfaceTrack.Value + unicode(" °", "utf-8")))
            if self.ui.chbRightTurnProhibited.isChecked():
                parameterList.append(("Limitation", "Right turn prohibited"))
            else:
                parameterList.append(("Limitation", "Left turn prohibited"))
        else:
            parameterList.append(("MOC", str(self.ui.txtMOC.Value.Metres) + " m"))
            parameterList.append(("", str(self.ui.txtMOC.Value.Feet) + " ft"))
                        
        parameterList.append(("Initial Departure Fix (IDF)", "group"))
#         parameterList.append(("X", self.pnlIDF.txtPointX.text()))
#         parameterList.append(("Y", self.pnlIDF.txtPointY.text()))
        DataHelper.pnlPositionParameter(self.pnlIDF, parameterList)
        if self.ui.cmbSegmentType.SelectedIndex == 0:
            parameterList.append(("Track From", "Plan : " + str(self.ui.txtTrackFrom.txtRadialPlan.Value) + define._degreeStr))
            parameterList.append(("", "Geodetic : " + str(self.ui.txtTrackFrom.txtRadialGeodetic.Value) + define._degreeStr))

            # parameterList.append(("Track From", self.ui.txtTrackFrom.Value + unicode(" °", "utf-8")))
        
        parameterList.append(("Heliport", "group"))
        DataHelper.pnlPositionParameter(self.pnlHRP, parameterList)
        parameterList.append(("Safety Area Length", str(self.ui.txtHSAL.Value.Metres) + " m"))
        parameterList.append(("Safety Area Width", str(self.ui.txtHSAW.Value.Metres) + " m"))
                
        parameterList.append(("Results / Checked Obstacles", "group"))        

        parameterList.append(("Checked Obstacles", "group"))
        
        for strFilter in self.filterList:
            self.obstaclesModel.setFilterFixedString(strFilter)
            c = self.obstaclesModel.rowCount()
            parameterList.append(("Number of Checked Obstacles(%s)"%strFilter, str(c)))  
        return parameterList
        
class IPinSVisualSegmentDep:
    ''' PinSVisualSegmentDep Interface'''
    def __init__(self):
        self.SelectionArea = None

    def imethod_1(self, string_0):
        pass

    def imethod_2(self, string_0):
        pass

class PinSVisualSegmentDepDirect(IPinSVisualSegmentDep):

    def __init__(self, pinSVisualSegmentDep_0):
        IPinSVisualSegmentDep.__init__(self)
        self.poaOIS = PrimaryObstacleArea()
        self.paOIS = PolylineArea()
        self.tanOIS = 0.0
        self.trackOIS = 0.0
        self.maxSurfAlt = 0.0
        self.ptHRP = Point3D()
        self.ptIDF = Point3D()
        self.ptL1 = Point3D()
        self.ptR1 = Point3D()
        turnDirection = []
        metres = float(pinSVisualSegmentDep_0.ui.txtHSAL.Value.Metres)
        num = float(pinSVisualSegmentDep_0.ui.txtHSAW.Value.Metres)
        self.ptHRP = pinSVisualSegmentDep_0.pnlHRP.getPoint3D()
        self.ptIDF = pinSVisualSegmentDep_0.pnlIDF.getPoint3D()
        num1 = MathHelper.calcDistance(self.ptIDF, self.ptHRP) - metres / 2
        if (num1 < 1482):
            raise UserWarning ,Messages.ERR_INSUFFICIENT_SEGMENT_LENGTH
        value = float(pinSVisualSegmentDep_0.ui.txtTrackFrom.Value)
        num2 = Unit.smethod_1(MathHelper.getBearing(self.ptHRP, self.ptIDF))
        num3 = MathHelper.smethod_77(num2, value, AngleUnits.Degrees, turnDirection)
        if (num3 == 0):
            str1 = "13.9km(7.5nm)"
            if (num1 > 13900):
                raise UserWarning, Messages.ERR_MAX_SEGMENT_LENGTH_X%str1
        elif (num3 <= 10):
            str3 = "11.9km(6.4nm)"
            if (num1 > 11900):
                raise UserWarning, Messages.ERR_MAX_SEGMENT_LENGTH_X%str3                
        elif (num3 > 20):
            if (num3 > 30):
                raise UserWarning, Messages.ERR_COURSE_CHANGES_GREATER_THAN_30_NOT_ALLOWED
            str5 = "6.5km(3.5nm)"                
            if (num1 > 6500):
                raise UserWarning, Messages.ERR_MAX_SEGMENT_LENGTH_X%str5
        else:
            str7 = "9.3km(5nm)"
            if (num1 > 9300):
                raise UserWarning, Messages.ERR_MAX_SEGMENT_LENGTH_X%str7
        altitude = pinSVisualSegmentDep_0.pnlMCAH.method_2(Altitude(self.ptHRP.get_Z()))
        metres1 = altitude.Metres
        altitude1 = pinSVisualSegmentDep_0.pnlMCAH.method_3(Altitude(self.ptHRP.get_Z()))
        metres2 = altitude1.Metres
        metres3 = pinSVisualSegmentDep_0.ui.txtMOC.Value.Metres
        if (metres2 - metres3 <= 0):
            raise UserWarning, Messages.ERR_INSUFFICIENT_MINIMUM_ALTITUDE
        angleGradientSlope = pinSVisualSegmentDep_0.ui.txtVSDG.Value
        percent = metres2 / (angleGradientSlope.Percent / 100)
        self.tanOIS = (metres2 - metres3) / percent
        if (percent > num1):
            raise UserWarning, Messages.ERR_IDF_TOO_CLOSE_OR_MIN_ALT_TOO_HIGH
        num2 = Unit.ConvertDegToRad(num2)
        value = Unit.ConvertDegToRad(value)
        self.trackOIS = num2
        num4 = Unit.ConvertDegToRad(15)
        point3d = MathHelper.distanceBearingPoint(self.ptHRP, num2, metres / 2)
        self.ptL1 = MathHelper.distanceBearingPoint(point3d, num2 - 1.5707963267949, 45).smethod_167(self.ptHRP.get_Z())
        self.ptR1 = MathHelper.distanceBearingPoint(point3d, num2 + 1.5707963267949, 45).smethod_167(self.ptHRP.get_Z())
        point3d1 = MathHelper.distanceBearingPoint(self.ptL1, num2 - num4, percent / math.cos(num4)).smethod_167(self.ptHRP.get_Z() + percent * self.tanOIS)
        point3d2 = MathHelper.distanceBearingPoint(self.ptR1, num2 + num4, percent / math.cos(num4)).smethod_167(self.ptHRP.get_Z() + percent * self.tanOIS)
        point3d3 = MathHelper.distanceBearingPoint(point3d1, num2 - num4, (num1 - percent) / math.cos(num4)).smethod_167(self.ptHRP.get_Z() + percent * self.tanOIS)
        point3d4 = MathHelper.distanceBearingPoint(point3d2, num2 + num4, (num1 - percent) / math.cos(num4)).smethod_167(self.ptHRP.get_Z() + percent * self.tanOIS)
        self.maxSurfAlt = self.ptHRP.get_Z() + percent * self.tanOIS
        self.paOIS = PolylineArea()
        polylineArea = self.paOIS
        point3dArray = [ self.ptL1, point3d1, point3d3, point3d4, point3d2, self.ptR1 ]
        polylineArea.method_7(point3dArray)
        self.paOIS.method_16()
        self.poaOIS = PrimaryObstacleArea(self.paOIS)
            
    def get_SelectionArea(self):
        return self.poaOIS.SelectionArea
    SelectionArea = property(get_SelectionArea, None, None, None)

    def imethod_0(self, obstacle_0):
        criticalObstacleType = CriticalObstacleType.No
        if (self.poaOIS.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
            point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.trackOIS, 100)
            point3d = MathHelper.getIntersectionPoint(obstacle_0.Position, point3d1, self.ptL1, self.ptR1)
            num = max([MathHelper.calcDistance(point3d, obstacle_0.Position) - obstacle_0.Tolerance, 0])
            num1 = min([self.ptHRP.get_Z() + num * self.tanOIS, self.maxSurfAlt])
            position = obstacle_0.Position
            z = position.get_Z() + obstacle_0.Trees - num1
            if (z > 0):
                criticalObstacleType = CriticalObstacleType.Yes
            return [num1, z, criticalObstacleType, PinsSurfaceType.PinsSurfaceType_OIS]

    def imethod_1(self, layers):
        resultLayer = AcadHelper.createVectorLayer("Pins Visual Segment Departure")
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.paOIS, True, {"Surface":PinsSurfaceType.PinsSurfaceType_OIS})
        # pointList = self.paOIS.method_14_closed()
        # resultLayer = QgisHelper.createPolylineLayer("Pins Visual Segment Departure",
        #                                               [(pointList, [("surface", PinsSurfaceType.PinsSurfaceType_OIS)])],
        #                                               [QgsField("surface", QVariant.String)])
        layers.append(resultLayer)
    
    def imethod_2(self, layers):
        resultLayer = AcadHelper.createVectorLayer("Pins Visual Segment Departure")

        if (self.paOIS.Count == 4):

            face = [self.paOIS[0].Position, self.paOIS[1].Position, self.paOIS[2].Position, self.paOIS[3].Position, self.paOIS[0].Position]
            # resultLayer = QgisHelper.createPolylineLayer("Pins Visual Segment Departure",
            #                                              [(face, [("surface", PinsSurfaceType.PinsSurfaceType_OIS)])],
            #                                              [QgsField("surface", QVariant.String)])
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, face, False, {"Surface":PinsSurfaceType.PinsSurfaceType_OIS})

            layers.append(resultLayer)
            return

        linesList = []
        face = [self.paOIS[0].Position, self.paOIS[1].Position, self.paOIS[4].Position, self.paOIS[5].Position, self.paOIS[0].Position]
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, face, False, {"Surface":PinsSurfaceType.PinsSurfaceType_OIS})

        linesList.append((face, [("surface", PinsSurfaceType.PinsSurfaceType_OIS)]))
        face = [self.paOIS[1].Position, self.paOIS[2].Position, self.paOIS[3].Position, self.paOIS[4].Position, self.paOIS[1].Position]
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, face, False, {"Surface":PinsSurfaceType.PinsSurfaceType_OIS})

        linesList.append((face, [("surface", PinsSurfaceType.PinsSurfaceType_OIS)]))
        # resultLayer = QgisHelper.createPolylineLayer("Pins Visual Segment Departure", linesList, [QgsField("surface", QVariant.String)])
        layers.append(resultLayer)

class PinSVisualSegmentDepManouvering(IPinSVisualSegmentDep):
    
    def __init__(self, pinSVisualSegmentDep_0):
        IPinSVisualSegmentDep.__init__(self)
        self.RADIUS = 750
        self.OCS = 0;
        self.OIS = 1;
        self.poaOIS = PrimaryObstacleArea()
        self.poaOCS = PrimaryObstacleArea()
        self.paOIS = PolylineArea()
        self.paOCS = PolylineArea()
        self.selectionArea = []
        self.ptsOCSL = []
        self.ptsOCSR = []
        self.ptHRP = Point3D()
        self.ptIDF = Point3D()
        self.track = 0.0
        self.tang = 0.0
        self.elevOIS = 0.0
        self.cancelled = False

        self.ptIDF = pinSVisualSegmentDep_0.pnlIDF.getPoint3D()
        self.ptHRP = pinSVisualSegmentDep_0.pnlHRP.getPoint3D()
        self.track = MathHelper.smethod_4(Unit.ConvertDegToRad(float(pinSVisualSegmentDep_0.ui.txtTakeOffSurfaceTrack.Value)))
        num = MathHelper.getBearing(self.ptIDF, self.ptHRP)
        MathHelper.getBearing(self.ptHRP, self.ptIDF);
        altitude = pinSVisualSegmentDep_0.pnlMCAH.method_3(Altitude(self.ptHRP.get_Z()))
        metres = altitude.Metres
        if (metres < 90):
            raise UserWarning, Messages.ERR_INSUFFICIENT_MINIMUM_ALTITUDE
        altitude1 = pinSVisualSegmentDep_0.pnlMCAH.method_2(Altitude(self.ptHRP.get_Z()))
        metres1 = altitude1.Metres
        self.tang = 0.125
        num1 = 741
        num2 = 1482
        if (metres > 183):
            num3 = math.trunc((metres - 183) / 30)
            if ((metres - 183) % 30 > 0):
                num3 = num3 + 1
            num2 = num2 + num3 * 185
        num4 = 50
        if (metres > 183 and metres <= 304):
            num5 = math.trunc((metres - 183) / 30)
            if ((metres - 183) % 30 > 0):
                num5 = num5 + 1
            num4 = num4 - num5 * 5
            if (num4 < 30):
                num4 = 30
        elif (metres > 304):
            num4 = 30
        num6 = Unit.ConvertDegToRad(num4)
        num7 = MathHelper.calcDistance(self.ptIDF, self.ptHRP)
        if (num7 < 1000):
            eRRINSUFFICIENTSEGMENTLENGTHIDFHRP = Messages.ERR_INSUFFICIENT_SEGMENT_LENGTH_IDF_HRP
            distance = Distance(num2)
            raise UserWarning, eRRINSUFFICIENTSEGMENTLENGTHIDFHRP % distance.Metres
        turnDirectionList = []
        num8 = MathHelper.smethod_77(num, self.track, AngleUnits.Radians, turnDirectionList)
        turnDirection = turnDirectionList[0]
        if (num8 + num6 >= 3.14159265358979):
            eRRPINSCCHGLARGEUSEDIRECT = Messages.ERR_PINS_CCHG_LARGE_USE_DIRECT
            num9 = Unit.smethod_1(3.14159265358979 - num6)
            raise UserWarning, eRRPINSCCHGLARGEUSEDIRECT % num9
        self.paOIS = PolylineArea()
        self.paOIS.method_1(self.ptIDF)
        if (turnDirection == TurnDirection.Nothing or MathHelper.smethod_99(num8, 0, 0.1)):
            point3d = MathHelper.distanceBearingPoint(self.ptHRP, num - num6, num2)
            point3d1 = MathHelper.distanceBearingPoint(self.ptHRP, num + num6, num2)
            if (pinSVisualSegmentDep_0.ui.chbLeftTurnProhibited.isChecked()):
                point3d = MathHelper.distanceBearingPoint(self.ptHRP, num, num2)
            elif (pinSVisualSegmentDep_0.ui.chbRightTurnProhibited.isChecked()):
                point3d1 = MathHelper.distanceBearingPoint(self.ptHRP, num, num2);
            self.paOIS.method_3(point3d, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, self.ptHRP))
            self.paOIS.method_1(point3d1)
        else:
            if num2 > num7:
                point3d2 = None
                point3d3 = None
            else:
                point3d2 = MathHelper.distanceBearingPoint(self.ptHRP, num - math.fabs(math.asin(num2 / num7)) - 1.5707963267949, num2)
                point3d3 = MathHelper.distanceBearingPoint(self.ptHRP, num + math.fabs(math.asin(num2 / num7)) + 1.5707963267949, num2)
            if (num8 < num6 and not pinSVisualSegmentDep_0.ui.chbLeftTurnProhibited.isChecked() and not pinSVisualSegmentDep_0.ui.chbRightTurnProhibited.isChecked()):
                point3d = MathHelper.distanceBearingPoint(self.ptHRP, self.track - num6, num2)
                point3d1 = MathHelper.distanceBearingPoint(self.ptHRP, self.track + num6, num2)
                if (MathHelper.smethod_119(point3d2, self.ptHRP, point3d)):
                    point3d = point3d2
                if (MathHelper.smethod_115(point3d3, self.ptHRP, point3d1)):
                    point3d1 = point3d3
                self.paOIS.method_3(point3d, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, self.ptHRP))
                self.paOIS.method_1(point3d1)
                self.paOIS.method_1(self.ptIDF)
            elif (turnDirection != TurnDirection.Left):
                point3d1 = MathHelper.distanceBearingPoint(self.ptHRP, self.track + num6, num2)
                if (MathHelper.smethod_115(point3d3, self.ptHRP, point3d1)):
                    point3d1 = point3d3
                if (pinSVisualSegmentDep_0.ui.chbLeftTurnProhibited.isChecked()):
                    point3d = MathHelper.distanceBearingPoint(self.ptHRP, self.track, num2)
                    self.paOIS.method_1(self.ptHRP)
                    if not MathHelper.smethod_119(point3d3, self.ptHRP, point3d):
                        self.paOIS.method_1(point3d)
                    else:
                        self.paOIS.method_3(point3d, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, self.ptHRP))
                        self.paOIS.method_1(point3d1)
                    self.paOIS.method_1(self.ptIDF)
                else:
                    num10 = Unit.ConvertDegToRad(30)
                    point3d = MathHelper.distanceBearingPoint(self.ptHRP, self.track - num6, num2) if num8 - num6 <= num10 else MathHelper.distanceBearingPoint(self.ptHRP, num + num10, num2)
                    if (MathHelper.smethod_119(point3d, self.ptIDF, self.ptHRP)):
                        self.paOIS.method_1(self.ptHRP);
                    self.paOIS.method_3(point3d, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, self.ptHRP))
                    self.paOIS.method_1(point3d1)
                    self.paOIS.method_1(self.ptIDF)
            else:
                point3d = MathHelper.distanceBearingPoint(self.ptHRP, self.track - num6, num2)
                if (MathHelper.smethod_119(point3d2, self.ptHRP, point3d)):
                    point3d = point3d2
                if (not pinSVisualSegmentDep_0.ui.chbRightTurnProhibited.isChecked()):
                    num11 = Unit.ConvertDegToRad(30)
                    point3d1 = MathHelper.distanceBearingPoint(self.ptHRP, self.track + num6, num2) if num8 - num6 <= num11 else MathHelper.distanceBearingPoint(self.ptHRP, num - num11, num2)
                    self.paOIS.method_3(point3d, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, self.ptHRP))
                    self.paOIS.method_1(point3d1)
                    if (MathHelper.smethod_115(point3d1, self.ptIDF, self.ptHRP)):
                        self.paOIS.method_1(self.ptHRP)
                    self.paOIS.method_1(self.ptIDF)
                else:
                    point3d1 = MathHelper.distanceBearingPoint(self.ptHRP, self.track, num2)
                    if (MathHelper.smethod_115(point3d2, self.ptHRP, point3d1)):
                        self.paOIS.method_3(point3d, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, self.ptHRP))
                    self.paOIS.method_1(point3d1)
                    self.paOIS.method_1(self.ptHRP)
                    self.paOIS.method_1(self.ptIDF)
#         polyline = AcadHelper.smethod_131(self.paOIS);
#         polyline.set_Closed(true);
#         polyline = polyline.smethod_159(num1, OffsetGapType.Fillet, TurnDirection.Right);
        self.paOIS.offsetCurve(num1)
        self.poaOIS = PrimaryObstacleArea(self.paOIS)
        self.elevOIS = self.ptHRP.get_Z() + max([metres / 2 - 46, 46])
        metres2 = float(pinSVisualSegmentDep_0.ui.txtHSAW.Value.Metres)
        metres3 = float(pinSVisualSegmentDep_0.ui.txtHSAL.Value.Metres)
        num = MathHelper.smethod_4(Unit.ConvertDegToRad(float(pinSVisualSegmentDep_0.ui.txtTakeOffSurfaceTrack.Value)))
        self.paOCS = PolylineArea()
        self.ptsOCSL = []
        self.ptsOCSR = []
        point3d4 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(self.ptHRP, num, metres3 / 2), num - 1.5707963267949, metres2 / 2)
        point3d5 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(self.ptHRP, num, metres3 / 2), num + 1.5707963267949, metres2 / 2)
        num12 = math.atan(0.1) if pinSVisualSegmentDep_0.ui.cmbDepartureType.SelectedIndex == 0 else math.atan(0.15)
        num13 = 152 / self.tang
        num14 = (120 - metres2 / 2) / math.tan(num12)
        self.ptsOCSL = []
        self.ptsOCSL.append(point3d4)
        self.ptsOCSL.append(MathHelper.distanceBearingPoint(point3d4, num - num12, num14 * math.cos(num12)).smethod_167(self.ptHRP.get_Z() + num14 * self.tang))
        self.ptsOCSL.append(MathHelper.distanceBearingPoint(self.ptsOCSL[1], num, num13 - num14).smethod_167(self.ptHRP.get_Z() + 152))
        self.ptsOCSR = []
        self.ptsOCSR.append(point3d5)
        self.ptsOCSR.append(MathHelper.distanceBearingPoint(point3d5, num + num12, num14 * math.cos(num12)).smethod_167(self.ptHRP.get_Z() + num14 * self.tang))
        self.ptsOCSR.append(MathHelper.distanceBearingPoint(self.ptsOCSR[1], num, num13 - num14).smethod_167(self.ptHRP.get_Z() + 152))
        self.paOCS = PolylineArea()
        for point in self.ptsOCSL:
            self.paOCS.method_1(point)
        for j in range(len(self.ptsOCSR) - 1, -1, -1):
            self.paOCS.method_1(self.ptsOCSR[j])
        self.paOCS.method_10()
        self.poaOCS = PrimaryObstacleArea(self.paOCS)
        self.selectionArea = (PrimaryObstacleArea(self.paOIS)).SelectionArea

    def get_Cancelled(self):
        return self.cancelled
    Cancelled = property(get_Cancelled, None, None, None)

    def get_SelectionArea(self):
        return self.selectionArea;
    SelectionArea = property(get_SelectionArea, None, None, None)

    def imethod_0(self, obstacle_0):
        criticalObstacleType = CriticalObstacleType.No
        if (self.poaOIS.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
            z = self.elevOIS
            num = 1
            if (self.poaOCS.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
                point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.track, 100)
                point3d = MathHelper.getIntersectionPoint(obstacle_0.Position, point3d1, self.ptsOCSL[0], self.ptsOCSR[0])
                num1 = max(MathHelper.calcDistance(point3d, obstacle_0.Position) - obstacle_0.Tolerance, 0)
                z = num1 * self.tang + self.ptHRP.get_Z()
                num = 0
            position = obstacle_0.Position
            z1 = position.get_Z() + obstacle_0.Trees - z
            if (z1 > 0):
                criticalObstacleType = CriticalObstacleType.Yes;
            return [z, z1, criticalObstacleType, PinsSurfaceType.PinsSurfaceType_OCS if num == 0 else PinsSurfaceType.PinsSurfaceType_LevelOIS]

    def imethod_1(self, layers):
        linesList = []
        pointList = self.paOIS.method_14_closed()
        linesList.append((pointList, [("surface", PinsSurfaceType.PinsSurfaceType_LevelOIS)]))
        polyline = self.paOCS.method_14_closed()
        linesList.append((polyline, [("surface", PinsSurfaceType.PinsSurfaceType_OCS)]))
        resultLayer = QgisHelper.createPolylineLayer("Pins Visual Segment Departure Manouvering 2D", linesList, [QgsField("surface", QVariant.String)])
        layers.append(resultLayer)

    def imethod_2(self, layers):
        polyline = self.paOIS.method_14_closed()
#         polyline.set_Elevation(self.elevOIS);
        linesList = []
        for i in range(1, len(self.ptsOCSL)):
            face = [self.ptsOCSL[i - 1], self.ptsOCSL[i], self.ptsOCSR[i], self.ptsOCSR[i - 1]]
            linesList.append((face, [("surface", PinsSurfaceType.PinsSurfaceType_OCS)]))
        
        linesList.append((polyline, [("surface", PinsSurfaceType.PinsSurfaceType_LevelOIS)]))
        resultLayer = QgisHelper.createPolylineLayer("Pins Visual Segment Departure Manouvering 3D", linesList, [QgsField("surface", QVariant.String)])
        layers.append(resultLayer)
        
class PinSVisualSegmentDepObstacles(ObstacleTable):
    def __init__(self, surfacesList):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)
        self.surfaceType = SurfaceTypes.PinSVisualSegmentDep
        
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
                surfaceString = feature.attribute("surface").toString()
                if surfaceString == surfaceType:
                    geom = feature.geometry()
                    rect.combineExtentWith(geom.boundingBox())
        return rect
        