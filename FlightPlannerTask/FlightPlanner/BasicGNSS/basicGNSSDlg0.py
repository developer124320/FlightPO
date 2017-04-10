# -*- coding: utf-8 -*-
'''
Created on 17 Feb 2015

@author: Administrator
'''
from PyQt4.QtGui import QDialog, QVBoxLayout, QMenu, QMessageBox, QStandardItemModel, QPixmap, QStandardItem, QTextDocument, QPushButton, QAbstractItemView, QComboBox, QFileDialog
# from PyQt4.QtCore import Qt
from FlightPlanner.BasicGNSS.ui_BasicGNSSDlg0 import Ui_basicGNSSDlg
from PyQt4.QtCore import SIGNAL, Qt, QSize, QSizeF, QCoreApplication, QString
from PyQt4.QtGui import QFont, QLineEdit
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.BasicGNSS.ParameterDlgs.DlgCaculateWaypoint import CalcDlg
from FlightPlanner.BasicGNSS.gnssSegments import FinalApproachSegment, MissedApproachSegment, IntermediateSegment,\
                InitialSegment1, InitialSegment2, InitialSegment3
from FlightPlanner.BasicGNSS.GnssSegmentObstacles import GnssSegmentObstacles
from FlightPlanner.types import RnavSegmentType, AircraftSpeedCategory, AltitudeUnits, SpeedUnits, AngleGradientSlopeUnits,\
                Point3D, RnavCommonWaypoint, WindType, AngleUnits, SurfaceTypes
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.helpers import Speed, Altitude, AngleGradientSlope, MathHelper, Unit
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from qgis.gui import QgsTextAnnotationItem, QgsAnnotationItem, QgsRubberBand
from qgis.core import QgsPoint, QGis,QgsRectangle,  QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.expressions import Expressions
from FlightPlanner.Captions import Captions
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel

from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.QgisHelper import AerodromeAndRwyCmb
from FlightPlanner.Obstacle.Obstacle import Obstacle
from Type.String import String
import define, math

class basicGNSSDlg(FlightPlanBaseDlg):
    
    SOCAnnotation = None
    FinalAnnotation = None
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.surfaceType = SurfaceTypes.BasicGNSS
        self.layers = None
        self.setObjectName("BasicGNSS_Dialog")
        # selftabCtrlGeneral.removeTab(2)
        self.ui = Ui_basicGNSSDlg()
        self.ui.setupUi(self)
        self.resize(500, 200)
        QgisHelper.matchingDialogSize(self, 980, 600)
