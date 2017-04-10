# -*- coding: utf-8 -*-
'''
Created on Mar 24, 2015

@author: jin
'''

import math

from PyQt4.QtGui import QDialog, QMessageBox, QColor, QInputDialog, QAbstractItemView, QPushButton, QFont, QLineEdit, QComboBox, QFileDialog
from PyQt4.QtCore import QVariant, QSizeF, Qt, SIGNAL, QCoreApplication, QString

from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnapper
from qgis.core import QGis, QgsGeometry, QgsFeatureRequest, QgsRaster

from FlightPlanner.ExportDlg.ExportDlg import ExportDlg

from FlightPlanner.Polyline import Polyline
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.QgisHelper import QgisHelper, Geo
from FlightPlanner.RnpAR.ui_RnpDlg import Ui_RnpDialog
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.types import AircraftSpeedCategory, DistanceUnits, OCAHType, AngleGradientSlopeUnits, \
        RnpArSegmentType, RnpArLegType, Point3D, AltitudeUnits, SurfaceTypes, GeoCalculationType
from FlightPlanner.DataHelper import DataHelper    
from FlightPlanner.helpers import MathHelper, Speed, Altitude, AngleGradientSlope, \
        Distance, Unit
from FlightPlanner.RnpAR.RnpARSegments import RnpArLeg, RnpArLegs, RnpArSegmentObstacles,\
        RnpArCalculatedSegment, RnpArCalculatedSegments, RnpArFinalApproachSegment, \
        RnpArInitialApproachSegment, RnpArIntermediateApproachSegment, RnpArMissedApproachSegment, \
        RnpArVebComponents, RnpArTemperatureComponents
from FlightPlanner.RnpAR.RnpArLegDlg import RnpArLegDlg
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.messages import Messages
from Type.String import String

import define

class RnpARDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.ui = Ui_RnpDialog()
        self.ui.setupUi(self)
        self.surfaceType = SurfaceTypes.RnpAR

        QgisHelper.matchingDialogSize(self, 980, 600)
        ''' UI State Initialize '''
        self.ui.btnAddTF_MA.setEnabled(False)
        self.ui.btnAddTF_FA.setEnabled(True)
        self.ui.groupBox_3.setEnabled(True)
        self.ui.btnEvaluate.setEnabled(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        
        self.ui.groupBox_23.setVisible(False)
        self.pnlLTP = PositionPanel(self.ui.frame_18, None, self)
        self.pnlLTP.setObjectName("positionLTP")
        self.pnlLTP.btnCalculater.setVisible(False)
        self.pnlLTP.groupBox.setTitle("Landing / Fictitious Threshold Point (LTP / FTP)")
        self.ui.horizontalLayout_41.addWidget(self.pnlLTP)
        self.connect(self.pnlLTP, SIGNAL("positionChanged"), self.initResultPanel)
        
        self.ui.cmbCAT.addItems(["A", "B", "C", "D", "E"])
        self.ui.cmbFinalOCAH.addItems([OCAHType.OCA, OCAHType.OCH])
        self.ui.cmbFinalOCAH.currentIndexChanged.connect(self.cmbFinalOCAH_currentIndexChanged)
        self.ui.txtFinalOCAH.setText("200")
        
        self.ui.tblLegsFA.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblLegsMA.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblLegsIA.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblLegsI.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.ui.tblObstacles.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblObstacles.setSortingEnabled(True)
        self.ui.cmbSurface.addItems(["All", RnpArSegmentType.Missed, RnpArSegmentType.Final, RnpArSegmentType.Intermediate, RnpArSegmentType.Initial])
#         self.obstaclesModel = None
#         self.ui.tblObstacles.setModel(self.obstaclesModel)
        self.ui.cmbUnits.addItems(["Metres", "Feet"])
        self.ui.txtOCA.setText(OCAHType.OCA)
        self.ui.txtOCH.setText(OCAHType.OCH)
        
        font = QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.ui.btnOpenData = QPushButton("")
        self.ui.btnOpenData.setFont(font)
        self.ui.verticalLayout_7.insertWidget(0, self.ui.btnOpenData)
#         self.ui.btnOpenData.setDisabled(True)
        self.ui.btnSaveData = QPushButton("")        
        self.ui.btnSaveData.setFont(font)
        self.ui.verticalLayout_7.insertWidget(1, self.ui.btnSaveData)
#         self.ui.btnSaveData.setDisabled(True)
        self.ui.btnPDTCheck = QPushButton("")
        self.ui.btnPDTCheck.setFont(font)
        self.ui.verticalLayout_7.insertWidget(0, self.ui.btnPDTCheck)

        self.ui.btnExportResult = QPushButton("")
        self.ui.btnExportResult.setFont(font)
        self.ui.verticalLayout_4.insertWidget(2, self.ui.btnExportResult)
        # self.ui.btnExportResult.setDisabled(True)
        self.ui.btnExportResult.clicked.connect(self.exportResult)
        
        self.ui.btnOpenData.clicked.connect(self.openData)
        self.ui.btnSaveData.clicked.connect(self.saveData)
        
        self.ui.btnOpenData.setIcon(self.ui.iconOpen)
        self.ui.btnExportResult.setIcon(self.ui.iconExport)
        self.ui.btnPDTCheck.setIcon(self.ui.iconPDT)
        self.ui.btnSaveData.setIcon(self.ui.iconSave) 
        self.ui.btnExportResult.setToolTip("Export Result")
        self.ui.btnOpenData.setToolTip("Open Data")
        self.ui.btnSaveData.setToolTip("Save Data")
        self.ui.btnPDTCheck.setToolTip("PDT Check")

        
        ''' Set Initial Values to Parameters'''
        self.ui.txtAdElev.setText("40")
        self.ui.txtVPA.setText("3")
        self.ui.txtACT.setText("-5")
        self.ui.cmbCAT.setCurrentIndex(AircraftSpeedCategory.D)
#         self.pnlLTP.txtAltitudeM.setText("37.9")
#         self.ui.tblLegsFA.setHorizontalHeader()
        
        '''Event Handlers Connect'''
        self.pnlLTP.txtAltitudeM.textChanged.connect(self.smethod_5)
        self.ui.cmbCAT.currentIndexChanged.connect(self.smethod_4)
        self.ui.txtVPA.textChanged.connect(self.smethod_5)
        self.ui.tblLegsFA.clicked.connect(self.method_38)
        self.ui.tblLegsI.clicked.connect(self.method_38)
        self.ui.tblLegsIA.clicked.connect(self.method_38)
        self.ui.tblLegsMA.clicked.connect(self.method_38)
        self.ui.txtFAP.textChanged.connect(self.method_40)
        self.ui.txtMocMA50.textChanged.connect(self.method_40)
        self.ui.txMACG.textChanged.connect(self.method_40)
        self.ui.txtMocMA30.textChanged.connect(self.method_40)
        self.ui.txtFinalOCAH.textChanged.connect(self.method_40)
        self.ui.txtMocI.textChanged.connect(self.method_40)
        self.ui.txtMocIA.textChanged.connect(self.method_40)
        self.ui.cmbSurface.currentIndexChanged.connect(self.cmbSurfaceChanged)
        self.ui.cmbUnits.currentIndexChanged.connect(self.setResultOCAH)
        
        ''' Buttons Click Connect'''
        self.ui.btnClose.clicked.connect(self.reject)
        self.ui.btnClose_2.clicked.connect(self.reject)
        self.ui.btnAddRF_IA.clicked.connect(self.btnAddRF_IA_Click)
        self.ui.btnAddRF_FA.clicked.connect(self.btnAddRF_IA_Click)
        self.ui.btnAddRF_I.clicked.connect(self.btnAddRF_IA_Click)
        self.ui.btnAddRF_MA.clicked.connect(self.btnAddRF_IA_Click)
        self.ui.btnAddTF_IA.clicked.connect(self.btnAddTF_IA_Click)
        self.ui.btnAddTF_FA.clicked.connect(self.btnAddTF_IA_Click)
        self.ui.btnAddTF_I.clicked.connect(self.btnAddTF_IA_Click)
        self.ui.btnAddTF_MA.clicked.connect(self.btnAddTF_IA_Click)
        self.ui.btnConstruct.clicked.connect(self.btnConstructClicked)
        self.ui.btnModify_FA.clicked.connect(self.btnModifyRF_IA_Click)
        self.ui.btnModify_I.clicked.connect(self.btnModifyRF_IA_Click)
        self.ui.btnModify_MA.clicked.connect(self.btnModifyRF_IA_Click)
        self.ui.btnModify_IA.clicked.connect(self.btnModifyRF_IA_Click)
        self.ui.btnRemove_FA.clicked.connect(self.btnRemoveRF_IA_Click)
        self.ui.btnRemove_I.clicked.connect(self.btnRemoveRF_IA_Click)
        self.ui.btnRemove_MA.clicked.connect(self.btnRemoveRF_IA_Click)
        self.ui.btnRemove_IA.clicked.connect(self.btnRemoveRF_IA_Click)
        self.ui.btnFAP.clicked.connect(self.btnFAPClicked)
        self.ui.btnEvaluate.clicked.connect(self.btnEvaluateClicked)
        self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheckClicked)
        
        self.smethod_4()
        
        ''' Member variables initialize '''
        self.rnpArDataGroup = RnpArDataGroup()
        self.defaultRnpValueMA = 0.3
        self.defaultRnpValueFA = 0.3
        self.defaultRnpValueI = 1
        self.defaultRnpValueIA = 1
        self.obstaclesModel = None
        self.method_31()
        
        lstTextControls = self.ui.groupBox_11.findChildren(QLineEdit)
        for ctrl in lstTextControls:
            ctrl.textChanged.connect(self.initResultPanel)

        lstTextControls = self.ui.groupBox_11.findChildren(QComboBox)
        for ctrl in lstTextControls:
            ctrl.currentIndexChanged.connect(self.initResultPanel)
        lstComboControls = self.ui.groupBox_11.findChildren(QComboBox)
        for ctrl in lstComboControls:
            ctrl.currentIndexChanged.connect(self.initResultPanel)

    def cmbFinalOCAH_currentIndexChanged(self):
        if self.ui.cmbFinalOCAH.currentIndex() == 1:
                self.ui.txtFinalOCAH.setText(str(round(float(self.ui.txtFinalOCAH.text()) - Unit.ConvertMeterToFeet(self.pnlLTP.Point3d.get_Z()), 2)))
        else:
            self.ui.txtFinalOCAH.setText(str(round(float(self.ui.txtFinalOCAH.text()) + Unit.ConvertMeterToFeet(self.pnlLTP.Point3d.get_Z()), 2)))

    def initResultPanel(self):
        if self.obstaclesModel != None and self.ui.btnEvaluate.isEnabled():
            self.obstaclesModel.clear()
            
            lstTextControls = self.ui.groupBox.findChildren(QLineEdit)
            for ctrl in lstTextControls:
                if ctrl.objectName() == "txtOCH" or ctrl.objectName() == "txtOCA":
                    continue
                ctrl.setText("")
        self.ui.btnEvaluate.setEnabled(False)
        self.ui.btnExportResult.setEnabled(False)
        
    def hideLegTablesColumns(self):
        self.ui.tblLegsFA.hideColumn(5)
        self.ui.tblLegsFA.hideColumn(7)
        self.ui.tblLegsMA.hideColumn(5)
        self.ui.tblLegsMA.hideColumn(7)
        self.ui.tblLegsIA.hideColumn(5)
        self.ui.tblLegsIA.hideColumn(7)
        self.ui.tblLegsI.hideColumn(5)
        self.ui.tblLegsI.hideColumn(7)
        
    def btnPDTCheckClicked(self):
        messagePDT = ""
        try:
            self.receiveRnpArInputData()
            rnpArFinalApproachSegment = RnpArFinalApproachSegment(self.rnpArDataGroup)
            item = self.rnpArDataGroup.Legs_FA[self.rnpArDataGroup.Legs_FA.Count - 1];
            if (not item.IsFAP):
                raise UserWarning, Messages.ERR_RNP_AR_NO_FAP
            point3d = item.Position
            rnpArLeg, num = rnpArFinalApproachSegment.method_1(self.rnpArDataGroup, -1)
    
            if (MathHelper.calcDistance(point3d, rnpArLeg.Position) > 100):
                raise UserWarning, Messages.ERR_RNP_AR_FAP_CHECK
            
            messagePDT += "fte:\t" + str(rnpArFinalApproachSegment.veb.fte.Metres) + " m\n"
            messagePDT += "atis:\t" + str(rnpArFinalApproachSegment.veb.atis.Metres) + " m\n"
            messagePDT += "anpe:\t" + str(rnpArFinalApproachSegment.veb.anpe.Metres) + " m\n"
            messagePDT += "wpr:\t" + str(rnpArFinalApproachSegment.veb.wpr.Metres) + " m\n"
            messagePDT += "ase75:\t" + str(rnpArFinalApproachSegment.veb.ase75.Metres) + " m\n"
            messagePDT += "aseFAP:\t" + str(rnpArFinalApproachSegment.veb.aseFAP.Metres) + " m\n"
            messagePDT += "vae75:\t" + str(rnpArFinalApproachSegment.veb.vae75.Metres) + " m\n"
            messagePDT += "vaeFAP:\t" + str(rnpArFinalApproachSegment.veb.vaeFAP.Metres) + " m\n"
            messagePDT += "isad75:\t" + str(rnpArFinalApproachSegment.veb.isad75.Metres) + " m\n"
            
            messagePDT += "isadFAP:\t" + str(rnpArFinalApproachSegment.veb.isadFAP.Metres) + " m\n"
            messagePDT += "bg(TF):\t" + str(rnpArFinalApproachSegment.veb.bg_TF.Metres) + " m\n"
            messagePDT += "bg(RF):\t" + str(rnpArFinalApproachSegment.veb.bg_RF.Metres) + " m\n"
            messagePDT += "moc75(TF):\t" + str(rnpArFinalApproachSegment.veb.moc75_TF.Metres) + " m\n"
            messagePDT += "moc75(RF):\t" + str(rnpArFinalApproachSegment.veb.moc75_RF.Metres) + " m\n"
            messagePDT += "mocFAP(TF):\t" + str(rnpArFinalApproachSegment.veb.mocFAP_TF.Metres) + " m\n"
            messagePDT += "mocFAP(RF):\t" + str(rnpArFinalApproachSegment.veb.mocFAP_RF.Metres) + " m\n"
            messagePDT += "OAS gradient(TF):\t" + str(rnpArFinalApproachSegment.veb.OASgradient_TF.Degrees) + " degree\n"
            messagePDT += "OAS gradient(RF):\t" + str(rnpArFinalApproachSegment.veb.OASgradient_RF.Degrees) + " degree\n"

            messagePDT += "OAS ORIGIN (TF):\t" + str(rnpArFinalApproachSegment.veb.OASorigin_TF.Metres) + " m\n"
            messagePDT += "OAS ORIGIN (RF):\t" + str(rnpArFinalApproachSegment.veb.OASorigin_RF.Metres) + " m\n"
            if (rnpArFinalApproachSegment.dFrop150.IsValid()):
                messagePDT += "FROP 150 m:\t" + str(rnpArFinalApproachSegment.dFrop150.Metres) + " m\n"
            if (rnpArFinalApproachSegment.dFrop15s.IsValid()):
                messagePDT += "FROP OCH (15 s):\t" + str(rnpArFinalApproachSegment.dFrop15s.Metres) + " m\n"
            if (rnpArFinalApproachSegment.dFrop50s.IsValid()):
                messagePDT += "FROP OCH (50 s):\t" + str(rnpArFinalApproachSegment.dFrop50s.Metres) + " m\n"
            QMessageBox.warning(self, "Information", messagePDT)
        except UserWarning as e:
            QMessageBox.warning(self, "Warning", e.message)
        
    def cmbSurfaceChanged(self):
        if self.obstaclesModel == None:
            return
        if self.ui.cmbSurface.currentIndex() == 0 and self.ui.cmbSurface.currentText() == "All":
            self.obstaclesModel.setFilterFixedString("")
        else:
            self.obstaclesModel.setFilterFixedString(self.ui.cmbSurface.currentText())
        
    def btnEvaluateClicked(self):
        try:
            self.obstaclesModel = RnpArSegmentObstacles(self.rnpArDataGroup, self.rnpArCalculatedSegment)
            rnpArMapLayers = QgisHelper.getSurfaceLayers(SurfaceTypes.RnpAR)
            self.obstaclesModel.loadObstacles(rnpArMapLayers)
            self.obstaclesModel.setLocateBtn(self.ui.btnEvaluate_2)
            self.ui.tblObstacles.setModel(self.obstaclesModel)
            self.obstaclesModel.setTableView(self.ui.tblObstacles)
            self.obstaclesModel.setHiddenColumns(self.ui.tblObstacles)
            self.ui.cmbSurface.setCurrentIndex(1)
            self.ui.tabBaroV.setCurrentIndex(1)            
            self.setResultOCAH()
            self.ui.btnExportResult.setEnabled(True)
            # raise ValueError, ""
        except UserWarning as e:
            QMessageBox.warning(self, "Information", e.message)

    def setResultOCAH(self):
        if self.ui.cmbUnits.currentIndex() == AltitudeUnits.M:
            self.ui.txtOCAResults.setText(str(round(RnpArSegmentObstacles.resultOCA.Metres)) + " m")
            self.ui.txtOCHResults.setText(str(round(RnpArSegmentObstacles.resultOCH.Metres)) + " m") 
        else:
            self.ui.txtOCAResults.setText(str(round(RnpArSegmentObstacles.resultOCA.Feet)) + " ft")
            self.ui.txtOCHResults.setText(str(round(RnpArSegmentObstacles.resultOCH.Feet)) + " ft") 
            
    def btnFAPClicked(self):
        if self.ui.txtFAP.text() == "":
            return
        self.receiveRnpArInputData()
        num = -1
        rnpArFinalApproachSegment = RnpArFinalApproachSegment(self.rnpArDataGroup)
        try:
            rnpArLeg, num = rnpArFinalApproachSegment.method_1(self.rnpArDataGroup, num)
            dlgRnpArLeg = RnpArLegDlg(self, self.rnpArDataGroup, rnpArLeg)
            if dlgRnpArLeg.exec_():
                if (num > -1):
                    while (self.rnpArDataGroup.Legs_FA.Count > num):
                        self.rnpArDataGroup.Legs_FA.RemoveAt(num)
                self.rnpArDataGroup.Legs_FA.Add(rnpArLeg)
                if self.rnpArDataGroup.Legs_FA.Count > 1:
                    self.rnpArDataGroup.Legs_FA.setData(self.rnpArDataGroup.Legs_FA.index(self.rnpArDataGroup.Legs_FA.Count - 2, RnpArLegs.ColIsFAP), QVariant(0))
                self.method_29()
            self.method_38()
        finally:
            rnpArFinalApproachSegment.method_0()
        
    def btnRemoveRF_IA_Click(self):
        tabIndex = self.ui.tabControlSegments.currentIndex()
        if (tabIndex == 1):
            self.rnpArDataGroup.Legs_MA.removeEndRow()
        elif (tabIndex == 2):
            self.rnpArDataGroup.Legs_FA.removeEndRow()
        elif (tabIndex == 3):
            self.rnpArDataGroup.Legs_I.removeEndRow()
        elif (tabIndex == 4):
            self.rnpArDataGroup.Legs_IA.removeEndRow()
            
        self.method_38()
        self.method_29()
        
    def btnModifyRF_IA_Click(self):
        tabIndex = self.ui.tabControlSegments.currentIndex()
        if (tabIndex == 1):
            selectedIdx = self.ui.tblLegsMA.selectedIndexes()
            if (len(selectedIdx) == self.rnpArDataGroup.Legs_MA.ColumnCount - 2):
                row = selectedIdx[0].row()
                rnpArLeg = self.rnpArDataGroup.Legs_MA[row]
                dlg = RnpArLegDlg(self, self.rnpArDataGroup, rnpArLeg, self.rnpArDataGroup.method_5(RnpArSegmentType.Missed, rnpArLeg), False)
                if dlg.exec_() == QDialog.Accepted:
                    self.method_29()

        elif (tabIndex == 2):
            selectedIdx = self.ui.tblLegsFA.selectedIndexes()
            if (len(selectedIdx) == self.rnpArDataGroup.Legs_FA.ColumnCount - 2):
                row = selectedIdx[0].row()
                rnpArLeg = self.rnpArDataGroup.Legs_FA[row]
                altitude = self.rnpArDataGroup.method_5(RnpArSegmentType.Final, rnpArLeg)
                dlg = RnpArLegDlg(self, self.rnpArDataGroup,rnpArLeg, altitude, False if row != self.rnpArDataGroup.Legs_FA.Count - 1 else self.rnpArDataGroup.Legs_I.Count == 0)
                if dlg.exec_() == QDialog.Accepted:
                    self.method_29()

        elif (tabIndex == 3):
            selectedIdx = self.ui.tblLegsI.selectedIndexes()
            if (len(selectedIdx) == self.rnpArDataGroup.Legs_I.ColumnCount - 2):
                row = selectedIdx[0].row()
                rnpArLeg = self.rnpArDataGroup.Legs_I[row]
                altitude = self.rnpArDataGroup.method_5(RnpArSegmentType.Intermediate, rnpArLeg)
                dlg = RnpArLegDlg(self, self.rnpArDataGroup,rnpArLeg, altitude, False)
                if dlg.exec_() == QDialog.Accepted:
                    self.method_29()
        elif (tabIndex == 4):
            selectedIdx = self.ui.tblLegsIA.selectedIndexes()
            if (len(selectedIdx) == self.rnpArDataGroup.Legs_IA.ColumnCount - 2):
                row = selectedIdx[0].row()
                rnpArLeg = self.rnpArDataGroup.Legs_IA[row]
                altitude = self.rnpArDataGroup.method_5(RnpArSegmentType.Initial, rnpArLeg)
                dlg = RnpArLegDlg(self, self.rnpArDataGroup,rnpArLeg, altitude, False)
                if dlg.exec_() == QDialog.Accepted:
                    self.method_29()

        self.method_38()
    def btnConstructClicked(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        try:
            self.receiveRnpArInputData()
            if self.rnpArDataGroup.FAP == None:
                raise UserWarning, "FAP Altitude is nothing!"
            if self.rnpArDataGroup.Legs_FA.RowCount == 0:
                raise UserWarning, "It does not exist any legs!"
            if self.rnpArDataGroup.Legs_FA[self.rnpArDataGroup.Legs_FA.RowCount - 1].IsFAP != True:
                raise UserWarning, "It does not exist FAP Leg!"
            rnpArFinalApproachSegment = RnpArFinalApproachSegment(self.rnpArDataGroup)
            item = self.rnpArDataGroup.Legs_FA[self.rnpArDataGroup.Legs_FA.Count - 1];
            if (not item.IsFAP):
                raise UserWarning, Messages.ERR_RNP_AR_NO_FAP
            point3d = item.Position
            rnpArLeg, num = rnpArFinalApproachSegment.method_1(self.rnpArDataGroup, -1)
    
            if (MathHelper.calcDistance(point3d, rnpArLeg.Position) > 100):
                raise UserWarning, Messages.ERR_RNP_AR_FAP_CHECK
            self.rnpArCalculatedSegment = RnpArCalculatedSegments()
            self.rnpArCalculatedSegment.append(rnpArFinalApproachSegment)
            if (self.rnpArDataGroup.Legs_MA.Count > 0):
                self.rnpArCalculatedSegment.insert(0, RnpArMissedApproachSegment(self.rnpArDataGroup))
            if (self.rnpArDataGroup.Legs_I.Count > 0):
                self.rnpArCalculatedSegment.append(RnpArIntermediateApproachSegment(self.rnpArDataGroup));
            if (self.rnpArDataGroup.Legs_IA.Count > 0):
                self.rnpArCalculatedSegment.append(RnpArInitialApproachSegment(self.rnpArDataGroup));
            
            surfaceLayers = []
            self.rnpArCalculatedSegment.method_1(self.rnpArDataGroup.Title, surfaceLayers)
            self.rnpArCalculatedSegment.method_2(self.rnpArDataGroup.Title, self.rnpArDataGroup.LTP, surfaceLayers)
    #         finally
    #         {
    #             rnpArCalculatedSegment.method_0();
    #         }
            QgisHelper.appendToCanvas(define._canvas, surfaceLayers, SurfaceTypes.RnpAR)
            self.resultLayerList = surfaceLayers
            QgisHelper.zoomToLayers(surfaceLayers)
            self.ui.btnEvaluate.setEnabled(True)
#             self.hide()
        except UserWarning as e:
            QMessageBox.warning(self, "Information", e.message)
            
    def btnAddRF_IA_Click(self):
        segmentIndex = self.ui.tabControlSegments.currentIndex() 
        self.receiveRnpArInputData()
        
        if segmentIndex == 1:
            dblValue, result = QInputDialog.getDouble(self, "RNP Value", "RNP:", self.defaultRnpValueMA)
            if not result:
                return
            self.hide()
            self.defaultRnpValueMA = dblValue
            self.setRnpRFlegTool(define._canvas, self.rnpArDataGroup, RnpArSegmentType.Missed, dblValue)
        
        elif segmentIndex == 2:
            dblValue, result = QInputDialog.getDouble(self, "RNP Value", "RNP:", self.defaultRnpValueFA)
            if not result:
                return
            self.hide()
            self.defaultRnpValueFA = dblValue
            self.setRnpRFlegTool(define._canvas, self.rnpArDataGroup, RnpArSegmentType.Final, dblValue)
        
        elif segmentIndex == 3:
            dblValue, result = QInputDialog.getDouble(self, "RNP Value", "RNP:", self.defaultRnpValueI)
            if not result:
                return
            self.hide()
            self.defaultRnpValueI = dblValue
            self.setRnpRFlegTool(define._canvas, self.rnpArDataGroup, RnpArSegmentType.Intermediate, dblValue)
            
        elif segmentIndex == 4:
            dblValue, result = QInputDialog.getDouble(self, "RNP Value", "RNP:", self.defaultRnpValueIA)
            if not result:
                return
            self.hide()
            self.defaultRnpValueIA = dblValue
            self.setRnpRFlegTool(define._canvas, self.rnpArDataGroup, RnpArSegmentType.Initial, dblValue)
        
    def btnAddTF_IA_Click(self):
        segmentIndex = self.ui.tabControlSegments.currentIndex() 
        self.receiveRnpArInputData()
        
        if segmentIndex == 1:
            dblValue, result = QInputDialog.getDouble(self, "RNP Value", "RNP:", self.defaultRnpValueMA)
            if not result:
                return
            self.hide()
            self.defaultRnpValueMA = dblValue
            self.setRnpTFlegTool(define._canvas, self.rnpArDataGroup, RnpArSegmentType.Missed, dblValue)
        
        elif segmentIndex == 2:
            dblValue, result = QInputDialog.getDouble(self, "RNP Value", "RNP:", self.defaultRnpValueFA)
            if not result:
                return
            self.hide()
            self.defaultRnpValueFA = dblValue
            self.setRnpTFlegTool(define._canvas, self.rnpArDataGroup, RnpArSegmentType.Final, dblValue)
        
        elif segmentIndex == 3:
            dblValue, result = QInputDialog.getDouble(self, "RNP Value", "RNP:", self.defaultRnpValueI)
            if not result:
                return
            self.hide()
            self.defaultRnpValueI = dblValue
            self.setRnpTFlegTool(define._canvas, self.rnpArDataGroup, RnpArSegmentType.Intermediate, dblValue)
            
        elif segmentIndex == 4:
            dblValue, result = QInputDialog.getDouble(self, "RNP Value", "RNP:", self.defaultRnpValueIA)
            if not result:
                return
            self.hide()
            self.defaultRnpValueIA = dblValue
            self.setRnpTFlegTool(define._canvas, self.rnpArDataGroup, RnpArSegmentType.Initial, dblValue)
        
        
    def setRnpTFlegTool(self, canvas, rnpArDataGroup_0, rnpArSegmentType_0, double_0):
        rnpArLeg1 = rnpArDataGroup_0.method_2(rnpArSegmentType_0)
        point3d = rnpArLeg1.method_1(rnpArDataGroup_0)
        num, flag = rnpArLeg1.method_2(rnpArDataGroup_0, rnpArSegmentType_0)
#         altitude = rnpArDataGroup_0.method_5(rnpArSegmentType_0, None)
        polyline = rnpArLeg1.method_4(rnpArDataGroup_0, rnpArSegmentType_0)
        rnpTFlegJig = RnpTFlegJig(canvas, rnpArSegmentType_0, rnpArDataGroup_0, point3d, double_0, num, flag)
        if (polyline != None):
            geoms = polyline.getGeometry()
            rnpTFlegJig.setGeometries(geoms)
        canvas.setMapTool(rnpTFlegJig)
        self.connect(rnpTFlegJig, SIGNAL("RnpArlegCaptured"), self.rnpArlegCaptured)

    def setRnpRFlegTool(self, canvas, rnpArDataGroup_0, rnpArSegmentType_0, double_0):
        rnpArLeg1 = rnpArDataGroup_0.method_2(rnpArSegmentType_0)
        point3d = rnpArLeg1.method_1(rnpArDataGroup_0)
        num = rnpArLeg1.method_3(rnpArDataGroup_0)
        polyline = rnpArLeg1.method_4(rnpArDataGroup_0, rnpArSegmentType_0)
        
        rnpRFlegJig = RnpRFlegJig(canvas, rnpArSegmentType_0, rnpArDataGroup_0, point3d, double_0, num)
        if (polyline != None):
            geoms = polyline.getGeometry()
            rnpRFlegJig.setGeometries(geoms)
                
        
        canvas.setMapTool(rnpRFlegJig)
        self.connect(rnpRFlegJig, SIGNAL("RnpArlegCaptured"), self.rnpArlegCaptured)


    def rnpArlegCaptured(self, rnpArSegmentType, rnpArLeg):
#         rnpArLeg = RnpTFlegJig.RnpArTFLeg
        dlgRnpArLeg = RnpArLegDlg(self, self.rnpArDataGroup, rnpArLeg)
        if dlgRnpArLeg.exec_() != QDialog.Accepted:
            self.show()
            return
        if rnpArSegmentType == RnpArSegmentType.Final:
            self.rnpArDataGroup.Legs_FA.Add(rnpArLeg)
        elif rnpArSegmentType == RnpArSegmentType.Missed:
            self.rnpArDataGroup.Legs_MA.Add(rnpArLeg)
        elif rnpArSegmentType == RnpArSegmentType.Initial:
            self.rnpArDataGroup.Legs_IA.Add(rnpArLeg)
        elif rnpArSegmentType == RnpArSegmentType.Intermediate:
            self.rnpArDataGroup.Legs_I.Add(rnpArLeg)
        self.show()
        self.method_31()
        self.rnpArDataGroup.Legs_FA_dataChanged(self.rnpArDataGroup.Legs_FA.index(len(self.rnpArDataGroup.Legs_FA.rnpArLegsList) - 1, 2), self.rnpArDataGroup.Legs_FA.index(len(self.rnpArDataGroup.Legs_FA.rnpArLegsList) - 1, 2))
#         if (DlgRnpArLeg.smethod_0(programBase_0, rnpArDataGroup_0, double0))
#         {
#             rnpArLeg = double0;
#             return rnpArLeg;
#         }
        
        
    def receiveRnpArInputData(self):
        self.rnpArDataGroup.ActiveSegment = 1
        try:
            self.rnpArDataGroup.FAP = Altitude(float(self.ui.txtFAP.text()), AltitudeUnits.FT)
        except:
            self.rnpArDataGroup.FAP = Altitude.NaN()
        
        self.rnpArDataGroup.OCAH_Type = self.ui.cmbFinalOCAH.currentText()
        try:
            if self.ui.cmbFinalOCAH.currentIndex() == 0:
                self.rnpArDataGroup.OCAH_Value = Altitude(float(self.ui.txtFinalOCAH.text()), AltitudeUnits.FT)
            else:
                self.rnpArDataGroup.OCAH_Value = Altitude(float(self.ui.txtFinalOCAH.text()) + Unit.ConvertMeterToFeet(self.pnlLTP.Point3d.get_Z()), AltitudeUnits.FT)
        except:
            self.rnpArDataGroup.OCAH_Value = Altitude.NaN()
            #raise UserWarning, "OCA Altitude is invalid!" 
        self.rnpArDataGroup.MACG = AngleGradientSlope(2.5, AngleGradientSlopeUnits.Percent)
        self.rnpArDataGroup.MOC_MA_30 = Altitude(30)
        self.rnpArDataGroup.MOC_MA_50 = Altitude(50)
        self.rnpArDataGroup.MOC_I = Altitude(150)
        self.rnpArDataGroup.MOC_IA = Altitude(300)
        self.rnpArDataGroup.Name = "RnpAR Data"
        self.rnpArDataGroup.LTP = self.pnlLTP.getPoint3D()
        self.rnpArDataGroup.CAT = self.ui.cmbCAT.currentIndex()
        
        try:
            self.rnpArDataGroup.AerodromeElevation = Altitude(float(self.ui.txtAdElev.text()))
        except ValueError:
            self.rnpArDataGroup.AerodromeElevation = Altitude.NaN()
        
        try:
            self.rnpArDataGroup.ACT = float(self.ui.txtACT.text())
        except ValueError:
            self.rnpArDataGroup.ACT = 0.0
        
        try:
            self.rnpArDataGroup.IAS_IA = Speed(float(self.ui.txtIAS_IA.text()))
        except ValueError:
            self.rnpArDataGroup.IAS_IA = Speed.NaN()
        
        try:
            self.rnpArDataGroup.IAS_I = Speed(float(self.ui.txtIAS_I.text()))
        except ValueError:
            self.rnpArDataGroup.IAS_I = Speed.NaN()
            
        try:
            self.rnpArDataGroup.IAS_FA = Speed(float(self.ui.txtIAS_FA.text()))
        except ValueError:
            self.rnpArDataGroup.IAS_FA = Speed.NaN()
            
        try:
            self.rnpArDataGroup.IAS_MA = Speed(float(self.ui.txtIAS_MA.text()))
        except ValueError:
            self.rnpArDataGroup.IAS_MA = Speed.NaN()
            
        try:
            self.rnpArDataGroup.Gradient_IA = AngleGradientSlope(float(self.ui.txtGradient_IA.text()))
        except ValueError:
            self.rnpArDataGroup.Gradient_IA = AngleGradientSlope.NaN()
            
        try:
            self.rnpArDataGroup.Gradient_I = AngleGradientSlope(float(self.ui.txtGradient_I.text()))
        except ValueError:
            self.rnpArDataGroup.Gradient_I = AngleGradientSlope.NaN()
            
        try:
            self.rnpArDataGroup.Gradient_MA = AngleGradientSlope(float(self.ui.txtGradient_MA.text()))
        except ValueError:
            self.rnpArDataGroup.Gradient_MA = AngleGradientSlope.NaN()
            
        try:
            self.rnpArDataGroup.VPA = AngleGradientSlope(float(self.ui.txtVPA.text()))
        except ValueError:
            self.rnpArDataGroup.VPA = AngleGradientSlope.NaN()
            
        try:
            self.rnpArDataGroup.ISA = float(self.ui.txtISA.text())
        except ValueError:
            self.rnpArDataGroup.ISA = 0.0
            
        try:
            self.rnpArDataGroup.RDH = Altitude(float(self.ui.txtRDH.text()))
        except ValueError:
            self.rnpArDataGroup.RDH = Altitude.NaN()
            
        try:
            self.rnpArDataGroup.HL = Altitude(float(self.ui.txtHL.text()))
        except ValueError:
            self.rnpArDataGroup.HL = Altitude.NaN()
            
#         if (dlgRnpArDataGroup.clearLegs)
#         {
#             self.rnpArDataGroup.Legs_MA.Clear();
#             self.rnpArDataGroup.Legs_FA.Clear();
#             self.rnpArDataGroup.Legs_I.Clear();
#             self.rnpArDataGroup.Legs_IA.Clear();
#         }
        
#         self.method_40()
    
    def method_29(self):
        self.initResultPanel()
#         self.tblResults.Clear();
#         self.picWarning.Visible = false;
#         self.gridObstacles.DataSource = null;
#         self.pnlSegment.Items.Clear();
#         foreach (RnpAR.RnpArSegmentObstacles obstacle in RnpAR.obstacles)
#         {
#             if (obstacle == null)
#             {
#                 continue;
#             }
#             obstacle.Dispose();
#         }
#         RnpAR.obstacles.Clear();
#         RnpAR.obstaclesChecked = 0;
#         RnpAR.resultOCH = Altitude.NaN;
#         RnpAR.resultOCA = Altitude.NaN;
#     }
        pass
    
    def method_31(self):
        if (self.rnpArDataGroup != None):
            self.ui.tblLegsMA.setModel(self.rnpArDataGroup.Legs_MA)
            self.ui.tblLegsFA.setModel(self.rnpArDataGroup.Legs_FA)
            self.ui.tblLegsI.setModel(self.rnpArDataGroup.Legs_I)
            self.ui.tblLegsIA.setModel(self.rnpArDataGroup.Legs_IA)
            self.ui.txtFAP.setText(str(self.rnpArDataGroup.FAP.Feet))
            self.ui.cmbFinalOCAH.setCurrentIndex(0 if self.rnpArDataGroup.OCAH_Type == OCAHType.OCA else 1)
            if self.ui.cmbFinalOCAH.currentIndex() == 1:
                self.ui.txtFinalOCAH.setText(str(round(Unit.ConvertMeterToFeet(self.rnpArDataGroup.OCAH_Value.Metres - self.pnlLTP.Point3d.get_Z()), 2)))
            else:
                self.ui.txtFinalOCAH.setText(str(round(self.rnpArDataGroup.OCAH_Value.Feet, 2)))
            self.ui.txMACG.setText(str(self.rnpArDataGroup.MACG.Percent))
            self.ui.txtMocMA30.setText(str(self.rnpArDataGroup.MOC_MA_30.Metres))
            self.ui.txtMocMA50.setText(str(self.rnpArDataGroup.MOC_MA_50.Metres))
            self.ui.txtMocI.setText(str(self.rnpArDataGroup.MOC_I.Metres))
            self.ui.txtMocIA.setText(str(self.rnpArDataGroup.MOC_IA.Metres))
        self.method_32()
        self.method_38()
        self.hideLegTablesColumns()
        self.initResultPanel()

    def method_32(self):
        if (self.rnpArDataGroup != None and self.ui.txtFAP.text() != "" and self.ui.txtFAP.text() != "None"):
            temperatureComponents = self.rnpArDataGroup.TemperatureComponents
            self.ui.txtIsa_Airport.setText(str(temperatureComponents.ISA_airport))
            self.ui.txtIsa_Low.setText(str(temperatureComponents.ISA_low))
            self.ui.txtIsa_High.setText(str(temperatureComponents.ISA_high))
            self.ui.txtNA_Below.setText(str(temperatureComponents.NA_below))
            self.ui.txtNA_Above.setText(str(temperatureComponents.NA_above))
            self.ui.txtVPA_Min.setText(str(temperatureComponents.VPA_min.Degrees))
            self.ui.txtVPA_Max.setText(str(temperatureComponents.VPA_max.Degrees))
#             self.ui.txtIsa.txtIsa_Low_25.setText(str(None if temperatureComponents.ISA_low_25 == None else temperatureComponents.ISA_low_25))
#             self.ui.txtIsa_Low_25.setVisible(temperatureComponents.ISA_low_25 != None)
#             self.ui.txtNA_Below_25.setText(str(None if temperatureComponents.NA_below_25 == None else temperatureComponents.NA_below_25))
#             self.ui.txtNA_Below_25.setVisible(temperatureComponents.NA_below_25 != None)

    def method_38(self):
        flag1 = False if self.rnpArDataGroup.Legs_FA.Count <= 0 else self.rnpArDataGroup.Legs_FA[self.rnpArDataGroup.Legs_FA.Count - 1].IsFAP
        flag = True
        self.ui.btnFAP.setEnabled(False if not flag or self.rnpArDataGroup.Legs_FA.Count <= 0 or self.rnpArDataGroup.Legs_I.RowCount != 0 or self.rnpArDataGroup.Legs_IA.RowCount != 0 else self.rnpArDataGroup.Legs_FA.Count > 0)
        self.ui.btnAddTF_MA.setEnabled(False if not flag else self.rnpArDataGroup.Legs_FA.RowCount > 0)
        self.ui.btnAddRF_MA.setEnabled(False if not flag else self.rnpArDataGroup.Legs_MA.RowCount > 0)
        self.ui.btnAddTF_FA.setEnabled(False if not flag or self.rnpArDataGroup.Legs_I.RowCount != 0 else not flag1)
        self.ui.btnAddRF_FA.setEnabled(False if not flag or self.rnpArDataGroup.Legs_FA.RowCount <= 0 or self.rnpArDataGroup.Legs_I.RowCount != 0 else not flag1)
        self.ui.btnAddTF_I.setEnabled(False if not flag or not flag1 else self.rnpArDataGroup.Legs_IA.RowCount == 0)
        self.ui.btnAddRF_I.setEnabled(False if not flag or not flag1 else self.rnpArDataGroup.Legs_IA.RowCount == 0)
        self.ui.btnAddTF_IA.setEnabled(False if not flag or not flag1 else self.rnpArDataGroup.Legs_I.RowCount > 0)
        self.ui.btnAddRF_IA.setEnabled(False if not flag or not flag1 else self.rnpArDataGroup.Legs_I.RowCount > 0)

        selectedIndexes = self.ui.tblLegsMA.selectedIndexes()
        flagSelectedCountMA = len(selectedIndexes) == self.rnpArDataGroup.Legs_MA.ColumnCount - 2
        self.ui.btnRemove_MA.setEnabled(False if not flag or self.rnpArDataGroup.Legs_MA.RowCount <= 0 or not flagSelectedCountMA else selectedIndexes[0].row() == self.rnpArDataGroup.Legs_MA.RowCount - 1 )
        self.ui.btnModify_MA.setEnabled(False if not flag or self.rnpArDataGroup.Legs_MA.RowCount <= 0 else flagSelectedCountMA)

        selectedIndexes = self.ui.tblLegsFA.selectedIndexes()
        flagSelectedCountFA = len(selectedIndexes) == self.rnpArDataGroup.Legs_FA.ColumnCount - 2
        flagSelectedFA = flagSelectedCountFA and selectedIndexes[0].row() == self.rnpArDataGroup.Legs_FA.RowCount - 1
        self.ui.btnRemove_FA.setEnabled(False if not flag or self.rnpArDataGroup.Legs_FA.RowCount <= 0 or not flagSelectedFA or self.rnpArDataGroup.Legs_I.RowCount != 0 else True)
        self.ui.btnModify_FA.setEnabled(False if not flag or self.rnpArDataGroup.Legs_FA.RowCount <= 0 else flagSelectedCountFA)
   
        selectedIndexes = self.ui.tblLegsI.selectedIndexes()
        flagSelectedCountI = len(selectedIndexes) == self.rnpArDataGroup.Legs_I.ColumnCount - 2
        flagSelectedI = flagSelectedCountI and selectedIndexes[0].row() == self.rnpArDataGroup.Legs_I.RowCount - 1
        self.ui.btnRemove_I.setEnabled(False if not flag or self.rnpArDataGroup.Legs_I.RowCount <= 0 or not flagSelectedI else self.rnpArDataGroup.Legs_IA.RowCount == 0)
        self.ui.btnModify_I.setEnabled(False if not flag or self.rnpArDataGroup.Legs_I.RowCount <= 0 else flagSelectedCountI)

        selectedIndexes = self.ui.tblLegsIA.selectedIndexes()
        flagSelectedCountIA = len(selectedIndexes) == self.rnpArDataGroup.Legs_IA.ColumnCount - 2
        flagSelectedIA = len(selectedIndexes) == self.rnpArDataGroup.Legs_IA.ColumnCount - 2 and selectedIndexes[0].row() == self.rnpArDataGroup.Legs_IA.RowCount - 1
        self.ui.btnRemove_IA.setEnabled(False if not flag or self.rnpArDataGroup.Legs_IA.RowCount <= 0 else flagSelectedIA);
        self.ui.btnModify_IA.setEnabled(False if not flag or self.rnpArDataGroup.Legs_IA.RowCount <= 0 else flagSelectedCountIA)


    def method_40(self):
        self.receiveRnpArInputData()
        self.method_29();
        
        try:
            self.rnpArDataGroup.OCAH_Type = self.ui.cmbFinalOCAH.currentText()
        except:
            pass
        try:
            if self.ui.cmbFinalOCAH.currentIndex() == 0:
                self.rnpArDataGroup.OCAH_Value = Altitude(float(self.ui.txtFinalOCAH.text()), AltitudeUnits.FT)
            else:
                self.rnpArDataGroup.OCAH_Value = Altitude(float(self.ui.txtFinalOCAH.text()) + Unit.ConvertMeterToFeet(self.pnlLTP.Point3d.get_Z()), AltitudeUnits.FT)

        except:
            pass

        try:
            self.rnpArDataGroup.MACG = AngleGradientSlope(float(self.ui.txtMACG.text()))
        except:
            pass
        
        try:
            self.rnpArDataGroup.MOC_MA_30 = Altitude(float(self.ui.txtMocMA30.text()))
        except:
            pass

        try:
            self.rnpArDataGroup.MOC_MA_50 = Altitude(float(self.ui.txtMocMA50.text()))
        except:
            pass

        try:
            self.rnpArDataGroup.FAP = Altitude(float(self.ui.txtFAP.text()), AltitudeUnits.FT)
        except:
            pass
        self.method_32()

        try:
            self.rnpArDataGroup.MOC_I = Altitude(float(self.txtMocI.text()))
        except:
            pass
        try:
            self.rnpArDataGroup.MOC_IA = Altitude(float(self.txtMocIA.text()))
        except:
            pass

    def smethod_4(self):
        index = self.ui.cmbCAT.currentIndex()
        if ( index < 0):
            return
        if index == AircraftSpeedCategory.A:
            self.ui.txtIAS_IA.setText(str(Speed(150).Knots))
            self.ui.txtIAS_I.setText(str(Speed(150).Knots))
            self.ui.txtIAS_FA.setText(str(Speed(100).Knots))
            self.ui.txtIAS_MA.setText(str(Speed(110).Knots))
            self.ui.txtRDH.setText(str(Altitude(12).Metres))
        elif index == AircraftSpeedCategory.B:
            self.ui.txtIAS_IA.setText(str(Speed(180).Knots))
            self.ui.txtIAS_I.setText(str(Speed(180).Knots))
            self.ui.txtIAS_FA.setText(str(Speed(130).Knots))
            self.ui.txtIAS_MA.setText(str(Speed(150).Knots))
            self.ui.txtRDH.setText(str(Altitude(14).Metres))
        elif index == AircraftSpeedCategory.C:
            self.ui.txtIAS_IA.setText(str(Speed(240).Knots))
            self.ui.txtIAS_I.setText(str(Speed(240).Knots))
            self.ui.txtIAS_FA.setText(str(Speed(160).Knots))
            self.ui.txtIAS_MA.setText(str(Speed(240).Knots))
            self.ui.txtRDH.setText(str(Altitude(15).Metres))
        elif index == AircraftSpeedCategory.D:
            self.ui.txtIAS_IA.setText(str(Speed(250).Knots))
            self.ui.txtIAS_I.setText(str(Speed(250).Knots))
            self.ui.txtIAS_FA.setText(str(Speed(185).Knots))
            self.ui.txtIAS_MA.setText(str(Speed(265).Knots))
            self.ui.txtRDH.setText(str(Altitude(15).Metres))
        elif index == AircraftSpeedCategory.E:
            self.ui.txtIAS_IA.setText(str(Speed(250).Knots))
            self.ui.txtIAS_I.setText(str(Speed(250).Knots))
            self.ui.txtIAS_FA.setText(str(Speed(185).Knots))
            self.ui.txtIAS_MA.setText(str(Speed(265).Knots))
            self.ui.txtRDH.setText(str(Altitude(17).Metres))
        self.smethod_5()
        
    def smethod_5(self):        
        if (self.ui.cmbCAT.currentIndex() < 0):
            return
        if self.ui.txtVPA.text() == "":
            return
        if not self.pnlLTP.Altitude().IsValid():
            return
        aircraftSpeedCategory = self.ui.cmbCAT.currentIndex()
        value = float(self.ui.txtVPA.text())
        altitude = self.pnlLTP.Altitude()
        num = None
        num1 = None
        if aircraftSpeedCategory == AircraftSpeedCategory.A:
            num = 40
            num1 = 13
        elif aircraftSpeedCategory == AircraftSpeedCategory.B:
            num = 43
            num1 = 18
        elif aircraftSpeedCategory == AircraftSpeedCategory.C:
            num = 46
            num1 = 22
        elif aircraftSpeedCategory == AircraftSpeedCategory.D or aircraftSpeedCategory == AircraftSpeedCategory.E:
            num = 49
            num1 = 26
        metres = 0
        if (altitude.Metres > 900):
            metres = metres + num1 * 0.02 * (altitude.Metres / 300)
        if (value > 3.2):
            metres = metres + num1 * 0.05 * ((value - 3.2) / 0.1)
        metres = MathHelper.smethod_0(metres, 0);
        self.ui.txtHL.setText(str(num + metres))
        
    def exportResult(self):
#         dlg = ExportDlg(self)
#         dlg.exec_()
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
                 
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return        
        self.filterList = ["", RnpArSegmentType.Missed, RnpArSegmentType.Final, RnpArSegmentType.Intermediate, RnpArSegmentType.Initial]
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, "RNP AR Obstacle Analyser", self.ui.tblObstacles, self.filterList, parameterList, resultHideColumnNames)
        self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbSurface.currentIndex()])
