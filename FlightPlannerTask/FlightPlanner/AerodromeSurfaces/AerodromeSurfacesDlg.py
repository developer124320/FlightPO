# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QSize, Qt, QString,QVariant
from PyQt4.QtGui import QMessageBox, QStandardItem,QApplication, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsVectorFileWriter,QgsPalLayerSettings,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, AerodromeSurfacesInnerHorizontalLocation, SurfaceTypes, ObstacleTableColumnType,AircraftSpeedCategory,\
    AerodromeSurfacesCriteriaType, AltitudeUnits, ObstacleAreaResult, Formating, RnavGnssFlightPhase, Point3D, AngleUnits, ConstructionType
from FlightPlanner.AerodromeSurfaces.Ui_AerodromeSurfacesGeneral import Ui_AerodromeSurfacesGeneral
from FlightPlanner.AerodromeSurfaces.Ui_AerodromeSurfacesAltitude import Ui_AerodromeSurfacesAltitude
from FlightPlanner.expressions import Expressions
from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.RnavTolerance0 import RnavGnssTolerance
from FlightPlanner.Captions import Captions
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.types import Point3D, Point3dCollection, AerodromeSurfacesRunwayCode, AerodromeSurfacesDatumElevation,\
    AerodromeSurfacesApproachType, ObstacleEvaluationMode
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, SecondaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable, Obstacle
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.Confirmations import Confirmations
from FlightPlanner.TempCorrection.TempCorrection import TempCorrection
from FlightPlanner.messages import Messages
from Type.switch import switch
from Type.Degrees import Degrees
from Type.Runway import RunwayList, Runway
from Type.SurfaceCriteria import AerodromeSurfacesCriteriaList, AerodromeSurfacesCriteria
from Type.Position import PositionType, Position
from Type.String import String, StringBuilder
from Type.Geometry import Line

from FlightPlanner.Dialogs.DlgAerodromeSurfacesCriteria import DlgAerodromeSurfacesCriteria
from FlightPlanner.Dialogs.DlgRunway import DlgRunway
from FlightPlanner.Dialogs.DlgAerodromeSurfaces import DlgAerodromeSurfaces
import define, math
class AerodromeSurfacesDlg(FlightPlanBaseDlg):
    singleObstaclesChecked = 0
    multiObstaclesChecked = 0
    singleObstacles = None
    multiObstacles = []
    runways = None
    criteria = None
    constructionLayers = []


    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        # self.parametersPanelAltitude = None
        self.setObjectName("AerodromeSurfacesDlg")
        self.surfaceType = SurfaceTypes.AerodromeSurfaces
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.AerodromeSurfaces)
        self.resize(600, 610)
        QgisHelper.matchingDialogSize(self, 600, 610)
        self.surfaceList = None
        self.updating = False

        self.calculationResults = []

        self.resultLayerList = []

        self.arpFeatureArray = []
        self.currentLayer = None
        self.rwyFeatureArray = []
        # self.initAerodromeAndRwyCmb()
        
        #############  init part   #########
        self.parametersPanel.pnlRwyCode.Items = AerodromeSurfacesRunwayCode.Items
        self.parametersPanel.pnlDatumElevation.Items = AerodromeSurfacesDatumElevation.Items
        self.parametersPanel.pnlApproachType.Items = AerodromeSurfacesApproachType.Items
        self.parametersPanelAltitude.pnlEvalMode.Items = ObstacleEvaluationMode.Items
        if (AerodromeSurfacesDlg.singleObstacles == None):
            AerodromeSurfacesDlg.singleObstacles = AerodromeSurfacesSingleObstacles()
        if (AerodromeSurfacesDlg.multiObstacles == None):
            AerodromeSurfacesDlg.multiObstacles = []
        if (AerodromeSurfacesDlg.runways == None):
            AerodromeSurfacesDlg.runways = RunwayList.smethod_0(self)
        if (AerodromeSurfacesDlg.criteria == None):
            AerodromeSurfacesDlg.criteria = AerodromeSurfacesCriteriaList.smethod_0(self)
        if AerodromeSurfacesDlg.runways != None and len(AerodromeSurfacesDlg.runways) > 0:
            self.method_36(AerodromeSurfacesDlg.runways[0])
        if AerodromeSurfacesDlg.criteria != None and len(AerodromeSurfacesDlg.criteria) > 0:
            self.parametersPanel.pnlCriteria.Items = AerodromeSurfacesDlg.criteria
        
        
    @staticmethod
    def AerodromeSurfaces():
        AerodromeSurfacesDlg.singleObstaclesChecked = 0
        AerodromeSurfacesDlg.multiObstaclesChecked = 0
        AerodromeSurfacesDlg.singleObstacles = None
        AerodromeSurfacesDlg.multiObstacles = None
        AerodromeSurfacesDlg.runways = None
        AerodromeSurfacesDlg.criteria = None


    def initObstaclesModel(self):
        self.obstaclesModel.MocMultiplier = 1
        return FlightPlanBaseDlg.initObstaclesModel(self)

    
    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return  
        self.filterList = []
        self.filterList.append("")
        if self.surfaceList == None or len(self.surfaceList) == 0:
            self.filterList = None
        else:
            for surf in self.surfaceList:
                self.filterList.append(surf.title)
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.BaroVNAV, self.ui.tblObstacles, self.filterList, parameterList, resultHideColumnNames)
#         self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
    
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("Runway", "group"))
        parameterList.append(("Name", self.parametersPanel.pnlRunway.SelectedItem))
        parameterList.append(("Code", self.parametersPanel.pnlRwyCode.SelectedItem))

        parameterList.append(("Aerodrome", "group"))
        parameterList.append(("Datum Elevation", self.parametersPanel.pnlDatumElevation.SelectedItem))

        parameterList.append(("Aerodrome Reference Point (ARP)", "group"))
        parameterList.append(("Lat", self.parametersPanel.pnlARP.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlARP.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlARP.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlARP.txtPointY.text()))
        parameterList.append(("Altitude", self.parametersPanel.pnlARP.txtAltitudeM.text() + "m"))
        parameterList.append(("", self.parametersPanel.pnlARP.txtAltitudeFt.text() + "ft"))

        parameterList.append(("Code Letter 'F'", self.parametersPanel.chbLetterF.Checked))

        parameterList.append(("Parameters", "group"))
        parameterList.append(("Criteria", self.parametersPanel.pnlCriteria.SelectedItem))
        parameterList.append(("Approach Type", self.parametersPanel.pnlApproachType.SelectedItem))
        parameterList.append(("Approach Obstacle Altitude", str(self.parametersPanel.pnlApproachObstacleAltitude.Value.Metres) + "m"))
        parameterList.append(("", str(self.parametersPanel.pnlApproachObstacleAltitude.Value.Feet) + "ft"))
        parameterList.append(("Departure Track Heading Change > 15", self.parametersPanel.chbDepTrackMoreThan15.Checked))
        parameterList.append(("1.6% Take Off Climb Surface", self.parametersPanel.chbSecondSlope.Checked))

        parameterList.append(("Construction", "group"))
        parameterList.append(("Construction Type", str(self.parametersPanel.pnlConstructionType.SelectedItem)))
        if self.parametersPanel.pnlConstructionType.SelectedItem == ConstructionType.Construct3D:
            parameterList.append(("Mark Contour Altitudes", self.parametersPanel.chbMarkAltitudes.Checked))

        parameterList.append(("Altitude of a Position", "group"))
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Mode", self.parametersPanelAltitude.pnlEvalMode.SelectedItem))
        if self.parametersPanelAltitude.pnlEvalMode.SelectedIndex == 0:
            parameterList.append(("Position", "group"))
            parameterList.append(("Lat", self.parametersPanelAltitude.pnlEvalPosition.txtLat.Value))
            parameterList.append(("Lon", self.parametersPanelAltitude.pnlEvalPosition.txtLong.Value))
            parameterList.append(("X", self.parametersPanelAltitude.pnlEvalPosition.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanelAltitude.pnlEvalPosition.txtPointY.text()))
            parameterList.append(("Altitude", self.parametersPanelAltitude.pnlEvalPosition.txtAltitudeM.text() + "m"))
            parameterList.append(("", self.parametersPanelAltitude.pnlEvalPosition.txtAltitudeFt.text() + "ft"))

            parameterList.append(("Insert Point And Text", self.parametersPanelAltitude.chbInsertPointAndText.Checked))
            if self.parametersPanelAltitude.chbInsertPointAndText.Checked:
                parameterList.append(("Text Height", str(int(self.parametersPanelAltitude.pnlTextHeight.Value))))
        else:
            parameterList.append(("Evaluate Only Penetrating Obstacles", self.parametersPanelAltitude.chbOnlyPenetratingObstacles.Checked))

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
        # self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        self.ui.btnPDTCheck.setVisible(False)
        return FlightPlanBaseDlg.uiStateInit(self)
    def initSurfaceCombo(self):
        self.method_34()
    def btnEvaluate_Click(self):
        selectedItem = self.parametersPanel.pnlRunway.SelectedItem
        self.surfaceSubGroupNames = [self.parametersPanel.pnlRunway.comboBox.currentText().replace(" ", "_")]
        aerodromeSurfacesCriterium = self.method_41(False)
        altitude = self.method_42(selectedItem)
        enabled = aerodromeSurfacesCriterium.Strip.Enabled
        flag = aerodromeSurfacesCriterium.InnerHorizontal.Enabled
        enabled1 = aerodromeSurfacesCriterium.InnerApproach.Enabled
        flag1 = False if(not aerodromeSurfacesCriterium.BalkedLanding.Enabled) else flag
        flag2 = False if(not aerodromeSurfacesCriterium.InnerTransitional.Enabled or not enabled1) else flag1
        enabled2 = aerodromeSurfacesCriterium.Approach.Enabled
        enabled3 = aerodromeSurfacesCriterium.TakeOff.Enabled
        flag3 = False if(not aerodromeSurfacesCriterium.Transitional.Enabled or not enabled2) else flag
        flag4 = False if(not aerodromeSurfacesCriterium.NavigationalAid.Enabled) else flag3
        flag5 = False if(not aerodromeSurfacesCriterium.Conical.Enabled) else flag
        flag6 = False if(not self.parametersPanel.pnlARP.IsValid() or not aerodromeSurfacesCriterium.OuterHorizontal.Enabled) else flag5
        aerodromeSurfacesSurfaces = []
        if (enabled):
            aerodromeSurfacesSurfaces.append(StripSurface(selectedItem, aerodromeSurfacesCriterium))
        if (enabled1):
            aerodromeSurfacesSurfaces.append(InnerApproachSurface(selectedItem, aerodromeSurfacesCriterium))
        if (flag1):
            aerodromeSurfacesSurfaces.append(BalkedLandingSurface(selectedItem, aerodromeSurfacesCriterium, altitude))
        if (flag2):
            aerodromeSurfacesSurfaces.append(InnerTransitionalSurface(selectedItem, aerodromeSurfacesCriterium, altitude))
        if (enabled2):
            aerodromeSurfacesSurfaces.append(ApproachSurface(selectedItem, aerodromeSurfacesCriterium, self.parametersPanel.pnlApproachObstacleAltitude.Value))
        if (enabled3):
            aerodromeSurfacesSurfaces.append(TakeOffSurface(selectedItem, aerodromeSurfacesCriterium))
        if (flag3):
            aerodromeSurfacesSurfaces.append(TransitionalSurface(selectedItem, aerodromeSurfacesCriterium, altitude))
        if (flag4):
            aerodromeSurfacesSurfaces.append(NavigationalAidSurface(selectedItem, aerodromeSurfacesCriterium, altitude))
        if (flag):
            aerodromeSurfacesSurfaces.append(InnerHorizontalSurface(selectedItem, aerodromeSurfacesCriterium, altitude))
        if (flag5):
            aerodromeSurfacesSurfaces.append(ConicalSurface(selectedItem, aerodromeSurfacesCriterium, altitude))
        if (flag6):
            aerodromeSurfacesSurfaces.append(OuterHorizontalSurface(selectedItem, aerodromeSurfacesCriterium, altitude, self.parametersPanel.pnlARP.Point3d))
        ObstacleTable.MocMultiplier = 1
        # if (self.parametersPanelAltitude.pnlEvalMode.SelectedIndex != 0):

        # if (not DlgAerodromeSurfaces.smethod_0(self, title, flagArray)):
        #     return
        # for i in range(len(flagArray)):
        #     k = len(flagArray) - 1 - i
        # # for k = (int)flagArray.Length - 1 k >= 0 k--)
        #     if (not flagArray[k]):
        #         aerodromeSurfacesSurfaces.remove(k)

        # self.obstaclesModel = AerodromeSurfacesMultiObstacles(aerodromeSurfacesSurfaces, self.parametersPanelAltitude.chbOnlyPenetratingObstacles.Checked)
        
        if (self.parametersPanelAltitude.pnlEvalMode.SelectedIndex != 0):
            title = []
            for i in range(len(aerodromeSurfacesSurfaces)):
                title.append("")
            for i in range(len(aerodromeSurfacesSurfaces)):
                title[i] = aerodromeSurfacesSurfaces[i].Title
            flagArray = []
            for i in range(len(title)):
                flagArray.append(False)
            for j in range(len(aerodromeSurfacesSurfaces)):
                flagArray[j] = True
            self.obstaclesModel = AerodromeSurfacesMultiObstacles(aerodromeSurfacesSurfaces, self.parametersPanelAltitude.chbOnlyPenetratingObstacles.Checked)
            AerodromeSurfacesDlg.multiObstacles = aerodromeSurfacesSurfaces
            self.surfaceList = aerodromeSurfacesSurfaces
            return FlightPlanBaseDlg.btnEvaluate_Click(self)
        else:
            self.obstaclesModel = AerodromeSurfacesSingleObstacles(aerodromeSurfacesSurfaces)
            point3d = None
            try:
                point3d = self.parametersPanelAltitude.pnlEvalPosition.Point3d
            except UserWarning:
                QMessageBox.warning(self, "Waring", UserWarning.message)
                return
            d = self.parametersPanelAltitude.pnlEvalPosition.ID

            if (d == None or d == ""):
                d = Captions.UNKNOWN
            num1 = define._trees
            num2 = define._tolerance

            # pointLayer = AcadHelper.createVectorLayer("SinglePointLayer", QGis.Point)
            mapUnits = define._canvas.mapUnits()
            if mapUnits == QGis.Meters:
                pointLayer = QgsVectorLayer("Point?crs=%s"%define._xyCrs.authid (), "SinglePointLayer", "memory")
            else:
                pointLayer = QgsVectorLayer("Point?crs=%s"%define._latLonCrs.authid (), "SinglePointLayer", "memory")
            if pointLayer != None:
                pointLayer.startEditing()
                fieldAltitude = "Altitude"
                fieldName = QgsField("Caption", QVariant.String)
                fieldName.setLength(10000)
                fieldNameBulge = "Bulge"
                fieldNameGeometryType = "Type"
                fieldCategory = "CATEGORY"
                fieldXdataName = "XDataName"
                fieldXdataPoint = "XDataPoint"
                fieldXDataTolerance = "XDataTol"
                fieldCenterPoint = "CenterPt"
                fieldSurface = "Surface"

                fAltitude = QgsField(fieldAltitude, QVariant.String)
                # print fAltitude.length()
                # fAltitude.setLength(100000)
                pointLayer.dataProvider().addAttributes( [fAltitude,
                                                         fieldName,
                                                         QgsField(fieldNameBulge, QVariant.String),
                                                         QgsField(fieldNameGeometryType, QVariant.String),
                                                         QgsField(fieldCategory, QVariant.String),
                                                         QgsField(fieldXdataName, QVariant.String),
                                                         QgsField(fieldXdataPoint, QVariant.String),
                                                         QgsField(fieldXDataTolerance, QVariant.String),
                                                         QgsField(fieldCenterPoint, QVariant.String),
                                                         QgsField(fieldSurface, QVariant.String)
                                                                     ])
                pointLayer.commitChanges()
            position = Point3D()
            positionDegree = Point3D()
            point = QgsPoint(point3d.get_X(), point3d.get_Y())
            obstacleLayers = QgisHelper.getSurfaceLayers(SurfaceTypes.Obstacles)
            obstacleLayer = obstacleLayers[0]
            position = Point3D(point.x(), point.y())
