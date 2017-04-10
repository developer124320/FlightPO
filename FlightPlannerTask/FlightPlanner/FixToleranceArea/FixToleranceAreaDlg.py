# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QMessageBox, QFileDialog, QDialog, QIcon, QPixmap
from qgis.core import  QGis, QgsLayerTreeGroup
from FlightPlanner.types import SurfaceTypes, DistanceUnits, AltitudeUnits
from FlightPlanner.FixToleranceArea.ui_FixToleranceArea import Ui_FixToleranceArea
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.messages import Messages
from FlightPlanner.types import Point3D, Matrix3d, Vector3d
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.Captions import Captions
import define, math

class FixToleranceAreaDlg(QDialog):
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setObjectName("FixToleranceAreaDlg")

        self.resize(470, 400)
        QgisHelper.matchingDialogSize(self, 650, 450)
        ui = Ui_FixToleranceArea()
        ui.setupUi(self)
        self.parametersPanel = ui

        self.uiStateInit()
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.FixToleranceArea)

        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/btnImage/dlgIcon.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.resultLayerList1 = []
        self.resultLayerList2 = []
        self.surfaceType2 = SurfaceTypes.FixConstruction
        self.surfaceType1 = SurfaceTypes.OverheadTolerance
    def uiStateInit(self):

        self.parametersPanel.btnEvaluate.setVisible(False)
        self.parametersPanel.btnPDTCheck.setVisible(False)
        self.parametersPanel.btnExportResult.setVisible(False)
        self.parametersPanel.btnEvaluate_2.setVisible(False)
        self.parametersPanel.btnExportResult_2.setVisible(False)
        self.parametersPanel.frameMoc.setVisible(False)
        self.parametersPanel.frameMOCMultipiler.setVisible(False)

        self.parametersPanel.btnConstruct.clicked.connect(self.btnConstruct_Click)
        self.parametersPanel.btnConstruct_2.clicked.connect(self.btnConstruct2_Click)

        self.parametersPanel.btnOpenData.clicked.connect(self.openData)
        self.parametersPanel.btnOpenData_2.clicked.connect(self.openData)

        self.parametersPanel.btnSaveData.clicked.connect(self.saveData)
        self.parametersPanel.btnSaveData_2.clicked.connect(self.saveData)
    def btnConstruct2_Click(self):
        qgsLayerTreeView = define._mLayerTreeView
        groupName = self.surfaceType2
        layerTreeModel = qgsLayerTreeView.layerTreeModel()
        layerTreeGroup = layerTreeModel.rootGroup()
        rowCount = layerTreeModel.rowCount()
        groupExisting = False
        if rowCount > 0:
            for i in range(rowCount):
                qgsLayerTreeNode = layerTreeModel.index2node(layerTreeModel.index(i, 0))
                if qgsLayerTreeNode.nodeType() == 0:
                    qgsLayerTreeNode._class_ = QgsLayerTreeGroup
                    if isinstance(qgsLayerTreeNode, QgsLayerTreeGroup) and qgsLayerTreeNode.name() == groupName:
                        groupExisting = True

        if groupExisting:
            if len(self.resultLayerList2) > 0:
                QgisHelper.removeFromCanvas(define._canvas, self.resultLayerList2)
                self.resultLayerList2 = []
            else:
                QMessageBox.warning(self, "Warning", "Please remove \"" + self.surfaceType2 + "\" layer group from LayerTreeView.")
                return
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
        value1 = float(self.parametersPanel.txtTrackingRadialTrack.Value);
        value2 = float(self.parametersPanel.txtIntersectingRadialTrack.Value);
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
        constructionLayer = AcadHelper.createVectorLayer(SurfaceTypes.FixConstruction, QGis.Line)

        for polylinrArea0 in resultPolylineAreaList:
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylinrArea0)
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.FixConstruction, True)
        self.resultLayerList2 = [constructionLayer]
        QgisHelper.zoomToLayers(self.resultLayerList2)
        # QgisHelper.zoomToLayers([constructionLayer])
    def btnConstruct_Click(self):
        qgsLayerTreeView = define._mLayerTreeView
        groupName = self.surfaceType1
        layerTreeModel = qgsLayerTreeView.layerTreeModel()
        layerTreeGroup = layerTreeModel.rootGroup()
        rowCount = layerTreeModel.rowCount()
        groupExisting = False
        if rowCount > 0:
            for i in range(rowCount):
                qgsLayerTreeNode = layerTreeModel.index2node(layerTreeModel.index(i, 0))
                if qgsLayerTreeNode.nodeType() == 0:
                    qgsLayerTreeNode._class_ = QgsLayerTreeGroup
                    if isinstance(qgsLayerTreeNode, QgsLayerTreeGroup) and qgsLayerTreeNode.name() == groupName:
                        groupExisting = True

        if groupExisting:
            if len(self.resultLayerList1) > 0:
                QgisHelper.removeFromCanvas(define._canvas, self.resultLayerList1)
                self.resultLayerList1 = []
            else:
                QMessageBox.warning(self, "Warning", "Please remove \"" + self.surfaceType1 + "\" layer group from LayerTreeView.")
                return


        num = None;
        num1 = None;
        num2 = None;
        num3 = None;
        point3d = None;
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
        point3d1 = self.parametersPanel.pnlNavAid.Point3d;
        value = float(self.parametersPanel.txtTrackRadial.Value);
        metres = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT).Metres;
        z = metres - point3d1.get_Z();
        if (self.parametersPanel.cmbNavAidType.currentIndex() != 0):
            num = 450 - value + 90;
            num1 = 15;
            num2 = 25;
            num3 = z * 0.839099631;
        else:
            num = 450 - value + 90;
            num1 = 5;
            num2 = 15;
            num3 = z * 1.191753593;
        num4 = Unit.ConvertDegToRad(num1);
        num5 = Unit.ConvertDegToRad(360 - num1);
        num6 = Unit.ConvertDegToRad(180 - num2);
        num7 = Unit.ConvertDegToRad(180 + num2);
        num8 = 0;
        num9 = Unit.ConvertDegToRad(180);
        point3d2 = MathHelper.distanceBearingPoint(point3d1, num4, num3);
        point3d3 = MathHelper.distanceBearingPoint(point3d1, num5, num3);
        point3d = MathHelper.smethod_68(point3d2, MathHelper.distanceBearingPoint(point3d1, num8, num3), point3d3)
        if (point3d == None):
            QMessageBox.warning(self, "Error", Messages.ERR_FAILED_TO_CALCULATE_CENTER_POINT)
            return
        #     throw new Exception(Messages.ERR_FAILED_TO_CALCULATE_CENTER_POINT);
        num10 = MathHelper.smethod_55(point3d2, point3d3, MathHelper.calcDistance(point3d2, point3d));
        point3d2 = MathHelper.distanceBearingPoint(point3d1, num6, num3);
        point3d3 = MathHelper.distanceBearingPoint(point3d1, num7, num3);
        point3d = MathHelper.smethod_68(point3d2, MathHelper.distanceBearingPoint(point3d1, num9, num3), point3d3)
        if (point3d == None):
            QMessageBox.warning(self, "Error", Messages.ERR_FAILED_TO_CALCULATE_CENTER_POINT)
        #     throw new Exception(Messages.ERR_FAILED_TO_CALCULATE_CENTER_POINT);
        num11 = MathHelper.smethod_55(point3d2, point3d3, MathHelper.calcDistance(point3d2, point3d));
        matrix3d = Matrix3d.Rotation(Unit.ConvertDegToRad(num), Vector3d(0, 0, 1), point3d1);
        point3d2 = MathHelper.distanceBearingPoint(point3d1, num8, num3);
        point3d3 = MathHelper.distanceBearingPoint(point3d1, num9, num3);
        line = PolylineArea([point3d2, point3d3]);
        resultPolylineAreaList.append(self.TransformBy(line, Unit.ConvertDegToRad(value), self.parametersPanel.pnlNavAid.Point3d))#.TransformBy(matrix3d))
        point3d2 = MathHelper.distanceBearingPoint(point3d1, num6, num3);
        point3d3 = MathHelper.distanceBearingPoint(point3d1, num4, num3);
        point3d4 = MathHelper.distanceBearingPoint(point3d1, num5, num3);
        point3d5 = MathHelper.distanceBearingPoint(point3d1, num7, num3);
        point3dArray = [point3d2, point3d3, point3d4, point3d5, point3d2];
        polyline = AcadHelper.smethod_126(point3dArray);
        if self.parametersPanel.cmbNavAidType.currentIndex() == 0:
            num10 = 0.0436609429083
            num11 = 0.131652497586
        else:
            num10 = 0.131652497586
            num11 = 0.221694662642
        polyline.SetBulgeAt(1, num10);
        polyline.SetBulgeAt(3, num11);
        # polyline.set_Elevation(point3d1.get_Z());
        resultPolylineAreaList.append(self.TransformBy(polyline, Unit.ConvertDegToRad(value), self.parametersPanel.pnlNavAid.Point3d))#polyline.TransformBy(matrix3d))
        # polyline.TransformBy(matrix3d);
        # AcadHelper.smethod_18(transaction, blockTableRecord, polyline, constructionLayer);
        # transaction.Commit();
        # AcadHelper.smethod_5();
        mapUnits = define._canvas.mapUnits()
        constructionLayer = AcadHelper.createVectorLayer(SurfaceTypes.OverheadTolerance, QGis.Line)
        for polylinrArea0 in resultPolylineAreaList:
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylinrArea0)
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.OverheadTolerance, True)
        self.resultLayerList1 = [constructionLayer]
        QgisHelper.zoomToLayers(self.resultLayerList1)
        # QgisHelper.zoomToLayers([constructionLayer])
    def TransformBy(self, polylineArea, angle_radian, centerPoint):
        resultPoilylineArea = PolylineArea()
        for polylineAreaPoint in polylineArea:
            point3d = polylineAreaPoint.Position
            bearing = MathHelper.smethod_4(MathHelper.getBearing(centerPoint, point3d) + angle_radian + Unit.ConvertDegToRad(180))
            resultPoilylineArea.Add(PolylineAreaPoint(MathHelper.distanceBearingPoint(centerPoint, bearing, MathHelper.calcDistance(point3d, centerPoint)), polylineAreaPoint.Bulge))
        return resultPoilylineArea
    def initParametersPan(self):
        self.parametersPanel.pnlNavAid = PositionPanel(self.parametersPanel.gbNavAid)