#         FlightPlanBaseDlg.exportResult()
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("LTP / FTP", "group"))
#         parameterList.append(("X", self.pnlLTP.txtPointX.text()))
#         parameterList.append(("Y", self.pnlLTP.txtPointY.text()))
#         parameterList.append(("Altitude", self.pnlLTP.txtAltitudeM.text() + " m/" + self.pnlLTP.txtAltitudeFt.text() + " ft"))
        DataHelper.pnlPositionParameter(self.pnlLTP, parameterList)
        parameterList.append(("Aircraft Category", self.ui.cmbCAT.currentText()))
        parameterList.append(("Aerodrome Elevation", self.ui.txtAdElev.text() + " m"))
        parameterList.append(("Average Cold Temperature", self.ui.txtACT.text() + unicode(" °C", "utf-8")))
        parameterList.append(("ISA", self.ui.txtISA.text() + unicode(" °C", "utf-8")))
        parameterList.append(("RDH", self.ui.txtRDH.text() + " m"))
        parameterList.append(("Height Loss", self.ui.txtHL.text() + " m"))
                        
        parameterList.append(("Final Approach", "group"))
        parameterList.append(("VPA", self.ui.txtVPA.text() + unicode(" °", "utf-8")))
        parameterList.append(("FAP Altitude", self.ui.txtFAP.text() + " m"))
        parameterList.append(("FAP - LTP Distance", str(self.rnpArDataGroup.FAPtoLTP.Metres) + " m"))
        
        parameterList.append(("Temperature Components", "group"))
        parameterList.append(("ISA airport", self.ui.txtIsa_Airport.text()+ unicode(" °C", "utf-8")))
        parameterList.append(("ISA low", self.ui.txtIsa_Low.text()+ unicode(" °C", "utf-8")))
        parameterList.append(("ISA high", self.ui.txtIsa_High.text() + unicode(" °C", "utf-8")))
        parameterList.append(("NA below", self.ui.txtNA_Below.text() + unicode(" °C", "utf-8")))
        parameterList.append(("NA above", self.ui.txtNA_Above.text() + unicode(" °C", "utf-8")))
        parameterList.append(("VPA min", self.ui.txtVPA_Min.text() + unicode(" °", "utf-8")))
        parameterList.append(("VPA max", self.ui.txtVPA_Max.text() + unicode(" °", "utf-8")))
        
        parameterList.append(("VEB / OAS Parameters", "group"))
        rnpArFinalApproachSegment = RnpArFinalApproachSegment(self.rnpArDataGroup)
        parameterList.append(("fte", str(rnpArFinalApproachSegment.veb.fte.Metres) + " m"))
        parameterList.append(("atis", str(rnpArFinalApproachSegment.veb.atis.Metres) + " m"))
        parameterList.append(("anpe", str(rnpArFinalApproachSegment.veb.anpe.Metres) + " m"))
        parameterList.append(("wpr", str(rnpArFinalApproachSegment.veb.wpr.Metres) + " m"))
        parameterList.append(("ase75", str(rnpArFinalApproachSegment.veb.ase75.Metres) + " m"))
        parameterList.append(("aseFAP", str(rnpArFinalApproachSegment.veb.aseFAP.Metres) + " m"))
        parameterList.append(("vae75", str(rnpArFinalApproachSegment.veb.vae75.Metres) + " m"))
        parameterList.append(("vaeFAP", str(rnpArFinalApproachSegment.veb.vaeFAP.Metres) + " m"))
        parameterList.append(("isad75", str(rnpArFinalApproachSegment.veb.isad75.Metres) + " m"))
        parameterList.append(("isadFAP", str(rnpArFinalApproachSegment.veb.isadFAP.Metres) + " m"))
        parameterList.append(("bg(TF)", str(rnpArFinalApproachSegment.veb.bg_TF.Metres) + " m"))
        parameterList.append(("bg(RF)", str(rnpArFinalApproachSegment.veb.bg_RF.Metres) + " m"))
        parameterList.append(("moc75(TF)", str(rnpArFinalApproachSegment.veb.moc75_TF.Metres) + " m"))
        parameterList.append(("moc75(RF)", str(rnpArFinalApproachSegment.veb.moc75_RF.Metres) + " m"))
        parameterList.append(("mocFAP(TF)", str(rnpArFinalApproachSegment.veb.mocFAP_TF.Metres) + " m"))
        parameterList.append(("mocFAP(RF)", str(rnpArFinalApproachSegment.veb.mocFAP_RF.Metres) + " m"))
        parameterList.append(("OAS gradient(TF)", str(rnpArFinalApproachSegment.veb.OASgradient_TF.Percent) + " %"))
        parameterList.append(("OAS gradient(RF)", str(rnpArFinalApproachSegment.veb.OASgradient_RF.Percent) + " %"))
        parameterList.append(("OAS origin(TF)", str(rnpArFinalApproachSegment.veb.OASorigin_TF.Metres) + " m"))
        parameterList.append(("OAS origin(RF)", str(rnpArFinalApproachSegment.veb.OASorigin_RF.Metres) + " m"))
        self.appenListParam(self.rnpArDataGroup.Legs_FA, parameterList, self.ui.txtIAS_FA)
        
        parameterList.append(("Missed Approach", "group"))
        parameterList.append(("OCA/H(%s)"%self.ui.cmbFinalOCAH.currentText(), self.ui.txtFinalOCAH.text() + " ft"))
        parameterList.append(("Climb Gradient", self.ui.txMACG.text() + " %"))
        parameterList.append(("MAS origin", str(self.rnpArDataGroup.Xmas.Metres) + " m"))
        parameterList.append(("SOC Altitude", str(self.rnpArDataGroup.SOCaltitude.Metres) + " m"))
        parameterList.append(("Z surface origin", str(self.rnpArDataGroup.Xz.Metres) + " m"))
        try:
            parameterList.append(("DMASRNP", str(self.rnpArDataGroup.Dmasrnp.NauticalMiles) + " nm"))
        except:
            parameterList.append(("DMASRNP", ""))
        self.appenListParam(self.rnpArDataGroup.Legs_MA, parameterList, self.ui.txtIAS_MA)
        
        parameterList.append(("Intermediate Approach", "group"))
        self.appenListParam(self.rnpArDataGroup.Legs_I, parameterList, self.ui.txtIAS_I)
        parameterList.append(("Initial Approach", "group"))
        self.appenListParam(self.rnpArDataGroup.Legs_IA, parameterList, self.ui.txtIAS_IA)
        
        parameterList.append(("Results / Checked Obstacles", "group"))        
        parameterList.append(("Results", "group"))
        parameterList.append(("OCH", self.ui.txtOCHResults.text() + " %s"%self.ui.cmbUnits.currentText()))
        parameterList.append(("OCA", self.ui.txtOCAResults.text() + " %s"%self.ui.cmbUnits.currentText()))
        parameterList.append(("Checked Obstacles", "group"))
        
        for strFilter in self.filterList:
            self.obstaclesModel.setFilterFixedString(strFilter)
            c = self.obstaclesModel.rowCount()
            parameterList.append(("Number of Checked Obstacles(%s)"%strFilter, str(c)))  
        return parameterList
    def appenListParam(self, legs, parameterList, iasTxtBox):
        for i in range(legs.RowCount):
            rnpLeg = legs.rnpArLegsList[i]
            parameterList.append((rnpLeg.get_type_text(), "group"))            
            parameterList.append(("X", legs.data(legs.index(i, 10), Qt.DisplayRole).toString()))
            parameterList.append(("Y", legs.data(legs.index(i, 11), Qt.DisplayRole).toString()))
            parameterList.append(("RNP", legs.data(legs.index(i, 1), Qt.DisplayRole).toString()))
            parameterList.append(("Altitude", legs.data(legs.index(i, 2), Qt.DisplayRole).toString()))
            parameterList.append(("IAS", iasTxtBox.text() + " kts"))
            parameterList.append(("Wind", legs.data(legs.index(i, 3), Qt.DisplayRole).toString()))
            parameterList.append(("Bank Angle", legs.data(legs.index(i, 4), Qt.DisplayRole).toString()))
            if rnpLeg.Type == RnpArLegType.RF:
                parameterList.append(("r", legs.data(legs.index(i, 6), Qt.DisplayRole).toString()))
                    