#                         if obstacleUnits != define._units:
#                             positionDegree = QgisHelper.Meter2DegreePoint3D(position)

            positionDegree = QgisHelper.CrsTransformPoint(point.x(), point.y(), define._canvas.mapSettings().destinationCrs(),obstacleLayer.crs(), point3d.get_Z())


            obstacle = Obstacle(d, point3d, pointLayer.id(), 0, None, num1, ObstacleTable.MocMultiplier, num2)
            obstacle.positionDegree = positionDegree
            string0 = self.obstaclesModel.method_0(obstacle, "")

            AcadHelper.setGeometryAndAttributesInLayer(pointLayer, point3d, False, {"Caption":string0[1]})

            self.obstaclesModel.setLocateBtn(self.ui.btnLocate)
            self.ui.tblObstacles.setModel(self.obstaclesModel)
            self.obstaclesModel.setTableView(self.ui.tblObstacles)
            self.obstaclesModel.setHiddenColumns(self.ui.tblObstacles)
            self.ui.tabCtrlGeneral.setCurrentIndex(1)
            c = self.obstaclesModel.rowCount()
            if c > 0:
                self.ui.btnExportResult.setEnabled(True)
            if (self.parametersPanelAltitude.chbInsertPointAndText.Checked and string0 != None):
                # pointLayer.startEditing()
                # feature = QgsFeature()
                # feature.setGeometry(QgsGeometry.fromPoint(point3d))
                # feature.setAttributes([string0])
                # pointLayer.addFeature(feature)
                # pointLayer.commitChanges()

                fontSize = self.parametersPanelAltitude.pnlTextHeight.Value

                palSetting = QgsPalLayerSettings()
                palSetting.readFromLayer(pointLayer)
                palSetting.enabled = True
                palSetting.fieldName = "Caption"
                palSetting.isExpression = True
                palSetting.placement = QgsPalLayerSettings.AroundPoint
                # palSetting.placementFlags = QgsPalLayerSettings.AboveLine
                # palSetting.Rotation = Unit.ConvertRadToDeg(7.85398163397448 - num)
                palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, str(int(fontSize)), "")
                palSetting.writeToLayer(pointLayer)

                define._messageLabel.setText(Messages.POINT_TEXT_INSERTED)
            QgisHelper.appendToCanvas(define._canvas, [pointLayer], self.surfaceType)
            # AerodromeSurfaces.AerodromeSurfacesSingleEvaluator aerodromeSurfacesSingleEvaluator = new AerodromeSurfaces.AerodromeSurfacesSingleEvaluator(aerodromeSurfacesSurfaces)
            # Point3d point3d = self.pnlEvalPosition.Point3d
            # string d = self.pnlEvalPosition.ID
            # if (string.IsNullOrEmpty(d))
            # {
            #     d = Captions.UNKNOWN
            # }
            # Obstacle obstacle = new Obstacle(d, point3d, Trees.smethod_2(point3d), 0.0001, 1, ObstacleType.Position)
            # string str = ""
            # if (not aerodromeSurfacesSingleEvaluator.method_0(obstacle, ref str))
            # {
            #     base.method_20(Messages.POSITION_OUTSIDE)
            #     return
            # }
            # self.pnlEvalPosition.method_1()
            # if (self.chbInsertPointAndText.Checked and not string.IsNullOrEmpty(str))
            # {
            #     AcadHelper.smethod_51(point3d, str, self.pnlTextHeight.Value, base.ConstructionLayer)
            #     base.method_20(Messages.POINT_TEXT_INSERTED)
            #     return
            # }
        
    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        AerodromeSurfacesDlg.constructionLayers = []
        pass

        selectedItem = self.parametersPanel.pnlRunway.SelectedItem
        aerodromeSurfacesCriterium = self.method_41(False)
        altitude = self.method_42(selectedItem)
        enabled = aerodromeSurfacesCriterium.Strip.Enabled
        flag = aerodromeSurfacesCriterium.InnerHorizontal.Enabled
        enabled1 = aerodromeSurfacesCriterium.InnerApproach.Enabled
        flag1 = False if(not aerodromeSurfacesCriterium.BalkedLanding.Enabled) else flag
        flag2 = False if(not aerodromeSurfacesCriterium.InnerTransitional.Enabled or not enabled1) else flag1
        enabled2 = aerodromeSurfacesCriterium.Approach.Enabled
        enabled3 = aerodromeSurfacesCriterium.TakeOff.Enabled
        flag3 = False if(not aerodromeSurfacesCriterium.Transitional.Enabled or not enabled2) else flag
        flag4 = False if(not aerodromeSurfacesCriterium.NavigationalAid.Enabled) else flag3
        flag5 = False if(not aerodromeSurfacesCriterium.Conical.Enabled) else flag
        flag6 = False if(not self.parametersPanel.pnlARP.IsValid or not aerodromeSurfacesCriterium.OuterHorizontal.Enabled) else flag5
        # aerodromeSurfacesSurfaces = new List<AerodromeSurfaces.IAerodromeSurfacesSurface>()
        aerodromeSurfacesSurfaces = []
        if (flag4):
            aerodromeSurfacesSurfaces.append(NavigationalAidSurface(selectedItem, aerodromeSurfacesCriterium, altitude))
        if (enabled2):
            aerodromeSurfacesSurfaces.append(ApproachSurface(selectedItem, aerodromeSurfacesCriterium, self.parametersPanel.pnlApproachObstacleAltitude.Value))
        if (flag1):
            aerodromeSurfacesSurfaces.append(BalkedLandingSurface(selectedItem, aerodromeSurfacesCriterium, altitude))
        if (flag5):
            aerodromeSurfacesSurfaces.append(ConicalSurface(selectedItem, aerodromeSurfacesCriterium, altitude))
        if (enabled1):
            aerodromeSurfacesSurfaces.append(InnerApproachSurface(selectedItem, aerodromeSurfacesCriterium))
        if (flag):
            aerodromeSurfacesSurfaces.append(InnerHorizontalSurface(selectedItem, aerodromeSurfacesCriterium, altitude))
        if (flag2):
            aerodromeSurfacesSurfaces.append(InnerTransitionalSurface(selectedItem, aerodromeSurfacesCriterium, altitude))
        if (flag6):
            aerodromeSurfacesSurfaces.append(OuterHorizontalSurface(selectedItem, aerodromeSurfacesCriterium, altitude, self.parametersPanel.pnlARP.Point3d))
        if (enabled):
            aerodromeSurfacesSurfaces.append(StripSurface(selectedItem, aerodromeSurfacesCriterium))
        if (enabled3):
            aerodromeSurfacesSurfaces.append(TakeOffSurface(selectedItem, aerodromeSurfacesCriterium))
        if (flag3):
            aerodromeSurfacesSurfaces.append(TransitionalSurface(selectedItem, aerodromeSurfacesCriterium, altitude))
        # title = new string[aerodromeSurfacesSurfaces.Count]
        title = []
        for i in range(len(aerodromeSurfacesSurfaces)):
            title.append("")
        for i in range(len(aerodromeSurfacesSurfaces)):
            title[i] = aerodromeSurfacesSurfaces[i].Title
        # flagArray = new bool[(int)title.Length]
        flagArray = []
        for i in range(len(title)):
            flagArray.append(False)
        for j in range(len(aerodromeSurfacesSurfaces)):
            flagArray[j] = True
        if (not DlgAerodromeSurfaces.smethod_0(self, title, flagArray)):
            return
        if (self.parametersPanel.pnlConstructionType.SelectedItem == ConstructionType.Construct2D  and self.parametersPanel.chbMarkAltitudes.Checked):
            value = self.parametersPanel.pnlAltitudesEvery.Value
            metres = 0.5 * (value.Metres / (aerodromeSurfacesCriterium.Transitional.Slope / float(100)))
            if (aerodromeSurfacesCriterium.InnerTransitional.Enabled):
                value1 = self.parametersPanel.pnlAltitudesEvery.Value
                metres = 0.5 * (value1.Metres / (aerodromeSurfacesCriterium.InnerTransitional.Slope / float(100)))
            altitude1 = self.parametersPanel.pnlAltitudesEvery.Value
            str0 = ":{0}".format(altitude1.OriginalUnits)
            for aerodromeSurfacesSurface in aerodromeSurfacesSurfaces:
                aerodromeSurfacesSurface.TextHeight = metres
                aerodromeSurfacesSurface.AltitudeFormat = str0
        # Document activeDocument = AcadHelper.ActiveDocument
        # using (DocumentLock documentLock = activeDocument.LockDocument())
        # {
        #     using (Transaction transaction = activeDocument.get_Database().get_TransactionManager().StartTransaction())
        #     {
        #         AerodromeSurfaces.transaction = transaction
        #         AerodromeSurfaces.space = AcadHelper.smethod_32(1, transaction, activeDocument.get_Database())
        # if (self.parametersPanel.pnlConstructionType.SelectedItem != ConstructionType.Construct3D):
        #     AerodromeSurfacesDlg.constructionLayer = AcadHelper.createVectorLayer(self.surfaceType)
        # else:
        #     AerodromeSurfacesDlg.constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Polygon)

        for k in range(len(aerodromeSurfacesSurfaces)):
            if (flagArray[k]):
                if (self.parametersPanel.pnlConstructionType.SelectedItem != ConstructionType.Construct3D):
                    aerodromeSurfacesSurfaces[k].vmethod_0(self.parametersPanel.chbMarkAltitudes.Checked, self.parametersPanel.pnlAltitudesEvery.Value)
                else:
                    aerodromeSurfacesSurfaces[k].vmethod_1()
        self.resultLayerList = AerodromeSurfacesDlg.constructionLayers
        subGropName = self.parametersPanel.pnlRunway.comboBox.currentText().replace(" ", "_")
        QgisHelper.appendToCanvas(define._canvas, self.resultLayerList, [self.surfaceType, subGropName])
        QgisHelper.zoomToLayers(self.resultLayerList)
        # self.ui.btnEvaluate.setEnabled(True)

        #         transaction.Commit()
        #         AcadHelper.smethod_5()
        #     }
        # }
        # base.method_19(Messages.CONSTRUCTION_FINISHED)

    def initParametersPan(self):
        ui0 = Ui_AerodromeSurfacesGeneral()
        self.parametersPanel = ui0
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanelAltitude = Ui_AerodromeSurfacesAltitude(self.ui.grbResult)
        self.ui.vlResultGroup.insertWidget(0, self.parametersPanelAltitude)

        self.ui.tabCtrlGeneral.setTabText(1, "Altitude of a Position / Results")
        self.ui.vlResultBtns.insertWidget(0, self.ui.btnEvaluate)
        self.ui.btnEvaluate.setEnabled(True)

        self.parametersPanel.pnlConstructionType.Items = [ConstructionType.Construct2D, ConstructionType.Construct3D]


        self.connect(self.parametersPanel.chbMarkAltitudes, SIGNAL("Event_0"), self.chbMarkAltitudes_Event_0)
        self.connect(self.parametersPanelAltitude.chbInsertPointAndText, SIGNAL("Event_0"), self.chbInsertPointAndText_Event_0)
        self.connect(self.parametersPanel.pnlConstructionType, SIGNAL("Event_0"), self.pnlConstructionType_Event_0)
        self.ui.tabCtrlGeneral.currentChanged.connect(self.tabControl_SelectedIndexChanged)
        self.connect(self.parametersPanel.chbSecondSlope, SIGNAL("Event_0"), self.chbSecondSlope_Event_0)
        self.connect(self.parametersPanel.chbDepTrackMoreThan15, SIGNAL("Event_0"), self.chbDepTrackMoreThan15_Event_0)
        self.connect(self.parametersPanel.pnlApproachObstacleAltitude, SIGNAL("Event_0"), self.pnlApproachObstacleAltitude_Event_0)
        #
        self.connect(self.parametersPanel.pnlApproachType, SIGNAL("Event_0"), self.pnlApproachType_Event_0)
        self.connect(self.parametersPanel.pnlCriteria, SIGNAL("Event_0"), self.pnlCriteria_Event_0)
        self.connect(self.parametersPanel.chbLetterF, SIGNAL("Event_0"), self.chbLetterF_Click0)
        self.connect(self.parametersPanel.pnlDatumElevation, SIGNAL("Event_0"), self.pnlDatumElevation_Event_0)
        self.connect(self.parametersPanel.pnlRwyCode, SIGNAL("Event_0"), self.pnlRwyCode_Event_0)
        self.connect(self.parametersPanel.pnlRunway, SIGNAL("Event_0"), self.pnlRunway_Event_0)
        self.connect(self.parametersPanelAltitude.pnlEvalMode, SIGNAL("Event_0"), self.pnlEvalMode_Event_0)
        # self.connect(self.parametersPanel.pnlVPA, SIGNAL("Event_0"), self.pnlVPA_Event_0)
        # self.connect(self.parametersPanel.pnlRDH, SIGNAL("Event_0"), self.pnlRDH_Event_0)
        # self.connect(self.parametersPanel.pnlOCAH, SIGNAL("Event_0"), self.pnlOCAH_Event_0)
        # self.connect(self.parametersPanel.pnlRwyDir, SIGNAL("Event_0"), self.pnlRwyDir_Event_0)
        # self.connect(self.parametersPanel.pnlThr, SIGNAL("positionChanged"), self.pnlThr_Event_0)
        self.connect(self.parametersPanel.pnlARP, SIGNAL("positionChanged"), self.pnlARP_Event_1)
        # self.connect(self.parametersPanel.pnlMinTemp, SIGNAL("Event_0"), self.pnlMinTemp_Event_0)
        #
        #
        #
        # self.ui.cmbUnits.currentIndexChanged.connect(self.setCriticalObstacle)
        self.parametersPanel.btnCriteriaModify.clicked.connect(self.btnCriteriaModify_Click)
        self.parametersPanel.btnCriteriaRemove.clicked.connect(self.btnCriteriaRemove_Click)
        self.parametersPanel.btnRwyAdd.clicked.connect(self.btnRwyAdd_Click)
        self.parametersPanel.btnRwyModify.clicked.connect(self.btnRwyModify_Click)
        self.parametersPanel.btnRwyRemove.clicked.connect(self.btnRwyRemove_Click)
        self.method_33()
    
    def btnCriteriaModify_Click(self):
        if (self.parametersPanel.pnlCriteria.SelectedIndex < 0):
            return
        aerodromeSurfacesCriterium = self.method_41(True)
        result, aerodromeSurfacesCriterium = DlgAerodromeSurfacesCriteria.smethod_0(self, aerodromeSurfacesCriterium)
        if (result):
            if (self.parametersPanel.pnlCriteria.IndexOf(aerodromeSurfacesCriterium) == -1):
                AerodromeSurfacesDlg.criteria.Add(aerodromeSurfacesCriterium)
            AerodromeSurfacesDlg.criteria.method_0(self)
            AerodromeSurfacesDlg.criteria.method_1()
            self.method_38(aerodromeSurfacesCriterium)
            self.method_33()
            
    def btnCriteriaRemove_Click(self):
        selectedItem = self.parametersPanel.pnlCriteria.SelectedItem
        if (selectedItem == None):
            return
        if (selectedItem.Criteria != AerodromeSurfacesCriteriaType.Custom):
            return
        if (QMessageBox.question(self, "Question", Confirmations.DELETE_CRITERIA.format(selectedItem.Name), QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes):
            num = self.parametersPanel.pnlCriteria.IndexOf(selectedItem)
            AerodromeSurfacesDlg.criteria.Remove(selectedItem)
            AerodromeSurfacesDlg.criteria.method_0(self)
            num = min(num, self.parametersPanel.pnlCriteria.Count - 1)
            self.method_37(num)
            self.method_33()
    
    def btnRwyAdd_Click(self):
        runway = Runway()
        self.dlgRunway = DlgRunway.smethod_0(self, runway)
        self.connect(self.dlgRunway, SIGNAL("DlgRunway_accept"), self.DlgRunway_acceptEvent)
    def DlgRunway_acceptEvent(self, runway):
        self.dlgRunway.close()
        AerodromeSurfacesDlg.runways.Add(runway)
        AerodromeSurfacesDlg.runways.method_0(self)
        AerodromeSurfacesDlg.runways.method_1()
        self.method_36(runway)
    def btnRwyModify_Click(self):
        selectedItem = self.parametersPanel.pnlRunway.SelectedItem
        if (selectedItem == None):
            return
        self.runwayIndex = AerodromeSurfacesDlg.runways.IndexOf(selectedItem)
        self.dlgRunway = DlgRunway.smethod_0(self, selectedItem)
        self.connect(self.dlgRunway, SIGNAL("DlgRunway_accept"), self.DlgRunway_acceptEvent1)
    def DlgRunway_acceptEvent1(self, runway):
        self.dlgRunway.close()
        AerodromeSurfacesDlg.runways[self.runwayIndex] = runway
        AerodromeSurfacesDlg.runways.method_0(self)
        AerodromeSurfacesDlg.runways.method_1()
        self.method_36(runway)
    def btnRwyRemove_Click(self):
        selectedItem = self.parametersPanel.pnlRunway.SelectedItem
        if (selectedItem == None):
            return
        if (QMessageBox.question(self, "Question", Confirmations.DELETE_RUNWAY.format(selectedItem.FullName), QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes):
            num = self.parametersPanel.pnlRunway.IndexOf(selectedItem)
            AerodromeSurfacesDlg.runways.Remove(selectedItem)
            AerodromeSurfacesDlg.runways.method_0(self)
            num = min(num, self.parametersPanel.pnlRunway.Count - 1)
            self.method_35(num)
    
    def pnlEvalMode_Event_0(self):
        self.chbLetterF_Click(self.parametersPanelAltitude.pnlEvalMode)
    def pnlRunway_Event_0(self):
        self.chbLetterF_Click(self.parametersPanel.pnlRunway)
    def pnlRwyCode_Event_0(self):
        self.chbLetterF_Click(self.parametersPanel.pnlRwyCode)
    def pnlDatumElevation_Event_0(self):
        self.chbLetterF_Click(self.parametersPanel.pnlDatumElevation)
    def pnlARP_Event_1(self):
        self.chbLetterF_Click(self.parametersPanel.pnlARP)
    def chbLetterF_Click0(self):
        self.chbLetterF_Click(self.parametersPanel.chbLetterF)
    def pnlCriteria_Event_0(self):
        self.chbLetterF_Click(self.parametersPanel.pnlCriteria)
    def pnlApproachType_Event_0(self):
        self.chbLetterF_Click(self.parametersPanel.pnlApproachType)
    def pnlApproachObstacleAltitude_Event_0(self):
        self.chbLetterF_Click(self.parametersPanel.pnlApproachObstacleAltitude)
    def chbDepTrackMoreThan15_Event_0(self):
        self.chbLetterF_Click(self.parametersPanel.chbDepTrackMoreThan15)
    def chbSecondSlope_Event_0(self):
        self.chbLetterF_Click(self.parametersPanel.chbSecondSlope)
    def pnlConstructionType_Event_0(self):
        self.chbLetterF_Click(self.parametersPanel.pnlConstructionType)
    def chbMarkAltitudes_Event_0(self):
        self.parametersPanel.pnlAltitudesEvery.Enabled = self.parametersPanel.chbMarkAltitudes.Checked
    def chbInsertPointAndText_Event_0(self):
        self.parametersPanelAltitude.pnlTextHeight.Enabled = self.parametersPanelAltitude.chbInsertPointAndText.Checked
    def tabControl_SelectedIndexChanged(self):
        # self.method_32()
        self.method_33()
    def chbLetterF_Click(self, sender):
        if (sender != self.parametersPanelAltitude.pnlEvalMode):
            self.method_31()
        else:
            self.method_34()
        if (sender == self.parametersPanel.pnlRunway):
            self.method_39()
        elif (sender == self.parametersPanel.pnlCriteria):
            self.method_40()
        self.method_33()
    
    def method_31(self):
        if (not self.updating):
            if (self.parametersPanelAltitude.pnlEvalMode.SelectedIndex == 0):
                AerodromeSurfacesDlg.singleObstaclesChecked = 0
                # AerodromeSurfacesDlg.singleObstacles.Clear()
                return
            # self.gridObstacles.DataSource = None
            self.ui.cmbObstSurface.clear()
            for multiObstacle in AerodromeSurfacesDlg.multiObstacles:
                if (multiObstacle == None):
                    continue
                # multiObstacle.Dispose()
            AerodromeSurfacesDlg.multiObstacles = []
    
    def method_33(self):
        if (self.ui.tabCtrlGeneral.currentIndex() != 0):
            selectedIndex = self.parametersPanelAltitude.pnlEvalMode.SelectedIndex == 0
            self.parametersPanelAltitude.pnlEvalPosition.Visible = selectedIndex
            self.parametersPanelAltitude.pnlInsertPointAndText.Visible = selectedIndex
            self.parametersPanelAltitude.chbOnlyPenetratingObstacles.Visible = not selectedIndex
        else:
            flag = self.parametersPanel.pnlCriteria.SelectedIndex < 2
            self.parametersPanel.pnlApproachType.Visible = flag
            self.parametersPanel.pnlApproachObstacleAltitude.Visible = flag
            self.parametersPanel.chbDepTrackMoreThan15.Visible = flag
            self.parametersPanel.chbSecondSlope.Visible = flag
            self.parametersPanel.pnlMarkAltitudes.Visible = self.parametersPanel.pnlConstructionType.SelectedItem == ConstructionType.Construct2D
    def method_34(self):
        if (self.parametersPanelAltitude.pnlEvalMode.SelectedIndex == 0):
            self.ui.frm_cmbObstSurface.setVisible(False)
            # self.gridObstacles.DataSource = AerodromeSurfacesDlg.singleObstacles
            return
        # self.gridObstacles.DataSource = None
        self.ui.frm_cmbObstSurface.setVisible(True)
        self.ui.cmbObstSurface.clear()
        self.ui.cmbObstSurface.addItem("")
        for multiObstacle in AerodromeSurfacesDlg.multiObstacles:
            self.ui.cmbObstSurface.addItem(multiObstacle.title)
        if (self.ui.cmbObstSurface.count() > 0):
            self.ui.cmbObstSurface.setCurrentIndex(0)
            # self.gridObstacles.DataSource = AerodromeSurfacesDlg.multiObstacles[0]
    def method_35(self, int_0):
        self.updating = True
        if (self.parametersPanel.pnlRunway.Items != []):
            self.parametersPanel.pnlRunway.Clear()
        self.parametersPanel.pnlRunway.Items = AerodromeSurfacesDlg.runways
        # self.pnlRunway.DisplayMember = "FullName"
        if (self.parametersPanel.pnlRunway.Count > 0):
            int_0 = max(int_0, 0)
            int_0 = min(int_0, self.parametersPanel.pnlRunway.Count - 1)
            self.parametersPanel.pnlRunway.SelectedIndex = int_0
        self.method_39()
        self.updating = False
    
    def method_36(self, runway_0):
        self.updating = True
        if (self.parametersPanel.pnlRunway.Items != []):
            self.parametersPanel.pnlRunway.Clear()
        self.parametersPanel.pnlRunway.Items = AerodromeSurfacesDlg.runways
        # self.parametersPanel.pnlRunway.DisplayMember = "FullName"
        self.parametersPanel.pnlRunway.SelectedIndex = self.parametersPanel.pnlRunway.IndexOf(runway_0)
        self.method_39()
        self.updating = False
    
    def method_37(self, int_0):
        self.updating = True
        if (self.parametersPanel.pnlCriteria.Items != []):
            self.parametersPanel.pnlCriteria.Clear()
        self.parametersPanel.pnlCriteria.Items = AerodromeSurfacesDlg.criteria
        # self.pnlCriteria.DisplayMember = "Name"
        if (self.parametersPanel.pnlCriteria.Count > 0):
            int_0 = max(int_0, 0)
            int_0 = min(int_0, self.parametersPanel.pnlCriteria.Count - 1)
            self.parametersPanel.pnlCriteria.SelectedIndex = int_0
        self.method_40()
        self.updating = False
    
    def method_38(self, aerodromeSurfacesCriteria_0):
        self.updating = True
        if (self.parametersPanel.pnlCriteria.Items != []):
            self.parametersPanel.pnlCriteria.Clear()
        self.parametersPanel.pnlCriteria.Items = AerodromeSurfacesDlg.criteria
        # self.pnlCriteria.DisplayMember = "Name"
        self.parametersPanel.pnlCriteria.SelectedIndex = self.parametersPanel.pnlCriteria.IndexOf(aerodromeSurfacesCriteria_0)
        self.method_40()
        self.updating = False
    
    def method_39(self):
        self.parametersPanel.btnRwyModify.setEnabled(self.parametersPanel.pnlRunway.SelectedIndex > -1)
        self.parametersPanel.btnRwyRemove.setEnabled(self.parametersPanel.pnlRunway.SelectedIndex > -1)

    def method_40(self):
        self.parametersPanel.btnCriteriaModify.setEnabled(self.parametersPanel.pnlCriteria.SelectedIndex > -1)
        self.parametersPanel.btnCriteriaRemove.setEnabled(self.parametersPanel.pnlCriteria.SelectedIndex > 1)
    def method_41(self, bool_0):
        selectedItem = self.parametersPanel.pnlCriteria.SelectedItem
        if (selectedItem.Criteria != AerodromeSurfacesCriteriaType.Custom):
            aerodromeSurfacesApproachType = AerodromeSurfacesApproachType.Precision
            if (self.parametersPanel.pnlApproachType.SelectedIndex == 0):
                aerodromeSurfacesApproachType = AerodromeSurfacesApproachType.NonInstrument
            elif (self.parametersPanel.pnlApproachType.SelectedIndex == 1):
                aerodromeSurfacesApproachType = AerodromeSurfacesApproachType.NonPrecision
            aerodromeSurfacesRunwayCode = AerodromeSurfacesRunwayCode.Code4
            if (self.parametersPanel.pnlRwyCode.SelectedIndex == 0):
                aerodromeSurfacesRunwayCode = AerodromeSurfacesRunwayCode.Code1
            elif (self.parametersPanel.pnlRwyCode.SelectedIndex == 1):
                aerodromeSurfacesRunwayCode = AerodromeSurfacesRunwayCode.Code2
            elif (self.parametersPanel.pnlRwyCode.SelectedIndex == 2):
                aerodromeSurfacesRunwayCode = AerodromeSurfacesRunwayCode.Code3
            metres = 0.0
            flag = False
            runway = self.parametersPanel.pnlRunway.SelectedItem
            if (runway != None):
                metres = runway.method_3(True).Metres
                flag = runway.method_5(PositionType.CWY)
            if (not bool_0):
                selectedItem.method_0(selectedItem.Criteria, aerodromeSurfacesApproachType, aerodromeSurfacesRunwayCode, metres, self.parametersPanel.chbLetterF.Checked, self.parametersPanel.chbDepTrackMoreThan15.Checked, self.parametersPanel.chbSecondSlope.Checked, flag)
            else:
                selectedItem = AerodromeSurfacesCriteria(selectedItem.Criteria, aerodromeSurfacesApproachType, aerodromeSurfacesRunwayCode, metres, self.parametersPanel.chbLetterF.Checked, self.parametersPanel.chbDepTrackMoreThan15.Checked, self.parametersPanel.chbSecondSlope.Checked, flag)
        return selectedItem
    
    def method_42(self, runway_0):
        value = self.parametersPanel.pnlDatumElevation.SelectedItem
        if (value == "Arp"):
            return self.parametersPanel.pnlARP.Altitude()
        if (value == "Thr"):
            return runway_0.method_4(PositionType.THR).AltitudeValue
        if (value == "End"):
            return runway_0.method_4(PositionType.END).AltitudeValue
        if (not value == "Thr_End"):
            return Altitude.smethod_0(value, AltitudeUnits.M)
        position = runway_0.method_4(PositionType.THR)
        position1 = runway_0.method_4(PositionType.END)
        if (position.AltitudeValue.Metres < position1.AltitudeValue.Metres):
            return position.AltitudeValue
        return position1.AltitudeValue
        
class AerodromeSurfacesSingleObstacles(ObstacleTable):
    def __init__(self, surfacesList = None):
        ObstacleTable.__init__(self, None)

        self.surfaces = surfacesList

    def setHiddenColumns(self, tableView):
#         tableView.hideColumn(self.IndexObstArea)
#         tableView.hideColumn(self.IndexDistInSecM)
        return ObstacleTable.setHiddenColumns(self, tableView)
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)

        self.IndexSurfaceName = fixedColumnCount
        self.IndexSurfAltM = fixedColumnCount + 1
        self.IndexSurfAltFt = fixedColumnCount + 2
        self.IndexDifferenceM = fixedColumnCount + 3
        self.IndexDifferenceFt = fixedColumnCount + 4
        self.IndexCritical = fixedColumnCount + 5

        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.SurfaceName,
                ObstacleTableColumnType.SurfAltM,
                ObstacleTableColumnType.SurfAltFt,
                ObstacleTableColumnType.DifferenceM,
                ObstacleTableColumnType.DifferenceFt,
                ObstacleTableColumnType.Critical
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)

    def addObstacleToModel(self, obstacle, checkResult):
        ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
        row = self.source.rowCount() - 1

        item = QStandardItem(str(checkResult[0]))
        item.setData(checkResult[0])
        self.source.setItem(row, self.IndexSurfaceName, item)

        item = QStandardItem(str(checkResult[1]))
        item.setData(checkResult[1])
        self.source.setItem(row, self.IndexSurfAltM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[1])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[1]))
        self.source.setItem(row, self.IndexSurfAltFt, item)

        item = QStandardItem(str(checkResult[2]))
        item.setData(checkResult[2])
        self.source.setItem(row, self.IndexDifferenceM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[2])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[2]))
        self.source.setItem(row, self.IndexDifferenceFt, item)

        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexCritical, item)

    def checkObstacle(self, obstacle_0):
        pass
    
    def method_0(self, obstacle_0, string_0):
        num = None
        num1 = None
        flag = False
        AerodromeSurfacesDlg.singleObstaclesChecked = AerodromeSurfacesDlg.singleObstaclesChecked + 1
        flag1 = False
        for current in self.surfaces:
        # List<AerodromeSurfaces.IAerodromeSurfacesSurface>.Enumerator enumerator = this.surfaces.GetEnumerator()
        # try
        # {
        #     while (enumerator.MoveNext())
        #     {
        #     current = enumerator.Current
            result, num, num1 = current.vmethod_2(obstacle_0)
            if (not result):
                continue
            criticalObstacleType = CriticalObstacleType.No
            if (num1 > 0):
                criticalObstacleType = CriticalObstacleType.Yes
            checkResults = [current.Title, num, num1, criticalObstacleType]
            self.addObstacleToModel(obstacle_0, checkResults)
            # AerodromeSurfaces.singleObstacles.method_11(obstacle_0, )
            string_0 = current.method_0(string_0, obstacle_0, num, num1)
            if (isinstance(current ,InnerHorizontalSurface) or isinstance(current ,ConicalSurface) or isinstance(current ,OuterHorizontalSurface)):
                flag = True
                return flag, string_0
            else:
                flag1 = True
        return flag1, string_0

