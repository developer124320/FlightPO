'''
Created on 4 Jun 2014

@author: Administrator
'''
from PyQt4.QtGui import QSizePolicy, QSpinBox, QLabel, QFileDialog, QFrame, QLineEdit, QHBoxLayout, QFont, QStandardItem, QMessageBox
from PyQt4.QtCore import SIGNAL,Qt, QCoreApplication, QSize
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.TaaCalculation.ui_TaaCalc import Ui_form_TAA
from FlightPlanner.types import SurfaceTypes, DistanceUnits, ObstacleTableColumnType
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.helpers import Unit,Altitude
from FlightPlanner.types import AltitudeUnits,Point3D, RnavCommonWaypoint, IntersectionStatus, TurnDirection, DistanceUnits
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.helpers import Unit, MathHelper, Distance
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Captions import Captions
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.TaaCalculation.DlgCaculateWaypoint import CalcDlg
from FlightPlanner.messages import Messages
from FlightPlanner.AcadHelper import AcadHelper

from qgis.core import QgsCoordinateReferenceSystem,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2


import define, math

class TaaCalculationDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("TaaCalculationDlg")
        self.surfaceType = SurfaceTypes.TaaCalculation
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.TaaCalculation)
        QgisHelper.matchingDialogSize(self, 1250, 500)
        self.taaCalculationAreas = []
        self.resultUnit = "Feet"
        self.layers = []
    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return  
        self.filterList = []
        self.filterList.append("")
        for taaArea in self.taaCalculationAreas:
            self.filterList.append(taaArea.title)
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, "Terminal Arrival Altitudes (TAA)", self.ui.tblObstacles, self.filterList, parameterList, resultHideColumnNames)
        self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("FAWP", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlFAWP.txtPointX.text()), float(self.parametersPanel.pnlFAWP.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlFAWP.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlFAWP.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlFAWP.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlFAWP.txtPointY.text()))
        
        parameterList.append(("IWP", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlIAWP.txtPointX.text()), float(self.parametersPanel.pnlIAWP.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlIAWP.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlIAWP.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlIAWP.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlIAWP.txtPointY.text()))
        
        parameterList.append(("IAWP1", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlIAWP1.txtPointX.text()), float(self.parametersPanel.pnlIAWP1.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlIAWP1.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlIAWP1.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlIAWP1.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlIAWP1.txtPointY.text()))
        parameterList.append(("Step-down Radius", self.parametersPanel.txtRadiusIAWP1.text() + "nm"))
        
        parameterList.append(("IAWP2", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlIAWP2.txtPointX.text()), float(self.parametersPanel.pnlIAWP2.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlIAWP2.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlIAWP2.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlIAWP2.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlIAWP2.txtPointY.text()))
        parameterList.append(("Step-down Radius", self.parametersPanel.txtRadiusIAWP2.text() + "nm"))
        
        parameterList.append(("IAWP3", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlIAWP3.txtPointX.text()), float(self.parametersPanel.pnlIAWP3.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlIAWP3.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlIAWP3.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlIAWP3.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlIAWP3.txtPointY.text()))
        parameterList.append(("Step-down Radius", self.parametersPanel.txtRadiusIAWP3.text() + "nm"))
        
        
        parameterList.append(("Results / Checked Obstacles", "group"))   
        parameterList.append(("Results", "group")) 
        parameterList.append(("Units", self.ui.cmbUnits.currentText())) 
        unitStr = ""
        taaCount = len(self.taaCalculationAreas)
        if self.ui.cmbUnits.currentIndex() == 0:
            unitStr = "m"
        else:
            unitStr = "ft"
        parameterList.append((self.taaCalculationAreas[0].title, self.ui.txtOCHResults.text() + unitStr)) 
        parameterList.append((self.taaCalculationAreas[1].title, self.ui.txtOCAResults.text() + unitStr)) 
        parameterList.append((self.taaCalculationAreas[2].title, self.ui.txtIAWP3Results.text() + unitStr)) 
        if taaCount > 3:
            parameterList.append((self.taaCalculationAreas[3].title, self.ui.txtIAWP4Results.text() + unitStr)) 
        if taaCount > 4:
            parameterList.append((self.taaCalculationAreas[4].title, self.ui.txtIAWP5Results.text() + unitStr)) 
        if taaCount > 5:
            parameterList.append((self.taaCalculationAreas[5].title, self.ui.txtIAWP6Results.text() + unitStr)) 
        
        parameterList.append(("Checked Obstacles", "group")) 
        for strFilter in self.filterList:
            self.obstaclesModel.setFilterFixedString(strFilter)
            c = self.obstaclesModel.rowCount()
            parameterList.append(("Number of Checked Obstacles(%s)"%strFilter, str(c)))  
        return parameterList
    def changeResultUnit(self):
        if self.newDlgExisting:
            if (self.resultUnit == "Metres" and self.ui.cmbUnits.currentText() == "Feet") :
                if self.resultUnitValue[0][1] != None:
                    self.ui.txtOCAResults.setText(self.resultUnitValue[0][0] + "ft")
                if self.resultUnitValue[1][1] != None:
                    self.ui.txtOCHResults.setText(self.resultUnitValue[1][0] + "ft")
                if self.resultUnitValue[2][1] != None:
                    self.ui.txtIAWP3Results.setText(self.resultUnitValue[2][0] + "ft")
                surfaceCount = len(self.taaCalculationAreas)
                if surfaceCount > 3:
                    if self.resultUnitValue[3][1] != None:
                        self.ui.txtIAWP4Results.setText(self.resultUnitValue[3][0] + "ft")
                if surfaceCount > 4:
                    if self.resultUnitValue[4][1] != None:
                        self.ui.txtIAWP5Results.setText(self.resultUnitValue[4][0] + "ft")
                if surfaceCount > 5:
                    if self.resultUnitValue[5][1] != None:
                        self.ui.txtIAWP6Results.setText(self.resultUnitValue[5][0] + "ft")
                self.resultUnit = "Feet"
            elif (self.resultUnit == "Feet" and self.ui.cmbUnits.currentText() == "Metres"):
                if self.resultUnitValue[0][1] != None:
                    self.ui.txtOCAResults.setText(str(round(Unit.ConvertFeetToMeter(float(self.resultUnitValue[0][0])), 1)) + "m")
                if self.resultUnitValue[1][1] != None:
                    self.ui.txtOCHResults.setText(str(round(Unit.ConvertFeetToMeter(float(self.resultUnitValue[1][0])), 1)) + "m")
                if self.resultUnitValue[2][1] != None:
                    self.ui.txtIAWP3Results.setText(str(round(Unit.ConvertFeetToMeter(float(self.resultUnitValue[2][0])), 1)) + "m")
                surfaceCount = len(self.taaCalculationAreas)
                if surfaceCount > 3:
                    if self.resultUnitValue[3][1] != None:
                        self.ui.txtIAWP4Results.setText(str(round(Unit.ConvertFeetToMeter(float(self.resultUnitValue[3][0])), 1)) + "m")
                if surfaceCount > 4:
                    if self.resultUnitValue[4][1] != None:
                        self.ui.txtIAWP5Results.setText(str(round(Unit.ConvertFeetToMeter(float(self.resultUnitValue[4][0])), 1)) + "m")
                if surfaceCount > 5:
                    if self.resultUnitValue[5][1] != None:
                        self.ui.txtIAWP6Results.setText(str(round(Unit.ConvertFeetToMeter(float(self.resultUnitValue[5][0])), 1)) + "m")
                self.resultUnit = "Metres"
