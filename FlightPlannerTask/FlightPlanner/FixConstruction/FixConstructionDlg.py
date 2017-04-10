# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QString,QSize, Qt
from PyQt4.QtGui import QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsVectorFileWriter,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType, SurfaceTypes, DistanceUnits,AircraftSpeedCategory, OrientationType, AltitudeUnits, ObstacleAreaResult
from FlightPlanner.FixConstruction.ui_FixConstruction import Ui_FixConstruction
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Holding.HoldingRnav.HoldingTemplateRnav import HoldingTemplateRnav
from FlightPlanner.Holding.HoldingTemplate import HoldingTemplate
from FlightPlanner.messages import Messages
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.types import Point3D
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.Captions import Captions
import define, math

class FixConstructionDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("FixConstructionDlg")
        self.surfaceType = SurfaceTypes.FixConstruction
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.FixConstruction)
        self.resize(470, 400)
        self.surfaceList = None
        self.resultLayerList = []
        
    
    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(1)
        self.ui.btnEvaluate.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)
        return FlightPlanBaseDlg.uiStateInit(self)
        
    def initParametersPan(self):
        ui = Ui_FixConstruction()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.frameMOCMultipiler.setVisible(False)
        
        self.parametersPanel.pnlTrackingPosition = PositionPanel(self.parametersPanel.gbTrackingAid)
        self.parametersPanel.pnlTrackingPosition.btnCalculater.hide()
        self.parametersPanel.pnlTrackingPosition.hideframe_Altitude()
        self.parametersPanel.pnlTrackingPosition.setObjectName("pnlTrackingPosition")
        ui.vl_gbTrackingAid.insertWidget(1, self.parametersPanel.pnlTrackingPosition)
        # self.connect(self.parametersPanel.pnlNavAid, SIGNAL("positionChanged"), self.initResultPanel)

        self.parametersPanel.pnlIntersectingPosition = PositionPanel(self.parametersPanel.gbIntersectingAid)
        self.parametersPanel.pnlIntersectingPosition.btnCalculater.hide()
        self.parametersPanel.pnlIntersectingPosition.hideframe_Altitude()
        self.parametersPanel.pnlIntersectingPosition.setObjectName("pnlIntersectingPosition")
        ui.vl_gbIntersectingAid.insertWidget(1, self.parametersPanel.pnlIntersectingPosition)
        # self.connect(self.parametersPanel.pnlNavAid, SIGNAL("positionChanged"), self.initResultPanel)


        self.parametersPanel.cmbTrackingType.addItems([Captions.VOR, Captions.NDB, Captions.LOC])
        self.parametersPanel.cmbIntersectingType.addItems([Captions.VOR, Captions.NDB, Captions.DME])

        self.parametersPanel.cmbTrackingType.currentIndexChanged.connect(self.method_30)
        self.parametersPanel.cmbIntersectingType.currentIndexChanged.connect(self.method_30)
        self.parametersPanel.btnCaptureTrackingRadialTrack.clicked.connect(self.captureTrackingRadialTrack)
        self.parametersPanel.btnCaptureIntersectingRadialTrack.clicked.connect(self.captureIntersectingRadialTrack)
        self.parametersPanel.btnMeasureDmeOffset.clicked.connect(self.measureDmeOffset)
        self.parametersPanel.btnMeasureIntersectingDistance.clicked.connect(self.measureIntersectingDistance)

        self.method_30()
    def btnConstruct_Click(self):
        num = None;
        num1 = None;
        line = None;
        polyline = None;
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        point3d3 = None;
        point3d4 = None;
        point3d5 = None;
        point3d6 = None;
        point3d7 = None;
        point3d8 = None;
        ficorResult = None;
        point = [];
        value = None;
        resultPolylineAreaList = []
        # if (!AcadHelper.Ready)
        # {
        #     return;
        # }
        # if (!self.method_27(true))
        # {
        #     return;
        # }
        # string constructionLayer = base.ConstructionLayer;
        point3d9 = self.parametersPanel.pnlTrackingPosition.Point3d;
        point3d10 = self.parametersPanel.pnlIntersectingPosition.Point3d;
        value1 = float(self.parametersPanel.txtTrackingRadialTrack.text());
        value2 = float(self.parametersPanel.txtIntersectingRadialTrack.text());
        num2 = Unit.ConvertDegToRad(value1);
        num3 = Unit.ConvertDegToRad(value2);
        if (self.parametersPanel.cmbTrackingType.currentIndex() != 0):
            num = Unit.ConvertDegToRad(2.4) if(self.parametersPanel.cmbTrackingType.currentIndex() != 1) else Unit.ConvertDegToRad(6.9);
        else:
            num = Unit.ConvertDegToRad(5.2);
        num1 = Unit.ConvertDegToRad(6.2) if(self.parametersPanel.cmbIntersectingType.currentIndex() != 0) else Unit.ConvertDegToRad(4.5);
        num4 = num2 + num;
        point3d11 = MathHelper.distanceBearingPoint(point3d9, num4, 100);
        num5 = num2 - num;
        point3d12 = MathHelper.distanceBearingPoint(point3d9, num5, 100);
        point3d13 = MathHelper.distanceBearingPoint(point3d9, num2, 100);

        point3d = MathHelper.getIntersectionPoint(point3d9, point3d13, point3d10, MathHelper.distanceBearingPoint(point3d10, num3, 100))
        if (self.parametersPanel.cmbIntersectingType.currentIndex() >= 2):
            metres = Distance(float(self.parametersPanel.txtIntersectingDistance.text()), DistanceUnits.NM).Metres;
            if (self.parametersPanel.chb0dmeAtThr.isChecked()):
                value = Distance(float(self.parametersPanel.txtDmeOffset.text()));
                metres = metres + value.Metres;
            num6 = 460 + metres * 0.0125;
            num7 = metres + num6;
            num8 = metres - num6;
            if (MathHelper.smethod_102(point3d9, point3d10)):
                point3d14 = MathHelper.distanceBearingPoint(point3d9, num4, num8);
                point3d15 = MathHelper.distanceBearingPoint(point3d9, num2, num8);
                point3d16 = MathHelper.distanceBearingPoint(point3d9, num5, num8);
                point3d17 = MathHelper.distanceBearingPoint(point3d9, num5, num7);
                point3d18 = MathHelper.distanceBearingPoint(point3d9, num2, num7);
                point3d19 = MathHelper.distanceBearingPoint(point3d9, num4, num7);
                point = [point3d14, point3d16, point3d17, point3d19];
                polyline = AcadHelper.smethod_126(point);
                polyline.SetBulgeAt(0, MathHelper.smethod_60(point3d14, point3d15, point3d16));
                polyline.SetBulgeAt(2, MathHelper.smethod_60(point3d17, point3d18, point3d19));
                polyline.set_Closed(True);
                resultPolylineAreaList.append(polyline)
                # AcadHelper.smethod_18(transaction, blockTableRecord, polyline, constructionLayer);
                point3d14 = MathHelper.distanceBearingPoint(point3d9, num2, num8);
                point3d15 = MathHelper.distanceBearingPoint(point3d9, num2, num7);
                resultPolylineAreaList.append(PolylineArea([point3d14, point3d15]))
                # line = new Line(point3d14, point3d15);
        #         AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                point3d14 = MathHelper.distanceBearingPoint(point3d9, num4, metres);
                point3d15 = MathHelper.distanceBearingPoint(point3d9, num2, metres);
                point3d16 = MathHelper.distanceBearingPoint(point3d9, num5, metres);
                point = [point3d14, point3d16 ];
                polyline = AcadHelper.smethod_126(point);
                polyline.SetBulgeAt(0, MathHelper.smethod_60(point3d14, point3d15, point3d16));
                resultPolylineAreaList.append(polyline)
                # AcadHelper.smethod_18(transaction, blockTableRecord, polyline, constructionLayer);
            else:
                ficorResult1 = self.method_37(point3d10, num2, point3d9, point3d13, num8, FicorInput.C);
                ficorResult2 = self.method_37(point3d10, num2, point3d9, point3d13, metres, FicorInput.C);
                ficorResult3 = self.method_37(point3d10, num2, point3d9, point3d13, num7, FicorInput.C);
                if (ficorResult1.Status != FicorStatus.TWO and ficorResult2.Status != FicorStatus.TWO):
                    if (ficorResult3.Status == FicorStatus.TWO):
                        ficorResult = FicorResult(None, FicorStatus.TWO);
                    else:
                        ficorResult = FicorResult(None, ficorResult2.Status);
                else:
                    ficorResult = FicorResult(None, FicorStatus.TWO);
                if (ficorResult.Status != FicorStatus.NID):
                    ficorInput = FicorInput.F;
                    num9 = 1;
                    if (ficorResult.Status == FicorStatus.TWO):
                        QMessageBox.warning(self,"Infomation", Messages.TWO_POSSIBLE_FIX_POSITIONS);
                        ficorInput = FicorInput.L;
                        num9 = 2;
                    num10 = 0;
                    while (num10 < num9):
                        ficorResult4 = self.method_37(point3d10, num4, point3d9, point3d11, num8, ficorInput);
                        ficorResult5 = self.method_37(point3d10, num2, point3d9, point3d13, num8, ficorInput);
                        ficorResult6 = self.method_37(point3d10, num5, point3d9, point3d12, num8, ficorInput);
                        ficorResult7 = self.method_37(point3d10, num4, point3d9, point3d11, metres, ficorInput);
                        ficorResult8 = self.method_37(point3d10, num2, point3d9, point3d13, metres, ficorInput);
                        ficorResult9 = self.method_37(point3d10, num5, point3d9, point3d12, metres, ficorInput);
                        ficorResult10 = self.method_37(point3d10, num4, point3d9, point3d11, num7, ficorInput);
                        ficorResult11 = self.method_37(point3d10, num2, point3d9, point3d13, num7, ficorInput);
                        ficorResult12 = self.method_37(point3d10, num5, point3d9, point3d12, num7, ficorInput);
                        if (ficorResult4.Status == FicorStatus.NID or ficorResult5.Status == FicorStatus.NID or ficorResult6.Status == FicorStatus.NID or ficorResult7.Status == FicorStatus.NID or ficorResult9.Status == FicorStatus.NID or ficorResult10.Status == FicorStatus.NID or ficorResult11.Status == FicorStatus.NID or ficorResult12.Status == FicorStatus.NID or ficorResult8.Status == FicorStatus.NID):
                            eRRFAILEDTOCONSTRUCTTHEFIXAUTOMATICALLY = Messages.ERR_FAILED_TO_CONSTRUCT_THE_FIX_AUTOMATICALLY;
                            value = Distance(float(self.parametersPanel.txtIntersectingDistance.text()), DistanceUnits.NM);
                            str000 = str(round(value.Metres, 4)) + "m"
                            value = str(round(Distance(num6).Metres, 4)) + "m";
                            QMessageBox.warning(self,"Error", eRRFAILEDTOCONSTRUCTTHEFIXAUTOMATICALLY %(str000, value))
        #                     ErrorMessageBox.smethod_0(self, string.Format(eRRFAILEDTOCONSTRUCTTHEFIXAUTOMATICALLY, str, value.method_0(":m")));
                            return;
                        elif (MathHelper.calcDistance(point3d9, ficorResult8.Point) < MathHelper.calcDistance(ficorResult5.Point, ficorResult8.Point)):
                            QMessageBox.warning(self, "Error", Messages.ERR_FIX_TOO_CLOSE_USE_OVERHEAD_TOLERANCE)
        #                     ErrorMessageBox.smethod_0(self, Messages.ERR_FIX_TOO_CLOSE_USE_OVERHEAD_TOLERANCE);
                            return;
                        else:
                            point = [ficorResult4.Point, ficorResult6.Point, ficorResult12.Point, ficorResult10.Point];
                            polyline = AcadHelper.smethod_126(point);
                            polyline.SetBulgeAt(0, MathHelper.smethod_60(ficorResult4.Point, ficorResult5.Point, ficorResult6.Point));
                            polyline.SetBulgeAt(2, MathHelper.smethod_60(ficorResult12.Point, ficorResult11.Point, ficorResult10.Point));
                            polyline.set_Closed(True);
                            resultPolylineAreaList.append(polyline)
                            # AcadHelper.smethod_18(transaction, blockTableRecord, polyline, constructionLayer);
                            resultPolylineAreaList.append(PolylineArea([ficorResult5.Point, ficorResult11.Point]))
                            # line = new Line(ficorResult5.Point, ficorResult11.Point);
                            # AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                            point = [ficorResult7.Point, ficorResult9.Point];
                            polyline = AcadHelper.smethod_126(point);
                            polyline.SetBulgeAt(0, MathHelper.smethod_60(ficorResult7.Point, ficorResult8.Point, ficorResult9.Point));
                            resultPolylineAreaList.append(polyline)
                            # AcadHelper.smethod_18(transaction, blockTableRecord, polyline, constructionLayer);
                            if (ficorResult.Status == FicorStatus.TWO):
                                ficorInput = FicorInput.S;
                            num10 += 1;
                else:
                    QMessageBox.warning(self, "Error", Messages.ERR_RADIAL_TRACK_DME_DISTANCE_DO_NOT_INTERSECT)
        #             ErrorMessageBox.smethod_0(self, Messages.ERR_RADIAL_TRACK_DME_DISTANCE_DO_NOT_INTERSECT);
                    return;
        elif (point3d == None):
            QMessageBox.warning(self, "Error", Messages.ERR_RADIALS_TRACKS_ARE_PARALLEL)
        #     ErrorMessageBox.smethod_0(self, Messages.ERR_RADIALS_TRACKS_ARE_PARALLEL);
            return;
        elif (MathHelper.smethod_99(MathHelper.getBearing(point3d9, point3d), num2, 0.001)):
            point3d20 = MathHelper.distanceBearingPoint(point3d10, num3 + num1, 100);
            point3d21 = MathHelper.distanceBearingPoint(point3d10, num3 - num1, 100);
            point3d1 = MathHelper.getIntersectionPoint(point3d9, point3d12, point3d10, point3d20);
            point3d2 = MathHelper.getIntersectionPoint(point3d9, point3d12, point3d10, point3d21);
            point3d3 = MathHelper.getIntersectionPoint(point3d9, point3d11, point3d10, point3d21);
            point3d4 = MathHelper.getIntersectionPoint(point3d9, point3d11, point3d10, point3d20);
            point3d5 = MathHelper.getIntersectionPoint(point3d9, point3d, point3d10, point3d20);
            point3d6 = MathHelper.getIntersectionPoint(point3d9, point3d, point3d10, point3d21);
            point3d7 = MathHelper.getIntersectionPoint(point3d9, point3d11, point3d10, point3d);
            point3d8 = MathHelper.getIntersectionPoint(point3d9, point3d12, point3d10, point3d);
            if (MathHelper.calcDistance(point3d9, point3d) < MathHelper.calcDistance(point3d5, point3d) or MathHelper.calcDistance(point3d10, point3d) < MathHelper.calcDistance(point3d5, point3d) or MathHelper.calcDistance(point3d9, point3d) < MathHelper.calcDistance(point3d8, point3d) or MathHelper.calcDistance(point3d10, point3d) < MathHelper.calcDistance(point3d8, point3d)):
                QMessageBox.warning(self, "Error", Messages.ERR_FIX_TOO_CLOSE_USE_OVERHEAD_TOLERANCE)
        #         ErrorMessageBox.smethod_0(self, Messages.ERR_FIX_TOO_CLOSE_USE_OVERHEAD_TOLERANCE);
                return;
            else:
                resultPolylineAreaList.append(PolylineArea([point3d5, point3d6]))
        #         line = new Line(point3d5, point3d6);
        #         AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                resultPolylineAreaList.append(PolylineArea([point3d7, point3d8]))
        #         line = new Line(point3d7, point3d8);
        #         AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
                point = [point3d1, point3d2, point3d3, point3d4];
                polyline = AcadHelper.smethod_126(point);
                polyline.set_Closed(True);
                resultPolylineAreaList.append(polyline)
        #         AcadHelper.smethod_18(transaction, blockTableRecord, polyline, constructionLayer);
        else:
            QMessageBox.warning(self, "Error", Messages.ERR_RADIALS_TRACKS_DO_NOT_INTERSECT)
        #     ErrorMessageBox.smethod_0(self, Messages.ERR_RADIALS_TRACKS_DO_NOT_INTERSECT);
            return;

        mapUnits = define._canvas.mapUnits()
        constructionLayer = None
        if define._mapCrs == None:
            if mapUnits == QGis.Meters:
                constructionLayer = QgsVectorLayer("linestring?crs=EPSG:32633", self.surfaceType, "memory")
            else:
                constructionLayer = QgsVectorLayer("linestring?crs=EPSG:4326", self.surfaceType, "memory")
        else:
            constructionLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), self.surfaceType, "memory")
        shpPath = ""
        if define.obstaclePath != None:
            shpPath = define.obstaclePath
        elif define.xmlPath != None:
            shpPath = define.xmlPath
        else:
            shpPath = define.appPath
        er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + QString(self.surfaceType).replace(" ", "") + ".shp", "utf-8", constructionLayer.crs())
        constructionLayer = QgsVectorLayer(shpPath + "/" + QString(self.surfaceType).replace(" ", "") + ".shp", self.surfaceType, "ogr")


        constructionLayer.startEditing()

        for polylinrArea0 in resultPolylineAreaList:
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPolyline(polylinrArea0.method_14()))
            pr = constructionLayer.dataProvider()
            pr.addFeatures([feature])
            # constructionLayer.addFeature(feature)
        constructionLayer.commitChanges()
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], self.surfaceType, True)
        QgisHelper.zoomToLayers([constructionLayer])
    def captureTrackingRadialTrack(self):
        captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrackingRadialTrack)
        define._canvas.setMapTool(captureTrackTool)
    def captureIntersectingRadialTrack(self):
        captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtIntersectingRadialTrack)
        define._canvas.setMapTool(captureTrackTool)
    def measureDmeOffset(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtDmeOffset, DistanceUnits.M)
        define._canvas.setMapTool(measureDistanceTool)
    def measureIntersectingDistance(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtIntersectingDistance, DistanceUnits.NM)
        define._canvas.setMapTool(measureDistanceTool)
    def method_30(self):
        if (self.parametersPanel.cmbTrackingType.currentIndex() != 0):
            self.parametersPanel.label_TrackingRadial.setText(Captions.TRACK);
        else:
            self.parametersPanel.label_TrackingRadial.setText(Captions.RADIAL);
        if (self.parametersPanel.cmbIntersectingType.currentIndex() != 0):
            self.parametersPanel.label_IntersectingRadial.setText(Captions.TRACK);
        else:
            self.parametersPanel.label_IntersectingRadial.setText(Captions.RADIAL);
        self.parametersPanel.frameTrackRoot.setVisible(self.parametersPanel.cmbIntersectingType.currentIndex() < 2);
        self.parametersPanel.frame_IntersectingDistance.setVisible(self.parametersPanel.cmbIntersectingType.currentIndex() == 2);
        self.parametersPanel.pnl0dmeAtThr.setVisible(self.parametersPanel.cmbIntersectingType.currentIndex() == 2);
    def method_37(self, point3d_0, double_0, point3d_1, point3d_2, double_1, ficorInput_0):
        point3d = None;
        point3d = MathHelper.getIntersectionPoint(point3d_1, point3d_2, point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_0 + Unit.ConvertDegToRad(90), 100))
        if (point3d != None):
            num = MathHelper.getBearing(point3d_0, point3d);
            num1 = MathHelper.calcDistance(point3d_0, point3d);
            if (num1 <= double_1):
                num2 = math.acos(num1 / double_1);
                point3d1 = MathHelper.distanceBearingPoint(point3d_0, num + num2, double_1);
                point3d2 = MathHelper.distanceBearingPoint(point3d_0, num - num2, double_1);
                if (ficorInput_0 == FicorInput.C):
                    if (MathHelper.smethod_99(MathHelper.getBearing(point3d_1, point3d2), MathHelper.getBearing(point3d_1, point3d1), 0.1)):
                        return FicorResult(FicorStatus.TWO);
                    return FicorResult(FicorStatus.ONE);
                if (ficorInput_0 == FicorInput.F):
                    if (MathHelper.smethod_99(MathHelper.getBearing(point3d_1, point3d_2), MathHelper.getBearing(point3d_1, point3d1), 0.1)):
                        return FicorResult(point3d1);
                    return FicorResult(point3d2);
                if (ficorInput_0 == FicorInput.L):
                    if (MathHelper.calcDistance(point3d_1, point3d2) < MathHelper.calcDistance(point3d_1, point3d1)):
                        return FicorResult(point3d1);
                    return FicorResult(point3d2);
                if (ficorInput_0 == FicorInput.S):
                    if (MathHelper.calcDistance(point3d_1, point3d2) > MathHelper.calcDistance(point3d_1, point3d1)):
                        return FicorResult(point3d1);
                    return FicorResult(point3d2);
        return FicorResult(None, FicorStatus.NID);