class AerodromeSurfacesMultiObstacles(ObstacleTable):
    def __init__(self, surfacesList, bool_0, title = ""):
        ObstacleTable.__init__(self, None)
        self.surfaces = surfacesList
        self.onlyPenetratingObstacles = bool_0

    def setHiddenColumns(self, tableView):

        # tableView.hideColumn(self.IndexSurfaceName)
#         tableView.hideColumn(self.IndexDistInSecM)
        return ObstacleTable.setHiddenColumns(self, tableView)
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)

        self.IndexSurfaceName = fixedColumnCount
        self.IndexSurfAltM = fixedColumnCount + 1
        self.IndexSurfAltFt = fixedColumnCount + 2
        self.IndexDifferenceM = fixedColumnCount + 3
        self.IndexDifferenceFt = fixedColumnCount + 4
        self.IndexCritical = fixedColumnCount + 5

        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.SurfaceName,
                ObstacleTableColumnType.SurfAltM,
                ObstacleTableColumnType.SurfAltFt,
                ObstacleTableColumnType.DifferenceM,
                ObstacleTableColumnType.DifferenceFt,
                ObstacleTableColumnType.Critical
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)

    def addObstacleToModel(self, obstacle, checkResult):
        ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
        row = self.source.rowCount() - 1

        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexSurfaceName, item)

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

    def checkObstacle(self, obstacle_0):
        num = None
        num1 = None
        AerodromeSurfacesDlg.multiObstaclesChecked = AerodromeSurfacesDlg.multiObstaclesChecked + 1
        num2 = 0
        for surface in self.surfaces:
            checkResult = []
            result, num, num1 = surface.vmethod_2(obstacle_0)
            if (result):
                criticalObstacleType = CriticalObstacleType.No
                if (num1 > 0):
                    criticalObstacleType = CriticalObstacleType.Yes
                if (not self.onlyPenetratingObstacles or (self.onlyPenetratingObstacles and criticalObstacleType == CriticalObstacleType.Yes)):
                    checkResult = [num, num1, criticalObstacleType, surface.title]
                    self.addObstacleToModel(obstacle_0, checkResult)
                    # AerodromeSurfacesDlg.multiObstacles[num2].method_11(obstacle_0, num, num1, criticalObstacleType)
                if (isinstance(surface, InnerHorizontalSurface) or isinstance(surface ,ConicalSurface) or isinstance(surface ,OuterHorizontalSurface)):
                    return
            num2 += 1


class IAerodromeSurfacesSurface:
    def __init__(self):
        self.centerLine = Point3dCollection()
        self.area = Point3dCollection()
        self.indexRwyStart = 0
        self.indexRwyThr = 0
        self.indexRwyEnd = 0
        self.indexLast = 0
        self.rwyDirection = 0.0
        self.textHeight = 0.0
        self.rwyName = ""
        self.layerName2D = ""
        self.layerName3D = ""
        self.title = ""
        self.altitudeFormat = ""

    def get_AltitudeFormat(self):
        return self.altitudeFormat
    def set_AltitudeFormat(self, val):
        self.altitudeFormat = val
    AltitudeFormat = property(get_AltitudeFormat, set_AltitudeFormat, None, None)

    def get_Area(self):
        return self.area
    Area = property(get_Area, None, None, None)

    def get_TextHeight(self):
        return self.textHeight
    def set_TextHeight(self, val):
        self.textHeight = val
    TextHeight = property(get_TextHeight, set_TextHeight, None, None)

    def get_Title(self):
        return self.title
    Title = property(get_Title, None, None, None)

    def method_0(self, string_0, obstacle_0, double_0, double_1):
        if (not String.IsNullOrEmpty(string_0)):
            string_0 = String.Concat([string_0, "\n"])
        bELOW = Formating.BELOW
        if (double_1 >= 0):
            dIFFERENCE = Formating.DIFFERENCE
            altitude = Altitude(double_1)
            bELOW = dIFFERENCE.format(altitude.method_0(":u"))
        name = [obstacle_0.Name, None, None, None, None, None]
        position = obstacle_0.Position
        altitude1 = Altitude(position.get_Z() + obstacle_0.Trees)
        name[1] = altitude1.method_0(":u")
        name[2] = self.rwyName
        name[3] = self.title
        altitude2 = Altitude(double_0)
        name[4] = altitude2.method_0(":u")
        name[5] = bELOW
        string_0 = String.Concat([string_0, "{0}, {1}, {2} {3} ({4}), {5}".format(name[0], name[1], name[2], name[3], name[4], name[5])])
        return string_0
        
    def method_1(self, runway_0, stripSurfaceCriteria_0):
        self.rwyName = runway_0.FullName
        self.layerName2D = AcadHelper.smethod_46("{0}_{1}_2D".format(String.QString2Str(runway_0.FullName), self.title))
        self.layerName3D = AcadHelper.smethod_46("{0}_{1}_3D".format(String.QString2Str(runway_0.FullName), self.title))
        self.rwyDirection = runway_0.Direction
        self.centerLine = Point3dCollection()
        self.centerLine.Add(MathHelper.distanceBearingPoint(runway_0.method_4(PositionType.START).Point3d, self.rwyDirection - math.pi, stripSurfaceCriteria_0.Length))
        self.centerLine.smethod_145(runway_0.Point3dCollectionValue)
        if (runway_0.method_5(PositionType.CWY)):
            self.centerLine.RemoveAt(self.centerLine.get_Count() - 1)
        self.centerLine.Add(MathHelper.distanceBearingPoint(runway_0.method_4(PositionType.SWY).Point3d, self.rwyDirection, stripSurfaceCriteria_0.Length))
        self.indexRwyStart = 1
        if (not runway_0.method_5(PositionType.START)):
            self.indexRwyThr = 1
        else:
            self.indexRwyThr = 2
        self.indexLast = self.centerLine.get_Count() - 1
        self.indexRwyEnd = self.indexLast - 1
        if (runway_0.method_5(PositionType.SWY)):
            aerodromeSurfacesSurface = self
            aerodromeSurfacesSurface.indexRwyEnd = aerodromeSurfacesSurface.indexRwyEnd - 1