#         self.setResultPanel()
#         return FlightPlanBaseDlg.changeResultUnit(self)


    def setResultPanel(self):
        self.resultUnitValue = []
        self.resultUnit = self.ui.cmbUnits.currentText()
        self.newDlgExisting = True
        if len(self.taaCalculationAreas) <= 0:
            return FlightPlanBaseDlg.setResultPanel(self)
        self.ui.txtOCA.setText(self.taaCalculationAreas[1].title)
        ocaResults = self.obstaclesModel.method_12(self.taaCalculationAreas[1].title, self.ui.cmbUnits.currentIndex())
        if ocaResults[1] != None:
            self.ui.txtOCAResults.setText(ocaResults[0] + ocaResults[1])
        else:
            self.ui.txtOCAResults.setText(ocaResults[0])
        self.resultUnitValue.append(ocaResults)

        self.ui.txtOCH.setText(self.taaCalculationAreas[0].title)
        ochResults = self.obstaclesModel.method_12(self.taaCalculationAreas[0].title, self.ui.cmbUnits.currentIndex())
        if ochResults[1] != None:
            self.ui.txtOCHResults.setText(ochResults[0] + ochResults[1])
        else:
            self.ui.txtOCHResults.setText(ochResults[0])
        self.resultUnitValue.append(ochResults)
        

        self.ui.txtIAWP3.setText(self.taaCalculationAreas[2].title)
        iawp3Results = self.obstaclesModel.method_12(self.taaCalculationAreas[2].title, self.ui.cmbUnits.currentIndex())
        if iawp3Results[1] != None:
            self.ui.txtIAWP3Results.setText(iawp3Results[0] + iawp3Results[1])
        else:
            self.ui.txtIAWP3Results.setText(iawp3Results[0])
        self.resultUnitValue.append(iawp3Results)
        
        surfaceCount = len(self.taaCalculationAreas)
        if surfaceCount > 3:
            self.ui.txtIAWP4.setText(self.taaCalculationAreas[3].title)
            iawp4Results = self.obstaclesModel.method_12(self.taaCalculationAreas[3].title, self.ui.cmbUnits.currentIndex())
            if iawp4Results[1] != None:
                self.ui.txtIAWP4Results.setText(iawp4Results[0] + iawp4Results[1])
            else:
                self.ui.txtIAWP4Results.setText(iawp4Results[0])
            self.resultUnitValue.append(iawp4Results)
            self.ui.frame_IAWP4.setVisible(True)
        if surfaceCount > 4:
            self.ui.txtIAWP5.setText(self.taaCalculationAreas[4].title)
            iawp5Results = self.obstaclesModel.method_12(self.taaCalculationAreas[4].title, self.ui.cmbUnits.currentIndex())
            if iawp5Results[1] != None:
                self.ui.txtIAWP5Results.setText(iawp5Results[0] + iawp5Results[1])
            else:
                self.ui.txtIAWP5Results.setText(iawp5Results[0])
            self.resultUnitValue.append(iawp5Results)
            self.ui.frame_IAWP5.setVisible(True)
        if surfaceCount > 5:
            self.ui.txtIAWP6.setText(self.taaCalculationAreas[5].title)
            iawp6Results = self.obstaclesModel.method_12(self.taaCalculationAreas[5].title, self.ui.cmbUnits.currentIndex())
            if iawp6Results[1] != None:
                self.ui.txtIAWP6Results.setText(iawp6Results[0] + iawp6Results[1])
            else:
                self.ui.txtIAWP6Results.setText(iawp6Results[0])
            self.resultUnitValue.append(iawp6Results)
            self.ui.frame_IAWP6.setVisible(True)
        

        return FlightPlanBaseDlg.setResultPanel(self)


    def initSurfaceCombo(self):
#         if self.parametersPanel.cmbSegmentType.currentIndex() == 0:
#             self.ui.cmbObstSurface.addItems([PinsSurfaceType.PinsSurfaceType_OCS, PinsSurfaceType.PinsSurfaceType_OIS, PinsSurfaceType.PinsSurfaceType_LevelOCS, PinsSurfaceType.PinsSurfaceType_LevelOIS])
#         else:
#             self.ui.cmbObstSurface.addItems([PinsSurfaceType.PinsSurfaceType_OCS, PinsSurfaceType.PinsSurfaceType_OIS, PinsSurfaceType.PinsSurfaceType_LevelOCS])
        self.ui.cmbObstSurface.addItem("All")
        for taaCalculationArea in self.taaCalculationAreas:
        #             polylineList.extend(taaCalculationArea.method_0())
           if self.comboResultEmptyFlag:
               self.ui.cmbObstSurface.addItem(taaCalculationArea.title)   
        return FlightPlanBaseDlg.initSurfaceCombo(self)


    def initObstaclesModel(self):
        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        self.obstaclesModel = TaaCalculationObstacles(self.taaCalculationAreas)
        
        return FlightPlanBaseDlg.initObstaclesModel(self)


    def btnEvaluate_Click(self):
#         taaCalculationAreas = self.method_45();
#         primaryObstacleArea = self.method_46();
# #         self.method_29();
#         for taaCalculationArea in taaCalculationAreas:
#             self.obstacles.Add(TaaCalculationObstacles(taaCalculationArea));
#         taaCalculationEvaluator = TaaCalculationEvaluator(taaCalculationAreas);
#         for obstacle in self.obstacles:
#             obstacle.BeginLoadData();
#         obstacleSelector = ObstacleSelector(taaCalculationEvaluator);
#         if (not obstacleSelector.method_1(self, primaryObstacleArea)):
#             if (not obstacleSelector.Cancelled):
#                 base.method_18(Messages.NOTHING_SELECTED);
#             }
#             self.method_29();
#         }
#         else
#         {
#             self.method_30(true);
#             self.tabControl.SelectedIndex = 1;
#             int count = 0;
#             int obstaclesChecked = 0;
#             foreach (TaaCalculation.TaaCalculationObstacles taaCalculationObstacle in TaaCalculation.obstacles)
#             {
#                 count = count + taaCalculationObstacle.Rows.Count;
#                 obstaclesChecked = obstaclesChecked + taaCalculationObstacle.ObstaclesChecked;
#             }
#             base.method_19(obstaclesChecked, count);
#         }
#     }
        return FlightPlanBaseDlg.btnEvaluate_Click(self)


    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        if not self.method_27():
            return


        if len(self.layers) > 0:
            QgisHelper.removeFromCanvas(define._canvas, self.layers)
            self.layers = []
        polylineList = []

        self.taaCalculationAreas = self.method_45()
        self.comboResultEmptyFlag = False
        if self.ui.cmbObstSurface.count() == 0:
            self.comboResultEmptyFlag = True
        for taaCalculationArea in self.taaCalculationAreas:
            constructionLayer = AcadHelper.createVectorLayer(taaCalculationArea.title)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, taaCalculationArea.nominal.previewArea, True)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, taaCalculationArea.buffer.previewArea, True)
            self.layers.append(constructionLayer)

        QgisHelper.appendToCanvas(define._canvas, self.layers, SurfaceTypes.TaaCalculation)
        QgisHelper.zoomToLayers(self.layers)
        self.resultLayerList = self.layers
        self.ui.btnEvaluate.setEnabled(True)

    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)   
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        
        frame_IAWP3 = QFrame(self.ui.grbResult_2)
        frame_IAWP3.setFrameShape(QFrame.NoFrame)
        frame_IAWP3.setFrameShadow(QFrame.Raised)
        frame_IAWP3.setObjectName("frame_IAWP3")
        horizontalLayout_IAWP3 = QHBoxLayout(frame_IAWP3)
        horizontalLayout_IAWP3.setSpacing(0)
        horizontalLayout_IAWP3.setMargin(0)
        horizontalLayout_IAWP3.setObjectName("horizontalLayout_IAWP3")
        self.ui.txtIAWP3 = QLineEdit(frame_IAWP3)
        self.ui.txtIAWP3.setText("IAWP 3")
        font = QFont()
        font.setFamily("Arial")
        self.ui.txtIAWP3.setFont(font)
        self.ui.txtIAWP3.setObjectName("txtIAWP3")
        horizontalLayout_IAWP3.addWidget(self.ui.txtIAWP3)
        self.ui.txtIAWP3Results = QLineEdit(frame_IAWP3)
        self.ui.txtIAWP3Results.setFont(font)
        self.ui.txtIAWP3Results.setObjectName("txtIAWP3Results")
        horizontalLayout_IAWP3.addWidget(self.ui.txtIAWP3Results)
        
        self.ui.frame_IAWP4 = QFrame(self.ui.grbResult_2)
        self.ui.frame_IAWP4.setFrameShape(QFrame.NoFrame)
        self.ui.frame_IAWP4.setFrameShadow(QFrame.Raised)
        self.ui.frame_IAWP4.setObjectName("self.ui.frame_IAWP4")
        horizontalLayout_IAWP4 = QHBoxLayout(self.ui.frame_IAWP4)
        horizontalLayout_IAWP4.setSpacing(0)
        horizontalLayout_IAWP4.setMargin(0)
        horizontalLayout_IAWP4.setObjectName("horizontalLayout_IAWP4")
        self.ui.txtIAWP4 = QLineEdit(self.ui.frame_IAWP4)
#         self.ui.txtIAWP3.setText("IAWP ")
#         font = QFont()
#         font.setFamily("Arial")
        self.ui.txtIAWP4.setFont(font)
        self.ui.txtIAWP4.setObjectName("txtIAWP4")
        horizontalLayout_IAWP4.addWidget(self.ui.txtIAWP4)
        self.ui.txtIAWP4Results = QLineEdit(self.ui.frame_IAWP4)
        self.ui.txtIAWP4Results.setFont(font)
        self.ui.txtIAWP4Results.setObjectName("txtIAWP4Results")
        horizontalLayout_IAWP4.addWidget(self.ui.txtIAWP4Results)
        
        self.ui.frame_IAWP5 = QFrame(self.ui.grbResult_2)
        self.ui.frame_IAWP5.setFrameShape(QFrame.NoFrame)
        self.ui.frame_IAWP5.setFrameShadow(QFrame.Raised)
        self.ui.frame_IAWP5.setObjectName("self.ui.frame_IAWP5")
        horizontalLayout_IAWP5 = QHBoxLayout(self.ui.frame_IAWP5)
        horizontalLayout_IAWP5.setSpacing(0)
        horizontalLayout_IAWP5.setMargin(0)
        horizontalLayout_IAWP5.setObjectName("horizontalLayout_IAWP5")
        self.ui.txtIAWP5 = QLineEdit(self.ui.frame_IAWP5)
