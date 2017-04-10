# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication, QString,QVariant
from PyQt4.QtGui import QMessageBox, QStandardItem, QFileDialog
from qgis.core import QgsPoint, QGis, QgsVectorLayer, QgsField, QgsPalLayerSettings

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, SurfaceTypes, ObstacleTableColumnType, AngleUnits, ConstructionType,\
    HeliportSurfacesApproachType, HeliportSurfacesApproachAngle, HeliportSurfacesApproachHeight, HeliportSurfacesUsage,\
    HeliportSurfacesSlopeCategory, TurnInvolvedType, Formating
from FlightPlanner.HeliportSurfaces.Ui_HeliportSurfacesAltitude import Ui_HeliportSurfacesAltitude
from FlightPlanner.HeliportSurfaces.Ui_HeliportSurfacesGeneral import Ui_HeliportSurfacesGeneral
from FlightPlanner.helpers import Altitude, Unit, MathHelper
from FlightPlanner.polylineArea import PolylineArea
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Captions import Captions
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.types import Point3D, Point3dCollection, OrientationType, ObstacleEvaluationMode
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable, Obstacle
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.Confirmations import Confirmations
from FlightPlanner.messages import Messages
from Type.switch import switch
from Type.SurfaceCriteria import HeliportSurfacesCriteriaList, HeliportSurfacesCriteria, HeliportSurfacesCriteriaStandard,\
    HeliportSurfacesCriteriaNonPrecision, HeliportSurfacesCriteriaPrecision, HeliportSurfacesCriteriaNonInstrument
from Type.Position import PositionType, Position
from Type.String import String, StringBuilder
from Type.Geometry import Line
from Type.Fato import FatoList, Fato
from Type.double import double
from Type.Extensions import Extensions

