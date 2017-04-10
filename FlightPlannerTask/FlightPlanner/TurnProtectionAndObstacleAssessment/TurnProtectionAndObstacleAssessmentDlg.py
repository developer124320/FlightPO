# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QString, Qt,  QVariant
from PyQt4.QtGui import QColor,QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsCoordinateReferenceSystem,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, \
                QgsVectorFileWriter, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, \
                QgsSymbolV2, QgsRendererCategoryV2, QgsGeometry
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapToolPan
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType, SurfaceTypes, \
                 DistanceUnits,AircraftSpeedCategory, RnavGnssFlightPhase, AltitudeUnits, \
                 ObstacleAreaResult, RnavFlightPhase, ConstructionType, RnavSpecification, IntersectionStatus,\
                 TurnDirection,RnavWaypointType, AngleUnits, OffsetGapType
from FlightPlanner.TurnProtectionAndObstacleAssessment.ui_TurnProtectionAndObstacleAssessment import Ui_TurnProtectionAndObstacleAssessment
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
from FlightPlanner.BasicGNSS.windSpiral import WindSpiral
from qgis.core import QGis, QgsRectangle, QgsGeometry, QgsCsException, QgsPoint,\
        QgsFeatureRequest, QgsCoordinateTransform, QgsFeature, QgsVectorLayer

from Type.switch import switch
import define, math

class TurnProtectionAndObstacleAssessmentDlg(FlightPlanBaseDlg):

    def __init__(self, parent):

        # line1 = QgsGeometry.fromPolyline([QgsPoint(100,100), QgsPoint(200, 100)])
        # line2 = QgsGeometry.fromPolyline([QgsPoint(150,150), QgsPoint(150, 50)])
        # result, geomList, ptList = line1.splitGeometry([QgsPoint(150,150), QgsPoint(150, 50)], True)


        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("TurnProtectionAndObstacleAssessmentDlg")
        self.surfaceType = SurfaceTypes.TurnProtectionAndObstacleAssessment
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.TurnProtectionAndObstacleAssessment)
        self.resize(540, 600)
        QgisHelper.matchingDialogSize(self, 720, 700)
        self.surfaceList = None
        self.manualPolygon = None

        self.mapToolPan = None
        self.toolSelectByPolygon = None

        self.accepted.connect(self.closed)
        self.rejected.connect(self.closed)

        self.wptLayer = None

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
#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)


    # def btnPDTCheck_Click(self):
    #     pdtResultStr = MathHelper.pdtCheckResultToString(float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), float(self.parametersPanel.txtIas.text()), float(self.parametersPanel.txtTime.text()))
    #
    #     QMessageBox.warning(self, "PDT Check", pdtResultStr)
    def btnEvaluate_Click(self):

        self.complexObstacleArea.ObstacleArea = None


        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        self.obstaclesModel = TurnProtectionAndObstacleAssessmentObstacles(self.complexObstacleArea, self.parametersPanel.pnlPrimaryMoc.Value, self.parametersPanel.pnlAltitude.Value, self.manualPolygon )


        FlightPlanBaseDlg.btnEvaluate_Click(self)
        self.ui.btnLocate.setEnabled(True)

    def distanceCheckMethod(self):
        if self.parametersPanel.cmbPhaseOfFlight.Visible != True:
            return
        phaseOfFlightType = self.parametersPanel.cmbPhaseOfFlight.SelectedItem
        if self.parametersPanel.cmbRnavSpecification.SelectedItem == "RnpApch":
            try:
                arpPt = self.parametersPanel.pnlArp.Point3d
                wpt1 = self.parametersPanel.pnlWaypoint1.Point3d
                wpt2 = self.parametersPanel.pnlWaypoint2.Point3d
                if MathHelper.calcDistance(arpPt, wpt1) > Unit.ConvertNMToMeter(30) or MathHelper.calcDistance(arpPt, wpt2) > Unit.ConvertNMToMeter(30):
                    QMessageBox.warning(self, "Warning", "Your part of STAR is outside 30 NM from the ARP")
            except:
                pass
            return
        if phaseOfFlightType.contains(">30"):
            try:
                arpPt = self.parametersPanel.pnlArp.Point3d
                wpt1 = self.parametersPanel.pnlWaypoint1.Point3d
                wpt2 = self.parametersPanel.pnlWaypoint2.Point3d
                if MathHelper.calcDistance(arpPt, wpt1) < Unit.ConvertNMToMeter(30) or MathHelper.calcDistance(arpPt, wpt2) < Unit.ConvertNMToMeter(30):
                    QMessageBox.warning(self, "Warning", "Your part of STAR is inside 30 NM from the ARP.\n Change RNAV Specification.")
            except:
                pass
        elif phaseOfFlightType.contains("<30"):
            try:
                arpPt = self.parametersPanel.pnlArp.Point3d
                wpt1 = self.parametersPanel.pnlWaypoint1.Point3d
                wpt2 = self.parametersPanel.pnlWaypoint2.Point3d
                if MathHelper.calcDistance(arpPt, wpt1) > Unit.ConvertNMToMeter(30) or MathHelper.calcDistance(arpPt, wpt2) > Unit.ConvertNMToMeter(30):
                    QMessageBox.warning(self, "Warning", "Your part of STAR is outside 30 NM from the ARP.\n Change RNAV Specification.")
            except:
                pass
        elif phaseOfFlightType.contains("<15"):
            try:
                arpPt = self.parametersPanel.pnlArp.Point3d
                wpt1 = self.parametersPanel.pnlWaypoint1.Point3d
                wpt2 = self.parametersPanel.pnlWaypoint2.Point3d
                if MathHelper.calcDistance(arpPt, wpt1) > Unit.ConvertNMToMeter(15) or MathHelper.calcDistance(arpPt, wpt2) > Unit.ConvertNMToMeter(15):
                    QMessageBox.warning(self, "Warning", "Your part of STAR is outside 15 NM from the ARP.\n Change RNAV Specification.")
            except:
                pass


    def btnConstruct_Click(self):
        # flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        # if not flag:
        #     return
        self.distanceCheckMethod()

        mapUnits = define._canvas.mapUnits()
        constructionLayer = AcadHelper.createVectorLayer(self.surfaceType)


        self.complexObstacleArea = None

        rnavGnssTolerance = None
        rnavGnssTolerance2 = None
        point3d = self.parametersPanel.pnlWaypoint1.Point3d
        point3d1 = None
        if self.parametersPanel.chbUseTwoWpt.Checked:
            point3d1 = self.parametersPanel.pnlWaypoint2.Point3d
        tas = Speed.smethod_0(self.parametersPanel.pnlIas.Value, self.parametersPanel.pnlIsa.Value, self.parametersPanel.pnlAltitude.Value)
        inboundTrack = MathHelper.smethod_3(self.parametersPanel.pnlInbound.Value)
        outboundTrack = MathHelper.smethod_3(self.parametersPanel.pnlOutbound.Value)
        rnavWaypointType = self.method_33()
        turnDirectionList = []
        polylineAreaAAA = PolylineArea()
        num2 = MathHelper.smethod_77(inboundTrack, outboundTrack, AngleUnits.Degrees, turnDirectionList)
        turnDirection_0 = turnDirectionList[0]
        # if (num2 > 120 and self.parametersPanel.cmbType1.SelectedIndex == 0):
        #     QMessageBox.warning(self, "Warning", Messages.ERR_COURSE_CHANGES_GREATER_THAN_120_NOT_ALLOWED)
        #     return (None, None, None, None, None, None, None, None, None, None)

