# -*- coding: utf-8 -*-
'''
Created on 4 Jun 2014

@author: Administrator
'''
from PyQt4.QtGui import QTextDocument, QSizePolicy, QSpinBox, QLabel, QFileDialog, QFrame, QLineEdit, QHBoxLayout, QFont, QStandardItem, QMessageBox
from PyQt4.QtGui import QColor, QAbstractItemView,QPen, QStandardItemModel, QStyleOption, QBrush, QGraphicsEllipseItem, QGraphicsScene, QPainterPath, QPainter, QStyleOptionGraphicsItem
from PyQt4.QtCore import QPointF, QSizeF, SIGNAL,Qt, QCoreApplication, QSize, QObject, QVariant
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.MSA.ui_MSA import Ui_MSADlg
from FlightPlanner.MSA.SplitSectorDlg import SplitSectorDlg
from FlightPlanner.types import SurfaceTypes, DistanceUnits, ObstacleTableColumnType
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.helpers import Unit,Altitude
from FlightPlanner.types import AngleUnits, AltitudeUnits,Point3D, RnavCommonWaypoint, IntersectionStatus, TurnDirection, DistanceUnits
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.helpers import Unit, MathHelper, Distance
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Captions import Captions
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.messages import Messages
from FlightPlanner.Panels.UnitResultPanel import UnitResultPanel
from FlightPlanner.captureCoordinateTool import CaptureCoordinateToolUpdate
from FlightPlanner.AcadHelper import AcadHelper

from qgis.core import QgsPalLayerSettings, QgsCoordinateReferenceSystem,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2
from qgis.gui import QgsTextAnnotationItem,QgsSvgAnnotationItem

import define, math

class MSADlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("MSADlg")
        self.surfaceType = SurfaceTypes.MSA
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.MSA)
        QgisHelper.matchingDialogSize(self, 670, 600)
        self.layers = []
        self.rowID = 0
        self.graphicsEllipseItemList = []
        self.draw(self.parametersPanel.picPreview, 0, 0)
        self.layers = []
        self.unitResultPanelList = []
        self.splitSectorDlg = SplitSectorDlg(self)
        self.ui.frmGeneralButtons.setMaximumSize(QSize(120, 16777215))
        self.symbolLayer = None
    def btnPDTCheck_Click(self):
        self.CaptureCoordTool = CaptureCoordinateToolUpdate(define._canvas) 
        define._canvas.setMapTool(self.CaptureCoordTool)
        self.connect(self.CaptureCoordTool, SIGNAL("resultPointValueList"), self.drawSymbol)
        return FlightPlanBaseDlg.btnPDTCheck_Click(self)

    def drawSymbol(self, resultValueList):
        if self.symbolLayer != None:
            QgisHelper.removeFromCanvas(define._canvas, [self.symbolLayer])
            self.symbolLayer = None
        point3d1 = Point3D(float(resultValueList[1]), float(resultValueList[2]))
        circlePoint3dCollection = MathHelper.constructCircle(point3d1, 2600, 50)
        linesList = []
        caption = [("Caption", "")]
        linesList.append((circlePoint3dCollection, caption))
        for i in range(self.standardItermModel.rowCount()):
            num3 = Unit.ConvertDegToRad(float(self.standardItermModel.item(i, 0).text()))
            num4 = Unit.ConvertDegToRad(float(self.standardItermModel.item(i, 1).text()))
            
            point3d2 = MathHelper.distanceBearingPoint(point3d1, num3, 325)
            item = Distance(None)
            if self.standardItermModel.item(i, 2) == None:
                item = Distance(None)
            elif self.standardItermModel.item(i, 2).text() == "":
                item = Distance(None)
            else:
                item = Distance(float(self.standardItermModel.item(i, 2).text()), DistanceUnits.NM)
            if item.IsValid():
                nauticalMiles = 104 * item.NauticalMiles;
                point3d4 = MathHelper.distanceBearingPoint(point3d1, num3, nauticalMiles);
                point3d5 = MathHelper.distanceBearingPoint(point3d1, num4, nauticalMiles);
                point3dArray = [point3d4, point3d5]
                polylineArea = PolylineArea()
                polylineArea.Add(PolylineAreaPoint(point3d4, MathHelper.smethod_57(TurnDirection.Right, point3d4, point3d5, point3d1)))
                polylineArea.Add(PolylineAreaPoint(point3d5))
                point3dArray = polylineArea.method_14()
                
                caption = [("Caption", "")]
                linesList.append((point3dArray, caption))
                
            point3dArray = [MathHelper.distanceBearingPoint(point3d1, num3, 2600), point3d2, MathHelper.distanceBearingPoint(point3d1, num3 + 10.0 / 180 * math.pi, 400), point3d1, MathHelper.distanceBearingPoint(point3d1, num3 - 10.0 / 180 * math.pi, 400), point3d2]
            
            caption = [("Caption", self.standardItermModel.item(i, 0).text() + unicode("°", "utf-8"))]
            linesList.append((point3dArray, caption))
        
        resultLayer = QgisHelper.createPolylineLayer("MSA Symbol (Procedure Design)", linesList, [QgsField("Caption", QVariant.String)])
        
        palSetting = QgsPalLayerSettings()
        palSetting.readFromLayer(resultLayer)
        palSetting.enabled = True
        palSetting.fieldName = "Caption"
        palSetting.isExpression = True
        palSetting.placement = QgsPalLayerSettings.Line
        palSetting.placementFlags = QgsPalLayerSettings.AboveLine
        palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '6', "")
        palSetting.writeToLayer(resultLayer)
        
        QgisHelper.appendToCanvas(define._canvas, [resultLayer], "MSA Symbol (Procedure Design)")
        self.symbolLayer = resultLayer
    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return  
        self.filterList = []
        self.filterList.append("")
        for msaCalculationArea in self.msaCalculationAreas:
            self.filterList.append(msaCalculationArea.name)
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.MSA, self.ui.tblObstacles, self.filterList, parameterList, resultHideColumnNames)
        self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
     
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        
        parameterList.append(("Homing Facility Position", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlFacility.txtPointX.text()), float(self.parametersPanel.pnlFacility.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlFacility.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlFacility.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlFacility.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlFacility.txtPointY.text()))        
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Moc", self.parametersPanel.txtMoc.text() + "m"))
        parameterList.append(("MOCmultipiler", str(self.parametersPanel.mocSpinBox.value())))
        
        parameterList.append(("Sectors", "group"))
        
        for i in range(self.standardItermModel.rowCount()):
            parameterList.append(("split " + str(i + 1), "group"))
            parameterList.append(("From", self.standardItermModel.item(i, 0).text() + unicode("°", "utf-8")))
            parameterList.append(("To", self.standardItermModel.item(i, 1).text() + unicode("°", "utf-8")))
            if self.standardItermModel.item(i, 2) == None:
                parameterList.append(("Step-down Radius", ""))
            else:
                parameterList.append(("Step-down Radius", self.standardItermModel.item(i, 2).text() + "nm"))
        
        parameterList.append(("Results / Checked Obstacles", "group"))   
        parameterList.append(("Results", "group")) 
        parameterList.append(("Units", self.ui.cmbUnits.currentText())) 
        for unitResultPanel in self.unitResultPanelList:            
            parameterList.append((unitResultPanel.txtSurface.text(), unitResultPanel.txtResult.text()))
        
        parameterList.append(("Checked Obstacles", "group"))
        for strFilter in self.filterList:
            self.obstaclesModel.setFilterFixedString(strFilter)
            c = self.obstaclesModel.rowCount()
            parameterList.append(("Number of Checked Obstacles(%s)"%strFilter, str(c)))  
        
        return parameterList
    
    def changeResultUnit(self):
        if self.newDlgExisting:
            for i in range(len(self.msaCalculationAreas)):
                self.unitResultPanelList[i].txtResult.setText(self.obstaclesModel.method_12(self.msaCalculationAreas[i].name, self.ui.cmbUnits.currentIndex()))
            
        return FlightPlanBaseDlg.changeResultUnit(self)

    def initObstaclesModel(self):
        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        self.obstaclesModel = MsaCalculationObstacles(self.msaCalculationAreas)
        return FlightPlanBaseDlg.initObstaclesModel(self)


    def initSurfaceCombo(self):
        self.ui.cmbObstSurface.addItem("All")
        for msaCalculationArea in self.msaCalculationAreas:
            self.ui.cmbObstSurface.addItem(msaCalculationArea.sectorTitle + msaCalculationArea.sectorRadius)   
        return FlightPlanBaseDlg.initSurfaceCombo(self)


    def btnEvaluate_Click(self):
        if not self.method_27():
            return
        
        self.msaCalculationAreas = self.method_42()
        
        FlightPlanBaseDlg.btnEvaluate_Click(self)
        
        for i in range(len(self.msaCalculationAreas)):
            self.unitResultPanelList[i].txtResult.setText(self.obstaclesModel.method_12(self.msaCalculationAreas[i].name, self.ui.cmbUnits.currentIndex()))
        self.newDlgExisting = True
        if self.ui.cmbObstSurface.currentIndex() == 0 and self.ui.cmbObstSurface.currentText() == "All":
            self.obstaclesModel.setFilterFixedString("")
        else:
            self.obstaclesModel.setFilterFixedString(self.ui.cmbObstSurface.currentText())
    def openData(self):
        self.standardItermModel.clear()
        itemFrom = QStandardItem("From(" + unicode("°", "utf-8") + ")")
        itemTo = QStandardItem("To(" + unicode("°", "utf-8") + ")")
        itemRadius = QStandardItem("Step-down Radius(nm)")
        self.standardItermModel.setHorizontalHeaderItem(0, itemFrom)
        self.standardItermModel.setHorizontalHeaderItem(1, itemTo)
        self.standardItermModel.setHorizontalHeaderItem(2, itemRadius)
        self.parametersPanel.tableViewSectors.setColumnWidth(0, 50)
        self.parametersPanel.tableViewSectors.setColumnWidth(1, 50)
        self.parametersPanel.tableViewSectors.setColumnWidth(2, 150)
        FlightPlanBaseDlg.openData(self)
        self.rowID = self.standardItermModel.rowCount()
        self.draw(self.parametersPanel.picPreview, 0, 0)

    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        if not self.method_27():
            return
        # if len(self.layers) > 0:
        #     QgisHelper.removeFromCanvas(define._canvas, self.layers)
        #     self.layers = []
        msaCalculationAreas = self.method_42()


        for msaCalculationArea in msaCalculationAreas:
            polylineList = []
            constructionLayer = AcadHelper.createVectorLayer(msaCalculationArea.sectorTitle + msaCalculationArea.sectorRadius)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, msaCalculationArea.nominalArea, True)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, msaCalculationArea.bufferArea, True)

            # for point3dCollection in msaCalculationArea.method_0():
            #     polyline = (point3dCollection, [])
            #     polylineList.append(polyline)
            # constructionLayer = QgisHelper.createPolylineLayer(msaCalculationArea.sectorTitle + msaCalculationArea.sectorRadius, polylineList)
            self.resultLayerList.append(constructionLayer)
        QgisHelper.appendToCanvas(define._canvas, self.resultLayerList, self.surfaceType, True)
        QgisHelper.zoomToLayers(self.resultLayerList)
        # self.resultLayerList = self.layers
        self.ui.btnEvaluate.setEnabled(True)  
        
        if len(self.unitResultPanelList) > 0:
            self.removeUnitResultPanel(self.unitResultPanelList, self.ui.verticalLayout_17)
        self.unitResultPanelList = self.creatUnitResultPanel(self.ui.grbResult_2, self.ui.verticalLayout_17, msaCalculationAreas)
        

    def removeUnitResultPanel(self, unitResultPanelList, layout):
        for unitResultPanel in unitResultPanelList:
            layout.removeWidget(unitResultPanel) 
    def creatUnitResultPanel(self, parent, layout, surfaceList):
        unitResultPanels = []
        for aera in surfaceList:
            unitResultPanel = UnitResultPanel(parent)
            unitResultPanel.txtSurface.setText(aera.name)
            unitResultPanels.append(unitResultPanel)
            layout.addWidget(unitResultPanel)
        return unitResultPanels
    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.btnPDTCheck.setText("Draw Symbol")
        self.ui.tabCtrlGeneral.removeTab(2)
        self.ui.frame_113.hide()
        self.ui.frame_114.hide()
        
        return FlightPlanBaseDlg.uiStateInit(self)        
    def initParametersPan(self):
        ui = Ui_MSADlg()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)
        
