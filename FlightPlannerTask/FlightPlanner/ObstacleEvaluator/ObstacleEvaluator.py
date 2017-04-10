# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QObject, Qt, QVariant
from PyQt4.QtGui import QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame,\
    QHBoxLayout, QIcon, QPixmap
from qgis.core import QgsPalLayerSettings, QgsMapLayerRegistry,QgsCoordinateReferenceSystem,QgsPoint, QGis, \
    QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, \
    QgsVectorFileWriter, QgsSymbolV2, QgsRendererCategoryV2
from qgis.gui import QgsMapTool, QgsMapToolPan
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CloseInObstacleType, Point3D,ObstacleType, CriticalObstacleType, ObstacleTableColumnType, ObstacleEvaluationMode, ProtectionAreaType, SurfaceTypes, DistanceUnits,AircraftSpeedCategory, OrientationType, AltitudeUnits, ObstacleAreaResult
from FlightPlanner.ObstacleEvaluator.ui_ObstacleEvaluator import Ui_ObstacleEvaluator
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.ProtectionAreaPanel import ProtectionAreaPanel
from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Prompts import Prompts
from FlightPlanner.Captions import Captions
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.Obstacle.Obstacle import Obstacle
from FlightPlanner.DataHelper import DataHelper
from Type.Geometry import Feature
from FlightPlanner.messages import Messages
from FlightPlanner.GeometryCreate.LineCreate import LineCreateTool
from FlightPlanner.Obstacle.ObstacleAreaJig import ObstacleAreaJigSelectArea, ObstacleAreaJigCreateArea
from FlightPlanner.AcadHelper import AcadHelper
import define, math

class ObstacleEvaluatorDlg(FlightPlanBaseDlg):
    list = [];

    resultObs2 = None;

    resultObs1 = None;

    resultDelta = None;

    resultFactor = None;

    resultMoc = None;
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("ObstacleEvaluatorDlg")
        self.surfaceType = SurfaceTypes.ObstacleEvaluator
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.ObstacleEvaluator)
        self.resize(600, 650)
        QgisHelper.matchingDialogSize(self, 750, 650)
        self.surfaceList = None
        

        test = dict(asd="sad", d = "det")
        test.update({"dd":"sdf"})
        s = test.items()[0][0]


        # layer = AcadHelper.createVectorLayer("test")
        # layer.startEditing()
        # feature = Feature(QgsGeometry.fromPolyline([Point3D(666666, 6666666), Point3D(677777, 6777777)]))
        # feature.setAttributes({'Caption':"sdfasfa"})
        # # feature.setGeometry()
        # # feature.setAttribute(0, "sadadsd")
        # layer.addFeature(feature)
        # layer.commitChanges()
        # QgisHelper.appendToCanvas(define._canvas, [layer], "test")
    def initObstaclesModel(self):

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
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.ObstacleEvaluator +" (" + self.surfaceType + ")", self.ui.tblObstacles , None, parameterList, resultHideColumnNames)
#         self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
    
    def getParameterList(self):
        if self.parametersPanel.tabCtrlGeneral.currentIndex() == 0:
            return self.SMC_getParameterList()
        elif self.parametersPanel.tabCtrlGeneral.currentIndex() == 1:
            return self.TAOA_getParameterList()

        elif self.parametersPanel.tabCtrlGeneral.currentIndex() == 2:
            return self.SDOA_getParameterList()
        elif self.parametersPanel.tabCtrlGeneral.currentIndex() == 3:
            return self.IMAOA_getParameterList()
        else:
            return self.MTA_getParameterList()
    def MTA_getParameterList(self):
        parameterList = []

        # parameterList.append(("Parameters", "group"))
        # parameterList.append(("Protection Area", self.parametersPanel.pnlProtectionAreaIMAOA.comboBox.currentText()))
        # parameterList.append(("X [Latest MAPt -&gt; SOC]l", self.parametersPanel.txtX.text() + "m"))
        # parameterList.append(("Nominal Tracke", self.parametersPanel.txtNominalTrackIMAOA.Value))
        # # parameterList.append(("Slope", self.parametersPanel.txtSlope.text() + "%"))
        #
        # parameterList.append(("Final Approach MOC", self.parametersPanel.txtFinalMOC.text() + "m"))
        # parameterList.append(("", self.parametersPanel.txtFinalMOCFt.text() + "ft"))
        #
        # parameterList.append(("Missed Approach MOC", self.parametersPanel.txtMissedMOC.text() + "m"))
        # parameterList.append(("", self.parametersPanel.txtMissedMOCFt.text() + "ft"))
        #
        # parameterList.append(("Missed Approach Climb Gradient", self.parametersPanel.txtGradient.text() + "%"))
        # parameterList.append(("Multiple Areas", str(self.parametersPanel.chbMultipleAreasIMAOA.isChecked())))
        #
        # parameterList.append(("MOCmultiplier", str(self.parametersPanel.mocSpinBoxIMAOA.value())))
        #
        # parameterList.append(("Results / Checked Obstacles", "group"))
        # parameterList.append(("Checked Obstacles", "group"))
        # c = self.obstaclesModel.rowCount()
        # parameterList.append(("Number of Checked Obstacles", str(c)))
        return parameterList
    def IMAOA_getParameterList(self):
        parameterList = []
        # parameterList.append(("general", "group"))
        parameterList.append(("Start of Climb (SOC)", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlSOCIMAOA.txtPointX.text()), float(self.parametersPanel.pnlSOCIMAOA.txtPointY.text()))

        parameterList.append(("Lat", self.parametersPanel.pnlSOCIMAOA.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlSOCIMAOA.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlSOCIMAOA.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlSOCIMAOA.txtPointY.text()))
        # parameterList.append(("ATT", self.parametersPanel.pnlTolerances.txtAtt.text() + "nm"))
        # parameterList.append(("XTT", self.parametersPanel.pnlTolerances.txtXtt.text() + "nm"))

        parameterList.append(("Parameters", "group"))
        parameterList.append(("Protection Area", self.parametersPanel.pnlProtectionAreaIMAOA.comboBox.currentText()))
        parameterList.append(("X [Latest MAPt -&gt; SOC]l", self.parametersPanel.txtX.text() + "m"))

        parameterList.append(("Nominal Track", "Plan : " + str(self.parametersPanel.txtNominalTrackIMAOA.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtNominalTrackIMAOA.txtRadialGeodetic.Value) + define._degreeStr))

        # parameterList.append(("Nominal Tracke", self.parametersPanel.txtNominalTrackIMAOA.Value))
        # parameterList.append(("Slope", self.parametersPanel.txtSlope.text() + "%"))

        parameterList.append(("Final Approach MOC", self.parametersPanel.txtFinalMOC.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtFinalMOCFt.text() + "ft"))

        parameterList.append(("Missed Approach MOC", self.parametersPanel.txtMissedMOC.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtMissedMOCFt.text() + "ft"))

        parameterList.append(("Missed Approach Climb Gradient", self.parametersPanel.txtGradient.text() + "%"))
        parameterList.append(("Multiple Areas", str(self.parametersPanel.chbMultipleAreasIMAOA.isChecked())))

        parameterList.append(("MOCmultiplier", str(self.parametersPanel.mocSpinBoxIMAOA.value())))

        parameterList.append(("Results / Checked Obstacles", "group"))
        parameterList.append(("Checked Obstacles", "group"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        return parameterList
    def SDOA_getParameterList(self):
        parameterList = []
        # parameterList.append(("general", "group"))
        parameterList.append(("Earliest Fix Position", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlFix.txtPointX.text()), float(self.parametersPanel.pnlFix.txtPointY.text()))

        parameterList.append(("Lat", self.parametersPanel.pnlFix.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlFix.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlFix.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlFix.txtPointY.text()))
        # parameterList.append(("ATT", self.parametersPanel.pnlTolerances.txtAtt.text() + "nm"))
        # parameterList.append(("XTT", self.parametersPanel.pnlTolerances.txtXtt.text() + "nm"))

        parameterList.append(("Parameters", "group"))
        parameterList.append(("Protection Area", self.parametersPanel.pnlProtectionAreaSDOA.comboBox.currentText()))

        parameterList.append(("Nominal Track", "Plan : " + str(self.parametersPanel.txtNominalTrackSDOA.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtNominalTrackSDOA.txtRadialGeodetic.Value) + define._degreeStr))

        # parameterList.append(("Nominal Tracke", self.parametersPanel.txtNominalTrackSDOA.Value))
        parameterList.append(("Slope", self.parametersPanel.txtSlope.text() + "%"))

        parameterList.append(("Preceding Segment OCA", self.parametersPanel.txtPrevOCAM.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtPrevOCA.text() + "ft"))

        parameterList.append(("Preceding Segment MOC", self.parametersPanel.txtPrevMOC.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtPrevMOCFt.text() + "ft"))

        parameterList.append(("Subsequent Segment MOC", self.parametersPanel.txtNextMOC.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtNextMOCFt.text() + "ft"))

        parameterList.append(("Multiple Areas", str(self.parametersPanel.chbMultipleAreasSDOA.isChecked())))
        parameterList.append(("MOCmultiplier", str(self.parametersPanel.mocSpinBoxSDOA.value())))

        parameterList.append(("Results / Checked Obstacles", "group"))
        parameterList.append(("Checked Obstacles", "group"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        return parameterList
    def SMC_getParameterList(self):
        parameterList = []
        # parameterList.append(("general", "group"))
        # parameterList.append(("Waypoint", "group"))
        # longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlWaypoint.txtPointX.text()), float(self.parametersPanel.pnlWaypoint.txtPointY.text()))
        
        # parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
        # parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
        # parameterList.append(("X", self.parametersPanel.pnlWaypoint.txtPointX.text()))
        # parameterList.append(("Y", self.parametersPanel.pnlWaypoint.txtPointY.text()))
        # parameterList.append(("ATT", self.parametersPanel.pnlTolerances.txtAtt.text() + "nm"))
        # parameterList.append(("XTT", self.parametersPanel.pnlTolerances.txtXtt.text() + "nm"))
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Protection Area", self.parametersPanel.pnlProtectionAreaSMC.comboBox.currentText()))
        parameterList.append(("Evaluation Mode", self.parametersPanel.cmbEvaluationMode.currentText()))

        if self.parametersPanel.cmbEvaluationMode.currentIndex() == 0:
            parameterList.append(("Position", "group"))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlPosition.txtPointX.text()), float(self.parametersPanel.pnlPosition.txtPointY.text()))

            parameterList.append(("Lat", self.parametersPanel.pnlPosition.txtLat.Value))
            parameterList.append(("Lon", self.parametersPanel.pnlPosition.txtLong.Value))
            parameterList.append(("X", self.parametersPanel.pnlPosition.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlPosition.txtPointY.text()))
        parameterList.append(("Primary MOC", self.parametersPanel.txtPrimaryMOC.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtPrimaryMOCFt.text() + "ft"))

        if self.parametersPanel.frameInsertPointAndText.isVisible():
            parameterList.append(("Insert Point And Text", str(self.parametersPanel.chbInsertPointAndText.isChecked())))
            parameterList.append(("Text Height", self.parametersPanel.txtTextHeight.text()))
        if self.parametersPanel.framePerpendicularToSMC.isVisible():
            parameterList.append(("Perpendicular To", str(self.parametersPanel.chbPerpendicularToSMC.isChecked())))
            parameterList.append(("Nominal Trackl()", self.parametersPanel.txtNominalTrackSMC.Value))
        parameterList.append(("Multiple Areas", str(self.parametersPanel.chbMultipleAreasSMC.isChecked())))
        parameterList.append(("MOCmultiplier", str(self.parametersPanel.mocSpinBoxSMC.value())))

        parameterList.append(("Results / Checked Obstacles", "group"))   
        parameterList.append(("Checked Obstacles", "group"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        return parameterList

    def TAOA_getParameterList(self):
        parameterList = []
        # parameterList.append(("general", "group"))
        # parameterList.append(("Waypoint", "group"))
        # longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlWaypoint.txtPointX.text()), float(self.parametersPanel.pnlWaypoint.txtPointY.text()))

        # parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
        # parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
        # parameterList.append(("X", self.parametersPanel.pnlWaypoint.txtPointX.text()))
        # parameterList.append(("Y", self.parametersPanel.pnlWaypoint.txtPointY.text()))
        # parameterList.append(("ATT", self.parametersPanel.pnlTolerances.txtAtt.text() + "nm"))
        # parameterList.append(("XTT", self.parametersPanel.pnlTolerances.txtXtt.text() + "nm"))

        parameterList.append(("Parameters", "group"))
        parameterList.append(("Used For", self.parametersPanel.cmbUsedFor.currentText()))
        if self.parametersPanel.cmbUsedFor.currentIndex() == 0:
            parameterList.append(("DER Position", "group"))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlDER.txtPointX.text()), float(self.parametersPanel.pnlDER.txtPointY.text()))

            parameterList.append(("Lat", self.parametersPanel.pnlDER.txtLat.Value))
            parameterList.append(("Lon", self.parametersPanel.pnlDER.txtLong.Value))
            parameterList.append(("X", self.parametersPanel.pnlDER.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlDER.txtPointY.text()))
        else:
            parameterList.append(("SOC Position", "group"))
            longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlSOC.txtPointX.text()), float(self.parametersPanel.pnlSOC.txtPointY.text()))

            parameterList.append(("Lat", self.parametersPanel.pnlSOC.txtLat.Value))
            parameterList.append(("Lon", self.parametersPanel.pnlSOC.txtLong.Value))
            parameterList.append(("X", self.parametersPanel.pnlSOC.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanel.pnlSOC.txtPointY.text()))

        parameterList.append(("Portion", self.parametersPanel.cmbPortion.currentText()))
        parameterList.append(("Protection Area", self.parametersPanel.pnlProtectionAreaTAOA.comboBox.currentText()))
        parameterList.append(("Track", self.parametersPanel.txtTrack.Value))

        if self.parametersPanel.frameStartingMOC.isVisible():
            parameterList.append(("Initial MOC Value", self.parametersPanel.txtStartingMOC.text() + "m"))
            parameterList.append(("", self.parametersPanel.txtStartingMOCFt.text() + "ft"))
        if self.parametersPanel.frameDepMocS.isVisible():
            parameterList.append(("MOC", self.parametersPanel.txtDepMocS.text() + "%"))
        if self.parametersPanel.frameDepMocT.isVisible():
            parameterList.append(("MOC", "group"))
            parameterList.append(("Greater of", self.parametersPanel.txtDepMocT1.text() + "m"))
            parameterList.append(("or", self.parametersPanel.txtDepMocT2.text() + "%"))
        if self.parametersPanel.frameMaMocS.isVisible():
            parameterList.append(("MOC", self.parametersPanel.txtMaMocS.text() + "m"))
            parameterList.append(("", self.parametersPanel.txtMaMocSFt.text() + "ft"))
        if self.parametersPanel.frameMaMocT.isVisible():
            parameterList.append(("MOC", self.parametersPanel.txtMaMocT.text() + "m"))
            parameterList.append(("", self.parametersPanel.txtMaMocTFt.text() + "ft"))
        if self.parametersPanel.framePDG.isVisible():
            parameterList.append(("PDG", self.parametersPanel.txtPDG.text() + "%"))
        if self.parametersPanel.frameMACG.isVisible():
            parameterList.append(("MACG", self.parametersPanel.txtMACG.text() + "%"))
        if self.parametersPanel.frameTurningAltitude.isVisible():
            parameterList.append(("Turning Altitude", self.parametersPanel.txtTurningAltitudeM.text() + "m"))
            parameterList.append(("", self.parametersPanel.txtTurningAltitude.text() + "ft"))
        if self.parametersPanel.frameSecondTurn.isVisible():
            parameterList.append(("Second Turn", str(self.parametersPanel.chbSecondTurn.isChecked())))
            parameterList.append((self.parametersPanel.label_NominalTrack_2.text(), self.parametersPanel.txtDistToEtp.text() + "m"))
        if self.parametersPanel.framePerpendicularToTAOA.isVisible():
            parameterList.append(("Perpendicular To", str(self.parametersPanel.chbPerpendicularToTAOA.isChecked())))
            parameterList.append(("Nominal Track", "Plan : " + str(self.parametersPanel.txtNominalTrackTAOA.txtRadialPlan.Value) + define._degreeStr))
            parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtNominalTrackTAOA.txtRadialGeodetic.Value) + define._degreeStr))

            # parameterList.append(("Nominal Track", self.parametersPanel.txtNominalTrackTAOA.Value))
        parameterList.append((self.parametersPanel.chbStoreDistances.text(), str(self.parametersPanel.chbStoreDistances.isChecked())))
        parameterList.append(("Multiple Areas", str(self.parametersPanel.chbMultipleAreasTAOA.isChecked())))
        parameterList.append(("MOCmultiplier:", str(self.parametersPanel.mocSpinBoxTAOA.value())))


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
        self.ui.btnConstruct.setVisible(False)
        self.ui.btnEvaluate.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)




        