#         self.ui.txtIAWP3.setText("IAWP ")
#         font = QFont()
#         font.setFamily("Arial")
        self.ui.txtIAWP5.setFont(font)
        self.ui.txtIAWP5.setObjectName("txtIAWP5")
        horizontalLayout_IAWP5.addWidget(self.ui.txtIAWP5)
        self.ui.txtIAWP5Results = QLineEdit(self.ui.frame_IAWP5)
        self.ui.txtIAWP5Results.setFont(font)
        self.ui.txtIAWP5Results.setObjectName("txtIAWP5Results")
        horizontalLayout_IAWP5.addWidget(self.ui.txtIAWP5Results)
        
        self.ui.frame_IAWP6 = QFrame(self.ui.grbResult_2)
        self.ui.frame_IAWP6.setFrameShape(QFrame.NoFrame)
        self.ui.frame_IAWP6.setFrameShadow(QFrame.Raised)
        self.ui.frame_IAWP6.setObjectName("self.ui.frame_IAWP6")
        horizontalLayout_IAWP6 = QHBoxLayout(self.ui.frame_IAWP6)
        horizontalLayout_IAWP6.setSpacing(0)
        horizontalLayout_IAWP6.setMargin(0)
        horizontalLayout_IAWP6.setObjectName("horizontalLayout_IAWP6")
        self.ui.txtIAWP6 = QLineEdit(self.ui.frame_IAWP6)
#         self.ui.txtIAWP3.setText("IAWP ")
#         font = QFont()
#         font.setFamily("Arial")
        self.ui.txtIAWP6.setFont(font)
        self.ui.txtIAWP6.setObjectName("txtIAWP6")
        horizontalLayout_IAWP6.addWidget(self.ui.txtIAWP6)
        self.ui.txtIAWP6Results = QLineEdit(self.ui.frame_IAWP6)
        self.ui.txtIAWP6Results.setFont(font)
        self.ui.txtIAWP6Results.setObjectName("txtIAWP6Results")
        horizontalLayout_IAWP6.addWidget(self.ui.txtIAWP6Results)
        
        self.ui.verticalLayout_17.addWidget(frame_IAWP3)
        self.ui.verticalLayout_17.addWidget(self.ui.frame_IAWP4)
        self.ui.verticalLayout_17.addWidget(self.ui.frame_IAWP5)
        self.ui.verticalLayout_17.addWidget(self.ui.frame_IAWP6)
        self.ui.frame_IAWP4.hide()
        self.ui.frame_IAWP5.hide()
        self.ui.frame_IAWP6.hide()
        self.ui.txtOCA.setText("IAWP 2")
        self.ui.txtOCH.setText("IAWP 1")        
        self.ui.label_123.setText("Area:")
        
        return FlightPlanBaseDlg.uiStateInit(self)        
    def initParametersPan(self):
        ui = Ui_form_TAA()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.frame_TakeOffSurfaceTrack_2.setVisible(False)
        self.parametersPanel.frame_TakeOffSurfaceTrack_3.setVisible(False)
        self.parametersPanel.frame_TakeOffSurfaceTrack_4.setVisible(False)

        self.parametersPanel.pnlFAWP = PositionPanel(self.parametersPanel.form)
        self.parametersPanel.pnlFAWP.groupBox.setTitle("FAF")
        self.parametersPanel.pnlFAWP.btnCalculater.hide()
        self.parametersPanel.pnlFAWP.hideframe_Altitude()
        self.parametersPanel.pnlFAWP.setObjectName("pnlFAWP")
        ui.horizontalLayout_1.insertWidget(1, self.parametersPanel.pnlFAWP)
        self.connect(self.parametersPanel.pnlFAWP, SIGNAL("positionChanged"), self.initResultPanel)
        
        self.parametersPanel.pnlIAWP = PositionPanel(self.parametersPanel.form)
        self.parametersPanel.pnlIAWP.groupBox.setTitle("IF")
        self.parametersPanel.pnlIAWP.btnCalculater.hide()
        self.parametersPanel.pnlIAWP.hideframe_Altitude()
        self.parametersPanel.pnlIAWP.setObjectName("pnlIAWP")
        ui.horizontalLayout_2.insertWidget(1, self.parametersPanel.pnlIAWP)
        self.connect(self.parametersPanel.pnlIAWP, SIGNAL("positionChanged"), self.initResultPanel)

        self.parametersPanel.pnlIAWP1 = PositionPanel(self.parametersPanel.gbIAWP1)
#         self.parametersPanel.pnlIAWP1.groupBox.setTitle("IWP1")
#         self.parametersPanel.pnlIAWP1.btnCalculater.hide()
        self.parametersPanel.pnlIAWP1.hideframe_Altitude()
        self.parametersPanel.pnlIAWP1.setObjectName("pnlIAWP1")
        ui.vl_gbIAWP1.insertWidget(0, self.parametersPanel.pnlIAWP1)
        self.connect(self.parametersPanel.pnlIAWP1, SIGNAL("positionChanged"), self.initResultPanel)
        
        self.parametersPanel.pnlIAWP2 = PositionPanel(self.parametersPanel.gbIAWP2)
#         self.parametersPanel.pnlIAWP1.groupBox.setTitle("IWP1")
#         self.parametersPanel.pnlIAWP2.btnCalculater.hide()
        self.parametersPanel.pnlIAWP2.hideframe_Altitude()
        self.parametersPanel.pnlIAWP2.setObjectName("pnlIAWP2")
        ui.vl_gbIAWP2.insertWidget(0, self.parametersPanel.pnlIAWP2)
        self.connect(self.parametersPanel.pnlIAWP2, SIGNAL("positionChanged"), self.initResultPanel)
        
        self.parametersPanel.pnlIAWP3 = PositionPanel(self.parametersPanel.gbIAWP3)
#         self.parametersPanel.pnlIAWP1.groupBox.setTitle("IWP1")
#         self.parametersPanel.pnlIAWP3.btnCalculater.hide()
        self.parametersPanel.pnlIAWP3.hideframe_Altitude()
        self.parametersPanel.pnlIAWP3.setObjectName("pnlIAWP3")
        ui.vl_gbIAWP3.insertWidget(0, self.parametersPanel.pnlIAWP3)
        self.connect(self.parametersPanel.pnlIAWP3, SIGNAL("positionChanged"), self.initResultPanel)

        self.frame_8_1 = QFrame(self)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8_1.setSizePolicy(sizePolicy)
        self.frame_8_1.setFrameShape(QFrame.StyledPanel)
        self.frame_8_1.setFrameShadow(QFrame.Raised)
        self.frame_8_1.setObjectName("frame_8")
        self.horizontalLayout_10_1 = QHBoxLayout(self.frame_8_1)
        self.horizontalLayout_10_1.setAlignment(Qt.AlignHCenter)
        self.horizontalLayout_10_1.setSpacing(0)
        self.horizontalLayout_10_1.setMargin(0)
        self.horizontalLayout_10_1.setObjectName("horizontalLayout_10")
        self.label_2_1 = QLabel(self.frame_8_1)
        self.label_2_1.setMaximumSize(QSize(100, 16777215))
        self.label_2_1.setFixedWidth(100)
        self.label_2_1.setText("MOCmultiplier")
        
        font = QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.label_2_1.setFont(font)
        self.label_2_1.setObjectName("label_2_1")
        self.horizontalLayout_10_1.addWidget(self.label_2_1)
        
        self.parametersPanel.mocSpinBox = QSpinBox(self.frame_8_1)
        self.parametersPanel.mocSpinBox.setFont(font)
        self.parametersPanel.mocSpinBox.setObjectName("mocSpinBox")
        self.parametersPanel.mocSpinBox.setMinimum(1)
        self.parametersPanel.mocSpinBox.setFixedWidth(100)
        self.horizontalLayout_10_1.addWidget(self.parametersPanel.mocSpinBox)
#         self.verticalLayout_9.addWidget(self.frame_8_1)
        
        self.parametersPanel.verticalLayout.addWidget(self.frame_8_1)
        
        
        self.parametersPanel.btnMeasureI1.clicked.connect(self.measureI1)
        self.parametersPanel.btnMeasureI2.clicked.connect(self.measureI2)
        self.parametersPanel.btnMeasureI3.clicked.connect(self.measureI3)
        self.parametersPanel.txtRadiusIAWP1.textChanged.connect(self.initResultPanel)
        self.parametersPanel.txtRadiusIAWP2.textChanged.connect(self.initResultPanel)
        self.parametersPanel.txtRadiusIAWP3.textChanged.connect(self.initResultPanel)
        self.parametersPanel.pnlIAWP1.btnCalculater.clicked.connect(self.calcDlgShow1)
        self.parametersPanel.pnlIAWP2.btnCalculater.clicked.connect(self.calcDlgShow2)
        self.parametersPanel.pnlIAWP3.btnCalculater.clicked.connect(self.calcDlgShow3)
    def calcDlgShow1(self):
        pointIf = None
        pointFaf = None
        bearing = 0.0
        try:
            pointFaf = self.parametersPanel.pnlFAWP.Point3d
            pointIf = self.parametersPanel.pnlIAWP.Point3d
            bearing = MathHelper.getBearing(pointFaf,pointIf)
        except:
            return
        dlg = CalcDlg(self, pointIf, bearing, "R")
        dlg.txtForm.setText("IF")
        dlg.txtBearing.setText("90")
        dlg.txtDistance.setText("5")
        dlg.show()
    def calcDlgShow2(self):
        pointIf = None
        pointFaf = None
        bearing = 0.0
        try:
            pointFaf = self.parametersPanel.pnlFAWP.Point3d
            pointIf = self.parametersPanel.pnlIAWP.Point3d
            bearing = MathHelper.getBearing(pointFaf,pointIf)
        except:
            return
        dlg = CalcDlg(self, pointIf, bearing, "C")
        dlg.txtForm.setText("IF")
        dlg.txtBearing.setText("180")
        dlg.txtDistance.setText("5")
        dlg.show()
    def calcDlgShow3(self):
        pointIf = None
        pointFaf = None
        bearing = 0.0
        try:
            pointFaf = self.parametersPanel.pnlFAWP.Point3d
            pointIf = self.parametersPanel.pnlIAWP.Point3d
            bearing = MathHelper.getBearing(pointFaf,pointIf)
        except:
            return
        dlg = CalcDlg(self, pointIf, bearing, "L")
        dlg.txtForm.setText("IF")
        dlg.txtBearing.setText("270")
        dlg.txtDistance.setText("5")
        dlg.show()

    def measureI1(self):

        measureIAWP1 = MeasureTool(define._canvas, self.parametersPanel.txtRadiusIAWP1, DistanceUnits.NM)
        define._canvas.setMapTool(measureIAWP1)
    def measureI2(self):
        measureIAWP2 = MeasureTool(define._canvas, self.parametersPanel.txtRadiusIAWP2, DistanceUnits.NM)
        define._canvas.setMapTool(measureIAWP2)
    def measureI3(self):
        measureIAWP3 = MeasureTool(define._canvas, self.parametersPanel.txtRadiusIAWP3, DistanceUnits.NM)
        define._canvas.setMapTool(measureIAWP3)
    def initResultPanel(self):        