#         self.parametersPanel.btnSectorNew.setEnabled(False)
        self.ui.frame_112.setVisible(False)
        self.ui.frame_113.setVisible(False)
        
        
        self.parametersPanel.pnlFacility = PositionPanel(self.parametersPanel.uiMsa)
        self.parametersPanel.pnlFacility.groupBox.setTitle("Homing Facility Position")
        self.parametersPanel.pnlFacility.btnCalculater.hide()
        self.parametersPanel.pnlFacility.hideframe_Altitude()
        self.parametersPanel.pnlFacility.setObjectName("pnlFacility")
        ui.verticalLayout.insertWidget(0, self.parametersPanel.pnlFacility)
        
        self.connect(self.parametersPanel.pnlFacility, SIGNAL("positionChanged"), self.initResultPanel)
        self.parametersPanel.btnSectorSplit.clicked.connect(self.btnSectorSplit_clicked)
        self.parametersPanel.btnSectorNew.clicked.connect(self.btnSectorNew_clicked)
        self.parametersPanel.btnSectorModify.clicked.connect(self.btnSectorModify_clicked)
        self.parametersPanel.btnSectorDelete.clicked.connect(self.btnSectorDelete_clicked)
        self.parametersPanel.tableViewSectors.clicked.connect(self.tableViewSectors_clicked)
        self.parametersPanel.tableViewSectors.doubleClicked.connect(self.tableViewSectors_doubleClicked)
       
        
        self.standardItermModel = QStandardItemModel()
        itemFrom = QStandardItem("From(" + unicode("°", "utf-8") + ")")
        itemTo = QStandardItem("To(" + unicode("°", "utf-8") + ")")
        itemRadius = QStandardItem("Step-down Radius(nm)")
        self.standardItermModel.setHorizontalHeaderItem(0, itemFrom)
        self.standardItermModel.setHorizontalHeaderItem(1, itemTo)
        self.standardItermModel.setHorizontalHeaderItem(2, itemRadius)
        self.standardItermModel.insertRow(0)
        self.standardItermModel.setData(self.standardItermModel.index(0, 0), QVariant(0))
        self.standardItermModel.setData(self.standardItermModel.index(0, 1), QVariant(0))
        self.standardItermModel.setData(self.standardItermModel.index(0, 2), QVariant(""))
        self.parametersPanel.tableViewSectors.setSelectionBehavior(1)
        self.parametersPanel.tableViewSectors.setModel(self.standardItermModel)
        self.parametersPanel.tableViewSectors.setColumnWidth(0, 50)
        self.parametersPanel.tableViewSectors.setColumnWidth(1, 50)
        self.parametersPanel.tableViewSectors.setColumnWidth(2, 150)
        self.parametersPanel.tableViewSectors.selectRow(0)
        
        self.parametersPanel.tableViewSectors.setEditTriggers(QAbstractItemView.NoEditTriggers)
    def method_27(self):
        if self.standardItermModel.rowCount()  == 0:
            QMessageBox.warning(self, "Warning", Messages.ERR_AT_LEAST_ONE_SECTOR_MUST_BE_SPECIFIED)
            return False
        return True
    def  method_42(self):
        point3d = self.parametersPanel.pnlFacility.Point3d;
        msaCalculationAreas = []
        num = 0;
        for i in range(self.standardItermModel.rowCount()):
            item = float(self.standardItermModel.item(i, 0).text())
            item1 = float(self.standardItermModel.item(i, 1).text())
            distance = Distance(None)
            if self.standardItermModel.item(i, 2) == None:
                distance = Distance(None)
            elif self.standardItermModel.item(i, 2).text() == "":
                distance = Distance(None)
            else:
                distance = Distance(float(self.standardItermModel.item(i, 2).text()), DistanceUnits.NM)
            num1 = Altitude(float(self.parametersPanel.txtMoc.text())).Metres;
            if (not distance.IsValid()):
                msaCalculationAreas.append(MsaCalculationArea(MsaCalculationAreaType.SingleArea, num, point3d, item, item1, Distance(25, DistanceUnits.NM), TurnDirection.Right, num1));
            else:
                msaCalculationAreas.append(MsaCalculationArea(MsaCalculationAreaType.InnerArea, num, point3d, item, item1, distance, TurnDirection.Right, num1));
                msaCalculationAreas.append(MsaCalculationArea(MsaCalculationAreaType.OuterArea, num, point3d, item, item1, distance, TurnDirection.Right, num1, Distance(25, DistanceUnits.NM)));
            num += 1
        return msaCalculationAreas;
    def method_43(self):
        distance = Distance(30, DistanceUnits.NM);
        polylineArea = PolylineArea(None, self.parametersPanel.pnlFacility.Point3d, distance.Metres);
        return PrimaryObstacleArea(polylineArea);
    def tableViewSectors_doubleClicked(self, modelIndex):
        if modelIndex == None:
            return
        startAngle = float(self.standardItermModel.item(modelIndex.row(), 0).text())
        endAngle = float(self.standardItermModel.item(modelIndex.row(), 1).text())
        self.draw(self.parametersPanel.picPreview, startAngle, endAngle)   
        
        if QMessageBox.Ok == QMessageBox.question(self, "Question", "Please click 'Ok' button if you want to split.\n" + "Please click 'No' button if you want to modify.", QMessageBox.Ok, QMessageBox.No): 
            self.btnSectorSplit_clicked()
        else:
            self.btnSectorModify_clicked()
    def tableViewSectors_clicked(self, modelIndex):
        if modelIndex == None:
            return
        startAngle = float(self.standardItermModel.item(modelIndex.row(), 0).text())
        endAngle = float(self.standardItermModel.item(modelIndex.row(), 1).text())
        self.draw(self.parametersPanel.picPreview, startAngle, endAngle)

    def btnSectorDelete_clicked(self):
        if self.rowID < 0:
            return
        self.modelIndex = self.parametersPanel.tableViewSectors.currentIndex()
        
        if self.modelIndex.row() == self.rowID:
            self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row() - 1, 1), QVariant(0))
            self.parametersPanel.tableViewSectors.selectRow(self.modelIndex.row() - 1)
            self.rowID -= 1
            self.standardItermModel.removeRow(self.modelIndex.row())
            self.draw(self.parametersPanel.picPreview, float(self.standardItermModel.item(self.modelIndex.row() - 1).text()), 0)
            self.parametersPanel.tableViewSectors.selectRow(self.modelIndex.row() - 1)
        elif self.modelIndex.row() == 0:
            self.standardItermModel.setData(self.standardItermModel.index(1, 0), QVariant(0))
            self.rowID -= 1
            self.standardItermModel.removeRow(self.modelIndex.row())
            self.draw(self.parametersPanel.picPreview, 0, float(self.standardItermModel.item(0, 1).text()))
            self.parametersPanel.tableViewSectors.selectRow(0)
        else:
            self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row() - 1, 1), QVariant(self.standardItermModel.item(self.modelIndex.row(), 1).text()))
            self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row() + 1, 0), QVariant(self.standardItermModel.item(self.modelIndex.row(), 1).text()))
            self.parametersPanel.tableViewSectors.selectRow(self.modelIndex.row() - 1)
            self.rowID -= 1
            self.standardItermModel.removeRow(self.modelIndex.row())
            self.draw(self.parametersPanel.picPreview, float(self.standardItermModel.item(self.modelIndex.row() - 1).text()), float(self.standardItermModel.item(self.modelIndex.row() - 1, 1).text()))
            self.parametersPanel.tableViewSectors.selectRow(self.modelIndex.row() - 1)
        
        
        
    def btnSectorModify_clicked(self):
