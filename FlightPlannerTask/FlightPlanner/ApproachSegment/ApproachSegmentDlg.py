# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import SurfaceTypes, ObstacleTableColumnType, ObstacleAreaResult, TurnDirection
from FlightPlanner.ApproachSegment.ui_ApproachSegment import Ui_ApproachSegment
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.helpers import MathHelper, Unit, Distance, AltitudeUnits, Altitude
from FlightPlanner.types import Point3D
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Prompts import Prompts
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, SecondaryObstacleArea, SecondaryObstacleAreaWithManyPoints, SecondaryAreaStraight
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.DataHelper import DataHelper
from map.tools import QgsMapToolSelectUtils
from Type.switch import switch

from PyQt4.QtCore import SIGNAL, QString, QObject, Qt, QRect, QCoreApplication
from PyQt4.QtGui import QColor, QMessageBox, QFileDialog, QLabel, QStandardItem
from qgis.core import QGis, QgsVectorLayer, QgsGeometry, QgsField, QgsFeature, QgsRectangle
from qgis.gui import  QgsMapTool, QgsRubberBand, QgsMapToolPan, QgsMapCanvasSnapper
import define, math

class ApproachSegmentDlg(FlightPlanBaseDlg):
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("ApproachSegmentDlg")
        self.surfaceType = SurfaceTypes.ApproachSegment
        self.selectedRow = None
        self.editingModelIndex = None

        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.ApproachSegment)
        self.resize(600, 650)
        QgisHelper.matchingDialogSize(self, 600, 700)
        self.surfaceList = None
        self.manualPolygon = None
        
        self.DeltaDistance = 0.5
        # IFeature[] m_pSectorFeature;
        self.m_iNAVAID = None;
        self.m_iCategory = None;
        self.m_iWarning = None;
        self.m_wcWarning = None;
        self.m_ipNAVAIDPos = None;
        self.m_ipFAFPos = None;
        self.m_ipMAPtPos = None;
        self.m_ipTHRPos = None;
        self.m_dblFAFAlt = None;
        self.m_dblMAPtAlt = None;
        self.m_dblTHRAlt = None;
        self.m_dblDistance = None;
        self.m_dblGradient = None;

        self.m_nSegmentCount = None;	# 2 for final segment and 1 for others
        self.m_ipPrimary = None;		# array of primary area in count of nSegmentCount
        self.m_ipSecondary = None;	# array of secondary area in count of 2*nSegmentCount
        self.m_ipOriginPrimary = None;
        self.m_ipOriginSeconday = None;

        self.resultObstacleAreaList = []
        self.nominalTrackLayer = None
        self.resultLayerList = []



        self.vorDmeFeatureArray = []
        self.currentLayer = define._canvas.currentLayer()
        self.initBasedOnCmb()
    def initBasedOnCmb(self):
        self.currentLayer = define._canvas.currentLayer()
        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.vorDmeFeatureArray = self.basedOnCmbFill(self.currentLayer, self.parametersPanel.cmbBasedOn, self.parametersPanel.pnlNavAidPos)
    def basedOnCmbFill(self, layer, basedOnCmbObj, vorDmePositionPanelObj):
        basedOnCmbObj.Clear()
        vorDmePositionPanelObj.Point3d = None
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')
        vorDmeList = []
        vorDmeFeatureList = []
        if idx >= 0:
            featIter = layer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idx].toString()
                attrValue = QString(attrValue)
                attrValue = attrValue.replace(" ", "")
                attrValue = attrValue.replace("/", "")
                attrValue = attrValue.toUpper()
                if self.parametersPanel.cmbNavAidType.SelectedIndex == 1:
                    if attrValue == "VOR" or attrValue == "VORDME" or attrValue == "VORTAC" or attrValue == "TACAN":
                        vorDmeList.append(attrValue)
                        vorDmeFeatureList.append(feat)
                else:
                    if attrValue == "NDB" or attrValue == "NDBDME":
                        vorDmeList.append(attrValue)
                        vorDmeFeatureList.append(feat)
            if len(vorDmeList) != 0:

                i = -1
                basedOnCmbObjItems = []
                for feat in vorDmeFeatureList:
                    typeValue = feat.attributes()[idx].toString()
                    nameValue = feat.attributes()[idxName].toString()
                    basedOnCmbObjItems.append(typeValue + " " + nameValue)
                basedOnCmbObjItems.sort()
                basedOnCmbObj.Items = basedOnCmbObjItems
                basedOnCmbObj.SelectedIndex = 0

                # if idxAttributes
                feat = vorDmeFeatureList[0]
                attrValue = feat.attributes()[idxLat].toDouble()
                lat = attrValue[0]

                attrValue = feat.attributes()[idxLong].toDouble()
                long = attrValue[0]

                attrValue = feat.attributes()[idxAltitude].toDouble()
                alt = attrValue[0]

                vorDmePositionPanelObj.Point3d = Point3D(long, lat, alt)
                self.connect(basedOnCmbObj, SIGNAL("Event_0"), self.basedOnCmbObj_Event_0)

        return vorDmeFeatureList
    def basedOnCmbObj_Event_0(self):
        if self.currentLayer == None or not self.currentLayer.isValid():
            return
        if len(self.vorDmeFeatureArray) == 0:
            return
        layer = self.currentLayer
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')

        feat = self.vorDmeFeatureArray[self.parametersPanel.cmbBasedOn.SelectedIndex]
        attrValue = feat.attributes()[idxLat].toDouble()
        lat = attrValue[0]

        attrValue = feat.attributes()[idxLong].toDouble()
        long = attrValue[0]

        attrValue = feat.attributes()[idxAltitude].toDouble()
        alt = attrValue[0]

        self.parametersPanel.pnlNavAidPos.Point3d = Point3D(long, lat, alt)
    def btnPDTCheck_Click(self):
        bOk1 = False
        bOk2 = False
        bOk3 = False;
        lpszTextWarning1 = ""
        lpszTextWarning2 = ""
        lpszTextWarning3 = "";
        lpszTextResult1 = ""
        lpszTextResult2 = ""
        lpszTextResult3 = "";

        lpszTextWarning1, lpszTextWarning2, lpszTextWarning3, lpszTextResult1, lpszTextResult2, lpszTextResult3, bOk1, bOk2, bOk3 = self.MakeWarning(lpszTextWarning1, lpszTextWarning2, lpszTextWarning3, lpszTextResult1, lpszTextResult2, lpszTextResult3, bOk1, bOk2, bOk3);

        strTitle = "";

        for case in switch(self.parametersPanel.txtApproachSegmentType.Value):
            if case(SegmentType.Final):
                strTitle = "Final Approach Segment Procedure Check";
                break;
            elif case(SegmentType.InterStraight) or case(SegmentType.InterWithIf) or case(SegmentType.InterWithNoIf):
                strTitle = "Intermediate Approach Segment Procedure Check";
                break;
            elif case(SegmentType.InitStraight) or case(SegmentType.InitArc):
                strTitle = "Initial Approach Segment Procedure Check";
                break;
            # if case(SegmentType):
            #     strTitle = "Missed Approach Segment Procedure Check";
            #     break;
        # this.Text = strTitle;

        resStr = "";
        resultStr = ""

        resultStr = lpszTextWarning1 + "\n" + lpszTextResult1 + "\n\n";
        resultStr += lpszTextWarning2 + "\n" + lpszTextResult2 + "\n\n";
        resultStr += lpszTextWarning3 + "\n" + lpszTextResult3;
        QMessageBox.warning(self, strTitle, resultStr)


    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")
        if filePathDir == "":
            return
        self.filterList = ["Faf", "Ma"]
        # for surf in self.surfaceList:
        #     self.filterList.append(surf.type)
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, self.surfaceType, self.ui.tblObstacles, self.filterList, parameterList, resultHideColumnNames)

    def getParameterList(self):
        parameterList = []
        parameterList.append(("Approach Segment Type", "group"))
        parameterList.append(("Type", self.parametersPanel.txtApproachSegmentType.Value))

        parameterList.append(("Positions", "group"))

        parameterList.append((self.parametersPanel.gbNavAid.Title, "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlNavAidPos.txtPointX.text()), float(self.parametersPanel.pnlNavAidPos.txtPointY.text()))
        parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
        parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
        parameterList.append(("X", self.parametersPanel.pnlNavAidPos.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlNavAidPos.txtPointY.text()))

        parameterList.append((self.parametersPanel.pnlFafPos.Caption, "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlFafPos.txtPointX.text()), float(self.parametersPanel.pnlFafPos.txtPointY.text()))
        parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
        parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
        parameterList.append(("X", self.parametersPanel.pnlFafPos.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlFafPos.txtPointY.text()))

        parameterList.append((self.parametersPanel.pnlMaptPos.Caption, "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlMaptPos.txtPointX.text()), float(self.parametersPanel.pnlMaptPos.txtPointY.text()))
        parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
        parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
        parameterList.append(("X", self.parametersPanel.pnlMaptPos.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlMaptPos.txtPointY.text()))

        parameterList.append((self.parametersPanel.pnlDerPos.Caption, "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlDerPos.txtPointX.text()), float(self.parametersPanel.pnlDerPos.txtPointY.text()))
        parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
        parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
        parameterList.append(("X", self.parametersPanel.pnlDerPos.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlDerPos.txtPointY.text()))

        parameterList.append(("Parameters", "group"))

        self.ui.tabCtrlGeneral.setCurrentIndex(0)

        if self.parametersPanel.cmbTurnDirection.Visible:
            parameterList.append((self.parametersPanel.cmbTurnDirection.Caption, self.parametersPanel.cmbTurnDirection.SelectedItem))
        if self.parametersPanel.cmbAircraftCatgory.Visible:
            parameterList.append((self.parametersPanel.cmbAircraftCatgory.Caption, self.parametersPanel.cmbAircraftCatgory.SelectedItem))
        if self.parametersPanel.gbJoin.Visible:
            if self.parametersPanel.radioJoinYes.isChecked():
                parameterList.append((self.parametersPanel.gbJoin.Caption, "Yes"))
            else:
                parameterList.append((self.parametersPanel.gbJoin.Caption, "No"))
        if self.parametersPanel.pnlDistance.Visible:
            parameterList.append((self.parametersPanel.pnlDistance.Caption, str(self.parametersPanel.pnlDistance.Value.NauticalMiles) + "nm"))
        if self.parametersPanel.pnlGradient.Visible:
            parameterList.append((self.parametersPanel.pnlGradient.Caption, str(self.parametersPanel.pnlGradient.Value.Percent) + "%"))
        self.ui.tabCtrlGeneral.setCurrentIndex(1)
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
        # self.ui.btnConstruct.setVisible(False)
        # self.ui.btnEvaluate.setVisible(False)
        # self.ui.btnPDTCheck.setVisible(False)
        # self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)

#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)

    def initSurfaceCombo(self):
        self.ui.cmbObstSurface.clear()
        self.ui.cmbObstSurface.addItems(["Faf", "Ma"])
    def btnEvaluate_Click(self):
        self.ui.frm_cmbObstSurface.setVisible(self.parametersPanel.txtApproachSegmentType.Value == SegmentType.Final)
        primaryMoc = None
        for case in switch (self.parametersPanel.txtApproachSegmentType.Value):
            if case(SegmentType.Final):

                primaryMoc = 75#;//(m_unitSys == cocaUnitSystem.sysSi) ? 75:246;
                break;
            if case(SegmentType.InterStraight) or case(SegmentType.InterWithIf) or case(SegmentType.InterWithNoIf):
                primaryMoc = 150#;//(m_unitSys == cocaUnitSystem.sysSi) ? 150:492;
                break;
            if case(SegmentType.InitStraight) or case(SegmentType.InitArc):
                primaryMoc = 300#;//(m_unitSys == cocaUnitSystem.sysSi) ? 300:1000;
                break;
        self.obstaclesModel = ApproachSegmentObstacles(self.resultObstacleAreaList, Altitude(primaryMoc));

        return FlightPlanBaseDlg.btnEvaluate_Click(self)
    def CalculateDistance(self):
        resDistance = None
        dblValue1 = None
        dblValue2 = None
        deltaValue = None;
        ipNAVAIDPos = self.parametersPanel.pnlNavAidPos.Point3d
        ipFAFPos = self.parametersPanel.pnlFafPos.Point3d
        ipMAPtPos = self.parametersPanel.pnlMaptPos.Point3d
        if ( self.parametersPanel.txtApproachSegmentType.Value == SegmentType.InitArc ):
            dblValue1 = MathHelper.calcDistance(ipNAVAIDPos, ipFAFPos);
            dblValue2 = MathHelper.calcDistance(ipNAVAIDPos, ipMAPtPos);
            resDistance = dblValue1;
            deltaValue = math.fabs( dblValue1 - dblValue2 );
            if (  deltaValue > self.DeltaDistance ): return -1;
            dblValue1 = MathHelper.getBearing(ipNAVAIDPos, ipFAFPos);
            if ( dblValue1 < 0 ): dblValue1 += 2 * math.pi;
            dblValue2 = MathHelper.getBearing(ipNAVAIDPos, ipMAPtPos);
            if ( dblValue2 < 0 ): dblValue2 += 2 * math.pi;
            if ( dblValue2 > dblValue1 ): deltaValue = dblValue2 - dblValue1;
            else: deltaValue = 2 * math.pi + dblValue2 - dblValue1;
            if ( self.parametersPanel.cmbTurnDirection.SelectedIndex == TurnDirection.Right):
                resDistance = ( 2 * math.pi - deltaValue ) * resDistance;
            else:
                resDistance = deltaValue * resDistance;
        else:
            resDistance = MathHelper.calcDistance(ipFAFPos, ipMAPtPos)

        # resDistance = Unit.ConvertMeterToNM(resDistance);

        self.parametersPanel.pnlDistance.Value = Distance(resDistance);

        return Unit.ConvertMeterToNM(resDistance);
    def changeDistGradient(self):

        try:
            self.parametersPanel.cmbTurnDirection.Visible = self.parametersPanel.txtApproachSegmentType.Value == SegmentType.InitArc
            self.parametersPanel.gbJoin.Visible = self.parametersPanel.txtApproachSegmentType.Value == SegmentType.InitArc

            self.CalculateDistance()
            self.CalculateGradient()

        except:
            pass
    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        define._messageLabel.setText("")
        # if( !GetUserParameters() ) return;
        self.m_iFinalInitInter = self.parametersPanel.txtApproachSegmentType.Value
        if ( self.parametersPanel.cmbAircraftCatgory.SelectedIndex != -1 ):
            m_iWarning = 0;
            if ( not self.CheckDistance_Gradient_Bearing() ): return;
        if (self.m_iFinalInitInter == SegmentType.InitArc and self.CalculateDistance() < 0):
            QMessageBox.warning(self, "Warning", "The points (IAF, IF) are not on same ARC distance from DME.");
            return;


        resultPointArrayList = []
        self.resultObstacleAreaList = []
        ipFeatureClassNominalTrack = PolylineArea()
        for case in switch (self.m_iFinalInitInter):
            if case(SegmentType.Final):
                self.DrawApproachSegmentFinal(resultPointArrayList, ipFeatureClassNominalTrack);
                break;
            if case(SegmentType.InterStraight):
                self.DrawApproachSegmentInterStraight(resultPointArrayList, ipFeatureClassNominalTrack);
                break;
            if case(SegmentType.InterWithIf):
                self.DrawApproachSegmentInterWithIF(resultPointArrayList, ipFeatureClassNominalTrack);
                break;
            if case(SegmentType.InterWithNoIf):
                selectLineMapTool = SelectLine(define._canvas, "Select primary area of initial segment to be able to draw limitation.", self)
                define._canvas.setMapTool(selectLineMapTool)
                QObject.connect(selectLineMapTool, SIGNAL("outputResult"), self.selectLineResult)
                define._messageLabel.setText("Select primary area of initial segment to be able to draw limitation.")
                return

                # IGeometry ipGeo;
                # ipGeo = m_SelectFeature.Shape;
                # IPolyline ipPolyLine = (IPolyline)ipGeo;
                # DrawApproachSegmentInterWithNoIF(ref ipFeatureClass, ref ipFeatureClassOther, ipPolyLine, m_iLayer);
                break;
            if case(SegmentType.InitStraight):
                self.DrawApproachSegmentInitial(resultPointArrayList, ipFeatureClassNominalTrack);
                break;
            if case(SegmentType.InitArc):
                # m_iNAVAID = 2;
                bJoin = self.parametersPanel.radioJoinYes.isChecked() == True;
                bColckwise = TurnDirection.Right if(self.parametersPanel.cmbTurnDirection.SelectedIndex == 1) else TurnDirection.Left
                resultPolylineAreaList = []
                self.DrawApproachSegmentInitialBasedDME(resultPolylineAreaList, ipFeatureClassNominalTrack, bJoin, bColckwise);
                break;
        # if self.m_iFinalInitInter != SegmentType.InitArc:
        self.nominalTrackLayer = AcadHelper.createNominalTrackLayer(ipFeatureClassNominalTrack.method_14(), None, "memory", "NominalTrack_" + self.surfaceType.replace(" ", "_").replace("-", "_"))
        constructLayer = None
        constructLayerMa = None
        if self.m_iFinalInitInter != SegmentType.Final:
            constructLayer = AcadHelper.createVectorLayer(SurfaceTypes.ApproachSegment)
        else:
            constructLayer = AcadHelper.createVectorLayer(SurfaceTypes.ApproachSegment + "_Faf")
            constructLayerMa = AcadHelper.createVectorLayer(SurfaceTypes.ApproachSegment + "_Ma")
        if self.m_iFinalInitInter == SegmentType.InitArc:
            for area, areaName in resultPolylineAreaList:
                AcadHelper.setGeometryAndAttributesInLayer(constructLayer, area)
            # QgisHelper.appendToCanvas(define._canvas, [constructLayer], SurfaceTypes.ApproachSegment)
        else:
            for pointArray, areaName in resultPointArrayList:
                # ptArray = []
                # for pt in pointArray:
                #     ptArray.append(pt)
                # ptArray.append(pointArray[0])
                if self.m_iFinalInitInter != SegmentType.Final:
                    AcadHelper.setGeometryAndAttributesInLayer(constructLayer, PolylineArea(pointArray).method_14_closed())
                else:
                    if areaName == "Faf":
                        AcadHelper.setGeometryAndAttributesInLayer(constructLayer, PolylineArea(pointArray).method_14_closed())
                    else:
                        AcadHelper.setGeometryAndAttributesInLayer(constructLayerMa, PolylineArea(pointArray).method_14_closed())

        if self.m_iFinalInitInter != SegmentType.Final:
            self.resultLayerList = [constructLayer, self.nominalTrackLayer]
            QgisHelper.appendToCanvas(define._canvas, [constructLayer, self.nominalTrackLayer], SurfaceTypes.ApproachSegment)
            QgisHelper.zoomToLayers([constructLayer, self.nominalTrackLayer])
        else:
            self.resultLayerList = [constructLayer, constructLayerMa, self.nominalTrackLayer]
            QgisHelper.appendToCanvas(define._canvas, [constructLayer, constructLayerMa, self.nominalTrackLayer], SurfaceTypes.ApproachSegment)
            QgisHelper.zoomToLayers([constructLayer, constructLayerMa, self.nominalTrackLayer])
        self.ui.btnEvaluate.setEnabled(True)
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
        # buttonInterferenceCheck.Enabled = true;
        # savetechnicalReportToolStripMenuItem.Enabled = true;
    def selectLineResult(self, selectedFeatures):
        if len(selectedFeatures) == 0:
            return

        feat = selectedFeatures[0]
        resultPointArrayList = []
        ipFeatureClassNominalTrack = PolylineArea()
        self.DrawApproachSegmentInterWithNoIF(resultPointArrayList, ipFeatureClassNominalTrack, feat.geometry())
        if len(resultPointArrayList) == 0:
            return
        if len(self.resultLayerList) != 0:
            QgisHelper.removeFromCanvas(define._canvas, self.resultLayerList)

        # nominalTrackLayer = AcadHelper.createNominalTrackLayer(ipFeatureClassNominalTrack.method_14())
        constructLayer = AcadHelper.createVectorLayer(SurfaceTypes.ApproachSegment)
        for pointArray in resultPointArrayList:
            AcadHelper.setGeometryAndAttributesInLayer(constructLayer, PolylineArea(pointArray).method_14_closed())
        self.resultLayerList = [constructLayer]
        QgisHelper.appendToCanvas(define._canvas, [constructLayer], SurfaceTypes.ApproachSegment)
        QgisHelper.zoomToLayers([constructLayer])
        self.ui.btnEvaluate.setEnabled(True)


    def initParametersPan(self):
        ui = Ui_ApproachSegment()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.SegmentType = ["Final Segment", "Intermediate Segment Straight", "Intermediate Segment With IF",
                       "Intermediate Segment With No IF", "Initial Segment Straight", "Initial Segment DME ARCS"]

        # self.parametersPanel.pnlMode.Items = ["Setup", "Input1", "Input2","Input3"]
        # self.parametersPanel.pnlUsedFor.Items = ["Departure", "Approach","ILS"]
        # self.parametersPanel.cmbBaseOrientation.Items = ["LR", "RL"]
        #
        # self.parametersPanel.chbWriteName.clicked.connect(self.chbWriteName_clicked)
        # self.parametersPanel.chbPolyline.clicked.connect(self.method_31)
        # #

        self.connect(self.parametersPanel.pnlFafPos, SIGNAL("positionChanged"), self.changeDistGradient)
        self.connect(self.parametersPanel.pnlMaptPos, SIGNAL("positionChanged"), self.changeDistGradient)
        self.connect(self.parametersPanel.pnlDerPos, SIGNAL("positionChanged"), self.changeDistGradient)
        self.connect(self.parametersPanel.cmbTurnDirection, SIGNAL("Event_0"), self.changeDistGradient)
        self.connect(self.parametersPanel.txtApproachSegmentType, SIGNAL("Event_0"), self.changeDistGradient)
        self.connect(self.parametersPanel.cmbNavAidType, SIGNAL("Event_0"), self.initBasedOnCmb)


        self.changeDistGradient()
        # self.chbWriteName_clicked(self.parametersPanel.chbWriteName.isChecked())
        # self.ui.btnEvaluate.setEnabled(True)
        # self.parametersPanel.pnlBasePoint.Point3d = Point3D(677803.9246, 6617150.6787)
        # self.parametersPanel.pnlThrDer.Point3d = Point3D(664684.9484, 6617888.008)
        # self.parametersPanel.pnlEtp.Point3d = Point3D(666182.2544, 6625897.6157)
        # self.parametersPanel.pnlOutbound.Value = 10.58
    def DrawApproachSegmentInitialBasedDME(self, resultPolylineAreaList, nominalTrackPolylineArea, bJoin, bClockwise):
        ipPoint = [None, None, None, None, None, None];
        ipLine = [None, None, None, None, None, None];
        ipSeg = [None, None, None, None, None, None];
        ipCircArc = [None, None, None, None, None, None];
        # ISegmentCollection ipSegCollPrimary = new PolylineClass(), ipSegCollSecondary1 = new PolylineClass(), ipSegCollSecondary2 = new PolylineClass();
        # m_nSegmentCount = 1;
        # m_ipPrimary = new IPolyline[1];
        # m_ipSecondary = new IPolyline[2];
        #
        # for ( int i = 0 ; i < 6 ; i++ ){
        #     ipPoint[i] = new PointClass();
        #     ipCircArc[i] = new CircularArcClass();
        #     ipLine[i] = new LineClass();
        # }
        #
        # double dblWidth,dblAngleIF, dblAngleIAF;
        m_ipNAVAIDPos = self.parametersPanel.pnlNavAidPos.Point3d
        m_ipMAPtPos = self.parametersPanel.pnlMaptPos.Point3d
        m_ipFAFPos = self.parametersPanel.pnlFafPos.Point3d
        m_ipTHRPos = self.parametersPanel.pnlDerPos.Point3d

        dblAngleIF = MathHelper.getBearing( m_ipNAVAIDPos, m_ipMAPtPos);
        dblAngleIAF = MathHelper.getBearing( m_ipNAVAIDPos, m_ipFAFPos);
        dblWidth = Unit.ConvertNMToMeter(2.5);

        if MathHelper.calcDistance(m_ipNAVAIDPos, m_ipFAFPos) != MathHelper.calcDistance(m_ipNAVAIDPos, m_ipMAPtPos):
            m_ipMAPtPos = MathHelper.distanceBearingPoint(m_ipNAVAIDPos, MathHelper.getBearing(m_ipNAVAIDPos, m_ipMAPtPos), MathHelper.calcDistance(m_ipNAVAIDPos, m_ipFAFPos))


        # esriArcOrientation AOrientation, BOrientation;
        if ( bClockwise == TurnDirection.Right ):
            AOrientation = TurnDirection.Left
            BOrientation = TurnDirection.Right
        else:
            AOrientation = TurnDirection.Right
            BOrientation = TurnDirection.Left
        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation(m_ipNAVAIDPos, m_ipMAPtPos, m_ipFAFPos, AOrientation )
        nominalTrackPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
        nominalTrackPolylineArea.Add(PolylineAreaPoint(toPoint))
        # ISegmentCollection ipNominalTrack =new PolylineClass();
        # ipCircArc[0].PutCoords( m_ipNAVAIDPos, m_ipMAPtPos, m_ipFAFPos, AOrientation );
        # ISegment ipTrack = (ISegment)ipCircArc[0];
        # ipNominalTrack.AddSegment(ipTrack);
        # IGeometry ipGeom = (IGeometry)ipNominalTrack;
        # ipGeom.SpatialReference = m_SpatialReference;
        # IPolyline ipPolyline = (IPolyline)ipGeom;
        #
        # BaseOperation.Create_PolylineFeature((IGeometry)ipPolyline, ref iFeatureClassother, featureField);
        #
        # bool bStore;

        if ( bJoin ):
            # double dblJoinWidth, dblAngleFAFIF;
            dblAngleFAFIF = 0.0
            dblJoinWidth = Unit.ConvertNMToMeter(10);#GetSegmentWidth( pApproachSegmentData->ipNAVAIDPos, pApproachSegmentData->ipMAPtPos, pApproachSegmentData->iNAVAID, pApproachSegmentData->mapUnit );
            dblAngleFAFIF = MathHelper.getBearing( m_ipTHRPos, m_ipMAPtPos) - math.pi / 2;

            if (bClockwise == TurnDirection.Right and not (dblAngleFAFIF >= dblAngleIF and dblAngleFAFIF <= dblAngleIF + math.pi )):
                # //MessageBox.Show("Area does not exist.");
                # //return;
                dblAngleFAFIF -= math.pi;
            if (bClockwise == TurnDirection.Left and dblAngleFAFIF >= dblAngleIF and dblAngleFAFIF <= dblAngleIF + math.pi):
                # //MessageBox.Show("Area does not exist.");
                # //return;
                dblAngleFAFIF -= math.pi;
            # //for primary
            ipPoint[0] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleIF + math.pi, dblWidth);
            ipPoint[1] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleIF, 0);
            ipPoint[2] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleFAFIF, dblJoinWidth / 4);
            ipPoint[3] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleIF, dblWidth);
            ipPoint[4] = MathHelper.distanceBearingPoint(m_ipFAFPos, dblAngleIAF, dblWidth);
            ipPoint[5] = MathHelper.distanceBearingPoint(m_ipFAFPos, dblAngleIAF + math.pi, dblWidth);

            resultPolylineArea = PolylineArea()
            for i in range(6):

                k = ( i + 1 ) % 6;
                if ( i == 2 or i == 3 or i == 5 ): #// arc
                    if ( i == 5 ):
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation(m_ipNAVAIDPos, ipPoint[i], ipPoint[k], BOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))

                        # ipCircArc[i].PutCoords( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], BOrientation );
                    elif ( i == 2):
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation(m_ipMAPtPos, ipPoint[i], ipPoint[k], AOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))
                        # ipCircArc[i].PutCoords( m_ipMAPtPos, ipPoint[i], ipPoint[k], AOrientation );
                    else:
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation(m_ipNAVAIDPos, ipPoint[i], ipPoint[k], AOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))
                        # ipCircArc[i].PutCoords( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], AOrientation );
                #     ipSeg[i] = (ISegment)ipCircArc[i];
                #     ipSegCollPrimary.AddSegment(ipSeg[i]);
                # }
                else:# // line
                    resultPolylineArea.Add(PolylineAreaPoint(ipPoint[i]))
                    resultPolylineArea.Add(PolylineAreaPoint(ipPoint[k]))
            resultPolylineAreaList.append([resultPolylineArea, "Primary"])

            #         ipLine[i].PutCoords( ipPoint[i], ipPoint[k] );
            #         ipSeg[i] = (ISegment)ipLine[i];
            #         ipSegCollPrimary.AddSegment(ipSeg[i]);
            #     }
            # }
            # bStore = !(iDrawStyle == 1);
            self.resultObstacleAreaList.append([PrimaryObstacleArea(resultPolylineArea), "Faf"])
            # m_ipPrimary[0] = MakePolyLineFromSegmentCollection(ipSegCollPrimary,  bStore, ref iFeatureClass, m_SpatialReference, featureField );

            # //for secondaries
            ipPoint[0] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleFAFIF, dblJoinWidth / 4);
            ipPoint[1] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleFAFIF, dblJoinWidth / 2);
            ipPoint[2] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleIF, dblWidth * 2);
            ipPoint[3] = MathHelper.distanceBearingPoint(m_ipFAFPos, dblAngleIAF, dblWidth * 2);
            ipPoint[4] = MathHelper.distanceBearingPoint(m_ipFAFPos, dblAngleIAF, dblWidth);
            ipPoint[5] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleIF, dblWidth);

            secondaryArcPoints = []
            resultPolylineArea = PolylineArea()
            for i in range(6):

                k = ( i + 1 ) % 6;
                if ( i != 0 and i != 3 ): #// arc
                    fromPoint = None
                    toPoint = None
                    middlePoint = None
                    if ( i == 1 ):
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation(m_ipMAPtPos, ipPoint[i], ipPoint[k], AOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))

                        radius = MathHelper.calcDistance(m_ipMAPtPos, toPoint)
                        bearing = MathHelper.getBearing(m_ipMAPtPos, fromPoint)
                        centerAngle = MathHelper.smethod_50(AOrientation, fromPoint, toPoint, m_ipMAPtPos)
                        middleBearing = None
                        if AOrientation == TurnDirection.Left:
                            middleBearing = MathHelper.smethod_4(bearing - centerAngle / 2)
                        else:
                            middleBearing = MathHelper.smethod_4(bearing + centerAngle / 2)
                        middlePoint = MathHelper.distanceBearingPoint(m_ipMAPtPos, middleBearing, radius)
                        secondaryArcPoints.append([fromPoint, middlePoint, toPoint])
                        # ipCircArc[i].PutCoords( m_ipMAPtPos, ipPoint[i], ipPoint[k], AOrientation );
                    elif ( i == 2 ):
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation(m_ipNAVAIDPos, ipPoint[i], ipPoint[k], AOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))

                        radius = MathHelper.calcDistance(m_ipNAVAIDPos, toPoint)
                        bearing = MathHelper.getBearing(m_ipNAVAIDPos, fromPoint)
                        centerAngle = MathHelper.smethod_50(AOrientation, fromPoint, toPoint, m_ipNAVAIDPos)
                        middleBearing = None
                        if AOrientation == TurnDirection.Left:
                            middleBearing = MathHelper.smethod_4(bearing - centerAngle / 2)
                        else:
                            middleBearing = MathHelper.smethod_4(bearing + centerAngle / 2)
                        middlePoint = MathHelper.distanceBearingPoint(m_ipNAVAIDPos, middleBearing, radius)
                        secondaryArcPoints.append([fromPoint, middlePoint, toPoint])
                        # ipCircArc[i].PutCoords( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], AOrientation );
                    elif ( i == 4):
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation(m_ipNAVAIDPos, ipPoint[i], ipPoint[k], BOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))

                        radius = MathHelper.calcDistance(m_ipNAVAIDPos, toPoint)
                        bearing = MathHelper.getBearing(m_ipNAVAIDPos, fromPoint)
                        centerAngle = MathHelper.smethod_50(BOrientation, fromPoint, toPoint, m_ipNAVAIDPos)
                        middleBearing = None
                        if BOrientation == TurnDirection.Left:
                            middleBearing = MathHelper.smethod_4(bearing - centerAngle / 2)
                        else:
                            middleBearing = MathHelper.smethod_4(bearing + centerAngle / 2)
                        middlePoint = MathHelper.distanceBearingPoint(m_ipNAVAIDPos, middleBearing, radius)
                        secondaryArcPoints.append([fromPoint, middlePoint, toPoint])
                        # ipCircArc[i].PutCoords( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], BOrientation );
                    else:
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation(m_ipMAPtPos, ipPoint[i], ipPoint[k], BOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))

                        radius = MathHelper.calcDistance(m_ipMAPtPos, toPoint)
                        bearing = MathHelper.getBearing(m_ipMAPtPos, fromPoint)
                        centerAngle = MathHelper.smethod_50(BOrientation, fromPoint, toPoint, m_ipMAPtPos)
                        middleBearing = None
                        if BOrientation == TurnDirection.Left:
                            middleBearing = MathHelper.smethod_4(bearing - centerAngle / 2)
                        else:
                            middleBearing = MathHelper.smethod_4(bearing + centerAngle / 2)
                        middlePoint = MathHelper.distanceBearingPoint(m_ipMAPtPos, middleBearing, radius)
                        secondaryArcPoints.append([fromPoint, middlePoint, toPoint])
                        # ipCircArc[i].PutCoords( m_ipMAPtPos, ipPoint[i], ipPoint[k], BOrientation );
                    # ipSeg[i] = (ISegment)ipCircArc[i];
                    # ipSegCollSecondary1.AddSegment(ipSeg[i]);
                else:# // line
                    resultPolylineArea.Add(PolylineAreaPoint(ipPoint[i]))
                    resultPolylineArea.Add(PolylineAreaPoint(ipPoint[k]))
            resultPolylineAreaList.append([resultPolylineArea, "Secomdary0"])
            self.resultObstacleAreaList.append([SecondaryObstacleArea(secondaryArcPoints[2][0], secondaryArcPoints[2][1], secondaryArcPoints[2][2],
                                                                     secondaryArcPoints[1][2], None, secondaryArcPoints[1][1], secondaryArcPoints[1][0]), "Faf"])

            self.resultObstacleAreaList.append([SecondaryObstacleArea(secondaryArcPoints[3][0], secondaryArcPoints[3][1], secondaryArcPoints[3][2],
                                                                     secondaryArcPoints[0][2], None, secondaryArcPoints[0][1], secondaryArcPoints[0][0]), "Faf"])
                    # ipLine[i].PutCoords( ipPoint[i], ipPoint[k] );
                    # ipSeg[i] = (ISegment)ipLine[i];
                    # ipSegCollSecondary1.AddSegment(ipSeg[i]);
            # bStore = !(iDrawStyle == 0);
            # m_ipSecondary[0] = MakePolyLineFromSegmentCollection(ipSegCollSecondary1, bStore, ref iFeatureClass, m_SpatialReference, featureField);

            ipPoint[0] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleIF + math.pi, dblWidth * 2);
            ipPoint[1] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleIF + math.pi, dblWidth);
            ipPoint[2] = MathHelper.distanceBearingPoint(m_ipFAFPos, dblAngleIAF + math.pi, dblWidth);
            ipPoint[3] = MathHelper.distanceBearingPoint(m_ipFAFPos, dblAngleIAF + math.pi, dblWidth * 2);
            resultPolylineArea = PolylineArea()
            secondaryArcPoints = []
            for i in range(4):

                k = ( i + 1 ) % 4;
                if ( i == 1 or i == 3 ):# // arc
                    if ( i == 1 ):
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation(m_ipNAVAIDPos, ipPoint[i], ipPoint[k], AOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))

                        radius = MathHelper.calcDistance(m_ipNAVAIDPos, toPoint)
                        bearing = MathHelper.getBearing(m_ipNAVAIDPos, fromPoint)
                        centerAngle = MathHelper.smethod_50(AOrientation, fromPoint, toPoint, m_ipNAVAIDPos)
                        middleBearing = None
                        if AOrientation == TurnDirection.Left:
                            middleBearing = MathHelper.smethod_4(bearing - centerAngle / 2)
                        else:
                            middleBearing = MathHelper.smethod_4(bearing + centerAngle / 2)
                        middlePoint = MathHelper.distanceBearingPoint(m_ipNAVAIDPos, middleBearing, radius)
                        secondaryArcPoints.append([fromPoint, middlePoint, toPoint])
                        # ipCircArc[i].PutCoords( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], AOrientation );
                    else:
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation(m_ipNAVAIDPos, ipPoint[i], ipPoint[k], BOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))

                        radius = MathHelper.calcDistance(m_ipNAVAIDPos, toPoint)
                        bearing = MathHelper.getBearing(m_ipNAVAIDPos, fromPoint)
                        centerAngle = MathHelper.smethod_50(BOrientation, fromPoint, toPoint, m_ipNAVAIDPos)
                        middleBearing = None
                        if BOrientation == TurnDirection.Left:
                            middleBearing = MathHelper.smethod_4(bearing - centerAngle / 2)
                        else:
                            middleBearing = MathHelper.smethod_4(bearing + centerAngle / 2)
                        middlePoint = MathHelper.distanceBearingPoint(m_ipNAVAIDPos, middleBearing, radius)
                        secondaryArcPoints.append([fromPoint, middlePoint, toPoint])

                    #     ipCircArc[i].PutCoords( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], BOrientation );
                    # ipSeg[i] = (ISegment)ipCircArc[i];
                    # ipSegCollSecondary2.AddSegment(ipSeg[i]);
                else:# // line
                    resultPolylineArea.Add(PolylineAreaPoint(ipPoint[i]))
                    resultPolylineArea.Add(PolylineAreaPoint(ipPoint[k]))
            resultPolylineAreaList.append([resultPolylineArea, "Secondary1"])
            self.resultObstacleAreaList.append([SecondaryObstacleArea(secondaryArcPoints[0][0], secondaryArcPoints[0][1], secondaryArcPoints[0][2],
                                                                     secondaryArcPoints[1][2], None, secondaryArcPoints[1][1], secondaryArcPoints[1][0]), "Faf"])

                    # ipLine[i].PutCoords( ipPoint[i], ipPoint[k] );
                    # ipSeg[i] = (ISegment)ipLine[i];
                    # ipSegCollSecondary2.AddSegment(ipSeg[i]);
            # m_ipSecondary[1] = MakePolyLineFromSegmentCollection(ipSegCollSecondary2, bStore, ref iFeatureClass, m_SpatialReference, featureField);

        else:
            # //for primary
            ipPoint[0] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleIF + math.pi, dblWidth);
            ipPoint[1] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleIF, dblWidth);
            ipPoint[2] = MathHelper.distanceBearingPoint(m_ipFAFPos, dblAngleIAF, dblWidth);
            ipPoint[3] = MathHelper.distanceBearingPoint(m_ipFAFPos, dblAngleIAF + math.pi, dblWidth);

            resultPolylineArea = PolylineArea()
            for i in range(4):

                k = ( i + 1 ) % 4;
                if ( i == 1 or i == 3 ):# // arc
                    if ( i == 1 ):
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], AOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))
                        # ipCircArc[i].PutCoords( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], AOrientation );
                    else:
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], BOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))
                    #     ipCircArc[i].PutCoords( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], BOrientation );
                    # ipSeg[i] = (ISegment)ipCircArc[i];
                    # ipSegCollPrimary.AddSegment(ipSeg[i]);
                else:# // line
                    resultPolylineArea.Add(PolylineAreaPoint(ipPoint[i]))
                    resultPolylineArea.Add(PolylineAreaPoint(ipPoint[k]))
            resultPolylineAreaList.append([resultPolylineArea, "Primary"])
            self.resultObstacleAreaList.append([PrimaryObstacleArea(resultPolylineArea), "Faf"])
                    # ipLine[i].PutCoords( ipPoint[i], ipPoint[k] );
                    # ipSeg[i] = (ISegment)ipLine[i];
                    # ipSegCollPrimary.AddSegment(ipSeg[i]);
            # bStore = !(iDrawStyle == 1);
            # m_ipPrimary[0] = MakePolyLineFromSegmentCollection(ipSegCollPrimary, bStore, ref iFeatureClass, m_SpatialReference, featureField);

            # //for Secondaries
            ipPoint[0] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleIF, dblWidth);
            ipPoint[1] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleIF, dblWidth * 2);
            ipPoint[2] = MathHelper.distanceBearingPoint(m_ipFAFPos, dblAngleIAF, dblWidth * 2);
            ipPoint[3] = MathHelper.distanceBearingPoint(m_ipFAFPos, dblAngleIAF, dblWidth);
            secondaryArcPoints = []
            for i in range(4):
                resultPolylineArea = PolylineArea()
                k = ( i + 1 ) % 4;
                if ( i == 1 or i == 3 ):# // arc
                    if ( i == 1 ):
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], AOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))

                        radius = MathHelper.calcDistance(m_ipNAVAIDPos, toPoint)
                        bearing = MathHelper.getBearing(m_ipNAVAIDPos, fromPoint)
                        centerAngle = MathHelper.smethod_50(AOrientation, fromPoint, toPoint, m_ipNAVAIDPos)
                        middleBearing = None
                        if AOrientation == TurnDirection.Left:
                            middleBearing = MathHelper.smethod_4(bearing - centerAngle / 2)
                        else:
                            middleBearing = MathHelper.smethod_4(bearing + centerAngle / 2)
                        middlePoint = MathHelper.distanceBearingPoint(m_ipNAVAIDPos, middleBearing, radius)
                        secondaryArcPoints.append([fromPoint, middlePoint, toPoint])
                        # ipCircArc[i].PutCoords( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], AOrientation );
                    else:
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], BOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))

                        radius = MathHelper.calcDistance(m_ipNAVAIDPos, toPoint)
                        bearing = MathHelper.getBearing(m_ipNAVAIDPos, fromPoint)
                        centerAngle = MathHelper.smethod_50(BOrientation, fromPoint, toPoint, m_ipNAVAIDPos)
                        middleBearing = None
                        if BOrientation == TurnDirection.Left:
                            middleBearing = MathHelper.smethod_4(bearing - centerAngle / 2)
                        else:
                            middleBearing = MathHelper.smethod_4(bearing + centerAngle / 2)
                        middlePoint = MathHelper.distanceBearingPoint(m_ipNAVAIDPos, middleBearing, radius)
                        secondaryArcPoints.append([fromPoint, middlePoint, toPoint])
                    #     ipCircArc[i].PutCoords( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], BOrientation );
                    # ipSeg[i] = (ISegment)ipCircArc[i];
                    # ipSegCollSecondary1.AddSegment(ipSeg[i]);

                else:# // line
                    resultPolylineArea.Add(PolylineAreaPoint(ipPoint[i]))
                    resultPolylineArea.Add(PolylineAreaPoint(ipPoint[k]))
                resultPolylineAreaList.append([resultPolylineArea, "Secondary0"])
                self.resultObstacleAreaList.append([SecondaryObstacleArea(secondaryArcPoints[0][0], secondaryArcPoints[0][1], secondaryArcPoints[0][2],
                                                                     secondaryArcPoints[1][2], None, secondaryArcPoints[1][1], secondaryArcPoints[1][0]), "Faf"])

            #         ipLine[i].PutCoords( ipPoint[i], ipPoint[k] );
            #         ipSeg[i] = (ISegment)ipLine[i];
            #         ipSegCollSecondary1.AddSegment(ipSeg[i]);
            # bStore = !(iDrawStyle == 0);
            # m_ipSecondary[0] = MakePolyLineFromSegmentCollection(ipSegCollSecondary1, bStore, ref iFeatureClass, m_SpatialReference, featureField);
            ipPoint[0] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleIF + math.pi, dblWidth * 2);
            ipPoint[1] = MathHelper.distanceBearingPoint(m_ipMAPtPos, dblAngleIF + math.pi, dblWidth);
            ipPoint[2] = MathHelper.distanceBearingPoint(m_ipFAFPos, dblAngleIAF + math.pi, dblWidth);
            ipPoint[3] = MathHelper.distanceBearingPoint(m_ipFAFPos, dblAngleIAF + math.pi, dblWidth * 2);
            secondaryArcPoints = []
            for i in range(4):
                resultPolylineArea = PolylineArea()
                k = ( i + 1 ) % 4;
                if ( i == 1 or i == 3 ):# // arc
                    if ( i == 1 ):
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], AOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))

                        radius = MathHelper.calcDistance(m_ipNAVAIDPos, toPoint)
                        bearing = MathHelper.getBearing(m_ipNAVAIDPos, fromPoint)
                        centerAngle = MathHelper.smethod_50(AOrientation, fromPoint, toPoint, m_ipNAVAIDPos)
                        middleBearing = None
                        if AOrientation == TurnDirection.Left:
                            middleBearing = MathHelper.smethod_4(bearing - centerAngle / 2)
                        else:
                            middleBearing = MathHelper.smethod_4(bearing + centerAngle / 2)
                        middlePoint = MathHelper.distanceBearingPoint(m_ipNAVAIDPos, middleBearing, radius)
                        secondaryArcPoints.append([fromPoint, middlePoint, toPoint])
                        # ipCircArc[i].PutCoords( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], AOrientation );
                    else:
                        fromPoint, toPoint, bulge = MathHelper.constructArcWithThreePointAndOrientation( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], BOrientation)
                        resultPolylineArea.Add(PolylineAreaPoint(fromPoint, bulge))
                        resultPolylineArea.Add(PolylineAreaPoint(toPoint))

                        radius = MathHelper.calcDistance(m_ipNAVAIDPos, toPoint)
                        bearing = MathHelper.getBearing(m_ipNAVAIDPos, fromPoint)
                        centerAngle = MathHelper.smethod_50(BOrientation, fromPoint, toPoint, m_ipNAVAIDPos)
                        middleBearing = None
                        if BOrientation == TurnDirection.Left:
                            middleBearing = MathHelper.smethod_4(bearing - centerAngle / 2)
                        else:
                            middleBearing = MathHelper.smethod_4(bearing + centerAngle / 2)
                        middlePoint = MathHelper.distanceBearingPoint(m_ipNAVAIDPos, middleBearing, radius)
                        secondaryArcPoints.append([fromPoint, middlePoint, toPoint])
                        # ipCircArc[i].PutCoords( m_ipNAVAIDPos, ipPoint[i], ipPoint[k], BOrientation );
                    # ipSeg[i] = (ISegment)ipCircArc[i];
                    # ipSegCollSecondary2.AddSegment(ipSeg[i]);
                else:# // line
                    resultPolylineArea.Add(PolylineAreaPoint(ipPoint[i]))
                    resultPolylineArea.Add(PolylineAreaPoint(ipPoint[k]))
                resultPolylineAreaList.append([resultPolylineArea, "Secondary1"])
                self.resultObstacleAreaList.append([SecondaryObstacleArea(secondaryArcPoints[0][0], secondaryArcPoints[0][1], secondaryArcPoints[0][2],
                                                                     secondaryArcPoints[1][2], None, secondaryArcPoints[1][1], secondaryArcPoints[1][0]), "Faf"])

            #         ipLine[i].PutCoords( ipPoint[i], ipPoint[k] );
            #         ipSeg[i] = (ISegment)ipLine[i];
            #         ipSegCollSecondary2.AddSegment(ipSeg[i]);
            # m_ipSecondary[1] = MakePolyLineFromSegmentCollection(ipSegCollSecondary2, bStore, ref iFeatureClass, m_SpatialReference, featureField);

    def DrawApproachSegmentFinal(self, resultPointArrayList, nominalTrackPolylineArea):
        TotalWith = [2.5 , 2.0]
        LimitDistance = [13.8, 21.9]
        DefaultWidth = 10.0;

        dblStWidth = None;
        dblDis = None;
        #////////////////////////////////////////////////////////////////////////
        # get nominal track by kay

        # IPolyline ipPolyLineNominal = new PolylineClass();
        # IPointCollection ipPColNominal = (IPointCollection)ipPolyLineNominal;
        nominalTrackPolylineArea.Add(PolylineAreaPoint(self.parametersPanel.pnlFafPos.Point3d));
        nominalTrackPolylineArea.Add(PolylineAreaPoint(self.parametersPanel.pnlNavAidPos.Point3d));
        nominalTrackPolylineArea.Add(PolylineAreaPoint(self.parametersPanel.pnlMaptPos.Point3d));
        # ipPolyLineNominal.SpatialReference = m_SpatialReference;
        # BaseOperation.Create_PolylineFeature((IGeometry)ipPolyLineNominal, ref iFeatureClassother, featureField);

        #////////////////////////////////////////////////////////////////////////

        for i in range(2):
            TotalWith[i] = Unit.ConvertNMToMeter(TotalWith[i]);
            LimitDistance[i] = Unit.ConvertNMToMeter(LimitDistance[i]);
        DefaultWidth = Unit.ConvertNMToMeter(DefaultWidth);
        dblStWidth = 2 * TotalWith[self.parametersPanel.cmbNavAidType.SelectedIndex];
        dblDis = LimitDistance[self.parametersPanel.cmbNavAidType.SelectedIndex];

        m_nSegmentCount = 2;
        # m_ipPrimary = new IPolyline[2];
        # m_ipSecondary = new IPolyline[4];
        #
        ipSp = self.parametersPanel.pnlNavAidPos.Point3d;
        ipEp = self.parametersPanel.pnlFafPos.Point3d;
        dblFAFWidth = self.GetSegmentWidth(ipSp, ipEp, self.parametersPanel.cmbNavAidType.SelectedIndex);
        self.resultObstacleAreaList = []
        if ( dblFAFWidth < DefaultWidth ):
            self.DrawProtectionCase1(ipSp,dblStWidth,ipEp,dblFAFWidth, resultPointArrayList);
        else:
            self.DrawProtectionCase2(ipSp,dblStWidth,ipEp,dblFAFWidth,dblDis, resultPointArrayList);

        ipEp = self.parametersPanel.pnlMaptPos.Point3d;
        dblMAPtWidth = self.GetSegmentWidth(ipSp,ipEp,self.parametersPanel.cmbNavAidType.SelectedIndex);
        if ( dblMAPtWidth < DefaultWidth ):
            self.DrawProtectionCase1(ipSp,dblStWidth,ipEp,dblMAPtWidth, resultPointArrayList, "Ma");
        else:
            self.DrawProtectionCase2(ipSp,dblStWidth,ipEp,dblMAPtWidth,dblDis,resultPointArrayList, "Ma");
    def DrawApproachSegmentInterStraight(self, resultPointArrayList, nominalTrackPolylineArea):
        ipSp = self.parametersPanel.pnlNavAidPos.Point3d;
        ipEp = self.parametersPanel.pnlMaptPos.Point3d;

        # //////////////////////////////////////////////////////////////////////////
        # // draw nominal track

        nominalTrackPolylineArea.Add(PolylineAreaPoint(self.parametersPanel.pnlFafPos.Point3d));
        nominalTrackPolylineArea.Add(PolylineAreaPoint(self.parametersPanel.pnlMaptPos.Point3d));


        # ipPolyLineNominal = new PolylineClass();
        # IPointCollection ipPColNominal = (IPointCollection)ipPolyLineNominal;
        # ipPColNominal.AddPoint(m_ipFAFPos);
        # ipPColNominal.AddPoint(m_ipMAPtPos);
        # ipPolyLineNominal.SpatialReference = m_SpatialReference;
        # BaseOperation.Create_PolylineFeature((IGeometry)ipPolyLineNominal, ref iFeatureClassother, featureField);
        # //////////////////////////////////////////////////////////////////////////

        dblIFWidth = Unit.ConvertNMToMeter(10.0);
        dblFAFWidth = self.GetSegmentWidth(ipSp, ipEp, self.parametersPanel.cmbNavAidType.SelectedIndex);

        # m_nSegmentCount = 1;
        # m_ipPrimary = new IPolyline[1];
        # m_ipSecondary = new IPolyline[2];

        ipSp = self.parametersPanel.pnlMaptPos.Point3d;
        ipEp = self.parametersPanel.pnlFafPos.Point3d;
        self.DrawProtectionCase1(ipSp,dblFAFWidth,ipEp,dblIFWidth, resultPointArrayList);
    def DrawApproachSegmentInterWithIF(self, resultPointArrayList, nominalTrackPolylineArea):
        # double a, b, c, d;
        m_ipNAVAIDPos = self.parametersPanel.pnlNavAidPos.Point3d
        m_ipMAPtPos = self.parametersPanel.pnlMaptPos.Point3d
        m_ipFAFPos = self.parametersPanel.pnlFafPos.Point3d
        a = MathHelper.calcDistance( m_ipNAVAIDPos, m_ipMAPtPos);
        b = MathHelper.calcDistance( m_ipMAPtPos, m_ipFAFPos );
        c = MathHelper.calcDistance( m_ipFAFPos, m_ipNAVAIDPos );
        d = Unit.ConvertNMToMeter(15);

        if ( b < 0.000001 ): return;

        # double p, h, DeltaDistance;
        p = ( a + b + c ) / 2;
        h = math.sqrt( p * ( p - a ) * ( p - b ) * ( p - c ) ) * 2 / b;

        DeltaDistance = math.sqrt( math.pow( d, 2.0 ) - math.pow( h, 2.0 ) ) - math.sqrt( math.pow( c, 2.0 ) - math.pow( h, 2.0 ) );

        if ( math.pow( b, 2.0 ) + math.pow( c, 2.0 ) - math.pow( a, 2.0 ) < 0 ): DeltaDistance *= -1;

        ipSp = m_ipNAVAIDPos;
        ipEp = m_ipMAPtPos;

        # //////////////////////////////////////////////////////////////////////////
        # // draw nominal track
        nominalTrackPolylineArea.Add(PolylineAreaPoint(m_ipFAFPos));
        nominalTrackPolylineArea.Add(PolylineAreaPoint(m_ipMAPtPos));

        DefaultWidth = 10.0;

        DefaultWidth = Unit.ConvertNMToMeter(DefaultWidth);
        # double dblIFWidth, dblFAFWidth;
        dblFAFWidth = self.GetSegmentWidth(ipSp,ipEp,self.parametersPanel.cmbNavAidType.SelectedIndex);

        # m_nSegmentCount = 1;
        # m_ipPrimary = new IPolyline[1];
        # m_ipSecondary = new IPolyline[2];

        ipSp = m_ipMAPtPos;
        ipEp = m_ipFAFPos;
        if ( DeltaDistance > 0 ):
            dblIFWidth = dblFAFWidth + ( DefaultWidth - dblFAFWidth ) * b / ( b + DeltaDistance);
            self.DrawProtectionCase1(ipSp,dblFAFWidth,ipEp,dblIFWidth,resultPointArrayList);
        else:
            dblIFWidth = DefaultWidth;
            self.DrawProtectionCase2(ipSp, dblFAFWidth,ipEp,dblIFWidth,b + DeltaDistance,resultPointArrayList);
    def DrawApproachSegmentInterWithNoIF(self, resultPointArrayList, nominalTrackPolylineArea, limitGeom):
        m_ipNAVAIDPos = self.parametersPanel.pnlNavAidPos.Point3d
        m_ipMAPtPos = self.parametersPanel.pnlMaptPos.Point3d
        m_ipFAFPos = self.parametersPanel.pnlFafPos.Point3d
        a = MathHelper.calcDistance( m_ipNAVAIDPos, m_ipMAPtPos);
        b = MathHelper.calcDistance( m_ipMAPtPos, m_ipFAFPos);
        c = MathHelper.calcDistance( m_ipFAFPos, m_ipNAVAIDPos);
        d = Unit.ConvertNMToMeter(15);

        if ( b < 0.0000001 ): return;

        # double p, h, DeltaDistance;
        p = ( a + b + c ) / 2;
        h = math.sqrt( p * ( p - a ) * ( p - b ) * ( p - c ) ) * 2 / b;

        DeltaDistance = math.sqrt( math.pow( d, 2.0 ) - math.pow( h, 2.0 ) ) - math.sqrt( math.pow( c, 2.0 ) - math.pow( h, 2.0 ) );

        if ( math.pow( b, 2.0 ) + math.pow( c, 2.0 ) - math.pow( a, 2.0 ) < 0 ): DeltaDistance *= -1;

        # esriUnits mapUnit = m_iMap.MapUnits;
        ipSp = m_ipNAVAIDPos;
        ipEp = m_ipMAPtPos;
        # double dblFAFWidth;
        DefaultWidth = 10.0;

        DefaultWidth = Unit.ConvertNMToMeter(DefaultWidth);
        dblFAFWidth = self.GetSegmentWidth(ipSp,ipEp,self.parametersPanel.cmbNavAidType.SelectedIndex);

        # m_nSegmentCount = 1;
        # m_ipPrimary = new IPolyline[1];
        # m_ipSecondary = new IPolyline[2];

        ipSp = m_ipMAPtPos;
        ipEp = m_ipFAFPos;
        bearing = MathHelper.getBearing(ipSp,ipEp);
        self.DrawProtectionCaseWithLimit(ipSp, dblFAFWidth, b + DeltaDistance, DefaultWidth, bearing, limitGeom, resultPointArrayList, nominalTrackPolylineArea);
    def DrawProtectionCaseWithLimit(self, ipStPoint, StWidth, dblDis, MdWidth, dblBearing, ipLimitLine, resultPointArrayList, nominalTrackPolylineArea):
        ipPoint = [None, None, None, None, None, None];
        ipMdPoint = MathHelper.distanceBearingPoint( ipStPoint, dblBearing, dblDis);

        maxDistance = 10000000000;
        ipEdPoint = MathHelper.distanceBearingPoint( ipStPoint, dblBearing, maxDistance );

        # // generalize limit line to improve speed
        maxAllowableOffset = 0.0001 if(define._units == QGis.Degrees) else 10;
        ipLimitLine = ipLimitLine.simplify(maxAllowableOffset);

        # // draw primary area
        # bStoreFeature = iDrawStyle != 1? true:false;
        ipPoint[0] = MathHelper.distanceBearingPoint( ipStPoint, dblBearing + math.pi / 2, StWidth / 4 );
        ipPoint[5] = MathHelper.distanceBearingPoint( ipStPoint, dblBearing - math.pi / 2, StWidth / 4 );
        ipPoint[2] = MathHelper.distanceBearingPoint( ipEdPoint, dblBearing + math.pi / 2, MdWidth / 4 );
        ipPoint[3] = MathHelper.distanceBearingPoint( ipEdPoint, dblBearing - math.pi / 2, MdWidth / 4 );
        ipPoint[1] = MathHelper.distanceBearingPoint( ipMdPoint, dblBearing + math.pi / 2, MdWidth / 4 );
        ipPoint[4] = MathHelper.distanceBearingPoint( ipMdPoint, dblBearing - math.pi / 2, MdWidth / 4 );


        # IPointCollection PrimaryColl = new MultipointClass();
        # for ( int i = 0 ; i < 6 ; i++ ) PrimaryColl.AddPoint( ipPoint[i] );
        # PrimaryColl.AddPoint( ipPoint[0] );
        primaryPointArray = self.MakePolyLineFromPointCollectionWithLimit(ipPoint, ipLimitLine);
        if ( primaryPointArray == None):
            QMessageBox.warning(self, "Warning", "Primary area has no intersection with limit!");
        else:
            self.resultObstacleAreaList.append([PrimaryObstacleArea(PolylineArea(primaryPointArray)), "Faf"])
            resultPointArrayList.append(primaryPointArray)

        # m_ipOriginPrimary = self.MakePolyLineFromPointCollection(ipPoint);
        # // draw 1st secondary area
        # bStoreFeature = iDrawStyle != 0? true:false;
        ipPoint1 = [None, None, None, None, None, None];
        ipPoint1[0] = MathHelper.distanceBearingPoint( ipStPoint, dblBearing + math.pi / 2, StWidth / 2 );
        ipPoint1[5] = MathHelper.distanceBearingPoint( ipStPoint, dblBearing + math.pi / 2, StWidth / 4 );
        ipPoint1[2] = MathHelper.distanceBearingPoint( ipEdPoint, dblBearing + math.pi / 2, MdWidth / 2 );
        ipPoint1[3] = MathHelper.distanceBearingPoint( ipEdPoint, dblBearing + math.pi / 2, MdWidth / 4 );
        ipPoint1[1] = MathHelper.distanceBearingPoint( ipMdPoint, dblBearing + math.pi / 2, MdWidth / 2 );
        ipPoint1[4] = MathHelper.distanceBearingPoint( ipMdPoint, dblBearing + math.pi / 2, MdWidth / 4 );

        ipPoint1.reverse()
        originPrimaryPolyline = [ipPoint1[0], ipPoint1[1], ipPoint1[2]]
        secondaryPointArray1 =  self.MakePolyLineFromPointCollectionWithLimit(ipPoint1, ipLimitLine);
        if ( secondaryPointArray1 == None ):
            QMessageBox.warning(self, "Warning", "Secondary area has no intersection with limit!");
        else:
            clippingPoliline = QgsGeometry.fromPolyline(originPrimaryPolyline)
            clipperPolygon = QgsGeometry.fromPolygon([ipLimitLine.asPolyline()])
            intersectPolyline = clippingPoliline.intersection(clipperPolygon)
            intersectionPointArray = None
            try:
                intersectionPointArray = intersectPolyline.asPolyline()
            except:
                intersectionPointArray = None
            secondaryObstacleArea1 = self.createSecondaryArea(secondaryPointArray1, primaryPointArray, intersectionPointArray)
            if secondaryObstacleArea1 != None:
                self.resultObstacleAreaList.append([secondaryObstacleArea1, "Faf"])
                resultPointArrayList.append(secondaryPointArray1)

        # m_ipOriginSeconday = new IPolyline[2];
        # if (PrimaryColl != null) m_ipOriginSeconday[0] = MakePolyLineFromPointCollection(PrimaryColl, false, ref iFeatureClass, m_SpatialReference, featureField);
        # // draw 2nd secondary area
        ipPoint2 = [None, None, None, None, None, None];
        ipPoint2[5] = MathHelper.distanceBearingPoint( ipStPoint, dblBearing - math.pi / 2, StWidth / 2 );
        ipPoint2[0] = MathHelper.distanceBearingPoint( ipStPoint, dblBearing - math.pi / 2, StWidth / 4 );
        ipPoint2[3] = MathHelper.distanceBearingPoint( ipEdPoint, dblBearing - math.pi / 2, MdWidth / 2 );
        ipPoint2[2] = MathHelper.distanceBearingPoint( ipEdPoint, dblBearing - math.pi / 2, MdWidth / 4 );
        ipPoint2[4] = MathHelper.distanceBearingPoint( ipMdPoint, dblBearing - math.pi / 2, MdWidth / 2 );
        ipPoint2[1] = MathHelper.distanceBearingPoint( ipMdPoint, dblBearing - math.pi / 2, MdWidth / 4 );

        ipPoint2.reverse()
        originPrimaryPolyline = [ipPoint2[0], ipPoint2[1], ipPoint2[2]]
        secondaryPointArray2 = self.MakePolyLineFromPointCollectionWithLimit(ipPoint2, ipLimitLine);
        if ( secondaryPointArray2 == None ):
            QMessageBox.warning(self, "Warning", "Secondary area has no intersection with limit!");
        else:
            clippingPoliline = QgsGeometry.fromPolyline(originPrimaryPolyline)
            clipperPolygon = QgsGeometry.fromPolygon([ipLimitLine.asPolyline()])
            intersectPolyline = clippingPoliline.intersection(clipperPolygon)
            intersectionPointArray = None
            try:
                intersectionPointArray = intersectPolyline.asPolyline()
            except:
                intersectionPointArray = None
            secondaryObstacleArea2 = self.createSecondaryArea(secondaryPointArray2, primaryPointArray, intersectionPointArray)
            if secondaryObstacleArea2 != None:
                self.resultObstacleAreaList.append([secondaryObstacleArea2, "Faf"])
                resultPointArrayList.append(secondaryPointArray2)
        #
        # IPointCollection Secondary2Coll = new MultipointClass();
        # for ( int i = 0 ; i < 6 ; i++ ) Secondary2Coll.AddPoint( ipPoint[i] );
        # Secondary2Coll.AddPoint( ipPoint[0] );
        # m_ipSecondary[2 * iSegment + 1] =  MakePolyLineFromPointCollectionWithLimit(Secondary2Coll, bStoreFeature, ref iFeatureClass, m_SpatialReference, ipLimitLine, featureField );
        # if ( m_ipSecondary[2 * iSegment + 1] == null )
        #     MessageBox.Show("Secondary area has no intersection with limit!");
        # if ( PrimaryColl != null) m_ipOriginSeconday[1] = MakePolyLineFromPointCollection(PrimaryColl, false, ref iFeatureClass, m_SpatialReference, featureField);
    def createSecondaryArea(self, secondaryPointArray, primaryPointArray, intersectionPointArray = None):
        if intersectionPointArray == None:
            if secondaryPointArray[0] == intersectionPointArray[0]:
                return SecondaryObstacleAreaWithManyPoints(PolylineArea(secondaryPointArray), PolylineArea(intersectionPointArray))
            elif secondaryPointArray[len(secondaryPointArray) - 1] == intersectionPointArray[0]:
                intersectionPointArray.reverse()
                return SecondaryObstacleAreaWithManyPoints(PolylineArea(secondaryPointArray), PolylineArea(intersectionPointArray))
            return None
        # startChange = secondaryPointArray[0] != intersectionPointArray[0]
        primaryPointArrayResult = []
        for pt in secondaryPointArray:
            for priPt in primaryPointArray:
                if pt == priPt:
                    primaryPointArrayResult.append(pt)
        if len(primaryPointArrayResult) == 0:
            return None
        return SecondaryObstacleAreaWithManyPoints(PolylineArea(secondaryPointArray), PolylineArea(primaryPointArrayResult))



    def MakePolyLineFromPointCollectionWithLimit(self, pointArray, polyline):
        clippingPolygon = QgsGeometry.fromPolygon([pointArray])
        clipperPolygon = QgsGeometry.fromPolygon([polyline.asPolyline()])
        if clipperPolygon == None:
            QMessageBox.warning(self, "Warning", "Selected polyline can not be made up polygon.\n Select the polyline which can made up polygon.")
            return None
        clipPolygon = clippingPolygon.intersection(clipperPolygon)
        if clipPolygon == None:
            return None
        try:
            return clipPolygon.asPolygon()[0]
        except:
            return None

    def DrawApproachSegmentInitial(self, resultPointArrayList, nominalTrackPolylineArea):
        ipSp = self.parametersPanel.pnlFafPos.Point3d;
        ipEp = self.parametersPanel.pnlMaptPos.Point3d;

        # //////////////////////////////////////////////////////////////////////////
        # // draw nominal track
        nominalTrackPolylineArea.Add(PolylineAreaPoint(ipSp));
        nominalTrackPolylineArea.Add(PolylineAreaPoint(ipEp));

        DefaultWidth = 10;
        DefaultWidth = Unit.ConvertNMToMeter(DefaultWidth);

        self.DrawProtectionCase1(ipSp,DefaultWidth,ipEp,DefaultWidth,resultPointArrayList);
    def GetSegmentWidth(self, ipNAVAID, ipFAF, iNAVAID):
        TotalWith = [2.5 , 2.0];
        SplayAngle = [10.3, 7.8 ];
        LimitDistance = [13.8, 21.9 ]
        DefaultWidth = 10.0;

        for i in range(2):
            SplayAngle[i] = SplayAngle[i] * math.pi / 180;
            TotalWith[i] = Unit.ConvertNMToMeter(TotalWith[i])
            LimitDistance[i] = Unit.ConvertNMToMeter(LimitDistance[i]);
        DefaultWidth = Unit.ConvertNMToMeter(DefaultWidth);


        # dblDistance, dblRes, dblLimitDistance;
        dblDistance = MathHelper.calcDistance(ipFAF, ipNAVAID);

        if ( iNAVAID == 2 ):
            dblLimitDistance = Unit.ConvertNMToMeter(7);
        else:
            dblLimitDistance = LimitDistance[iNAVAID];

        if ( dblDistance >= LimitDistance[iNAVAID] ):
            dblRes = DefaultWidth;
        else:
            dblRes = 2 * TotalWith[iNAVAID] + ( DefaultWidth - 2 * TotalWith[iNAVAID] ) * dblDistance / LimitDistance[iNAVAID];

        return dblRes;
    def CalculateGradient(self):
        dblDistance = self.CalculateDistance();
        iCATEGORY = self.parametersPanel.cmbAircraftCatgory.SelectedIndex;
        altitudeFAF = self.parametersPanel.pnlFafPos.Altitude().Feet
        altitudeTHR = 0.0
        if self.parametersPanel.txtApproachSegmentType.Value == SegmentType.Final:
            altitudeTHR = self.parametersPanel.pnlDerPos.Altitude().Feet
        else:
            altitudeTHR = self.parametersPanel.pnlMaptPos.Altitude().Feet
        if ( self.parametersPanel.txtApproachSegmentType.Value == SegmentType.Final ):
            if ( iCATEGORY == 2 ):
                resGradient = Unit.ConvertFeetToMeter( altitudeFAF - altitudeTHR - 35 ) / Unit.ConvertNMToMeter( dblDistance )#* BaseOperation.NM_TO_KM * 1000 );
            else:
                resGradient = Unit.ConvertFeetToMeter( altitudeFAF - altitudeTHR - 50 ) / Unit.ConvertNMToMeter( dblDistance )#* BaseOperation.NM_TO_KM * 1000 );

        else:
            if ( self.parametersPanel.txtApproachSegmentType.Value == SegmentType.InitStraight ):
                resGradient = Unit.ConvertFeetToMeter( altitudeFAF - altitudeTHR ) / Unit.ConvertNMToMeter( dblDistance )#* BaseOperation.NM_TO_KM * 1000 );
            elif ( iCATEGORY == 2 ):
                resGradient = Unit.ConvertFeetToMeter( altitudeFAF - altitudeTHR ) / Unit.ConvertNMToMeter( dblDistance )#* BaseOperation.NM_TO_KM * 1000 );
            elif ( iCATEGORY == 1 ):
                resGradient = Unit.ConvertFeetToMeter( altitudeFAF - altitudeTHR ) / Unit.ConvertNMToMeter( dblDistance - 1.5 )# * BaseOperation.NM_TO_KM * 1000 );
            else:
                resGradient = Unit.ConvertFeetToMeter( altitudeFAF - altitudeTHR )  / Unit.ConvertNMToMeter( dblDistance - 1 )# * BaseOperation.NM_TO_KM * 1000 );

        if ( resGradient < 0 ):
            self.parametersPanel.pnlGradient.Value = "";
            return resGradient
        else:
            self.parametersPanel.pnlGradient.Value = round(resGradient * 100, 2);

        return round(resGradient * 100, 2);
    def CalculateDeltaBearing(self):
        ipFAFPos = self.parametersPanel.pnlFafPos.Point3d
        ipMAPtPos = self.parametersPanel.pnlMaptPos.Point3d
        ipTHRPos = self.parametersPanel.pnlDerPos.Point3d
        res = MathHelper.getBearing(ipFAFPos, ipMAPtPos);
        res -= MathHelper.getBearing(ipMAPtPos, ipTHRPos);
        res = math.fabs(res) / math.pi * 180;

        if (res > 360 - res): res = 360 - res;
        return res;
    def CalculateBearing(self):
        ipFAFPos = self.parametersPanel.pnlFafPos.Point3d
        ipMAPtPos = self.parametersPanel.pnlMaptPos.Point3d
        res = MathHelper.getBearing(ipFAFPos, ipMAPtPos);
        if (res > math.pi / 2): res = 2 * math.pi + math.pi / 2 - res;
        elif (res < 0): res = math.pi / 2 - res;
        else: res = math.pi / 2 - res;
        return res * 180 / math.pi;
    def CalculateArcRadius(self):
        ipFAFPos = self.parametersPanel.pnlFafPos.Point3d
        ipNAVAIDPos = self.parametersPanel.pnlNavAidPos.Point3d
        resDistance = MathHelper.calcDistance(ipNAVAIDPos, ipFAFPos);
        resDistance = Unit.ConvertMeterToNM(resDistance);
        return resDistance;
    def DrawProtectionCase1(self, ipStPoint, StWidth, ipEdPoint, EdWidth, resultPointArrayList, areaName = None):
        if areaName == None:
            areaName = "Faf"
        dblDistance = MathHelper.calcDistance(ipStPoint, ipEdPoint);
        if (dblDistance < 0.000000001): return;

        # double dblBearing;
        dblBearing = MathHelper.getBearing(ipStPoint, ipEdPoint);

        ipPoints = [None, None, None, None];
        # for (int i = 0; i < 4; i++) ipPoint[i] = new PointClass();

        # draw primary area
        # bStoreFeature = iDrawStyle != 1 ? true : false;
        ipPoints[0] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing + math.pi / 2, StWidth / 4);
        ipPoints[3] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing - math.pi / 2, StWidth / 4);
        ipPoints[1] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing + math.pi / 2, EdWidth / 4);
        ipPoints[2] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing - math.pi / 2, EdWidth / 4);

        area = PolylineArea(ipPoints)
        resultPointArrayList.append([ipPoints, areaName])
        PrimaryColl = PrimaryObstacleArea(PolylineArea(area.method_14_closed()))
        self.resultObstacleAreaList.append([PrimaryColl, areaName])
        # for i in range(4):PrimaryColl.AddPoint(ipPoint[i]);
        # PrimaryColl.AddPoint(ipPoint[0]);
        # m_ipPrimary[iSegment] = MakePolyLineFromPointCollection(PrimaryColl, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);

        # draw 1st secondary area
        # bStoreFeature = iDrawStyle != 0 ? true : false;
        ipPoints1 = [None, None, None, None]
        ipPoints1[0] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing + math.pi / 2, StWidth / 2);
        ipPoints1[3] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing + math.pi / 2, StWidth / 4);
        ipPoints1[1] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing + math.pi / 2, EdWidth / 2);
        ipPoints1[2] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing + math.pi / 2, EdWidth / 4);

        Secondary1Coll = SecondaryObstacleArea(ipPoints1[3], ipPoints1[2], ipPoints1[0], ipPoints1[1])
        resultPointArrayList.append([ipPoints1, areaName])
        self.resultObstacleAreaList.append([Secondary1Coll, areaName])
        # for (int i = 0; i < 4; i++) Secondary1Coll.AddPoint(ipPoint[i]);
        # Secondary1Coll.AddPoint(ipPoint[0]);
        # m_ipSecondary[2 * iSegment] = MakePolyLineFromPointCollection(Secondary1Coll, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);

        # draw 2nd secondary area
        ipPoints2 = [None, None, None, None]
        ipPoints2[3] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing - math.pi / 2, StWidth / 2);
        ipPoints2[0] = MathHelper.distanceBearingPoint(ipStPoint, dblBearing - math.pi / 2, StWidth / 4);
        ipPoints2[2] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing - math.pi / 2, EdWidth / 2);
        ipPoints2[1] = MathHelper.distanceBearingPoint(ipEdPoint, dblBearing - math.pi / 2, EdWidth / 4);

        Secondary1Col2 = SecondaryObstacleArea(ipPoints2[0], ipPoints2[1], ipPoints2[3], ipPoints2[2])
        resultPointArrayList.append([ipPoints2, areaName])
        self.resultObstacleAreaList.append([Secondary1Col2, areaName])
        # IPointCollection Secondary2Coll = new MultipointClass();
        # for (int i = 0; i < 4; i++) Secondary2Coll.AddPoint(ipPoint[i]);
        # Secondary2Coll.AddPoint(ipPoint[0]);
        # m_ipSecondary[2 * iSegment + 1] = MakePolyLineFromPointCollection(Secondary2Coll, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);
    def DrawProtectionCase2(self, ipStPoint, StWidth, ipEdPoint, EdWidth, dblDis, resultPointArrayList, areaName = None):
        # POLYLINE_FIELD featureField;
        # featureField.areaID = enumArea.areaFinalApproach;
        # featureField.bearing = 0;
        # featureField.nonsiAlt = 0;
        # featureField.siAlt = 0;
        dblDistance = None;
        if areaName == None:
            areaName = "Faf"
        dblDistance = MathHelper.calcDistance( ipStPoint, ipEdPoint);
        if ( dblDistance < 0.0000001 ): return;

        dblBearing = None;
        dblBearing = MathHelper.getBearing( ipStPoint, ipEdPoint);

        ipPoint = [None, None, None, None, None, None];
        # IPoint ipMdPoint = new PointClass();
        # for ( int i = 0 ; i < 6 ; i++ ) ipPoint[i] = new PointClass();

        ipMdPoint = MathHelper.distanceBearingPoint( ipStPoint, dblBearing, dblDis );

        # // draw primary area
        # bool bStoreFeature = iDrawStyle != 1? true:false;
        ipPoint[0] = MathHelper.distanceBearingPoint( ipStPoint, dblBearing + math.pi / 2, StWidth / 4 );
        ipPoint[5] = MathHelper.distanceBearingPoint( ipStPoint, dblBearing - math.pi / 2, StWidth / 4 );
        ipPoint[2] = MathHelper.distanceBearingPoint( ipEdPoint, dblBearing + math.pi / 2, EdWidth / 4 );
        ipPoint[3] = MathHelper.distanceBearingPoint( ipEdPoint, dblBearing - math.pi / 2, EdWidth / 4 );
        ipPoint[1] = MathHelper.distanceBearingPoint( ipMdPoint, dblBearing + math.pi / 2, EdWidth / 4 );
        ipPoint[4] = MathHelper.distanceBearingPoint( ipMdPoint, dblBearing - math.pi / 2, EdWidth / 4 );

        resultPointArrayList.append([ipPoint, areaName])
        self.resultObstacleAreaList.append([PrimaryObstacleArea(PolylineArea(ipPoint)), areaName])
        # IPointCollection PrimaryColl = new MultipointClass();
        # for ( int i = 0 ; i < 6 ; i++ ) PrimaryColl.AddPoint( ipPoint[i] );
        # PrimaryColl.AddPoint( ipPoint[0] );
        # m_ipPrimary[iSegment] = MakePolyLineFromPointCollection(PrimaryColl, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);
        #
        # // draw 1st secondary area
        # bStoreFeature = iDrawStyle != 0? true:false;
        ipPoint1 = [None, None, None, None, None, None];
        ipPoint1[0] = MathHelper.distanceBearingPoint( ipStPoint, dblBearing + math.pi / 2, StWidth / 2 );
        ipPoint1[5] = MathHelper.distanceBearingPoint( ipStPoint, dblBearing + math.pi / 2, StWidth / 4 );
        ipPoint1[2] = MathHelper.distanceBearingPoint( ipEdPoint, dblBearing + math.pi / 2, EdWidth / 2 );
        ipPoint1[3] = MathHelper.distanceBearingPoint( ipEdPoint, dblBearing + math.pi / 2, EdWidth / 4 );
        ipPoint1[1] = MathHelper.distanceBearingPoint( ipMdPoint, dblBearing + math.pi / 2, EdWidth / 2 );
        ipPoint1[4] = MathHelper.distanceBearingPoint( ipMdPoint, dblBearing + math.pi / 2, EdWidth / 4 );
        ipPoint1.reverse()
        resultPointArrayList.append([ipPoint1, areaName])
        self.resultObstacleAreaList.append([SecondaryObstacleAreaWithManyPoints(PolylineArea(ipPoint1), PolylineArea([ipPoint1[0], ipPoint1[1], ipPoint1[2]])), areaName])
        # IPointCollection Secondary1Coll = new MultipointClass();
        # for ( int i = 0 ; i < 6 ; i++ ) Secondary1Coll.AddPoint( ipPoint[i] );
        # Secondary1Coll.AddPoint( ipPoint[0] );
        # m_ipSecondary[2 * iSegment] = MakePolyLineFromPointCollection(Secondary1Coll, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);
        #
        # // draw 2nd secondary area
        ipPoint2 = [None, None, None, None, None, None];
        ipPoint2[5] = MathHelper.distanceBearingPoint( ipStPoint, dblBearing - math.pi / 2, StWidth / 2 );
        ipPoint2[0] = MathHelper.distanceBearingPoint( ipStPoint, dblBearing - math.pi / 2, StWidth / 4 );
        ipPoint2[3] = MathHelper.distanceBearingPoint( ipEdPoint, dblBearing - math.pi / 2, EdWidth / 2 );
        ipPoint2[2] = MathHelper.distanceBearingPoint( ipEdPoint, dblBearing - math.pi / 2, EdWidth / 4 );
        ipPoint2[4] = MathHelper.distanceBearingPoint( ipMdPoint, dblBearing - math.pi / 2, EdWidth / 2 );
        ipPoint2[1] = MathHelper.distanceBearingPoint( ipMdPoint, dblBearing - math.pi / 2, EdWidth / 4 );

        ipPoint2.reverse()
        resultPointArrayList.append([ipPoint2, areaName])
        self.resultObstacleAreaList.append([SecondaryObstacleAreaWithManyPoints(PolylineArea(ipPoint2), PolylineArea([ipPoint2[0], ipPoint2[1], ipPoint2[2]])), areaName])
        # IPointCollection Secondary2Coll = new MultipointClass();
        # for ( int i = 0 ; i < 6 ; i++ ) Secondary2Coll.AddPoint( ipPoint[i] );
        # Secondary2Coll.AddPoint( ipPoint[0] );
        # m_ipSecondary[2 * iSegment + 1] = MakePolyLineFromPointCollection(Secondary2Coll, bStoreFeature, ref iFeatureClass, m_SpatialReference, featureField);
    def CheckDistance_Gradient_Bearing(self):
        bOk1 = False
        bOk2 = False
        bOk3 = False;
        lpszTextWarning1 = ""
        lpszTextWarning2 = ""
        lpszTextWarning3 = "";
        lpszTextResult1 = ""
        lpszTextResult2 = ""
        lpszTextResult3 = '';
        lpszMessage = "";

        lpszTextWarning1, lpszTextWarning2, lpszTextWarning3, lpszTextResult1, lpszTextResult2, lpszTextResult3, bOk1, bOk2, bOk3 = self.MakeWarning(lpszTextWarning1, lpszTextWarning2, lpszTextWarning3, lpszTextResult1, lpszTextResult2, lpszTextResult3, bOk1, bOk2, bOk3);

        bSuccess = True;
        # DialogResult buttonResult;
        if (self.m_iFinalInitInter != SegmentType.InitStraight and not bOk1 ):
            lpszMessage = lpszTextWarning1 + lpszTextResult1;
            buttonResult = QMessageBox.warning(self, "Conformation", lpszMessage, QMessageBox.Yes | QMessageBox.No);
            bSuccess = buttonResult == QMessageBox.Yes;
            if (bSuccess):
                self.m_wcWarning = lpszMessage;
            else: return bSuccess;

        if ( not bOk2 ):
            lpszMessage = lpszTextWarning2 + lpszTextResult2;
            buttonResult = QMessageBox.warning(self, "Conformation", lpszMessage, QMessageBox.Yes | QMessageBox.No);
            bSuccess = buttonResult == QMessageBox.Yes;
            if (bSuccess):
                self.m_wcWarning = lpszMessage;
            else: return bSuccess;
        if ( not bOk3 ):
            lpszMessage = lpszTextWarning3 + lpszTextResult3;
            buttonResult = QMessageBox.warning(self, "Conformation", lpszMessage, QMessageBox.Yes | QMessageBox.No);
            bSuccess = buttonResult == QMessageBox.Yes;
            if (bSuccess):
                self.m_wcWarning = lpszMessage;

        return bSuccess;

    def MakeWarning(self, warning1, warning2, warning3, result1, result2, result3, bOk1, bOk2, bOk3):
        selectCategory = self.parametersPanel.cmbAircraftCatgory.SelectedIndex;

        bOk1 = bOk2 = bOk3 = True;
        strFormat1 = ""
        strFormat2 = ""
        strFormat3 = "";
        # lpszUnit,lpszNot1,lpszNot2,lpszNot3;
        res1 = None
        res2 = None
        res3 = None;

        res1 = self.CalculateDistance();
        res2 = self.CalculateGradient();
        res3 = res2;
        # if ( m_unitSys == cocaUnitSystem.sysNonsi)	lpszUnit = "NM";
        # else lpszUnit = "Km";

        LBoundDistance = None
        UBoundDistance = None
        UBoundGradient = None
        LBoundGradient = None
        UBoundBearing = None;

        for case in switch (self.parametersPanel.txtApproachSegmentType.Value):
            if case(SegmentType.Final):
                # if ( m_unitSys == cocaUnitSystem.sysNonsi ) LBoundDistance = 3.0; else LBoundDistance = 5.6;
                LBoundDistance = 3.0
                if ( selectCategory == 0 ): UBoundGradient = 6.5;
                elif ( selectCategory == 1 ): UBoundGradient = 6.1;
                else: UBoundGradient = 10.0;
                LBoundGradient = 5.2;

                # //if ( res1 < LBoundDistance ) *bOk1 = false;
                if( res1 <LBoundDistance ): bOk1 = False;
                # //if ( res2 < LBoundGradient ) *bOk2 = false;
                if( res2 < LBoundGradient ): bOk2 = False;
                # //if ( res3 > UBoundGradient ): bOk3 = false;
                if( res3 > UBoundGradient ): bOk3 = False;

                warning1 = "The minimum final approach segment length shall not be less than 3.0NM (5.6km). See PANS OPS 5.1.3.";
                warning2 = "The minimum final approach segment descent gradient is 5.2%, See PANS OPS 5.3.1.1.";
                warning3 = "The maximum final approach segment descent gradient is 6.5% for Cat A/B, 6.1% for Cat C/D and 10% for Cat H. See PANS OPS 5.3.1.2.";
                strFormat1 = "Your calculated final approach segment length is {0}{1} which is {2} in accordance with PANS OPS.";
                strFormat2 = "Your calculated final approach segment descent gradient is {0}% which is {1} in accordance with PANS OPS.";
                strFormat3 = "Your calculated final approach segment descent gradient is {0}% which is {1} in accordance with PANS OPS.";

                break;
            if case(SegmentType.InterStraight) or case(SegmentType.InterWithIf) or case(SegmentType.InterWithNoIf):#intermediate straight, with IF, with no IF
                # if ( m_unitSys == cocaUnitSystem.sysNonsi ){
                if ( selectCategory == 2 ):
                    LBoundDistance = 2.0;
                    UBoundDistance = 5.0;
                else:
                    LBoundDistance = 5.0;
                    UBoundDistance = 15.0;
                if ( selectCategory == 2 ):
                    UBoundGradient = 10.0;
                    UBoundBearing = 60.0;
                else:
                    UBoundGradient = 5.2;
                    UBoundBearing = 30.0;
                res3 = self.CalculateDeltaBearing();
                if ( res1 < LBoundDistance or res1 > UBoundDistance ): bOk1 = False;
                if ( res2 > UBoundGradient ): bOk2 = False;
                if ( res3 > UBoundBearing ): bOk3 = False;

                warning1 = "The length of the intermediate approach segment shall not be more than 15NM-28km (Cat H, 5.0NM- 9.3km) or less than 5.0NM-9.3km (Cat H, 2.0NM- 3.7km), See PANS OPS 4.3.1.1.";
                warning2 = "The maximum descent gradient in the intermediate approach segment is 5.2%(Cat H, 10%), See PANS OPS 4.3.3.2.";
                warning3 = "Intermediate track shall not differ from the final approach track by more than 30°(Cat H, 60°), See PANS OPS 4.3.";
                strFormat1 = "Your calculated intermediate segment length is {0}{1} which is {2} in accordance with PANS OPS.";
                strFormat2 = "Your calculated intermediate segment descent gradient is {0}% which is {1} in accordance with PANS OPS.";
                strFormat3 = "Your calculated differences between intermediate track and final approach track is {0}° which is {1} in accordance with PANS OPS.";
                if ( res3 < 0 ):
                    bOk3 = False;
                    warning3 = "";
                    strFormat3  = "Not able to calculate differences between Intermediate and Final. Please select the MAPt position.";
                break;
            else:
                if ( selectCategory == 0 ): UBoundGradient = 8.0;
                else: UBoundGradient = 10.0;
                UBoundBearing = 120.0;

                # if ( m_unitSys == cocaUnitSystem.sysSi ){
                #     if ( selectCategory == 2 ) LBoundDistance = 9.3;
                #     else LBoundDistance = 13.0;
                # }
                # else{
                if ( selectCategory == 2 ): LBoundDistance = 5.0;
                else: LBoundDistance = 7.0;
                res1 = self.CalculateArcRadius();
                res3 = self.CalculateDeltaBearing();
                if ( self.m_iFinalInitInter == SegmentType.InitArc and res1 < LBoundDistance ): bOk1 = False;
                if ( res2 > UBoundGradient ): bOk2 = False;
                if ( res3 > UBoundBearing ): bOk3 = False;

                warning1 = "The minimum arc radius shall be 13 km (7 NM) (Cat H, 9.3 km (5 NM)). See PANS OPS 3.3.2";
                warning2 = "The maximum descent gradient in the initial approach segment is 8%(Cat H, 10%), See PANS OPS 4.3.3.2.";
                warning3 = "Initial track shall not differ from the intermediate track by more than 120°, See PANS OPS 4.3.";
                strFormat1 = "Your arc radius is {0}{1} which {2} is in accordance with PANS OPS ";
                strFormat2 = "Your calculated initial segment descent gradient is {0}% which is {1} in accordance with PANS OPS.";
                strFormat3 = "Your calculated differences between initial track and intermediate track is {0}° which is {1} in accordance with PANS OPS.";
                if ( res3 < 0 ):
                    bOk3 = False;
                    warning3 = "";
                    strFormat3 = "Not able to calculate differences between Initial and Intermediate. Please select the FAF position.";
                break;

        lpszNot1 = "" if(bOk1) else "not";
        lpszNot2 = "" if(bOk2) else "not"
        lpszNot3 = "" if(bOk3) else "not"
        lpszUnit = "NM"
        result1 = strFormat1.format(res1, lpszUnit, lpszNot1);
        result2 = strFormat2.format(res2, lpszNot2);
        result3 = strFormat3.format(res3, lpszNot3);
        return warning1, warning2, warning3, result1, result2, result3, bOk1, bOk2, bOk3

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