#         return parameterList             

class RnpArDataGroup:

    def __init__(self):
        self.Legs_MA = RnpArLegs()
#         self.Legs_MA.setHeaderData(int, Qt_Orientation, QVariant, role=Qt_EditRole)
        self.Legs_FA = RnpArLegs()
        self.Legs_FA.dataChanged.connect(self.Legs_FA_dataChanged)
        self.Legs_I = RnpArLegs()
        self.Legs_IA = RnpArLegs()
        self.ACT = 0.0
        self.ActiveSegment = 0
        self.AerodromeElevation = Altitude.NaN()
        self.CAT = ""
        self.FAP = Altitude.NaN()
        self.Gradient_I = AngleGradientSlope.NaN()
        self.Gradient_IA = AngleGradientSlope.NaN()
        self.Gradient_MA = AngleGradientSlope.NaN()
        self.HL = Altitude.NaN()
        self.IAS_FA = Speed.NaN()
        self.IAS_I = Speed.NaN()
        self.IAS_IA = Speed.NaN()
        self.IAS_MA = Speed.NaN()
        self.ISA = 0.0
        self.LTP = None
        self.MACG = AngleGradientSlope.NaN()
        self.MOC_I = Altitude.NaN()
        self.MOC_IA = Altitude.NaN()
        self.MOC_MA_30 = Altitude.NaN()
        self.MOC_MA_50 = Altitude.NaN()
        self.Name = ""
        self.OCAH_Type = ""
        self.OCAH_Value = Altitude.NaN()
        self.RDH = Altitude.NaN()
        self.VPA = AngleGradientSlope.NaN()
    def Legs_FA_dataChanged(self, topLeftIndex, bottomRightIndex):
        rowIndex = topLeftIndex.row()
        colIndex = topLeftIndex.column()
        if colIndex != 2 or rowIndex < len(self.Legs_FA.rnpArLegsList) - 2:
            return
        data = self.Legs_FA.data(topLeftIndex).toString()
        altitude = Unit.ConvertFeetToMeter(float(data.left(data.length() - 2)))
        re = 6367435.67964 # radius of the Earth (Metre)
        metres = re * math.log1p((re + altitude)/(re + self.LTP.get_Z() + self.RDH.Metres) - 1)/ (self.VPA.Percent / 100)
        try:
            if round(metres, 4) == round(self.FAPtoLTP.Metres, 4):
                previousPoint = self.Legs_FA.rnpArLegsList[rowIndex].Previous
                self.Legs_FA.setData(self.Legs_FA.index(rowIndex + 1, self.Legs_FA.ColPreviousX), QVariant(previousPoint.get_X()))
                self.Legs_FA.setData(self.Legs_FA.index(rowIndex + 1, self.Legs_FA.ColPreviousY), QVariant(previousPoint.get_Y()))
                self.Legs_FA.rnpArLegsList[rowIndex + 1].Previous = previousPoint

                # self.Legs_FA.rnpArLegsList.pop(rowIndex)
                self.Legs_FA.removeRow(rowIndex)
                self.Legs_FA.updateRow(rowIndex, self.Legs_FA.rnpArLegsList[rowIndex])
                return
        except:
            pass

        if len(self.Legs_FA.rnpArLegsList) == 0:
            return
        typeStr = self.Legs_FA.rnpArLegsList[rowIndex].TypeText
        typeStr = String.Str2QString(typeStr)
        if not typeStr.contains("RF"):
            bearing = MathHelper.getBearing(self.LTP, self.Legs_FA.rnpArLegsList[rowIndex].Position)
            position = MathHelper.distanceBearingPoint(self.LTP, bearing, metres)
            self.Legs_FA.setData(self.Legs_FA.index(rowIndex, self.Legs_FA.ColPositionX), QVariant(position.get_X()))
            self.Legs_FA.setData(self.Legs_FA.index(rowIndex, self.Legs_FA.ColPositionY), QVariant(position.get_Y()))
            self.Legs_FA.rnpArLegsList[rowIndex].Position = position
            if rowIndex < len(self.Legs_FA.rnpArLegsList) - 1:
                self.Legs_FA.setData(self.Legs_FA.index(rowIndex + 1, self.Legs_FA.ColPreviousX), QVariant(position.get_X()))
                self.Legs_FA.setData(self.Legs_FA.index(rowIndex + 1, self.Legs_FA.ColPreviousY), QVariant(position.get_Y()))
                self.Legs_FA.rnpArLegsList[rowIndex + 1].Previous = position
        else:
            inbound = self.Legs_FA.rnpArLegsList[rowIndex].Inbound
            bulge = MathHelper.smethod_59(inbound, self.Legs_FA.rnpArLegsList[rowIndex].Previous, self.Legs_FA.rnpArLegsList[rowIndex].Position)
            start = self.Legs_FA.rnpArLegsList[rowIndex].Previous
            finish = self.Legs_FA.rnpArLegsList[rowIndex].Position
            point3d2 = MathHelper.distanceBearingPoint(start, inbound + 1.5707963267949, 100);
            num = MathHelper.getBearing(finish, start);
            point3d3 = MathHelper.distanceBearingPoint(finish, num, MathHelper.calcDistance(finish, start) / 2);
            point3d4 = MathHelper.distanceBearingPoint(point3d3, num + 1.5707963267949, 100);
            point3d = MathHelper.getIntersectionPoint(start, point3d2, point3d3, point3d4)
            entity = PolylineArea([start, finish])
            if point3d != None:
                radius = MathHelper.calcDistance(point3d, start);
                entity[0].bulge = bulge
            else:
                radius = None

            # lineGeom = QgsGeometry.fromPolyline(entity.getCurve(4))
            #
            # pointArray = entity.method_14(4)

            polylineArea = entity
            # polylineArea.Add(PolylineAreaPoint(self.Legs_FA.rnpArLegsList[rowIndex].Previous, bulge))
            # polylineArea.Add(PolylineAreaPoint(self.Legs_FA.rnpArLegsList[rowIndex].Position))
            pointArray = []
            for i in range(rowIndex):
                typeStr0 = self.Legs_FA.rnpArLegsList[i].Type
                typeStr0 = String.Str2QString(typeStr0)
                if not typeStr0.contains("RF"):
                    pointArray.append(self.Legs_FA.rnpArLegsList[i].Previous)
                    pointArray.append(self.Legs_FA.rnpArLegsList[i].Position)
                else:
                    inbound = self.Legs_FA.rnpArLegsList[rowIndex].Inbound
                    bulge = MathHelper.smethod_59(inbound, self.Legs_FA.rnpArLegsList[rowIndex].Previous, self.Legs_FA.rnpArLegsList[rowIndex].Position)
                    start = self.Legs_FA.rnpArLegsList[rowIndex].Previous
                    finish = self.Legs_FA.rnpArLegsList[rowIndex].Position
                    point3d2 = MathHelper.distanceBearingPoint(start, inbound + 1.5707963267949, 100);
                    num = MathHelper.getBearing(finish, start);
                    point3d3 = MathHelper.distanceBearingPoint(finish, num, MathHelper.calcDistance(finish, start) / 2);
                    point3d4 = MathHelper.distanceBearingPoint(point3d3, num + 1.5707963267949, 100);
                    point3d = MathHelper.getIntersectionPoint(start, point3d2, point3d3, point3d4)
                    entity0 = PolylineArea([start, finish])
                    if point3d != None:
                        radius = MathHelper.calcDistance(point3d, start);
                        entity0[0].bulge = bulge
                    else:
                        radius = None
                    polylineArea0 = entity0
                    # polylineArea0.Add(PolylineAreaPoint(self.Legs_FA.rnpArLegsList[i].Previous, bulge))
                    # polylineArea0.Add(PolylineAreaPoint(self.Legs_FA.rnpArLegsList[i].Position))
                    pointArray.extend(polylineArea0.method_14())
            pointArray.extend(polylineArea.method_14())
            position = MathHelper.getPointAtDist(pointArray, metres)
            self.Legs_FA.setData(self.Legs_FA.index(rowIndex, self.Legs_FA.ColPositionX), QVariant(position.x()))
            self.Legs_FA.setData(self.Legs_FA.index(rowIndex, self.Legs_FA.ColPositionY), QVariant(position.y()))
            self.Legs_FA.rnpArLegsList[rowIndex].Position = position
            if rowIndex < len(self.Legs_FA.rnpArLegsList) - 1:
                self.Legs_FA.setData(self.Legs_FA.index(rowIndex + 1, self.Legs_FA.ColPreviousX), QVariant(position.x()))
                self.Legs_FA.setData(self.Legs_FA.index(rowIndex + 1, self.Legs_FA.ColPreviousY), QVariant(position.y()))
                self.Legs_FA.rnpArLegsList[rowIndex + 1].Previous = position
        if typeStr.contains("FAP"):
            self.FAPtoLTP.Metres = metres





        # else:


        pass
        
    def get_dmasrnp(self):
        speed = Speed.smethod_0(self.IAS_FA, self.ISA, self.AerodromeElevation) + Speed(10)
        num = self.Legs_FA[0].Rnp if self.Legs_FA.Count > 0 else None
        num1 = self.Legs_MA[0].Rnp if self.Legs_MA.Count > 0 else None
        if num == None or num1 == None:
            return Distance.NaN()
        return Distance((num1 - num) * (speed.Knots / 8), DistanceUnits.NM);
    Dmasrnp = property(get_dmasrnp, None, None, None)

    def get_FAPtoLTP(self):
        metres = 6367435.67964 + (self.FAP.Metres if(self.FAP.Metres != None) else 0.0)
        num = 6367435.67964 + self.LTP.z()
        rDH = self.RDH
        num1 = 6367435.67964 * math.log(metres / (num + rDH.Metres))
        vPA = self.VPA
        return Distance(num1 / math.tan(vPA.Radians))
    FAPtoLTP = property(get_FAPtoLTP, None, None, None)
    
    def get_Frop150(self):
        flag = False
        for current in self.Legs_FA:
            if (current.Type == RnpArLegType.RF):
                flag = True
                break;

        if (not flag):
            return Distance.NaN()
        metres = 150 - self.RDH.Metres
        vPA = self.VPA;
        return Distance(metres / math.tan(vPA.Radians))
    Frop150 = property(get_Frop150, None, None, None)
    
    def get_Frop15s(self):
        if (not self.OCAH_Value.IsValid()):
            return Distance.NaN()
        num = self.OCAH_Value.Metres - self.LTP.z() if self.OCAH_Type == OCAHType.OCA else self.OCAH_Value.Metres
        speed = Speed.smethod_0(self.IAS_FA, self.ISA, self.AerodromeElevation) + Speed(15)
        metres = num - self.RDH.Metres
        vPA = self.VPA
        return Distance(metres / math.tan(vPA.Radians) + speed.MetresPerSecond * 15);
    Frop15s = property(get_Frop15s, None, None, None)

    def get_Frop50s(self):
        if not self.OCAH_Value.IsValid():
            return Distance.NaN()
        num = self.OCAH_Value.Metres - self.LTP.z() if self.OCAH_Type == OCAHType.OCA else self.OCAH_Value.Metres
        speed = Speed.smethod_0(self.IAS_FA, self.ISA, self.AerodromeElevation) + Speed(15)
        metres = num - self.RDH.Metres
        vPA = self.VPA
        return Distance(metres / math.tan(vPA.Radians) + speed.MetresPerSecond * 50)
    Frop50s = property(get_Frop50s, None, None, None)

    def get_MaxFinalBankRF(self):
        bank = 0;
        for i in range(self.Legs_FA.Count):
            if (self.Legs_FA[i].Type == RnpArLegType.RF and self.Legs_FA[i].Bank > bank):
                bank = self.Legs_FA[i].Bank
        return bank
    MaxFinalBankRF = property(get_MaxFinalBankRF, None, None, None)

    def get_MaxFinalRnp(self):
        rnp = self.Legs_FA[0].Rnp if self.Legs_FA.Count > 0 else None
        for item in self.Legs_FA:
            if (item.Rnp > rnp):
                rnp = self.item.Rnp;
        return rnp;
    MaxFinalRnp = property(get_MaxFinalRnp, None, None, None)

    def get_Smas(self):
        num = self.OCAH_Value.Metres - self.LTP.z() if self.OCAH_Type == OCAHType.OCA else self.OCAH_Value.Metres
        num1 = MathHelper.getBearing(self.LTP, self.Legs_FA[0].Position)
        point3d = self.LTP
        metres = num - self.RDH.Metres
        vPA = self.VPA
        return MathHelper.distanceBearingPoint(point3d, num1, metres / math.tan(vPA.Radians))
    Smas = property(get_Smas, None, None, None)
    
    def get_SOC(self):
        num = MathHelper.getBearing(self.LTP, self.Legs_FA[0].Position);
        point3d = self.LTP
        xsoc = self.Xsoc;
        return MathHelper.distanceBearingPoint(point3d, num, xsoc.Metres).smethod_167(self.SOCaltitude.Metres)
    SOC = property(get_SOC, None, None, None)

    def get_SOCaltitude(self):
        num = self.OCAH_Value.Metres - self.LTP.z() if self.OCAH_Type == OCAHType.OCA else self.OCAH_Value.Metres
        altitude = self.LTP.z()
        hL = self.HL
        return Altitude(altitude + num - hL.Metres)
    SOCaltitude = property(get_SOCaltitude, None, None, None)

    def get_TemperatureComponents(self):
        try:
            return RnpArTemperatureComponents(self.IAS_FA, self.VPA, self.ISA, self.ACT, self.AerodromeElevation, self.FAP, Altitude(self.LTP.z()), self.CAT)
        except:
            return None
    TemperatureComponents = property(get_TemperatureComponents, None, None, None)
    
    def get_Title(self):
        name = self.Name;
        str = self.CAT
        vPA = self.VPA;
        return "%s, CAT %s, VPA %.2f" % (name, str, vPA.Degrees)
    Title = property(get_Title, None, None, None)


    def get_Xmas(self):
        metres = (self.OCAH_Value.Metres - self.LTP.z() if self.OCAH_Type == OCAHType.OCA else self.OCAH_Value.Metres) - self.RDH.Metres
        vPA = self.VPA
        return Distance(metres / math.tan(vPA.Radians))
    Xmas = property(get_Xmas, None, None, None)

    def get_Xsoc(self):
        speed = Speed.smethod_0(self.IAS_FA, self.ISA, self.AerodromeElevation) + Speed(10)
        rnp = 1.225 * self.Legs_FA[0].Rnp
        num = 18.3
        vPA = self.VPA
        num1 = 22.9 / math.tan(vPA.Radians)
        metresPerSecond = 15 * speed.MetresPerSecond + 1.33333333333333 * math.sqrt(rnp * rnp + num * num + num1 * num1)
        metres = (self.OCAH_Value.Metres - self.LTP.z() if self.OCAH_Type == OCAHType.OCA else self.OCAH_Value.Metres) - self.RDH.Metres
        angleGradientSlope = self.VPA;
        return Distance(metres / math.tan(angleGradientSlope.Radians) - metresPerSecond)
    Xsoc = property(get_Xsoc, None, None, None)

    def get_Xz(self):
        num = self.OCAH_Value.Metres - self.LTP.z() if self.OCAH_Type == OCAHType.OCA else self.OCAH_Value.Metres
        metres = self.Xsoc.Metres
        metres1 = num - self.HL.Metres
        vPA = self.VPA
        return Distance(metres - metres1 / math.tan(vPA.Radians))
    Xz = property(get_Xz, None, None, None)