#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)
    
        
    def btnConstruct_Click(self):
        self.TAOA_PDG_Evaluate()

    def btnEvaluate_Click(self):
        if self.parametersPanel.tabCtrlGeneral.currentIndex() == 0:
            self.SMC_Evaluate()
        elif self.parametersPanel.tabCtrlGeneral.currentIndex() == 1:
            self.TAOA_MACG_Evaluate()

        elif self.parametersPanel.tabCtrlGeneral.currentIndex() == 2:
            self.SDOA_Evaluate()
            return FlightPlanBaseDlg.btnEvaluate_Click(self)
        elif self.parametersPanel.tabCtrlGeneral.currentIndex() == 3:
            self.IMAOA_Evaluate()
            return FlightPlanBaseDlg.btnEvaluate_Click(self)
        else:
            self.MTA_Evaluate()


    def MTA_Evaluate(self):
        self.method_28_MTA()
        if QMessageBox.question(self, "Question", "Please click \"Yes\" if you want to create new area.\nPlease click \"No\" if you want to select any area.", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            # if self.comboBox.currentIndex() == ProtectionAreaType.Primary:
            obstacleAreaJig= ObstacleAreaJigCreateArea(define._canvas, 0)
            define._canvas.setMapTool(obstacleAreaJig)
            self.connect(obstacleAreaJig, SIGNAL("outputResult"), self.AreaResult)
            # elif self.comboBox.currentIndex() == ProtectionAreaType.Secondary:
        else:
            obstacleAreaJig= ObstacleAreaJigSelectArea(define._canvas, 0)
            define._canvas.setMapTool(obstacleAreaJig)
            self.connect(obstacleAreaJig, SIGNAL("outputResult"), self.AreaResult)
    def AreaResult(self, resultArea, resultRubberBand):
        self.primaryObstacleAreaMTA = resultArea
        QgisHelper.ClearRubberBandInCanvas(define._canvas)

        oonstructionLayer = AcadHelper.createVectorLayer("PrimaryArea_MTA");
        AcadHelper.setGeometryAndAttributesInLayer(oonstructionLayer, self.primaryObstacleAreaMTA.PreviewArea, True)

        QgisHelper.appendToCanvas(define._canvas, [oonstructionLayer], SurfaceTypes.MountainousTerrainAnalyser)
        
        self.obstaclesModel = MountainousTerrainAnalyserObstacles(self.primaryObstacleAreaMTA)
        self.surfaceType = SurfaceTypes.MountainousTerrainAnalyser
        FlightPlanBaseDlg.btnEvaluate_Click(self)
        self.ui.tabCtrlGeneral.setCurrentIndex(0)
        if len(ObstacleEvaluatorDlg.list) <= 0:
            return
        
        if (self.method_33_MTA()):
            self.method_29_MTA();
            # base.method_18(string.Format(Messages.X_POSITIONS_SUCCESSFULLY_ANALYSED, obstacleSelector.ObstaclesChecked));
        else:
            return;
        ObstacleEvaluatorDlg.list = []
    def SMC_Evaluate(self):
        self.surfaceType = SurfaceTypes.SecondaryMoc
        num = MathHelper.smethod_4(Unit.ConvertDegToRad(float(self.parametersPanel.txtNominalTrackSMC.Value))) if(self.parametersPanel.chbPerpendicularToSMC.isChecked()) else None;
        selectedArea = self.parametersPanel.pnlProtectionAreaSMC.SelectedArea;
        selectedArea.nominalTrack = num;

        self.obstaclesModel = SecMocObstacles(selectedArea, float(self.parametersPanel.txtPrimaryMOC.text()))
        self.obstaclesModel.MocMultiplier = self.parametersPanel.mocSpinBoxSMC.value()
        if (self.parametersPanel.cmbEvaluationMode.currentIndex() != 0):

            return FlightPlanBaseDlg.btnEvaluate_Click(self)

        else:
            point3d = None
            try:
                point3d = self.parametersPanel.pnlPosition.Point3d;
            except UserWarning:
                QMessageBox.warning(self, "Waring", UserWarning.message)
                return
            d = self.parametersPanel.pnlPosition.ID;

            if (d == None):
                d = Captions.UNKNOWN;
            num1 = define._trees
            num2 = define._tolerance

            pointLayer = None;
            mapUnits = define._canvas.mapUnits()
            if define._mapCrs == None:
                if mapUnits == QGis.Meters:
                    pointLayer = QgsVectorLayer("point?crs=EPSG:32633", "SinglePointLayer", "memory")
                else:
                    pointLayer = QgsVectorLayer("point?crs=EPSG:4326", "SinglePointLayer", "memory")
            else:
                pointLayer = QgsVectorLayer("point?crs=%s"%define._mapCrs.authid (), "SinglePointLayer", "memory")
            shpPath = ""
            if define.obstaclePath != None:
                shpPath = define.obstaclePath
            elif define.xmlPath != None:
                shpPath = define.xmlPath
            else:
                shpPath = define.appPath
            er = QgsVectorFileWriter.writeAsVectorFormat(pointLayer, shpPath + "/" + "SinglePointLayer" + ".shp", "utf-8", pointLayer.crs())
            pointLayer = QgsVectorLayer(shpPath + "/" + "SinglePointLayer" + ".shp", "SinglePointLayer", "ogr")

            pointLayer.startEditing()
            fieldName = "Caption"
            pointLayer.dataProvider().addAttributes( [QgsField(fieldName, QVariant.String)] )
            pointLayer.commitChanges()
            QgisHelper.appendToCanvas(define._canvas, [pointLayer], self.surfaceType)
        #     double num1 = Trees.smethod_1(point3d.get_Z());
        #     double num2 = MountainousTerrain.smethod_1(point3d, num1);
            position = Point3D()
            positionDegree = Point3D()
            point = QgsPoint(point3d.get_X(), point3d.get_Y())
            obstacleLayers = QgisHelper.getSurfaceLayers(SurfaceTypes.Obstacles)
            obstacleLayer = obstacleLayers[0]
            position = Point3D(point.x(), point.y())
#                         if obstacleUnits != define._units:
#                             positionDegree = QgisHelper.Meter2DegreePoint3D(position)

            positionDegree = QgisHelper.CrsTransformPoint(point.x(), point.y(), define._canvas.mapSettings().destinationCrs(),obstacleLayer.crs(), point3d.get_Z())


            obstacle = Obstacle(d, point3d, pointLayer.id(), 0, None, num1, ObstacleTable.MocMultiplier, num2);
            obstacle.positionDegree = positionDegree
            string0 = self.obstaclesModel.method_0(obstacle, "")
            self.obstaclesModel.setLocateBtn(self.ui.btnLocate)
            self.ui.tblObstacles.setModel(self.obstaclesModel)
            self.obstaclesModel.setTableView(self.ui.tblObstacles)
            self.obstaclesModel.setHiddenColumns(self.ui.tblObstacles)
            self.ui.tabCtrlGeneral.setCurrentIndex(1)
            c = self.obstaclesModel.rowCount()
            if c > 0:
                self.ui.btnExportResult.setEnabled(True)
            if (self.parametersPanel.chbInsertPointAndText.isChecked() and string0 != None):
                pointLayer.startEditing()
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPoint(point3d))
                feature.setAttributes([string0])
                pr = pointLayer.dataProvider()
                pr.addFeatures([feature])
                # pointLayer.addFeature(feature)
                pointLayer.commitChanges()

                fontSize = self.parametersPanel.txtTextHeight.text()

                palSetting = QgsPalLayerSettings()
                palSetting.readFromLayer(pointLayer)
                palSetting.enabled = True
                palSetting.fieldName = "Caption"
                palSetting.isExpression = True
                palSetting.placement = QgsPalLayerSettings.Line
                palSetting.placementFlags = QgsPalLayerSettings.AboveLine
                # palSetting.Rotation = Unit.ConvertRadToDeg(7.85398163397448 - num)
                palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '%s'%(fontSize), "")
                palSetting.writeToLayer(pointLayer)

                define._messageLabel.setText(Messages.POINT_TEXT_INSERTED);
                return;
        #
        #

    def TAOA_MACG_Evaluate(self):
        self.surfaceType = SurfaceTypes.TurnAreaObstacleAnalyser
        point3d = self.parametersPanel.pnlSOC.Point3d;
        num = MathHelper.smethod_4(Unit.ConvertDegToRad(float(self.parametersPanel.txtNominalTrackTAOA.Value))) if(self.parametersPanel.chbPerpendicularToTAOA.isChecked ()) else None;
        self.selectedArea = self.parametersPanel.pnlProtectionAreaTAOA.SelectedArea
        self.selectedArea.nominalTrack = num;
        turnAreaMaStraightEvaluator = None;
        self.point0 = point3d
        if (self.parametersPanel.cmbPortion.currentIndex() == 0):
            value = float(self.parametersPanel.txtTrack.Value);
            metres = float(self.parametersPanel.txtMaMocS.text());
            angleGradientSlope = float(self.parametersPanel.txtMACG.text());
            self.obstaclesModel = TurnAreaObstaclesMA(("TurnAreaMaStraightEvaluator", [self.selectedArea, point3d, value, metres, angleGradientSlope, None, self.parametersPanel.chbStoreDistances.isChecked()]));
        elif (self.parametersPanel.cmbPortion.currentIndex() == 1):
            metres1 = None;
            if (self.parametersPanel.chbSecondTurn.isChecked()):
                metres1 = float(self.parametersPanel.txtDistToEtp.text());
                point3d = self.parametersPanel.pnlETP.Point3d.smethod_167(point3d.get_Z());
            value1 = float(self.parametersPanel.txtTrack.Value);
            num1 = float(self.parametersPanel.txtMaMocT.text());
            angleGradientSlope1 = float(self.parametersPanel.txtMACG.text());
            self.obstaclesModel = TurnAreaObstaclesMA(("TurnAreaMaStraightEvaluator", [self.selectedArea, point3d, value1, num1, angleGradientSlope1, metres1, self.parametersPanel.chbStoreDistances.isChecked()]));
        elif (self.parametersPanel.cmbPortion.currentIndex() != 2):
            QgisHelper.ClearRubberBandInCanvas(define._canvas)
            selectTool = AcadHelper.smethod_102(Prompts.SELECT_ALTITUDE_BOUNDARY_LINE, None, None, self);
            QObject.connect(selectTool, SIGNAL("AcadHelper_Smethod_102_Event"), self.resultLineCreateMACG)
            # self.proceedClicked = True
            define._canvas.setToolTip(Prompts.SELECT_ALTITUDE_BOUNDARY_LINE)
            # self.hide()
            # lineCreateTool = LineCreateTool(define._canvas)
            # define._canvas.setMapTool(lineCreateTool)
            # self.connect(lineCreateTool, SIGNAL("resultLineCreate"), self.resultLineCreateMACG)
            return

        else:
            num2 = None;
            if (self.parametersPanel.chbSecondTurn.isChecked()):
                num2 = float(self.parametersPanel.txtDistToEtp.text());
                point3d = self.parametersPanel.pnlETP.Point3d.smethod_167(point3d.get_Z());
            point3d1 = self.parametersPanel.pnlETP.Point3d;
            value3 = float(self.parametersPanel.txtTrack.Value);
            metres3 = float(self.parametersPanel.txtMaMocT.text());
            angleGradientSlope3 = float(self.parametersPanel.txtMACG.text());
            self.obstaclesModel = TurnAreaObstaclesMA(("TurnAreaMaTurnEvaluator", [self.selectedArea, point3d, point3d1, value3, metres3, angleGradientSlope3, num2, self.parametersPanel.chbStoreDistances.isChecked()]));
        self.obstaclesModel.MocMultiplier = self.parametersPanel.mocSpinBoxTAOA.value()
        FlightPlanBaseDlg.btnEvaluate_Click(self)
        # if self.parametersPanel.chbStoreDistances.isChecked():
        #     self.obstaclesModel.tblObstacles.setColumnWidth(self.obstaclesModel.IndexTag, 500)

    def resultLineCreateMACG(self, geom):
        pointArray = geom.asPolyline()
        startPoint = Point3D(pointArray[0].x(), pointArray[0].y())
        endPoint = Point3D(pointArray[len(pointArray) - 1].x(), pointArray[len(pointArray) - 1].y())

        value2 = float(self.parametersPanel.txtTrack.Value);
        metres2 = float(self.parametersPanel.txtMaMocT.text());
        angleGradientSlope2 = float(self.parametersPanel.txtMACG.text());
        self.obstaclesModel = TurnAreaObstaclesMA(("TurnAreaMATurnAtAltitudeEvaluator", [self.selectedArea, self.point0, value2, metres2, angleGradientSlope2, Altitude(float(self.parametersPanel.txtTurningAltitudeM.text())), startPoint, endPoint, self.parametersPanel.chbStoreDistances.isChecked()]));
        self.obstaclesModel.MocMultiplier = self.parametersPanel.mocSpinBoxTAOA.value()
        return FlightPlanBaseDlg.btnEvaluate_Click(self)
    def TAOA_PDG_Evaluate(self):
        self.surfaceType = SurfaceTypes.TurnAreaObstacleAnalyser
        point3d = self.parametersPanel.pnlDER.Point3d;
        num = MathHelper.smethod_4(Unit.ConvertDegToRad(float(self.parametersPanel.txtNominalTrackTAOA.Value))) if(self.parametersPanel.chbPerpendicularToTAOA.isChecked()) else None;
        self.selectedArea = self.parametersPanel.pnlProtectionAreaTAOA.SelectedArea;
        self.selectedArea.nominalTrack = num;
        self.area0 = self.selectedArea
        self.point0 = point3d
        turnAreaDepStraightEvaluator = None;
        if (self.parametersPanel.cmbPortion.currentIndex() == 0):
            num1 = Altitude(float(self.parametersPanel.txtStartingMOC.text())).Metres if(Altitude(float(self.parametersPanel.txtStartingMOC.text())).IsValid()) else 0;
            value = float(self.parametersPanel.txtTrack.Value);
            percent = float(self.parametersPanel.txtDepMocS.text()) #.Percent;
            angleGradientSlope = float(self.parametersPanel.txtPDG.text());
            self.obstaclesModel = TurnAreaObstaclesDep(("TurnAreaDepStraightEvaluator", [self.selectedArea, point3d, value, num1, percent, angleGradientSlope, self.parametersPanel.chbStoreDistances.isChecked()]));
        elif (self.parametersPanel.cmbPortion.currentIndex() == 1):
            metres = None;
            if (self.parametersPanel.chbSecondTurn.isChecked()):
                metres = float(self.parametersPanel.txtDistToEtp.text());
                point3d = self.parametersPanel.pnlETP.Point3d.smethod_167(point3d.get_Z());
            num2 = Altitude(float(self.parametersPanel.txtStartingMOC.text())).Metres if(Altitude(float(self.parametersPanel.txtStartingMOC.text())).IsValid()) else 0;
            value1 = float(self.parametersPanel.txtTrack.Value);
            metres1 = float(self.parametersPanel.txtDepMocT1.text());
            percent1 = float(self.parametersPanel.txtDepMocT2.text());
            angleGradientSlope1 = float(self.parametersPanel.txtPDG.text());
            self.obstaclesModel = TurnAreaObstaclesDep(("TurnAreaDepTurnStraightEvaluator", [self.selectedArea, point3d, value1, metres1, num2, percent1, angleGradientSlope1, metres, self.parametersPanel.chbStoreDistances.isChecked()]));
        elif (self.parametersPanel.cmbPortion.currentIndex() != 2):
            QgisHelper.ClearRubberBandInCanvas(define._canvas)
            selectTool = AcadHelper.smethod_102(Prompts.SELECT_ALTITUDE_BOUNDARY_LINE, None, None, self);
            QObject.connect(selectTool, SIGNAL("AcadHelper_Smethod_102_Event"), self.resultLineCreateDEP)
            # self.proceedClicked = True
            define._canvas.setToolTip(Prompts.SELECT_ALTITUDE_BOUNDARY_LINE)
            # self.hide()
            # lineCreateTool = LineCreateTool(define._canvas)
            # define._canvas.setMapTool(lineCreateTool)
            # self.connect(lineCreateTool, SIGNAL("resultLineCreate"), self.resultLineCreateDEP)
            return

        else:
            metres3 = None
            if (self.parametersPanel.chbSecondTurn.isChecked()):
                metres3 = float(self.parametersPanel.txtDistToEtp.text());
                point3d = self.parametersPanel.pnlETP.Point3d.smethod_167(point3d.get_Z());
            num4 = Altitude(float(self.parametersPanel.txtStartingMOC.text())).Metres if(Altitude(float(self.parametersPanel.txtStartingMOC.text())).IsValid()) else 0
            point3d1 = self.parametersPanel.pnlETP.Point3d;
            value3 = float(self.parametersPanel.txtTrack.Value);
            metres4 = float(self.parametersPanel.txtDepMocT1.text());
            percent3 = float(self.parametersPanel.txtDepMocT2.text());
            angleGradientSlope3 = float(self.parametersPanel.txtPDG.text());
            self.obstaclesModel = TurnAreaObstaclesDep(("TurnAreaDepTurnEvaluator", [self.selectedArea, point3d, point3d1, value3, metres4, num4, percent3, angleGradientSlope3, metres3, self.parametersPanel.chbStoreDistances.isChecked()]));
        self.obstaclesModel.MocMultiplier = self.parametersPanel.mocSpinBoxTAOA.value()
        FlightPlanBaseDlg.btnEvaluate_Click(self)
        # if self.parametersPanel.chbStoreDistances.isChecked():
        #     self.obstaclesModel.tblObstacles.setColumnWidth(self.obstaclesModel.IndexTag, 500)

        return
    def resultLineCreateDEP(self, geom):
        define._canvas.setMapTool(QgsMapToolPan(define._canvas))
        num3 = Altitude(float(self.parametersPanel.txtStartingMOC.text())).Metres if(Altitude(float(self.parametersPanel.txtStartingMOC.text())).IsValid()) else 0;
        value2 = float(self.parametersPanel.txtTrack.Value);
        metres2 = float(self.parametersPanel.txtDepMocT1.text());
        percent2 = float(self.parametersPanel.txtDepMocT2.text());
        angleGradientSlope2 = float(self.parametersPanel.txtPDG.text());

        pointArray = geom.asPolyline()
        startPoint = Point3D(pointArray[0].x(), pointArray[0].y())
        endPoint = Point3D(pointArray[len(pointArray) - 1].x(), pointArray[len(pointArray) - 1].y())
        self.obstaclesModel = TurnAreaObstaclesDep(("TurnAreaDepTurnAtAltitudeEvaluator", [self.selectedArea, self.point0, value2, metres2, num3, percent2, angleGradientSlope2, Altitude(float(self.parametersPanel.txtTurningAltitudeM.text())), startPoint, endPoint, self.parametersPanel.chbStoreDistances.isChecked()]));
        self.obstaclesModel.MocMultiplier = self.parametersPanel.mocSpinBoxTAOA.value()
        return FlightPlanBaseDlg.btnEvaluate_Click(self)
    def SDOA_Evaluate(self):
        self.surfaceType = SurfaceTypes.StepDownObstacleAnalyser
        num = MathHelper.smethod_4(Unit.ConvertDegToRad(float(self.parametersPanel.txtNominalTrackSDOA.Value)));
        selectedArea = self.parametersPanel.pnlProtectionAreaSDOA.SelectedArea;
        selectedArea.nominalTrack = num;
        self.obstaclesModel = StepDownObstacles(selectedArea, self.parametersPanel.pnlFix.Point3d, num, float(self.parametersPanel.txtSlope.text()), Altitude(float(self.parametersPanel.txtPrevOCAM.text())), Altitude(float(self.parametersPanel.txtPrevMOC.text())), Altitude(float(self.parametersPanel.txtNextMOC.text())));
        self.obstaclesModel.MocMultiplier = self.parametersPanel.mocSpinBoxSDOA.value()

    def IMAOA_Evaluate(self):
        self.surfaceType = SurfaceTypes.InitialMissedApproachObstacleAnalyser
        num = MathHelper.smethod_4(Unit.ConvertDegToRad(float(self.parametersPanel.txtNominalTrackIMAOA.Value)));
        selectedArea = self.parametersPanel.pnlProtectionAreaIMAOA.SelectedArea;
        selectedArea.nominalTrack = num;
        self.obstaclesModel = InitialMissedApproachObstacles(selectedArea, self.parametersPanel.pnlSOCIMAOA.Point3d, num, Distance(float(self.parametersPanel.txtX.text()), DistanceUnits.M), float(self.parametersPanel.txtGradient.text()), Altitude(float(self.parametersPanel.txtFinalMOC.text())), Altitude(float(self.parametersPanel.txtMissedMOC.text())));
        self.obstaclesModel.MocMultiplier = self.parametersPanel.mocSpinBoxIMAOA.value()
        
    def initParametersPan(self):
        ui = Ui_ObstacleEvaluator()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.pnlProtectionAreaSMC = ProtectionAreaPanel(self.parametersPanel.grbParametersSecondaryMoc, SurfaceTypes.SecondaryMoc)
        ui.vlParametersSecondaryMoc.insertWidget(0, self.parametersPanel.pnlProtectionAreaSMC)
        # self.connect(self.parametersPanel.pnlProtectionAreaSMC, SIGNAL("valueChanged()"), self.method_32_SMC)

        self.parametersPanel.pnlPosition = PositionPanel(self.parametersPanel.grbParametersSecondaryMoc)
        self.parametersPanel.pnlPosition.groupBox.setTitle("Position")
        self.parametersPanel.pnlPosition.btnCalculater.hide()
        self.parametersPanel.pnlPosition.hideframe_Altitude()
        self.parametersPanel.pnlPosition.setObjectName("pnlPosition")
        ui.vlParametersSecondaryMoc.insertWidget(2, self.parametersPanel.pnlPosition)
        self.connect(self.parametersPanel.pnlPosition, SIGNAL("positionChanged"), self.method_32_SMC)

        self.parametersPanel.pnlDER = PositionPanel(self.parametersPanel.grbParametersTurnAreaObstacleAnalyser)
        self.parametersPanel.pnlDER.groupBox.setTitle("DER Position")
        self.parametersPanel.pnlDER.btnCalculater.hide()
        # self.parametersPanel.pnlDER.hideframe_Altitude()
        self.parametersPanel.pnlDER.setObjectName("pnlDER")
        ui.vlParametersTurnAreaObstacleAnalyser.insertWidget(1, self.parametersPanel.pnlDER)

        self.parametersPanel.pnlSOC = PositionPanel(self.parametersPanel.grbParametersTurnAreaObstacleAnalyser)
        self.parametersPanel.pnlSOC.groupBox.setTitle("SOC Position")
        self.parametersPanel.pnlSOC.btnCalculater.hide()
        # self.parametersPanel.pnlSOC.hideframe_Altitude()
        self.parametersPanel.pnlSOC.setObjectName("pnlSOC")
        ui.vlParametersTurnAreaObstacleAnalyser.insertWidget(2, self.parametersPanel.pnlSOC)

        self.parametersPanel.pnlSOCIMAOA = PositionPanel(self.parametersPanel.tab_InitialMissedApproachObstacleAnalyser)
        self.parametersPanel.pnlSOCIMAOA.groupBox.setTitle("Start of Climb (SOC)")
        self.parametersPanel.pnlSOCIMAOA.btnCalculater.hide()
        # self.parametersPanel.pnlSOCIMAOA.hideframe_Altitude()
        self.parametersPanel.pnlSOCIMAOA.setObjectName("pnlSOCIMAOA")
        ui.verticalLayout_4.insertWidget(0, self.parametersPanel.pnlSOCIMAOA)

        self.parametersPanel.pnlFix = PositionPanel(self.parametersPanel.tab_StepDownObstacleAnalyser)
        self.parametersPanel.pnlFix.groupBox.setTitle("Earliest Fix Position")
        self.parametersPanel.pnlFix.btnCalculater.hide()
        self.parametersPanel.pnlFix.hideframe_Altitude()
        self.parametersPanel.pnlFix.setObjectName("pnlFix")
        ui.vLayoutPositionFix.insertWidget(0, self.parametersPanel.pnlFix)

        self.parametersPanel.pnlProtectionAreaTAOA = ProtectionAreaPanel(self.parametersPanel.grbParametersTurnAreaObstacleAnalyser, SurfaceTypes.TurnAreaObstacleAnalyser)
        ui.vlParametersTurnAreaObstacleAnalyser.insertWidget(4, self.parametersPanel.pnlProtectionAreaTAOA)

        self.parametersPanel.pnlETP = PositionPanel(self.parametersPanel.grbParametersTurnAreaObstacleAnalyser)
        self.parametersPanel.pnlETP.groupBox.setTitle("ETP Position")
        self.parametersPanel.pnlETP.btnCalculater.hide()
        self.parametersPanel.pnlETP.hideframe_Altitude()
        self.parametersPanel.pnlETP.setObjectName("pnlETP")
        ui.vlParametersTurnAreaObstacleAnalyser.insertWidget(15, self.parametersPanel.pnlETP)

        self.parametersPanel.pnlProtectionAreaIMAOA = ProtectionAreaPanel(self.parametersPanel.grbParametersInitialMissedApproachObstacleAnalyser, SurfaceTypes.InitialMissedApproachObstacleAnalyser)
        ui.vlParametersStepDownObstacleAnalyser_2.insertWidget(0, self.parametersPanel.pnlProtectionAreaIMAOA)
        # self.parametersPanel.pnlProtectionAreaIMAOA.AllowComplexArea = False;

        self.parametersPanel.pnlProtectionAreaSDOA = ProtectionAreaPanel(self.parametersPanel.grbParametersStepDownObstacleAnalyser, SurfaceTypes.StepDownObstacleAnalyser)
        ui.vlParametersStepDownObstacleAnalyser.insertWidget(0, self.parametersPanel.pnlProtectionAreaSDOA)
        # self.parametersPanel.pnlProtectionAreaSDOA.AllowComplexArea = False;


        self.parametersPanel.cmbEvaluationMode.addItems(["Single", "Multiple"])

        self.parametersPanel.cmbUsedFor.addItems([Captions.DEPARTURE, Captions.MISSED_APPROACH])
        self.parametersPanel.cmbUsedFor.currentIndexChanged.connect(self.method_31_TAOA)

        self.parametersPanel.cmbPortion.addItems([Captions.STRAIGHT, Captions.TURNING_STRAIGHT, Captions.TURNING, Captions.TURN_AT_AN_ALTITUDE])
        self.parametersPanel.cmbPortion.currentIndexChanged.connect(self.method_31_TAOA)

        self.connect(self.parametersPanel.pnlProtectionAreaTAOA, SIGNAL("Event0"), self.method_31_TAOA)
        self.connect(self.parametersPanel.pnlProtectionAreaSMC, SIGNAL("Event0"), self.method_31_SMC)
        self.connect(self.parametersPanel.pnlMOC, SIGNAL("Event_0"), self.method_30_MTA)
        self.connect(self.parametersPanel.pnlElevWithin, SIGNAL("Event_0"), self.method_30_MTA)
        self.connect(self.parametersPanel.pnlElevChange, SIGNAL("Event_0"), self.method_30_MTA)
        self.connect(self.parametersPanel.pnlResultElevChange, SIGNAL("Event_1"), self.method_32_MTA)


        self.parametersPanel.chbSecondTurn.clicked.connect(self.method_31_TAOA)
        self.parametersPanel.chbPerpendicularToTAOA.clicked.connect(self.method_31_TAOA)
        self.parametersPanel.chbSecondTurn.clicked.connect(self.method_31_TAOA)

        self.parametersPanel.tabCtrlGeneral.currentChanged.connect(self.tabCtrlGeneral_CurrentChanged)