#             throw new Exception(Messages.ERR_COURSE_CHANGES_GREATER_THAN_120_NOT_ALLOWED)
        num = MathHelper.smethod_4(Unit.ConvertDegToRad(inboundTrack))
        num1 = MathHelper.smethod_4(Unit.ConvertDegToRad(outboundTrack))


        # winSpiral = WindSpiral(point3d, num, tas, self.parametersPanel.pnlWind.Value, float(self.parametersPanel.pnlBankAngle.Value), turnDirection_0)
        # resultPointArrayList = []
        # for i in range(3):
        #     resultPointArrayList.append([winSpiral.Start[i], winSpiral.Middle[i], winSpiral.Finish[i]])
        # for pointArray in resultPointArrayList:
        #     AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, pointArray)


        aircraftSpeedCategory = AircraftSpeedCategory.H if (self.parametersPanel.chbCatH.Checked) else AircraftSpeedCategory.C
        # if (self.parametersPanel.cmbRnavSpecification.SelectedIndex <= 0):
        #     rnavGnssTolerance = RnavGnssTolerance(None, None, None, None, self.parametersPanel.pnlTolerances.XTT, self.parametersPanel.pnlTolerances.ATT, self.parametersPanel.pnlTolerances.ASW)
        # else:
        #     rnavSpecification = self.rnavSpecification
        #     rnavFlightPhase = self.phaseOfFlight
        #     rnavGnssTolerance = RnavGnssTolerance(rnavSpecification, None, aircraftSpeedCategory,  rnavFlightPhase, Distance(MathHelper.calcDistance(point3d, self.parametersPanel.pnlArp.Point3d))) if (rnavFlightPhase != RnavFlightPhase.Enroute) else RnavGnssTolerance(rnavSpecification, None, aircraftSpeedCategory, rnavFlightPhase, Distance(50, DistanceUnits.NM))
        rnavGnssTolerance = RnavGnssTolerance(None, None, None, None, self.parametersPanel.pnlTolerances.XTT, self.parametersPanel.pnlTolerances.ATT, self.parametersPanel.pnlTolerances.ASW)
        rnavGnssTolerance2 = RnavGnssTolerance(None, None, None, None, self.parametersPanel.pnlTolerances2.XTT, self.parametersPanel.pnlTolerances2.ATT, self.parametersPanel.pnlTolerances2.ASW)
        point3dCollection_0 = self.method_39(point3d, rnavGnssTolerance, num)
        resultPolylineAreaList = []
        if not self.parametersPanel.chbUseTwoWpt.Checked:
            polylineAreaAAA, self.complexObstacleArea, turnDirection, turnConstructionMethod, polylineArea, polylineArea1, polylineArea2, polylineArea3, polylineArea4, point3dCollection = self.method_40()
            if polylineAreaAAA == None and self.complexObstacleArea == None and polylineArea2 == None:
                return

            count = polylineArea1.Count

            # if self.parametersPanel.cmbType1.SelectedIndex != 2 and self.parametersPanel.chbUseTwoWpt.Checked and self.parametersPanel.rdnDF.isChecked():
            #     polylineArea4.method_1(self.parametersPanel.pnlWaypoint2.Point3d)
            resultPolylineAreaList.append(PolylineArea.smethod_131(polylineArea1))
            resultPolylineAreaList.append(PolylineArea.smethod_131(polylineArea2))
            resultPolylineAreaList.append(PolylineArea.smethod_136(self.complexObstacleArea.ObstacleArea.previewArea, True))
            resultPolylineAreaList.append(PolylineArea.smethod_131(polylineArea4))
        else:
            if (num2 <= (60 if (aircraftSpeedCategory == AircraftSpeedCategory.H) else 30) and self.parametersPanel.chbCircularArcs.Checked):
                turnConstructionMethod_0 = TurnConstructionMethod.CircularArcs

                self.complexObstacleArea, resultPolylineAreaList = self.circularArcMethod(self.parametersPanel.pnlWaypoint1.Point3d, self.parametersPanel.pnlWaypoint2.Point3d, num, num1, rnavGnssTolerance, rnavGnssTolerance2, turnDirection_0)

                # for polylineArea in resultPolylineAreaList:
                #     AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea)
                # AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, nominalTrackPolyline)
            elif rnavWaypointType == RnavWaypointType.FlyOver:
                if self.parametersPanel.rdnDF.isChecked():
                    self.complexObstacleArea, resultPolylineAreaList = self.flyOverTurnAllowedWithDF_method(point3d, point3d1, num, num1, rnavGnssTolerance, rnavGnssTolerance2, turnDirection_0)
                elif self.parametersPanel.rdnCF.isChecked() and round(MathHelper.getBearing(point3d, point3d1), 2) != round(num1, 2):
                    self.complexObstacleArea, resultPolylineAreaList = self.flyOverTurnAllowedWithCF_method(point3d, point3d1, num, num1, rnavGnssTolerance, rnavGnssTolerance2, turnDirection_0)
                else:
                    self.complexObstacleArea, resultPolylineAreaList = self.flyOverTurnAllowedWithTF_method(point3d, point3d1, num, num1, rnavGnssTolerance, rnavGnssTolerance2, turnDirection_0)

            elif rnavWaypointType == RnavWaypointType.FlyBy:
                if self.parametersPanel.rdnCF.isChecked() and round(MathHelper.getBearing(point3d, point3d1), 2) != round(num1, 2):
                    self.complexObstacleArea, resultPolylineAreaList = self.InCaseFlyByCFMethod(point3d, point3d1, num, num1, rnavGnssTolerance, rnavGnssTolerance2, turnDirection_0)
                else:
                    self.complexObstacleArea, resultPolylineAreaList = self.InCaseFlyByMethod(point3d, point3d1, num, num1, rnavGnssTolerance, rnavGnssTolerance2, turnDirection_0)
            else:
                polylineAreaAAA, self.complexObstacleArea, turnDirection, turnConstructionMethod, polylineArea, polylineArea1, polylineArea2, polylineArea3, polylineArea4, point3dCollection = self.method_40()
                if polylineAreaAAA == None and self.complexObstacleArea == None and polylineArea2 == None:
                    return

                count = polylineArea1.Count

                if self.parametersPanel.cmbType1.SelectedIndex != 2 and self.parametersPanel.chbUseTwoWpt.Checked and self.parametersPanel.rdnDF.isChecked():
                    polylineArea4.method_1(self.parametersPanel.pnlWaypoint2.Point3d)
                resultPolylineAreaList.append(PolylineArea.smethod_131(polylineArea1))
                resultPolylineAreaList.append(PolylineArea.smethod_131(polylineArea2))
                resultPolylineAreaList.append(PolylineArea.smethod_136(self.complexObstacleArea.ObstacleArea.previewArea, True))
                resultPolylineAreaList.append(PolylineArea.smethod_131(polylineArea4))
        if (self.parametersPanel.chbDrawTolerance.Checked):
            point3dCollection_0 = self.method_39(point3d, rnavGnssTolerance, num);
            resultPolylineAreaList.append(PolylineArea.smethod_133(point3dCollection_0, True))
            if point3d1 != None:
                point3dCollection_0 = self.method_39(point3d1, rnavGnssTolerance2, num1);
                resultPolylineAreaList.append(PolylineArea.smethod_133(point3dCollection_0, True))

        for polylineAreaTemp in resultPolylineAreaList:
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineAreaTemp)
        self.wptLayer = AcadHelper.WPT2Layer(self.parametersPanel.pnlWaypoint1.Point3d, self.parametersPanel.pnlWaypoint2.Point3d, "WPT_" + self.surfaceType.replace(" ", "_").replace("-", "_"), [self.parametersPanel.cmbType1.SelectedItem, self.parametersPanel.cmbType2.SelectedItem])
        # self.wptLayer = AcadHelper.WPT2Layer(winSpiral.method_0(num1 + 15 * math.pi / 180, AngleUnits.Radians), self.parametersPanel.pnlWaypoint2.Point3d, "WPT", [self.parametersPanel.cmbType1.SelectedItem, self.parametersPanel.cmbType2.SelectedItem])

        QgisHelper.appendToCanvas(define._canvas, [constructionLayer, self.wptLayer], self.surfaceType)

        self.resultLayerList = [constructionLayer, self.wptLayer]
        QgisHelper.zoomToLayers(self.resultLayerList)
        self.ui.btnEvaluate.setEnabled(True)
        self.manualEvent(self.parametersPanel.cmbSelectionMode.SelectedIndex)
    def InCaseFlyByCFMethod(self, point3d_Wpt1, point3d_Wpt2, inboundTrack, outboundTrack, rnavGnssTolerance1, rnavGnssTolerance2, turnDirection):
        inboundTrackMinus90 = MathHelper.smethod_4(inboundTrack - math.pi / 2)
        inboundTrackPlus90 = MathHelper.smethod_4(inboundTrack + math.pi / 2)
        inboundTrackPlus180 = MathHelper.smethod_4(inboundTrack + math.pi)
        outboundTrackMinus90 = MathHelper.smethod_4(outboundTrack - math.pi / 2)
        outboundTrackPlus90 = MathHelper.smethod_4(outboundTrack + math.pi / 2)
        outboundTrackPlus180 = MathHelper.smethod_4(outboundTrack + math.pi)
        complexObstacleArea = ComplexObstacleArea()
        asw1 = rnavGnssTolerance1.ASW / 2
        att1 = rnavGnssTolerance1.ATT
        asw2 = rnavGnssTolerance2.ASW / 2
        att2 = rnavGnssTolerance2.ATT
        if not self.parametersPanel.pnlArp.Visible or not self.parametersPanel.pnlArp.IsValid():
            asw2 = asw1



        cfWpt1 = point3d_Wpt1
        point3d_Wpt1 = MathHelper.getIntersectionPoint(point3d_Wpt1, MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack, 100),
                                                       point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus180, 100))


        distFromEnd = 0.0
        if self.parametersPanel.pnlArp.Visible and self.parametersPanel.pnlArp.IsValid():
            distBetweenWPT = MathHelper.calcDistance(self.parametersPanel.pnlArp.Point3d,
                                                 MathHelper.getIntersectionPoint(self.parametersPanel.pnlArp.Point3d, MathHelper.distanceBearingPoint(self.parametersPanel.pnlArp.Point3d, outboundTrack, 100),
                                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100)))
            if distBetweenWPT > Unit.ConvertNMToMeter(30):
                distFromEnd = distBetweenWPT - Unit.ConvertNMToMeter(30)
            elif distBetweenWPT > Unit.ConvertNMToMeter(15):
                distFromEnd = distBetweenWPT - Unit.ConvertNMToMeter(15)
            if distFromEnd > 0.0:
                d = 0.0
                if asw1.Metres > asw2.Metres:
                    d = (asw1.Metres - asw2.Metres) * math.tan(Unit.ConvertDegToRad(60)) * 2
                elif asw1.Metres < asw2.Metres:
                    d = (asw2.Metres - asw1.Metres) * math.tan(Unit.ConvertDegToRad(75)) * 2
                if d == 0.0 or d > distFromEnd:
                    distFromEnd = 0.0
        if not (distFromEnd > 0.0 and asw1.Metres != asw2.Metres):
            asw2 = asw1

        turnAngleCF = MathHelper.smethod_76(Unit.smethod_1(inboundTrack), Unit.smethod_1(MathHelper.getBearing(cfWpt1, point3d_Wpt2)), AngleUnits.Degrees)
        turnAngle = MathHelper.smethod_76(Unit.smethod_1(inboundTrack), Unit.smethod_1(outboundTrack), AngleUnits.Degrees)
        if turnAngle < turnAngleCF:
            point3d_Wpt1 = cfWpt1
        # turnAngle = turnAngleCF

        rnavWaypointType1 = self.method_33()
        resultPolylineAreList = []
        # turnAngle = MathHelper.smethod_76(Unit.smethod_1(inboundTrack), Unit.smethod_1(outboundTrack), AngleUnits.Degrees)
        turnAngleRad = Unit.ConvertDegToRad(turnAngle)
        joinAngleRad = Unit.ConvertDegToRad(30)
        speedTas = Speed.smethod_0(self.parametersPanel.pnlIas.Value, self.parametersPanel.pnlIsa.Value, self.parametersPanel.pnlAltitude.Value)
        speedWind = self.parametersPanel.pnlWind.Value
        valueBankAngle = self.parametersPanel.pnlBankAngle.Value
        distance = Distance.smethod_0(speedTas, valueBankAngle)
        metres3 = distance.Metres
        distance = RnavWaypoints.getDistanceFromWaypointToEarliestTurningPoint(rnavWaypointType1, Distance(att1.Metres), Distance(metres3), turnAngle, AngleUnits.Degrees)
        distFromWpt1ToEarliest = distance.Metres
        point3dEarliest = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, math.fabs(distFromWpt1ToEarliest)) if (distFromWpt1ToEarliest >= 0) else MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack, math.fabs(distFromWpt1ToEarliest))
        distance = RnavWaypoints.getDistanceFromWaypointToLatestTurningPoint(rnavWaypointType1, speedTas, speedWind, float(self.parametersPanel.pnlPilotTime.Value), float(self.parametersPanel.pnlBankEstTime.Value), Distance(att1.Metres), Distance(metres3), turnAngle, AngleUnits.Degrees)
        distFromWpt1ToLatest = distance.Metres
        point3dLatest = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, math.fabs(distFromWpt1ToLatest)) if (distFromWpt1ToLatest >= 0) else MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack, math.fabs(distFromWpt1ToLatest))
        joinBearing1 = 0.0

        primaryPolylineArea = PolylineArea()
        primaryOutLine = PolylineArea()
        primaryInLine = PolylineArea()
        secondaryPolylineAreaOut = PolylineArea()
        secondaryPolylineAreaIn = PolylineArea()
        if turnAngle <= 90:
            if turnDirection == TurnDirection.Right:
                #### Creating Primary Area
                # cfStartPt = MathHelper.distanceBearingPoint(cfWpt1, inboundTrackMinus90, asw1.Metres)
                # primaryPolylineArea.method_1(cfStartPt)
                # primaryOutLine.method_1(cfStartPt)

                ptEk = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
                primaryPolylineArea.method_1(ptEk)
                primaryOutLine.method_1(ptEk)

                startPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackMinus90, asw1.Metres)
                windSpiral1 = WindSpiral(startPt1, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                startPt2 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackPlus90, asw1.Metres)
                windSpiral2 = WindSpiral(startPt2, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                pt0 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                pt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackMinus90, asw2.Metres)
                if windSpiral1.method_1(pt0, pt1, False):
                    middlePt11, contactPt11, p = windSpiral1.getContactWithBearingOfTangent(inboundTrack, 0)
                    point3dArray = [startPt1, contactPt11]
                    intersectPolylineArea11 = PolylineArea(point3dArray)
                    intersectPolylineArea11.SetBulgeAt(0, MathHelper.smethod_60(startPt1, middlePt11, contactPt11))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                    primaryPolylineArea.extend(intersectPolylineArea11)
                    primaryOutLine.extend(intersectPolylineArea11)

                    middlePt12, contactPt12, p = windSpiral1.getContactWithBearingOfTangent(outboundTrack, 0)
                    intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                                   contactPt12, MathHelper.distanceBearingPoint(contactPt12, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt1)
                    primaryPolylineArea.method_1(contactPt12)
                    primaryOutLine.method_1(intersectPt1)
                    primaryOutLine.method_1(contactPt12)

                    if windSpiral2.method_1(pt0, pt1, False):
                        bearing = MathHelper.smethod_4(MathHelper.getBearing(windSpiral1.Center[1], windSpiral2.Center[1]) - math.pi / 2)
                        intersectPt2 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], bearing, windSpiral1.Radius[1])
                        contactPt14 = MathHelper.distanceBearingPoint(windSpiral2.Center[1], bearing, windSpiral2.Radius[1])
                        primaryPolylineArea.method_1(intersectPt2)
                        primaryPolylineArea.method_1(contactPt14)
                        primaryOutLine.method_1(intersectPt2)
                        primaryOutLine.method_1(contactPt14)

                        contactPt13 = windSpiral2.method_0(MathHelper.smethod_4(outboundTrack + joinAngleRad), AngleUnits.Radians)
                        primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                        intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 10000),
                                                                   primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))

                        if intersectPt3 == None:
                            contactPt13 = contactPt14
                            intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                                                       primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                                                primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))
                        else:
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 10000),
                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))

                    else:
                        contactPt13 = windSpiral1.method_0(MathHelper.smethod_4(outboundTrack + joinAngleRad), AngleUnits.Radians)
                        primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                        intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 10000),
                                                                   primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))

                        if intersectPt3 == None:
                            contactPt13 = contactPt12
                            intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                                                       primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                                                primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))
                        else:
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 10000),
                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))

                    primaryPolylineArea.method_1(contactPt13)
                    primaryOutLine.method_1(contactPt13)

                    # if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    #     testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                    #                                              point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                    #     if testPt != None and MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:


                    primaryPolylineArea.method_1(intersectPt3)
                    primaryOutLine.method_1(intersectPt3)

                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(mergePtPrimary)

                        primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                        primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)
                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)
                        else:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary1)
                        primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

                    else:
                        primaryPolylineArea.method_1(primaryEndPt1)
                        primaryOutLine.method_1(primaryEndPt1)



                    primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                    primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(primaryEndPt2)
                        primaryInLine.method_1(primaryEndPt2)

                        primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)

                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)
                        else:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary2)
                        primaryPolylineArea.method_1(mergePtPrimaryIn)
                        primaryInLine.method_1(mergePtPrimary2)
                        primaryInLine.method_1(mergePtPrimaryIn)
                    else:
                        primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                        primaryInLine.method_1(primaryEndPt2ByAsw1)

                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryPolylineArea.method_1(primaryEndPt2)
                    # primaryOutLine.method_1(primaryEndPt1)
                    # primaryInLine.method_1(primaryEndPt2)

                    ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
                    intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100),
                                                                   primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt4)
                    primaryPolylineArea.method_1(ptEk1)
                    primaryInLine.method_1(intersectPt4)
                    primaryInLine.method_1(ptEk1)

                    # cfendPt = MathHelper.distanceBearingPoint(cfWpt1, inboundTrackPlus90, asw1.Metres)
                    # primaryPolylineArea.method_1(cfendPt)
                    # primaryInLine.method_1(cfendPt)

                    primaryPolylineArea.method_1(ptEk)
                    resultPolylineAreList.append(primaryPolylineArea)
                    complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))

                    # resultPolylineAreList.append(PolylineArea(windSpiral1.get_Object().asPolyline()))
                    # resultPolylineAreList.append(PolylineArea(windSpiral2.get_Object().asPolyline()))

                    #### SecondaryAreaIn
                    secondaryPolylineAreaIn.extend(primaryInLine)
                    # cfSecPt = MathHelper.distanceBearingPoint(cfendPt, inboundTrackPlus90, asw1.Metres)
                    ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackPlus90, asw1.Metres)
                    d = asw1.Metres
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        d = asw2.Metres
                    secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus90, d)
                    secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                                                                             ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100))
                    # secondaryPolylineAreaIn.method_1(cfSecPt)
                    secondaryPolylineAreaIn.method_1(ptEK11)
                    secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)
                    else:
                        primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                        secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)

                    resultPolylineAreList.append(secondaryPolylineAreaIn)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))

                    #### SecondaryAreaOut
                    secondaryPolylineAreaOut = primaryOutLine.method_23(asw1.Metres, OffsetGapType.Fillet)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                        if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                            secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                        secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                        secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                        secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackPlus90, asw1.Metres))

                    secondaryPolylineAreaOut.reverse()
                    secondaryPolylineAreaOut.extend(primaryOutLine)
                    secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
                    resultPolylineAreList.append(secondaryPolylineAreaOut)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))

                else:
                    middlePt11, contactPt11, p = windSpiral1.getContactWithBearingOfTangent(inboundTrack, 0)
                    point3dArray = [startPt1, contactPt11]
                    intersectPolylineArea11 = PolylineArea(point3dArray)
                    intersectPolylineArea11.SetBulgeAt(0, MathHelper.smethod_60(startPt1, middlePt11, contactPt11))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                    primaryPolylineArea.extend(intersectPolylineArea11)
                    primaryOutLine.extend(intersectPolylineArea11)

                    primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                    intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                                   primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                    testPt = MathHelper.getIntersectionPoint(intersectPt1, MathHelper.distanceBearingPoint(intersectPt1, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                    if MathHelper.calcDistance(intersectPt1, testPt) < distFromEnd:
                        primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                        intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                                   primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt1)
                    primaryOutLine.method_1(intersectPt1)
                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryOutLine.method_1(primaryEndPt1)

                    primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)

                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(mergePtPrimary)

                        primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                        primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)
                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)
                        else:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary1)
                        primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

                    else:
                        primaryPolylineArea.method_1(primaryEndPt1)
                        primaryOutLine.method_1(primaryEndPt1)

                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryOutLine.method_1(primaryEndPt1)
                    # primaryPolylineArea.method_1(primaryEndPt2)
                    # primaryInLine.method_1(primaryEndPt2)
                    primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(primaryEndPt2)
                        primaryInLine.method_1(primaryEndPt2)

                        primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)

                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)
                        else:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary2)
                        primaryPolylineArea.method_1(mergePtPrimaryIn)
                        primaryInLine.method_1(mergePtPrimary2)
                        primaryInLine.method_1(mergePtPrimaryIn)
                    else:
                        primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                        primaryInLine.method_1(primaryEndPt2ByAsw1)

                    ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
                    intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100),
                                                                   primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt4)
                    primaryPolylineArea.method_1(ptEk1)
                    primaryInLine.method_1(intersectPt4)
                    primaryInLine.method_1(ptEk1)

                    # cfendPt = MathHelper.distanceBearingPoint(cfWpt1, inboundTrackPlus90, asw1.Metres)
                    # primaryPolylineArea.method_1(cfendPt)
                    # primaryInLine.method_1(cfendPt)

                    primaryPolylineArea.method_1(ptEk)
                    resultPolylineAreList.append(primaryPolylineArea)
                    complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))

                    #### SecondaryAreaIn
                    secondaryPolylineAreaIn.extend(primaryInLine)
                    # cfSecPt = MathHelper.distanceBearingPoint(cfendPt, inboundTrackPlus90, asw1.Metres)
                    ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackPlus90, asw1.Metres)
                    d = asw1.Metres
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        d = asw2.Metres
                    secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus90, d)
                    secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                                                                             ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100))
                    # secondaryPolylineAreaIn.method_1(cfSecPt)
                    secondaryPolylineAreaIn.method_1(ptEK11)
                    secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)
                    else:
                        primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                        secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)

                    resultPolylineAreList.append(secondaryPolylineAreaIn)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))

                    #### SecondaryAreaOut
                    secondaryPolylineAreaOut = primaryOutLine.method_23(asw1.Metres, OffsetGapType.Fillet)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        testPt = MathHelper.getIntersectionPoint(intersectPt1, MathHelper.distanceBearingPoint(intersectPt1, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                        if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                            secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)


                        secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                        secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                        secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackPlus90, asw1.Metres))

                    secondaryPolylineAreaOut.reverse()
                    secondaryPolylineAreaOut.extend(primaryOutLine)
                    secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
                    resultPolylineAreList.append(secondaryPolylineAreaOut)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))
            else:

                #### Creating Primary Area
                # cfStartPt = MathHelper.distanceBearingPoint(cfWpt1, inboundTrackPlus90, asw1.Metres)
                # primaryPolylineArea.method_1(cfStartPt)
                # primaryOutLine.method_1(cfStartPt)

                ptEk = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
                primaryPolylineArea.method_1(ptEk)
                primaryOutLine.method_1(ptEk)

                startPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackPlus90, asw1.Metres)
                windSpiral1 = WindSpiral(startPt1, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                startPt2 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackMinus90, asw1.Metres)
                windSpiral2 = WindSpiral(startPt2, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                pt0 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                pt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackPlus90, asw2.Metres)
                if windSpiral1.method_1(pt0, pt1, False):
                    p, contactPt11, middlePt11 = windSpiral1.getContactWithBearingOfTangent(inboundTrack, 0)
                    point3dArray = [startPt1, contactPt11]
                    intersectPolylineArea11 = PolylineArea(point3dArray)
                    intersectPolylineArea11.SetBulgeAt(0, MathHelper.smethod_60(startPt1, middlePt11, contactPt11))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                    primaryPolylineArea.extend(intersectPolylineArea11)
                    primaryOutLine.extend(intersectPolylineArea11)

                    p, contactPt12, middlePt12 = windSpiral1.getContactWithBearingOfTangent(outboundTrack, 0)
                    intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                                   contactPt12, MathHelper.distanceBearingPoint(contactPt12, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt1)
                    primaryPolylineArea.method_1(contactPt12)
                    primaryOutLine.method_1(intersectPt1)
                    primaryOutLine.method_1(contactPt12)

                    if windSpiral2.method_1(pt0, pt1, False):
                        bearing = MathHelper.smethod_4(MathHelper.getBearing(windSpiral1.Center[1], windSpiral2.Center[1]) + math.pi / 2)
                        intersectPt2 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], bearing, windSpiral1.Radius[1])
                        contactPt14 = MathHelper.distanceBearingPoint(windSpiral2.Center[1], bearing, windSpiral2.Radius[1])
                        primaryPolylineArea.method_1(intersectPt2)
                        primaryPolylineArea.method_1(contactPt14)
                        primaryOutLine.method_1(intersectPt2)
                        primaryOutLine.method_1(contactPt14)

                        contactPt13 = windSpiral2.method_0(MathHelper.smethod_4(outboundTrack - joinAngleRad), AngleUnits.Radians)
                        primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                        # intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                        #                                            primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                        intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 10000),
                                                                   primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))

                        if intersectPt3 == None:
                            contactPt13 = contactPt14
                            intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                                                       primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                                                primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))

                        else:
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 10000),
                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))

                    else:
                        contactPt13 = windSpiral1.method_0(MathHelper.smethod_4(outboundTrack - joinAngleRad), AngleUnits.Radians)
                        primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                        # intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                        #                                            primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                        intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 10000),
                                                                   primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))

                        if intersectPt3 == None:
                            contactPt13 = contactPt12
                            intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                                                       primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))
                        else:
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 10000),
                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))


                    primaryPolylineArea.method_1(contactPt13)
                    primaryOutLine.method_1(contactPt13)
                    primaryPolylineArea.method_1(intersectPt3)
                    primaryOutLine.method_1(intersectPt3)

                    primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)

                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(mergePtPrimary)

                        primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                        primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)
                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)
                        else:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary1)
                        primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

                    else:
                        primaryPolylineArea.method_1(primaryEndPt1)
                        primaryOutLine.method_1(primaryEndPt1)

                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryPolylineArea.method_1(primaryEndPt2)
                    # primaryOutLine.method_1(primaryEndPt1)
                    # primaryInLine.method_1(primaryEndPt2)
                    primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(primaryEndPt2)
                        primaryInLine.method_1(primaryEndPt2)

                        primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)

                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)
                        else:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary2)
                        primaryPolylineArea.method_1(mergePtPrimaryIn)
                        primaryInLine.method_1(mergePtPrimary2)
                        primaryInLine.method_1(mergePtPrimaryIn)
                    else:
                        primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                        primaryInLine.method_1(primaryEndPt2ByAsw1)

                    ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
                    intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack + turnAngleRad / 2), 100),
                                                                   primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt4)
                    primaryPolylineArea.method_1(ptEk1)
                    primaryInLine.method_1(intersectPt4)
                    primaryInLine.method_1(ptEk1)

                    # cfendPt = MathHelper.distanceBearingPoint(cfWpt1, inboundTrackMinus90, asw1.Metres)
                    # primaryPolylineArea.method_1(cfendPt)
                    # primaryInLine.method_1(cfendPt)

                    primaryPolylineArea.method_1(ptEk)
                    resultPolylineAreList.append(primaryPolylineArea)
                    complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))

                    # resultPolylineAreList.append(PolylineArea(windSpiral1.get_Object().asPolyline()))
                    # resultPolylineAreList.append(PolylineArea(windSpiral2.get_Object().asPolyline()))

                    #### SecondaryAreaIn
                    secondaryPolylineAreaIn.extend(primaryInLine)
                    ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackMinus90, asw1.Metres)
                    d = asw1.Metres
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        d = asw2.Metres
                    secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, d)
                    # secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, asw1.Metres)
                    secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                                                                             ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack + turnAngleRad / 2), 100))
                    # cfSecPt = MathHelper.distanceBearingPoint(cfendPt, inboundTrackMinus90, asw1.Metres)
                    # secondaryPolylineAreaIn.method_1(cfSecPt)
                    secondaryPolylineAreaIn.method_1(ptEK11)
                    secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)
                    else:
                        primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                        secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)

                    resultPolylineAreList.append(secondaryPolylineAreaIn)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))

                    #### SecondaryAreaOut
                    secondaryPolylineAreaOut = primaryOutLine.method_23(-asw1.Metres, OffsetGapType.Fillet)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        secondaryPolylineAreaOut.reverse()
                        testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                        if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                            secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                        secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                        secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                        secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackMinus90, asw1.Metres))
                        ptArray = primaryOutLine.method_14()
                        primaryOutLine = PolylineArea(ptArray)
                        primaryOutLine.reverse()
                    # secondaryPolylineAreaOut.reverse()
                    secondaryPolylineAreaOut.extend(primaryOutLine)
                    secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
                    resultPolylineAreList.append(secondaryPolylineAreaOut)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))
                else:
                    p, contactPt11, middlePt11 = windSpiral1.getContactWithBearingOfTangent(inboundTrack, 0)
                    point3dArray = [startPt1, contactPt11]
                    intersectPolylineArea11 = PolylineArea(point3dArray)
                    intersectPolylineArea11.SetBulgeAt(0, MathHelper.smethod_60(startPt1, middlePt11, contactPt11))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                    primaryPolylineArea.extend(intersectPolylineArea11)
                    primaryOutLine.extend(intersectPolylineArea11)

                    primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                    intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                                   primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                    testPt = MathHelper.getIntersectionPoint(intersectPt1, MathHelper.distanceBearingPoint(intersectPt1, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                    if MathHelper.calcDistance(intersectPt1, testPt) < distFromEnd:
                        primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                        intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                                   primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))

                    primaryPolylineArea.method_1(intersectPt1)
                    primaryOutLine.method_1(intersectPt1)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(mergePtPrimary)

                        primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                        primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)
                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)
                        else:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary1)
                        primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

                    else:
                        primaryPolylineArea.method_1(primaryEndPt1)
                        primaryOutLine.method_1(primaryEndPt1)
                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryOutLine.method_1(primaryEndPt1)

                    primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                    primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(primaryEndPt2)
                        primaryInLine.method_1(primaryEndPt2)

                        primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)

                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)
                        else:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary2)
                        primaryPolylineArea.method_1(mergePtPrimaryIn)
                        primaryInLine.method_1(mergePtPrimary2)
                        primaryInLine.method_1(mergePtPrimaryIn)
                    else:
                        primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                        primaryInLine.method_1(primaryEndPt2ByAsw1)

                    ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
                    intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack + turnAngleRad / 2), 100),
                                                                   primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt4)
                    primaryPolylineArea.method_1(ptEk1)
                    primaryInLine.method_1(intersectPt4)
                    primaryInLine.method_1(ptEk1)

                    # cfendPt = MathHelper.distanceBearingPoint(cfWpt1, inboundTrackMinus90, asw1.Metres)
                    # primaryPolylineArea.method_1(cfendPt)
                    # primaryInLine.method_1(cfendPt)

                    primaryPolylineArea.method_1(ptEk)
                    resultPolylineAreList.append(primaryPolylineArea)
                    complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))

                    #### SecondaryAreaIn
                    secondaryPolylineAreaIn.extend(primaryInLine)
                    ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackMinus90, asw1.Metres)
                    d = asw1.Metres
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        d = asw2.Metres
                    secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, d)
                    # secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, asw1.Metres)
                    secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                                                                             ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack + turnAngleRad / 2), 100))
                    # cfSecPt = MathHelper.distanceBearingPoint(cfendPt, inboundTrackMinus90, asw1.Metres)
                    # secondaryPolylineAreaIn.method_1(cfSecPt)
                    secondaryPolylineAreaIn.method_1(ptEK11)
                    secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)
                    else:
                        primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                        secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)

                    resultPolylineAreList.append(secondaryPolylineAreaIn)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))

                    #### SecondaryAreaOut
                    secondaryPolylineAreaOut = primaryOutLine.method_23(-asw1.Metres, OffsetGapType.Fillet)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        secondaryPolylineAreaOut.reverse()
                        testPt = MathHelper.getIntersectionPoint(intersectPt1, MathHelper.distanceBearingPoint(intersectPt1, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                        if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                            secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                        secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                        secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                        secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackMinus90, asw1.Metres))
                        ptArray = primaryOutLine.method_14()
                        primaryOutLine = PolylineArea(ptArray)
                        primaryOutLine.reverse()
                    # secondaryPolylineAreaOut.reverse()
                    secondaryPolylineAreaOut.extend(primaryOutLine)
                    secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
                    resultPolylineAreList.append(secondaryPolylineAreaOut)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))
        else:
            if turnDirection == TurnDirection.Right:
                #### Creating Primary Area
                # cfStartPt = MathHelper.distanceBearingPoint(cfWpt1, inboundTrackMinus90, asw1.Metres)
                # primaryPolylineArea.method_1(cfStartPt)
                # primaryOutLine.method_1(cfStartPt)

                ptEk = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
                primaryPolylineArea.method_1(ptEk)
                primaryOutLine.method_1(ptEk)

                startPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackMinus90, asw1.Metres)
                windSpiral1 = WindSpiral(startPt1, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                startPt2 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackPlus90, asw1.Metres)
                windSpiral2 = WindSpiral(startPt2, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                pt0 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                pt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackMinus90, asw2.Metres)
                # if windSpiral1.method_1(pt0, pt1, False):
                middlePt11, contactPt11, p = windSpiral1.getContactWithBearingOfTangent(inboundTrack, 0)
                point3dArray = [startPt1, contactPt11]
                intersectPolylineArea11 = PolylineArea(point3dArray)
                intersectPolylineArea11.SetBulgeAt(0, MathHelper.smethod_60(startPt1, middlePt11, contactPt11))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                primaryPolylineArea.extend(intersectPolylineArea11)
                primaryOutLine.extend(intersectPolylineArea11)

                middlePt12, contactPt12, p = windSpiral1.getContactWithBearingOfTangent(inboundTrackPlus90, 0)
                intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                               contactPt12, MathHelper.distanceBearingPoint(contactPt12, inboundTrackMinus90, 100))
                primaryPolylineArea.method_1(intersectPt1)
                primaryPolylineArea.method_1(contactPt12)
                primaryOutLine.method_1(intersectPt1)
                primaryOutLine.method_1(contactPt12)

                middlePt14, contactPt14, rightMiddlePt14 = windSpiral2.getContactWithBearingOfTangent(inboundTrackPlus90, 0)
                leftMiddlePt13, contactPt13, p = windSpiral2.getContactWithBearingOfTangent(MathHelper.smethod_4(outboundTrack + joinAngleRad))
                pointArray = [contactPt14, contactPt13]
                tempPolylineArea = PolylineArea(pointArray)
                tempPolylineArea.SetBulgeAt(0, MathHelper.smethod_60(contactPt14, leftMiddlePt13, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                primaryPolylineArea.extend(tempPolylineArea)
                primaryOutLine.extend(tempPolylineArea)

                primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                           point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                pt = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2)),
                                                           primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2)))




                if pt != None:
                    intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                           primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))

                    testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                    if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                        primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                        intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                                        primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt3)
                    primaryOutLine.method_1(intersectPt3)

                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryOutLine.method_1(primaryEndPt1)
                else:
                    primaryPolylineArea.method_1(intersectPt3)
                    primaryOutLine.method_1(intersectPt3)



                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                    mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                    primaryPolylineArea.method_1(mergePtPrimary)

                    primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                    primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)
                    if asw1.Metres > asw2.Metres:
                        mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                                   primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                        mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)
                    else:
                        mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                                   primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                        mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)

                    primaryPolylineArea.method_1(mergePtPrimary1)
                    primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

                else:
                    primaryPolylineArea.method_1(primaryEndPt1)
                    primaryOutLine.method_1(primaryEndPt1)

                primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                    mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                    primaryPolylineArea.method_1(primaryEndPt2)
                    primaryInLine.method_1(primaryEndPt2)

                    primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)

                    if asw1.Metres > asw2.Metres:
                        mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                                   primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                        mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)
                    else:
                        mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                                   primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                        mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)

                    primaryPolylineArea.method_1(mergePtPrimary2)
                    primaryPolylineArea.method_1(mergePtPrimaryIn)
                    primaryInLine.method_1(mergePtPrimary2)
                    primaryInLine.method_1(mergePtPrimaryIn)
                else:
                    primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                    primaryInLine.method_1(primaryEndPt2ByAsw1)

                ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
                intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100),
                                                               primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
                primaryPolylineArea.method_1(intersectPt4)
                primaryPolylineArea.method_1(ptEk1)
                primaryInLine.method_1(intersectPt4)
                primaryInLine.method_1(ptEk1)


                # cfendPt = MathHelper.distanceBearingPoint(cfWpt1, inboundTrackPlus90, asw1.Metres)
                # primaryPolylineArea.method_1(cfendPt)
                # primaryInLine.method_1(cfendPt)

                primaryPolylineArea.method_1(ptEk)
                resultPolylineAreList.append(primaryPolylineArea)


                # resultPolylineAreList.append(PolylineArea(windSpiral1.get_Object().asPolyline()))
                # resultPolylineAreList.append(PolylineArea(windSpiral2.get_Object().asPolyline()))

                #### SecondaryAreaIn
                secondaryPolylineAreaIn.extend(primaryInLine)
                ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackPlus90, asw1.Metres)
                d = asw1.Metres
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    d = asw2.Metres
                secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus90, d)
                secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                                                                         ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100))
                # cfSecPt = MathHelper.distanceBearingPoint(cfendPt, inboundTrackPlus90, asw1.Metres)
                # secondaryPolylineAreaIn.method_1(cfSecPt)
                secondaryPolylineAreaIn.method_1(ptEK11)
                secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                    secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                    secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                    secondaryPolylineAreaIn.method_1(primaryEndPt2)
                else:
                    primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                    secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                    secondaryPolylineAreaIn.method_1(primaryEndPt2)

                resultPolylineAreList.append(secondaryPolylineAreaIn)

                #### SecondaryAreaOut
                secondaryPolylineAreaOut = primaryOutLine.method_23(asw1.Metres, OffsetGapType.Fillet)
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                    if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                        secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                    secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                    secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                    secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                    secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                    secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackPlus90, asw1.Metres))
                secondaryPolylineAreaOut.reverse()
                secondaryPolylineAreaOut.extend(primaryOutLine)
                secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
                resultPolylineAreList.append(secondaryPolylineAreaOut)

                complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))
                complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))
                complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))

                # else:
                #     middlePt11, contactPt11, p = windSpiral1.getContactWithBearingOfTangent(inboundTrack, 0)
                #     point3dArray = [startPt1, contactPt11]
                #     intersectPolylineArea11 = PolylineArea(point3dArray)
                #     intersectPolylineArea11.SetBulgeAt(0, MathHelper.smethod_60(startPt1, middlePt11, contactPt11))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                #
                #     primaryPolylineArea.extend(intersectPolylineArea11)
                #     primaryOutLine.extend(intersectPolylineArea11)
                #
                #     primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                #     intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                #                                                    primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                #     primaryPolylineArea.method_1(intersectPt1)
                #     primaryOutLine.method_1(intersectPt1)
                #     primaryPolylineArea.method_1(primaryEndPt1)
                #     primaryOutLine.method_1(primaryEndPt1)
                #
                #     primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                #
                #     primaryPolylineArea.method_1(primaryEndPt1)
                #     primaryPolylineArea.method_1(primaryEndPt2)
                #     primaryOutLine.method_1(primaryEndPt1)
                #     primaryInLine.method_1(primaryEndPt2)
                #
                #     ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
                #     intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100),
                #                                                    primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
                #     primaryPolylineArea.method_1(intersectPt4)
                #     primaryPolylineArea.method_1(ptEk1)
                #     primaryInLine.method_1(intersectPt4)
                #     primaryInLine.method_1(ptEk1)
                #
                #     primaryPolylineArea.method_1(ptEk)
                #     resultPolylineAreList.append(primaryPolylineArea)
                #
                #     #### SecondaryAreaIn
                #     secondaryPolylineAreaIn.extend(primaryInLine)
                #     ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackPlus90, asw1.Metres)
                #     secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus90, asw1.Metres)
                #     secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                #                                                              ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100))
                #     secondaryPolylineAreaIn.method_1(ptEK11)
                #     secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
                #     secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                #     secondaryPolylineAreaIn.method_1(primaryEndPt2)
                #
                #     resultPolylineAreList.append(secondaryPolylineAreaIn)
                #
                #     #### SecondaryAreaOut
                #     secondaryPolylineAreaOut = primaryOutLine.method_23(asw1.Metres, OffsetGapType.Fillet)
                #     secondaryPolylineAreaOut.reverse()
                #     secondaryPolylineAreaOut.extend(primaryOutLine)
                #     secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
                #     resultPolylineAreList.append(secondaryPolylineAreaOut)
            else:
                #### Creating Primary Area
                # cfStartPt = MathHelper.distanceBearingPoint(cfWpt1, inboundTrackPlus90, asw1.Metres)
                # primaryPolylineArea.method_1(cfStartPt)
                # primaryOutLine.method_1(cfStartPt)

                ptEk = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
                primaryPolylineArea.method_1(ptEk)
                primaryOutLine.method_1(ptEk)

                startPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackPlus90, asw1.Metres)
                windSpiral1 = WindSpiral(startPt1, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                startPt2 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackMinus90, asw1.Metres)
                windSpiral2 = WindSpiral(startPt2, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                pt0 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                pt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackPlus90, asw2.Metres)
                # if windSpiral1.method_1(pt0, pt1, False):
                p, contactPt11, middlePt11 = windSpiral1.getContactWithBearingOfTangent(inboundTrack, 0)
                point3dArray = [startPt1, contactPt11]
                intersectPolylineArea11 = PolylineArea(point3dArray)
                intersectPolylineArea11.SetBulgeAt(0, MathHelper.smethod_60(startPt1, middlePt11, contactPt11))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                primaryPolylineArea.extend(intersectPolylineArea11)
                primaryOutLine.extend(intersectPolylineArea11)

                p, contactPt12, middlePt12 = windSpiral1.getContactWithBearingOfTangent(inboundTrackMinus90, 0)
                intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                               contactPt12, MathHelper.distanceBearingPoint(contactPt12, inboundTrackPlus90, 100))
                primaryPolylineArea.method_1(intersectPt1)
                primaryPolylineArea.method_1(contactPt12)
                primaryOutLine.method_1(intersectPt1)
                primaryOutLine.method_1(contactPt12)

                middlePt14, contactPt14, rightMiddlePt14 = windSpiral2.getContactWithBearingOfTangent(inboundTrackMinus90, 0)
                leftMiddlePt13, contactPt13, p = windSpiral2.getContactWithBearingOfTangent(MathHelper.smethod_4(outboundTrack - joinAngleRad))
                pointArray = [contactPt14, contactPt13]
                tempPolylineArea = PolylineArea(pointArray)
                tempPolylineArea.SetBulgeAt(0, MathHelper.smethod_60(contactPt14, p, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                primaryPolylineArea.extend(tempPolylineArea)
                primaryOutLine.extend(tempPolylineArea)

                primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)


                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                           point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, 100))
                pt = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2)),
                                                           primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2)))

                if pt != None:
                    intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                           primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                    testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                    if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                        primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                        intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                           primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))

                    primaryPolylineArea.method_1(intersectPt3)
                    primaryOutLine.method_1(intersectPt3)


                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryOutLine.method_1(primaryEndPt1)
                else:
                    primaryPolylineArea.method_1(intersectPt3)
                    primaryOutLine.method_1(intersectPt3)



                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                    mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                    primaryPolylineArea.method_1(mergePtPrimary)

                    primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                    primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)
                    if asw1.Metres > asw2.Metres:
                        mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                                   primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                        mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)
                    else:
                        mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                                   primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                        mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)

                    primaryPolylineArea.method_1(mergePtPrimary1)
                    primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

                else:
                    primaryPolylineArea.method_1(primaryEndPt1)
                    primaryOutLine.method_1(primaryEndPt1)

                primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                    mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                    primaryPolylineArea.method_1(primaryEndPt2)
                    primaryInLine.method_1(primaryEndPt2)

                    primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)

                    if asw1.Metres > asw2.Metres:
                        mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                                   primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                        mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)
                    else:
                        mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                                   primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                        mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)

                    primaryPolylineArea.method_1(mergePtPrimary2)
                    primaryPolylineArea.method_1(mergePtPrimaryIn)
                    primaryInLine.method_1(mergePtPrimary2)
                    primaryInLine.method_1(mergePtPrimaryIn)
                else:
                    primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                    primaryInLine.method_1(primaryEndPt2ByAsw1)

                ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
                intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack + turnAngleRad / 2), 100),
                                                               primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
                primaryPolylineArea.method_1(intersectPt4)
                primaryPolylineArea.method_1(ptEk1)
                primaryInLine.method_1(intersectPt4)
                primaryInLine.method_1(ptEk1)


                # cfendPt = MathHelper.distanceBearingPoint(cfWpt1, inboundTrackMinus90, asw1.Metres)
                # primaryPolylineArea.method_1(cfendPt)
                # primaryInLine.method_1(cfendPt)

                primaryPolylineArea.method_1(ptEk)
                resultPolylineAreList.append(primaryPolylineArea)

                # resultPolylineAreList.append(PolylineArea(windSpiral1.get_Object().asPolyline()))
                # resultPolylineAreList.append(PolylineArea(windSpiral2.get_Object().asPolyline()))

                #### SecondaryAreaIn
                secondaryPolylineAreaIn.extend(primaryInLine)
                ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackMinus90, asw1.Metres)
                d = asw1.Metres
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    d = asw2.Metres
                secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, d)
                # secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, asw1.Metres)
                secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                                                                         ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack + turnAngleRad / 2), 100))
                # cfSecPt = MathHelper.distanceBearingPoint(cfendPt, inboundTrackMinus90, asw1.Metres)
                # secondaryPolylineAreaIn.method_1(cfSecPt)
                secondaryPolylineAreaIn.method_1(ptEK11)
                secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                    secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                    secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                    secondaryPolylineAreaIn.method_1(primaryEndPt2)
                else:
                    primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                    secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                    secondaryPolylineAreaIn.method_1(primaryEndPt2)

                resultPolylineAreList.append(secondaryPolylineAreaIn)

                #### SecondaryAreaOut
                secondaryPolylineAreaOut = primaryOutLine.method_23(-asw1.Metres, OffsetGapType.Fillet)
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    secondaryPolylineAreaOut.reverse()
                    testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                    if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                        secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                    secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                    secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                    secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                    secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                    secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackMinus90, asw1.Metres))
                    ptArray = primaryOutLine.method_14()
                    primaryOutLine = PolylineArea(ptArray)
                    primaryOutLine.reverse()
                # secondaryPolylineAreaOut.reverse()
                secondaryPolylineAreaOut.extend(primaryOutLine)
                secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
                resultPolylineAreList.append(secondaryPolylineAreaOut)

                complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))
                complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))
                complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))


        if not MathHelper.pointInPolygon(primaryPolylineArea.method_14(), cfWpt1, 0.001):
            polylineArea = PolylineArea()
            polylineArea.method_1(cfWpt1)
            if turnDirection == TurnDirection.Right:
                polylineArea.method_1(MathHelper.distanceBearingPoint(ptEk, inboundTrackMinus90, asw1.Metres))
            else:
                polylineArea.method_1(MathHelper.distanceBearingPoint(ptEk, inboundTrackPlus90, asw1.Metres))
            polylineArea.method_1(ptEK11)
            # polylineArea.method_1(MathHelper.getIntersectionPoint(cfWpt1, MathHelper.distanceBearingPoint(cfWpt1, MathHelper.smethod_4(inboundTrack + Unit.ConvertDegToRad(15)), 100),\
            #                                                       point3d_Wpt1, MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackMinus90, 100)))
            # polylineArea.method_1(MathHelper.getIntersectionPoint(cfWpt1, MathHelper.distanceBearingPoint(cfWpt1, MathHelper.smethod_4(inboundTrack - Unit.ConvertDegToRad(15)), 100),\
            #                                                       point3d_Wpt1, MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackMinus90, 100)))
            polylineArea.method_1(cfWpt1)
            resultPolylineAreList.append(polylineArea)

        nominalTrackPolylineArea = PolylineArea()
        num19 = metres3 * math.tan(Unit.ConvertDegToRad(turnAngle / 2))
        if (self.parametersPanel.chbCatH.Checked):
            metresPerSecond1 = 3 * speedTas.MetresPerSecond
            num = metresPerSecond1
        else:
            metresPerSecond1 = 5 * speedTas.MetresPerSecond
            num = metresPerSecond1
        num = metresPerSecond1

        point3d33 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, num19)
        point3d34 = MathHelper.distanceBearingPoint(point3d33, inboundTrackPlus90, 100)
        point3d35 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrack, num19)
        point3d36 = MathHelper.distanceBearingPoint(point3d35, outboundTrackPlus90, 100)
        point3d2 = MathHelper.getIntersectionPoint(point3d33, point3d34, point3d35, point3d36)
        point3d33 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, num19 + num)
        point3d34 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, num19)
        point3d35 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrack, num19)
        point3d36 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrack, num19 + num)
        nominalTrackPolylineArea.method_1(point3d33)
        nominalTrackPolylineArea.Add(PolylineAreaPoint(point3d34, MathHelper.smethod_57(turnDirection, point3d34, point3d35, point3d2)))
        nominalTrackPolylineArea.method_1(point3d35)
        nominalTrackPolylineArea.method_1(point3d36)
        if self.parametersPanel.rdnDF.isChecked():
            nominalTrackPolylineArea.method_1(point3d_Wpt2)
        # nominalTrackPolylineArea.insert(0, cfWpt1)
        resultPolylineAreList.append(nominalTrackPolylineArea)

        ## WayPoints Tolerances
        wptTolPolylineArea1 = PolylineArea()
        wptTolPolylineArea2 = PolylineArea()
        if turnDirection == TurnDirection.Right:
            pt = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, asw1.Metres)
            wptTolPolylineArea1.method_1(MathHelper.distanceBearingPoint(pt, inboundTrackMinus90, asw1.Metres))


        return complexObstacleArea, resultPolylineAreList
    def InCaseFlyByMethod(self, point3d_Wpt1, point3d_Wpt2, inboundTrack, outboundTrack, rnavGnssTolerance1, rnavGnssTolerance2, turnDirection):
        inboundTrackMinus90 = MathHelper.smethod_4(inboundTrack - math.pi / 2)
        inboundTrackPlus90 = MathHelper.smethod_4(inboundTrack + math.pi / 2)
        inboundTrackPlus180 = MathHelper.smethod_4(inboundTrack + math.pi)
        outboundTrackMinus90 = MathHelper.smethod_4(outboundTrack - math.pi / 2)
        outboundTrackPlus90 = MathHelper.smethod_4(outboundTrack + math.pi / 2)
        outboundTrackPlus180 = MathHelper.smethod_4(outboundTrack + math.pi)
        complexObstacleArea = ComplexObstacleArea()
        asw1 = rnavGnssTolerance1.ASW / 2
        att1 = rnavGnssTolerance1.ATT
        asw2 = rnavGnssTolerance2.ASW / 2
        att2 = rnavGnssTolerance2.ATT
        if not self.parametersPanel.pnlArp.Visible or not self.parametersPanel.pnlArp.IsValid():
            asw2 = asw1


        distFromEnd = 0.0
        if self.parametersPanel.pnlArp.Visible and self.parametersPanel.pnlArp.IsValid():
            distBetweenWPT = MathHelper.calcDistance(self.parametersPanel.pnlArp.Point3d,
                                                 MathHelper.getIntersectionPoint(self.parametersPanel.pnlArp.Point3d, MathHelper.distanceBearingPoint(self.parametersPanel.pnlArp.Point3d, outboundTrack, 100),
                                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100)))
            if distBetweenWPT > Unit.ConvertNMToMeter(30):
                distFromEnd = distBetweenWPT - Unit.ConvertNMToMeter(30)
            elif distBetweenWPT > Unit.ConvertNMToMeter(15):
                distFromEnd = distBetweenWPT - Unit.ConvertNMToMeter(15)
            if distFromEnd > 0.0:
                d = 0.0
                if asw1.Metres > asw2.Metres:
                    d = (asw1.Metres - asw2.Metres) * math.tan(Unit.ConvertDegToRad(60)) * 2
                elif asw1.Metres < asw2.Metres:
                    d = (asw2.Metres - asw1.Metres) * math.tan(Unit.ConvertDegToRad(75)) * 2
                if d == 0.0 or d > distFromEnd:
                    distFromEnd = 0.0
        if not (distFromEnd > 0.0 and asw1.Metres != asw2.Metres):
            asw2 = asw1


        rnavWaypointType1 = self.method_33()
        resultPolylineAreList = []
        turnAngle = MathHelper.smethod_76(Unit.smethod_1(inboundTrack), Unit.smethod_1(outboundTrack), AngleUnits.Degrees)
        turnAngleRad = Unit.ConvertDegToRad(turnAngle)
        joinAngleRad = Unit.ConvertDegToRad(30)
        speedTas = Speed.smethod_0(self.parametersPanel.pnlIas.Value, self.parametersPanel.pnlIsa.Value, self.parametersPanel.pnlAltitude.Value)
        speedWind = self.parametersPanel.pnlWind.Value
        valueBankAngle = self.parametersPanel.pnlBankAngle.Value
        distance = Distance.smethod_0(speedTas, valueBankAngle)
        metres3 = distance.Metres
        distance = RnavWaypoints.getDistanceFromWaypointToEarliestTurningPoint(rnavWaypointType1, Distance(att1.Metres), Distance(metres3), turnAngle, AngleUnits.Degrees)
        distFromWpt1ToEarliest = distance.Metres
        point3dEarliest = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, math.fabs(distFromWpt1ToEarliest)) if (distFromWpt1ToEarliest >= 0) else MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack, math.fabs(distFromWpt1ToEarliest))
        distance = RnavWaypoints.getDistanceFromWaypointToLatestTurningPoint(rnavWaypointType1, speedTas, speedWind, float(self.parametersPanel.pnlPilotTime.Value), float(self.parametersPanel.pnlBankEstTime.Value), Distance(att1.Metres), Distance(metres3), turnAngle, AngleUnits.Degrees)
        distFromWpt1ToLatest = distance.Metres
        point3dLatest = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, math.fabs(distFromWpt1ToLatest)) if (distFromWpt1ToLatest >= 0) else MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack, math.fabs(distFromWpt1ToLatest))
        joinBearing1 = 0.0

        primaryPolylineArea = PolylineArea()
        primaryOutLine = PolylineArea()
        primaryInLine = PolylineArea()
        secondaryPolylineAreaOut = PolylineArea()
        secondaryPolylineAreaIn = PolylineArea()
        if turnAngle <= 90:
            if turnDirection == TurnDirection.Right:
                #### Creating Primary Area


                ptEk = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
                primaryPolylineArea.method_1(ptEk)
                primaryOutLine.method_1(ptEk)

                startPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackMinus90, asw1.Metres)
                windSpiral1 = WindSpiral(startPt1, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                startPt2 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackPlus90, asw1.Metres)
                windSpiral2 = WindSpiral(startPt2, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                pt0 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                pt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackMinus90, asw2.Metres)
                if windSpiral1.method_1(pt0, pt1, False):
                    middlePt11, contactPt11, p = windSpiral1.getContactWithBearingOfTangent(inboundTrack, 0)
                    point3dArray = [startPt1, contactPt11]
                    intersectPolylineArea11 = PolylineArea(point3dArray)
                    intersectPolylineArea11.SetBulgeAt(0, MathHelper.smethod_60(startPt1, middlePt11, contactPt11))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                    primaryPolylineArea.extend(intersectPolylineArea11)
                    primaryOutLine.extend(intersectPolylineArea11)

                    middlePt12, contactPt12, p = windSpiral1.getContactWithBearingOfTangent(outboundTrack, 0)
                    intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                                   contactPt12, MathHelper.distanceBearingPoint(contactPt12, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt1)
                    primaryPolylineArea.method_1(contactPt12)
                    primaryOutLine.method_1(intersectPt1)
                    primaryOutLine.method_1(contactPt12)

                    if windSpiral2.method_1(pt0, pt1, False):
                        bearing = MathHelper.smethod_4(MathHelper.getBearing(windSpiral1.Center[1], windSpiral2.Center[1]) - math.pi / 2)
                        intersectPt2 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], bearing, windSpiral1.Radius[1])
                        contactPt14 = MathHelper.distanceBearingPoint(windSpiral2.Center[1], bearing, windSpiral2.Radius[1])
                        primaryPolylineArea.method_1(intersectPt2)
                        primaryPolylineArea.method_1(contactPt14)
                        primaryOutLine.method_1(intersectPt2)
                        primaryOutLine.method_1(contactPt14)

                        contactPt13 = windSpiral2.method_0(MathHelper.smethod_4(outboundTrack + joinAngleRad), AngleUnits.Radians)
                        primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                        intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 10000),
                                                                   primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))

                        if intersectPt3 == None:
                            contactPt13 = contactPt14
                            intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                                                       primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))
                        else:
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 10000),
                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))


                    else:
                        contactPt13 = windSpiral1.method_0(MathHelper.smethod_4(outboundTrack + joinAngleRad), AngleUnits.Radians)
                        primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                        intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 10000),
                                                                   primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))

                        if intersectPt3 == None:
                            contactPt13 = contactPt12
                            intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                                                       primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))
                        else:
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 10000),
                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))



                    primaryPolylineArea.method_1(contactPt13)
                    primaryOutLine.method_1(contactPt13)
                    primaryPolylineArea.method_1(intersectPt3)
                    primaryOutLine.method_1(intersectPt3)

                    primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)

                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(mergePtPrimary)

                        primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                        primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)
                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)
                        else:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary1)
                        primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

                    else:
                        primaryPolylineArea.method_1(primaryEndPt1)
                        primaryOutLine.method_1(primaryEndPt1)

                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryOutLine.method_1(primaryEndPt1)
                    # primaryPolylineArea.method_1(primaryEndPt2)
                    # primaryInLine.method_1(primaryEndPt2)

                    primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(primaryEndPt2)
                        primaryInLine.method_1(primaryEndPt2)

                        primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)

                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)
                        else:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary2)
                        primaryPolylineArea.method_1(mergePtPrimaryIn)
                        primaryInLine.method_1(mergePtPrimary2)
                        primaryInLine.method_1(mergePtPrimaryIn)
                    else:
                        primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                        primaryInLine.method_1(primaryEndPt2ByAsw1)

                    ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
                    intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100),
                                                                   primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt4)
                    primaryPolylineArea.method_1(ptEk1)
                    primaryInLine.method_1(intersectPt4)
                    primaryInLine.method_1(ptEk1)

                    primaryPolylineArea.method_1(ptEk)
                    resultPolylineAreList.append(primaryPolylineArea)
                    complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))

                    # resultPolylineAreList.append(PolylineArea(windSpiral1.get_Object().asPolyline()))
                    # resultPolylineAreList.append(PolylineArea(windSpiral2.get_Object().asPolyline()))

                    #### SecondaryAreaIn
                    secondaryPolylineAreaIn.extend(primaryInLine)
                    ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackPlus90, asw1.Metres)
                    d = asw1.Metres
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        d = asw2.Metres
                    secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus90, d)
                    secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                                                                             ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100))
                    secondaryPolylineAreaIn.method_1(ptEK11)
                    secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)
                    else:
                        primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                        secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)


                    resultPolylineAreList.append(secondaryPolylineAreaIn)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))

                    #### SecondaryAreaOut
                    secondaryPolylineAreaOut = primaryOutLine.method_23(asw1.Metres, OffsetGapType.Fillet)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                        if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                            secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                        secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                        secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                        secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackPlus90, asw1.Metres))
                    secondaryPolylineAreaOut.reverse()
                    secondaryPolylineAreaOut.extend(primaryOutLine)
                    secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
                    resultPolylineAreList.append(secondaryPolylineAreaOut)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))

                else:
                    middlePt11, contactPt11, p = windSpiral1.getContactWithBearingOfTangent(inboundTrack, 0)
                    point3dArray = [startPt1, contactPt11]
                    intersectPolylineArea11 = PolylineArea(point3dArray)
                    intersectPolylineArea11.SetBulgeAt(0, MathHelper.smethod_60(startPt1, middlePt11, contactPt11))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                    primaryPolylineArea.extend(intersectPolylineArea11)
                    primaryOutLine.extend(intersectPolylineArea11)

                    primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                    pt = MathHelper.getIntersectionPointWithTwoLine(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2)),
                                                                   primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2)))
                    intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                                       primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                    testPt = MathHelper.getIntersectionPoint(intersectPt1, MathHelper.distanceBearingPoint(intersectPt1, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                    if MathHelper.calcDistance(intersectPt1, testPt) < distFromEnd:
                        primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                        intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))

                    primaryPolylineArea.method_1(intersectPt1)
                    primaryOutLine.method_1(intersectPt1)
                    # if pt != None:
                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryOutLine.method_1(primaryEndPt1)
                    # else:
                    #     ptArray, intersectPtList = MathHelper.getPointsLeftWithLine(primaryOutLine, [MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackMinus90, asw1.Metres * 100), primaryEndPt1])
                    #     primaryOutLine = PolylineArea(ptArray)
                    #
                    #     ptArray, intersectPtList = MathHelper.getPointsLeftWithLine(primaryPolylineArea, [MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackMinus90, asw1.Metres * 100), primaryEndPt1])
                    #     primaryPolylineArea = PolylineArea(ptArray)

                    primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)

                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(mergePtPrimary)

                        primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                        primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)
                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)
                        else:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary1)
                        primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

                    else:
                        primaryPolylineArea.method_1(primaryEndPt1)
                        primaryOutLine.method_1(primaryEndPt1)

                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryOutLine.method_1(primaryEndPt1)
                    # primaryPolylineArea.method_1(primaryEndPt2)
                    # primaryInLine.method_1(primaryEndPt2)
                    primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(primaryEndPt2)
                        primaryInLine.method_1(primaryEndPt2)

                        primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)

                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)
                        else:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary2)
                        primaryPolylineArea.method_1(mergePtPrimaryIn)
                        primaryInLine.method_1(mergePtPrimary2)
                        primaryInLine.method_1(mergePtPrimaryIn)
                    else:
                        primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                        primaryInLine.method_1(primaryEndPt2ByAsw1)

                    ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
                    intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100),
                                                                   primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt4)
                    primaryPolylineArea.method_1(ptEk1)
                    primaryInLine.method_1(intersectPt4)
                    primaryInLine.method_1(ptEk1)

                    primaryPolylineArea.method_1(ptEk)
                    resultPolylineAreList.append(primaryPolylineArea)
                    complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))

                    #### SecondaryAreaIn
                    secondaryPolylineAreaIn.extend(primaryInLine)
                    ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackPlus90, asw1.Metres)
                    d = asw1.Metres
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        d = asw2.Metres
                    secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus90, d)
                    secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                                                                             ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100))
                    secondaryPolylineAreaIn.method_1(ptEK11)
                    secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)
                    else:
                        primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                        secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)
                    # secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                    # secondaryPolylineAreaIn.method_1(primaryEndPt2)

                    resultPolylineAreList.append(secondaryPolylineAreaIn)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))

                    #### SecondaryAreaOut
                    secondaryPolylineAreaOut = primaryOutLine.method_23(asw1.Metres, OffsetGapType.Fillet)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        testPt = MathHelper.getIntersectionPoint(intersectPt1, MathHelper.distanceBearingPoint(intersectPt1, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                        if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                            secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                        secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                        secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                        secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackPlus90, asw1.Metres))


                    secondaryPolylineAreaOut.reverse()
                    secondaryPolylineAreaOut.extend(primaryOutLine)
                    secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
                    resultPolylineAreList.append(secondaryPolylineAreaOut)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))
            else:

                #### Creating Primary Area
                ptEk = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
                primaryPolylineArea.method_1(ptEk)
                primaryOutLine.method_1(ptEk)

                startPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackPlus90, asw1.Metres)
                windSpiral1 = WindSpiral(startPt1, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                startPt2 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackMinus90, asw1.Metres)
                windSpiral2 = WindSpiral(startPt2, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                pt0 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                pt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackPlus90, asw2.Metres)
                if windSpiral1.method_1(pt0, pt1, False):
                    p, contactPt11, middlePt11 = windSpiral1.getContactWithBearingOfTangent(inboundTrack, 0)
                    point3dArray = [startPt1, contactPt11]
                    intersectPolylineArea11 = PolylineArea(point3dArray)
                    intersectPolylineArea11.SetBulgeAt(0, MathHelper.smethod_60(startPt1, middlePt11, contactPt11))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                    primaryPolylineArea.extend(intersectPolylineArea11)
                    primaryOutLine.extend(intersectPolylineArea11)

                    p, contactPt12, middlePt12 = windSpiral1.getContactWithBearingOfTangent(outboundTrack, 0)
                    intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                                   contactPt12, MathHelper.distanceBearingPoint(contactPt12, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt1)
                    primaryPolylineArea.method_1(contactPt12)
                    primaryOutLine.method_1(intersectPt1)
                    primaryOutLine.method_1(contactPt12)

                    if windSpiral2.method_1(pt0, pt1, False):
                        bearing = MathHelper.smethod_4(MathHelper.getBearing(windSpiral1.Center[1], windSpiral2.Center[1]) + math.pi / 2)
                        intersectPt2 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], bearing, windSpiral1.Radius[1])
                        contactPt14 = MathHelper.distanceBearingPoint(windSpiral2.Center[1], bearing, windSpiral2.Radius[1])
                        primaryPolylineArea.method_1(intersectPt2)
                        primaryPolylineArea.method_1(contactPt14)
                        primaryOutLine.method_1(intersectPt2)
                        primaryOutLine.method_1(contactPt14)

                        contactPt13 = windSpiral2.method_0(MathHelper.smethod_4(outboundTrack - joinAngleRad), AngleUnits.Radians)
                        primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                        # intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                        #                                            primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                        intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 10000),
                                                                   primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))

                        if intersectPt3 == None:
                            contactPt13 = contactPt14
                            intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                                                       primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))
                        else:
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 10000),
                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))


                    else:
                        contactPt13 = windSpiral1.method_0(MathHelper.smethod_4(outboundTrack - joinAngleRad), AngleUnits.Radians)
                        primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                        # intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                        #                                            primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                        intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 10000),
                                                                   primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))

                        if intersectPt3 == None:
                            contactPt13 = contactPt12
                            intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                                                       primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))
                        else:
                            testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                            if MathHelper.calcDistance(intersectPt1, testPt) < distFromEnd:
                                primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                                intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 10000),
                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) + 3000))




                    primaryPolylineArea.method_1(contactPt13)
                    primaryOutLine.method_1(contactPt13)
                    primaryPolylineArea.method_1(intersectPt3)
                    primaryOutLine.method_1(intersectPt3)

                    primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)

                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(mergePtPrimary)

                        primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                        primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)
                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)
                        else:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary1)
                        primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

                    else:
                        primaryPolylineArea.method_1(primaryEndPt1)
                        primaryOutLine.method_1(primaryEndPt1)

                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryPolylineArea.method_1(primaryEndPt2)
                    # primaryOutLine.method_1(primaryEndPt1)
                    # primaryInLine.method_1(primaryEndPt2)
                    primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(primaryEndPt2)
                        primaryInLine.method_1(primaryEndPt2)

                        primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)

                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)
                        else:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary2)
                        primaryPolylineArea.method_1(mergePtPrimaryIn)
                        primaryInLine.method_1(mergePtPrimary2)
                        primaryInLine.method_1(mergePtPrimaryIn)
                    else:
                        primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                        primaryInLine.method_1(primaryEndPt2ByAsw1)

                    ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
                    intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack + turnAngleRad / 2), 100),
                                                                   primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt4)
                    primaryPolylineArea.method_1(ptEk1)
                    primaryInLine.method_1(intersectPt4)
                    primaryInLine.method_1(ptEk1)

                    primaryPolylineArea.method_1(ptEk)
                    resultPolylineAreList.append(primaryPolylineArea)
                    complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))

                    # resultPolylineAreList.append(PolylineArea(windSpiral1.get_Object().asPolyline()))
                    # resultPolylineAreList.append(PolylineArea(windSpiral2.get_Object().asPolyline()))

                    #### SecondaryAreaIn
                    secondaryPolylineAreaIn.extend(primaryInLine)
                    ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackMinus90, asw1.Metres)
                    d = asw1.Metres
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        d = asw2.Metres
                    secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, d)
                    # secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, asw1.Metres)
                    secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                                                                             ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack + turnAngleRad / 2), 100))
                    secondaryPolylineAreaIn.method_1(ptEK11)
                    secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)
                    else:
                        primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                        secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)
                    # secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                    # secondaryPolylineAreaIn.method_1(primaryEndPt2)

                    resultPolylineAreList.append(secondaryPolylineAreaIn)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))

                    #### SecondaryAreaOut
                    secondaryPolylineAreaOut = primaryOutLine.method_23(-asw1.Metres, OffsetGapType.Fillet)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        secondaryPolylineAreaOut.reverse()
                        testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                        if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                            secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                        secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                        secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                        secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackMinus90, asw1.Metres))
                        ptArray = primaryOutLine.method_14()
                        primaryOutLine = PolylineArea(ptArray)
                        primaryOutLine.reverse()
                    # secondaryPolylineAreaOut.reverse()
                    secondaryPolylineAreaOut.extend(primaryOutLine)
                    secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
                    resultPolylineAreList.append(secondaryPolylineAreaOut)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))
                else:
                    p, contactPt11, middlePt11 = windSpiral1.getContactWithBearingOfTangent(inboundTrack, 0)
                    point3dArray = [startPt1, contactPt11]
                    intersectPolylineArea11 = PolylineArea(point3dArray)
                    intersectPolylineArea11.SetBulgeAt(0, MathHelper.smethod_60(startPt1, middlePt11, contactPt11))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                    primaryPolylineArea.extend(intersectPolylineArea11)
                    primaryOutLine.extend(intersectPolylineArea11)

                    primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                    # intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                    #                                                primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))

                    pt = MathHelper.getIntersectionPointWithTwoLine(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2)),
                                                                   primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2)))
                    intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                                       primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                    testPt = MathHelper.getIntersectionPoint(intersectPt1, MathHelper.distanceBearingPoint(intersectPt1, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                    if testPt != None and MathHelper.calcDistance(intersectPt1, testPt) < distFromEnd:
                        primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                        intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                                       primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))

                    # primaryPolylineArea.method_1(intersectPt1)
                    # primaryOutLine.method_1(intersectPt1)
                    # if pt != None:
                    #     primaryPolylineArea.method_1(primaryEndPt1)
                    #     primaryOutLine.method_1(primaryEndPt1)
                    # else:
                    #     ptArray, intersectPtList = MathHelper.getPointsLeftWithLine(primaryOutLine, [MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackMinus90, asw1.Metres * 5), primaryEndPt1])
                    #     primaryOutLine = PolylineArea(ptArray)
                    #
                    #     ptArray, intersectPtList = MathHelper.getPointsLeftWithLine(primaryPolylineArea, [MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackMinus90, asw1.Metres * 5), primaryEndPt1])
                    #     primaryPolylineArea = PolylineArea(ptArray)

                    primaryPolylineArea.method_1(intersectPt1)
                    primaryOutLine.method_1(intersectPt1)

                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(mergePtPrimary)

                        primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                        primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)
                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)
                        else:
                            mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                            mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary1)
                        primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

                    else:
                        primaryPolylineArea.method_1(primaryEndPt1)
                        primaryOutLine.method_1(primaryEndPt1)
                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryOutLine.method_1(primaryEndPt1)

                    primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                    primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                        mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                        primaryPolylineArea.method_1(primaryEndPt2)
                        primaryInLine.method_1(primaryEndPt2)

                        primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)

                        if asw1.Metres > asw2.Metres:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)
                        else:
                            mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                                       primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                            mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)

                        primaryPolylineArea.method_1(mergePtPrimary2)
                        primaryPolylineArea.method_1(mergePtPrimaryIn)
                        primaryInLine.method_1(mergePtPrimary2)
                        primaryInLine.method_1(mergePtPrimaryIn)
                    else:
                        primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                        primaryInLine.method_1(primaryEndPt2ByAsw1)

                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryPolylineArea.method_1(primaryEndPt2)
                    # primaryOutLine.method_1(primaryEndPt1)
                    # primaryInLine.method_1(primaryEndPt2)

                    ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
                    intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack + turnAngleRad / 2), 100),
                                                                   primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt4)
                    primaryPolylineArea.method_1(ptEk1)
                    primaryInLine.method_1(intersectPt4)
                    primaryInLine.method_1(ptEk1)

                    primaryPolylineArea.method_1(ptEk)
                    resultPolylineAreList.append(primaryPolylineArea)
                    complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))

                    #### SecondaryAreaIn
                    secondaryPolylineAreaIn.extend(primaryInLine)
                    ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackMinus90, asw1.Metres)
                    d = asw1.Metres
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        d = asw2.Metres
                    secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, d)
                    # secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, asw1.Metres)
                    secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                                                                             ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack + turnAngleRad / 2), 100))
                    secondaryPolylineAreaIn.method_1(ptEK11)
                    secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                        secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)
                    else:
                        primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                        secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                        secondaryPolylineAreaIn.method_1(primaryEndPt2)
                    # secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                    # secondaryPolylineAreaIn.method_1(primaryEndPt2)

                    resultPolylineAreList.append(secondaryPolylineAreaIn)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))

                    #### SecondaryAreaOut
                    secondaryPolylineAreaOut = primaryOutLine.method_23(-asw1.Metres, OffsetGapType.Fillet)
                    if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                        secondaryPolylineAreaOut.reverse()
                        testPt = MathHelper.getIntersectionPoint(intersectPt1, MathHelper.distanceBearingPoint(intersectPt1, outboundTrack, 100),
                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                        if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                            secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                        secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                        secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                        secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                        secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackMinus90, asw1.Metres))
                        ptArray = primaryOutLine.method_14()
                        primaryOutLine = PolylineArea(ptArray)
                        primaryOutLine.reverse()
                    # secondaryPolylineAreaOut.reverse()
                    secondaryPolylineAreaOut.extend(primaryOutLine)
                    secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
                    resultPolylineAreList.append(secondaryPolylineAreaOut)
                    complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))
        else:
            if turnDirection == TurnDirection.Right:
                #### Creating Primary Area

                ptEk = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
                primaryPolylineArea.method_1(ptEk)
                primaryOutLine.method_1(ptEk)

                startPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackMinus90, asw1.Metres)
                windSpiral1 = WindSpiral(startPt1, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                startPt2 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackPlus90, asw1.Metres)
                windSpiral2 = WindSpiral(startPt2, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                pt0 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                pt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackMinus90, asw2.Metres)
                # if windSpiral1.method_1(pt0, pt1, False):
                middlePt11, contactPt11, p = windSpiral1.getContactWithBearingOfTangent(inboundTrack, 0)
                point3dArray = [startPt1, contactPt11]
                intersectPolylineArea11 = PolylineArea(point3dArray)
                intersectPolylineArea11.SetBulgeAt(0, MathHelper.smethod_60(startPt1, middlePt11, contactPt11))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                primaryPolylineArea.extend(intersectPolylineArea11)
                primaryOutLine.extend(intersectPolylineArea11)

                middlePt12, contactPt12, p = windSpiral1.getContactWithBearingOfTangent(inboundTrackPlus90, 0)
                intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                               contactPt12, MathHelper.distanceBearingPoint(contactPt12, inboundTrackMinus90, 100))
                primaryPolylineArea.method_1(intersectPt1)
                primaryPolylineArea.method_1(contactPt12)
                primaryOutLine.method_1(intersectPt1)
                primaryOutLine.method_1(contactPt12)

                middlePt14, contactPt14, rightMiddlePt14 = windSpiral2.getContactWithBearingOfTangent(inboundTrackPlus90, 0)
                leftMiddlePt13, contactPt13, p = windSpiral2.getContactWithBearingOfTangent(MathHelper.smethod_4(outboundTrack + joinAngleRad))
                pointArray = [contactPt14, contactPt13]
                tempPolylineArea = PolylineArea(pointArray)
                tempPolylineArea.SetBulgeAt(0, MathHelper.smethod_60(contactPt14, leftMiddlePt13, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                primaryPolylineArea.extend(tempPolylineArea)
                primaryOutLine.extend(tempPolylineArea)

                primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                           point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                pt = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2)),
                                                           primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2)))


                if pt != None:
                    intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                           primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                    testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                    if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                        primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                        intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                           primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))
                    primaryPolylineArea.method_1(intersectPt3)
                    primaryOutLine.method_1(intersectPt3)

                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryOutLine.method_1(primaryEndPt1)
                else:
                    primaryPolylineArea.method_1(intersectPt3)
                    primaryOutLine.method_1(intersectPt3)

                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                    mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                    primaryPolylineArea.method_1(mergePtPrimary)

                    primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                    primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)
                    if asw1.Metres > asw2.Metres:
                        mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                                   primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                        mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)
                    else:
                        mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                                   primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                        mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)

                    primaryPolylineArea.method_1(mergePtPrimary1)
                    primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

                else:
                    primaryPolylineArea.method_1(primaryEndPt1)
                    primaryOutLine.method_1(primaryEndPt1)

                d = asw1.Metres
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    d = asw2.Metres
                primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, d)
                primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                    mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                    primaryPolylineArea.method_1(primaryEndPt2)
                    primaryInLine.method_1(primaryEndPt2)

                    primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)

                    if asw1.Metres > asw2.Metres:
                        mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                                   primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                        mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)
                    else:
                        mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                                   primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                        mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)

                    primaryPolylineArea.method_1(mergePtPrimary2)
                    primaryPolylineArea.method_1(mergePtPrimaryIn)
                    primaryInLine.method_1(mergePtPrimary2)
                    primaryInLine.method_1(mergePtPrimaryIn)
                else:
                    primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                    primaryInLine.method_1(primaryEndPt2ByAsw1)

                # primaryPolylineArea.method_1(primaryEndPt2)
                # primaryInLine.method_1(primaryEndPt2)

                ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
                intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100),
                                                               primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
                primaryPolylineArea.method_1(intersectPt4)
                primaryPolylineArea.method_1(ptEk1)
                primaryInLine.method_1(intersectPt4)
                primaryInLine.method_1(ptEk1)


                primaryPolylineArea.method_1(ptEk)
                resultPolylineAreList.append(primaryPolylineArea)


                # resultPolylineAreList.append(PolylineArea(windSpiral1.get_Object().asPolyline()))
                # resultPolylineAreList.append(PolylineArea(windSpiral2.get_Object().asPolyline()))

                #### SecondaryAreaIn
                secondaryPolylineAreaIn.extend(primaryInLine)
                ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackPlus90, asw1.Metres)
                d = asw1.Metres
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    d = asw2.Metres
                secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus90, d)
                secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                                                                         ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100))
                secondaryPolylineAreaIn.method_1(ptEK11)
                secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                    secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                    secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                    secondaryPolylineAreaIn.method_1(primaryEndPt2)
                else:
                    primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                    secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                    secondaryPolylineAreaIn.method_1(primaryEndPt2)
                # secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                # secondaryPolylineAreaIn.method_1(primaryEndPt2)

                resultPolylineAreList.append(secondaryPolylineAreaIn)

                #### SecondaryAreaOut
                secondaryPolylineAreaOut = primaryOutLine.method_23(asw1.Metres, OffsetGapType.Fillet)
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                    if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                        secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                    secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                    secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                    secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                    secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                    secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackPlus90, asw1.Metres))
                secondaryPolylineAreaOut.reverse()
                secondaryPolylineAreaOut.extend(primaryOutLine)
                secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
                resultPolylineAreList.append(secondaryPolylineAreaOut)

                complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))
                complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))
                complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))

                # else:
                #     middlePt11, contactPt11, p = windSpiral1.getContactWithBearingOfTangent(inboundTrack, 0)
                #     point3dArray = [startPt1, contactPt11]
                #     intersectPolylineArea11 = PolylineArea(point3dArray)
                #     intersectPolylineArea11.SetBulgeAt(0, MathHelper.smethod_60(startPt1, middlePt11, contactPt11))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                #
                #     primaryPolylineArea.extend(intersectPolylineArea11)
                #     primaryOutLine.extend(intersectPolylineArea11)
                #
                #     primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                #     intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                #                                                    primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                #     primaryPolylineArea.method_1(intersectPt1)
                #     primaryOutLine.method_1(intersectPt1)
                #     primaryPolylineArea.method_1(primaryEndPt1)
                #     primaryOutLine.method_1(primaryEndPt1)
                #
                #     primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                #
                #     primaryPolylineArea.method_1(primaryEndPt1)
                #     primaryPolylineArea.method_1(primaryEndPt2)
                #     primaryOutLine.method_1(primaryEndPt1)
                #     primaryInLine.method_1(primaryEndPt2)
                #
                #     ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
                #     intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100),
                #                                                    primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
                #     primaryPolylineArea.method_1(intersectPt4)
                #     primaryPolylineArea.method_1(ptEk1)
                #     primaryInLine.method_1(intersectPt4)
                #     primaryInLine.method_1(ptEk1)
                #
                #     primaryPolylineArea.method_1(ptEk)
                #     resultPolylineAreList.append(primaryPolylineArea)
                #
                #     #### SecondaryAreaIn
                #     secondaryPolylineAreaIn.extend(primaryInLine)
                #     ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackPlus90, asw1.Metres)
                #     2asw1.Metres)
                #     secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                #                                                              ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), 100))
                #     secondaryPolylineAreaIn.method_1(ptEK11)
                #     secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
                #     secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                #     secondaryPolylineAreaIn.method_1(primaryEndPt2)
                #
                #     resultPolylineAreList.append(secondaryPolylineAreaIn)
                #
                #     #### SecondaryAreaOut
                #     secondaryPolylineAreaOut = primaryOutLine.method_23(asw1.Metres, OffsetGapType.Fillet)
                #     secondaryPolylineAreaOut.reverse()
                #     secondaryPolylineAreaOut.extend(primaryOutLine)
                #     secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
                #     resultPolylineAreList.append(secondaryPolylineAreaOut)
            else:
                #### Creating Primary Area

                ptEk = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
                primaryPolylineArea.method_1(ptEk)
                primaryOutLine.method_1(ptEk)

                startPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackPlus90, asw1.Metres)
                windSpiral1 = WindSpiral(startPt1, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                startPt2 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackMinus90, asw1.Metres)
                windSpiral2 = WindSpiral(startPt2, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                pt0 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                pt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackPlus90, asw2.Metres)
                # if windSpiral1.method_1(pt0, pt1, False):
                p, contactPt11, middlePt11 = windSpiral1.getContactWithBearingOfTangent(inboundTrack, 0)
                point3dArray = [startPt1, contactPt11]
                intersectPolylineArea11 = PolylineArea(point3dArray)
                intersectPolylineArea11.SetBulgeAt(0, MathHelper.smethod_60(startPt1, middlePt11, contactPt11))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                primaryPolylineArea.extend(intersectPolylineArea11)
                primaryOutLine.extend(intersectPolylineArea11)

                p, contactPt12, middlePt12 = windSpiral1.getContactWithBearingOfTangent(inboundTrackMinus90, 0)
                intersectPt1 = MathHelper.getIntersectionPoint(contactPt11, MathHelper.distanceBearingPoint(contactPt11, inboundTrack, 100),
                                                               contactPt12, MathHelper.distanceBearingPoint(contactPt12, inboundTrackPlus90, 100))
                primaryPolylineArea.method_1(intersectPt1)
                primaryPolylineArea.method_1(contactPt12)
                primaryOutLine.method_1(intersectPt1)
                primaryOutLine.method_1(contactPt12)

                middlePt14, contactPt14, rightMiddlePt14 = windSpiral2.getContactWithBearingOfTangent(inboundTrackMinus90, 0)
                leftMiddlePt13, contactPt13, p = windSpiral2.getContactWithBearingOfTangent(MathHelper.smethod_4(outboundTrack - joinAngleRad))
                pointArray = [contactPt14, contactPt13]
                tempPolylineArea = PolylineArea(pointArray)
                tempPolylineArea.SetBulgeAt(0, MathHelper.smethod_60(contactPt14, p, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))

                primaryPolylineArea.extend(tempPolylineArea)
                primaryOutLine.extend(tempPolylineArea)

                primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)


                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                           point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, 100))
                pt = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2)),
                                                           primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2)))

                if pt != None:
                    intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                           primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, 100))
                    testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                    if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                        primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                        intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                           primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, 100))

                    primaryPolylineArea.method_1(intersectPt3)
                    primaryOutLine.method_1(intersectPt3)


                    # primaryPolylineArea.method_1(primaryEndPt1)
                    # primaryOutLine.method_1(primaryEndPt1)
                else:
                    primaryPolylineArea.method_1(intersectPt3)
                    primaryOutLine.method_1(intersectPt3)

                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                    mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                    primaryPolylineArea.method_1(mergePtPrimary)

                    primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                    primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)
                    if asw1.Metres > asw2.Metres:
                        mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                                   primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                        mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)
                    else:
                        mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                                   primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                        mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)

                    primaryPolylineArea.method_1(mergePtPrimary1)
                    primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

                else:
                    primaryPolylineArea.method_1(primaryEndPt1)
                    primaryOutLine.method_1(primaryEndPt1)

                d = asw1.Metres
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    d = asw2.Metres
                primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, d)
                primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                    mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                    primaryPolylineArea.method_1(primaryEndPt2)
                    primaryInLine.method_1(primaryEndPt2)

                    primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)

                    if asw1.Metres > asw2.Metres:
                        mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                                   primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                        mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)
                    else:
                        mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                                   primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                        mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)

                    primaryPolylineArea.method_1(mergePtPrimary2)
                    primaryPolylineArea.method_1(mergePtPrimaryIn)
                    primaryInLine.method_1(mergePtPrimary2)
                    primaryInLine.method_1(mergePtPrimaryIn)
                else:
                    primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                    primaryInLine.method_1(primaryEndPt2ByAsw1)

                # primaryPolylineArea.method_1(primaryEndPt2)
                # primaryInLine.method_1(primaryEndPt2)

                ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
                intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack + turnAngleRad / 2), 100),
                                                               primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
                primaryPolylineArea.method_1(intersectPt4)
                primaryPolylineArea.method_1(ptEk1)
                primaryInLine.method_1(intersectPt4)
                primaryInLine.method_1(ptEk1)


                primaryPolylineArea.method_1(ptEk)
                resultPolylineAreList.append(primaryPolylineArea)

                # resultPolylineAreList.append(PolylineArea(windSpiral1.get_Object().asPolyline()))
                # resultPolylineAreList.append(PolylineArea(windSpiral2.get_Object().asPolyline()))

                #### SecondaryAreaIn
                secondaryPolylineAreaIn.extend(primaryInLine)
                ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackMinus90, asw1.Metres)
                d = asw1.Metres
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    d = asw2.Metres
                secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, d)
                # secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, asw1.Metres)
                secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                                                                         ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack + turnAngleRad / 2), 100))
                secondaryPolylineAreaIn.method_1(ptEK11)
                secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                    secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                    secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                    secondaryPolylineAreaIn.method_1(primaryEndPt2)
                else:
                    primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                    secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                    secondaryPolylineAreaIn.method_1(primaryEndPt2)
                # secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                # secondaryPolylineAreaIn.method_1(primaryEndPt2)

                resultPolylineAreList.append(secondaryPolylineAreaIn)

                #### SecondaryAreaOut
                secondaryPolylineAreaOut = primaryOutLine.method_23(-asw1.Metres, OffsetGapType.Fillet)
                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    secondaryPolylineAreaOut.reverse()
                    testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                    if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                        secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                    secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                    secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                    secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                    secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                    secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackMinus90, asw1.Metres))
                    ptArray = primaryOutLine.method_14()
                    primaryOutLine = PolylineArea(ptArray)
                    primaryOutLine.reverse()
                # secondaryPolylineAreaOut.reverse()
                secondaryPolylineAreaOut.extend(primaryOutLine)
                secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
                resultPolylineAreList.append(secondaryPolylineAreaOut)

                complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))
                complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))
                complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))

        nominalTrackPolylineArea = PolylineArea()
        num19 = metres3 * math.tan(Unit.ConvertDegToRad(turnAngle / 2))
        if (self.parametersPanel.chbCatH.Checked):
            metresPerSecond1 = 3 * speedTas.MetresPerSecond
            num = metresPerSecond1
        else:
            metresPerSecond1 = 5 * speedTas.MetresPerSecond
            num = metresPerSecond1
        num = metresPerSecond1

        point3d33 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, num19)
        point3d34 = MathHelper.distanceBearingPoint(point3d33, inboundTrackPlus90, 100)
        point3d35 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrack, num19)
        point3d36 = MathHelper.distanceBearingPoint(point3d35, outboundTrackPlus90, 100)
        point3d2 = MathHelper.getIntersectionPoint(point3d33, point3d34, point3d35, point3d36)
        point3d33 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, num19 + num)
        point3d34 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, num19)
        point3d35 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrack, num19)
        point3d36 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrack, num19 + num)
        nominalTrackPolylineArea.method_1(point3d33)
        nominalTrackPolylineArea.Add(PolylineAreaPoint(point3d34, MathHelper.smethod_57(turnDirection, point3d34, point3d35, point3d2)))
        nominalTrackPolylineArea.method_1(point3d35)
        nominalTrackPolylineArea.method_1(point3d36)
        if self.parametersPanel.rdnDF.isChecked():
            nominalTrackPolylineArea.method_1(point3d_Wpt2)

        resultPolylineAreList.append(nominalTrackPolylineArea)

        ## WayPoints Tolerances
        wptTolPolylineArea1 = PolylineArea()
        wptTolPolylineArea2 = PolylineArea()
        if turnDirection == TurnDirection.Right:
            pt = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, asw1.Metres)
            wptTolPolylineArea1.method_1(MathHelper.distanceBearingPoint(pt, inboundTrackMinus90, asw1.Metres))


        return complexObstacleArea, resultPolylineAreList

    def flyOverTurnAllowedWithTF_method(self, point3d_Wpt1, point3d_Wpt2, inboundTrack, outboundTrack, rnavGnssTolerance1, rnavGnssTolerance2, turnDirection):
        inboundTrackMinus90 = MathHelper.smethod_4(inboundTrack - math.pi / 2)
        inboundTrackPlus90 = MathHelper.smethod_4(inboundTrack + math.pi / 2)
        inboundTrackPlus180 = MathHelper.smethod_4(inboundTrack + math.pi)
        outboundTrackMinus90 = MathHelper.smethod_4(outboundTrack - math.pi / 2)
        outboundTrackPlus90 = MathHelper.smethod_4(outboundTrack + math.pi / 2)
        outboundTrackPlus180 = MathHelper.smethod_4(outboundTrack + math.pi)
        complexObstacleArea = ComplexObstacleArea()
        asw1 = rnavGnssTolerance1.ASW / 2
        att1 = rnavGnssTolerance1.ATT
        asw2 = rnavGnssTolerance2.ASW / 2
        att2 = rnavGnssTolerance2.ATT
        if not self.parametersPanel.pnlArp.Visible or not self.parametersPanel.pnlArp.IsValid():
            asw2 = asw1


        distFromEnd = 0.0
        if self.parametersPanel.pnlArp.Visible and self.parametersPanel.pnlArp.IsValid():
            distBetweenWPT = MathHelper.calcDistance(self.parametersPanel.pnlArp.Point3d,
                                                 MathHelper.getIntersectionPoint(self.parametersPanel.pnlArp.Point3d, MathHelper.distanceBearingPoint(self.parametersPanel.pnlArp.Point3d, outboundTrack, 100),
                                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100)))
            if distBetweenWPT > Unit.ConvertNMToMeter(30):
                distFromEnd = distBetweenWPT - Unit.ConvertNMToMeter(30)
            elif distBetweenWPT > Unit.ConvertNMToMeter(15):
                distFromEnd = distBetweenWPT - Unit.ConvertNMToMeter(15)
            if distFromEnd > 0.0:
                d = 0.0
                if asw1.Metres > asw2.Metres:
                    d = (asw1.Metres - asw2.Metres) * math.tan(Unit.ConvertDegToRad(60)) * 2
                elif asw1.Metres < asw2.Metres:
                    d = (asw2.Metres - asw1.Metres) * math.tan(Unit.ConvertDegToRad(75)) * 2
                if d == 0.0 or d > distFromEnd:
                    distFromEnd = 0.0

        if not (distFromEnd > 0.0 and asw1.Metres != asw2.Metres):
            asw2 = asw1


        rnavWaypointType1 = self.method_33()
        resultPolylineAreList = []
        turnAngle = MathHelper.smethod_76(Unit.smethod_1(inboundTrack), Unit.smethod_1(outboundTrack), AngleUnits.Degrees)
        turnAngleRad = Unit.ConvertDegToRad(turnAngle)
        joinAngleRad = Unit.ConvertDegToRad(30)
        speedTas = Speed.smethod_0(self.parametersPanel.pnlIas.Value, self.parametersPanel.pnlIsa.Value, self.parametersPanel.pnlAltitude.Value)
        speedWind = self.parametersPanel.pnlWind.Value
        valueBankAngle = self.parametersPanel.pnlBankAngle.Value
        distance = Distance.smethod_0(speedTas, valueBankAngle)
        metres3 = distance.Metres
        distance = RnavWaypoints.getDistanceFromWaypointToEarliestTurningPoint(rnavWaypointType1, Distance(att1.Metres), Distance(metres3), turnAngle, AngleUnits.Degrees)
        distFromWpt1ToEarliest = distance.Metres
        point3dEarliest = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, math.fabs(distFromWpt1ToEarliest)) if (distFromWpt1ToEarliest >= 0) else MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack, math.fabs(distFromWpt1ToEarliest))
        distance = RnavWaypoints.getDistanceFromWaypointToLatestTurningPoint(rnavWaypointType1, speedTas, speedWind, float(self.parametersPanel.pnlPilotTime.Value), float(self.parametersPanel.pnlBankEstTime.Value), Distance(att1.Metres), Distance(metres3), turnAngle, AngleUnits.Degrees)
        distFromWpt1ToLatest = distance.Metres
        point3dLatest = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, math.fabs(distFromWpt1ToLatest)) if (distFromWpt1ToLatest >= 0) else MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack, math.fabs(distFromWpt1ToLatest))
        joinBearing1 = 0.0

        primaryPolylineArea = PolylineArea()
        primaryOutLine = PolylineArea()
        primaryInLine = PolylineArea()
        secondaryPolylineAreaOut = PolylineArea()
        secondaryPolylineAreaIn = PolylineArea()

        if turnDirection == TurnDirection.Right:
            #### Creating Primary Area
            ptEk = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
            primaryPolylineArea.method_1(ptEk)
            primaryOutLine.method_1(ptEk)

            startPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackMinus90, asw1.Metres)
            windSpiral1 = WindSpiral(startPt1, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
            pt0 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
            pt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackMinus90, asw2.Metres)
            # if windSpiral1.method_1(pt0, pt1, False):
            leftMiddlePt13, contactPt13, rightMiddlePt13 = windSpiral1.getContactWithBearingOfTangent(MathHelper.smethod_4(outboundTrack + joinAngleRad))
            intersectPolylineArea13 = PolylineArea()
            if round(windSpiral1.Radius[0], 2) == round(MathHelper.calcDistance(windSpiral1.Center[0], contactPt13), 2):
                point3dArray = [startPt1, contactPt13]
                intersectPolylineArea13 = PolylineArea(point3dArray)
                intersectPolylineArea13.SetBulgeAt(0, MathHelper.smethod_60(startPt1, leftMiddlePt13, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))
            elif round(windSpiral1.Radius[1], 2) == round(MathHelper.calcDistance(windSpiral1.Center[1], contactPt13), 2):
                point3dArray = [startPt1, windSpiral1.Finish[0], contactPt13]
                intersectPolylineArea13 = PolylineArea(point3dArray)
                intersectPolylineArea13.SetBulgeAt(0, MathHelper.smethod_60(startPt1, windSpiral1.Middle[0], windSpiral1.Finish[0]))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                intersectPolylineArea13.SetBulgeAt(1, MathHelper.smethod_60(windSpiral1.Finish[0], leftMiddlePt13, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))
            else:
                point3dArray = [startPt1, windSpiral1.Finish[0], windSpiral1.Finish[1],contactPt13]
                intersectPolylineArea13 = PolylineArea(point3dArray)
                intersectPolylineArea13.SetBulgeAt(0, MathHelper.smethod_60(startPt1, windSpiral1.Middle[0], windSpiral1.Finish[0]))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                intersectPolylineArea13.SetBulgeAt(1, MathHelper.smethod_60(windSpiral1.Finish[0], windSpiral1.Middle[1], windSpiral1.Finish[1]))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                intersectPolylineArea13.SetBulgeAt(2, MathHelper.smethod_60(windSpiral1.Finish[1], leftMiddlePt13, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))


            primaryPolylineArea.extend(intersectPolylineArea13)
            primaryOutLine.extend(intersectPolylineArea13)

            primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
            # testPt0 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackMinus90, asw2.Metres)
            testPt1 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                      primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))

            if testPt1 == None:
                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                      point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))

                primaryPolylineArea.method_1(intersectPt3)
                primaryOutLine.method_1(intersectPt3)
            else:
                intersectPt3 = testPt1
                testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                    primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                    intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                      primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))

                primaryPolylineArea.method_1(intersectPt3)
                primaryOutLine.method_1(intersectPt3)

                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                    mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                    primaryPolylineArea.method_1(mergePtPrimary)

                    primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                    primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)
                    if asw1.Metres > asw2.Metres:
                        mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                                   primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                        mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)
                    else:
                        mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                                   primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                        mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)

                    primaryPolylineArea.method_1(mergePtPrimary1)
                    primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

                else:
                    primaryPolylineArea.method_1(primaryEndPt1)
                    primaryOutLine.method_1(primaryEndPt1)
            d = asw1.Metres
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                d = asw2.Metres
            primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, d)
            primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                primaryPolylineArea.method_1(primaryEndPt2)
                primaryInLine.method_1(primaryEndPt2)

                primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)

                if asw1.Metres > asw2.Metres:
                    mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                               primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                    mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)
                else:
                    mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                               primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                    mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)

                primaryPolylineArea.method_1(mergePtPrimary2)
                primaryPolylineArea.method_1(mergePtPrimaryIn)
                primaryInLine.method_1(mergePtPrimary2)
                primaryInLine.method_1(mergePtPrimaryIn)
            else:
                primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                primaryInLine.method_1(primaryEndPt2ByAsw1)

            ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
            ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackPlus90, asw1.Metres)
            intersectPt4 = MathHelper.getIntersectionPointWithTwoLine(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                           primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))
            if intersectPt4 == None:
                intersectPt4 = MathHelper.getIntersectionPoint(primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100),
                                                                     ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack + joinAngleRad / 2), 100))
                primaryPolylineArea.method_1(intersectPt4)
                primaryInLine.method_1(intersectPt4)
                primaryPolylineArea.method_1(ptEK11)
                primaryInLine.method_1(ptEK11)
                # intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, inboundTrackPlus90, 100),
                #                                                         primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
            else:
                primaryPolylineArea.method_1(intersectPt4)
                primaryInLine.method_1(intersectPt4)
                primaryPolylineArea.method_1(ptEk1)
                primaryInLine.method_1(ptEk1)

            primaryPolylineArea.method_1(ptEk)
            primaryInLine.method_1(ptEk)
            resultPolylineAreList.append(primaryPolylineArea)

            #### SecondaryAreaIn
            secondaryPolylineAreaIn.extend(primaryInLine)
            d = asw1.Metres
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                d = asw2.Metres
            # secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus90, d)
            secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus90, d)
            secondaryInIntersectPt = MathHelper.getIntersectionPointWithTwoLine(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                                     ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack + joinAngleRad / 2), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))
            if secondaryInIntersectPt == None:
                if turnAngle > 90:
                    secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus90, 100),
                                                                                    ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack + joinAngleRad / 2), 100))

                else:
                    secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                                                                                    ptEK11, MathHelper.distanceBearingPoint(ptEK11, inboundTrackPlus90, 100))
            secondaryPolylineAreaIn.method_1(ptEK11)
            secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                secondaryPolylineAreaIn.method_1(primaryEndPt2)
            else:
                primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                secondaryPolylineAreaIn.method_1(primaryEndPt2)


            resultPolylineAreList.append(secondaryPolylineAreaIn)

            #### SecondaryAreaOut
            secondaryPolylineAreaOut = primaryOutLine.method_23(asw1.Metres, OffsetGapType.Fillet)
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                         point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                    secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackPlus90, asw1.Metres))


            secondaryPolylineAreaOut.reverse()
            secondaryPolylineAreaOut.extend(primaryOutLine)
            secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
            resultPolylineAreList.append(secondaryPolylineAreaOut)

            complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))
            complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))
            complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))

        else:
            #### Creating Primary Area
            ptEk = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
            primaryPolylineArea.method_1(ptEk)
            primaryOutLine.method_1(ptEk)

            startPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackPlus90, asw1.Metres)
            windSpiral1 = WindSpiral(startPt1, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
            pt0 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
            pt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackPlus90, asw2.Metres)
            # if windSpiral1.method_1(pt0, pt1, False):
            leftMiddlePt13, contactPt13, rightMiddlePt13 = windSpiral1.getContactWithBearingOfTangent(MathHelper.smethod_4(outboundTrack - joinAngleRad))
            intersectPolylineArea13 = PolylineArea()
            if round(windSpiral1.Radius[0], 2) == round(MathHelper.calcDistance(windSpiral1.Center[0], contactPt13), 2):
                point3dArray = [startPt1, contactPt13]
                intersectPolylineArea13 = PolylineArea(point3dArray)
                intersectPolylineArea13.SetBulgeAt(0, MathHelper.smethod_60(startPt1, rightMiddlePt13, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))
            elif round(windSpiral1.Radius[1], 2) == round(MathHelper.calcDistance(windSpiral1.Center[1], contactPt13), 2):
                point3dArray = [startPt1, windSpiral1.Finish[0], contactPt13]
                intersectPolylineArea13 = PolylineArea(point3dArray)
                intersectPolylineArea13.SetBulgeAt(0, MathHelper.smethod_60(startPt1, windSpiral1.Middle[0], windSpiral1.Finish[0]))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                intersectPolylineArea13.SetBulgeAt(1, MathHelper.smethod_60(windSpiral1.Finish[0], rightMiddlePt13, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))
            else:
                point3dArray = [startPt1, windSpiral1.Finish[0], windSpiral1.Finish[1],contactPt13]
                intersectPolylineArea13 = PolylineArea(point3dArray)
                intersectPolylineArea13.SetBulgeAt(0, MathHelper.smethod_60(startPt1, windSpiral1.Middle[0], windSpiral1.Finish[0]))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                intersectPolylineArea13.SetBulgeAt(1, MathHelper.smethod_60(windSpiral1.Finish[0], windSpiral1.Middle[1], windSpiral1.Finish[1]))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                intersectPolylineArea13.SetBulgeAt(2, MathHelper.smethod_60(windSpiral1.Finish[1], rightMiddlePt13, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))


            primaryPolylineArea.extend(intersectPolylineArea13)
            primaryOutLine.extend(intersectPolylineArea13)

            primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
            # testPt0 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackPlus90, asw2.Metres)
            testPt1 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                      primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))
            if testPt1 == None:
                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                      point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, 100))
                primaryPolylineArea.method_1(intersectPt3)
                primaryOutLine.method_1(intersectPt3)
            else:
                intersectPt3 = testPt1
                testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                    primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                    intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                      primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))

                primaryPolylineArea.method_1(intersectPt3)
                primaryOutLine.method_1(intersectPt3)

            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                primaryPolylineArea.method_1(mergePtPrimary)

                primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)
                if asw1.Metres > asw2.Metres:
                    mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                               primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                    mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)
                else:
                    mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                               primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                    mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)

                primaryPolylineArea.method_1(mergePtPrimary1)
                primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

            else:
                primaryPolylineArea.method_1(primaryEndPt1)
                primaryOutLine.method_1(primaryEndPt1)

                # primaryPolylineArea.method_1(primaryEndPt1)
                # primaryOutLine.method_1(primaryEndPt1)
            d = asw1.Metres
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                d = asw2.Metres
            primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, d)
            primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                primaryPolylineArea.method_1(primaryEndPt2)
                primaryInLine.method_1(primaryEndPt2)

                primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)

                if asw1.Metres > asw2.Metres:
                    mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                               primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                    mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)
                else:
                    mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                               primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                    mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)

                primaryPolylineArea.method_1(mergePtPrimary2)
                primaryPolylineArea.method_1(mergePtPrimaryIn)
                primaryInLine.method_1(mergePtPrimary2)
                primaryInLine.method_1(mergePtPrimaryIn)
            else:
                primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                primaryInLine.method_1(primaryEndPt2ByAsw1)

            # primaryPolylineArea.method_1(primaryEndPt2)
            # primaryInLine.method_1(primaryEndPt2)

            ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
            ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackMinus90, asw1.Metres)
            intersectPt4 = MathHelper.getIntersectionPointWithTwoLine(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack + turnAngleRad / 2), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                           primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))
            if intersectPt4 == None:
                intersectPt4 = MathHelper.getIntersectionPoint(primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100),
                                                                     ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack - joinAngleRad / 2), 100))
                primaryPolylineArea.method_1(intersectPt4)
                primaryInLine.method_1(intersectPt4)
                primaryPolylineArea.method_1(ptEK11)
                primaryInLine.method_1(ptEK11)
                # intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, inboundTrackMinus90, 100),
                #                                                         primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
            else:
                primaryPolylineArea.method_1(intersectPt4)
                primaryInLine.method_1(intersectPt4)
                primaryPolylineArea.method_1(ptEk1)
                primaryInLine.method_1(ptEk1)

            primaryPolylineArea.method_1(ptEk)
            primaryInLine.method_1(ptEk)
            resultPolylineAreList.append(primaryPolylineArea)

            #### SecondaryAreaIn
            secondaryPolylineAreaIn.extend(primaryInLine)
            d = asw1.Metres
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                d = asw2.Metres
            secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, d)
            secondaryInIntersectPt = MathHelper.getIntersectionPointWithTwoLine(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                                     ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack - joinAngleRad / 2), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))
            if secondaryInIntersectPt == None:
                if turnAngle > 90:
                    secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackMinus90, 100),
                                                                                    ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack - joinAngleRad / 2), 100))
                else:
                    secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                                                                                    ptEK11, MathHelper.distanceBearingPoint(ptEK11, inboundTrackMinus90, 100))
            secondaryPolylineAreaIn.method_1(ptEK11)
            secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                secondaryPolylineAreaIn.method_1(primaryEndPt2)
            else:
                primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                secondaryPolylineAreaIn.method_1(primaryEndPt2)
            # secondaryPolylineAreaIn.method_1(secondaryInEndPt)
            # secondaryPolylineAreaIn.method_1(primaryEndPt2)

            resultPolylineAreList.append(secondaryPolylineAreaIn)

            #### SecondaryAreaOut
            secondaryPolylineAreaOut = primaryOutLine.method_23(-asw1.Metres, OffsetGapType.Fillet)
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                secondaryPolylineAreaOut.reverse()
                testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                         point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                    secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackMinus90, asw1.Metres))
                ptArray = primaryOutLine.method_14()
                primaryOutLine = PolylineArea(ptArray)
                primaryOutLine.reverse()
            secondaryPolylineAreaOut.extend(primaryOutLine)
            secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
            resultPolylineAreList.append(secondaryPolylineAreaOut)

            complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))
            complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))
            complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))

        nominalTrackPolylineArea = PolylineArea()
        num14 = 0.6 * turnAngle if (turnAngle < 50) else 30
        if (turnAngle < 50):
            num3 = 90 - num14
            num1 = num3
        else:
            num3 = 60
        num1 = num3
        distance = Distance.smethod_0(speedTas, 15)
        metres6 = distance.Metres
        num15 = metres3 * math.sin(Unit.ConvertDegToRad(turnAngle))
        num16 = metres3 * math.cos(Unit.ConvertDegToRad(turnAngle)) * math.tan(Unit.ConvertDegToRad(num14))
        num17 = metres3 * ((1 - math.cos(Unit.ConvertDegToRad(turnAngle)) / math.cos(Unit.ConvertDegToRad(num14))) / math.sin(Unit.ConvertDegToRad(num14)))
        num18 = metres6 * math.tan(Unit.ConvertDegToRad(num14 / 2))
        if (self.parametersPanel.chbCatH.Checked):
            metresPerSecond = 5 * speedTas.MetresPerSecond
        else:
            metresPerSecond = 10 * speedTas.MetresPerSecond
            num2 = metresPerSecond
        num2 = metresPerSecond
        point3d31 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrack, num15 + num16 + num17 + num18)
        if (turnDirection != TurnDirection.Left):
            point3d3 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack + Unit.ConvertDegToRad(90), metres3)
            point3d5 = MathHelper.distanceBearingPoint(point3d3, outboundTrack - Unit.ConvertDegToRad(num1), metres3)
            point3d4 = MathHelper.distanceBearingPoint(point3d31, outboundTrack - Unit.ConvertDegToRad(90), metres6)
            point3d6 = MathHelper.distanceBearingPoint(point3d4, MathHelper.getBearing(point3d4, point3d31) + Unit.ConvertDegToRad(num14), metres6)
        else:
            point3d3 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack - Unit.ConvertDegToRad(90), metres3)
            point3d5 = MathHelper.distanceBearingPoint(point3d3, outboundTrack + Unit.ConvertDegToRad(num1), metres3)
            point3d4 = MathHelper.distanceBearingPoint(point3d31, outboundTrack + Unit.ConvertDegToRad(90), metres6)
            point3d6 = MathHelper.distanceBearingPoint(point3d4, MathHelper.getBearing(point3d4, point3d31) - Unit.ConvertDegToRad(num14), metres6)
        # point3d32 = MathHelper.distanceBearingPoint(point3d31, outboundTrack, num2)
        nominalTrackPolylineArea.Add(PolylineAreaPoint(point3d_Wpt1, MathHelper.smethod_57(turnDirection, point3d_Wpt1, point3d5, point3d3)))
        nominalTrackPolylineArea.method_1(point3d5)
        if (turnDirection == TurnDirection.Left):
            nominalTrackPolylineArea.Add(PolylineAreaPoint(point3d6, MathHelper.smethod_57(TurnDirection.Right, point3d6, point3d31, point3d4)))
        elif (turnDirection != TurnDirection.Right):
            nominalTrackPolylineArea.method_1(point3d6)
        else:
            nominalTrackPolylineArea.Add(PolylineAreaPoint(point3d6, MathHelper.smethod_57(TurnDirection.Left, point3d6, point3d31, point3d4)))
        nominalTrackPolylineArea.method_1(point3d31)
        if (turnDirection == TurnDirection.Left):
            bearing = outboundTrackPlus90
        else:
            bearing = outboundTrackMinus90
        if MathHelper.getIntersectionPointBetweenPolylineArea(nominalTrackPolylineArea, PolylineArea([point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, bearing, 10000)])) == None:
            nominalTrackPolylineArea.method_1(point3d_Wpt2)
        resultPolylineAreList.append(nominalTrackPolylineArea)


        return complexObstacleArea, resultPolylineAreList

    def flyOverTurnAllowedWithCF_method(self, point3d_Wpt1, point3d_Wpt2, inboundTrack, outboundTrack, rnavGnssTolerance1, rnavGnssTolerance2, turnDirection):
        inboundTrackMinus90 = MathHelper.smethod_4(inboundTrack - math.pi / 2)
        inboundTrackPlus90 = MathHelper.smethod_4(inboundTrack + math.pi / 2)
        inboundTrackPlus180 = MathHelper.smethod_4(inboundTrack + math.pi)
        outboundTrackMinus90 = MathHelper.smethod_4(outboundTrack - math.pi / 2)
        outboundTrackPlus90 = MathHelper.smethod_4(outboundTrack + math.pi / 2)
        outboundTrackPlus180 = MathHelper.smethod_4(outboundTrack + math.pi)
        complexObstacleArea = ComplexObstacleArea()
        asw1 = rnavGnssTolerance1.ASW / 2
        att1 = rnavGnssTolerance1.ATT
        asw2 = rnavGnssTolerance2.ASW / 2
        att2 = rnavGnssTolerance2.ATT
        if not self.parametersPanel.pnlArp.Visible or not self.parametersPanel.pnlArp.IsValid():
            asw2 = asw1

        cfWpt1 = point3d_Wpt1
        point3d_Wpt1 = MathHelper.getIntersectionPoint(point3d_Wpt1, MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack, 100),
                                                       point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus180, 100))

        distFromEnd = 0.0
        if self.parametersPanel.pnlArp.Visible and self.parametersPanel.pnlArp.IsValid():
            distBetweenWPT = MathHelper.calcDistance(self.parametersPanel.pnlArp.Point3d,
                                                 MathHelper.getIntersectionPoint(self.parametersPanel.pnlArp.Point3d, MathHelper.distanceBearingPoint(self.parametersPanel.pnlArp.Point3d, outboundTrack, 100),
                                                                                 point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100)))

            if distBetweenWPT > Unit.ConvertNMToMeter(30):
                distFromEnd = distBetweenWPT - Unit.ConvertNMToMeter(30)
            elif distBetweenWPT > Unit.ConvertNMToMeter(15):
                distFromEnd = distBetweenWPT - Unit.ConvertNMToMeter(15)
            if distFromEnd > 0.0:
                d = 0.0
                if asw1.Metres > asw2.Metres:
                    d = (asw1.Metres - asw2.Metres) * math.tan(Unit.ConvertDegToRad(60)) * 2
                elif asw1.Metres < asw2.Metres:
                    d = (asw2.Metres - asw1.Metres) * math.tan(Unit.ConvertDegToRad(75)) * 2
                if d == 0.0 or d > distFromEnd:
                    distFromEnd = 0.0
        if not (distFromEnd > 0.0 and asw1.Metres != asw2.Metres):
            asw2 = asw1

        turnAngleCF = MathHelper.smethod_76(Unit.smethod_1(inboundTrack), Unit.smethod_1(MathHelper.getBearing(cfWpt1, point3d_Wpt2)), AngleUnits.Degrees)
        turnAngle = MathHelper.smethod_76(Unit.smethod_1(inboundTrack), Unit.smethod_1(outboundTrack), AngleUnits.Degrees)
        if turnAngle < turnAngleCF:
            point3d_Wpt1 = cfWpt1

        rnavWaypointType1 = self.method_33()
        resultPolylineAreList = []

        turnAngleRad = Unit.ConvertDegToRad(turnAngle)
        joinAngleRad = Unit.ConvertDegToRad(30)
        speedTas = Speed.smethod_0(self.parametersPanel.pnlIas.Value, self.parametersPanel.pnlIsa.Value, self.parametersPanel.pnlAltitude.Value)
        speedWind = self.parametersPanel.pnlWind.Value
        valueBankAngle = self.parametersPanel.pnlBankAngle.Value
        distance = Distance.smethod_0(speedTas, valueBankAngle)
        metres3 = distance.Metres
        distance = RnavWaypoints.getDistanceFromWaypointToEarliestTurningPoint(rnavWaypointType1, Distance(att1.Metres), Distance(metres3), turnAngle, AngleUnits.Degrees)
        distFromWpt1ToEarliest = distance.Metres
        point3dEarliest = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, math.fabs(distFromWpt1ToEarliest)) if (distFromWpt1ToEarliest >= 0) else MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack, math.fabs(distFromWpt1ToEarliest))
        distance = RnavWaypoints.getDistanceFromWaypointToLatestTurningPoint(rnavWaypointType1, speedTas, speedWind, float(self.parametersPanel.pnlPilotTime.Value), float(self.parametersPanel.pnlBankEstTime.Value), Distance(att1.Metres), Distance(metres3), turnAngle, AngleUnits.Degrees)
        distFromWpt1ToLatest = distance.Metres
        point3dLatest = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, math.fabs(distFromWpt1ToLatest)) if (distFromWpt1ToLatest >= 0) else MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack, math.fabs(distFromWpt1ToLatest))
        joinBearing1 = 0.0

        primaryPolylineArea = PolylineArea()
        primaryOutLine = PolylineArea()
        primaryInLine = PolylineArea()
        secondaryPolylineAreaOut = PolylineArea()
        secondaryPolylineAreaIn = PolylineArea()

        if turnDirection == TurnDirection.Right:
            #### Creating Primary Area
            # cfStartPt = MathHelper.distanceBearingPoint(cfWpt1, inboundTrackMinus90, asw1.Metres)
            # primaryPolylineArea.method_1(cfStartPt)
            # primaryOutLine.method_1(cfStartPt)

            ptEk = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
            primaryPolylineArea.method_1(ptEk)
            primaryOutLine.method_1(ptEk)

            startPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackMinus90, asw1.Metres)
            windSpiral1 = WindSpiral(startPt1, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
            pt0 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
            pt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackMinus90, asw2.Metres)
            # if windSpiral1.method_1(pt0, pt1, False):
            leftMiddlePt13, contactPt13, rightMiddlePt13 = windSpiral1.getContactWithBearingOfTangent(MathHelper.smethod_4(outboundTrack + joinAngleRad))
            intersectPolylineArea13 = PolylineArea()
            if round(windSpiral1.Radius[0], 2) == round(MathHelper.calcDistance(windSpiral1.Center[0], contactPt13), 2):
                point3dArray = [startPt1, contactPt13]
                intersectPolylineArea13 = PolylineArea(point3dArray)
                intersectPolylineArea13.SetBulgeAt(0, MathHelper.smethod_60(startPt1, leftMiddlePt13, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))
            elif round(windSpiral1.Radius[1], 2) == round(MathHelper.calcDistance(windSpiral1.Center[1], contactPt13), 2):
                point3dArray = [startPt1, windSpiral1.Finish[0], contactPt13]
                intersectPolylineArea13 = PolylineArea(point3dArray)
                intersectPolylineArea13.SetBulgeAt(0, MathHelper.smethod_60(startPt1, windSpiral1.Middle[0], windSpiral1.Finish[0]))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                intersectPolylineArea13.SetBulgeAt(1, MathHelper.smethod_60(windSpiral1.Finish[0], leftMiddlePt13, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))
            else:
                point3dArray = [startPt1, windSpiral1.Finish[0], windSpiral1.Finish[1],contactPt13]
                intersectPolylineArea13 = PolylineArea(point3dArray)
                intersectPolylineArea13.SetBulgeAt(0, MathHelper.smethod_60(startPt1, windSpiral1.Middle[0], windSpiral1.Finish[0]))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                intersectPolylineArea13.SetBulgeAt(1, MathHelper.smethod_60(windSpiral1.Finish[0], windSpiral1.Middle[1], windSpiral1.Finish[1]))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                intersectPolylineArea13.SetBulgeAt(2, MathHelper.smethod_60(windSpiral1.Finish[1], leftMiddlePt13, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))


            primaryPolylineArea.extend(intersectPolylineArea13)
            primaryOutLine.extend(intersectPolylineArea13)

            primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
            testPt0 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackMinus90, asw2.Metres)
            testPt1 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                      primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))
            if testPt1 == None:
                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), 100),
                                                      point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                primaryPolylineArea.method_1(intersectPt3)
                primaryOutLine.method_1(intersectPt3)
            else:
                intersectPt3 = testPt1
                testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                    primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                    intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack + joinAngleRad), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                      primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))

                primaryPolylineArea.method_1(intersectPt3)
                primaryOutLine.method_1(intersectPt3)

                if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                    mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                    mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                    primaryPolylineArea.method_1(mergePtPrimary)

                    primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                    primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)
                    if asw1.Metres > asw2.Metres:
                        mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                                   primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                        mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)
                    else:
                        mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                                   primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                        mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackPlus90, asw2.Metres)

                    primaryPolylineArea.method_1(mergePtPrimary1)
                    primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

                else:
                    primaryPolylineArea.method_1(primaryEndPt1)
                    primaryOutLine.method_1(primaryEndPt1)
                # primaryPolylineArea.method_1(primaryEndPt1)
                # primaryOutLine.method_1(primaryEndPt1)
            d = asw1.Metres
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                d = asw2.Metres
            primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, d)

            primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                primaryPolylineArea.method_1(primaryEndPt2)
                primaryInLine.method_1(primaryEndPt2)

                primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)

                if asw1.Metres > asw2.Metres:
                    mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                               primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                    mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)
                else:
                    mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                               primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                    mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackMinus90, asw2.Metres)

                primaryPolylineArea.method_1(mergePtPrimary2)
                primaryPolylineArea.method_1(mergePtPrimaryIn)
                primaryInLine.method_1(mergePtPrimary2)
                primaryInLine.method_1(mergePtPrimaryIn)
            else:
                primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                primaryInLine.method_1(primaryEndPt2ByAsw1)

            ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
            ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackPlus90, asw1.Metres)
            intersectPt4 = MathHelper.getIntersectionPointWithTwoLine(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack - turnAngleRad / 2), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                           primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))
            if intersectPt4 == None:
                intersectPt4 = MathHelper.getIntersectionPoint(primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100),
                                                                     ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack + joinAngleRad / 2), 100))
                primaryPolylineArea.method_1(intersectPt4)
                primaryInLine.method_1(intersectPt4)
                primaryPolylineArea.method_1(ptEK11)
                primaryInLine.method_1(ptEK11)
                # intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, inboundTrackPlus90, 100),
                #                                                         primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
            else:
                primaryPolylineArea.method_1(intersectPt4)
                primaryInLine.method_1(intersectPt4)
                primaryPolylineArea.method_1(ptEk1)
                primaryInLine.method_1(ptEk1)

            # cfendPt = MathHelper.distanceBearingPoint(cfWpt1, inboundTrackPlus90, asw1.Metres)
            # primaryPolylineArea.method_1(cfendPt)
            # primaryInLine.method_1(cfendPt)
            #
            primaryPolylineArea.method_1(ptEk)
            resultPolylineAreList.append(primaryPolylineArea)

            #### SecondaryAreaIn
            secondaryPolylineAreaIn.extend(primaryInLine)
            d = asw1.Metres
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                d = asw2.Metres
            secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus90, d)
            secondaryInIntersectPt = MathHelper.getIntersectionPointWithTwoLine(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                                     ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack + joinAngleRad / 2), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))
            if secondaryInIntersectPt == None:
                # if turnAngleCF > 90:
                secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus90, 100),
                                                                                ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack + joinAngleRad / 2), 100))

                # else:
                #     secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                #                                                                     ptEK11, MathHelper.distanceBearingPoint(ptEK11, inboundTrackPlus90, 100))
            # cfSecPt = MathHelper.distanceBearingPoint(cfendPt, outboundTrackPlus90, asw1.Metres)
            # secondaryPolylineAreaIn.method_1(cfSecPt)
            secondaryPolylineAreaIn.method_1(ptEK11)
            secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                secondaryPolylineAreaIn.method_1(primaryEndPt2)
            else:
                primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
                secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                secondaryPolylineAreaIn.method_1(primaryEndPt2)

            resultPolylineAreList.append(secondaryPolylineAreaIn)

            #### SecondaryAreaOut
            secondaryPolylineAreaOut = primaryOutLine.method_23(asw1.Metres, OffsetGapType.Fillet)
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                         point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                    secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackPlus90, asw1.Metres))

            secondaryPolylineAreaOut.reverse()
            secondaryPolylineAreaOut.extend(primaryOutLine)
            secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
            resultPolylineAreList.append(secondaryPolylineAreaOut)

            complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))
            complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))
            complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))

        else:
            #### Creating Primary Area
            # cfStartPt = MathHelper.distanceBearingPoint(cfWpt1, inboundTrackPlus90, asw1.Metres)
            # primaryPolylineArea.method_1(cfStartPt)
            # primaryOutLine.method_1(cfStartPt)

            ptEk = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
            primaryPolylineArea.method_1(ptEk)
            primaryOutLine.method_1(ptEk)

            startPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackPlus90, asw1.Metres)
            windSpiral1 = WindSpiral(startPt1, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
            pt0 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
            pt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackPlus90, asw2.Metres)
            # if windSpiral1.method_1(pt0, pt1, False):
            leftMiddlePt13, contactPt13, rightMiddlePt13 = windSpiral1.getContactWithBearingOfTangent(MathHelper.smethod_4(outboundTrack - joinAngleRad))
            intersectPolylineArea13 = PolylineArea()
            if round(windSpiral1.Radius[0], 2) == round(MathHelper.calcDistance(windSpiral1.Center[0], contactPt13), 2):
                point3dArray = [startPt1, contactPt13]
                intersectPolylineArea13 = PolylineArea(point3dArray)
                intersectPolylineArea13.SetBulgeAt(0, MathHelper.smethod_60(startPt1, rightMiddlePt13, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))
            elif round(windSpiral1.Radius[1], 2) == round(MathHelper.calcDistance(windSpiral1.Center[1], contactPt13), 2):
                point3dArray = [startPt1, windSpiral1.Finish[0], contactPt13]
                intersectPolylineArea13 = PolylineArea(point3dArray)
                intersectPolylineArea13.SetBulgeAt(0, MathHelper.smethod_60(startPt1, windSpiral1.Middle[0], windSpiral1.Finish[0]))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                intersectPolylineArea13.SetBulgeAt(1, MathHelper.smethod_60(windSpiral1.Finish[0], rightMiddlePt13, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))
            else:
                point3dArray = [startPt1, windSpiral1.Finish[0], windSpiral1.Finish[1],contactPt13]
                intersectPolylineArea13 = PolylineArea(point3dArray)
                intersectPolylineArea13.SetBulgeAt(0, MathHelper.smethod_60(startPt1, windSpiral1.Middle[0], windSpiral1.Finish[0]))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                intersectPolylineArea13.SetBulgeAt(1, MathHelper.smethod_60(windSpiral1.Finish[0], windSpiral1.Middle[1], windSpiral1.Finish[1]))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                intersectPolylineArea13.SetBulgeAt(2, MathHelper.smethod_60(windSpiral1.Finish[1], rightMiddlePt13, contactPt13))#, windSpiral.Middle[0], windSpiral.Finish[0]))


            primaryPolylineArea.extend(intersectPolylineArea13)
            primaryOutLine.extend(intersectPolylineArea13)

            primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres)
            testPt0 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackPlus90, asw2.Metres)
            testPt1 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                      primaryEndPt1, MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))
            if testPt1 == None:
                intersectPt3 = MathHelper.getIntersectionPoint(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), 100),
                                                      point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, 100))
                primaryPolylineArea.method_1(intersectPt3)
                primaryOutLine.method_1(intersectPt3)
            else:
                intersectPt3 = testPt1
                testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                             point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                if MathHelper.calcDistance(intersectPt3, testPt) < distFromEnd:
                    primaryEndPtWithAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                    intersectPt3 = MathHelper.getIntersectionPointWithTwoLine(contactPt13, MathHelper.distanceBearingPoint(contactPt13, MathHelper.smethod_4(outboundTrack - joinAngleRad), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                      primaryEndPtWithAsw2, MathHelper.distanceBearingPoint(primaryEndPtWithAsw2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))

                primaryPolylineArea.method_1(intersectPt3)
                primaryOutLine.method_1(intersectPt3)
                # primaryPolylineArea.method_1(primaryEndPt1)
                # primaryOutLine.method_1(primaryEndPt1)
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                mergePtPrimary = MathHelper.distanceBearingPoint(primaryEndPt1, outboundTrackPlus180, distFromEnd)
                mergePtSecondaryOut = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                primaryPolylineArea.method_1(mergePtPrimary)

                primaryEndPt1ByAsw2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                primaryEndPt1ByAsw2SecondaryOut = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2)
                if asw1.Metres > asw2.Metres:
                    mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(30)), 100),
                                                               primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                    mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)
                else:
                    mergePtSecondaryOut1 = MathHelper.getIntersectionPoint(mergePtSecondaryOut, MathHelper.distanceBearingPoint(mergePtSecondaryOut, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(15)), 100),
                                                               primaryEndPt1ByAsw2SecondaryOut, MathHelper.distanceBearingPoint(primaryEndPt1ByAsw2SecondaryOut, outboundTrackPlus180, 100))
                    mergePtPrimary1 = MathHelper.distanceBearingPoint(mergePtSecondaryOut1, outboundTrackMinus90, asw2.Metres)

                primaryPolylineArea.method_1(mergePtPrimary1)
                primaryPolylineArea.method_1(primaryEndPt1ByAsw2)

            else:
                primaryPolylineArea.method_1(primaryEndPt1)
                primaryOutLine.method_1(primaryEndPt1)

                # primaryPolylineArea.method_1(primaryEndPt1)
                # primaryOutLine.method_1(primaryEndPt1)
            d = asw1.Metres
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                d = asw2.Metres
            primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, d)
            primaryEndPt2ByAsw1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                mergePtPrimaryIn = MathHelper.distanceBearingPoint(primaryEndPt2ByAsw1, outboundTrackPlus180, distFromEnd)
                mergePtSecondaryIn = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres * 2), outboundTrackPlus180, distFromEnd)
                primaryPolylineArea.method_1(primaryEndPt2)
                primaryInLine.method_1(primaryEndPt2)

                primaryEndPt2ByAsw2SecondaryIn = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)

                if asw1.Metres > asw2.Metres:
                    mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack + Unit.ConvertDegToRad(30)), 100),
                                                               primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                    mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)
                else:
                    mergePtSecondaryIn1 = MathHelper.getIntersectionPoint(mergePtSecondaryIn, MathHelper.distanceBearingPoint(mergePtSecondaryIn, MathHelper.smethod_4(outboundTrack - Unit.ConvertDegToRad(15)), 100),
                                                               primaryEndPt2ByAsw2SecondaryIn, MathHelper.distanceBearingPoint(primaryEndPt2ByAsw2SecondaryIn, outboundTrackPlus180, 100))
                    mergePtPrimary2 = MathHelper.distanceBearingPoint(mergePtSecondaryIn1, outboundTrackPlus90, asw2.Metres)

                primaryPolylineArea.method_1(mergePtPrimary2)
                primaryPolylineArea.method_1(mergePtPrimaryIn)
                primaryInLine.method_1(mergePtPrimary2)
                primaryInLine.method_1(mergePtPrimaryIn)
            else:
                primaryPolylineArea.method_1(primaryEndPt2ByAsw1)
                primaryInLine.method_1(primaryEndPt2ByAsw1)

            ptEk1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
            ptEK11 = MathHelper.distanceBearingPoint(ptEk1, inboundTrackMinus90, asw1.Metres)
            intersectPt4 = MathHelper.getIntersectionPointWithTwoLine(ptEk1, MathHelper.distanceBearingPoint(ptEk1, MathHelper.smethod_4(outboundTrack + turnAngleRad / 2), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                           primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))
            if intersectPt4 == None:
                intersectPt4 = MathHelper.getIntersectionPoint(primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100),
                                                                     ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack - joinAngleRad / 2), 100))
                primaryPolylineArea.method_1(intersectPt4)
                primaryInLine.method_1(intersectPt4)
                primaryPolylineArea.method_1(ptEK11)
                primaryInLine.method_1(ptEK11)
                # intersectPt4 = MathHelper.getIntersectionPoint(ptEk1, MathHelper.distanceBearingPoint(ptEk1, inboundTrackMinus90, 100),
                #                                                         primaryEndPt2, MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackPlus180, 100))
            else:
                primaryPolylineArea.method_1(intersectPt4)
                primaryInLine.method_1(intersectPt4)
                primaryPolylineArea.method_1(ptEk1)
                primaryInLine.method_1(ptEk1)

            # cfendPt = MathHelper.distanceBearingPoint(cfWpt1, inboundTrackMinus90, asw1.Metres)
            # primaryPolylineArea.method_1(cfendPt)
            # primaryInLine.method_1(cfendPt)
            #
            primaryPolylineArea.method_1(ptEk)
            resultPolylineAreList.append(primaryPolylineArea)

            #### SecondaryAreaIn
            secondaryPolylineAreaIn.extend(primaryInLine)
            d = asw1.Metres
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                d = asw2.Metres
            secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, d)
            # secondaryInEndPt = MathHelper.distanceBearingPoint(primaryEndPt2, outboundTrackMinus90, asw1.Metres)
            secondaryInIntersectPt = MathHelper.getIntersectionPointWithTwoLine(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                                     ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack - joinAngleRad / 2), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))
            if secondaryInIntersectPt == None:
                # if turnAngle > 90:
                secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackMinus90, 100),
                                                                                ptEK11, MathHelper.distanceBearingPoint(ptEK11, MathHelper.smethod_4(outboundTrack - joinAngleRad / 2), 100))
                # else:
                #     secondaryInIntersectPt = MathHelper.getIntersectionPoint(secondaryInEndPt, MathHelper.distanceBearingPoint(secondaryInEndPt, outboundTrackPlus180, 100),
                #                                                                     ptEK11, MathHelper.distanceBearingPoint(ptEK11, inboundTrackMinus90, 100))
            # cfSecPt = MathHelper.distanceBearingPoint(cfendPt, outboundTrackMinus90, asw1.Metres)
            # secondaryPolylineAreaIn.method_1(cfSecPt)
            secondaryPolylineAreaIn.method_1(ptEK11)
            secondaryPolylineAreaIn.method_1(secondaryInIntersectPt)
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                secondaryPolylineAreaIn.method_1(mergePtSecondaryIn)
                secondaryPolylineAreaIn.method_1(mergePtSecondaryIn1)
                secondaryPolylineAreaIn.method_1(primaryEndPt2ByAsw2SecondaryIn)
                secondaryPolylineAreaIn.method_1(primaryEndPt2)
            else:
                primaryEndPt2 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw1.Metres)
                secondaryPolylineAreaIn.method_1(secondaryInEndPt)
                secondaryPolylineAreaIn.method_1(primaryEndPt2)

            resultPolylineAreList.append(secondaryPolylineAreaIn)

            #### SecondaryAreaOut
            secondaryPolylineAreaOut = primaryOutLine.method_23(-asw1.Metres, OffsetGapType.Fillet)
            if distFromEnd > 0.0 and asw1.Metres != asw2.Metres:
                secondaryPolylineAreaOut.reverse()
                testPt = MathHelper.getIntersectionPoint(intersectPt3, MathHelper.distanceBearingPoint(intersectPt3, outboundTrack, 100),
                                                         point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, 100))
                if testPt != None and MathHelper.calcDistance(secondaryPolylineAreaOut.method_14()[len(secondaryPolylineAreaOut.method_14()) - 1], testPt) > distFromEnd:
                    secondaryPolylineAreaOut.method_1(mergePtSecondaryOut)
                secondaryPolylineAreaOut.method_1(mergePtSecondaryOut1)
                secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2SecondaryOut)
                secondaryPolylineAreaOut.method_1(primaryEndPt1ByAsw2)
                secondaryPolylineAreaOut.method_1(mergePtPrimary1)
                secondaryPolylineAreaOut.method_1(MathHelper.distanceBearingPoint(mergePtSecondaryOut, outboundTrackMinus90, asw1.Metres))
                ptArray = primaryOutLine.method_14()
                primaryOutLine = PolylineArea(ptArray)
                primaryOutLine.reverse()
            # secondaryPolylineAreaOut.reverse()
            secondaryPolylineAreaOut.extend(primaryOutLine)
            secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])
            resultPolylineAreList.append(secondaryPolylineAreaOut)

            complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))
            complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryInLine, True, asw1.Metres))
            complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryOutLine, True, asw1.Metres))

        if not MathHelper.pointInPolygon(primaryPolylineArea.method_14(), cfWpt1, 0.001):
            polylineArea = PolylineArea()
            polylineArea.method_1(cfWpt1)
            if turnDirection == TurnDirection.Right:
                polylineArea.method_1(MathHelper.distanceBearingPoint(ptEk, inboundTrackMinus90, asw1.Metres))
            else:
                polylineArea.method_1(MathHelper.distanceBearingPoint(ptEk, inboundTrackPlus90, asw1.Metres))

            polylineArea.method_1(ptEK11)
            # polylineArea.method_1(MathHelper.getIntersectionPoint(cfWpt1, MathHelper.distanceBearingPoint(cfWpt1, MathHelper.smethod_4(inboundTrack + Unit.ConvertDegToRad(15)), 100),\
            #                                                       point3d_Wpt1, MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackMinus90, 100)))
            # polylineArea.method_1(MathHelper.getIntersectionPoint(cfWpt1, MathHelper.distanceBearingPoint(cfWpt1, MathHelper.smethod_4(inboundTrack - Unit.ConvertDegToRad(15)), 100),\
            #                                                       point3d_Wpt1, MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackMinus90, 100)))
            polylineArea.method_1(cfWpt1)
            resultPolylineAreList.append(polylineArea)

        nominalTrackPolylineArea = PolylineArea()
        turnAngle = turnAngleCF
        num14 = 0.6 * turnAngle if (turnAngle < 50) else 30
        if (turnAngle < 50):
            num3 = 90 - num14
            num1 = num3
        else:
            num3 = 60
        num1 = num3
        distance = Distance.smethod_0(speedTas, 15)
        metres6 = distance.Metres
        num15 = metres3 * math.sin(Unit.ConvertDegToRad(turnAngle))
        num16 = metres3 * math.cos(Unit.ConvertDegToRad(turnAngle)) * math.tan(Unit.ConvertDegToRad(num14))
        num17 = metres3 * ((1 - math.cos(Unit.ConvertDegToRad(turnAngle)) / math.cos(Unit.ConvertDegToRad(num14))) / math.sin(Unit.ConvertDegToRad(num14)))
        num18 = metres6 * math.tan(Unit.ConvertDegToRad(num14 / 2))
        if (self.parametersPanel.chbCatH.Checked):
            metresPerSecond = 5 * speedTas.MetresPerSecond
        else:
            metresPerSecond = 10 * speedTas.MetresPerSecond
            num2 = metresPerSecond
        num2 = metresPerSecond
        point3d31 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrack, num15 + num16 + num17 + num18)
        if (turnDirection != TurnDirection.Left):
            point3d3 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack + Unit.ConvertDegToRad(90), metres3)
            point3d5 = MathHelper.distanceBearingPoint(point3d3, outboundTrack - Unit.ConvertDegToRad(num1), metres3)
            point3d4 = MathHelper.distanceBearingPoint(point3d31, outboundTrack - Unit.ConvertDegToRad(90), metres6)
            point3d6 = MathHelper.distanceBearingPoint(point3d4, MathHelper.getBearing(point3d4, point3d31) + Unit.ConvertDegToRad(num14), metres6)
        else:
            point3d3 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack - Unit.ConvertDegToRad(90), metres3)
            point3d5 = MathHelper.distanceBearingPoint(point3d3, outboundTrack + Unit.ConvertDegToRad(num1), metres3)
            point3d4 = MathHelper.distanceBearingPoint(point3d31, outboundTrack + Unit.ConvertDegToRad(90), metres6)
            point3d6 = MathHelper.distanceBearingPoint(point3d4, MathHelper.getBearing(point3d4, point3d31) - Unit.ConvertDegToRad(num14), metres6)
        # point3d32 = MathHelper.distanceBearingPoint(point3d31, outboundTrack, num2)
        nominalTrackPolylineArea.Add(PolylineAreaPoint(point3d_Wpt1, MathHelper.smethod_57(turnDirection, point3d_Wpt1, point3d5, point3d3)))
        nominalTrackPolylineArea.method_1(point3d5)
        if (turnDirection != TurnDirection.Left):
            testPtNomninal = MathHelper.getIntersectionPointWithTwoLine(point3d5, MathHelper.distanceBearingPoint(point3d5, MathHelper.smethod_4(outboundTrack + joinAngleRad), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                          point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))
        else:
            testPtNomninal = MathHelper.getIntersectionPointWithTwoLine(point3d5, MathHelper.distanceBearingPoint(point3d5, MathHelper.smethod_4(outboundTrack - joinAngleRad), MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)),
                                                          point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus180, MathHelper.calcDistance(point3d_Wpt2, point3d_Wpt1)))

        if testPtNomninal == None:
            nominalTrackPolylineArea.method_1(point3d_Wpt2)
        else:
            nominalTrackPolylineArea.method_1(testPtNomninal)
            nominalTrackPolylineArea.method_1(point3d_Wpt2)
        # if (turnDirection == TurnDirection.Left):
        #     nominalTrackPolylineArea.Add(PolylineAreaPoint(point3d6, MathHelper.smethod_57(TurnDirection.Right, point3d6, point3d31, point3d4)))
        # elif (turnDirection != TurnDirection.Right):
        #     nominalTrackPolylineArea.method_1(point3d6)
        # else:
        #     nominalTrackPolylineArea.Add(PolylineAreaPoint(point3d6, MathHelper.smethod_57(TurnDirection.Left, point3d6, point3d31, point3d4)))
        # nominalTrackPolylineArea.method_1(point3d31)
        # if (turnDirection == TurnDirection.Left):
        #     bearing = outboundTrackPlus90
        # else:
        #     bearing = outboundTrackMinus90
        # if MathHelper.getIntersectionPointBetweenPolylineArea(nominalTrackPolylineArea, PolylineArea([point3d_Wpt2, MathHelper.distanceBearingPoint(point3d_Wpt2, bearing, 10000)])) == None:
        #     nominalTrackPolylineArea.method_1(point3d_Wpt2)
        nominalTrackPolylineArea.insert(0, PolylineAreaPoint(cfWpt1))
        resultPolylineAreList.append(nominalTrackPolylineArea)


        return complexObstacleArea, resultPolylineAreList


    def flyOverTurnAllowedWithDF_method(self, point3d_Wpt1, point3d_Wpt2, inboundTrack, outboundTrack, rnavGnssTolerance1, rnavGnssTolerance2, turnDirection):
        inboundTrackMinus90 = MathHelper.smethod_4(inboundTrack - math.pi / 2)
        inboundTrackPlus90 = MathHelper.smethod_4(inboundTrack + math.pi / 2)
        inboundTrackPlus180 = MathHelper.smethod_4(inboundTrack + math.pi)
        outboundTrackMinus90 = MathHelper.smethod_4(outboundTrack - math.pi / 2)
        outboundTrackPlus90 = MathHelper.smethod_4(outboundTrack + math.pi / 2)
        outboundTrackPlus180 = MathHelper.smethod_4(outboundTrack + math.pi)
        complexObstacleArea = ComplexObstacleArea()
        asw1 = rnavGnssTolerance1.ASW / 2
        att1 = rnavGnssTolerance1.ATT
        asw2 = rnavGnssTolerance2.ASW / 2
        att2 = rnavGnssTolerance2.ATT

        rnavWaypointType1 = self.method_33()
        resultPolylineAreList = []
        turnAngle = MathHelper.smethod_76(Unit.smethod_1(inboundTrack), Unit.smethod_1(outboundTrack), AngleUnits.Degrees)
        joinAngleRad = Unit.ConvertDegToRad(15)
        speedTas = Speed.smethod_0(self.parametersPanel.pnlIas.Value, self.parametersPanel.pnlIsa.Value, self.parametersPanel.pnlAltitude.Value)
        speedWind = self.parametersPanel.pnlWind.Value
        valueBankAngle = self.parametersPanel.pnlBankAngle.Value
        distance = Distance.smethod_0(speedTas, valueBankAngle)
        metres3 = distance.Metres
        distance = RnavWaypoints.getDistanceFromWaypointToEarliestTurningPoint(rnavWaypointType1, Distance(att1.Metres), Distance(metres3), turnAngle, AngleUnits.Degrees)
        distFromWpt1ToEarliest = distance.Metres
        point3dEarliest = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, math.fabs(distFromWpt1ToEarliest)) if (distFromWpt1ToEarliest >= 0) else MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack, math.fabs(distFromWpt1ToEarliest))
        distance = RnavWaypoints.getDistanceFromWaypointToLatestTurningPoint(rnavWaypointType1, speedTas, speedWind, float(self.parametersPanel.pnlPilotTime.Value), float(self.parametersPanel.pnlBankEstTime.Value), Distance(att1.Metres), Distance(metres3), turnAngle, AngleUnits.Degrees)
        distFromWpt1ToLatest = distance.Metres
        point3dLatest = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, math.fabs(distFromWpt1ToLatest)) if (distFromWpt1ToLatest >= 0) else MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack, math.fabs(distFromWpt1ToLatest))
        joinBearing1 = 0.0
        if turnAngle <= 90:
            if turnDirection == TurnDirection.Right:
                primaryPolylineArea = PolylineArea()
                ptEtK = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
                primaryPolylineArea.method_1(ptEtK)
                ptWindSipalStart = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackMinus90, asw1.Metres)
                windSpiral = WindSpiral(ptWindSipalStart, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)

                middlePt, intersectWithSpiralPt = windSpiral.getContact(point3d_Wpt2, joinAngleRad, 0, turnDirection)
                point3dArray = [windSpiral.Start[0], intersectWithSpiralPt]
                intersectPolylineArea = PolylineArea(point3dArray)
                intersectPolylineArea.SetBulgeAt(0, MathHelper.smethod_60(windSpiral.Start[0], middlePt, intersectWithSpiralPt))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                primaryPolylineArea.extend(intersectPolylineArea)

                joinBearing0 = MathHelper.smethod_4(MathHelper.getBearing(intersectWithSpiralPt, point3d_Wpt2) - joinAngleRad)
                ptPrimaryEnd0 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(joinBearing0 + joinAngleRad - math.pi / 2), asw2.Metres)
                intersectPt = MathHelper.getIntersectionPoint(intersectWithSpiralPt, MathHelper.distanceBearingPoint(intersectWithSpiralPt, joinBearing0, 100),
                                                              ptPrimaryEnd0, MathHelper.distanceBearingPoint(ptPrimaryEnd0, MathHelper.smethod_4(joinBearing0 + joinAngleRad + math.pi), 100))
                if not MathHelper.IsContainedInTwoPoint(intersectWithSpiralPt, ptPrimaryEnd0, intersectPt):
                    ptPrimaryEnd0 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                    intersectPt = MathHelper.getIntersectionPoint(intersectWithSpiralPt, MathHelper.distanceBearingPoint(intersectWithSpiralPt, joinBearing0, 100),
                                                              ptPrimaryEnd0, MathHelper.distanceBearingPoint(ptPrimaryEnd0, outboundTrackPlus180, 100))



                primaryPolylineArea.method_1(intersectPt)
                primaryPolylineArea.method_1(ptPrimaryEnd0)

                primaryPoylineOut = PolylineArea()
                for polylineAreaPoint in primaryPolylineArea:
                    primaryPoylineOut.append(polylineAreaPoint)
                primaryPolylineArea.method_1(point3d_Wpt2)

                primaryPoylineIn = PolylineArea()
                ptEtK1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
                joinBearing1 = MathHelper.smethod_4(MathHelper.getBearing(ptEtK1, point3d_Wpt2) + joinAngleRad)
                ptPrimaryEnd1 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(joinBearing1 - joinAngleRad + math.pi / 2), asw2.Metres)
                primaryPolylineArea.method_1(ptPrimaryEnd1)
                primaryPoylineIn.method_1(ptPrimaryEnd1)

                intersectPt1 = MathHelper.getIntersectionPoint(ptEtK1, MathHelper.distanceBearingPoint(ptEtK1, joinBearing1, 100),
                                                              ptPrimaryEnd1, MathHelper.distanceBearingPoint(ptPrimaryEnd1, MathHelper.smethod_4(joinBearing1 - joinAngleRad + math.pi), 100))
                if not MathHelper.IsContainedInTwoPoint(ptEtK1, ptPrimaryEnd1, intersectPt1):
                    ptPrimaryEnd1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                    intersectPt1 = MathHelper.getIntersectionPoint(ptEtK1, MathHelper.distanceBearingPoint(ptEtK1, joinBearing1, 100),
                                                              ptPrimaryEnd1, MathHelper.distanceBearingPoint(ptPrimaryEnd1, outboundTrackPlus180, 100))

                primaryPolylineArea.method_1(intersectPt1)
                primaryPoylineIn.method_1(intersectPt1)
                primaryPolylineArea.method_1(ptEtK1)
                primaryPoylineIn.method_1(ptEtK1)
                primaryPolylineArea.method_1(ptEtK)


                offsetPolylineAreaOut = primaryPoylineOut.method_23(asw1.Metres, OffsetGapType.Fillet)
                pointArray = offsetPolylineAreaOut.method_14(4)
                pointArray.reverse()
                secondaryPolylineAreaOut = PolylineArea(pointArray)
                secondaryPolylineAreaOut.extend(primaryPoylineOut)
                secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])

                secondaryPolylineAreaIn = PolylineArea()
                ptEtK11 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres * 2)
                # joinBearing11 = MathHelper.smethod_4(MathHelper.getBearing(ptEtK11, point3d_Wpt2) + joinAngleRad)
                ptPrimaryEnd11 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(joinBearing1 - joinAngleRad + math.pi / 2), asw2.Metres + asw1.Metres)


                intersectPt11 = MathHelper.getIntersectionPoint(ptEtK11, MathHelper.distanceBearingPoint(ptEtK11, joinBearing1, 100),
                                                              ptPrimaryEnd11, MathHelper.distanceBearingPoint(ptPrimaryEnd11, MathHelper.smethod_4(joinBearing1 - joinAngleRad + math.pi), 100))
                if not MathHelper.IsContainedInTwoPoint(ptEtK11, ptPrimaryEnd11, intersectPt11):
                    ptPrimaryEnd11 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres + asw1.Metres)
                    intersectPt11 = MathHelper.getIntersectionPoint(ptEtK11, MathHelper.distanceBearingPoint(ptEtK11, joinBearing1, 100),
                                                              ptPrimaryEnd11, MathHelper.distanceBearingPoint(ptPrimaryEnd11, outboundTrackPlus180, 100))
                secondaryPolylineAreaIn.method_1(ptEtK11)
                secondaryPolylineAreaIn.method_1(intersectPt11)
                secondaryPolylineAreaIn.method_1(ptPrimaryEnd11)
                secondaryPolylineAreaIn.extend(primaryPoylineIn)
                secondaryPolylineAreaIn.method_1(ptEtK11)

                resultPolylineAreList.append(primaryPolylineArea)
                resultPolylineAreList.append(secondaryPolylineAreaOut)
                resultPolylineAreList.append(secondaryPolylineAreaIn)
                complexObstacleArea.append(PrimaryObstacleArea(primaryPolylineArea))
                complexObstacleArea.append(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryPoylineOut))
                complexObstacleArea.append(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryPoylineIn))
            else:
                primaryPolylineArea = PolylineArea()
                ptEtK = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, asw1.Metres)
                primaryPolylineArea.method_1(ptEtK)
                ptWindSipalStart = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackPlus90, asw1.Metres)
                windSpiral = WindSpiral(ptWindSipalStart, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)

                middlePt, intersectWithSpiralPt = windSpiral.getContact(point3d_Wpt2, joinAngleRad, 0, turnDirection)
                point3dArray = [windSpiral.Start[0], intersectWithSpiralPt]
                intersectPolylineArea = PolylineArea(point3dArray)
                intersectPolylineArea.SetBulgeAt(0, MathHelper.smethod_60(windSpiral.Start[0], middlePt, intersectWithSpiralPt))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                # intersectPolylineArea = windSpiral.getIntersectPolylineArea(outboundTrack + joinAngleRad, AngleUnits.Radians)
                primaryPolylineArea.extend(intersectPolylineArea)

                joinBearing0 = MathHelper.smethod_4(MathHelper.getBearing(intersectWithSpiralPt, point3d_Wpt2) + joinAngleRad)
                ptPrimaryEnd0 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(joinBearing0 - joinAngleRad + math.pi / 2), asw2.Metres)
                intersectPt = MathHelper.getIntersectionPoint(intersectWithSpiralPt, MathHelper.distanceBearingPoint(intersectWithSpiralPt, joinBearing0, 100),
                                                              ptPrimaryEnd0, MathHelper.distanceBearingPoint(ptPrimaryEnd0, MathHelper.smethod_4(joinBearing0 - joinAngleRad + math.pi), 100))
                if not MathHelper.IsContainedInTwoPoint(intersectWithSpiralPt, ptPrimaryEnd0, intersectPt):
                    ptPrimaryEnd0 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres)
                    intersectPt = MathHelper.getIntersectionPoint(intersectWithSpiralPt, MathHelper.distanceBearingPoint(intersectWithSpiralPt, joinBearing0, 100),
                                                              ptPrimaryEnd0, MathHelper.distanceBearingPoint(ptPrimaryEnd0, outboundTrackPlus180, 100))



                primaryPolylineArea.method_1(intersectPt)
                primaryPolylineArea.method_1(ptPrimaryEnd0)

                primaryPoylineOut = PolylineArea()
                for polylineAreaPoint in primaryPolylineArea:
                    primaryPoylineOut.append(polylineAreaPoint)
                primaryPolylineArea.method_1(point3d_Wpt2)

                primaryPoylineIn = PolylineArea()
                ptEtK1 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres)
                joinBearing1 = MathHelper.smethod_4(MathHelper.getBearing(ptEtK1, point3d_Wpt2) - joinAngleRad)
                ptPrimaryEnd1 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(joinBearing1 + joinAngleRad - math.pi / 2), asw2.Metres)
                primaryPolylineArea.method_1(ptPrimaryEnd1)
                primaryPoylineIn.method_1(ptPrimaryEnd1)

                intersectPt1 = MathHelper.getIntersectionPoint(ptEtK1, MathHelper.distanceBearingPoint(ptEtK1, joinBearing1, 100),
                                                              ptPrimaryEnd1, MathHelper.distanceBearingPoint(ptPrimaryEnd1, MathHelper.smethod_4(joinBearing1 + joinAngleRad + math.pi), 100))
                if not MathHelper.IsContainedInTwoPoint(ptEtK1, ptPrimaryEnd1, intersectPt1):
                    ptPrimaryEnd1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
                    intersectPt1 = MathHelper.getIntersectionPoint(ptEtK1, MathHelper.distanceBearingPoint(ptEtK1, joinBearing1, 100),
                                                              ptPrimaryEnd1, MathHelper.distanceBearingPoint(ptPrimaryEnd1, outboundTrackPlus180, 100))

                primaryPolylineArea.method_1(intersectPt1)
                primaryPoylineIn.method_1(intersectPt1)
                primaryPolylineArea.method_1(ptEtK1)
                primaryPoylineIn.method_1(ptEtK1)
                primaryPolylineArea.method_1(ptEtK)


                offsetPolylineAreaOut = primaryPoylineOut.method_23(-asw1.Metres, OffsetGapType.Fillet)
                pointArray = offsetPolylineAreaOut.method_14(4)
                # pointArray.reverse()
                secondaryPolylineAreaOut = PolylineArea(pointArray)
                secondaryPolylineAreaOut.extend(primaryPoylineOut)
                secondaryPolylineAreaOut.append(secondaryPolylineAreaOut[0])

                secondaryPolylineAreaIn = PolylineArea()
                ptEtK11 = MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, asw1.Metres * 2)
                # joinBearing11 = MathHelper.smethod_4(MathHelper.getBearing(ptEtK11, point3d_Wpt2) + joinAngleRad)
                ptPrimaryEnd11 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(joinBearing1 + joinAngleRad - math.pi / 2), asw2.Metres + asw1.Metres)


                intersectPt11 = MathHelper.getIntersectionPoint(ptEtK11, MathHelper.distanceBearingPoint(ptEtK11, joinBearing1, 100),
                                                              ptPrimaryEnd11, MathHelper.distanceBearingPoint(ptPrimaryEnd11, MathHelper.smethod_4(joinBearing1 + joinAngleRad + math.pi), 100))
                if not MathHelper.IsContainedInTwoPoint(ptEtK11, ptPrimaryEnd11, intersectPt11):
                    ptPrimaryEnd11 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres + asw1.Metres)
                    intersectPt11 = MathHelper.getIntersectionPoint(ptEtK11, MathHelper.distanceBearingPoint(ptEtK11, joinBearing1, 100),
                                                              ptPrimaryEnd11, MathHelper.distanceBearingPoint(ptPrimaryEnd11, outboundTrackPlus180, 100))
                secondaryPolylineAreaIn.method_1(ptEtK11)
                secondaryPolylineAreaIn.method_1(intersectPt11)
                secondaryPolylineAreaIn.method_1(ptPrimaryEnd11)
                secondaryPolylineAreaIn.extend(primaryPoylineIn)
                secondaryPolylineAreaIn.method_1(ptEtK11)

                resultPolylineAreList.append(primaryPolylineArea)
                resultPolylineAreList.append(secondaryPolylineAreaOut)
                resultPolylineAreList.append(secondaryPolylineAreaIn)
                complexObstacleArea.append(PrimaryObstacleArea(primaryPolylineArea))
                complexObstacleArea.append(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaOut, primaryPoylineOut))
                complexObstacleArea.append(SecondaryObstacleAreaWithManyPoints(secondaryPolylineAreaIn, primaryPoylineIn))

            nominalArcStartPt, nominalArcStartMiddlePt, nominalArcEndPt = MathHelper.getPointsOfArcWithContactPtAndOutPt(point3d_Wpt1, inboundTrack, point3d_Wpt2, joinBearing1, turnDirection)
            point3dArray = [nominalArcStartPt, nominalArcEndPt]
            nominalPolylineArea = PolylineArea(point3dArray)
            nominalPolylineArea.SetBulgeAt(0, MathHelper.smethod_60(nominalArcStartPt, nominalArcStartMiddlePt, nominalArcEndPt))#, windSpiral.Middle[0], windSpiral.Finish[0]))
            nominalPolylineArea.method_1(point3d_Wpt2)
            resultPolylineAreList.append(nominalPolylineArea)
        else:
            if turnDirection == TurnDirection.Right:
                primaryPoylineOut = PolylineArea()
                offsetBeforeLine = PolylineArea()
                distP_S = MathHelper.calcDistance(point3d_Wpt1, point3dLatest) * math.tan(joinAngleRad)
                secondaryStartPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackMinus90, asw1.Metres + distP_S)
                startPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackMinus90, asw1.Metres)
                primaryPolylineArea = PolylineArea()
                primaryOutPt1 = MathHelper.getIntersectionPoint(secondaryStartPt1, MathHelper.distanceBearingPoint(secondaryStartPt1, MathHelper.smethod_4(inboundTrackPlus180 - joinAngleRad), 100.0),
                                                       startPt1, MathHelper.distanceBearingPoint(startPt1, inboundTrackPlus180, 100.0))

                ptEK = MathHelper.getIntersectionPoint(primaryOutPt1, MathHelper.distanceBearingPoint(primaryOutPt1, MathHelper.smethod_4(inboundTrackPlus180 - joinAngleRad), 100.0),
                                                       point3dEarliest, MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackMinus90, 100.0))
                primaryPolylineArea.method_1(ptEK)
                primaryPolylineArea.method_1(primaryOutPt1)
                primaryPoylineOut.method_1(primaryOutPt1)


                windSpiral1 = WindSpiral(startPt1, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                windSpiralMiddlePt1, windSpiralContactPt1, p = windSpiral1.getContactWithBearingOfTangent(inboundTrackPlus90, 1, turnDirection)
                point3dArray = [windSpiral1.Start[0], windSpiralContactPt1]
                windSpiralPolylineArea1 = PolylineArea(point3dArray)
                windSpiralPolylineArea1.SetBulgeAt(0, MathHelper.smethod_60(windSpiral1.Start[0], windSpiralMiddlePt1, windSpiralContactPt1))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                primaryPolylineArea.extend(windSpiralPolylineArea1)
                primaryPoylineOut.extend(windSpiralPolylineArea1)
                offsetBeforeLine.extend(windSpiralPolylineArea1)

                startPt2 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackPlus90, asw1.Metres)
                windSpiral2 = WindSpiral(startPt2, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)

                startPt3 = MathHelper.distanceBearingPoint(primaryOutPt1, inboundTrackPlus90, asw1.Metres * 2)
                windSpiral3 = WindSpiral(startPt3, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                windSpiral3Bearing = windSpiral3.getBearingOfTangentWithOutPt(point3d_Wpt2, 1, turnDirection)
                pt, windSpiral2ContactStartPt, p = windSpiral2.getContactWithBearingOfTangent(inboundTrackPlus90, None, turnDirection)

                windSpiral2MiddlePt, windSpiral2ContactPt, p = windSpiral2.getContactWithBearingOfTangent(MathHelper.smethod_4(windSpiral3Bearing - joinAngleRad), None, turnDirection)
                primaryOutPt3 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(windSpiral3Bearing - math.pi / 2), asw2.Metres)
                testPt = MathHelper.getIntersectionPointWithTwoLine(windSpiral2ContactPt, MathHelper.distanceBearingPoint(windSpiral2ContactPt, MathHelper.smethod_4(windSpiral3Bearing - joinAngleRad), MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) * 2),
                                                                primaryOutPt3, MathHelper.distanceBearingPoint(primaryOutPt3, MathHelper.smethod_4(windSpiral3Bearing + math.pi), MathHelper.calcDistance(point3d_Wpt1, point3d_Wpt2) * 2))
                if testPt == None:
                    primaryOutPt2 = MathHelper.getIntersectionPoint(windSpiral2ContactPt, MathHelper.distanceBearingPoint(windSpiral2ContactPt, inboundTrackPlus180, 100.0),
                                                                    primaryOutPt3, MathHelper.distanceBearingPoint(primaryOutPt3, MathHelper.smethod_4(windSpiral3Bearing + math.pi), 100.0))

                else:
                    point3dArray = [windSpiral2ContactStartPt, windSpiral2ContactPt]
                    windSpiralPolylineArea2 = PolylineArea(point3dArray)
                    windSpiralPolylineArea2.SetBulgeAt(0, MathHelper.smethod_60(windSpiral2ContactStartPt, windSpiral2MiddlePt, windSpiral2ContactPt))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                    if MathHelper.smethod_60(windSpiral2ContactStartPt, windSpiral2MiddlePt, windSpiral2ContactPt) > - 30:
                        primaryPolylineArea.extend(windSpiralPolylineArea2)
                        primaryPoylineOut.extend(windSpiralPolylineArea2)
                        offsetBeforeLine.extend(windSpiralPolylineArea2)

                    # primaryOutPt3 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(windSpiral3Bearing - math.pi / 2), asw2.Metres)
                    primaryOutPt2 = MathHelper.getIntersectionPoint(windSpiral2ContactPt, MathHelper.distanceBearingPoint(windSpiral2ContactPt, MathHelper.smethod_4(windSpiral3Bearing - joinAngleRad), 100.0),
                                                                    primaryOutPt3, MathHelper.distanceBearingPoint(primaryOutPt3, MathHelper.smethod_4(windSpiral3Bearing + math.pi), 100.0))

                primaryPolylineArea.method_1(primaryOutPt2)
                primaryPolylineArea.method_1(primaryOutPt3)
                primaryPoylineOut.method_1(primaryOutPt2)
                primaryPoylineOut.method_1(primaryOutPt3)
                offsetBeforeLine.method_1(primaryOutPt2)

                primaryPolylineArea.method_1(point3d_Wpt2)

                joinBearingIn = MathHelper.getBearing(ptEK, point3d_Wpt2)
                primaryPoylineIn = PolylineArea()
                primaryInPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(joinBearingIn + math.pi / 2), asw2.Metres)
                primaryInPt2 = MathHelper.getIntersectionPoint(primaryInPt1, MathHelper.distanceBearingPoint(primaryInPt1, MathHelper.smethod_4(joinBearingIn + math.pi), 100),
                                                               ptEK, MathHelper.distanceBearingPoint(ptEK, MathHelper.smethod_4(joinBearingIn + joinAngleRad), 100))
                primaryPolylineArea.method_1(primaryInPt1)
                primaryPolylineArea.method_1(primaryInPt2)
                primaryPoylineIn.method_1(primaryInPt1)
                primaryPoylineIn.method_1(primaryInPt2)

                primaryPolylineArea.method_1(ptEK)
                resultPolylineAreList.append(primaryPolylineArea)

                #### Create SecondaryArea1
                secondaryPolylineArea = PolylineArea()
                secondaryPolylineArea.method_1(primaryOutPt1)

                offsetAfterLine = offsetBeforeLine.method_23(distP_S, OffsetGapType.Fillet)
                secondaryPolylineArea.extend(offsetAfterLine)

                ptArray = secondaryPolylineArea.method_14(4)
                p = ptArray[len(ptArray) - 1]
                secondaryOutPt3 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(windSpiral3Bearing - math.pi / 2), asw2.Metres + asw1.Metres)
                secondaryOutPt2 = MathHelper.getIntersectionPoint(p, MathHelper.distanceBearingPoint(p, MathHelper.smethod_4(windSpiral3Bearing - joinAngleRad), 100.0),
                                                                secondaryOutPt3, MathHelper.distanceBearingPoint(secondaryOutPt3, MathHelper.smethod_4(windSpiral3Bearing + math.pi), 100.0))
                secondaryPolylineArea.method_1(secondaryOutPt2)
                secondaryPolylineArea.method_1(secondaryOutPt3)

                tempPolylineArea = PolylineArea(primaryPoylineOut.method_14())
                tempPolylineArea.reverse()
                secondaryPolylineArea.extend(tempPolylineArea)
                #
                resultPolylineAreList.append(secondaryPolylineArea)

                #### Create SecondaryArea2
                secondaryPolylineArea2 = PolylineArea()
                secondaryPolylineArea2.method_1(primaryInPt1)
                secondaryPolylineArea2.method_1(primaryInPt2)

                secondaryInPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(MathHelper.getBearing(ptEK, point3d_Wpt2) + math.pi / 2), asw2.Metres + asw1.Metres)

                secondaryPolylineArea2.method_1(MathHelper.getIntersectionPoint(primaryInPt2, MathHelper.distanceBearingPoint(primaryInPt2, MathHelper.getBearing(ptEK, primaryInPt2), 100),
                                                                               secondaryInPt1, MathHelper.distanceBearingPoint(secondaryInPt1, MathHelper.smethod_4(MathHelper.getBearing(ptEK, point3d_Wpt2) + math.pi), 100)))
                secondaryPolylineArea2.method_1(secondaryInPt1)
                secondaryPolylineArea2.method_1(primaryInPt1)
                resultPolylineAreList.append(secondaryPolylineArea2)

                complexObstacleArea.append(PrimaryObstacleArea(primaryPolylineArea))
                complexObstacleArea.append(SecondaryObstacleAreaWithManyPoints(secondaryPolylineArea, primaryPoylineOut))
                complexObstacleArea.append(SecondaryObstacleAreaWithManyPoints(secondaryPolylineArea2, primaryPoylineIn))

            else:
                primaryPoylineOut = PolylineArea()
                offsetBeforeLine = PolylineArea()
                distP_S = MathHelper.calcDistance(point3d_Wpt1, point3dLatest) * math.tan(joinAngleRad)
                secondaryStartPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackPlus90, asw1.Metres + distP_S)
                startPt1 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackPlus90, asw1.Metres)
                primaryPolylineArea = PolylineArea()
                primaryOutPt1 = MathHelper.getIntersectionPoint(secondaryStartPt1, MathHelper.distanceBearingPoint(secondaryStartPt1, MathHelper.smethod_4(inboundTrackPlus180 + joinAngleRad), 100.0),
                                                       startPt1, MathHelper.distanceBearingPoint(startPt1, inboundTrackPlus180, 100.0))

                ptEK = MathHelper.getIntersectionPoint(primaryOutPt1, MathHelper.distanceBearingPoint(primaryOutPt1, MathHelper.smethod_4(inboundTrackPlus180 + joinAngleRad), 100.0),
                                                       point3dEarliest, MathHelper.distanceBearingPoint(point3dEarliest, inboundTrackPlus90, 100.0))
                primaryPolylineArea.method_1(ptEK)
                primaryPolylineArea.method_1(primaryOutPt1)
                primaryPoylineOut.method_1(primaryOutPt1)


                windSpiral1 = WindSpiral(startPt1, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                p, windSpiralContactPt1, windSpiralMiddlePt1 = windSpiral1.getContactWithBearingOfTangent(inboundTrackMinus90, 1, turnDirection)
                point3dArray = [windSpiral1.Start[0], windSpiralContactPt1]
                windSpiralPolylineArea1 = PolylineArea(point3dArray)
                windSpiralPolylineArea1.SetBulgeAt(0, MathHelper.smethod_60(windSpiral1.Start[0], windSpiralMiddlePt1, windSpiralContactPt1))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                primaryPolylineArea.extend(windSpiralPolylineArea1)
                primaryPoylineOut.extend(windSpiralPolylineArea1)
                offsetBeforeLine.extend(windSpiralPolylineArea1)

                startPt2 = MathHelper.distanceBearingPoint(point3dLatest, inboundTrackMinus90, asw1.Metres)
                windSpiral2 = WindSpiral(startPt2, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)

                startPt3 = MathHelper.distanceBearingPoint(primaryOutPt1, inboundTrackMinus90, asw1.Metres * 2)
                windSpiral3 = WindSpiral(startPt3, inboundTrack, speedTas, speedWind, valueBankAngle, turnDirection)
                windSpiral3Bearing = windSpiral3.getBearingOfTangentWithOutPt(point3d_Wpt2, 1, turnDirection)
                pt, windSpiral2ContactStartPt, p = windSpiral2.getContactWithBearingOfTangent(inboundTrackMinus90, 1, turnDirection)

                p, windSpiral2ContactPt, windSpiral2MiddlePt = windSpiral2.getContactWithBearingOfTangent(MathHelper.smethod_4(windSpiral3Bearing + joinAngleRad), 1, turnDirection)
                point3dArray = [windSpiral2ContactStartPt, windSpiral2ContactPt]
                windSpiralPolylineArea2 = PolylineArea(point3dArray)
                windSpiralPolylineArea2.SetBulgeAt(0, MathHelper.smethod_60(windSpiral2ContactStartPt, windSpiral2MiddlePt, windSpiral2ContactPt))#, windSpiral.Middle[0], windSpiral.Finish[0]))
                primaryPolylineArea.extend(windSpiralPolylineArea2)
                primaryPoylineOut.extend(windSpiralPolylineArea2)
                offsetBeforeLine.extend(windSpiralPolylineArea2)

                primaryOutPt3 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(windSpiral3Bearing + math.pi / 2), asw2.Metres)
                primaryOutPt2 = MathHelper.getIntersectionPoint(windSpiral2ContactPt, MathHelper.distanceBearingPoint(windSpiral2ContactPt, MathHelper.smethod_4(windSpiral3Bearing + joinAngleRad), 100.0),
                                                                primaryOutPt3, MathHelper.distanceBearingPoint(primaryOutPt3, MathHelper.smethod_4(windSpiral3Bearing + math.pi), 100.0))

                primaryPolylineArea.method_1(primaryOutPt2)
                primaryPolylineArea.method_1(primaryOutPt3)
                primaryPoylineOut.method_1(primaryOutPt2)
                primaryPoylineOut.method_1(primaryOutPt3)
                offsetBeforeLine.method_1(primaryOutPt2)

                primaryPolylineArea.method_1(point3d_Wpt2)

                joinBearingIn = MathHelper.getBearing(ptEK, point3d_Wpt2)
                primaryPoylineIn = PolylineArea()
                primaryInPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(joinBearingIn - math.pi / 2), asw2.Metres)
                primaryInPt2 = MathHelper.getIntersectionPoint(primaryInPt1, MathHelper.distanceBearingPoint(primaryInPt1, MathHelper.smethod_4(joinBearingIn + math.pi), 100),
                                                               ptEK, MathHelper.distanceBearingPoint(ptEK, MathHelper.smethod_4(joinBearingIn - joinAngleRad), 100))
                primaryPolylineArea.method_1(primaryInPt1)
                primaryPolylineArea.method_1(primaryInPt2)
                primaryPoylineIn.method_1(primaryInPt1)
                primaryPoylineIn.method_1(primaryInPt2)

                primaryPolylineArea.method_1(ptEK)
                resultPolylineAreList.append(primaryPolylineArea)

                #### Create SecondaryArea1
                secondaryPolylineArea = PolylineArea()
                secondaryPolylineArea.method_1(primaryOutPt1)

                offsetAfterLine = offsetBeforeLine.method_23(-distP_S, OffsetGapType.Fillet)
                offsetAfterLine.reverse()
                secondaryPolylineArea.extend(offsetAfterLine)

                ptArray = secondaryPolylineArea.method_14(4)
                p = ptArray[len(ptArray) - 1]
                secondaryOutPt3 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(windSpiral3Bearing + math.pi / 2), asw2.Metres + asw1.Metres)
                secondaryOutPt2 = MathHelper.getIntersectionPoint(p, MathHelper.distanceBearingPoint(p, MathHelper.smethod_4(windSpiral3Bearing + joinAngleRad), 100.0),
                                                                secondaryOutPt3, MathHelper.distanceBearingPoint(secondaryOutPt3, MathHelper.smethod_4(windSpiral3Bearing + math.pi), 100.0))
                secondaryPolylineArea.method_1(secondaryOutPt2)
                secondaryPolylineArea.method_1(secondaryOutPt3)

                tempPolylineArea = PolylineArea(primaryPoylineOut.method_14())
                tempPolylineArea.reverse()
                secondaryPolylineArea.extend(tempPolylineArea)
                #
                resultPolylineAreList.append(secondaryPolylineArea)

                #### Create SecondaryArea2
                secondaryPolylineArea2 = PolylineArea()
                secondaryPolylineArea2.method_1(primaryInPt1)
                secondaryPolylineArea2.method_1(primaryInPt2)

                secondaryInPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, MathHelper.smethod_4(joinBearingIn - math.pi / 2), asw2.Metres + asw1.Metres)

                secondaryPolylineArea2.method_1(MathHelper.getIntersectionPoint(primaryInPt2, MathHelper.distanceBearingPoint(primaryInPt2, MathHelper.getBearing(ptEK, primaryInPt2), 100),
                                                                               secondaryInPt1, MathHelper.distanceBearingPoint(secondaryInPt1, MathHelper.smethod_4(MathHelper.getBearing(ptEK, point3d_Wpt2) + math.pi), 100)))
                secondaryPolylineArea2.method_1(secondaryInPt1)
                secondaryPolylineArea2.method_1(primaryInPt1)
                resultPolylineAreList.append(secondaryPolylineArea2)

                complexObstacleArea.append(PrimaryObstacleArea(primaryPolylineArea))
                complexObstacleArea.append(SecondaryObstacleAreaWithManyPoints(secondaryPolylineArea, primaryPoylineOut))
                complexObstacleArea.append(SecondaryObstacleAreaWithManyPoints(secondaryPolylineArea2, primaryPoylineIn))


            nominalTrackPolylineArea = PolylineArea()
            pathBearing = 0.0
            if turnDirection == TurnDirection.Right:
                angle = (windSpiral3Bearing - joinBearingIn) / 2
                pathBearing = joinBearingIn + angle
            else:
                angle = (joinBearingIn - windSpiral3Bearing) / 2
                pathBearing = windSpiral3Bearing + angle
            nominalArcStartPt, nominalArcMiddlePt, nominalArcEndPt = MathHelper.getPointsOfArcWithContactPtAndOutPt(point3d_Wpt1, inboundTrack, point3d_Wpt2, pathBearing, turnDirection)
            point3dArray = [nominalArcStartPt, nominalArcEndPt]
            nominalTrackPolylineArea = PolylineArea(point3dArray)
            nominalTrackPolylineArea.SetBulgeAt(0, MathHelper.smethod_60(nominalArcStartPt, nominalArcMiddlePt, nominalArcEndPt))#, windSpiral.Middle[0], windSpiral.Finish[0]))
            nominalTrackPolylineArea.method_1(point3d_Wpt2)
            resultPolylineAreList.append(nominalTrackPolylineArea)











        return complexObstacleArea, resultPolylineAreList





    def circularArcMethod(self, point3d_Wpt1, point3d_Wpt2, inboundTrack, outboundTrack, rnavGnssTolerance1, rnavGnssTolerance2, turnDirection):
        inboundTrackMinus90 = MathHelper.smethod_4(inboundTrack - math.pi / 2)
        inboundTrackPlus90 = MathHelper.smethod_4(inboundTrack + math.pi / 2)
        inboundTrackPlus180 = MathHelper.smethod_4(inboundTrack + math.pi)
        outboundTrackMinus90 = MathHelper.smethod_4(outboundTrack - math.pi / 2)
        outboundTrackPlus90 = MathHelper.smethod_4(outboundTrack + math.pi / 2)
        outboundTrackPlus180 = MathHelper.smethod_4(outboundTrack + math.pi)
        complexObstacleArea = ComplexObstacleArea()
        asw1 = rnavGnssTolerance1.ASW / 2
        att1 = rnavGnssTolerance1.ATT
        asw2 = rnavGnssTolerance2.ASW / 2
        att2 = rnavGnssTolerance2.ATT

        resultPolylineAreList = []

        if turnDirection == TurnDirection.Right:
            turnAngleRadian = MathHelper.smethod_4(outboundTrack - inboundTrack)

            primaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres)
            outArcStartPt0 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackMinus90, asw1.Metres)
            outArcEndPt0 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackMinus90, asw1.Metres * math.cos(turnAngleRadian))
            outArcStartPt0, outArcEndPt0, outArcBulge0 = MathHelper.getArcWithTwoContactAndBearing(outArcStartPt0, inboundTrack, outArcEndPt0, MathHelper.getBearing(primaryEndPt1, outArcEndPt0), turnDirection)

            primaryPolylineArea = PolylineArea()
            primaryPolylineArea.method_3(outArcStartPt0, outArcBulge0)
            primaryPolylineArea.method_1(outArcEndPt0)
            primaryPolylineArea.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres))
            primaryPolylineArea.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres))
            primaryPolylineArea.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus90, asw1.Metres * math.cos(turnAngleRadian)))
            primaryPolylineArea.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackPlus90, asw1.Metres / math.cos(turnAngleRadian)))
            primaryPolylineArea.method_1(outArcStartPt0)

            primaryPolyline0 = PolylineArea()
            primaryPolyline0.method_3(outArcStartPt0, outArcBulge0)
            primaryPolyline0.method_1(outArcEndPt0)
            primaryPolyline0.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres))
            primaryPolyline1 = PolylineArea()
            primaryPolyline1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres))
            primaryPolyline1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus90, asw1.Metres * math.cos(turnAngleRadian)))
            primaryPolyline1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackPlus90, asw1.Metres / math.cos(turnAngleRadian)))

            complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))
            resultPolylineAreList.append(primaryPolylineArea)

            secondaryEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2)
            outArcStartPt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackMinus90, asw1.Metres * 2)
            outArcEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackMinus90, asw1.Metres * 2 * math.cos(turnAngleRadian))
            outArcStartPt1, outArcEndPt1, outArcBulge1 = MathHelper.getArcWithTwoContactAndBearing(outArcStartPt1, inboundTrack, outArcEndPt1, MathHelper.getBearing(secondaryEndPt1, outArcEndPt1), turnDirection)

            secondaryPolylineArea0 = PolylineArea()
            secondaryPolylineArea0.method_3(outArcStartPt1, outArcBulge1)
            secondaryPolylineArea0.method_1(outArcEndPt1)
            secondaryPolylineArea0.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2))
            secondaryPolylineArea0.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres))
            outArcPointList0 = primaryPolyline0.method_14()
            outArcPointList0.reverse()
            for pt in outArcPointList0:
                secondaryPolylineArea0.method_1(pt)
            secondaryPolylineArea0.method_1(outArcStartPt1)

            complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineArea0, primaryPolyline0, True))
            resultPolylineAreList.append(secondaryPolylineArea0)

            secondaryPolylineArea1 = PolylineArea()
            secondaryPolylineArea1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres))
            secondaryPolylineArea1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2))
            secondaryPolylineArea1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus90, asw1.Metres * 2 * math.cos(turnAngleRadian)))
            secondaryPolylineArea1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackPlus90, asw1.Metres* 2 / math.cos(turnAngleRadian)))
            secondaryPolylineArea1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackPlus90, asw1.Metres / math.cos(turnAngleRadian)))
            secondaryPolylineArea1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus90, asw1.Metres * math.cos(turnAngleRadian)))
            secondaryPolylineArea1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres))
            complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineArea1, primaryPolyline1, True))

            resultPolylineAreList.append(secondaryPolylineArea1)



        else:#if turnDirection == TurnDirection.Left:
            turnAngleRadian = MathHelper.smethod_4(inboundTrack - outboundTrack)

            outArcStartPt0 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackPlus90, asw1.Metres * math.cos(turnAngleRadian))
            outArcEndPt0 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus90, asw1.Metres)
            outArcCenterPt0 = MathHelper.CalcCenter(turnAngleRadian, outArcStartPt0, outArcEndPt0)
            outArcPointList0 = MathHelper.constructArcWithCenterAngle(outArcCenterPt0, MathHelper.calcDistance(outArcStartPt0, outArcCenterPt0), outboundTrackPlus90, turnAngleRadian * 2, 30)
            outArcPointList0.reverse()
            outArcBulge0 = MathHelper.smethod_57(turnDirection, outArcPointList0[0], outArcPointList0[15], outArcPointList0[len(outArcPointList0) - 1])

            primaryPolylineArea = PolylineArea(outArcPointList0)
            primaryPolylineArea.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres))
            primaryPolylineArea.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres))
            primaryPolylineArea.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackMinus90, asw1.Metres * math.cos(turnAngleRadian)))
            primaryPolylineArea.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackMinus90, asw1.Metres / math.cos(turnAngleRadian)))
            primaryPolylineArea.method_1(outArcPointList0[0])
            primaryPolyline0 = PolylineArea(outArcPointList0)
            primaryPolyline0.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres))
            primaryPolyline1 = PolylineArea()
            primaryPolyline1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres))
            primaryPolyline1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackMinus90, asw1.Metres * math.cos(turnAngleRadian)))
            primaryPolyline1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackMinus90, asw1.Metres / math.cos(turnAngleRadian)))

            complexObstacleArea.Add(PrimaryObstacleArea(primaryPolylineArea))
            resultPolylineAreList.append(primaryPolylineArea)

            outArcStartPt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackPlus90, asw1.Metres * 2 * math.cos(turnAngleRadian))
            outArcEndPt1 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus90, asw1.Metres * 2)
            outArcCenterPt1 = MathHelper.CalcCenter(turnAngleRadian, outArcStartPt1, outArcEndPt1)
            outArcPointList1 = MathHelper.constructArcWithCenterAngle(outArcCenterPt1, MathHelper.calcDistance(outArcStartPt1, outArcCenterPt1), outboundTrackPlus90, turnAngleRadian * 2, 30)
            outArcPointList1.reverse()
            outArcBulge1 = MathHelper.smethod_57(turnDirection, outArcPointList1[0], outArcPointList1[15], outArcPointList1[len(outArcPointList0) - 1])

            secondaryPolylineArea0 = PolylineArea()
            secondaryPolylineArea0.method_1(outArcPointList0[0])
            for pt in outArcPointList1:
                secondaryPolylineArea0.method_1(pt)
            secondaryPolylineArea0.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres * 2))
            secondaryPolylineArea0.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackPlus90, asw2.Metres))
            outArcPointList0.reverse()
            for pt in outArcPointList0:
                secondaryPolylineArea0.method_1(pt)
            complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineArea0, primaryPolyline0, True))
            resultPolylineAreList.append(secondaryPolylineArea0)

            secondaryPolylineArea1 = PolylineArea()
            secondaryPolylineArea1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres))
            secondaryPolylineArea1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres * 2))
            secondaryPolylineArea1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackMinus90, asw1.Metres * 2 * math.cos(turnAngleRadian)))
            secondaryPolylineArea1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackMinus90, asw1.Metres* 2 / math.cos(turnAngleRadian)))
            secondaryPolylineArea1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrackMinus90, asw1.Metres / math.cos(turnAngleRadian)))
            secondaryPolylineArea1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackMinus90, asw1.Metres * math.cos(turnAngleRadian)))
            secondaryPolylineArea1.method_1(MathHelper.distanceBearingPoint(point3d_Wpt2, outboundTrackMinus90, asw2.Metres))
            complexObstacleArea.Add(SecondaryObstacleAreaWithManyPoints(secondaryPolylineArea1, primaryPolyline1, True))
            resultPolylineAreList.append(secondaryPolylineArea1)

        rnavWaypointType1 = self.method_33()
        turnAngle = MathHelper.smethod_76(Unit.smethod_1(inboundTrack), Unit.smethod_1(outboundTrack), AngleUnits.Degrees)
        turnAngleRad = Unit.ConvertDegToRad(turnAngle)
        joinAngleRad = Unit.ConvertDegToRad(30)
        speedTas = Speed.smethod_0(self.parametersPanel.pnlIas.Value, self.parametersPanel.pnlIsa.Value, self.parametersPanel.pnlAltitude.Value)
        speedWind = self.parametersPanel.pnlWind.Value
        valueBankAngle = self.parametersPanel.pnlBankAngle.Value
        distance = Distance.smethod_0(speedTas, valueBankAngle)
        metres3 = distance.Metres
        distance = RnavWaypoints.getDistanceFromWaypointToEarliestTurningPoint(rnavWaypointType1, Distance(att1.Metres), Distance(metres3), turnAngle, AngleUnits.Degrees)
        distFromWpt1ToEarliest = distance.Metres
        point3dEarliest = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, math.fabs(distFromWpt1ToEarliest)) if (distFromWpt1ToEarliest >= 0) else MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack, math.fabs(distFromWpt1ToEarliest))
        distance = RnavWaypoints.getDistanceFromWaypointToLatestTurningPoint(rnavWaypointType1, speedTas, speedWind, float(self.parametersPanel.pnlPilotTime.Value), float(self.parametersPanel.pnlBankEstTime.Value), Distance(att1.Metres), Distance(metres3), turnAngle, AngleUnits.Degrees)
        distFromWpt1ToLatest = distance.Metres
        point3dLatest = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, math.fabs(distFromWpt1ToLatest)) if (distFromWpt1ToLatest >= 0) else MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrack, math.fabs(distFromWpt1ToLatest))


        nominalTrackPolylineArea = PolylineArea()
        num19 = metres3 * math.tan(Unit.ConvertDegToRad(turnAngle / 2))
        if (self.parametersPanel.chbCatH.Checked):
            metresPerSecond1 = 3 * speedTas.MetresPerSecond
            num = metresPerSecond1
        else:
            metresPerSecond1 = 5 * speedTas.MetresPerSecond
            num = metresPerSecond1
        num = metresPerSecond1

        point3d33 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, num19)
        point3d34 = MathHelper.distanceBearingPoint(point3d33, inboundTrackPlus90, 100)
        point3d35 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrack, num19)
        point3d36 = MathHelper.distanceBearingPoint(point3d35, outboundTrackPlus90, 100)
        point3d2 = MathHelper.getIntersectionPoint(point3d33, point3d34, point3d35, point3d36)
        point3d33 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, num19 + num)
        point3d34 = MathHelper.distanceBearingPoint(point3d_Wpt1, inboundTrackPlus180, num19)
        point3d35 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrack, num19)
        point3d36 = MathHelper.distanceBearingPoint(point3d_Wpt1, outboundTrack, num19 + num)
        nominalTrackPolylineArea.method_1(point3d33)
        nominalTrackPolylineArea.Add(PolylineAreaPoint(point3d34, MathHelper.smethod_57(turnDirection, point3d34, point3d35, point3d2)))
        nominalTrackPolylineArea.method_1(point3d35)
        nominalTrackPolylineArea.method_1(point3d36)
        if self.parametersPanel.rdnDF.isChecked():
            nominalTrackPolylineArea.method_1(point3d_Wpt2)

        resultPolylineAreList.append(nominalTrackPolylineArea)
        return complexObstacleArea, resultPolylineAreList











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
        ui = Ui_TurnProtectionAndObstacleAssessment()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.pnlWind.setAltitude(self.parametersPanel.pnlAltitude.Value)

        self.parametersPanel.cmbSelectionMode.Items = ["Automatic", "Manual"]

        self.parametersPanel.cmbConstructionType.Items = ["2D", "3D"]
        self.parametersPanel.cmbType1.Items = ["Fly-By", "Fly-Over", "RF"]
        self.parametersPanel.cmbType2.Items = ["Fly-By", "Fly-Over", "RF"]

        self.parametersPanel.cmbRnavSpecification.Items = ["", "Rnav5", "Rnav2", "Rnav1", "Rnp4", "Rnp2", "Rnp1", "ARnp2", "ARnp1", "ARnp09", "ARnp08", "ARnp07", "ARnp06", "ARnp05", "ARnp04", "ARnp03", "RnpApch"]


        self.connect(self.parametersPanel.pnlAltitude, SIGNAL("Event_0"), self.altitudeChanged)
        self.connect(self.parametersPanel.pnlIas, SIGNAL("Event_0"), self.altitudeChanged)
        self.connect(self.parametersPanel.pnlIsa, SIGNAL("Event_0"), self.altitudeChanged)
        self.connect(self.parametersPanel.chbUseTwoWpt, SIGNAL("Event_0"), self.method_31)
        self.connect(self.parametersPanel.cmbConstructionType, SIGNAL("Event_0"), self.method_31)
        self.connect(self.parametersPanel.cmbRnavSpecification, SIGNAL("Event_0"), self.cmbRnavSpecificationChangeed)
        self.connect(self.parametersPanel.cmbPhaseOfFlight, SIGNAL("Event_0"), self.cmbPhaseOfFlightChanged)
        self.connect(self.parametersPanel.cmbSelectionMode, SIGNAL("Event_0"), self.manualEvent)
        self.connect(self.parametersPanel.chbCatH, SIGNAL("Event_0"), self.method_31)
        self.connect(self.parametersPanel.cmbType1, SIGNAL("Event_0"), self.setOutBoundTrack)
        self.connect(self.parametersPanel.cmbType2, SIGNAL("Event_0"), self.setOutBoundTrack)

        self.connect(self.parametersPanel.pnlWaypoint1, SIGNAL("positionChanged"), self.setOutBoundTrack)
        self.connect(self.parametersPanel.pnlWaypoint2, SIGNAL("positionChanged"), self.setOutBoundTrack)
        self.parametersPanel.rdnDF.clicked.connect(self.courseTypeChanged)
        self.parametersPanel.rdnTF.clicked.connect(self.courseTypeChanged)
        self.parametersPanel.rdnCF.clicked.connect(self.courseTypeChanged)

        self.method_31()
        self.altitudeChanged()
        self.method_35(-1)

        self.courseTypeChanged()
    def courseTypeChanged(self):
        if self.parametersPanel.rdnDF.isChecked() or self.parametersPanel.rdnTF.isChecked():
            self.parametersPanel.pnlOutbound.Enabled = False
            self.setOutBoundTrack()
        else:
            self.parametersPanel.pnlOutbound.Enabled = True
    def setOutBoundTrack(self):
        try:
            ptWpt1 = self.parametersPanel.pnlWaypoint1.Point3d
            ptWpt2 = self.parametersPanel.pnlWaypoint2.Point3d
            self.parametersPanel.pnlOutbound.Value = Unit.ConvertRadToDeg(MathHelper.getBearing(ptWpt1, ptWpt2))
        except:
            pass


    def cmbRnavSpecificationChangeed(self):
        self.method_34(-1)
        self.method_35(-1)
        self.method_31()

        # self.toleranceChange(self.parametersPanel.cmbRnavSpecification.SelectedItem, self.parametersPanel.chbCatH.Checked)

    def toleranceChange(self, rnavSpacificationType, catHchecked = False):
        xtt = 0.0
        att = 0.0
        asw = 0.0
        if not catHchecked:
            if rnavSpacificationType == RnavSpecification.Rnav5:
                att = 2.01
                xtt = 2.51
                asw = 5.76
            elif rnavSpacificationType == RnavSpecification.Rnav2 or rnavSpacificationType == RnavSpecification.Rnav1:
                att = 1.6
                xtt = 2.0
                asw = 5.0
            elif rnavSpacificationType == RnavSpecification.Rnp4:
                att = 3.2
                xtt = 4.0
                asw = 8.0
            elif rnavSpacificationType == RnavSpecification.Rnp2:
                att = 1.6
                xtt = 2.0
                asw = 5.0
            elif rnavSpacificationType == RnavSpecification.Rnp1:
                att = 0.8
                xtt = 1.0
                asw = 3.5
            elif rnavSpacificationType == RnavSpecification.ARnp2:
                att = 0.8
                xtt = 1.0
                asw = 3.5
            else:
                att = 0.8
                xtt = 1.0
                asw = 2.0
        else:
            if rnavSpacificationType == RnavSpecification.Rnav5:
                att = 2.01
                xtt = 2.51
                asw = 4.76
            elif rnavSpacificationType == RnavSpecification.Rnav2 or rnavSpacificationType == RnavSpecification.Rnav1:
                att = 1.6
                xtt = 2.0
                asw = 4.0
            elif rnavSpacificationType == RnavSpecification.Rnp4:
                att = 3.2
                xtt = 4.0
                asw = 7.0
            elif rnavSpacificationType == RnavSpecification.Rnp2:
                att = 1.6
                xtt = 2.0
                asw = 7.0
            elif rnavSpacificationType == RnavSpecification.Rnp1:
                att = 0.8
                xtt = 1.0
                asw = 2.5
            else:
                att = 0.8
                xtt = 1.0
                asw = 2.0
        self.parametersPanel.pnlTolerances.ATT = Distance(att, DistanceUnits.NM)
        self.parametersPanel.pnlTolerances.XTT = Distance(xtt, DistanceUnits.NM)
        self.parametersPanel.pnlTolerances.ASW = Distance(asw, DistanceUnits.NM)

        self.parametersPanel.pnlTolerances2.ATT = Distance(att, DistanceUnits.NM)
        self.parametersPanel.pnlTolerances2.XTT = Distance(xtt, DistanceUnits.NM)
        self.parametersPanel.pnlTolerances2.ASW = Distance(asw, DistanceUnits.NM)

    def cmbPhaseOfFlightChanged(self):
        self.method_35(-1)
        self.method_31()
        # self.toleranceChange(self.parametersPanel.cmbRnavSpecification.SelectedItem, self.parametersPanel.chbCatH.Checked)

    def altitudeChanged(self):
        self.parametersPanel.pnlWind.setAltitude(self.parametersPanel.pnlAltitude.Value)
        try:
            self.parametersPanel.pnlTas.Value = Speed.smethod_0(self.parametersPanel.pnlIas.Value, self.parametersPanel.pnlIsa.Value, self.parametersPanel.pnlAltitude.Value)
        except:
            raise ValueError("Value Invalid")
    def method_31(self):
        self.parametersPanel.cmbPhaseOfFlight.Visible = self.parametersPanel.cmbRnavSpecification.SelectedIndex > 0
        self.parametersPanel.pnlArp.Visible = False if (self.parametersPanel.cmbRnavSpecification.SelectedIndex <= 0 or self.parametersPanel.cmbPhaseOfFlight.SelectedIndex < 0) else self.phaseOfFlight != RnavFlightPhase.Enroute
        self.parametersPanel.chbDrawTolerance.Visible = self.parametersPanel.cmbConstructionType.SelectedItem == ConstructionType.Construct2D
        self.parametersPanel.gbWaypoint2.Visible = self.parametersPanel.chbUseTwoWpt.Checked
        self.parametersPanel.frmRadioBtns.Visible = self.parametersPanel.chbUseTwoWpt.Checked
        self.parametersPanel.gbWaypoint1.Caption = "Waypoint1" if self.parametersPanel.chbUseTwoWpt.Checked else "Waypoint"
        rnavTolerance = None
        if self.parametersPanel.cmbRnavSpecification.SelectedIndex > 0 and self.parametersPanel.cmbPhaseOfFlight.SelectedIndex >= 0:
            if (self.parametersPanel.chbCatH.Checked):
                rnavTolerance = RnavGnssTolerance(self.parametersPanel.cmbRnavSpecification.SelectedItem, self.phaseOfFlight, AircraftSpeedCategory.H)
            else:
                rnavTolerance = RnavGnssTolerance(self.parametersPanel.cmbRnavSpecification.SelectedItem, self.phaseOfFlight, AircraftSpeedCategory.C)

            self.parametersPanel.pnlTolerances.ATT = Distance(round(rnavTolerance.ATT.NauticalMiles, 2), DistanceUnits.NM)
            self.parametersPanel.pnlTolerances.XTT = Distance(round(rnavTolerance.XTT.NauticalMiles, 2), DistanceUnits.NM)
            self.parametersPanel.pnlTolerances.ASW = Distance(round(rnavTolerance.ASW.NauticalMiles, 2), DistanceUnits.NM)

            self.parametersPanel.pnlTolerances2.ATT = Distance(round(rnavTolerance.ATT.NauticalMiles, 2), DistanceUnits.NM)
            self.parametersPanel.pnlTolerances2.XTT = Distance(round(rnavTolerance.XTT.NauticalMiles, 2), DistanceUnits.NM)
            self.parametersPanel.pnlTolerances2.ASW = Distance(round(rnavTolerance.ASW.NauticalMiles, 2), DistanceUnits.NM)
        else:
            att = 0.8
            xtt = 1.0
            asw = 2.0
            self.parametersPanel.pnlTolerances.ATT = Distance(att, DistanceUnits.NM)
            self.parametersPanel.pnlTolerances.XTT = Distance(xtt, DistanceUnits.NM)
            self.parametersPanel.pnlTolerances.ASW = Distance(asw, DistanceUnits.NM)

            self.parametersPanel.pnlTolerances2.ATT = Distance(att, DistanceUnits.NM)
            self.parametersPanel.pnlTolerances2.XTT = Distance(xtt, DistanceUnits.NM)
            self.parametersPanel.pnlTolerances2.ASW = Distance(asw, DistanceUnits.NM)
        phaseOfFlightType = self.parametersPanel.cmbPhaseOfFlight.SelectedItem
        if phaseOfFlightType != None:
            if phaseOfFlightType.contains("EN-ROUTE"):
                self.parametersPanel.pnlBankAngle.Value = 15
                self.parametersPanel.pnlBankEstTime.Value = 5
                self.parametersPanel.pnlPilotTime.Value = 10
            elif phaseOfFlightType.contains("STAR"):
                self.parametersPanel.pnlBankAngle.Value = 25
                self.parametersPanel.pnlBankEstTime.Value = 5
                self.parametersPanel.pnlPilotTime.Value = 6
            elif phaseOfFlightType.contains("SID"):
                self.parametersPanel.pnlBankAngle.Value = 25
                self.parametersPanel.pnlBankEstTime.Value = 3
                self.parametersPanel.pnlPilotTime.Value = 3
            elif phaseOfFlightType.contains("IAF") or phaseOfFlightType.contains("FAF") or phaseOfFlightType.contains("IF"):
                self.parametersPanel.pnlBankAngle.Value = 25
                self.parametersPanel.pnlBankEstTime.Value = 5
                self.parametersPanel.pnlPilotTime.Value = 6
            elif phaseOfFlightType.contains("MA"):
                self.parametersPanel.pnlBankAngle.Value = 15
                self.parametersPanel.pnlBankEstTime.Value = 3
                self.parametersPanel.pnlPilotTime.Value = 3
    def method_34(self, int_0):
        self.parametersPanel.cmbPhaseOfFlight.Clear()
        rnavSpecification_0 = self.parametersPanel.cmbRnavSpecification.SelectedItem
        phaseOfFlightList = []
        # phaseOfFlightList = RnavGnssTolerance.smethod_0(self.parametersPanel.cmbRnavSpecification.SelectedItem)
        if rnavSpecification_0 == "Rnav5" or rnavSpecification_0 == "Rnav2":
            phaseOfFlightList.append(PhaseOfFlightType.EnrouteMore30)
            phaseOfFlightList.append(PhaseOfFlightType.StarMore30)
            phaseOfFlightList.append(PhaseOfFlightType.SidMore30)
        elif rnavSpecification_0 == "Rnav1":
            phaseOfFlightList.append(PhaseOfFlightType.EnrouteMore30)
            phaseOfFlightList.append(PhaseOfFlightType.StarMore30)
            phaseOfFlightList.append(PhaseOfFlightType.SidMore30)
            phaseOfFlightList.append(PhaseOfFlightType.StarLess30)
            phaseOfFlightList.append(PhaseOfFlightType.SidLess30)
            phaseOfFlightList.append(PhaseOfFlightType.IfIafLess30)
            phaseOfFlightList.append(PhaseOfFlightType.SidLess15)
            phaseOfFlightList.append(PhaseOfFlightType.MaLess15)
        elif rnavSpecification_0 == "Rnp4" or rnavSpecification_0 == "Rnp2":
            phaseOfFlightList.append(PhaseOfFlightType.Enroute)
            phaseOfFlightList.append(PhaseOfFlightType.StarMore30)
            phaseOfFlightList.append(PhaseOfFlightType.SidMore30)
        elif rnavSpecification_0 == "Rnp1":
            phaseOfFlightList.append(PhaseOfFlightType.StarMore30)
            phaseOfFlightList.append(PhaseOfFlightType.SidMore30)
            phaseOfFlightList.append(PhaseOfFlightType.StarLess30)
            phaseOfFlightList.append(PhaseOfFlightType.SidLess30)
            phaseOfFlightList.append(PhaseOfFlightType.SidLess15)
            phaseOfFlightList.append(PhaseOfFlightType.MaLess15)
        elif rnavSpecification_0 == "ARnp2":
            phaseOfFlightList.append(PhaseOfFlightType.Enroute)
        elif rnavSpecification_0 == "ARnp1":
            phaseOfFlightList.append(PhaseOfFlightType.Enroute)
            phaseOfFlightList.append(PhaseOfFlightType.StarMore30)
            phaseOfFlightList.append(PhaseOfFlightType.SidMore30)
            phaseOfFlightList.append(PhaseOfFlightType.StarLess30)
            phaseOfFlightList.append(PhaseOfFlightType.SidLess30)
            phaseOfFlightList.append(PhaseOfFlightType.IfIafLess30)
            phaseOfFlightList.append(PhaseOfFlightType.SidLess15)
            phaseOfFlightList.append(PhaseOfFlightType.MaLess15)
        elif rnavSpecification_0 == "ARnp09" or rnavSpecification_0 == "ARnp08" or rnavSpecification_0 == "ARnp07" or rnavSpecification_0 == "ARnp06" or rnavSpecification_0 == "ARnp05" or rnavSpecification_0 == "ARnp04" or rnavSpecification_0 == "ARnp03":
            phaseOfFlightList.append(PhaseOfFlightType.StarMore30)
            phaseOfFlightList.append(PhaseOfFlightType.SidMore30)
            phaseOfFlightList.append(PhaseOfFlightType.StarLess30)
            phaseOfFlightList.append(PhaseOfFlightType.SidLess30)
            phaseOfFlightList.append(PhaseOfFlightType.IfIafLess30)
            phaseOfFlightList.append(PhaseOfFlightType.SidLess15)
            phaseOfFlightList.append(PhaseOfFlightType.MaLess15)
        elif rnavSpecification_0 == "RnpApch":
            phaseOfFlightList.append(PhaseOfFlightType.IfIafLess30)
            phaseOfFlightList.append(PhaseOfFlightType.MaLess30)
            phaseOfFlightList.append(PhaseOfFlightType.Faf)
            phaseOfFlightList.append(PhaseOfFlightType.Mapt)
            phaseOfFlightList.append(PhaseOfFlightType.MaLess15)
        else:
            return []
        self.parametersPanel.cmbPhaseOfFlight.Items = phaseOfFlightList
    def method_35(self, int_0):
        if (int_0 < 0):
            int_0 = self.parametersPanel.cmbType1.SelectedIndex
        self.parametersPanel.cmbType1.Clear()
        self.parametersPanel.cmbType2.Clear()
        # if (self.parametersPanel.cmbRnavSpecification.SelectedIndex < 1):
        self.parametersPanel.cmbType1.Items = ["Fly-By", "Fly-Over", "RF"]
        self.parametersPanel.cmbType2.Items = ["Fly-By", "Fly-Over", "RF"]
        # elif (self.parametersPanel.cmbPhaseOfFlight.SelectedIndex >= 0):
        #     if self.phaseOfFlight == PhaseOfFlightType.Enroute or self.phaseOfFlight == PhaseOfFlightType.EnrouteMore30:
        #         self.parametersPanel.cmbType1.Items = ["Fly-By"]
        #         self.parametersPanel.cmbType2.Items = ["Fly-By"]
        #     # elif self.phaseOfFlight == RnavFlightPhase.STAR:
        #     else:
        #         self.parametersPanel.cmbType1.Items = ["Fly-By", "Fly-Over", "RF"]
        #         self.parametersPanel.cmbType2.Items = ["Fly-By", "Fly-Over", "RF"]
        self.parametersPanel.cmbType1.SelectedIndex = max([0, min([int_0, self.parametersPanel.cmbType1.Count - 1])])
        self.parametersPanel.cmbType2.SelectedIndex = max([0, min([int_0, self.parametersPanel.cmbType2.Count - 1])])

    def method_37(self, point3d_0, rnavGnssTolerance_0, double_0):
        aTT = rnavGnssTolerance_0.ATT
        point3d = MathHelper.distanceBearingPoint(point3d_0, double_0, aTT.Metres)
        xTT = rnavGnssTolerance_0.XTT
        point3d1 = MathHelper.distanceBearingPoint(point3d, double_0 + math.pi / 2, xTT.Metres)
        distance = rnavGnssTolerance_0.ATT
        point3d2 = MathHelper.distanceBearingPoint(point3d1, double_0 + math.pi, distance.Metres * 2)
        aTT1 = rnavGnssTolerance_0.ATT
        point3d3 = MathHelper.distanceBearingPoint(point3d_0, double_0, aTT1.Metres)
        xTT1 = rnavGnssTolerance_0.XTT
        point3d4 = MathHelper.distanceBearingPoint(point3d3, double_0 - math.pi / 2, xTT1.Metres)
        distance1 = rnavGnssTolerance_0.ATT
        point3d5 = MathHelper.distanceBearingPoint(point3d4, double_0 + math.pi, distance1.Metres * 2)
        point3dArray = [point3d1, point3d2, point3d5, point3d4]
        return Point3dCollection(point3dArray)
    def method_33(self):
        return self.parametersPanel.cmbType1.SelectedIndex
        # return 0 if self.parametersPanel.cmbType1.SelectedIndex != 2 else 2


    def method_39(self, point3d_0, rnavGnssTolerance_0, double_0):
        aTT = rnavGnssTolerance_0.ATT
        point3d = MathHelper.distanceBearingPoint(point3d_0, double_0, aTT.Metres)
        xTT = rnavGnssTolerance_0.XTT
        point3d1 = MathHelper.distanceBearingPoint(point3d, double_0 + math.pi / 2, xTT.Metres)
        distance = rnavGnssTolerance_0.ATT
        point3d2 = MathHelper.distanceBearingPoint(point3d1, double_0 + math.pi, distance.Metres * 2)
        aTT1 = rnavGnssTolerance_0.ATT
        point3d3 = MathHelper.distanceBearingPoint(point3d_0, double_0, aTT1.Metres)
        xTT1 = rnavGnssTolerance_0.XTT
        point3d4 = MathHelper.distanceBearingPoint(point3d3, double_0 - math.pi / 2, xTT1.Metres)
        distance1 = rnavGnssTolerance_0.ATT
        point3d5 = MathHelper.distanceBearingPoint(point3d4, double_0 + math.pi, distance1.Metres * 2)
        point3dArray = [point3d1, point3d2, point3d5, point3d4]
        return Point3dCollection(point3dArray)

    def method_40(self):
        rnavGnssTolerance = None
        rnavGnssTolerance2 = None
        point3d = self.parametersPanel.pnlWaypoint1.Point3d
        Speed.smethod_0(self.parametersPanel.pnlIas.Value, self.parametersPanel.pnlIsa.Value, self.parametersPanel.pnlAltitude.Value)
        num = MathHelper.smethod_3(self.parametersPanel.pnlInbound.Value)
        num1 = MathHelper.smethod_3(self.parametersPanel.pnlOutbound.Value)
        rnavWaypointType = self.method_33()
        turnDirectionList = []
        polylineAreaAAA = PolylineArea()
        num2 = MathHelper.smethod_77(num, num1, AngleUnits.Degrees, turnDirectionList)
        turnDirection_0 = turnDirectionList[0]
        if (num2 > 120 and self.parametersPanel.cmbType1.SelectedIndex == 0):
            QMessageBox.warning(self, "Warning", Messages.ERR_COURSE_CHANGES_GREATER_THAN_120_NOT_ALLOWED)
            return (None, None, None, None, None, None, None, None, None, None)