#         self.splitSectorDlg = self.splitSectorDlg(self)
        self.splitSectorDlg.setWindowTitle("Split Sector(Modify)")
        self.splitSectorDlg.ui.frame_Length.setEnabled(False)
        self.splitSectorDlg.ui.frame_Length_2.setEnabled(True)
        self.modelIndex = self.parametersPanel.tableViewSectors.currentIndex()
        if self.modelIndex.row() == self.standardItermModel.rowCount() - 1:
            self.splitSectorDlg.ui.frame_Length_2.setEnabled(False)
        self.splitSectorDlg.ui.txtFrom.setText(self.standardItermModel.item(self.modelIndex.row()).text())
        self.splitSectorDlg.ui.txtTo.setText(self.standardItermModel.item(self.modelIndex.row(), 1).text())
        if self.standardItermModel.item(self.modelIndex.row(), 2) != None:
            self.splitSectorDlg.ui.txtRadius.setText(self.standardItermModel.item(self.modelIndex.row(), 2).text())
        
        self.splitSectorDlg.show()
        QObject.connect(self.splitSectorDlg.ui.buttonBox, SIGNAL("accepted()"), self.splitEvent)
        
            
    def btnSectorNew_clicked(self):
        self.standardItermModel.clear()
        # item0 = QStandardItem("0")
        # item1 = QStandardItem("0")
        # item2 = QStandardItem("")
        # self.standardItermModel.appendRow([item0, item1, item2])

        itemFrom = QStandardItem("From(" + unicode("°", "utf-8") + ")")
        itemTo = QStandardItem("To(" + unicode("°", "utf-8") + ")")
        itemRadius = QStandardItem("Step-down Radius(nm)")
        self.standardItermModel.setHorizontalHeaderItem(0, itemFrom)
        self.standardItermModel.setHorizontalHeaderItem(1, itemTo)
        self.standardItermModel.setHorizontalHeaderItem(2, itemRadius)
        self.standardItermModel.insertRow(0)
        self.standardItermModel.setData(self.standardItermModel.index(0, 0), QVariant(0))
        self.standardItermModel.setData(self.standardItermModel.index(0, 1), QVariant(0))
        self.standardItermModel.setData(self.standardItermModel.index(0, 2), QVariant(""))
        self.parametersPanel.tableViewSectors.setSelectionBehavior(1)
        self.parametersPanel.tableViewSectors.setModel(self.standardItermModel)
        self.parametersPanel.tableViewSectors.setColumnWidth(0, 50)
        self.parametersPanel.tableViewSectors.setColumnWidth(1, 50)
        self.parametersPanel.tableViewSectors.setColumnWidth(2, 150)
        self.parametersPanel.tableViewSectors.selectRow(0)
    def btnSectorSplit_clicked(self):
        
        
        self.splitSectorDlg.setWindowTitle("Split Sector(Split)")
        self.splitSectorDlg.ui.frame_Length.setEnabled(False)
        self.splitSectorDlg.ui.frame_Length_2.setEnabled(True)
        
        self.modelIndex = self.parametersPanel.tableViewSectors.currentIndex()
        
        self.splitSectorDlg.ui.txtFrom.setText(self.standardItermModel.item(self.modelIndex.row()).text())
        self.splitSectorDlg.ui.txtTo.setText("")
        self.splitSectorDlg.ui.txtRadius.setText("")
        result = self.splitSectorDlg.show()
        QObject.connect(self.splitSectorDlg.ui.buttonBox, SIGNAL("accepted()"), self.splitEvent)
        
    def splitEvent(self):   
        if self.splitSectorDlg.windowTitle() == "Split Sector(Modify)": 
            if self.modelIndex.row() != self.standardItermModel.rowCount() - 1:
                try:
                    if float(self.splitSectorDlg.ui.txtTo.text()) <= float(self.splitSectorDlg.ui.txtFrom.text()):
                        self.splitSectorDlg.accept()
                        return
                except:
                    self.splitSectorDlg.accept()
                    return
                if float(self.splitSectorDlg.ui.txtTo.text()) <= 0 or float(self.splitSectorDlg.ui.txtTo.text()) >= 360:
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row(), 1), QVariant(0))
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row(), 2), QVariant(self.splitSectorDlg.ui.txtRadius.text()))
                    self.draw(self.parametersPanel.picPreview, float(self.splitSectorDlg.ui.txtFrom.text()), 0)
                    self.standardItermModel.removeRows(self.modelIndex.row() + 1, self.rowID - self.modelIndex.row())
                else:
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row(), 1), QVariant(self.splitSectorDlg.ui.txtTo.text()))
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row(), 2), QVariant(self.splitSectorDlg.ui.txtRadius.text()))
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row() + 1, 0), QVariant(self.splitSectorDlg.ui.txtTo.text()))
                    self.draw(self.parametersPanel.picPreview, float(self.splitSectorDlg.ui.txtFrom.text()), float(self.splitSectorDlg.ui.txtTo.text()))
            else:
                self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row(), 2), QVariant(self.splitSectorDlg.ui.txtRadius.text()))
        else:
            try:
                if float(self.splitSectorDlg.ui.txtTo.text()) <= float(self.splitSectorDlg.ui.txtFrom.text()):
                    self.splitSectorDlg.accept()
                    return
            except:
                self.splitSectorDlg.accept()
                return
            if self.modelIndex.row() != self.standardItermModel.rowCount() - 1:
                if self.splitSectorDlg.ui.txtTo.text() == self.standardItermModel.item(self.modelIndex.row() , 1).text():
                    self.splitSectorDlg.accept()
                    return
            
            if self.modelIndex.row() != self.standardItermModel.rowCount() - 1:
                if float(self.standardItermModel.item(self.modelIndex.row(), 1).text()) <= float(self.splitSectorDlg.ui.txtTo.text()) or float(self.splitSectorDlg.ui.txtTo.text()) <= 0 or float(self.splitSectorDlg.ui.txtTo.text()) >= 360:
                    self.splitSectorDlg.accept()
                    return
                else:
                    toValue = self.standardItermModel.item(self.modelIndex.row(), 1).text()
                    self.standardItermModel.insertRow(self.modelIndex.row() + 1)     
                    
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row() + 1, 0), QVariant(self.splitSectorDlg.ui.txtTo.text()))
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row() + 1, 1), QVariant(self.standardItermModel.item(self.modelIndex.row(), 1).text()))
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row() + 1, 2), QVariant(self.standardItermModel.item(self.modelIndex.row(), 2).text()))
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row(), 2), QVariant(self.splitSectorDlg.ui.txtRadius.text()))
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row(), 1), QVariant(self.splitSectorDlg.ui.txtTo.text()))
                    self.draw(self.parametersPanel.picPreview, float(self.splitSectorDlg.ui.txtFrom.text()), float(self.splitSectorDlg.ui.txtTo.text()))
            else:
                if float(self.splitSectorDlg.ui.txtTo.text()) <= 0 or float(self.splitSectorDlg.ui.txtTo.text()) >= 360:
                    if self.modelIndex.row() == self.rowID:
                        self.splitSectorDlg.accept()
                        return
    
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row(), 1), QVariant(0))
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row(), 2), QVariant(self.splitSectorDlg.ui.txtRadius.text()))
                    self.draw(self.parametersPanel.picPreview, float(self.splitSectorDlg.ui.txtFrom.text()), 0)          
                    return         
                else:
#                     if float(self.splitSectorDlg.ui.txtTo.text()) >= float(self.standardItermModel.item(self.modelIndex.row() + 1).text()):
#                         self.splitSectorDlg.accept()
#                         return
                    toValue = self.standardItermModel.item(self.modelIndex.row(), 1).text()
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row(), 1), QVariant(self.splitSectorDlg.ui.txtTo.text()))
    #                 self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row(), 2), QVariant(self.splitSectorDlg.ui.txtRadius.text()))
                    self.rowID += 1                
                    
                    self.standardItermModel.insertRow(self.modelIndex.row() + 1)     
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row() + 1, 0), QVariant(self.standardItermModel.item(self.modelIndex.row(), 1).text()))
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row() + 1, 1), QVariant(toValue))
                    self.standardItermModel.setData(self.standardItermModel.index(self.modelIndex.row(), 2), QVariant(self.splitSectorDlg.ui.txtRadius.text()))
                    self.draw(self.parametersPanel.picPreview, float(self.splitSectorDlg.ui.txtFrom.text()), float(self.splitSectorDlg.ui.txtTo.text()))
        self.splitSectorDlg.accept()
        pass           
    def draw(self, graphicsView, startAngle0, endAngle0):
        if endAngle0 != 0:
            startAngle = self.getStartAngle(startAngle0, endAngle0)
            spanAngle = endAngle0 - startAngle0
        else:
            startAngle = self.getStartAngle(startAngle0, 360)
            spanAngle = 360 - startAngle0
        graphicsScene = QGraphicsScene()
        graphicsEllipseItem = QGraphicsEllipseItem(0, 0, graphicsView.width() - 20, graphicsView.width() - 20)
        graphicsEllipseItem.setStartAngle(startAngle * 16)
        graphicsEllipseItem.setSpanAngle(spanAngle * 16)
        brush = QBrush()
        pen = QPen()
        pen.setColor(Qt.red)
        brush.setColor(Qt.darkRed)
        brush.setStyle(Qt.SolidPattern)
        graphicsEllipseItem.setBrush(brush)
        
        graphicsEllipseItem1 = QGraphicsEllipseItem(0, 0, graphicsView.width() - 20, graphicsView.width() - 20)
        graphicsScene.addItem(graphicsEllipseItem1)
        graphicsScene.addItem(graphicsEllipseItem)
        if self.rowID > 0:
            for i in range(self.standardItermModel.rowCount()):
                
                if float(self.standardItermModel.item(i, 1).text()) != 0:
                    startAngle = self.getStartAngle(float(self.standardItermModel.item(i, 0).text()), float(self.standardItermModel.item(i, 1).text()))
                    spanAngle = float(self.standardItermModel.item(i, 1).text()) - float(self.standardItermModel.item(i, 0).text())
                else:
                    startAngle = self.getStartAngle(float(self.standardItermModel.item(i, 0).text()), 360)
                    spanAngle = 360 - float(self.standardItermModel.item(i, 0).text())