#
#         self.parametersPanel.cmbHoldingFunctionality.currentIndexChanged.connect(self.cmbHoldingFunctionalityCurrentIndexChanged)
#         self.parametersPanel.cmbOutboundLimit.currentIndexChanged.connect(self.cmbOutboundLimitCurrentIndexChanged)
#         self.parametersPanel.btnCaptureNominalTrackSMC.clicked.connect(self.captureNominalTrackSMC)
#         self.parametersPanel.btnCaptureTrackSMC.clicked.connect(self.captureTrackSMC)
#         self.parametersPanel.btnCaptureNominalTrackTAOA.clicked.connect(self.captureNominalTrackTAOA)
#         self.parametersPanel.btnCaptureNominalTrackSDOA.clicked.connect(self.captureNominalTrackSDOA)
#         self.parametersPanel.btnCaptureNominalTrackIMAOA.clicked.connect(self.captureNominalTrackIMAOA)
        self.parametersPanel.btnCaptureDistToEtp.clicked.connect(self.captureDistToEtp)
        self.parametersPanel.btnCaptureX.clicked.connect(self.captureX)
        self.parametersPanel.chbInsertPointAndText.clicked.connect(self.method_32_SMC)
        self.parametersPanel.chbPerpendicularToSMC.clicked.connect(self.method_32_SMC)
        self.connect(self.parametersPanel.txtNominalTrackSMC, SIGNAL("Event_0"), self.method_32_SMC)
        self.parametersPanel.txtPrimaryMOC.textChanged.connect(self.method_32_SMC)
        self.parametersPanel.cmbEvaluationMode.currentIndexChanged.connect(self.method_32_SMC)
