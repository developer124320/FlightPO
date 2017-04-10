# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import SurfaceTypes, ObstacleTableColumnType, ObstacleAreaResult, TurnDirection
from FlightPlanner.RaceTrackAndHolding.ui_RaceTrackAndHolding import Ui_RaceTrackAndHolding
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.helpers import MathHelper, Unit, Distance, DistanceUnits, AltitudeUnits, Altitude, Speed, SpeedUnits
from FlightPlanner.types import Point3D
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Prompts import Prompts
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, SecondaryObstacleArea, SecondaryObstacleAreaWithManyPoints, SecondaryAreaStraight
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.DataHelper import DataHelper
from map.tools import QgsMapToolSelectUtils
from Type.switch import switch



from PyQt4.QtCore import SIGNAL, QString, QCoreApplication, Qt, QRect
from PyQt4.QtGui import QColor, QMessageBox, QFileDialog, QMenu, QLabel, QStandardItem
from qgis.core import QGis, QgsVectorLayer, QgsGeometry, QgsField, QgsFeature, QgsPoint
from qgis.gui import  QgsMapTool, QgsRubberBand, QgsMapToolPan, QgsMapCanvasSnapper
import define, math,  os, platform


class RaceTrackDlg(FlightPlanBaseDlg):
    def __init__(self, parent, dlgType = "NavAid"):
        FlightPlanBaseDlg.__init__(self, parent)




        self.setObjectName("RaceTrackDlg")
        self.dlgType = dlgType
        if self.dlgType == "NavAid":
            self.surfaceType = SurfaceTypes.RaceTrackNavAid
            self.m_iRaceTrackStyle = 1
        elif self.dlgType == "Fix":
            self.surfaceType = SurfaceTypes.RaceTrackFix
            self.m_iRaceTrackStyle = 2
        else:
            self.surfaceType = SurfaceTypes.Holding
            self.m_iRaceTrackStyle = 3
        self.selectedRow = None
        self.editingModelIndex = None




        # f, geomList, pointList = geom.splitGeometry(line, True)
        
        self.m_polylineFixArea = None
        self.m_iNAVAID = None
        self.m_ipNAVAIDPos = None;
        self.m_ipDMENAVAIDPos = None;
        self.m_iDirection = None;
        self.m_iCondition = None;
        self.m_bOmnidirectional = None;
        self.m_dblInboundTrackBearing = None;
        self.m_dblAltitudeNAVA = None;
        self.m_dblAltitudeInitial = None;
        self.m_dblAltitudeTurn = None;
        self.m_dblAltitudeFinal = None;
        self.m_dblDMEdistance = None;
        self.m_OutboundTime = None;
        self.m_ISAVAR = None;
        self.m_dblIAS = None;
        self.m_OutputK = None;
        self.m_OutputIASInput = None;
        self.m_OutputV = None;
        self.m_Outputv = None;
        self.m_OutputR = None;
        self.m_Outputr = None;
        self.m_Outputh = None;
        self.m_OutputOutboundTime = None;
        self.m_OutputISAVar = None;
        self.m_OutputW1 = None;
        self.m_OutputE45 = None;
        self.m_Outputt = None;
        self.m_OutputWr = []
        for i in range(20):
            self.m_OutputWr.append(None)
        self.m_OutputXE = None;
        self.m_OutputYE = None;
        self.m_OutputEX = None;
        self.m_OutputEY = None;
        self.m_OutputDestPt = [];
        for i in range(8):
            self.m_OutputDestPt.append(None)
        self.m_strWarning = [];
        for i in range(5):
            self.m_strWarning.append(None)
        self.m_nWarning = None;
        self.MAX_ALLOWABLE_OFFSET = None;
        self.m_dblDefMOCSI = []
        self.m_strFieldName = []
        
        

        self.initParametersPan()
        self.setWindowTitle(self.surfaceType)
        self.resize(600, 650)
        QgisHelper.matchingDialogSize(self, 650, 700)
        self.surfaceList = None
        self.manualPolygon = None
        
        

        self.resultObstacleAreaList = []
        self.nominalTrackLayer = None
        self.resultLayerList = []



        self.vorDmeFeatureArray = []
        self.currentLayer = define._canvas.currentLayer()
        self.initBasedOnCmb()
        
        if (self.m_iRaceTrackStyle == 3):
            defaultMOCSI = [[ 300, 600 ], [ 150, 300 ], [ 120, 240 ], [ 90, 180 ], [ 60, 120 ] ];
            fieldNames = [ "Normal Condition", "Turbulence Condition", "Holding MOC" ];
            # m_MOCForm = new MOCForm();
            # m_MOCForm.rn = 5;
            # m_MOCForm.cn = 2;
            self.m_dblDefMOCSI = defaultMOCSI;
            self.m_strFieldName = fieldNames;
        else:
            defaultMOCSI = [ [ 300, 600 ] ];
            fieldNames = [ "Normal Condition", "Turbulence Condition", "RaceTrack MOC" ];
            # m_MOCForm = new MOCForm();
            # m_MOCForm.rn = 1;
            # m_MOCForm.cn = 2;
            self.m_dblDefMOCSI = defaultMOCSI;
            self.m_strFieldName = fieldNames;
    def RaceTrackForm_Load(self):
        if (self.m_iRaceTrackStyle == 3):
            defaultMOCSI = [ [ 300, 600 ], [ 150, 300 ], [ 120, 240 ], [ 90, 180 ], [ 60, 120 ] ];
            fieldNames = [ "Normal Condition", "Turbulence Condition", "Holding MOC" ];
            self.m_dblDefMOCSI = defaultMOCSI;
            self.m_strFieldName = fieldNames;
        else:
            defaultMOCSI = [ [ 300, 600 ] ];
            fieldNames = [ "Normal Condition", "Turbulence Condition", "RaceTrack MOC" ];
            self.m_dblDefMOCSI = defaultMOCSI;
            self.m_strFieldName = fieldNames;
    def initBasedOnCmb(self):

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

        pass

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

        parameterList.append(("Positions", "group"))
        self.ui.tabCtrlGeneral.setCurrentIndex(0)

        if self.parametersPanel.gbNavAid.Visible:
            parameterList.append((self.parametersPanel.gbNavAid.Caption, "group"))
            parameterList.append((self.parametersPanel.cmbNavAidType.Caption, self.parametersPanel.cmbNavAidType.SelectedItem))
            parameterList.append((self.parametersPanel.cmbBasedOn.Caption, self.parametersPanel.cmbBasedOn.SelectedItem))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlNavAidPos.txtPointX.text()), float(self.parametersPanel.pnlNavAidPos.txtPointY.text()))
            parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
            parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
            parameterList.append(("X", self.parametersPanel.pnlNavAidPos.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlNavAidPos.txtPointY.text()))
        if self.parametersPanel.pnlDmePos.Visible and self.parametersPanel.pnlDmePos.btnCapture.isEnabled():
            parameterList.append((self.parametersPanel.pnlDmePos.Caption, "group"))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlDmePos.txtPointX.text()), float(self.parametersPanel.pnlDmePos.txtPointY.text()))
            parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
            parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
            parameterList.append(("X", self.parametersPanel.pnlDmePos.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlDmePos.txtPointY.text()))
        if self.parametersPanel.cmbEntry.Visible:
            parameterList.append((self.parametersPanel.cmbEntry.Caption, self.parametersPanel.cmbEntry.SelectedItem))
        if self.parametersPanel.txtBearing.Visible:
            parameterList.append((self.parametersPanel.txtBearing.Caption, self.parametersPanel.txtBearing.Value))

        parameterList.append(("Parameters", "group"))



        if self.parametersPanel.cmbDirection.Visible:
            parameterList.append((self.parametersPanel.cmbDirection.Caption, self.parametersPanel.cmbDirection.SelectedItem))
        if self.parametersPanel.cmbCondition.Visible:
            parameterList.append((self.parametersPanel.cmbCondition.Caption, self.parametersPanel.cmbCondition.SelectedItem))
        if self.parametersPanel.cmbAircraftCatgory.Visible:
            parameterList.append((self.parametersPanel.cmbAircraftCatgory.Caption, self.parametersPanel.cmbAircraftCatgory.SelectedItem))
        if self.parametersPanel.cmbDirection.Visible:
            parameterList.append((self.parametersPanel.cmbDirection.Caption, self.parametersPanel.cmbDirection.SelectedItem))
        if self.parametersPanel.txtNAVAlt.Visible:
            parameterList.append((self.parametersPanel.txtNAVAlt.Caption, str(self.parametersPanel.txtNAVAlt.Value.Metres) + "m"))
            parameterList.append(("", str(self.parametersPanel.txtNAVAlt.Value.Feet) + "ft"))
        if self.parametersPanel.txtInitialAlt.Visible:
            parameterList.append((self.parametersPanel.txtInitialAlt.Caption, str(self.parametersPanel.txtInitialAlt.Value.Metres) + "m"))
            parameterList.append(("", str(self.parametersPanel.txtInitialAlt.Value.Feet) + "ft"))
        if self.parametersPanel.txtTurnAlt.Visible:
            parameterList.append((self.parametersPanel.txtTurnAlt.Caption, str(self.parametersPanel.txtTurnAlt.Value.Metres) + "m"))
            parameterList.append((self.parametersPanel.txtTurnAlt.Caption, str(self.parametersPanel.txtTurnAlt.Value.Feet) + "ft"))
        if self.parametersPanel.txtFinalAlt.Visible:
            parameterList.append((self.parametersPanel.txtFinalAlt.Caption, str(self.parametersPanel.txtFinalAlt.Value.Metres) + "m"))
            parameterList.append(("", str(self.parametersPanel.txtFinalAlt.Value.Feet) + "ft"))
        if self.parametersPanel.txtLimitDistance.Visible:
            parameterList.append((self.parametersPanel.txtLimitDistance.Caption, str(self.parametersPanel.txtLimitDistance.Value.NauticalMiles) + "nm"))
        if self.parametersPanel.txtOutboundTime.Visible:
            parameterList.append((self.parametersPanel.txtOutboundTime.Caption, str(self.parametersPanel.txtOutboundTime.Value)))
        if self.parametersPanel.txtOutboundLeg.Visible:
            parameterList.append((self.parametersPanel.txtOutboundLeg.Caption, str(self.parametersPanel.txtOutboundLeg.Value.NauticalMiles) + "nm"))
        if self.parametersPanel.txtISA.Visible:
            parameterList.append((self.parametersPanel.txtISA.Caption, str(self.parametersPanel.txtISA.Value)))
        if self.parametersPanel.txtIAS.Visible:
            parameterList.append((self.parametersPanel.txtIAS.Caption, str(self.parametersPanel.txtIAS.Value.Knots) + "kts"))
        if self.parametersPanel.txtTAS.Visible:
            parameterList.append((self.parametersPanel.txtTAS.Caption, str(self.parametersPanel.txtTAS.Value.Knots) + "kts"))

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
        self.ui.btnPDTCheck.setVisible(False)
        # self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)