#             throw new Exception(Messages.ERR_COURSE_CHANGES_GREATER_THAN_120_NOT_ALLOWED)
        num = MathHelper.smethod_4(Unit.ConvertDegToRad(num))
        num1 = MathHelper.smethod_4(Unit.ConvertDegToRad(num1))
        aircraftSpeedCategory = AircraftSpeedCategory.H if (self.parametersPanel.chbCatH.Checked) else AircraftSpeedCategory.C
        if (self.parametersPanel.cmbRnavSpecification.SelectedIndex <= 0):
            rnavGnssTolerance = RnavGnssTolerance(None, None, None, None, self.parametersPanel.pnlTolerances.XTT, self.parametersPanel.pnlTolerances.ATT, self.parametersPanel.pnlTolerances.ASW)
            rnavGnssTolerance2 = RnavGnssTolerance(None, None, None, None, self.parametersPanel.pnlTolerances2.XTT, self.parametersPanel.pnlTolerances2.ATT, self.parametersPanel.pnlTolerances2.ASW)

        else:
            rnavSpecification = self.rnavSpecification
            rnavFlightPhase = self.phaseOfFlight
            rnavGnssTolerance = RnavGnssTolerance(rnavSpecification, None, aircraftSpeedCategory,  rnavFlightPhase, Distance(MathHelper.calcDistance(point3d, self.parametersPanel.pnlArp.Point3d))) if (rnavFlightPhase != RnavFlightPhase.Enroute) else RnavGnssTolerance(rnavSpecification, None, aircraftSpeedCategory, rnavFlightPhase, Distance(50, DistanceUnits.NM))
            rnavGnssTolerance2 = RnavGnssTolerance(rnavSpecification, None, aircraftSpeedCategory,  rnavFlightPhase, Distance(MathHelper.calcDistance(self.parametersPanel.pnlWaypoint2.Point3d, self.parametersPanel.pnlArp.Point3d))) if (rnavFlightPhase != RnavFlightPhase.Enroute) else RnavGnssTolerance(rnavSpecification, None, aircraftSpeedCategory, rnavFlightPhase, Distance(50, DistanceUnits.NM))
        point3dCollection_0 = self.method_39(point3d, rnavGnssTolerance, num)
        # if (num2 <= (60 if (aircraftSpeedCategory == AircraftSpeedCategory.H) else 30) and self.parametersPanel.chbCircularArcs.Checked):
        #     turnConstructionMethod_0 = TurnConstructionMethod.CircularArcs
        #
        #     complexObstacleArea, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4 = self.method_41(point3d, num, num1, rnavGnssTolerance, turnDirection_0)
        #     return (polylineAreaAAA, complexObstacleArea, turnDirection_0, turnConstructionMethod_0, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4, point3dCollection_0)
        if (rnavWaypointType == RnavWaypointType.RF):
            turnConstructionMethod_0 = TurnConstructionMethod.FixedRadius
            complexObstacleArea, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4 = self.method_42(point3d, num, num1, rnavGnssTolerance, turnDirection_0)
            return (polylineAreaAAA, complexObstacleArea, turnDirection_0, turnConstructionMethod_0, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4, point3dCollection_0)
