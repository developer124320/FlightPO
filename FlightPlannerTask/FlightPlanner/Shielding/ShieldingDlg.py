# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QSize, Qt, QString,QVariant
from PyQt4.QtGui import QMessageBox, QStandardItem,QApplication, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsVectorFileWriter,QgsPalLayerSettings,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import TurnDirection, AerodromeSurfacesInnerHorizontalLocation, SurfaceTypes, ObstacleTableColumnType,AircraftSpeedCategory,\
    AerodromeSurfacesCriteriaType, AltitudeUnits, ObstacleAreaResult, Formating, RnavGnssFlightPhase, Point3D, AngleUnits, ConstructionType
from FlightPlanner.Shielding.Ui_ShieldingGeneral import Ui_ShieldingGeneral
from FlightPlanner.Shielding.Ui_ShieldingAltitude import Ui_ShieldingAltitude
from FlightPlanner.expressions import Expressions
from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.QgisHelper import QgisHelper, Geo
from FlightPlanner.RnavTolerance0 import RnavGnssTolerance
from FlightPlanner.Captions import Captions
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.types import Point3D, Point3dCollection, NavigationalAidType, CriticalObstacleType,\
    AerodromeSurfacesApproachType, ObstacleEvaluationMode
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, SecondaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable, Obstacle
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.Confirmations import Confirmations
from FlightPlanner.Dialogs.DlgNavigationalAid import DlgNavigationalAid
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
from Type.NavigationalAid import NavigationalAidList, DirectionalNavigationalAid, LineOfSight, OmnidirectionalNavigationalAid
import define, math
class ShieldingDlg(FlightPlanBaseDlg):

    GPS_SLOPE_DEG = 5
    GPS_SLOPE_RAD = 0.0872664625997165
    navAids = None
    obstaclesChecked = None
    obstacles = None
    obscursionsChecked = None
    obscursions = None
    constructionLayers = []


    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        # self.parametersPanelAltitude = None
        self.setObjectName("ShieldingDlg")
        self.surfaceType = SurfaceTypes.Shielding
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.Shielding)
        self.resize(600, 610)
        QgisHelper.matchingDialogSize(self, 650, 400)
        self.surfaceList = None
        self.updating = False

        self.calculationResults = []

        self.resultLayerList = []

        self.arpFeatureArray = []
        self.currentLayer = define._canvas.currentLayer()
        self.rwyFeatureArray = []
        # self.initAerodromeAndRwyCmb()
        
        #############  init part   #########




    def initAerodromeAndRwyCmb(self):

        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.arpFeatureArray = self.aerodromeAndRwyCmbFill(self.currentLayer, self.parametersPanel.cmbAerodrome, self.parametersPanel.pnlArp, self.parametersPanel.cmbRwyDir)
            self.calcRwyBearing()
    def calcRwyBearing(self):
        try:
            point3End = self.parametersPanel.pnlThrEnd.Point3d
            point3dThr = self.parametersPanel.pnlThr.Point3d
            self.parametersPanel.pnlRwyDir.Value = round(Unit.ConvertRadToDeg(MathHelper.getBearing(point3dThr, point3End)), 4)
        except:
            pass

    def aerodromeAndRwyCmbFill(self, layer, aerodromeCmbObj, aerodromePositionPanelObj, rwyDirCmbObj = None):
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')
        arpList = []
        arpFeatureList = []
        if idx >= 0:
            featIter = layer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idx].toString()
                attrValue = QString(attrValue)
                attrValue = attrValue.replace(" ", "")
                attrValue = attrValue.toUpper()
                if attrValue == "AERODROMEREFERENCEPOINT":
                    arpList.append(attrValue)
                    arpFeatureList.append(feat)
            if len(arpList) != 0:

                i = -1
                attrValueList = []
                for feat in arpFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    items = attrValueList
                    if len(items) != 0:
                        existFlag = False
                        for item in items:
                            if item == attrValue:
                                existFlag = True
                        if existFlag:
                            continue
                    attrValueList.append(attrValue)
                attrValueList.sort()
                aerodromeCmbObj.Items = attrValueList
                aerodromeCmbObj.SelectedIndex = 0

                # if idxAttributes
                for feat in arpFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    if attrValue != aerodromeCmbObj.SelectedItem:
                        continue
                    attrValue = feat.attributes()[idxLat].toDouble()
                    lat = attrValue[0]

                    attrValue = feat.attributes()[idxLong].toDouble()
                    long = attrValue[0]

                    attrValue = feat.attributes()[idxAltitude].toDouble()
                    alt = attrValue[0]

                    aerodromePositionPanelObj.Point3d = Point3D(long, lat, alt)
                    self.connect(aerodromeCmbObj, SIGNAL("Event_0"), self.aerodromeCmbObj_Event_0)
                    break
            if rwyDirCmbObj != None:
                idxAttr = layer.fieldNameIndex('Attributes')
                if idxAttr >= 0:
                    rwyFeatList = []
                    featIter = layer.getFeatures()
                    rwyDirCmbObjItems = []
                    for feat in featIter:
                        attrValue = feat.attributes()[idxAttr].toString()
                        if attrValue == aerodromeCmbObj.SelectedItem:
                            attrValue = feat.attributes()[idxName].toString()
                            s = attrValue.replace(" ", "")
                            compStr = s.left(6).toUpper()
                            if compStr == "THRRWY":
                                valStr = s.right(s.length() - 6)
                                rwyDirCmbObjItems.append(aerodromeCmbObj.SelectedItem + " RWY " + valStr)
                                rwyFeatList.append(feat)
                    rwyDirCmbObjItems.sort()
                    rwyDirCmbObj.Items = rwyDirCmbObjItems
                    self.connect(rwyDirCmbObj, SIGNAL("Event_0"), self.rwyDirCmbObj_Event_0)
                    self.rwyFeatureArray = rwyFeatList
                    self.rwyDirCmbObj_Event_0()

                    self.aerodromeCmbObj_Event_0()
                    self.calcRwyBearing()
        return arpFeatureList
    def rwyDirCmbObj_Event_0(self):
        if len(self.rwyFeatureArray) == 0:
            return
        idxName = self.currentLayer.fieldNameIndex('Name')
        idxLat = self.currentLayer.fieldNameIndex('Latitude')
        idxLong = self.currentLayer.fieldNameIndex('Longitude')
        idxAltitude = self.currentLayer.fieldNameIndex('Altitude')
        idxAttr = self.currentLayer.fieldNameIndex('Attributes')
        featIter = self.currentLayer.getFeatures()
        for feat in self.rwyFeatureArray:
            attrValue = feat.attributes()[idxName].toString()
            attrValueStr = QString(attrValue)
            attrValueStr = attrValueStr.replace(" ", "").right(attrValueStr.length() - 3)
            itemStr = self.parametersPanel.cmbRwyDir.SelectedItem
            itemStr = QString(itemStr)
            itemStr = itemStr.replace(" ", "").right(itemStr.length() - 4)
            if attrValueStr != itemStr:
                continue
            latAttrValue = feat.attributes()[idxLat].toDouble()
            lat = latAttrValue[0]

            longAttrValue = feat.attributes()[idxLong].toDouble()
            long = longAttrValue[0]

            altAttrValue = feat.attributes()[idxAltitude].toDouble()
            alt = altAttrValue[0]

            self.parametersPanel.pnlThr.Point3d = Point3D(long, lat, alt)

            valStr = None
            if attrValue.right(1).toUpper() =="L" or attrValue.right(1).toUpper() =="R":
                s = attrValue.left(attrValue.length() - 1)
                valStr = s.right(2)
            else:
                valStr = attrValue.right(2)
            val = int(valStr)
            val += 18
            if val > 36:
                val -= 36
            newValStr = None
            if len(str(val)) == 1:
                newValStr = "0" + str(val)
            else:
                newValStr = str(val)
            otherAttrValue = attrValue.replace(valStr, newValStr)
            ss = otherAttrValue.right(1)
            if ss.toUpper() == "L":
                otherAttrValue = otherAttrValue.left(otherAttrValue.length() - 1) + "R"
            elif ss.toUpper() == "R":
                otherAttrValue = otherAttrValue.left(otherAttrValue.length() - 1) + "L"
            for feat in self.rwyFeatureArray:
                attrValue = feat.attributes()[idxName].toString()
                if attrValue != otherAttrValue:
                    continue
                latAttrValue = feat.attributes()[idxLat].toDouble()
                lat = latAttrValue[0]

                longAttrValue = feat.attributes()[idxLong].toDouble()
                long = longAttrValue[0]

                altAttrValue = feat.attributes()[idxAltitude].toDouble()
                alt = altAttrValue[0]

                self.parametersPanel.pnlThrEnd.Point3d = Point3D(long, lat, alt)
                break
            break
        self.calcRwyBearing()
    def aerodromeCmbObj_Event_0(self):
        if len(self.arpFeatureArray) == 0:
            return
        self.parametersPanel.pnlArp.Point3d = None
        self.parametersPanel.pnlThr.Point3d = None
        self.parametersPanel.pnlThrEnd.Point3d = None
        idxName = self.currentLayer.fieldNameIndex('Name')
        idxLat = self.currentLayer.fieldNameIndex('Latitude')
        idxLong = self.currentLayer.fieldNameIndex('Longitude')
        idxAltitude = self.currentLayer.fieldNameIndex('Altitude')
        self.rwyFeatureArray = []
        # if idxAttributes
        for feat in self.arpFeatureArray:
            attrValue = feat.attributes()[idxName].toString()
            if attrValue != self.parametersPanel.cmbAerodrome.SelectedItem:
                continue
            attrValue = feat.attributes()[idxLat].toDouble()
            lat = attrValue[0]

            attrValue = feat.attributes()[idxLong].toDouble()
            long = attrValue[0]

            attrValue = feat.attributes()[idxAltitude].toDouble()
            alt = attrValue[0]

            self.parametersPanel.pnlArp.Point3d = Point3D(long, lat, alt)
            break
        idxAttr = self.currentLayer.fieldNameIndex('Attributes')
        if idxAttr >= 0:
            self.parametersPanel.cmbRwyDir.Clear()
            rwyFeatList = []
            featIter = self.currentLayer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idxAttr].toString()
                if attrValue == self.parametersPanel.cmbAerodrome.SelectedItem:
                    attrValue = feat.attributes()[idxName].toString()
                    s = attrValue.replace(" ", "")
                    compStr = s.left(6).toUpper()
                    if compStr == "THRRWY":
                        valStr = s.right(s.length() - 6)
                        self.parametersPanel.cmbRwyDir.Add(self.parametersPanel.cmbAerodrome.SelectedItem + " RWY " + valStr)
                        rwyFeatList.append(feat)
                        self.rwyFeatureArray = rwyFeatList
            self.rwyDirCmbObj_Event_0()

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
#         self.filterList = []
#         for taaArea in self.taaCalculationAreas:
#             self.filterList.append(taaArea.title)
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.Shielding, self.ui.tblObstacles, None, parameterList, resultHideColumnNames )
#         self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)

    def getParameterList(self):
        parameterList = []
        parameterList.append(("General", "group"))
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Navigation Type", self.parametersPanel.pnlNavType.SelectedItem))

        if (self.parametersPanel.pnlNavType.SelectedIndex != 0):
            parameterList.append(("Waypoint1", "group"))
            # longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlNavAid.txtPointX.text()), float(self.parametersPanel.pnlNavAid.txtPointY.text()))
            parameterList.append(("Lat", self.parametersPanel.pnlWaypoint1.txtLat.Value))
            parameterList.append(("Lon", self.parametersPanel.pnlWaypoint1.txtLong.Value))
            parameterList.append(("X", self.parametersPanel.pnlWaypoint1.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlWaypoint1.txtPointY.text()))
            parameterList.append(("Turning Waypoint", self.parametersPanel.chbTurningWaypoint1.Checked))

            parameterList.append(("Waypoint2", "group"))
            # longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlNavAid.txtPointX.text()), float(self.parametersPanel.pnlNavAid.txtPointY.text()))
            parameterList.append(("Lat", self.parametersPanel.pnlWaypoint2.txtLat.Value))
            parameterList.append(("Lon", self.parametersPanel.pnlWaypoint2.txtLong.Value))
            parameterList.append(("X", self.parametersPanel.pnlWaypoint2.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlWaypoint2.txtPointY.text()))
            parameterList.append(("Turning Waypoint", self.parametersPanel.chbTurningWaypoint2.Checked))

            parameterList.append(("Minimum Altitude", self.parametersPanel.pnlMinimumAltitude.txtAltitudeM.text() + "m"))
            parameterList.append(("", self.parametersPanel.pnlMinimumAltitude.txtAltitudeFt.text() + "ft"))

            parameterList.append(("Segment Width", str(self.parametersPanel.pnlSegmentWidth.Value.NauticalMiles) + "nm"))
            parameterList.append(("Allow for Earth Curvature", self.parametersPanel.chbEarthCurvature.Checked))

            parameterList.append(("Construction", "group"))
            parameterList.append(("Construction Type", self.parametersPanel.pnlConstructionType.SelectedItem))
            parameterList.append(("Mark Contour Altitudes", self.parametersPanel.chbMarkAltitudes.Checked))
            if self.parametersPanel.chbMarkAltitudes.Checked:
                parameterList.append(("Every", self.parametersPanel.pnlAltitudesEvery.txtAltitudeM.text() + "m"))
                parameterList.append(("", self.parametersPanel.pnlAltitudesEvery.txtAltitudeFt.text() + "ft"))
                parameterList.append(("Text Height", self.parametersPanel.pnlAltitudesTextHeight.numberBox.text()))
        else:
            parameterList.append(("Navigational Aid", "group"))
            parameterList.append(("", self.parametersPanel.pnlNavAid.SelectedItem.ToString()))
            # longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlNavAid.txtPointX.text()), float(self.parametersPanel.pnlNavAid.txtPointY.text()))
            parameterList.append(("Position", "group"))
            parameterList.append(("Lat", self.parametersPanel.pnlNavAidPos.txtLat.Value))
            parameterList.append(("Lon", self.parametersPanel.pnlNavAidPos.txtLong.Value))
            parameterList.append(("X", self.parametersPanel.pnlNavAidPos.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlNavAidPos.txtPointY.text()))
            parameterList.append(("Altitude", self.parametersPanel.pnlNavAidPos.txtAltitudeFt.text() + "ft"))
            parameterList.append(("", self.parametersPanel.pnlNavAidPos.txtAltitudeM.text() + "m"))
            if(isinstance(self.parametersPanel.pnlNavAid.SelectedItem, DirectionalNavigationalAid)) or isinstance(self.parametersPanel.pnlNavAid.SelectedItem, LineOfSight):
                parameterList.append(("Track", "Plan : " + str(self.parametersPanel.pnlTrack.txtRadialPlan.Value) + define._degreeStr))
                parameterList.append(("", "Geodetic : " + str(self.parametersPanel.pnlTrack.txtRadialGeodetic.Value) + define._degreeStr))
            if(not isinstance(self.parametersPanel.pnlNavAid.SelectedItem, DirectionalNavigationalAid)):
                pass
            elif self.parametersPanel.pnlNavAid.SelectedItem.a.IsNaN():
                parameterList.append(("Distance to Threshold", str(self.parametersPanel.pnlDistToThr.Value.Metres) + "m"))
            parameterList.append(("Allow for Earth Curvature", self.parametersPanel.chbEarthCurvature.Checked))

            parameterList.append(("Construction", "group"))
            parameterList.append(("Construction Type", self.parametersPanel.pnlConstructionType.SelectedItem))
            if self.parametersPanel.pnlConstructionType.SelectedItem == ConstructionType.Construct2D:
                parameterList.append(("Mark Contour Altitudes", self.parametersPanel.chbMarkAltitudes.Checked))
                if self.parametersPanel.chbMarkAltitudes.Checked:
                    parameterList.append(("Every", self.parametersPanel.pnlAltitudesEvery.txtAltitudeM.text() + "m"))
                    parameterList.append(("", self.parametersPanel.pnlAltitudesEvery.txtAltitudeFt.text() + "ft"))
                    parameterList.append(("Text Height", self.parametersPanel.pnlAltitudesTextHeight.numberBox.text()))
            else:
                parameterList.append(("Rendering Quality", str(self.parametersPanel.trackBar.value())))

        parameterList.append(("Altitude of a position_Results", "group"))
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Mode", self.parametersPanelAltitude.pnlEvalMode.SelectedItem))
        if self.parametersPanelAltitude.pnlEvalMode.SelectedIndex == 0:
            parameterList.append(("Position", "group"))
            parameterList.append(("ID", self.parametersPanelAltitude.pnlEvalPosition.txtID.text()))
            parameterList.append(("Lat", self.parametersPanelAltitude.pnlEvalPosition.txtLat.Value))
            parameterList.append(("Lon", self.parametersPanelAltitude.pnlEvalPosition.txtLong.Value))
            parameterList.append(("X", self.parametersPanelAltitude.pnlEvalPosition.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanelAltitude.pnlEvalPosition.txtPointY.text()))
            parameterList.append(("Altitude", self.parametersPanelAltitude.pnlEvalPosition.txtAltitudeFt.text() + "ft"))
            parameterList.append(("", self.parametersPanelAltitude.pnlEvalPosition.txtAltitudeM.text() + "m"))

            parameterList.append(("Insert Point And Text", self.parametersPanelAltitude.chbInsertPointAndText.Checked))
            parameterList.append(("Text Height", self.parametersPanelAltitude.pnlAnnotationTextHeight.numberBox.text()))
        else:
            parameterList.append(("Evaluate Only Penetrating Obstacles", self.parametersPanelAltitude.chbInsertPointAndText.Checked))



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
        self.ui.tabCtrlGeneral.removeTab(2)
        self.ui.btnPDTCheck.setVisible(False)
        return FlightPlanBaseDlg.uiStateInit(self)
    def initSurfaceCombo(self):
        pass
        self.method_34(self.parametersPanel.pnlNavAid.SelectedItem)
    def btnEvaluate_Click(self):
        num = Geo.EarthRadius().Metres if(self.parametersPanel.chbEarthCurvature.Checked) else 0.0
        if (self.parametersPanel.pnlNavType.SelectedIndex != 0):
            self.obstaclesModel= ShieldingObstacles(self.parametersPanel.pnlNavType.SelectedItem, [self.parametersPanel.pnlWaypoint1.Point3d, self.parametersPanel.chbTurningWaypoint1.Checked, self.parametersPanel.pnlWaypoint2.Point3d, self.parametersPanel.chbTurningWaypoint2.Checked, self.parametersPanel.pnlSegmentWidth.Value, self.parametersPanel.pnlMinimumAltitude.Value, num, self.parametersPanelAltitude.chbOnlyPenetratingObstacles.Checked])
        else:
            selectedItem = self.parametersPanel.pnlNavAid.SelectedItem
            self.obstaclesModel = ShieldingObstacles(self.parametersPanel.pnlNavType.SelectedItem, [selectedItem, self.parametersPanel.pnlNavAidPos.Point3d, self.parametersPanel.pnlTrack.Value, self.parametersPanel.pnlDistToThr.Value, num, self.parametersPanelAltitude.chbOnlyPenetratingObstacles.Checked])
        if self.parametersPanelAltitude.pnlEvalMode.SelectedIndex == 1:
            return FlightPlanBaseDlg.btnEvaluate_Click(self)
        else:
            self.obstaclesModel.clear()
            if not self.parametersPanelAltitude.pnlEvalPosition.IsValid():
                return
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
            self.obstaclesModel.checkObstacle(obstacle)
            string0 = self.obstaclesModel.singlePointDisplayName
            if string0 == None:
                self.ui.tblObstacles.setModel(self.obstaclesModel)
                return

            AcadHelper.setGeometryAndAttributesInLayer(pointLayer, point3d, False, {"Caption":string0})

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

                fontSize = self.parametersPanelAltitude.pnlAnnotationTextHeight.Value

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
        
    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        if self.parametersPanel.pnlConstructionType.SelectedItem == ConstructionType.Construct2D:
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType)
            self.method_57(constructionLayer)
        else:
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Polygon)
            self.method_54(constructionLayer)
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], self.surfaceType)
        QgisHelper.zoomToLayers([constructionLayer])

    def initParametersPan(self):
        ui0 = Ui_ShieldingGeneral()
        self.parametersPanel = ui0
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanelAltitude = Ui_ShieldingAltitude(self.ui.grbResult)
        self.ui.vlResultGroup.insertWidget(0, self.parametersPanelAltitude)

        self.ui.tabCtrlGeneral.setTabText(1, "Altitude of a Position / Results")
        self.ui.vlResultBtns.insertWidget(0, self.ui.btnEvaluate)
        self.ui.btnEvaluate.setEnabled(True)

        self.parametersPanel.pnlNavType.Items = [Captions.CONVENTIONAL, Captions.GPS]
        if (ShieldingDlg.navAids == None):
            ShieldingDlg.navAids = NavigationalAidList.smethod_0(None)
        self.method_34(ShieldingDlg.navAids[0])
        self.parametersPanelAltitude.pnlEvalMode.Items = ObstacleEvaluationMode.Items

        self.parametersPanel.pnlConstructionType.Items = [ConstructionType.Construct2D, ConstructionType.Construct3D]


        # self.connect(self.parametersPanel.chbMarkAltitudes, SIGNAL("Event_0"), self.chbMarkAltitudes_Event_0)
        # self.connect(self.parametersPanelAltitude.chbInsertPointAndText, SIGNAL("Event_0"), self.chbInsertPointAndText_Event_0)
        self.connect(self.parametersPanel.pnlConstructionType, SIGNAL("Event_0"), self.method_38)
        # self.ui.tabCtrlGeneral.currentChanged.connect(self.tabControl_SelectedIndexChanged)
        # self.connect(self.parametersPanel.chbSecondSlope, SIGNAL("Event_0"), self.chbSecondSlope_Event_0)
        # self.connect(self.parametersPanel.chbDepTrackMoreThan15, SIGNAL("Event_0"), self.chbDepTrackMoreThan15_Event_0)
        # self.connect(self.parametersPanel.pnlApproachObstacleAltitude, SIGNAL("Event_0"), self.pnlApproachObstacleAltitude_Event_0)
        # #
        self.connect(self.parametersPanel.pnlNavAid, SIGNAL("Event_0"), self.method_38)
        self.connect(self.parametersPanel.pnlNavType, SIGNAL("Event_0"), self.method_38)
        self.connect(self.parametersPanel.chbMarkAltitudes, SIGNAL("Event_0"), self.chbMarkAltitudes_Click)
        self.connect(self.parametersPanelAltitude.chbInsertPointAndText, SIGNAL("Event_0"), self.chbInsertPointAndText_Click)
        # self.connect(self.parametersPanel.pnlDatumElevation, SIGNAL("Event_0"), self.pnlDatumElevation_Event_0)
        # self.connect(self.parametersPanel.pnlRwyCode, SIGNAL("Event_0"), self.pnlRwyCode_Event_0)
        # self.connect(self.parametersPanel.pnlRunway, SIGNAL("Event_0"), self.pnlRunway_Event_0)
        # self.connect(self.parametersPanelAltitude.pnlEvalMode, SIGNAL("Event_0"), self.pnlEvalMode_Event_0)
        # # self.connect(self.parametersPanel.pnlVPA, SIGNAL("Event_0"), self.pnlVPA_Event_0)
        # # self.connect(self.parametersPanel.pnlRDH, SIGNAL("Event_0"), self.pnlRDH_Event_0)
        # # self.connect(self.parametersPanel.pnlOCAH, SIGNAL("Event_0"), self.pnlOCAH_Event_0)
        self.connect(self.parametersPanelAltitude.pnlEvalMode, SIGNAL("Event_0"), self.method_32)
        self.connect(self.parametersPanel.pnlWaypoint1, SIGNAL("positionChanged"), self.method_38)
        self.connect(self.parametersPanel.pnlNavAidPos, SIGNAL("positionChanged"), self.method_38)
        self.ui.tabCtrlGeneral.currentChanged.connect(self.method_32)
        # # self.connect(self.parametersPanel.pnlMinTemp, SIGNAL("Event_0"), self.pnlMinTemp_Event_0)
        # #
        # #
        # #
        # # self.ui.cmbUnits.currentIndexChanged.connect(self.setCriticalObstacle)
        # self.parametersPanel.btnCriteriaModify.clicked.connect(self.btnCriteriaModify_Click)
        # self.parametersPanel.btnCriteriaRemove.clicked.connect(self.btnCriteriaRemove_Click)
        self.parametersPanel.btnNavAidAdd.clicked.connect(self.btnNavAidAdd_Click)
        self.parametersPanel.btnNavAidModify.clicked.connect(self.btnNavAidModify_Click)
        self.parametersPanel.btnNavAidRemove.clicked.connect(self.btnNavAidRemove_Click)
        self.method_32()
        self.isWorking = False

    def btnNavAidAdd_Click(self):
        navigationalAid = None
        if (self.parametersPanel.pnlNavAid.SelectedIndex > -1):
            selectedItem = self.parametersPanel.pnlNavAid.SelectedItem
            extendedDialogResult = QMessageBox.question(self, "Question", Confirmations.COPY_SELECTED_RECORD%(selectedItem.Name), QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if (extendedDialogResult == QMessageBox.Cancel):
                return
            if (extendedDialogResult == QMessageBox.Yes):
                navigationalAid = selectedItem.vmethod_0("")
        result, navigationalAid = DlgNavigationalAid.smethod_0(self, navigationalAid)
        if (result):
            ShieldingDlg.navAids.Add(navigationalAid)
            ShieldingDlg.navAids.method_0(self)
            ShieldingDlg.navAids.method_1()
            self.method_34(navigationalAid)
            self.method_32()


    def btnNavAidModify_Click(self):
        selectedItem = self.parametersPanel.pnlNavAid.SelectedItem
        if (selectedItem == None):
            return
        num = ShieldingDlg.navAids.IndexOf(selectedItem)
        if (DlgNavigationalAid.smethod_0(self, selectedItem)):
            ShieldingDlg.navAids[num] = selectedItem
            ShieldingDlg.navAids.method_0(self)
            ShieldingDlg.navAids.method_1()
            self.method_34(selectedItem)
            self.method_32()

    def btnNavAidRemove_Click(self):
        selectedItem = self.parametersPanel.pnlNavAid.SelectedItem
        if (selectedItem == None):
            return
        if (QMessageBox.question(self, "Question", Confirmations.DELETE_NAV_AID%(selectedItem.Name), QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes):
            num = self.parametersPanel.pnlNavAid.IndexOf(selectedItem)
            ShieldingDlg.navAids.Remove(selectedItem)
            ShieldingDlg.navAids.method_0(self)
            num = min(num, self.parametersPanel.pnlNavAid.Count - 1)
            self.method_33(num)
            self.method_32()

    def chbMarkAltitudes_Click(self):
        self.parametersPanel.pnlAltitudesEvery.Enabled = self.parametersPanel.chbMarkAltitudes.Checked
        self.parametersPanel.pnlAltitudesTextHeight.Enabled = self.parametersPanel.chbMarkAltitudes.Checked

    def chbInsertPointAndText_Click(self):
        self.parametersPanelAltitude.pnlAnnotationTextHeight.Enabled = self.parametersPanelAltitude.chbInsertPointAndText.Checked

    def method_32(self):
    #     self.gbParameters.SuspendLayout()
    #     self.gbConstruction.SuspendLayout()
    #     self.gbEvalParameters.SuspendLayout()
    #     try
    #     {
        if (self.ui.tabCtrlGeneral.currentIndex() == 0):
            if (self.parametersPanel.pnlNavType.SelectedIndex != 0):
                self.parametersPanel.gbNavAid.Visible = False
                self.parametersPanel.gbWaypoint1.Visible = True
                self.parametersPanel.gbWaypoint2.Visible = True
                self.parametersPanel.pnlTrack.Visible = False
                self.parametersPanel.pnlDistToThr.Visible = False
                self.parametersPanel.pnlMinimumAltitude.Visible = True
                self.parametersPanel.pnlSegmentWidth.Visible = True
            else:
                selectedItem = self.parametersPanel.pnlNavAid.SelectedItem
                self.parametersPanel.gbNavAid.Visible = True
                self.parametersPanel.gbWaypoint1.Visible = False
                self.parametersPanel.gbWaypoint2.Visible = False
                self.parametersPanel.pnlTrack.Visible = True if(isinstance(selectedItem, DirectionalNavigationalAid)) else isinstance(selectedItem, LineOfSight)
                self.parametersPanel.pnlDistToThr.Visible = False if(not isinstance(selectedItem, DirectionalNavigationalAid)) else selectedItem.a.IsNaN()
                self.parametersPanel.pnlMinimumAltitude.Visible = False
                self.parametersPanel.pnlSegmentWidth.Visible = False
            self.parametersPanel.pnlMarkAltitudes.Visible = self.parametersPanel.pnlConstructionType.SelectedItem == ConstructionType.Construct2D
            self.parametersPanel.pnlAltitudesTextHeight.Visible = self.parametersPanel.pnlConstructionType.SelectedItem == ConstructionType.Construct2D
            self.parametersPanel.pnl3DQuality.Visible = self.parametersPanel.pnlConstructionType.SelectedItem == ConstructionType.Construct3D
        else:#if (self.tabControl.SelectedIndex == 1)
            selectedIndex = self.parametersPanelAltitude.pnlEvalMode.SelectedIndex == 0
            self.parametersPanelAltitude.chbOnlyPenetratingObstacles.Checked = False
            self.parametersPanelAltitude.pnlEvalPosition.Visible = selectedIndex
            self.parametersPanelAltitude.pnlInsertPointAndText.Visible = selectedIndex
            self.parametersPanelAltitude.chbOnlyPenetratingObstacles.Visible = not selectedIndex
        #     }
        # }
        # finally
        # {
        #     self.gbParameters.ResumeLayout()
        #     self.gbConstruction.ResumeLayout()
        #     self.gbEvalParameters.ResumeLayout()
        # }
    def method_33(self, int_0):
        # if (this.pnlNavAid.DataSource != null)
        # {
        #     this.pnlNavAid.ComboBox.DataSource = null
        # }
        # this.pnlNavAid.DataSource = Shielding.navAids
        # this.pnlNavAid.DisplayMember = "DisplayName"
        self.isWorking = True
        self.parametersPanel.pnlNavAid.Items = ShieldingDlg.navAids
        self.isWorking = False
        if (self.parametersPanel.pnlNavAid.Count > 0):
            int_0 = max(int_0, 0)
            int_0 = min(int_0, self.parametersPanel.pnlNavAid.Count - 1)
            self.parametersPanel.pnlNavAid.SelectedIndex = int_0
        self.method_35()
        
    def method_34(self, navigationalAid_0):
        # if (this.pnlNavAid.DataSource != null)
        # {
        #     this.pnlNavAid.ComboBox.DataSource = null
        # }
        # this.pnlNavAid.DataSource = Shielding.navAids
        # this.pnlNavAid.DisplayMember = "DisplayName"
        self.isWorking = True
        self.parametersPanel.pnlNavAid.Items = ShieldingDlg.navAids
        self.isWorking = False
        self.parametersPanel.pnlNavAid.SelectedIndex = self.parametersPanel.pnlNavAid.IndexOf(navigationalAid_0)
        self.method_35()
        
    def method_35(self):
        if self.isWorking:
            return
        hardCoded = True
        if (self.parametersPanel.pnlNavAid.SelectedIndex > -1):
            hardCoded = self.parametersPanel.pnlNavAid.SelectedItem.HardCoded
        self.parametersPanel.btnNavAidModify.Enabled = not hardCoded
        self.parametersPanel.btnNavAidRemove.Enabled = not hardCoded
        
    def method_38(self, sender):
        if (sender == self.parametersPanel.pnlNavType):
            # self.method_36()
            self.method_32()
            return
        if (sender == self.parametersPanel.pnlNavAid):
            self.method_35()
            self.method_32()
            return
        if (sender == self.parametersPanel.pnlConstructionType):
            self.method_32()
            return
        if (sender == self.parametersPanelAltitude.pnlEvalMode):
            self.method_32()
    
    def method_50(self, constructionLayer, point3d_0, double_0, string_1):
        point3d = point3d_0.smethod_167(0)
        AcadHelper.smethod_18(MathHelper.constructCircle(point3d, double_0, 50), constructionLayer)
        if (not String.IsNullOrEmpty(string_1)):
            point3d = MathHelper.distanceBearingPoint(point3d, 0, double_0)
            dBText = AcadHelper.smethod_140(string_1, point3d, self.parametersPanel.pnlAltitudesTextHeight.Value, 1, 1)
            AcadHelper.smethod_18(dBText, constructionLayer)

    def method_51(self, constructionLayer, point3d_0, point3d_1, point3d_2, string_1):
        point3d0 = [point3d_0, point3d_2]
        polyline = PolylineArea(point3d0)
        polyline.SetBulgeAt(0, MathHelper.smethod_60(point3d_0, point3d_1, point3d_2))
        AcadHelper.smethod_18(polyline, constructionLayer)
        if (not String.IsNullOrEmpty(string_1)):
            dBText = AcadHelper.smethod_140(string_1, point3d_1.smethod_167(0), self.parametersPanel.pnlAltitudesTextHeight.Value, 1, 1)
            dBText.set_Rotation(5 * math.pi / 2  - MathHelper.getBearing(point3d_0, point3d_2))
            AcadHelper.smethod_18(dBText, constructionLayer)

    def method_52(self, constructionLayer, point3d_0, double_0, double_1, string_1):
        value = self.parametersPanel.pnlAltitudesTextHeight.Value
        point3d = MathHelper.distanceBearingPoint(point3d_0, double_0, double_1).smethod_167(0)
        point3d1 = MathHelper.distanceBearingPoint(point3d, double_0 - math.pi / 2 , value * 0.4).smethod_167(0)
        point3d2 = MathHelper.distanceBearingPoint(point3d, double_0 + math.pi / 2 , value).smethod_167(0)
        AcadHelper.smethod_18(Line(point3d1, point3d2), constructionLayer)
        if (not String.IsNullOrEmpty(string_1)):
            point3d3 = MathHelper.distanceBearingPoint(point3d2, double_0 + math.pi / 2 , value * 0.2).smethod_167(0)
            dBText = AcadHelper.smethod_140(string_1, point3d3, value, 0, 2)
            dBText.set_Rotation(5 * math.pi / 2 - MathHelper.getBearing(point3d1, point3d2))
            AcadHelper.smethod_18(dBText, constructionLayer)

    def method_53(self, constructionLayer, point3d_0, point3d_1, string_1):
        AcadHelper.smethod_18(Line(point3d_0.smethod_167(0), point3d_1.smethod_167(0)), constructionLayer)
        num = MathHelper.getBearing(point3d_0, point3d_1)
        if (not String.IsNullOrEmpty(string_1)):
            point3d = MathHelper.distanceBearingPoint(point3d_0, num, MathHelper.calcDistance(point3d_0, point3d_1) / 2).smethod_167(0)
            dBText = AcadHelper.smethod_140(string_1, point3d, self.parametersPanel.pnlAltitudesTextHeight.Value, 1, 1)
            if (num > math.pi):
                num = MathHelper.getBearing(point3d_1, point3d_0)
            dBText.set_Rotation(5 * math.pi / 2 - num)
            AcadHelper.smethod_18(dBText, constructionLayer)

    def method_54(self, constructionLayer):
        # dBText = None
        # point3d
        # point3d1
        # point3d2
        # point3d3
        # Point3d point3d4
        # Point3d point3d5
        # Point3d point3d6
        # Point3d point3d7
        # Point3d point3d8
        # Altitude value
        # Distance distance
        # AngleGradientSlope alfa
        # string str
        # string str1
        # string str2
        # double metres
        # string str3
        # string str4
        # string str5
        # string str6
        checked = self.parametersPanel.chbMarkAltitudes.Checked
        num = self.parametersPanel.pnlAltitudesEvery.Value.Metres
        value1 = self.parametersPanel.pnlAltitudesTextHeight.Value
        num1 = Geo.EarthRadius().Metres if(self.parametersPanel.chbEarthCurvature.Checked) else None
        if (checked):
            value = self.parametersPanel.pnlAltitudesEvery.Value
            str0 = "0.##:{0}".format("m")#value.OriginalUnits.ToString().ToLowerInvariant().Trim())
        else:
            str0 = None
        str7 = str0
        if (self.parametersPanel.pnlNavType.SelectedIndex != 0):
            point3d9 = self.parametersPanel.pnlWaypoint1.Point3d
            point3d10 = self.parametersPanel.pnlWaypoint2.Point3d
            num2 = MathHelper.getBearing(point3d9, point3d10)
            distance = self.parametersPanel.pnlSegmentWidth.Value
            metres1 = distance.Metres / 2
            metres2 = self.parametersPanel.pnlMinimumAltitude.Value.Metres
            num3 = MathHelper.smethod_191(metres2, 0.0872664625997165, metres1, num1)
            if (checked):
                num4 = math.trunc(metres2 / num) * num
                if (num4 < metres2):
                    num4 = num4 + num
                while (num4 < num3):
                    num5 = MathHelper.smethod_192(metres2, 0.0872664625997165, num4, metres1, num1)
                    if (num5 >= metres1):
                        break
                    point3d3 = MathHelper.distanceBearingPoint(point3d9, num2 + math.pi / 2 , num5)
                    point3d4 = MathHelper.distanceBearingPoint(point3d9, num2 + math.pi, num5)
                    point3d5 = MathHelper.distanceBearingPoint(point3d9, num2 - math.pi / 2 , num5)
                    point3d6 = MathHelper.distanceBearingPoint(point3d10, num2 + math.pi / 2 , num5)
                    point3d7 = MathHelper.distanceBearingPoint(point3d10, num2, num5)
                    point3d8 = MathHelper.distanceBearingPoint(point3d10, num2 - math.pi / 2 , num5)
                    value = Altitude(num4)
                    self.method_53(constructionLayer, point3d3, point3d6, value.method_0(str7))
                    value = Altitude(num4)
                    self.method_53(constructionLayer, point3d5, point3d8, value.method_0(str7))
                    if (self.parametersPanel.chbTurningWaypoint1.Checked):
                        value = Altitude(num4)
                        self.method_51(constructionLayer, point3d3, point3d4, point3d5, value.method_0(str7))
                    if (self.parametersPanel.chbTurningWaypoint2.Checked):
                        value = Altitude(num4)
                        self.method_51(constructionLayer, point3d6, point3d7, point3d8, value.method_0(str7))
                    num4 = num4 + num
            point3d3 = MathHelper.distanceBearingPoint(point3d9, num2 + math.pi / 2 , metres1)
            point3d4 = MathHelper.distanceBearingPoint(point3d9, num2 + math.pi, metres1)
            point3d5 = MathHelper.distanceBearingPoint(point3d9, num2 - math.pi / 2 , metres1)
            point3d6 = MathHelper.distanceBearingPoint(point3d10, num2 + math.pi / 2 , metres1)
            point3d7 = MathHelper.distanceBearingPoint(point3d10, num2, metres1)
            point3d8 = MathHelper.distanceBearingPoint(point3d10, num2 - math.pi / 2 , metres1)
            if (checked):
                str1 = Altitude(num3).method_0(str7)
            else:
                str1 = None
            str8 = str1
            self.method_53(constructionLayer, point3d3, point3d6, str8)
            self.method_53(constructionLayer, point3d5, point3d8, str8)
            if (self.parametersPanel.chbTurningWaypoint1.Checked):
                self.method_51(constructionLayer, point3d3, point3d4, point3d5, str8)
            if (self.parametersPanel.chbTurningWaypoint2.Checked):
                self.method_51(constructionLayer, point3d6, point3d7, point3d8, str8)
        else:
            selectedItem = self.parametersPanel.pnlNavAid.SelectedItem
            point3d11 = self.parametersPanel.pnlNavAidPos.Point3d
            if isinstance(selectedItem, OmnidirectionalNavigationalAid):
                omnidirectionalNavigationalAid = selectedItem
                z = point3d11.get_Z()
                radians = omnidirectionalNavigationalAid.Alfa.Radians
                distance = omnidirectionalNavigationalAid.r
                num6 = MathHelper.smethod_191(z, radians, distance.Metres, num1)
                metres3 = omnidirectionalNavigationalAid.R.Metres
                alfa = omnidirectionalNavigationalAid.Alfa
                num7 = MathHelper.smethod_191(z, alfa.Radians, metres3, num1)
                if (checked):
                    value = Altitude(z)
                    dBText1 = AcadHelper.smethod_142_v15(value.method_0(str7), point3d11.smethod_167(0), self.parametersPanel.pnlAltitudesTextHeight.Value, 4)
                    AcadHelper.smethod_18(dBText1, constructionLayer)
                if (checked):
                    str5 = Altitude(num6).method_0(str7)
                else:
                    str5 = None
                str9 = str5
                distance = omnidirectionalNavigationalAid.r
                self.method_50(constructionLayer, point3d11, distance.Metres, str9)
                if (checked):
                    num8 = math.trunc(num6 / num) * num
                    if (num8 < num6):
                        num8 = num8 + num
                    while (num8 < num7):
                        alfa = omnidirectionalNavigationalAid.Alfa
                        num9 = MathHelper.smethod_192(z, alfa.Radians, num8, metres3, num1)
                        if (num9 >= metres3):
                            break
                        value = Altitude(num8)
                        self.method_50(constructionLayer, point3d11, num9, value.method_0(str7))
                        num8 = num8 + num
                if (checked):
                    str6 = Altitude(num7).method_0(str7)
                else:
                    str6 = None
                self.method_50(constructionLayer, point3d11, metres3, str6)
            if isinstance(selectedItem, DirectionalNavigationalAid):
                directionalNavigationalAid = selectedItem
                z1 = point3d11.get_Z()
                num10 = Unit.ConvertDegToRad(self.parametersPanel.pnlTrack.Value)
                num11 = directionalNavigationalAid.a.Metres if(directionalNavigationalAid.a.IsValid()) else self.parametersPanel.pnlDistToThr.Value.Metres
                metres4 = directionalNavigationalAid.b.Metres
                metres5 = directionalNavigationalAid.h.Metres
                if (directionalNavigationalAid.a.IsValid()):
                    metres = directionalNavigationalAid.r.Metres
                else:
                    metres6 = self.parametersPanel.pnlDistToThr.Value.Metres
                    distance = directionalNavigationalAid.r
                    metres = metres6 + distance.Metres
                num12 = metres
                metres7 = directionalNavigationalAid.D.Metres
                metres8 = directionalNavigationalAid.H.Metres
                metres9 = directionalNavigationalAid.L.Metres
                radians1 = directionalNavigationalAid.phi.Radians
                point3d12 = MathHelper.distanceBearingPoint(point3d11, num10 - math.pi, metres4)
                point3d13 = MathHelper.distanceBearingPoint(point3d12, num10 - math.pi / 2 , metres7)
                point3d14 = MathHelper.distanceBearingPoint(point3d13, num10, num11 + metres4)
                point3d15 = MathHelper.distanceBearingPoint(point3d14, num10 - radians1, (metres9 - metres7) / math.sin(radians1))
                point3d16 = MathHelper.distanceBearingPoint(point3d12, num10 - math.pi / 2 , metres9)
                point3dArray = [point3d13, point3d14, point3d15, point3d16]
                polyline = PolylineArea(point3dArray)
                # polyline.set_Closed(True)
                AcadHelper.smethod_18(polyline, constructionLayer)
                if (checked):
                    point3d12 = MathHelper.distanceBearingPoint(point3d11.smethod_167(0), num10 - math.pi / 2 , metres7 + (metres9 - metres7) / 2)
                    value = Altitude(z1 + metres8)
                    dBText = AcadHelper.smethod_140(value.method_0(str7), point3d12, self.parametersPanel.pnlAltitudesTextHeight.Value, 0, 2)
                    AcadHelper.smethod_18(dBText, constructionLayer)
                point3d17 = point3d14
                point3d18 = point3d15
                point3d12 = MathHelper.distanceBearingPoint(point3d11, num10 - math.pi, metres4)
                point3d13 = MathHelper.distanceBearingPoint(point3d12, num10 + math.pi / 2 , metres7)
                point3d14 = MathHelper.distanceBearingPoint(point3d13, num10, num11 + metres4)
                point3d15 = MathHelper.distanceBearingPoint(point3d14, num10 + radians1, (metres9 - metres7) / math.sin(radians1))
                point3d16 = MathHelper.distanceBearingPoint(point3d12, num10 + math.pi / 2 , metres9)
                point3dArray = [point3d13, point3d14, point3d15, point3d16 ]
                polyline = PolylineArea(point3dArray)
                # polyline.set_Closed(True)
                AcadHelper.smethod_18(polyline, constructionLayer)
                if (checked):
                    point3d12 = MathHelper.distanceBearingPoint(point3d11.smethod_167(0), num10 + math.pi / 2 , metres7 + (metres9 - metres7) / 2)
                    value = Altitude(z1 + metres8)
                    dBText = AcadHelper.smethod_140(value.method_0(str7), point3d12, self.parametersPanel.pnlAltitudesTextHeight.Value, 0, 2)
                    AcadHelper.smethod_18(dBText, constructionLayer)
                point3d19 = point3d14
                point3d20 = point3d15
                point3d12 = MathHelper.distanceBearingPoint(point3d11, num10 - math.pi, metres4)
                point3d13 = MathHelper.distanceBearingPoint(point3d12, num10 - math.pi / 2 , metres7)
                point3d14 = MathHelper.distanceBearingPoint(point3d13, num10, num11 + metres4)
                point3d15 = MathHelper.distanceBearingPoint(point3d14, num10 + math.pi / 2 , 2 * metres7)
                point3d16 = MathHelper.distanceBearingPoint(point3d15, num10 - math.pi, num11 + metres4)
                point3dArray = [point3d14, point3d13, point3d16, point3d15 ]
                AcadHelper.smethod_18(PolylineArea(point3dArray), constructionLayer)
                if (checked):
                    value = Altitude(z1)
                    dBText = AcadHelper.smethod_140(value.method_0(str7), point3d11.smethod_167(0), self.parametersPanel.pnlAltitudesTextHeight.Value, 0, 2)
                    AcadHelper.smethod_18(dBText, constructionLayer)
                num13 = math.atan(metres5 / (num12 - num11))
                point3d2_0 = []
                MathHelper.smethod_34(point3d17, point3d18, point3d11, num12, point3d2_0)
                point3d2 = point3d2_0[0]
                point3d = point3d2_0[1]
                point3d2_1 = []
                MathHelper.smethod_34(point3d19, point3d20, point3d11, num12, point3d2_1)
                point3d2 = point3d2_1[0]
                point3d1 = point3d2_1[1]
                point3dArray = [point3d17, point3d, point3d1, point3d19 ]
                polyline = PolylineArea(point3dArray)
                polyline.SetBulgeAt(1, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, point3d11))
                AcadHelper.smethod_18(polyline, constructionLayer)
                if (checked):
                    str3 = Altitude(z1).method_0(str7)
                else:
                    str3 = None
                self.method_53(constructionLayer, point3d17, point3d19, str3)
                num14 = num12 - num11
                num15 = MathHelper.smethod_191(z1, num13, num14, num1)
                if (checked):
                    str4 = Altitude(num15).method_0(str7)
                else:
                    str4 = None
                str10 = str4
                self.method_51(constructionLayer, point3d, MathHelper.distanceBearingPoint(point3d11, num10, num12), point3d1, str10)
                if (checked):
                    line = Line()
                    num16 = math.trunc(z1 / num) * num
                    if (num16 <= z1):
                        num16 = num16 + num
                    while (num16 < num15):
                        num17 = MathHelper.smethod_192(z1, num13, num16, num14, num1)
                        if (num17 >= num14):
                            break
                        pt1 = MathHelper.getIntersectionPoint(point3d17, point3d, MathHelper.distanceBearingPoint(point3d17, num10, num17), MathHelper.distanceBearingPoint(point3d19, num10, num17))
                        pt2 = MathHelper.getIntersectionPoint(point3d1, point3d19, MathHelper.distanceBearingPoint(point3d17, num10, num17), MathHelper.distanceBearingPoint(point3d19, num10, num17))
                        point3dCollection = Point3dCollection()
                        polyline.IntersectWithNew(PolylineArea([pt1, pt2]), 2, point3dCollection)
                        value = Altitude(num16)
                        if len(point3dCollection) > 1:
                            pt1 = point3dCollection[0]
                            pt2 = point3dCollection[1]
                        self.method_53(constructionLayer, pt1, pt2, value.method_0(str7))

                        # AcadHelper.smethod_18([pt1, pt2], constructionLayer)
                        #
                        # line.set_StartPoint(MathHelper.distanceBearingPoint(point3d17, num10, num17).smethod_167(0))
                        # line.set_EndPoint(MathHelper.distanceBearingPoint(point3d19, num10, num17).smethod_167(0))
                        # point3dCollection = Point3dCollection()
                        # polyline.IntersectWithNew(line, 2, point3dCollection)
                        # item = point3dCollection.get_Item(0)
                        # item1 = point3dCollection.get_Item(1)
                        # value = Altitude(num16)
                        # self.method_53(constructionLayer, item, item1, value.method_0(str7))
                        num16 = num16 + num
                    # AcadHelper.smethod_24(line)
                    return
            elif isinstance(selectedItem, LineOfSight):
                lineOfSight = selectedItem
                z2 = point3d11.get_Z()
                value = lineOfSight.StartingHeight
                num18 = z2 + value.Metres.smethod_17()
                num19 = Unit.ConvertDegToRad(self.parametersPanel.pnlTrack.Value)
                metres10 = lineOfSight.FinishingDistance.Metres
                alfa = lineOfSight.Slope
                num20 = MathHelper.smethod_191(num18, alfa.Radians, metres10, num1)
                if (checked):
                    num21 = math.trunc(num18 / num) * num
                    if (num21 < num18):
                        num21 = num21 + num
                    while (num21 < num20):
                        alfa = lineOfSight.Slope
                        num22 = MathHelper.smethod_192(num18, alfa.Radians, num21, metres10, num1)
                        if (num22 >= metres10):
                            break
                        value = Altitude(num21)
                        self.method_52(constructionLayer, point3d11, num19, num22, value.method_0(str7))
                        num21 = num21 + num
                AcadHelper.smethod_18(Line(point3d11.smethod_167(0), MathHelper.distanceBearingPoint(point3d11, num19, metres10).smethod_167(0)), constructionLayer)
                if (checked):
                    str2 = Altitude(num20).method_0(str7)
                else:
                    str2 = None
                self.method_52(constructionLayer, point3d11, num19, metres10, str2)
                return

    def method_55(self, constructionLayer, point3d_0, point3dCollection_0, int_0):
        int0 = int_0 * 4
        num = 0
        count = point3dCollection_0.get_Count() - 1
        point3dCollection = Point3dCollection()
        num1 = 0
        num2 = Unit.ConvertDegToRad(360 / float(int0))
        # for i in range(int0 + 1):
        #     for j in range(num, count + 1):
        #         num3 = MathHelper.calcDistance(point3d_0, point3dCollection_0.get_Item(j))
        #         point3d = MathHelper.distanceBearingPoint(point3d_0, num1, num3)
        #         item = point3dCollection_0.get_Item(j)
        #         point3d1 = point3d.smethod_167(item.get_Z())
        #         point3dCollection.Add(point3d1)
        #     num1 = num1 + num2
        # # PolygonMesh polygonMesh = new PolygonMesh(0, int0 + 1, count + 1, point3dCollection, true, true)
        # AcadHelper.smethod_18(point3dCollection, constructionLayer)
        for j in range(num, count + 1):
            point3dCollection = Point3dCollection()
            for i in range(int0 + 1):
                num3 = MathHelper.calcDistance(point3d_0, point3dCollection_0.get_Item(j))
                point3d = MathHelper.distanceBearingPoint(point3d_0, num1, num3)
                item = point3dCollection_0.get_Item(j)
                point3d1 = point3d.smethod_167(item.get_Z())
                point3dCollection.Add(point3d1)
                num1 = num1 + num2
        # PolygonMesh polygonMesh = new PolygonMesh(0, int0 + 1, count + 1, point3dCollection, true, true)
            AcadHelper.smethod_18(point3dCollection, constructionLayer)
    
    def method_56(self, constructionLayer, point3d_0, point3dCollection_0, double_0, double_1, int_0):
        int0 = int_0 * 4
        num = 0
        count = point3dCollection_0.get_Count() - 1

        num1 = Unit.ConvertDegToRad(double_0 - math.fabs(double_1))
        num2 = Unit.ConvertDegToRad(2 * math.fabs(double_1) / float(int0))

        # point3dCollection = Point3dCollection()
        # for i in range(int0 + 1):
        #     for j in range(num, count + 1):
        #         num3 = MathHelper.calcDistance(point3d_0, point3dCollection_0.get_Item(j))
        #         point3d = MathHelper.distanceBearingPoint(point3d_0, num1, num3)
        #         item = point3dCollection_0.get_Item(j)
        #         point3d1 = point3d.smethod_167(item.get_Z())
        #         point3dCollection.Add(point3d1)
        #     num1 = num1 + num2
        # AcadHelper.smethod_18(point3dCollection, constructionLayer)

        for j in range(num, count + 1):
            point3dCollection = Point3dCollection()
            num1 = Unit.ConvertDegToRad(double_0 - math.fabs(double_1))
            num2 = Unit.ConvertDegToRad(2 * math.fabs(double_1) / float(int0))
            for i in range(int0 + 1):
                num3 = MathHelper.calcDistance(point3d_0, point3dCollection_0.get_Item(j))
                point3d = MathHelper.distanceBearingPoint(point3d_0, num1, num3)
                item = point3dCollection_0.get_Item(j)
                point3d1 = point3d.smethod_167(item.get_Z())
                point3dCollection.Add(point3d1)
                num1 = num1 + num2
        # PolygonMesh polygonMesh = new PolygonMesh(0, int0 + 1, count + 1, point3dCollection, true, true)
            AcadHelper.smethod_18(point3dCollection, constructionLayer)

    def method_57(self, constructionLayer):
        point3d = None
        point3d1 = None
        point3d2 = None
        value = None
        alfa = None
        metres = None
        num = Geo.EarthRadius().Metres if(self.parametersPanel.chbEarthCurvature.Checked) else None
        value1 = self.parametersPanel.trackBar.value()
        if (self.parametersPanel.pnlNavType.SelectedIndex != 0):
            point3d3 = self.parametersPanel.pnlWaypoint1.Point3d
            point3d4 = self.parametersPanel.pnlWaypoint2.Point3d
            num1 = MathHelper.getBearing(point3d3, point3d4)
            value = self.parametersPanel.pnlSegmentWidth.Value
            metres1 = value.Metres / float(2) / float(value1)
            num2 = 0
            metres2 = self.parametersPanel.pnlMinimumAltitude.Value.Metres
            point3dCollection = Point3dCollection()
            point3dCollection1 = Point3dCollection()
            point3dCollection2 = Point3dCollection()
            point3dCollection3 = Point3dCollection()
            point3dCollection.Add(point3d3.smethod_167(metres2))
            point3dCollection1.Add(point3d4.smethod_167(metres2))
            point3dCollection2.Add(point3d3.smethod_167(metres2))
            point3dCollection3.Add(point3d4.smethod_167(metres2))
            for i in range(1, value1 + 1):
                num2 = num2 + metres1
                point3d5 = MathHelper.distanceBearingPoint(point3d3, num1 + math.pi / 2, num2)
                point3d6 = MathHelper.distanceBearingPoint(point3d3, num1 - math.pi / 2, num2)
                point3d7 = MathHelper.distanceBearingPoint(point3d4, num1 + math.pi / 2, num2)
                point3d8 = MathHelper.distanceBearingPoint(point3d4, num1 - math.pi / 2, num2)
                num3 = MathHelper.smethod_191(metres2, 0.0872664625997165, num2, num)
                point3dCollection.Insert(0, point3d5.smethod_167(num3))
                point3dCollection.Add(point3d6.smethod_167(num3))
                point3dCollection1.Insert(0, point3d7.smethod_167(num3))
                point3dCollection1.Add(point3d8.smethod_167(num3))
                if (self.parametersPanel.chbTurningWaypoint1.Checked):
                    point3dCollection2.Add(MathHelper.distanceBearingPoint(point3d3, num1 + math.pi, num2).smethod_167(num3))
                if (self.parametersPanel.chbTurningWaypoint2.Checked):
                    point3dCollection3.Add(MathHelper.distanceBearingPoint(point3d4, num1, num2).smethod_167(num3))
                if self.parametersPanel.chbTurningWaypoint1.Checked and self.parametersPanel.chbTurningWaypoint2.Checked:
                    AcadHelper.smethod_18([point3d5.smethod_167(num3), point3d7.smethod_167(num3)], constructionLayer)
                    AcadHelper.smethod_18([point3d6.smethod_167(num3), point3d8.smethod_167(num3)], constructionLayer)
                else:
                    AcadHelper.smethod_153_v15(point3dCollection, point3dCollection1, constructionLayer)
            if (self.parametersPanel.chbTurningWaypoint1.Checked):
                self.method_56(constructionLayer, point3d3, point3dCollection2, Unit.smethod_1(num1) + 180, 90, value1)
            if (self.parametersPanel.chbTurningWaypoint2.Checked):
                self.method_56(constructionLayer, point3d4, point3dCollection3, Unit.smethod_1(num1), 90, value1)
            AcadHelper.smethod_18([point3d3, point3d4], constructionLayer)
        else:
            selectedItem = self.parametersPanel.pnlNavAid.SelectedItem
            point3d9 = self.parametersPanel.pnlNavAidPos.Point3d
            if isinstance(selectedItem, OmnidirectionalNavigationalAid):
                omnidirectionalNavigationalAid = selectedItem
                z = point3d9.get_Z()
                metres3 = omnidirectionalNavigationalAid.R.Metres
                value = omnidirectionalNavigationalAid.r
                num4 = math.fabs(metres3 - value.Metres) / value1
                metres4 = omnidirectionalNavigationalAid.r.Metres
                point3dCollection4 = Point3dCollection()
                alfa = omnidirectionalNavigationalAid.Alfa
                num5 = MathHelper.smethod_191(z, alfa.Radians, metres4, num)
                point3dCollection4.Add(MathHelper.distanceBearingPoint(point3d9, 0, metres4).smethod_167(num5))
                # Vector3d normal = AcadHelper.Normal
                value = omnidirectionalNavigationalAid.r
                # Circle circle = new Circle(point3d9, normal, value.Metres)
                circle = MathHelper.constructCircle(point3d9, value.Metres, 50)
                # circle.set_Thickness(num5 - point3d9.get_Z())
                AcadHelper.smethod_18(circle, constructionLayer)
                for j in range(1, value1 + 1):
                    metres4 = metres4 + num4
                    alfa = omnidirectionalNavigationalAid.Alfa
                    num5 = MathHelper.smethod_191(z, alfa.Radians, metres4, num)
                    point3dCollection4.Add(MathHelper.distanceBearingPoint(point3d9, 0, metres4).smethod_167(num5))
                self.method_55(constructionLayer, point3d9, point3dCollection4, value1)
            if isinstance(selectedItem, DirectionalNavigationalAid):
                directionalNavigationalAid = selectedItem
                z1 = point3d9.get_Z()
                num6 = Unit.ConvertDegToRad(self.parametersPanel.pnlTrack.Value)
                num7 = directionalNavigationalAid.a.Metres if(directionalNavigationalAid.a.IsValid()) else self.parametersPanel.pnlDistToThr.Value.Metres
                metres5 = directionalNavigationalAid.b.Metres
                metres6 = directionalNavigationalAid.h.Metres
                if (directionalNavigationalAid.a.IsValid()):
                    metres = directionalNavigationalAid.r.Metres
                else:
                    metres7 = self.parametersPanel.pnlDistToThr.Value.Metres
                    value = directionalNavigationalAid.r
                    metres = metres7 + value.Metres
                num8 = metres
                metres8 = directionalNavigationalAid.D.Metres
                metres9 = directionalNavigationalAid.H.Metres
                num9 = directionalNavigationalAid.L.Metres
                radians = directionalNavigationalAid.phi.Radians
                point3d10 = MathHelper.distanceBearingPoint(point3d9, num6 - math.pi, metres5)
                point3d11 = MathHelper.distanceBearingPoint(point3d10, num6 - math.pi / 2, metres8).smethod_167(z1 + metres9)
                point3d12 = MathHelper.distanceBearingPoint(point3d11, num6, num7 + metres5).smethod_167(z1 + metres9)
                point3d13 = MathHelper.distanceBearingPoint(point3d12, num6 - radians, (num9 - metres8) / math.sin(radians)).smethod_167(z1 + metres9)
                point3d14 = MathHelper.distanceBearingPoint(point3d10, num6 - math.pi / 2, num9).smethod_167(z1 + metres9)
                # face = new Face(point3d11, point3d12, point3d13, point3d14, True, True, True, True)
                face = [point3d11, point3d12, point3d13, point3d14, point3d11]
                AcadHelper.smethod_18(face, constructionLayer)
                point3d15 = point3d12
                point3d16 = point3d13
                point3d10 = MathHelper.distanceBearingPoint(point3d9, num6 - math.pi, metres5)
                point3d11 = MathHelper.distanceBearingPoint(point3d10, num6 + math.pi / 2, metres8).smethod_167(z1 + metres9)
                point3d12 = MathHelper.distanceBearingPoint(point3d11, num6, num7 + metres5).smethod_167(z1 + metres9)
                point3d13 = MathHelper.distanceBearingPoint(point3d12, num6 + radians, (num9 - metres8) / math.sin(radians)).smethod_167(z1 + metres9)
                point3d14 = MathHelper.distanceBearingPoint(point3d10, num6 + math.pi / 2, num9).smethod_167(z1 + metres9)
                # face = new Face(point3d11, point3d12, point3d13, point3d14, True, True, True, True)
                face = [point3d11, point3d12, point3d13, point3d14, point3d11]
                AcadHelper.smethod_18(face, constructionLayer)
                point3d17 = point3d12
                point3d18 = point3d13
                point3d10 = MathHelper.distanceBearingPoint(point3d9, num6 - math.pi, metres5)
                point3d11 = MathHelper.distanceBearingPoint(point3d10, num6 - math.pi / 2, metres8).smethod_167(point3d9.get_Z())
                point3d12 = MathHelper.distanceBearingPoint(point3d11, num6, num7 + metres5).smethod_167(point3d9.get_Z())
                point3d13 = MathHelper.distanceBearingPoint(point3d12, num6 + math.pi / 2, 2 * metres8).smethod_167(point3d9.get_Z())
                point3d14 = MathHelper.distanceBearingPoint(point3d13, num6 - math.pi, num7 + metres5).smethod_167(point3d9.get_Z())
                # face = new Face(point3d11, point3d12, point3d13, point3d14, True, True, True, True)
                face = [point3d11, point3d12, point3d13, point3d14, point3d11]
                AcadHelper.smethod_18(face, constructionLayer)
                # face = new Face(point3d11, point3d14, point3d14.smethod_167(z1 + metres9), point3d11.smethod_167(z1 + metres9), True, True, True, True)
                face = [point3d11, point3d14, point3d14.smethod_167(z1 + metres9), point3d11.smethod_167(z1 + metres9), point3d11]
                AcadHelper.smethod_18(face, constructionLayer)
                # face = new Face(point3d11, point3d12, point3d12.smethod_167(z1 + metres9), point3d11.smethod_167(z1 + metres9), True, True, True, True)
                face = [point3d11, point3d12, point3d12.smethod_167(z1 + metres9), point3d11.smethod_167(z1 + metres9), point3d11]
                AcadHelper.smethod_18(face, constructionLayer)
                # face = new Face(point3d13, point3d14, point3d14.smethod_167(z1 + metres9), point3d13.smethod_167(z1 + metres9), True, True, True, True)
                face = [point3d13, point3d14, point3d14.smethod_167(z1 + metres9), point3d13.smethod_167(z1 + metres9), point3d13]
                AcadHelper.smethod_18(face, constructionLayer)
                # face = new Face(point3d15, point3d16, point3d16, point3d15.smethod_167(point3d9.get_Z()), True, True, True, True)
                face = [point3d15, point3d16, point3d16, point3d15.smethod_167(point3d9.get_Z()), point3d15]
                AcadHelper.smethod_18(face, constructionLayer)
                # face = new Face(point3d17, point3d18, point3d18, point3d17.smethod_167(point3d9.get_Z()), True, True, True, True)
                face = [point3d17, point3d18, point3d18, point3d17.smethod_167(point3d9.get_Z()), point3d17]
                AcadHelper.smethod_18(face, constructionLayer)
                num10 = math.atan(metres6 / (num8 - num7))
                point3d2_0 = []
                MathHelper.smethod_34(point3d15, point3d16, point3d9, num8, point3d2_0)
                point3d2 = point3d2_0[0]
                point3d = point3d2_0[1]
                point3d2_1 = []
                MathHelper.smethod_34(point3d17, point3d18, point3d9, num8, point3d2_1)
                point3d2 = point3d2_1[0]
                point3d1 = point3d2_1[1]
                polyline = None
                line = None
                # try
                # {
                value1 = int(round((num8 - num7) / (metres5 + num8) * value1))
                num11 = (num8 - num7) / float(value1)
                point3dArray = [point3d15, point3d, point3d1, point3d17]
                polyline = PolylineArea(point3dArray)
                polyline.SetBulgeAt(1, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, point3d9))
                line = Line()
                point3dCollection5 = Point3dCollection()
                point3dCollection6 = Point3dCollection()
                point3dCollection5.Add(point3d15.smethod_167(point3d9.get_Z()))
                point3dCollection6.Add(point3d17.smethod_167(point3d9.get_Z()))
                num12 = 0
                for k in range(1, value1):
                    num12 = num12 + num11
                    num13 = MathHelper.smethod_191(z1, num10, num12, num)
                    # line.set_StartPoint(MathHelper.distanceBearingPoint(point3d15, num6, num12).smethod_167(0))
                    # line.set_EndPoint(MathHelper.distanceBearingPoint(point3d17, num6, num12).smethod_167(0))
                    # AcadHelper.smethod_18(line, constructionLayer)

                    # polyline.IntersectWithNew(line, 2, point3dCollection7)
                    # if len(point3dCollection7) == 0:
                    #     continue
                    pt1 = MathHelper.getIntersectionPoint(point3d15, point3d, MathHelper.distanceBearingPoint(point3d15, num6, num12), MathHelper.distanceBearingPoint(point3d17, num6, num12))
                    pt2 = MathHelper.getIntersectionPoint(point3d1, point3d17, MathHelper.distanceBearingPoint(point3d15, num6, num12), MathHelper.distanceBearingPoint(point3d17, num6, num12))
                    point3dCollection7 = Point3dCollection()
                    polyline.IntersectWithNew(PolylineArea([pt1, pt2]), 2, point3dCollection7)
                    if len(point3dCollection7) > 1:
                        pt1 = point3dCollection7[0]
                        pt2 = point3dCollection7[1]
                    point3dCollection5.Add(pt1.smethod_167(num13))
                    point3dCollection6.Add(pt2.smethod_167(num13))

                    AcadHelper.smethod_18([pt1, pt2], constructionLayer)
                    # point3dCollection5.Add(point3dCollection7.get_Item(0).smethod_167(num13))
                    # point3dCollection6.Add(point3dCollection7.get_Item(1).smethod_167(num13))
                point3d19 = MathHelper.distanceBearingPoint(point3d9, num6, num8).smethod_167(MathHelper.smethod_191(z1, num10, num8 - num7, num))
                # point3dCollection5.Add(point3d19)
                # point3dCollection6.Add(point3d19)
                # AcadHelper.smethod_153_v15(point3dCollection5, point3dCollection6, constructionLayer)
                AcadHelper.smethod_18(polyline, constructionLayer)
            elif isinstance(selectedItem, LineOfSight):
                lineOfSight = selectedItem
                z2 = point3d9.get_Z()
                startingHeight = lineOfSight.StartingHeight
                num14 = z2 + startingHeight.Metres if(startingHeight.Metres != None) else 0
                value = lineOfSight.FinishingDistance
                metres10 = value.Metres / float(value1)
                num15 = 0
                num16 = Unit.ConvertDegToRad(self.parametersPanel.pnlTrack.Value)
                point3dCollection8 = Point3dCollection()
                point3dCollection8.Add(point3d9.smethod_167(num14))
                for l in range(1, value1 + 1):
                    num15 = num15 + metres10
                    alfa = lineOfSight.Slope
                    num17 = MathHelper.smethod_191(num14, alfa.Radians, num15, num)
                    point3dCollection8.Add(MathHelper.distanceBearingPoint(point3d9, num16, num15).smethod_167(num17))
                AcadHelper.smethod_18(point3dCollection8, constructionLayer)
                return
            
    def method_58(self, point3d_0, point3d_1, point3d_2):
        point3d = None
        num = 0.0001
        num1 = MathHelper.getBearing(point3d_0, point3d_1)
        point3d = MathHelper.getIntersectionPoint(point3d_0, point3d_1, point3d_2, MathHelper.distanceBearingPoint(point3d_2, num1 + math.pi / 2, 100))
        point3d1 = MathHelper.distanceBearingPoint(point3d_0, num1 + math.pi / 2, 100)
        point3d2 = MathHelper.distanceBearingPoint(point3d_1, num1 + math.pi / 2, 100)
        if (MathHelper.smethod_115(point3d, point3d_0, point3d1) and MathHelper.smethod_119(point3d, point3d_1, point3d2)):
            return max(num, MathHelper.getBearing(point3d, point3d_2))
        if (MathHelper.smethod_119(point3d, point3d_0, point3d1)):
            return max(num, MathHelper.getBearing(point3d_0, point3d_2))
        return max(num, MathHelper.getBearing(point3d_1, point3d_2))

