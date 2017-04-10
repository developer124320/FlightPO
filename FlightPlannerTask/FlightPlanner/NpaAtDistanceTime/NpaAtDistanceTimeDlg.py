# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QString, Qt,  QVariant, QSizeF
from PyQt4.QtGui import QColor,QMessageBox,QTextDocument,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsCoordinateReferenceSystem,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, \
                QgsVectorFileWriter, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, \
                QgsSymbolV2, QgsRendererCategoryV2, QgsGeometry, QgsPalLayerSettings
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapToolPan, QgsTextAnnotationItem
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType, SurfaceTypes, \
                 DistanceUnits,AircraftSpeedCategory, RnavGnssFlightPhase, AltitudeUnits, \
                 RnavCommonWaypoint, RnavFlightPhase, ConstructionType, RnavSpecification, IntersectionStatus,\
                 TurnDirection,RnavWaypointType, AngleUnits, OffsetGapType
from FlightPlanner.NpaAtDistanceTime.ui_NpaAtDistanceTime import Ui_NpaAtDistanceTime
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
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, ComplexObstacleArea, SecondaryObstacleArea, SecondaryObstacleAreaWithManyPoints
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.IasHelp.IasHelpDlg import IasHelpDlg
from FlightPlanner.messages import Messages
from FlightPlanner.RnavTolerance0 import RnavGnssTolerance
from FlightPlanner.Captions import Captions
from FlightPlanner.PaIls.DlgCalcFapPosition import DlgFapCalcPosition
from FlightPlanner.BasicGNSS.ParameterDlgs.DlgCaculateWaypoint import CalcDlg
from qgis.core import QGis, QgsRectangle, QgsGeometry, QgsCsException, QgsPoint,\
        QgsFeatureRequest, QgsCoordinateTransform, QgsFeature, QgsVectorLayer

from Type.switch import switch
import define, math

class NpaAtDistanceTimeDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):



        FlightPlanBaseDlg.__init__(self, parent)

        # self.dlgType = dlgType

        self.setObjectName("PaIlsDlg")

        self.surfaceType = SurfaceTypes.NpaAtDistanceTime
        self.initParametersPan()
        self.setWindowTitle(self.surfaceType)
        self.resize(540, 600)
        QgisHelper.matchingDialogSize(self, 650, 700)
        self.surfaceList = None
        self.manualPolygon = None

        self.mapToolPan = None
        self.toolSelectByPolygon = None

        self.accepted.connect(self.closed)
        self.rejected.connect(self.closed)

        self.wptLayer = None

        self.arpFeatureArray = []
        self.currentLayer = define._canvas.currentLayer()
        self.rwyFeatureArray = []
        self.rwyEndPosition = None
        self.initAerodromeAndRwyCmb()
        
        self.socRubber = None
        self.socAnnotation = QgsTextAnnotationItem(define._canvas)
        self.socAnnotation.setDocument(QTextDocument(Captions.SOC))
        self.socAnnotation.setFrameBackgroundColor(Qt.white)
        self.socAnnotation.setFrameSize(QSizeF(30, 20))
        self.socAnnotation.setFrameColor(Qt.magenta)
        self.socAnnotation.hide()
        self.socPoint3d = None
        
        self.daRubber = None
        self.daAnnotation = QgsTextAnnotationItem(define._canvas)
        self.daAnnotation.setDocument(QTextDocument(Captions.DA))
        self.daAnnotation.setFrameBackgroundColor(Qt.white)
        self.daAnnotation.setFrameSize(QSizeF(30, 20))
        self.daAnnotation.setFrameColor(Qt.magenta)
        self.daAnnotation.hide()
        self.daPoint3d = None

        self.annotationFAWP = self.parametersPanel.pnlFafPosition.annotation
        self.annotationMAPt = self.parametersPanel.pnlMaPtPosition.annotation
        # self.surfaceType = self.dlgType
    def initAerodromeAndRwyCmb(self):

        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.arpFeatureArray = self.aerodromeAndRwyCmbFill(self.currentLayer, self.parametersPanel.cmbAerodrome, None, self.parametersPanel.cmbRwyDir)
            self.calcRwyBearing()
    def calcRwyBearing(self):
        try:
            point3dMapt = self.parametersPanel.pnlMaPtPosition.Point3d
            point3dFaf = self.parametersPanel.pnlFafPosition.Point3d
            if point3dMapt == None:
                self.parametersPanel.pnlInboundTrack.Value = 0.0
                return
            self.parametersPanel.pnlInboundTrack.Value = round(Unit.ConvertRadToDeg(MathHelper.getBearing(point3dFaf, point3dMapt)), 4)
            self.showMarkDaSoc()
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
                # attrValueList.insert(0, "")
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

                    # aerodromePositionPanelObj.Point3d = Point3D(long, lat, alt)
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
        return arpFeatureList
    def rwyDirCmbObj_Event_0(self):
        if len(self.rwyFeatureArray) == 0:
            self.calcRwyBearing()
            return
        idxName = self.currentLayer.fieldNameIndex('Name')
        idxLat = self.currentLayer.fieldNameIndex('Latitude')
        idxLong = self.currentLayer.fieldNameIndex('Longitude')
        idxAltitude = self.currentLayer.fieldNameIndex('Altitude')
        idxAttr = self.currentLayer.fieldNameIndex('Attributes')
        # rwyFeatList = []
        featIter = self.currentLayer.getFeatures()
        # for feat in featIter:
        #     attrValue = feat.attributes()[idxAttr].toString()
        #     if attrValue == self.cmbAerodrome.SelectedItem:
        #         attrValue = feat.attributes()[idxName].toString()
        #         s = attrValue.replace(" ", "")
        #         compStr = s.left(6).toUpper()
        #         if compStr == "THRRWY":
        #             valStr = s.right(s.length() - 6)
        #             rwyFeatList.append(feat)
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

            self.parametersPanel.pnlThrPosition.Point3d = Point3D(long, lat, alt)

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

                self.parametersPanel.pnlRwyEndPosition.Point3d = Point3D(long, lat, alt)
                break
            break
        self.calcRwyBearing()
    def aerodromeCmbObj_Event_0(self):
        if len(self.arpFeatureArray) == 0:
            return
        # self.parametersPanel.pnlArp.Point3d = None
        self.parametersPanel.pnlRwyEndPosition.Point3d = None
        self.parametersPanel.pnlThrPosition.Point3d = None
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
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, self.surfaceType, self.ui.tblObstacles, None, parameterList, resultHideColumnNames)

    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("RNAV Specification", self.parametersPanel.cmbRnavSpecification.SelectedItem))
        if self.parametersPanel.cmbRnavSpecification.SelectedIndex == 0:
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
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlWaypoint1.txtPointX.text()), float(self.parametersPanel.pnlWaypoint1.txtPointY.text()))

        parameterList.append(("Lat", self.parametersPanel.pnlWaypoint1.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlWaypoint1.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlWaypoint1.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlWaypoint1.txtPointY.text()))

        parameterList.append(("Cat.H", str(self.parametersPanel.chbCatH.Checked)))
        parameterList.append((self.parametersPanel.chbCircularArcs.Caption, str(self.parametersPanel.chbCircularArcs.Checked)))

        parameterList.append(("Parameters", "group"))
        parameterList.append(("Selection Mode", self.parametersPanel.cmbSelectionMode.SelectedItem))
        parameterList.append(("In-bound Track", "Plan : " + str(self.parametersPanel.pnlInbound.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.pnlInbound.txtRadialGeodetic.Value) + define._degreeStr))

        # parameterList.append(("In-bound Track", self.parametersPanel.txtInbound.Value))
        parameterList.append(("Out-bound Track", "Plan : " + str(self.parametersPanel.pnlOutbound.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.pnlOutbound.txtRadialGeodetic.Value) + define._degreeStr))

        # parameterList.append(("Out-bound Track", self.parametersPanel.txtOutbound.Value))
        parameterList.append(("IAS", str(self.parametersPanel.pnlIas.Value.Knots) + "kts"))
        parameterList.append(("Altitude", str(self.parametersPanel.pnlAltitude.Value.Feet) + "ft"))
        parameterList.append(("ISA", str(self.parametersPanel.pnlIsa.Value)))
        parameterList.append(("Bank Angle", str(self.parametersPanel.pnlBankAngle.Value)))
        parameterList.append(("Wind", str(self.parametersPanel.pnlWind.Value.Knots) + "kts"))
        parameterList.append(("Primary Moc", str(self.parametersPanel.pnlPrimaryMoc.Value.Metres) + "m"))
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstructionType.SelectedItem))
        parameterList.append(("MOCmultipiler", str(self.parametersPanel.mocSpinBox.value())))
        if self.parametersPanel.cmbConstructionType.SelectedIndex == 0:
            parameterList.append(("Draw Waypoint Tolerance", str(self.parametersPanel.chbDrawTolerance.Checked)))

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
        self.ui.tabCtrlGeneral.removeTab(1)
        self.ui.btnEvaluate.setVisible(False)
        self.ui.btnConstruct.setVisible(False)