#     public RnpArDataGroup(XmlFile xmlFile_0, XmlNode xmlNode_0)
#     {
#         self.method_0(xmlFile_0, (XmlElement)xmlNode_0);
#     }

#     public void method_0(XmlFile xmlFile_0, XmlElement xmlElement_0)
#     {
#         AngleGradientSlope angleGradientSlope;
#         Position position;
#         Altitude altitude;
#         double num;
#         string str;
#         Speed speed;
#         int num1;
#         xmlFile_0.method_15(xmlElement_0, "ActiveSegment", out num1);
#         self.ActiveSegment = num1;
#         xmlFile_0.method_7(xmlElement_0, "Name", out str);
#         self.Name = str;
#         xmlFile_0.method_63(xmlElement_0, "LTP", out position);
#         self.LTP = position;
#         xmlFile_0.method_15(xmlElement_0, "CAT", out num1);
#         self.CAT = (AircraftSpeedCategory)num1;
#         xmlFile_0.method_35(xmlElement_0, "AerodromeElevation", out altitude);
#         self.AerodromeElevation = altitude;
#         xmlFile_0.method_23(xmlElement_0, "ACT", out num);
#         self.ACT = num;
#         xmlFile_0.method_43(xmlElement_0, "IAS_IA", out speed);
#         self.IAS_IA = speed;
#         xmlFile_0.method_43(xmlElement_0, "IAS_I", out speed);
#         self.IAS_I = speed;
#         xmlFile_0.method_43(xmlElement_0, "IAS_FA", out speed);
#         self.IAS_FA = speed;
#         xmlFile_0.method_43(xmlElement_0, "IAS_MA", out speed);
#         self.IAS_MA = speed;
#         xmlFile_0.method_47(xmlElement_0, "Gradient_IA", out angleGradientSlope);
#         self.Gradient_IA = angleGradientSlope;
#         xmlFile_0.method_47(xmlElement_0, "Gradient_I", out angleGradientSlope);
#         self.Gradient_I = angleGradientSlope;
#         xmlFile_0.method_47(xmlElement_0, "Gradient_MA", out angleGradientSlope);
#         self.Gradient_MA = angleGradientSlope;
#         xmlFile_0.method_47(xmlElement_0, "VPA", out angleGradientSlope);
#         self.VPA = angleGradientSlope;
#         xmlFile_0.method_47(xmlElement_0, "MACG", out angleGradientSlope);
#         self.MACG = angleGradientSlope;
#         xmlFile_0.method_23(xmlElement_0, "ISA", out num);
#         self.ISA = num;
#         xmlFile_0.method_35(xmlElement_0, "RDH", out altitude);
#         self.RDH = altitude;
#         xmlFile_0.method_35(xmlElement_0, "HL", out altitude);
#         self.HL = altitude;
#         xmlFile_0.method_35(xmlElement_0, "FAP", out altitude);
#         self.FAP = altitude;
#         xmlFile_0.method_15(xmlElement_0, "FinalOCAH_Type", out num1);
#         self.OCAH_Type = (OCAHType)num1;
#         xmlFile_0.method_35(xmlElement_0, "FinalOCAH_Value", out altitude);
#         self.OCAH_Value = altitude;
#         xmlFile_0.method_35(xmlElement_0, "MOC_MA_30", out altitude);
#         self.MOC_MA_30 = altitude;
#         xmlFile_0.method_35(xmlElement_0, "MOC_MA_50", out altitude);
#         self.MOC_MA_50 = altitude;
#         xmlFile_0.method_35(xmlElement_0, "MOC_I", out altitude);
#         self.MOC_I = altitude;
#         xmlFile_0.method_35(xmlElement_0, "MOC_IA", out altitude);
#         self.MOC_IA = altitude;
#         self.Legs_MA = RnpArLegs.smethod_0(xmlFile_0, xmlElement_0, "MissedApproachLegs");
#         self.Legs_FA = RnpArLegs.smethod_0(xmlFile_0, xmlElement_0, "FinalApproachLegs");
#         self.Legs_I = RnpArLegs.smethod_0(xmlFile_0, xmlElement_0, "IntermediateLegs");
#         self.Legs_IA = RnpArLegs.smethod_0(xmlFile_0, xmlElement_0, "InitialLegs");
#     }