#             return self.method_42(point3d, num, num1, rnavGnssTolerance, (TurnDirection)((int)turnDirection_0), out polylineArea_0, out polylineArea_1, out polylineArea_2, out polylineArea_3, out polylineArea_4)
        turnConstructionMethod_0 = TurnConstructionMethod.BoundingCircles
        polylineAreaAAA, complexObstacleArea, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4 = self.method_43(point3d, num, num1, rnavGnssTolerance, turnDirection_0, rnavGnssTolerance2)
        return (polylineAreaAAA, complexObstacleArea, turnDirection_0, turnConstructionMethod_0, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4, point3dCollection_0)
#         return self.method_43(point3d, num, num1, rnavGnssTolerance, (TurnDirection)((int)turnDirection_0), out polylineArea_0, out polylineArea_1, out polylineArea_2, out polylineArea_3, out polylineArea_4)

    def method_41(self, point3d_0, double_0, double_1, rnavGnssTolerance_0, turnDirection_0):
        point3d = None
        point3d1 = None
        point3d2 = None
        point3d3 = None
        point3d4 = None
        point3d5 = None
        point3d6 = None
        point3d7 = None
        point3d8 = None
        point3d9 = None
        point3d10 = None
        point3d11 = None
        point3d12 = None
        point3d13 = None
        point3d14 = None
        point3d15 = None
        point3d16 = None
        point3d17 = None
        point3d18 = None
        point3d19 = None
        aTT = None
        point3d0 = []
        double0 = double_0
        num = MathHelper.smethod_4(double0 - math.pi / 2)
        num1 = MathHelper.smethod_4(double0 + math.pi / 2)
        num2 = MathHelper.smethod_4(double0 + math.pi)
        double1 = double_1
        num3 = MathHelper.smethod_4(double1 - math.pi / 2)
        num4 = MathHelper.smethod_4(double1 + math.pi / 2)
        num5 = MathHelper.smethod_4(double1 + math.pi)
        complexObstacleArea = ComplexObstacleArea()
        polylineArea_0 = PolylineArea()
        polylineArea_1 = PolylineArea()
        polylineArea_2 = PolylineArea()
        polylineArea_3 = PolylineArea()
        polylineArea_4 = PolylineArea()
        if (turnDirection_0 != TurnDirection.Right):
            aSW = rnavGnssTolerance_0.ASW
            point3d9 = MathHelper.distanceBearingPoint(point3d_0, num1, aSW.Metres / 2)
            aTT = rnavGnssTolerance_0.ATT
            point3d8 = MathHelper.distanceBearingPoint(point3d9, num2, aTT.Metres)
            aTT = rnavGnssTolerance_0.ASW
            point3d10 = MathHelper.distanceBearingPoint(point3d_0, num4, aTT.Metres / 2)
            aTT = rnavGnssTolerance_0.ATT
            point3d11 = MathHelper.distanceBearingPoint(point3d10, double1, aTT.Metres)
            aTT = rnavGnssTolerance_0.ASW
            point3d13 = MathHelper.distanceBearingPoint(point3d_0, num1, aTT.Metres)
            aTT = rnavGnssTolerance_0.ATT
            point3d12 = MathHelper.distanceBearingPoint(point3d13, num2, aTT.Metres)
            aTT = rnavGnssTolerance_0.ASW
            point3d14 = MathHelper.distanceBearingPoint(point3d_0, num4, aTT.Metres)
            aTT = rnavGnssTolerance_0.ATT
            point3d15 = MathHelper.distanceBearingPoint(point3d14, double1, aTT.Metres)
            aTT = rnavGnssTolerance_0.ATT
            point3d20 = MathHelper.distanceBearingPoint(point3d10, num5, aTT.Metres)
            aTT = rnavGnssTolerance_0.ATT
            point3d21 = MathHelper.distanceBearingPoint(point3d14, num5, aTT.Metres)
            point3d18 = MathHelper.getIntersectionPoint(point3d20, point3d21, point3d8, point3d12)
            aTT = rnavGnssTolerance_0.ASW
            point3d22 = MathHelper.distanceBearingPoint(point3d_0, num, aTT.Metres / 2)
            aTT = rnavGnssTolerance_0.ASW
            point3d23 = MathHelper.distanceBearingPoint(point3d_0, num, aTT.Metres)
            point3d = MathHelper.getIntersectionPoint(point3d20, point3d21, point3d22, MathHelper.distanceBearingPoint(point3d22, double0, 100))
            point3d4 = MathHelper.getIntersectionPoint(point3d20, point3d21, point3d23, MathHelper.distanceBearingPoint(point3d23, double0, 100))
            point3d1 = MathHelper.getIntersectionPoint(point3d10, point3d14, point3d22, MathHelper.distanceBearingPoint(point3d22, double0, 100))
            point3d5 = MathHelper.getIntersectionPoint(point3d10, point3d14, point3d23, MathHelper.distanceBearingPoint(point3d23, double0, 100))
            aTT = rnavGnssTolerance_0.ASW
            point3d22 = MathHelper.distanceBearingPoint(point3d_0, num3, aTT.Metres / 2)
            aTT = rnavGnssTolerance_0.ASW
            point3d23 = MathHelper.distanceBearingPoint(point3d_0, num3, aTT.Metres)
            point3d2 = MathHelper.getIntersectionPoint(point3d9, point3d13, point3d22, MathHelper.distanceBearingPoint(point3d22, double1, 100))
            point3d6 = MathHelper.getIntersectionPoint(point3d9, point3d13, point3d23, MathHelper.distanceBearingPoint(point3d23, double1, 100))
            aTT = rnavGnssTolerance_0.ATT
            point3d20 = MathHelper.distanceBearingPoint(point3d9, double0, aTT.Metres)
            aTT = rnavGnssTolerance_0.ATT
            point3d21 = MathHelper.distanceBearingPoint(point3d13, double0, aTT.Metres)
            point3d19 = MathHelper.getIntersectionPoint(point3d20, point3d21, point3d11, point3d15)
            point3d3 = MathHelper.getIntersectionPoint(point3d20, point3d21, point3d22, MathHelper.distanceBearingPoint(point3d22, double1, 100))
            point3d7 = MathHelper.getIntersectionPoint(point3d20, point3d21, point3d23, MathHelper.distanceBearingPoint(point3d23, double1, 100))
            point3d0 = [point3d12, point3d13, point3d14, point3d15]
            polylineArea_3.method_7(point3d0)
            polylineArea_3[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d13, point3d14, point3d_0)
            point3d0 = [point3d8, point3d9, point3d10, point3d11]
            polylineArea_2.method_7(point3d0)
            polylineArea_2[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d9, point3d10, point3d_0)
            point3d0 = [point3d4, point3d5, point3d6, point3d7]
            polylineArea_0.method_7(point3d0)
            point3d0 = [point3d, point3d1, point3d2, point3d3]
            polylineArea_1.method_7(point3d0)
            point3d20 = MathHelper.getIntersectionPoint(point3d, point3d4, point3d_0, MathHelper.distanceBearingPoint(point3d_0, num2, 100))
            point3d21 = MathHelper.getIntersectionPoint(point3d3, point3d7, point3d_0, MathHelper.distanceBearingPoint(point3d_0, double1, 100))
            point3d0 = [point3d20, point3d_0, point3d21]
            polylineArea_4.method_7(point3d0)
            polylineArea = PolylineArea()
            polylineArea.method_1(point3d18)
            polylineArea.method_8(polylineArea_3)
            polylineArea.method_1(point3d19)
            polylineArea.method_8(polylineArea_0.method_17())
            complexObstacleArea.ObstacleArea = PrimaryObstacleArea(polylineArea)
            polylineArea.clear()
            polylineArea.method_1(point3d18)
            polylineArea.method_8(polylineArea_2)
            polylineArea.method_1(point3d19)
            polylineArea.method_8(polylineArea_1.method_17())
            complexObstacleArea.Add(PrimaryObstacleArea(polylineArea))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d8, point3d9, point3d12, point3d13))
            point3d20 = MathHelper.smethod_93(turnDirection_0, point3d9, point3d10, point3d_0)
            point3d21 = MathHelper.smethod_93(turnDirection_0, point3d13, point3d14, point3d_0)
            complexObstacleArea.Add(SecondaryObstacleArea(point3d9, point3d20, point3d10, point3d13, None, point3d21, point3d14))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d10, point3d11, point3d14, point3d15))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d, point3d1, point3d4, point3d5))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d1, point3d2, point3d5, point3d6))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d2, point3d3, point3d6, point3d7))
        else:
            aTT = rnavGnssTolerance_0.ASW
            point3d1 = MathHelper.distanceBearingPoint(point3d_0, num, aTT.Metres / 2)
            distance = rnavGnssTolerance_0.ATT
            point3d = MathHelper.distanceBearingPoint(point3d1, num2, distance.Metres)
            aSW1 = rnavGnssTolerance_0.ASW
            point3d2 = MathHelper.distanceBearingPoint(point3d_0, num3, aSW1.Metres / 2)
            aTT1 = rnavGnssTolerance_0.ATT
            point3d3 = MathHelper.distanceBearingPoint(point3d2, double1, aTT1.Metres)
            distance1 = rnavGnssTolerance_0.ASW
            point3d5 = MathHelper.distanceBearingPoint(point3d_0, num, distance1.Metres)
            aTT2 = rnavGnssTolerance_0.ATT
            point3d4 = MathHelper.distanceBearingPoint(point3d5, num2, aTT2.Metres)
            aSW2 = rnavGnssTolerance_0.ASW
            point3d6 = MathHelper.distanceBearingPoint(point3d_0, num3, aSW2.Metres)
            distance2 = rnavGnssTolerance_0.ATT
            point3d7 = MathHelper.distanceBearingPoint(point3d6, double1, distance2.Metres)
            aTT3 = rnavGnssTolerance_0.ATT
            point3d24 = MathHelper.distanceBearingPoint(point3d2, num5, aTT3.Metres)
            distance3 = rnavGnssTolerance_0.ATT
            point3d25 = MathHelper.distanceBearingPoint(point3d6, num5, distance3.Metres)
            point3d16 = MathHelper.getIntersectionPoint(point3d24, point3d25, point3d, point3d4)
            aSW3 = rnavGnssTolerance_0.ASW
            point3d26 = MathHelper.distanceBearingPoint(point3d_0, num1, aSW3.Metres / 2)
            aSW4 = rnavGnssTolerance_0.ASW
            point3d27 = MathHelper.distanceBearingPoint(point3d_0, num1, aSW4.Metres)
            point3d8 = MathHelper.getIntersectionPoint(point3d24, point3d25, point3d26, MathHelper.distanceBearingPoint(point3d26, double0, 100))
            point3d12 = MathHelper.getIntersectionPoint(point3d24, point3d25, point3d27, MathHelper.distanceBearingPoint(point3d27, double0, 100))
            point3d9 = MathHelper.getIntersectionPoint(point3d2, point3d6, point3d26, MathHelper.distanceBearingPoint(point3d26, double0, 100))
            point3d13 = MathHelper.getIntersectionPoint(point3d2, point3d6, point3d27, MathHelper.distanceBearingPoint(point3d27, double0, 100))
            distance4 = rnavGnssTolerance_0.ASW
            point3d26 = MathHelper.distanceBearingPoint(point3d_0, num4, distance4.Metres / 2)
            aSW5 = rnavGnssTolerance_0.ASW
            point3d27 = MathHelper.distanceBearingPoint(point3d_0, num4, aSW5.Metres)
            point3d10 = MathHelper.getIntersectionPoint(point3d1, point3d5, point3d26, MathHelper.distanceBearingPoint(point3d26, double1, 100))
            point3d14 = MathHelper.getIntersectionPoint(point3d1, point3d5, point3d27, MathHelper.distanceBearingPoint(point3d27, double1, 100))
            aTT4 = rnavGnssTolerance_0.ATT
            point3d24 = MathHelper.distanceBearingPoint(point3d1, double0, aTT4.Metres)
            aTT5 = rnavGnssTolerance_0.ATT
            point3d25 = MathHelper.distanceBearingPoint(point3d5, double0, aTT5.Metres)
            point3d17 = MathHelper.getIntersectionPoint(point3d24, point3d25, point3d3, point3d7)
            point3d11 = MathHelper.getIntersectionPoint(point3d24, point3d25, point3d26, MathHelper.distanceBearingPoint(point3d26, double1, 100))
            point3d15 = MathHelper.getIntersectionPoint(point3d24, point3d25, point3d27, MathHelper.distanceBearingPoint(point3d27, double1, 100))
            point3d0 = [point3d4, point3d5, point3d6, point3d7 ]
            polylineArea_0.method_7(point3d0)
            polylineArea_0[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d5, point3d6, point3d_0)
            point3dArray = [point3d, point3d1, point3d2, point3d3]
            polylineArea_1.method_7(point3dArray)
            polylineArea_1[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d1, point3d2, point3d_0)
            point3dArray1 = [point3d12, point3d13, point3d14, point3d15]
            polylineArea_3.method_7(point3dArray1)
            point3dArray2 = [point3d8, point3d9, point3d10, point3d11]
            polylineArea_2.method_7(point3dArray2)
            point3d24 = MathHelper.getIntersectionPoint(point3d8, point3d12, point3d_0, MathHelper.distanceBearingPoint(point3d_0, num2, 100))
            point3d25 = MathHelper.getIntersectionPoint(point3d11, point3d15, point3d_0, MathHelper.distanceBearingPoint(point3d_0, double1, 100))
            point3d01 = [point3d24, point3d_0, point3d25]
            polylineArea_4.method_7(point3d01)
            polylineArea1 = PolylineArea()
            polylineArea1.method_1(point3d16)
            polylineArea1.method_8(polylineArea_0)
            polylineArea1.method_1(point3d17)
            polylineArea1.method_8(polylineArea_3.method_17())
            complexObstacleArea.ObstacleArea = PrimaryObstacleArea(polylineArea1)
            polylineArea1.clear()
            polylineArea1.method_1(point3d16)
            polylineArea1.method_8(polylineArea_1)
            polylineArea1.method_1(point3d17)
            polylineArea1.method_8(polylineArea_2.method_17())
            complexObstacleArea.Add(PrimaryObstacleArea(polylineArea1))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d, point3d1, point3d4, point3d5))
            point3d24 = MathHelper.smethod_93(turnDirection_0, point3d1, point3d2, point3d_0)
            point3d25 = MathHelper.smethod_93(turnDirection_0, point3d5, point3d6, point3d_0)
            complexObstacleArea.Add(SecondaryObstacleArea(point3d1, point3d24, point3d2, point3d5, None,  point3d25, point3d6))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d2, point3d3, point3d6, point3d7))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d8, point3d9, point3d12, point3d13))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d9, point3d10, point3d13, point3d14))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d10, point3d11, point3d14, point3d15))
        return (complexObstacleArea, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4)

    def method_42(self, point3d_0, double_0, double_1, rnavGnssTolerance_0, turnDirection_0):
        point3d = None
        point3d1 = None
        point3d2 = None
        point3d3 = None
        point3d4 = None
        point3d5 = None
        point3d6 = None
        point3d7 = None
        point3d8 = None
        point3d9 = None
        aSW = None
        point3d0 = None
        double0 = double_0
        num = MathHelper.smethod_4(double0 - math.pi / 2)
        num1 = MathHelper.smethod_4(double0 + math.pi / 2)
        num2 = MathHelper.smethod_4(double0 + math.pi)
        double1 = double_1
        num3 = MathHelper.smethod_4(double1 - math.pi / 2)
        num4 = MathHelper.smethod_4(double1 + math.pi / 2)
        MathHelper.smethod_4(double1 + math.pi)
        speed = Speed.smethod_0(self.parametersPanel.pnlIas.Value, self.parametersPanel.pnlIsa.Value, self.parametersPanel.pnlAltitude.Value)
        value = self.parametersPanel.pnlBankAngle.Value
        knots = speed.Knots
        value1 = self.parametersPanel.pnlWind.Value
        num5 = Unit.ConvertNMToMeter(math.pow(knots + value1.Knots, 2) / (68626 * math.tan(Unit.ConvertDegToRad(value))))
        if (num5 < rnavGnssTolerance_0.ASW.Metres):
            obj = num5
            aSW = rnavGnssTolerance_0.ASW
            sss = str(aSW.Meters) + "m"
            QMessageBox.warning(self, "Warning", "The calculated radius of %f m cannot be smaller than 1/2 AW (%s)"%obj%sss)