#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)

    def initSurfaceCombo(self):
        self.ui.cmbObstSurface.clear()
        # self.ui.cmbObstSurface.addItems(["Faf", "Ma"])
    def btnEvaluate_Click(self):
        self.obstaclesModel = RaceTrackAndHoldingObstacles(self.resultObstacleAreaList, self.m_dblDefMOCSI, self.m_iRaceTrackStyle, self.m_iCondition)
        return FlightPlanBaseDlg.btnEvaluate_Click(self)

    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        self.m_nWarning = 0;

        if (not self.GetUserParameters(True)):
            return;
        if (not self.CheckInputValueForInitSpeed()):
            return;
        if (not self.CheckDescentRate()):
            return;
        if (not self.CheckDivergences()):
            return;

        resultPolylineAreaList = []
        nominalTraclPolylineArea = []

        for case in switch(self.m_iRaceTrackStyle):
            if case(1) or case(2):
                self.DrawRaceTrack(resultPolylineAreaList, nominalTraclPolylineArea);
                break;
            elif case(3):
                self.DrawHolding(resultPolylineAreaList, nominalTraclPolylineArea);
                break;

        constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)
        nominalTrackLayer = AcadHelper.createVectorLayer("Nominal Track_" + self.surfaceType.replace(" ", "_").replace("-", "_"), QGis.Line)
        for area in nominalTraclPolylineArea:
            AcadHelper.setGeometryAndAttributesInLayer(nominalTrackLayer, area.method_14_closed())
        # AcadHelper.setGeometryAndAttributesInLayer(nominalTrackLayer, nominalTraclPolylineArea.method_14())
        for area in resultPolylineAreaList:
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, area.method_14_closed())

        QgisHelper.appendToCanvas(define._canvas, [constructionLayer, nominalTrackLayer], self.surfaceType)
        self.resultLayerList = [constructionLayer, nominalTrackLayer]
        QgisHelper.zoomToLayers(self.resultLayerList)
        self.ui.btnEvaluate.setEnabled(True)


    def initParametersPan(self):
        ui = Ui_RaceTrackAndHolding()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)



        self.connect(self.parametersPanel.pnlNavAidPos, SIGNAL("positionChanged"), self.CalcOutBoundTime)
        self.connect(self.parametersPanel.pnlDmePos, SIGNAL("positionChanged"), self.CalcOutBoundTime)
        # self.connect(self.parametersPanel.pnlDerPos, SIGNAL("positionChanged"), self.changeDistGradient)
        # self.connect(self.parametersPanel.cmbTurnDirection, SIGNAL("Event_0"), self.changeDistGradient)
        # self.connect(self.parametersPanel.txtApproachSegmentType, SIGNAL("Event_0"), self.changeDistGradient)
        self.connect(self.parametersPanel.cmbNavAidType, SIGNAL("Event_0"), self.initBasedOnCmb)
        self.connect(self.parametersPanel.cmbNavAidType, SIGNAL("Event_0"), self.comboNAVAID_SelectedIndexChanged)
        self.connect(self.parametersPanel.cmbCondition, SIGNAL("Event_0"), self.comboCondition_SelectedIndexChanged)
        self.connect(self.parametersPanel.cmbAircraftCatgory, SIGNAL("Event_0"), self.comboCategory_SelectedIndexChanged)
        self.connect(self.parametersPanel.cmbDirection, SIGNAL("Event_0"), self.comboDirection_SelectedIndexChanged)

        self.connect(self.parametersPanel.txtNAVAlt, SIGNAL("Event_0"), self.textNAVAlt_TextChanged)
        self.connect(self.parametersPanel.txtInitialAlt, SIGNAL("Event_0"), self.textInitialAlt_TextChanged)
        self.connect(self.parametersPanel.txtTurnAlt, SIGNAL("Event_0"), self.textTurnAlt_TextChanged)
        self.connect(self.parametersPanel.txtISA, SIGNAL("Event_0"), self.textISA_TextChanged)
        self.connect(self.parametersPanel.txtOutboundTime, SIGNAL("Event_0"), self.textOutboundTime_TextChanged)
        self.connect(self.parametersPanel.txtLimitDistance, SIGNAL("Event_0"), self.textLimitDistance_TextChanged)
        self.connect(self.parametersPanel.txtBearing, SIGNAL("Event_0"), self.CalcOutBoundTime)
        self.connect(self.parametersPanel.txtIAS, SIGNAL("Event_0"), self.textISA_TextChanged)
        self.comboNAVAID_SelectedIndexChanged()
    def ConstructTemplate(self, direction, rotAngle, iFeatureClass, featureField):
        # //Construct BasePt
        # double x, y, dblTas, radius;
        NBASE = 20
        Gn = 100;
        # i;
        # IPoint[] BasePt;

        BasePt = [];
        
        for i in range(NBASE):
            BasePt.append(Point3D())
        x = self.m_ipNAVAIDPos.x()
        y = self.m_ipNAVAIDPos.y();

        dblTas = Unit.ConvertNMToMeter(self.m_dblIAS)
        radius = Unit.ConvertNMToMeter(self.m_Outputr);

        BasePt[0].PutCoords( x, y );
        BasePt[1].PutCoords( x - 5 * dblTas, y );
        BasePt[2].PutCoords( x - 11 * dblTas, y );

        temp = Point3D();
        # double alpha,d;

        x = BasePt[2].X
        y = BasePt[2].Y;
        
        temp.PutCoords( x, y + radius );
        for i in range(1, 5):
            alpha = 3 * math.pi / float(2) - math.pi / 4 * i;
            BasePt[i+2] = MathHelper.distanceBearingPointArcGIS( temp, alpha, radius);

        temp.PutCoords( x + 6 * dblTas, y + radius );
        for i in range(3):
            alpha = math.pi / 2 - math.pi / 4 * i;
            BasePt[i+7] = MathHelper.distanceBearingPointArcGIS( temp, alpha, radius );

        BasePt[10] = MathHelper.distanceBearingPointArcGIS( BasePt[6], math.pi * 5 / 360 * 2, ( self.m_OutboundTime - 5 ) * dblTas );
        BasePt[11] = MathHelper.distanceBearingPointArcGIS( BasePt[6], math.pi * 5 / 360 * 2, ( self.m_OutboundTime + 21 ) * dblTas );
        BasePt[12] = MathHelper.distanceBearingPointArcGIS (BasePt[6], math.pi * (-5) / 360 * 2, ( self.m_OutboundTime - 5 ) * dblTas );
        BasePt[13] = MathHelper.distanceBearingPointArcGIS( BasePt[6], math.pi * (-5) / 360 * 2, ( self.m_OutboundTime + 21 ) * dblTas );

        x = BasePt[11].X
        y = BasePt[11].Y;
        temp.PutCoords( x, y - radius );
        for i in range(1, 4):
            alpha = math.pi / float(2) - i * math.pi / float(4);
            BasePt[i+13] = MathHelper.distanceBearingPointArcGIS( temp, alpha, radius );

        x = BasePt[13].X
        y = BasePt[13].Y;
        temp.PutCoords( x, y - radius );
        for i in range(3):
            alpha = (-1) * i * math.pi / float(4);
            BasePt[i+16] = MathHelper.distanceBearingPointArcGIS( temp, alpha, radius );

        x = BasePt[12].X
        y = BasePt[12].Y;
        BasePt[19].PutCoords( x, y - 2 * radius );

        if ( math.fabs(rotAngle) > 0.000001):
            for i in range(1, NBASE):
                alpha = MathHelper.getBearing( BasePt[0], BasePt[i]);
                d = MathHelper.calcDistance( BasePt[0], BasePt[i]);
                BasePt[i]  = MathHelper.distanceBearingPointArcGIS( BasePt[0] ,alpha + rotAngle, d);

        tt = [None, None, None];
        alpha = math.pi * 2 * 10 / 360 ;

        # for ( i = 0 ; i < 3 ; i++) tt[i] = new PointClass();
        
        d = Unit.ConvertNMToMeter(self.m_OutputWr[6]);
        tt[0] = MathHelper.distanceBearingPointArcGIS( BasePt[6], math.pi * 3 / 2 - alpha + rotAngle, d );
        d = Unit.ConvertNMToMeter(self.m_OutputWr[10]);
        tt[1] = MathHelper.distanceBearingPointArcGIS( BasePt[10] ,math.pi * 3 / 2 - alpha + rotAngle, d );
        d = Unit.ConvertNMToMeter(self.m_OutputWr[11]);
        tt[2] = MathHelper.distanceBearingPointArcGIS( BasePt[11], math.pi * 3 / 2 - alpha + rotAngle, d );


        if ( direction == -1 ):
            for i in range(1, NBASE):
                BasePt[i] = QgisHelper.Reverse_Point( BasePt[0], rotAngle,BasePt[i]);
        # //ConstructTemplate
        # int[] NumPoints;
        NumPoints = [9, 1, 3, 3, 1];

        iPolylineArray = [];

        nowNumber = 1
        pn = 0;
        ipSegColl = []
        for i in range(5):
            # //pPolyLine[i].CreateInstance(CLSID_Polyline);
            ipSegColl = [];
            pn = 0;
            while( pn < NumPoints[i] ):
                if ( nowNumber == 12 or nowNumber == 13 ):
                    nowNumber = 14;
                # ipConCirArc = new CircularArcClass();
                d = Unit.ConvertNMToMeter(self.m_OutputWr[nowNumber]);
                ipConCirArc = PolylineArea(None, BasePt[nowNumber], d)
                # ipConCirArc = MathHelper.constructCircle(BasePt[nowNumber], d, 50);
                # ISegment ipSegment = (ISegment)ipConCirArc;
                ipSegColl.append(ipConCirArc);
                pn += 1;
                nowNumber += 1
            ipItemPolyline = PolylineArea(QgisHelper.convexFull(ipSegColl));
            # ipItemPolyline.Smooth(MAX_ALLOWABLE_OFFSET);
            # // generalize polyline to improve speed
            # double maxAllowableOffset = (self.m_mapUnit == esriUnits.esriDecimalDegrees)? 0.0001 : 10;
            # ipItemPolyline.Generalize(maxAllowableOffset);
            iPolylineArray.append(ipItemPolyline);

        # ipTemp = PolylineArea();
        # for i in range(5):
        #     aa = iPolylineArray[i];
        #     ipTemp.AddSegmentCollection(aa);
        # }
        ipTemplate = PolylineArea(QgisHelper.convexFull( iPolylineArray ))

        ipSpiral = iPolylineArray[0];

        # //check racetrack
        # //Draw Nominal Track
        OutPtColl = [];
        Cp = Point3D();
        tP = []
        for i in range(4*Gn+1):
            tP.append(Point3D())

        x = self.m_ipNAVAIDPos.X
        y = self.m_ipNAVAIDPos.Y;

        Cp = MathHelper.distanceBearingPointArcGIS( self.m_ipNAVAIDPos, math.pi / 2 + rotAngle, radius );

        for i in range(Gn):
            alpha = math.pi * 3 / 2 - math.pi * i / Gn;
            tP[i] = Point3D();
            tP[i] = MathHelper.distanceBearingPointArcGIS( Cp, alpha + rotAngle, radius );

            if ( direction == -1 ):
                tP[i] = QgisHelper.Reverse_Point( self.m_ipNAVAIDPos, rotAngle, tP[i]);
            OutPtColl.append(tP[i]);

        Cp = MathHelper.distanceBearingPointArcGIS( Cp, rotAngle, dblTas * self.m_OutboundTime );

        point1 = Point3D()
        point2 = Point3D();

        point1 = MathHelper.distanceBearingPointArcGIS( Cp, rotAngle + math.pi / 2, radius);
        point2 = MathHelper.distanceBearingPointArcGIS( Cp, rotAngle - math.pi / 2, radius);

        for i in range(Gn):
            alpha = math.pi / 2 - math.pi * i / Gn;
            tP[Gn+i] = Point3D();
            tP[Gn+i] = MathHelper.distanceBearingPointArcGIS( Cp, alpha + rotAngle, radius );
            if ( direction == -1 ):
                tP[Gn+i] = QgisHelper.Reverse_Point( self.m_ipNAVAIDPos, rotAngle, tP[Gn+i]);
            OutPtColl.append(tP[Gn+i]);
        OutPtColl.append(tP[0]);

        ipTempPoly = PolylineArea(OutPtColl)
        iFeatureClass.append(ipTempPoly)
        return ipTemplate, ipSpiral
        # ipPtColl = ipTempPoly;
        #
        # ipPtColl.SetPointCollection(OutPtColl);
        # BaseOperation.Create_PolylineFeature((IGeometry)ipTempPoly, ref iFeatureClass, featureField);
    def DrawFixToleranceOfRaceTrack(self, iFeatureClass, featureField):
        d = 0
        bearing = 0.0;
        alpha = [0.0, 0.0, 0.0, 0.0];

        bearing = self.m_dblInboundTrackBearing;

        for case in switch( self.m_iNAVAID ):	
            if case(2):
                d = math.tan( math.pi * 2 * 50 / 360 ) * ( self.m_dblAltitudeInitial - self.m_dblAltitudeNAVA );
                alpha[1] = math.asin( 0.2 / math.tan( math.pi * 2 * 50 / 360 )) - math.pi * 2 * 5 / 360;
                break;
            elif case(3):
                d = math.tan( math.pi * 2 * 50 / 360 ) * ( self.m_dblAltitudeInitial - self.m_dblAltitudeNAVA );
                alpha[1] = math.asin( 0.2 / math.tan( math.pi * 2 * 50 / 360 )) - math.pi * 2 * 5 / 360;
                break;
            elif case(0):
                d = math.tan( math.pi * 2 * 40 / 360 ) * ( self.m_dblAltitudeInitial - self.m_dblAltitudeNAVA );
                alpha[1] = math.pi * 2 * 15 / 360;
                break;
            elif case(1):
                d = math.tan( math.pi * 2 * 40 / 360 ) * ( self.m_dblAltitudeInitial - self.m_dblAltitudeNAVA );
                alpha[1] = math.pi * 2 * 15 / 360;
                break;
        # alpha[1] = alpha[1]
        alpha[0] = -alpha[1];
        alpha[2] = math.pi - alpha[1] - math.pi * 2 * 10 / 360;
        alpha[3] = math.pi * 2 - alpha[2];

        ipCircArc = PolylineArea();
        ipLine = [None, None, None, None];
        ipSegColl = PolylineArea();

        d = Unit.ConvertFeetToMeter(d)#BaseOperation.ConvertUnit( self.m_mapUnit, self.m_unitSys, cocaUnitType.whatHeight, d, false );

        for i in range(4):
            self.m_OutputDestPt[i] = MathHelper.distanceBearingPointArcGIS( self.m_ipNAVAIDPos, alpha[i] + bearing, d );

        for i in range(4):
            if( i == 0 or i == 2 ) :#// arc
                # ipCircArc[i] = PolylineArea();
                ipCircArc.Add(PolylineAreaPoint(MathHelper.distanceBearingPointArcGIS(self.m_ipNAVAIDPos, alpha[i] + bearing, d), math.tan((alpha[i + 1] - alpha[i]) / 4)))
                ipCircArc.Add(PolylineAreaPoint(MathHelper.distanceBearingPointArcGIS(self.m_ipNAVAIDPos, alpha[i] + bearing - alpha[i + 1] - alpha[i], d)))
                # ipCircArc[i].PutCoordsByAngle(self.m_ipNAVAIDPos, alpha[i] + bearing, alpha[i + 1] - alpha[i], d);
                # //ISegment ipSeg = (ISegment)ipCircArc[i];
                # //ipSegColl.AddSegment(ipSeg);                # ipSegColl.AddSegment((ISegment)ipCircArc[i]);
            else:# { // line
                # ipLine[i] = PolylineArea();
                ipCircArc.Add(PolylineAreaPoint(self.m_OutputDestPt[i]))
                ipCircArc.Add(PolylineAreaPoint(self.m_OutputDestPt[( i + 1 ) % 4] ))
        #         //ISegment ipSeg = (ISegment)ipLine[i];
        #         //ipSegColl.AddSegment(ipSeg);
        #         ipSegColl.AddSegment((ISegment)ipLine[i]);
        #     }
        # }
        iFeatureClass.append(ipCircArc)
        # BaseOperation.Create_PolylineFeature((IGeometry)ipSegColl, ref iFeatureClass, featureField);
    def ConstructDMElimitLine(self, ipCp, r, srcPolyLine, ipSrc):
        # IPolyline ipResPolyline;
        #
        # double xx, yy, cx, cy, sx, sy, alpha;
        cx = ipCp.x(); cy = ipCp.y();
        sx = ipSrc.x(); sy = ipSrc.y();

        res = [];

        for i in range(10):
            alpha = 2 * math.pi / 10 * i;
            xx = cx + math.cos(alpha) * r - sx;
            yy = cy + math.sin(alpha) * r - sy;
            tempPolyline = PolylineArea();
            tempPolyline = PolylineArea.MovePolyLine(srcPolyLine, xx, yy );
            # aaa = (ISegmentCollection)tempPolyline;
            res.append(tempPolyline);

        # IPolygon resPolygon = new PolygonClass();
        ipResPolyline = PolylineArea(QgisHelper.convexFull(res))

        # IRing ipRing = new RingClass();
        #
        # resPolygon.QueryExteriorRings(ref ipRing);
        #
        # IPolygon bbb = new PolygonClass();
        # ISegmentCollection aa = (ISegmentCollection)bbb;
        #
        # aa.SetSegmentCollection((ISegmentCollection)ipRing);
        # ITopologicalOperator ipTopoBound = (ITopologicalOperator)bbb;
        # IGeometry geo;
        # geo = ipTopoBound.Boundary;
        # ipResPolyline = (IPolyline)geo;

        return ipResPolyline;
    def DrawRaceTrack(self, iFeatureClass, iOtherFeatureClass):
        # POLYLINE_FIELD featureField;
        # 
        # double dblNonSIaltitude, dblSIaltitude;

        self.CalcParameters();
        self.resultObstacleAreaList = []

        # //Draw FIX TOLERANCE
        
        for i in range(4):
            self.m_OutputDestPt[i] = None;

        # double angle;
        # double d, xx, yy;
        angle = self.m_dblInboundTrackBearing;
        # //set field's value
        # if (self.m_unitSys == cocaUnitSystem.sysNonsi ){
        #     featureField.nonsiAlt = dblNonSIaltitude =  self.m_dblAltitudeFinal;
        dblSIaltitude = Unit.ConvertFeetToMeter(self.m_dblAltitudeFinal)#, cocaUnitType.whatHeight, cocaUnitSystem.sysNonsi );
        # }
        # else{
        #     featureField.siAlt = dblSIaltitude =  self.m_dblAltitudeFinal;
        #     featureField.nonsiAlt = dblNonSIaltitude = BaseOperation.ConvertValueFromUnits(dblSIaltitude, cocaUnitType.whatHeight, cocaUnitSystem.sysSi );
        # }
        # featureField.areaID = enumArea.areaRaceTrack;
        # featureField.bearing = 0;
        # //RaceInput->ipProgressDlg->SetLine(2,L"Drawing fix tolerance...",FALSE,NULL);
        if ( self.m_polylineFixArea == None ):
            self.DrawFixToleranceOfRaceTrack(iOtherFeatureClass, dblSIaltitude)
        else:
            ipPointColl = self.m_polylineFixArea;
            for i in range(4):
                self.m_OutputDestPt[i] = ipPointColl[i]

        # //RaceInput->ipProgressDlg->SetProgress64(1,6);
        #
        # //Draw Template and Basic Area
        Template = PolylineArea();
        Spiral = PolylineArea();
        ResultSeg = []
        ResultPolyLine = PolylineArea();


        # //RaceInput->ipProgressDlg->SetLine(2,L"Constructing template...",FALSE,NULL);
        Template, Spiral = self.ConstructTemplate(self.m_iDirection, angle, iOtherFeatureClass, dblSIaltitude);
        # // generalize polyline to improve speed
        # maxAllowableOffset = (self.m_mapUnit == esriUnits.esriDecimalDegrees)? 0.0001 : 10;
        # Template.Generalize(maxAllowableOffset);

        # //RaceInput->ipProgressDlg->SetProgress64(1,6);


        DMElimitLine = PolylineArea();
        if ( self.m_iNAVAID % 2 == 1 ):
            # //RaceInput->ipProgressDlg->SetLine(2,L"Constructing DME limiting line...",FALSE,NULL);
            # IPolyline tempSpiral;
            tempSpiral = PolylineArea.RotatePolyLineArcGIS(Spiral,  self.m_ipNAVAIDPos, -math.pi );

            add = 0.25
            # if ( self.m_unitSys == cocaUnitSystem.sysSi ) add = 0.46; else add = 0.25;
            d = self.m_dblDMEdistance;
            d = d + ( add + d * 0.0125 );
            d = Unit.ConvertNMToMeter(d)#BaseOperation.ConvertUnit( self.m_mapUnit, self.m_unitSys, cocaUnitType.whatDist, d, false );
            DMElimitLine = self.ConstructDMElimitLine( self.m_ipDMENAVAIDPos, d, tempSpiral, self.m_ipNAVAIDPos );
            # DMElimitLine.Smooth(MAX_ALLOWABLE_OFFSET);
        #     //RaceInput->ipProgressDlg->SetProgress64(1,6);
        # }

        # if (raceTrackWithTemplateToolStripMenuItem.Checked)
        #     BaseOperation.Create_PolylineFeature(Template, ref iFeatureClass, featureField);//template
        #
        # //RaceInput->ipProgressDlg->SetLine(2,L"Creating polyline features...",FALSE,NULL);

        # double NAVAIDX, NAVAIDY;

        NAVAIDX = self.m_ipNAVAIDPos.x();
        NAVAIDY = self.m_ipNAVAIDPos.y();

        iPolyLineArray = []

        for i in range(4):
            xx = self.m_OutputDestPt[i].x();
            yy = self.m_OutputDestPt[i].y();
            xx -= NAVAIDX;
            yy -= NAVAIDY;
            iTempPolyline = PolylineArea.MovePolyLine(Template, xx, yy );
            iPolyLineArray.append(iTempPolyline);
            ResultSeg.append(iTempPolyline);
        #     ISegmentCollection aaaColl = (ISegmentCollection)iPolyLineArray.get_Element(i);
        #     ResultSeg.AddSegmentCollection(aaaColl);
        #     //aaaColl.RemoveSegments(0, aaaColl.SegmentCount, false);
        # # }

        ResultPolyLine = None
        if ( not self.m_bOmnidirectional ):
            # //self.m_enumStepID = stepIDBasicArea;

            if ( self.m_iNAVAID % 2 == 1 ):
                # tempPoly = new PolygonClass();
                tempPoly = PolylineArea(QgisHelper.convexFull(ResultSeg))
                # //RaceInput->ipProgressDlg->SetProgress64(1,6);
                ResultPolyLine = self.CutPolygon(tempPoly, DMElimitLine);
                # //RaceInput->ipProgressDlg->SetProgress64(1,6);
            else:
                ResultPolyLine = PolylineArea(QgisHelper.convexFull(ResultSeg))
            #     //RaceInput->ipProgressDlg->SetProgress64(1,6);
            # }
            iFeatureClass.append(ResultPolyLine)
            self.resultObstacleAreaList.append(PrimaryObstacleArea(ResultPolyLine))
            # BaseOperation.Create_PolylineFeature(ResultPolyLine, ref iFeatureClass, featureField);
    
            d = Unit.ConvertKMToMeters(4.6)#BaseOperation.ConvertUnit( self.m_mapUnit, cocaUnitSystem.sysSi, cocaUnitType.whatDist, 4.6, false );

            buffer = PolylineArea(QgisHelper.offsetCurve(ResultPolyLine.method_14(), d ))
            # //if ( self.m_unitSys == cocaUnitSystem.sysNonsi ){
            # //    dblNonSIaltitude +=  RaceInput->dblMOC;
            # //    dblSIaltitude = BaseOperation.ConvertValueToUnits( dblNonSIaltitude, cocaUnitType.whatHeight, cocaUnitSystem.sysNonsi );
            # //}
            # //else{
            # //    dblSIaltitude += RaceInput->dblMOC;
            # //    dblNonSIaltitude = BaseOperation.ConvertValueToUnits( dblSIaltitude, cocaUnitType.whatHeight, cocaUnitSystem.sysSi );
            # //}
            iFeatureClass.append(buffer)
            self.resultObstacleAreaList.append(SecondaryObstacleAreaWithManyPoints(buffer, ResultPolyLine, True))
        #     BaseOperation.Create_PolylineFeature(buffer, ref iFeatureClass, featureField);
        #     //RaceInput->ipProgressDlg->SetProgress64(1,6);
        # }


        if ( not self.m_bOmnidirectional ):
            return;

        # double ex, ey;
        ex = self.m_OutputEX;
        ey = self.m_OutputEY;
        ex = Unit.ConvertNMToMeter(ex)#BaseOperation.ConvertUnit( self.m_mapUnit, self.m_unitSys, cocaUnitType.whatDist, ex, false );
        ey = Unit.ConvertNMToMeter(ey)#BaseOperation.ConvertUnit( self.m_mapUnit, self.m_unitSys, cocaUnitType.whatDist, ey, false );

        d = MathHelper.calcDistance( self.m_ipNAVAIDPos, self.m_OutputDestPt[0])#, self.m_iMap, self.m_mapUnit );

        tP = None
        iOmniPolylineArray = [];
        for i in range(10):
            tP = MathHelper.distanceBearingPointArcGIS(self.m_ipNAVAIDPos, 2 * math.pi * i / float(10), d);
            xx = tP.x();
            yy = tP.y();
            tP = Point3D(xx - ex, yy - ey);
            tP = QgisHelper.Rotate_Point(self.m_ipNAVAIDPos, self.m_dblInboundTrackBearing, tP, "ArcGIS");

            # IPolyline tempPolyline;

            xx = tP.x();
            yy = tP.y();
            tempPolyline = PolylineArea.MovePolyLine(Template, xx - NAVAIDX, yy - NAVAIDY);
            iOmniPolylineArray.append(tempPolyline);
            ResultSeg.append(tempPolyline)
        #     ISegmentCollection aaa = (ISegmentCollection)iOmniPolylineArray.get_Element(i);
        #     ResultSeg.AddSegmentCollection(aaa);
        #     //aaa.Release();
        #     //tempPolyline.Release();
        # }

        if ( self.m_iNAVAID % 2 == 1 ):
            tempPoly = PolylineArea();
            tempPoly = PolylineArea(QgisHelper.convexFull(ResultSeg))
            ResultPolyLine = self.CutPolygon(tempPoly, DMElimitLine);
        else:
            ResultPolyLine = PolylineArea(QgisHelper.convexFull(ResultSeg))
        iFeatureClass.append(ResultPolyLine)

        Result2 = []
        Result2.append(ResultPolyLine);

        # IPolyline RotatedSpiral;
        RotatedSpiral = PolylineArea.RotatePolyLineArcGIS(Spiral, self.m_ipNAVAIDPos, math.pi * 70 / 180 );

        # double alpha;

        for i in range(4):
            self.m_OutputDestPt[i + 4] = None;
            alpha = MathHelper.getBearing(self.m_ipNAVAIDPos, self.m_OutputDestPt[i]) + math.pi * 70 / 180;
            self.m_OutputDestPt[i + 4] = MathHelper.distanceBearingPointArcGIS( self.m_ipNAVAIDPos, alpha, d );

        iOtherPolylineArray = [];
        for i in range(8):
            # IPolyline tempPolyline;
            xx = self.m_OutputDestPt[i].x();
            yy = self.m_OutputDestPt[i].y();
            tempPolyline = PolylineArea.MovePolyLine(RotatedSpiral,  xx - NAVAIDX, yy - NAVAIDY );
            iOtherPolylineArray.append(tempPolyline);
            Result2.append(iOtherPolylineArray[i])
        #     ISegmentCollection ccc = (ISegmentCollection)iOtherPolylineArray.get_Element(i);
        #
        #     Result2.AddSegmentCollection( ccc );
        #     //ccc.Release();
        # }

        ResultPolyLine = PolylineArea(QgisHelper.convexFull(Result2))
        # //Result2.Release();
        iFeatureClass.append(ResultPolyLine)
        self.resultObstacleAreaList.append(PrimaryObstacleArea(ResultPolyLine))
        # BaseOperation.Create_PolylineFeature( ResultPolyLine, ref iFeatureClass, featureField );

        # //RaceInput->ipProgressDlg->SetProgress64(1,6);

        d = Unit.ConvertKMToMeters(4.6)#BaseOperation.ConvertUnit( self.m_mapUnit, cocaUnitSystem.sysSi, cocaUnitType.whatDist, 4.6, false );
        omnibuffer = PolylineArea();
        omnibuffer = PolylineArea(QgisHelper.offsetCurve(ResultPolyLine.method_14(), d))

        # //if ( self.m_unitSys == cocaUnitSystem.sysNonsi ){
        # //    dblNonSIaltitude +=  RaceInput->dblMOC;
        # //    dblSIaltitude = BaseOperation.ConvertValueToUnits( dblNonSIaltitude, cocaUnitType.whatHeight, sysNonsi );
        # //}
        # //else{
        # //    dblSIaltitude += RaceInput->dblMOC;
        # //    dblNonSIaltitude = BaseOperation.ConvertValueToUnits( dblSIaltitude, cocaUnitType.whatHeight,cocaUnitSystem.sysSi );
        # //}
        iFeatureClass.append(omnibuffer)
        self.resultObstacleAreaList.append(SecondaryObstacleAreaWithManyPoints(omnibuffer, ResultPolyLine, True))
        # BaseOperation.Create_PolylineFeature(omnibuffer, ref iFeatureClass, featureField);
    def DrawHolding(self, iFeatureClass, iOtherFeatureClass):
        self.resultObstacleAreaList = []
        # POLYLINE_FIELD featureField;
        # 
        # double dblNonSIaltitude, dblSIaltitude;

        self.CalcParameters();

        # //Draw FIX TOLERANCE

        for i in range(4):
            self.m_OutputDestPt[i] = Point3D();

        # double angle;
        # double d, xx, yy;
        angle = self.m_dblInboundTrackBearing;
        # //set field's value
        dblNonSIaltitude = self.m_dblAltitudeFinal
        # if (self.m_unitSys == cocaUnitSystem.sysNonsi)
        # {
        #     featureField.nonsiAlt = ;
        featureField = dblSIaltitude = Unit.ConvertFeetToMeter(dblNonSIaltitude);
        # featureField.areaID = enumArea.areaRaceTrack;
        # featureField.bearing = 0;
        # //RaceInput->ipProgressDlg->SetLine(2,L"Drawing fix tolerance...",FALSE,NULL);
        if (self.m_polylineFixArea == None):
            self.DrawFixToleranceOfRaceTrack(iOtherFeatureClass, featureField);
        else:
            ipPointColl = self.m_polylineFixArea;
            for i in range(4):
                self.m_OutputDestPt[i] = ipPointColl[i]

        # //RaceInput->ipProgressDlg->SetProgress64(1,6);

        # //Draw Template and Basic Area
        Template = PolylineArea();
        Spiral = PolylineArea();
        ResultSeg = PolylineArea();
        ResultPolyLine = PolylineArea();


        # //RaceInput->ipProgressDlg->SetLine(2,L"Constructing template...",FALSE,NULL);
        Template, Spiral = self.ConstructTemplate(self.m_iDirection, angle, iOtherFeatureClass, featureField);
        # // generalize polyline to improve speed
        # maxAllowableOffset = (self.m_mapUnit == esriUnits.esriDecimalDegrees) ? 0.0001 : 10;
        # Template.Generalize(maxAllowableOffset);

        # //RaceInput->ipProgressDlg->SetProgress64(1,6);


        DMElimitLine = PolylineArea();
        if (self.m_iNAVAID % 2 == 1):
            # //RaceInput->ipProgressDlg->SetLine(2,L"Constructing DME limiting line...",FALSE,NULL);
            tempSpiral = PolylineArea();
            tempSpiral = PolylineArea.RotatePolyLineArcGIS(Spiral, self.m_ipNAVAIDPos, math.pi);

            # double add;
            add = 0.25
            # if (self.m_unitSys == cocaUnitSystem.sysSi) add = 0.46; else add = 0.25;
            d = self.m_dblDMEdistance;
            d = d + (add + d * 0.0125);
            d = Unit.ConvertNMToMeter(d);
            DMElimitLine = self.ConstructDMElimitLine(self.m_ipDMENAVAIDPos, d, tempSpiral, self.m_ipNAVAIDPos);
            # DMElimitLine.Smooth(MAX_ALLOWABLE_OFFSET);
            # //RaceInput->ipProgressDlg->SetProgress64(1,6);
        
        # if (raceTrackWithTemplateToolStripMenuItem.Checked)
        #     BaseOperation.Create_PolylineFeature(Template, ref iFeatureClass, featureField);//template
        # 
        # //RaceInput->ipProgressDlg->SetLine(2,L"Creating polyline features...",FALSE,NULL);

        # double NAVAIDX, NAVAIDY;

        NAVAIDX = self.m_ipNAVAIDPos.X;
        NAVAIDY = self.m_ipNAVAIDPos.Y;

        iPolyLineArray = [];
        ResultSeg = []

        for i in range(4):
            xx = self.m_OutputDestPt[i].X;
            yy = self.m_OutputDestPt[i].Y;
            xx -= NAVAIDX;
            yy -= NAVAIDY;
            iTempPolyline = PolylineArea.MovePolyLine(Template, xx, yy);
            iPolyLineArray.append(iTempPolyline);
            ResultSeg.append(iTempPolyline);
        #     ISegmentCollection aaaColl = (ISegmentCollection)iPolyLineArray.get_Element(i);
        #     ResultSeg.AddSegmentCollection(aaaColl);
        #     //aaaColl.RemoveSegments(0, aaaColl.SegmentCount, false);
        # }

        BufferDistance = [ [1.9, 1], [3.7, 2] ,[5.6, 3], [7.4, 4], [9.3, 5]];
        BufferMOC = [ [300, 984], [150, 492], [120, 394], [90, 294], [60, 197]];
        # double tempMOC;

        if (not self.m_bOmnidirectional):
            # //self.m_enumStepID = stepIDBasicArea;
            if (self.m_iNAVAID % 2 == 1):
                tempPoly = PolylineArea();
                tempPoly = PolylineArea(QgisHelper.convexFull(ResultSeg))
                # //RaceInput->ipProgressDlg->SetProgress64(1,6);
                ResultPolyLine = self.CutPolygon(tempPoly, DMElimitLine);
                # //RaceInput->ipProgressDlg->SetProgress64(1,6);
            else:
                ResultPolyLine = PolylineArea(QgisHelper.convexFull(ResultSeg))
                # //RaceInput->ipProgressDlg->SetProgress64(1,6);
            iFeatureClass.append(ResultPolyLine)
            # self.resultObstacleAreaList.append(PrimaryObstacleArea(ResultPolyLine))
            # BaseOperation.Create_PolylineFeature(ResultPolyLine, ref iFeatureClass, featureField);

            for i in range(5):
                d = Unit.ConvertNMToMeter(BufferDistance[i][1])
                # if ( self.m_unitSys == cocaUnitSystem.sysSi )
                #     d = BaseOperation.ConvertUnit(self.m_mapUnit, cocaUnitSystem.sysSi, cocaUnitType.whatDist, BufferDistance[i,0], false);
                # else
                #     d = BaseOperation.ConvertUnit(self.m_mapUnit, cocaUnitSystem.sysNonsi, cocaUnitType.whatDist, BufferDistance[i, 1], false);

                buffer = PolylineArea();
                buffer = PolylineArea(QgisHelper.offsetCurve(ResultPolyLine.method_14_closed(), d))
                # //if ( RaceInput-> iUnit == sysNonsi ){
                # //    tempMOC = BufferMOC[i][1];
                # //    if( RaceInput->iCondition == 1 ) tempMOC *= 2;
                # //    dblNonSIaltitude +=  tempMOC;
                # //    dblSIaltitude = BaseOperation.ConvertValueFromUnits( dblNonSIaltitude, cocaUnitType.whatHeight, sysNonsi );
                # //}
                # //else{
                # //    tempMOC = BufferMOC[i][0];
                # //    if( RaceInput->iCondition == 1 ) tempMOC *= 2;
                # //    dblSIaltitude += tempMOC;
                # //    dblNonSIaltitude = BaseOperation.ConvertValueFromUnits( dblSIaltitude, cocaUnitType.whatHeight,cocaUnitSystem.sysSi );

                iFeatureClass.append(buffer)
                self.resultObstacleAreaList.append(PrimaryObstacleArea(buffer))
                # BaseOperation.Create_PolylineFeature(buffer, ref iFeatureClass, featureField);
                # //RaceInput->ipProgressDlg->SetProgress64(1,6);

        if (not self.m_bOmnidirectional):
            return;

        # double ex, ey;
        ex = self.m_OutputEX;
        ey = self.m_OutputEY;
        ex = Unit.ConvertNMToMeter(ex);
        ey = Unit.ConvertNMToMeter(ey);

        d = MathHelper.calcDistance(self.m_ipNAVAIDPos, self.m_OutputDestPt[0]);

        tP = Point3D();
        iOmniPolylineArray = [];
        for i in range(10):
            tP = MathHelper.distanceBearingPointArcGIS(self.m_ipNAVAIDPos, 2 * math.pi * i / float(10), d);
            xx = tP.X; yy = tP.Y;
            tP.PutCoords(xx - ex, yy - ey);
            tP = QgisHelper.Rotate_Point(self.m_ipNAVAIDPos, self.m_dblInboundTrackBearing, tP, "ArcGIS");

            # IPolyline tempPolyline;

            xx = tP.X; yy = tP.Y;
            tempPolyline = PolylineArea.MovePolyLine(Template, xx - NAVAIDX, yy - NAVAIDY);
            iOmniPolylineArray.append(tempPolyline);
            # ISegmentCollection aaa = (ISegmentCollection)iOmniPolylineArray.get_Element(i);
            ResultSeg.append(tempPolyline);
            # //aaa.Release();
            # //tempPolyline.Release();

        if (self.m_iNAVAID % 2 == 1):
            tempPoly = PolylineArea();
            tempPoly = PolylineArea(QgisHelper.convexFull(ResultSeg))
            ResultPolyLine = self.CutPolygon(tempPoly, DMElimitLine);
        else:
            ResultPolyLine = PolylineArea(QgisHelper.convexFull(ResultSeg))
        iFeatureClass.append(ResultPolyLine)
        # BaseOperation.Create_PolylineFeature(ResultPolyLine, ref iFeatureClass, featureField);
        # //RaceInput->ipProgressDlg->SetProgress64(1,6);

        # //ResultSeg.Release();
        Result2 = ResultPolyLine;

        # IPolyline RotatedSpiral;
        RotatedSpiral = PolylineArea.RotatePolyLineArcGIS(Spiral, self.m_ipNAVAIDPos, math.pi * 70 / float(180));

        # double alpha;

        for i in range(4):
            self.m_OutputDestPt[i + 4] = Point3D();
            alpha = MathHelper.getBearing(self.m_ipNAVAIDPos, self.m_OutputDestPt[i]) + math.pi * 70 / float(180);
            self.m_OutputDestPt[i + 4] = MathHelper.distanceBearingPointArcGIS(self.m_ipNAVAIDPos, alpha, d);

        iOtherPolylineArray = [];
        for i in range(8):
            xx = self.m_OutputDestPt[i].x();
            yy = self.m_OutputDestPt[i].y();
            tempPolyline = PolylineArea.MovePolyLine(RotatedSpiral, xx - NAVAIDX, yy - NAVAIDY);
            iOtherPolylineArray.append(tempPolyline);
        iOtherPolylineArray.append(ResultPolyLine);
        ResultPolyLine = PolylineArea(QgisHelper.convexFull(iOtherPolylineArray))
        iFeatureClass.append(ResultPolyLine)
        for i in range(5):
            d = Unit.ConvertNMToMeter(BufferDistance[i][1])
            omnibuffer = PolylineArea();
            omnibuffer = PolylineArea(QgisHelper.offsetCurve(ResultPolyLine.method_14_closed(), d));
            iFeatureClass.append(omnibuffer)
            self.resultObstacleAreaList.append(PrimaryObstacleArea(omnibuffer))

    def CutPolygon(self, tempPoly, polylineArea):

        constructionLineLayer = QgsVectorLayer("polygon?crs=%s"%define._xyCrs.authid (), "as", "memory")

        geom = QgsGeometry.fromPolygon([tempPoly.method_14_closed()])
        feat= QgsFeature()
        feat.setGeometry(geom)
        constructionLineLayer.startEditing()
        pr = constructionLineLayer.dataProvider()
        pr.addFeatures([feat])
        # constructionLineLayer.addFeature(feat)
        constructionLineLayer.commitChanges()
        constructionLineLayer.startEditing()
        line = [QgsPoint(-10, 50), QgsPoint(200, 50)]
        n = constructionLineLayer.splitFeatures(polylineArea.method_14(), True)
        constructionLineLayer.commitChanges()
        print constructionLineLayer.featureCount()
        ptList = None
        for f in constructionLineLayer.getFeatures():
            g = f.geometry()
            ptList = g.asPolygon()
            realGeom = QgsGeometry.fromPolygon(ptList)
            break

        # geom = QgsGeometry.fromPolygon([tempPoly.method_14_closed()])
        # flag, geomList, ptList = geom.splitGeometry(polylineArea.method_14(), True)
        # if len(geomList) == 2:
        #     realGeom = geomList[1]
        if realGeom.length() < 0.0000001:
            return tempPoly
        return PolylineArea(ptList[0])
        # else:
        #     realGeom = geomList[0]
        #     if realGeom.length() < 0.0000001:
        #         return tempPoly
        #     return PolylineArea(realGeom.asPolygon[0])
    def CalcParameters(self):
        dblAltitude = self.m_dblAltitudeInitial - self.m_dblAltitudeNAVA;

        aa = 0;

        aa = Unit.ConvertFeetToMeter(dblAltitude)#, cocaUnitType.whatHeight, cocaUnitSystem.sysNonsi);

        k = 171233 * math.pow( 288 + self.m_ISAVAR - 0.006496 * aa, 0.5 ) / math.pow( 288 - 0.006496 * aa , 2.628 );

        self.m_OutputK = k;
        self.m_OutputK = self.m_dblIAS;
        self.m_OutputV = dblV = self.m_dblIAS * k;
        self.m_Outputv = dblv = dblV / 3600;
        self.m_OutputR = R = 509.26 / dblV#( ( self.m_unitSys == cocaUnitSystem.sysSi )? 943.27 : 509.26 )/ dblV;
        self.m_Outputr = r = dblV / ( 62.83 * R );
        self.m_Outputh = dblAltitude / 1000;
        self.m_OutputISAVar = self.m_ISAVAR;
        self.m_OutputOutboundTime = self.m_OutboundTime;

        # if ( self.m_unitSys == cocaUnitSystem.sysSi )
        #     self.m_OutputWr[0] = ( 12 * dblAltitude / 1000 + 87 ) / 3600.0;
        # else
        self.m_OutputWr[0] = ( 2 * dblAltitude / 1000 + 47 ) / 3600.0;


        self.m_OutputE45 = E45 = 45 * self.m_OutputWr[0] / R;

        self.m_OutputWr[1] = 5 * self.m_OutputWr[0];
        self.m_OutputWr[2] = 11 * self.m_OutputWr[0];

        for i in range(8):
            if ( i < 5 ):
                self.m_OutputWr[i + 2] = self.m_OutputWr[2] + i * E45;
            else:
                self.m_OutputWr[i + 2] = self.m_OutputWr[1] + ( i - 1 ) * E45;
        self.m_OutputWr[10] = ( self.m_OutboundTime + 6 ) * self.m_OutputWr[0] + 4 * E45;
        self.m_OutputWr[11] = self.m_OutputWr[10] + 14 * self.m_OutputWr[0];
        self.m_OutputWr[12] = self.m_OutputWr[10];
        self.m_OutputWr[13] = self.m_OutputWr[11];
        self.m_OutputWr[14] = self.m_OutputWr[11] + E45;
        self.m_OutputWr[15] = self.m_OutputWr[11] + 2 * E45;
        self.m_OutputWr[16] = self.m_OutputWr[15];
        self.m_OutputWr[17] = self.m_OutputWr[11] + 3 * E45;
        self.m_OutputWr[18] = self.m_OutputWr[11] + 4 * E45;
        self.m_OutputWr[19] = self.m_OutputWr[10] + 4 * E45;

        # double ex, ey;
        # //calculation of coordinate of point 'E'
        dblXE = 2 * r + ( self.m_OutboundTime + 15) * dblv + ( self.m_OutboundTime + 26 + 195 / R ) * self.m_OutputWr[0];
        # //-(self.m_dblTime + 21) * self.m_dblIAS * cos((double)5 / 360 * 2 * Math.PI)
        # //+11 * self.m_dblIAS - radius - W[15];

        ex = (self.m_OutboundTime + 21) * dblv * math.cos(5 / float(360 * 2) * math.pi)-11 * dblv + r + self.m_OutputWr[15] - dblXE;


        dblYE = 11 * dblv * math.cos( 20 / float(360) * math.pi * 2 ) + r * ( 1 + math.sin(20 / float(360) * math.pi * 2 ) ) + \
             ( self.m_OutboundTime + 15 ) * dblv * math.tan( 5 / float(360) * math.pi * 2 ) + ( self.m_OutboundTime + 26 + 125 / R ) * self.m_OutputWr[0];
        ey = -(self.m_OutboundTime + 21) * dblv * math.sin(5 / float(360) * 2 * math.pi) - self.m_OutputWr[18] + dblYE;

        self.m_OutputXE = dblXE;
        self.m_OutputYE = dblYE;

        self.m_OutputEX = ex;
        self.m_OutputEY = ey;

        self.m_dblIAS = dblv#BaseOperation.ConvertUnit( self.m_mapUnit, self.m_unitSys, cocaUnitType.whatDist, dblv, false );
        MAX_ALLOWABLE_OFFSET = 0.15#BaseOperation.ConvertUnit( self.m_mapUnit, cocaUnitSystem.sysSi, cocaUnitType.whatDist, 0.15, false );
    def CheckDivergences(self):
        dblAltitude = self.m_dblAltitudeInitial - self.m_dblAltitudeNAVA;
        convAltitude = Unit.ConvertFeetToMeter(dblAltitude)#, cocaUnitType.whatHeight, cocaUnitSystem.sysNonsi);

        k = 171233 * math.pow( 288 + self.m_ISAVAR - 0.006496 * convAltitude, 0.5 ) / math.pow( 288 - 0.006496 * convAltitude , 2.628 );

        dblV = self.m_dblIAS * k;
        dblv = dblV / 3600;
        R = 509.26 / dblV#( ( self.m_unitSys == cocaUnitSystem.sysSi )? 943.27 : 509.26 )/ dblV;
        r = dblV / ( 62.83 * R );

        bSuccess = True;

        # double radius, rotAngle;
        radius = Unit.ConvertNMToMeter(r);

        if (self.m_dblInboundTrackBearing > math.pi * 3 / 2):
            rotAngle = 2 * math.pi - self.m_dblInboundTrackBearing + math.pi / 2;
        else:
            rotAngle = math.pi / 2 - self.m_dblInboundTrackBearing;

        if (rotAngle < 0):
            rotAngle += 2 * math.pi;

        
        Cp = MathHelper.distanceBearingPointArcGIS( self.m_ipNAVAIDPos, math.pi / 2 + rotAngle, radius);
        Cp = MathHelper.distanceBearingPointArcGIS( Cp, rotAngle, self.m_dblIAS * self.m_OutboundTime);

        point1 = MathHelper.distanceBearingPointArcGIS( Cp, rotAngle + math.pi / 2, radius);
        point2 = MathHelper.distanceBearingPointArcGIS( Cp, rotAngle - math.pi / 2, radius);

        if ( self.m_iNAVAID % 2 == 1 ):
            al1 = math.fabs(MathHelper.getBearing(point1, self.m_ipDMENAVAIDPos) - rotAngle - math.pi);
            al2 = math.fabs(MathHelper.getBearing(point2, self.m_ipDMENAVAIDPos) - rotAngle - math.pi);
            al1 = math.fabs(al1 * 180 / (math.pi) - 360);
            al2 = math.fabs(al2 * 180 / (math.pi) - 360);


            if (al2 > al1):
                al1 = al2;

            if ( al1 > 23 ):
                warning = "Angle of divergences is {0} degrees.\nThe maximum divergence between the fix, the tracking facility and the DME shall not be more than 23 degrees.\nPlease see Doc 8168 Volume II Figure I-2-2-1".format(str(round(al1, 1)));
                buttonResult = QMessageBox.warning(self, "Conformation", warning + " Do you want to continue?", QMessageBox.Yes | QMessageBox.No);
                bSuccess = buttonResult == QMessageBox.Yes;
                if ( bSuccess ):
                    self.m_nWarning += 1
                    self.m_strWarning[self.m_nWarning] = warning;
        return bSuccess;
    
    def CheckDescentRate(self):
        nItem = self.parametersPanel.cmbAircraftCatgory.SelectedIndex;
        dblTurnAltMin = 0
        dblFinalAltMin = 0
        dblFinalAltMax = 0;
        bSuccess = True;

        if ( nItem <2 ):
            dblTurnAltMin = self.m_dblAltitudeInitial - 804 * self.m_OutboundTime / 60;
            dblFinalAltMin = self.m_dblAltitudeTurn - 655 * self.m_OutboundTime / 60;
            dblFinalAltMax = self.m_dblAltitudeTurn - 394 * self.m_OutboundTime / 60;
        else:
            dblTurnAltMin = self.m_dblAltitudeInitial - 1197 * self.m_OutboundTime / 60;
            dblFinalAltMin = self.m_dblAltitudeTurn - 1000 * self.m_OutboundTime / 60;
            dblFinalAltMax = self.m_dblAltitudeTurn - 590 * self.m_OutboundTime / 60;
        if ( self.m_dblAltitudeTurn < dblTurnAltMin or self.m_dblAltitudeFinal < dblFinalAltMin or self.m_dblAltitudeFinal > dblFinalAltMax):
            buttonResult = QMessageBox.warning(self, "Conformation", "Maximum/minimum descent of your racetrack is not in accordance with PANS OPS. See Doc 8168 v.II Part I-Section 4, Chapter 3, Table I-4-3-1. Do you want to continue?", QMessageBox.Yes | QMessageBox.No);
            bSuccess = buttonResult == QMessageBox.Yes
            if ( bSuccess ):
                self.m_nWarning += 1
                self.m_strWarning[self.m_nWarning] = "Maximum/minimum descent of your racetrack is not in accordance with PANS OPS. See Doc 8168 v.II Part I-Section 4, Chapter 3, Table I-4-3-1";
        return bSuccess;
    def CheckInputValueForInitSpeed(self):
        nItem = self.parametersPanel.cmbAircraftCatgory.SelectedIndex;
        dblSpeedInput = self.parametersPanel.txtIAS.Value.Knots
        dblSpeedMin = 0
        dblSpeedMax = 0;
        for case in switch(nItem):
            if case(0):# // Aircraft Category A
                dblSpeedMin = 90#(m_unitSys == cocaUnitSystem.sysSi? (double)165:(double)90);
                dblSpeedMax = 110#(m_unitSys == cocaUnitSystem.sysSi ? (double)205 : (double)110);
                break;
            elif case(1):# // Aircraft Category B
                dblSpeedMin = 120#(m_unitSys == cocaUnitSystem.sysSi ? (double)220 : (double)120);
                dblSpeedMax = 140#(m_unitSys == cocaUnitSystem.sysSi ? (double)260 : (double)140);
                break;
            elif case(2):# // Aircraft Category C
                dblSpeedMin = 160#(m_unitSys == cocaUnitSystem.sysSi ? (double)295 : (double)160);
                dblSpeedMax = 240#(m_unitSys == cocaUnitSystem.sysSi ? (double)445 : (double)240);
                break;
            elif case(3):# // Aircraft Category D
                dblSpeedMin = 185#(m_unitSys == cocaUnitSystem.sysSi ? (double)345 : (double)185);
                dblSpeedMax = 250#(m_unitSys == cocaUnitSystem.sysSi ? (double)465 : (double)250);
                break;
            elif case(4): #// Aircraft Category E
                dblSpeedMin = 185#(m_unitSys == cocaUnitSystem.sysSi ? (double)345 : (double)185);
                dblSpeedMax = 250#(m_unitSys == cocaUnitSystem.sysSi ? (double)467 : (double)250);
                break;
            else:# // nothing
                dblSpeedMin = 0;
                dblSpeedMax = 0;
                break;
        cMsg1 = "Range of speeds for initial approach is not according to PANS OPS.\n\n";
        cMsg2 = "See Table I-4-1-2. Do you want to use input speed?";
        cMsg = cMsg1 + cMsg2;

        bSuccess = True;
        buttonResult = None;
        if ( (dblSpeedInput < dblSpeedMin) or (dblSpeedInput > dblSpeedMax) ):
            buttonResult = QMessageBox.warning(self, "Conformation", cMsg, QMessageBox.Yes | QMessageBox.No );
            bSuccess = buttonResult == QMessageBox.Yes;
            if ( bSuccess ):
                self.m_nWarning += 1
                self.m_strWarning[self.m_nWarning] = "Range of speeds for initial approach is not according to PANS OPS.See Table I-4-1-2.";
        return bSuccess;

    def textLimitDistance_TextChanged(self):
        self.CalcOutBoundTime();
        self.CalcRelatedVariables();

    def textOutboundTime_TextChanged(self):
        self.CalcRelatedVariables();
    def textISA_TextChanged(self):
        self.CalcRelatedVariables();
        self.CalcOutBoundTime();

    def textNAVAlt_TextChanged(self):
        self.CalcRelatedVariables();
        self.CalcOutBoundTime();

    def textInitialAlt_TextChanged(self):
        self.CalcRelatedVariables();
        self.CalcOutBoundTime();

    def textTurnAlt_TextChanged(self):
        self.CalcRelatedVariables();
        self.CalcOutBoundTime();

    def CalcRelatedVariables(self):
        alti = self.parametersPanel.txtInitialAlt.Value.Feet
        alti -= self.parametersPanel.txtNAVAlt.Value.Feet
        if (alti < 0):
            return;

        isa = self.parametersPanel.txtISA.Value

        aa = Unit.ConvertFeetToMeter(alti);

        k = 171233 * math.pow( 288 + isa - 0.006496 * aa, 0.5 ) / math.pow( 288 - 0.006496 * aa , 2.628 );

        tas = k * self.parametersPanel.txtIAS.Value.Knots;
        if (tas < 0.000001):
            self.parametersPanel.txtTAS.Value = None;
        else:
            self.parametersPanel.txtTAS.Value = Speed(tas)

        outleg = tas * self.parametersPanel.txtOutboundTime.Value / 3600;

        if (outleg < 0.000001):
            self.parametersPanel.txtOutboundLeg.Value = None
        else:
            self.parametersPanel.txtOutboundLeg.Value = Distance(outleg, DistanceUnits.NM);

    def comboDirection_SelectedIndexChanged(self):
        self.CalcOutBoundTime();
    def comboCategory_SelectedIndexChanged(self):
        buff = 0;
        nItem = self.parametersPanel.cmbAircraftCatgory.SelectedIndex;
        for case in switch(nItem):
            if case(0):# // Aircraft Category A
                buff = 110#(m_unitSys==cocaUnitSystem.sysSi? "205":"110");
                break;
            elif case(1):# // Aircraft Category B
                buff = 140#(m_unitSys==cocaUnitSystem.sysSi? "260":"140"); break;
                break;
            elif case(2):# // Aircraft Category C
                buff = 240#(m_unitSys==cocaUnitSystem.sysSi? "445":"240"); break;
                break;
            elif case(3): #// Aircraft Category D
                buff = 250#(m_unitSys==cocaUnitSystem.sysSi? "465":"250"); break;
                break;
            elif case(4): #// Aircraft Category E
                buff = 250#(m_unitSys==cocaUnitSystem.sysSi? "467":"250"); break;
                break;
            else: #// nothing
                buff = 0;
                break;
        self.parametersPanel.txtIAS.Value = Speed(buff);

    def comboCondition_SelectedIndexChanged(self):
        self.m_iCondition = self.parametersPanel.cmbCondition.SelectedIndex;
    
    def comboNAVAID_SelectedIndexChanged(self):
        nCurrSel = self.parametersPanel.cmbNavAidType.SelectedIndex;
        if (nCurrSel == 1 or nCurrSel == 3):
            self.parametersPanel.pnlDmePos.Enabled = True;
            self.parametersPanel.txtLimitDistance.Enabled = True;
            self.parametersPanel.txtOutboundTime.Enabled = False;
        else:
            self.parametersPanel.pnlDmePos.Enabled = False;
            self.parametersPanel.txtLimitDistance.Enabled = False;
            self.parametersPanel.txtOutboundTime.Enabled = True;
    def GetUserParameters(self, showMessage):
        resb = True;
        buff = "";
        nCurSel = self.parametersPanel.cmbNavAidType.SelectedIndex;
        if (nCurSel >= 0):
            self.m_iNAVAID = nCurSel;
        else:
            if ( showMessage and self.m_iRaceTrackStyle == 1 ):
                QMessageBox.warning(self, "Warning", "Please, select or input value of NAVAID!");
            if (self.m_iRaceTrackStyle == 1):
                if ( showMessage):
                    return False;
                resb = False;
        self.m_dblInboundTrackBearing = math.pi / 2 - Unit.ConvertDegToRad(self.parametersPanel.txtBearing.Value);
        if self.parametersPanel.pnlNavAidPos.IsValid():
            self.m_ipNAVAIDPos = self.parametersPanel.pnlNavAidPos.Point3d
        else:
            QMessageBox.warning(self, "Warning", "NAVAID Position is not valid.")
            return False

        if( self.m_iNAVAID == 1 or self.m_iNAVAID == 3) :
            if self.parametersPanel.pnlDmePos.IsValid():
                self.m_ipDMENAVAIDPos = self.parametersPanel.pnlDmePos.Point3d
            else:
                QMessageBox.warning(self, "Warning", "DME Position is not valid.")
                return False
            self.m_dblDMEdistance = self.parametersPanel.txtLimitDistance.Value.NauticalMiles

        nCurSel = self.parametersPanel.cmbDirection.SelectedIndex;
        if (nCurSel >= 0):
           if ( nCurSel == 0 ):
               self.m_iDirection = 1;
           else:
               self.m_iDirection = -1;
        else:
            if (showMessage):
                QMessageBox.warning(self, "Warning", "Please, select or input value of Direction !");
                return False;
            resb = False;

        nCurSel = self.parametersPanel.cmbEntry.SelectedIndex;
        if (nCurSel >= 0):
           if ( nCurSel == 0 ):
               self.m_bOmnidirectional = True;
           else:
               self.m_bOmnidirectional = False;
        else:
            if (showMessage):
                QMessageBox.warning(self, "Warning", "Please, select Entry !");
                return False;
            resb = False;

        nCurSel = self.parametersPanel.cmbCondition.SelectedIndex;
        if (nCurSel >= 0):
           if ( nCurSel == 0 ):
               self.m_iCondition = 0;
           else:
               self.m_iCondition = 1;
        else:
            if (showMessage):
                QMessageBox.warning(self, "Warning", "Please, select Condition !");
                return False;
            resb = False;
        self.m_dblAltitudeNAVA = self.parametersPanel.txtNAVAlt.Value.Feet
        self.m_dblAltitudeInitial = self.parametersPanel.txtInitialAlt.Value.Feet
        self.m_dblAltitudeTurn = self.parametersPanel.txtTurnAlt.Value.Feet
        self.m_dblAltitudeFinal = self.parametersPanel.txtFinalAlt.Value.Feet
        self.m_ISAVAR = self.parametersPanel.txtISA.Value
        self.m_dblIAS = self.parametersPanel.txtIAS.Value.Knots
        bSuccess = True;
        int_time = 0;
        dbl_time = self.parametersPanel.txtOutboundTime.Value
        int_time = int(dbl_time);
        if ( dbl_time > int_time or (int_time%30) != 0 or int_time < 60 or int_time > 180 ):
            if ( showMessage and self.m_iNAVAID % 2 == 0 ):
                buttonResult = QMessageBox.question(self, "Question", "Outbound time of your racetrack is not in accordance with PANS OPS. See Doc 8168 v.II Part I-Section 4, Chapter 3.5.5.\n Do you want to continue?", QMessageBox.Yes | QMessageBox.No)
                bSuccess = buttonResult == QMessageBox.Yes;
                if (bSuccess):
                    self.m_strWarning[0] = "Outbound time of your racetrack is not in accordance with PANS OPS. See Doc 8168 v.II Part I-Section 4, Chapter 3.5.5.";
        self.m_OutboundTime = float(int_time);
        return bSuccess;

    def CalcOutBoundTime(self):
    # //if (!GetUserParameters(false)) return;
        self.GetUserParameters(False);
        if (self.m_iNAVAID == 0 or self.m_iNAVAID == 2):
            return;
        dblAltitude = self.m_dblAltitudeInitial - self.m_dblAltitudeNAVA;
        aa = dblAltitude;
        k = 171233 * math.pow(288 + self.m_ISAVAR - 0.006496 * aa, 0.5) / math.pow(288 - 0.006496 * aa, 2.628);

        dblV = self.m_dblIAS * k;
        dblv = dblV / 3600;
        R = 509.26 / dblV#((self.m_unitSys == cocaUnitSystem.sysSi) ? 943.27 : 509.26) / dblV;
        r = dblV / (62.83 * R);

        r = Unit.ConvertNMToMeter(r)#BaseOperation.ConvertUnit(self.m_mapUnit, self.m_unitSys, cocaUnitType.whatDist, r, false);
        ipRotatePos = MathHelper.distanceBearingPointArcGIS(self.m_ipNAVAIDPos, math.pi - self.m_dblInboundTrackBearing, 2 * r);
        add = 0.25
        d = self.m_dblDMEdistance;
        d = d + (add + d * 0.0125);

        d = Unit.ConvertNMToMeter(d)#BaseOperation.ConvertUnit(self.m_mapUnit, self.m_unitSys, cocaUnitType.whatDist, d, false);
        res = 0
        result, ipIntersect = MathHelper.GetIntersectionPointBetweenLineandArc(ipRotatePos, self.m_dblInboundTrackBearing, self.m_ipDMENAVAIDPos, d)
        if (result):
            d = MathHelper.calcDistance(ipRotatePos, ipIntersect);
            d = Unit.ConvertMeterToNM(d)
            res = d / dblv;
        if (res > 0):
            self.parametersPanel.txtOutboundTime.Value = res;
        else:
            self.parametersPanel.txtOutboundTime.Value = None

    def openData(self):
        FlightPlanBaseDlg.openData(self)
        self.comboNAVAID_SelectedIndexChanged()


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