class ApproachSegmentObstacles(ObstacleTable):
    def __init__(self, surfacesList, primaryMoc):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)

        self.surfaceType = SurfaceTypes.ApproachSegment
        self.surfacesList = surfacesList
        self.primaryMoc = primaryMoc.Metres
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
        self.IndexDistInSecM = fixedColumnCount + 1
        self.IndexMocAppliedM = fixedColumnCount + 2
        self.IndexMocAppliedFt = fixedColumnCount + 3
        # self.IndexMocMultiplier = fixedColumnCount + 2
        self.IndexOcaM = fixedColumnCount + 4
        self.IndexOcaFt = fixedColumnCount + 5
        self.IndexSurface = fixedColumnCount + 6
        # self.IndexCritical = fixedColumnCount + 4

        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DistInSecM,
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                # ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt,
                ObstacleTableColumnType.Surface
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
        self.source.setItem(row, self.IndexDistInSecM, item)

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
        self.source.setItem(row, self.IndexOcaM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[3])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[3]))
        self.source.setItem(row, self.IndexOcaFt, item)

        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4])
        self.source.setItem(row, self.IndexSurface, item)

        # item = QStandardItem(str(checkResult[2]))
        # item.setData(checkResult[2])
        # self.source.setItem(row, self.IndexCritical, item)

    def checkObstacle(self, obstacle_0):
        if len(self.surfacesList) == 0:
            return
        for area, areaName in self.surfacesList:
            resultValue = []
            mocMultiplier = self.primaryMoc * obstacle_0.MocMultiplier;
            obstacleAreaResult = area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier, resultValue);
            if len(resultValue) == 2:
                num = resultValue[0]
                num1 = resultValue[1]
            else:
                continue
            if (obstacleAreaResult != ObstacleAreaResult.Outside):
                position = obstacle_0.Position;
                if num == None:
                    checkResult = [obstacleAreaResult, num1, num];
                    self.addObstacleToModel(obstacle_0, checkResult)
                    continue

                # z = position.get_Z() + obstacle_0.Trees + num;
                # criticalObstacleType = CriticalObstacleType.No;
                # if (z > self.enrouteAltitude):
                #     criticalObstacleType = CriticalObstacleType.Yes;
                checkResult = [obstacleAreaResult, num1, num, num + position.get_Z(), areaName];
                self.addObstacleToModel(obstacle_0, checkResult)