class FicorInput:
    C = "C"
    F = "F"
    L = "L"
    S = "S"
class FicorStatus:
    NID = "NID"
    ONE = "One"
    TWO = "TWO"
    OK = "OK"
class FicorResult:
    def __init__(self, point3d_0 = None, ficorStatus_0 = None):
        self.status = None
        self.point = None
        
        if point3d_0 == None:
            self.point = Point3D.get_Origin();
            self.status = ficorStatus_0;
            return
        if ficorStatus_0 == None:
            self.point = point3d_0;
            self.status = FicorStatus.OK;
            return
    def get_point(self):
        return self.point
    Point = property(get_point, None, None, None)

    def get_status(self):
        return self.status
    Status = property(get_status, None, None, None)

class HoldingRnavArea:
#     private PrimaryObstacleArea area;
# 
#     private double moc;
    def get_area(self):
        return self.area
    Area = property(get_area, None, None, None)
    
    def get_moc(self):
        return self.moc
    Moc = property(get_moc, None, None, None)
    
    def __init__(self, polylineArea_0, altitude_0):
        self.area = PrimaryObstacleArea(polylineArea_0);
        self.moc = altitude_0.Metres;

    def method_0(self, obstacle_0):
        double_0 = self.moc * obstacle_0.MocMultiplier;
        double_1 = None
        if (not self.area.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
            return (False, double_0, double_1)
        position = obstacle_0.Position;
        double_1 = position.get_Z() + obstacle_0.Trees + double_0;
        return (True, double_0, double_1)
class HoldingRnavObstacles(ObstacleTable):
    def __init__(self, bool_0, typeStr, surfacesList = None, altitude = None, inner = None, outer = None, poly = None, altitude_1 = None, distance_0 = None):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)
        
        self.surfaceType = SurfaceTypes.FixConstruction
        self.obstaclesChecked = None
        self.typeStr = typeStr
        self.altitude = altitude.Metres
        if self.typeStr == "buffer":            
            self.surfacesList = surfacesList
            
        else:
            self.inner = inner
            self.outer = outer
            self.poly = poly
            self.moc = altitude_1.Metres
            self.offset = distance_0
        self.bool = bool_0
    def setHiddenColumns(self, tableView):
        tableView.hideColumn(self.IndexObstArea)
        tableView.hideColumn(self.IndexDistInSecM)
        return ObstacleTable.setHiddenColumns(self, tableView)
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        newHeaderCount = 0
        if bool:
            self.IndexObstArea = fixedColumnCount 
            self.IndexDistInSecM = fixedColumnCount + 1
            self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DistInSecM
                ])
            newHeaderCount = 2
        self.IndexMocAppliedM = fixedColumnCount + newHeaderCount
        self.IndexMocAppliedFt = fixedColumnCount + 1 + newHeaderCount
        self.IndexMocMultiplier = fixedColumnCount + 2 + newHeaderCount
        self.IndexOcaM = fixedColumnCount + 3 + newHeaderCount
        self.IndexOcaFt = fixedColumnCount + 4 + newHeaderCount
        self.IndexCritical = fixedColumnCount + 5 + newHeaderCount
                 
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt,
                ObstacleTableColumnType.Critical            
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)
    
    def addObstacleToModel(self, obstacle, checkResult):
        if self.typeStr == "buffer":
            ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
            row = self.source.rowCount() - 1
        
            item = QStandardItem(str(checkResult[0]))
            item.setData(checkResult[0])
            self.source.setItem(row, self.IndexMocAppliedM, item)
              
            item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[0])))
            item.setData(Unit.ConvertMeterToFeet(checkResult[0]))
            self.source.setItem(row, self.IndexMocAppliedFt, item)
              
            item = QStandardItem(str(ObstacleTable.MocMultiplier))
            item.setData(ObstacleTable.MocMultiplier)
            self.source.setItem(row, self.IndexMocMultiplier, item)
              
            item = QStandardItem(str(checkResult[1]))
            item.setData(checkResult[1])
            self.source.setItem(row, self.IndexOcaM, item)
              
            item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[1])))
            item.setData(Unit.ConvertMeterToFeet(checkResult[1]))
            self.source.setItem(row, self.IndexOcaFt, item)
            
            item = QStandardItem(str(checkResult[2]))
            item.setData(checkResult[2])
            self.source.setItem(row, self.IndexCritical, item) 
        else:
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
        if self.typeStr == "buffer":
            criticalObstacleType = CriticalObstacleType.No;
            for current in self.surfacesList:
                result, num, num1 = current.method_0
                if (result):
                    if (num1 > self.altitude):
                        criticalObstacleType = CriticalObstacleType.Yes;
                    checkResult = []
                    checkResult.append(num)
                    checkResult.append(num1)
                    checkResult.append(criticalObstacleType)
                    self.addObstacleToModel(obstacle_0, checkResult)
                    break
        else:
            mocMultiplier = self.moc * obstacle_0.MocMultiplier;
            metres = None
            num = None
            obstacleAreaResult = ObstacleAreaResult.Outside;
            if (not self.inner.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
                num = MathHelper.calcDistance(self.poly.getClosestPointTo(obstacle_0.Position, False), obstacle_0.Position) - obstacle_0.Tolerance;
                if (num > self.offset.Metres):
                    return;
                metres = mocMultiplier * (1 - num / self.offset.Metres);
                obstacleAreaResult = ObstacleAreaResult.Secondary;
            else:
                metres = mocMultiplier;
                obstacleAreaResult = ObstacleAreaResult.Primary;
            position = obstacle_0.Position;
            z = position.get_Z() + obstacle_0.Trees + metres;
            criticalObstacleType = CriticalObstacleType.No;
            if (z > self.altitude):
                criticalObstacleType = CriticalObstacleType.Yes;
            checkResult = []
            checkResult.append(obstacleAreaResult)
            checkResult.append(num)
            checkResult.append(metres)
            checkResult.append(z)
            checkResult.append(criticalObstacleType)
            self.addObstacleToModel(obstacle_0, checkResult)