#         self.objectName()
        self.ui.btnEvaluate.setEnabled(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
#         self.ui.btnMarkSoc.setEnabled(False)
        self.ui.btnEvaluate_2.setEnabled(False)
        self.ui.radioBtn_Straight.setChecked(True)
        self.ui.grbImage.setStyleSheet("border-image: url(Resource/IA20.png);")
        
#         self.ui.groupBox_32.hide()
#         self.ui.groupBox_33.hide()
        self.ui.groupBox_8.hide()
        font = QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.ui.btnMarkSoc = QPushButton("")    
        self.ui.btnMarkSoc.setFont(font)  
        self.ui.btnMarkSoc.setIcon(self.ui.iconMark)
        self.ui.btnMarkSoc.setIconSize(QSize(32,32))
        self.ui.btnMarkSoc.setToolTip("Mark SOC")
        self.ui.verticalLayout_4.insertWidget(0, self.ui.btnMarkSoc)
#         self.ui.btnOpenData = QPushButton("Open Data")
#         self.ui.btnOpenData.setFont(font)
#         self.ui.verticalLayout_7.insertWidget(0, self.ui.btnOpenData)
#         
#         self.ui.btnSaveData = QPushButton("Save Data")        
#         self.ui.btnSaveData.setFont(font)
#         self.ui.verticalLayout_7.insertWidget(1, self.ui.btnSaveData)
#         self.ui.btnExportResult = QPushButton("Export Result")
#         self.ui.btnExportResult.setFont(font)
#         self.ui.verticalLayout_4.insertWidget(3, self.ui.btnExportResult)
        self.ui.btnExportResult.setDisabled(True)
        self.ui.btnExportResult.clicked.connect(self.exportResult)
        self.ui.btnOpenData.clicked.connect(self.openData)
        self.ui.btnSaveData.clicked.connect(self.saveData)
                
#         self.ui.btnUpdateQA_2.hide()
        self.socRubber = []
        self.socAnnotation = []
        QgisHelper.ClearCanvas(define._canvas)
        
#         self.segmendtsModel = QStandardItemModel()
#         icon = QIcon()
#         icon.addPixmap(QPixmap("Resource/apply.png"), QIcon.Normal, QIcon.Off)
#         item1 = QStandardItem(icon, "Missed Approach")
#         self.segmendtsModel.setItem(0, 0, item1)
#         item2 = QStandardItem(icon, "Final Approach")
#         self.segmendtsModel.setItem(1, 0, item2)
#         item3 = QStandardItem(icon, "Intermediate")
#         self.segmendtsModel.setItem(2, 0, item3)
#         item4 = QStandardItem(icon, "Initial 1")
#         self.segmendtsModel.setItem(3, 0, item4)
#         item5 = QStandardItem(icon, "Initial 2")
#         self.segmendtsModel.setItem(4, 0, item5)
#         item6 = QStandardItem(icon, "Initial 3")
#         self.segmendtsModel.setItem(5, 0, item6)        
#         self.ui.trvSegments.setModel(self.segmendtsModel)
#         index1 = self.segmendtsModel.indexFromItem(item2)
#         self.ui.trvSegments.setCurrentIndex(index1) 
#         self.connect(self.ui.trvSegments , SIGNAL("clicked(QModelIndex)"), self.segmentsChange)
        
        graphicsItems = define._canvas.items()
        scene = define._canvas.scene()
        for item in graphicsItems:
            item._class_ = QgsAnnotationItem
            if isinstance(item, QgsAnnotationItem) : 
                scene.removeItem( item)
            else:
                item._class_ = QgsRubberBand
                if isinstance(item, QgsRubberBand):
                    scene.removeItem( item)
        
#         self.collapseAllInLayout(self.ui.verticalLayout_parameters)
        self.ui.frame_MocMA.setVisible(True)
#         
# #         self.ui.cmbDataGroup.addItem("test")
        self.ui.cmbCategory.addItems(["A", "B", "C", "D", "E", "H", "Custom"])
        self.ui.cmbCategory.currentIndexChanged.connect(self.changeCategory)
        self.ui.cmbCategory.setCurrentIndex(3)
        
        self.ui.cmbConstruction.addItems(["2D", "3D"])
        self.ui.txtIsa.setText("15")
#         
        self.annotationARP = QgsTextAnnotationItem(define._canvas)
        self.annotationARP.setDocument(QTextDocument("ARP"))
#         self.annotationARP.setMapPosition(QgsPoint(664465.4750, 6616266.0911))
        self.annotationARP.hide()

        arpFrame = Frame(self.ui.groupBox_7)
        arpFrame.layoutBoxPanel.setMargin(9)
        self.ui.horizontalLayout_14.insertWidget(0, arpFrame)

        self.cmbAerodrome = ComboBoxPanel(arpFrame, True)
        self.cmbAerodrome.Caption = "Aerodrome"
        self.cmbAerodrome.LabelWidth = 120
        arpFrame.Add = self.cmbAerodrome

        self.cmbRwyDir = ComboBoxPanel(arpFrame, True)
        self.cmbRwyDir.Caption = "Runway Direction"
        self.cmbRwyDir.LabelWidth = 120
        self.cmbRwyDir.Width = 120
        arpFrame.Add = self.cmbRwyDir

        self.gbARP = PositionPanel(self.ui.groupBox_7, self.annotationARP)
        self.gbARP.setObjectName("positionARP")
        self.gbARP.groupBox.setTitle("Aerodrom / Heliport Reference Point")
        
#         self.gbARP.txtPointX.setText("664465.4750")
#         self.gbARP.txtPointY.setText("6616266.0911")
        self.gbARP.hideframe_Altitude()
        self.gbARP.btnCalculater.setVisible(False)
        arpFrame.Add = self.gbARP
        self.gbARP.btnCapture.clicked.connect(self.buttunsDisable)
# 
        self.ui.cmbUnits.addItems(["meter", "feet"])
        self.ui.cmbUnits.setCurrentIndex(1)
        self.ui.cmbSurface.addItems(["All", RnavSegmentType.MissedApproach, RnavSegmentType.FinalApproach, RnavSegmentType.Intermediate, RnavSegmentType.Initial1, RnavSegmentType.Initial2, RnavSegmentType.Initial3])
        
        self.hLayout_RunwayTHR = QVBoxLayout(self.ui.frame_2)
        self.hLayout_RunwayTHR.setSpacing(0)
        self.hLayout_RunwayTHR.setMargin(0)
        self.hLayout_RunwayTHR.setObjectName("hLayout_RunwayTHR")
        
        self.gbRunwayTHR = PositionPanel(self.ui.frame_2)
        self.gbRunwayTHR.setObjectName("positionRunwayTHR")
        self.gbRunwayTHR.groupBox.setTitle("Runway THR")
#         self.gbARP.txtPointX.setText("664465.4750")
#         self.gbARP.txtPointY.setText("6616266.0911")
        self.gbRunwayTHR.hideframe_Altitude()
        self.gbRunwayTHR.btnCalculater.setVisible(False)
        self.hLayout_RunwayTHR.addWidget(self.gbRunwayTHR)
        self.gbRunwayTHR.btnCapture.clicked.connect(self.buttunsDisable)

        self.gbRunwayEnd = PositionPanel(self.ui.frame_2)
        self.gbRunwayEnd.setObjectName("positionRunwayEnd")
        self.gbRunwayEnd.groupBox.setTitle("Runway End")
#         self.gbARP.txtPointX.setText("664465.4750")
#         self.gbARP.txtPointY.setText("6616266.0911")
        self.gbRunwayEnd.hideframe_Altitude()
        self.gbRunwayEnd.btnCalculater.setVisible(False)
        self.hLayout_RunwayTHR.addWidget(self.gbRunwayEnd)
        self.gbRunwayEnd.btnCapture.clicked.connect(self.buttunsDisable)



        # self.hLayout_RunwayTHR.addWidget(self.ui.frame_18_1)
#         self.ui.cmbRnavSpecification.addItems(["Rnav5", "Rnav2", "Rnav1", "Rnp4", "Rnp2", "Rnp1", "ARnp2", "ARnp1", "ARnp09", "ARnp08", "ARnp07", "ARnp06", "ARnp05", "ARnp04", "ARnp03", "RnpApch"])
#         self.ui.cmbRnavSpecification.setCurrentIndex(2)
        self.verticalLayout_grbPoints = QVBoxLayout(self)
        self.verticalLayout_grbPoints.setSpacing(0)
        self.verticalLayout_grbPoints.setMargin(0)
        self.verticalLayout_grbPoints.setObjectName("verticalLayout_grbPoints")
#         
        self.annotationMAHWP = QgsTextAnnotationItem(define._canvas)
        self.annotationMAHWP.setDocument(QTextDocument("MAHF"))
        self.annotationMAHWP.hide()
#         self.annotationMAHWP.setMapPosition(QgsPoint(663824.4766, 6608668.6437))
        
        self.verticalLayout_MAPoints = QVBoxLayout(self.ui.frameMA_Point)
        self.verticalLayout_MAPoints.setSpacing(0)
        self.verticalLayout_MAPoints.setMargin(0)
        self.verticalLayout_MAPoints.setObjectName("verticalLayout_MAPoints")
        
        self.gbMAHWP = PositionPanel(self.ui.frameMA_Point, self.annotationMAHWP)
        self.gbMAHWP.groupBox.setTitle("MAHF")
        self.gbMAHWP.setObjectName("positionMAHWP")
#         self.gbMAHWP.setPosition(663824.4766, 6608668.6437)
#         self.ui.verticalLayout_grbPoints.addWidget(self.gbMAHWP)
        self.gbMAHWP.btnCalculater.clicked.connect(self.calcMAHWP_Dlg)
        self.gbMAHWP.btnCapture.clicked.connect(self.buttunsDisable)
        self.gbMAHWP.txtPointX.textChanged.connect(self.drawLineBand)
        self.gbMAHWP.txtPointY.textChanged.connect(self.drawLineBand)
        self.gbMAHWP.hideframe_Altitude()
        self.verticalLayout_MAPoints.addWidget(self.gbMAHWP)
#                 
        self.annotationMAWP = QgsTextAnnotationItem(define._canvas)
        self.annotationMAWP.setDocument(QTextDocument("MAPt"))
        self.annotationMAWP.hide()
#         self.annotationMAWP.setMapPosition(QgsPoint(664685.0273, 6617887.9264))
        self.gbMAWP = PositionPanel(self.ui.frameMA_Point, self.annotationMAWP)
        self.gbMAWP.groupBox.setTitle("MAPt")
        self.gbMAWP.setObjectName("positionMAWP")
        self.gbMAWP.btnCalculater.setVisible(False)
#         self.gbMAWP.setPosition(664685.0273, 6617887.9264)
#         self.ui.verticalLayout_grbPoints.addWidget(self.gbMAWP)
        self.gbMAWP.btnCalculater.clicked.connect(self.calcMAWP_Dlg)
        self.gbMAWP.btnCapture.clicked.connect(self.buttunsDisable)
        self.gbMAWP.txtPointX.textChanged.connect(self.drawLineBand)
        self.gbMAWP.txtPointY.textChanged.connect(self.drawLineBand)
        self.gbMAWP.hideframe_Altitude()
        self.verticalLayout_MAPoints.addWidget(self.gbMAWP)
#         
        self.annotationFAWP = QgsTextAnnotationItem(define._canvas)
        self.annotationFAWP.setDocument(QTextDocument("FAF"))
        self.annotationFAWP.hide()
        
        self.verticalLayout_FAPoints = QVBoxLayout(self.ui.frameFA_Point)
        self.verticalLayout_FAPoints.setSpacing(0)
        self.verticalLayout_FAPoints.setMargin(0)
        self.verticalLayout_FAPoints.setObjectName("verticalLayout_FAPoints")
        
#         self.annotationFAWP.setMapPosition(QgsPoint(665605.8453, 6627101.4135))
        self.gbFAWP = PositionPanel(self.ui.frameFA_Point, self.annotationFAWP)
        self.gbFAWP.groupBox.setTitle("FAF")
        self.gbFAWP.setObjectName("positionFAWP")
#         self.gbFAWP.setPosition(665605.8453, 6627101.4135)
#         self.ui.verticalLayout_grbPoints.addWidget(self.gbFAWP)
        self.gbFAWP.btnCalculater.clicked.connect(self.calcFAWP_Dlg)
        self.gbFAWP.btnCapture.clicked.connect(self.buttunsDisable)
        self.gbFAWP.txtPointX.textChanged.connect(self.drawLineBand)
        self.gbFAWP.txtPointY.textChanged.connect(self.drawLineBand)
#         self.gbFAWP.frame_Altitude.setVisible(False)
        self.gbFAWP.hideframe_Altitude()
        self.verticalLayout_FAPoints.addWidget(self.gbFAWP)
        
        
        self.verticalLayout_IAPoints = QVBoxLayout(self.ui.frameIA_Point)
        self.verticalLayout_IAPoints.setSpacing(0)
        self.verticalLayout_IAPoints.setMargin(0)
        self.verticalLayout_IAPoints.setObjectName("verticalLayout_IAPoints")
         
        self.annotationIWP = QgsTextAnnotationItem(define._canvas)
        self.annotationIWP.setDocument(QTextDocument("IF"))
        self.annotationIWP.hide()
#         self.annotationIWP.setMapPosition(QgsPoint(666977.3404, 6641852.8886))
        self.gbIWP = PositionPanel(self.ui.frameIA_Point, self.annotationIWP)
        self.gbIWP.groupBox.setTitle("IF")
        self.gbIWP.setObjectName("positionIWP")
#         self.gbIWP.setPosition(666977.3404, 6641852.8886)
#         self.ui.verticalLayout_grbPoints.addWidget(self.gbIWP)
        self.gbIWP.btnCalculater.clicked.connect(self.calcIWP_Dlg)
        self.gbIWP.btnCapture.clicked.connect(self.buttunsDisable)
        self.gbIWP.txtPointX.textChanged.connect(self.drawLineBand)
        self.gbIWP.txtPointY.textChanged.connect(self.drawLineBand)
        self.gbIWP.hideframe_Altitude()
        self.verticalLayout_IAPoints.addWidget(self.gbIWP)
#         
        self.annotationIAWP1 = QgsTextAnnotationItem(define._canvas)
        self.annotationIAWP1.setDocument(QTextDocument("IAFR"))
        self.annotationIAWP1.hide()
#         self.annotationIAWP1.setMapPosition(QgsPoint(657757.3195,6642704.7333))
        self.gbIAWP1 = PositionPanel(self.ui.frameIW1, self.annotationIAWP1)        
        self.gbIAWP1.groupBox.setTitle("IAFR")
        self.gbIAWP1.setObjectName("positionIAWP1")
#         self.gbIAWP1.setPosition(657757.3195,6642704.7333)
        self.ui.verticalLayout_IW1.insertWidget(0, self.gbIAWP1)
        self.gbIAWP1.btnCalculater.clicked.connect(self.calcIAWP1_Dlg)
        self.gbIAWP1.btnCapture.clicked.connect(self.buttunsDisable)
        self.gbIAWP1.txtPointX.textChanged.connect(self.drawLineBand)
        self.gbIAWP1.txtPointY.textChanged.connect(self.drawLineBand)
        self.gbIAWP1.hideframe_Altitude()
#         
        self.annotationIAWP2 = QgsTextAnnotationItem(define._canvas)
        self.annotationIAWP2.setDocument(QTextDocument("IAFC"))
        self.annotationIAWP2.hide()
#         self.annotationIAWP2.setMapPosition(QgsPoint(667829.0442, 6651073.1104))
        self.gbIAWP2 = PositionPanel(self.ui.frameIW2, self.annotationIAWP2)
        self.gbIAWP2.groupBox.setTitle("IAFC")
        self.gbIAWP2.setObjectName("positionIAWP2")
#         self.gbIAWP2.setPosition(667829.0442, 6651073.1104)
        self.ui.verticalLayout_IW2.insertWidget(0, self.gbIAWP2)
        self.gbIAWP2.btnCalculater.clicked.connect(self.calcIAWP2_Dlg)
        self.gbIAWP2.btnCapture.clicked.connect(self.buttunsDisable)
        self.gbIAWP2.txtPointX.textChanged.connect(self.drawLineBand)
        self.gbIAWP2.txtPointY.textChanged.connect(self.drawLineBand)
        self.gbIAWP2.hideframe_Altitude()
#         
        self.annotationIAWP3 = QgsTextAnnotationItem(define._canvas)
        self.annotationIAWP3.setDocument(QTextDocument("IAFL"))
        self.annotationIAWP3.hide()
#         self.annotationIAWP3.setMapPosition(QgsPoint(676197.7064, 6641000.9784))
        self.gbIAWP3 = PositionPanel(self.ui.frameIW3, self.annotationIAWP3)
        self.gbIAWP3.groupBox.setTitle("IAFL")
        self.gbIAWP3.hideframe_Altitude()
        self.gbIAWP3.setObjectName("positionIAWP3")
#         self.gbIAWP3.setPosition(676197.7064, 6641000.9784)
        self.ui.verticalLayout_IW3.insertWidget(0, self.gbIAWP3)
        self.gbIAWP3.btnCalculater.clicked.connect(self.calcIAWP3_Dlg)
        self.gbIAWP3.btnCapture.clicked.connect(self.buttunsDisable)
        self.gbIAWP3.txtPointX.textChanged.connect(self.drawLineBand)
        self.gbIAWP3.txtPointY.textChanged.connect(self.drawLineBand)
#                 
#         self.ui.verticalLayout_grbPoints.setSpacing(0)
#         self.ui.verticalLayout_grbPoints.setContentsMargins(0, 0, 0, 0)
#         self.collapseAllInLayout(self.ui.verticalLayout_grbPoints)
#         self.gbMAWP.setVisible(True)
#         self.gbFAWP.setVisible(True)
        self.RwyTHR = None
        self.RwyEND = None 
        self.parameterCalcList = []
        self.ui.btnConstruct.clicked.connect(self.construct)
#         self.ui.btnUpdateQA.clicked.connect(self.updateQA)
        self.ui.btnEvaluate.clicked.connect(self.evalute)
        self.ui.btnClose.clicked.connect(self.reject)
        self.ui.btnClose_2.clicked.connect(self.reject)
        self.ui.cmbSurface.currentIndexChanged.connect(self.cmbSurfaceChanged)
        self.ui.btnEvaluate_2.clicked.connect(self.locate)
        self.ui.btnMarkSoc.clicked.connect(self.markSoc)
        self.ui.btnMarkSoc.setEnabled(False)
        self.ui.chbInsertSymbols.stateChanged.connect(self.annotationFlag)
        
        
        self.ui.cmbRnavSpecification.addItems(["Rnav1", "Rnp1", "ARnp1", "ARnp09", "ARnp08", "ARnp07", "ARnp06", "ARnp05", "ARnp04", "ARnp03", "RnpApch"])
        self.ui.cmbRnavSpecification_2.addItems(["Rnav1", "Rnp1", "ARnp1", "ARnp09", "ARnp08", "ARnp07", "ARnp06", "ARnp05", "ARnp04", "ARnp03", "RnpApch"])
        self.ui.cmbRnavSpecification_3.addItems(["Rnav1", "Rnp1", "ARnp2", "ARnp1", "ARnp09", "ARnp08", "ARnp07", "ARnp06", "ARnp05", "ARnp04", "ARnp03", "RnpApch"])
        self.ui.cmbRnavSpecification_4.addItems(["Rnav1", "Rnp1", "ARnp2", "ARnp1", "ARnp09", "ARnp08", "ARnp07", "ARnp06", "ARnp05", "ARnp04", "ARnp03", "RnpApch"])
        self.ui.cmbRnavSpecification_5.addItems(["Rnav1", "Rnp1", "ARnp2", "ARnp1", "ARnp09", "ARnp08", "ARnp07", "ARnp06", "ARnp05", "ARnp04", "ARnp03", "RnpApch"])
            
        self.ui.cmbRnavSpecification.currentIndexChanged.connect(self.cmbRnavSpecificationChanged)
        self.ui.cmbRnavSpecification_2.currentIndexChanged.connect(self.cmbRnavSpecificationChanged_2)
        self.ui.cmbRnavSpecification_3.currentIndexChanged.connect(self.cmbRnavSpecificationChanged_3)
        self.ui.cmbRnavSpecification_4.currentIndexChanged.connect(self.cmbRnavSpecificationChanged_4)
        self.ui.cmbRnavSpecification_5.currentIndexChanged.connect(self.cmbRnavSpecificationChanged_5)
        
#         
        self.obstaclesModel = GnssSegmentObstacles(None)
        self.obstaclesModel.setSurfaceType(SurfaceTypes.BasicGNSS)
#         
        self.ui.tblObstacles.setModel(self.obstaclesModel)
        self.ui.tblObstacles.setSortingEnabled(True)
#         
#         define._canvas.mapUnitsChanged.connect(self.changeMapUnit)
        self.ui.cmbUnits.currentIndexChanged.connect(self.setResultPanel)
#         self.ui.txtWindIA1.setEnabled(False)
#         self.ui.txtWindIA3.setEnabled(False)
#         self.ui.cmbWindIA1.addItems(["ICAO", "UK", "Custom"])
#         self.ui.cmbWindIA3.addItems(["ICAO", "UK", "Custom"])
        self.ui.txtAltitudeIA1.textChanged.connect(self.changeWindIA1)
        altitude = Altitude(float(self.ui.txtAltitudeIA1.text()), AltitudeUnits.FT)
        if altitude != None:
            self.ui.pnlWindIA1.setAltitude(altitude) 
        self.ui.txtAltitudeIA3.textChanged.connect(self.changeWindIA3)
        altitude = Altitude(float(self.ui.txtAltitudeIA3.text()), AltitudeUnits.FT)
        if altitude != None:
            self.ui.pnlWindIA3.setAltitude(altitude) 
         
        self.lineBand = QgsRubberBand(define._canvas, QGis.Line)
        self.lineBand.setColor(Qt.red)
        self.lineBand.setWidth(1.5)
         
        self.ui.tblObstacles.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblObstacles.clicked.connect(self.tblObstaclesClicked)
        self.ui.tblObstacles.verticalHeader().sectionClicked.connect(self.tblObstaclesClicked)
         
#         lstTextControls = self.ui.groupBox_11.findChildren(QLineEdit)
#         for ctrl in lstTextControls:
#             ctrl.textChanged.connect(self.initResultPanel)
             
        lstTextControls = self.ui.groupBox_11.findChildren(QComboBox)
        for ctrl in lstTextControls:
            ctrl.currentIndexChanged.connect(self.initResultPanel)
        self.ui.tabControlSegments.currentChanged.connect(self.tabControlSegmentsCurrentChanged)
        
        self.ui.radioBtn_T_Bar.clicked.connect(self.radioTClicked)
        self.ui.radioBtn_Y_Bar.clicked.connect(self.radioYClicked)
        self.ui.radioBtn_Straight.clicked.connect(self.radioSClicked)
        
        self.ui.btnCriticalLocate.clicked.connect(self.btnCriticalLocateClicked)
        
        
        self.selectedRnavSpecificationFA = "Rnav1"
        self.selectedRnavSpecificationMA = "Rnav1"
        self.selectedRnavSpecificationIA = "Rnav1"
        self.selectedRnavSpecificationIW1 = "Rnav1"
        self.selectedRnavSpecificationIW2 = "Rnav1"
        self.selectedRnavSpecificationIW3 = "Rnav1"
        
        self.selectedRnavSpecificationFAIndex = 0
        self.selectedRnavSpecificationMAIndex = 0
        self.selectedRnavSpecificationIAIndex = 0
        
        self.ui.txtCriticalAltitudeFt.setEnabled(False)
        self.ui.txtCriticalAltitudeM.setEnabled(False)
        self.ui.txtCriticalID.setEnabled(False)
        self.ui.txtCriticalSurface.setEnabled(False)
        self.ui.txtCriticalX.setEnabled(False)
        self.ui.txtCriticalY.setEnabled(False)
        
#         self.gbRunwayTHR.btnCapture.clicked
        
        self.radioBtnStr = ""
        # self.gbRunwayTHR.txtPointY.textChanged.connect(self.CalcRwyBearing)
        # self.gbRunwayEnd.txtPointY.textChanged.connect(self.CalcRwyBearing)
        self.connect(self.gbRunwayTHR, SIGNAL("positionChanged"), self.CalcRwyBearing)
        self.connect(self.gbRunwayEnd, SIGNAL("positionChanged"), self.CalcRwyBearing)

        self.connect(self.ui.tblObstacles, SIGNAL("tableViewObstacleMouseReleaseEvent_rightButton"), self.tableViewObstacleMouseTeleaseEvent_rightButton)
        self.connect(self.ui.tblObstacles, SIGNAL("pressedEvent"), self.tblObstacles_pressed)
        
        
        self.gbIAWP1.setVisible(False)
        self.ui.gbParamIW_1.setVisible(False)
        self.gbIAWP3.setVisible(False)
        self.ui.gbParamIW_3.setVisible(False)

        self.nominalPolylineAreaList = []
        self.trackRadialPanelSetEnabled()

        self.arpFeatureArray = []
        self.currentLayer = define._canvas.currentLayer()
        self.rwyFeatureArray = []
        self.initAerodromeAndRwyCmb()

        self.resultLayerList = []

        self.criticalObstaclesBySurfaces = dict()
    def initAerodromeAndRwyCmb(self):
        # self.currentLayer = define._canvas.currentLayer()
        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.arpFeatureArray = self.aerodromeAndRwyCmbFill(self.currentLayer, self.cmbAerodrome, self.gbARP, self.cmbRwyDir)
            # AerodromeAndRwyCmb.aerodromeAndRwyCmbFill(self.currentLayer, self.cmbAerodrome, self.gbARP, self.cmbRwyDir, self.gbRunwayTHR, self.gbRunwayEnd)


#         self.ui.horizontalLayout_6.addWidget(self.ui.frame_3)
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
                aerodromeCmbObjItems = []
                for feat in arpFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    items = aerodromeCmbObj.Items
                    if len(items) != 0:
                        existFlag = False
                        for item in items:
                            if item == attrValue:
                                existFlag = True
                        if existFlag:
                            continue
                    aerodromeCmbObjItems.append(attrValue)
                aerodromeCmbObjItems.sort()
                aerodromeCmbObj.Items = aerodromeCmbObjItems
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

                    aerodromePositionPanelObj.Point3d = Point3D(long, lat, alt)
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

                    # items = rwyDirCmbObj.Items
                    # if len(items) != 0:
                    #     rwyDirCmbObj.SelectedIndex = 0
                    #     for feat in rwyFeatList:
                    #         attrValue = feat.attributes()[idxName].toString()
                    #         if attrValue != rwyDirCmbObj.SelectedItem:
                    #             continue
                    #         latAttrValue = feat.attributes()[idxLat].toDouble()
                    #         lat = latAttrValue[0]
                    #
                    #         longAttrValue = feat.attributes()[idxLong].toDouble()
                    #         long = longAttrValue[0]
                    #
                    #         altAttrValue = feat.attributes()[idxAltitude].toDouble()
                    #         alt = altAttrValue[0]
                    #
                    #         self.gbRunwayTHR.Point3d = Point3D(long, lat, alt)
                    #
                    #         valStr = None
                    #         if attrValue.right(1).toUpper() =="L" or attrValue.right(1).toUpper() =="R":
                    #             s = attrValue.right(attrValue.length() - 1)
                    #             valStr = s.right(2)
                    #         else:
                    #             valStr = attrValue.right(2)
                    #         val = int(valStr)
                    #         val += 18
                    #         if val > 36:
                    #             val -= 36
                    #         newValStr = None
                    #         if len(str(val)) == 1:
                    #             newValStr = "0" + str(val)
                    #         else:
                    #             newValStr = str(val)
                    #         otherAttrValue = attrValue.replace(valStr, newValStr)
                    #         for feat in rwyFeatList:
                    #             attrValue = feat.attributes()[idxName].toString()
                    #             if attrValue != otherAttrValue:
                    #                 continue
                    #             latAttrValue = feat.attributes()[idxLat].toDouble()
                    #             lat = latAttrValue[0]
                    #
                    #             longAttrValue = feat.attributes()[idxLong].toDouble()
                    #             long = longAttrValue[0]
                    #
                    #             altAttrValue = feat.attributes()[idxAltitude].toDouble()
                    #             alt = altAttrValue[0]
                    #
                    #             self.gbRunwayEnd.Point3d = Point3D(long, lat, alt)
                    #             break
                    #         break

                    # if len(rwyFeatList) != 0:
                    #     for feat in rwyFeatList:







        return arpFeatureList
    def rwyDirCmbObj_Event_0(self):
        if len(self.rwyFeatureArray) == 0:
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
            itemStr = self.cmbRwyDir.SelectedItem
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

            self.gbRunwayTHR.Point3d = Point3D(long, lat, alt)

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

                self.gbRunwayEnd.Point3d = Point3D(long, lat, alt)
                break
            break
    def aerodromeCmbObj_Event_0(self):
        if len(self.arpFeatureArray) == 0:
            return
        self.gbARP.Point3d = None
        self.gbRunwayTHR.Point3d = None
        self.gbRunwayEnd.Point3d = None
        idxName = self.currentLayer.fieldNameIndex('Name')
        idxLat = self.currentLayer.fieldNameIndex('Latitude')
        idxLong = self.currentLayer.fieldNameIndex('Longitude')
        idxAltitude = self.currentLayer.fieldNameIndex('Altitude')
        self.rwyFeatureArray = []
        # if idxAttributes
        for feat in self.arpFeatureArray:
            attrValue = feat.attributes()[idxName].toString()
            if attrValue != self.cmbAerodrome.SelectedItem:
                continue
            attrValue = feat.attributes()[idxLat].toDouble()
            lat = attrValue[0]

            attrValue = feat.attributes()[idxLong].toDouble()
            long = attrValue[0]

            attrValue = feat.attributes()[idxAltitude].toDouble()
            alt = attrValue[0]

            self.gbARP.Point3d = Point3D(long, lat, alt)
            break
        idxAttr = self.currentLayer.fieldNameIndex('Attributes')
        if idxAttr >= 0:
            self.cmbRwyDir.Clear()
            rwyFeatList = []
            featIter = self.currentLayer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idxAttr].toString()
                if attrValue == self.cmbAerodrome.SelectedItem:
                    attrValue = feat.attributes()[idxName].toString()
                    s = attrValue.replace(" ", "")
                    compStr = s.left(6).toUpper()
                    if compStr == "THRRWY":
                        valStr = s.right(s.length() - 6)
                        self.cmbRwyDir.Add(self.cmbAerodrome.SelectedItem + " RWY " + valStr)
                        rwyFeatList.append(feat)
                        self.rwyFeatureArray = rwyFeatList
            self.rwyDirCmbObj_Event_0()
        # resultValueList.append(altitudeValue.toString())
        #     pass
        # altitudeValue = feature.attributes()[idx]

        # resultValueList.append(altitudeValue.toString())

    def tblObstacles_pressed(self, modelIndex):
        self.selectedObstacleMoselIndex = modelIndex
    def tableViewObstacleMouseTeleaseEvent_rightButton(self, e):
        if self.obstaclesModel == None:
            return
        featID = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexObjectId)).toString()
        layerID = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexLayerId)).toString()
        name = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexName)).toString()
        xValue = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexX)).toString()
        yValue = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexY)).toString()
        altitudeMValue = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexAltM)).toString()
        surfaceName = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexSurface)).toString()
        ocaMValue = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexOcaM)).toString()
        # ocaMValue = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexOcaM)).toString()
        obstacle = Obstacle(name, Point3D(float(xValue), float(yValue), float(altitudeMValue)), layerID, featID, None, 0.0, self.obstaclesModel.MocMultiplier, 0.0)
        self.changedCriticalObstacleValue = {"Obstacle": obstacle,
                                             "SurfaceName": surfaceName,
                                             "OcaM": float(ocaMValue) if ocaMValue != "" else None}


        menu = QMenu()
        actionSetCriticalObst = QgisHelper.createAction(menu, "Set Most Critical Obstacles", self.menuSetCriticalObstClick)
        menu.addAction( actionSetCriticalObst )
        menu.exec_( self.ui.tblObstacles.mapToGlobal(e.pos() ))
    def menuSetCriticalObstClick(self):
        obstacle = self.changedCriticalObstacleValue["Obstacle"]
        self.ui.txtCriticalID.setText(str(obstacle.name))
        self.ui.txtCriticalX.setText(str(obstacle.position.get_X()))
        self.ui.txtCriticalY.setText(str(obstacle.position.get_Y()))
        try:
            self.ui.txtCriticalAltitudeM.setText(str(obstacle.position.get_Z()))
        except:
            self.ui.txtCriticalAltitudeM.setText(str(0.0))
        try:
            self.ui.txtCriticalAltitudeFt.setText(str(Altitude(obstacle.position.get_Z()).Feet))
        except:
            self.ui.txtCriticalAltitudeFt.setText(str(0.0))
        self.ui.txtCriticalSurface.setText(self.changedCriticalObstacleValue["SurfaceName"])

        surfaceName = self.changedCriticalObstacleValue["SurfaceName"]
        oca = self.changedCriticalObstacleValue["OcaM"]
        tempValFt = None
        tempValM = None
        try:
            tempValM = float(oca)
            if self.ui.cmbUnits.currentText() == "feet":
                tempValFt = Unit.ConvertMeterToFeet(tempValM)
                oca = tempValFt
        except:
            pass


        self.ui.txtOCA.setText(RnavSegmentType.FinalApproach)
        if self.changedCriticalObstacleValue["SurfaceName"] == RnavSegmentType.FinalApproach:
            self.ui.txtOCAResults.setText(str(round(oca, 2)))
                    # else:
        #     self.ui.txtOCAResults.setText(Captions.GROUND_PLANE)

        self.ui.txtOCH.setText(RnavSegmentType.MissedApproach)
        if self.changedCriticalObstacleValue["SurfaceName"] == RnavSegmentType.MissedApproach:
            self.ui.txtOCHResults.setText(str(round(oca, 2)))
        # else:
        #     self.ui.txtOCHResults.setText(Captions.GROUND_PLANE)

        self.ui.txtOCH_2.setText(RnavSegmentType.Intermediate)
        if self.changedCriticalObstacleValue["SurfaceName"] == RnavSegmentType.Intermediate:
            self.ui.txtOCHResults_2.setText(str(round(oca, 2)))
        # else:
        #     self.ui.txtOCHResults_2.setText(Captions.GROUND_PLANE)

        self.ui.txtOCA_2.setText(RnavSegmentType.Initial1)
        if self.changedCriticalObstacleValue["SurfaceName"] == RnavSegmentType.Initial1:
            self.ui.txtOCAResults_2.setText(str(round(oca, 2)))
        # else:
        #     self.ui.txtOCAResults_2.setText(Captions.GROUND_PLANE)

        self.ui.txtOCH_3.setText(RnavSegmentType.Initial2)
        if self.changedCriticalObstacleValue["SurfaceName"] == RnavSegmentType.Initial2:
            self.ui.txtOCHResults_3.setText(str(round(oca, 2)))
        # else:
        #     self.ui.txtOCHResults_3.setText(Captions.GROUND_PLANE)

        self.ui.txtOCH_4.setText(RnavSegmentType.Initial3)
        if self.changedCriticalObstacleValue["SurfaceName"] == RnavSegmentType.Initial3:
            self.ui.txtOCHResults_4.setText(str(round(oca, 2)))
        # else:
        #     self.ui.txtOCHResults_4.setText(Captions.GROUND_PLANE)
        if tempValM != None:
            self.criticalObstaclesBySurfaces.__setitem__(String.QString2Str(self.changedCriticalObstacleValue["SurfaceName"]), [str(round(tempValM, 2)) + " m", str(round(tempValFt, 2)) + " ft"])
        else:
            self.criticalObstaclesBySurfaces.__setitem__(String.QString2Str(self.changedCriticalObstacleValue["SurfaceName"]), [Captions.GROUND_PLANE, Captions.GROUND_PLANE])




    def trackRadialPanelSetEnabled(self):
        positionPanels = self.findChildren(PositionPanel)
        flag = False
        if len(positionPanels) > 0:
            flag = False
            for pnl in positionPanels:
                if pnl.IsValid():
                    flag = True
                    break
        trPanels = self.findChildren(TrackRadialBoxPanel)
        if len(trPanels) > 0:
            for pnl in trPanels:
                pnl.Enabled = flag
    def btnCriticalLocateClicked(self):
        point = None
        try:
            point = QgsPoint(float(self.ui.txtCriticalX.text()), float(self.ui.txtCriticalY.text()))
        except:
            return
        if define._units == QGis.Meters:
            extent = QgsRectangle(point.x() - 350, point.y() - 350, point.x() + 350, point.y() + 350)
        else:
            extent = QgsRectangle(point.x() - 0.005, point.y() - 0.005, point.x() + 0.005, point.y() + 0.005)

        if extent is None:
            return           
 
        QgisHelper.zoomExtent(point, extent, 2)
 
    def getExtentForLocate(self, point):
        extent = None