#         FlightPlanBaseDlg.initResultPanel()
        self.ui.txtIAWP3.setText("IAWP 3")
    def method_27(self):
        
        result1,str1 = self.method_35(self.parametersPanel.txtRadiusIAWP1);
        result2,str2 = self.method_35(self.parametersPanel.txtRadiusIAWP2);
        result3,str3 = self.method_35(self.parametersPanel.txtRadiusIAWP3);
        str = ""
        if not result1:
            str = str + "Value of IAWP1's step-down radius " + str1
        if not result2:
            if str == "":
                str = str + "Value of IAWP2's step-down radius " + str2
            else:
                str = str + "\nValue of IAWP2's step-down radius " + str2
        if not result3:
            if str == "":
                str = str + "Value of IAWP3's step-down radius " + str3
            else:
                str = str + "\nValue of IAWP3's step-down radius " + str3
        result4, str4 = self.method_33()
        if result4:
            messageStr = str
        else:
            messageStr = str4 + "\n" + str 
        if not result4 or not result1 or not result2 or not result3:
            QMessageBox.warning(self, "Warning", messageStr)
            return False
        return True
    def method_30(self, bool_0):
        if (self.obstacles == None):
            return;
        if (len(self.obstacles) == 0):
            return;
#         self.gbResults.SuspendLayout();
        try:
            self.ui.tblResults.Clear();
            for obstacle in self.obstacles:
                self.tblResults.Add(obstacle.Title, obstacle.method_12(self.resultUnits));
            self.tblResults.UpdateContent();
            if (bool_0):
                self.pnlArea.Items.Clear();
                for taaCalculationObstacle in self.obstacles:
                    self.pnlArea.Items.Add(taaCalculationObstacle.Title);
                self.pnlArea.SelectedIndex = 0;
                self.gridObstacles.DataSource = self.obstacles[0];
        finally:
            self.gbResults.ResumeLayout();
    def method_33(self):
        str = ""
        str1 = ""
        str2 = ""
        messageStr = ""
        waypointStatu, str = self.method_34("IAFR", self.parametersPanel.pnlIAWP1, -90.3, -69.7);
        if (waypointStatu == WaypointStatus.Invalid):
            messageStr = messageStr + str
#             QMessageBox.warning(self, "Warning", str + "(IAWP1)")
#             return False;
#         self.imgIAWP1.Visible = waypointStatu == TaaCalculation.WaypointStatus.Invalid;
#         self.toolTip.SetToolTip(self.imgIAWP1, str);
        waypointStatu1 ,str1 = self.method_34("IAFC", self.parametersPanel.pnlIAWP2, -5.3, -5.3);
        if (waypointStatu1 == WaypointStatus.Invalid):
            if messageStr != "":
                messageStr = messageStr + "\n" + str1
            else:
                messageStr = messageStr
#             QMessageBox.warning(self, "Warning", str + "(IAWP2)")
#             return False;
#         self.imgIAWP2.Visible = waypointStatu1 == TaaCalculation.WaypointStatus.Invalid;
#         self.toolTip.SetToolTip(self.imgIAWP2, str);
        waypointStatu2 ,str2 = self.method_34("IAFL", self.parametersPanel.pnlIAWP3, 69.7, 90.3);
#         self.imgIAWP3.Visible = waypointStatu2 == TaaCalculation.WaypointStatus.Invalid;
#         self.toolTip.SetToolTip(self.imgIAWP3, str);
        if (waypointStatu2 == WaypointStatus.Invalid):
            if messageStr != "":
                messageStr = messageStr + "\n" + str2
            else:
                messageStr = str2
             
        if (waypointStatu == WaypointStatus.Invalid) or (waypointStatu1 == WaypointStatus.Invalid) or (waypointStatu2 == WaypointStatus.Invalid):
#             QMessageBox.warning(self, "Warning", messageStr)
            return (False, messageStr);
        return (waypointStatu2 != WaypointStatus.Invalid, None);

    def method_34(self, rnavCommonWaypoint_0, positionPanel_0, double_0, double_1):
        if (not positionPanel_0.IsValid()):
            return WaypointStatus.Unassigned;
        if (not self.parametersPanel.pnlFAWP.IsValid()):
            return WaypointStatus.Unassigned;
        if (not self.parametersPanel.pnlIAWP.IsValid()):
            return WaypointStatus.Unassigned;
        if define._units == QGis.Meters:
            point3d = QgisHelper.CrsTransformPoint(self.parametersPanel.pnlFAWP.Point3d.get_X(), self.parametersPanel.pnlFAWP.Point3d.get_Y(), define._xyCrs, define._latLonCrs)
            degree = point3d.get_Y()
            degree1 = point3d.get_X()
    #         if (not self.pnlFAWP.method_3(out degree, out degree1))
    #         {
    #             throw new Exception(Geo.LastError);
    #         }
            point3d = QgisHelper.CrsTransformPoint(self.parametersPanel.pnlIAWP.Point3d.get_X(), self.parametersPanel.pnlIAWP.Point3d.get_Y(), define._xyCrs, define._latLonCrs)
            degree2= point3d.get_Y()
            degree3 = point3d.get_X()
    #         if (!self.pnlIWP.method_3(out degree2, out degree3))
    #         {
    #             throw new Exception(Geo.LastError);
    #         }
            point3d = QgisHelper.CrsTransformPoint(positionPanel_0.Point3d.get_X(), positionPanel_0.Point3d.get_Y(), define._xyCrs, define._latLonCrs)
            degree4 = point3d.get_Y()
            degree5 = point3d.get_X()
        else:
            degree = self.parametersPanel.pnlFAWP.Point3d.get_Y()
            degree1 = self.parametersPanel.pnlFAWP.Point3d.get_X()
            degree2= self.parametersPanel.pnlIAWP.Point3d.get_Y()
            degree3 = self.parametersPanel.pnlIAWP.Point3d.get_X()
            degree4 = positionPanel_0.Point3d.get_Y()
            degree5 = positionPanel_0.Point3d.get_X()
#         if (!positionPanel_0.method_3(out degree4, out degree5))
#         {
#             throw new Exception(Geo.LastError);
#         }
        distance, num, num2 = self.smethod_4(degree, degree1, degree2, degree3)
#         {
#             throw new Exception(Geo.LastError);
#         }
        distance, num1, num2 = self.smethod_4(degree2, degree3, degree4, degree5)
#         {
#             throw new Exception(Geo.LastError);
#         }
        
        double_0 = MathHelper.smethod_3(num + double_0);
        double_1 = MathHelper.smethod_3(num + double_1);
        s = "IF"
        if (double_0 < double_1):
            if (num1 < double_0 or num1 > double_1):
                bEARINGXOUTSIDEOFVALIDRANGE = Messages.BEARING_X_OUTSIDE_OF_VALID_RANGE%(s, rnavCommonWaypoint_0, double_0, double_1)
#                 object[] rnavCommonWaypointIWP = new object[] { Enums.RnavCommonWaypoint_IWP, EnumHelper.smethod_0(rnavCommonWaypoint_0), double_0.ToString("000.##"), double_1.ToString("000.##") };
#                 string_0 = string.Format(bEARINGXOUTSIDEOFVALIDRANGE, rnavCommonWaypointIWP);
                return (WaypointStatus.Invalid, bEARINGXOUTSIDEOFVALIDRANGE)
#             }
#         }
        elif (num1 > double_1 and num1 < double_0):
#         {
            str = Messages.BEARING_X_OUTSIDE_OF_VALID_RANGE%(s, rnavCommonWaypoint_0, double_0, double_1)
#             object[] objArray = new object[] { Enums.RnavCommonWaypoint_IWP, EnumHelper.smethod_0(rnavCommonWaypoint_0), double_0.ToString("000.##"), double_1.ToString("000.##") };
#             string_0 = string.Format(str, objArray);
            return (WaypointStatus.Invalid, str)