#             throw new Exception(string.Format("The calculated radius of {0} m cannot be smaller than 1/2 AW ({1})", obj, aSW.method_0(":m")))
        num6 = MathHelper.smethod_76(double0, double1, AngleUnits.Radians)
        complexObstacleArea = ComplexObstacleArea()
        polylineArea_0 = PolylineArea()
        polylineArea_1 = PolylineArea()
        polylineArea_2 = PolylineArea()
        polylineArea_3 = PolylineArea()
        polylineArea_4 = PolylineArea()
        metres = rnavGnssTolerance_0.BV.Metres
        aSW = rnavGnssTolerance_0.XTT
        metres1 = num5 - (1.5 * aSW.Metres + metres)
        aSW = rnavGnssTolerance_0.XTT
        metres2 = num5 - (0.75 * aSW.Metres + metres / 2)
        aSW = rnavGnssTolerance_0.XTT
        metres3 = num5 + (0.75 * aSW.Metres + metres / 2 + 93)
        aSW = rnavGnssTolerance_0.XTT
        metres4 = num5 + (1.5 * aSW.Metres + metres + 186)
        if (turnDirection_0 != TurnDirection.Right):
            point3d10 = MathHelper.distanceBearingPoint(point3d_0, num, num5)
            point3d11 = MathHelper.distanceBearingPoint(point3d10, num4, num5)
            aSW = rnavGnssTolerance_0.ATT
            point3d12 = MathHelper.distanceBearingPoint(point3d_0, num2, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            point3d13 = MathHelper.distanceBearingPoint(point3d12, num, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            point3d14 = MathHelper.distanceBearingPoint(point3d12, num, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d15 = MathHelper.distanceBearingPoint(point3d12, num1, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d16 = MathHelper.distanceBearingPoint(point3d12, num1, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            point3d17 = MathHelper.distanceBearingPoint(point3d_0, num, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            point3d18 = MathHelper.distanceBearingPoint(point3d_0, num, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d19 = MathHelper.distanceBearingPoint(point3d_0, num1, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d20 = MathHelper.distanceBearingPoint(point3d_0, num1, aSW.Metres)
            point3d21 = point3d17
            point3d22 = point3d18
            point3d5_6 = []
            MathHelper.smethod_34(point3d15, point3d19, point3d10, metres3, point3d5_6)
            point3d5 = point3d5_6[0]
            point3d6 = point3d5_6[1]
            point3d5_7 = []
            MathHelper.smethod_34(point3d16, point3d20, point3d10, metres4, point3d5_7)
            point3d5 = point3d5_7[0]
            point3d7 = point3d5_7[1]
            aSW = rnavGnssTolerance_0.ASW
            point3d23 = MathHelper.distanceBearingPoint(point3d11, num3, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            point3d24 = MathHelper.distanceBearingPoint(point3d11, num3, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d25 = MathHelper.distanceBearingPoint(point3d11, num4, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d26 = MathHelper.distanceBearingPoint(point3d11, num4, aSW.Metres)
            point3d12 = MathHelper.distanceBearingPoint(point3d11, double1, 500)
            aSW = rnavGnssTolerance_0.ASW
            MathHelper.distanceBearingPoint(point3d12, num3, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            MathHelper.distanceBearingPoint(point3d12, num3, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d27 = MathHelper.distanceBearingPoint(point3d12, num4, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d28 = MathHelper.distanceBearingPoint(point3d12, num4, aSW.Metres)
            point3d29 = point3d23
            point3d30 = point3d24
            point3d5_8 = []
            MathHelper.smethod_34(point3d25, point3d27, point3d10, metres3, point3d5_8)
            point3d5 = point3d5_8[0]
            point3d8 = point3d5_8[1]
            point3d5_9 = []
            MathHelper.smethod_34(point3d26, point3d28, point3d10, metres4, point3d5_9)
            point3d5 = point3d5_9[0]
            point3d9 = point3d5_9[1]
            aSW = rnavGnssTolerance_0.ASW
            point3d12 = MathHelper.distanceBearingPoint(point3d9, num3, aSW.Metres)
            aSW = rnavGnssTolerance_0.ATT
            point3d12 = MathHelper.distanceBearingPoint(point3d12, double1, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            point3d31 = MathHelper.distanceBearingPoint(point3d12, num3, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            point3d32 = MathHelper.distanceBearingPoint(point3d12, num3, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d33 = MathHelper.distanceBearingPoint(point3d12, num4, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d34 = MathHelper.distanceBearingPoint(point3d12, num4, aSW.Metres)
            point3d0 = [point3d16, point3d7, point3d9, point3d34]
            polylineArea_0.method_7(point3d0)
            polylineArea_0[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d7, point3d9, point3d10)
            point3d0 = [point3d15, point3d6, point3d8, point3d33]
            polylineArea_1.method_7(point3d0)
            polylineArea_1[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d6, point3d8, point3d10)
            point3d0 = [point3d14, point3d22, point3d30, point3d32]
            polylineArea_2.method_7(point3d0)
            polylineArea_2[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d22, point3d30, point3d10)
            point3d0 = [point3d13, point3d21, point3d29, point3d31]
            polylineArea_3.method_7(point3d0)
            polylineArea_3[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d21, point3d29, point3d10)
            point3d0 = [point3d_0, point3d11]
            polylineArea_4.method_7(point3d0)
            polylineArea_4[0].Bulge = MathHelper.smethod_57(turnDirection_0, point3d_0, point3d11, point3d10)
            polylineArea = PolylineArea()
            point3d0 = [point3d16, point3d7, point3d9, point3d34, point3d31, point3d29, point3d21, point3d13]
            polylineArea.method_7(point3d0)
            polylineArea[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d7, point3d9, point3d10)
            polylineArea[5].Bulge = MathHelper.smethod_57(MathHelper.smethod_67(turnDirection_0), point3d29, point3d21, point3d10)
            complexObstacleArea.ObstacleArea = PrimaryObstacleArea(polylineArea)
            polylineArea = PolylineArea()
            point3d0 = [point3d15, point3d6, point3d8, point3d33, point3d32, point3d30, point3d22, point3d14]
            polylineArea.method_7(point3d0)
            polylineArea[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d6, point3d8, point3d10)
            polylineArea[5].Bulge = MathHelper.smethod_57(MathHelper.smethod_67(turnDirection_0), point3d30, point3d22, point3d10)
            complexObstacleArea.Add(PrimaryObstacleArea(polylineArea))
            point3d35 = MathHelper.distanceBearingPoint(point3d10, MathHelper.getBearing(point3d10, point3d_0) - num6 / 2, metres1)
            point3d36 = MathHelper.distanceBearingPoint(point3d10, MathHelper.getBearing(point3d10, point3d_0) - num6 / 2, metres2)
            point3d37 = MathHelper.distanceBearingPoint(point3d10, MathHelper.getBearing(point3d10, MathHelper.distanceBearingPoint(point3d8, MathHelper.getBearing(point3d8, point3d6), MathHelper.calcDistance(point3d8, point3d6) / 2)), metres3)
            point3d38 = MathHelper.distanceBearingPoint(point3d10, MathHelper.getBearing(point3d10, MathHelper.distanceBearingPoint(point3d9, MathHelper.getBearing(point3d9, point3d7), MathHelper.calcDistance(point3d9, point3d7) / 2)), metres4)
            complexObstacleArea.Add(SecondaryObstacleArea(point3d15, point3d6, point3d16, point3d7))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d14, point3d22, point3d13, point3d21))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d8, point3d33, point3d9, point3d34))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d30, point3d32, point3d29, point3d31))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d22, point3d36, point3d30, point3d21,None, point3d35, point3d29))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d6, point3d37, point3d8, point3d7, None, point3d38, point3d9))
        else:
            point3d39 = MathHelper.distanceBearingPoint(point3d_0, num1, num5)
            point3d40 = MathHelper.distanceBearingPoint(point3d39, num3, num5)
            aSW = rnavGnssTolerance_0.ATT
            point3d41 = MathHelper.distanceBearingPoint(point3d_0, num2, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            point3d42 = MathHelper.distanceBearingPoint(point3d41, num1, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            point3d43 = MathHelper.distanceBearingPoint(point3d41, num1, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d44 = MathHelper.distanceBearingPoint(point3d41, num, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d45 = MathHelper.distanceBearingPoint(point3d41, num, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            point3d46 = MathHelper.distanceBearingPoint(point3d_0, num1, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            point3d47 = MathHelper.distanceBearingPoint(point3d_0, num1, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d48 = MathHelper.distanceBearingPoint(point3d_0, num, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d49 = MathHelper.distanceBearingPoint(point3d_0, num, aSW.Metres)
            point3d50 = point3d46
            point3d51 = point3d47
            point3d0_1 = []
            MathHelper.smethod_34(point3d44, point3d48, point3d39, metres3, point3d0_1)
            point3d = point3d0_1[0]
            point3d1 = point3d0_1[1]
            point3d0_2 = []
            MathHelper.smethod_34(point3d45, point3d49, point3d39, metres4, point3d0_2)
            point3d = point3d0_2[0]
            point3d2 = point3d0_2[1]
            aSW = rnavGnssTolerance_0.ASW
            point3d52 = MathHelper.distanceBearingPoint(point3d40, num4, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            point3d53 = MathHelper.distanceBearingPoint(point3d40, num4, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d54 = MathHelper.distanceBearingPoint(point3d40, num3, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d55 = MathHelper.distanceBearingPoint(point3d40, num3, aSW.Metres)
            point3d41 = MathHelper.distanceBearingPoint(point3d40, double1, 500)
            aSW = rnavGnssTolerance_0.ASW
            MathHelper.distanceBearingPoint(point3d41, num4, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            MathHelper.distanceBearingPoint(point3d41, num4, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d56 = MathHelper.distanceBearingPoint(point3d41, num3, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d57 = MathHelper.distanceBearingPoint(point3d41, num3, aSW.Metres)
            point3d58 = point3d52
            point3d59 = point3d53
            point3d0_3 = []
            MathHelper.smethod_34(point3d54, point3d56, point3d39, metres3, point3d0_3)
            point3d = point3d0_3[0]
            point3d3 = point3d0_3[1]
            point3d0_4 = []
            MathHelper.smethod_34(point3d55, point3d57, point3d39, metres4, point3d0_4)
            point3d = point3d0_4[0]
            point3d4 = point3d0_4[1]
            aSW = rnavGnssTolerance_0.ASW
            point3d41 = MathHelper.distanceBearingPoint(point3d4, num4, aSW.Metres)
            aSW = rnavGnssTolerance_0.ATT
            point3d41 = MathHelper.distanceBearingPoint(point3d41, double1, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            point3d60 = MathHelper.distanceBearingPoint(point3d41, num4, aSW.Metres)
            aSW = rnavGnssTolerance_0.ASW
            point3d61 = MathHelper.distanceBearingPoint(point3d41, num4, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d62 = MathHelper.distanceBearingPoint(point3d41, num3, aSW.Metres / 2)
            aSW = rnavGnssTolerance_0.ASW
            point3d63 = MathHelper.distanceBearingPoint(point3d41, num3, aSW.Metres)
            point3d0 = [point3d45, point3d2, point3d4, point3d63]
            polylineArea_0.method_7(point3d0)
            polylineArea_0[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d2, point3d4, point3d39)
            point3d0 = [point3d44, point3d1, point3d3, point3d62]
            polylineArea_1.method_7(point3d0)
            polylineArea_1[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d1, point3d3, point3d39)
            point3d0 = [point3d43, point3d51, point3d59, point3d61]
            polylineArea_2.method_7(point3d0)
            polylineArea_2[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d51, point3d59, point3d39)
            point3d0 = [point3d42, point3d50, point3d58, point3d60]
            polylineArea_3.method_7(point3d0)
            polylineArea_3[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d50, point3d58, point3d39)
            point3d0 = [point3d_0, point3d40 ]
            polylineArea_4.method_7(point3d0)
            polylineArea_4[0].Bulge = MathHelper.smethod_57(turnDirection_0, point3d_0, point3d40, point3d39)
            polylineArea1 = PolylineArea()
            point3d0 = [point3d45, point3d2, point3d4, point3d63, point3d60, point3d58, point3d50, point3d42]
            polylineArea1.method_7(point3d0)
            polylineArea1[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d2, point3d4, point3d39)
            polylineArea1[5].Bulge = MathHelper.smethod_57(MathHelper.smethod_67(turnDirection_0), point3d58, point3d50, point3d39)
            complexObstacleArea.ObstacleArea = PrimaryObstacleArea(polylineArea1)
            polylineArea1 = PolylineArea()
            point3d0 = [point3d44, point3d1, point3d3, point3d62, point3d61, point3d59, point3d51, point3d43]
            polylineArea1.method_7(point3d0)
            polylineArea1[1].Bulge = MathHelper.smethod_57(turnDirection_0, point3d1, point3d3, point3d39)
            polylineArea1[5].Bulge = MathHelper.smethod_57(MathHelper.smethod_67(turnDirection_0), point3d59, point3d51, point3d39)
            complexObstacleArea.Add(PrimaryObstacleArea(polylineArea1))
            point3d64 = MathHelper.distanceBearingPoint(point3d39, MathHelper.getBearing(point3d39, point3d_0) + num6 / 2, metres1)
            point3d65 = MathHelper.distanceBearingPoint(point3d39, MathHelper.getBearing(point3d39, point3d_0) + num6 / 2, metres2)
            point3d66 = MathHelper.distanceBearingPoint(point3d39, MathHelper.getBearing(point3d39, MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d3, point3d1), MathHelper.calcDistance(point3d3, point3d1) / 2)), metres3)
            point3d67 = MathHelper.distanceBearingPoint(point3d39, MathHelper.getBearing(point3d39, MathHelper.distanceBearingPoint(point3d4, MathHelper.getBearing(point3d4, point3d2), MathHelper.calcDistance(point3d4, point3d2) / 2)), metres4)
            complexObstacleArea.Add(SecondaryObstacleArea(point3d44, point3d1, point3d45, point3d2))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d43, point3d51, point3d42, point3d50))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d3, point3d62, point3d4, point3d63))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d59, point3d61, point3d58, point3d60))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d51, point3d65, point3d59, point3d50,None,  point3d64, point3d58))
            complexObstacleArea.Add(SecondaryObstacleArea(point3d1, point3d66, point3d3, point3d2,None, point3d67, point3d4))
        return (complexObstacleArea, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4)

    def method_43(self, point3d_0, double_0, double_1, rnavGnssTolerance_0, turnDirection_0, rnavGnssTolerance2):
        point3d = None
        point3d1 = None
        num = None
        point3d2 = None
        num1 = None
        num2 = None
        point3d3 = None
        point3d4 = None
        point3d5 = None
        point3d6 = None
        point3d7 = None
        point3d8 = None
        point3d9 = None
        point3d10 = None
        point3d11 = None
        point3d12 = None
        point3d13 = None
        point3d14 = None
        point3d15 = None
        point3d16 = None
        point3d17 = None
        point3d18 = None
        point3d19 = None
        point3d20 = None
        point3d21 = None
        point3d22 = None
        point3d23 = None
        point3d24 = None
        point3d25 = None
        point3d26 = None
        point3d27 = None
        point3d28 = None
        point3d29 = None
        point3d30 = None
        point3dArray = None
        num3 = None
        metresPerSecond = None
        metresPerSecond1 = None
        complexObstacleArea = ComplexObstacleArea()
        polylineArea_0 = PolylineArea()
        polylineArea_1 = PolylineArea()
        polylineArea_2 = PolylineArea()
        polylineArea_3 = PolylineArea()
        polylineArea_4 = PolylineArea()

        polylineAreaAAA = PolylineArea()
        rnavWaypointType = self.method_33()
        num4 = MathHelper.smethod_4(double_0)
        num5 = MathHelper.smethod_4(num4 + math.pi / 2)
        num6 = MathHelper.smethod_4(num4 - math.pi / 2)
        num7 = MathHelper.smethod_4(num4 + math.pi)
        num8 = MathHelper.smethod_4(double_1)
        num9 = MathHelper.smethod_4(num8 + math.pi / 2)
        num10 = MathHelper.smethod_4(num8 - math.pi / 2)
        num11 = MathHelper.smethod_4(num8 + math.pi)
        metres = rnavGnssTolerance_0.ASW.Metres
        metresWayPoint2 = rnavGnssTolerance2.ASW.Metres
        metres1 = rnavGnssTolerance_0.ATT.Metres
        metres2 = rnavGnssTolerance_0.XTT.Metres
        num12 = MathHelper.smethod_76(Unit.smethod_1(num4), Unit.smethod_1(num8), AngleUnits.Degrees)
        num13 = Unit.ConvertDegToRad(30)
        speed = Speed.smethod_0(self.parametersPanel.pnlIas.Value, self.parametersPanel.pnlIsa.Value, self.parametersPanel.pnlAltitude.Value)
        value = self.parametersPanel.pnlWind.Value
        value1 = self.parametersPanel.pnlBankAngle.Value
        distance = Distance.smethod_0(speed, value1)
        metres3 = distance.Metres
        distance = RnavWaypoints.getDistanceFromWaypointToEarliestTurningPoint(rnavWaypointType, Distance(metres1), Distance(metres3), num12, AngleUnits.Degrees)
        metres4 = distance.Metres
        point3d = MathHelper.distanceBearingPoint(point3d_0, num7, math.fabs(metres4)) if (metres4 >= 0) else MathHelper.distanceBearingPoint(point3d_0, num4, math.fabs(metres4))
        distance = RnavWaypoints.getDistanceFromWaypointToLatestTurningPoint(rnavWaypointType, speed, value, float(self.parametersPanel.pnlPilotTime.Value), float(self.parametersPanel.pnlBankEstTime.Value), Distance(metres1), Distance(metres3), num12, AngleUnits.Degrees)
        metres5 = distance.Metres
        point3d1 = MathHelper.distanceBearingPoint(point3d_0, num7, math.fabs(metres5)) if (metres5 >= 0) else MathHelper.distanceBearingPoint(point3d_0, num4, math.fabs(metres5))
        if (rnavWaypointType != RnavWaypointType.FlyBy):
            num14 = 0.6 * num12 if (num12 < 50) else 30
            if (num12 < 50):
                num3 = 90 - num14
                num1 = num3
            else:
                num3 = 60
            num1 = num3
            distance = Distance.smethod_0(speed, 15)
            metres6 = distance.Metres
            num15 = metres3 * math.sin(Unit.ConvertDegToRad(num12))
            num16 = metres3 * math.cos(Unit.ConvertDegToRad(num12)) * math.tan(Unit.ConvertDegToRad(num14))
            num17 = metres3 * ((1 - math.cos(Unit.ConvertDegToRad(num12)) / math.cos(Unit.ConvertDegToRad(num14))) / math.sin(Unit.ConvertDegToRad(num14)))
            num18 = metres6 * math.tan(Unit.ConvertDegToRad(num14 / 2))
            if (self.parametersPanel.chbCatH.Checked):
                metresPerSecond = 5 * speed.MetresPerSecond
            else:
                metresPerSecond = 10 * speed.MetresPerSecond
                num2 = metresPerSecond
            num2 = metresPerSecond
            point3d31 = MathHelper.distanceBearingPoint(point3d_0, num8, num15 + num16 + num17 + num18)
            if (turnDirection_0 != TurnDirection.Left):
                point3d3 = MathHelper.distanceBearingPoint(point3d_0, num4 + Unit.ConvertDegToRad(90), metres3)
                point3d5 = MathHelper.distanceBearingPoint(point3d3, num8 - Unit.ConvertDegToRad(num1), metres3)
                point3d4 = MathHelper.distanceBearingPoint(point3d31, num8 - Unit.ConvertDegToRad(90), metres6)
                point3d6 = MathHelper.distanceBearingPoint(point3d4, MathHelper.getBearing(point3d4, point3d31) + Unit.ConvertDegToRad(num14), metres6)
            else:
                point3d3 = MathHelper.distanceBearingPoint(point3d_0, num4 - Unit.ConvertDegToRad(90), metres3)
                point3d5 = MathHelper.distanceBearingPoint(point3d3, num8 + Unit.ConvertDegToRad(num1), metres3)
                point3d4 = MathHelper.distanceBearingPoint(point3d31, num8 + Unit.ConvertDegToRad(90), metres6)
                point3d6 = MathHelper.distanceBearingPoint(point3d4, MathHelper.getBearing(point3d4, point3d31) - Unit.ConvertDegToRad(num14), metres6)
            point3d32 = MathHelper.distanceBearingPoint(point3d31, num8, num2)
            polylineArea_4.Add(PolylineAreaPoint(point3d_0, MathHelper.smethod_57(turnDirection_0, point3d_0, point3d5, point3d3)))
            polylineArea_4.method_1(point3d5)
            if (turnDirection_0 == TurnDirection.Left):
                polylineArea_4.Add(PolylineAreaPoint(point3d6, MathHelper.smethod_57(TurnDirection.Right, point3d6, point3d31, point3d4)))
            elif (turnDirection_0 != TurnDirection.Right):
                polylineArea_4.method_1(point3d6)
            else:
                polylineArea_4.Add(PolylineAreaPoint(point3d6, MathHelper.smethod_57(TurnDirection.Left, point3d6, point3d31, point3d4)))
            polylineArea_4.method_1(point3d31)
            polylineArea_4.method_1(point3d32)
        else:
            num19 = metres3 * math.tan(Unit.ConvertDegToRad(num12 / 2))
            if (self.parametersPanel.chbCatH.Checked):
                metresPerSecond1 = 3 * speed.MetresPerSecond
                num = metresPerSecond1
            else:
                metresPerSecond1 = 5 * speed.MetresPerSecond
                num = metresPerSecond1
            num = metresPerSecond1
            point3d33 = MathHelper.distanceBearingPoint(point3d_0, num7, num19)
            point3d34 = MathHelper.distanceBearingPoint(point3d33, num5, 100)
            point3d35 = MathHelper.distanceBearingPoint(point3d_0, num8, num19)
            point3d36 = MathHelper.distanceBearingPoint(point3d35, num9, 100)
            point3d2 = MathHelper.getIntersectionPoint(point3d33, point3d34, point3d35, point3d36)
            point3d33 = MathHelper.distanceBearingPoint(point3d_0, num7, num19 + num)
            point3d34 = MathHelper.distanceBearingPoint(point3d_0, num7, num19)
            point3d35 = MathHelper.distanceBearingPoint(point3d_0, num8, num19)
            point3d36 = MathHelper.distanceBearingPoint(point3d_0, num8, num19 + num)
            polylineArea_4.method_1(point3d33)
            polylineArea_4.Add(PolylineAreaPoint(point3d34, MathHelper.smethod_57(turnDirection_0, point3d34, point3d35, point3d2)))
            polylineArea_4.method_1(point3d35)
            polylineArea_4.method_1(point3d36)
        if (turnDirection_0 != TurnDirection.Right):
            windSpiral = WindSpiral(MathHelper.distanceBearingPoint(point3d1, num5, metres / 2), num4, speed, value, value1, TurnDirection.Left)
            windSpiral1 = WindSpiral(MathHelper.distanceBearingPoint(point3d1, num6, metres / 2), num4, speed, value, value1, TurnDirection.Left)
            polylineArea_2.method_1(MathHelper.distanceBearingPoint(point3d, num5, metres / 2))
            polylineArea_2.method_1(MathHelper.distanceBearingPoint(point3d1, num5, metres / 2))
            num20 = num8 - num13
            point3d37 = windSpiral.method_0(num20, AngleUnits.Radians)
            point3d38 = windSpiral1.method_0(num20, AngleUnits.Radians)
            point3d39 = MathHelper.distanceBearingPoint(point3d_0, num9, metres / 2)
            point3d40 = MathHelper.distanceBearingPoint(point3d39, num8, 10000)
            if (windSpiral.method_1(point3d39, point3d40, True) or windSpiral1.method_1(point3d39, point3d40, True)):
                num21 = num6 if (num12 >= 90) else num8
                if (not MathHelper.smethod_119(point3d38, point3d37, MathHelper.distanceBearingPoint(point3d37, num20, 1000))):
                    if (rnavWaypointType == RnavWaypointType.FlyBy):
                        point3d19 = MathHelper.distanceBearingPoint(windSpiral.Center[0], num5, windSpiral.Radius[0])
                        polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, point3d19, windSpiral.Center[0])
                        polylineArea_2.method_1(point3d19)
                        point3d41 = windSpiral.method_0(num21, AngleUnits.Radians)
                        point3d22 = MathHelper.getIntersectionPoint(point3d41, MathHelper.distanceBearingPoint(point3d41, num21, 100), point3d19, MathHelper.distanceBearingPoint(point3d19, num4, 100))
                        polylineArea_2.method_1(point3d22)
                        if (not MathHelper.smethod_117(point3d37, windSpiral.Center[0], windSpiral.Finish[0], False)):
                            polylineArea_2.method_3(point3d41, MathHelper.smethod_57(turnDirection_0, point3d41, point3d37, windSpiral.Center[0]))
                        else:
                            polylineArea_2.method_3(point3d41, MathHelper.smethod_57(turnDirection_0, point3d41, windSpiral.Finish[0], windSpiral.Center[0]))
                            polylineArea_2.method_3(windSpiral.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral.Start[1], point3d37, windSpiral.Center[1]))
                    elif (not MathHelper.smethod_117(point3d37, windSpiral.Center[0], windSpiral.Finish[0], False)):
                        polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, point3d37, windSpiral.Center[0])
                    else:
                        polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, windSpiral.Finish[0], windSpiral.Center[0])
                        polylineArea_2.method_3(windSpiral.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral.Start[1], point3d37, windSpiral.Center[1]))
                    polylineArea_2.method_1(point3d37)
                    point3d19 = MathHelper.getIntersectionPoint(point3d37, MathHelper.distanceBearingPoint(point3d37, num20, 100), point3d_0, MathHelper.distanceBearingPoint(point3d_0, num8, 100))
                    polylineArea_2.method_1(point3d19)
                else:
                    point3d42 = windSpiral.method_0(num6, AngleUnits.Radians)
                    point3d43 = windSpiral1.method_0(num6, AngleUnits.Radians)
                    if (rnavWaypointType != RnavWaypointType.FlyBy):
                        polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, windSpiral.Finish[0], windSpiral.Center[0])
                        polylineArea_2.method_3(windSpiral.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral.Start[1], point3d42, windSpiral.Center[1]))
                        polylineArea_2.method_1(point3d42)
                    else:
                        point3d19 = MathHelper.distanceBearingPoint(windSpiral.Center[0], num5, windSpiral.Radius[0])
                        polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, point3d19, windSpiral.Center[0])
                        polylineArea_2.method_1(point3d19)
                        point3d44 = windSpiral.method_0(num21, AngleUnits.Radians)
                        point3d21 = MathHelper.getIntersectionPoint(point3d44, MathHelper.distanceBearingPoint(point3d44, num21, 100), point3d19, MathHelper.distanceBearingPoint(point3d19, num4, 100))
                        polylineArea_2.method_1(point3d21)
                        if (not MathHelper.smethod_117(point3d44, windSpiral.Center[0], windSpiral.Finish[0], False)):
                            polylineArea_2.method_3(point3d44, MathHelper.smethod_57(turnDirection_0, point3d44, windSpiral.Finish[0], windSpiral.Center[0]))
                            polylineArea_2.method_3(windSpiral.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral.Start[1], point3d42, windSpiral.Center[1]))
                            polylineArea_2.method_1(point3d42)
                        else:
                            polylineArea_2.method_3(point3d44, MathHelper.smethod_57(turnDirection_0, point3d44, point3d42, windSpiral.Center[1]))
                            polylineArea_2.method_1(point3d42)

                    # polylineArea_2.method_3(point3d43, MathHelper.smethod_57(turnDirection_0, point3d43, point3d38, windSpiral1.Center[1]))
                    if self.parametersPanel.cmbRnavSpecification.SelectedIndex == 0:
                        if self.parametersPanel.chbUseTwoWpt.Checked and (self.parametersPanel.rdnDF.isChecked() or self.parametersPanel.rdnTF.isChecked()):
                            point3d19 = MathHelper.distanceBearingPoint(self.parametersPanel.pnlWaypoint2.Point3d, num9, metresWayPoint2 / 2)
                            pt = MathHelper.getIntersectionPoint(point3d38, MathHelper.distanceBearingPoint(point3d38, num20, 100), point3d19, MathHelper.distanceBearingPoint(point3d19, MathHelper.smethod_4(num8), 100))
                            # tempPolylinearea = PolylineArea()
                            # for polylineAreaPoint in polylineArea_1:
                            #     tempPolylinearea.append(polylineAreaPoint)
                            # tempPolylinearea.method_1(pt)
                            # pt = MathHelper.getIntersectionPointBetweenPolylineArea(tempPolylinearea, PolylineArea([point3d7, MathHelper.distanceBearingPoint(point3d7, num8, MathHelper.calcDistance(point3d_0, self.parametersPanel.pnlWaypoint2.Point3d))]))

                            if MathHelper.calcDistance(point3d_0, point3d19) < MathHelper.calcDistance(point3d_0, pt):
                                tempPolylinearea = PolylineArea()
                                for polylineAreaPoint in polylineArea_2:
                                    tempPolylinearea.append(polylineAreaPoint)
                                tempPolylinearea.method_1(pt)
                                pt = MathHelper.getIntersectionPointBetweenPolylineArea(tempPolylinearea, PolylineArea([self.parametersPanel.pnlWaypoint2.Point3d, MathHelper.distanceBearingPoint(self.parametersPanel.pnlWaypoint2.Point3d, num9, 50000)]))
                                polylineArea_2.method_1(pt)
                                polylineArea_2.method_1(pt)
                            else:
                                polylineArea_2.method_1(pt)
                                polylineArea_2.method_1(point3d19)
                        else:
                            point3d19 = MathHelper.getIntersectionPoint(point3d38, MathHelper.distanceBearingPoint(point3d38, num20, 100), point3d_0, MathHelper.distanceBearingPoint(point3d_0, num8, 100))

                            polylineArea_2.method_1(point3d38)
                            polylineArea_2.method_1(point3d19)
                    else:
                        point3d19 = MathHelper.getIntersectionPoint(point3d38, MathHelper.distanceBearingPoint(point3d38, num20, 100), point3d_0, MathHelper.distanceBearingPoint(point3d_0, num8, 100))

                        polylineArea_2.method_1(point3d38)
                        polylineArea_2.method_1(point3d19)
            else:
                num22 = num8 + Unit.ConvertDegToRad(15)
                point3d45 = windSpiral.method_0(num22, AngleUnits.Radians)
                if (rnavWaypointType != RnavWaypointType.FlyBy):
                    if (not MathHelper.smethod_115(point3d45, windSpiral.Center[0], windSpiral.Finish[0])):
                        polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, point3d45, windSpiral.Center[0])
                    else:
                        polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, windSpiral.Finish[0], windSpiral.Center[0])
                        polylineArea_2.method_3(windSpiral.Finish[0], MathHelper.smethod_57(turnDirection_0, windSpiral.Finish[0], point3d45, windSpiral.Center[1]))
                    polylineArea_2.method_1(point3d45)
                    polylineArea_2.method_1(MathHelper.distanceBearingPoint(point3d45, num22, 10000))
                else:
                    point3d19 = MathHelper.distanceBearingPoint(windSpiral.Center[0], num5, windSpiral.Radius[0])
                    polylineArea_2[polylineArea_2.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_2[polylineArea_2.Count - 1].Position, point3d19, windSpiral.Center[0])
                    polylineArea_2.method_1(point3d19)
                    point3d46 = windSpiral.method_0(num8, AngleUnits.Radians)
                    point3d20 = MathHelper.getIntersectionPoint(point3d19, MathHelper.distanceBearingPoint(point3d19, num4, 100), point3d46, MathHelper.distanceBearingPoint(point3d46, num11, 100))
                    polylineArea_2.method_1(point3d20)
                    point3d19 = MathHelper.distanceBearingPoint(point3d45, num22, 10000)
                    point3d20 = MathHelper.getIntersectionPoint(point3d20, point3d46, point3d45, point3d19)
                    point3dArray = [point3d20, point3d19]
                    polylineArea_2.method_7(point3dArray)
            polylineArea_2.method_16()
            # polylineArea_2.reverse()
            polylineArea_2 = self.method_44(polylineArea_2, point3d39, point3d40)

            count = polylineArea_2.Count
            for i in range(count):
                if i + 1 == count:break
                if i != 0 and i + 1 != count:
                    if polylineArea_2[i].Position.get_X() == polylineArea_2[i-1].Position.get_X() and polylineArea_2[i].Position.get_X() == polylineArea_2[i+1].Position.get_X():
                        polylineArea_2.pop(i)
                        count -= 1

                        continue
                    if polylineArea_2[i].Position.get_Y() == polylineArea_2[i-1].Position.get_Y() and polylineArea_2[i].Position.get_Y() == polylineArea_2[i+1].Position.get_Y():
                        polylineArea_2.pop(i)
                        count -= 1
                        continue
            if self.parametersPanel.cmbRnavSpecification.SelectedIndex == 0:
                if self.parametersPanel.chbUseTwoWpt.Checked and (self.parametersPanel.rdnDF.isChecked() or self.parametersPanel.rdnTF.isChecked()):
                    polylineArea_3 = polylineArea_2.method_23(-(metresWayPoint2 / 2), OffsetGapType.Fillet, 0, 2, 2)
                else:
                    polylineArea_3 = polylineArea_2.method_23(-(metres / 2), OffsetGapType.Fillet, 0, 2, 2)
            else:
                polylineArea_3 = polylineArea_2.method_23(-(metres / 2), OffsetGapType.Fillet, 0, 2, 2)
            polylineArea_3.reverse()
            # polylineArea_3333 = PolylineArea()
            # i = polylineArea_3.Count - 1
            # for polylineAreaPoint000 in polylineArea_3:
            #     polylineArea_3333.Add(polylineArea_3[i])
            #     i -=1
            # polylineArea_3 = polylineArea_3333
            #
            #
            # polylineArea_3333 = PolylineArea()
            # i = polylineArea_2.Count - 1
            # for polylineAreaPoint000 in polylineArea_2:
            #     polylineArea_3333.Add(polylineArea_2[i])
            #     i -=1
            # polylineArea_2 = polylineArea_3333
            # i=0
            # for item in polylineArea_2:
            #     polylineArea_3[i].set_Bulge(item.Bulge)
            #     i += 1


            polylineAreaAAA = PolylineArea([point3d39, point3d40])
            # for i in range(len(polylineArea_3_0), 0):
            #     polylineArea_3.Add(polylineArea_3_0[i])
            self.method_45(complexObstacleArea, polylineArea_2, polylineArea_3)
            polylineArea_3 = self.method_44(polylineArea_3, MathHelper.distanceBearingPoint(point3d39, num9, metres / 2), MathHelper.distanceBearingPoint(point3d40, num9, -metres / 2))
            point3d39 = MathHelper.distanceBearingPoint(point3d_0, num10, metres / 2)
            point3d40 = MathHelper.distanceBearingPoint(point3d39, num8, 1000)
            point3d47 = MathHelper.distanceBearingPoint(point3d_0, num10, metres)
            point3d48 = MathHelper.distanceBearingPoint(point3d47, num8, 1000)
            position = MathHelper.distanceBearingPoint(point3d, num6, metres / 2)
            position1 = MathHelper.distanceBearingPoint(point3d, num6, metres)
            if (MathHelper.smethod_119(position, point3d39, point3d40) and MathHelper.smethod_119(position1, point3d39, point3d40)):
                point3d49 = MathHelper.distanceBearingPoint(position1, num8 - Unit.ConvertDegToRad(15), 100)
                point3d23 = MathHelper.getIntersectionPoint(point3d39, point3d40, position1, point3d49)
                point3d24 = MathHelper.getIntersectionPoint(point3d47, point3d48, position1, point3d49)
                point3d50 = point3d23
                point3d51 = MathHelper.distanceBearingPoint(point3d24, num9, metres / 2)
                complexObstacleArea.Add(SecondaryObstacleArea(point3d23, point3d51, point3d50, point3d24))
                point3dArray = [position1, point3d23, point3d51]
                polylineArea_1.method_7(point3dArray)
                point3dArray = [position1, point3d50, point3d24]
                polylineArea_0.method_7(point3dArray)
            elif (not MathHelper.smethod_115(position, point3d39, point3d40) or not MathHelper.smethod_119(position1, point3d47, point3d48)):
                num23 = num4 - Unit.ConvertDegToRad(num12 / 2)
                point3d52 = MathHelper.distanceBearingPoint(position, num23, 100)
                point3d53 = MathHelper.distanceBearingPoint(position1, num23, 100)
                point3d27 = MathHelper.getIntersectionPoint(point3d39, point3d40, position, point3d52)
                point3d28 = MathHelper.getIntersectionPoint(point3d47, point3d48, position1, point3d53)
                complexObstacleArea.Add(SecondaryObstacleArea(position, point3d27, position1, point3d28))
                point3dArray = [position, point3d27 ]
                polylineArea_1.method_7(point3dArray)
                point3dArray = [position1, point3d28]
                polylineArea_0.method_7(point3dArray)
            else:
                num24 = num4 - Unit.ConvertDegToRad(num12 / 2)
                point3d54 = MathHelper.distanceBearingPoint(position, num24, 100)
                point3d55 = MathHelper.distanceBearingPoint(position1, num8 - Unit.ConvertDegToRad(15), 100)
                point3d25 = MathHelper.getIntersectionPoint(point3d39, point3d40, position, point3d54)
                point3d26 = MathHelper.getIntersectionPoint(point3d47, point3d48, position1, point3d55)
                point3d56 = point3d26
                point3d57 = MathHelper.distanceBearingPoint(point3d56, num9, metres / 2)
                complexObstacleArea.Add(SecondaryObstacleArea(position, point3d25, position1, position1))
                complexObstacleArea.Add(SecondaryObstacleArea(point3d25, point3d57, position1, point3d26))
                point3dArray = [position, point3d25, point3d57]
                polylineArea_1.method_7(point3dArray)
                point3dArray = [position1, point3d26, point3d56]
                polylineArea_0.method_7(point3dArray)
            position2 = polylineArea_2[polylineArea_2.Count - 1].Position
            point3d29 = MathHelper.getIntersectionPoint(position2, MathHelper.distanceBearingPoint(position2, num10, 1000), point3d39, point3d40)
            point3d30 = MathHelper.getIntersectionPoint(position2, MathHelper.distanceBearingPoint(position2, num10, 1000), point3d47, point3d48)
            position = polylineArea_1[polylineArea_1.Count - 1].Position
            position1 = polylineArea_0[polylineArea_0.Count - 1].Position
            if (MathHelper.smethod_121(position, point3d30, position2, False) and MathHelper.smethod_121(position1, point3d30, position2, False)):
                complexObstacleArea.Add(SecondaryObstacleArea(position, point3d29, position1, point3d30))
                polylineArea_1.method_1(point3d29)
                polylineArea_0.method_1(point3d30)
            polylineArea = PolylineArea()
            polylineArea.method_8(polylineArea_3)
            polylineArea.method_1(polylineArea_2[polylineArea_2.Count - 1].Position)
            polylineArea.method_1(polylineArea_1[polylineArea_1.Count - 1].Position)
            polylineArea.method_8(polylineArea_0.method_17())
            complexObstacleArea.ObstacleArea = PrimaryObstacleArea(polylineArea)
            polylineArea = PolylineArea()
            polylineArea.method_8(polylineArea_2)
            polylineArea.method_8(polylineArea_1.method_17())
            complexObstacleArea.Insert(0, PrimaryObstacleArea(polylineArea))
        else:
            windSpiral2 = WindSpiral(MathHelper.distanceBearingPoint(point3d1, num6, metres / 2), num4, speed, value, value1, TurnDirection.Right)
            windSpiral3 = WindSpiral(MathHelper.distanceBearingPoint(point3d1, num5, metres / 2), num4, speed, value, value1, TurnDirection.Right)
            polylineArea_1.method_1(MathHelper.distanceBearingPoint(point3d, num6, metres / 2))
            polylineArea_1.method_1(MathHelper.distanceBearingPoint(point3d1, num6, metres / 2))
            num25 = num8 + num13
            point3d58 = windSpiral2.method_0(num25, AngleUnits.Radians)
            point3d59 = windSpiral3.method_0(num25, AngleUnits.Radians)
            point3d60 = MathHelper.distanceBearingPoint(point3d_0, num10, metres / 2)
            point3d61 = MathHelper.distanceBearingPoint(point3d60, num8, 10000)
            if (windSpiral2.method_1(point3d60, point3d61, True) or windSpiral3.method_1(point3d60, point3d61, True)):
                num26 = num5 if (num12 >= 90) else num8
                if (not MathHelper.smethod_115(point3d59, point3d58, MathHelper.distanceBearingPoint(point3d58, num25, 1000))):
                    if (rnavWaypointType == RnavWaypointType.FlyBy):
                        point3d7 = MathHelper.distanceBearingPoint(windSpiral2.Center[0], num6, windSpiral2.Radius[0])
                        polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, point3d7, windSpiral2.Center[0])
                        polylineArea_1.method_1(point3d7)
                        point3d62 = windSpiral2.method_0(num26, AngleUnits.Radians)
                        point3d10 = MathHelper.getIntersectionPoint(point3d62, MathHelper.distanceBearingPoint(point3d62, num26, 100), point3d7, MathHelper.distanceBearingPoint(point3d7, num4, 100))
                        polylineArea_1.method_1(point3d10)
                        if (not MathHelper.smethod_121(point3d58, windSpiral2.Center[0], windSpiral2.Finish[0], False)):
                            polylineArea_1.method_3(point3d62, MathHelper.smethod_57(turnDirection_0, point3d62, point3d58, windSpiral2.Center[0]))
                        else:
                            polylineArea_1.method_3(point3d62, MathHelper.smethod_57(turnDirection_0, point3d62, windSpiral2.Finish[0], windSpiral2.Center[0]))
                            polylineArea_1.method_3(windSpiral2.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral2.Start[1], point3d58, windSpiral2.Center[1]))
                    elif (not MathHelper.smethod_121(point3d58, windSpiral2.Center[0], windSpiral2.Finish[0], False)):
                        polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, point3d58, windSpiral2.Center[0])
                    else:
                        polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, windSpiral2.Finish[0], windSpiral2.Center[0])
                        polylineArea_1.method_3(windSpiral2.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral2.Start[1], point3d58, windSpiral2.Center[1]))
                    if self.parametersPanel.cmbRnavSpecification.SelectedIndex == 0:
                        if self.parametersPanel.chbUseTwoWpt.Checked and (self.parametersPanel.rdnDF.isChecked() or self.parametersPanel.rdnTF.isChecked()):
                            point3d7 = MathHelper.distanceBearingPoint(self.parametersPanel.pnlWaypoint2.Point3d, num10, metresWayPoint2 / 2)
                            pt = MathHelper.getIntersectionPoint(point3d58, MathHelper.distanceBearingPoint(point3d58, num25, 100), point3d7, MathHelper.distanceBearingPoint(point3d7, MathHelper.smethod_4(num8), 100))
                            # tempPolylinearea = PolylineArea()
                            # for polylineAreaPoint in polylineArea_1:
                            #     tempPolylinearea.append(polylineAreaPoint)
                            # tempPolylinearea.method_1(pt)
                            # pt = MathHelper.getIntersectionPointBetweenPolylineArea(tempPolylinearea, PolylineArea([point3d7, MathHelper.distanceBearingPoint(point3d7, num8, MathHelper.calcDistance(point3d_0, self.parametersPanel.pnlWaypoint2.Point3d))]))

                            if MathHelper.calcDistance(point3d_0, point3d7) < MathHelper.calcDistance(point3d_0, pt):
                                tempPolylinearea = PolylineArea()
                                for polylineAreaPoint in polylineArea_1:
                                    tempPolylinearea.append(polylineAreaPoint)
                                tempPolylinearea.method_1(pt)
                                pt = MathHelper.getIntersectionPointBetweenPolylineArea(tempPolylinearea, PolylineArea([self.parametersPanel.pnlWaypoint2.Point3d, MathHelper.distanceBearingPoint(self.parametersPanel.pnlWaypoint2.Point3d, num10, 50000)]))
                                polylineArea_1.method_1(pt)
                                polylineArea_1.method_1(pt)
                            else:
                                polylineArea_1.method_1(pt)
                                polylineArea_1.method_1(point3d7)
                        else:
                            polylineArea_1.method_1(point3d58)
                            point3d7 = MathHelper.getIntersectionPoint(point3d58, MathHelper.distanceBearingPoint(point3d58, num25, 100), point3d_0, MathHelper.distanceBearingPoint(point3d_0, num8, 100))
                            polylineArea_1.method_1(point3d7)
                    else:
                        polylineArea_1.method_1(point3d58)
                        point3d7 = MathHelper.getIntersectionPoint(point3d58, MathHelper.distanceBearingPoint(point3d58, num25, 100), point3d_0, MathHelper.distanceBearingPoint(point3d_0, num8, 100))
                        polylineArea_1.method_1(point3d7)
                else:
                    point3d63 = windSpiral2.method_0(num5, AngleUnits.Radians)
                    point3d64 = windSpiral3.method_0(num5, AngleUnits.Radians)
                    if (rnavWaypointType != RnavWaypointType.FlyBy):
                        polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, windSpiral2.Finish[0], windSpiral2.Center[0])
                        polylineArea_1.method_3(windSpiral2.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral2.Start[1], point3d63, windSpiral2.Center[1]))
                        polylineArea_1.method_1(point3d63)
                    else:
                        point3d7 = MathHelper.distanceBearingPoint(windSpiral2.Center[0], num6, windSpiral2.Radius[0])
                        polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, point3d7, windSpiral2.Center[0])
                        polylineArea_1.method_1(point3d7)
                        point3d65 = windSpiral2.method_0(num26, AngleUnits.Radians)
                        point3d9 = MathHelper.getIntersectionPoint(point3d65, MathHelper.distanceBearingPoint(point3d65, num26, 100), point3d7, MathHelper.distanceBearingPoint(point3d7, num4, 100))
                        polylineArea_1.method_1(point3d9)
                        if (not MathHelper.smethod_121(point3d65, windSpiral2.Center[0], windSpiral2.Finish[0], False)):
                            polylineArea_1.method_3(point3d65, MathHelper.smethod_57(turnDirection_0, point3d65, windSpiral2.Finish[0], windSpiral2.Center[0]))
                            polylineArea_1.method_3(windSpiral2.Start[1], MathHelper.smethod_57(turnDirection_0, windSpiral2.Start[1], point3d63, windSpiral2.Center[1]))
                            polylineArea_1.method_1(point3d63)
                        else:
                            polylineArea_1.method_3(point3d65, MathHelper.smethod_57(turnDirection_0, point3d65, point3d63, windSpiral2.Center[1]))
                            polylineArea_1.method_1(point3d63)
                    # polylineArea_1.method_3(point3d64, MathHelper.smethod_57(turnDirection_0, point3d64, point3d59, windSpiral3.Center[1]))
                    point3d7 = None
                    if self.parametersPanel.cmbRnavSpecification.SelectedIndex == 0:
                        if self.parametersPanel.chbUseTwoWpt.Checked and (self.parametersPanel.rdnDF.isChecked() or self.parametersPanel.rdnTF.isChecked()):
                            testDist = MathHelper.calcDistance(point3d_0, point3d59)
                            point3d7 = MathHelper.distanceBearingPoint(self.parametersPanel.pnlWaypoint2.Point3d, num10, metresWayPoint2 / 2)

                            pt = MathHelper.getIntersectionPoint(point3d59, MathHelper.distanceBearingPoint(point3d59, num25, 100), point3d7, MathHelper.distanceBearingPoint(point3d7, MathHelper.smethod_4(num8 + math.pi), 100))

                            # tempPolylinearea = PolylineArea()
                            # for polylineAreaPoint in polylineArea_1:
                            #     tempPolylinearea.append(polylineAreaPoint)
                            # tempPolylinearea.method_1(pt)
                            # pt = MathHelper.getIntersectionPointBetweenPolylineArea(tempPolylinearea, PolylineArea([point3d7, MathHelper.distanceBearingPoint(point3d7, num8, MathHelper.calcDistance(point3d_0, self.parametersPanel.pnlWaypoint2.Point3d))]))



                            if MathHelper.calcDistance(point3d_0, point3d7) < MathHelper.calcDistance(point3d_0, pt):
                                tempPolylinearea = PolylineArea()
                                for polylineAreaPoint in polylineArea_1:
                                    tempPolylinearea.append(polylineAreaPoint)
                                tempPolylinearea.method_1(pt)
                                pt = MathHelper.getIntersectionPointBetweenPolylineArea(tempPolylinearea, PolylineArea([self.parametersPanel.pnlWaypoint2.Point3d, MathHelper.distanceBearingPoint(self.parametersPanel.pnlWaypoint2.Point3d, num10, 50000)]))
                                polylineArea_1.method_1(pt)
                                polylineArea_1.method_1(pt)
                            else:
                                polylineArea_1.method_1(pt)
                                polylineArea_1.method_1(point3d7)
                        else:
                            point3d7 = MathHelper.getIntersectionPoint(point3d59, MathHelper.distanceBearingPoint(point3d59, num25, 100), point3d_0, MathHelper.distanceBearingPoint(point3d_0, num8, 100))
                            polylineArea_1.method_1(point3d59)
                            polylineArea_1.method_1(point3d7)
                    else:
                        point3d7 = MathHelper.getIntersectionPoint(point3d59, MathHelper.distanceBearingPoint(point3d59, num25, 100), point3d_0, MathHelper.distanceBearingPoint(point3d_0, num8, 100))
                        polylineArea_1.method_1(point3d59)
                        polylineArea_1.method_1(point3d7)
            else:
                num27 = num8 - Unit.ConvertDegToRad(15)
                point3d66 = windSpiral2.method_0(num27, AngleUnits.Radians)
                if (rnavWaypointType != RnavWaypointType.FlyBy):
                    if (not MathHelper.smethod_119(point3d66, windSpiral2.Center[0], windSpiral2.Finish[0])):
                        polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, point3d66, windSpiral2.Center[0])
                    else:
                        polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, windSpiral2.Finish[0], windSpiral2.Center[0])
                        polylineArea_1.method_3(windSpiral2.Finish[0], MathHelper.smethod_57(turnDirection_0, windSpiral2.Finish[0], point3d66, windSpiral2.Center[1]))
                    polylineArea_1.method_1(point3d66)
                    polylineArea_1.method_1(MathHelper.distanceBearingPoint(point3d66, num27, 10000))
                else:
                    point3d7 = MathHelper.distanceBearingPoint(windSpiral2.Center[0], num6, windSpiral2.Radius[0])
                    polylineArea_1[polylineArea_1.Count - 1].Bulge = MathHelper.smethod_57(turnDirection_0, polylineArea_1[polylineArea_1.Count - 1].Position, point3d7, windSpiral2.Center[0])
                    polylineArea_1.method_1(point3d7)
                    point3d67 = windSpiral2.method_0(num8, AngleUnits.Radians)
                    point3d8 = MathHelper.getIntersectionPoint(point3d7, MathHelper.distanceBearingPoint(point3d7, num4, 100), point3d67, MathHelper.distanceBearingPoint(point3d67, num11, 100))
                    polylineArea_1.method_1(point3d8)
                    point3d7 = MathHelper.distanceBearingPoint(point3d66, num27, 10000)
                    point3d8 = MathHelper.getIntersectionPoint(point3d8, point3d67, point3d66, point3d7)
                    point3dArray = [point3d8, point3d7]
                    polylineArea_1.method_7(point3dArray)
            polylineArea_1.method_16()
            polylineArea_1 = self.method_44(polylineArea_1, point3d60, point3d61)

            polylineAreaAAA = PolylineArea([point3d60, point3d61])

            if self.parametersPanel.cmbRnavSpecification.SelectedIndex == 0:
                if self.parametersPanel.chbUseTwoWpt.Checked and (self.parametersPanel.rdnDF.isChecked() or self.parametersPanel.rdnTF.isChecked()):
                    polylineArea_0 = polylineArea_1.method_23(metresWayPoint2 / 2, OffsetGapType.Fillet, 0, 2, 2)
                else:
                    polylineArea_0 = polylineArea_1.method_23(metres / 2, OffsetGapType.Fillet, 0, 2, 2)
            else:
                polylineArea_0 = polylineArea_1.method_23(metres / 2, OffsetGapType.Fillet, 0, 2, 2)
            self.method_45(complexObstacleArea, polylineArea_1, polylineArea_0)
            polylineArea_0 = self.method_44(polylineArea_0, MathHelper.distanceBearingPoint(point3d60, num10, metres / 2), MathHelper.distanceBearingPoint(point3d61, num10, metres / 2))
            point3d60 = MathHelper.distanceBearingPoint(point3d_0, num9, metres / 2)
            point3d61 = MathHelper.distanceBearingPoint(point3d60, num8, 1000)
            point3d68 = MathHelper.distanceBearingPoint(point3d_0, num9, metres)
            point3d69 = MathHelper.distanceBearingPoint(point3d68, num8, 1000)
            position3 = MathHelper.distanceBearingPoint(point3d, num5, metres / 2)
            position4 = MathHelper.distanceBearingPoint(point3d, num5, metres)
            if (MathHelper.smethod_115(position3, point3d60, point3d61) and MathHelper.smethod_115(position4, point3d60, point3d61)):
                point3d70 = MathHelper.distanceBearingPoint(position4, num8 + Unit.ConvertDegToRad(15), 100)
                point3d11 = MathHelper.getIntersectionPoint(point3d60, point3d61, position4, point3d70)
                point3d12 = MathHelper.getIntersectionPoint(point3d68, point3d69, position4, point3d70)
                point3d71 = point3d11
                point3d72 = MathHelper.distanceBearingPoint(point3d12, num10, metres / 2)
                complexObstacleArea.Add(SecondaryObstacleArea(point3d11, point3d72, point3d71, point3d12))
                point3dArray = [position4, point3d11, point3d72]
                polylineArea_2.method_7(point3dArray)
                point3dArray = [position4, point3d71, point3d12]
                polylineArea_3.method_7(point3dArray)
            elif (not MathHelper.smethod_119(position3, point3d60, point3d61) or not MathHelper.smethod_115(position4, point3d68, point3d69)):
                num28 = num4 + Unit.ConvertDegToRad(num12 / 2)
                point3d73 = MathHelper.distanceBearingPoint(position3, num28, 100)
                point3d74 = MathHelper.distanceBearingPoint(position4, num28, 100)
                point3d15 = MathHelper.getIntersectionPoint(point3d60, point3d61, position3, point3d73)
                point3d16 = MathHelper.getIntersectionPoint(point3d68, point3d69, position4, point3d74)
                complexObstacleArea.Add(SecondaryObstacleArea(position3, point3d15, position4, point3d16))
                point3dArray = [position3, point3d15 ]
                polylineArea_2.method_7(point3dArray)
                point3dArray = [position4, point3d16 ]
                polylineArea_3.method_7(point3dArray)
            else:
                num29 = num4 + Unit.ConvertDegToRad(num12 / 2)
                point3d75 = MathHelper.distanceBearingPoint(position3, num29, 100)
                point3d76 = MathHelper.distanceBearingPoint(position4, num8 + Unit.ConvertDegToRad(15), 100)
                point3d13 = MathHelper.getIntersectionPoint(point3d60, point3d61, position3, point3d75)
                point3d14 = MathHelper.getIntersectionPoint(point3d68, point3d69, position4, point3d76)
                point3d77 = point3d14
                point3d78 = MathHelper.distanceBearingPoint(point3d77, num10, metres / 2)
                complexObstacleArea.Add(SecondaryObstacleArea(position3, point3d13, position4, position4))
                complexObstacleArea.Add(SecondaryObstacleArea(point3d13, point3d78, position4, point3d14))
                point3dArray = [position3, point3d13, point3d78 ]
                polylineArea_2.method_7(point3dArray)
                point3dArray = [position4, point3d14, point3d77 ]
                polylineArea_3.method_7(point3dArray)
            position5 = polylineArea_1[polylineArea_1.Count - 1].Position
            point3d17 = MathHelper.getIntersectionPoint(position5, MathHelper.distanceBearingPoint(position5, num9, 1000), point3d60, point3d61)
            point3d18 = MathHelper.getIntersectionPoint(position5, MathHelper.distanceBearingPoint(position5, num9, 1000), point3d68, point3d69)
            position3 = polylineArea_2[polylineArea_2.Count - 1].Position
            position4 = polylineArea_3[polylineArea_3.Count - 1].Position

            # if self.parametersPanel.chbUseTwoWpt.Checked:
            #     point3d17 = self.parametersPanel.pnlWaypoint2.Point3d

            if (MathHelper.smethod_117(position3, point3d18, position5, False) and MathHelper.smethod_117(position4, point3d18, position5, False)):
                complexObstacleArea.Add(SecondaryObstacleArea(position3, point3d17, position4, point3d18))
                polylineArea_2.method_1(point3d17)
                polylineArea_3.method_1(point3d18)
            polylineArea1 = PolylineArea()
            polylineArea1.method_8(polylineArea_0)
            polylineArea1.method_1(polylineArea_1[polylineArea_1.Count - 1].Position)
            polylineArea1.method_1(polylineArea_2[polylineArea_2.Count - 1].Position)
            polylineArea1.method_8(polylineArea_3.method_17())
            complexObstacleArea.ObstacleArea = PrimaryObstacleArea(polylineArea1)
            polylineArea1 = PolylineArea()
            polylineArea1.method_8(polylineArea_1)
            polylineArea1.method_8(polylineArea_2.method_17())
            complexObstacleArea.Insert(0, PrimaryObstacleArea(polylineArea1))
        return (polylineAreaAAA, complexObstacleArea, polylineArea_0, polylineArea_1, polylineArea_2, polylineArea_3, polylineArea_4)

    def method_44(self, polylineArea_0, point3d_0, point3d_1):
        # point3dArray = polylineArea_0.method_14()
        # polyline = QgsGeometry.fromPolyline(point3dArray)
        # line = QgsGeometry.fromPolyline([point3d_0.smethod_167(0), point3d_1.smethod_167(0)])
        # if polyline.intersects(line):
        #     point3dAt = point3dArray[0]
        #     point3d = point3dAt
        #     geom = polyline.intersection(line)
        #     # for point3d1 in geom.asPoint():
        #     point3d1 = geom.asPoint()
        #     if (MathHelper.calcDistance(point3dAt, point3d1) <= MathHelper.calcDistance(point3dAt, point3d)):
        #         return polylineArea_0
        #     point3d = point3dArray[2]
        #     splitCurves = polyline.splitGeometry([point3d_0.smethod_167(0), point3d_1.smethod_167(0)], False)
        #     if len(splitCurves) > 0 :
        #         item = splitCurves[1][0]
        #         polylineArea = PolylineArea.smethod_1(item)
        #         # return polylineArea
        return polylineArea_0
