'''
Created on Mar 30, 2015

@author: Administrator
'''
from PyQt4.QtGui import QDialog, QFileDialog, QFont, QMessageBox, QPushButton, \
            QAbstractItemView, QWidget, QLineEdit, QComboBox, QIcon, QPixmap,\
            QStandardItemModel, QStandardItem, QCheckBox, QPalette, QBrush, QColor,\
            QMenu
from PyQt4.QtCore import QCoreApplication, Qt, QString, SIGNAL
from qgis._core import QgsLayerTreeGroup, QGis, QgsPoint, QgsRectangle

from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.ui_FlightPlannerBase import Ui_FlightPlannerBase
from FlightPlanner.Captions import Captions
from FlightPlanner.ExportDlg.ExportDlg import ExportDlg
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.messages import Messages
from FlightPlanner.types import Point3D
from FlightPlanner.Obstacle.Obstacle import Obstacle
from Type.String import String

import define

class FlightPlanBaseDlg(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        palette = QPalette();
        brush = QBrush(QColor(255, 255, 255, 255));
        brush.setStyle(Qt.SolidPattern);
        palette.setBrush(QPalette.Active, QPalette.Base, brush);
        palette.setBrush(QPalette.Active, QPalette.Window, brush);
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush);
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush);
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush);
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush);
        self.setPalette(palette);

        self.ui = Ui_FlightPlannerBase()
        self.ui.setupUi(self)

        
        self.newDlgExisting = False
        
        self.chbHideCloseInObst = QCheckBox(self.ui.grbResult)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chbHideCloseInObst.setFont(font)
        self.chbHideCloseInObst.setObjectName("chbHideCloseInObst")
        self.ui.vlResultGroup.addWidget(self.chbHideCloseInObst)
        self.chbHideCloseInObst.setText("Hide close-in obstacles")
        self.chbHideCloseInObst.setVisible(False)
        self.ui.tblHistory.setSelectionBehavior(1)
        # self.ui.tabCtrlGeneral.setTabsClosable(True)

        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)

        ''' combo boxes event '''
        self.ui.cmbObstSurface.currentIndexChanged.connect(self.cmbObstSurfaceChanged)
        self.ui.cmbUnits.currentIndexChanged.connect(self.changeResultUnit)
        ''' buttons clicked connect '''
        self.ui.btnClose.clicked.connect(self.reject)
        self.ui.btnClose_2.clicked.connect(self.reject)
        self.ui.btnHistoryClose.clicked.connect(self.reject)
        self.ui.btnConstruct.clicked.connect(self.btnConstruct_Click)
        self.ui.btnEvaluate.clicked.connect(self.btnEvaluate_Click)
        self.ui.btnOpenData.clicked.connect(self.openData)
        self.ui.btnSaveData.clicked.connect(self.saveData)
        self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        self.ui.btnExportResult.clicked.connect(self.exportResult)
        self.ui.tblHistory.clicked.connect(self.tblHistory_Click)
        self.ui.btnUpdateQA.clicked.connect(self.btnUpdateQA_Click)
        self.ui.btnUpdateQA_2.clicked.connect(self.btnUpdateQA_2_Click)
        self.ui.btnCriticalLocate.clicked.connect(self.criticalLocate)
        self.connect(self.ui.tblObstacles, SIGNAL("tableViewObstacleMouseReleaseEvent_rightButton"), self.tableViewObstacleMouseTeleaseEvent_rightButton)
        self.connect(self.ui.tblObstacles, SIGNAL("pressedEvent"), self.tblObstacles_pressed)
        ''' properties '''
        self.parametersPanel = None
        self.obstaclesModel = None
        self.surfaceType = ""
        self.surfaceSubGroupNames = []

        self.uiStateInit()
        self.obstacleTableInit()
        self.newDlgExisting = True
        self.resultColumnNames = []

        self.stdItemModelHistory = QStandardItemModel()
        # self.stdItemModelHistory.
        self.ui.tblHistory.setModel(self.stdItemModelHistory)

        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/btnImage/dlgIcon.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        self.resultLayerList = []
        self.symbolLayers = []
        self.selectedObstacleMoselIndex = None
        self.changedCriticalObstacleValue = []
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
        pass
    #     OasObstacles.resultCriticalObst.Obstacle = self.changedCriticalObstacleValue["Obstacle"]
    #     OasObstacles.resultCriticalObst.Surface = self.changedCriticalObstacleValue["SurfaceName"]
    #     OasObstacles.resultCriticalObst.Assigned = True
    #     ocaMValue = self.changedCriticalObstacleValue["OcaM"]
    #
    #     OasObstacles.resultOCA = Altitude(float(ocaMValue) if ocaMValue != "" else None)
    #     if OasObstacles.resultOCA == None:
    #         OasObstacles.resultOCH = None
    #     else:
    #         OasObstacles.resultOCH = OasObstacles.resultOCA - self.ui.pnlThr.Altitude()
    #
    #     point3d = self.ui.pnlThr.Point3d
    #     num = Unit.ConvertDegToRad(float(self.ui.txtTrack.Value))
    #     num1 = self.method_40()
    #     zC = OasObstacles.constants.ZC / OasObstacles.constants.ZA
    #     point3d1 = MathHelper.distanceBearingPoint(point3d, num, zC)
    #     metres2 = OasObstacles.resultCriticalObst.method_2(point3d).Metres
    #     z = metres2 - point3d.z()
    #     num3 = math.tan(Unit.ConvertDegToRad(num1))
    #     num4 = z / num3
    #     OasObstacles.resultSocPosition = MathHelper.distanceBearingPoint(point3d1, num + 3.14159265358979, num4).smethod_167(0)
    #     if (num4 > zC):
    #         OasObstacles.resultSocText = Messages.X_BEFORE_THRESHOLD % (num4 - zC)
    #     else:
    #         OasObstacles.resultSocText = Messages.X_PAST_THRESHOLD % (zC - num4)
    #     self.setCriticalObstacle()


    def criticalLocate(self):
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
    def trackRadialPanelSetEnabled(self):
        positionPanels = self.findChildren(PositionPanel)
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
    def setDataInHistoryModel(self, dataList, newFlag = False):
        # dataList is list of list of tuple with name and data
        # example
        # dataList = [ list of name, list of data ]
        # dataList = [["lat", "lon"], ["59", "17"]]
        if newFlag:
            self.stdItemModelHistory.setHorizontalHeaderLabels(dataList[0][0])
            for i in range(len(dataList)):
                for j in range(len(dataList[i][1])):
                    item = QStandardItem(dataList[i][1][j])
                    item.setEditable(False)
                    self.stdItemModelHistory.setItem(i, j, item)
            return
        if len(dataList) > 0:
            rowcount = self.stdItemModelHistory.rowCount()
            if self.stdItemModelHistory.rowCount() > 0:

                for i in range(len(dataList[1])):
                    item = QStandardItem(dataList[1][i])
                    item.setEditable(False)
                    self.stdItemModelHistory.setItem(rowcount, i, item)
                pass
            else:
                self.stdItemModelHistory.setHorizontalHeaderLabels(dataList[0])
                for i in range(len(dataList[1])):
                    item = QStandardItem(dataList[1][i])
                    item.setEditable(False)
                    self.stdItemModelHistory.setItem(0, i, item)
    def btnPDTCheck_Click(self):
        pass
    def cmbObstSurfaceChanged(self):
        if self.obstaclesModel != None:
            if self.ui.cmbObstSurface.currentIndex() == 0 and self.ui.cmbObstSurface.currentText() == "All":
                self.obstaclesModel.setFilterFixedString("")
            else:
                self.obstaclesModel.setFilterFixedString(self.ui.cmbObstSurface.currentText())


    def obstacleTableInit(self):
        self.ui.tblObstacles.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblObstacles.setSortingEnabled(True)

    def uiStateInit(self):
        self.ui.cmbUnits.addItems([Captions.METRES, Captions.FEET])
        self.ui.cmbUnits.setCurrentIndex(1)
        self.ui.cmbUnits.currentIndexChanged.connect(self.changeResultUnit)
        pass
    def tblHistory_Click(self, modelIndex):
        pass
    def btnConstruct_Click(self):
        # qgsLayerTreeView = define._mLayerTreeView
        # groupName = self.surfaceType
        # layerTreeModel = qgsLayerTreeView.layerTreeModel()
        # layerTreeGroup = layerTreeModel.rootGroup()
        # rowCount = layerTreeModel.rowCount()
        # groupExisting = False
        # if rowCount > 0:
        #     for i in range(rowCount):
        #         qgsLayerTreeNode = layerTreeModel.index2node(layerTreeModel.index(i, 0))
        #         if qgsLayerTreeNode.nodeType() == 0:
        #             qgsLayerTreeNode._class_ =  QgsLayerTreeGroup
        #             if isinstance(qgsLayerTreeNode, QgsLayerTreeGroup) and qgsLayerTreeNode.name() == groupName:
        #                 groupExisting = True
        #
        # if groupExisting:
        #     if len(self.resultLayerList) > 0:
        #         QgisHelper.removeFromCanvas(define._canvas, self.resultLayerList)
        #         self.resultLayerList = []
        #     else:
        #         QMessageBox.warning(self, "Warning", "Please remove \"" + self.surfaceType + "\" layer group from LayerTreeView.")
        #         return False
        self.resultLayerList = []
        return True


    def btnUpdateQA_Click(self):
        pass
    def btnUpdateQA_2_Click(self):
        pass
    def btnEvaluate_Click(self):
        try:
            if self.obstaclesModel == None:
                self.initObstaclesModel()
                if self.obstaclesModel == None:
                    return
            surfaceLayers = QgisHelper.getSurfaceLayers(self.surfaceType, self.surfaceSubGroupNames)
            self.initObstaclesModel()
            self.obstaclesModel.loadObstacles(surfaceLayers)


            self.obstaclesModel.setLocateBtn(self.ui.btnLocate)
            self.ui.tblObstacles.setModel(self.obstaclesModel)
            self.obstaclesModel.setTableView(self.ui.tblObstacles)
            self.obstaclesModel.setHiddenColumns(self.ui.tblObstacles)
            self.ui.tabCtrlGeneral.setCurrentIndex(1)
            if self.ui.cmbObstSurface.isVisible():
                self.ui.cmbObstSurface.clear()
                self.initSurfaceCombo()
                self.ui.cmbObstSurface.setCurrentIndex(0)
            self.ui.btnExportResult.setEnabled(True)
            self.setResultPanel()

        except UserWarning as e:
            QMessageBox.warning(self, "Information", e.message)

    def initParametersPan(self):
        parametersPanelWidget = QWidget(self)