# 
    def method_10(self, obstacle_0):
        point3d = None
        point3d1 = None
        num = self.method_9()
        point3d2 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.rwyDirection - math.pi, obstacle_0.Tolerance)
        point3d3 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.rwyDirection, obstacle_0.Tolerance)
        for i in range(self.centerLine.get_Count()):
            item = self.centerLine.get_Item(i - 1)
            item1 = self.centerLine.get_Item(i)
            point3d = MathHelper.getIntersectionPoint(point3d2, MathHelper.distanceBearingPoint(point3d2, self.rwyDirection - math.pi / 2, 100), item, item1)
            point3d1 = MathHelper.getIntersectionPoint(point3d3, MathHelper.distanceBearingPoint(point3d3, self.rwyDirection - math.pi / 2, 100), item, item1)
            num1 = MathHelper.calcDistance(item, item1)
            if (MathHelper.smethod_110(point3d, item, item1)):
                z = item.get_Z() + MathHelper.calcDistance(item, point3d) * ((item1.get_Z() - item.get_Z()) / num1)
                num = min(z, num)
            if (MathHelper.smethod_110(point3d1, item, item1)):
                z1 = item.get_Z() + MathHelper.calcDistance(item, point3d1) * ((item1.get_Z() - item.get_Z()) / num1)
                num = min(z1, num)
        return num

    def method_11(self, point3d_0, point3d_1, point3d_2, double_0):
        num = max(MathHelper.calcDistance(point3d_0, point3d_2) - double_0, 0)
        num1 = MathHelper.calcDistance(point3d_0, point3d_1)
        if (MathHelper.smethod_96(num1)):
            return point3d_0.get_Z()
        return point3d_0.get_Z() + (point3d_1.get_Z() - point3d_0.get_Z()) / num1 * num


    def method_12(self, obstacle_0, point3dCollection_0, point3dCollection_1):
        point3d = None
        point3d1 = None
        point3d2 = None
        point3d3 = None
        point3d4 = None
        point3d5 = None
        z = point3dCollection_1.get_Item(0).get_Z()
        for point3dCollection1 in point3dCollection_1:
            z = max(z, point3dCollection1.get_Z())
        point3d6 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.rwyDirection - math.pi, obstacle_0.Tolerance)
        position = obstacle_0.Position
        point3d7 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.rwyDirection, obstacle_0.Tolerance)
        for i in range(point3dCollection_0.get_Count()):
            item = point3dCollection_0.get_Item(i - 1)
            item1 = point3dCollection_0.get_Item(i)
            item2 = point3dCollection_1.get_Item(i - 1)
            item3 = point3dCollection_1.get_Item(i)
            point3d = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, self.rwyDirection - math.pi / 2, 100), item, item1)
            point3d1 = MathHelper.getIntersectionPoint(position, MathHelper.distanceBearingPoint(position, self.rwyDirection - math.pi / 2, 100), item, item1)
            point3d2 = MathHelper.getIntersectionPoint(point3d7, MathHelper.distanceBearingPoint(point3d7, self.rwyDirection - math.pi / 2, 100), item, item1)
            point3d3 = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, self.rwyDirection - math.pi / 2, 100), item2, item3)
            point3d4 = MathHelper.getIntersectionPoint(position, MathHelper.distanceBearingPoint(position, self.rwyDirection - math.pi / 2, 100), item2, item3)
            point3d5 = MathHelper.getIntersectionPoint(point3d7, MathHelper.distanceBearingPoint(point3d7, self.rwyDirection - math.pi / 2, 100), item2, item3)
            num = MathHelper.calcDistance(item, item1)
            num1 = MathHelper.calcDistance(item2, item3)
            if (MathHelper.smethod_110(point3d, item, item1)):
                z1 = item.get_Z() + MathHelper.calcDistance(item, point3d) * ((item1.get_Z() - item.get_Z()) / num)
                z2 = item2.get_Z() + MathHelper.calcDistance(item2, point3d3) * ((item3.get_Z() - item2.get_Z()) / num1)
                num2 = self.method_11(point3d.smethod_167(z1), point3d3.smethod_167(z2), point3d6, obstacle_0.Tolerance)
                z = min(num2, z)
            if (MathHelper.smethod_110(point3d1, item, item1)):
                z3 = item.get_Z() + MathHelper.calcDistance(item, point3d1) * ((item1.get_Z() - item.get_Z()) / num)
                num3 = item2.get_Z() + MathHelper.calcDistance(item2, point3d4) * ((item3.get_Z() - item2.get_Z()) / num1)
                num4 = self.method_11(point3d1.smethod_167(z3), point3d4.smethod_167(num3), position, obstacle_0.Tolerance)
                z = min(num4, z)
            if (MathHelper.smethod_110(point3d2, item, item1)):
                z4 = item.get_Z() + MathHelper.calcDistance(item, point3d2) * ((item1.get_Z() - item.get_Z()) / num)
                z5 = item2.get_Z() + MathHelper.calcDistance(item2, point3d5) * ((item3.get_Z() - item2.get_Z()) / num1)
                num5 = self.method_11(point3d2.smethod_167(z4), point3d5.smethod_167(z5), point3d7, obstacle_0.Tolerance)
                z = min(num5, z)
        return z

    def method_13(self, point3d_0, altitude_0, point3d_1, point3d_2, bool_0, constructionLayer):
        dBText = AcadHelper.smethod_140(altitude_0.method_0(self.altitudeFormat), point3d_0.smethod_167(0), self.textHeight, 1, 1)
        num = MathHelper.getBearing(point3d_1, point3d_2)
        if (not MathHelper.smethod_136(num, AngleUnits.Radians)):
            num = num - math.pi
        dBText.set_Rotation(7.85398163397448 - num)
        constructionLayer.setLayerName(self.layerName2D)
        AcadHelper.smethod_18(dBText, constructionLayer)
        if (bool_0):
            AcadHelper.smethod_18(Line(point3d_1.smethod_167(0), point3d_2.smethod_167(0)), constructionLayer)
# 
    def method_14(self, point3d_0, altitude_0, double_0, constructionLayer):
        dBText = AcadHelper.smethod_140(altitude_0.method_0(self.altitudeFormat), point3d_0.smethod_167(0), self.textHeight, 1, 1)
        if (not MathHelper.smethod_136(double_0, AngleUnits.Radians)):
            double_0 = double_0 - math.pi
        dBText.set_Rotation(7.85398163397448 - double_0)
        constructionLayer.setLayerName(self.layerName2D)
        AcadHelper.smethod_18(dBText, constructionLayer)

    def method_15(self, point3d_0, point3d_1, point3d_2, point3d_3, altitude_0, double_0, double_1, double_2, bool_0, bool_1, constructionLayer):
        point3d = None
        point3d1 = None
        num = min(point3d_0.get_Z(), point3d_1.get_Z())
        metres = math.trunc(num / altitude_0.Metres) * altitude_0.Metres
        if (metres < num):
            metres = metres + altitude_0.Metres
        num1 = max(point3d_2.get_Z(), point3d_3.get_Z())
        point3d2 = MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_1), MathHelper.calcDistance(point3d_0, point3d_1) / 2)
        if (bool_0 or MathHelper.smethod_98(num, metres)):
            self.method_13(point3d2, Altitude(num), point3d_0, point3d_1, False, constructionLayer)
        while (metres < num1):
            num2 = MathHelper.smethod_192(num, math.atan(double_0 / 100), metres, double_2, 0)
            if (num2 >= double_2):
                break
            point3d3 = MathHelper.distanceBearingPoint(point3d_0, double_1, num2)
            point3d4 = MathHelper.distanceBearingPoint(point3d_1, double_1, num2)
            point3d = MathHelper.getIntersectionPoint(point3d_0, point3d_2, point3d3, point3d4)
            point3d1 = MathHelper.getIntersectionPoint(point3d_1, point3d_3, point3d3, point3d4)
            point3d2 = MathHelper.distanceBearingPoint(point3d, MathHelper.getBearing(point3d, point3d1), MathHelper.calcDistance(point3d, point3d1) / 2)
            self.method_13(point3d2, Altitude(metres), point3d, point3d1, True, constructionLayer)
            metres = metres + altitude_0.Metres
        point3d2 = MathHelper.distanceBearingPoint(point3d_2, MathHelper.getBearing(point3d_2, point3d_3), MathHelper.calcDistance(point3d_2, point3d_3) / 2)
        if (bool_1):
            self.method_13(point3d2, Altitude(num1), point3d_2, point3d_3, False, constructionLayer)

    def method_16(self, point3dCollection_0, point3dCollection_1, altitude_0, double_0, double_1, int_0, constructionLayer):
        point3d = None
        count = point3dCollection_0.get_Count()
        for i in range(count):
            item = point3dCollection_0.get_Item(i - 1)
            item1 = point3dCollection_1.get_Item(i - 1)
            point3d1 = point3dCollection_0.get_Item(i)
            item2 = point3dCollection_1.get_Item(i)
            z = min(item.get_Z(), point3d1.get_Z())
            if (item.get_Z() > point3d1.get_Z()):
                item, point3d1 = MathHelper.smethod_184(item, point3d1)
                item1, item2 = MathHelper.smethod_184(item1, item2)
            metres = math.trunc(z / altitude_0.Metres) * altitude_0.Metres
            if (metres < z):
                metres = metres + altitude_0.Metres
            num = max(item1.get_Z(), item2.get_Z())
            if (not MathHelper.smethod_102(point3d1, item2)):
                z1 = (item1.get_Z() - item.get_Z()) / (double_0 / 100)
                num1 = (item2.get_Z() - point3d1.get_Z()) / (double_0 / 100)
                while (metres < num):
                    num2 = MathHelper.smethod_192(item.get_Z(), math.atan(double_0 / 100), metres, z1, 0)
                    if (num2 >= z1):
                        break
                    num3 = MathHelper.smethod_192(point3d1.get_Z(), math.atan(double_0 / 100), metres, num1, 0)
                    if (num3 >= num1):
                        break
                    point3d2 = MathHelper.distanceBearingPoint(item, double_1, num2)
                    point3d3 = MathHelper.distanceBearingPoint(point3d1, double_1, num3)
                    if (num2 < 0):
                        point3d2 = MathHelper.getIntersectionPoint(item, point3d1, point3d2, point3d3)
                    if (num3 < 0):
                        point3d3 = MathHelper.getIntersectionPoint(item, point3d1, point3d2, point3d3)
                    constructionLayer.setLayerName(self.layerName2D)
                    AcadHelper.smethod_18(Line(point3d2.smethod_167(0), point3d3.smethod_167(0)), constructionLayer)
                    metres = metres + altitude_0.Metres
            else:
                point3d = MathHelper.getIntersectionPoint(point3d1, MathHelper.distanceBearingPoint(point3d1, self.rwyDirection + math.pi / 2, 100), item, MathHelper.distanceBearingPoint(item, self.rwyDirection, 100))
                num4 = MathHelper.calcDistance(point3d1, point3d)
                num5 = MathHelper.calcDistance(item, point3d)
                num6 = num4 / num5
                z2 = (point3d1.get_Z() - item.get_Z()) / num5 * 100
                num7 = (num - z) / (z2 / 100)
                double0 = (num - z) / (double_0 / 100)
                while (metres < num):
                    num8 = MathHelper.smethod_192(z, math.atan(z2 / 100), metres, num7, 0)
                    if (num8 >= num7):
                        if (i == int_0):
                            num10 = MathHelper.calcDistance(point3dCollection_0.get_Item(0), point3dCollection_1.get_Item(i))
                            z = point3dCollection_0.get_Item(i).get_Z()
                            metres = math.trunc(z / altitude_0.Metres) * altitude_0.Metres
                            if (metres < z):
                                metres = metres + altitude_0.Metres
                            num = point3dCollection_1.get_Item(i).get_Z()
                            item3 = point3dCollection_0.get_Item(i)
                            item4 = point3dCollection_0.get_Item(i)
                            self.method_14(item3, Altitude(item4.get_Z()), self.rwyDirection, constructionLayer)
                            while (metres < num):
                                num11 = MathHelper.smethod_192(z, math.atan(double_0 / 100), metres, num10, 0)
                                if (num11 >= num10):
                                    break
                                point3d6 = MathHelper.distanceBearingPoint(point3dCollection_0.get_Item(i), double_1, num11)
                                self.method_14(point3d6, Altitude(metres), self.rwyDirection, constructionLayer)
                                metres = metres + altitude_0.Metres
                            item5 = point3dCollection_1.get_Item(i)
                            item6 = point3dCollection_1.get_Item(i)
                            self.method_14(item5, Altitude(item6.get_Z()), self.rwyDirection, constructionLayer)
                        return
                    num9 = MathHelper.smethod_192(z, math.atan(double_0 / 100), metres, double0, 0)
                    if (num9 >= double0):
                        if (i == int_0):
                            num10 = MathHelper.calcDistance(point3dCollection_0.get_Item(0), point3dCollection_1.get_Item(i))
                            z = point3dCollection_0.get_Item(i).get_Z()
                            metres = math.trunc(z / altitude_0.Metres) * altitude_0.Metres
                            if (metres < z):
                                metres = metres + altitude_0.Metres
                            num = point3dCollection_1.get_Item(i).get_Z()
                            item3 = point3dCollection_0.get_Item(i)
                            item4 = point3dCollection_0.get_Item(i)
                            self.method_14(item3, Altitude(item4.get_Z()), self.rwyDirection, constructionLayer)
                            while (metres < num):
                                num11 = MathHelper.smethod_192(z, math.atan(double_0 / 100), metres, num10, 0)
                                if (num11 >= num10):
                                    break
                                point3d6 = MathHelper.distanceBearingPoint(point3dCollection_0.get_Item(i), double_1, num11)
                                self.method_14(point3d6, Altitude(metres), self.rwyDirection, constructionLayer)
                                metres = metres + altitude_0.Metres
                            item5 = point3dCollection_1.get_Item(i)
                            item6 = point3dCollection_1.get_Item(i)
                            self.method_14(item5, Altitude(item6.get_Z()), self.rwyDirection, constructionLayer)
                        return
                    point3d4 = MathHelper.distanceBearingPoint(item, MathHelper.getBearing(item, point3d1), num8 / math.cos(math.atan(num6)))
                    point3d5 = MathHelper.distanceBearingPoint(item, double_1, num9)
                    constructionLayer.setLayerName(self.layerName2D)
                    AcadHelper.smethod_18(Line(point3d4.smethod_167(0), point3d5.smethod_167(0)), constructionLayer)
                    metres = metres + altitude_0.Metres
        # Label0:
            if (i == int_0):
                num10 = MathHelper.calcDistance(point3dCollection_0.get_Item(0), point3dCollection_1.get_Item(i))
                z = point3dCollection_0.get_Item(i).get_Z()
                metres = math.trunc(z / altitude_0.Metres) * altitude_0.Metres
                if (metres < z):
                    metres = metres + altitude_0.Metres
                num = point3dCollection_1.get_Item(i).get_Z()
                item3 = point3dCollection_0.get_Item(i)
                item4 = point3dCollection_0.get_Item(i)
                self.method_14(item3, Altitude(item4.get_Z()), self.rwyDirection, constructionLayer)
                while (metres < num):
                    num11 = MathHelper.smethod_192(z, math.atan(double_0 / 100), metres, num10, 0)
                    if (num11 >= num10):
                        break
                    point3d6 = MathHelper.distanceBearingPoint(point3dCollection_0.get_Item(i), double_1, num11)
                    self.method_14(point3d6, Altitude(metres), self.rwyDirection, constructionLayer)
                    metres = metres + altitude_0.Metres
                item5 = point3dCollection_1.get_Item(i)
                item6 = point3dCollection_1.get_Item(i)
                self.method_14(item5, Altitude(item6.get_Z()), self.rwyDirection, constructionLayer)