#         surfaceType = self.source.item(sourceRow, self.IndexSurface).text()
        surfaceLayers = QgisHelper.getSurfaceLayers(SurfaceTypes.BasicGNSS)
        for sfLayer in surfaceLayers:
            lId = sfLayer.name()
            if lId.contains(self.ui.txtCriticalSurface.text()):
                extent = sfLayer.extent()
                break
        return extent
    def radioSClicked(self):
        self.ui.grbImage.setStyleSheet("border-image: url(Resource/IA20.png);")
        self.radioBtnStr = "Straight"
        self.gbIAWP1.setVisible(False)
        self.ui.gbParamIW_1.setVisible(False)
        self.gbIAWP3.setVisible(False)
        self.ui.gbParamIW_3.setVisible(False)
    def radioYClicked(self):
        self.ui.grbImage.setStyleSheet("border-image: url(Resource/IA30.png);")
        self.radioBtnStr = "Y-Bar"
        
        self.gbIAWP1.setVisible(True)
        self.ui.gbParamIW_1.setVisible(True)
        self.gbIAWP3.setVisible(True)
        self.ui.gbParamIW_3.setVisible(True)
    def radioTClicked(self):
        self.ui.grbImage.setStyleSheet("border-image: url(Resource/IA10.png);")
        self.radioBtnStr = "T-Bar"
        self.gbIAWP1.setVisible(True)
        self.ui.gbParamIW_1.setVisible(True)
        self.gbIAWP3.setVisible(True)
        self.ui.gbParamIW_3.setVisible(True)
    
    def cmbRnavSpecificationChanged(self, index):
        if self.ui.tabControlSegments.currentIndex() == 1:
            self.selectedRnavSpecificationMA = self.ui.cmbRnavSpecification.currentText()
            self.selectedRnavSpecificationMAIndex = self.ui.cmbRnavSpecification.currentIndex()
        elif self.ui.tabControlSegments.currentIndex() == 2:
            self.selectedRnavSpecificationFA = self.ui.cmbRnavSpecification.currentText()
            self.selectedRnavSpecificationFAIndex = self.ui.cmbRnavSpecification.currentIndex()
        elif self.ui.tabControlSegments.currentIndex() == 3:
            self.selectedRnavSpecificationIA = self.ui.cmbRnavSpecification.currentText()
            self.selectedRnavSpecificationIAIndex = self.ui.cmbRnavSpecification.currentIndex()
    def cmbRnavSpecificationChanged_2(self, index):
        self.selectedRnavSpecificationIA = self.ui.cmbRnavSpecification_2.currentText()
    def cmbRnavSpecificationChanged_3(self, index):
        self.selectedRnavSpecificationIW1 = self.ui.cmbRnavSpecification_3.currentText()
    def cmbRnavSpecificationChanged_4(self, index):
        self.selectedRnavSpecificationIW2 = self.ui.cmbRnavSpecification_4.currentText()
    def cmbRnavSpecificationChanged_5(self, index):
        self.selectedRnavSpecificationIW3 = self.ui.cmbRnavSpecification_5.currentText()
    def tabControlSegmentsCurrentChanged(self, index):