#         self.parametersPanel.btnIasHelp.clicked.connect(self.iasHelpShow)
#         self.parametersPanel.txtIas.textChanged.connect(self.iasChanged)
#         self.parametersPanel.txtIsa.textChanged.connect(self.isaChanged)
        self.parametersPanel.txtPrimaryMOC.textChanged.connect(self.txtPrimaryMOCMChanged)
        self.parametersPanel.txtPrimaryMOCFt.textChanged.connect(self.txtPrimaryMOCFtChanged)

        self.parametersPanel.chbMultipleAreasIMAOA.setVisible(False)
        self.parametersPanel.chbMultipleAreasSMC.setVisible(False)
        self.parametersPanel.chbMultipleAreasTAOA.setVisible(False)
        self.parametersPanel.chbMultipleAreasSDOA.setVisible(False)

        self.method_32_SMC()
        self.method_31_TAOA()
#
        self.flag = 0
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtPrimaryMOCFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtPrimaryMOC.text())), 4)))
            except:
                self.parametersPanel.txtPrimaryMOCFt.setText("0.0")

        self.parametersPanel.txtStartingMOC.textChanged.connect(self.txtStartingMOCMChanged)
        self.parametersPanel.txtStartingMOCFt.textChanged.connect(self.txtStartingMOCFtChanged)
#
        self.flag1 = 0
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtStartingMOCFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtStartingMOC.text())), 4)))
            except:
                self.parametersPanel.txtStartingMOCFt.setText("0.0")

        self.parametersPanel.txtMaMocT.textChanged.connect(self.txtMaMocTMChanged)
        self.parametersPanel.txtMaMocTFt.textChanged.connect(self.txtMaMocTFtChanged)
#
        self.flag3 = 0
        if self.flag3==0:
            self.flag3=1;
        if self.flag3==2:
            self.flag3=0;
        if self.flag3==1:
            try:
                self.parametersPanel.txtMaMocTFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMaMocT.text())), 4)))
            except:
                self.parametersPanel.txtMaMocTFt.setText("0.0")

        self.parametersPanel.txtMaMocS.textChanged.connect(self.txtMaMocSMChanged)
        self.parametersPanel.txtMaMocSFt.textChanged.connect(self.txtMaMocSFtChanged)
#
        self.flag2 = 0
        if self.flag2==0:
            self.flag2=1;
        if self.flag2==2:
            self.flag2=0;
        if self.flag2==1:
            try:
                self.parametersPanel.txtMaMocSFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMaMocS.text())), 4)))
            except:
                self.parametersPanel.txtMaMocSFt.setText("0.0")

        self.parametersPanel.txtPrevOCAM.textChanged.connect(self.txtxtPrevOCAMChanged)
        self.parametersPanel.txtPrevOCA.textChanged.connect(self.txtxtPrevOCAFtChanged)
        self.flag5 = 0
        if self.flag5==0:
            self.flag5=1;
        if self.flag5==2:
            self.flag5=0;
        if self.flag5==1:
            try:
                self.parametersPanel.txtPrevOCAM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtPrevOCA.text())), 4)))
            except:
                self.parametersPanel.txtPrevOCAM.setText("0.0")

        self.parametersPanel.txtTurningAltitudeM.textChanged.connect(self.txtTurningAltitudeMChanged)
        self.parametersPanel.txtTurningAltitude.textChanged.connect(self.txtTurningAltitudeFtChanged)
        self.flag4 = 0
        if self.flag4==0:
            self.flag4=1;
        if self.flag4==2:
            self.flag4=0;
        if self.flag4==1:
            try:
                self.parametersPanel.txtTurningAltitude.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtTurningAltitudeM.text())), 4)))
            except:
                self.parametersPanel.txtTurningAltitude.setText("0.0")

        self.parametersPanel.txtPrevMOC.textChanged.connect(self.txtPrevMOCMChanged)
        self.parametersPanel.txtPrevMOCFt.textChanged.connect(self.txtPrevMOCFtChanged)
        self.flag6 = 0
        if self.flag6==0:
            self.flag6=1;
        if self.flag6==2:
            self.flag6=0;
        if self.flag6==1:
            try:
                self.parametersPanel.txtPrevMOCFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtPrevMOC.text())), 4)))
            except:
                self.parametersPanel.txtPrevMOCFt.setText("0.0")

        self.parametersPanel.txtNextMOC.textChanged.connect(self.txtNextMOCMChanged)
        self.parametersPanel.txtNextMOCFt.textChanged.connect(self.txtNextMOCFtChanged)
        self.flag7 = 0
        if self.flag7==0:
            self.flag7=1;
        if self.flag7==2:
            self.flag7=0;
        if self.flag7==1:
            try:
                self.parametersPanel.txtNextMOCFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtNextMOC.text())), 4)))
            except:
                self.parametersPanel.txtNextMOCFt.setText("0.0")

        self.parametersPanel.txtFinalMOC.textChanged.connect(self.txtFinalMOCMChanged)
        self.parametersPanel.txtFinalMOCFt.textChanged.connect(self.txtFinalMOCFtChanged)
        self.flag8 = 0
        if self.flag8==0:
            self.flag8=1;
        if self.flag8==2:
            self.flag8=0;
        if self.flag8==1:
            try:
                self.parametersPanel.txtFinalMOCFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtFinalMOC.text())), 4)))
            except:
                self.parametersPanel.txtFinalMOCFt.setText("0.0")

        self.parametersPanel.txtMissedMOC.textChanged.connect(self.txtMissedMOCMChanged)
        self.parametersPanel.txtMissedMOCFt.textChanged.connect(self.txtMissedMOCFtChanged)
        self.flag9 = 0
        if self.flag9==0:
            self.flag9=1;
        if self.flag9==2:
            self.flag9=0;
        if self.flag9==1:
            try:
                self.parametersPanel.txtMissedMOCFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMissedMOC.text())), 4)))
            except:
                self.parametersPanel.txtMissedMOCFt.setText("0.0")
        self.ui.btnEvaluate.setEnabled(True)
