# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import SurfaceTypes, ObstacleTableColumnType, ObstacleAreaResult, TurnDirection
from FlightPlanner.MASegment.ui_MASegment import Ui_MASegment
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.helpers import MathHelper, Unit, Distance, DistanceUnits, AltitudeUnits, Altitude, SpeedUnits, Speed
from FlightPlanner.Captions import Captions
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Prompts import Prompts
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, SecondaryObstacleArea, SecondaryObstacleAreaWithManyPoints, SecondaryAreaStraight
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.DataHelper import DataHelper
from map.tools import QgsMapToolSelectUtils
from Type.switch import switch

from PyQt4.QtCore import SIGNAL, QCoreApplication, QObject, Qt, QRect
from PyQt4.QtGui import QColor, QMessageBox, QFileDialog, QMenu, QLabel, QStandardItem
from qgis.core import QGis, QgsVectorLayer, QgsGeometry, QgsField, QgsFeature, QgsRectangle
from qgis.gui import  QgsMapTool, QgsRubberBand, QgsMapToolPan, QgsMapCanvasSnapper
import define, math

class MASegmentDlg(FlightPlanBaseDlg):
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("MASegmentDlg")
        self.surfaceType = SurfaceTypes.MASegment
        self.selectedRow = None
        self.editingModelIndex = None

        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.MASegment)
        self.resize(600, 650)
        QgisHelper.matchingDialogSize(self, 600, 700)
        self.surfaceList = None
        self.manualPolygon = None
        
        self.DeltaDistance = 0.5

        self.resultObstacleAreaList = []
        self.nominalTrackLayer = None
        self.resultLayerList = []
    def btnPDTCheck_Click(self):
        ipFAFPos = self.parametersPanel.pnlFafPos.Point3d
        ipMAPtPos = self.parametersPanel.pnlMaptPos.Point3d
        ipMAENDPos = self.parametersPanel.pnlMaEndPos.Point3d
        alpha = math.fabs(MathHelper.getBearing(ipFAFPos, ipMAPtPos) - MathHelper.getBearing(ipMAPtPos, ipMAENDPos)) * 180 / math.pi;
        # ApproachSegProceCheck chkDlg = new ApproachSegProceCheck();

        m_iFinalInitInter = 7;

        if (alpha > 15):
            m_bNoError1 = False;
            m_pTxtWarning1 = "Straight missed approach turn should be less than or equal to 15 degrees. See PANS OPS Part1-Section 4, Chapter 6.3.";
            m_pTxtResult1 = "Your turn is {0} degrees which is more than 15 degrees".format(str(alpha));

        else:
            m_bNoError1 = True;
            m_pTxtWarning1 = "Straight missed approach turn which are less than or equal to 15 degrees are in accordance within PANS OPS.";
            m_pTxtResult1 = "Your turn is {0} degrees which is less than 15 degrees".format(str(alpha));

        # ShowDialog(this);

        strTitle = "Missed Approach Segment Procedure Check";
        # this.Text = strTitle;

        resStr = "";

        resultStr = m_pTxtWarning1 + m_pTxtResult1 + "\n";
        QMessageBox.warning(self, strTitle, resultStr)

    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        # self.ui.btnConstruct.setVisible(False)
        # self.ui.btnEvaluate.setVisible(False)
        # self.ui.btnPDTCheck.setVisible(False)
        # self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)