from FlightPlanner.Dialogs.DlgFato import DlgFato
from FlightPlanner.Dialogs.DlgAerodromeSurfaces import DlgAerodromeSurfaces
import define, math
class HeliportSurfacesDlg(FlightPlanBaseDlg):
    
    singleObstaclesChecked = 0
    multiObstaclesChecked = 0
    singleObstacles = None
    multiObstacles = None
    fatos = None
    criteriaList = None
    constructLayer = None

    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        # self.parametersPanelAltitude = None
        self.setObjectName("AerodromeSurfacesDlg")
        self.surfaceType = SurfaceTypes.HeliportSurfaces
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.HeliportSurfaces)
        self.resize(680, 610)
        QgisHelper.matchingDialogSize(self, 680, 500)
        self.surfaceList = None
        self.updating = False

        self.calculationResults = []

        self.resultLayerList = []

        self.arpFeatureArray = []
        self.currentLayer = None
        self.rwyFeatureArray = []
        # self.initAerodromeAndRwyCmb()
        
        #############  init part   #########
        self.parametersPanel.pnlApproachType.Items = HeliportSurfacesApproachType.Items
        self.parametersPanel.pnlApproachAngle.Items = HeliportSurfacesApproachAngle.Items
        self.parametersPanel.pnlHeightAboveFATO.Items = HeliportSurfacesApproachHeight.Items
        self.parametersPanel.pnlUsage.Items = HeliportSurfacesUsage.Items
        self.parametersPanel.pnlSlopeCategory.Items = HeliportSurfacesSlopeCategory.Items
        self.parametersPanelAltitude.pnlEvalMode.Items = ObstacleEvaluationMode.Items
        self.parametersPanel.pnlTurningApproach.Items = TurnInvolvedType.Items
        self.parametersPanel.pnlTurningTakeOff.Items = TurnInvolvedType.Items
        if (HeliportSurfacesDlg.singleObstacles == None):
            pass
            # HeliportSurfacesDlg.singleObstacles = HeliportSurfacesSingleObstacles()
        if (HeliportSurfacesDlg.multiObstacles == None):
            pass
            # HeliportSurfacesDlg.multiObstacles = new List<HeliportSurfaces.HeliportSurfacesMultiObstacles>()
        if (HeliportSurfacesDlg.fatos == None):
            HeliportSurfacesDlg.fatos = FatoList.smethod_0(self)
        if (HeliportSurfacesDlg.criteriaList == None):
            HeliportSurfacesDlg.criteriaList = HeliportSurfacesCriteriaList.smethod_0(self)

        if HeliportSurfacesDlg.fatos != None and len(HeliportSurfacesDlg.fatos) > 0:
            self.method_36(HeliportSurfacesDlg.fatos[0])
        if HeliportSurfacesDlg.criteriaList != None and len(HeliportSurfacesDlg.criteriaList) > 0:
            self.parametersPanel.pnlCriteria.Items = HeliportSurfacesDlg.criteriaList

    @staticmethod
    def HeliportSurfaces():
        HeliportSurfacesDlg.singleObstaclesChecked = 0
        HeliportSurfacesDlg.multiObstaclesChecked = 0
        HeliportSurfacesDlg.singleObstacles = None
        HeliportSurfacesDlg.multiObstacles = None
        HeliportSurfacesDlg.fatos = None
        HeliportSurfacesDlg.criteriaList = None

    def initObstaclesModel(self):
        self.obstaclesModel.MocMultiplier = 1
        return FlightPlanBaseDlg.initObstaclesModel(self)

    def initSurfaceCombo(self):
        self.method_34()
    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return  
        self.filterList = []
        self.filterList.append("")
        for surf in self.surfaceList:
            self.filterList.append(surf.Title)
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.BaroVNAV, self.ui.tblObstacles, self.filterList, parameterList, resultHideColumnNames)
#         self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
    
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("Final Approach && Take Off area (FATO)", str(self.parametersPanel.pnlFato.comboBox.currentText())))

        parameterList.append(("Parameters", "group"))
        if self.parametersPanel.pnlApproachType.SelectedIndex == 0:
            if self.parametersPanel.pnlTurningTakeOff.SelectedIndex == 1:
                parameterList.append(("Turning Take-off Climb In-bound Track", str(self.parametersPanel.pnlTurningTakeOffTrack.Value)))
                parameterList.append(("Turning Take-off Climb Center Position", "group"))
                parameterList.append(("Lat", self.parametersPanel.pnlTurningTakeOffCenter.txtLat.Value))
                parameterList.append(("Lon", self.parametersPanel.pnlTurningTakeOffCenter.txtLong.Value))
                parameterList.append(("X", self.parametersPanel.pnlTurningTakeOffCenter.txtPointX.text()))
                parameterList.append(("Y", self.parametersPanel.pnlTurningTakeOffCenter.txtPointY.text()))
            parameterList.append(("Take-off Climb Surface Involving a Turn", str(self.parametersPanel.pnlTurningTakeOff.comboBox.currentText())))

            if self.parametersPanel.pnlTurningTakeOff.SelectedIndex == 1:
                parameterList.append(("Turning Approach In-bound Track", str(self.parametersPanel.pnlTurningTakeOffTrack.Value)))
                parameterList.append(("Turning Approach Center Position", "group"))
                parameterList.append(("Lat", self.parametersPanel.pnlTurningApproachCenter.txtLat.Value))
                parameterList.append(("Lon", self.parametersPanel.pnlTurningApproachCenter.txtLong.Value))
                parameterList.append(("X", self.parametersPanel.pnlTurningApproachCenter.txtPointX.text()))
                parameterList.append(("Y", self.parametersPanel.pnlTurningApproachCenter.txtPointY.text()))
            parameterList.append(("Approach Surface Involving a Turn", str(self.parametersPanel.pnlTurningApproach.comboBox.currentText())))
            parameterList.append(("Slope Category", str(self.parametersPanel.pnlSlopeCategory.comboBox.currentText())))
            parameterList.append(("Usage", str(self.parametersPanel.pnlUsage.comboBox.currentText())))
        elif self.parametersPanel.pnlApproachType.SelectedIndex == 1:
            parameterList.append(("Usage", str(self.parametersPanel.pnlUsage.comboBox.currentText())))
        else:
            parameterList.append(("Height Above FATO", str(self.parametersPanel.pnlHeightAboveFATO.comboBox.currentText())))
            parameterList.append(("Approach Angle", str(self.parametersPanel.pnlApproachAngle.comboBox.currentText())))
        parameterList.append(("Approach Type", str(self.parametersPanel.pnlApproachType.comboBox.currentText())))

        parameterList.append(("Construction", "group"))
        parameterList.append(("Construction Type", str(self.parametersPanel.pnlConstructionType.SelectedItem)))

        parameterList.append(("Altitude of a Position / Results", "group"))
        parameterList.append(("Parameters", "group"))
        if self.parametersPanelAltitude.pnlEvalMode.SelectedIndex == 0:
            parameterList.append(("Insert Point And Text", str(self.parametersPanelAltitude.chbInsertPointAndText.Checked)))
            if self.parametersPanelAltitude.chbInsertPointAndText.Checked:
                parameterList.append(("Text Height", str(self.parametersPanelAltitude.pnlTextHeight.Value)))

            parameterList.append(("Position", "group"))
            parameterList.append(("Lat", self.parametersPanelAltitude.pnlEvalPosition.txtLat.Value))
            parameterList.append(("Lon", self.parametersPanelAltitude.pnlEvalPosition.txtLong.Value))
            parameterList.append(("X", self.parametersPanelAltitude.pnlEvalPosition.txtPointX.text()))
            parameterList.append(("Y", self.parametersPanelAltitude.pnlEvalPosition.txtPointY.text()))
            parameterList.append(("Altitude", self.parametersPanelAltitude.pnlEvalPosition.txtAltitudeM.text() + "m"))
            parameterList.append(("", self.parametersPanelAltitude.pnlEvalPosition.txtAltitudeFt.text() + "ft"))
        else:
            parameterList.append(("Evaluate Only Penetrating Obstacles", str(self.parametersPanelAltitude.chbOnlyPenetratingObstacles.Checked)))
        parameterList.append(("Mode", str(self.parametersPanelAltitude.pnlEvalMode.SelectedItem)))

        

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
    def btnEvaluate_Click(self):
        if len(self.surfaceList) == 0:
            return
        if (self.parametersPanelAltitude.pnlEvalMode.SelectedIndex != 0):
            title = []
            for i in range(len(self.surfaceList)):
                title.append("")
            for i in range(len(self.surfaceList)):
                title[i] = self.surfaceList[i].Title
            flagArray = []
            for i in range(len(title)):
                flagArray.append(False)
            for j in range(len(self.surfaceList)):
                flagArray[j] = True
            self.obstaclesModel = HeliportSurfacesMultiObstacles(self.surfaceList, self.parametersPanelAltitude.chbOnlyPenetratingObstacles.Checked)
            HeliportSurfacesDlg.multiObstacles = self.surfaceList
            return FlightPlanBaseDlg.btnEvaluate_Click(self)
        else:
            self.obstaclesModel = HeliportSurfacesSingleObstacles(self.surfaceList)
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

            positionDegree = QgisHelper.CrsTransformPoint(point.x(), point.y(), define._canvas.mapSettings().destinationCrs(),obstacleLayer.crs(), point3d.get_Z())


            obstacle = Obstacle(d, point3d, pointLayer.id(), 0, None, num1, ObstacleTable.MocMultiplier, num2)
            obstacle.positionDegree = positionDegree
            flag, string0 = self.obstaclesModel.method_0(obstacle, "")

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

    def btnConstruct_Click(self):
        # flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        # if not flag:
        #     return
        if self.parametersPanel.pnlConstructionType.SelectedItem == ConstructionType.Construct2D:
            HeliportSurfacesDlg.constructLayer = AcadHelper.createVectorLayer(self.surfaceType)
        else:
            HeliportSurfacesDlg.constructLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Polygon)
        
        selectedItem = self.parametersPanel.pnlFato.SelectedItem
        heliportSurfacesCriterium = self.selectedCriteria
        flag = False if(self.parametersPanel.pnlApproachType.SelectedIndex != 0) else self.parametersPanel.pnlTurningApproach.SelectedIndex == 1
        flag2 = flag
        point3d = self.parametersPanel.pnlTurningApproachCenter.Point3d if(flag) else Point3D.get_Origin()
        num = self.parametersPanel.pnlTurningApproachTrack.Value if(flag2) else double.NaN()
        flag1 = False if(self.parametersPanel.pnlApproachType.SelectedIndex != 0) else self.parametersPanel.pnlTurningTakeOff.SelectedIndex == 1
        flag3 = flag1
        point3d1 = self.parametersPanel.pnlTurningTakeOffCenter.Point3d if(flag1) else Point3D.get_Origin()
        num1 = self.parametersPanel.pnlTurningTakeOffTrack.Value if(flag3) else double.NaN()
        heliportSurfacesSurfaces =[ApproachSurface(selectedItem, heliportSurfacesCriterium, flag2, point3d, num),
                                TakeOffSurface(selectedItem, heliportSurfacesCriterium, flag3, point3d1, num1),
                                TransitionalSurface(selectedItem, heliportSurfacesCriterium)]
        title = []
        flagArray = []
        for i in range(len(heliportSurfacesSurfaces)):
            title.append("")
            flagArray.append(False)
        for i in range(len(heliportSurfacesSurfaces)):
            title[i] = heliportSurfacesSurfaces[i].Title

        for j in range(len(heliportSurfacesSurfaces)):
            flagArray[j] = True
        if (DlgAerodromeSurfaces.smethod_0(self, title, flagArray)):
            if (self.parametersPanel.pnlConstructionType.SelectedItem == ConstructionType.Construct2D) and self.parametersPanel.chbMarkAltitudes.Checked:
                value = self.parametersPanel.pnlAltitudesEvery.Value
                metres = 0.5 * (value.Metres / (heliportSurfacesCriterium.TransitionalSlope / float(100)))
                altitude = self.parametersPanel.pnlAltitudesEvery.Value
                str0 = ":{0}".format(self.parametersPanel.pnlAltitudesEvery.OriginalUnits)
                for heliportSurfacesSurface in heliportSurfacesSurfaces:
                    heliportSurfacesSurface.TextHeight = metres
                    heliportSurfacesSurface.AltitudeFormat = str0
            # Document activeDocument = AcadHelper.ActiveDocument
            # using (DocumentLock documentLock = activeDocument.LockDocument())
            # {
            #     using (Transaction transaction = activeDocument.get_Database().get_TransactionManager().StartTransaction())
            #     {
            #         HeliportSurfaces.transaction = transaction
            #         HeliportSurfaces.space = AcadHelper.smethod_32(1, transaction, activeDocument.get_Database())
            for k in range(len(heliportSurfacesSurfaces)):
                if (flagArray[k]):
                    if (self.parametersPanel.pnlConstructionType.SelectedItem!= ConstructionType.Construct3D):
                        heliportSurfacesSurfaces[k].vmethod_0(self.parametersPanel.chbMarkAltitudes.Checked, self.parametersPanel.pnlAltitudesEvery.Value)
                    else:
                        heliportSurfacesSurfaces[k].vmethod_1()

            if HeliportSurfacesDlg.constructLayer != None and isinstance(HeliportSurfacesDlg.constructLayer, QgsVectorLayer):
                QgisHelper.appendToCanvas(define._canvas, [HeliportSurfacesDlg.constructLayer], self.surfaceType)
                QgisHelper.zoomToLayers([HeliportSurfacesDlg.constructLayer])

                self.surfaceList = heliportSurfacesSurfaces
            else:
                self.surfaceList = []

            # transaction.Commit()
            # AcadHelper.smethod_5()
            #     }
            # }
            # base.method_19(Messages.CONSTRUCTION_FINISHED)



    def initParametersPan(self):
        ui0 = Ui_HeliportSurfacesGeneral()
        self.parametersPanel = ui0
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanelAltitude = Ui_HeliportSurfacesAltitude(self.ui.grbResult)
        self.ui.vlResultGroup.insertWidget(0, self.parametersPanelAltitude)

        self.ui.tabCtrlGeneral.setTabText(1, "Altitude of a Position / Results")
        self.ui.vlResultBtns.insertWidget(0, self.ui.btnEvaluate)
        self.ui.btnEvaluate.setEnabled(True)

        self.parametersPanel.pnlConstructionType.Items = [ConstructionType.Construct2D, ConstructionType.Construct3D]


        self.connect(self.parametersPanel.chbMarkAltitudes, SIGNAL("Event_0"), self.chbMarkAltitudes_Event_0)
        # self.connect(self.parametersPanelAltitude.chbInsertPointAndText, SIGNAL("Event_0"), self.chbInsertPointAndText_Event_0)
        self.connect(self.parametersPanel.pnlConstructionType, SIGNAL("Event_0"), self.pnlConstructionType_Event_0)
        # self.ui.tabCtrlGeneral.currentChanged.connect(self.tabControl_SelectedIndexChanged)
        self.connect(self.parametersPanel.pnlTurningApproach, SIGNAL("Event_0"), self.pnlTurningApproach_Event_0)
        # self.connect(self.parametersPanel.chbDepTrackMoreThan15, SIGNAL("Event_0"), self.chbDepTrackMoreThan15_Event_0)
        # self.connect(self.parametersPanel.pnlApproachObstacleAltitude, SIGNAL("Event_0"), self.pnlApproachObstacleAltitude_Event_0)
        # #
        self.connect(self.parametersPanel.pnlApproachType, SIGNAL("Event_0"), self.pnlApproachType_Event_0)
        self.connect(self.parametersPanel.pnlCriteria, SIGNAL("Event_0"), self.pnlCriteria_Event_0)
        self.connect(self.parametersPanel.pnlFato, SIGNAL("Event_0"), self.pnlFato_Event_0)
        # self.connect(self.parametersPanel.pnlCriteria, SIGNAL("Event_0"), self.pnlCriteria_Event_0)
        self.connect(self.parametersPanelAltitude.chbInsertPointAndText, SIGNAL("Event_0"), self.chbInsertPointAndText_Click0)
        # self.connect(self.parametersPanel.pnlDatumElevation, SIGNAL("Event_0"), self.pnlDatumElevation_Event_0)
        self.connect(self.parametersPanel.pnlTurningTakeOff, SIGNAL("Event_0"), self.pnlTurningTakeOff_Event_0)
        self.connect(self.parametersPanel.pnlTurningTakeOffTrack, SIGNAL("Event_0"), self.pnlTurningTakeOffTrack_Event_0)
        self.connect(self.parametersPanel.pnlTurningApproachTrack, SIGNAL("Event_0"), self.pnlTurningApproachTrack_Event_0)
        self.connect(self.parametersPanelAltitude.pnlEvalMode, SIGNAL("Event_0"), self.pnlEvalMode_Event_0)
        self.connect(self.parametersPanel.pnlTurningTakeOffCenter, SIGNAL("positionChanged"), self.pnlTurningTakeOffCenter_Event_1)
        self.connect(self.parametersPanel.pnlTurningApproachCenter, SIGNAL("positionChanged"), self.pnlTurningApproachCenter_Event_1)

        self.parametersPanel.btnCriteriaModify.clicked.connect(self.btnCriteriaModify_Click)
        self.parametersPanel.btnCriteriaRemove.clicked.connect(self.btnCriteriaRemove_Click)
        self.parametersPanel.btnFatoAdd.clicked.connect(self.btnFatoAdd_Click)
        self.parametersPanel.btnFatoModify.clicked.connect(self.btnFatoModify_Click)
        self.parametersPanel.btnFatoRemove.clicked.connect(self.btnFatoRemove_Click)
        self.chbMarkAltitudes_Event_0()
    def btnCriteriaModify_Click(self):
        if (self.parametersPanel.pnlCriteria.SelectedIndex < 0):
            return
        if (self.parametersPanel.pnlCriteria.SelectedIndex == 0):
            flag = self.parametersPanel.pnlApproachType.method_0()
            flag1 = flag
            if (flag):
                for case in switch(self.parametersPanel.pnlApproachType.SelectedIndex):
                    if case(0):
                        if (not self.parametersPanel.pnlUsage.method_0()):
                            flag1 = False
                        if (self.parametersPanel.pnlSlopeCategory.method_0()):
                            break
                        flag1 = False
                        break
                    elif case(1):
                        if (self.parametersPanel.pnlUsage.method_0()):
                            break
                        flag1 = False
                        break
                    elif case(2):
                        if (not self.parametersPanel.pnlApproachAngle.method_0()):
                            flag1 = False
                        if (self.parametersPanel.pnlHeightAboveFATO.method_0()):
                            break
                        flag1 = False
                        break
            if (not flag1):
                return
        heliportSurfacesCriterium = self.selectedCriteria

    def btnCriteriaRemove_Click(self):
        selectedItem = self.parametersPanel.pnlCriteria.SelectedItem
        if (selectedItem == None):
            return
        if isinstance(selectedItem, HeliportSurfacesCriteriaStandard):
            return
        if (QMessageBox.question(self, "Question", Confirmations.DELETE_CRITERIA.format(selectedItem.Name), QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes):
            num = self.parametersPanel.pnlCriteria.IndexOf(selectedItem)
            HeliportSurfacesDlg.criteriaList.Remove(num)
            HeliportSurfacesDlg.criteriaList.method_0(self)
            num = min(num, self.parametersPanel.pnlCriteria.Count - 1)
            self.method_37(num)
            self.method_33()

    def btnFatoAdd_Click(self):
        fato = Fato()
        self.dlgFato = DlgFato.smethod_0(self, fato)
        self.connect(self.dlgFato, SIGNAL("DlgFato_accept"), self.DlgFato_acceptEvent)

    def DlgFato_acceptEvent(self, fato):
        self.dlgFato.close()
        HeliportSurfacesDlg.fatos.Add(fato)
        HeliportSurfacesDlg.fatos.method_0(self)
        HeliportSurfacesDlg.fatos.method_1()
        self.method_36(fato)

    def btnFatoModify_Click(self):
        selectedItem = self.parametersPanel.pnlFato.SelectedItem
        if (selectedItem == None):
            return
        self.fatosIndex = HeliportSurfacesDlg.fatos.IndexOf(selectedItem)
        self.dlgFato = DlgFato.smethod_0(self, selectedItem)
        self.connect(self.dlgFato, SIGNAL("DlgFato_accept"), self.DlgFato_acceptEvent1)

    def DlgFato_acceptEvent1(self, fato):
        self.dlgFato.close()
        HeliportSurfacesDlg.fatos[self.fatosIndex] = fato
        HeliportSurfacesDlg.fatos.method_0(self)
        HeliportSurfacesDlg.fatos.method_1()
        self.method_36(fato)

    def btnFatoRemove_Click(self):
        selectedItem = self.parametersPanel.pnlFato.SelectedItem
        if (selectedItem == None):
            return
        if (QMessageBox.question(self, "Question", Confirmations.DELETE_FATO.format(selectedItem.FullName), QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes):
            num = self.parametersPanel.pnlFato.IndexOf(selectedItem)
            HeliportSurfacesDlg.fatos.Remove(num)
            HeliportSurfacesDlg.fatos.method_0(self)
            num = min(num, self.parametersPanel.pnlFato.Count - 1)
            self.method_35(num)

    def pnlFato_Event_0(self):
        self.method_41(self.parametersPanel.pnlFato)

    def pnlEvalMode_Event_0(self):
        self.method_41(self.parametersPanelAltitude.pnlEvalMode)


    def pnlConstructionType_Event_0(self):
        self.method_41(self.parametersPanel.pnlConstructionType)

    def pnlTurningTakeOffCenter_Event_1(self):
        self.method_41(self.parametersPanel.pnlTurningTakeOffCenter)

    def pnlTurningTakeOffTrack_Event_0(self):
        self.method_41(self.parametersPanel.pnlTurningTakeOffTrack)

    def pnlTurningTakeOff_Event_0(self):
        self.method_41(self.parametersPanel.pnlTurningTakeOff)

    def pnlTurningApproachTrack_Event_0(self):
        self.method_41(self.parametersPanel.pnlTurningApproachTrack)

    def pnlTurningApproachCenter_Event_1(self):
        self.method_41(self.parametersPanel.pnlTurningApproachCenter)

    def pnlTurningApproach_Event_0(self):
        self.method_41(self.parametersPanel.pnlTurningApproach)

    def pnlApproachType_Event_0(self):
        self.method_41(self.parametersPanel.pnlApproachType)

    def pnlCriteria_Event_0(self):
        self.method_41(self.parametersPanel.pnlCriteria)

    def chbMarkAltitudes_Event_0(self):
        self.parametersPanel.pnlAltitudesEvery.Enabled = self.parametersPanel.chbMarkAltitudes.Checked

    def chbInsertPointAndText_Click0(self):
        self.parametersPanelAltitude.pnlTextHeight.Enabled = self.parametersPanelAltitude.chbInsertPointAndText.Checked

    def method_31(self):
        pass
    
    def method_33(self):
        flag = False
        # self.gbParameters.SuspendLayout()
        # self.gbEvalParameters.SuspendLayout()
        # try
        # {
        # if (self.tabControl.SelectedIndex != 0)
        # {
        selectedIndex = self.parametersPanelAltitude.pnlEvalMode.SelectedIndex == 0
        self.parametersPanelAltitude.pnlEvalPosition.Visible = selectedIndex
        self.parametersPanelAltitude.pnlInsertPointAndText.Visible = selectedIndex
        self.parametersPanelAltitude.chbOnlyPenetratingObstacles.Visible = not selectedIndex
        # }
        # else
        # {
        selectedIndex1 = self.parametersPanel.pnlCriteria.SelectedIndex == 0
        flag1 = self.parametersPanel.pnlApproachType.SelectedIndex == 0
        selectedIndex2 = self.parametersPanel.pnlApproachType.SelectedIndex == 1
        flag2 = self.parametersPanel.pnlApproachType.SelectedIndex == 2
        self.parametersPanel.pnlApproachType.Visible = selectedIndex1
        self.parametersPanel.pnlApproachAngle.Visible = False if(not selectedIndex1) else flag2
        self.parametersPanel.pnlHeightAboveFATO.Visible = False if(not selectedIndex1) else flag2
        comboBoxPanel = self.parametersPanel.pnlUsage
        if (not selectedIndex1):
            flag = False
        else:
            flag = True if(flag1) else selectedIndex2
        comboBoxPanel.Visible = flag
        self.parametersPanel.pnlSlopeCategory.Visible = False if(not selectedIndex1) else flag1
        self.parametersPanel.pnlTurningApproach.Visible = False if(not selectedIndex1) else flag1
        self.parametersPanel.pnlTurningApproachCenter.Visible = False if(not selectedIndex1 or not flag1) else self.parametersPanel.pnlTurningApproach.SelectedIndex == 1
        self.parametersPanel.pnlTurningApproachTrack.Visible = False if(not selectedIndex1 or not flag1) else self.parametersPanel.pnlTurningApproach.SelectedIndex == 1
        self.parametersPanel.pnlTurningTakeOff.Visible = False if(not selectedIndex1) else flag1
        self.parametersPanel.pnlTurningTakeOffCenter.Visible = False if(not selectedIndex1 or not flag1) else self.parametersPanel.pnlTurningTakeOff.SelectedIndex == 1
        self.parametersPanel.pnlTurningTakeOffTrack.Visible = False if(not selectedIndex1 or not flag1) else self.parametersPanel.pnlTurningTakeOff.SelectedIndex == 1
        self.parametersPanel.pnlMarkAltitudes.Visible = self.parametersPanel.pnlConstructionType.Value == ConstructionType.Construct2D

        # }
        # finally
        # {
        #     self.gbParameters.ResumeLayout()
        #     self.gbEvalParameters.ResumeLayout()
        # }
    def method_34(self):
        if (self.parametersPanelAltitude.pnlEvalMode.SelectedIndex == 0):
            self.ui.frm_cmbObstSurface.setVisible(False)
            # self.gridObstacles.DataSource = HeliportSurfaces.singleObstacles
            return
        # self.gridObstacles.DataSource = null
        self.ui.frm_cmbObstSurface.setVisible(True)
        self.ui.cmbObstSurface.clear()
        if HeliportSurfacesDlg.multiObstacles == None:
            return
        for multiObstacle in HeliportSurfacesDlg.multiObstacles:
            self.ui.cmbObstSurface.addItem(multiObstacle.Title)
        if (self.ui.cmbObstSurface.count() > 0):
            self.ui.cmbObstSurface.setCurrentIndex(0)
            # self.gridObstacles.DataSource = HeliportSurfaces.multiObstacles[0]

    def method_35(self, int_0):
        self.updating = True
        if (self.parametersPanel.pnlFato.Items != []):
            self.parametersPanel.pnlFato.Clear()
        self.parametersPanel.pnlFato.Items = HeliportSurfacesDlg.fatos
        # self.pnlRunway.DisplayMember = "FullName"
        if (self.parametersPanel.pnlFato.Count > 0):
            int_0 = max(int_0, 0)
            int_0 = min(int_0, self.parametersPanel.pnlFato.Count - 1)
            self.parametersPanel.pnlFato.SelectedIndex = int_0
        self.method_39()
        self.updating = False

    def method_36(self, fato_0):
        self.updating = True
        if (self.parametersPanel.pnlFato.Items != []):
            self.parametersPanel.pnlFato.Clear()
        self.parametersPanel.pnlFato.Items = HeliportSurfacesDlg.fatos
        # self.parametersPanel.pnlRunway.DisplayMember = "FullName"
        self.parametersPanel.pnlFato.SelectedIndex = self.parametersPanel.pnlFato.IndexOf(fato_0)
        self.method_39()
        self.updating = False

    def method_37(self, int_0):
        self.updating = True
        if (self.parametersPanel.pnlCriteria.Items != []):
            self.parametersPanel.pnlCriteria.Clear()
        self.parametersPanel.pnlCriteria.Items = HeliportSurfacesDlg.criteriaList
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
        self.parametersPanel.pnlCriteria.Items = HeliportSurfacesDlg.criteriaList
        # self.pnlCriteria.DisplayMember = "Name"
        self.parametersPanel.pnlCriteria.SelectedIndex = self.parametersPanel.pnlCriteria.IndexOf(aerodromeSurfacesCriteria_0)
        self.method_40()
        self.updating = False
    def method_39(self):
        self.parametersPanel.btnFatoModify.setEnabled(self.parametersPanel.pnlFato.SelectedIndex > -1)
        self.parametersPanel.btnFatoRemove.setEnabled(self.parametersPanel.pnlFato.SelectedIndex > -1)
    def method_40(self):
        self.parametersPanel.btnCriteriaModify.setEnabled(self.parametersPanel.pnlCriteria.SelectedIndex > -1)
        self.parametersPanel.btnCriteriaRemove.setEnabled(self.parametersPanel.pnlCriteria.SelectedIndex > -1)

    def method_41(self, sender):
        if (sender != self.parametersPanelAltitude.pnlEvalMode):
            self.method_31()
        else:
            self.method_34()
        if (sender == self.parametersPanel.pnlFato):
            self.method_39()
        elif (sender == self.parametersPanel.pnlCriteria):
            self.method_40()
        self.method_33()

    def get_selectedCriteria(self):
        selectedItem = self.parametersPanel.pnlCriteria.SelectedItem
        if (selectedItem != None):
            for case in switch(self.parametersPanel.pnlApproachType.SelectedIndex):
                if case(0):
                    return HeliportSurfacesCriteriaNonInstrument(self.parametersPanel.pnlSlopeCategory.SelectedItem, self.parametersPanel.pnlUsage.SelectedItem)
                elif case(1):
                    return HeliportSurfacesCriteriaNonPrecision(self.parametersPanel.pnlUsage.SelectedItem)
                elif case(2):
                    return HeliportSurfacesCriteriaPrecision(self.parametersPanel.pnlApproachAngle.SelectedItem, self.parametersPanel.pnlHeightAboveFATO.SelectedItem)
        return selectedItem

    selectedCriteria = property(get_selectedCriteria, None, None, None)


class IHeliportSurfacesSurface:
    def __init__(self):
        self.centerLine = None
        self.area = None
        self.fatoDirection = None
        self.fatoDirectionP90 = None
        self.fatoDirectionM90 = None
        self.fatoDirectionP180 = None
        self.textHeight = None
        self.innerEdge = None
        self.fatoName = None
        self.layerName2D = None
        self.layerName3D = None
        self.title = None
        self.altitudeFormat = None

    def get_AltitudeFormat(self):
        return self.altitudeFormat
    def set_AltitudeFormat(self, value):
        self.altitudeFormat = value
    AltitudeFormat = property(get_AltitudeFormat, set_AltitudeFormat, None, None)

    def get_Area(self):
        return self.area
    Area = property(get_Area, None, None, None)

    def get_TextHeight(self):
        return self.textHeight
    def set_TextHeight(self, value):
        self.textHeight = value
    TextHeight = property(get_TextHeight, set_TextHeight, None, None)

    def get_Title(self):
        return self.title
    Title = property(get_Title, None, None, None)


    def method_0(self, string_0, obstacle_0, double_0, double_1):
        if (not String.IsNullOrEmpty(string_0)):
            string_0 = String.Concat([string_0, "\\P"])
        bELOW = Formating.BELOW
        if (double_1 >= 0):
            dIFFERENCE = Formating.DIFFERENCE
            altitude = Altitude(double_1)
            bELOW = dIFFERENCE.format(altitude.method_0(":u"))
        name = [obstacle_0.Name, None, None, None, None, None]
        position = obstacle_0.Position
        altitude1 = Altitude(position.get_Z() + obstacle_0.Trees)
        name[1] = altitude1.method_0(":u")
        name[2] = self.fatoName
        name[3] = self.title
        altitude2 = Altitude(double_0)
        name[4] = altitude2.method_0(":u")
        name[5] = bELOW
        string_0 = String.Concat([string_0, "{0}, {1}, {2} {3} ({4}), {5}".format(name[0], name[1], name[2], name[3], name[4], name[5])])
        return string_0

    def method_1(self, fato_0, heliportSurfacesCriteria_0):
        self.fatoName = fato_0.FullName
        self.layerName2D = AcadHelper.smethod_46("{0}_{1}_2D".format(fato_0.FullName, self.title))
        self.layerName3D = AcadHelper.smethod_46("{0}_{1}_3D".format(fato_0.FullName, self.title))
        self.fatoDirection = fato_0.Direction
        self.fatoDirectionM90 = MathHelper.smethod_4(self.fatoDirection - math.pi / 2)
        self.fatoDirectionP90 = MathHelper.smethod_4(self.fatoDirection + math.pi / 2)
        self.fatoDirectionP180 = MathHelper.smethod_4(self.fatoDirection + math.pi)
        self.method_2(heliportSurfacesCriteria_0)
        self.method_4(heliportSurfacesCriteria_0)
        fromCWY = False
        safetyAreaStart = 0.0
        safetyAreaEnd = 0.0
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaNonInstrument):
            fromCWY = heliportSurfacesCriteria_0.FromCWY
            safetyAreaStart = fato_0.SafetyAreaStart
            safetyAreaEnd = fato_0.SafetyAreaEnd
            self.innerEdge = fato_0.SafetyAreaWidth
        elif (not isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaNonPrecision)):
            if (not isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaPrecision)):
                raise  (Messages.ERR_UNSUPPORTED_CRITERIA)
            fromCWY = True
            safetyAreaStart = heliportSurfacesCriteria_0.ApproachDistFromEnd
            safetyAreaEnd = fato_0.SafetyAreaEnd
            self.innerEdge = heliportSurfacesCriteria_0.ApproachInnerEdge
        else:
            fromCWY = True
            safetyAreaStart = fato_0.SafetyAreaStart
            safetyAreaEnd = fato_0.SafetyAreaEnd
            self.innerEdge = heliportSurfacesCriteria_0.ApproachInnerEdge
        self.centerLine = Point3dCollection()
        self.centerLine.smethod_144(fato_0.Point3dCollection)
        self.centerLine.Insert(0, MathHelper.distanceBearingPoint(self.centerLine.get_Item(0), self.fatoDirectionP180, safetyAreaStart))
        if (fromCWY):
            if (not fato_0.method_4(PositionType.CWY)):
                self.centerLine.Add(MathHelper.distanceBearingPoint(self.centerLine.get_Item(self.centerLine.get_Count() - 1), self.fatoDirection, safetyAreaEnd))
            return
        if (fato_0.method_4(PositionType.CWY)):
            self.centerLine.RemoveAt(self.centerLine.get_Count() - 1)
        self.centerLine.Add(MathHelper.distanceBearingPoint(self.centerLine.get_Item(self.centerLine.get_Count() - 1), self.fatoDirection, safetyAreaEnd))

    def method_10(self, obstacle_0, point3dCollection_0, point3dCollection_1):
        # Point3d point3d
        # Point3d point3d1
        # Point3d point3d2
        # Point3d point3d3
        # Point3d point3d4
        # Point3d point3d5
        z = point3dCollection_1.get_Item(0).get_Z()
        for point3dCollection1 in point3dCollection_1:
            z = max(z, point3dCollection1.get_Z())
        point3d6 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.fatoDirection - math.pi, obstacle_0.Tolerance)
        position = obstacle_0.Position
        point3d7 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.fatoDirection, obstacle_0.Tolerance)
        for i in range(1, point3dCollection_0.get_Count()):
            item = point3dCollection_0.get_Item(i - 1)
            item1 = point3dCollection_0.get_Item(i)
            item2 = point3dCollection_1.get_Item(i - 1)
            item3 = point3dCollection_1.get_Item(i)
            point3d = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, self.fatoDirection - math.pi / 2, 100), item, item1)
            point3d1 = MathHelper.getIntersectionPoint(position, MathHelper.distanceBearingPoint(position, self.fatoDirection - math.pi / 2, 100), item, item1)
            point3d2 = MathHelper.getIntersectionPoint(point3d7, MathHelper.distanceBearingPoint(point3d7, self.fatoDirection - math.pi / 2, 100), item, item1)
            point3d3 = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, self.fatoDirection - math.pi / 2, 100), item2, item3)
            point3d4 = MathHelper.getIntersectionPoint(position, MathHelper.distanceBearingPoint(position, self.fatoDirection - math.pi / 2, 100), item2, item3)
            point3d5 = MathHelper.getIntersectionPoint(point3d7, MathHelper.distanceBearingPoint(point3d7, self.fatoDirection - math.pi / 2, 100), item2, item3)
            num = MathHelper.calcDistance(item, item1)
            num1 = MathHelper.calcDistance(item2, item3)
            if (MathHelper.smethod_110(point3d, item, item1)):
                z1 = item.get_Z() + MathHelper.calcDistance(item, point3d) * ((item1.get_Z() - item.get_Z()) / num)
                z2 = item2.get_Z() + MathHelper.calcDistance(item2, point3d3) * ((item3.get_Z() - item2.get_Z()) / num1)
                num2 = self.method_9(point3d.smethod_167(z1), point3d3.smethod_167(z2), point3d6, obstacle_0.Tolerance)
                z = min(num2, z)
            if (MathHelper.smethod_110(point3d1, item, item1)):
                z3 = item.get_Z() + MathHelper.calcDistance(item, point3d1) * ((item1.get_Z() - item.get_Z()) / num)
                num3 = item2.get_Z() + MathHelper.calcDistance(item2, point3d4) * ((item3.get_Z() - item2.get_Z()) / num1)
                num4 = self.method_9(point3d1.smethod_167(z3), point3d4.smethod_167(num3), position, obstacle_0.Tolerance)
                z = min(num4, z)
            if (MathHelper.smethod_110(point3d2, item, item1)):
                z4 = item.get_Z() + MathHelper.calcDistance(item, point3d2) * ((item1.get_Z() - item.get_Z()) / num)
                z5 = item2.get_Z() + MathHelper.calcDistance(item2, point3d5) * ((item3.get_Z() - item2.get_Z()) / num1)
                num5 = self.method_9(point3d2.smethod_167(z4), point3d5.smethod_167(z5), point3d7, obstacle_0.Tolerance)
                z = min(num5, z)
        return z

    def method_11(self, point3d_0, altitude_0, point3d_1, point3d_2, bool_0):
        dBText = AcadHelper.smethod_140(altitude_0.method_0(self.altitudeFormat), point3d_0.smethod_167(0), self.textHeight, 1, 1)
        num = MathHelper.getBearing(point3d_1, point3d_2)
        if (not MathHelper.smethod_136(num, AngleUnits.Radians)):
            num = num - math.pi
        dBText.set_Rotation(5 * math.pi / 2 - num)
        HeliportSurfacesDlg.constructLayer.setLayerName(self.layerName2D)
        AcadHelper.smethod_18(dBText, HeliportSurfacesDlg.constructLayer)
        if (bool_0):
            AcadHelper.smethod_18(Line(point3d_1.smethod_167(0), point3d_2.smethod_167(0)), HeliportSurfacesDlg.constructLayer)

    def method_12(self, point3d_0, altitude_0, double_0):
        dBText = AcadHelper.smethod_140(altitude_0.method_0(self.altitudeFormat), point3d_0.smethod_167(0), self.textHeight, 1, 1)
        if (not MathHelper.smethod_136(double_0, AngleUnits.Radians)):
            double_0 = double_0 - math.pi
        dBText.set_Rotation(5 * math.pi / 2 - double_0)
        HeliportSurfacesDlg.constructLayer.setLayerName(self.layerName2D)
        AcadHelper.smethod_18(dBText, HeliportSurfacesDlg.constructLayer)

    def method_13(self, point3d_0, point3d_1, point3d_2, point3d_3, altitude_0, double_0, double_1, double_2, bool_0, bool_1):
        # Point3d point3d
        # Point3d point3d1
        num = min(point3d_0.get_Z(), point3d_1.get_Z())
        metres = math.trunc(num / altitude_0.Metres) * altitude_0.Metres
        if (metres < num):
            metres = metres + altitude_0.Metres
        num1 = max(point3d_2.get_Z(), point3d_3.get_Z())
        point3d2 = MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_1), MathHelper.calcDistance(point3d_0, point3d_1) / 2)
        if (bool_0 or MathHelper.smethod_98(num, metres)):
            self.method_11(point3d2, Altitude(num), point3d_0, point3d_1, False)
        while (metres < num1):
            num2 = MathHelper.smethod_192(num, math.atan(double_0 / float(100)), metres, double_2, 0)
            if (num2 >= double_2):
                break
            point3d3 = MathHelper.distanceBearingPoint(point3d_0, double_1, num2)
            point3d4 = MathHelper.distanceBearingPoint(point3d_1, double_1, num2)
            point3d = MathHelper.getIntersectionPoint(point3d_0, point3d_2, point3d3, point3d4)
            point3d1 = MathHelper.getIntersectionPoint(point3d_1, point3d_3, point3d3, point3d4)
            point3d2 = MathHelper.distanceBearingPoint(point3d, MathHelper.getBearing(point3d, point3d1), MathHelper.calcDistance(point3d, point3d1) / 2)
            self.method_11(point3d2, Altitude(metres), point3d, point3d1, True)
            metres = metres + altitude_0.Metres
        point3d2 = MathHelper.distanceBearingPoint(point3d_2, MathHelper.getBearing(point3d_2, point3d_3), MathHelper.calcDistance(point3d_2, point3d_3) / 2)
        if (bool_1):
            self.method_11(point3d2, Altitude(num1), point3d_2, point3d_3, False)

    def method_14(self, point3dCollection_0, point3dCollection_1, altitude_0, double_0, double_1, int_0):
        # Point3d point3d
        count = point3dCollection_0.get_Count()
        for i in range(1, count):
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
                z1 = (item1.get_Z() - item.get_Z()) / (double_0 / float(100))
                num1 = (item2.get_Z() - point3d1.get_Z()) / (double_0 / float(100))
                while (metres < num):
                    num2 = MathHelper.smethod_192(item.get_Z(), math.atan(double_0 / float(100)), metres, z1, 0)
                    if (num2 >= z1):
                        break
                    num3 = MathHelper.smethod_192(point3d1.get_Z(), math.atan(double_0 / float(100)), metres, num1, 0)
                    if (num3 >= num1):
                        break
                    point3d2 = MathHelper.distanceBearingPoint(item, double_1, num2)
                    point3d3 = MathHelper.distanceBearingPoint(point3d1, double_1, num3)
                    if (num2 < 0):
                        point3d2 = MathHelper.getIntersectionPoint(item, point3d1, point3d2, point3d3)
                    if (num3 < 0):
                        point3d3 = MathHelper.getIntersectionPoint(item, point3d1, point3d2, point3d3)
                    HeliportSurfacesDlg.constructLayer.setLayerName(self.layerName2D)
                    AcadHelper.smethod_18(Line(point3d2.smethod_167(0), point3d3.smethod_167(0)), HeliportSurfacesDlg.constructLayer)
                    metres = metres + altitude_0.Metres
            else:
                point3d = MathHelper.getIntersectionPoint(point3d1, MathHelper.distanceBearingPoint(point3d1, self.fatoDirection + math.pi / 2, 100), item, MathHelper.distanceBearingPoint(item, self.fatoDirection, 100))
                num4 = MathHelper.calcDistance(point3d1, point3d)
                num5 = MathHelper.calcDistance(item, point3d)
                num6 = num4 / num5
                z2 = (point3d1.get_Z() - item.get_Z()) / num5 * 100
                num7 = (num - z) / (z2 / float(100))
                double0 = (num - z) / (double_0 / float(100))
                while (metres < num):
                    num8 = MathHelper.smethod_192(z, math.atan(z2 / float(100)), metres, num7, 0)
                    if (num8 >= num7):
                        pass
                    else:
                        num9 = MathHelper.smethod_192(z, math.atan(double_0 / float(100)), metres, double0, 0)
                        if (num9 >= double0):
                            pass
                        else:
                            point3d4 = MathHelper.distanceBearingPoint(item, MathHelper.getBearing(item, point3d1), num8 / math.cos(math.atan(num6)))
                            point3d5 = MathHelper.distanceBearingPoint(item, double_1, num9)
                            HeliportSurfacesDlg.constructLayer.setLayerName(self.layerName2D)
                            AcadHelper.smethod_18(Line(point3d4.smethod_167(0), point3d5.smethod_167(0)), HeliportSurfacesDlg.constructLayer)
                            metres = metres + altitude_0.Metres
            if (i == int_0):
                num10 = MathHelper.calcDistance(point3dCollection_0.get_Item(0), point3dCollection_1.get_Item(i))
                z = point3dCollection_0.get_Item(i).get_Z()
                metres = math.trunc(z / altitude_0.Metres) * altitude_0.Metres
                if (metres < z):
                    metres = metres + altitude_0.Metres
                num = point3dCollection_1.get_Item(i).get_Z()
                item3 = point3dCollection_0.get_Item(i)
                item4 = point3dCollection_0.get_Item(i)
                self.method_12(item3, Altitude(item4.get_Z()), self.fatoDirection)
                while (metres < num):
                    num11 = MathHelper.smethod_192(z, math.atan(double_0 / float(100)), metres, num10, 0)
                    if (num11 >= num10):
                        break
                    point3d6 = MathHelper.distanceBearingPoint(point3dCollection_0.get_Item(i), double_1, num11)
                    self.method_12(point3d6, Altitude(metres), self.fatoDirection)
                    metres = metres + altitude_0.Metres
                item5 = point3dCollection_1.get_Item(i)
                item6 = point3dCollection_1.get_Item(i)
                self.method_12(item5, Altitude(item6.get_Z()), self.fatoDirection)

    def method_15(self, orientationType_0, polyline_0, list_0, list_1, list_2, list_3):
        point3dCollection = Point3dCollection()
        num = math.pi / 2 if(orientationType_0 == OrientationType.Left) else -math.pi / 2
        item = self.innerEdge / float(2)
        num1 = MathHelper.getBearing(polyline_0.GetPoint3dAt(0), polyline_0.GetPoint3dAt(1))
        startPts = []
        pointAtDist = MathHelper.distanceBearingPoint(polyline_0.GetPointAtDist(0, startPts), num1 + num, item)
        point3dCollection.Add(pointAtDist)
        item1 = 0.0
        for i in range(len(list_0)):
            if (Extensions.smethod_18(list_0[i])):
                item = item + list_1[i] * (list_0[i] / float(100))
            item1 = item1 + list_1[i]
            # if (item1 < polyline_0.get_Length()):
            startPts = []
            pointAtDist = polyline_0.GetPointAtDist(item1, startPts)
            pointAtDist = MathHelper.distanceBearingPoint(pointAtDist, num1 + num, item)
            # else:
            #     pointAtDist = polyline_0.GetPointAtParameter(polyline_0.get_EndParam())
            #     pointAtDist = MathHelper.distanceBearingPoint(pointAtDist, num1 + num, item)
            point3dCollection.Add(pointAtDist)
        return point3dCollection

    def method_2(self, heliportSurfacesCriteria_0):
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaNonInstrument):
            return heliportSurfacesCriteria_0.Divergence
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaNonPrecision):
            return heliportSurfacesCriteria_0.ApproachDivergence
        if (not isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaPrecision)):
            raise (Messages.ERR_UNSUPPORTED_CRITERIA)
        return heliportSurfacesCriteria_0.ApproachDivergence1

    def method_3(self, heliportSurfacesCriteria_0):
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaNonInstrument):
            return heliportSurfacesCriteria_0.Slope1
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaNonPrecision):
            return heliportSurfacesCriteria_0.ApproachSlope
        if (not isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaPrecision)):
            raise (Messages.ERR_UNSUPPORTED_CRITERIA)
        return heliportSurfacesCriteria_0.ApproachSlope1

    def method_4(self, heliportSurfacesCriteria_0):
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaNonInstrument):
            return heliportSurfacesCriteria_0.Divergence
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaNonPrecision):
            return heliportSurfacesCriteria_0.TakeOffDivergence1
        if (not isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaPrecision)):
            raise (Messages.ERR_UNSUPPORTED_CRITERIA)
        return heliportSurfacesCriteria_0.TakeOffDivergence1

    def method_5(self, heliportSurfacesCriteria_0):
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaNonInstrument):
            return heliportSurfacesCriteria_0.Slope1
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaNonPrecision):
            return heliportSurfacesCriteria_0.TakeOffSlope1
        if (not isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaPrecision)):
            raise (Messages.ERR_UNSUPPORTED_CRITERIA)
        return heliportSurfacesCriteria_0.TakeOffSlope1

    def method_6(self):
        z = self.centerLine.get_Item(0).get_Z()
        for i in range(1, self.centerLine.get_Count()):
            item = self.centerLine.get_Item(i)
            z = min(z, item.get_Z())
        return z

    def method_7(self):
        z = self.centerLine.get_Item(0).get_Z()
        for i in range(1, self.centerLine.get_Count()):
            item = self.centerLine.get_Item(i)
            z = max(z, item.get_Z())
        return z

    def method_8(self, obstacle_0):
        # Point3d point3d
        # Point3d point3d1
        num = self.method_7()
        point3d2 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.fatoDirection - math.pi, obstacle_0.Tolerance)
        point3d3 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.fatoDirection, obstacle_0.Tolerance)
        for i in range(1, self.centerLine.get_Count()):
            item = self.centerLine.get_Item(i - 1)
            item1 = self.centerLine.get_Item(i)
            point3d = MathHelper.getIntersectionPoint(point3d2, MathHelper.distanceBearingPoint(point3d2, self.fatoDirection - math.pi / 2, 100), item, item1)
            point3d1 = MathHelper.getIntersectionPoint(point3d3, MathHelper.distanceBearingPoint(point3d3, self.fatoDirection - math.pi / 2, 100), item, item1)
            num1 = MathHelper.calcDistance(item, item1)
            if (MathHelper.smethod_110(point3d, item, item1)):
                z = item.get_Z() + MathHelper.calcDistance(item, point3d) * ((item1.get_Z() - item.get_Z()) / num1)
                num = min(z, num)
            if (MathHelper.smethod_110(point3d1, item, item1)):
                z1 = item.get_Z() + MathHelper.calcDistance(item, point3d1) * ((item1.get_Z() - item.get_Z()) / num1)
                num = min(z1, num)
        return num

    def method_9(self, point3d_0, point3d_1, point3d_2, double_0):
        num = max(MathHelper.calcDistance(point3d_0, point3d_2) - double_0, 0)
        num1 = MathHelper.calcDistance(point3d_0, point3d_1)
        if (MathHelper.smethod_96(num1)):
            return point3d_0.get_Z()
        return point3d_0.get_Z() + (point3d_1.get_Z() - point3d_0.get_Z()) / num1 * num

    def vmethod_0(self, bool_0, altitude_0):
        pass

    def vmethod_1(self):
        pass

    def vmethod_2(self, obstacle_0):
        pass
    # , out double double_0, out double double_1