# 
    def method_2(self, runway_0, aerodromeSurfacesCriteria_0):
        num = self.rwyDirection + math.pi
        point3d = MathHelper.distanceBearingPoint(runway_0.method_4(PositionType.THR).Point3d, num, aerodromeSurfacesCriteria_0.InnerApproach.DistFromTHR)
        point3d1 = MathHelper.distanceBearingPoint(point3d, num - math.pi / 2, aerodromeSurfacesCriteria_0.InnerApproach.Width / 2)
        point3d2 = MathHelper.distanceBearingPoint(point3d, num + math.pi / 2, aerodromeSurfacesCriteria_0.InnerApproach.Width / 2)
        z = point3d1.get_Z() + aerodromeSurfacesCriteria_0.InnerApproach.Length * (aerodromeSurfacesCriteria_0.InnerApproach.Slope / 100)
        point3d3 = MathHelper.distanceBearingPoint(point3d1, num, aerodromeSurfacesCriteria_0.InnerApproach.Length).smethod_167(z)
        z = point3d2.get_Z() + aerodromeSurfacesCriteria_0.InnerApproach.Length * (aerodromeSurfacesCriteria_0.InnerApproach.Slope / 100)
        point3d4 = MathHelper.distanceBearingPoint(point3d2, num, aerodromeSurfacesCriteria_0.InnerApproach.Length).smethod_167(z)
        point3dCollection = Point3dCollection()
        point3dCollection.Add(point3d2)
        point3dCollection.Add(point3d4)
        point3dCollection.Add(point3d3)
        point3dCollection.Add(point3d1)
        return point3dCollection

    def method_3(self, runway_0, aerodromeSurfacesCriteria_0, altitude_0):
        metres = altitude_0.Metres + aerodromeSurfacesCriteria_0.InnerHorizontal.Height
        distFromTHR = aerodromeSurfacesCriteria_0.BalkedLanding.DistFromTHR
        num = runway_0.method_3(True).Metres
        origin = Point3D.get_Origin()
        if (MathHelper.smethod_96(distFromTHR)):
            origin = self.centerLine.get_Item(self.indexLast)
        elif (aerodromeSurfacesCriteria_0.BalkedLanding.DistFromTHRFixed or num > distFromTHR):
            num1 = 0.0
            flag = False
            num2 = self.indexRwyThr + 1
            while (True):
                if (num2 < self.centerLine.get_Count()):
                    item = self.centerLine.get_Item(num2 - 1)
                    point3d = self.centerLine.get_Item(num2)
                    num3 = MathHelper.smethod_21(item, point3d, False)
                    if (num1 + num3 >= distFromTHR):
                        num4 = MathHelper.calcDistance(item, point3d)
                        num5 = math.fabs(item.get_Z() - point3d.get_Z())
                        num6 = math.atan(num5 / num4)
                        num7 = distFromTHR - num1
                        num8 = num7 * math.sin(num6)
                        origin = MathHelper.distanceBearingPoint(item, MathHelper.getBearing(item, point3d), num7).smethod_167(item.get_Z() + num8) if(item.get_Z() <= point3d.get_Z()) else MathHelper.distanceBearingPoint(item, MathHelper.getBearing(item, point3d), num7).smethod_167(item.get_Z() - num8)
                        flag = True
                        break
                    else:
                        num1 = num1 + num3
                        num2 += 1
                else:
                    break
            if (not flag):
                origin = MathHelper.distanceBearingPoint(self.centerLine.get_Item(self.indexLast), self.rwyDirection, distFromTHR - num1)
        else:
            origin = self.centerLine.get_Item(self.indexRwyEnd)
        point3d1 = MathHelper.distanceBearingPoint(origin, self.rwyDirection - math.pi / 2, aerodromeSurfacesCriteria_0.BalkedLanding.InnerEdge / 2)
        point3d2 = MathHelper.distanceBearingPoint(origin, self.rwyDirection + math.pi / 2, aerodromeSurfacesCriteria_0.BalkedLanding.InnerEdge / 2)
        double_0 = (metres - origin.get_Z()) / (float(aerodromeSurfacesCriteria_0.BalkedLanding.Slope) / 100)
        double0 = double_0 / math.cos(math.atan(float(aerodromeSurfacesCriteria_0.BalkedLanding.Divergence) / 100))
        z = point3d1.get_Z() + double_0 * (float(aerodromeSurfacesCriteria_0.BalkedLanding.Slope) / 100)
        point3d3 = MathHelper.distanceBearingPoint(point3d1, self.rwyDirection - math.atan(float(aerodromeSurfacesCriteria_0.BalkedLanding.Divergence) / 100), double0).smethod_167(z)
        z = point3d2.get_Z() + double_0 * (float(aerodromeSurfacesCriteria_0.BalkedLanding.Slope) / 100)
        point3d4 = MathHelper.distanceBearingPoint(point3d2, self.rwyDirection + math.atan(float(aerodromeSurfacesCriteria_0.BalkedLanding.Divergence) / 100), double0).smethod_167(z)
        point3dCollection = Point3dCollection()
        point3dCollection.Add(point3d2)
        point3dCollection.Add(point3d4)
        point3dCollection.Add(point3d3)
        point3dCollection.Add(point3d1)
        return point3dCollection, double_0

    def method_4(self, aerodromeSurfacesCriteria_0, altitude_0):
        point3d = None
        point3dCollection = Point3dCollection()
        num = 0
        num1 = 0
        num2 = 0
        num3 = 0
        num4 = 0
        num5 = 0
        item = self.centerLine.get_Item(self.indexRwyStart)
        item1 = self.centerLine.get_Item(self.indexRwyEnd)
        if (aerodromeSurfacesCriteria_0.InnerHorizontal.Location == AerodromeSurfacesInnerHorizontalLocation.Strip):
            item = self.centerLine.get_Item(0)
            item1 = self.centerLine.get_Item(self.indexLast)
        num6 = MathHelper.getBearing(item, item1)
        if (aerodromeSurfacesCriteria_0.InnerHorizontal.Location == AerodromeSurfacesInnerHorizontalLocation.MidPoint):
            point3d1 = MathHelper.distanceBearingPoint(item, MathHelper.getBearing(item, item1), MathHelper.calcDistance(item, item1) / 2)
            point3d2 = MathHelper.distanceBearingPoint(point3d1, MathHelper.getBearing(item, item1) - math.pi / 2, 100)
            num7 = self.indexRwyStart + 1
            while (num7 <= self.indexRwyEnd):
                item2 = self.centerLine.get_Item(num7 - 1)
                item3 = self.centerLine.get_Item(num7)
                point3d = MathHelper.getIntersectionPoint(item2, item3, point3d1, point3d2)
                if (MathHelper.smethod_110(point3d, item2, item3)):
                    item = point3d
                    item1 = point3d
                    point3d_0 = item.smethod_167(altitude_0.Metres + aerodromeSurfacesCriteria_0.InnerHorizontal.Height)
                    point3d_1 = item1.smethod_167(altitude_0.Metres + aerodromeSurfacesCriteria_0.InnerHorizontal.Height)
                    point3dCollection = Point3dCollection()
                    num = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_0, num6 - math.pi, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius))
                    num1 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_0, num6 - math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius))
                    num2 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_1, num6 - math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius))
                    num3 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_1, num6, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius))
                    num4 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_1, num6 + math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius))
                    num5 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_0, num6 + math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius))
                    return point3dCollection, point3d_0, point3d_1
                else:
                    num7 += 1
        point3d_0 = item.smethod_167(altitude_0.Metres + aerodromeSurfacesCriteria_0.InnerHorizontal.Height)
        point3d_1 = item1.smethod_167(altitude_0.Metres + aerodromeSurfacesCriteria_0.InnerHorizontal.Height)
        point3dCollection = Point3dCollection()
        num = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_0, num6 - math.pi, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius))
        num1 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_0, num6 - math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius))
        num2 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_1, num6 - math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius))
        num3 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_1, num6, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius))
        num4 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_1, num6 + math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius))
        num5 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_0, num6 + math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius))
        return point3dCollection, point3d_0, point3d_1

    def method_5(self, aerodromeSurfacesCriteria_0, altitude_0):
        # point3d
        # double metres
        # Point3dCollection point3dCollection
        # double height
        # int num
        # int num1
        # int num2
        # int num3
        # int num4
        # int num5
        item = self.centerLine.get_Item(self.indexRwyStart)
        item1 = self.centerLine.get_Item(self.indexRwyEnd)
        if (aerodromeSurfacesCriteria_0.InnerHorizontal.Location == AerodromeSurfacesInnerHorizontalLocation.Strip):
            item = self.centerLine.get_Item(0)
            item1 = self.centerLine.get_Item(self.indexLast)
        num6 = MathHelper.getBearing(item, item1)
        if (aerodromeSurfacesCriteria_0.InnerHorizontal.Location == AerodromeSurfacesInnerHorizontalLocation.MidPoint):
            point3d1 = MathHelper.distanceBearingPoint(item, MathHelper.getBearing(item, item1), MathHelper.calcDistance(item, item1) / 2)
            point3d2 = MathHelper.distanceBearingPoint(point3d1, MathHelper.getBearing(item, item1) - math.pi / 2, 100)
            num7 = self.indexRwyStart + 1
            while (num7 <= self.indexRwyEnd):
                item2 = self.centerLine.get_Item(num7 - 1)
                item3 = self.centerLine.get_Item(num7)
                point3d = MathHelper.getIntersectionPoint(item2, item3, point3d1, point3d2)
                if (MathHelper.smethod_110(point3d, item2, item3)):
                    item = point3d
                    item1 = point3d
                    point3d_0 = item.smethod_167(altitude_0.Metres + aerodromeSurfacesCriteria_0.InnerHorizontal.Height)
                    point3d_1 = item1.smethod_167(altitude_0.Metres + aerodromeSurfacesCriteria_0.InnerHorizontal.Height)
                    metres = altitude_0.Metres + aerodromeSurfacesCriteria_0.InnerHorizontal.Height + aerodromeSurfacesCriteria_0.Conical.Height
                    point3dCollection = Point3dCollection()
                    height = aerodromeSurfacesCriteria_0.Conical.Height / (float(aerodromeSurfacesCriteria_0.Conical.Slope) / 100)
                    num = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_0, num6 - math.pi, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius + height).smethod_167(metres))
                    num1 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_0, num6 - math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius + height).smethod_167(metres))
                    num2 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_1, num6 - math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius + height).smethod_167(metres))
                    num3 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_1, num6, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius + height).smethod_167(metres))
                    num4 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_1, num6 + math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius + height).smethod_167(metres))
                    num5 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_0, num6 + math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius + height).smethod_167(metres))
                    return point3dCollection, point3d_0, point3d_1
                else:
                    num7 += 1
        point3d_0 = item.smethod_167(altitude_0.Metres + aerodromeSurfacesCriteria_0.InnerHorizontal.Height)
        point3d_1 = item1.smethod_167(altitude_0.Metres + aerodromeSurfacesCriteria_0.InnerHorizontal.Height)
        metres = altitude_0.Metres + aerodromeSurfacesCriteria_0.InnerHorizontal.Height + aerodromeSurfacesCriteria_0.Conical.Height
        point3dCollection = Point3dCollection()
        height = aerodromeSurfacesCriteria_0.Conical.Height / (float(aerodromeSurfacesCriteria_0.Conical.Slope) / 100)
        num = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_0, num6 - math.pi, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius + height).smethod_167(metres))
        num1 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_0, num6 - math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius + height).smethod_167(metres))
        num2 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_1, num6 - math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius + height).smethod_167(metres))
        num3 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_1, num6, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius + height).smethod_167(metres))
        num4 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_1, num6 + math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius + height).smethod_167(metres))
        num5 = point3dCollection.Add(MathHelper.distanceBearingPoint(point3d_0, num6 + math.pi / 2, aerodromeSurfacesCriteria_0.InnerHorizontal.Radius + height).smethod_167(metres))
        return point3dCollection, point3d_0, point3d_1

    def method_6(self, aerodromeSurfacesCriteria_0):
        num = self.rwyDirection + math.pi
        point3d = MathHelper.distanceBearingPoint(self.centerLine.get_Item(self.indexRwyThr), num, aerodromeSurfacesCriteria_0.Approach.DistFromTHR)
        return MathHelper.distanceBearingPoint(point3d, num - math.pi / 2, float(aerodromeSurfacesCriteria_0.Approach.InnerEdge) / 2)

    def method_7(self, aerodromeSurfacesCriteria_0):
        num = self.rwyDirection + math.pi
        point3d = MathHelper.distanceBearingPoint(self.centerLine.get_Item(self.indexRwyThr), num, aerodromeSurfacesCriteria_0.Approach.DistFromTHR)
        return MathHelper.distanceBearingPoint(point3d, num + math.pi / 2, float(aerodromeSurfacesCriteria_0.Approach.InnerEdge) / 2)

    def method_8(self):
        z = self.centerLine.get_Item(0).get_Z()
        for i in range(1, self.centerLine.get_Count()):
            item = self.centerLine.get_Item(i)
            z = min(z, item.get_Z())
        return z

    def method_9(self):
        z = self.centerLine.get_Item(0).get_Z()
        for i in range(1, self.centerLine.get_Count()):
            item = self.centerLine.get_Item(i)
            z = max(z, item.get_Z())
        return z

    def vmethod_0(self, bool_0, altitude_0):
        pass

    def vmethod_1(self):
        pass

    def vmethod_2(self, obstacle_0):
        pass

class ApproachSurface(IAerodromeSurfacesSurface):
    def __init__(self, runway_0, aerodromeSurfacesCriteria_0, altitude_0):
        IAerodromeSurfacesSurface.__init__(self)
        
        self.title = Captions.APPROACH
        self.method_1(runway_0, aerodromeSurfacesCriteria_0.Strip)
        self.innerEdge = aerodromeSurfacesCriteria_0.Approach.InnerEdge
        self.distFromTHR = aerodromeSurfacesCriteria_0.Approach.DistFromTHR
        self.divergence = float(aerodromeSurfacesCriteria_0.Approach.Divergence)
        self.length1 = float(aerodromeSurfacesCriteria_0.Approach.Length1)
        self.slope1 = float(aerodromeSurfacesCriteria_0.Approach.Slope1)
        self.hasSection2 = aerodromeSurfacesCriteria_0.Approach.HasSection2
        self.length2 = float(aerodromeSurfacesCriteria_0.Approach.Length2)
        self.slope2 = float(aerodromeSurfacesCriteria_0.Approach.Slope2)
        self.length3 = float(aerodromeSurfacesCriteria_0.Approach.Length3)
        self.totalLength = aerodromeSurfacesCriteria_0.Approach.TotalLength
        num = self.rwyDirection + math.pi
        point3d = self.method_6(aerodromeSurfacesCriteria_0)
        point3d1 = self.method_7(aerodromeSurfacesCriteria_0)
        num1 = self.length1 / math.cos(math.atan(float(self.divergence) / 100))
        z = point3d.get_Z() + self.length1 * (float(self.slope1) / 100)
        point3d2 = MathHelper.distanceBearingPoint(point3d, num - math.atan(float(self.divergence) / 100), num1).smethod_167(z)
        z = point3d1.get_Z() + self.length1 * (float(self.slope1) / 100)
        point3d3 = MathHelper.distanceBearingPoint(point3d1, num + math.atan(float(self.divergence) / 100), num1).smethod_167(z)
        self.points3 = None
        self.points1 = Point3dCollection()
        self.points1.Add(point3d1)
        self.points1.Add(point3d3)
        self.points1.Add(point3d2)
        self.points1.Add(point3d)
        if (self.hasSection2):
            point3d = point3d2
            point3d1 = point3d3
            altitude = runway_0.method_4(PositionType.THR).AltitudeValue
            metres = altitude.Metres + 150
            if (altitude_0.IsValid()):
                metres = max(altitude_0.Metres, metres)
            z1 = (metres - point3d.get_Z()) / (float(self.slope2) / 100)
            self.length2 = max(z1, self.length2)
            if (self.totalLength > self.length1 + self.length2):
                self.length3 = self.totalLength - self.length1 - self.length2
            else:
                self.length2 = self.totalLength - self.length1
                self.length3 = 0
            num1 = self.length2 / math.cos(math.atan(float(self.divergence) / 100))
            z = point3d.get_Z() + self.length2 * (float(self.slope2) / 100)
            point3d2 = MathHelper.distanceBearingPoint(point3d, num - math.atan(float(self.divergence) / 100), num1).smethod_167(z)
            z = point3d1.get_Z() + self.length2 * (float(self.slope2) / 100)
            point3d3 = MathHelper.distanceBearingPoint(point3d1, num + math.atan(float(self.divergence) / 100), num1).smethod_167(z)
            self.points2 = Point3dCollection()
            self.points2.Add(point3d1)
            self.points2.Add(point3d3)
            self.points2.Add(point3d2)
            self.points2.Add(point3d)
            if (self.length3 > 0):
                point3d = point3d2
                point3d1 = point3d3
                num1 = self.length3 / math.cos(math.atan(float(self.divergence) / 100))
                point3d2 = MathHelper.distanceBearingPoint(point3d, num - math.atan(float(self.divergence) / 100), num1)
                point3d3 = MathHelper.distanceBearingPoint(point3d1, num + math.atan(float(self.divergence) / 100), num1)
                self.points3 = Point3dCollection()
                self.points3.Add(point3d1)
                self.points3.Add(point3d3)
                self.points3.Add(point3d2)
                self.points3.Add(point3d)
        self.area = Point3dCollection()
        self.area.Add(self.points1.get_Item(0))
        self.area.Add(self.points1.get_Item(1))
        if (self.hasSection2):
            self.area.Add(self.points2.get_Item(1))
            if (self.points3 != None):
                self.area.Add(self.points3.get_Item(1))
                self.area.Add(self.points3.get_Item(2))
            self.area.Add(self.points2.get_Item(2))
        self.area.Add(self.points1.get_Item(2))
        self.area.Add(self.points1.get_Item(3))
        
    def vmethod_0(self, bool_0, altitude_0):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Database(), self.layerName2D, 4)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName2D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_133(self.points1, True), constructionLayer)
        if (bool_0):
            self.method_15(self.points1.get_Item(3), self.points1.get_Item(0), self.points1.get_Item(2), self.points1.get_Item(1), altitude_0, self.slope1, self.rwyDirection + math.pi, self.length1, True, True, constructionLayer)
        if (self.hasSection2):
            AcadHelper.smethod_18(AcadHelper.smethod_133(self.points2, True), constructionLayer)
            if (bool_0):
                self.method_15(self.points2.get_Item(3), self.points2.get_Item(0), self.points2.get_Item(2), self.points2.get_Item(1), altitude_0, self.slope2, self.rwyDirection + math.pi, self.length2, True, True, constructionLayer)
            if (self.points3 != None):
                AcadHelper.smethod_18(AcadHelper.smethod_133(self.points3, True), constructionLayer)
                if (bool_0):
                    item = self.points3.get_Item(1)
                    point3d = self.points3.get_Item(2)
                    point3d1 = MathHelper.distanceBearingPoint(point3d, MathHelper.getBearing(point3d, item), MathHelper.calcDistance(point3d, item) / 2)
                    self.method_13(point3d1, Altitude(item.get_Z()), point3d, item, False, constructionLayer)
                    
    def vmethod_1(self):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Database(), this.layerName3D, 4)
        point3dCollection = Point3dCollection()
        point3dCollection1 = Point3dCollection()
        point3dCollection.Add(self.points1.get_Item(0))
        point3dCollection.Add(self.points1.get_Item(1))
        point3dCollection1.Add(self.points1.get_Item(3))
        point3dCollection1.Add(self.points1.get_Item(2))
        if (self.hasSection2):
            point3dCollection.Add(self.points2.get_Item(1))
            point3dCollection1.Add(self.points2.get_Item(2))
            if (self.points3 != None):
                point3dCollection.Add(self.points3.get_Item(1))
                point3dCollection1.Add(self.points3.get_Item(2))
        constructionLayer = AcadHelper.createVectorLayer(self.layerName3D, QGis.Polygon)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_153_v15(point3dCollection, point3dCollection1, constructionLayer)

    def vmethod_2(self, obstacle_0):
        # Point3d point3d
        # Point3d point3d1
        double_0 = None
        double_1 = None
        z = obstacle_0.Position.get_Z() + obstacle_0.Trees
        if (MathHelper.pointInPolygon(self.points1, obstacle_0.Position, obstacle_0.Tolerance)):
            item = self.points1.get_Item(0)
            item1 = self.points1.get_Item(3)
            point3d = MathHelper.getIntersectionPoint(item, item1, obstacle_0.Position, MathHelper.distanceBearingPoint(obstacle_0.Position, self.rwyDirection, 100))
            num = max(MathHelper.calcDistance(point3d, obstacle_0.Position) - obstacle_0.Tolerance, 0)
            double_0 = item.get_Z() + num * (float(self.slope1) / 100)
            double_1 = z - double_0
            return True, double_0, double_1
        if (self.hasSection2):
            if (MathHelper.pointInPolygon(self.points2, obstacle_0.Position, obstacle_0.Tolerance)):
                item2 = self.points2.get_Item(0)
                point3d2 = self.points2.get_Item(3)
                point3d1 = MathHelper.getIntersectionPoint(item2, point3d2, obstacle_0.Position, MathHelper.distanceBearingPoint(obstacle_0.Position, self.rwyDirection, 100))
                num1 = max(MathHelper.calcDistance(point3d1, obstacle_0.Position) - obstacle_0.Tolerance, 0)
                double_0 = item2.get_Z() + num1 * (float(self.slope2) / 100)
                double_1 = z - double_0
                return True, double_0, double_1
            if (self.points3 != None and MathHelper.pointInPolygon(self.points3, obstacle_0.Position, obstacle_0.Tolerance)):
                item3 = self.points3.get_Item(0)
                double_0 = item3.get_Z()
                double_1 = z - double_0
                return True, double_0, double_1
        return False, double_0, double_1

class BalkedLandingSurface(IAerodromeSurfacesSurface):
    def __init__(self,  runway_0, aerodromeSurfacesCriteria_0, altitude_0):
        IAerodromeSurfacesSurface.__init__(self)
        
        self.title = Captions.BALKED_LANDING
        self.method_1(runway_0, aerodromeSurfacesCriteria_0.Strip)
        self.distFromTHR = aerodromeSurfacesCriteria_0.BalkedLanding.DistFromTHR
        self.distFromTHRFixed = aerodromeSurfacesCriteria_0.BalkedLanding.DistFromTHRFixed
        self.innerEdge = aerodromeSurfacesCriteria_0.BalkedLanding.InnerEdge
        self.divergence = float(aerodromeSurfacesCriteria_0.BalkedLanding.Divergence)
        self.slope = float(aerodromeSurfacesCriteria_0.BalkedLanding.Slope)
        self.area, self.length = self.method_3(runway_0, aerodromeSurfacesCriteria_0, altitude_0)

    def vmethod_0(self, bool_0, altitude_0):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName2D, 24)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName2D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_133(self.area, True), constructionLayer)
        if (bool_0):
            self.method_15(self.area.get_Item(3), self.area.get_Item(0), self.area.get_Item(2), self.area.get_Item(1), altitude_0, self.slope, self.rwyDirection, self.length, True, True, constructionLayer)

    def vmethod_1(self):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName3D, 24)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName3D, QGis.Polygon)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        face = [self.area.get_Item(0), self.area.get_Item(1), self.area.get_Item(2), self.area.get_Item(3)]#, true, true, true, true)
        AcadHelper.smethod_18(face, constructionLayer)

    def vmethod_2(self, obstacle_0):
        # Point3d point3d
        double_0 = None
        double_1 = None
        if (not MathHelper.pointInPolygon(self.area, obstacle_0.Position, obstacle_0.Tolerance)):
            return False, double_0, double_1
        z = obstacle_0.Position.get_Z() + obstacle_0.Trees
        item = self.area.get_Item(0)
        item1 = self.area.get_Item(3)
        point3d = MathHelper.getIntersectionPoint(item, item1, obstacle_0.Position, MathHelper.distanceBearingPoint(obstacle_0.Position, self.rwyDirection, 100))
        num = max(MathHelper.calcDistance(point3d, obstacle_0.Position) - obstacle_0.Tolerance, 0)
        double_0 = item.get_Z() + num * (float(self.slope) / 100)
        double_1 = z - double_0
        return True, double_0, double_1