#         self.parametersPanel.txtTas.setText(str(round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)).Knots, 4)))
    def txtMissedMOCMChanged(self):
        if self.flag9==0:
            self.flag9=1;
        if self.flag9==2:
            self.flag9=0;
        if self.flag9==1:
            try:
                self.parametersPanel.txtMissedMOCFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMissedMOC.text())), 4)))
            except:
                self.parametersPanel.txtMissedMOCFt.setText("0.0")
    def txtMissedMOCFtChanged(self):
        if self.flag9==0:
            self.flag9=2;
        if self.flag9==1:
            self.flag9=0;
        if self.flag9==2:
            try:
                self.parametersPanel.txtMissedMOC.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtMissedMOCFt.text())), 4)))
            except:
                self.parametersPanel.txtMissedMOC.setText("0.0")
    def txtFinalMOCMChanged(self):
        if self.flag8==0:
            self.flag8=1;
        if self.flag8==2:
            self.flag8=0;
        if self.flag8==1:
            try:
                self.parametersPanel.txtFinalMOCFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtFinalMOC.text())), 4)))
            except:
                self.parametersPanel.txtFinalMOCFt.setText("0.0")
    def txtFinalMOCFtChanged(self):
        if self.flag8==0:
            self.flag8=2;
        if self.flag8==1:
            self.flag8=0;
        if self.flag8==2:
            try:
                self.parametersPanel.txtFinalMOC.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtFinalMOCFt.text())), 4)))
            except:
                self.parametersPanel.txtFinalMOC.setText("0.0")
    def txtNextMOCMChanged(self):
        if self.flag7==0:
            self.flag7=1;
        if self.flag7==2:
            self.flag7=0;
        if self.flag7==1:
            try:
                self.parametersPanel.txtNextMOCFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtNextMOC.text())), 4)))
            except:
                self.parametersPanel.txtNextMOCFt.setText("0.0")
    def txtNextMOCFtChanged(self):
        if self.flag7==0:
            self.flag7=2;
        if self.flag7==1:
            self.flag7=0;
        if self.flag7==2:
            try:
                self.parametersPanel.txtNextMOC.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtNextMOCFt.text())), 4)))
            except:
                self.parametersPanel.txtNextMOC.setText("0.0")
    def txtPrevMOCMChanged(self):
        if self.flag6==0:
            self.flag6=1;
        if self.flag6==2:
            self.flag6=0;
        if self.flag6==1:
            try:
                self.parametersPanel.txtPrevMOCFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtPrevMOC.text())), 4)))
            except:
                self.parametersPanel.txtPrevMOCFt.setText("0.0")
    def txtPrevMOCFtChanged(self):
        if self.flag6==0:
            self.flag6=2;
        if self.flag6==1:
            self.flag6=0;
        if self.flag6==2:
            try:
                self.parametersPanel.txtPrevMOC.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtPrevMOCFt.text())), 4)))
            except:
                self.parametersPanel.txtPrevMOC.setText("0.0")

    def txtxtPrevOCAMChanged(self):
        if self.flag5==0:
            self.flag5=2;
        if self.flag5==1:
            self.flag5=0;
        if self.flag5==2:
            try:
                self.parametersPanel.txtPrevOCA.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtPrevOCAM.text())), 4)))
            except:
                self.parametersPanel.txtPrevOCA.setText("0.0")
    def txtxtPrevOCAFtChanged(self):
        if self.flag5==0:
            self.flag5=1;
        if self.flag5==2:
            self.flag5=0;
        if self.flag5==1:

            try:
                self.parametersPanel.txtPrevOCAM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtPrevOCA.text())), 4)))
            except:
                self.parametersPanel.txtPrevOCAM.setText("0.0")
    def txtTurningAltitudeMChanged(self):
        if self.flag4==0:
            self.flag4=1;
        if self.flag4==2:
            self.flag4=0;
        if self.flag4==1:
            try:
                self.parametersPanel.txtTurningAltitude.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtTurningAltitudeM.text())), 4)))
            except:
                self.parametersPanel.txtTurningAltitude.setText("0.0")
    def txtTurningAltitudeFtChanged(self):
        if self.flag4==0:
            self.flag4=2;
        if self.flag4==1:
            self.flag4=0;
        if self.flag4==2:
            try:
                self.parametersPanel.txtTurningAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtTurningAltitude.text())), 4)))
            except:
                self.parametersPanel.txtTurningAltitudeM.setText("0.0")
    def txtMaMocTMChanged(self):
        if self.flag3==0:
            self.flag3=1;
        if self.flag3==2:
            self.flag3=0;
        if self.flag3==1:
            try:
                self.parametersPanel.txtMaMocTFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMaMocT.text())), 4)))
            except:
                self.parametersPanel.txtMaMocTFt.setText("0.0")
    def txtMaMocTFtChanged(self):
        if self.flag3==0:
            self.flag3=2;
        if self.flag3==1:
            self.flag3=0;
        if self.flag3==2:
            try:
                self.parametersPanel.txtMaMocT.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtMaMocTFt.text())), 4)))
            except:
                self.parametersPanel.txtMaMocT.setText("0.0")
    def txtMaMocSMChanged(self):
        if self.flag2==0:
            self.flag2=1;
        if self.flag2==2:
            self.flag2=0;
        if self.flag2==1:
            try:
                self.parametersPanel.txtMaMocSFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMaMocS.text())), 4)))
            except:
                self.parametersPanel.txtMaMocSFt.setText("0.0")
    def txtMaMocSFtChanged(self):
        if self.flag2==0:
            self.flag2=2;
        if self.flag2==1:
            self.flag2=0;
        if self.flag2==2:
            try:
                self.parametersPanel.txtMaMocS.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtMaMocSFt.text())), 4)))
            except:
                self.parametersPanel.txtMaMocS.setText("0.0")
    def txtPrimaryMOCMChanged(self):
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:

            try:
                self.parametersPanel.txtPrimaryMOCFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtPrimaryMOC.text())), 4)))
            except:
                self.parametersPanel.txtPrimaryMOCFt.setText("0.0")
    def txtPrimaryMOCFtChanged(self):
        if self.flag==0:
            self.flag=1;
        if self.flag==2:
            self.flag=0;
        if self.flag==1:
            try:
                self.parametersPanel.txtPrimaryMOC.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtPrimaryMOCFt.text())), 4)))
            except:
                self.parametersPanel.txtPrimaryMOC.setText("0.0")
    def txtStartingMOCMChanged(self):
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtStartingMOCFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtStartingMOC.text())), 4)))
            except:
                self.parametersPanel.txtStartingMOCFt.setText("0.0")
    def txtStartingMOCFtChanged(self):
        if self.flag1==0:
            self.flag1=2;
        if self.flag1==1:
            self.flag1=0;
        if self.flag1==2:
            try:
                self.parametersPanel.txtStartingMOC.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtStartingMOCFt.text())), 4)))
            except:
                self.parametersPanel.txtStartingMOC.setText("0.0")

    # def captureTrackSMC(self):
    #     captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrack)
    #     define._canvas.setMapTool(captureTrackTool)
    def captureNominalTrackSMC(self):
        captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtNominalTrackSMC)
        define._canvas.setMapTool(captureTrackTool)
    def captureNominalTrackTAOA(self):
        captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtNominalTrackTAOA)
        define._canvas.setMapTool(captureTrackTool)
    def captureNominalTrackSDOA(self):
        captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtNominalTrackSDOA)
        define._canvas.setMapTool(captureTrackTool)
    def captureNominalTrackIMAOA(self):
        captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtNominalTrackIMAOA)
        define._canvas.setMapTool(captureTrackTool)
    def captureDistToEtp(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtDistToEtp, DistanceUnits.M)
        define._canvas.setMapTool(measureDistanceTool)
    def captureX(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtX, DistanceUnits.M)
        define._canvas.setMapTool(measureDistanceTool)
    def method_31_SMC(self):
        if (self.parametersPanel.cmbEvaluationMode.currentIndex() != 0):
            self.parametersPanel.pnlPosition.groupBox.setVisible(False);
            # self.pnlPrimaryMOC.Padding = new System.Windows.Forms.Padding(0);
            self.parametersPanel.frameInsertPointAndText.setVisible(False);
        else:
            self.parametersPanel.pnlPosition.groupBox.setVisible(True);
            # self.pnlPrimaryMOC.Padding = new System.Windows.Forms.Padding(0, 3, 0, 0);
            self.parametersPanel.frameInsertPointAndText.setVisible(True);
        self.parametersPanel.framePerpendicularToSMC.setVisible(self.parametersPanel.pnlProtectionAreaSMC.Value != ProtectionAreaType.Primary);
        self.parametersPanel.frameTextHeight.setEnabled(self.parametersPanel.chbInsertPointAndText.isChecked())
        self.parametersPanel.txtNominalTrackSMC.Enabled = self.parametersPanel.chbPerpendicularToSMC.isChecked()
        self.ui.btnEvaluate.setEnabled(True)
    def tabCtrlGeneral_CurrentChanged(self):
        if self.parametersPanel.tabCtrlGeneral.currentIndex() == 1:
            self.ui.btnConstruct.setIcon(QIcon())
            self.ui.btnConstruct.setText("Determine\nPDG")
            self.ui.btnEvaluate.setIcon(QIcon())
            self.ui.btnEvaluate.setText("Determine\nMACG")
        else:
            self.ui.btnEvaluate.setText("")
            self.ui.btnConstruct.setText("")
            icon = QIcon()
            icon.addPixmap(QPixmap("Resource/btnImage/construct.png"), QIcon.Normal, QIcon.Off)
            self.ui.btnConstruct.setIcon(icon)
            icon = QIcon()
            icon.addPixmap(QPixmap("Resource/btnImage/evaluate.png"), QIcon.Normal, QIcon.Off)
            self.ui.btnEvaluate.setIcon(icon)
        self.method_31_TAOA()
    def method_32_SMC(self):
        self.method_31_SMC();

    def method_31_TAOA(self):
        flag = False
        # if (self.pnlUsedFor.SelectedIndex == 0)
        # {
        #     if (self.gridObstacles.DataSource != TurnAreaObstacleAnalyser.obstaclesDep)
        #     {
        #         self.gridObstacles.DataSource = TurnAreaObstacleAnalyser.obstaclesDep;
        #     }
        # }
        # else if (self.gridObstacles.DataSource != TurnAreaObstacleAnalyser.obstaclesMA)
        # {
        #     self.gridObstacles.DataSource = TurnAreaObstacleAnalyser.obstaclesMA;
        # }
        self.ui.btnConstruct.setVisible(self.parametersPanel.cmbUsedFor.currentIndex() == 0);
        self.ui.btnEvaluate.setVisible(self.parametersPanel.cmbUsedFor.currentIndex() == 1);
        self.parametersPanel.pnlDER.setVisible(self.parametersPanel.cmbUsedFor.currentIndex() == 0);
        self.parametersPanel.pnlSOC.setVisible(self.parametersPanel.cmbUsedFor.currentIndex() == 1);
        # GroupBox groupBox = self.gbETP;
        if (self.parametersPanel.cmbPortion.currentIndex() == 2):
            flag = True;
        else:
            flag = False if(self.parametersPanel.cmbPortion.currentIndex() != 1) else self.parametersPanel.chbSecondTurn.isChecked();
        self.parametersPanel.pnlETP.setVisible(flag);
        self.parametersPanel.frameStartingMOC.setVisible(self.parametersPanel.cmbUsedFor.currentIndex() == 0);
        self.parametersPanel.frameDepMocS.setVisible(False if(self.parametersPanel.cmbPortion.currentIndex() != 0) else self.parametersPanel.cmbUsedFor.currentIndex() == 0);
        self.parametersPanel.frameDepMocT.setVisible(False if(self.parametersPanel.cmbPortion.currentIndex() <= 0) else self.parametersPanel.cmbUsedFor.currentIndex() == 0)
        self.parametersPanel.frameMaMocS.setVisible(False if(self.parametersPanel.cmbPortion.currentIndex() != 0) else self.parametersPanel.cmbUsedFor.currentIndex() == 1)
        self.parametersPanel.frameMaMocT.setVisible(False if(self.parametersPanel.cmbPortion.currentIndex() <= 0) else self.parametersPanel.cmbUsedFor.currentIndex() == 1)
        # self.pnlMaMocS.Visible = (self.pnlPortion.SelectedIndex != 0 ? false : self.pnlUsedFor.SelectedIndex == 1);
        # self.pnlMaMocT.Visible = (self.pnlPortion.SelectedIndex <= 0 ? false : self.pnlUsedFor.SelectedIndex == 1);
        self.parametersPanel.framePDG.setVisible(self.parametersPanel.cmbUsedFor.currentIndex() == 0);
        self.parametersPanel.frameMACG.setVisible(self.parametersPanel.cmbUsedFor.currentIndex() == 1);
        self.parametersPanel.frameTurningAltitude.setVisible(self.parametersPanel.cmbPortion.currentIndex() == 3);
        self.parametersPanel.frameSecondTurn.setVisible(True if(self.parametersPanel.cmbPortion.currentIndex() == 1) else self.parametersPanel.cmbPortion.currentIndex() == 2);
        if (self.parametersPanel.cmbUsedFor.currentIndex() != 0):
            self.parametersPanel.label_NominalTrack_2.setText(Captions.DIST_SOC_ETP + "(m)");
        else:
            self.parametersPanel.label_NominalTrack_2.setText(Captions.DIST_DER_ETP + "(m)");
        self.parametersPanel.framePerpendicularToTAOA.setVisible(self.parametersPanel.pnlProtectionAreaTAOA.Value != ProtectionAreaType.Primary);
        if (self.parametersPanel.cmbUsedFor.currentIndex() != 0):
            self.parametersPanel.chbStoreDistances.setText(Captions.STORE_DZ_DO_DISTANCES);
        else:
            self.parametersPanel.chbStoreDistances.setText(Captions.STORE_DR_DO_DISTANCES);
        self.chbHideCloseInObst.setVisible(self.parametersPanel.cmbUsedFor.currentIndex() == 0);
        self.parametersPanel.frameDistToEtp.setEnabled(self.parametersPanel.chbSecondTurn.isChecked())
        self.parametersPanel.txtNominalTrackTAOA.Enabled = self.parametersPanel.chbPerpendicularToTAOA.isChecked()
        if self.parametersPanel.tabCtrlGeneral.currentIndex() != 1:
            self.ui.btnConstruct.setVisible(False)
            self.ui.btnEvaluate.setVisible(True)
        if self.parametersPanel.cmbUsedFor.currentIndex() == 1 and self.parametersPanel.cmbPortion.currentIndex() == 0:
            self.parametersPanel.txtMaMocS.setText("30")
            self.parametersPanel.txtMaMocT.setText("30")
        else:
            self.parametersPanel.txtMaMocS.setText("50")
            self.parametersPanel.txtMaMocT.setText("50")

        if self.parametersPanel.cmbUsedFor.currentIndex() == 0 and (self.parametersPanel.cmbPortion.currentIndex() == 1 or self.parametersPanel.cmbPortion.currentIndex() == 2):
            self.parametersPanel.txtDepMocT1.setText("75")
        else:
            self.parametersPanel.txtDepMocT1.setText("90")
    def method_28_MTA(self):
        ObstacleEvaluatorDlg.resultObs1 = None
        ObstacleEvaluatorDlg.resultObs2 = None
        ObstacleEvaluatorDlg.resultDelta = None;
        ObstacleEvaluatorDlg.resultFactor = None;
        ObstacleEvaluatorDlg.resultMoc = None;
        self.method_29_MTA();
    def method_29_MTA(self):
        self.parametersPanel.pnlResultElevChange.Value = ObstacleEvaluatorDlg.resultDelta;
        self.parametersPanel.pnlResultElevChange.ButtonVisible = False if(ObstacleEvaluatorDlg.resultDelta == None or ObstacleEvaluatorDlg.resultDelta == "") else True;
        self.parametersPanel.pnlResultFactor.Value = ObstacleEvaluatorDlg.resultFactor;
        self.parametersPanel.pnlResultMOC.Value = ObstacleEvaluatorDlg.resultMoc;
    def method_30_MTA(self):
        self.method_28_MTA()
    def method_32_MTA(self):
        # AcadHelper.smethod_27(DrawingSpace.ModelSpace, true);
        # ObjectId activeSpaceId = AcadHelper.ActiveSpaceId;
        position = [ObstacleEvaluatorDlg.resultObs2.Position, ObstacleEvaluatorDlg.resultObs1.Position];


        constructionLayer = AcadHelper.createVectorLayer(SurfaceTypes.MountainousTerrainAnalyser + " Line");
        AcadHelper.smethod_145(position, constructionLayer);

        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.MountainousTerrainAnalyser)
    def method_33_MTA(self):
        flag = False;
        metres = self.parametersPanel.pnlElevWithin.Value.Metres;
        num = self.parametersPanel.pnlElevChange.Value.Metres;
        # base.imethod_0(Messages.ANALYSING, MountainousTerrainAnalyser.list.Count);
        
        self.obstacleSort(ObstacleEvaluatorDlg.list);
        i = len(ObstacleEvaluatorDlg.list) - 1
        while i >= 0:
            num1 = 0;
            while (num1 < i):
                item = ObstacleEvaluatorDlg.list[i];
                obstacle = ObstacleEvaluatorDlg.list[num1];
                num2 = MathHelper.calcDistance(item.Position, obstacle.Position);
                num3 = self.method_34_MTA(item, obstacle);
                if (num3 <= num):
                    break;
                if (num2 <= metres):
                    ObstacleEvaluatorDlg.resultObs1 = item;
                    ObstacleEvaluatorDlg.resultObs2 = obstacle;
                    num = num3;
                num1 += 1
            i -= 1
        if (ObstacleEvaluatorDlg.resultObs1 == None or not ObstacleEvaluatorDlg.resultObs2 == None or ObstacleEvaluatorDlg.resultObs1.Assigned or not ObstacleEvaluatorDlg.resultObs2.Assigned):
            ObstacleEvaluatorDlg.resultObs1 = ObstacleEvaluatorDlg.list[0];
            ObstacleEvaluatorDlg.resultObs2 = ObstacleEvaluatorDlg.list[len(ObstacleEvaluatorDlg.list) - 1];
        value = self.parametersPanel.pnlElevWithin.Value;
        distance = Distance(0, value.OriginalUnits) + MathHelper.calcDistance(ObstacleEvaluatorDlg.resultObs1.Position, ObstacleEvaluatorDlg.resultObs2.Position);
        altitude = self.parametersPanel.pnlElevChange.Value;
        altitude1 = Altitude(0, altitude.OriginalUnit()) + self.method_34_MTA(ObstacleEvaluatorDlg.resultObs1, ObstacleEvaluatorDlg.resultObs2);
        ObstacleEvaluatorDlg.resultDelta = "%s (%s)"%(str(round(altitude1.Metres, 4)) + "m", str(round(distance.NauticalMiles, 4)) + "nm");
        metres1 = altitude1.Metres;
        value1 = self.parametersPanel.pnlElevChange.Value;
        num4 = MathHelper.smethod_0(min([2, max([1, metres1 / value1.Metres])]), 1);
        if (altitude1.Metres < self.parametersPanel.pnlElevChange.Value.Metres or distance.Metres > self.parametersPanel.pnlElevWithin.Value.Metres):
            num4 = 1;
        ObstacleEvaluatorDlg.resultFactor = "%s x"%(str(round(num4, 1)))
        value2 = self.parametersPanel.pnlMOC.Value * num4;
        ObstacleEvaluatorDlg.resultMoc = str(round(value2.Metres, 4)) + "m";
        return True;
    def method_34_MTA(self, obstacle_0, obstacle_1):
        z = obstacle_0.Position.get_Z() + obstacle_0.Trees;
        position = obstacle_1.Position;
        return math.fabs(z - (position.get_Z() + obstacle_1.Trees));
    def obstacleSort(self, obstacleList):
        i = 0
        for obstacle in obstacleList:
            if i == 0:
                i += 1
                continue
            for j in range(i):
                z = obstacleList[j].Position.get_Z() + obstacleList[j].Trees;
                num = obstacle.Position.get_Z() + obstacle.Trees;
                if z > num:
                    obstacleList.pop(i)
                    obstacleList.insert(j, obstacle)
                    break
            i += 1
            # return resultObstacleList