#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)

    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")
        if filePathDir == "":
            return
        # self.filterList = ["Faf", "Ma"]
        # for surf in self.surfaceList:
        #     self.filterList.append(surf.type)
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, self.surfaceType, self.ui.tblObstacles, None, parameterList, resultHideColumnNames)

    def getParameterList(self):
        parameterList = []
        parameterList.append((self.parametersPanel.gbMASegmentType.Caption, "group"))
        parameterList.append(("Type", self.parametersPanel.txtMASegmentType.Value))

        parameterList.append(("Positions", "group"))
        self.ui.tabCtrlGeneral.setCurrentIndex(0)

        if self.parametersPanel.pnlFafPos.Visible:
            parameterList.append((self.parametersPanel.pnlFafPos.Caption, "group"))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlFafPos.txtPointX.text()), float(self.parametersPanel.pnlFafPos.txtPointY.text()))
            parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
            parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
            parameterList.append(("X", self.parametersPanel.pnlFafPos.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlFafPos.txtPointY.text()))
        if self.parametersPanel.pnlMaptPos.Visible:
            parameterList.append((self.parametersPanel.pnlMaptPos.Caption, "group"))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlMaptPos.txtPointX.text()), float(self.parametersPanel.pnlMaptPos.txtPointY.text()))
            parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
            parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
            parameterList.append(("X", self.parametersPanel.pnlMaptPos.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlMaptPos.txtPointY.text()))
        if self.parametersPanel.pnlMaTpPos.Visible:
            parameterList.append((self.parametersPanel.pnlMaTpPos.Caption, "group"))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlMaTpPos.txtPointX.text()), float(self.parametersPanel.pnlMaTpPos.txtPointY.text()))
            parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
            parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
            parameterList.append(("X", self.parametersPanel.pnlMaTpPos.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlMaTpPos.txtPointY.text()))
        if self.parametersPanel.gbMaEndPos.Visible:
            parameterList.append((self.parametersPanel.gbMaEndPos.Caption, "group"))
            parameterList.append(("Type", self.parametersPanel.cmbMaEndType.SelectedItem))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlMaEndPos.txtPointX.text()), float(self.parametersPanel.pnlMaEndPos.txtPointY.text()))
            parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
            parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
            parameterList.append(("X", self.parametersPanel.pnlMaEndPos.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlMaEndPos.txtPointY.text()))
        if self.parametersPanel.gbNavAid.Visible:
            parameterList.append((self.parametersPanel.gbNavAid.Caption, "group"))
            parameterList.append(("Type", self.parametersPanel.cmbNavAidType.SelectedItem))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlNavAidPos.txtPointX.text()), float(self.parametersPanel.pnlNavAidPos.txtPointY.text()))
            parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
            parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
            parameterList.append(("X", self.parametersPanel.pnlNavAidPos.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlNavAidPos.txtPointY.text()))
        if self.parametersPanel.gbAddNavAid.Visible:
            parameterList.append((self.parametersPanel.gbAddNavAid.Caption, "group"))
            parameterList.append(("Type", self.parametersPanel.cmbNavAidType.SelectedItem))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlAddNavAidPos.txtPointX.text()), float(self.parametersPanel.pnlAddNavAidPos.txtPointY.text()))
            parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
            parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
            parameterList.append(("X", self.parametersPanel.pnlAddNavAidPos.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlAddNavAidPos.txtPointY.text()))

        parameterList.append(("Parameters", "group"))



        if self.parametersPanel.cmbTypeMapt.Visible:
            parameterList.append((self.parametersPanel.cmbTypeMapt.Caption, self.parametersPanel.cmbTypeMapt.SelectedItem))
        if self.parametersPanel.cmbTypeTP.Visible:
            parameterList.append((self.parametersPanel.cmbTypeTP.Caption, self.parametersPanel.cmbTypeTP.SelectedItem))
        if self.parametersPanel.cmbAircraftCatgory.Visible:
            parameterList.append((self.parametersPanel.cmbAircraftCatgory.Caption, self.parametersPanel.cmbAircraftCatgory.SelectedItem))
        if self.parametersPanel.cmbDirection.Visible:
            parameterList.append((self.parametersPanel.cmbDirection.Caption, self.parametersPanel.cmbDirection.SelectedItem))
        if self.parametersPanel.pnlAerodromeAlt.Visible:
            parameterList.append((self.parametersPanel.pnlAerodromeAlt.Caption, str(self.parametersPanel.pnlAerodromeAlt.Value.Metres) + "m"))
            parameterList.append(("", str(self.parametersPanel.pnlAerodromeAlt.Value.Feet) + "ft"))
        if self.parametersPanel.pnlPrimaryMoc.Visible:
            parameterList.append((self.parametersPanel.pnlPrimaryMoc.Caption, str(self.parametersPanel.pnlPrimaryMoc.Value.Metres) + "m"))
            parameterList.append(("", str(self.parametersPanel.pnlPrimaryMoc.Value.Feet) + "ft"))
        if self.parametersPanel.pnlOCA.Visible:
            parameterList.append((self.parametersPanel.pnlOCA.Caption, str(self.parametersPanel.pnlOCA.Value.Metres) + "m"))
            parameterList.append(("", str(self.parametersPanel.pnlOCA.Value.Feet) + "ft"))
        if self.parametersPanel.pnlTpAlt.Visible:
            parameterList.append((self.parametersPanel.pnlTpAlt.Caption, str(self.parametersPanel.pnlTpAlt.Value.Metres) + "m"))
            parameterList.append(("", str(self.parametersPanel.pnlTpAlt.Value.Feet) + "ft"))
        if self.parametersPanel.pnlEndTurnAlt.Visible:
            parameterList.append((self.parametersPanel.pnlEndTurnAlt.Caption, str(self.parametersPanel.pnlEndTurnAlt.Value.Metres) + "m"))
            parameterList.append(("", str(self.parametersPanel.pnlEndTurnAlt.Value.Feet) + "ft"))
        if self.parametersPanel.pnlEndAlt.Visible:
            parameterList.append((self.parametersPanel.pnlEndAlt.Caption, str(self.parametersPanel.pnlEndAlt.Value.Metres) + "m"))
            parameterList.append(("", str(self.parametersPanel.pnlEndAlt.Value.Feet) + "ft"))
        if self.parametersPanel.pnlTurnGradient.Visible:
            parameterList.append((self.parametersPanel.pnlTurnGradient.Caption, str(self.parametersPanel.pnlTurnGradient.Value.Percent) + "%"))
        if self.parametersPanel.pnlBearing.Visible:
            parameterList.append((self.parametersPanel.pnlBearing.Caption, str(self.parametersPanel.pnlBearing.Value)))
        if self.parametersPanel.pnlDistance.Visible:
            parameterList.append((self.parametersPanel.pnlDistance.Caption, str(self.parametersPanel.pnlDistance.Value.NauticalMiles) + "nm"))
        if self.parametersPanel.pnlClimbGradient.Visible:
            parameterList.append((self.parametersPanel.pnlClimbGradient.Caption, str(self.parametersPanel.pnlClimbGradient.Value.Percent) + "%"))
        if self.parametersPanel.cmbTrackGuidance.Visible:
            parameterList.append((self.parametersPanel.cmbTrackGuidance.Caption, self.parametersPanel.cmbTrackGuidance.SelectedItem))
        if self.parametersPanel.cmbAddTrackGuidance.Visible:
            parameterList.append((self.parametersPanel.cmbAddTrackGuidance.Caption, self.parametersPanel.cmbAddTrackGuidance.SelectedItem))
        if self.parametersPanel.cmbTurnMAPt.Visible:
            parameterList.append((self.parametersPanel.cmbTurnMAPt.Caption, self.parametersPanel.cmbTurnMAPt.SelectedItem))
        if self.parametersPanel.gbTpTolerance.Visible:
            parameterList.append((self.parametersPanel.gbTpTolerance.Caption, "group"))
            parameterList.append((self.parametersPanel.txtKEarlist.Caption, str(self.parametersPanel.txtKEarlist.Value) + "nm"))
            parameterList.append((self.parametersPanel.txtLatestFix.Caption, str(self.parametersPanel.txtLatestFix.Value) + "nm"))
            parameterList.append((self.parametersPanel.txtC.Caption, str(self.parametersPanel.txtC.Value) + "nm"))
            parameterList.append((self.parametersPanel.txtLatestTurn.Caption, str(self.parametersPanel.txtLatestTurn.Value) + "nm"))
        if self.parametersPanel.gbNominalTrack.Visible:
            parameterList.append((self.parametersPanel.gbNominalTrack.Caption, "group"))
            parameterList.append((self.parametersPanel.pnlTrueStartTrack.Caption, str(self.parametersPanel.pnlTrueStartTrack.Value)))
            parameterList.append((self.parametersPanel.pnlTrueEndTrack.Caption, str(self.parametersPanel.pnlTrueEndTrack.Value)))
            parameterList.append((self.parametersPanel.txtArcLength.Caption, str(self.parametersPanel.txtArcLength.Value) + "nm"))
        if self.parametersPanel.gbVelocity.Visible:
            parameterList.append((str(self.parametersPanel.gbVelocity.Caption).replace(",", "_"), "group"))
            parameterList.append((self.parametersPanel.txtISAVAR.Caption, str(self.parametersPanel.txtISAVAR.Value)))
            parameterList.append((self.parametersPanel.pnlIAS.Caption, str(self.parametersPanel.pnlIAS.Value.Knots) + "kts"))
            # parameterList.append((self.parametersPanel.pnlWind.lblIA.text(), str(self.parametersPanel.pnlWind.Value.Knots) + "kts"))
            parameterList.append((self.parametersPanel.pnlTAS.Caption, str(self.parametersPanel.pnlTAS.Value.Knots) + "kts"))
        if self.parametersPanel.gbTurn.Visible:
            parameterList.append((self.parametersPanel.gbTurn.Caption, "group"))
            parameterList.append((self.parametersPanel.txtBankAngle.Caption, str(self.parametersPanel.txtBankAngle.Value)))
            parameterList.append((self.parametersPanel.txtRateOfTurn.Caption, str(self.parametersPanel.txtRateOfTurn.Value)))
            parameterList.append((self.parametersPanel.txtWindEffect.Caption, str(self.parametersPanel.txtWindEffect.Value)))
        if self.parametersPanel.gbMAPtTolerance.Visible:
            parameterList.append((self.parametersPanel.gbMAPtTolerance.Caption, "group"))
            parameterList.append((self.parametersPanel.txtEarlist.Caption, str(self.parametersPanel.txtEarlist.Value) + "nm"))
            parameterList.append((self.parametersPanel.txtLatest.Caption, str(self.parametersPanel.txtLatest.Value) + "nm"))
            parameterList.append((self.parametersPanel.txtD.Caption, str(self.parametersPanel.txtD.Value) + "nm"))
        if self.parametersPanel.gbMAPtToSocDist.Visible:
            parameterList.append((self.parametersPanel.gbMAPtToSocDist.Caption, "group"))
            parameterList.append((self.parametersPanel.txtX.Caption, str(self.parametersPanel.txtX.Value) + "nm"))
            parameterList.append((self.parametersPanel.txtDistMAPtSOC.Caption, str(self.parametersPanel.txtDistMAPtSOC.Value.NauticalMiles) + "nm"))
        if self.parametersPanel.txtEarlistTemp.Visible:
            parameterList.append((self.parametersPanel.txtEarlistTemp.Caption, str(self.parametersPanel.txtEarlistTemp.Value)))
        if self.parametersPanel.txtLatestTemp.Visible:
            parameterList.append((self.parametersPanel.txtLatestTemp.Caption, str(self.parametersPanel.txtLatestTemp.Value)))

        self.ui.tabCtrlGeneral.setCurrentIndex(1)

        parameterList.append(("Results / Checked Obstacles", "group"))
        parameterList.append(("Checked Obstacles", "group"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        return parameterList

    def btnEvaluate_Click(self):
        primaryMoc = None
        sect = self.parametersPanel.cmbTrackGuidance.SelectedIndex

        self.obstaclesModel = MASegmentObstacles(self.resultObstacleAreaList, self.parametersPanel.pnlPrimaryMoc.Value, self.parametersPanel.pnlClimbGradient.Value.Percent, self.parametersPanel.pnlOCA.Value, sect);

        return FlightPlanBaseDlg.btnEvaluate_Click(self)

    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        self.resultObstacleAreaList = []
        nominalTrackPolylineArea = PolylineArea()
        resultPolylineAreaList = []
        if (self.parametersPanel.cmbTrackGuidance.SelectedIndex == 0):
            if (self.parametersPanel.cmbAddTrackGuidance.SelectedIndex == 0):
                self.DrawMAStraightSegmentWithAdditonalNAV(resultPolylineAreaList, nominalTrackPolylineArea);
            else:
                self.DrawMAStraightSegmentWithoutAdditonalNAV(resultPolylineAreaList, nominalTrackPolylineArea);
        else:
            self.DrawMAStraightSegmentWithNoTrack(resultPolylineAreaList, nominalTrackPolylineArea);

        nominalTrackLayer = AcadHelper.createNominalTrackLayer(nominalTrackPolylineArea.method_14(), None, "memory", "NominalTrack_" + self.surfaceType.replace(" ", "_").replace("-", "_"))
        constructLayer = AcadHelper.createVectorLayer(self.surfaceType + "_Straight")

        if len(resultPolylineAreaList) == 0:
            return
        for polylineArea in resultPolylineAreaList:
            AcadHelper.setGeometryAndAttributesInLayer(constructLayer, polylineArea, True)
        QgisHelper.appendToCanvas(define._canvas, [nominalTrackLayer, constructLayer], self.surfaceType)
        QgisHelper.zoomToLayers([nominalTrackLayer, constructLayer])
        self.resultLayerList = [nominalTrackLayer, constructLayer]
        # }

        # IFeatureLayer iFLayer = new FeatureLayerClass();
        # iFLayer.FeatureClass = ipFeatureClass;
        # string layerName = ipFeatureClass.AliasName;
        # iFLayer.Name = layerName;
        # m_iMap.AddLayer(iFLayer);
        #
        # IFeatureLayer iOtherLayer = new FeatureLayerClass();
        # iOtherLayer.FeatureClass = ipFeatureClassOther;
        # iOtherLayer.Name = ipFeatureClassOther.AliasName;
        # m_iMap.AddLayer(iOtherLayer);
        #
        # m_ipMapControl.Extent = iFLayer.AreaOfInterest;
        #
        self.ui.btnEvaluate.setEnabled(True);
        # savetechnicalReportToolStripMenuItem.Enabled = true;
    def DrawMAStraightSegmentWithoutAdditonalNAV(self, resultPolylineAreaList, nominalTrackPolylineArea):
        # POLYLINE_FIELD featureField;
        # //enumAreaID = areaFinalApproach;
        # featureField.areaID = enumArea.areaMA;
        # featureField.bearing = 0;
        # featureField.siAlt = 0;
        # featureField.nonsiAlt = 0;

        TotalWith = [2.5, 2.0];
        LimitDistance = [13.8, 21.9];
        DefaultWidth = 10.0;

        # double dblStWidth;
        # double dblDis;
        m_iNAVAID = self.parametersPanel.cmbNavAidType.SelectedIndex
        # for (int i = 0; i < 2; i++)
        # {
        #     TotalWith[i] = MathHelper.ConvertUnit(m_iMap.MapUnits, cocaUnitSystem.sysNonsi, cocaUnitType.whatDist, TotalWith[i], false);
        #     LimitDistance[i] = MathHelper.ConvertUnit(m_iMap.MapUnits, cocaUnitSystem.sysNonsi, cocaUnitType.whatDist, LimitDistance[i], false);
        # }
        # DefaultWidth = MathHelper.ConvertUnit(m_iMap.MapUnits, cocaUnitSystem.sysNonsi, cocaUnitType.whatDist, DefaultWidth, false);
        dblStWidth = 2 * TotalWith[m_iNAVAID];
        dblDis = LimitDistance[m_iNAVAID];

        # m_nSegmentCount = 2;
        # m_ipPrimary = new IPolyline[2];
        # m_ipSecondary = new IPolyline[4];

        # IPoint ipSp, ipEp;
        m_ipNAVAIDPos = self.parametersPanel.pnlNavAidPos.Point3d
        m_ipFAFPos = self.parametersPanel.pnlFafPos.Point3d
        m_ipMAPtPos = self.parametersPanel.pnlMaptPos.Point3d

        m_dblEarlist = Unit.ConvertNMToMeter(self.parametersPanel.txtEarlist.Value)
        m_dblDistMAPtSOC = self.parametersPanel.txtDistMAPtSOC.Value.Metres
        if (math.fabs(MathHelper.getBearing(m_ipNAVAIDPos, m_ipFAFPos) - MathHelper.getBearing(m_ipNAVAIDPos, m_ipMAPtPos)) > math.pi / 2):
            ipSp = MathHelper.distanceBearingPoint(m_ipMAPtPos, MathHelper.getBearing(m_ipMAPtPos, m_ipNAVAIDPos), m_dblEarlist);
            ipEp = MathHelper.distanceBearingPoint(m_ipMAPtPos, MathHelper.getBearing(m_ipNAVAIDPos, m_ipMAPtPos), m_dblDistMAPtSOC);
        else:
            ipSp = MathHelper.distanceBearingPoint(m_ipMAPtPos, MathHelper.getBearing(m_ipNAVAIDPos, m_ipMAPtPos), m_dblEarlist);
            ipEp = MathHelper.distanceBearingPoint(m_ipMAPtPos, MathHelper.getBearing(m_ipMAPtPos, m_ipNAVAIDPos), m_dblDistMAPtSOC);



        # //////////////////////////////////////////////////////////////////////////
        # // draw nominal track
        m_ipMAENDPos = self.parametersPanel.pnlMaEndPos.Point3d
        # IPolyline ipPolyLineNominal = new PolylineClass();
        # IPointCollection ipPColNominal = (IPointCollection)ipPolyLineNominal;
        nominalTrackPolylineArea.Add(PolylineAreaPoint(ipSp));
        nominalTrackPolylineArea.Add(PolylineAreaPoint(ipEp));
        nominalTrackPolylineArea.Add(PolylineAreaPoint(m_ipMAENDPos))
        # ipPolyLineNominal.SpatialReference = m_SpatialReference;
        # MathHelper.Create_PolylineFeature((IGeometry)ipPolyLineNominal, ref iFeatureClassother, featureField);

        # //////////////////////////////////////////////////////////////////////////

        # MathHelper.AddGeometryToMapAsGraphics((IGeometry)m_ipMAPtPos, m_iMap, 15);
        # MathHelper.AddGeometryToMapAsGraphics((IGeometry)ipEp, m_iMap, 15);

        dblWidthEarlist = self.GetSegmentWidth(m_ipNAVAIDPos, ipSp, m_iNAVAID);
        dblWidthSOC = self.GetSegmentWidth(m_ipNAVAIDPos, ipEp, m_iNAVAID);

        # //if (dblWidthSOC < DefaultWidth)
        self.DrawProtectionCase1(ipSp, dblWidthEarlist, ipEp, dblWidthSOC, resultPolylineAreaList);
        # //else
        #     //DrawProtectionCase2(ipSp, dblWidthEarlist, ipEp, dblWidthSOC, dblDis, iDrawStyle, 0, ref iFeatureClass);

        ipSp = ipEp;
        ipEp = m_ipMAENDPos;
        dblMAENDWidth = self.GetSegmentWidth(m_ipNAVAIDPos, ipEp, m_iNAVAID);
        # //if (dblMAENDWidth < DefaultWidth)
        self.DrawProtectionCase1(ipSp, dblWidthSOC, ipEp, dblMAENDWidth, resultPolylineAreaList);
    def DrawMAStraightSegmentWithNoTrack(self, resultPolylineAreaList, nominalTrackPolylineArea):
        # POLYLINE_FIELD featureField;
        # //enumAreaID = areaFinalApproach;
        # featureField.areaID = enumArea.areaMA;
        # featureField.bearing = 0;
        # featureField.siAlt = 0;
        # featureField.nonsiAlt = 0;

        TotalWith = [2.5, 2.0];
        LimitDistance = [13.8, 21.9];
        DefaultWidth = 10.0;

        # double dblStWidth;
        # double dblDis;
        m_iNAVAID = self.parametersPanel.cmbNavAidType.SelectedIndex
        # for (int i = 0; i < 2; i++)
        # {
        #     TotalWith[i] = MathHelper.ConvertUnit(m_iMap.MapUnits, cocaUnitSystem.sysNonsi, cocaUnitType.whatDist, TotalWith[i], false);
        #     LimitDistance[i] = MathHelper.ConvertUnit(m_iMap.MapUnits, cocaUnitSystem.sysNonsi, cocaUnitType.whatDist, LimitDistance[i], false);
        # }
        # DefaultWidth = MathHelper.ConvertUnit(m_iMap.MapUnits, cocaUnitSystem.sysNonsi, cocaUnitType.whatDist, DefaultWidth, false);
        dblStWidth = 2 * TotalWith[m_iNAVAID];
        dblDis = LimitDistance[m_iNAVAID];

        # m_nSegmentCount = 1;
        # m_ipPrimary = new IPolyline[1];
        # m_ipSecondary = new IPolyline[2];
        # 
        # IPoint ipSp, ipEp;
        m_ipNAVAIDPos = self.parametersPanel.pnlNavAidPos.Point3d
        m_ipFAFPos = self.parametersPanel.pnlFafPos.Point3d
        m_ipMAPtPos = self.parametersPanel.pnlMaptPos.Point3d
        m_ipMAENDPos = self.parametersPanel.pnlMaEndPos.Point3d

        m_dblEarlist = Unit.ConvertNMToMeter(self.parametersPanel.txtEarlist.Value)
        m_dblDistMAPtSOC = self.parametersPanel.txtDistMAPtSOC.Value.Metres

        if (math.fabs(MathHelper.getBearing(m_ipNAVAIDPos, m_ipFAFPos) - MathHelper.getBearing(m_ipNAVAIDPos, m_ipMAPtPos)) > math.pi / 2):
            ipSp = MathHelper.distanceBearingPoint(m_ipMAPtPos, MathHelper.getBearing(m_ipMAPtPos, m_ipNAVAIDPos), m_dblEarlist);
            ipEp = MathHelper.distanceBearingPoint(m_ipMAPtPos, MathHelper.getBearing(m_ipNAVAIDPos, m_ipMAPtPos), m_dblDistMAPtSOC);
        else:
            ipSp = MathHelper.distanceBearingPoint(m_ipMAPtPos, MathHelper.getBearing(m_ipNAVAIDPos, m_ipMAPtPos), m_dblEarlist);
            ipEp = MathHelper.distanceBearingPoint(m_ipMAPtPos, MathHelper.getBearing(m_ipMAPtPos, m_ipNAVAIDPos), m_dblDistMAPtSOC);



        # //////////////////////////////////////////////////////////////////////////
        # // draw nominal track 

        # IPolyline ipPolyLineNominal = new PolylineClass();
        # IPointCollection ipPColNominal = (IPointCollection)ipPolyLineNominal;
        nominalTrackPolylineArea.Add(PolylineAreaPoint(ipSp));
        # //ipPColNominal.AddPoint(ipEp);
        nominalTrackPolylineArea.Add(PolylineAreaPoint(m_ipMAENDPos));
        # ipPolyLineNominal.SpatialReference = m_SpatialReference;
        # MathHelper.Create_PolylineFeature((IGeometry)ipPolyLineNominal, ref iFeatureClassother, featureField);
        # 
        # //////////////////////////////////////////////////////////////////////////
        # 
        # MathHelper.AddGeometryToMapAsGraphics((IGeometry)m_ipMAPtPos, m_iMap, 15);
        # MathHelper.AddGeometryToMapAsGraphics((IGeometry)ipEp, m_iMap, 15);

        dblWidthEarlist = self.GetSegmentWidth(m_ipNAVAIDPos, ipSp, m_iNAVAID);
        dblWidthSOC = self.GetSegmentWidth(m_ipNAVAIDPos, ipEp, m_iNAVAID);

        # //if (dblWidthSOC < DefaultWidth)

        tempAlpha = math.atan2((dblWidthSOC - dblWidthEarlist) / 2, MathHelper.calcDistance(ipSp, ipEp)) + 15 * math.pi / 180;
        dblMAENDWidth = dblWidthEarlist + 2 * MathHelper.calcDistance(ipSp, m_ipMAENDPos) * math.tan(tempAlpha);

        # double dblDistance;
        dblDistance = MathHelper.calcDistance(ipSp, m_ipMAENDPos);
        if (dblDistance < 0.000001): return;

        # double dblBearing;
        dblBearing = MathHelper.getBearing(ipSp, m_ipMAENDPos);

        ipPoint = [None, None, None, None];
        # for (int i = 0; i < 4; i++) ipPoint[i] = new PointClass();

        # // draw primary area
        # bool bStoreFeature = iDrawStyle != 1 ? true : false;
        ipPoint[0] = MathHelper.distanceBearingPoint(ipSp, dblBearing + math.pi / 2, dblWidthEarlist / 2);
        ipPoint[3] = MathHelper.distanceBearingPoint(ipSp, dblBearing - math.pi / 2, dblWidthEarlist / 2);
        ipPoint[1] = MathHelper.distanceBearingPoint(m_ipMAENDPos, dblBearing + math.pi / 2, dblMAENDWidth / 2);
        ipPoint[2] = MathHelper.distanceBearingPoint(m_ipMAENDPos, dblBearing - math.pi / 2, dblMAENDWidth / 2);

        resultPolylineAreaList.append(PolylineArea(ipPoint))
        self.resultObstacleAreaList.append(PrimaryObstacleArea(PolylineArea(ipPoint)))
        # IPointCollection PrimaryColl = new MultipointClass();
        # for (int i = 0; i < 4; i++) PrimaryColl.AddPoint(ipPoint[i]);
        # PrimaryColl.AddPoint(ipPoint[0]);
        # m_ipPrimary[0] = MakePolyLineFromPointCollection(PrimaryColl, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);

    def DrawMAStraightSegmentWithAdditonalNAV(self, resultPolylineSreaList, nominalTrackPolylineArea):
        # POLYLINE_FIELD featureField;
        # #enumAreaID = areaFinalApproach;
        # featureField.areaID = enumArea.areaMA;
        # featureField.bearing = 0;
        # featureField.siAlt = 0;
        # featureField.nonsiAlt = 0;

        TotalWith = [2.5, 2.0 ];
        LimitDistance = [13.8, 21.9 ];
        DefaultWidth = 10.0;

        dblStWidth = None;
        dblDis = None;
        m_iNAVAID = self.parametersPanel.cmbNavAidType.SelectedIndex

        # for i in range(2):
        #     TotalWith[i] = MathHelper.ConvertUnit(m_iMap.MapUnits, cocaUnitSystem.sysNonsi, cocaUnitType.whatDist, TotalWith[i], false);
        #     LimitDistance[i] = MathHelper.ConvertUnit(m_iMap.MapUnits, cocaUnitSystem.sysNonsi, cocaUnitType.whatDist, LimitDistance[i], false);
        # }
        # DefaultWidth = MathHelper.ConvertUnit(m_iMap.MapUnits, cocaUnitSystem.sysNonsi, cocaUnitType.whatDist, DefaultWidth, false);
        dblStWidth = 2 * TotalWith[m_iNAVAID];
        dblDis = LimitDistance[m_iNAVAID];

        m_nSegmentCount = 2;
        # m_ipPrimary = new IPolyline[2];
        # m_ipSecondary = new IPolyline[4];

        # IPoint ipSp, ipEp;
        m_ipMAPtPos = self.parametersPanel.pnlMaptPos.Point3d
        m_ipNAVAIDPos = self.parametersPanel.pnlNavAidPos.Point3d
        m_dblEarlist = Unit.ConvertNMToMeter(self.parametersPanel.txtEarlist.Value)
        m_dblDistMAPtSOC = self.parametersPanel.txtDistMAPtSOC.Value.Metres
        ipSp = MathHelper.distanceBearingPoint(m_ipMAPtPos, MathHelper.getBearing(m_ipMAPtPos, m_ipNAVAIDPos), m_dblEarlist);
        ipEp = MathHelper.distanceBearingPoint(m_ipMAPtPos, MathHelper.getBearing(m_ipNAVAIDPos, m_ipMAPtPos), m_dblDistMAPtSOC);

        m_ipMAENDPos = self.parametersPanel.pnlMaEndPos.Point3d
        #####################################
        # draw nominal track
        nominalTrackPolylineArea.Add(PolylineAreaPoint(ipSp))
        nominalTrackPolylineArea.Add(PolylineAreaPoint(ipEp))
        nominalTrackPolylineArea.Add(PolylineAreaPoint(m_ipMAENDPos))

        # IPolyline ipPolyLineNominal = new PolylineClass();
        # IPointCollection ipPColNominal = (IPointCollection)ipPolyLineNominal;
        # ipPColNominal.AddPoint(ipSp);
        # ipPColNominal.AddPoint(ipEp);
        # ipPColNominal.AddPoint(m_ipMAENDPos);
        # ipPolyLineNominal.SpatialReference = m_SpatialReference;
        # MathHelper.Create_PolylineFeature((IGeometry)ipPolyLineNominal, ref ipFeatureClassOther, featureField);

        #####################################

        # MathHelper.AddGeometryToMapAsGraphics((IGeometry)m_ipMAPtPos, m_iMap, 15);
        # MathHelper.AddGeometryToMapAsGraphics((IGeometry)ipEp, m_iMap, 15);

        dblWidthEarlist = self.GetSegmentWidth(m_ipNAVAIDPos, ipSp, m_iNAVAID);
        dblWidthSOC = self.GetSegmentWidth(m_ipNAVAIDPos, ipEp, m_iNAVAID);
        m_ipAddNAVAIDPos = self.parametersPanel.pnlAddNavAidPos.Point3d
        m_iAddNAVAID = self.parametersPanel.cmbAddNavAidType.SelectedIndex
        dblWidthEarlistAdd = self.GetSegmentWidth(m_ipAddNAVAIDPos, ipSp, m_iAddNAVAID);
        dblWidthSOCAdd = self.GetSegmentWidth(m_ipAddNAVAIDPos, ipEp, m_iAddNAVAID);

        self.DrawProtectionCase3(ipSp, dblWidthEarlist,dblWidthEarlistAdd, ipEp, dblWidthSOC, dblWidthSOCAdd, resultPolylineSreaList);

        ipSp = ipEp;
        ipEp = m_ipMAENDPos;
        dblMAENDWidth = self.GetSegmentWidth(m_ipNAVAIDPos, ipEp, m_iNAVAID);
        dblMAENDWidthAdd = self.GetSegmentWidth(m_ipAddNAVAIDPos, ipEp, m_iAddNAVAID);

        self.DrawProtectionCase3(ipSp, dblWidthSOC, dblWidthSOCAdd, ipEp, dblMAENDWidth, dblMAENDWidthAdd, resultPolylineSreaList);
    def DrawProtectionCase1(self, ipStPoint, StWidth, ipEdPoint, EdWidth, resultPolylineSreaList):

        # POLYLINE_FIELD featureField;
        # featureField.areaID = enumArea.areaFinalApproach;
        # featureField.bearing = 0;
        # featureField.nonsiAlt = 0;
        # featureField.siAlt = 0;
        #
        # double dblDistance;
        dblDistance = MathHelper.calcDistance(ipStPoint, ipEdPoint);
        if (dblDistance < 0.000001):
            return;

        # double dblBearing;
        dblBearing = MathHelper.getBearing(ipStPoint, ipEdPoint);

        ipPoint = [None, None, None, None];
        # for (int i = 0; i < 4; i++) ipPoint[i] = new PointClass();

        # draw primary area
        # bool bStoreFeature = iDrawStyle != 1 ? true : false;
        ipPoint[0] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing + math.pi / 2, StWidth / 4);
        ipPoint[3] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing - math.pi / 2, StWidth / 4);
        ipPoint[1] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing + math.pi / 2, EdWidth / 4);
        ipPoint[2] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing - math.pi / 2, EdWidth / 4);

        resultPolylineSreaList.append(PolylineArea(ipPoint))
        self.resultObstacleAreaList.append(PrimaryObstacleArea(PolylineArea(ipPoint)))
        # IPointCollection PrimaryColl = new MultipointClass();
        # for (int i = 0; i < 4; i++) PrimaryColl.AddPoint(ipPoint[i]);
        # PrimaryColl.AddPoint(ipPoint[0]);
        # m_ipPrimary[iSegment] = MakePolyLineFromPointCollection(PrimaryColl, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);

        # draw 1st secondary area
        # bStoreFeature = iDrawStyle != 0 ? true : false;
        ipPoint[0] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing + math.pi / 2, StWidth / 2);
        ipPoint[3] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing + math.pi / 2, StWidth / 4);
        ipPoint[1] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing + math.pi / 2, EdWidth / 2);
        ipPoint[2] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing + math.pi / 2, EdWidth / 4);

        resultPolylineSreaList.append(PolylineArea(ipPoint))
        self.resultObstacleAreaList.append(SecondaryObstacleArea(ipPoint[2], ipPoint[3], ipPoint[1], ipPoint[0]))
        # IPointCollection Secondary1Coll = new MultipointClass();
        # for (int i = 0; i < 4; i++) Secondary1Coll.AddPoint(ipPoint[i]);
        # Secondary1Coll.AddPoint(ipPoint[0]);
        # m_ipSecondary[2 * iSegment] = MakePolyLineFromPointCollection(Secondary1Coll, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);

        # draw 2nd secondary area
        ipPoint[3] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing - math.pi / 2, StWidth / 2);
        ipPoint[0] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing - math.pi / 2, StWidth / 4);
        ipPoint[2] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing - math.pi / 2, EdWidth / 2);
        ipPoint[1] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing - math.pi / 2, EdWidth / 4);

        resultPolylineSreaList.append(PolylineArea(ipPoint))
        self.resultObstacleAreaList.append(SecondaryObstacleArea(ipPoint[0], ipPoint[1], ipPoint[3], ipPoint[2]))
        # IPointCollection Secondary2Coll = new MultipointClass();
        # for (int i = 0; i < 4; i++) Secondary2Coll.AddPoint(ipPoint[i]);
        # Secondary2Coll.AddPoint(ipPoint[0]);
        # m_ipSecondary[2 * iSegment + 1] = MakePolyLineFromPointCollection(Secondary2Coll, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);

    def DrawProtectionCase2(self, ipStPoint, StWidth, ipEdPoint, EdWidth, dblDis, resultPolylineSreaList):
        # POLYLINE_FIELD featureField;
        # featureField.areaID = enumArea.areaFinalApproach;
        # featureField.bearing = 0;
        # featureField.nonsiAlt = 0;
        # featureField.siAlt = 0;
        # double dblDistance;
        dblDistance = MathHelper.calcDistance(ipStPoint, ipEdPoint);
        if (dblDistance < 0.000001):
            return;

        # double dblBearing;
        dblBearing = MathHelper.getBearing(ipStPoint, ipEdPoint);

        ipPoint = [None, None, None, None, None, None];
        # IPoint ipMdPoint = new PointClass();
        # for (int i = 0; i < 6; i++) ipPoint[i] = new PointClass();

        ipMdPoint = MathHelper.distanceBearingPoint(ipStPoint, dblBearing, dblDis);

        # // draw primary area
        # bool bStoreFeature = iDrawStyle != 1 ? true : false;
        ipPoint[0] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing + math.pi / 2, StWidth / 4);
        ipPoint[5] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing - math.pi / 2, StWidth / 4);
        ipPoint[2] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing + math.pi / 2, EdWidth / 4);
        ipPoint[3] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing - math.pi / 2, EdWidth / 4);
        ipPoint[1] = MathHelper.distanceBearingPoint(ipMdPoint, dblBearing + math.pi / 2, EdWidth / 4);
        ipPoint[4] = MathHelper.distanceBearingPoint(ipMdPoint, dblBearing - math.pi / 2, EdWidth / 4);

        resultPolylineSreaList.append(PolylineArea(ipPoint))
        self.resultObstacleAreaList.append(PrimaryObstacleArea(PolylineArea(ipPoint)))
        # IPointCollection PrimaryColl = new MultipointClass();
        # for (int i = 0; i < 6; i++) PrimaryColl.AddPoint(ipPoint[i]);
        # PrimaryColl.AddPoint(ipPoint[0]);
        # m_ipPrimary[iSegment] = MakePolyLineFromPointCollection(PrimaryColl, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);
        #
        # // draw 1st secondary area
        # bStoreFeature = iDrawStyle != 0 ? true : false;
        ipPoint[0] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing + math.pi / 2, StWidth / 2);
        ipPoint[5] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing + math.pi / 2, StWidth / 4);
        ipPoint[2] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing + math.pi / 2, EdWidth / 2);
        ipPoint[3] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing + math.pi / 2, EdWidth / 4);
        ipPoint[1] = MathHelper.distanceBearingPoint(ipMdPoint, dblBearing + math.pi / 2, EdWidth / 2);
        ipPoint[4] = MathHelper.distanceBearingPoint(ipMdPoint, dblBearing + math.pi / 2, EdWidth / 4);

        resultPolylineSreaList.append(PolylineArea(ipPoint))
        self.resultObstacleAreaList.append(SecondaryObstacleAreaWithManyPoints(PolylineArea(ipPoint), PolylineArea([ipPoint[3], ipPoint[4], ipPoint[5]])))
        # IPointCollection Secondary1Coll = new MultipointClass();
        # for (int i = 0; i < 6; i++) Secondary1Coll.AddPoint(ipPoint[i]);
        # Secondary1Coll.AddPoint(ipPoint[0]);
        # m_ipSecondary[2 * iSegment] = MakePolyLineFromPointCollection(Secondary1Coll, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);
        #
        # // draw 2nd secondary area
        ipPoint[5] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing - math.pi / 2, StWidth / 2);
        ipPoint[0] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing - math.pi / 2, StWidth / 4);
        ipPoint[3] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing - math.pi / 2, EdWidth / 2);
        ipPoint[2] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing - math.pi / 2, EdWidth / 4);
        ipPoint[4] = MathHelper.distanceBearingPoint(ipMdPoint, dblBearing - math.pi / 2, EdWidth / 2);
        ipPoint[1] = MathHelper.distanceBearingPoint(ipMdPoint, dblBearing - math.pi / 2, EdWidth / 4);

        resultPolylineSreaList.append(PolylineArea(ipPoint))
        self.resultObstacleAreaList.append(SecondaryObstacleAreaWithManyPoints(PolylineArea(ipPoint), PolylineArea([ipPoint[0], ipPoint[1], ipPoint[2]])))

        # IPointCollection Secondary2Coll = new MultipointClass();
        # for (int i = 0; i < 6; i++) Secondary2Coll.AddPoint(ipPoint[i]);
        # Secondary2Coll.AddPoint(ipPoint[0]);
        # m_ipSecondary[2 * iSegment + 1] = MakePolyLineFromPointCollection(Secondary2Coll, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);

    def DrawProtectionCase3(self, ipStPoint, StWidth, StAddWidth, ipEdPoint, EdWidth, EdAddWidth, resultPolylineSreaList):
        # POLYLINE_FIELD featureField;
        # featureField.areaID = enumArea.areaFinalApproach;
        # featureField.bearing = 0;
        # featureField.nonsiAlt = 0;
        # featureField.siAlt = 0;
        # 
        # double dblDistance;
        dblDistance = MathHelper.calcDistance(ipStPoint, ipEdPoint);
        if (dblDistance < 0.0000001):
            return;

        # double dblBearing;
        dblBearing = MathHelper.getBearing(ipStPoint, ipEdPoint);

        ipPoint = []
        for i in range(10):
            ipPoint.append(None)

        ipPoint[0] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing + math.pi / 2, StWidth / 2);
        ipPoint[3] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing - math.pi / 2, StWidth / 2);
        ipPoint[1] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing + math.pi / 2, EdWidth / 2);
        ipPoint[2] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing - math.pi / 2, EdWidth / 2);

        ipPoint[7] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing + math.pi / 2, StAddWidth / 2);
        ipPoint[6] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing - math.pi / 2, StAddWidth / 2);
        ipPoint[4] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing + math.pi / 2, EdAddWidth / 2);
        ipPoint[5] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing - math.pi / 2, EdAddWidth / 2);

        # IPointCollection PrimaryColl = new MultipointClass();
        # IPointCollection Secondary1Coll = new MultipointClass();
        # IPointCollection Secondary2Coll = new MultipointClass();

        if (EdAddWidth >= EdWidth):
            self.DrawProtectionCase1(ipStPoint, StWidth, ipEdPoint, EdWidth, resultPolylineSreaList);
            return;
        elif (StAddWidth < StWidth):
            self.DrawProtectionCase1(ipStPoint, StAddWidth, ipEdPoint, EdAddWidth, resultPolylineSreaList);
            return;
        else:
            # IPoint temp1 = new PointClass();
            # IPoint temp2 = new PointClass();
            temp1 = MathHelper.getIntersectionPoint(ipPoint[0], ipPoint[1], ipPoint[7], ipPoint[4]);
            ipPoint[8] = temp1;
            temp2 = MathHelper.getIntersectionPoint(ipPoint[3], ipPoint[2], ipPoint[6], ipPoint[5]);
            ipPoint[9] = temp2;

            ipNewPoint = [None, None, None, None, None, None]
            # for i in range(6):
            #     ipNewPoint[i] = None

            ipNewPoint[0] = MathHelper.GetInsidePointForSegment(ipPoint[0], ipPoint[3], 3);
            ipNewPoint[5] = MathHelper.GetInsidePointForSegment(ipPoint[3], ipPoint[0], 3);
            ipNewPoint[1] = MathHelper.GetInsidePointForSegment(ipPoint[8], ipPoint[9], 3);
            ipNewPoint[4] = MathHelper.GetInsidePointForSegment(ipPoint[9], ipPoint[8], 3);
            ipNewPoint[2] = MathHelper.GetInsidePointForSegment(ipPoint[4], ipPoint[5], 3);
            ipNewPoint[3] = MathHelper.GetInsidePointForSegment(ipPoint[5], ipPoint[4], 3);

            # # draw primary area
            # bool bStoreFeature = iDrawStyle != 1 ? true : false;
            resultPolylineSreaList.append(PolylineArea(ipNewPoint))
            self.resultObstacleAreaList.append(PrimaryObstacleArea(PolylineArea(ipNewPoint)))
            # for i in range(6):
            #     PrimaryColl.AddPoint(ipNewPoint[i]);
            # PrimaryColl.AddPoint(ipNewPoint[0]);
            # m_ipPrimary[iSegment] = MakePolyLineFromPointCollection(PrimaryColl, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);

            # # draw secondary area
            # bStoreFeature = iDrawStyle != 0 ? true : false;
            resultPolylineSreaList.append(PolylineArea([ipPoint[0], ipPoint[8], ipPoint[4],
                                                        ipNewPoint[2], ipNewPoint[1], ipNewPoint[0],
                                                        ipPoint[0]]))
            self.resultObstacleAreaList.append(SecondaryObstacleAreaWithManyPoints(PolylineArea([ipPoint[0], ipPoint[8], ipPoint[4],
                                                        ipNewPoint[2], ipNewPoint[1], ipNewPoint[0],
                                                        ipPoint[0]]),
                                                    PolylineArea(ipNewPoint[2], ipNewPoint[1], ipNewPoint[0])))
        #     Secondary1Coll.AddPoint(ipPoint[0]); Secondary1Coll.AddPoint(ipPoint[8]); Secondary1Coll.AddPoint(ipPoint[4]);
        #     Secondary1Coll.AddPoint(ipNewPoint[2]); Secondary1Coll.AddPoint(ipNewPoint[1]); Secondary1Coll.AddPoint(ipNewPoint[0]);
        #     Secondary1Coll.AddPoint(ipPoint[0]);
        #     m_ipSecondary[2 * iSegment] = MakePolyLineFromPointCollection(Secondary1Coll, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);
            resultPolylineSreaList.append(PolylineArea([ipNewPoint[5], ipNewPoint[4], ipNewPoint[3],
                                                        ipPoint[5], ipPoint[9], ipPoint[3],
                                                        ipNewPoint[5]]))
            self.resultObstacleAreaList.append(SecondaryObstacleAreaWithManyPoints(PolylineArea([ipNewPoint[5], ipNewPoint[4], ipNewPoint[3],
                                                        ipPoint[5], ipPoint[9], ipPoint[3],
                                                        ipNewPoint[5]]),
                                                    PolylineArea(ipNewPoint[5], ipNewPoint[4], ipNewPoint[3])))

        #     Secondary2Coll.AddPoint(ipNewPoint[5]); Secondary2Coll.AddPoint(ipNewPoint[4]); Secondary2Coll.AddPoint(ipNewPoint[3]);
        #     Secondary2Coll.AddPoint(ipPoint[5]); Secondary2Coll.AddPoint(ipPoint[9]); Secondary2Coll.AddPoint(ipPoint[3]);
        #     Secondary2Coll.AddPoint(ipNewPoint[5]);
        #     m_ipSecondary[2 * iSegment + 1] = MakePolyLineFromPointCollection(Secondary2Coll, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);
        #
        # }
    def GetSegmentWidth(self, ipNAVAID, ipFAF, iNAVAID):
        TotalWith = [2.5, 2.0 ];
        SplayAngle = [ 10.3, 7.8 ]
        LimitDistance = [ 13.8, 21.9 ]
        DefaultWidth = 10.0;

        # for (int i = 0; i < 2; i++)
        # {
        #     SplayAngle[i] = SplayAngle[i] * math.pi / 180;
        #     TotalWith[i] = MathHelper.ConvertUnit(mapUnit, cocaUnitSystem.sysNonsi, cocaUnitType.whatDist, TotalWith[i], false);
        #     LimitDistance[i] = MathHelper.ConvertUnit(mapUnit, cocaUnitSystem.sysNonsi, cocaUnitType.whatDist, LimitDistance[i], false);
        # }
        # DefaultWidth = MathHelper.ConvertUnit(mapUnit, cocaUnitSystem.sysNonsi, cocaUnitType.whatDist, DefaultWidth, false);


        # double dblDistance, dblRes, dblLimitDistance;
        dblDistance = MathHelper.calcDistance(ipFAF, ipNAVAID);

        if (iNAVAID == 2):
            dblLimitDistance = Unit.ConvertNMToMeter(7)#MathHelper.ConvertUnit(mapUnit, cocaUnitSystem.sysNonsi, cocaUnitType.whatDist, 7, false);
        else:
            dblLimitDistance = Unit.ConvertNMToMeter(LimitDistance[iNAVAID]);
        dblRes = None
        if (dblDistance >= LimitDistance[iNAVAID]):
            dblRes = DefaultWidth;
        else:
            dblRes = 2 * TotalWith[iNAVAID] + (DefaultWidth - 2 * TotalWith[iNAVAID]) * dblDistance / LimitDistance[iNAVAID];

        return Unit.ConvertNMToMeter(dblRes);
    def selectLineResult(self, selectedFeatures):
        pass

    def initParametersPan(self):
        ui = Ui_MASegment()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.SegmentType = ["Final Segment", "Intermediate Segment Straight", "Intermediate Segment With IF",
                       "Intermediate Segment With No IF", "Initial Segment Straight", "Initial Segment DME ARCS"]


        self.connect(self.parametersPanel.pnlFafPos, SIGNAL("positionChanged"), self.pnlFafPos_PositionChanged)
        self.connect(self.parametersPanel.pnlMaptPos, SIGNAL("positionChanged"), self.CalcFAF_MAPtDistance)
        # self.connect(self.parametersPanel.pnlDerPos, SIGNAL("positionChanged"), self.changeDistGradient)
        self.connect(self.parametersPanel.cmbTypeMapt, SIGNAL("Event_0"), self.cmbTypeMAPt_SelectedIndexChanged)
        self.connect(self.parametersPanel.cmbTypeTP, SIGNAL("Event_0"), self.comboTypeTP_Turn_SelectedIndexChanged)

        self.connect(self.parametersPanel.cmbAircraftCatgory, SIGNAL("Event_0"), self.comboAcftCategory_SelectedIndexChanged)
        self.connect(self.parametersPanel.pnlIAS, SIGNAL("Event_0"), self.textIASVelocity_TextChanged)
        self.connect(self.parametersPanel.txtISAVAR, SIGNAL("Event_0"), self.textIASVelocity_TextChanged)
        self.connect(self.parametersPanel.pnlTAS, SIGNAL("Event_0"), self.textTASVelocity_TextChanged)
        self.connect(self.parametersPanel.txtLatest, SIGNAL("Event_0"), self.textLatest_TextChanged)
        self.connect(self.parametersPanel.txtX, SIGNAL("Event_0"), self.textLatest_TextChanged)

        self.connect(self.parametersPanel.pnlAerodromeAlt, SIGNAL("Event_0"), self.textAerodromeAlt_TextChanged)
        self.connect(self.parametersPanel.pnlDistance, SIGNAL("Event_0"), self.textDistance_TextChanged)

    def comboTypeTP_Turn_SelectedIndexChanged(self):
        iSelect = self.parametersPanel.cmbTypeTP.SelectedIndex;

        for case in switch (iSelect):
            if case(0):
                self.parametersPanel.cmbTurnMAPt.Enabled = False;
                self.parametersPanel.txtKEarlist.Value = self.parametersPanel.txtEarlistTemp.Value;
                self.parametersPanel.txtLatestFix.Text = self.parametersPanel.txtLatestTemp.Value;
                break;
            elif case(1):
                self.parametersPanel.cmbTurnMAPt.Enabled = True;
                self.parametersPanel.txtLatestFix.Value = 0;
                self.CalcMATPPosition();
                if (self.parametersPanel.cmbTurnMAPt.SelectedIndex == 1):
                    self.parametersPanel.txtKEarlist.Value = self.parametersPanel.txtEarlistTemp.Value;
                else:
                    self.parametersPanel.txtKEarlist.Value = self.parametersPanel.txtEarlist.Value
                break;
            elif case(2):
                self.parametersPanel.cmbTurnMAPt.Enabled = False;

                self.parametersPanel.txtKEarlist.Value = self.parametersPanel.txtEarlist.Value
                self.parametersPanel.txtLatestFix.Value = self.parametersPanel.txtLatest.Value
                self.parametersPanel.txtLatestTurn.Value = self.parametersPanel.txtLatestTemp.Value;
                break;
    def CalcMATPPosition(self):
        m_ipNAVAIDPos = self.parametersPanel.pnlNavAidPos.Point3d
        m_ipFAFPos = self.parametersPanel.pnlFafPos.Point3d
        m_ipMAPtPos = self.parametersPanel.pnlMaptPos.Point3d
        ipMATPPos = None
        m_dblDistMAPtSOC = self.parametersPanel.txtDistMAPtSOC.Value.Metres
        if (math.fabs(MathHelper.getBearing(m_ipNAVAIDPos, m_ipFAFPos) - MathHelper.getBearing(m_ipNAVAIDPos, m_ipMAPtPos)) > math.pi / 2):
            ipMATPPos = MathHelper.distanceBearingPoint(m_ipMAPtPos, MathHelper.getBearing(m_ipNAVAIDPos, m_ipMAPtPos), m_dblDistMAPtSOC);
        else:
            ipMATPPos = MathHelper.distanceBearingPoint(m_ipMAPtPos, MathHelper.getBearing(m_ipMAPtPos, m_ipNAVAIDPos), m_dblDistMAPtSOC);

        try:
            alpha = math.pi / 2 - Unit.ConvertDegToRad(self.parametersPanel.pnlBearing.Value)
            dis = (self.parametersPanel.pnlTpAlt.Value.Metres - self.parametersPanel.pnlOCA.Value.Metres) / self.parametersPanel.pnlClimbGradient.Value.Percent * 100;
            ipMATPPos = MathHelper.distanceBearingPoint(ipMATPPos, alpha, dis);
        except:
            return
        self.parametersPanel.pnlMaTpPos.Point3d = ipMATPPos

    def textAerodromeAlt_TextChanged(self):
        k = self.calc_factorK();
        ## #TAS = k * IAS
        buff = self.parametersPanel.pnlIAS.Value.Knots;
        tas = k * buff;
        # if (tas < 0.000001) textTASVelocity.Text = "";
        self.parametersPanel.pnlTAS.Value = Speed(tas, SpeedUnits.KTS);

        if ( self.parametersPanel.cmbTypeMapt.SelectedIndex == 2 ):
            self.CalcEarlist_Latest_MAPtSOC_ForTiming();
    def textLatest_TextChanged(self):
        if (self.parametersPanel.cmbTypeMapt.SelectedIndex == 2):
            return;
        latest = self.parametersPanel.txtLatest.Value;
        x = self.parametersPanel.txtX.Value;
        self.parametersPanel.txtDistMAPtSOC.Value = Distance(latest + x, DistanceUnits.NM);

    def pnlFafPos_PositionChanged(self):
        self.CalcMAPtPosition()
        self.CalcFAF_MAPtDistance()
    def CalcFAF_MAPtDistance(self):
        try:
            dist = MathHelper.calcDistance(self.parametersPanel.pnlFafPos.Point3d, self.parametersPanel.pnlMaptPos.Point3d)
            self.parametersPanel.pnlDistance.Value = Distance(dist)
        except:
            pass
    def textDistance_TextChanged(self):
        # if ( textDistance.Focused ) CalcMAPtPosition();
        self.CalcMAPtPosition()
        if (self.parametersPanel.cmbTypeMapt.SelectedIndex == 2):
            self.CalcEarlist_Latest_MAPtSOC_ForTiming();
    def CalcMAPtPosition(self):
        ipFAFPos = self.parametersPanel.pnlFafPos.Point3d
        ipMAPtPos = self.parametersPanel.pnlMaptPos.Point3d
        angleFAF_MAPt = MathHelper.getBearing(ipFAFPos, ipMAPtPos);
        distanceFAF_MAPt = self.parametersPanel.pnlDistance.Value.Metres;
        # distanceFAF_MAPt = MathHelper.distanceBearingPoint(m_iMap.MapUnits, m_unitSys, cocaUnitType.whatDist, distanceFAF_MAPt, false);

        ipMAPtPos = MathHelper.distanceBearingPoint(ipFAFPos, angleFAF_MAPt, distanceFAF_MAPt);
        self.parametersPanel.pnlMaptPos.Point3d = ipMAPtPos

    def textTASVelocity_TextChanged(self):
        # double d, X;
        d = self.calc_D();
        self.parametersPanel.txtD.Value = d;
        X = self.calc_X();
        self.parametersPanel.txtX.Value = X;
    def calc_D(self):
        # string buff;
        # double tas = 0, d;

        # try
        # {
        tas = self.parametersPanel.pnlTAS.Value.Knots;
        # tas = Convert.ToDouble(buff);
        # }
        # catch (System.Exception ex)
        # {
        #
        # }

        # if (m_unitSys == cocaUnitSystem.sysSi)
        #     d = (tas + 19) * 3 / 3600;
        # else
        #     d = (tas + 10) * 3 / 3600;
        d = (tas + 10) * 3 / 3600;
        return d;
    def calc_X(self):
        # string buff;
        # double tas = 0, X;
        # int time, iCategory;
        #
        # try
        # {
        tas = self.parametersPanel.pnlTAS.Value.Knots
        # tas = Convert.ToDouble(buff);
        # }
        # catch (System.Exception ex)
        # {
        #
        # }

        iCategory = self.parametersPanel.cmbAircraftCatgory.SelectedIndex;

        if (iCategory == -1):
            return -1;
        elif (iCategory < 5):
            time = 15;
        else:
            time = 5;

        # if (m_unitSys == cocaUnitSystem.sysSi)
        #     X = (tas + 19) * time / 3600;
        # else
        #     X = (tas + 10) * time / 3600;
        X = (tas + 10) * time / 3600;
        return X;
    def textIASVelocity_TextChanged(self):
        # string buff;
        # double k, tas;

        k = self.calc_factorK();
        ## #TAS = k * IAS
        buff = self.parametersPanel.pnlIAS.Value.Knots;
        tas = k * buff;
        # if (tas < 0.000001) textTASVelocity.Text = "";
        self.parametersPanel.pnlTAS.Value = Speed(tas, SpeedUnits.KTS);
    def calc_factorK(self):
        # double k, isa, alt = 0;
        # string buff;
        # 
        # # Altitude = Initial Altitude - NAV Altitude  
        
        alt = self.parametersPanel.pnlAerodromeAlt.Value.Feet;
        # alt = Convert.ToDouble(buff);

        # if (m_unitSys == cocaUnitSystem.sysSi) alt += 300;
        alt += 1000;

        # # k Calculation
        isa = self.parametersPanel.txtISAVAR.Value;
        # isa = GetISA_VAR_cel(buff);


        k = 171233 * math.pow(288 + isa - 0.006496 * alt, 0.5) / math.pow(288 - 0.006496 * alt, 2.628);

        return k;
    def cmbTypeMAPt_SelectedIndexChanged(self):
        selectIndex = self.parametersPanel.cmbTypeMapt.SelectedIndex;

        if (selectIndex == 0):
            self.parametersPanel.pnlDistance.Enabled = False;
            self.parametersPanel.pnlFafPos.Visible = True;
            # axToolbarSelectFAFFIX.Visible = False;
            # axToolbarSelectFix.Visible = False;
            self.parametersPanel.pnlMaptPos.Visible = True;

            # textEarlist.Text = "0";
            # textLatest.Text = "0";
        elif (selectIndex == 1):
            self.parametersPanel.pnlDistance.Enabled = False;
            self.parametersPanel.pnlFafPos.Visible = True;
            self.parametersPanel.pnlMaptPos.Visible = False;
            # axToolbarSelectFix.Visible = True;
            # axToolbarMAPtPickup.Visible = False;
            # axToolbarFAFPickup.Visible = True;
            # axToolbarSelectFAFFIX.Visible = False;

            # textEarlist.Text = "";
            # textLatest.Text = "";
        else :
            self.parametersPanel.pnlDistance.Enabled = True;
            self.parametersPanel.pnlFafPos.Visible = False;
            self.parametersPanel.pnlMaptPos.Visible = True;

            # axToolbarSelectFix.Visible = False;
            # axToolbarMAPtPickup.Visible = True;
            # axToolbarFAFPickup.Visible = False;
            # axToolbarSelectFAFFIX.Visible = True;

            # textEarlist.Text = "";
            # textLatest.Text = "";
            # #CalcEarlist_Latest_MAPtSOC_ForTiming();
    def comboAcftCategory_SelectedIndexChanged(self):

        buff = None;
        nItem = self.parametersPanel.cmbAircraftCatgory.SelectedIndex;
        if self.parametersPanel.txtMASegmentType.Value == "Straight":
            for case in switch (nItem):
                if case(0): ## Aircraft Category A
                    buff = 100#(m_unitSys == cocaUnitSystem.sysSi ? "185" : "100"); break;
                    break
                elif case(1): ## Aircraft Category B
                    buff = 130#(m_unitSys == cocaUnitSystem.sysSi ? "240" : "130"); break;
                    break
                elif case(2): ## Aircraft Category C
                    buff = 160#(m_unitSys == cocaUnitSystem.sysSi ? "295" : "160"); break;
                    break
                elif case(3): ## Aircraft Category D
                    buff = 185#(m_unitSys == cocaUnitSystem.sysSi ? "345" : "185"); break;
                    break
                elif case(4): ## Aircraft Category E
                    buff = 230#(m_unitSys == cocaUnitSystem.sysSi ? "425" : "230"); break;
                    break
                elif case(5): ## Aircraft Category H
                    buff = 90#(m_unitSys == cocaUnitSystem.sysSi ? "165" : "90"); break;
                else: ## nothing
                    buff = 0;
                    break;
            self.parametersPanel.pnlIAS.Value = Speed(buff);
            if (self.parametersPanel.cmbTypeMapt.SelectedIndex == 2):
                self.CalcEarlist_Latest_MAPtSOC_ForTiming();
        else:
            for case in switch (nItem):
                if case(0): ## Aircraft Category A
                    buff = 110#(m_unitSys == cocaUnitSystem.sysSi ? "185" : "100"); break;
                    break
                elif case(1): ## Aircraft Category B
                    buff = 150#(m_unitSys == cocaUnitSystem.sysSi ? "240" : "130"); break;
                    break
                elif case(2): ## Aircraft Category C
                    buff = 240#(m_unitSys == cocaUnitSystem.sysSi ? "295" : "160"); break;
                    break
                elif case(3): ## Aircraft Category D
                    buff = 265#(m_unitSys == cocaUnitSystem.sysSi ? "345" : "185"); break;
                    break
                elif case(4): ## Aircraft Category E
                    buff = 275#(m_unitSys == cocaUnitSystem.sysSi ? "425" : "230"); break;
                    break
                elif case(5): ## Aircraft Category H
                    buff = 90#(m_unitSys == cocaUnitSystem.sysSi ? "165" : "90"); break;
                else: ## nothing
                    buff = 0;
                    break;
            self.parametersPanel.pnlIAS.Value = Speed(buff);



    def CalcEarlist_Latest_MAPtSOC_ForTiming(self):
        iCategory = self.parametersPanel.cmbAircraftCatgory.SelectedIndex;
        # double disFAF_MAPt, dblA, dblB, dblAlt, TASMIN, TASMAX, kmin, kmax, X1, X2, X3, X4, X5, X6;
        # double dblEarlist, dblLatest, dblMAPtSOC;

        # try
        # {
        dblA = self.parametersPanel.txtEarlistTemp.Value;
        dblB = self.parametersPanel.txtLatestTemp.Value
        disFAF_MAPt = self.parametersPanel.pnlDistance.Value.NauticalMiles;
        dblAlt = self.parametersPanel.pnlAerodromeAlt.Value.Feet;
        #     #if (m_unitSys == cocaUnitSystem.sysSi) disFAF_MAPt *= 1000;
        #     #else disFAF_MAPt = MathHelper.ConvertValueFromUnits(disFAF_MAPt, cocaUnitType.whatDist, cocaUnitSystem.sysNonsi) * 1000;
        # }
        # catch (System.Exception ex)
        # {
        #     return;
        # }
        kmin = 171233 * math.pow(288 - 10 - 0.006496 * dblAlt, 0.5) / math.pow(288 - 0.006496 * dblAlt, 2.628);
        kmax = 171233 * math.pow(288 + 15 - 0.006496 * dblAlt, 0.5) / math.pow(288 - 0.006496 * dblAlt, 2.628);

        IASMIN = [130, 155, 215, 240, 285, 110, 70, 85, 115, 130, 155, 60]
        IASMAX = [185, 240, 295, 345, 425, 165, 100, 130, 160, 185, 230, 90 ]

        if (iCategory == -1):
            return;



        # if (m_unitSys == cocaUnitSystem.sysSi)
        # {
        #     TASMIN = IASMIN[iCategory] * kmin;
        #     TASMAX = IASMAX[iCategory] * kmax;
        #     X1 = math.pow( math.pow(dblA, 2) + math.pow(TASMIN * 10 /3600, 2) + math.pow(56 * disFAF_MAPt / TASMIN, 2), 0.5);
        #     X2 = math.pow(math.pow(dblA, 2) + math.pow(TASMAX * 10 / 3600, 2) + math.pow(56 * disFAF_MAPt / TASMAX, 2), 0.5);
        #     X3 = math.pow(math.pow(dblB, 2) + math.pow(TASMIN * 13 / 3600, 2) + math.pow(56 * disFAF_MAPt / TASMIN, 2), 0.5);
        #     X4 = math.pow(math.pow(dblB, 2) + math.pow(TASMAX * 13 / 3600, 2) + math.pow(56 * disFAF_MAPt / TASMAX, 2), 0.5);
        #     X5 = math.pow(math.pow(dblB, 2) + math.pow(TASMIN * 13 / 3600, 2) + math.pow(56 * disFAF_MAPt / TASMIN, 2), 0.5) + 15 * (TASMIN + 19) / 3600;
        #     X6 = math.pow(math.pow(dblB, 2) + math.pow(TASMAX * 13 / 3600, 2) + math.pow(56 * disFAF_MAPt / TASMAX, 2), 0.5) + 15 * (TASMAX + 19) / 3600;
        # }
        # else
        TASMIN = IASMIN[iCategory + 5] * kmin;
        TASMAX = IASMAX[iCategory + 5] * kmax;
        X1 = math.pow(math.pow(dblA, 2) + math.pow(TASMIN * 10 / 3600, 2) + math.pow(30 * disFAF_MAPt / TASMIN, 2), 0.5);
        X2 = math.pow(math.pow(dblA, 2) + math.pow(TASMAX * 10 / 3600, 2) + math.pow(30 * disFAF_MAPt / TASMAX, 2), 0.5);
        X3 = math.pow(math.pow(dblB, 2) + math.pow(TASMIN * 13 / 3600, 2) + math.pow(30 * disFAF_MAPt / TASMIN, 2), 0.5);
        X4 = math.pow(math.pow(dblB, 2) + math.pow(TASMAX * 13 / 3600, 2) + math.pow(30 * disFAF_MAPt / TASMAX, 2), 0.5);
        X5 = math.pow(math.pow(dblB, 2) + math.pow(TASMIN * 13 / 3600, 2) + math.pow(30 * disFAF_MAPt / TASMIN, 2), 0.5) + 15 * (TASMIN + 19) / 3600;
        X6 = math.pow(math.pow(dblB, 2) + math.pow(TASMAX * 13 / 3600, 2) + math.pow(30 * disFAF_MAPt / TASMAX, 2), 0.5) + 15 * (TASMAX + 19) / 3600;
        

        dblEarlist = max([X1, X2]);
        dblLatest = max([X3, X4]);
        dblMAPtSOC = max([X5, X6]);

        self.parametersPanel.txtEarlist.Value = dblEarlist;
        self.parametersPanel.txtLatest.Value = dblLatest;
        self.parametersPanel.txtDistMAPtSOC.Value = Distance(dblMAPtSOC, DistanceUnits.NM);
    def Point3dsComparer(self,a, b):
        if (a.get_X() < b.get_X()):
            return -1;
        if (a.get_X() > b.get_X()):
            return 1;
        if (a.get_Y() < b.get_Y()):
            return -1;
        if (a.get_Y() > b.get_Y()):
            return 1;
        if (a.get_Z() < b.get_Z()):
            return -1;
        if (a.get_Z() > b.get_Z()):
            return 1;
        return 0;