#         self.parametersPanel.pnlWaypoint.groupBox.setTitle("FAWP")
        self.parametersPanel.pnlNavAid.btnCalculater.hide()
#         self.parametersPanel.pnlNavAid.hideframe_Altitude()
        self.parametersPanel.pnlNavAid.setObjectName("pnlNavAid")
        self.parametersPanel.vl_NavAid.addWidget(self.parametersPanel.pnlNavAid)
        # self.connect(self.parametersPanel.pnlNavAid, SIGNAL("positionChanged"), self.initResultPanel)

        self.parametersPanel.cmbNavAidType.addItems([Captions.VOR, Captions.NDB])
                
#         self.parametersPanel.cmbHoldingFunctionality.currentIndexChanged.connect(self.cmbHoldingFunctionalityCurrentIndexChanged)
#         self.parametersPanel.cmbOutboundLimit.currentIndexChanged.connect(self.cmbOutboundLimitCurrentIndexChanged)
#         self.parametersPanel.btnCaptureTrack.clicked.connect(self.captureBearing)
#         self.parametersPanel.btnCaptureDistance.clicked.connect(self.measureDistance)
#         self.parametersPanel.btnCaptureLength.clicked.connect(self.measureLength)        
        self.parametersPanel.txtAltitude.textChanged.connect(self.altitudeFtChanged)
        self.parametersPanel.txtAltitudeM.textChanged.connect(self.altitudeMChanged)

        

        self.flag = 0
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")


        # FixConstruction Part
        self.parametersPanel.pnlTrackingPosition = PositionPanel(self.parametersPanel.gbTrackingAid)
        self.parametersPanel.pnlTrackingPosition.btnCalculater.hide()
        self.parametersPanel.pnlTrackingPosition.hideframe_Altitude()
        self.parametersPanel.pnlTrackingPosition.setObjectName("pnlTrackingPosition")
        self.parametersPanel.vl_gbTrackingAid.insertWidget(1, self.parametersPanel.pnlTrackingPosition)
        # self.connect(self.parametersPanel.pnlNavAid, SIGNAL("positionChanged"), self.initResultPanel)

        self.parametersPanel.pnlIntersectingPosition = PositionPanel(self.parametersPanel.gbIntersectingAid)
        self.parametersPanel.pnlIntersectingPosition.btnCalculater.hide()
        self.parametersPanel.pnlIntersectingPosition.hideframe_Altitude()
        self.parametersPanel.pnlIntersectingPosition.setObjectName("pnlIntersectingPosition")
        self.parametersPanel.vl_gbIntersectingAid.insertWidget(1, self.parametersPanel.pnlIntersectingPosition)
        # self.connect(self.parametersPanel.pnlNavAid, SIGNAL("positionChanged"), self.initResultPanel)


        self.parametersPanel.cmbTrackingType.addItems([Captions.VOR, Captions.NDB, Captions.LOC])
        self.parametersPanel.cmbIntersectingType.addItems([Captions.VOR, Captions.NDB, Captions.DME])

        self.parametersPanel.cmbTrackingType.currentIndexChanged.connect(self.method_30)
        self.parametersPanel.cmbIntersectingType.currentIndexChanged.connect(self.method_30)
        # self.parametersPanel.btnCaptureTrackingRadialTrack.clicked.connect(self.captureTrackingRadialTrack)
        # self.parametersPanel.btnCaptureIntersectingRadialTrack.clicked.connect(self.captureIntersectingRadialTrack)
        self.parametersPanel.btnMeasureDmeOffset.clicked.connect(self.measureDmeOffset)
        self.parametersPanel.btnMeasureIntersectingDistance.clicked.connect(self.measureIntersectingDistance)
        self.parametersPanel.chb0dmeAtThr.clicked.connect(self.method_30)
        self.method_30()
        self.parametersPanel.btnClose.clicked.connect(self.dlgClose)
        self.parametersPanel.btnClose_2.clicked.connect(self.dlgClose)
    def dlgClose(self):
        self.accept()

    def altitudeFtChanged(self):
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtAltitudeM.setText(str(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude.text()))))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")


    def altitudeMChanged(self):
        if self.flag==0:
            self.flag=1;
        if self.flag==2:
            self.flag=0;
        if self.flag==1:
            try:
                self.parametersPanel.txtAltitude.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAltitudeM.text())), 4)))
            except:
                self.parametersPanel.txtAltitude.setText("0.0")


    # def captureBearing(self):
    #     self.captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrackRadial)
    #     define._canvas.setMapTool(self.captureTrackTool)

    # def captureTrackingRadialTrack(self):
    #     captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrackingRadialTrack)
    #     define._canvas.setMapTool(captureTrackTool)
    # def captureIntersectingRadialTrack(self):
    #     captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtIntersectingRadialTrack)
    #     define._canvas.setMapTool(captureTrackTool)
    def measureDmeOffset(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtDmeOffset, DistanceUnits.M)
        define._canvas.setMapTool(measureDistanceTool)
    def measureIntersectingDistance(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtIntersectingDistance, DistanceUnits.NM)
        define._canvas.setMapTool(measureDistanceTool)
    def method_30(self):
        if (self.parametersPanel.cmbTrackingType.currentIndex() != 0):
            self.parametersPanel.txtTrackingRadialTrack.Caption = Captions.TRACK
        else:
            self.parametersPanel.txtTrackingRadialTrack.Caption = Captions.RADIAL;
        if (self.parametersPanel.cmbIntersectingType.currentIndex() != 0):
            self.parametersPanel.txtIntersectingRadialTrack.Caption = Captions.TRACK
        else:
            self.parametersPanel.txtIntersectingRadialTrack.Caption = Captions.RADIAL
        self.parametersPanel.txtIntersectingRadialTrack.Visible = self.parametersPanel.cmbIntersectingType.currentIndex() < 2
        self.parametersPanel.frame_IntersectingDistance.setVisible(self.parametersPanel.cmbIntersectingType.currentIndex() == 2);
        self.parametersPanel.pnl0dmeAtThr.setVisible(self.parametersPanel.cmbIntersectingType.currentIndex() == 2);
        self.parametersPanel.frame_DmeOffset.setEnabled(self.parametersPanel.chb0dmeAtThr.isChecked())
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
    def saveData(self):
        try:
            filePathDir = QFileDialog.getSaveFileName(self, "Save Input Data",QCoreApplication.applicationDirPath (),"Xml Files(*.xml)")
            if filePathDir == "":
                return
            DataHelper.saveInputParameters(filePathDir, self)
            return filePathDir
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)

    def openData(self):
        try:
            filePathDir = QFileDialog.getOpenFileName(self, "Open Input Data",QCoreApplication.applicationDirPath (),"Xml Files(*.xml)")
            if filePathDir == "":
                return
            DataHelper.loadInputParameters(filePathDir, self)
            return filePathDir
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
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