#         }
        return (WaypointStatus.Valid, "")
#     }
# 
    def method_35(self, distanceBoxPanel_0):
        if distanceBoxPanel_0.text() == "":
            return True, None 
        distance = Distance(float(distanceBoxPanel_0.text()), DistanceUnits.NM)
#         distanceNM = distance.NauticalMiles
        if (distance.NauticalMiles < 10 or distance.NauticalMiles > 15):
            str = "can not be smaller 10 or greater than 15."
            return False, str
        return True, None 
#         {
#             string vALUECANNOTBESMALLERTHANORGREATERTHAN = Validations.VALUE_CANNOT_BE_SMALLER_THAN_OR_GREATER_THAN;
#             string str = (new Distance(10, DistanceUnits.NM)).method_0(":nm");
#             Distance distance = new Distance(15, DistanceUnits.NM);
#             distanceBoxPanel_0.method_2(string.Format(vALUECANNOTBESMALLERTHANORGREATERTHAN, str, distance.method_0(":nm")));
#         }
#         }
    def method_45(self):
        point3d = self.parametersPanel.pnlFAWP.Point3d
        point3d1 = self.parametersPanel.pnlIAWP.Point3d
        num = MathHelper.getBearing(point3d1, point3d)
        origin = Point3D.get_Origin()
        num1 = num + 1.5707963267949
        isValid = self.parametersPanel.pnlIAWP1.IsValid()
        flag = isValid
        if (isValid):
            origin = self.parametersPanel.pnlIAWP1.Point3d
            num1 = MathHelper.getBearing(point3d1, origin)
        point3d2 = point3d1
        isValid1 = self.parametersPanel.pnlIAWP2.IsValid()
        flag1 = isValid1
        if (isValid1):
            point3d2 = self.parametersPanel.pnlIAWP2.Point3d
        origin1 = Point3D.get_Origin()
        num2 = num - 1.5707963267949
        isValid2 = self.parametersPanel.pnlIAWP3.IsValid()
        flag2 = isValid2
        if (isValid2):
            origin1 = self.parametersPanel.pnlIAWP3.Point3d
            num2 = MathHelper.getBearing(point3d1, origin1)
        taaCalculationAreas = []
        num3 = 300
        if (flag):
            try:
                value = Distance(float(self.parametersPanel.txtRadiusIAWP1.text()), DistanceUnits.NM)
            except:
                value = Distance(None)
            if (not value.IsValid()):
                taaCalculationAreas.append(TaaCalculationArea(TaaCalculationAreaType.SingleArea, RnavCommonWaypoint.IAWP1, point3d1, origin, num, num1, Distance(25, DistanceUnits.NM), TurnDirection.Right, num3))
            else:
                taaCalculationAreas.append(TaaCalculationArea(TaaCalculationAreaType.InnerArea, RnavCommonWaypoint.IAWP1, point3d1, origin, num, num1, value, TurnDirection.Right, num3))
                taaCalculationAreas.append(TaaCalculationArea(TaaCalculationAreaType.OuterArea, RnavCommonWaypoint.IAWP1, point3d1, origin, num, num1, value, TurnDirection.Right, num3, Distance(25, DistanceUnits.NM)))
        if (not flag1):
            taaCalculationAreas.append(TaaCalculationArea(TaaCalculationAreaType.SingleArea, RnavCommonWaypoint.IAWP2, point3d1, point3d2, num1, num2, Distance(25, DistanceUnits.NM), TurnDirection.Right, num3));
        else:
            try:
                distance = Distance(float(self.parametersPanel.txtRadiusIAWP2.text()), DistanceUnits.NM)
            except:
                distance = Distance(None)
            if (not distance.IsValid()):
                taaCalculationAreas.append(TaaCalculationArea(TaaCalculationAreaType.SingleArea, RnavCommonWaypoint.IAWP2, point3d1, point3d2, num1, num2, Distance(25, DistanceUnits.NM), TurnDirection.Right, num3))
            else:
                taaCalculationAreas.append(TaaCalculationArea(TaaCalculationAreaType.InnerArea, RnavCommonWaypoint.IAWP2, point3d1, point3d2, num1, num2, distance, TurnDirection.Right, num3))
                taaCalculationAreas.append(TaaCalculationArea(TaaCalculationAreaType.OuterArea, RnavCommonWaypoint.IAWP2, point3d1, point3d2, num1, num2, distance, TurnDirection.Right, num3, Distance(25, DistanceUnits.NM)))
        if (flag2):
            try:
                value1 = Distance(float(self.parametersPanel.txtRadiusIAWP3.text()), DistanceUnits.NM)
            except:
                value1 = Distance(None)
            if (not value1.IsValid()):
                taaCalculationAreas.append(TaaCalculationArea(TaaCalculationAreaType.SingleArea, RnavCommonWaypoint.IAWP3, point3d1, origin1, num, num2, Distance(25, DistanceUnits.NM), TurnDirection.Left, num3))
            else:
                taaCalculationAreas.append(TaaCalculationArea(TaaCalculationAreaType.InnerArea, RnavCommonWaypoint.IAWP3, point3d1, origin1, num, num2, value1, TurnDirection.Left, num3))
                taaCalculationAreas.append(TaaCalculationArea(TaaCalculationAreaType.OuterArea, RnavCommonWaypoint.IAWP3, point3d1, origin1, num, num2, value1, TurnDirection.Left, num3, Distance(25, DistanceUnits.NM)))
        return taaCalculationAreas
    def method_46(self):