class RaceTrackAndHoldingObstacles(ObstacleTable):
    def __init__(self, surfacesList, primaryMocList, type, iCondition):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)
        if type == 3:
            self.surfaceType = SurfaceTypes.Holding
            self.primaryMoc = primaryMocList
        elif type == 1:
            self.surfaceType = SurfaceTypes.RaceTrackNavAid
            self.primaryMoc = primaryMocList[0][iCondition]
        else:
            self.surfaceType = SurfaceTypes.RaceTrackFix
            self.primaryMoc = primaryMocList[0][iCondition]

        self.surfacesList = surfacesList

        self.dlgType = type
        self.condition = iCondition
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

        # item = QStandardItem(str(checkResult[4]))
        # item.setData(checkResult[4])
        # self.source.setItem(row, self.IndexSurface, item)

        # item = QStandardItem(str(checkResult[2]))
        # item.setData(checkResult[2])
        # self.source.setItem(row, self.IndexCritical, item)

    def checkObstacle(self, obstacle_0):
        if len(self.surfacesList) == 0:
            return
        area = None
        if self.dlgType != 3:
            if self.surfacesList[0].pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance):
                area = self.surfacesList[0]
            else:
                area = self.surfacesList[1]

            resultValue = []
            mocMultiplier = self.primaryMoc * obstacle_0.MocMultiplier;
            obstacleAreaResult = area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier, resultValue);
            if len(resultValue) == 2:
                num = resultValue[0]
                num1 = resultValue[1]
            else:
                return
            if (obstacleAreaResult != ObstacleAreaResult.Outside):
                position = obstacle_0.Position;
                if num == None:
                    checkResult = [obstacleAreaResult, num1, num];
                    self.addObstacleToModel(obstacle_0, checkResult)
                    return

                # z = position.get_Z() + obstacle_0.Trees + num;
                # criticalObstacleType = CriticalObstacleType.No;
                # if (z > self.enrouteAltitude):
                #     criticalObstacleType = CriticalObstacleType.Yes;
                checkResult = [obstacleAreaResult, num1, num, num + position.get_Z()];
                self.addObstacleToModel(obstacle_0, checkResult)
        else:
            i = -1
            for area in self.surfacesList:
                i += 1
                if not area.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance):
                    continue

                moc = self.primaryMoc[i][self.condition]
                resultValue = []
                mocMultiplier = moc * obstacle_0.MocMultiplier;
                obstacleAreaResult = area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier, resultValue);
                if len(resultValue) == 2:
                    num = resultValue[0]
                    num1 = resultValue[1]
                else:
                    return
                if (obstacleAreaResult != ObstacleAreaResult.Outside):
                    position = obstacle_0.Position;
                    if num == None:
                        checkResult = [obstacleAreaResult, num1, num];
                        self.addObstacleToModel(obstacle_0, checkResult)
                        return
    
                    # z = position.get_Z() + obstacle_0.Trees + num;
                    # criticalObstacleType = CriticalObstacleType.No;
                    # if (z > self.enrouteAltitude):
                    #     criticalObstacleType = CriticalObstacleType.Yes;
                    checkResult = [obstacleAreaResult, num1, num, num + position.get_Z()];
                    self.addObstacleToModel(obstacle_0, checkResult)
                return