#     public void method_1(XmlFile xmlFile_0, XmlNode xmlNode_0)
#     {
#         XmlElement xmlElement = xmlFile_0.CreateElement("RnpArDataGroup");
#         xmlFile_0.method_17(xmlElement, "ActiveSegment", self.ActiveSegment);
#         xmlFile_0.method_9(xmlElement, "Name", self.Name);
#         xmlFile_0.method_65(xmlElement, "LTP", self.LTP);
#         xmlFile_0.method_17(xmlElement, "CAT", (int)self.CAT);
#         xmlFile_0.method_37(xmlElement, "AerodromeElevation", self.AerodromeElevation);
#         xmlFile_0.method_25(xmlElement, "ACT", self.ACT);
#         xmlFile_0.method_45(xmlElement, "IAS_IA", self.IAS_IA);
#         xmlFile_0.method_45(xmlElement, "IAS_I", self.IAS_I);
#         xmlFile_0.method_45(xmlElement, "IAS_FA", self.IAS_FA);
#         xmlFile_0.method_45(xmlElement, "IAS_MA", self.IAS_MA);
#         xmlFile_0.method_49(xmlElement, "Gradient_IA", self.Gradient_IA);
#         xmlFile_0.method_49(xmlElement, "Gradient_I", self.Gradient_I);
#         xmlFile_0.method_49(xmlElement, "Gradient_MA", self.Gradient_MA);
#         xmlFile_0.method_49(xmlElement, "VPA", self.VPA);
#         xmlFile_0.method_49(xmlElement, "MACG", self.MACG);
#         xmlFile_0.method_25(xmlElement, "ISA", self.ISA);
#         xmlFile_0.method_37(xmlElement, "RDH", self.RDH);
#         xmlFile_0.method_37(xmlElement, "HL", self.HL);
#         xmlFile_0.method_37(xmlElement, "FAP", self.FAP);
#         xmlFile_0.method_17(xmlElement, "FinalOCAH_Type", (int)self.OCAH_Type);
#         xmlFile_0.method_37(xmlElement, "FinalOCAH_Value", self.OCAH_Value);
#         xmlFile_0.method_37(xmlElement, "MOC_MA_30", self.MOC_MA_30);
#         xmlFile_0.method_37(xmlElement, "MOC_MA_50", self.MOC_MA_50);
#         xmlFile_0.method_37(xmlElement, "MOC_I", self.MOC_I);
#         xmlFile_0.method_37(xmlElement, "MOC_IA", self.MOC_IA);
#         self.Legs_MA.method_0(xmlFile_0, xmlElement, "MissedApproachLegs");
#         self.Legs_FA.method_0(xmlFile_0, xmlElement, "FinalApproachLegs");
#         self.Legs_I.method_0(xmlFile_0, xmlElement, "IntermediateLegs");
#         self.Legs_IA.method_0(xmlFile_0, xmlElement, "InitialLegs");
#         xmlNode_0.AppendChild(xmlElement);
#     }

    def method_2(self, rnpArSegmentType_0):
        rnpArLeg = RnpArLegs()
        if (rnpArSegmentType_0 != RnpArSegmentType.Missed):
            for legsFA in self.Legs_FA:
                rnpArLeg.Add(legsFA)

            if (rnpArSegmentType_0 == RnpArSegmentType.Intermediate or rnpArSegmentType_0 == RnpArSegmentType.Initial):
                for legsI in self.Legs_I:
                    rnpArLeg.Add(legsI)
            if (rnpArSegmentType_0 == RnpArSegmentType.Initial):
                for legsIum in self.Legs_IA:
                    rnpArLeg.Add(legsIum)
        else:
            for legsMA in self.Legs_MA.rnpArLegsList:
                rnpArLeg.Add(legsMA)
        return rnpArLeg;

    def method_3(self, rnpArSegmentType_0):
        if (rnpArSegmentType_0 == RnpArSegmentType.Final):
            return self.VPA
        if rnpArSegmentType_0 == RnpArSegmentType.Initial:
            return self.Gradient_IA
        if (rnpArSegmentType_0 == RnpArSegmentType.Intermediate):
            return self.Gradient_I
        return self.Gradient_MA

    def method_4(self, rnpArSegmentType_0, int_0):
        if (rnpArSegmentType_0 == RnpArSegmentType.Missed):
            if (int_0 != 0):
                return self.Legs_MA[int_0 - 1]
            return self.Legs_FA[self.Legs_FA.Count - 1]
        if (rnpArSegmentType_0 == RnpArSegmentType.Final):
            if (int_0 == 0):
                return None
            return self.Legs_FA[int_0 - 1]
        if (rnpArSegmentType_0 == RnpArSegmentType.Intermediate):
            if (int_0 != 0):
                return self.Legs_I[int_0 - 1]
            return self.Legs_FA[self.Legs_FA.Count - 1]
        if (rnpArSegmentType_0 != RnpArSegmentType.Initial):
            return None
        if (int_0 != 0):
            return self.Legs_IA[int_0 - 1]
        return self.Legs_I[self.Legs_I.Count - 1]

    def method_5(self, rnpArSegmentType_0, rnpArLeg_0):
        rnpArLeg1 = RnpArLegs()
        if (rnpArSegmentType_0 != RnpArSegmentType.Missed):
            for current in self.Legs_FA:
                rnpArLeg1.Add(current);
            if (rnpArSegmentType_0 == RnpArSegmentType.Intermediate or rnpArSegmentType_0 == RnpArSegmentType.Initial):
                for rnpArLeg in self.Legs_I:
                    rnpArLeg1.Add(rnpArLeg)
            if (rnpArSegmentType_0 == RnpArSegmentType.Initial):
                for current1 in self.Legs_IA:
                    rnpArLeg1.Add(current1)
        else:
            for legsMA in self.Legs_MA:
                if (legsMA == rnpArLeg_0):
                    break;
                rnpArLeg1.Add(legsMA)
        if (rnpArSegmentType_0 == RnpArSegmentType.Missed):
            sOCaltitude = self.SOCaltitude
        else:
            altitude = self.LTP.z()
            sOCaltitude = Altitude(altitude + self.RDH.Metres)
        altitude1 = sOCaltitude
        if (rnpArLeg1.rowCount == 0):
            return altitude1
        
        polyline = Polyline()

        point3d = self.Smas if rnpArSegmentType_0 == RnpArSegmentType.Missed else self.LTP
        polyline.AddVertexAt(polyline.get_NumberOfVertices(), point3d, 0, 0, 0)