class SecMocObstacles(ObstacleTable):
    def __init__(self, iobstacleArea_0, double_0):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, None)
        self.area = iobstacleArea_0;
        self.primaryMOC = double_0;
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
        # self.IndexCritical = fixedColumnCount + 7

        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DistInSecM,
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt
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

        # item = QStandardItem(str(checkResult[4]))
        # item.setData(checkResult[4])
        # self.source.setItem(row, self.IndexCritical, item)

    def checkObstacle(self, obstacle_0):
        num = None;
        num1 = None;
        mocMultiplier = self.primaryMOC * obstacle_0.MocMultiplier;
        resultList = []
        obstacleAreaResult = self.area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier, resultList);
        if len(resultList) == 0:
            return
        num = resultList[0]
        num1 = resultList[1]
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            position = obstacle_0.Position;
            z = position.get_Z() + obstacle_0.Trees + num;
            checkResult = [obstacleAreaResult, num1, num, z];
            self.addObstacleToModel(obstacle_0, checkResult)
            # SecondaryMoc.obstacles.method_11(obstacle_0, obstacleAreaResult, num1, num, z);
        
        
            
    def method_0(self, obstacle_0, string_0):
        num = None;
        num1 = None;
        mocMultiplier = self.primaryMOC * obstacle_0.MocMultiplier;
        resultList = []
        obstacleAreaResult = self.area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier, resultList);
        if len(resultList) == 0:
            return
        num = resultList[0]
        num1 = resultList[1]
        position = obstacle_0.Position;
        z = position.get_Z() + obstacle_0.Trees + num;
        checkResult = [obstacleAreaResult, num1, num, z];

        self.addObstacleToModel(obstacle_0, checkResult)

        # SecondaryMoc.obstacles.method_11(obstacle_0, obstacleAreaResult, num1, num, z);
        name = obstacle_0.Name;
        point3d = obstacle_0.Position;
        altitude = Altitude(point3d.get_Z() + obstacle_0.Trees);
        string_0 = "{%s}, {%s}, {%s}"%(name, altitude.method_0(":u"), self.area.ToString());
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            mOC = Captions.MOC;
            altitude1 = Altitude(num);
            string_0 = string_0 + ", {%s} {%s}"%(mOC, altitude1.method_0(":u"));
        return string_0

class TurnAreaObstaclesMA(ObstacleTable):
    def __init__(self, parameterDictionary):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, None)
        self.paramDictionary = parameterDictionary
    def setHiddenColumns(self, tableView):
#         tableView.hideColumn(self.IndexObstArea)
#         tableView.hideColumn(self.IndexDistInSecM)
        return ObstacleTable.setHiddenColumns(self, tableView)
    def setHeaderLabels(self):

        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)

        self.IndexObstArea = fixedColumnCount
        self.IndexDistInSecM = fixedColumnCount + 1
        self.IndexDzM = fixedColumnCount + 2
        self.IndexDoM = fixedColumnCount + 3
        self.IndexMocReqM = fixedColumnCount + 4
        self.IndexMocReqFt = fixedColumnCount + 5
        self.IndexMocMultiplier = fixedColumnCount + 6
        self.IndexAcAltM = fixedColumnCount + 7
        self.IndexAcAltFt = fixedColumnCount + 8
        self.IndexAltReqM = fixedColumnCount + 9
        self.IndexAltReqFt = fixedColumnCount + 10
        self.IndexMACG = fixedColumnCount + 11
        self.IndexCritical = fixedColumnCount + 12
        self.IndexTag = fixedColumnCount + 13

        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DistInSecM,
                ObstacleTableColumnType.DzM,
                ObstacleTableColumnType.DoM,
                ObstacleTableColumnType.MocReqM,
                ObstacleTableColumnType.MocReqFt,
                ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.AcAltM,
                ObstacleTableColumnType.AcAltFt,
                ObstacleTableColumnType.AltReqM,
                ObstacleTableColumnType.AltReqFt,
                ObstacleTableColumnType.MACG,
                ObstacleTableColumnType.Critical,
                ObstacleTableColumnType.Tag
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
        self.source.setItem(row, self.IndexDzM, item)

        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexDoM, item)

        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4])
        self.source.setItem(row, self.IndexMocReqM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[4])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[4]))
        self.source.setItem(row, self.IndexMocReqFt, item)

        item = QStandardItem(str(ObstacleTable.MocMultiplier))
        item.setData(ObstacleTable.MocMultiplier)
        self.source.setItem(row, self.IndexMocMultiplier, item)

        item = QStandardItem(str(checkResult[5]))
        item.setData(checkResult[5])
        self.source.setItem(row, self.IndexAcAltM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[5])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[5]))
        self.source.setItem(row, self.IndexAcAltFt, item)

        item = QStandardItem(str(checkResult[6]))
        item.setData(checkResult[6])
        self.source.setItem(row, self.IndexAltReqM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[6])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[6]))
        self.source.setItem(row, self.IndexAltReqFt, item)

        item = QStandardItem(str(checkResult[7]))
        item.setData(checkResult[7])
        self.source.setItem(row, self.IndexMACG, item)

        item = QStandardItem(str(checkResult[8]))
        item.setData(checkResult[8])
        self.source.setItem(row, self.IndexCritical, item)

        item = QStandardItem(str(checkResult[9]))
        item.setData(checkResult[9])
        if checkResult[9] != None:
            item.setToolTip(checkResult[9])
        self.source.setItem(row, self.IndexTag, item)

    def checkObstacle(self, obstacle_0):
        checkResult = []
        if self.paramDictionary[0] == "TurnAreaMaStraightEvaluator":
            checkResult = self.checkObstacleTurnAreaMaStraight(obstacle_0, self.paramDictionary[1])

        elif self.paramDictionary[0] == "TurnAreaMATurnAtAltitudeEvaluator":
            checkResult = self.checkObstacleTurnAreaMATurnAtAltitude(obstacle_0, self.paramDictionary[1])
        elif self.paramDictionary[0] == "TurnAreaMaTurnEvaluator":
            checkResult = self.checkObstacleTurnAreaMaTurn(obstacle_0, self.paramDictionary[1])

        if checkResult != None:
            self.addObstacleToModel(obstacle_0, checkResult)

    def checkObstacleTurnAreaMaStraight(self, obstacle_0, paramList):
        area = paramList[0];
        trackRad = Unit.ConvertDegToRad(paramList[2]);
        ptSOC = paramList[1];
        ptSOC2 = MathHelper.distanceBearingPoint(ptSOC, trackRad - 1.5707963267949, 100);
        moc = paramList[3];
        macg = paramList[4];
        distSocToEtp = paramList[5];
        storeDistances = paramList[6];
        
        num = None;
        point3d = None;
        drDzDoObstacleTag = None;
        obstacleAreaResult = ObstacleAreaResult.Outside;
        num1 = None;
        num2 = None;
        mocMultiplier = moc * obstacle_0.MocMultiplier;
        resultList = []
        obstacleAreaResult = area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier, resultList);
        if len(resultList) == 0:
            return None
        num1 = resultList[0]
        num2 = resultList[1]
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, trackRad + 3.14159265358979, obstacle_0.Tolerance);
            point3d2 = MathHelper.distanceBearingPoint(point3d1, trackRad, 100);
            point3d = MathHelper.getIntersectionPoint(ptSOC, ptSOC2, point3d1, point3d2);
            num = 1E-08 if(not MathHelper.smethod_119(point3d1, ptSOC, ptSOC2)) else MathHelper.calcDistance(point3d, point3d1);
            num3 = (distSocToEtp if(not distSocToEtp == None  and not math.isinf(distSocToEtp)) else 0) + num;
            z = ptSOC.get_Z() + macg / 100 * num3;
            position = obstacle_0.Position;
            z1 = position.get_Z() + obstacle_0.Trees + num1;
            z2 = 100 * ((z1 - ptSOC.get_Z()) / num3);
            criticalObstacleType = CriticalObstacleType.No;
            if (z2 > macg):
                criticalObstacleType = CriticalObstacleType.Yes;
            if (storeDistances):
                drDzDoObstacleTag = "Do1 = %s\nDo2 = %s\nhasDrz = False"%(point3d.ToString(), point3d1.ToString())
                # drDzDoObstacleTag = None #DrDzDoObstacleTag(point3d, point3d1);
            else:
                drDzDoObstacleTag = None;
            drDzDoObstacleTag1 = drDzDoObstacleTag;
            return [obstacleAreaResult, num2, distSocToEtp, num, num1, z, z1, z2, criticalObstacleType, drDzDoObstacleTag1]
        return None
    def checkObstacleTurnAreaMATurnAtAltitude(self, obstacle_0, paramList):
        area = paramList[0];
        ptSOC = paramList[1];
        ptLine1 = paramList[6];
        ptLine2 = paramList[7];
        track = Unit.ConvertDegToRad(paramList[2]);
        trackLine = MathHelper.getBearing(ptLine1, ptLine2);
        moc = paramList[3];
        macg = paramList[4];
        ta = paramList[5].Metres;
        storeDistances = paramList[8];
        ptSOC2 = MathHelper.distanceBearingPoint(ptSOC, track - 1.5707963267949, 100);
        
        point3d = None;
        point3d1 = None;
        drDzDoObstacleTag = None;
        obstacleAreaResult = ObstacleAreaResult.Outside;
        num = None;
        num1 = None;
        mocMultiplier = moc * obstacle_0.MocMultiplier;
        resultList = []
        obstacleAreaResult = area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier, resultList);
        if len(resultList) == 0:
            return None
        num = resultList[0]
        num1 = resultList[1]
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            point3d = MathHelper.getIntersectionPoint(ptLine1, ptLine2, obstacle_0.Position, MathHelper.distanceBearingPoint(obstacle_0.Position, trackLine + 1.5707963267949, 100));
            point3d1 = MathHelper.getIntersectionPoint(point3d, MathHelper.distanceBearingPoint(point3d, track, 100), ptSOC, ptSOC2);
            if (MathHelper.smethod_119(point3d, ptSOC, ptSOC2)):
                MathHelper.calcDistance(point3d, point3d1);
            num2 = max([0.0001, MathHelper.calcDistance(obstacle_0.Position, point3d) - obstacle_0.Tolerance]);
            num3 = ta + macg / 100 * num2;
            position = obstacle_0.Position;
            z = position.get_Z() + obstacle_0.Trees + num;
            num4 = 100 * ((z - ta) / num2);
            criticalObstacleType = CriticalObstacleType.No;
            if (num4 > macg):
                criticalObstacleType = CriticalObstacleType.Yes;
            point3d2 = MathHelper.distanceBearingPoint(point3d, MathHelper.getBearing(point3d, obstacle_0.Position), num2);
            if (storeDistances):
                drDzDoObstacleTag = "Do1 = %s\nDo2 = %s\nhasDrz = False"%(point3d.ToString(), point3d2.ToString())
                # drDzDoObstacleTag = None #DrDzDoObstacleTag(point3d, point3d2);
            else:
                drDzDoObstacleTag = None
            drDzDoObstacleTag1 = drDzDoObstacleTag;
            return [obstacleAreaResult, num1, None, num2, num, num3, z, num4, criticalObstacleType, drDzDoObstacleTag1]

    def checkObstacleTurnAreaMaTurn(self, obstacle_0, paramList):
        point3d = None;
        area = paramList[0];
        trackRad = Unit.ConvertDegToRad(paramList[3]);
        ptSOC = paramList[1];
        ptETP = paramList[2];
        moc = paramList[4];
        macg = paramList[5];
        distSocToEtp = paramList[6];
        storeDistances = paramList[7];
        point3d = MathHelper.getIntersectionPoint(ptETP, MathHelper.distanceBearingPoint(ptETP, trackRad, 100), ptSOC, MathHelper.distanceBearingPoint(ptSOC, trackRad - 1.5707963267949, 100));
        detp = MathHelper.calcDistance(point3d, ptETP);
        if (not distSocToEtp == None and not math.isinf(distSocToEtp)):
            detp = distSocToEtp;
        ptDr1 = point3d;
        ptDr2 = ptETP;

        obstacleAreaResult = ObstacleAreaResult.Outside;
        num = None;
        num1 = None;
        mocMultiplier = moc * obstacle_0.MocMultiplier;
        resultList = []
        obstacleAreaResult = area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier, resultList);
        if len(resultList) == 0:
            return None
        num = resultList[0]
        num1 = resultList[1]
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            point3d = MathHelper.distanceBearingPoint(obstacle_0.Position, MathHelper.getBearing(obstacle_0.Position, ptETP), obstacle_0.Tolerance);
            num2 = MathHelper.calcDistance(ptETP, point3d);
            if (num2 <= obstacle_0.Tolerance):
                num2 = 1E-08;
            num3 = detp + num2;
            z = ptSOC.get_Z() + macg / 100 * num3;
            position = obstacle_0.Position;
            z1 = position.get_Z() + obstacle_0.Trees + num;
            z2 = 100 * ((z1 - ptSOC.get_Z()) / num3);
            criticalObstacleType = CriticalObstacleType.No;
            if (z2 > macg):
                criticalObstacleType = CriticalObstacleType.Yes;
            drDzDoObstacleTag = None;
            if (storeDistances):
                if distSocToEtp == None or math.isinf(distSocToEtp):
                    drDzDoObstacleTag = "Drz1 = %s\nDrz2 = %s\nDo1 = %s\nDo2 = %s\nhasDrz = True"%(ptDr1.ToString(), ptDr2.ToString(), ptETP.ToString(), point3d.ToString())
                else:
                    drDzDoObstacleTag = "Do1 = %s\nDo2 = %s\nhasDrz = False"%(ptETP.ToString(), point3d.ToString())

                # drDzDoObstacleTag = None #(!distSocToEtp.smethod_18() ? new DrDzDoObstacleTag(ptDr1, ptDr2, ptETP, point3d) : new DrDzDoObstacleTag(ptETP, point3d));
            return [obstacleAreaResult, num1, detp, num2, num, z, z1, z2, criticalObstacleType, drDzDoObstacleTag]
        return None