#         Point3d point3d;
#         Point3d point3d1;
#         Point3d point3d2;
#         Point3d point3d3;
#         Point3d point3d4;
#         Point3d point3d5;
#         IntersectionStatus intersectionStatu;
#         Point3d point3d6;
#         Point3d point3d7;
#         Point3d point3d8;
#         Point3d point3d9;
#         Point3d point3d10;
#         Point3d point3d11;
#         Point3d point3d12;
#         Point3d point3d13;
#         Point3d point3d14;
#         Point3d point3d15;
#         Point3d point3d16;
        distance = Distance(30, DistanceUnits.NM)
        distance1 = Distance(5, DistanceUnits.NM)
        point3d17 = self.parametersPanel.pnlFAWP.Point3d;
        point3d18 = self.parametersPanel.pnlIWP.Point3d;
        num = MathHelper.getBearing(point3d18, point3d17);
        origin = Point3D.get_Origin();
        num1 = num + 1.5707963267949;
        isValid = self.parametersPanel.pnlIAWP1.IsValid;
        flag = isValid;
        if (isValid):
            origin = self.parametersPanel.pnlIAWP1.Point3d;
            num1 = MathHelper.getBearing(point3d18, origin);
        point3d19 = point3d18;
        isValid1 = self.parametersPanel.pnlIAWP2.IsValid;
        flag1 = isValid1;
        if (isValid1):
            point3d19 = self.parametersPanel.pnlIAWP2.Point3d;
        origin1 = Point3D.get_Origin();
        num2 = num - 1.5707963267949;
        isValid2 = self.parametersPanel.pnlIAWP3.IsValid;
        flag2 = isValid2;
        if (isValid2):
            origin1 = self.parametersPanel.pnlIAWP3.Point3d;
            num2 = MathHelper.getBearing(point3d18, origin1);
        polylineArea = PolylineArea();
        if (flag):
            num3 = num1 - 1.5707963267949;
            point3d20 = MathHelper.distanceBearingPoint(origin, num3, distance.Metres);
            point3d21 = MathHelper.distanceBearingPoint(point3d20, num3 - 1.5707963267949, 100);
            point3d = MathHelper.getIntersectionPoint(point3d20, point3d21, point3d18, point3d17);
            point3d22 = MathHelper.distanceBearingPoint(origin, num1, distance.Metres);
            if (not flag2):
                point3d23 = MathHelper.distanceBearingPoint(point3d18, num, distance1.Metres);
                if (MathHelper.calcDistance(origin, point3d18) >= distance.Metres):
                    polylineArea.Add(PolylineAreaPoint(point3d23));
                else:
                    polylineArea.Add(PolylineAreaPoint(MathHelper.distanceBearingPoint(point3d23, num - 1.5707963267949, distance1.Metres)));
                    polylineArea.Add(PolylineAreaPoint(MathHelper.distanceBearingPoint(point3d, num - 1.5707963267949, distance1.Metres)));
            polylineArea.Add(PolylineAreaPoint(point3d));
            polylineArea.Add(PolylineAreaPoint(point3d20, MathHelper.smethod_57(TurnDirection.Right, point3d20, point3d22, origin)));
            polylineArea.Add(PolylineAreaPoint(point3d22));
            polylineArea.Add(PolylineAreaPoint(MathHelper.distanceBearingPoint(point3d22, num1 + 1.5707963267949, distance1.Metres)));
        if (not flag1):
            if (not flag):
                point3d10 = MathHelper.distanceBearingPoint(point3d18, num1, distance.Metres);
                point3d11 = MathHelper.distanceBearingPoint(point3d10, num1 - 1.5707963267949, distance1.Metres);
            else:
                point3d24 = MathHelper.distanceBearingPoint(point3d18, num1 + 1.5707963267949, distance1.Metres);
                point3d25 = MathHelper.distanceBearingPoint(point3d24, num1, distance.Metres);
                point3d12_10List = []
                MathHelper.smethod_34(point3d24, point3d25, point3d18, distance.Metres, point3d12_10List);
                point3d12 = point3d12_10List[0]
                point3d10 = point3d12_10List[1]
                point3d11 = point3d10;
            if (not flag2):
                point3d13 = MathHelper.distanceBearingPoint(point3d18, num2, distance.Metres);
                point3d14 = MathHelper.distanceBearingPoint(point3d13, num2 + 1.5707963267949, distance1.Metres);
            else:
                point3d26 = MathHelper.distanceBearingPoint(point3d18, num2 - 1.5707963267949, distance1.Metres);
                point3d27 = MathHelper.distanceBearingPoint(point3d26, num2, distance.Metres);
                point3d15_13List = []
                MathHelper.smethod_34(point3d26, point3d27, point3d18, distance.Metres, point3d15_13List);
                point3d15 = point3d15_13List[0]
                point3d13 = point3d15_13List[1]
                point3d14 = point3d13;
            if (not flag):
                polylineArea.Add(PolylineAreaPoint(point3d11));
            polylineArea.Add(PolylineAreaPoint(point3d10, MathHelper.smethod_57(TurnDirection.Right, point3d10, point3d13, point3d18)));
            polylineArea.Add(PolylineAreaPoint(point3d13));
            if (not flag2):
                polylineArea.Add(PolylineAreaPoint(point3d14));
        else:
            if (not flag):
                point3d2 = point3d18;
                point3d3 = MathHelper.distanceBearingPoint(point3d18, num1, distance.Metres);
                point3d1_6List = []
                intersectionStatu = MathHelper.smethod_34(point3d2, point3d3, point3d19, distance.Metres, point3d1_6List);
                point3d1 = point3d1_6List[0]
                point3d6 = point3d1_6List[1]
                point3d7 = MathHelper.distanceBearingPoint(point3d6, num1 - 1.5707963267949, distance1.Metres);
            else:
                point3d2 = MathHelper.distanceBearingPoint(point3d18, num1 + 1.5707963267949, distance1.Metres);
                point3d3 = MathHelper.distanceBearingPoint(point3d2, num1, distance.Metres);
                point3d1_6List = []
                intersectionStatu = MathHelper.smethod_34(point3d2, point3d3, point3d19, distance.Metres, point3d1_6List);
                point3d1 = point3d1_6List[0]
                point3d6 = point3d1_6List[1]
                point3d7 = point3d6;
            intersectionStatu1 = IntersectionStatus.Nothing;
            if (not flag2):
                point3d4 = point3d18;
                point3d5 = MathHelper.distanceBearingPoint(point3d18, num2, distance.Metres);
                point3d1_8List = []
                intersectionStatu1 = MathHelper.smethod_34(point3d4, point3d5, point3d19, distance.Metres, point3d1_8List);
                point3d1 = point3d1_8List[0]
                point3d8 = point3d1_8List[1]
                point3d9 = MathHelper.distanceBearingPoint(point3d8, num2 + 1.5707963267949, distance1.Metres);
            else:
                point3d4 = MathHelper.distanceBearingPoint(point3d18, num2 - 1.5707963267949, distance1.Metres);
                point3d5 = MathHelper.distanceBearingPoint(point3d4, num2, distance.Metres);
                point3d1_8List = []
                intersectionStatu1 = MathHelper.smethod_34(point3d4, point3d5, point3d19, distance.Metres, point3d1_8List);
                point3d1 = point3d1_8List[0]
                point3d8 = point3d1_8List[1]
                point3d9 = point3d8;
            if (intersectionStatu != IntersectionStatus.Intersection or intersectionStatu1 != IntersectionStatus.Intersection):
                num4 = MathHelper.getBearing(point3d18, point3d19);
                point3d28 = MathHelper.distanceBearingPoint(point3d19, num4 - 1.5707963267949, distance.Metres);
                point3d29 = MathHelper.distanceBearingPoint(point3d28, num4 + 3.14159265358979, 100);
                point3d30 = MathHelper.distanceBearingPoint(point3d19, num4 + 1.5707963267949, distance.Metres);
                point3d31 = MathHelper.distanceBearingPoint(point3d30, num4 + 3.14159265358979, 100);
                point3d6 = MathHelper.getIntersectionPoint(point3d2, point3d3, point3d28, point3d29);
                point3d8 = MathHelper.getIntersectionPoint(point3d4, point3d5, point3d30, point3d31);
                if (not flag):
                    polylineArea.Add(PolylineAreaPoint(MathHelper.distanceBearingPoint(point3d6, num1 - 1.5707963267949, distance1.Metres)));
                polylineArea.Add(PolylineAreaPoint(point3d6));
                polylineArea.Add(PolylineAreaPoint(point3d28, MathHelper.smethod_57(TurnDirection.Right, point3d28, point3d30, point3d19)));
                polylineArea.Add(PolylineAreaPoint(point3d30));
                polylineArea.Add(PolylineAreaPoint(point3d8));
                if (not flag2):
                    polylineArea.Add(PolylineAreaPoint(MathHelper.distanceBearingPoint(point3d8, num2 + 1.5707963267949, distance1.Metres)));
            else:
                if (not flag):
                    polylineArea.Add(PolylineAreaPoint(point3d7));
                polylineArea.Add(PolylineAreaPoint(point3d6, MathHelper.smethod_57(TurnDirection.Right, point3d6, point3d8, point3d19)));
                polylineArea.Add(PolylineAreaPoint(point3d8));
                if (not flag2):
                    polylineArea.Add(PolylineAreaPoint(point3d9));
        if (flag2):
            num5 = num2 + 1.5707963267949;
            point3d32 = MathHelper.distanceBearingPoint(origin1, num2, distance.Metres);
            point3d33 = MathHelper.distanceBearingPoint(origin1, num5, distance.Metres);
            point3d34 = MathHelper.distanceBearingPoint(point3d33, num5 + 1.5707963267949, 100);
            point3d16 = MathHelper.getIntersectionPoint(point3d33, point3d34, point3d18, point3d17);
            polylineArea.Add(PolylineAreaPoint(MathHelper.distanceBearingPoint(point3d32, num2 - 1.5707963267949, distance1.Metres)));
            polylineArea.Add(PolylineAreaPoint(point3d32, MathHelper.smethod_57(TurnDirection.Right, point3d32, point3d33, origin1)));
            polylineArea.Add(PolylineAreaPoint(point3d33));
            polylineArea.Add(PolylineAreaPoint(point3d16));
            if (not flag):
                point3d35 = MathHelper.distanceBearingPoint(point3d18, num, distance1.Metres);
                if (MathHelper.calcDistance(origin1, point3d18) >= distance.Metres):
                    polylineArea.Add(PolylineAreaPoint(point3d35));
                else:
                    polylineArea.Add(PolylineAreaPoint(MathHelper.distanceBearingPoint(point3d16, num + 1.5707963267949, distance1.Metres)));
                    polylineArea.Add(PolylineAreaPoint(MathHelper.distanceBearingPoint(point3d35, num + 1.5707963267949, distance1.Metres)));
        return PrimaryObstacleArea(polylineArea);
    
    
    def smethod_4(self, degrees_0, degrees_1, degrees_2, degrees_3):
        num, double_0, double_1 = self.smethod_9(degrees_0, degrees_1, degrees_2, degrees_3);
        distance_0 = Distance(num, DistanceUnits.KM);
        return distance_0, double_0, double_1 
    def smethod_9(self, degrees_0, degrees_1, degrees_2, degrees_3):
        num10 = Unit.ConvertDegToRad(degrees_0);
        num11 = Unit.ConvertDegToRad(degrees_1);
        num12 = Unit.ConvertDegToRad(degrees_2);
        num13 = Unit.ConvertDegToRad(degrees_3);
        semiMajorAxis = 6378293.645208759 
        eccentricity = 6356617.987679838 / 6378293.645208759
        num14 = math.sqrt(semiMajorAxis * semiMajorAxis - semiMajorAxis * semiMajorAxis * (eccentricity * eccentricity));
        num14 = 6400000 * 2 - semiMajorAxis
        num15 = (semiMajorAxis - num14) / semiMajorAxis;
        num16 = 1 - num15;
        num17 = num16 * math.sin(num10) / math.cos(num10);
        num18 = num16 * math.sin(num12) / math.cos(num12);
        num19 = 1 / math.sqrt(num17 * num17 + 1);
        num20 = num19 * num17;
        num21 = 1 / math.sqrt(num18 * num18 + 1);
        num22 = num19 * num21;
        num23 = num22 * num18;
        num24 = num23 * num17;
        num25 = num13 - num11;
        
        
        num = math.sin(num25);
        num1 = math.cos(num25);
        num17 = num21 * num;
        num18 = num23 - num20 * num21 * num1;
        num2 = math.sqrt(num17 * num17 + num18 * num18);
        num3 = num22 * num1 + num24;
        num4 = math.atan2(num2, num3);
        num26 = num22 * num / num2;
        num5 = -num26 * num26 + 1;
        num6 = num24 + num24;
        if (num5 > 0):
            num6 = -num6 / num5 + num3;
        num7 = num6 * num6 * 2 - 1;
        num8 = ((-3 * num5 + 4) * num15 + 4) * num5 * num15 / 16;
        num9 = num25;
        num25 = ((num7 * num3 * num8 + num6) * num2 * num8 + num4) * num26;
        num25 = (1 - num8) * num25 * num15 + num13 - num11;
        while (math.fabs(num9 - num25) > 5E-14):
            num = math.sin(num25);
            num1 = math.cos(num25);
            num17 = num21 * num;
            num18 = num23 - num20 * num21 * num1;
            num2 = math.sqrt(num17 * num17 + num18 * num18);
            num3 = num22 * num1 + num24;
            num4 = math.atan2(num2, num3);
            num26 = num22 * num / num2;
            num5 = -num26 * num26 + 1;
            num6 = num24 + num24;
            if (num5 > 0):
                num6 = -num6 / num5 + num3;
            num7 = num6 * num6 * 2 - 1;
            num8 = ((-3 * num5 + 4) * num15 + 4) * num5 * num15 / 16;
            num9 = num25;
            num25 = ((num7 * num3 * num8 + num6) * num2 * num8 + num4) * num26;
            num25 = (1 - num8) * num25 * num15 + num13 - num11;
        
        num24 = math.atan2(num17, num18);
        num23 = math.atan2(num19 * num, num23 * num1 - num20 * num21) + 3.14159265358979;
        num25 = math.sqrt((1 / num16 / num16 - 1) * num5 + 1) + 1;
        num25 = (num25 - 2) / num25;
        num8 = 1 - num25;
        num8 = (num25 * num25 / 4 + 1) / num8;
        num9 = (0.375 * num25 * num25 - 1) * num25;
        num25 = num7 * num3;
        num22 = 1 - num7 - num7;
        num22 = ((((num2 * num2 * 4 - 3) * num22 * num6 * num9 / 6 - num25) * num9 / 4 + num6) * num2 * num9 + num4) * num8 * semiMajorAxis * num16;
        double_0 = num22 / 1000;
        double_1 = Unit.smethod_1(MathHelper.smethod_4(num24));
        double_2 = Unit.smethod_1(MathHelper.smethod_4(num23));
        return (double_0, double_1, double_2)