#         self.ui.cmbRnavSpecification.clear()
        if index == 1:
            self.resize(400, 200)
            
            self.ui.horizontalLayout_5.addWidget(self.ui.groupBox_6)
            self.verticalLayout_MAPoints.insertWidget(1, self.gbMAWP)
#             if self.selectedRnavSpecificationMAIndex != 0:
            self.ui.cmbRnavSpecification.setCurrentIndex(self.selectedRnavSpecificationMAIndex)
            
            print self.selectedRnavSpecificationMAIndex
            self.ui.frame_RNVA.setVisible(True)
            self.ui.frame_IasMA.setVisible(True)
            self.ui.frame_MocMA1.setVisible(True)
            self.ui.frame_MocMA2.setVisible(True)
            self.ui.frame_SOC.setVisible(True)
            self.ui.frame_MA.setVisible(True)
            self.ui.frame_MocMA.setVisible(False)
            self.ui.frame_MocI.setVisible(False)
            self.ui.frame_MocIA1.setVisible(False)
            self.ui.frame_MocIA2.setVisible(False)
            self.ui.frame_MocIA3.setVisible(False)
            self.ui.frame_AltitudeIA1.setVisible(False)
            self.ui.frame_AltitudeIA3.setVisible(False)
            self.ui.frame_BankIA1.setVisible(False)
            self.ui.frame_BankIA3.setVisible(False)
            self.ui.frame_IasIA1.setVisible(False)
            self.ui.frame_IasIA3.setVisible(False)
            self.ui.pnlWindIA1.setVisible(False)
            self.ui.pnlWindIA3.setVisible(False)
        elif index == 2:
            self.resize(400, 200)
            self.verticalLayout_FAPoints.insertWidget(0, self.gbMAWP)
            self.ui.horizontalLayout_6.addWidget(self.ui.groupBox_6)
            self.verticalLayout_FAPoints.insertWidget(1, self.gbFAWP)
#             if self.selectedRnavSpecificationFAIndex != 0:
#             self.ui.cmbConstruction.setCurrentIndex(self.selectedRnavSpecificationFAIndex)
            
            self.ui.frame_RNVA.setVisible(False)
            self.ui.frame_IasMA.setVisible(False)
            self.ui.frame_MocMA1.setVisible(False)
            self.ui.frame_MocMA2.setVisible(False)
            self.ui.frame_SOC.setVisible(False)
            self.ui.frame_MA.setVisible(False)
            self.ui.frame_MocMA.setVisible(True)
            self.ui.frame_MocI.setVisible(False)
            self.ui.frame_MocIA1.setVisible(False)
            self.ui.frame_MocIA2.setVisible(False)
            self.ui.frame_MocIA3.setVisible(False)
            self.ui.frame_AltitudeIA1.setVisible(False)
            self.ui.frame_AltitudeIA3.setVisible(False)
            self.ui.frame_BankIA1.setVisible(False)
            self.ui.frame_BankIA3.setVisible(False)
            self.ui.frame_IasIA1.setVisible(False)
            self.ui.frame_IasIA3.setVisible(False)
            self.ui.pnlWindIA1.setVisible(False)
            self.ui.pnlWindIA3.setVisible(False)
        elif index == 3:
            self.resize(400, 200)
#             self.ui.cmbRnavSpecification.addItems(["Rnav1", "Rnp1", "ARnp2", "ARnp1", "ARnp09", "ARnp08", "ARnp07", "ARnp06", "ARnp05", "ARnp04", "ARnp03", "RnpApch"])
            self.ui.horizontalLayout_7.addWidget(self.ui.groupBox_6)
            self.verticalLayout_IAPoints.insertWidget(0, self.gbFAWP)
            self.verticalLayout_IAPoints.insertWidget(1, self.gbIWP)
            self.ui.groupBox_6.layout().addWidget(self.ui.frame_MocI)
#             if self.selectedRnavSpecificationIAIndex != 0:
            self.ui.cmbRnavSpecification.setCurrentIndex(self.selectedRnavSpecificationIAIndex)
            print self.selectedRnavSpecificationIAIndex
            self.ui.frame_RNVA.setVisible(True)
            self.ui.frame_IasMA.setVisible(False)
            self.ui.frame_MocMA1.setVisible(False)
            self.ui.frame_MocMA2.setVisible(False)
            self.ui.frame_SOC.setVisible(False)
            self.ui.frame_MA.setVisible(False)
            self.ui.frame_MocMA.setVisible(False)
            self.ui.frame_MocI.setVisible(True)
            self.ui.frame_MocIA1.setVisible(False)
            self.ui.frame_MocIA2.setVisible(False)
            self.ui.frame_MocIA3.setVisible(False)
            self.ui.frame_AltitudeIA1.setVisible(False)
            self.ui.frame_AltitudeIA3.setVisible(False)
            self.ui.frame_BankIA1.setVisible(False)
            self.ui.frame_BankIA3.setVisible(False)
            self.ui.frame_IasIA1.setVisible(False)
            self.ui.frame_IasIA3.setVisible(False)
            self.ui.pnlWindIA1.setVisible(False)
            self.ui.pnlWindIA3.setVisible(False)
        elif index == 4:
#             self.ui.horizontalLayout_7.addWidget(self.ui.groupBox_6)
            self.ui.verticalLayout_IW.insertWidget(0, self.gbIWP)
            
            self.ui.verticalLayout_ParamIW.addWidget(self.ui.frame_MocI)
            
            
            self.ui.verticalLayout_ParamIW1.addWidget(self.ui.frame_IasIA1)
            self.ui.verticalLayout_ParamIW1.addWidget(self.ui.frame_AltitudeIA1)
            self.ui.verticalLayout_ParamIW1.addWidget(self.ui.frame_BankIA1)
            self.ui.verticalLayout_ParamIW1.addWidget(self.ui.pnlWindIA1)
            self.ui.verticalLayout_ParamIW1.addWidget(self.ui.frame_MocIA1)
            self.ui.frame_IasIA1.setVisible(True)
            self.ui.frame_AltitudeIA1.setVisible(True)
            self.ui.frame_BankIA1.setVisible(True)
            self.ui.pnlWindIA1.setVisible(True)
            self.ui.frame_MocIA1.setVisible(True)
            
            self.ui.verticalLayout_ParamIW2.addWidget(self.ui.frame_MocIA2)
            self.ui.frame_MocIA2.setVisible(True)
            
            self.ui.verticalLayout_ParamIW3.addWidget(self.ui.frame_IasIA3)
            self.ui.verticalLayout_ParamIW3.addWidget(self.ui.frame_AltitudeIA3)
            self.ui.verticalLayout_ParamIW3.addWidget(self.ui.frame_BankIA3)
            self.ui.verticalLayout_ParamIW3.addWidget(self.ui.pnlWindIA3)
            self.ui.verticalLayout_ParamIW3.addWidget(self.ui.frame_MocIA3)
            self.ui.frame_IasIA3.setVisible(True)
            self.ui.frame_AltitudeIA3.setVisible(True)
            self.ui.frame_BankIA3.setVisible(True)
            self.ui.pnlWindIA3.setVisible(True)
            self.ui.frame_MocIA3.setVisible(True)
            self.ui.cmbRnavSpecification_2.setCurrentIndex(self.selectedRnavSpecificationIAIndex)
#         print index
    def saveData(self):
        try:
            filePathDir = QFileDialog.getSaveFileName(self, "Save Input Data",QCoreApplication.applicationDirPath (),"Xml Files(*.xml)")        
            if filePathDir == "":
                return
            otherParam = [("ComboIndexs", [("MA", self.selectedRnavSpecificationMAIndex), ("FA", self.selectedRnavSpecificationFAIndex), ("IA", self.selectedRnavSpecificationIAIndex)]),\
                           ("RadioConditions", [("Y-Bar", str(self.ui.radioBtn_Y_Bar.isChecked())), ("Straight", str(self.ui.radioBtn_Straight.isChecked())), ("T-Bar", str(self.ui.radioBtn_T_Bar.isChecked()))])]
            
            DataHelper.saveInputParameters(filePathDir, self, otherParam)
            
            return filePathDir
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
#         fileName = FlightPlanBaseDlg.saveData(self)
#         if fileName == None:
#             return
#         doc = DataHelper.loadXmlDocFromFile(fileName)
#         dialogNodeList = doc.elementsByTagName(self.objectName())
#         if dialogNodeList.isEmpty():
#             raise UserWarning, "This file is not correct."
#         dialogElem = dialogNodeList.at(0).toElement()
#         
#         elemCmbIndexs= doc.createElement("CmbIndexs")
#         elemCmbMAIndex = doc.createElement("MA")
#         elemCmbMAIndex.appendChild(doc.createTextNode(str(self.selectedRnavSpecificationMAIndex)))
#         elemCmbFAIndex = doc.createElement("FA")
#         elemCmbFAIndex.appendChild(doc.createTextNode(str(self.selectedRnavSpecificationFAIndex)))
#         elemCmbIAIndex = doc.createElement("IA")
#         elemCmbIAIndex.appendChild(doc.createTextNode(str(self.selectedRnavSpecificationIAIndex)))
#         elemCmbIndexs.appendChild(elemCmbMAIndex)
#         elemCmbIndexs.appendChild(elemCmbFAIndex)
#         elemCmbIndexs.appendChild(elemCmbIAIndex)
#         dialogElem.appendChild(elemCmbIndexs)
#         if self.RwyEND !=None and self.RwyTHR != None:            
#             elemTrack = doc.createElement("Runway")            
#             elemStart = doc.createElement("RwyTHR")
#             elemX = doc.createElement("X")
#             elemX.appendChild(doc.createTextNode(str(self.RwyTHR.x())))
#             elemY = doc.createElement("Y")
#             elemY.appendChild(doc.createTextNode(str(self.RwyTHR.y())))
#             elemStart.appendChild(elemX)
#             elemStart.appendChild(elemY)
#             elemTrack.appendChild(elemStart)
#     
#             elemEnd = doc.createElement("RwyEND")
#             elemX = doc.createElement("X")
#             elemX.appendChild(doc.createTextNode(str(self.RwyEND.x())))
#             elemY = doc.createElement("Y")
#             elemY.appendChild(doc.createTextNode(str(self.RwyEND.y())))
#             elemEnd.appendChild(elemX)
#             elemEnd.appendChild(elemY)
#             elemTrack.appendChild(elemEnd)
#             dialogElem.appendChild(elemTrack)
#             
#         if len(self.parameterCalcList) > 0:
#             elemParameter = doc.createElement("CalculaterParameters")
#             for i in range(len(self.parameterCalcList)):
#                 if self.parameterCalcList[i] == None:
#                     elemBearing = doc.createElement("Bearing")
#                     elemBearing.appendChild(doc.createTextNode(""))
#                     elemDistance = doc.createElement("Distance")
#                     elemDistance.appendChild(doc.createTextNode(""))
#                     elemParameter.appendChild(elemBearing)
#                     elemParameter.appendChild(elemDistance)
#                 else:
#                     strBearing, strDistance = self.parameterCalcList[i]
#                     elemBearing = doc.createElement("Bearing")
#                     elemBearing.appendChild(doc.createTextNode(strBearing))
#                     elemDistance = doc.createElement("Distance")
#                     elemDistance.appendChild(doc.createTextNode(strDistance))
#                     elemParameter.appendChild(elemBearing)
#                     elemParameter.appendChild(elemDistance)
#             dialogElem.appendChild(elemParameter)         
#         DataHelper.saveXmlDocToFile(fileName, doc)
        

    def openData(self):
        try:
            filePathDir = QFileDialog.getOpenFileName(self, "Open Input Data",QCoreApplication.applicationDirPath (),"Xml Files(*.xml)")        
            if filePathDir == "":
                return
            layers = define._canvas.layers()
            if layers != None and len(layers) > 0:
                for layer in layers:
                    if layer.name() == "Symbols":
                        self.currentLayer = layer
                        try:
                            self.initAerodromeAndRwyCmb()
                        except:
                            pass
                        try:
                            self.initBasedOnCmb()
                        except:
                            pass
                        break

            resultOtherParam = []
            DataHelper.loadInputParameters(filePathDir, self, ["ComboIndexs", "RadioConditions"], resultOtherParam)
            self.selectedRnavSpecificationMAIndex = resultOtherParam[0][1].toInt()[0]
            self.selectedRnavSpecificationFAIndex = resultOtherParam[1][1].toInt()[0]
            self.selectedRnavSpecificationIAIndex = resultOtherParam[2][1].toInt()[0]
            
            if resultOtherParam[3][1] == "True":
                self.ui.radioBtn_Y_Bar.setChecked(True)
                self.radioYClicked()
            elif resultOtherParam[4][1] == "True":
                self.ui.radioBtn_Straight.setChecked(True)
                self.radioSClicked()
            else:
                self.ui.radioBtn_T_Bar.setChecked(True)
                self.radioTClicked()