#                 Point3dCollection point3dCollection = new Point3dCollection()
#                 if (polyline.IntersectWith(line, 2, point3dCollection) > 0)
#                 {
#                     Point3d point3dAt = polyline.GetPoint3dAt(0)
#                     Point3d point3d = point3dAt
#                     foreach (Point3d point3d1 in point3dCollection)
#                     {
#                         if (MathHelper.calcDistance(point3dAt, point3d1) <= MathHelper.calcDistance(point3dAt, point3d))
#                         {
#                             continue
#                         }
#                         point3d = point3d1
#                     }
#                     point3dCollection.Clear()
#                     point3dCollection.Add(point3d)
#                     DBObjectCollection splitCurves = polyline.GetSplitCurves(point3dCollection)
#                     try
#                     {
#                         if (splitCurves.get_Count() > 0)
#                         {
#                             Polyline item = splitCurves.get_Item(0) as Polyline
#                             if (item != null)
#                             {
#                                 polylineArea = PolylineArea.smethod_1(item)
#                                 return polylineArea
#                             }
#                         }
#                     }
#                     finally
#                     {
#                         AcadHelper.smethod_25(splitCurves)
#                     }
#                 }
#             }
#             return polylineArea_0
#         }
#         return polylineArea
#     }
    def method_45(self, complexObstacleArea_0, polylineArea_0, polylineArea_1):
        point3d = None
        point3d1 = None
        point3d2 = None
        point3d3 = None
        num = 0
        num1 = 0
        while (num < polylineArea_0.Count):
            if (num1 >= polylineArea_1.Count):
                break
            if (polylineArea_0[num].Bulge == 0 and polylineArea_1[num1].Bulge == 0):
                if (num != polylineArea_0.Count - 1):
                    if (num1 != polylineArea_1.Count - 1):
                        complexObstacleArea_0.Add(SecondaryObstacleArea(polylineArea_0[num].Position, polylineArea_0[num + 1].Position, polylineArea_1[num1].Position, polylineArea_1[num1 + 1].Position, MathHelper.getBearing(polylineArea_0[num + 1].Position, polylineArea_0[num].Position)))
                        num += 1
                        num1 += 1
                        continue
                return
            elif (polylineArea_0[num].Bulge != 0 and polylineArea_1[num1].Bulge != 0):
                if (num != polylineArea_0.Count - 1):
                    if (num1 != polylineArea_1.Count - 1):
                        position = polylineArea_0[num].Position
                        position1 = polylineArea_0[num + 1].Position
                        position2 = polylineArea_1[num1].Position
                        position3 = polylineArea_1[num1 + 1].Position
                        point3d = MathHelper.smethod_71(position, position1, polylineArea_0[num].Bulge)
                        point3d1 = MathHelper.smethod_71(position2, position3, polylineArea_1[num1].Bulge)
                        point3d4 = MathHelper.smethod_93(MathHelper.smethod_66(polylineArea_0[num].Bulge), position, position1, point3d)
                        point3d5 = MathHelper.smethod_93(MathHelper.smethod_66(polylineArea_1[num1].Bulge), position2, position3, point3d1)
                        complexObstacleArea_0.Add(SecondaryObstacleArea(position, point3d4, position1, position2, None, point3d5, position3, polylineArea_0[num].Bulge, polylineArea_1[num].Bulge))
                        num += 1
                        num1 += 1
                        continue
                return
            elif (polylineArea_1[num1].Bulge == 0):
                if (num == polylineArea_0.Count - 1):
                    return
                position4 = polylineArea_0[num].Position
                position5 = polylineArea_0[num + 1].Position
                point3d3 = MathHelper.smethod_71(position4, position5, polylineArea_0[num1].Bulge)
                point3d6 = MathHelper.smethod_93(MathHelper.smethod_66(polylineArea_0[num].Bulge), position4, position5, point3d3)
                num2 = MathHelper.calcDistance(point3d3, polylineArea_1[num1].Position)
                point3d7 = MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d3, position4), num2)
                point3d8 = MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d3, point3d6), num2)
                point3d9 = MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d3, position5), num2)
                complexObstacleArea_0.Add(SecondaryObstacleArea(position4, point3d6, position5, point3d7, None, point3d8, point3d9))
                num += 1
            else:
                if (num1 == polylineArea_1.Count - 1):
                    return
                position6 = polylineArea_1[num1].Position
                position7 = polylineArea_1[num1 + 1].Position
                point3d2 = MathHelper.smethod_71(position6, position7, polylineArea_1[num1].Bulge)
                point3d10 = MathHelper.smethod_93(MathHelper.smethod_66(polylineArea_1[num1].Bulge), position6, position7, point3d2)
                complexObstacleArea_0.Add(SecondaryObstacleArea(position6, point3d10, position7))
                num1 += 1
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
    def get_phaseOfFlight(self):
        for case in switch(self.parametersPanel.cmbPhaseOfFlight.SelectedItem):
            if case(PhaseOfFlightType.Enroute) or case(PhaseOfFlightType.EnrouteMore30):
                return RnavGnssFlightPhase.Enroute
            elif case(PhaseOfFlightType.StarMore30) or case(PhaseOfFlightType.SidMore30):
                return RnavGnssFlightPhase.StarSid
            elif case(PhaseOfFlightType.StarLess30) or case(PhaseOfFlightType.SidLess30) or case(PhaseOfFlightType.IfIafLess30) or case(PhaseOfFlightType.MaLess30):
                return RnavGnssFlightPhase.Star30Sid30IfIafMa30
            elif case(PhaseOfFlightType.SidLess15):
                return RnavGnssFlightPhase.Sid15
            elif case(PhaseOfFlightType.MaLess15):
                return RnavGnssFlightPhase.Ma15
            elif case(PhaseOfFlightType.Mapt):
                return RnavGnssFlightPhase.Mapt
            elif case(PhaseOfFlightType.Faf):
                return RnavGnssFlightPhase.Faf
        # if self.parametersPanel.cmbPhaseOfFlight.SelectedItem == "Enroute":
        #     return 0
        # elif self.parametersPanel.cmbPhaseOfFlight.SelectedItem == "STAR":
        #     return 2
        return -1