class HeliportSurfacesSingleObstacles(ObstacleTable):
    def __init__(self, surfacesList = None):
        ObstacleTable.__init__(self, None)

        self.surfaces = surfacesList

    def setHiddenColumns(self, tableView):
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
        HeliportSurfacesDlg.singleObstaclesChecked = HeliportSurfacesDlg.singleObstaclesChecked + 1
        flag = False
        for surface in self.surfaces:
            result, num, num1 = surface.vmethod_2(obstacle_0)
            if (not result):
                continue
            criticalObstacleType = CriticalObstacleType.No
            if (num1 > 0):
                criticalObstacleType = CriticalObstacleType.Yes
            self.addObstacleToModel(obstacle_0, [surface.Title, num, num1, criticalObstacleType])
            string_0 = surface.method_0(string_0, obstacle_0, num, num1)
            flag = True
        return flag, string_0

class HeliportSurfacesMultiObstacles(ObstacleTable):
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
        HeliportSurfacesDlg.multiObstaclesChecked = HeliportSurfacesDlg.multiObstaclesChecked + 1
        num2 = 0
        for surface in self.surfaces:
            result, num, num1 = surface.vmethod_2(obstacle_0)
            if (result):
                criticalObstacleType = CriticalObstacleType.No
                if (num1 > 0):
                    criticalObstacleType = CriticalObstacleType.Yes
                if (not self.onlyPenetratingObstacles or (self.onlyPenetratingObstacles and criticalObstacleType == CriticalObstacleType.Yes)):
                    self.addObstacleToModel(obstacle_0, [num, num1, criticalObstacleType, surface.title])
                    # HeliportSurfaces.multiObstacles[num2].method_11(obstacle_0, num, num1, criticalObstacleType)
            num2 += 1