#         self.parametersPanel = uiObject
        if self.parametersPanel != None:
            self.parametersPanel.setupUi(parametersPanelWidget)
            self.ui.vlScrollWidget.addWidget(parametersPanelWidget)
            lstTextControls = self.ui.grbGeneral.findChildren(QLineEdit)
            for ctrl in lstTextControls:
                ctrl.textChanged.connect(self.initResultPanel)
            lstComboControls = self.ui.grbGeneral.findChildren(QComboBox)
            for ctrl in lstComboControls:
                ctrl.currentIndexChanged.connect(self.initResultPanel)
        # lstTextControls = self.findChildren(QLineEdit)
        # for ctrl in lstTextControls:
        #     ctrl.setMinimumWidth(100)
        #     ctrl.setMaximumWidth(100)
        # lstComboControls = self.findChildren(QComboBox)
        # for ctrl in lstComboControls:
        #     ctrl.setMinimumWidth(100)
        #     ctrl.setMaximumWidth(100)

            # newWidth = int(define._appWidth / float(1280) * parametersPanelWidget.width())
            # newHeight = int(define._appHeight / float(800) * parametersPanelWidget.height())
            # if newWidth > define._appWidth:
            #     newWidth -= 50
            # if newHeight > define._appHeight:
            #     newHeight -= 50
            # parametersPanelWidget.resize(newWidth, newHeight)
    def initResultPanel(self):
        if self.obstaclesModel != None and self.ui.btnEvaluate.isEnabled():
            self.obstaclesModel.clear()
            lstTextControls = self.ui.grbResult.findChildren(QLineEdit)
            for ctrl in lstTextControls:
                if ctrl.objectName() == "txtOCH" or ctrl.objectName() == "txtOCA":
                    continue
                ctrl.setText("")
        self.ui.btnExportResult.setDisabled(True)
        # self.ui.btnEvaluate.setEnabled(False)

        
    def initObstaclesModel(self):
        pass
    
    def initSurfaceCombo(self):
        pass
    
    def setResultPanel(self):
        pass
    def saveData(self):
        try:
            filePathDir = QFileDialog.getSaveFileName(self, "Save Input Data",QCoreApplication.applicationDirPath (),"Xml Files(*.xml)")        
            if filePathDir == "":
                return
            DataHelper.saveInputParameters(filePathDir, self)

            # contents = None
            # with open(filePathDir, 'rb', 0) as tempFile:
            #     contents = tempFile.read()
            #     tempFile.flush()
            #     tempFile.close()
            # bytes = FasDataBlockFile.CRC_Calculation(contents)
            # string_0 = QString(filePathDir)
            # path = string_0.left(string_0.length() - 3) + "crc"
            # fileStream = open(path, 'wb')
            # fileStream.write(bytes)
            # fileStream.close()
            return filePathDir
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
            
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

            # contents = None
            # with open(filePathDir, 'rb', 0) as tempFile:
            #     contents = tempFile.read()
            #     tempFile.close()
            # bytes = FasDataBlockFile.CRC_Calculation(contents)
            #
            # string_0 = QString(filePathDir)
            # crcFileDir = string_0.left(string_0.length() - 3) + "crc"
            # crcFileContents = None
            # with open(crcFileDir, 'rb', 0) as tempFileCrc:
            #     crcFileContents = tempFileCrc.read()
            #     tempFileCrc.close()
            # if bytes != crcFileContents:
            #     QMessageBox.warning(self, "Error", "Input file has been changed by outside.")
            #     return

            DataHelper.loadInputParameters(filePathDir, self)
            return filePathDir
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
            
    def exportResult(self):
        dlg = ExportDlg(self)
        dlg.ui.txtHeading.setText(self.surfaceType + "_Export")
        columnNames = []
        if self.obstaclesModel != None:
            columnNames = self.obstaclesModel.fixedColumnLabels
        self.stModel = QStandardItemModel()
        for i in range(len(columnNames)):
            stItem = QStandardItem(columnNames[i])
            stItem.setCheckable(True)
            checkFlag = True
            for hideColName in self.obstaclesModel.hideColumnLabels:
                if columnNames[i] == hideColName:
                    checkFlag = False
                    break
            if checkFlag: 
                stItem.setCheckState(Qt.Checked)
            else:
                stItem.setCheckState(Qt.Unchecked)
            self.stModel.setItem(i, 0, stItem)
        if len(columnNames) <= 0:
            return
        dlg.ui.listColumns.setModel(self.stModel)
        result = dlg.exec_()
        return (result, dlg.resultHideColumnIndexs)
    def changeResultUnit(self):
        pass

    def method_27(self, qarecord_0):
        pass
        # QA.smethod_2(qarecord_0);
        # self.method_20(Messages.QA_UPDATED);