#             print resultOtherParam
            if self.gbIWP.Point3d != None:
                self.annotationIWP.setMapPosition(self.gbIWP.Point3d)
                self.annotationIWP.show()
            if self.gbIAWP3.Point3d != None:
                self.annotationIAWP3.setMapPosition(self.gbIAWP3.Point3d)
                self.annotationIAWP3.show()
            if self.gbIAWP2.Point3d != None:
                self.annotationIAWP2.setMapPosition(self.gbIAWP2.Point3d)
                self.annotationIAWP2.show()
            if self.gbIAWP1.Point3d != None:
                self.annotationIAWP1.setMapPosition(self.gbIAWP1.Point3d)
                self.annotationIAWP1.show()
            if self.gbARP.Point3d != None:
                self.annotationARP.setMapPosition(self.gbARP.Point3d)
                self.annotationARP.show()
            if self.gbFAWP.Point3d != None:
                self.annotationFAWP.setMapPosition(self.gbFAWP.Point3d)
                self.annotationFAWP.show()
            if self.gbMAHWP.Point3d != None:
                self.annotationMAHWP.setMapPosition(self.gbMAHWP.Point3d)
                self.annotationMAHWP.show()
            if self.gbMAWP.Point3d != None:
                self.annotationMAWP.setMapPosition(self.gbMAWP.Point3d)
                self.annotationMAWP.show()
            return filePathDir
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
        

    def initResultPanel(self):
        if self.obstaclesModel != None and self.ui.btnEvaluate.isEnabled():
            self.obstaclesModel.clear()
            
            self.ui.btnExportResult.setEnabled(False)
            lstTextControls = self.ui.groupBox.findChildren(QLineEdit)
            for ctrl in lstTextControls:
                ctrl.setText("")
        self.ui.btnEvaluate.setEnabled(False)
        
    def tblObstaclesClicked(self, idx):
        if len(self.ui.tblObstacles.selectedIndexes()) > 0:
            self.ui.btnEvaluate_2.setEnabled(True)
    def locate(self):
        selectedRowIndexes = self.ui.tblObstacles.selectedIndexes()
        self.obstaclesModel.locate(selectedRowIndexes)
#         QMessageBox.warning(self, "info", self.obstaclesModel.data(selectedRowIndexes[1]).toString())
        pass
    def markSoc(self):
        if len(self.socRubber) < 2:
            self.socRubber = [QgsRubberBand(define._canvas, QGis.Line), QgsRubberBand(define._canvas, QGis.Line)]
        for soc in self.socRubber:
            soc.reset(QGis.Line)
            soc.setWidth(10)
            soc.setColor(Qt.red)
        
        num1 = MathHelper.getBearing(self.gbMAWP.getPoint3D(), self.gbMAHWP.getPoint3D())
        num = 5 * (math.pi / 2) - (num1 + math.pi) if not MathHelper.smethod_136(num1, AngleUnits.Radians) else 5 * (math.pi / 2) - num1
        point3d = MathHelper.distanceBearingPoint(self.obstaclesModel.surfacesList[1].SOC(), num1 + math.pi / 2, 100)
        self.socRubber[0].addPoint(self.obstaclesModel.surfacesList[1].SOC())
        self.socRubber[0].addPoint(point3d)
        self.socRubber[0].show()
        
#         DBText dBText = AcadHelper.smethod_140(Captions.SOC, point3d, 50, 1, 3);
#         dBText.set_Rotation(num);
#         AcadHelper.smethod_18(transaction, blockTableRecord, dBText, str);
        if basicGNSSDlg.SOCAnnotation == None:
            basicGNSSDlg.SOCAnnotation = QgsTextAnnotationItem(define._canvas)
            basicGNSSDlg.SOCAnnotation.setDocument(QTextDocument(Captions.SOC))
            basicGNSSDlg.SOCAnnotation.setFrameBackgroundColor(Qt.white)
            basicGNSSDlg.SOCAnnotation.setFrameSize(QSizeF(30, 20))
            basicGNSSDlg.SOCAnnotation.setFrameColor(Qt.magenta)
        
        basicGNSSDlg.SOCAnnotation.setMapPosition(point3d)
        basicGNSSDlg.SOCAnnotation.show()

        point3d = MathHelper.distanceBearingPoint(self.obstaclesModel.surfacesList[1].StartOfFinalMA(), num1 + math.pi / 2, 100)
        self.socRubber[1].addPoint(self.obstaclesModel.surfacesList[1].StartOfFinalMA())
        self.socRubber[1].addPoint(point3d)
        self.socRubber[1].show()
        
#         AcadHelper.smethod_18(transaction, blockTableRecord, new Line(BasicGnssApproachObstacleAnalyser.startOfFinalMA, point3d), str);
#         dBText = AcadHelper.smethod_140(Captions.FINAL_MISSED_APPROACH, point3d, 50, 1, 3);
#         dBText.set_Rotation(num);
#         AcadHelper.smethod_18(transaction, blockTableRecord, dBText, str);
        if basicGNSSDlg.FinalAnnotation == None:
            basicGNSSDlg.FinalAnnotation = QgsTextAnnotationItem(define._canvas)
            basicGNSSDlg.FinalAnnotation.setDocument(QTextDocument(Captions.FINAL_MISSED_APPROACH))
            basicGNSSDlg.FinalAnnotation.setFrameBackgroundColor(Qt.white)
            basicGNSSDlg.FinalAnnotation.setFrameSize(QSizeF(30, 20))
            basicGNSSDlg.FinalAnnotation.setFrameColor(Qt.magenta)
        
        basicGNSSDlg.FinalAnnotation.setMapPosition(point3d)
        basicGNSSDlg.FinalAnnotation.show()
        pass
    
    def changeMapUnit(self):
        self.ui.btnEvaluate.setEnabled(False)
    def collapseAllInLayout(self, layout):
        i = 0
        while (i < layout.count()):
            item = layout.itemAt(i).widget()
            item.setVisible(False)
            i += 1
        
    def cmbSurfaceChanged(self):
        if self.ui.cmbSurface.currentIndex() == 0 and self.ui.cmbSurface.currentText() == "All":
            self.obstaclesModel.setFilterFixedString("")
        else:
            self.obstaclesModel.setFilterFixedString(str(self.ui.cmbSurface.currentText()))
        if self.obstaclesModel.rowCount() == 0:
            self.ui.btnEvaluate_2.setEnabled(False)
#         self.obstaclesModel.setVerticalHeader()
    def segmentsChange(self, modelIndex):
        selectSegId = modelIndex.row()
        if selectSegId == 0:
            self.ui.grbImage.setStyleSheet("border-image: url(Resource/MissedApproach.png);")
            self.collapseAllInLayout(self.ui.verticalLayout_grbPoints)
            self.gbMAHWP.setVisible(True)
            self.gbMAWP.setVisible(True)
            self.collapseAllInLayout(self.ui.verticalLayout_parameters)
            self.ui.frame_RNVA.setVisible(True)
            self.ui.frame_IasMA.setVisible(True)
            self.ui.frame_MocMA1.setVisible(True)
            self.ui.frame_MocMA2.setVisible(True)
            self.ui.frame_SOC.setVisible(True)
            self.ui.frame_MA.setVisible(True)
        elif selectSegId == 1:
            self.ui.grbImage.setStyleSheet("border-image: url(Resource/FinalApproach.png);")
            self.collapseAllInLayout(self.ui.verticalLayout_grbPoints)
            self.gbMAWP.setVisible(True)
            self.gbFAWP.setVisible(True)
            self.collapseAllInLayout(self.ui.verticalLayout_parameters)
            self.ui.frame_MocMA.setVisible(True)
        elif selectSegId == 2:
            self.ui.grbImage.setStyleSheet("border-image: url(Resource/Intermediate.png);")
            self.collapseAllInLayout(self.ui.verticalLayout_grbPoints)
            self.gbFAWP.setVisible(True)
            self.gbIWP.setVisible(True)
            self.collapseAllInLayout(self.ui.verticalLayout_parameters)
            self.ui.frame_RNVA.setVisible(True)
            self.ui.frame_MocI.setVisible(True)
        elif selectSegId == 3:
            self.ui.grbImage.setStyleSheet("border-image: url(Resource/IA1.png);")
            self.collapseAllInLayout(self.ui.verticalLayout_grbPoints)
            self.gbIWP.setVisible(True)
            self.gbIAWP1.setVisible(True)
            self.collapseAllInLayout(self.ui.verticalLayout_parameters)
            self.ui.frame_RNVA.setVisible(True)
            self.ui.frame_IasIA1.setVisible(True)
            self.ui.frame_AltitudeIA1.setVisible(True)
            self.ui.frame_BankIA1.setVisible(True)
            self.ui.pnlWindIA1.setVisible(True)
            self.ui.frame_MocIA1.setVisible(True)
        elif selectSegId == 4:
            self.ui.grbImage.setStyleSheet("border-image: url(Resource/IA2.png);")
            self.collapseAllInLayout(self.ui.verticalLayout_grbPoints)
            self.gbIWP.setVisible(True)
            self.gbIAWP2.setVisible(True)
            self.collapseAllInLayout(self.ui.verticalLayout_parameters)
            self.ui.frame_RNVA.setVisible(True)            
            self.ui.frame_MocIA2.setVisible(True)           
        elif selectSegId == 5:
            self.ui.grbImage.setStyleSheet("border-image: url(Resource/IA3.png);")
            self.collapseAllInLayout(self.ui.verticalLayout_grbPoints)
            self.gbIWP.setVisible(True)
            self.gbIAWP3.setVisible(True)
            self.collapseAllInLayout(self.ui.verticalLayout_parameters)
            self.ui.frame_RNVA.setVisible(True)
            self.ui.frame_IasIA3.setVisible(True)
            self.ui.frame_AltitudeIA3.setVisible(True)
            self.ui.frame_BankIA3.setVisible(True)
            self.ui.pnlWindIA3.setVisible(True)
            self.ui.frame_MocIA3.setVisible(True)
    def calcMAHWP_Dlg(self):
        try:
            position = self.gbFAWP.getPoint3D()
            position1 = self.gbMAWP.getPoint3D()
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
            return
        if position == None or position1 == None:
            QMessageBox.warning(self, "Error", "Please input Final Approach Waypoint and Missed Approach Waypoint.", buttons=QMessageBox.Ok, defaultButton=QMessageBox.NoButton)
            return
        try:
            positionList = [self.gbMAHWP.getPoint3D()]
        except UserWarning :
            positionList = [None]
        calcMAHWPDlg = CalcDlg(self, RnavCommonWaypoint.MAHWP, self.ui.cmbCategory.currentIndex(), position, position1, positionList)
#         calcMAHWPDlg.ui = CalcSimpleDlg()
#         calcMAHWPDlg.ui.setupUi(calcMAHWPDlg)
        calcMAHWPDlg.setWindowTitle("Calculate MAHF")
#         calcMAHWPDlg.ui.lbl1.setText(unicode("Acceptable bearings are 181.3° - 195.3°", "utf-8"))
#         calcMAHWPDlg.ui.lbl2.setText(unicode("Acceptable minimum distance is 1 nm", "utf-8"))
        calcMAHWPDlg.txtForm.setText("MAPt")
        calcMAHWPDlg.groupBox_5.setVisible(False)
        calcMAHWPDlg.groupBox_4.setVisible(False)
        calcMAHWPDlg.lblDistance.setText("Distance (nm):")
#         calcMAHWPDlg.ui.txtBearing.setText("187.86")
        calcMAHWPDlg.txtDistance.setEnabled(True)
        if len(self.parameterCalcList) > 2 and self.parameterCalcList[2] != None :
            str1, str2 = self.parameterCalcList[2]
            calcMAHWPDlg.txtBearing.setText(str1)
            calcMAHWPDlg.txtDistance.setText(str2)
        calcMAHWPDlg.show()
        self.annotationMAHWP.show()
    def calcMAWP_Dlg(self):
        try:
            position3 = self.gbFAWP.getPoint3D()
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
            return
        try:
            positionList = [self.RwyTHR, self.RwyEND, self.gbMAWP.getPoint3D()]
        except UserWarning:
            positionList = [self.RwyTHR, self.RwyEND, None]
        calcMAWPDlg = CalcDlg(self, RnavCommonWaypoint.MAWP, self.ui.cmbCategory.currentIndex(), position3, None, positionList)
        calcMAWPDlg.setWindowTitle("Calculate MAWP")
        calcMAWPDlg.lbl2.setVisible(False)
#         calcMAWPDlg.txtForm.setText("FAWP")
#         calcMAWPDlg.txtBearing.setText("188.25")
        calcMAWPDlg.txtDistance.setText("Abeam THR")
        calcMAWPDlg.txtDistance.setEnabled(False)
        calcMAWPDlg.btnCaptureDistance.setVisible(False)
        calcMAWPDlg.lblDistance.setText("Distance:")
        calcMAWPDlg.txtDistance.setText("Abeam THR")
        if len(self.parameterCalcList) > 1 and self.parameterCalcList[1] != None :
            str1, str2 = self.parameterCalcList[1]
            calcMAWPDlg.txtBearing.setText(str1)
            calcMAWPDlg.txtDistance.setText(str2)