#         return self.parametersPanel.cmbPhaseOfFlight.currentIndex()
    phaseOfFlight = property(get_phaseOfFlight, None, None, None)

    def get_rnavSpecification(self):
        return self.parametersPanel.cmbRnavSpecification.SelectedItem
    rnavSpecification = property(get_rnavSpecification, None, None, None)

#             RnavStraightSegmentAnalyser.obstacles.method_11(obstacle_0, obstacleAreaResult, num1, num, z, criticalObstacleType)
class PhaseOfFlightType:
    Enroute = "EN-ROUTE"
    EnrouteMore30 = "EN-ROUTE (>30 NM ARP)"
    StarMore30 = "STAR (>30 NM ARP)"
    SidMore30 = "SID (>30 NM ARP)"
    StarLess30 = "STAR (<30 NM ARP)"
    SidLess30 = "SID (<30 NM ARP)"
    IfIafLess30 = "IF/IAF (<30 NM ARP)"
    MaLess30 = "MA (<30 NM ARP)"
    SidLess15 = "SID (<15 NM ARP)"
    MaLess15 = "MA (<15 NM ARP)"
    Mapt = "MAPt(LP/LPV Only)"
    Faf = "FAF"





class TurnConstructionMethod:
    CircularArcs = "CircularArcs"
    FixedRadius = "FixedRadius"
    BoundingCircles = "BoundingCircles"

class TurnProtectionAndObstacleAssessmentObstacles(ObstacleTable):
    def __init__(self, complexObstacleArea_0, altitude_0, altitude_1, manualPoly):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, None)
        self.manualPolygon = manualPoly
        self.surfaceType = SurfaceTypes.RnavStraightSegmentAnalyser
        self.area = complexObstacleArea_0;
        self.primaryMoc = altitude_0.Metres;
        self.enrouteAltitude = altitude_1.Metres;
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
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            position = obstacle_0.Position;
            if num == None:
                checkResult = [obstacleAreaResult, num1, num,  position.get_Z() + obstacle_0.Trees, CriticalObstacleType.No];
                self.addObstacleToModel(obstacle_0, checkResult)
                return

            z = position.get_Z() + obstacle_0.Trees + num;
            criticalObstacleType = CriticalObstacleType.No;
            if (z > self.enrouteAltitude):
                criticalObstacleType = CriticalObstacleType.Yes;
            checkResult = [obstacleAreaResult, num1, num, z, criticalObstacleType];
            self.addObstacleToModel(obstacle_0, checkResult)
        m = 0

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