class SegmentType:
    Final = "Final Segment"
    InterStraight = "Intermediate Segment Straight"
    InterWithIf = "Intermediate Segment With IF"
    InterWithNoIf = "Intermediate Segment With No IF"
    InitStraight = "Initial Segment Straight"
    InitArc = "Initial Segment DME ARCS"

class RubberBandPolygon(QgsMapTool):
    def __init__(self, canvas, parent):
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
        self.pointCount = 0
        self.parentDlg = parent
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
            self.pointCount += 1
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
            self.parentDlg.show()
            self.pointCount = 0
            define._canvas.setToolTip("")
            define._messageLabel.setText("")
            self.emit(SIGNAL("outputResult"), self.polygonGeom)


    def canvasMoveEvent( self, e ):
        if self.pointCount == 0:
            define._canvas.setToolTip(Prompts.START_POINT_OF_OBSTACLE_AREA_OR)
            define._messageLabel.setText(Prompts.START_POINT_OF_OBSTACLE_AREA_OR)
        else:
            define._canvas.setToolTip(Prompts.NEXT_POINT_OF_OBSTACLE_AREA_OR)
            define._messageLabel.setText(Prompts.NEXT_POINT_OF_OBSTACLE_AREA_OR)
        if ( self.mRubberBand == None ):
            return
        if ( self.mRubberBand.numberOfVertices() > 0 ):
            self.mRubberBand.removeLastPoint( 0 )
            self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )

    def deactivate(self):