#                 graphicsScene = QGraphicsScene()
                graphicsEllipseItem = QGraphicsEllipseItem(0, 0, graphicsView.width() - 20, graphicsView.width() - 20)
                graphicsEllipseItem.setStartAngle(startAngle * 16)
                graphicsEllipseItem.setSpanAngle(spanAngle * 16)
                graphicsEllipseItemRadius = QGraphicsEllipseItem(0, 0, 0, 0)
                if self.standardItermModel.item(i, 2) != None:
                    radiusStr = self.standardItermModel.item(i, 2).text()
                else:
                    radiusStr = ""
                if radiusStr != "" and radiusStr != "0":
                    graphicsEllipseItemRadius = QGraphicsEllipseItem(20, 20, (graphicsView.width() - 20) / 2, (graphicsView.width() - 20) / 2)
                    graphicsEllipseItemRadius.setStartAngle(startAngle * 16)
                    graphicsEllipseItemRadius.setSpanAngle(spanAngle * 16)
                    
                
                graphicsScene.addItem(graphicsEllipseItem)
                graphicsScene.addItem(graphicsEllipseItemRadius)
#         print graphicsView.width()
        graphicsView.setScene(graphicsScene)
    def getStartAngle(self, startAngle, endAngle):
        temp = 360 - (endAngle - 90)
        if temp > 360 :
            temp = temp - 360
        return temp