class ApproachSurface(IHeliportSurfacesSurface):
    # private Polyline centerPoly
    # 
    # private List<double> divergence
    # 
    # private List<double> divergenceLength
    # 
    # private List<double> outerWidth
    # 
    # private List<double> slope
    # 
    # private List<double> slopeLength
    # 
    # private double totalLength
    # 
    # private double direction

    def __init__(self, fato_0, heliportSurfacesCriteria_0, bool_0, point3d_0, double_0):
        IHeliportSurfacesSurface.__init__(self)
        
        self.title = Captions.APPROACH
        self.method_1(fato_0, heliportSurfacesCriteria_0)
        self.direction = fato_0.Direction + math.pi
        self.divergence = []
        self.divergenceLength = []
        self.slope = []
        self.slopeLength = []
        self.outerWidth = []
        self.totalLength = 0
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaNonInstrument):
            heliportSurfacesCriteria0 = heliportSurfacesCriteria_0
            self.totalLength = heliportSurfacesCriteria0.TotalLength
            self.divergence.append(heliportSurfacesCriteria0.Divergence)
            self.divergence.append(double.NaN())
            outerWidth = (heliportSurfacesCriteria0.OuterWidth - fato_0.SafetyAreaWidth) / float(2) / (heliportSurfacesCriteria0.Divergence / float(100))
            self.divergenceLength.append(outerWidth)
            self.divergenceLength.append(heliportSurfacesCriteria0.TotalLength - outerWidth)
            self.outerWidth.append(heliportSurfacesCriteria0.OuterWidth)
            self.outerWidth.append(heliportSurfacesCriteria0.OuterWidth)
            self.slope.append(heliportSurfacesCriteria0.Slope1)
            self.slope.append(heliportSurfacesCriteria0.Slope2)
            self.slope.append(double.NaN())
            self.slopeLength.append(heliportSurfacesCriteria0.Length1)
            self.slopeLength.append(heliportSurfacesCriteria0.Length2)
            self.slopeLength.append(double.NaN())
            point3d = MathHelper.distanceBearingPoint(fato_0.method_3(PositionType.START).Point3d, self.direction, fato_0.SafetyAreaStart)
            polylineArea = PolylineArea()
            polylineArea.method_1(point3d)
            polylineArea.method_1(MathHelper.distanceBearingPoint(point3d, self.direction, self.totalLength))
            self.centerPoly = AcadHelper.smethod_135_v15(polylineArea)
            return
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaNonPrecision):
            heliportSurfacesCriteriaNonPrecision = heliportSurfacesCriteria_0
            self.divergence.append(heliportSurfacesCriteriaNonPrecision.ApproachDivergence)
            self.divergenceLength.append(heliportSurfacesCriteriaNonPrecision.ApproachLength)
            self.slope.append(heliportSurfacesCriteriaNonPrecision.ApproachSlope)
            self.slopeLength.append(heliportSurfacesCriteriaNonPrecision.ApproachLength)
            self.outerWidth.append(self.innerEdge + 2 * (heliportSurfacesCriteriaNonPrecision.ApproachDivergence / float(100) * heliportSurfacesCriteriaNonPrecision.ApproachLength))
            self.totalLength = heliportSurfacesCriteriaNonPrecision.ApproachLength
            point3d1 = MathHelper.distanceBearingPoint(fato_0.method_3(PositionType.START).Point3d, self.direction, fato_0.SafetyAreaStart)
            polylineArea1 = PolylineArea()
            polylineArea1.method_1(point3d1)
            polylineArea1.method_1(MathHelper.distanceBearingPoint(point3d1, self.direction, self.totalLength))
            self.centerPoly = AcadHelper.smethod_135_v15(polylineArea1)
            return
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaPrecision):
            heliportSurfacesCriteriaPrecision = heliportSurfacesCriteria_0
            self.divergence.append(heliportSurfacesCriteriaPrecision.ApproachDivergence1)
            self.divergence.append(heliportSurfacesCriteriaPrecision.ApproachDivergence2)
            self.divergence.append(double.NaN())
            self.divergenceLength.append(heliportSurfacesCriteriaPrecision.ApproachLengthDivergence1)
            self.divergenceLength.append(heliportSurfacesCriteriaPrecision.ApproachLengthDivergence2)
            self.divergenceLength.append(heliportSurfacesCriteriaPrecision.ApproachTotalLength - heliportSurfacesCriteriaPrecision.ApproachLengthDivergence1 - heliportSurfacesCriteriaPrecision.ApproachLengthDivergence1)
            self.outerWidth.append(heliportSurfacesCriteriaPrecision.ApproachWidthDivergence1)
            self.outerWidth.append(heliportSurfacesCriteriaPrecision.ApproachWidthDivergence2)
            self.outerWidth.append(heliportSurfacesCriteriaPrecision.ApproachWidthDivergence2)
            self.slope.append(heliportSurfacesCriteriaPrecision.ApproachSlope1)
            self.slope.append(heliportSurfacesCriteriaPrecision.ApproachSlope2)
            self.slope.append(double.NaN())
            self.slopeLength.append(heliportSurfacesCriteriaPrecision.ApproachLengthSlope1)
            self.slopeLength.append(heliportSurfacesCriteriaPrecision.ApproachLengthSlope2)
            self.slopeLength.append(heliportSurfacesCriteriaPrecision.ApproachTotalLength - heliportSurfacesCriteriaPrecision.ApproachLengthSlope1 - heliportSurfacesCriteriaPrecision.ApproachLengthSlope1)
            self.totalLength = heliportSurfacesCriteriaPrecision.ApproachTotalLength
            point3d2 = MathHelper.distanceBearingPoint(fato_0.method_3(PositionType.START).Point3d, self.direction, heliportSurfacesCriteriaPrecision.ApproachDistFromEnd)
            polylineArea2 = PolylineArea()
            polylineArea2.method_1(point3d2)
            polylineArea2.method_1(MathHelper.distanceBearingPoint(point3d2, self.direction, self.totalLength))
            self.centerPoly = AcadHelper.smethod_135_v15(polylineArea2)

    def vmethod_0(self, bool_0, altitude_0):
        # AcadHelper.smethod_42(HeliportSurfaces.space.get_Database(), self.layerName2D, 4)
        point3dCollection = self.method_15(OrientationType.Left, self.centerPoly, self.divergence, self.divergenceLength, self.slope, self.slopeLength)
        point3dCollection1 = self.method_15(OrientationType.Right, self.centerPoly, self.divergence, self.divergenceLength, self.slope, self.slopeLength)
        point3dCollection2 = Point3dCollection()
        point3dCollection2.smethod_144(point3dCollection)
        point3dCollection2.smethod_144(point3dCollection1.smethod_153())
        HeliportSurfacesDlg.constructLayer.setLayerName(self.layerName2D)
        AcadHelper.smethod_18(AcadHelper.smethod_137_v15(point3dCollection2, True), HeliportSurfacesDlg.constructLayer)

    def vmethod_1(self):
        pass

    def vmethod_2(self, obstacle_0):
        double_0 = double.NaN()
        double_1 = double.NaN()
        return False, double_0, double_1