#         self.rubberBand.reset(QGis.Point)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))

class SelectLine(QgsMapTool):

    def __init__(self, canvas, stringMsg = None, parent = None):
        self.mCanvas = canvas
        # self.areaType = areaType
        QgsMapTool.__init__(self, canvas)
        self.mCursor = Qt.ArrowCursor
        self.mRubberBand = None
        self.mDragging = False
        self.mSelectRect = QRect()
        self.mRubberBandResult = None
        self.mSnapper = QgsMapCanvasSnapper(canvas)
        self.lineCount = 0
        self.resultGeomList = []
        self.geomList = []
        self.area = None
        self.isFinished = False
        self.stringMsg = stringMsg
        self.msgMenu = None
        self.parentDlg = parent
        if self.stringMsg != None:
            define._canvas.setToolTip(stringMsg)
            pass


            # self.msgMenu = self.createContextMenu(self.stringMsg)
#     QgsRubberBand* mRubberBand;
#     def reset(self):
#         self.startPoint = None
#         self.endPoint = None
#         self.isDrawing = False
#         SelectByRect.RubberRect.reset(QGis.Polygon)
#         self.layer = self.canvas.currentLayer()
    def createContextMenu(self, msg):
        label = QLabel(msg)
        # actionEnterMsg = QgisHelper.createAction(menu, msg, self.menuMsgClick)
        # menu.addAction(actionEnterMsg)
        return label
    def menuMsgClick(self):
        pass
    def canvasPressEvent(self, e):
        QgisHelper.ClearRubberBandInCanvas(define._canvas)
        self.mSelectRect.setRect( 0, 0, 0, 0 )
        self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
        self.startPoint, self.pointID, self.layer= self.snapPoint(e.pos())

    def canvasMoveEvent(self, e):
        # self.msgMenu.setGeometry()
        # self.msgMenu.exec_(define._canvas.mapToGlobal(e.pos()))
        if ( e.buttons() != Qt.LeftButton ):
            return
        if ( not self.mDragging ):
            self.mDragging = True
            self.mSelectRect.setTopLeft( e.pos() )
        self.mSelectRect.setBottomRight( e.pos() )
        QgsMapToolSelectUtils.setRubberBand( self.mCanvas, self.mSelectRect,self.mRubberBand )

    def canvasReleaseEvent(self, e):
        self.endPoint, self.pointID, self.layer= self.snapPoint(e.pos())

        vlayer = QgsMapToolSelectUtils.getCurrentVectorLayer( self.mCanvas )
        if ( vlayer == None ):
            if ( self.mRubberBand != None):
                self.mRubberBand.reset( QGis.Polygon )
                del self.mRubberBand
                self.mRubberBand = None
                self.mDragging = False
            return


        if (not self.mDragging ):
            QgsMapToolSelectUtils.expandSelectRectangle(self. mSelectRect, vlayer, e.pos() )
        else:
            if ( self.mSelectRect.width() == 1 ):
                self.mSelectRect.setLeft( self.mSelectRect.left() + 1 )
            if ( self.mSelectRect.height() == 1 ):
                self.mSelectRect.setBottom( self.mSelectRect.bottom() + 1 )

        if ( self.mRubberBand != None ):
            QgsMapToolSelectUtils.setRubberBand( self.mCanvas, self.mSelectRect, self.mRubberBand )
            selectGeom = self.mRubberBand.asGeometry()


            selectedFeatures = QgsMapToolSelectUtils.setSelectFeaturesOrRubberband_Tas_1( self.mCanvas, selectGeom, e )
            if len(selectedFeatures) > 0:
                self.emit(SIGNAL("outputResult"), selectedFeatures)
                self.parentDlg.show()


            del selectGeom

            self.mRubberBand.reset( QGis.Polygon )
            del self.mRubberBand
            self.mRubberBand = None
        self.mDragging = False

    def snapPoint(self, p, bNone = False):
        if define._snapping == False:
            return (define._canvas.getCoordinateTransform().toMapCoordinates( p ), None, None)
        snappingResults = self.mSnapper.snapToBackgroundLayers( p )
        if ( snappingResults[0] != 0 or len(snappingResults[1]) < 1 ):

            if bNone:
                return (None, None, None)
            else:
                return (define._canvas.getCoordinateTransform().toMapCoordinates( p ), None, None)
        else:
            return (snappingResults[1][0].snappedVertex, snappingResults[1][0].snappedAtGeometry, snappingResults[1][0].layer)