class MsaCalculationArea:
    def __init__(self, msaCalculationAreaType_0, int_0, point3d_0, double_0, double_1, distance_0, turnDirection_0, double_2, distance_1 = None):
        self.hasInnerCircle = False
        self.name = None
        self.nominalArea = None
        self.bufferArea = None
        if distance_1 == None:
            polylineArea = PolylineArea()
            num = Unit.ConvertNMToMeter(5);
            num1 = Unit.ConvertDegToRad(double_0);
            num2 = Unit.ConvertDegToRad(double_1);
            if (MathHelper.smethod_63(double_0, double_1, AngleUnits.Degrees) != TurnDirection.Nothing):
                point3d = MathHelper.distanceBearingPoint(point3d_0, num1, distance_0.Metres);
                point3d1 = MathHelper.distanceBearingPoint(point3d_0, num2, distance_0.Metres);
                polylineArea = PolylineArea()
                polylineArea.Add(PolylineAreaPoint(point3d_0))
                polylineArea.Add(PolylineAreaPoint(point3d, MathHelper.smethod_57(turnDirection_0, point3d, point3d1, point3d_0)))
                polylineArea.Add(PolylineAreaPoint(point3d1))
            else:
                polylineArea = PolylineArea(None, point3d_0, distance_0.Metres)
            self.nominal = PrimaryObstacleArea(polylineArea);
            self.nominalArea = polylineArea
            self.buffer = PrimaryObstacleArea(polylineArea.method_18(num));
            self.bufferArea = polylineArea.method_18(num)
            self.sectorIndex = int_0;
            self.sectorTitle = self.method_2(double_0, double_1);
            self.sectorRadius = self.method_3(msaCalculationAreaType_0, distance_0);
            self.sectorType = msaCalculationAreaType_0;
            self.primaryMoc = double_2;
            self.name = self.sectorTitle + self.sectorRadius
        else:
            polylineArea = PolylineArea()
            num = Unit.ConvertNMToMeter(5);
            num1 = Unit.ConvertDegToRad(double_0);
            num2 = Unit.ConvertDegToRad(double_1);
            if (MathHelper.smethod_63(double_0, double_1, AngleUnits.Degrees) != TurnDirection.Nothing):
                point3d = MathHelper.distanceBearingPoint(point3d_0, num1, distance_1.Metres);
                point3d1 = MathHelper.distanceBearingPoint(point3d_0, num2, distance_1.Metres);
                point3d2 = MathHelper.distanceBearingPoint(point3d_0, num2, distance_0.Metres);
                point3d3 = MathHelper.distanceBearingPoint(point3d_0, num1, distance_0.Metres);
                polylineArea = PolylineArea()
                polylineArea.Add(PolylineAreaPoint(point3d, MathHelper.smethod_57(turnDirection_0, point3d, point3d1, point3d_0)))
                polylineArea.Add(PolylineAreaPoint(point3d1))
                polylineArea.Add(PolylineAreaPoint(point3d2, MathHelper.smethod_57(MathHelper.smethod_67(turnDirection_0), point3d2, point3d3, point3d_0)))
                polylineArea.Add(PolylineAreaPoint(point3d3))
            else:
                polylineArea = PolylineArea(None, point3d_0, distance_1.Metres);
                self.innerCircleCenter = point3d_0;
                self.innerCircleRadius = distance_0.Metres - num;
                self.hasInnerCircle = True;
            self.nominal = PrimaryObstacleArea(polylineArea);
            self.nominalArea = polylineArea
            self.buffer = PrimaryObstacleArea(polylineArea.method_18(num));
            self.bufferArea = polylineArea.method_18(num)
            self.sectorIndex = int_0;
            self.sectorTitle = self.method_2(double_0, double_1);
            self.sectorRadius = self.method_3(msaCalculationAreaType_0, distance_0);
            self.sectorType = msaCalculationAreaType_0;
            self.primaryMoc = double_2;
            self.name = self.sectorTitle + self.sectorRadius
    
    def method_0(self):
        point3dCollectionList = []
        polylineArea = self.method_131(self.nominal.previewArea); 
        point3dCollectionList.append(polylineArea.method_14_closed())
        
        polylineArea = self.method_131(self.buffer.previewArea); 
        point3dCollectionList.append(polylineArea.method_14_closed())
        