class ConicalSurface(IAerodromeSurfacesSurface):
    def __init__(self, runway_0, aerodromeSurfacesCriteria_0, altitude_0):
        IAerodromeSurfacesSurface.__init__(self)

        self.title = Captions.CONICAL
        self.method_1(runway_0, aerodromeSurfacesCriteria_0.Strip)
        self.innerPoints, self.ptCen1, self.ptCen2 = self.method_4(aerodromeSurfacesCriteria_0, altitude_0)
        self.outerPoints, self.ptCen1, self.ptCen2 = self.method_5(aerodromeSurfacesCriteria_0, altitude_0)
        self.slope = float(aerodromeSurfacesCriteria_0.Conical.Slope)
        self.radiusInner = MathHelper.calcDistance(self.ptCen1, self.innerPoints.get_Item(0))
        self.radiusOuter = MathHelper.calcDistance(self.ptCen1, self.outerPoints.get_Item(0))
        if (not MathHelper.smethod_102(self.ptCen1, self.ptCen2)):
            self.pointsCen1 = Point3dCollection()
            point3dCollection = self.pointsCen1
            point3dArray = [MathHelper.distanceBearingPoint(self.outerPoints.get_Item(5), MathHelper.getBearing(self.ptCen2, self.ptCen1), self.radiusOuter), self.outerPoints.get_Item(5), self.outerPoints.get_Item(1), MathHelper.distanceBearingPoint(self.outerPoints.get_Item(1), MathHelper.getBearing(self.ptCen2, self.ptCen1), self.radiusOuter)]
            point3dCollection.smethod_145(point3dArray)
            self.pointsSquare = Point3dCollection()
            point3dCollection1 = self.pointsSquare
            item = [self.outerPoints.get_Item(1), self.outerPoints.get_Item(2), self.outerPoints.get_Item(4), self.outerPoints.get_Item(5)]
            point3dCollection1.smethod_145(item)
            self.pointsCen2 = Point3dCollection()
            point3dCollection2 = self.pointsCen2
            point3dArray1 = [MathHelper.distanceBearingPoint(self.outerPoints.get_Item(2), MathHelper.getBearing(self.ptCen1, self.ptCen2), self.radiusOuter), self.outerPoints.get_Item(2), self.outerPoints.get_Item(4), MathHelper.distanceBearingPoint(self.outerPoints.get_Item(4), MathHelper.getBearing(self.ptCen1, self.ptCen2), self.radiusOuter)]
            point3dCollection2.smethod_145(point3dArray1)
        self.innerArea = PolylineArea()
        self.innerArea.method_1(self.innerPoints.get_Item(1))
        self.innerArea.Add(PolylineAreaPoint(self.innerPoints.get_Item(2), MathHelper.smethod_60(self.innerPoints.get_Item(2), self.innerPoints.get_Item(3), self.innerPoints.get_Item(4))))
        self.innerArea.method_1(self.innerPoints.get_Item(4))
        self.innerArea.Add(PolylineAreaPoint(self.innerPoints.get_Item(5), MathHelper.smethod_60(self.innerPoints.get_Item(5), self.innerPoints.get_Item(0), self.innerPoints.get_Item(1))))
        self.outerArea = PolylineArea()
        self.outerArea.method_1(self.outerPoints.get_Item(1))
        self.outerArea.Add(PolylineAreaPoint(self.outerPoints.get_Item(2), MathHelper.smethod_60(self.outerPoints.get_Item(2), self.outerPoints.get_Item(3), self.outerPoints.get_Item(4))))
        self.outerArea.method_1(self.outerPoints.get_Item(4))
        self.outerArea.Add(PolylineAreaPoint(self.outerPoints.get_Item(5), MathHelper.smethod_60(self.outerPoints.get_Item(5), self.outerPoints.get_Item(0), self.outerPoints.get_Item(1))))
        self.area = self.outerArea
        # self.area = (new PrimaryObstacleArea(self.outerArea)).SelectionArea

    def vmethod_0(self, bool_0, altitude_0):
        # Point3d point3d
        # Point3d point3d1
        # Point3d point3d2
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName2D, 8)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName2D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_140_v15(self.innerArea, True), constructionLayer)
        if (bool_0):
            z = self.innerPoints.get_Item(0).get_Z()
            metres = math.trunc(z / altitude_0.Metres) * altitude_0.Metres
            if (metres <= z):
                metres = metres + altitude_0.Metres
            num = self.outerPoints.get_Item(0).get_Z()
            num1 = MathHelper.getBearing(self.ptCen1, self.ptCen2)
            if (not MathHelper.smethod_102(self.ptCen1, self.ptCen2)):
                point3d = MathHelper.distanceBearingPoint(self.innerPoints.get_Item(1), MathHelper.getBearing(self.innerPoints.get_Item(1), self.innerPoints.get_Item(2)), MathHelper.calcDistance(self.innerPoints.get_Item(1), self.innerPoints.get_Item(2)) / 2)
                self.method_14(point3d, Altitude(z), num1, constructionLayer)
                point3d = MathHelper.distanceBearingPoint(self.innerPoints.get_Item(5), MathHelper.getBearing(self.innerPoints.get_Item(5), self.innerPoints.get_Item(4)), MathHelper.calcDistance(self.innerPoints.get_Item(5), self.innerPoints.get_Item(4)) / 2)
                self.method_14(point3d, Altitude(z), num1, constructionLayer)
            else:
                point3d = MathHelper.distanceBearingPoint(self.ptCen1, self.rwyDirection - math.pi / 2, self.radiusInner)
                self.method_14(point3d, Altitude(z), self.rwyDirection, constructionLayer)
                point3d = MathHelper.distanceBearingPoint(self.ptCen1, self.rwyDirection + math.pi / 2, self.radiusInner)
                self.method_14(point3d, Altitude(z), self.rwyDirection, constructionLayer)
            num2 = MathHelper.calcDistance(self.innerPoints.get_Item(0), self.outerPoints.get_Item(0))
            while (metres < num):
                num3 = MathHelper.smethod_192(z, math.atan(float(self.slope) / 100), metres, num2, 0)
                if (num3 >= num2):
                    break
                if (not MathHelper.smethod_102(self.ptCen1, self.ptCen2)):
                    point3d1 = MathHelper.distanceBearingPoint(self.innerPoints.get_Item(1), num1 - math.pi / 2, num3)
                    point3d2 = MathHelper.distanceBearingPoint(self.innerPoints.get_Item(2), num1 - math.pi / 2, num3)
                    point3d = MathHelper.distanceBearingPoint(point3d1, MathHelper.getBearing(point3d1, point3d2), MathHelper.calcDistance(point3d1, point3d2) / 2)
                    self.method_13(point3d, Altitude(metres), point3d1, point3d2, False, constructionLayer)
                    point3d1 = MathHelper.distanceBearingPoint(self.innerPoints.get_Item(5), num1 + math.pi / 2, num3)
                    point3d2 = MathHelper.distanceBearingPoint(self.innerPoints.get_Item(4), num1 + math.pi / 2, num3)
                    point3d = MathHelper.distanceBearingPoint(point3d1, MathHelper.getBearing(point3d1, point3d2), MathHelper.calcDistance(point3d1, point3d2) / 2)
                    self.method_13(point3d, Altitude(metres), point3d1, point3d2, False, constructionLayer)
                else:
                    point3d = MathHelper.distanceBearingPoint(self.ptCen1, self.rwyDirection - math.pi / 2, self.radiusInner + num3)
                    self.method_14(point3d, Altitude(metres), self.rwyDirection, constructionLayer)
                    point3d = MathHelper.distanceBearingPoint(self.ptCen1, self.rwyDirection + math.pi / 2, self.radiusInner + num3)
                    self.method_14(point3d, Altitude(metres), self.rwyDirection, constructionLayer)
                polylineArea = PolylineArea()
                self.innerArea.method_1(self.innerPoints.get_Item(1))
                self.innerArea.Add(PolylineAreaPoint(self.innerPoints.get_Item(2), MathHelper.smethod_60(self.innerPoints.get_Item(2), self.innerPoints.get_Item(3), self.innerPoints.get_Item(4))))
                self.innerArea.method_1(self.innerPoints.get_Item(4))
                self.innerArea.Add(PolylineAreaPoint(self.innerPoints.get_Item(5), MathHelper.smethod_60(self.innerPoints.get_Item(5), self.innerPoints.get_Item(0), self.innerPoints.get_Item(1))))
                point3d3 = MathHelper.distanceBearingPoint(self.innerPoints.get_Item(0), self.rwyDirection - math.pi, num3)
                point3d1 = MathHelper.distanceBearingPoint(self.innerPoints.get_Item(1), self.rwyDirection - math.pi / 2, num3)
                point3d2 = MathHelper.distanceBearingPoint(self.innerPoints.get_Item(2), self.rwyDirection - math.pi / 2, num3)
                point3d4 = MathHelper.distanceBearingPoint(self.innerPoints.get_Item(3), self.rwyDirection, num3)
                point3d5 = MathHelper.distanceBearingPoint(self.innerPoints.get_Item(4), self.rwyDirection + math.pi / 2, num3)
                point3d6 = MathHelper.distanceBearingPoint(self.innerPoints.get_Item(5), self.rwyDirection + math.pi / 2, num3)
                polyline = PolylineArea()
                polyline.method_1(point3d1.smethod_176())
                polyline.method_3(point3d2.smethod_176(), MathHelper.smethod_60(point3d2, point3d4, point3d5))
                polyline.method_1(point3d5.smethod_176())
                polyline.method_3(point3d6.smethod_176(), MathHelper.smethod_60(point3d6, point3d3, point3d1))
                polyline.method_1(point3d1.smethod_176())
                AcadHelper.smethod_18(polyline, constructionLayer)
                metres = metres + altitude_0.Metres
            AcadHelper.smethod_18(AcadHelper.smethod_140_v15(self.outerArea, True), constructionLayer)
            if (MathHelper.smethod_102(self.ptCen1, self.ptCen2)):
                point3d = MathHelper.distanceBearingPoint(self.ptCen1, self.rwyDirection - math.pi / 2, self.radiusOuter)
                self.method_14(point3d, Altitude(num), self.rwyDirection, constructionLayer)
                point3d = MathHelper.distanceBearingPoint(self.ptCen1, self.rwyDirection + math.pi / 2, self.radiusOuter)
                self.method_14(point3d, Altitude(num), self.rwyDirection, constructionLayer)
                return
            point3d = MathHelper.distanceBearingPoint(self.outerPoints.get_Item(1), MathHelper.getBearing(self.outerPoints.get_Item(1), self.outerPoints.get_Item(2)), MathHelper.calcDistance(self.outerPoints.get_Item(1), self.outerPoints.get_Item(2)) / 2)
            self.method_14(point3d, Altitude(num), num1, constructionLayer)
            point3d = MathHelper.distanceBearingPoint(self.outerPoints.get_Item(5), MathHelper.getBearing(self.outerPoints.get_Item(5), self.outerPoints.get_Item(4)), MathHelper.calcDistance(self.outerPoints.get_Item(5), self.outerPoints.get_Item(4)) / 2)
            self.method_14(point3d, Altitude(num), num1, constructionLayer)

    def vmethod_1(self):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Database(), this.layerName3D, 8)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName3D, QGis.Polygon)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        num = -1
        num1 = -1
        point3dCollection = Point3dCollection()
        item = [self.innerPoints.get_Item(1), self.innerPoints.get_Item(2)]
        point3dCollection.smethod_145(item)
        ptCol, num1 = MathHelper.smethod_139(self.innerPoints.get_Item(2), self.innerPoints.get_Item(3), self.innerPoints.get_Item(4), num1)
        point3dCollection.smethod_144(ptCol)
        point3dArray = [self.innerPoints.get_Item(4), self.innerPoints.get_Item(5)]
        point3dCollection.smethod_145(point3dArray)
        ptCol1, num = MathHelper.smethod_139(self.innerPoints.get_Item(5), self.innerPoints.get_Item(0), self.innerPoints.get_Item(1), num)
        point3dCollection.smethod_144(ptCol1)
        point3dCollection.Add(self.innerPoints.get_Item(1))
        point3dCollection1 = Point3dCollection()
        item1 = [self.outerPoints.get_Item(1), self.outerPoints.get_Item(2) ]
        point3dCollection1.smethod_145(item1)
        ptCol2, num1 = MathHelper.smethod_139(self.outerPoints.get_Item(2), self.outerPoints.get_Item(3), self.outerPoints.get_Item(4), num1)
        point3dCollection1.smethod_144(ptCol2)
        point3dArray1 = [self.outerPoints.get_Item(4), self.outerPoints.get_Item(5) ]
        point3dCollection1.smethod_145(point3dArray1)
        ptCol3, num = MathHelper.smethod_139(self.outerPoints.get_Item(5), self.outerPoints.get_Item(0), self.outerPoints.get_Item(1), num)
        point3dCollection1.smethod_144(ptCol3)
        point3dCollection1.Add(self.outerPoints.get_Item(1))
        AcadHelper.smethod_153_v15(point3dCollection, point3dCollection1, constructionLayer)

    def vmethod_2(self, obstacle_0):
        # Point3d point3d
        double_0 = None
        double_1 = None
        z = obstacle_0.Position.get_Z() + obstacle_0.Trees
        if (MathHelper.smethod_102(self.ptCen1, self.ptCen2)):
            num = MathHelper.calcDistance(self.ptCen1, obstacle_0.Position) - obstacle_0.Tolerance
            if (num > self.radiusOuter):
                return False, double_0, double_1
            double_0 = self.ptCen1.get_Z() + float(self.slope) / 100 * (num - self.radiusInner)
            double_1 = z - double_0
            return True, double_0, double_1
        if (MathHelper.pointInPolygon(self.pointsSquare, obstacle_0.Position, obstacle_0.Tolerance)):
            num1 = MathHelper.getBearing(self.ptCen1, self.ptCen2)
            point3d = MathHelper.getIntersectionPoint(self.ptCen1, self.ptCen2, obstacle_0.Position, MathHelper.distanceBearingPoint(obstacle_0.Position, num1 + math.pi / 2, 100))
            num2 = MathHelper.calcDistance(point3d, obstacle_0.Position) - obstacle_0.Tolerance
            double_0 = self.ptCen1.get_Z() + float(self.slope) / 100 * (num2 - self.radiusInner)
            double_1 = z - double_0
            return True, double_0, double_1
        if (MathHelper.pointInPolygon(self.pointsCen1, obstacle_0.Position, obstacle_0.Tolerance)):
            num3 = MathHelper.calcDistance(self.ptCen1, obstacle_0.Position) - obstacle_0.Tolerance
            if (num3 > self.radiusOuter):
                return False, double_0, double_1
            double_0 = self.ptCen1.get_Z() + float(self.slope) / 100 * (num3 - self.radiusInner)
            double_1 = z - double_0
            return True, double_0, double_1
        if (not MathHelper.pointInPolygon(self.pointsCen2, obstacle_0.Position, obstacle_0.Tolerance)):
            return False, double_0, double_1
        num4 = MathHelper.calcDistance(self.ptCen2, obstacle_0.Position) - obstacle_0.Tolerance
        if (num4 > self.radiusOuter):
            return False, double_0, double_1
        double_0 = self.ptCen2.get_Z() + float(self.slope) / 100 * (num4 - self.radiusInner)
        double_1 = z - double_0
        return True, double_0, double_1

class InnerApproachSurface(IAerodromeSurfacesSurface):
    # private double width
    #
    # private double distFromTHR
    #
    # private double length
    #
    # private double slope

    def __init__(self, runway_0, aerodromeSurfacesCriteria_0):
        IAerodromeSurfacesSurface.__init__(self)
        self.title = Captions.INNER_APPROACH
        self.method_1(runway_0, aerodromeSurfacesCriteria_0.Strip)
        self.distFromTHR = aerodromeSurfacesCriteria_0.InnerApproach.DistFromTHR
        self.length = float(aerodromeSurfacesCriteria_0.InnerApproach.Length)
        self.width = float(aerodromeSurfacesCriteria_0.InnerApproach.Width)
        self.slope = float(aerodromeSurfacesCriteria_0.InnerApproach.Slope)
        self.area = self.method_2(runway_0, aerodromeSurfacesCriteria_0)

    def vmethod_0(self, bool_0, altitude_0):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName2D, 1)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName2D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_137_v15(self.area, True), constructionLayer)
        if (bool_0):
            self.method_15(self.area.get_Item(3), self.area.get_Item(0), self.area.get_Item(2), self.area.get_Item(1), altitude_0, self.slope, self.rwyDirection + math.pi, self.length, True, True, constructionLayer)

    def vmethod_1(self):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName3D, 1)
        face = [self.area.get_Item(0), self.area.get_Item(1), self.area.get_Item(2), self.area.get_Item(3), self.area.get_Item(0)]
        constructionLayer = AcadHelper.createVectorLayer(self.layerName3D, QGis.Polygon)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_18(face, constructionLayer)

    def vmethod_2(self, obstacle_0):
        # Point3d point3d
        double_0 = None
        double_1 = None
        if (not MathHelper.pointInPolygon(self.area, obstacle_0.Position, obstacle_0.Tolerance)):
            return False, double_0, double_1
        z = obstacle_0.Position.get_Z() + obstacle_0.Trees
        item = self.area.get_Item(0)
        item1 = self.area.get_Item(3)
        point3d = MathHelper.getIntersectionPoint(item, item1, obstacle_0.Position, MathHelper.distanceBearingPoint(obstacle_0.Position, self.rwyDirection, 100))
        num = max(MathHelper.calcDistance(point3d, obstacle_0.Position) - obstacle_0.Tolerance, 0)
        double_0 = item.get_Z() + num * (float(self.slope) / 100)
        double_1 = z - double_0
        return True, double_0, double_1