#         startParam = polyline.get_StartParam()
        for item in rnpArLeg1:
            point3d1 = item.Position
            if (item.Type != RnpArLegType.TF):
                polyline.SetBulgeAt(polyline.get_NumberOfVertices() - 1, MathHelper.smethod_59(item.Inbound, point3d, point3d1))
            else:
                polyline.SetBulgeAt(polyline.get_NumberOfVertices() - 1, 0);
            num = 4 * Unit.ConvertNMToMeter(item.Rnp)
            polyline.SetStartWidthAt(polyline.get_NumberOfVertices() - 1, num);
            polyline.SetEndWidthAt(polyline.get_NumberOfVertices() - 1, num);
            polyline.AddVertexAt(polyline.get_NumberOfVertices(), point3d1, 0, 0, 0);
            distanceAtParameter = MathHelper.calcDistance(point3d, point3d1)#polyline.GetDistanceAtParameter(polyline.get_EndParam()) - polyline.GetDistanceAtParameter(startParam);
            angleGradientSlope = self.method_3(item.Segment)
            altitude1 = altitude1 + Altitude(distanceAtParameter * (angleGradientSlope.Percent / 100))
            point3d = point3d1;
#             startParam = polyline.get_EndParam()

        return altitude1

class RnplegJig(QgsMapTool):
    def __init__(self, canvas, rnpArSegmentType, rnpArDataGroup, point3d_0, double_0, double_1):
        self.tempPoint = Point3D()
        self.rnpArSegmentType = rnpArSegmentType
        self.rnpArDataGroup = rnpArDataGroup
        self.finish = Point3D()
        self.rnp = double_0
        self.width = 4 * Unit.ConvertNMToMeter(double_0);
        self.start = point3d_0;
        self.inbound = double_1;
        self.rnpArLeg = None
        self.mSnapper = QgsMapCanvasSnapper(canvas)
        
        self.canvas = canvas
        QgsMapTool.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas,QGis.Polygon)
        self.rubberBand.setColor(QColor(255, 0, 0, 100))

        self.rubberBandPrev = QgsRubberBand(self.canvas,QGis.Polygon)
        self.rubberBandPrev.setColor(QColor(255, 0, 0, 100))
        
        self.mSnapper = QgsMapCanvasSnapper(canvas)
        self.rubberBandPt = QgsRubberBand(canvas, QGis.Point)
        self.rubberBandPt.setColor(Qt.red)
        self.rubberBandPt.setWidth(10)

        self.obstaclesLayerList = QgisHelper.getSurfaceLayers(SurfaceTypes.Obstacles)
        self.demLayerList = QgisHelper.getSurfaceLayers(SurfaceTypes.DEM)

        self.resetAll()
    
    def setGeometries(self, geoms):
        for geom in geoms:
            self.rubberBandPrev.addGeometry(geom, None)
        self.rubberBandPrev.show()
     
    def resetAll(self):  
        self.rubberBandPrev.reset(QGis.Polygon)    
        self.reset() 
        
    def reset(self):
        self.finish = None
        self.isDrawing = True
        self.rubberBand.reset(QGis.Polygon)
       
    def canvasPressEvent(self, e):       
        #self.isEmittingPoint = True
        self.rubberBandPt.reset(QGis.Point)

        self.Point, self.pointID, self.layer= self.snapPoint(e.pos())
        self.selectedLayerFromSnapPoint = None
        resultValueList = []
        snapPoint = None
        if self.obstaclesLayerList != None:
            for obstacleLayer in self.obstaclesLayerList:
                if self.layer == None:
                    break
                if obstacleLayer.name() == self.layer.name():
                    self.selectedLayerFromSnapPoint = self.layer
                    break
        if self.selectedLayerFromSnapPoint != None:
            dataProvider = self.selectedLayerFromSnapPoint.dataProvider()
            featureIter = dataProvider.getFeatures( QgsFeatureRequest(self.pointID))
            feature = None
            for feature0 in featureIter:
                feature = feature0
            idx = self.selectedLayerFromSnapPoint.fieldNameIndex('Altitude')
            altitudeValue = feature.attributes()[idx]

            snapPoint = Point3D(self.Point.x(), self.Point.y(), float(altitudeValue.toString()))
        else:
            if self.Point != None:
                identifyResult = None
                idValue = "Background"
                if self.demLayerList != None:

                    for demLayer in self.demLayerList:
                        identifyResults = demLayer.dataProvider().identify(self.Point, QgsRaster.IdentifyFormatValue)
                        identifyResult = identifyResults.results()
                if identifyResult != None:
                    snapPoint = Point3D(self.Point.x(), self.Point.y(), float(identifyResult[1].toString()))
                else:
                    snapPoint = Point3D(self.Point.x(), self.Point.y())
        if snapPoint == None:
            self.finish = Point3D(self.toMapCoordinates(e.pos()).x(), self.toMapCoordinates(e.pos()).y())
        else:
            self.finish = snapPoint    
            
        if self.start != self.finish:
            self.setRnpArLeg()
            self.resetAll() 
            self.isDrawing = False
            self.emit(SIGNAL("RnpArlegCaptured"), QString(self.rnpArSegmentType), self.rnpArLeg)
            self.deactivate()
    
    def setRnpArLeg(self):    
        pass
    
    def canvasMoveEvent(self, e):
        self.rubberBandPt.reset(QGis.Point)
        self.Point, self.pointID, self.layer= self.snapPoint(e.pos())
        self.selectedLayerFromSnapPoint = None
        resultValueList = []
        snapPoint = None
        if self.obstaclesLayerList != None:
            for obstacleLayer in self.obstaclesLayerList:
                if self.layer == None:
                    break
                if obstacleLayer.name() == self.layer.name():
                    self.selectedLayerFromSnapPoint = self.layer
                    break
        if self.selectedLayerFromSnapPoint != None:
            dataProvider = self.selectedLayerFromSnapPoint.dataProvider()
            featureIter = dataProvider.getFeatures( QgsFeatureRequest(self.pointID))
            feature = None
            for feature0 in featureIter:
                feature = feature0
            idx = self.selectedLayerFromSnapPoint.fieldNameIndex('Altitude')
            altitudeValue = feature.attributes()[idx]

            snapPoint = Point3D(self.Point.x(), self.Point.y(), altitudeValue)
        else:
            if self.Point != None:
                identifyResult = None
                idValue = "Background"
                if self.demLayerList != None:

                    for demLayer in self.demLayerList:
                        identifyResults = demLayer.dataProvider().identify(self.Point, QgsRaster.IdentifyFormatValue)
                        identifyResult = identifyResults.results()
                if identifyResult != None and identifyResult[1].toString() != "":
                    snapPoint = Point3D(self.Point.x(), self.Point.y(), float(identifyResult[1].toString()))
                else:
                    snapPoint = Point3D(self.Point.x(), self.Point.y())
        if snapPoint != None:
            self.rubberBandPt.addPoint(snapPoint)
            self.rubberBandPt.show()
        if self.isDrawing:
            if snapPoint == None:
                self.finish = Point3D(self.toMapCoordinates(e.pos()).x(), self.toMapCoordinates(e.pos()).y())
            else:
                self.finish = snapPoint
            self.drawLine()
            
    def drawLine(self):        
        pass
        
    def deactivate(self):
        self.rubberBandPt.reset(QGis.Point)
