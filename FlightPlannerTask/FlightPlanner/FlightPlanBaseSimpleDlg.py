'''
Created on 18 May 2014

@author: Administrator
'''

from PyQt4.QtGui import QDialog, QFileDialog, QMessageBox, QWidget, QPalette,\
    QBrush, QColor, QIcon, QPixmap
from PyQt4.QtCore import QCoreApplication, Qt
from qgis.core import QgsLayerTreeGroup

from FlightPlanner.messages import Messages
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.ui_FlightPlannerBaseNoTab import Ui_FlightPlannerSimpleBase
from FlightPlanner.QgisHelper import QgisHelper
import define

from Type.QA.QA import QA

class FlightPlanBaseSimpleDlg(QDialog):
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
        self.ui = Ui_FlightPlannerSimpleBase()
        self.ui.setupUi(self)        
              
        ''' buttons clicked connect '''
        self.ui.btnClose.clicked.connect(self.reject)
#         self.ui.btnClose_2.clicked.connect(self.reject)
        self.ui.btnConstruct.clicked.connect(self.btnConstruct_Click)
        self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        self.ui.btnUpdateQA.clicked.connect(self.btnUpdateQA_Click)
#         self.ui.btnEvaluate.clicked.connect(self.btnEvaluate_Click)
        self.ui.btnOpenData.clicked.connect(self.openData)
        self.ui.btnSaveData.clicked.connect(self.saveData)
        self.ui.btnExportResult.clicked.connect(self.exportResult)
        self.ui.btnExportResult.setDisabled(True)
        self.ui.btnExportResult.setVisible(False)
        ''' properties '''
        self.parametersPanel = None
        self.ui.btnUpdateQA.setVisible(False)
        # self.ui.btnUpdateQA_2.setVisible(False)
        
        self.uiStateInit()
#         self.obstacleTableInit()
        self.ui.btnPDTCheck.setVisible(False)

        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/btnImage/dlgIcon.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.resultLayerList = []
    def uiStateInit(self):
        pass
    
    def btnConstruct_Click(self):
        qgsLayerTreeView = define._mLayerTreeView
        groupName = self.surfaceType
        layerTreeModel = qgsLayerTreeView.layerTreeModel()
        layerTreeGroup = layerTreeModel.rootGroup()
        rowCount = layerTreeModel.rowCount()
        groupExisting = False
        if rowCount > 0:
            for i in range(rowCount):
                qgsLayerTreeNode = layerTreeModel.index2node(layerTreeModel.index(i, 0))
                if qgsLayerTreeNode.nodeType() == 0:
                    qgsLayerTreeNode._class_ = QgsLayerTreeGroup
                    if isinstance(qgsLayerTreeNode, QgsLayerTreeGroup) and qgsLayerTreeNode.name() == groupName:
                        groupExisting = True

        if groupExisting:
            if len(self.resultLayerList) > 0:
                QgisHelper.removeFromCanvas(define._canvas, self.resultLayerList)
                self.resultLayerList = []
            else:
                QMessageBox.warning(self, "Warning", "Please remove \"" + self.surfaceType + "\" layer group from LayerTreeView.")
                return False
        return True
    def btnPDTCheck_Click(self):
        pass
    def btnUpdateQA_Click(self):
        pass
    def initParametersPan(self):
        parametersPanelWidget = QWidget(self)
#         self.parametersPanel = uiObject
        if self.parametersPanel != None:
            self.parametersPanel.setupUi(parametersPanelWidget)
            self.ui.verticalLayout_ScrollWidget.addWidget(parametersPanelWidget)
#             lstTextControls = self.ui.grbGeneral.findChildren(QLineEdit)
#             for ctrl in lstTextControls:
#                 ctrl.textChanged.connect(self.initResultPanel)
#             lstComboControls = self.ui.grbGeneral.findChildren(QComboBox)
#             for ctrl in lstComboControls:
#                 ctrl.currentIndexChanged.connect(self.initResultPanel)
        
    def initResultPanel(self):
#         if self.obstaclesModel != None and self.ui.btnEvaluate.isEnabled():
#             self.obstaclesModel.clear()
#             lstTextControls = self.ui.grbResult.findChildren(QLineEdit)
#             for ctrl in lstTextControls:
#                 if ctrl.objectName() == "txtOCH" or ctrl.objectName() == "txtOCA":
#                     continue
#                 ctrl.setText("")
        self.ui.btnExportResult.setDisabled(True)
#         self.ui.btnEvaluate.setEnabled(False)
        
    def initObstaclesModel(self):
        pass
    
    def initSurfaceCombo(self):
        pass
    
    def saveData(self):
        try:
            filePathDir = QFileDialog.getSaveFileName(self, "Save Input Data",QCoreApplication.applicationDirPath (),"Xml Files(*.xml)")        
            if filePathDir == "":
                return
            DataHelper.saveInputParameters(filePathDir, self)
            return filePathDir
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
            
    def openData(self):
        try:
            filePathDir = QFileDialog.getOpenFileName(self, "Open Input Data",QCoreApplication.applicationDirPath (),"Xml Files(*.xml)")        
            if filePathDir == "":
                return
            DataHelper.loadInputParameters(filePathDir, self)
            return filePathDir
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
            
    def exportResult(self):
        pass
    def method_20(self, message):
        QMessageBox.information(self, "Result", message)
    def method_27(self, qarecord_0):
        QA.smethod_2(qarecord_0);
        self.method_20(Messages.QA_UPDATED);