class TakeOffSurface(IHeliportSurfacesSurface):
    # private Polyline centerPoly
    # 
    # private List<double> divergence
    # 
    # private List<double> divergenceLength
    # 
    # private List<double> outerWidth
    # 
    # private List<double> slope
    # 
    # private List<double> slopeLength
    # 
    # private double totalLength
    # 
    # private double direction

    def __init__(self, fato_0, heliportSurfacesCriteria_0, bool_0, point3d_0, double_0):
        IHeliportSurfacesSurface.__init__(self)
        self.title = Captions.TAKE_OFF_CLIMB
        self.method_1(fato_0, heliportSurfacesCriteria_0)
        self.direction = fato_0.Direction
        self.divergence = []
        self.divergenceLength = []
        self.slope = []
        self.slopeLength = []
        self.outerWidth = []
        self.totalLength = 0
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaNonInstrument):
            heliportSurfacesCriteria0 = heliportSurfacesCriteria_0
            self.totalLength = heliportSurfacesCriteria0.TotalLength
            self.divergence.append(heliportSurfacesCriteria0.Divergence)
            self.divergence.append(double.NaN())
            outerWidth = (heliportSurfacesCriteria0.OuterWidth - fato_0.SafetyAreaWidth) / float(2) / (heliportSurfacesCriteria0.Divergence / float(100))
            self.divergenceLength.append(outerWidth)
            self.divergenceLength.append(heliportSurfacesCriteria0.TotalLength - outerWidth)
            self.outerWidth.append(heliportSurfacesCriteria0.OuterWidth)
            self.outerWidth.append(heliportSurfacesCriteria0.OuterWidth)
            self.slope.append(heliportSurfacesCriteria0.Slope1)
            self.slope.append(heliportSurfacesCriteria0.Slope2)
            self.slope.append(double.NaN())
            self.slopeLength.append(heliportSurfacesCriteria0.Length1)
            self.slopeLength.append(heliportSurfacesCriteria0.Length2)
            self.slopeLength.append(double.NaN())
            point3d = MathHelper.distanceBearingPoint(fato_0.method_3(PositionType.END).Point3d, self.direction, fato_0.SafetyAreaEnd)
            polylineArea = PolylineArea()
            polylineArea.method_1(point3d)
            polylineArea.method_1(MathHelper.distanceBearingPoint(point3d, self.direction, self.totalLength))
            self.centerPoly = AcadHelper.smethod_135_v15(polylineArea)
            return
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaNonPrecision):
            heliportSurfacesCriteriaNonPrecision = heliportSurfacesCriteria_0
            self.divergence.append(heliportSurfacesCriteriaNonPrecision.TakeOffDivergence1)
            self.divergence.append(heliportSurfacesCriteriaNonPrecision.TakeOffDivergence2)
            self.divergence.append(heliportSurfacesCriteriaNonPrecision.TakeOffDivergence3)
            self.divergenceLength.append(heliportSurfacesCriteriaNonPrecision.TakeOffLength1)
            self.divergenceLength.append(heliportSurfacesCriteriaNonPrecision.TakeOffLength2)
            self.divergenceLength.append(heliportSurfacesCriteriaNonPrecision.TakeOffLength3)
            self.outerWidth.append(heliportSurfacesCriteriaNonPrecision.TakeOffOuterWidth1)
            self.outerWidth.append(heliportSurfacesCriteriaNonPrecision.TakeOffOuterWidth2)
            self.outerWidth.append(heliportSurfacesCriteriaNonPrecision.TakeOffOuterWidth3)
            self.slope.append(heliportSurfacesCriteriaNonPrecision.TakeOffSlope1)
            self.slope.append(heliportSurfacesCriteriaNonPrecision.TakeOffSlope2)
            self.slope.append(heliportSurfacesCriteriaNonPrecision.TakeOffSlope3)
            self.slopeLength.append(heliportSurfacesCriteriaNonPrecision.TakeOffLength1)
            self.slopeLength.append(heliportSurfacesCriteriaNonPrecision.TakeOffLength2)
            self.slopeLength.append(heliportSurfacesCriteriaNonPrecision.TakeOffLength3)
            self.totalLength = heliportSurfacesCriteriaNonPrecision.TakeOffLength1 + heliportSurfacesCriteriaNonPrecision.TakeOffLength2 + heliportSurfacesCriteriaNonPrecision.TakeOffLength3
            point3d1 = MathHelper.distanceBearingPoint(fato_0.method_3(PositionType.END).Point3d, self.direction, fato_0.SafetyAreaEnd)
            polylineArea1 = PolylineArea()
            polylineArea1.method_1(point3d1)
            polylineArea1.method_1(MathHelper.distanceBearingPoint(point3d1, self.direction, self.totalLength))
            self.centerPoly = AcadHelper.smethod_135_v15(polylineArea1)
            return
        if isinstance(heliportSurfacesCriteria_0, HeliportSurfacesCriteriaPrecision):
            heliportSurfacesCriteriaPrecision = heliportSurfacesCriteria_0
            self.divergence.append(heliportSurfacesCriteriaPrecision.TakeOffDivergence1)
            self.divergence.append(heliportSurfacesCriteriaPrecision.TakeOffDivergence2)
            self.divergence.append(heliportSurfacesCriteriaPrecision.TakeOffDivergence3)
            self.divergenceLength.append(heliportSurfacesCriteriaPrecision.TakeOffLength1)
            self.divergenceLength.append(heliportSurfacesCriteriaPrecision.TakeOffLength2)
            self.divergenceLength.append(heliportSurfacesCriteriaPrecision.TakeOffLength3)
            self.outerWidth.append(heliportSurfacesCriteriaPrecision.TakeOffOuterWidth1)
            self.outerWidth.append(heliportSurfacesCriteriaPrecision.TakeOffOuterWidth2)
            self.outerWidth.append(heliportSurfacesCriteriaPrecision.TakeOffOuterWidth3)
            self.slope.append(heliportSurfacesCriteriaPrecision.TakeOffSlope1)
            self.slope.append(heliportSurfacesCriteriaPrecision.TakeOffSlope2)
            self.slope.append(heliportSurfacesCriteriaPrecision.TakeOffSlope3)
            self.slopeLength.append(heliportSurfacesCriteriaPrecision.TakeOffLength1)
            self.slopeLength.append(heliportSurfacesCriteriaPrecision.TakeOffLength2)
            self.slopeLength.append(heliportSurfacesCriteriaPrecision.TakeOffLength3)
            self.totalLength = heliportSurfacesCriteriaPrecision.TakeOffLength1 + heliportSurfacesCriteriaPrecision.TakeOffLength2 + heliportSurfacesCriteriaPrecision.TakeOffLength3
            point3d2 = MathHelper.distanceBearingPoint(fato_0.method_3(PositionType.END).Point3d, self.direction, fato_0.SafetyAreaEnd)
            polylineArea2 = PolylineArea()
            polylineArea2.method_1(point3d2)
            polylineArea2.method_1(MathHelper.distanceBearingPoint(point3d2, self.direction, self.totalLength))
            self.centerPoly = AcadHelper.smethod_135_v15(polylineArea2)

    def vmethod_0(self, bool_0, altitude_0):
        # AcadHelper.smethod_42(HeliportSurfaces.space.get_Database(), self.layerName2D, 9)
        point3dCollection = self.method_15(OrientationType.Left, self.centerPoly, self.divergence, self.divergenceLength, self.slope, self.slopeLength)
        point3dCollection1 = self.method_15(OrientationType.Right, self.centerPoly, self.divergence, self.divergenceLength, self.slope, self.slopeLength)
        point3dCollection2 = Point3dCollection()
        point3dCollection2.smethod_144(point3dCollection)
        point3dCollection2.smethod_144(point3dCollection1.smethod_153())
        HeliportSurfacesDlg.constructLayer.setLayerName(self.layerName2D)
        AcadHelper.smethod_18(AcadHelper.smethod_137_v15(point3dCollection2, True), HeliportSurfacesDlg.constructLayer)

    def vmethod_1(self):
        pass

    def vmethod_2(self, obstacle_0):
        double_0 = double.NaN()
        double_1 = double.NaN()
        return False, double_0, double_1
    
    