class ShieldingObstacles(ObstacleTable):
    def __init__(self, navType, dataList):
        ObstacleTable.__init__(self, None)
        self.navType = navType
        self.singlePointDisplayName = ""
        if navType == Captions.CONVENTIONAL:
            self.navAid = dataList[0]
            self.ptAid = dataList[1]
            self.trackDeg = dataList[2]
            self.trackRad = Unit.smethod_0(dataList[2])
            self.distToThr = dataList[3].Metres
            self.earthRadius = dataList[4]
            self.onlyPenetratingObstacles = dataList[5]
            if (self.navAid.Type == NavigationalAidType.Directional):
                self.method_111()
        elif navType == Captions.GPS:
            point3d_0 = dataList[0]
            bool_0 = dataList[1]
            point3d_1 = dataList[2]
            bool_1 = dataList[3]
            distance_0 = dataList[4]
            altitude_0 = dataList[5]
            double_0 = dataList[6]
            bool_2 = dataList[7]
            self.ptWPt1 = point3d_0
            self.ptWPt2 = point3d_1
            self.isWPt1Turning = bool_0
            self.isWPt2Turning = bool_1
            self.segSemiWidth = distance_0.Metres
            self.oca = altitude_0.Metres
            self.track = MathHelper.getBearing(point3d_0, point3d_1)
            self.earthRadius = double_0
            self.onlyPenetratingObstacles = bool_2
            self.ptsArea = Point3dCollection()
            self.ptsArea.Add(MathHelper.distanceBearingPoint(point3d_0, self.track + math.pi / 2, self.segSemiWidth))
            self.ptsArea.Add(MathHelper.distanceBearingPoint(point3d_1, self.track + math.pi / 2, self.segSemiWidth))
            self.ptsArea.Add(MathHelper.distanceBearingPoint(point3d_1, self.track - math.pi / 2, self.segSemiWidth))
            self.ptsArea.Add(MathHelper.distanceBearingPoint(point3d_0, self.track - math.pi / 2, self.segSemiWidth))
            if (bool_0):
                self.ptsWPt1 = Point3dCollection()
                self.ptsWPt1.Add(MathHelper.distanceBearingPoint(point3d_0, self.track + math.pi / 2, self.segSemiWidth))
                self.ptsWPt1.Add(MathHelper.distanceBearingPoint(self.ptsWPt1.get_Item(0), self.track + math.pi, self.segSemiWidth))
                point3d = MathHelper.distanceBearingPoint(point3d_0, self.track - math.pi / 2, self.segSemiWidth)
                self.ptsWPt1.Add(MathHelper.distanceBearingPoint(point3d, self.track + math.pi, self.segSemiWidth))
                self.ptsWPt1.Add(point3d)
            if (bool_1):
                self.ptsWPt2 = Point3dCollection()
                self.ptsWPt2.Add(MathHelper.distanceBearingPoint(point3d_1, self.track + math.pi / 2, self.segSemiWidth))
                self.ptsWPt2.Add(MathHelper.distanceBearingPoint(self.ptsWPt2.get_Item(0), self.track, self.segSemiWidth))
                point3d1 = MathHelper.distanceBearingPoint(point3d_1, self.track - math.pi / 2, self.segSemiWidth)
                self.ptsWPt2.Add(MathHelper.distanceBearingPoint(point3d1, self.track, self.segSemiWidth))
                self.ptsWPt2.Add(point3d1)
            
    def method_111(self):
        # Point3d point3d
        # Point3d point3d1
        # Point3d point3d2
        directionalNavigationalAid = self.navAid
        num = directionalNavigationalAid.a.Metres if(directionalNavigationalAid.a.IsValid()) else self.distToThr
        metres = directionalNavigationalAid.b.Metres
        metres1 = directionalNavigationalAid.h.Metres
        num1 = directionalNavigationalAid.r.Metres if(directionalNavigationalAid.a.IsValid()) else self.distToThr + directionalNavigationalAid.r.Metres
        metres2 = directionalNavigationalAid.D.Metres
        num2 = directionalNavigationalAid.H.Metres
        metres3 = directionalNavigationalAid.L.Metres
        radians = directionalNavigationalAid.phi.Radians
        self.ptsLeft = Point3dCollection()
        point3d3 = MathHelper.distanceBearingPoint(self.ptAid, self.trackRad - 3.14159265358979, metres)
        point3d4 = MathHelper.distanceBearingPoint(point3d3, self.trackRad - math.pi / 2, metres2).smethod_167(num2)
        point3d5 = MathHelper.distanceBearingPoint(point3d4, self.trackRad, num + metres).smethod_167(num2)
        point3d6 = MathHelper.distanceBearingPoint(point3d5, self.trackRad - radians, (metres3 - metres2) / math.sin(radians)).smethod_167(num2)
        point3d7 = MathHelper.distanceBearingPoint(point3d3, self.trackRad - math.pi / 2, metres3).smethod_167(num2)
        point3dCollection = self.ptsLeft
        point3dArray = [point3d4, point3d5, point3d6, point3d7]
        point3dCollection.smethod_145(point3dArray)
        point3d8 = point3d5
        point3d9 = point3d6
        self.ptsRight = Point3dCollection()
        point3d3 = MathHelper.distanceBearingPoint(self.ptAid, self.trackRad - 3.14159265358979, metres)
        point3d4 = MathHelper.distanceBearingPoint(point3d3, self.trackRad + math.pi / 2, metres2).smethod_167(num2)
        point3d5 = MathHelper.distanceBearingPoint(point3d4, self.trackRad, num + metres).smethod_167(num2)
        point3d6 = MathHelper.distanceBearingPoint(point3d5, self.trackRad + radians, (metres3 - metres2) / math.sin(radians)).smethod_167(num2)
        point3d7 = MathHelper.distanceBearingPoint(point3d3, self.trackRad + math.pi / 2, metres3).smethod_167(num2)
        point3dCollection1 = self.ptsRight
        point3dArray1 = [point3d4, point3d5, point3d6, point3d7]
        point3dCollection1.smethod_145(point3dArray1)
        point3d10 = point3d5
        point3d11 = point3d6
        self.ptsGround = Point3dCollection()
        point3d3 = MathHelper.distanceBearingPoint(self.ptAid, self.trackRad - 3.14159265358979, metres)
        point3d4 = MathHelper.distanceBearingPoint(point3d3, self.trackRad - math.pi / 2, metres2).smethod_167(self.ptAid.get_Z())
        point3d5 = MathHelper.distanceBearingPoint(point3d4, self.trackRad, num + metres).smethod_167(self.ptAid.get_Z())
        point3d6 = MathHelper.distanceBearingPoint(point3d5, self.trackRad + math.pi / 2, 2 * metres2).smethod_167(self.ptAid.get_Z())
        point3d7 = MathHelper.distanceBearingPoint(point3d6, self.trackRad - 3.14159265358979, num + metres).smethod_167(self.ptAid.get_Z())
        point3dCollection2 = self.ptsGround
        point3dArray2 = [point3d4, point3d5, point3d6, point3d7]
        point3dCollection2.smethod_145(point3dArray2)
        self.slope = math.atan(metres1 / (num1 - num))
        point3d2_1 = []
        MathHelper.smethod_34(point3d8, point3d9, self.ptAid, num1, point3d2_1)
        point3d2 = point3d2_1[0]
        point3d = point3d2_1[1]
        point3d2_1 = []
        MathHelper.smethod_34(point3d10, point3d11, self.ptAid, num1, point3d2_1)
        point3d2 = point3d2_1[0]
        point3d1 = point3d2_1[1]
        polylineArea = PolylineArea()
        polylineArea.method_1(point3d8)
        polylineArea.method_3(point3d, MathHelper.smethod_57(TurnDirection.Right, point3d, point3d1, self.ptAid))
        polylineArea.method_1(point3d1)
        polylineArea.method_1(point3d10)
        self.slopingArea = PrimaryObstacleArea(polylineArea)
    
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
        if self.navType == Captions.CONVENTIONAL:
            str0 = ""
            result, self.singlePointDisplayName = self.conventionalMethod0(obstacle_0, False, str0)
        elif self.navType == Captions.GPS:
            str0 = ""
            result, self.singlePointDisplayName = self.gpsMethod0(obstacle_0, True, str0)
        # num = None
        # num1 = None
        # 
        # AerodromeSurfacesDlg.multiObstaclesChecked = AerodromeSurfacesDlg.multiObstaclesChecked + 1
        # num2 = 0
        # for surface in self.surfaces:
        #     checkResult = []
        #     result, num, num1 = surface.vmethod_2(obstacle_0)
        #     if (result):
        #         criticalObstacleType = CriticalObstacleType.No
        #         if (num1 > 0):
        #             criticalObstacleType = CriticalObstacleType.Yes
        #         if (not self.onlyPenetratingObstacles or (self.onlyPenetratingObstacles and criticalObstacleType == CriticalObstacleType.Yes)):
        #             checkResult = [num, num1, criticalObstacleType, surface.title]
        #             self.addObstacleToModel(obstacle_0, checkResult)
        #             # AerodromeSurfacesDlg.multiObstacles[num2].method_11(obstacle_0, num, num1, criticalObstacleType)
        #         if (isinstance(surface, InnerHorizontalSurface) or isinstance(surface ,ConicalSurface) or isinstance(surface ,OuterHorizontalSurface)):
        #             return
        #     num2 += 1
    def gpsMethod0(self, obstacle_0, bool_0, string_0):
        point3d = None
        num = None
        num1 = None
        num2 = None
        criticalObstacleType = None
        z = obstacle_0.Position.get_Z() + obstacle_0.Trees
        if (MathHelper.pointInPolygon(self.ptsArea, obstacle_0.Position, obstacle_0.Tolerance)):
            point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.track + math.pi / 2, 100)
            point3d = MathHelper.getIntersectionPoint(self.ptWPt1, self.ptWPt2, obstacle_0.Position, point3d1)
            num = MathHelper.calcDistance(point3d, obstacle_0.Position)
            num2 = MathHelper.smethod_191(self.oca, 0.0872664625997165, num - obstacle_0.Tolerance, self.earthRadius) if(num > obstacle_0.Tolerance) else self.oca
            num1 = z - num2
            criticalObstacleType = CriticalObstacleType.Yes if(num1 > 0) else CriticalObstacleType.No
            if (self.onlyPenetratingObstacles and num1 > 0) or not self.onlyPenetratingObstacles:
                self.addObstacleToModel(obstacle_0, [Captions.GPS, num2, num1, criticalObstacleType])
        elif (not self.isWPt1Turning or not MathHelper.pointInPolygon(self.ptsWPt1, obstacle_0.Position, obstacle_0.Tolerance)):
            if (not self.isWPt2Turning or not MathHelper.pointInPolygon(self.ptsWPt2, obstacle_0.Position, obstacle_0.Tolerance)):
                return False, None
            num = MathHelper.calcDistance(self.ptWPt2, obstacle_0.Position)
            if (num > obstacle_0.Tolerance):
                if (num - obstacle_0.Tolerance > self.segSemiWidth):
                    return False, None
                num2 = MathHelper.smethod_191(self.oca, 0.0872664625997165, num - obstacle_0.Tolerance, self.earthRadius)
            else:
                num2 = self.oca
            num1 = z - num2
            criticalObstacleType = CriticalObstacleType.Yes if(num1 > 0) else CriticalObstacleType.No
            if (self.onlyPenetratingObstacles and num1 > 0) or not self.onlyPenetratingObstacles:
                self.addObstacleToModel(obstacle_0, [Captions.GPS, num2, num1, criticalObstacleType])
        else:
            num = MathHelper.calcDistance(self.ptWPt1, obstacle_0.Position)
            if (num > obstacle_0.Tolerance):
                if (num - obstacle_0.Tolerance > self.segSemiWidth):
                    return False, None
                num2 = MathHelper.smethod_191(self.oca, 0.0872664625997165, num - obstacle_0.Tolerance, self.earthRadius)
            else:
                num2 = self.oca
            num1 = z - num2
            criticalObstacleType = CriticalObstacleType.Yes if(num1 > 0) else CriticalObstacleType.No
            if (self.onlyPenetratingObstacles and num1 > 0) or not self.onlyPenetratingObstacles:
                self.addObstacleToModel(obstacle_0, [Captions.GPS, num2, num1, criticalObstacleType])
        if (bool_0):
            str0 = Captions.BELOW if(round(num1, 1) < 0) else Captions.ABOVE
            name = [obstacle_0.Name, str(round(z, 1)) + " m", Captions.GPS, str(round(num2, 1)) + " m", str0, ""]
            num3 = math.fabs(num1)
            name[5] = str(round(num3, 1)) + " m"
            string_0 = "{0}, {1}, {2} - {3}, {4} {5}".format(obstacle_0.Name, str(round(z, 1)) + " m", Captions.GPS, str(round(num2, 1)) + " m", str0, str(round(num3, 1)) + " m")
        return True, string_0

    def conventionalMethod0(self, obstacle_0, bool_0, string_0):
        point3d = None
        criticalObstacleType = None
        point3d1 = None
        num = None
        z = None
        z1 = None
        num1 = None
        num2 = None
        if (isinstance(self.navAid, OmnidirectionalNavigationalAid)):
            omnidirectionalNavigationalAid = self.navAid
            num3 = MathHelper.calcDistance(self.ptAid, obstacle_0.Position) - obstacle_0.Tolerance
            MathHelper.calcDistance(self.ptAid, obstacle_0.Position)
            tolerance = obstacle_0.Tolerance
            if (num3 > omnidirectionalNavigationalAid.R.Metres):
                return False, None
            if (num3 >= omnidirectionalNavigationalAid.r.Metres):
                point3d = MathHelper.distanceBearingPoint(self.ptAid, MathHelper.getBearing(self.ptAid, obstacle_0.Position), num3)
                num = MathHelper.calcDistance(self.ptAid, point3d)
                z1 = self.ptAid.get_Z()
                alfa = omnidirectionalNavigationalAid.Alfa
                num1 = MathHelper.smethod_191(z1, alfa.Radians, num, self.earthRadius)
            else:
                num1 = self.ptAid.get_Z()
            z = obstacle_0.Position.get_Z() + obstacle_0.Trees
            num2 = z - num1
            criticalObstacleType = CriticalObstacleType.Yes if(num2 > 0) else CriticalObstacleType.No
            if (self.onlyPenetratingObstacles and num2 > 0) or not self.onlyPenetratingObstacles:
                self.addObstacleToModel(obstacle_0, [self.navAid.Name, num1, num2, criticalObstacleType])
        elif (not isinstance(self.navAid, DirectionalNavigationalAid)):
            if (not isinstance(self.navAid, LineOfSight)):
                return False, None
            lineOfSight = self.navAid
            point3d = MathHelper.distanceBearingPoint(self.ptAid, MathHelper.getBearing(self.ptAid, obstacle_0.Position), MathHelper.calcDistance(self.ptAid, obstacle_0.Position) - obstacle_0.Tolerance) if(MathHelper.calcDistance(self.ptAid, obstacle_0.Position) > obstacle_0.Tolerance) else self.ptAid
            num = MathHelper.calcDistance(self.ptAid, point3d)
            z = obstacle_0.Position.get_Z() + obstacle_0.Trees
            z2 = self.ptAid.get_Z()
            startingHeight = lineOfSight.StartingHeight
            z1 = z2 + startingHeight.Metres.smethod_17()
            slope = lineOfSight.Slope
            num1 = MathHelper.smethod_191(z1, slope.Radians, num, self.earthRadius)
            num2 = z - num1
            criticalObstacleType = CriticalObstacleType.Yes if(num2 > 0) else CriticalObstacleType.No
            if (self.onlyPenetratingObstacles and num2 > 0) or not self.onlyPenetratingObstacles:
                self.addObstacleToModel(obstacle_0, [self.navAid.Name, num1, num2, criticalObstacleType])
        else:
            directionalNavigationalAid = self.navAid
            if (not MathHelper.pointInPolygon(self.ptsGround, obstacle_0.Position, obstacle_0.Tolerance)):
                if (self.slopingArea.imethod_0(obstacle_0.Position, obstacle_0.Tolerance)):
                    position = self.slopingArea.PreviewArea[0].Position
                    position1 = self.slopingArea.PreviewArea[3].Position
                    point3d1 = MathHelper.getIntersectionPoint(position, position1, obstacle_0.Position, MathHelper.distanceBearingPoint(obstacle_0.Position, self.trackRad - 3.14159265358979, 100))
                    num = max(MathHelper.calcDistance(point3d1, obstacle_0.Position) - obstacle_0.Tolerance, 0)
                    z1 = self.ptAid.get_Z()
                    num1 = MathHelper.smethod_191(z1, self.slope, num, self.earthRadius)
                if (MathHelper.pointInPolygon(self.ptsLeft, obstacle_0.Position, obstacle_0.Tolerance) or MathHelper.pointInPolygon(self.ptsRight, obstacle_0.Position, obstacle_0.Tolerance)):
                    if (not num1 == None):
                        z3 = self.ptAid.get_Z()
                        h = directionalNavigationalAid.H
                        num1 = min(num1, z3 + h.Metres)
                    else:
                        num1 = self.ptAid.get_Z() + directionalNavigationalAid.H.Metres
            else:
                num1 = self.ptAid.get_Z()
            if (num1 == None):
                return False, None
            z = obstacle_0.Position.get_Z() + obstacle_0.Trees
            num2 = z - num1
            criticalObstacleType = CriticalObstacleType.Yes if(num2 > 0) else CriticalObstacleType.No
            if (self.onlyPenetratingObstacles and num2 > 0) or not self.onlyPenetratingObstacles:
                self.addObstacleToModel(obstacle_0, [self.navAid.Name, num1, num2, criticalObstacleType])
        if (bool_0):
            str0 = Captions.BELOW if(round(num2, 1) < 0) else Captions.ABOVE
            name = [obstacle_0.Name, str(round(z, 1)) + " m", self.navAid.Name, str(round(num1, 1)) + " m", str0, None]
            num4 = math.fabs(num2)
            name[5] = str(round(num4, 1)) + " m"
            string_0 = "{0}, {1}, {2} - {3}, {4} {5}".format(obstacle_0.Name, str(round(z, 1)) + " m", self.navAid.Name, str(round(num1, 1)) + " m", str0, str(round(num4, 1)) + " m")
        return True, string_0