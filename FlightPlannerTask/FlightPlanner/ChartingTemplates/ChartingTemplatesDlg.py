# -*- coding: UTF-8 -*-
'''
Created on 24 May 2014

@author: Administrator
'''
from PyQt4.QtGui import QMessageBox, QStandardItem, QFileDialog
from PyQt4.QtCore import QCoreApplication, QString, SIGNAL, Qt, QFile, QFileInfo, QTextStream
from PyQt4.QtXml import QDomDocument
from qgis.core import QGis, QgsLayerTreeLayer, QgsVectorLayer
from qgis.gui import QgsMapTool, QgsMapCanvasSnapper, QgsRubberBand
from map.tools import QgsMapToolSelectUtils
from FlightPlanner.QgisHelper import QgisHelper, Geo

from FlightPlanner.ChartingTemplates.ui_ChartingTemplates import Ui_ChartingTemplates
from FlightPlanner.Dialogs.DlgChartingTemplate import DlgChartingTemplate
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import DrawingSpace, Point3D, AngleUnits, SurfaceTypes,\
                Matrix3d, Vector3d
from Type.FasDataBlockFile import FasDataBlockFile
from FlightPlanner.types import EnumsType, TurnDirection, Point3dCollection
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.helpers import Distance, Speed, Altitude, MathHelper, Unit
from Type.Degrees import Degrees, DegreesType, DegreesStyle
from Type.switch import switch
from Type.String import String
import define
import math

class ChartingTemplatesDlg(FlightPlanBaseDlg):
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("ChartingGridDlg")
        self.surfaceType = SurfaceTypes.ChartingGrid

        self.initParametersPan()
        self.uiStateInit()
        self.setWindowTitle(SurfaceTypes.ChartingGrid)
        self.resize(500, 400)

        self.constructionLayer = None
        self.selectedRow = None


    def btnEvaluate_Click(self):
        return FlightPlanBaseDlg.btnEvaluate_Click(self)



    

        

    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(1)
        self.ui.tabCtrlGeneral.removeTab(1)
        self.ui.btnOpenData.setVisible(False)
        self.ui.btnSaveData.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)
        self.ui.btnEvaluate.setVisible(False)

        # self.ui.btnConstruct.setIcon(None)
        self.ui.btnConstruct.setToolTip("Load")

        return FlightPlanBaseDlg.uiStateInit(self)
         


    def initParametersPan(self):
        ui = Ui_ChartingTemplates()
        self.parametersPanel = ui
        
        FlightPlanBaseDlg.initParametersPan(self)
        self.parametersPanel.grid.pressed.connect(self.grid_pressed)
        self.parametersPanel.btnAdd.clicked.connect(self.btnAdd_clicked)
        self.parametersPanel.btnModify.clicked.connect(self.btnModify_clicked)
        self.parametersPanel.btnRemove.clicked.connect(self.btnRemove_clicked)
    def btnRemove_clicked(self):
        if self.selectedRow == None:
            return
        self.parametersPanel.gridModel.removeRow(self.selectedRow)
        self.method_30()
    def btnModify_clicked(self):
        if self.selectedRow == None:
            return
        result, str0, drawingSpace = DlgChartingTemplate.smethod_1(self, self.parametersPanel.gridModel.item(self.selectedRow, 0).text(), self.parametersPanel.gridModel.item(self.selectedRow, 1).text())
        if result:
            self.parametersPanel.gridModel.setItem(self.selectedRow, 0, QStandardItem(str0))
            self.parametersPanel.gridModel.setItem(self.selectedRow, 1, QStandardItem(drawingSpace))
        self.method_30()
    def btnAdd_clicked(self):
        filePath = QFileDialog.getOpenFileName(self, "Open xml file",QCoreApplication.applicationDirPath (),"xml files(*.xml )")
        if filePath == "":
            return
        fileInfo = QFileInfo(filePath)
        if not fileInfo.isFile():
            return
        str0 = ""
        drawingSpace = DrawingSpace.PaperSpace
        result, str0, drawingSpace = DlgChartingTemplate.smethod_0(self, str0, drawingSpace, filePath)
        if result:
            numArray = fileInfo.size()
            rowCount = self.parametersPanel.gridModel.rowCount()
            self.parametersPanel.gridModel.setItem(rowCount, 0, QStandardItem(str0))
            self.parametersPanel.gridModel.setItem(rowCount, 1, QStandardItem(drawingSpace))
            self.parametersPanel.gridModel.setItem(rowCount, 2, QStandardItem(str(numArray)))
        self.method_30()


    def btnConstruct_Click(self):
        pass

    def grid_pressed(self, modelIndex):
        self.selectedRow = modelIndex.row()

    def method_30(self):
        filePath = define.appPath + "/Resource/settingData/phxtemplates.xml"
        fileInfo = QFileInfo(filePath)
        if fileInfo.exists():
            QFile.remove(filePath)

        doc = QDomDocument()
        rootElem = doc.createElement("Templates")
        xmlDeclaration = doc.createProcessingInstruction( "xml", "version=\"1.0\" encoding=\"utf-8\"" )
        doc.appendChild( xmlDeclaration )

        for i in range(self.parametersPanel.gridModel.rowCount()):
            elem = doc.createElement("Templates" + self.parametersPanel.gridModel.item(i, 0).text())
            valueElem = doc.createElement("title")
            valueElem.appendChild(doc.createTextNode(self.parametersPanel.gridModel.item(i, 0).text()))
            elem.appendChild(valueElem)

            valueElem = doc.createElement("space")
            valueElem.appendChild(doc.createTextNode(self.parametersPanel.gridModel.item(i, 1).text()))
            elem.appendChild(valueElem)

            valueElem = doc.createElement("value")
            valueElem.appendChild(doc.createTextNode(self.parametersPanel.gridModel.item(i, 2).text()))
            elem.appendChild(valueElem)

            rootElem.appendChild(elem)

        doc.appendChild(rootElem)
        qFile = QFile(filePath)
        if qFile.open(QFile.WriteOnly):
            textStream = QTextStream(qFile)
            doc.save(textStream, 4)
            qFile.close()

            # ###CRC file is created.
            contents = None
            with open(filePath, 'rb', 0) as tempFile:
                contents = tempFile.read()
                tempFile.flush()
                tempFile.close()
            bytes = FasDataBlockFile.CRC_Calculation(contents)
            string_0 = QString(filePath)
            path = string_0.left(string_0.length() - 3) + "crc"
            fileStream = open(path, 'wb')
            fileStream.write(bytes)
            fileStream.close()
    # def method_31(self):
    #     if (self.grid.SelectedRows == null || self.grid.SelectedRows.Count == 1)
    #     {
    #         return true;
    #     }
    #     InfoMessageBox.smethod_0(self, Validations.PLEASE_SELECT_A_TEMPLATE);
        
    def method_32(self):
        flag = self.selectedRow != None
        self.parametersPanel.btnModify.setEnabled(flag)
        self.parametersPanel.btnRemove.setEnabled(flag)
    
    