#         calcMAWPDlg.txtTHR_X.setText(self.gbMAWP.txtPointX.text())
#         calcMAWPDlg.txtTHR_Y.setText(self.gbMAWP.txtPointY.text())
        calcMAWPDlg.show()
        self.annotationMAWP.show()
    def calcFAWP_Dlg(self):
        try:
            self.RwyTHR = self.gbRunwayTHR.Point3d
        except UserWarning:
            QMessageBox.warning(self, "Warning", "You must input basic data!")
            return
        try:
            self.RwyEND = self.gbRunwayEnd.Point3d
        except UserWarning:
            QMessageBox.warning(self, "Warning", "You must input basic data!")
            return
        try:
            positionList = [self.RwyTHR, self.RwyEND, self.gbFAWP.getPoint3D()]
        except UserWarning:
            positionList = [self.RwyTHR, self.RwyEND, None]
        calcFAWPDlg = CalcDlg(self, RnavCommonWaypoint.FAWP, self.ui.cmbCategory.currentIndex(), None, None, positionList)
#         calcFAWPDlg.ui = CalcDlg()
#         calcFAWPDlg.ui.setupUi(calcFAWPDlg)
        calcFAWPDlg.setWindowTitle("Calculate FAF")
        calcFAWPDlg.groupBox_4.setVisible(False)
        calcFAWPDlg.groupBox_5.setVisible(False)
        calcFAWPDlg.resize(200,100)
#         calcFAWPDlg.lbl1.setText(unicode("Acceptable bearings are 355.4° - 025.4°", "utf-8"))
#         calcFAWPDlg.lbl2.setText(unicode("Acceptable minimum distance is 3 nm", "utf-8"))
        calcFAWPDlg.txtForm.setText("MAPt")
        if len(self.parameterCalcList) > 0 and self.parameterCalcList[0] != None :
            str1, str2 = self.parameterCalcList[0]
            calcFAWPDlg.txtBearing.setText(str1)
            calcFAWPDlg.txtDistance.setText(str2)
#         calcFAWPDlg.txtBearing.setText("007.86")
#         calcFAWPDlg.txtDistance.setText("")
        calcFAWPDlg.txtDistance.setEnabled(True)
        self.annotationFAWP.show()
        calcFAWPDlg.show()
    def calcIWP_Dlg(self):
        try:
            position6 = self.gbMAWP.getPoint3D()
            position7 = self.gbFAWP.getPoint3D()
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
            return
        try:
            positionList = [self.gbIWP.getPoint3D()]
        except UserWarning:
            positionList = [None]
        calcIWPDlg = CalcDlg(self, RnavCommonWaypoint.IWP, self.ui.cmbCategory.currentIndex(), position6, position7, positionList)
        calcIWPDlg.setWindowTitle("Calculate IF")
        calcIWPDlg.groupBox_5.setVisible(False)
        calcIWPDlg.groupBox_4.setVisible(False)
        calcIWPDlg.txtForm.setText("FAF")
        calcIWPDlg.lblDistance.setText("Distance (nm):")
        calcIWPDlg.txtDistance.setEnabled(True)
        if len(self.parameterCalcList) > 3 and self.parameterCalcList[3] != None :
            str1, str2 = self.parameterCalcList[3]
            calcIWPDlg.txtBearing.setText(str1)
            calcIWPDlg.txtDistance.setText(str2)
        calcIWPDlg.show()
        self.annotationIWP.show()
    def calcIAWP1_Dlg(self):
        try:
            position9 = self.gbFAWP.getPoint3D()
            position10 = self.gbIWP.getPoint3D()
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
            return
        try:
            positionList = [self.gbIAWP1.getPoint3D()]
        except UserWarning:
            positionList = [None]
        
        calcIAWP1Dlg = CalcDlg(self, RnavCommonWaypoint.IAWP1, self.ui.cmbCategory.currentIndex(), position9, position10, positionList, self.radioBtnStr)
        calcIAWP1Dlg.setWindowTitle("Calculate IAFR")
        calcIAWP1Dlg.txtForm.setText("IF")
        calcIAWP1Dlg.groupBox_4.setVisible(False)
        calcIAWP1Dlg.groupBox_5.setVisible(False)
        calcIAWP1Dlg.lblDistance.setText("Distance (nm):")
        calcIAWP1Dlg.txtDistance.setEnabled(True)
#         if len(self.parameterCalcList) > 4 and self.parameterCalcList[4] != None :
#             str1, str2 = self.parameterCalcList[4]
#             calcIAWP1Dlg.txtBearing.setText(str1)
#             calcIAWP1Dlg.txtDistance.setText(str2)
        calcIAWP1Dlg.show()
        self.annotationIAWP1.show()
    def calcIAWP2_Dlg(self):
        try:
            position9 = self.gbFAWP.getPoint3D()
            position10 = self.gbIWP.getPoint3D()
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
            return
        try:
            positionList = [self.gbIAWP2.getPoint3D()]
        except UserWarning:
            positionList = [None]
        calcIAWP2Dlg = CalcDlg(self, RnavCommonWaypoint.IAWP2, self.ui.cmbCategory.currentIndex(), position9, position10, positionList, self.radioBtnStr)
        calcIAWP2Dlg.setWindowTitle("Calculate IAFC")
        calcIAWP2Dlg.txtForm.setText("IF")
        calcIAWP2Dlg.groupBox_4.setVisible(False)
        calcIAWP2Dlg.groupBox_5.setVisible(False)
        calcIAWP2Dlg.lblDistance.setText("Distance (nm):")
        calcIAWP2Dlg.txtDistance.setEnabled(True)
#         if len(self.parameterCalcList) > 5 and self.parameterCalcList[5] != None :
#             str1, str2 = self.parameterCalcList[5]
#             calcIAWP2Dlg.txtBearing.setText(str1)
#             calcIAWP2Dlg.txtDistance.setText(str2)
        calcIAWP2Dlg.show()
        self.annotationIAWP2.show()
    def calcIAWP3_Dlg(self):
        try:
            position9 = self.gbFAWP.getPoint3D()
            position10 = self.gbIWP.getPoint3D()
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
            return
        try:
            positionList = [self.gbIAWP3.getPoint3D()]
        except UserWarning:
            positionList = [None]
        calcIAWP3Dlg = CalcDlg(self, RnavCommonWaypoint.IAWP3, self.ui.cmbCategory.currentIndex(), position9, position10, positionList, self.radioBtnStr)
        calcIAWP3Dlg.setWindowTitle("Calculate IAFL")
        calcIAWP3Dlg.txtForm.setText("IF")
        calcIAWP3Dlg.groupBox_4.setVisible(False)
        calcIAWP3Dlg.groupBox_5.setVisible(False)
        calcIAWP3Dlg.lblDistance.setText("Distance (nm):")
        calcIAWP3Dlg.txtDistance.setEnabled(True)