class TurnAreaObstaclesDep(ObstacleTable):
    def __init__(self, parameterDictionary):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, None)
        self.paramDictionary = parameterDictionary
    def setHiddenColumns(self, tableView):
#         tableView.hideColumn(self.IndexObstArea)
#         tableView.hideColumn(self.IndexDistInSecM)
        return ObstacleTable.setHiddenColumns(self, tableView)
    def setHeaderLabels(self):

        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)

        self.IndexObstArea = fixedColumnCount
        self.IndexDistInSecM = fixedColumnCount + 1
        self.IndexDrM = fixedColumnCount + 2
        self.IndexDoM = fixedColumnCount + 3
        self.IndexMocReqM = fixedColumnCount + 4
        self.IndexMocReqFt = fixedColumnCount + 5
        self.IndexMocMultiplier = fixedColumnCount + 6
        self.IndexAcAltM = fixedColumnCount + 7
        self.IndexAcAltFt = fixedColumnCount + 8
        self.IndexAltReqM = fixedColumnCount + 9
        self.IndexAltReqFt = fixedColumnCount + 10
        self.IndexPDG = fixedColumnCount + 11
        self.IndexCritical = fixedColumnCount + 12
        self.IndexCloseIn = fixedColumnCount + 13
        self.IndexTag = fixedColumnCount + 14

        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DistInSecM,
                ObstacleTableColumnType.DrM,
                ObstacleTableColumnType.DoM,
                ObstacleTableColumnType.MocReqM,
                ObstacleTableColumnType.MocReqFt,
                ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.AcAltM,
                ObstacleTableColumnType.AcAltFt,
                ObstacleTableColumnType.AltReqM,
                ObstacleTableColumnType.AltReqFt,
                ObstacleTableColumnType.PDG,
                ObstacleTableColumnType.Critical,
                ObstacleTableColumnType.CloseIn,
                ObstacleTableColumnType.Tag
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
        self.source.setItem(row, self.IndexDrM, item)

        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexDoM, item)

        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4])
        self.source.setItem(row, self.IndexMocReqM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[4])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[4]))
        self.source.setItem(row, self.IndexMocReqFt, item)

        item = QStandardItem(str(ObstacleTable.MocMultiplier))
        item.setData(ObstacleTable.MocMultiplier)
        self.source.setItem(row, self.IndexMocMultiplier, item)

        item = QStandardItem(str(checkResult[5]))
        item.setData(checkResult[5])
        self.source.setItem(row, self.IndexAcAltM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[5])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[5]))
        self.source.setItem(row, self.IndexAcAltFt, item)

        item = QStandardItem(str(checkResult[6]))
        item.setData(checkResult[6])
        self.source.setItem(row, self.IndexAltReqM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[6])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[6]))
        self.source.setItem(row, self.IndexAltReqFt, item)

        item = QStandardItem(str(checkResult[7]))
        item.setData(checkResult[7])
        self.source.setItem(row, self.IndexPDG, item)

        item = QStandardItem(str(checkResult[8]))
        item.setData(checkResult[8])
        self.source.setItem(row, self.IndexCritical, item)

        item = QStandardItem(str(checkResult[9]))
        item.setData(checkResult[9])
        self.source.setItem(row, self.IndexCloseIn, item)

        item = QStandardItem(str(checkResult[10]))
        item.setData(checkResult[10])
        if checkResult[10] != None:
            item.setToolTip(checkResult[10])
        self.source.setItem(row, self.IndexTag, item)

    def checkObstacle(self, obstacle_0):
        checkResult = []
        if self.paramDictionary[0] == "TurnAreaDepStraightEvaluator":
            checkResult = self.checkObstacleTurnAreaDepStraight(obstacle_0, self.paramDictionary[1])

        elif self.paramDictionary[0] == "TurnAreaDepTurnAtAltitudeEvaluator":
            checkResult = self.checkObstacleTurnAreaDepTurnAtAltitude(obstacle_0, self.paramDictionary[1])
        elif self.paramDictionary[0] == "TurnAreaDepTurnEvaluator":
            checkResult = self.checkObstacleTurnAreaDepTurn(obstacle_0, self.paramDictionary[1])
        elif self.paramDictionary[0] == "TurnAreaDepTurnStraightEvaluator":
            checkResult = self.checkObstacleTurnAreaDepTurnStraight(obstacle_0, self.paramDictionary[1])
        if checkResult != None:
            self.addObstacleToModel(obstacle_0, checkResult)

    def checkObstacleTurnAreaDepStraight(self, obstacle_0, paramList):
        area = paramList[0];
        trackRad = Unit.ConvertDegToRad(paramList[2]);
        ptDER = paramList[1];
        ptDER2 = MathHelper.distanceBearingPoint(ptDER, trackRad - 1.5707963267949, 100);
        startingMoc = paramList[3];
        moc = paramList[4];
        pdg = paramList[5];
        storeDistances = paramList[6];

        num = None;
        point3d = None;
        drDzDoObstacleTag = None;
        obstacleAreaResult = ObstacleAreaResult.Outside;
        num1 = None;
        num2 = None;
        point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, trackRad + 3.14159265358979, obstacle_0.Tolerance);
        point3d2 = MathHelper.distanceBearingPoint(point3d1, trackRad, 100);
        point3d = MathHelper.getIntersectionPoint(ptDER, ptDER2, point3d1, point3d2);
        num = 1E-08 if(not MathHelper.smethod_119(point3d1, ptDER, ptDER2)) else  MathHelper.calcDistance(point3d, point3d1);
        mocMultiplier = startingMoc + moc / 100 * num * obstacle_0.MocMultiplier;
        resultList = []
        obstacleAreaResult = area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier, resultList);
        if len(resultList) == 0:
            return None
        num1 = resultList[0]
        num2 = resultList[1]
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            z = ptDER.get_Z() + 5 + pdg / 100 * num;
            position = obstacle_0.Position;
            z1 = position.get_Z() + obstacle_0.Trees + num1;
            z2 = 100 * ((z1 - (ptDER.get_Z() + 5)) / num);
            criticalObstacleType = CriticalObstacleType.No;
            if (z2 > pdg):
                criticalObstacleType = CriticalObstacleType.Yes;
            closeInObstacleType = CloseInObstacleType.No;
            if (z1 <= ptDER.get_Z() + 60):
                closeInObstacleType = CloseInObstacleType.Yes;
            if (storeDistances):
                drDzDoObstacleTag = "Do1 = %s\nDo2 = %s\nhasDrz = False"%(point3d.ToString(), point3d1.ToString())

                # drDzDoObstacleTag = None #DrDzDoObstacleTag(point3d, point3d1);
            else:
                drDzDoObstacleTag = None;
            drDzDoObstacleTag1 = drDzDoObstacleTag;
            return [obstacleAreaResult, num2, None, num, num1, z, z1, z2, criticalObstacleType, closeInObstacleType, drDzDoObstacleTag1]
        return None
    def checkObstacleTurnAreaDepTurnAtAltitude(self, obstacle_0, paramList):
        area = paramList[0];
        ptDER = paramList[1];
        ptLine1 = paramList[8];
        ptLine2 = paramList[9];
        track = Unit.ConvertDegToRad(paramList[2]);
        trackLine = MathHelper.getBearing(ptLine1, ptLine2);
        minMoc = paramList[3];
        startingMoc = paramList[4];
        moc = paramList[5];
        pdg = paramList[6];
        ta = paramList[7].Metres;
        storeDistances = paramList[10];
        ptDER2 = MathHelper.distanceBearingPoint(ptDER, track - 1.5707963267949, 100);
        
        point3d = None;
        point3d1 = None;
        drDzDoObstacleTag = None;
        obstacleAreaResult = ObstacleAreaResult.Outside;
        num = None;
        num1 = None;
        point3d = MathHelper.getIntersectionPoint(ptLine1, ptLine2, obstacle_0.Position, MathHelper.distanceBearingPoint(obstacle_0.Position, trackLine + 1.5707963267949, 100));
        point3d1 = MathHelper.getIntersectionPoint(point3d, MathHelper.distanceBearingPoint(point3d, track, 100), ptDER, ptDER2);
        num2 = MathHelper.calcDistance(point3d, point3d1) if(MathHelper.smethod_119(point3d, ptDER, ptDER2)) else 0.0001;
        num3 = max([0.0001, MathHelper.calcDistance(obstacle_0.Position, point3d) - obstacle_0.Tolerance]);
        num4 = max([startingMoc + moc / 100 * (num2 + num3) * obstacle_0.MocMultiplier, minMoc]);
        resultList = []
        obstacleAreaResult = area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, num4, resultList);
        if len(resultList) == 0:
            return None
        num = resultList[0]
        num1 = resultList[1]
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            num5 = ta + pdg / 100 * num3;
            position = obstacle_0.Position;
            z = position.get_Z() + obstacle_0.Trees + num;
            num6 = 100 * ((z - ta) / num3);
            criticalObstacleType = CriticalObstacleType.No;
            if (num6 > pdg):
                criticalObstacleType = CriticalObstacleType.Yes;
            closeInObstacleType = CloseInObstacleType.No;
            if (z <= ptDER.get_Z() + 60):
                closeInObstacleType = CloseInObstacleType.Yes;
            point3d2 = MathHelper.distanceBearingPoint(point3d, MathHelper.getBearing(point3d, obstacle_0.Position), num3);
            if (storeDistances):
                drDzDoObstacleTag = "Do1 = %s\nDo2 = %s\nhasDrz = False"%(point3d.ToString(), point3d2.ToString())

                # drDzDoObstacleTag = None # DrDzDoObstacleTag(point3d1, point3d, point3d, point3d2);
            else:
                drDzDoObstacleTag = None;
            drDzDoObstacleTag1 = drDzDoObstacleTag;
            return [obstacleAreaResult, num1, num2, num3, num, num5, z, num6, criticalObstacleType, closeInObstacleType, drDzDoObstacleTag1]
        return None

    def checkObstacleTurnAreaDepTurn(self, obstacle_0, paramList):
        point3d = None;
        area = paramList[0];
        trackRad = Unit.ConvertDegToRad(paramList[3]);
        ptDER = paramList[1];
        ptETP = paramList[2];
        minMoc = paramList[4];
        startingMoc = paramList[5];
        moc = paramList[6];
        pdg = paramList[7];
        distDerToEtp = paramList[8];
        storeDistances = paramList[9];
        point3d = MathHelper.getIntersectionPoint(ptETP, MathHelper.distanceBearingPoint(ptETP, trackRad, 100), ptDER, MathHelper.distanceBearingPoint(ptDER, trackRad - 1.5707963267949, 100));
        detp = MathHelper.calcDistance(point3d, ptETP);
        if (not paramList[8] == None and not math.isinf(paramList[8]) ):
            detp = paramList[8];
        ptDr1 = point3d;
        ptDr2 = ptETP;

        obstacleAreaResult = ObstacleAreaResult.Outside;
        num = None;
        num1 = None;
        point3d = MathHelper.distanceBearingPoint(obstacle_0.Position, MathHelper.getBearing(obstacle_0.Position, ptETP), obstacle_0.Tolerance);
        num2 = MathHelper.calcDistance(ptETP, point3d);
        if (num2 <= obstacle_0.Tolerance):
            num2 = 1E-08;
        num3 = detp + num2;
        num4 = max([startingMoc + moc / 100 * num3 * obstacle_0.MocMultiplier, minMoc]);
        resultList = []
        obstacleAreaResult = area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, num4, resultList);
        if len(resultList) == 0:
            return None
        num = resultList[0]
        num1 = resultList[1]
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            z = ptDER.get_Z() + 5 + pdg / 100 * num3;
            position = obstacle_0.Position;
            z1 = position.get_Z() + obstacle_0.Trees + num;
            z2 = 100 * ((z1 - (ptDER.get_Z() + 5)) / num3);
            criticalObstacleType = CriticalObstacleType.No;
            if (z2 > pdg):
                criticalObstacleType = CriticalObstacleType.Yes;
            closeInObstacleType = CloseInObstacleType.No;
            if (z1 <= ptDER.get_Z() + 60):
                closeInObstacleType = CloseInObstacleType.Yes;
            drDzDoObstacleTag = None;
            if (storeDistances):
                if distDerToEtp == None or math.isinf(distDerToEtp):
                    drDzDoObstacleTag = "Drz1 = %s\nDrz2 = %s\nDo1 = %s\nDo2 = %s\nhasDrz = True"%(ptDr1.ToString(), ptDr2.ToString(), ptETP.ToString(), point3d.ToString())
                else:
                    drDzDoObstacleTag = "Do1 = %s\nDo2 = %s\nhasDrz = False"%(ptETP.ToString(), point3d.ToString())

                # drDzDoObstacleTag = None # (!distDerToEtp.smethod_18() ? new DrDzDoObstacleTag(ptDr1, ptDr2, ptETP, point3d) : new DrDzDoObstacleTag(ptETP, point3d));
            return [obstacleAreaResult, num1, detp, num2, num, z, z1, z2, criticalObstacleType, closeInObstacleType, drDzDoObstacleTag]
        return None

    def checkObstacleTurnAreaDepTurnStraight(self, obstacle_0, paramList):
        area = paramList[0];
        trackRad = Unit.ConvertDegToRad(paramList[2]);
        ptDER = paramList[1];
        ptDER2 = MathHelper.distanceBearingPoint(ptDER, trackRad - 1.5707963267949, 100);
        minMoc = paramList[3];
        startingMoc = paramList[4];
        moc = paramList[5];
        pdg = paramList[6];
        distDerToEtp = paramList[7];
        storeDistances = paramList[8];

        num = None;
        point3d = None;
        drDzDoObstacleTag = None;
        obstacleAreaResult = ObstacleAreaResult.Outside;
        num1 = None;
        num2 = None;
        point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, trackRad + 3.14159265358979, obstacle_0.Tolerance);
        point3d2 = MathHelper.distanceBearingPoint(point3d1, trackRad, 100);
        point3d = MathHelper.getIntersectionPoint(ptDER, ptDER2, point3d1, point3d2);
        num = 1E-08 if(not MathHelper.smethod_119(point3d1, ptDER, ptDER2)) else MathHelper.calcDistance(point3d, point3d1);
        num3 = (distDerToEtp if(not distDerToEtp == None  and not math.isinf(distDerToEtp)) else 0) + num;
        num4 = max([startingMoc + moc / 100 * num3 * obstacle_0.MocMultiplier, minMoc]);
        resultList = []
        obstacleAreaResult = area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, num4, resultList);
        if len(resultList) == 0:
            return None
        num1 = resultList[0]
        num2 = resultList[1]
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            z = ptDER.get_Z() + 5 + pdg / 100 * num3;
            position = obstacle_0.Position;
            z1 = position.get_Z() + obstacle_0.Trees + num1;
            z2 = 100 * ((z1 - (ptDER.get_Z() + 5)) / num3);
            criticalObstacleType = CriticalObstacleType.No;
            if (z2 > pdg):
                criticalObstacleType = CriticalObstacleType.Yes;
            closeInObstacleType = CloseInObstacleType.No;
            if (z1 <= ptDER.get_Z() + 60):
                closeInObstacleType = CloseInObstacleType.Yes;
            if (storeDistances):
                drDzDoObstacleTag = None #DrDzDoObstacleTag(point3d, point3d1);
            else:
                drDzDoObstacleTag = None;
            drDzDoObstacleTag1 = drDzDoObstacleTag;
            return [obstacleAreaResult, num2, distDerToEtp, num, num1, z, z1, z2, criticalObstacleType, closeInObstacleType, drDzDoObstacleTag1]
        return None