#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)


    # def btnPDTCheck_Click(self):
    #     pdtResultStr = MathHelper.pdtCheckResultToString(float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), float(self.parametersPanel.txtIas.text()), float(self.parametersPanel.txtTime.text()))
    #
    #     QMessageBox.warning(self, "PDT Check", pdtResultStr)
    def btnEvaluate_Click(self):

        # self.complexObstacleArea.ObstacleArea = None
        #
        # ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        # self.obstaclesModel = TurnProtectionAndObstacleAssessmentObstacles(self.complexObstacleArea, self.parametersPanel.pnlPrimaryMoc.Value, self.parametersPanel.pnlAltitude.Value, self.manualPolygon )


        FlightPlanBaseDlg.btnEvaluate_Click(self)
        self.ui.btnLocate.setEnabled(True)



    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return





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
        ui = Ui_NpaAtDistanceTime()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)



        self.parametersPanel.cmbAircraftCategory.Items = ["A", "B", "C", "D", "E", "H", "Custom"]



        self.connect(self.parametersPanel.pnlAerodromeAltitude, SIGNAL("editingFinished"), self.altitudeChanged)
        self.connect(self.parametersPanel.pnlIas, SIGNAL("Event_0"), self.altitudeChanged)
        self.connect(self.parametersPanel.pnlTas, SIGNAL("Event_0"), self.showMarkDaSoc)
        self.connect(self.parametersPanel.pnlIsa, SIGNAL("editingFinished"), self.altitudeChanged)
        self.connect(self.parametersPanel.pnlEstimatedAltitude, SIGNAL("Event_0"), self.pnlEstimatedAltitude_Event_0)
        self.connect(self.parametersPanel.pnlEstimatedAltitude, SIGNAL("editingFinished"), self.showMarkDaSoc)
        self.connect(self.parametersPanel.cmbAircraftCategory, SIGNAL("Event_0"), self.cmbAircraftCategory_Event_0)
        # # self.connect(self.parametersPanel.cmbPhaseOfFlight, SIGNAL("Event_0"), self.cmbPhaseOfFlightChanged)
        # # self.connect(self.parametersPanel.cmbSelectionMode, SIGNAL("Event_0"), self.manualEvent)
        self.connect(self.parametersPanel.pnlDistA, SIGNAL("editingFinished"), self.showMarkDaSoc)
        self.connect(self.parametersPanel.pnlDistB, SIGNAL("editingFinished"), self.showMarkDaSoc)
        # self.connect(self.parametersPanel.pnlRDH, SIGNAL("editingFinished"), self.pnlRDH_Event_0)
        # self.connect(self.parametersPanel.pnlDistX, SIGNAL("Event_0"), self.showMarkDaSoc)
        # # self.connect(self.parametersPanel.cmbType2, SIGNAL("Event_0"), self.method_31)
        #
        self.connect(self.parametersPanel.pnlFafPosition, SIGNAL("positionChanged"), self.calcRwyBearing)
        self.connect(self.parametersPanel.pnlMaPtPosition, SIGNAL("positionChanged"), self.calcRwyBearing)
        self.connect(self.parametersPanel.pnlThrPosition, SIGNAL("positionChanged"), self.putDistances)

        # self.parametersPanel.pnlFafPosition.btnCalculater.clicked.connect(self.pnlFafPosition_btnCalculater_clicked)
        # self.parametersPanel.pnlMaPtPosition.btnCalculater.clicked.connect(self.pnlMaPtPosition_btnCalculater_clicked)

        #
        self.parametersPanel.cmbAircraftCategory.SelectedIndex = 0

        # self.putAircraftSpeed()
        self.fixToleranceFAF = 1900
        self.altitudeChanged()
        self.calcSocAltitude()




    def pnlFafPosition_btnCalculater_clicked(self):
        self.gbFAWP = self.parametersPanel.pnlFafPosition
        dlg = CalcDlg(self, RnavCommonWaypoint.FAWP, self.parametersPanel.cmbAircraftCategory.SelectedIndex, None, None, [self.parametersPanel.pnlThrPosition.Point3d, self.parametersPanel.pnlRwyEndPosition.Point3d, None])
        dlg.setWindowTitle("Calculate FAF")
        dlg.groupBox_4.setVisible(False)
        dlg.groupBox_5.setVisible(False)
        dlg.resize(200,100)

        dlg.txtForm.setText("")
        self.parameterCalcList = []
        dlg.txtDistance.setEnabled(True)
        self.annotationFAWP.show()
        dlg.show()

    def pnlMaPtPosition_btnCalculater_clicked(self):
        self.gbMAWP = self.parametersPanel.pnlMaPtPosition
        dlg = CalcDlg(self, RnavCommonWaypoint.MAWP, self.parametersPanel.cmbAircraftCategory.SelectedIndex, None, None, [self.parametersPanel.pnlThrPosition.Point3d, self.parametersPanel.pnlRwyEndPosition.Point3d, None])
        dlg.setWindowTitle("Calculate MAPt")
        dlg.groupBox_4.setVisible(False)
        dlg.groupBox_5.setVisible(False)
        dlg.resize(200,100)

        dlg.txtForm.setText("")
        self.parameterCalcList = []
        dlg.txtDistance.setEnabled(True)
        self.annotationMAPt.show()
        dlg.show()

    def putDistances(self):
        try:
            point3dThr = self.parametersPanel.pnlThrPosition.Point3d
            point3dFaf = self.parametersPanel.pnlFafPosition.Point3d

            point3dMapt = self.parametersPanel.pnlMaPtPosition.Point3d

            speedTas = self.parametersPanel.pnlTas.Value
            inboundTrackRad = Unit.ConvertDegToRad(self.parametersPanel.pnlInboundTrack.Value)
            inboundTrack180Rad = MathHelper.smethod_4(inboundTrackRad + math.pi)




            dDist = Distance(MathHelper.calcDistance(point3dFaf, point3dMapt))
            self.parametersPanel.pnlDistOfFafMapt.Value = dDist

            aDist = self.parametersPanel.pnlDistA.Value
            bDist = self.parametersPanel.pnlDistB.Value

            tasMin = Speed.smethod_0(self.parametersPanel.pnlIas.Value, -10, self.parametersPanel.pnlAerodromeAltitude.Value)
            tasMax = Speed.smethod_0(self.parametersPanel.pnlIas.Value, 15, self.parametersPanel.pnlAerodromeAltitude.Value)

            # calculate Distance from earliest MAPt to nominal MAPt:
            x1 = math.sqrt(math.pow(aDist.NauticalMiles, 2) + math.pow(tasMin.Knots * 10 / float(3600), 2) + math.pow(30 * dDist.NauticalMiles / tasMin.Knots, 2))
            x2 = math.sqrt(math.pow(aDist.NauticalMiles, 2) + math.pow(tasMax.Knots * 10 / float(3600), 2) + math.pow(30 * dDist.NauticalMiles / tasMax.Knots, 2))
            distEarliestMaptToNominalMapt = Distance(max(x1, x2), DistanceUnits.NM)
            self.parametersPanel.pnlDistOfEarliestToNominalMapt.Value = distEarliestMaptToNominalMapt

            #calculate Distance from nominal MAPt to latest MAPt
            x3 = math.sqrt(math.pow(bDist.NauticalMiles, 2) + math.pow(tasMin.Knots * 13 / float(3600), 2) + math.pow(30 * dDist.NauticalMiles / tasMin.Knots, 2))
            x4 = math.sqrt(math.pow(bDist.NauticalMiles, 2) + math.pow(tasMax.Knots * 13 / float(3600), 2) + math.pow(30 * dDist.NauticalMiles / tasMax.Knots, 2))
            distNominalMaptToLatestMapt = Distance(max(x3, x4), DistanceUnits.NM)
            self.parametersPanel.pnlDistOfNominalToLatestMapt.Value = distNominalMaptToLatestMapt

            #calculate Distance from Mapt to SOC
            x5 = x3 + 15 * (tasMin.Knots + 10) / float(3600)
            x6 = x4 + 15 * (tasMax.Knots + 10) / float(3600)
            distMaptSoc = Distance(max(x5, x6), DistanceUnits.NM)
            socMaptDistMeters = distMaptSoc.Metres
            socThrDistMeters = MathHelper.calcDistance(point3dMapt, point3dThr) - socMaptDistMeters



            sockBearing = inboundTrackRad
            self.socPoint3d = MathHelper.distanceBearingPoint(point3dMapt, sockBearing, socMaptDistMeters).smethod_167(self.calcSocAltitude())


            self.parametersPanel.pnlDistOfMaptSoc.Value = Distance(socMaptDistMeters)
            self.parametersPanel.pnlDistOfSocThr.Value = Distance(MathHelper.calcDistance(self.socPoint3d, point3dThr))
            self.parametersPanel.pnlDistOfFafMapt.Value = Distance(MathHelper.calcDistance(point3dFaf, point3dMapt))#MathHelper.calcDistance(point3dThr, self.socPoint3d))
            self.parametersPanel.pnlDistOfMaptThr.Value = Distance(MathHelper.calcDistance(point3dMapt, point3dThr))
        except:
            pass
    def calcDAndXDistance(self, speed_0, speed_1, double_0):
        return Distance((speed_0 + speed_1).MetresPerSecond * double_0).Metres
    def showMarkDaSoc(self):
        try:
            self.putDistances()
            flag = FlightPlanBaseDlg.btnConstruct_Click(self)
            # if not flag:
            #     return
            point3dThr = self.parametersPanel.pnlThrPosition.Point3d
            point3dFaf = self.parametersPanel.pnlFafPosition.Point3d

            point3dMapt = self.parametersPanel.pnlMaPtPosition.Point3d
            if self.socPoint3d == None:
                return
            socLayer = AcadHelper.createVectorLayer("SOC_MAPt_" + self.surfaceType, QGis.Point)
            AcadHelper.setGeometryAndAttributesInLayer(socLayer, self.socPoint3d, False, {"Caption":"SOC"})
            AcadHelper.setGeometryAndAttributesInLayer(socLayer, point3dMapt, False, {"Caption":"MAPt"})

            QgisHelper.appendToCanvas(define._canvas, [socLayer], self.surfaceType)

            palSetting = QgsPalLayerSettings()
            palSetting.readFromLayer(socLayer)
            palSetting.enabled = True
            palSetting.fieldName = "Caption"
            palSetting.isExpression = True
            palSetting.placement = QgsPalLayerSettings.AroundPoint
            palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '8', "")
            palSetting.writeToLayer(socLayer)

            # QgisHelper.zoomToLayers([socLayer])
            self.resultLayerList = [socLayer]



            return socLayer
        except:
            pass


    def pnlEstimatedAltitude_Event_0(self):
        self.calcSocAltitude()
        # self.putDistances()

    def cmbAircraftCategory_Event_0(self):
        self.putAircraftSpeed()
        self.showMarkDaSoc()


    def calcSocAltitude(self):
        # val = self.parametersPanel.pnlEstimatedAltitude.Value.Metres - self.parametersPanel.pnlHeightLoss.Value.Metres
        self.parametersPanel.pnlSocAltitude.Value = Altitude(self.parametersPanel.pnlEstimatedAltitude.Value.Metres)
        return self.parametersPanel.pnlEstimatedAltitude.Value.Metres


    def altitudeChanged(self):
        self.parametersPanel.pnlWind.setAltitude(self.parametersPanel.pnlAerodromeAltitude.Value)
        try:
            self.parametersPanel.pnlTas.Value = Speed.smethod_0(self.parametersPanel.pnlIas.Value, self.parametersPanel.pnlIsa.Value, self.parametersPanel.pnlAerodromeAltitude.Value)
            self.showMarkDaSoc()
        except:
            raise ValueError("Value Invalid")

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

        fieldName = "CATEGORY"
        resultLayer.dataProvider().addAttributes( [QgsField(fieldName, QVariant.String)] )
        resultLayer.startEditing()
        fields = resultLayer.pendingFields()
        i = 1
        feature = QgsFeature()
        feature.setFields(fields)

        feature.setGeometry(QgsGeometry.fromPoint (self.parametersPanel.pnlWaypoint1.Point3d))
        feature.setAttribute(fieldName, "Waypoint1")
        pr = resultLayer.dataProvider()
        pr.addFeatures([feature])
        # resultLayer.addFeature(feature)
        feature.setGeometry(QgsGeometry.fromPoint (self.parametersPanel.pnlWaypoint2.Point3d))
        feature.setAttribute(fieldName, "Waypoint2")
        pr = resultLayer.dataProvider()
        pr.addFeatures([feature])
        # resultLayer.addFeature(feature)
        resultLayer.commitChanges()

        renderCatFly = None
        if self.parametersPanel.cmbType1.SelectedIndex == 1:
            '''FlyOver'''

            symbolFlyOver = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
            symbolFlyOver.deleteSymbolLayer(0)
            svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyover.svg", 10.0, 0.0)
            symbolFlyOver.appendSymbolLayer(svgSymLayer)
            renderCatFly = QgsRendererCategoryV2(0, symbolFlyOver,"Fly Over")
        elif self.parametersPanel.cmbType1.SelectedIndex == 0:
            '''FlyBy'''
            symbolFlyBy = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
            symbolFlyBy.deleteSymbolLayer(0)
            svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyby.svg", 10.0, 0.0)
            symbolFlyBy.appendSymbolLayer(svgSymLayer)
            renderCatFly = QgsRendererCategoryV2(0, symbolFlyBy,"Fly By")
        else:
            return None
        WPT_EXPRESION = "CASE WHEN  \"CATEGORY\" = 'Waypoint1'  THEN 0 " + \
                                        "END"
        symRenderer = QgsCategorizedSymbolRendererV2(WPT_EXPRESION, [renderCatFly])

        resultLayer.setRendererV2(symRenderer)
        return resultLayer
    def putAircraftSpeed(self):
        speedTas = self.parametersPanel.pnlTas.Value

        if self.parametersPanel.cmbAircraftCategory.SelectedIndex == AircraftSpeedCategory.A:
            self.parametersPanel.pnlIas.Value = Speed(100)
            # self.parametersPanel.pnlIas.Value = Speed(90)
        elif self.parametersPanel.cmbAircraftCategory.SelectedIndex == AircraftSpeedCategory.B:
            self.parametersPanel.pnlIas.Value = Speed(130)
            # self.parametersPanel.pnlIas.Value = Speed(120)
        elif self.parametersPanel.cmbAircraftCategory.SelectedIndex == AircraftSpeedCategory.C:
            self.parametersPanel.pnlIas.Value = Speed(160)
            # self.parametersPanel.pnlIas.Value = Speed(140)
        elif self.parametersPanel.cmbAircraftCategory.SelectedIndex == AircraftSpeedCategory.D:
            self.parametersPanel.pnlIas.Value = Speed(185)
            # self.parametersPanel.pnlIas.Value = Speed(165)
        elif self.parametersPanel.cmbAircraftCategory.SelectedIndex == AircraftSpeedCategory.E:
            self.parametersPanel.pnlIas.Value = Speed(230)
            # self.parametersPanel.pnlIas.Value = Speed(210)
        elif self.parametersPanel.cmbAircraftCategory.SelectedIndex == AircraftSpeedCategory.Custom:
            # self.parametersPanel.pnlIas.Value = self.customIas
            self.parametersPanel.pnlIas.Value = Speed(185)
        elif self.parametersPanel.cmbAircraftCategory.SelectedIndex == AircraftSpeedCategory.H:
            # self.parametersPanel.pnlIas.Value = self.customIas
            self.parametersPanel.pnlIas.Value = Speed(90)
        self.parametersPanel.pnlIas.Enabled = self.parametersPanel.cmbAircraftCategory.SelectedIndex == AircraftSpeedCategory.Custom


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
    def canvasPressEvent( self, e ):
        if ( self.mRubberBand == None ):
            self.mRubberBand0.reset( QGis.Polygon )
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
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))