#         if len(self.parameterCalcList) > 6 and self.parameterCalcList[6] != None :
#             str1, str2 = self.parameterCalcList[6]
#             calcIAWP3Dlg.txtBearing.setText(str1)
#             calcIAWP3Dlg.txtDistance.setText(str2)
        calcIAWP3Dlg.show()
        self.annotationIAWP3.show()
    def construct(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        try:
            QgisHelper.removeFromCanvas(define._canvas, define._surfaceLayers)
            gnssMapLayers = []
#             self.selectedRnavSpecification = self.ui.cmbRnavSpecification.currentText()
            self.aircraftSpeedCategory = self.ui.cmbCategory.currentIndex()

            finalApproachSegment = FinalApproachSegment(self.gbIWP.getPoint3D(), self.gbFAWP.getPoint3D(), self.gbMAWP.getPoint3D(),
                                                     self.gbARP.getPoint3D(),
                                                     self.selectedRnavSpecificationFA,
                                                     self.aircraftSpeedCategory,
                                                     float(self.ui.TxtMocFA.text()))
            self.nominalPolylineAreaList.append(finalApproachSegment.nominalLine)
            missedApproachSegment = MissedApproachSegment(self.gbMAWP.getPoint3D(),
                                                      self.gbMAHWP.getPoint3D(),
                                                      self.gbARP.getPoint3D(),
                                                      self.selectedRnavSpecificationMA,
                                                      self.aircraftSpeedCategory,
                                                      Altitude(float(self.ui.TxtMocFA.text())),
                                                      float(self.ui.txtIsa.text()),
                                                      Speed(float(self.ui.txtIasMA.text()), SpeedUnits.KTS),
                                                      Altitude(float(self.ui.txtMocMA1.text())),
                                                      Altitude(float(self.ui.txtMocMA2.text())),
                                                      Altitude(float(self.ui.txtSocAltitude.text()), AltitudeUnits.FT),
                                                      AngleGradientSlope(float(self.ui.txtMACG.text()), AngleGradientSlopeUnits.Percent))
            self.nominalPolylineAreaList.append(missedApproachSegment.nominalLine)
            intermediateSegment = IntermediateSegment(self.gbIAWP2.getPoint3D(),
                                                    self.gbIWP.getPoint3D(),
                                                    self.gbFAWP.getPoint3D(),
                                                    self.gbMAWP.getPoint3D(),
                                                    self.selectedRnavSpecificationIA,
                                                    self.aircraftSpeedCategory,
                                                    Altitude(float(self.ui.TxtMocI.text())))
            self.nominalPolylineAreaList.append(intermediateSegment.nominalLine)
            initialSegment2 = InitialSegment2(self.gbIAWP2.getPoint3D(),
                                                self.gbIWP.getPoint3D(),
                                                self.gbFAWP.getPoint3D(),
                                                self.gbARP.getPoint3D(),
                                                self.selectedRnavSpecificationIW2,
                                                self.aircraftSpeedCategory,
                                                Altitude(float(self.ui.TxtMocIA2.text())))
            self.nominalPolylineAreaList.append(initialSegment2.nominalLine)
            if self.ui.radioBtn_Straight.isChecked():

                self.obstaclesModel.surfacesList = [finalApproachSegment,
                                                    missedApproachSegment,
                                                    intermediateSegment,
                                                    initialSegment2]

            else:
                initialSegment1 = InitialSegment1(self.gbIAWP1.getPoint3D(),
                                                self.gbIWP.getPoint3D(),
                                                self.gbFAWP.getPoint3D(),
                                                self.gbARP.getPoint3D(),
                                                self.selectedRnavSpecificationIW1,
                                                self.aircraftSpeedCategory,
                                                Speed(float(self.ui.txtIasIA1.text()), SpeedUnits.KTS),
                                                Altitude(float(self.ui.txtAltitudeIA1.text()), AltitudeUnits.FT),
                                                float(self.ui.txtIsa.text()),
                                                float(self.ui.txtBankIA1.text()),
                                                Speed(float(self.ui.pnlWindIA1.speedBox.text()), SpeedUnits.KTS),
                                                Altitude(float(self.ui.TxtMocIA1.text())))
                self.nominalPolylineAreaList.append(initialSegment1.nominalLine)
                initialSegment3 = InitialSegment3(self.gbIAWP3.getPoint3D(),
                                                self.gbIWP.getPoint3D(),
                                                self.gbFAWP.getPoint3D(),
                                                self.gbARP.getPoint3D(),
                                                self.selectedRnavSpecificationIW3,
                                                self.aircraftSpeedCategory,
                                                Speed(float(self.ui.txtIasIA3.text()), SpeedUnits.KTS),
                                                Altitude(float(self.ui.txtAltitudeIA3.text()), AltitudeUnits.FT),
                                                float(self.ui.txtIsa.text()),
                                                float(self.ui.txtBankIA3.text()),
                                                Speed(float(self.ui.pnlWindIA3.speedBox.text()), SpeedUnits.KTS),
                                                Altitude(float(self.ui.TxtMocIA3.text())))
                self.nominalPolylineAreaList.append(initialSegment3.nominalLine)
                self.obstaclesModel.surfacesList = [finalApproachSegment,
                                                    missedApproachSegment,
                                                    intermediateSegment,
                                                    initialSegment1,
                                                    initialSegment2,
                                                    initialSegment3]
                
            for seg in self.obstaclesModel.surfacesList:
                seg.vmethod_1("NON-Precision", gnssMapLayers)
                #seg.drawPrimary("BasicGNSS", gnssMapLayers)
                #seg.drawSecondary("BasicGNSS", gnssMapLayers)
            
            gnssMapLayers.insert(0, self.nominalTrack2Layer())
            gnssMapLayers.insert(1, self.WPT2Layer())
            QgisHelper.appendToCanvas(define._canvas, gnssMapLayers, "NON-Precision with T- or Y-Bar")
            QgisHelper.zoomToLayers(gnssMapLayers)
            self.ui.btnEvaluate.setEnabled(True)
            self.ui.chbInsertSymbols.setChecked(False)
            
            self.layers = gnssMapLayers
            self.resultLayerList = gnssMapLayers
            self.nominalPolylineAreaList = []
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
#         except BaseException as e:
#             QMessageBox.warning(self, "Error", e.message)
    def evalute(self):
#         try:
        ObstacleTable.MocMultiplier = self.ui.mocSpinBox.value()
        gnssMapLayers = QgisHelper.getSurfaceLayers(SurfaceTypes.BasicGNSS)
        self.obstaclesModel.loadObstacles(gnssMapLayers)

        for surfaceName in RnavSegmentType.Items:
            valueMeterText = self.obstaclesModel.method_13(surfaceName, 0)
            valueFeetText = self.obstaclesModel.method_13(surfaceName, 1)
            self.criticalObstaclesBySurfaces.__setitem__(surfaceName, [valueMeterText, valueFeetText])

        self.setResultPanel()
        self.ui.btnMarkSoc.setEnabled(True)
        self.ui.btnExportResult.setEnabled(True)
#         self.obstaclesModel.setVerticalHeader()
        self.obstaclesModel.setHiddenColumns(self.ui.tblObstacles)
        self.ui.tabBaroV.setCurrentIndex(1)
        
        ocaMaxObs = self.obstaclesModel.ocaMaxObstacle
        
        self.ui.txtCriticalID.setText(str(ocaMaxObs.name))
        self.ui.txtCriticalX.setText(str(ocaMaxObs.Position.get_X()))
        self.ui.txtCriticalY.setText(str(ocaMaxObs.Position.get_Y()))
        try:
            self.ui.txtCriticalAltitudeM.setText(str(ocaMaxObs.Position.get_Z()))
        except:
            self.ui.txtCriticalAltitudeM.setText(str(0.0))
        try:
            self.ui.txtCriticalAltitudeFt.setText(str(Altitude(ocaMaxObs.Position.get_Z()).Feet))
        except:
            self.ui.txtCriticalAltitudeFt.setText(str(0.0))
        self.ui.txtCriticalSurface.setText(ocaMaxObs.area)




    def setResultPanel(self):
        self.ui.txtOCA.setText(RnavSegmentType.FinalApproach)
        self.ui.txtOCH.setText(RnavSegmentType.MissedApproach)
        self.ui.txtOCH_2.setText(RnavSegmentType.Intermediate)
        self.ui.txtOCA_2.setText(RnavSegmentType.Initial1)
        self.ui.txtOCH_3.setText(RnavSegmentType.Initial2)
        self.ui.txtOCH_4.setText(RnavSegmentType.Initial3)

        self.ui.txtOCAResults.setText(self.criticalObstaclesBySurfaces.__getitem__(RnavSegmentType.FinalApproach)[self.ui.cmbUnits.currentIndex()])
        self.ui.txtOCHResults.setText(self.criticalObstaclesBySurfaces.__getitem__(RnavSegmentType.MissedApproach)[self.ui.cmbUnits.currentIndex()])
        self.ui.txtOCHResults_2.setText(self.criticalObstaclesBySurfaces.__getitem__(RnavSegmentType.Intermediate)[self.ui.cmbUnits.currentIndex()])
        self.ui.txtOCAResults_2.setText(self.criticalObstaclesBySurfaces.__getitem__(RnavSegmentType.Initial1)[self.ui.cmbUnits.currentIndex()])
        self.ui.txtOCHResults_3.setText(self.criticalObstaclesBySurfaces.__getitem__(RnavSegmentType.Initial2)[self.ui.cmbUnits.currentIndex()])
        self.ui.txtOCHResults_4.setText(self.criticalObstaclesBySurfaces.__getitem__(RnavSegmentType.Initial3)[self.ui.cmbUnits.currentIndex()])

        # valueText = self.obstaclesModel.method_13(RnavSegmentType.FinalApproach, self.ui.cmbUnits.currentIndex())
        # self.ui.txtOCAResults.setText(valueText)
        #
        #
        # valueText = self.obstaclesModel.method_13(RnavSegmentType.MissedApproach, self.ui.cmbUnits.currentIndex())
        # self.ui.txtOCHResults.setText(valueText)
        #
        #
        # valueText = self.obstaclesModel.method_13(RnavSegmentType.Intermediate, self.ui.cmbUnits.currentIndex())
        # self.ui.txtOCHResults_2.setText(valueText)
        #
        #
        # valueText = self.obstaclesModel.method_13(RnavSegmentType.Initial1, self.ui.cmbUnits.currentIndex())
        # self.ui.txtOCAResults_2.setText(valueText)
        #
        #
        # valueText = self.obstaclesModel.method_13(RnavSegmentType.Initial2, self.ui.cmbUnits.currentIndex())
        # self.ui.txtOCHResults_3.setText(valueText)
        #
        #
        # valueText = self.obstaclesModel.method_13(RnavSegmentType.Initial3, self.ui.cmbUnits.currentIndex())
        # self.ui.txtOCHResults_4.setText(valueText)
        if self.ui.cmbSurface.currentIndex() == 0 and self.ui.cmbSurface.currentText() == "All":
            self.obstaclesModel.setFilterFixedString("")
        else:
            self.obstaclesModel.setFilterFixedString(str(self.ui.cmbSurface.currentText()))

    def buttunsDisable(self):
        pass
    def CalcRwyBearing(self):
        try:
            pointTHR = self.gbRunwayTHR.Point3d
            pointEnd = self.gbRunwayEnd.Point3d
            self.trackRadialPanelSetEnabled()
            self.ui.txtRunwayBearing.Value = Unit.ConvertRadToDeg(MathHelper.getBearing(pointEnd, pointTHR))
        except:
            return
#         button = self.sender()
#         gbClass = button.parentWidget().parentWidget().parentWidget()
#         if gbClass != self.gbARP:
#             self.gbARP.btnCapture.setChecked(False)
#         if gbClass!= self.gbFAWP:
#             self.gbFAWP.btnCapture.setChecked(False)
#         if gbClass!= self.gbMAWP:
#             self.gbMAWP.btnCapture.setChecked(False)
#         if gbClass!= self.gbMAHWP:
#             self.gbMAHWP.btnCapture.setChecked(False)
#         if gbClass!= self.gbIWP:
#             self.gbIWP.btnCapture.setChecked(False)
#         if gbClass!= self.gbIAWP1:
#             self.gbIAWP1.btnCapture.setChecked(False)
#         if gbClass!= self.gbIAWP2:
#             self.gbIAWP2.btnCapture.setChecked(False)
#         if gbClass!= self.gbIAWP3:
#             self.gbIAWP3.btnCapture.setChecked(False)
#             
    def annotationShow(self, annotation, gbClass):
        annotation.setMapPosition(QgsPoint (float(gbClass.txtPointX.text()), float(gbClass.txtPointY.text())))
    def changeCategory(self):
        if self.ui.cmbCategory.currentIndex() == AircraftSpeedCategory.A:
            self.ui.txtIasMA.setText(str(Speed(100).Knots))
            self.ui.txtIasIA1.setText(str(Speed(150).Knots))
            self.ui.txtIasIA3.setText(str(Speed(150).Knots))
            self.ui.txtMocMA2.setText(str(Altitude(50).Metres))
            self.ui.txtMACG.setText(str(AngleGradientSlope(2.5, AngleGradientSlopeUnits.Percent).Percent))
            return
        elif self.ui.cmbCategory.currentIndex() == AircraftSpeedCategory.B:
            self.ui.txtIasMA.setText(str(Speed(130).Knots))
            self.ui.txtIasIA1.setText(str(Speed(180).Knots))
            self.ui.txtIasIA3.setText(str(Speed(180).Knots))
            self.ui.txtMocMA2.setText(str(Altitude(50).Metres))
            self.ui.txtMACG.setText(str(AngleGradientSlope(2.5, AngleGradientSlopeUnits.Percent).Percent))
            return
        elif self.ui.cmbCategory.currentIndex() == AircraftSpeedCategory.C:
            self.ui.txtIasMA.setText(str(Speed(160).Knots))
            self.ui.txtIasIA1.setText(str(Speed(240).Knots))
            self.ui.txtIasIA3.setText(str(Speed(240).Knots))
            self.ui.txtMocMA2.setText(str(Altitude(50).Metres))
            self.ui.txtMACG.setText(str(AngleGradientSlope(2.5, AngleGradientSlopeUnits.Percent).Percent))
            return
        elif self.ui.cmbCategory.currentIndex() == AircraftSpeedCategory.D:
            self.ui.txtIasMA.setText(str(Speed(185).Knots))
            self.ui.txtIasIA1.setText(str(Speed(250).Knots))
            self.ui.txtIasIA3.setText(str(Speed(250).Knots))
            self.ui.txtMocMA2.setText(str(Altitude(50).Metres))
            self.ui.txtMACG.setText(str(AngleGradientSlope(2.5, AngleGradientSlopeUnits.Percent).Percent))
            return
        elif self.ui.cmbCategory.currentIndex() == AircraftSpeedCategory.E:
            self.ui.txtIasMA.setText(str(Speed(230).Knots))
            self.ui.txtIasIA1.setText(str(Speed(250).Knots))
            self.ui.txtIasIA3.setText(str(Speed(250).Knots))
            self.ui.txtMocMA2.setText(str(Altitude(50).Metres))
            self.ui.txtMACG.setText(str(AngleGradientSlope(2.5, AngleGradientSlopeUnits.Percent).Percent))
            return
        elif self.ui.cmbCategory.currentIndex() == AircraftSpeedCategory.H:
            self.ui.txtIasMA.setText(str(Speed(70).Knots))
            self.ui.txtIasIA1.setText(str(Speed(120).Knots))
            self.ui.txtIasIA3.setText(str(Speed(120).Knots))
            self.ui.txtMocMA2.setText(str(Altitude(40).Metres))
            self.ui.txtMACG.setText(str(AngleGradientSlope(4.2, AngleGradientSlopeUnits.Percent).Percent))
            return
    def changeWindIA1(self, valueTxt):
        try:
            altitude = Altitude(float(valueTxt), AltitudeUnits.FT)
            if altitude != None:
                self.ui.pnlWindIA1.setAltitude(altitude)            
        except:
            altitude = None
    def changeWindIA3(self, valueTxt):
        try:
            altitude = Altitude(float(valueTxt), AltitudeUnits.FT)
            if altitude != None:
                self.ui.pnlWindIA3.setAltitude(altitude)            
        except:
            altitude = None
    
    def annotationFlag(self):
        if self.ui.chbInsertSymbols.isChecked():
            self.annotationARP.show()
            self.annotationFAWP.show()
            self.annotationIAWP1.show()
            self.annotationIAWP2.show()
            self.annotationIAWP3.show()
            self.annotationIWP.show()
            self.annotationMAHWP.show()
            self.annotationMAWP.show()
            self.lineBand.show()
        else:
            self.annotationARP.hide()
            self.annotationFAWP.hide()
            self.annotationIAWP1.hide()
            self.annotationIAWP2.hide()
            self.annotationIAWP3.hide()
            self.annotationIWP.hide()
            self.annotationMAHWP.hide()
            self.annotationMAWP.hide()
            self.lineBand.hide()
    def drawLineBand(self, posTxt):
#         self.annotationFlag()
        self.ui.chbInsertSymbols.setChecked(True)
        try:
            self.pointList = []
            self.lineBand.reset(QGis.Line)
            #self.lineBand.setWidth(200)
            try:
                pointFA = self.gbFAWP.getPoint3D()
                if pointFA != None:
                    self.pointList.append(pointFA)
            except UserWarning:
                pass
            try:
                pointMA = self.gbMAWP.getPoint3D()
                if pointMA != None:
                    self.pointList.append(pointMA)
            except:
                pass
            try:
                pointMAH = self.gbMAHWP.getPoint3D()
                if pointMAH != None:
                    self.pointList.append(pointMAH)
            except:
                pass
            try:
                pointIW = self.gbIWP.getPoint3D()
                if pointIW != None:
                    self.pointList.append(pointIW)
            except:
                pass
            try:
                pointIW1 = self.gbIAWP1.getPoint3D()
            except:
                pass
            try:
                pointIW2 = self.gbIAWP2.getPoint3D()
                if pointIW2 != None:
                    self.pointList.append(pointIW2)
            except:
                pass
            try:
                pointIW3 = self.gbIAWP3.getPoint3D()
            except:
                pass
            if len(self.pointList) > 1:
                self.lineBand.addGeometry(QgsGeometry.fromPolyline(self.pointList),None)
            if pointIW != None and pointIW1 != None:
                self.lineBand.addGeometry(QgsGeometry.fromPolyline([pointIW, pointIW1]), None)
                self.points_1 = [pointIW, pointIW1]
            if pointIW != None and pointIW3 != None:
                self.lineBand.addGeometry(QgsGeometry.fromPolyline([pointIW, pointIW3]),None)
                self.points_3 = [pointIW, pointIW3]
    #         self.lineBand.addPoint(pointIW3)
        except UnboundLocalError:
            pass
              
        finally:
            try:
                self.lineBand.show()
            except:
                pass
    
    def nominalTrack2Layer(self):
        mapUnits = define._canvas.mapUnits()
        resultLayer = AcadHelper.createVectorLayer("NominalTrack_" + self.surfaceType.replace(" ", "_").replace("-", "_"), QGis.Line)
        for nominalPolylineArea in self.nominalPolylineAreaList:
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, nominalPolylineArea)
        return resultLayer
#         return resultLayer
    def WPT2Layer(self):
        resultLayer = AcadHelper.createVectorLayer("WPT_" + self.surfaceType.replace(" ", "_").replace("-", "_"), QGis.Point)
        i = 1
        while i < 8:
            if i == 1:
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.annotationMAHWP.mapPosition(), False, {"Category":"MAHF"})
            elif i == 2:
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.annotationMAWP.mapPosition(), False, {"Category":"MAPt"})
            elif i == 3:
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.annotationFAWP.mapPosition(), False, {"Category":"FAF"})
            elif i == 4:
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.annotationIWP.mapPosition(), False, {"Category":"IF"})
            elif i == 5:
                if not self.ui.radioBtn_Straight.isChecked():
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.annotationIAWP1.mapPosition(), False, {"Category":"IAFR"})
            elif i == 6:
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.annotationIAWP2.mapPosition(), False, {"Category":"IAFC"})
            elif i == 7:
                if not self.ui.radioBtn_Straight.isChecked():
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.annotationIAWP3.mapPosition(), False, {"Category":"IAFL"})

            i += 1
        
        '''FlyOver'''
        mawpBearing = MathHelper.getBearing(self.annotationMAHWP.mapPosition(), self.annotationMAWP.mapPosition())
        symbolFlyOver = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
        symbolFlyOver.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyover.svg", 9.0, 0.0)#Unit.ConvertRadToDeg(mawpBearing))
        symbolFlyOver.appendSymbolLayer(svgSymLayer)
        renderCatFlyOver = QgsRendererCategoryV2(1, symbolFlyOver,"FlyOver")
        
        '''FlyBy'''
        symbolFlyBy = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
        symbolFlyBy.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyby.svg", 9.0, 0.0)#Unit.ConvertRadToDeg(mawpBearing))
        symbolFlyBy.appendSymbolLayer(svgSymLayer)
        renderCatFlyBy = QgsRendererCategoryV2(0, symbolFlyBy,"FlyBy")

        symRenderer = QgsCategorizedSymbolRendererV2(Expressions.GNSS_WPT_EXPRESION, [renderCatFlyOver, renderCatFlyBy])

        resultLayer.setRendererV2(symRenderer)
        return resultLayer
        
    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return        
        self.filterList = ["", RnavSegmentType.MissedApproach, RnavSegmentType.FinalApproach, RnavSegmentType.Intermediate, RnavSegmentType.Initial1, RnavSegmentType.Initial2, RnavSegmentType.Initial3]
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.BasicGNSS, self.ui.tblObstacles, self.filterList, parameterList, resultHideColumnNames)
        self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbSurface.currentIndex()])