class InnerHorizontalSurface(IAerodromeSurfacesSurface):
    # private PrimaryObstacleArea outerArea
    #
    # private Point3d ptCen1
    #
    # private Point3d ptCen2
    #
    # private Point3dCollection points

    def __init__(self, runway_0, aerodromeSurfacesCriteria_0, altitude_0):
        IAerodromeSurfacesSurface.__init__(self)

        self.title = Captions.INNER_HORIZONTAL
        self.method_1(runway_0, aerodromeSurfacesCriteria_0.Strip)
        self.points, self.ptCen1, self.ptCen2 = self.method_4(aerodromeSurfacesCriteria_0, altitude_0)
        polylineArea = PolylineArea()
        polylineArea.method_1(self.points.get_Item(1))
        polylineArea.Add(PolylineAreaPoint(self.points.get_Item(2), MathHelper.smethod_60(self.points.get_Item(2), self.points.get_Item(3), self.points.get_Item(4))))
        polylineArea.method_1(self.points.get_Item(4))
        polylineArea.Add(PolylineAreaPoint(self.points.get_Item(5), MathHelper.smethod_60(self.points.get_Item(5), self.points.get_Item(0), self.points.get_Item(1))))
        self.outerArea = PrimaryObstacleArea(polylineArea)
        self.area = self.outerArea.SelectionArea

    def vmethod_0(self, bool_0, altitude_0):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName2D, 5)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName2D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_140_v15(self.outerArea.PreviewArea, True), constructionLayer)
        if (bool_0):
            if (not MathHelper.smethod_102(self.ptCen1, self.ptCen2)):
                item = self.points.get_Item(1)
                point3d = self.points.get_Item(2)
                point3d1 = MathHelper.distanceBearingPoint(item, MathHelper.getBearing(item, point3d), MathHelper.calcDistance(item, point3d) / 2)
                self.method_13(point3d1, Altitude(self.ptCen1.get_Z()), item, point3d, False, constructionLayer)
            else:
                item1 = self.points.get_Item(1)
                item2 = self.points.get_Item(1)
                self.method_14(item1, Altitude(item2.get_Z()), self.rwyDirection, constructionLayer)
            if (MathHelper.smethod_102(self.ptCen1, self.ptCen2)):
                point3d2 = self.points.get_Item(4)
                item3 = self.points.get_Item(1)
                self.method_14(point3d2, Altitude(item3.get_Z()), self.rwyDirection, constructionLayer)
                return
            point3d3 = self.points.get_Item(4)
            item4 = self.points.get_Item(5)
            point3d4 = MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d3, item4), MathHelper.calcDistance(point3d3, item4) / 2)
            self.method_13(point3d4, Altitude(self.ptCen1.get_Z()), point3d3, item4, False, constructionLayer)

    def vmethod_1(self):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName3D, 5)
        polyline = AcadHelper.smethod_140_v15(self.outerArea.PreviewArea, True)
        # polyline.SetDataselfDefaults()
        # polyline.set_Layer(self.layerName3D)
        # polyline.set_Elevation(self.ptCen1.get_Z())
        # DBObjectCollection dBObjectCollection = new DBObjectCollection()
        # dBObjectCollection.Add(polyline)
        # foreach (Entity entity in Autodesk.AutoCAD.DataselfServices.Region.CreateFromCurves(dBObjectCollection))
        # {
        constructionLayer = AcadHelper.createVectorLayer(self.layerName3D, QGis.Polygon)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_18(polyline, constructionLayer)
    #     AcadHelper.smethod_25(dBObjectCollection)
    # }

    def vmethod_2(self, obstacle_0):
        double_0 = None
        double_1 = None
        if (not self.outerArea.imethod_0(obstacle_0.Position, obstacle_0.Tolerance)):
            return False, double_0, double_1
        z = obstacle_0.Position.get_Z() + obstacle_0.Trees
        double_0 = self.ptCen1.get_Z()
        double_1 = z - double_0
        return True, double_0, double_1

class InnerTransitionalSurface(IAerodromeSurfacesSurface):
    # private Point3dCollection points1R
    # 
    # private Point3dCollection points2R
    # 
    # private Point3dCollection points1L
    # 
    # private Point3dCollection points2L
    # 
    # private Point3dCollection areaR
    # 
    # private Point3dCollection areaL
    # 
    # private double slope

    def __init__(self, runway_0, aerodromeSurfacesCriteria_0, altitude_0):
        IAerodromeSurfacesSurface.__init__(self)
        
        num = None
        self.title = Captions.INNER_TRANSITIONAL
        self.method_1(runway_0, aerodromeSurfacesCriteria_0.Strip)
        self.slope = float(aerodromeSurfacesCriteria_0.InnerTransitional.Slope)
        metres = altitude_0.Metres + aerodromeSurfacesCriteria_0.InnerHorizontal.Height
        point3dCollection = self.method_2(runway_0, aerodromeSurfacesCriteria_0)
        point3dCollection1, num = self.method_3(runway_0, aerodromeSurfacesCriteria_0, altitude_0)
        item = point3dCollection1.get_Item(0)
        point3d = point3dCollection1.get_Item(3)
        point3d1 = MathHelper.distanceBearingPoint(item, MathHelper.getBearing(item, point3d), MathHelper.calcDistance(item, point3d) / 2)
        point3d2 = MathHelper.distanceBearingPoint(item, self.rwyDirection - (math.pi / 2), 100)
        self.points1R = Point3dCollection()
        self.points1R.Add(point3dCollection.get_Item(1))
        self.points1R.Add(point3dCollection.get_Item(0))
        num1 = self.indexRwyThr + 1
        while (True):
            if (num1 < self.centerLine.get_Count()):
                item1 = self.centerLine.get_Item(num1 - 1)
                item2 = self.centerLine.get_Item(num1)
                self.points1R.Add(MathHelper.distanceBearingPoint(item1, self.rwyDirection - (math.pi / 2), aerodromeSurfacesCriteria_0.InnerApproach.Width / 2))
                if (MathHelper.smethod_119(item2, point3d1, point3d2)):
                    break
                if (num1 != self.indexRwyEnd):
                    num1 += 1
                else:
                    self.points1R.Add(MathHelper.distanceBearingPoint(item2, self.rwyDirection - (math.pi / 2), aerodromeSurfacesCriteria_0.InnerApproach.Width / 2))
                    break
            else:
                break
        self.points1R.Add(point3dCollection1.get_Item(3))
        self.points1R.Add(point3dCollection1.get_Item(2))
        self.points2R = Point3dCollection()
        for point3d3 in self.points1R:
            z = (metres - point3d3.get_Z()) / (float(self.slope) / 100)
            self.points2R.Add(MathHelper.distanceBearingPoint(point3d3, self.rwyDirection - (math.pi / 2), z).smethod_167(metres))
        self.points1L = Point3dCollection()
        self.points1L.Add(point3dCollection.get_Item(2))
        self.points1L.Add(point3dCollection.get_Item(3))
        num2 = self.indexRwyThr + 1
        while (True):
            if (num2 < self.centerLine.get_Count()):
                item3 = self.centerLine.get_Item(num2 - 1)
                item4 = self.centerLine.get_Item(num2)
                self.points1L.Add(MathHelper.distanceBearingPoint(item3, self.rwyDirection + (math.pi / 2), float(aerodromeSurfacesCriteria_0.InnerApproach.Width) / 2))
                if (MathHelper.smethod_119(item4, point3d1, point3d2)):
                    break
                if (num2 != self.indexRwyEnd):
                    num2 += 1
                else:
                    self.points1L.Add(MathHelper.distanceBearingPoint(item4, self.rwyDirection + (math.pi / 2), float(aerodromeSurfacesCriteria_0.InnerApproach.Width) / 2))
                    break
            else:
                break
        self.points1L.Add(point3dCollection1.get_Item(0))
        self.points1L.Add(point3dCollection1.get_Item(1))
        self.points2L = Point3dCollection()
        for point3d4 in self.points1L:
            z1 = (metres - point3d4.get_Z()) / (float(self.slope) / 100)
            self.points2L.Add(MathHelper.distanceBearingPoint(point3d4, self.rwyDirection + (math.pi / 2), z1).smethod_167(metres))
        self.areaR = Point3dCollection()
        for i in range(self.points2R.get_Count()):
            self.areaR.Add(self.points2R.get_Item(i))
        for j in range(self.points1R.get_Count()):
            self.areaR.Add(self.points1R.get_Item(self.points1R.get_Count() - 1 - j))
        self.areaL = Point3dCollection()
        for k in range(self.points2L.get_Count()):
            self.areaL.Add(self.points2L.get_Item(k))
        for l in range(self.points1L.get_Count()):
            self.areaL.Add(self.points1L.get_Item(self.points1L.get_Count() - 1 - l))
        self.area = Point3dCollection()
        for m in range(self.points2R.get_Count()):
            self.area.Add(self.points2R.get_Item(m))
        for n in range(self.points2L.get_Count()):
            self.area.Add(self.points2L.get_Item(self.points2L.get_Count() - 1 - n))

    def vmethod_0(self, bool_0, altitude_0):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName2D, 2)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName2D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_137_v15(self.areaR, True), constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_137_v15(self.areaL, True), constructionLayer)
        if (bool_0):
            self.method_16(self.points1R, self.points2R, altitude_0, self.slope, self.rwyDirection - (math.pi / 2), 2, constructionLayer)
            self.method_16(self.points1L, self.points2L, altitude_0, self.slope, self.rwyDirection + (math.pi / 2), 2, constructionLayer)

    def vmethod_1(self):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName3D, 2)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName3D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_153_v15(self.points1R, self.points2R, constructionLayer)
        AcadHelper.smethod_153_v15(self.points1L, self.points2L, constructionLayer)

    def vmethod_2(self, obstacle_0):
        double_0 = None
        double_1 = None
        if (MathHelper.pointInPolygon(self.areaR, obstacle_0.Position, obstacle_0.Tolerance)):
            z = obstacle_0.Position.get_Z() + obstacle_0.Trees
            double_0 = self.method_12(obstacle_0, self.points1R, self.points2R)
            double_1 = z - double_0
            return True, double_0, double_1
        if (not MathHelper.pointInPolygon(self.areaL, obstacle_0.Position, obstacle_0.Tolerance)):
            return False, double_0, double_1
        num = obstacle_0.Position.get_Z() + obstacle_0.Trees
        double_0 = self.method_12(obstacle_0, self.points1L, self.points2L)
        double_1 = num - double_0
        return True, double_0, double_1

class NavigationalAidSurface(IAerodromeSurfacesSurface):
    # private Point3dCollection pointsR
    #
    # private Point3dCollection pointsL
    #
    # private Point3dCollection pointsM
    #
    # private Point3dCollection areaL
    #
    # private Point3dCollection areaR
    #
    # private double slope

    def __init__(self, runway_0, aerodromeSurfacesCriteria_0, altitude_0):
        IAerodromeSurfacesSurface.__init__(self)

        self.title = Captions.NAVIGATIONAL_AID_SURFACE
        self.method_1(runway_0, aerodromeSurfacesCriteria_0.Strip)
        self.slope = float(aerodromeSurfacesCriteria_0.NavigationalAid.Slope)
        metres = altitude_0.Metres + aerodromeSurfacesCriteria_0.InnerHorizontal.Height
        num = float(self.slope) / 100
        slope = float(aerodromeSurfacesCriteria_0.Transitional.Slope) / 100
        width = aerodromeSurfacesCriteria_0.Strip.Width
        self.pointsM = Point3dCollection()
        self.pointsM.Add(MathHelper.distanceBearingPoint(self.centerLine.get_Item(self.indexRwyThr), self.rwyDirection - math.pi, aerodromeSurfacesCriteria_0.Strip.Length))
        for i in range(self.indexRwyThr, self.centerLine.get_Count()):
            self.pointsM.Add(self.centerLine.get_Item(i))
        self.pointsR = Point3dCollection()
        for point3d in self.pointsM:
            z = (metres - point3d.get_Z()) / num
            if (z <= width + (metres - point3d.get_Z()) / slope):
                self.pointsR.Add(MathHelper.distanceBearingPoint(point3d, self.rwyDirection - (math.pi / 2), z).smethod_167(metres))
            else:
                num1 = num * width / (slope - num)
                self.pointsR.Add(MathHelper.distanceBearingPoint(point3d, self.rwyDirection - (math.pi / 2), width + num1).smethod_167(point3d.get_Z() + slope * num1))
        self.pointsL = Point3dCollection()
        for point3d1 in self.pointsM:
            z1 = (metres - point3d1.get_Z()) / num
            if (z1 <= width + (metres - point3d1.get_Z()) / slope):
                self.pointsL.Add(MathHelper.distanceBearingPoint(point3d1, self.rwyDirection + (math.pi / 2), z1).smethod_167(metres))
            else:
                num2 = num * width / (slope - num)
                self.pointsL.Add(MathHelper.distanceBearingPoint(point3d1, self.rwyDirection + (math.pi / 2), width + num2).smethod_167(point3d1.get_Z() + slope * num2))
        self.areaR = Point3dCollection()
        for j in range(self.pointsR.get_Count()):
            self.areaR.Add(self.pointsR.get_Item(j))
        for k in range(self.pointsM.get_Count()):
            self.areaR.Add(self.pointsM.get_Item(self.pointsM.get_Count() - 1 - k))
        self.areaL = Point3dCollection()
        for l in range(self.pointsL.get_Count()):
            self.areaL.Add(self.pointsL.get_Item(l))
        for m in range(self.pointsM.get_Count()):
            self.areaL.Add(self.pointsM.get_Item(self.pointsM.get_Count() - 1 - m))
        self.area = Point3dCollection()
        for n in range(self.pointsR.get_Count()):
            self.area.Add(self.pointsR.get_Item(n))
        for o in range(self.pointsL.get_Count()):
            self.area.Add(self.pointsL.get_Item(self.pointsL.get_Count() - 1 - o))

    def vmethod_0(self, bool_0, altitude_0):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName2D, 3)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName2D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_137_v15(self.areaR, True), constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_137_v15(self.areaL, True), constructionLayer)
        if (bool_0):
            count = self.pointsM.get_Count() - 1
            self.method_16(self.pointsM, self.pointsR, altitude_0, self.slope, self.rwyDirection - (math.pi / 2), count, constructionLayer)
            self.method_16(self.pointsM, self.pointsL, altitude_0, self.slope, self.rwyDirection + (math.pi / 2), count, constructionLayer)

    def vmethod_1(self):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName3D, 3)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName3D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_153_v15(self.pointsM, self.pointsR, constructionLayer)
        AcadHelper.smethod_153_v15(self.pointsM, self.pointsL, constructionLayer)

    def vmethod_2(self, obstacle_0):
        double_0 = None
        double_1 = None
        if (MathHelper.pointInPolygon(self.areaR, obstacle_0.Position, obstacle_0.Tolerance)):
            z = obstacle_0.Position.get_Z() + obstacle_0.Trees
            double_0 = self.method_12(obstacle_0, self.pointsM, self.pointsR)
            double_1 = z - double_0
            return True, double_0, double_1
        if (not MathHelper.pointInPolygon(self.areaL, obstacle_0.Position, obstacle_0.Tolerance)):
            return False, double_0, double_1
        num = obstacle_0.Position.get_Z() + obstacle_0.Trees
        double_0 = self.method_12(obstacle_0, self.pointsM, self.pointsL)
        double_1 = num - double_0
        return True, double_0, double_1