class TaaCalculationAreaType:
    SingleArea = "SingleArea"
    InnerArea = "InnerArea"
    OuterArea = "OuterArea"
    
class WaypointStatus:
    Unassigned = "Unassigned"
    Invalid = "Invalid"
    Valid = "Valid"

class TaaCalculationArea:
    def __init__(self, taaCalculationAreaType_0, rnavCommonWaypoint_0, point3d_0, point3d_1, double_0, double_1, distance_0, turnDirection_0, double_2, distance_1 = None):
        self.hasInnerCircle = False
        if distance_1 == None:
            point3d = Point3D()
            point3d1 = Point3D()
            point3d2 = Point3D()
            point3d3 = Point3D()
            point3dList01 = []
            point3dList23 = []
            polylineArea = PolylineArea()
            num = Unit.ConvertNMToMeter(5)
            if (rnavCommonWaypoint_0 != RnavCommonWaypoint.IAWP2):
                polylineArea = PolylineArea()
                intersectionStatu = MathHelper.smethod_34(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_0, distance_0.Metres), point3d_1, distance_0.Metres, point3dList01)
                point3d = point3dList01[0]
                point3d1 = point3dList01[1]
                MathHelper.smethod_34(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_1, distance_0.Metres), point3d_1, distance_0.Metres, point3dList23)
                point3d2 = point3dList23[0]
                point3d3 = point3dList23[1]
                if (intersectionStatu != IntersectionStatus.Intersection):
                    polylineArea.Add(PolylineAreaPoint(point3d2, MathHelper.smethod_57(turnDirection_0, point3d2, point3d3, point3d_1)))
                    polylineArea.Add(PolylineAreaPoint(point3d3))
                else:
                    polylineArea.Add(PolylineAreaPoint(point3d_0))
                    polylineArea.Add(PolylineAreaPoint(point3d1, MathHelper.smethod_57(turnDirection_0, point3d1, point3d3, point3d_1)))
                    polylineArea.Add(PolylineAreaPoint(point3d3))
            elif (not MathHelper.smethod_102(point3d_1, point3d_0)):
                intersectionStatu1 = MathHelper.smethod_34(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_0, distance_0.Metres), point3d_1, distance_0.Metres, point3dList01)
                point3d = point3dList01[0]
                point3d1 = point3dList01[1]
                intersectionStatu2 = MathHelper.smethod_34(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_1, distance_0.Metres), point3d_1, distance_0.Metres, point3dList23)
                point3d2 = point3dList23[0]
                point3d3 = point3dList23[1]
                if (intersectionStatu1 == IntersectionStatus.Intersection and intersectionStatu2 == IntersectionStatus.Intersection):
                    polylineArea.Add(PolylineAreaPoint(point3d1, MathHelper.smethod_57(turnDirection_0, point3d1, point3d3, point3d_1)))
                    polylineArea.Add(PolylineAreaPoint(point3d3))
                    polylineArea.Add(PolylineAreaPoint(point3d_0))
                elif (intersectionStatu1 != IntersectionStatus.Intersection):
                    if intersectionStatu2 != IntersectionStatus.Intersection:
                        polylineArea = PolylineArea(None, point3d_1, distance_0.Metres) 
                    else:
                        polylineArea.Add(PolylineAreaPoint(point3d2, MathHelper.smethod_57(turnDirection_0, point3d2, point3d3, point3d_1)))
                        polylineArea.Add(PolylineAreaPoint(point3d3))
                else:
                    polylineArea.Add(PolylineAreaPoint(point3d1, MathHelper.smethod_57(turnDirection_0, point3d1, point3d, point3d_1)))
                    polylineArea.Add(PolylineAreaPoint(point3d))
            else:
                point3d = MathHelper.distanceBearingPoint(point3d_0, double_0, distance_0.Metres)
                point3d1 = MathHelper.distanceBearingPoint(point3d_0, double_1, distance_0.Metres)
                polylineArea.Add(PolylineAreaPoint(point3d, MathHelper.smethod_57(turnDirection_0, point3d, point3d1, point3d_0)))
                polylineArea.Add(PolylineAreaPoint(point3d1))
                polylineArea.Add(PolylineAreaPoint(point3d_0))
            self.nominal = PrimaryObstacleArea(polylineArea)
            self.buffer = PrimaryObstacleArea(polylineArea.method_18(num))
            self.waypoint = rnavCommonWaypoint_0
            self.radius = self.method_2(taaCalculationAreaType_0, distance_0)
            self.primaryMoc = double_2
            if self.waypoint == 4:                
                self.title = "IAWP1" + " " + self.radius
            elif self.waypoint == 5:                
                self.title = "IAWP2" + " " + self.radius
            elif self.waypoint == 6:                
                self.title = "IAWP3" + " " + self.radius
        else:
            point3d = Point3D()
            point3d1 = Point3D()
            point3d2 = Point3D()
            point3d3 = Point3D()
            point3d4 = Point3D()
            point3d5 = Point3D()
            point3d6 = Point3D()
            point3d7 = Point3D()
            point3dList01 = []
            point3dList23 = []
            point3dList45 = []
            point3dList67 = []
            intersectionStatu = IntersectionStatus()
            intersectionStatu1 = IntersectionStatus()
            intersectionStatu2 = IntersectionStatus()
            intersectionStatu3 = IntersectionStatus()
            polylineArea = PolylineArea()
            num = Unit.ConvertNMToMeter(5)
            turnDirection = MathHelper.smethod_67(turnDirection_0)
            if (rnavCommonWaypoint_0 != RnavCommonWaypoint.IAWP2):
                polylineArea = PolylineArea()
                intersectionStatu = MathHelper.smethod_34(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_0, distance_1.Metres), point3d_1, distance_1.Metres, point3dList01)
                point3d = point3dList01[0]
                point3d1 = point3dList01[1]                
                intersectionStatu1 = MathHelper.smethod_34(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_1, distance_1.Metres), point3d_1, distance_1.Metres, point3dList23)
                point3d2 = point3dList23[0]
                point3d3 = point3dList23[1]  
                if (intersectionStatu != IntersectionStatus.Intersection):
                    polylineArea.Add(PolylineAreaPoint(point3d2, MathHelper.smethod_57(turnDirection_0, point3d2, point3d3, point3d_1)))
                    polylineArea.Add(PolylineAreaPoint(point3d3))
                else:
                    polylineArea.Add(PolylineAreaPoint(point3d1, MathHelper.smethod_57(turnDirection_0, point3d1, point3d3, point3d_1)))
                    polylineArea.Add(PolylineAreaPoint(point3d3))
                intersectionStatu2 = MathHelper.smethod_34(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_1, distance_0.Metres), point3d_1, distance_0.Metres, point3dList45)
                point3d4 = point3dList45[0]
                point3d5 = point3dList45[1]   
                intersectionStatu3 = MathHelper.smethod_34(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_0, distance_0.Metres), point3d_1, distance_0.Metres, point3dList67)
                point3d6 = point3dList67[0]
                point3d7 = point3dList67[1]   
                if (intersectionStatu3 != IntersectionStatus.Intersection):
                    polylineArea.Add(PolylineAreaPoint(point3d5, MathHelper.smethod_57(turnDirection, point3d5, point3d4, point3d_1)))
                    polylineArea.Add(PolylineAreaPoint(point3d4))
                    if (intersectionStatu == IntersectionStatus.Intersection):
                        polylineArea.Add(PolylineAreaPoint(point3d_0))
                else:
                    polylineArea.Add(PolylineAreaPoint(point3d5, MathHelper.smethod_57(turnDirection, point3d5, point3d7, point3d_1)))
                    polylineArea.Add(PolylineAreaPoint(point3d7))
            elif (not MathHelper.smethod_102(point3d_1, point3d_0)):
                intersectionStatu = MathHelper.smethod_34(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_0, distance_1.Metres), point3d_1, distance_1.Metres, point3dList01)
                point3d = point3dList01[0]
                point3d1 = point3dList01[1]   
                intersectionStatu1 = MathHelper.smethod_34(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_1, distance_1.Metres), point3d_1, distance_1.Metres, point3dList23)
                point3d2 = point3dList23[0]
                point3d3 = point3dList23[1]  
                intersectionStatu2 = MathHelper.smethod_34(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_1, distance_0.Metres), point3d_1, distance_0.Metres, point3dList45)
                point3d4 = point3dList45[0]
                point3d5 = point3dList45[1] 
                intersectionStatu3 = MathHelper.smethod_34(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_0, distance_0.Metres), point3d_1, distance_0.Metres, point3dList67)
                point3d6 = point3dList67[0]
                point3d7 = point3dList67[1]
                if (intersectionStatu != IntersectionStatus.Intersection or intersectionStatu1 != IntersectionStatus.Intersection):
                    if (intersectionStatu != IntersectionStatus.Intersection):
                        if intersectionStatu1 != IntersectionStatus.Intersection:
                            polylineArea = PolylineArea(point3d_1, distance_1.Metres)
                        else:
                            polylineArea.Add(PolylineAreaPoint(point3d2, MathHelper.smethod_57(turnDirection_0, point3d2, point3d1, point3d_1)))
                            polylineArea.Add(PolylineAreaPoint(point3d1))
                    else:
                        polylineArea.Add(PolylineAreaPoint(point3d1, MathHelper.smethod_57(turnDirection_0, point3d1, point3d, point3d_1)))
                        polylineArea.Add(PolylineAreaPoint(point3d))
                    self.innerCircleCenter = point3d_1
                    self.innerCircleRadius = distance_0.Metres - num
                    self.hasInnerCircle = True
                else:
                    polylineArea.Add(PolylineAreaPoint(point3d1, MathHelper.smethod_57(turnDirection_0, point3d1, point3d3, point3d_1)))
                    polylineArea.Add( PolylineAreaPoint(point3d3))
                    if (intersectionStatu2 == IntersectionStatus.Intersection and intersectionStatu3 == IntersectionStatus.Intersection):
                        polylineArea.Add(PolylineAreaPoint(point3d5, MathHelper.smethod_57(turnDirection, point3d5, point3d7, point3d_1)))
                        polylineArea.Add(PolylineAreaPoint(point3d7))
                    elif (intersectionStatu2 == IntersectionStatus.Intersection):
                        polylineArea.Add(PolylineAreaPoint(point3d_0))
                        polylineArea.Add(PolylineAreaPoint(point3d4, MathHelper.smethod_57(turnDirection, point3d4, point3d5, point3d_1)))
                        polylineArea.Add(PolylineAreaPoint(point3d5))
                    elif (intersectionStatu3 != IntersectionStatus.Intersection):
                        polylineArea.Add(PolylineAreaPoint(point3d_0))
                        self.innerCircleCenter = point3d_1
                        self.innerCircleRadius = distance_0.Metres - num
                        self.hasInnerCircle = True
                    else:
                        polylineArea.Add(PolylineAreaPoint(point3d7, MathHelper.smethod_57(turnDirection, point3d7, point3d6, point3d_1)))
                        polylineArea.Add(PolylineAreaPoint(point3d6))
                        polylineArea.Add(PolylineAreaPoint(point3d_0))
            else:
                point3d = MathHelper.distanceBearingPoint(point3d_0, double_0, distance_1.Metres)
                point3d1 = MathHelper.distanceBearingPoint(point3d_0, double_1, distance_1.Metres)
                point3d2 = MathHelper.distanceBearingPoint(point3d_0, double_1, distance_0.Metres)
                point3d3 = MathHelper.distanceBearingPoint(point3d_0, double_0, distance_0.Metres)
                polylineArea.Add(PolylineAreaPoint(point3d, MathHelper.smethod_57(turnDirection_0, point3d, point3d1, point3d_0)))
                polylineArea.Add(PolylineAreaPoint(point3d1))
                polylineArea.Add(PolylineAreaPoint(point3d2, MathHelper.smethod_57(turnDirection, point3d2, point3d3, point3d_0)))
                polylineArea.Add(PolylineAreaPoint(point3d3))
            self.nominal = PrimaryObstacleArea(polylineArea)
            self.buffer = PrimaryObstacleArea(polylineArea.method_18(num))
            self.waypoint = rnavCommonWaypoint_0
            self.radius = " " + self.method_2(taaCalculationAreaType_0, distance_0)
            self.primaryMoc = double_2
            if self.waypoint == 4:                
                self.title = "IAWP1" + self.radius
            elif self.waypoint == 5:                
                self.title = "IAWP2" + self.radius
            elif self.waypoint == 6:                
                self.title = "IAWP3" + self.radius
    def method_0(self):
        linesList = []
        pointList = self.nominal.previewArea.method_14_closed()
        polyline = (pointList, [])
        linesList.append(polyline)
        pointList = self.buffer.previewArea.method_14_closed()
        polyline = (pointList, [])
        linesList.append(polyline)
        return linesList