#         polyline.set_Closed(true);
#         polyline.set_ConstantWidth(500);
#         AcadHelper.smethod_18(transaction_0, blockTableRecord_0, polyline, string_0);
#         polyline = AcadHelper.smethod_131(this.buffer.PreviewArea);
#         polyline.set_Closed(true);
#         AcadHelper.smethod_18(transaction_0, blockTableRecord_0, polyline, string_0);
        if (self.hasInnerCircle):
            point3dCollectionList.append(MathHelper.constructCircle(self.innerCircleCenter, self.innerCircleRadius, 50))
#             AcadHelper.smethod_18(transaction_0, blockTableRecord_0, new Circle(this.innerCircleCenter, AcadHelper.Normal, this.innerCircleRadius), string_0);
        return point3dCollectionList
    def method_1(self, obstacle_0):
        double_0 = self.primaryMoc * obstacle_0.MocMultiplier;
        double_1 = None
        if (not self.buffer.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
            return (False, double_0, double_1)
        if (self.hasInnerCircle and MathHelper.calcDistance(self.innerCircleCenter, obstacle_0.Position) + obstacle_0.Tolerance < self.innerCircleRadius):
            return (False, double_0, double_1)
        position = obstacle_0.Position;
        double_1 = position.get_Z() + obstacle_0.Trees + double_0;
        return (True, double_0, double_1)
    
    def method_2(self, double_0, double_1):
        return str(round(double_0, 2)) + " - " + str(round(double_1, 2))
    
    def method_3(self, msaCalculationAreaType_0, distance_0):
        if (msaCalculationAreaType_0 == MsaCalculationAreaType.InnerArea):
            return " (0 -" + str(int(distance_0.NauticalMiles)) + " nm)"
#             return string.Format(" (0 - {0})", distance_0.method_0("0.#:nm"));
        if (msaCalculationAreaType_0 != MsaCalculationAreaType.OuterArea):
            return ""
        str0 = str(int(distance_0.NauticalMiles))
        distance = Distance(25, DistanceUnits.NM);
        return " (" + str0 + " - " + str(int(distance.NauticalMiles)) + " nm)"
#         return " ({0} - {1})", str, distance.method_0("0:nm"));
    def method_131(self, polylineArea_0):
#         Polyline polyline = new Polyline();
        polyline = PolylineArea()
        if (not polylineArea_0.isCircle):
            for i in range(polylineArea_0.Count):
                item = polylineArea_0[i];
                x = item.Position.get_X();
                position = item.Position;
                polyline.Add(PolylineAreaPoint(Point3D(x, position.get_Y()), item.Bulge))
        else:
            point3d = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 0, polylineArea_0.Radius);
            point3d1 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 1.5707963267949, polylineArea_0.Radius);
            point3d2 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 3.14159265358979, polylineArea_0.Radius);
            point3d3 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint, 4.71238898038469, polylineArea_0.Radius);
            polyline.Add(PolylineAreaPoint(Point3D(point3d.get_X(), point3d.get_Y()), MathHelper.smethod_60(point3d, point3d1, point3d2)))
            polyline.Add(PolylineAreaPoint(Point3D(point3d2.get_X(), point3d2.get_Y()), MathHelper.smethod_60(point3d2, point3d3, point3d)))
            polyline.Add(PolylineAreaPoint(Point3D(point3d.get_X(), point3d.get_Y()), 0))
        return polyline
class MsaCalculationObstacles(ObstacleTable):
    def __init__(self, surfacesList):
        ObstacleTable.__init__(self, surfacesList)
        self.surfaceType = SurfaceTypes.MSA
        self.surfacesList  = surfacesList
        self.obstaclesChecked = 0
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
        num2 = 0;
        
        for area in self.surfacesList:
            result, num, num1 = area.method_1(obstacle_0)
            if (result):
                checkResult = [num, num1, area.sectorTitle + area.sectorRadius]
                self.addObstacleToModel(obstacle_0, checkResult)
#                 MsaCalculation.obstacles[num2].method_11(obstacle_0, num, num1);
#                 MsaCalculation.MsaCalculationObstacles item = MsaCalculation.obstacles[num2];
                self.obstaclesChecked += 1;
            num2 += 1
    def method_12(self, surfaceName, altitudeUnits_0):
        self.setFilterFixedString(surfaceName)
        self.sort(self.IndexOcaM, Qt.DescendingOrder )
        
        if (self.rowCount() == 0):
            return Captions.GROUND_PLANE
        if (altitudeUnits_0 == AltitudeUnits.M):
            item = self.data(self.index(0, self.IndexOcaM), Qt.DisplayRole).toDouble()[0]
            num = item % 50;
            if (num > 0):
                item = item + (50 - num)
            altitude = Altitude(round(item), AltitudeUnits.M);
            return str(int(altitude.Metres)) + "m"
        item1 = self.data(self.index(0, self.IndexOcaFt), Qt.DisplayRole).toDouble()[0]
        num1 = item1 % 100
        if (num1 > 0):
            item1 = item1 + (100 - num1);
        altitude1 = Altitude(round(item1), AltitudeUnits.FT);
        return str(int(altitude1.Feet)) + "ft"
class MsaCalculationAreaType:
    SingleArea = 0
    InnerArea = 1
    OuterArea = 2