class MASegmentObstacles(ObstacleTable):
    def __init__(self, surfacesList, primaryMoc, climbGradient, ocaAlt, secttor):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)

        self.surfaceType = SurfaceTypes.MASegment
        self.surfacesList = surfacesList
        self.primaryMoc = primaryMoc.Metres

        self.dblClimbGradient = climbGradient
        self.dblOCA = ocaAlt.Metres
        self.dr = None
        self.m_nSectors = secttor
        # self.altitude = altitude
    def setHiddenColumns(self, tableView):
        tableView.hideColumn(self.IndexTreesFt)
        tableView.hideColumn(self.IndexTreesM)
        # tableView.hideColumn(self.IndexSurface)
        return ObstacleTable.setHiddenColumns(self, tableView)
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        newHeaderCount = 0

        self.IndexObstArea = fixedColumnCount
        self.IndexDrM = fixedColumnCount + 1
        self.IndexMocAppliedM = fixedColumnCount + 2
        self.IndexMocAppliedFt = fixedColumnCount + 3
        self.IndexAltReqM = fixedColumnCount + 4
        self.IndexAltReqFt = fixedColumnCount + 5
        self.IndexPDG = fixedColumnCount + 6
        # self.IndexOcaM = fixedColumnCount + 4
        # self.IndexOcaFt = fixedColumnCount + 5
        # self.IndexSurface = fixedColumnCount + 6
        # self.IndexCritical = fixedColumnCount + 4

        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DrM,
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                ObstacleTableColumnType.AltReqM,
                ObstacleTableColumnType.AltReqFt,
                ObstacleTableColumnType.PDG,
                # ObstacleTableColumnType.OcaM,
                # ObstacleTableColumnType.OcaFt,
                # ObstacleTableColumnType.
                # ObstacleTableColumnType.Critical
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)
#
    def addObstacleToModel(self, obstacle, checkResult):
        ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
        row = self.source.rowCount() - 1

        item = QStandardItem(str(checkResult[0]))
        item.setData(checkResult[0])
        self.source.setItem(row, self.IndexObstArea, item)

        item = QStandardItem(str(checkResult[1]))
        item.setData(checkResult[1])
        self.source.setItem(row, self.IndexDrM, item)

        item = QStandardItem(str(checkResult[2]))
        item.setData(checkResult[2])
        self.source.setItem(row, self.IndexMocAppliedM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[2])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[2]))
        self.source.setItem(row, self.IndexMocAppliedFt, item)

        # item = QStandardItem(str(ObstacleTable.MocMultiplier))
        # item.setData(ObstacleTable.MocMultiplier)
        # self.source.setItem(row, self.IndexMocMultiplier, item)

        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexAltReqM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[3])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[3]))
        self.source.setItem(row, self.IndexAltReqFt, item)

        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4])
        self.source.setItem(row, self.IndexPDG, item)

        # item = QStandardItem(str(checkResult[2]))
        # item.setData(checkResult[2])
        # self.source.setItem(row, self.IndexCritical, item)

    def checkObstacle(self, obstacle_0):
        if len(self.surfacesList) == 0:
            return

        for area in self.surfacesList:
            resultValue = []
            mocMultiplier = self.primaryMoc * obstacle_0.MocMultiplier;
            obstacleAreaResult = area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier, resultValue);
            if len(resultValue) == 2:
                num = resultValue[0]
                num1 = resultValue[1]
            else:
                return
            if isinstance(area, PrimaryObstacleArea):
                self.dr = MathHelper.calcDistance(area.PreviewArea[2].Position, area.PreviewArea[3].Position)
            if (obstacleAreaResult != ObstacleAreaResult.Outside):
                position = obstacle_0.Position;
                if num == None:
                    checkResult = [obstacleAreaResult, num1, num];
                    self.addObstacleToModel(obstacle_0, checkResult)
                    continue
                pdg = 0
                if (self.m_nSectors == 0):

                    moc = num
                    oca = self.dblOCA;
                    altreqM = oca - position.get_Z() - moc
                    pdg = 0
                    # ResultMOC[5] = (float)BaseOperation.ConvertValueFromUnits(ResultMOC[4], cocaUnitType.whatHeight, cocaUnitSystem.sysSi);

                    # ResultMOC[8] = dblDr * 1000;
                    # ResultMOC[9] = (float)BaseOperation.ConvertValueFromUnits(dblDr, cocaUnitType.whatDist, cocaUnitSystem.sysSi);
                    #
                    # ResultMOC[8] *= -1;
                    # ResultMOC[9] *= -1;
                else:
                    moc = num
                    # ResultMOC[1] = (float)BaseOperation.ConvertValueFromUnits(ResultMOC[0], cocaUnitType.whatHeight, cocaUnitSystem.sysSi);

                    oca = self.dblOCA + self.dr * 1000 * self.dblClimbGradient / 100;
                    # ResultMOC[3] = (float)BaseOperation.ConvertValueFromUnits(ResultMOC[2], cocaUnitType.whatHeight, cocaUnitSystem.sysSi);
                    altreqM = oca - position.get_Z() - moc;
                    pdg = (position.get_Z() - self.dblOCA + moc) / self.dr * 100 / 1000;
                    # ResultMOC[5] = (float)BaseOperation.ConvertValueFromUnits(ResultMOC[4], cocaUnitType.whatHeight, cocaUnitSystem.sysSi);
                    # ResultMOC[6] = (altSI - dblOCA + MOC) / dblDr * 100 / 1000;
                    # ResultMOC[7] = ResultMOC[6];
                    # ResultMOC[8] = dblDr * 1000;
                    # ResultMOC[9] = (float)BaseOperation.ConvertValueFromUnits(dblDr, cocaUnitType.whatDist, cocaUnitSystem.sysSi);
                # z = position.get_Z() + obstacle_0.Trees + num;
                # criticalObstacleType = CriticalObstacleType.No;
                # if (z > self.enrouteAltitude):
                #     criticalObstacleType = CriticalObstacleType.Yes;
                checkResult = [obstacleAreaResult, self.dr, moc, altreqM, pdg];
                self.addObstacleToModel(obstacle_0, checkResult)