#         polylineList.extend(self.nominal.previewArea.method_14_closed())
#         polylineList.extend(self.buffer.previewArea.method_14_closed())
    
    
    def method_1(self, obstacle_0):
        double_0 = self.primaryMoc * obstacle_0.MocMultiplier
        if (not self.buffer.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
            return (None, None, False)
        if (self.hasInnerCircle and MathHelper.calcDistance(self.innerCircleCenter, obstacle_0.Position) + obstacle_0.Tolerance < self.innerCircleRadius):
            return (None, None, False)
        position = obstacle_0.Position
        double_1 = position.get_Z() + obstacle_0.Trees + double_0
        return (double_0, double_1, True)
    def method_2(self, taaCalculationAreaType_0, distance_0):
        if (taaCalculationAreaType_0 == TaaCalculationAreaType.InnerArea):
            return str(distance_0.NauticalMiles) + "nm"
        if (taaCalculationAreaType_0 != TaaCalculationAreaType.OuterArea):
            return ""
#         str = str(distance_0.NauticalMiles)
        distance = Distance(25, DistanceUnits.NM)
        return str(distance.NauticalMiles) + "nm"
class TaaCalculationObstacles(ObstacleTable):
    def __init__(self, surfacesList):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)
        
        self.surfaceType = SurfaceTypes.TaaCalculation
        self.title = None
        self.radius = None
        self.waypoint = None
        self.obstaclesChecked = None
        self.surfacesList = surfacesList
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        self.IndexMocAppliedM = fixedColumnCount 
        self.IndexMocAppliedFt = fixedColumnCount + 1
        self.IndexMocMultiplier = fixedColumnCount + 2
        self.IndexOcaM = fixedColumnCount + 3
        self.IndexOcaFt = fixedColumnCount + 4
        self.IndexSurface = fixedColumnCount + 5
                 
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt, 
                ObstacleTableColumnType.Surface               
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)
    
    def addObstacleToModel(self, obstacle, checkResult):
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
        self.source.setItem(row, self.IndexSurface, item)
    def checkObstacle(self, obstacle_0):
        num = 0.0
        num1 = 0.0
        num2 = 0
        for surface in self.surfacesList:
            num, num1, result = surface.method_1(obstacle_0)
            checkResult = [num, num1]
            if (result):
                checkResult.append(surface.title)
                self.addObstacleToModel(obstacle_0, checkResult)
#                 TaaCalculation.TaaCalculationObstacles item = TaaCalculation.obstacles[num2];
#                 item.ObstaclesChecked = item.ObstaclesChecked + 1;
#             }
#             num2 += 1
    def method_12(self,title, altitudeUnits_0):
        self.setFilterFixedString(title)
        self.sort(self.IndexOcaM, Qt.DescendingOrder )
        
        if (self.rowCount() == 0):
            return (Captions.GROUND_PLANE, None);

        item = self.data(self.index(0, self.IndexOcaFt), Qt.DisplayRole).toDouble()[0] if altitudeUnits_0 != AltitudeUnits.M else self.data(self.index(0, self.IndexOcaM), Qt.DisplayRole).toDouble()[0]
        
        
        if (altitudeUnits_0 == AltitudeUnits.M):
            num = item % 50
            if (num > 0):
                item = item + (50 - num)
            altitude = Altitude(round(item))
            return (str(altitude.Metres), "m")
        elif (altitudeUnits_0 != AltitudeUnits.FT):
            return ""
        else:
            num1 = item % 100
            if (num1 > 0):
                item = item + (100 - num1)
            altitude = Altitude(round(item), AltitudeUnits.FT)
            return (str(altitude.Feet), "ft")
    