#         self.rubberBand.reset(QGis.Line)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))
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


    
class RnpTFlegJig(RnplegJig):
    def __init__(self, canvas, rnpArSegmentType, rnpArDataGroup, point3d_0, double_0, double_1, bool_0):
        RnplegJig.__init__(self, canvas, rnpArSegmentType, rnpArDataGroup, point3d_0, double_0, double_1)
        self.constantTrack = bool_0;

    def setRnpArLeg(self):    
        self.rnpArLeg = RnpArLeg(RnpArLegType.TF)
        if self.constantTrack:
            point3d = MathHelper.distanceBearingPoint(self.start, self.inbound - math.pi / 2.0, 100)
            drawPoint = MathHelper.getIntersectionPoint(self.finish,
                                        MathHelper.distanceBearingPoint(self.finish, self.inbound - math.pi / 2.0, 100),
                                        self.start, 
                                        MathHelper.distanceBearingPoint(self.start, self.inbound, 100))
            if MathHelper.smethod_115(drawPoint, self.start, point3d):
                drawPoint = self.start
            else:
                identifyResult = None
                if self.demLayerList != None:
                    for demLayer in self.demLayerList:
                        identifyResults = demLayer.dataProvider().identify(drawPoint, QgsRaster.IdentifyFormatValue)
                        identifyResult = identifyResults.results()
                    if identifyResult != None and identifyResult[1].toString() != "":
                        drawPoint = Point3D(drawPoint.x(), drawPoint.y(), float(identifyResult[1].toString()))
            self.rnpArLeg.Position = Point3D(drawPoint.x(), drawPoint.y())
        else:
            self.rnpArLeg.Position = Point3D(self.finish.x(), self.finish.y())
        distance = Distance(MathHelper.calcDistance(self.start, self.finish))
        startDegree = None
        if define._units == QGis.Meters:
            startDegree = QgisHelper.CrsTransformPoint(self.start.x(), self.start.y(), define._xyCrs, define._latLonCrs)
        else:
            startDegree = self.start
        endDegree = None
        if define._units == QGis.Meters:
            endDegree = QgisHelper.CrsTransformPoint(self.finish.x(), self.finish.y(), define._xyCrs, define._latLonCrs)
        else:
            endDegree = self.finish
        f, dist, d0, d1 = Geo.smethod_4(GeoCalculationType.Ellipsoid, startDegree.y(), startDegree.x(), endDegree.y(), endDegree.x())
        distance = dist
        altitude = self.rnpArDataGroup.method_5(self.rnpArSegmentType, None)
        if (self.rnpArSegmentType != RnpArSegmentType.Missed):
            metres = distance.Metres
            angleGradientSlope = self.rnpArDataGroup.method_3(self.rnpArSegmentType)
            altitude = altitude + Altitude(metres * (angleGradientSlope.Percent / 100))

        self.rnpArLeg.Rnp = self.rnp
        self.rnpArLeg.Segment = self.rnpArSegmentType
        self.rnpArLeg.Altitude = Altitude(altitude.Metres)#MathHelper.smethod_0(altitude.Feet, -2), AltitudeUnits.FT);
        self.rnpArLeg.Wind = Speed.NaN()
        self.rnpArLeg.Previous = self.start
        self.rnpArLeg.Position.SetZ(altitude.Metres)
            
    def drawLine(self):
        if self.constantTrack:
            point3d = MathHelper.distanceBearingPoint(self.start, self.inbound - math.pi / 2.0, 100)
            drawPoint = MathHelper.getIntersectionPoint(self.finish,
                                        MathHelper.distanceBearingPoint(self.finish, self.inbound - math.pi / 2.0, 100),
                                        self.start, 
                                        MathHelper.distanceBearingPoint(self.start, self.inbound, 100))
            if MathHelper.smethod_115(drawPoint, self.start, point3d):
                drawPoint = self.start
            
        else:
            drawPoint = self.finish
             
        self.rubberBand.reset(QGis.Polygon)
        lineGeom = QgsGeometry.fromPolyline([self.start, drawPoint])

        pt0 = MathHelper.distanceBearingPoint(self.start, MathHelper.getBearing(self.start, drawPoint) - Unit.ConvertDegToRad(90), self.width / 2.0,)
        pt1 = MathHelper.distanceBearingPoint(self.start, MathHelper.getBearing(self.start, drawPoint) + Unit.ConvertDegToRad(90), self.width / 2.0,)
        pt2 = MathHelper.distanceBearingPoint(drawPoint, MathHelper.getBearing(self.start, drawPoint) + Unit.ConvertDegToRad(90), self.width / 2.0,)
        pt3 = MathHelper.distanceBearingPoint(drawPoint, MathHelper.getBearing(self.start, drawPoint) - Unit.ConvertDegToRad(90), self.width / 2.0,)
        self.rubberBand.addPoint(pt0)
        self.rubberBand.addPoint(pt1)
        self.rubberBand.addPoint(pt2)
        self.rubberBand.addPoint(pt3)
        # bufferGeom = lineGeom.buffer(self.width / 2.0, 0, 2, 0, 0)
        # self.rubberBand.addGeometry(bufferGeom, None)
        self.rubberBand.show()

class RnpRFlegJig(RnplegJig):

    def __init__(self, canvas, rnpArSegmentType, rnpArDataGroup, point3d_0, double_0, double_1):
        RnplegJig.__init__(self, canvas, rnpArSegmentType, rnpArDataGroup, point3d_0, double_0, double_1)
        self.radius = 0.0
    
    def setRnpArLeg(self):    
        self.rnpArLeg = RnpArLeg(RnpArLegType.RF)
        if self.radius == None:
            self.rnpArLeg.Type = RnpArLegType.TF
            
        self.rnpArLeg.Inbound = self.inbound
        self.rnpArLeg.Radius = Distance(self.radius)
        self.rnpArLeg.Position = Point3D(self.finish.x(), self.finish.y())
        distance = Distance(MathHelper.calcDistance(self.start, self.finish))
        startDegree = None
        if define._units == QGis.Meters:
            startDegree = QgisHelper.CrsTransformPoint(self.start.x(), self.start.y(), define._xyCrs, define._latLonCrs)
        else:
            startDegree = self.start
        endDegree = None
        if define._units == QGis.Meters:
            endDegree = QgisHelper.CrsTransformPoint(self.finish.x(), self.finish.y(), define._xyCrs, define._latLonCrs)
        else:
            endDegree = self.finish
        f, dist, d0, d1 = Geo.smethod_4(GeoCalculationType.Ellipsoid, startDegree.y(), startDegree.x(), endDegree.y(), endDegree.x())
        distance = dist

        altitude = self.rnpArDataGroup.method_5(self.rnpArSegmentType, None)
        
        if (self.rnpArSegmentType != RnpArSegmentType.Missed):
            metres = distance.Metres
            angleGradientSlope = self.rnpArDataGroup.method_3(self.rnpArSegmentType)
            altitude = altitude + Altitude(metres * (angleGradientSlope.Percent / 100))

        self.rnpArLeg.Rnp = self.rnp
        self.rnpArLeg.Segment = self.rnpArSegmentType
        self.rnpArLeg.Altitude = Altitude(altitude.Metres)#MathHelper.smethod_0(altitude.Feet, -2), AltitudeUnits.FT);
        self.rnpArLeg.Wind = Speed.NaN()
        self.rnpArLeg.Previous = self.start
        self.rnpArLeg.Position.SetZ(altitude.Metres)
                    
    def drawLine(self):        
        self.rubberBand.reset(QGis.Polygon)
        bulge = MathHelper.smethod_59(self.inbound, self.start, self.finish)
#         if math.fabs(bulge) >= 1:
#             print bulge
        point3d2 = MathHelper.distanceBearingPoint(self.start, self.inbound + 1.5707963267949, 100);
        num = MathHelper.getBearing(self.finish, self.start);
        point3d3 = MathHelper.distanceBearingPoint(self.finish, num, MathHelper.calcDistance(self.finish, self.start) / 2);
        point3d4 = MathHelper.distanceBearingPoint(point3d3, num + 1.5707963267949, 100);
        point3d = MathHelper.getIntersectionPoint(self.start, point3d2, point3d3, point3d4)
        entity = PolylineArea([self.start, self.finish])
        if point3d != None:
            self.radius = MathHelper.calcDistance(point3d, self.start);
            entity[0].bulge = bulge
        else:
            self.radius = None
                
        lineGeom = QgsGeometry.fromPolyline(entity.getCurve(4))

        pointArray = entity.method_14(4)


        pt0 = MathHelper.distanceBearingPoint(self.start, MathHelper.getBearing(self.start, pointArray[1]) - Unit.ConvertDegToRad(90), self.width / 2.0,)
        pt1 = MathHelper.distanceBearingPoint(self.start, MathHelper.getBearing(self.start, pointArray[1]) + Unit.ConvertDegToRad(90), self.width / 2.0,)
        pt2 = MathHelper.distanceBearingPoint(self.finish, MathHelper.getBearing(pointArray[len(pointArray) - 2], self.finish) + Unit.ConvertDegToRad(90), self.width / 2.0,)
        pt3 = MathHelper.distanceBearingPoint(self.finish, MathHelper.getBearing(pointArray[len(pointArray) - 2], self.finish) - Unit.ConvertDegToRad(90), self.width / 2.0,)
        polylineArea0 = PolylineArea()
        polylineArea0.Add(PolylineAreaPoint(pt0, bulge))
        polylineArea0.Add(PolylineAreaPoint(pt3))
        polylineArea1 = PolylineArea()
        polylineArea1.Add(PolylineAreaPoint(pt2, -bulge))
        polylineArea1.Add(PolylineAreaPoint(pt1))

        for pt in polylineArea0.method_14(4):
            self.rubberBand.addPoint(pt)
        for pt in polylineArea1.method_14(4):
            self.rubberBand.addPoint(pt)
        # self.rubberBand.addPoint(pt2)
        # self.rubberBand.addPoint(pt3)

        # bufferGeom = lineGeom.buffer(self.width / 2.0, 0, 2, 0, 0)
        # self.rubberBand.addGeometry(bufferGeom, None)
        self.rubberBand.show()