class StepDownObstacles(ObstacleTable):
    def __init__(self, iobstacleArea_0, point3d_0, double_0, angleGradientSlope_0, altitude_0, altitude_1, altitude_2):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, None)
        
        self.area = iobstacleArea_0;
        self.tr = double_0;
        self.trm90 = MathHelper.smethod_4(self.tr - 1.5707963267949);
        self.ptFix = point3d_0;
        self.ptFixm90 = MathHelper.distanceBearingPoint(self.ptFix, self.trm90, 100);
        self.ptFix2 = MathHelper.distanceBearingPoint(self.ptFix, self.tr, 1000);
        self.startAlt = altitude_0.Metres - altitude_1.Metres;
        self.nextMoc = altitude_2.Metres;
        self.maxDist = Unit.ConvertNMToMeter(5);
        self.tanSlope = angleGradientSlope_0/ 100;
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
        self.IndexSurfAltM = fixedColumnCount + 5
        self.IndexSurfAltFt = fixedColumnCount + 6
        self.IndexDifferenceM = fixedColumnCount + 7
        self.IndexDifferenceFt = fixedColumnCount + 8
        self.IndexOcaM = fixedColumnCount + 9
        self.IndexOcaFt = fixedColumnCount + 10

        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DistInSecM,
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.SurfAltM,
                ObstacleTableColumnType.SurfAltFt,
                ObstacleTableColumnType.DifferenceM,
                ObstacleTableColumnType.DifferenceFt,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt
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
        self.source.setItem(row, self.IndexSurfAltM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[3])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[3]))
        self.source.setItem(row, self.IndexSurfAltFt, item)

        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4])
        self.source.setItem(row, self.IndexDifferenceM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[4])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[4]))
        self.source.setItem(row, self.IndexDifferenceFt, item)

        item = QStandardItem(str(checkResult[5]))
        item.setData(checkResult[5])
        self.source.setItem(row, self.IndexOcaM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[5])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[5]))
        self.source.setItem(row, self.IndexOcaFt, item)

    def checkObstacle(self, obstacle_0):
        point3d = None;
        obstacleAreaResult = ObstacleAreaResult.Outside;
        num = None;
        num1 = None;
        z = None;
        num2 = None;
        num3 = None;
        point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.tr, obstacle_0.Tolerance);
        point3d = MathHelper.getIntersectionPoint(self.ptFix, self.ptFix2, point3d1, MathHelper.distanceBearingPoint(point3d1, self.trm90, 100));
        if (MathHelper.smethod_119(point3d, self.ptFix, self.ptFixm90)):
            num4 = min([self.maxDist, MathHelper.calcDistance(self.ptFix, point3d)]);
            num2 = self.startAlt - num4 * self.tanSlope;
            z1 = obstacle_0.Position.get_Z() + obstacle_0.Trees;
            num3 = z1 - num2;
            mocMultiplier = self.nextMoc * obstacle_0.MocMultiplier;
            resultList = []
            obstacleAreaResult = self.area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier, resultList);
            if len(resultList) == 0:
                return
            num = resultList[0]
            num1 = resultList[1]
            if (obstacleAreaResult != ObstacleAreaResult.Outside and num3 > 0):
                position = obstacle_0.Position;
                z = position.get_Z() + obstacle_0.Trees + num;
                checkResult = [obstacleAreaResult, num1, num, num2, num3, z]
                self.addObstacleToModel(obstacle_0, checkResult)

class InitialMissedApproachObstacles(ObstacleTable):
    def __init__(self, iobstacleArea_0, point3d_0, double_0, distance_0, angleGradientSlope_0, altitude_0, altitude_1):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, None)

        self.area = iobstacleArea_0;
        self.tr = double_0;
        self.trm90 = MathHelper.smethod_4(self.tr - 1.5707963267949);
        self.tr180 = MathHelper.smethod_4(self.tr - 3.14159265358979);
        self.ptSoc = point3d_0;
        self.ptSocm90 = MathHelper.distanceBearingPoint(self.ptSoc, self.trm90, 100);
        self.ptMapt = MathHelper.distanceBearingPoint(self.ptSoc, self.tr180, distance_0.Metres);
        self.ptMaptm90 = MathHelper.distanceBearingPoint(self.ptMapt, self.trm90, 100);
        self.finalMoc = altitude_0.Metres;
        self.missedMoc = altitude_1.Metres;
        self.maxDist = distance_0.Metres;
        self.tanGradient = angleGradientSlope_0 / 100;
    def setHiddenColumns(self, tableView):
#         tableView.hideColumn(self.IndexObstArea)
#         tableView.hideColumn(self.IndexDistInSecM)
        return ObstacleTable.setHiddenColumns(self, tableView)
    def setHeaderLabels(self):

        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)

        self.IndexObstArea = fixedColumnCount
        self.IndexDistInSecM = fixedColumnCount + 1
        self.IndexDsocM = fixedColumnCount + 2
        self.IndexMocAppliedM = fixedColumnCount + 3
        self.IndexMocAppliedFt = fixedColumnCount + 4
        self.IndexMocMultiplier = fixedColumnCount + 5
        self.IndexOcaM = fixedColumnCount + 6
        self.IndexOcaFt = fixedColumnCount + 7

        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DistInSecM,
                ObstacleTableColumnType.DsocM,
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt
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
        self.source.setItem(row, self.IndexDsocM, item)

        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexMocAppliedM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[3])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[3]))
        self.source.setItem(row, self.IndexMocAppliedFt, item)

        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4])
        self.source.setItem(row, self.IndexOcaM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[4])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[4]))
        self.source.setItem(row, self.IndexOcaFt, item)

    def checkObstacle(self, obstacle_0):
        mocMultiplier = None;
        obstacleAreaResult = ObstacleAreaResult.Outside;
        num = None;
        num1 = None;
        num2 = None;
        z = None;
        point3d = MathHelper.distanceBearingPoint(obstacle_0.Position, self.tr180, obstacle_0.Tolerance);
        point3d = MathHelper.getIntersectionPoint(self.ptMapt, self.ptSoc, point3d, MathHelper.distanceBearingPoint(point3d, self.trm90, 100));
        if (not MathHelper.smethod_115(point3d, self.ptMapt, self.ptMaptm90)):
            num2 = MathHelper.calcDistance(self.ptSoc, point3d);
            if (not MathHelper.smethod_119(point3d, self.ptSoc, self.ptSocm90)):
                mocMultiplier = min([self.finalMoc, self.missedMoc + num2 * self.tanGradient]);
                self.ptSoc.get_Z();
            else:
                mocMultiplier = self.missedMoc;
                z1 = self.ptSoc.get_Z() + num2 * self.tanGradient;
        else:
            mocMultiplier = self.finalMoc;
            self.ptSoc.get_Z();
        mocMultiplier = mocMultiplier * obstacle_0.MocMultiplier;
        resultList = []
        obstacleAreaResult = self.area.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, mocMultiplier, resultList);
        if len(resultList) == 0:
            return
        num = resultList[0]
        num1 = resultList[1]
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            position = obstacle_0.Position;
            z = position.get_Z() + obstacle_0.Trees + num;
            z2 = obstacle_0.Position.get_Z() + obstacle_0.Trees;
            checkResult = [obstacleAreaResult, num1, num2, num, z]
            self.addObstacleToModel(obstacle_0, checkResult)
class MountainousTerrainAnalyserObstacles(ObstacleTable):
    def __init__(self, primaryArea):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, None)

        self.area = primaryArea;

    def checkObstacle(self, obstacle_0):
        if self.area.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance):
            ObstacleEvaluatorDlg.list.append(obstacle_0)