#         FlightPlanBaseDlg.exportResult()
    def getParameterList(self):
        parameterList = []
        
        parameterList.append(("Input Data", "group"))
        parameterList.append(("general", "group"))
        parameterList.append(("ISA", self.ui.txtIsa.text() + unicode("°C", "utf-8")))
        parameterList.append(("Aircraft Category", self.ui.cmbCategory.currentText()))
        parameterList.append(("Construction Type", self.ui.cmbConstruction.currentText()))
        parameterList.append(("MOCMultiplier", self.ui.mocSpinBox.text()))
                
        parameterList.append(("Aerodrom / Heliport Reference Point", "group"))
        # longLatPoint = QgisHelper.Meter2Degree(float(self.gbARP.txtPointX.text()), float(self.gbARP.txtPointY.text()))
        
        parameterList.append(("Lat", self.gbARP.txtLat.Value))
        parameterList.append(("Lon", self.gbARP.txtLong.Value))
        parameterList.append(("X", self.gbARP.txtPointX.text()))
        parameterList.append(("Y", self.gbARP.txtPointY.text()))
        
        if self.gbRunwayTHR.IsValid():
            parameterList.append(("Runway THR", "group"))
            # longLatPoint = QgisHelper.Meter2Degree(float(self.gbRunwayTHR.txtPointX.text()), float(self.gbRunwayTHR.txtPointY.text()))
            
            parameterList.append(("Lat", self.gbRunwayTHR.txtLat.Value))
            parameterList.append(("Lon", self.gbRunwayTHR.txtLong.Value))
            parameterList.append(("X", self.gbRunwayTHR.txtPointX.text()))
            parameterList.append(("Y", self.gbRunwayTHR.txtPointY.text()))
        if self.gbRunwayEnd.IsValid():    
            parameterList.append(("Runway End", "group"))
            # longLatPoint = QgisHelper.Meter2Degree(float(self.gbRunwayEnd.txtPointX.text()), float(self.gbRunwayEnd.txtPointY.text()))
            
            parameterList.append(("Lat", self.gbRunwayEnd.txtLat.Value))
            parameterList.append(("Lon", self.gbRunwayEnd.txtLong.Value))
            parameterList.append(("X", self.gbRunwayEnd.txtPointX.text()))
            parameterList.append(("Y", self.gbRunwayEnd.txtPointY.text()))

            parameterList.append(("Runway Back Azimuth", "Plan : " + str(self.ui.txtRunwayBearing.txtRadialPlan.Value) + define._degreeStr))
            parameterList.append(("", "Geodetic : " + str(self.ui.txtRunwayBearing.txtRadialGeodetic.Value) + define._degreeStr))

            # parameterList.append(("Runway Back Azimuth", self.ui.txtRunwayBearing.Value + unicode("°", "utf-8")))
        parameterList.append(("Insert Symbols", str(self.ui.chbInsertSymbols.isChecked())))
        
        parameterList.append(("Missed Approach", "group"))
        parameterList.append(("MAHF", "group"))
        # longLatPoint = QgisHelper.Meter2Degree(float(self.gbMAHWP.txtPointX.text()), float(self.gbMAHWP.txtPointY.text()))
        parameterList.append(("Lat", self.gbMAHWP.txtLat.Value))
        parameterList.append(("Lon", self.gbMAHWP.txtLong.Value))
        parameterList.append(("X", self.gbMAHWP.txtPointX.text()))
        parameterList.append(("Y", self.gbMAHWP.txtPointY.text()))
        
        parameterList.append(("MAPt", "group"))
        # longLatPoint = QgisHelper.Meter2Degree(float(self.gbMAWP.txtPointX.text()), float(self.gbMAWP.txtPointY.text()))
        parameterList.append(("Lat", self.gbMAWP.txtLat.Value))
        parameterList.append(("Lon", self.gbMAWP.txtLong.Value))
        parameterList.append(("X", self.gbMAWP.txtPointX.text()))
        parameterList.append(("Y", self.gbMAWP.txtPointY.text()))
        
        parameterList.append(("Parameters(Missed Approach)", "group"))
        parameterList.append(("Rnav Specification", self.selectedRnavSpecificationMA))
        parameterList.append(("IAS", self.ui.txtIasMA.text() + "kts"))
        parameterList.append(("Primary Moc[int.]", self.ui.txtMocMA1.text() + "m"))
        parameterList.append(("Primary Moc[fin.]", self.ui.txtMocMA2.text() + "m"))
        parameterList.append(("SOC Altitude", self.ui.txtSocAltitude.text() + "ft"))
        parameterList.append(("MA Climb Gradient", self.ui.txtMACG.text() + "%"))
        
        
        parameterList.append(("Final Approach", "group"))
#         parameterList.append(("MAPt", "group"))
#         longLatPoint = QgisHelper.Meter2Degree(float(self.gbMAWP.txtPointX.text()), float(self.gbMAWP.txtPointY.text()))
#         parameterList.append(("Lat", str(longLatPoint.get_Y())))
#         parameterList.append(("Lon", str(longLatPoint.get_X())))
#         parameterList.append(("X", self.gbMAWP.txtPointX.text()))
#         parameterList.append(("Y", self.gbMAWP.txtPointY.text()))
        
        parameterList.append(("FAF", "group"))
        # longLatPoint = QgisHelper.Meter2Degree(float(self.gbFAWP.txtPointX.text()), float(self.gbFAWP.txtPointY.text()))
        parameterList.append(("Lat", self.gbFAWP.txtLat.Value))
        parameterList.append(("Lon", self.gbFAWP.txtLong.Value))
        parameterList.append(("X", self.gbFAWP.txtPointX.text()))
        parameterList.append(("Y", self.gbFAWP.txtPointY.text()))
                
        parameterList.append(("Parameters(Final Approach)", "group"))
        parameterList.append(("Primary Moc", self.ui.TxtMocFA.text() + "m"))
        
        parameterList.append(("Intermediate Approach", "group"))
#         parameterList.append(("FAF", "group"))
#         longLatPoint = QgisHelper.Meter2Degree(float(self.gbFAWP.txtPointX.text()), float(self.gbFAWP.txtPointY.text()))
#         parameterList.append(("Lat", str(longLatPoint.get_Y())))
#         parameterList.append(("Lon", str(longLatPoint.get_X())))
#         parameterList.append(("X", self.gbFAWP.txtPointX.text()))
#         parameterList.append(("Y", self.gbFAWP.txtPointY.text()))
        
        parameterList.append(("IF", "group"))
        # longLatPoint = QgisHelper.Meter2Degree(float(self.gbIWP.txtPointX.text()), float(self.gbIWP.txtPointY.text()))
        parameterList.append(("Lat", self.gbIWP.txtLat.Value))
        parameterList.append(("Lon", self.gbIWP.txtLong.Value))
        parameterList.append(("X", self.gbIWP.txtPointX.text()))
        parameterList.append(("Y", self.gbIWP.txtPointY.text()))
                
        parameterList.append(("Parameters(Intermediate Approach)", "group"))
        parameterList.append(("RNAV Specification", self.selectedRnavSpecificationIA))
        parameterList.append(("Primary Moc", self.ui.TxtMocI.text() + "m"))
        
        parameterList.append(("Initial Approach", "group"))
#         parameterList.append(("IF", "group"))
#         longLatPoint = QgisHelper.Meter2Degree(float(self.gbIWP.txtPointX.text()), float(self.gbIWP.txtPointY.text()))
#         parameterList.append(("Lat", str(longLatPoint.get_Y())))
#         parameterList.append(("Lon", str(longLatPoint.get_X())))
#         parameterList.append(("X", self.gbIWP.txtPointX.text()))
#         parameterList.append(("Y", self.gbIWP.txtPointY.text()))
                
#         parameterList.append(("Parameters", "group"))
#         parameterList.append(("RNAV Specification", self.selectedRnavSpecificationIA))
#         parameterList.append(("Primary Moc", self.ui.TxtMocI.text() + "m"))
        
        parameterList.append(("Y-Bar", str(self.ui.radioBtn_Y_Bar.isChecked())))
        parameterList.append(("Straight", str(self.ui.radioBtn_Straight.isChecked())))
        parameterList.append(("T-Bar", str(self.ui.radioBtn_T_Bar.isChecked())))
        
        if not self.ui.radioBtn_Straight.isChecked():
            parameterList.append(("IAFR", "group"))
            # longLatPoint = QgisHelper.Meter2Degree(float(self.gbIAWP1.txtPointX.text()), float(self.gbIAWP1.txtPointY.text()))
            parameterList.append(("Lat", self.gbIAWP1.txtLat.Value))
            parameterList.append(("Lon", self.gbIAWP1.txtLong.Value))
            parameterList.append(("X", self.gbIAWP1.txtPointX.text()))
            parameterList.append(("Y", self.gbIAWP1.txtPointY.text()))
                    
            parameterList.append(("Parameters(IAFR)", "group"))
            parameterList.append(("RNAV Specification", self.ui.cmbRnavSpecification_3.currentText()))
            parameterList.append(("IAS", self.ui.txtIasIA1.text() + "kts"))
            parameterList.append(("Altitude", self.ui.txtAltitudeIA1.text() + "ft"))
            parameterList.append(("Bank Angle", self.ui.txtBankIA1.text()))
            parameterList.append(("Wind", self.ui.pnlWindIA1.speedBox.text() + "kts"))
            parameterList.append(("Primary Moc", self.ui.TxtMocIA1.text() + "m"))
        
        parameterList.append(("IAFC", "group"))
        # longLatPoint = QgisHelper.Meter2Degree(float(self.gbIAWP2.txtPointX.text()), float(self.gbIAWP2.txtPointY.text()))
        parameterList.append(("Lat", self.gbIAWP2.txtLat.Value))
        parameterList.append(("Lon", self.gbIAWP2.txtLong.Value))
        parameterList.append(("X", self.gbIAWP2.txtPointX.text()))
        parameterList.append(("Y", self.gbIAWP2.txtPointY.text()))
                
        parameterList.append(("Parameters(IAFC)", "group"))
        parameterList.append(("RNAV Specification", self.ui.cmbRnavSpecification_4.currentText()))
        parameterList.append(("Primary Moc", self.ui.TxtMocIA2.text() + "m"))
        
        if not self.ui.radioBtn_Straight.isChecked():
            parameterList.append(("IAFL", "group"))
            # longLatPoint = QgisHelper.Meter2Degree(float(self.gbIAWP3.txtPointX.text()), float(self.gbIAWP3.txtPointY.text()))
            parameterList.append(("Lat", self.gbIAWP3.txtLat.Value))
            parameterList.append(("Lon", self.gbIAWP3.txtLong.Value))
            parameterList.append(("X", self.gbIAWP3.txtPointX.text()))
            parameterList.append(("Y", self.gbIAWP3.txtPointY.text()))
                    
            parameterList.append(("Parameters(IAFL)", "group"))
            parameterList.append(("RNAV Specification", self.ui.cmbRnavSpecification_5.currentText()))
            parameterList.append(("IAS", self.ui.txtIasIA3.text() + "kts"))
            parameterList.append(("Altitude", self.ui.txtAltitudeIA3.text() + "ft"))
            parameterList.append(("Bank Angle", self.ui.txtBankIA3.text()))
            parameterList.append(("Wind", self.ui.pnlWindIA3.speedBox.text() + "kts"))
            parameterList.append(("Primary Moc", self.ui.TxtMocIA3.text() + "m"))
        
        parameterList.append(("Results / Checked Obstacles", "group"))
        parameterList.append(("The Most Critical Obstacle", "group"))
        parameterList.append(("ID", self.ui.txtCriticalID.text()))
        parameterList.append(("X", self.ui.txtCriticalX.text()))
        parameterList.append(("Y", self.ui.txtCriticalY.text()))
        parameterList.append(("Altitude", self.ui.txtCriticalAltitudeM.text() + "m"))
        parameterList.append(("", self.ui.txtCriticalAltitudeFt.text() + "ft"))
        parameterList.append(("Surface", self.ui.txtCriticalSurface.text()))
                
        parameterList.append(("Results", "group"))
        parameterList.append(("Missed Approach", self.ui.txtOCHResults.text() ))
        parameterList.append(("Final Approach", self.ui.txtOCAResults.text() ))
        parameterList.append(("Intermediate", self.ui.txtOCHResults_2.text() ))
        parameterList.append(("Initial 1", self.ui.txtOCAResults_2.text() ))
        parameterList.append(("Initial 2", self.ui.txtOCHResults_3.text() ))
        parameterList.append(("Initial 3", self.ui.txtOCHResults_4.text() ))
        parameterList.append(("Checked Obstacles", "group"))
        
        for strFilter in self.filterList:
            self.obstaclesModel.setFilterFixedString(strFilter)
            c = self.obstaclesModel.rowCount()
            parameterList.append(("Number of Checked Obstacles(%s)"%strFilter, str(c)))  
        
        return parameterList             