class OuterHorizontalSurface(IAerodromeSurfacesSurface):
    # private PrimaryObstacleArea outerArea
    #
    # private PolylineArea innerArea
    #
    # private Point3d ptCen1
    #
    # private Point3d ptCen2
    #
    # private Point3d ptArp
    #
    # private Point3dCollection innerPoints
    #
    # private double altitude
    #
    # private double radius

    def __init__(self, runway_0, aerodromeSurfacesCriteria_0, altitude_0, point3d_0):
        IAerodromeSurfacesSurface.__init__(self)

        self.title = Captions.OUTER_HORIZONTAL
        self.method_1(runway_0, aerodromeSurfacesCriteria_0.Strip)
        self.altitude = aerodromeSurfacesCriteria_0.OuterHorizontal.Height + point3d_0.get_Z()
        self.ptArp = point3d_0
        self.radius = float(aerodromeSurfacesCriteria_0.OuterHorizontal.Radius)
        self.innerPoints, self.ptCen1, self.ptCen2 = self.method_5(aerodromeSurfacesCriteria_0, altitude_0)
        for i in range(self.innerPoints.get_Count() - 1):
            self.innerPoints.set_Item(i, self.innerPoints.get_Item(i).smethod_167(self.altitude))
        self.innerArea = PolylineArea()
        self.innerArea.method_1(self.innerPoints.get_Item(1))
        self.innerArea.Add(PolylineAreaPoint(self.innerPoints.get_Item(2), MathHelper.smethod_60(self.innerPoints.get_Item(2), self.innerPoints.get_Item(3), self.innerPoints.get_Item(4))))
        self.innerArea.method_1(self.innerPoints.get_Item(4))
        self.innerArea.Add(PolylineAreaPoint(self.innerPoints.get_Item(5), MathHelper.smethod_60(self.innerPoints.get_Item(5), self.innerPoints.get_Item(0), self.innerPoints.get_Item(1))))
        self.outerArea = PrimaryObstacleArea(PolylineArea(None, point3d_0.smethod_167(self.altitude), aerodromeSurfacesCriteria_0.OuterHorizontal.Radius))
        self.area = self.outerArea.SelectionArea

    def vmethod_0(self, bool_0, altitude_0):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName2D, 127)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName2D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_140_v15(self.innerArea, True), constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_140_v15(self.outerArea.PreviewArea, True), constructionLayer)
        if (bool_0):
            if (not MathHelper.smethod_102(self.ptCen1, self.ptCen2)):
                item = self.innerPoints.get_Item(1)
                point3d = self.innerPoints.get_Item(2)
                point3d1 = MathHelper.distanceBearingPoint(item, MathHelper.getBearing(item, point3d), MathHelper.calcDistance(item, point3d) / 2)
                self.method_13(point3d1, Altitude(self.altitude), item, point3d, False, constructionLayer)
            else:
                item1 = self.innerPoints.get_Item(1)
                item2 = self.innerPoints.get_Item(1)
                self.method_14(item1, Altitude(item2.get_Z()), self.rwyDirection, constructionLayer)
            self.method_14(MathHelper.distanceBearingPoint(self.ptArp, self.rwyDirection - (math.pi / 2), self.radius), Altitude(self.altitude), self.rwyDirection, constructionLayer)
            if (not MathHelper.smethod_102(self.ptCen1, self.ptCen2)):
                point3d2 = self.innerPoints.get_Item(5)
                item3 = self.innerPoints.get_Item(4)
                point3d3 = MathHelper.distanceBearingPoint(point3d2, MathHelper.getBearing(point3d2, item3), MathHelper.calcDistance(point3d2, item3) / 2)
                self.method_13(point3d3, Altitude(self.altitude), point3d2, item3, False, constructionLayer)
            else:
                item4 = self.innerPoints.get_Item(5)
                point3d4 = self.innerPoints.get_Item(4)
                self.method_14(item4, Altitude(point3d4.get_Z()), self.rwyDirection, constructionLayer)
            self.method_14(MathHelper.distanceBearingPoint(self.ptArp, self.rwyDirection + (math.pi / 2), self.radius), Altitude(self.altitude), self.rwyDirection, constructionLayer)

    def vmethod_1(self):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName3D, 127)
        polyline = AcadHelper.smethod_140_v15(self.innerArea, True)
        # polyline.SetDataselfDefaults()
        # polyline.set_Layer(self.layerName3D)
        # polyline.set_Elevation(self.altitude)
        polyline1 = AcadHelper.smethod_140_v15(self.outerArea.PreviewArea, True)
        # polyline1.SetDataselfDefaults()
        # polyline1.set_Layer(self.layerName3D)
        # polyline1.set_Elevation(self.altitude)
        # DBObjectCollection dBObjectCollection = new DBObjectCollection()
        # dBObjectCollection.Add(polyline)
        # DBObjectCollection dBObjectCollection1 = new DBObjectCollection()
        # dBObjectCollection1.Add(polyline1)
        # DBObjectCollection dBObjectCollection2 = Autodesk.AutoCAD.DataselfServices.Region.CreateFromCurves(dBObjectCollection)
        # Autodesk.AutoCAD.DataselfServices.Region item = Autodesk.AutoCAD.DataselfServices.Region.CreateFromCurves(dBObjectCollection1).get_Item(0) as Autodesk.AutoCAD.DataselfServices.Region
        # foreach (Autodesk.AutoCAD.DataselfServices.Region region in dBObjectCollection2)
        # {
        #     item.BooleanOperation(2, region)
        # }
        poly1 = QgsGeometry.fromPolygon([polyline1.method_14_closed()])
        poly0 = QgsGeometry.fromPolygon([polyline.method_14_closed()])
        pointArray = poly1.difference(poly0).asPolygon()[0]
        
        constructionLayer = AcadHelper.createVectorLayer(self.layerName3D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_18(pointArray, constructionLayer)
        # AcadHelper.smethod_25(dBObjectCollection2)
        # AcadHelper.smethod_25(dBObjectCollection)
        # AcadHelper.smethod_25(dBObjectCollection1)

    def vmethod_2(self, obstacle_0):
        double_0 = None
        double_1 = None
        if (not self.outerArea.imethod_0(obstacle_0.Position, obstacle_0.Tolerance)):
            return False, double_0, double_1
        z = obstacle_0.Position.get_Z() + obstacle_0.Trees
        double_0 = self.altitude
        double_1 = z - double_0
        return True, double_0, double_1

class StripSurface(IAerodromeSurfacesSurface):
    # private double length
    #
    # private double width

    def __init__(self, runway_0, aerodromeSurfacesCriteria_0):
        IAerodromeSurfacesSurface.__init__(self)

        self.title = Captions.STRIP
        self.method_1(runway_0, aerodromeSurfacesCriteria_0.Strip)
        self.length = aerodromeSurfacesCriteria_0.Strip.Length
        self.width = aerodromeSurfacesCriteria_0.Strip.Width
        self.area = Point3dCollection()
        for i in range(self.centerLine.get_Count()):
            self.area.Add(MathHelper.distanceBearingPoint(self.centerLine.get_Item(i), self.rwyDirection - (math.pi / 2), self.width))
        for j in range(self.centerLine.get_Count()):
            self.area.Add(MathHelper.distanceBearingPoint(self.centerLine.get_Item(self.centerLine.get_Count() - 1 - j), self.rwyDirection + (math.pi / 2), self.width))

    def vmethod_0(self, bool_0, altitude_0):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName2D, 30)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName2D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_137_v15(self.area, True), constructionLayer)

    def vmethod_1(self):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName3D, 30)
        point3dCollection = Point3dCollection()
        for point3d in self.centerLine:
            point3dCollection.Add(MathHelper.distanceBearingPoint(point3d, self.rwyDirection - (math.pi / 2), self.width))
        point3dCollection1 = Point3dCollection()
        for point3d1 in self.centerLine:
            point3dCollection1.Add(MathHelper.distanceBearingPoint(point3d1, self.rwyDirection + (math.pi / 2), self.width))
            
        constructionLayer = AcadHelper.createVectorLayer(self.layerName3D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_153_v15(point3dCollection, point3dCollection1, constructionLayer)

    def vmethod_2(self, obstacle_0):
        double_0 = None
        double_1 = None
        if (not MathHelper.pointInPolygon(self.area, obstacle_0.Position, obstacle_0.Tolerance)):
            return False, double_0, double_1
        z = obstacle_0.Position.get_Z() + obstacle_0.Trees
        double_0 = self.method_10(obstacle_0)
        double_1 = z - double_0
        return True, double_0, double_1

class TakeOffSurface(IAerodromeSurfacesSurface):
    # private Point3dCollection points1
    #
    # private Point3dCollection points2
    #
    # private double innerEdge
    #
    # private double distFromEND
    #
    # private double divergence
    #
    # private double slope
    #
    # private double length
    #
    # private double finalWidth
    #
    # private bool distFromENDFixed

    def __init__(self, runway_0, aerodromeSurfacesCriteria_0):
        IAerodromeSurfacesSurface.__init__(self)

        self.title = Captions.TAKE_OFF_CLIMB
        self.method_1(runway_0, aerodromeSurfacesCriteria_0.Strip)
        self.distFromEND = aerodromeSurfacesCriteria_0.TakeOff.DistFromEND
        self.distFromENDFixed = aerodromeSurfacesCriteria_0.TakeOff.DistFromENDFixed
        self.innerEdge = aerodromeSurfacesCriteria_0.TakeOff.InnerEdge
        self.divergence = float(aerodromeSurfacesCriteria_0.TakeOff.Divergence)
        self.slope = float(aerodromeSurfacesCriteria_0.TakeOff.Slope)
        self.length = aerodromeSurfacesCriteria_0.TakeOff.Length
        self.finalWidth = aerodromeSurfacesCriteria_0.TakeOff.FinalWidth
        num = self.distFromEND
        origin = Point3D()
        flag = False
        if (runway_0.method_5(PositionType.CWY)):
            if (self.distFromENDFixed):
                origin = runway_0.method_4(PositionType.CWY).Point3d
                flag = True
            elif (MathHelper.calcDistance(runway_0.method_4(PositionType.END).Point3d, runway_0.method_4(PositionType.CWY).Point3d) >= num):
                origin = runway_0.method_4(PositionType.CWY).Point3d
                flag = True
        if (not flag):
            num1 = 0
            num2 = self.indexRwyEnd + 1
            while (True):
                if (num2 < self.centerLine.get_Count()):
                    item = self.centerLine.get_Item(num2 - 1)
                    point3d = self.centerLine.get_Item(num2)
                    num3 = MathHelper.smethod_21(item, point3d, False)
                    if (num1 + num3 >= num):
                        num4 = MathHelper.calcDistance(item, point3d)
                        num5 = math.fabs(item.get_Z() - point3d.get_Z())
                        num6 = math.atan(num5 / num4)
                        num7 = num - num1
                        num8 = num7 * math.sin(num6)
                        origin = MathHelper.distanceBearingPoint(item, MathHelper.getBearing(item, point3d), num7)
                        origin = MathHelper.distanceBearingPoint(item, MathHelper.getBearing(item, point3d), num7).smethod_167(item.get_Z() + num8) if(item.get_Z() <= point3d.get_Z()) else MathHelper.distanceBearingPoint(item, MathHelper.getBearing(item, point3d), num7).smethod_167(item.get_Z() - num8)
                        flag = True
                        break
                    else:
                        num1 = num1 + num3
                        num2 += 1
                else:
                    break
            if (not flag):
                origin = MathHelper.distanceBearingPoint(self.centerLine.get_Item(self.indexLast), self.rwyDirection, num - num1)
        point3d1 = MathHelper.distanceBearingPoint(origin, self.rwyDirection - (math.pi / 2), self.innerEdge / 2)
        point3d2 = MathHelper.distanceBearingPoint(origin, self.rwyDirection + (math.pi / 2), self.innerEdge / 2)
        num9 = (self.finalWidth - self.innerEdge) / 2 / (self.divergence / 100)
        num10 = num9 / math.cos(math.atan(self.divergence / 100))
        z = point3d1.get_Z() + num9 * (self.slope / 100)
        point3d3 = MathHelper.distanceBearingPoint(point3d1, self.rwyDirection - math.atan(self.divergence / 100), num10).smethod_167(z)
        z = point3d2.get_Z() + num9 * (self.slope / 100)
        point3d4 = MathHelper.distanceBearingPoint(point3d2, self.rwyDirection + math.atan(self.divergence / 100), num10).smethod_167(z)
        self.points1 = Point3dCollection()
        self.points1.Add(point3d2)
        self.points1.Add(point3d4)
        self.points1.Add(point3d3)
        self.points1.Add(point3d1)
        self.points2 = None
        if (num9 < self.length):
            point3d1 = point3d3
            point3d2 = point3d4
            num10 = self.length - num9
            z = point3d1.get_Z() + num10 * (self.slope / 100)
            point3d3 = MathHelper.distanceBearingPoint(point3d1, self.rwyDirection, num10).smethod_167(z)
            z = point3d2.get_Z() + num10 * (self.slope / 100)
            point3d4 = MathHelper.distanceBearingPoint(point3d2, self.rwyDirection, num10).smethod_167(z)
            self.points2 = Point3dCollection()
            self.points2.Add(point3d2)
            self.points2.Add(point3d4)
            self.points2.Add(point3d3)
            self.points2.Add(point3d1)
        self.area = Point3dCollection()
        self.area.Add(self.points1.get_Item(0))
        self.area.Add(self.points1.get_Item(1))
        if (self.points2 != None):
            self.area.Add(self.points2.get_Item(1))
            self.area.Add(self.points2.get_Item(2))
        self.area.Add(self.points1.get_Item(2))
        self.area.Add(self.points1.get_Item(3))

    def vmethod_0(self, bool_0, altitude_0):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName2D, 9)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName2D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_137_v15(self.area, True), constructionLayer)
        if (bool_0):
            self.method_15(self.points1.get_Item(3), self.points1.get_Item(0), self.points1.get_Item(2), self.points1.get_Item(1), altitude_0, self.slope, self.rwyDirection, self.length, True, self.points2 == None, constructionLayer)
            if (self.points2 != None):
                self.method_15(self.points2.get_Item(3), self.points2.get_Item(0), self.points2.get_Item(2), self.points2.get_Item(1), altitude_0, self.slope, self.rwyDirection, self.length, False, True, constructionLayer)

    def vmethod_1(self):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName3D, 9)
        point3dCollection = Point3dCollection()
        point3dCollection1 = Point3dCollection()
        point3dCollection.Add(self.points1.get_Item(0))
        point3dCollection.Add(self.points1.get_Item(1))
        point3dCollection1.Add(self.points1.get_Item(3))
        point3dCollection1.Add(self.points1.get_Item(2))
        if (self.points2 != None):
            point3dCollection.Add(self.points2.get_Item(1))
            point3dCollection1.Add(self.points2.get_Item(2))
        constructionLayer = AcadHelper.createVectorLayer(self.layerName3D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_153_v15(point3dCollection, point3dCollection1, constructionLayer)

    def vmethod_2(self, obstacle_0):
        # Point3d point3d
        double_0 = None
        double_1 = None
        if (not MathHelper.pointInPolygon(self.area, obstacle_0.Position, obstacle_0.Tolerance)):
            return False, double_0, double_1
        z = obstacle_0.Position.get_Z() + obstacle_0.Trees
        item = self.points1.get_Item(0)
        item1 = self.points1.get_Item(3)
        point3d = MathHelper.getIntersectionPoint(item, item1, obstacle_0.Position, MathHelper.distanceBearingPoint(obstacle_0.Position, self.rwyDirection + math.pi, 100))
        num = max(MathHelper.calcDistance(point3d, obstacle_0.Position) - obstacle_0.Tolerance, 0)
        double_0 = item.get_Z() + num * (self.slope / 100)
        double_1 = z - double_0
        return True, double_0, double_1

class TransitionalSurface(IAerodromeSurfacesSurface):
    # private Point3dCollection points1R
    #
    # private Point3dCollection points2R
    #
    # private Point3dCollection points1L
    #
    # private Point3dCollection points2L
    #
    # private Point3dCollection areaR
    #
    # private Point3dCollection areaL
    #
    # private double slope

    def __init__(self, runway_0, aerodromeSurfacesCriteria_0, altitude_0):
        IAerodromeSurfacesSurface.__init__(self)

        self.title = Captions.TRANSITIONAL
        self.method_1(runway_0, aerodromeSurfacesCriteria_0.Strip)
        self.slope = float(aerodromeSurfacesCriteria_0.Transitional.Slope)
        metres = altitude_0.Metres + aerodromeSurfacesCriteria_0.InnerHorizontal.Height
        num = self.rwyDirection + math.pi
        point3d = self.method_6(aerodromeSurfacesCriteria_0)
        point3d1 = self.method_7(aerodromeSurfacesCriteria_0)
        z = (metres - point3d1.get_Z()) / (float(aerodromeSurfacesCriteria_0.Approach.Slope1) / 100)
        z = z / math.cos(math.atan(float(aerodromeSurfacesCriteria_0.Approach.Divergence) / 100))
        self.points1R = Point3dCollection()
        self.points1R.Add(MathHelper.distanceBearingPoint(point3d1, num + math.atan(float(aerodromeSurfacesCriteria_0.Approach.Divergence) / 100), z).smethod_167(metres))
        self.points1R.Add(point3d1)
        for i in range(self.indexRwyThr, self.centerLine.get_Count()):
            self.points1R.Add(MathHelper.distanceBearingPoint(self.centerLine.get_Item(i), self.rwyDirection - (math.pi / 2), aerodromeSurfacesCriteria_0.Strip.Width))
        self.points2R = Point3dCollection()
        for j in range(self.points1R.get_Count()):
            item = self.points1R.get_Item(j)
            z = (metres - item.get_Z()) / (self.slope / 100)
            self.points2R.Add(MathHelper.distanceBearingPoint(self.points1R.get_Item(j), self.rwyDirection - (math.pi / 2), z).smethod_167(metres))
        z = (metres - point3d.get_Z()) / (float(aerodromeSurfacesCriteria_0.Approach.Slope1) / 100)
        z = z / math.cos(math.atan(float(aerodromeSurfacesCriteria_0.Approach.Divergence) / 100))
        self.points1L = Point3dCollection()
        self.points1L.Add(MathHelper.distanceBearingPoint(point3d, num - math.atan(float(aerodromeSurfacesCriteria_0.Approach.Divergence) / 100), z).smethod_167(metres))
        self.points1L.Add(point3d)
        for k in range(self.indexRwyThr, self.centerLine.get_Count()):
            self.points1L.Add(MathHelper.distanceBearingPoint(self.centerLine.get_Item(k), self.rwyDirection + (math.pi / 2), aerodromeSurfacesCriteria_0.Strip.Width))
        self.points2L = Point3dCollection()
        for l in range(self.points1L.get_Count()):
            item1 = self.points1L.get_Item(l)
            z = (metres - item1.get_Z()) / (self.slope / 100)
            self.points2L.Add(MathHelper.distanceBearingPoint(self.points1L.get_Item(l), self.rwyDirection + (math.pi / 2), z).smethod_167(metres))
        self.areaR = Point3dCollection()
        for m in range(self.points2R.get_Count()):
            self.areaR.Add(self.points2R.get_Item(m))
        for n in range(self.points1R.get_Count()):
            self.areaR.Add(self.points1R.get_Item(self.points1R.get_Count() - 1 - n))
        self.areaL = Point3dCollection()
        for o in range(self.points2L.get_Count()):
            self.areaL.Add(self.points2L.get_Item(o))
        for p in range(self.points1L.get_Count()):
            self.areaL.Add(self.points1L.get_Item(self.points1L.get_Count() - 1 - p))
        self.area = Point3dCollection()
        for q in range(self.points2R.get_Count()):
            self.area.Add(self.points2R.get_Item(q))
        for r in range(self.points2L.get_Count()):
            self.area.Add(self.points2L.get_Item(self.points2L.get_Count() - 1 - r))

    def vmethod_0(self, bool_0, altitude_0):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName2D, 6)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName2D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_137_v15(self.areaR, True), constructionLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_137_v15(self.areaL, True), constructionLayer)
        if (bool_0):
            self.method_16(self.points1R, self.points2R, altitude_0, self.slope, self.rwyDirection - (math.pi / 2), 2, constructionLayer)
            self.method_16(self.points1L, self.points2L, altitude_0, self.slope, self.rwyDirection + (math.pi / 2), 2, constructionLayer)

    def vmethod_1(self):
        # AcadHelper.smethod_42(AerodromeSurfaces.space.get_Dataself(), self.layerName3D, 6)
        constructionLayer = AcadHelper.createVectorLayer(self.layerName3D)
        AerodromeSurfacesDlg.constructionLayers.append(constructionLayer)
        AcadHelper.smethod_153_v15(self.points1R, self.points2R, constructionLayer)
        AcadHelper.smethod_153_v15(self.points1L, self.points2L, constructionLayer)

    def vmethod_2(self, obstacle_0):
        double_0 = None
        double_1 = None
        if (MathHelper.pointInPolygon(self.areaR, obstacle_0.Position, obstacle_0.Tolerance)):
            z = obstacle_0.Position.get_Z() + obstacle_0.Trees
            double_0 = self.method_12(obstacle_0, self.points1R, self.points2R)
            double_1 = z - double_0
            return True, double_0, double_1
        if (not MathHelper.pointInPolygon(self.areaL, obstacle_0.Position, obstacle_0.Tolerance)):
            return False, double_0, double_1
        num = obstacle_0.Position.get_Z() + obstacle_0.Trees
        double_0 = self.method_12(obstacle_0, self.points1L, self.points2L)
        double_1 = num - double_0
        return True, double_0, double_1