class TransitionalSurface(IHeliportSurfacesSurface):
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
    #
    # private double height
    #
    # private double divergenceApproach
    #
    # private double divergenceTakeOff
    #
    # private double slopeApproach
    #
    # private double slopeTakeOff

    def __init__(self, fato_0, heliportSurfacesCriteria_0):
        IHeliportSurfacesSurface.__init__(self)

        self.title = Captions.TRANSITIONAL
        self.method_1(fato_0, heliportSurfacesCriteria_0)
        self.slope = heliportSurfacesCriteria_0.TransitionalSlope
        self.height = heliportSurfacesCriteria_0.TransitionalHeight
        self.divergenceApproach = self.method_2(heliportSurfacesCriteria_0)
        self.divergenceTakeOff = self.method_4(heliportSurfacesCriteria_0)
        self.slopeApproach = self.method_3(heliportSurfacesCriteria_0)
        self.slopeTakeOff = self.method_5(heliportSurfacesCriteria_0)
        num = 0
        count = self.centerLine.get_Count() - 1
        num1 = self.height / (self.slopeApproach / float(100))
        num1 = num1 / math.cos(math.atan(self.divergenceApproach / float(100)))
        point3d = MathHelper.distanceBearingPoint(self.centerLine.get_Item(0), self.fatoDirectionM90, self.innerEdge / float(2))
        self.points1R = Point3dCollection()
        self.points1R.Add(MathHelper.distanceBearingPoint(point3d, self.fatoDirectionP180 + math.atan(self.divergenceApproach / float(100)), num1).smethod_167(point3d.get_Z() + self.height))
        for point3d1 in self.centerLine:
            self.points1R.Add(MathHelper.distanceBearingPoint(point3d1, self.fatoDirectionM90, self.innerEdge / float(2)))
        num1 = self.height / (self.slopeTakeOff / float(100))
        num1 = num1 / math.cos(math.atan(self.divergenceTakeOff / float(100)))
        point3d = MathHelper.distanceBearingPoint(self.centerLine.get_Item(count), self.fatoDirectionM90, self.innerEdge / float(2))
        self.points1R.Add(MathHelper.distanceBearingPoint(point3d, self.fatoDirection - math.atan(self.divergenceTakeOff / float(100)), num1).smethod_167(point3d.get_Z() + self.height))
        self.points2R = Point3dCollection()
        for i in range(self.points1R.get_Count()):
            item = self.points1R.get_Item(i)
            if (i != 0):
                if (i == self.points1R.get_Count() - 1):
                    self.points2R.Add(item)
                    continue
                else:
                    num1 = self.height / (self.slope / float(100))
                    self.points2R.Add(MathHelper.distanceBearingPoint(item, self.fatoDirectionM90, num1).smethod_167(item.get_Z() + self.height))
                    continue
            self.points2R.Add(item)
        num1 = self.height / (self.slopeApproach / float(100))
        num1 = num1 / math.cos(math.atan(self.divergenceApproach / float(100)))
        point3d = MathHelper.distanceBearingPoint(self.centerLine.get_Item(num), self.fatoDirectionP90, self.innerEdge / float(2))
        self.points1L = Point3dCollection()
        self.points1L.Add(MathHelper.distanceBearingPoint(point3d, self.fatoDirectionP180 - math.atan(self.divergenceApproach / float(100)), num1).smethod_167(point3d.get_Z() + self.height))
        for point3d2 in self.centerLine:
            self.points1L.Add(MathHelper.distanceBearingPoint(point3d2, self.fatoDirectionP90, self.innerEdge / float(2)))
        num1 = self.height / (self.slopeTakeOff / float(100))
        num1 = num1 / math.cos(math.atan(self.divergenceTakeOff / float(100)))
        point3d = MathHelper.distanceBearingPoint(self.centerLine.get_Item(count), self.fatoDirectionP90, self.innerEdge / float(2))
        self.points1L.Add(MathHelper.distanceBearingPoint(point3d, self.fatoDirection + math.atan(self.divergenceTakeOff / float(100)), num1).smethod_167(point3d.get_Z() + self.height))
        self.points2L = Point3dCollection()
        for j in range(self.points1L.get_Count()):
            item1 = self.points1L.get_Item(j)
            if (j != 0):
                if (j == self.points1L.get_Count() - 1):
                    self.points2L.Add(item1)
                    continue
                else:
                    num1 = self.height / (self.slope / float(100))
                    self.points2L.Add(MathHelper.distanceBearingPoint(item1, self.fatoDirectionP90, num1).smethod_167(item1.get_Z() + self.height))
                    continue
            self.points2L.Add(item1)
        self.areaR = Point3dCollection()
        for k in range(self.points2R.get_Count()):
            self.areaR.Add(self.points2R.get_Item(k))
        for l in range(self.points1R.get_Count()):
            i = self.points1R.get_Count() - 1 - l
            self.areaR.Add(self.points1R.get_Item(i))
        self.areaL = Point3dCollection()
        for m in range(self.points2L.get_Count()):
            self.areaL.Add(self.points2L.get_Item(m))
        for n in range(self.points1L.get_Count()):
            i = self.points1L.get_Count() - 1 - n
            self.areaL.Add(self.points1L.get_Item(i))
        self.area = Point3dCollection()
        for o in range(self.points2R.get_Count()):
            self.area.Add(self.points2R.get_Item(o))
        for p in range(self.points2L.get_Count()):
            i = self.points2L.get_Count() - 1 - p
            self.area.Add(self.points2L.get_Item(i))

    def vmethod_0(self, bool_0, altitude_0):
        # AcadHelper.smethod_42(HeliportSurfaces.space.get_Dataself(), self.layerName2D, 6)
        HeliportSurfacesDlg.constructLayer.setLayerName(self.layerName2D)
        AcadHelper.smethod_18(AcadHelper.smethod_137_v15(self.areaR, True), HeliportSurfacesDlg.constructLayer)
        AcadHelper.smethod_18(AcadHelper.smethod_137_v15(self.areaL, True), HeliportSurfacesDlg.constructLayer)
        if (bool_0):
            self.method_14(self.points1R, self.points2R, altitude_0, self.slope, self.fatoDirection - math.pi / 2, 2)
            self.method_14(self.points1L, self.points2L, altitude_0, self.slope, self.fatoDirection + math.pi / 2, 2)

    def vmethod_1(self):
        # AcadHelper.smethod_42(HeliportSurfaces.space.get_Dataself(), self.layerName3D, 6)
        HeliportSurfacesDlg.constructLayer.setLayerName(self.layerName3D)
        AcadHelper.smethod_153_v15(self.points1R, self.points2R, HeliportSurfacesDlg.constructLayer)
        AcadHelper.smethod_153_v15(self.points1L, self.points2L, HeliportSurfacesDlg.constructLayer)

    def vmethod_2(self, obstacle_0):
        double_0 = double.NaN()
        double_1 = double.NaN()
        if (MathHelper.pointInPolygon(self.areaR, obstacle_0.Position, obstacle_0.Tolerance)):
            z = obstacle_0.Position.get_Z() + obstacle_0.Trees
            double_0 = self.method_10(obstacle_0, self.points1R, self.points2R)
            double_1 = z - double_0
            return True, double_0, double_1
        if (not MathHelper.pointInPolygon(self.areaL, obstacle_0.Position, obstacle_0.Tolerance)):
            return False, double_0, double_1
        num = obstacle_0.Position.get_Z() + obstacle_0.Trees
        double_0 = self.method_10(obstacle_0, self.points1L, self.points2L)
        double_1 = num - double_0
        return True, double_0, double_1