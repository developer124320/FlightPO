'''
Created on 10 Feb 2015

@author: Administrator
'''
from PyQt4.QtCore import QSize, Qt

from PyQt4.QtGui import QGridLayout, QDialog, QToolBar, QAction, QIcon, QStandardItemModel, QTableView, \
    QHeaderView, QStandardItem, QMessageBox
# from qgis.gui import 
from qgis.core import QgsVectorDataProvider
# from FlightPlanner.QgisHelper import QgisHelper
import define

class QgsAttributeTableDialog(QDialog):
    '''
    classdocs
    '''
    def __init__(self, parent, vectorlayer):
        QDialog.__init__(self, parent)
#         self.w = QDialog(self)
        self.baseLayer = vectorlayer
        self.canChangeAttributes = self.validate(QgsVectorDataProvider.ChangeAttributeValues)
        self.canDeleteFeatures = self.validate(QgsVectorDataProvider.DeleteFeatures)
        self.canAddAttributes = self.validate(QgsVectorDataProvider.AddAttributes)
        self.canDeleteAttributes = self.validate(QgsVectorDataProvider.DeleteAttributes)
        self.canAddFeatures = self.validate(QgsVectorDataProvider.AddFeatures)
        
        gridLayout = QGridLayout(self)
        self.setLayout(gridLayout)
        
        self.setWindowTitle("Attribute Table")
        self.setFixedSize(QSize(800, 600))
        
        editorToolbar = QToolBar()
        editorToolbar.setFixedSize(QSize(768, 48))
        self.actionToggleEditing = QAction(QIcon("Resource\\edit.png"),"ToggleEditing", self)
        self.actionToggleEditing.triggered.connect(self.toggleEditing)
        if (self.canChangeAttributes or self.canDeleteFeatures or self.canAddAttributes or self.canDeleteAttributes or self.canAddFeatures) and (not self.baseLayer.isReadOnly()):
            self.actionToggleEditing.setEnabled(True)
        else:
            self.actionToggleEditing.setEnabled(False)        
        self.actionToggleEditing.setCheckable(True)
        editorToolbar.addAction(self.actionToggleEditing)
        
        self.actionSave = QAction(QIcon("Resource\\filesave.png"),"Save Edits", self)
        self.actionSave.triggered.connect(self.saveEditing)
        self.actionSave.setCheckable(False)
        self.actionSave.setEnabled(False)
        editorToolbar.addAction(self.actionSave)
        
        self.actiondeleteRows = QAction(QIcon("Resource\\mActionDeleteSelected.png"),"Delete selected features", self)
        self.actiondeleteRows.triggered.connect(self.deleteRows)
        self.actiondeleteRows.setCheckable(False)
        self.actiondeleteRows.setEnabled(False)
        editorToolbar.addAction(self.actiondeleteRows)
        
        self.actionUnselectAll = QAction(QIcon("Resource\\mActionDeselectAll.png"),"Unselect All", self)
        self.actionUnselectAll.triggered.connect(self.unselectAll)
        self.actionUnselectAll.setCheckable(False)
        self.actionUnselectAll.setEnabled(True)
        editorToolbar.addAction(self.actionUnselectAll)
        
        self.actionSelectedToZoom = QAction(QIcon("Resource\\mActionZoomToSelected.png"),"Zoom map to the selected rows", self)
        self.actionSelectedToZoom.triggered.connect(self.selectedToZoom)
        self.actionSelectedToZoom.setCheckable(False)
        self.actionSelectedToZoom.setEnabled(True)
        editorToolbar.addAction(self.actionSelectedToZoom)

        gridLayout.addWidget(editorToolbar, 0, 0, 1, 1)
         
        self.model = QStandardItemModel()
        
#         self.model.itemChanged.connect(self.attributeChanged)
        self.attributeTable = QTableView(self)
        self.attributeTable.setModel(self.model)
        self.attributeTable.setColumnWidth(0, 200)
        self.attributeTable.setColumnWidth(1, 160)
        self.attributeTable.clicked.connect(self.tableSelectionChanged)
        self.attributeTable.setSortingEnabled(True)
        
        self.changeItemList = []
        self.selectRows = []
        self.isSave = True        
        self.initTable()
        gridLayout.addWidget(self.attributeTable, 1, 0, 1, 1)
#         self.attributeTable.selectionChanged.connect(self.selectFeature)
    def tableSelectionChanged(self):
        idxList = self.attributeTable.selectedIndexes()
        if idxList != None and len(idxList) > 0:
            self.baseLayer.removeSelection()
            fidList = []
            for idx in idxList:
                fid = int(self.model.item(idx.row()).text())
                fidList.append(fid)
            self.baseLayer.setSelectedFeatures(fidList)
    def toggleEditing(self):
        if self.baseLayer != None:
            
            if not self.actionToggleEditing.isChecked():
                
                if self.isSave:
                    self.baseLayer.commitChanges() 
                    self.actionSave.setEnabled(False)
                    self.actiondeleteRows.setEnabled(False)
                    self.model.itemChanged.disconnect(self.attributeChanged)
                    self.toggleEditingTable(False)                   
                else:      
                    button = QMessageBox.warning( self, "Stop Editing", "Do you want to save the changes to layer?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel )              
                    if (  button == QMessageBox.Cancel ):
                        self.actionToggleEditing.setChecked(True)
                        
                    elif button == QMessageBox.Save:
                        self.saveEditing()
                        self.baseLayer.commitChanges() 
                        self.actionSave.setEnabled(False)
                        self.actiondeleteRows.setEnabled(False)
                        self.model.itemChanged.disconnect(self.attributeChanged)
                        self.toggleEditingTable(False)      
                    else:
                        self.initTable()
                        self.baseLayer.commitChanges() 
                        self.actionSave.setEnabled(False)
                        self.actiondeleteRows.setEnabled(False)
                        self.model.itemChanged.disconnect(self.attributeChanged)
                        self.toggleEditingTable(False)             
#                 self.isEditable = False
            else:
                self.actionSave.setEnabled(True)
                self.actiondeleteRows.setEnabled(True)
                self.baseLayer.startEditing()
                self.toggleEditingTable(True)
                self.model.itemChanged.connect(self.attributeChanged)
#                 self.isEditable = True
    def toggleEditingTable(self, isEditable):
        columnCount = self.model.columnCount()
        rowCount = self.model.rowCount()
        col = 0
        while col < columnCount:
            row = 0
            while row < rowCount:
                self.model.item(row, col).setEditable(isEditable)
                row += 1
            col += 1
         
    def attributeChanged(self, standardItem):
        self.isSave = False
#         if not self.isDelete: 
        self.changeItemList.append(standardItem)
#         featureId = standardItem.row()
#         self.baseLayer.changeAttributeValue(featureId,
#                                        standardItem.column(), standardItem.text())
    def saveEditing(self):
        self.isSave = True
        if len(self.changeItemList) > 0:
            for standardItem in self.changeItemList:
                featureId = standardItem.row()
                self.baseLayer.changeAttributeValue(featureId,
                                               standardItem.column(), standardItem.text())
            self.changeItemList = []
        if len(self.selectRows) > 0:
            for id in self.selectRows:
                self.baseLayer.deleteFeature(id)                
            self.selectRows = []
    def initTable(self):
        self.model.clear()
#         header = QHeaderView(Qt.Horizontal)
#         headerModel = QStandardItemModel()
         
        layer = self.baseLayer
        fields = layer.pendingFields()
        headersList = ["fid"]
        for field in fields:
            headersList.append(field.name())
        self.model.setHorizontalHeaderLabels(headersList)
             
#         headerModel.setHorizontalHeaderLabels(headersList)
#         header.setModel(headerModel)
#         self.attributeTable.setHorizontalHeader(header)
 
        if len(layer.selectedFeatures ()) > 0:
            features = layer.selectedFeatures ()
        else:
            features = layer.getFeatures()
        for feature in features:
            record = [QStandardItem(str(feature.id()))]
            
            for field in feature.fields():
                name = field.name()
                attribute = feature.attribute(name).toString()
                  
                stdItemValue = QStandardItem(attribute)
                stdItemValue.setEditable(False)                  
                record.append(stdItemValue)
            self.model.appendRow(record)
    def deleteRows(self):
        if len(self.attributeTable.selectedIndexes()) > 0 :    
            self.isSave = False        
            selectedIndexs = self.attributeTable.selectedIndexes()
            k = -1
            self.selectRows = []
            for index in selectedIndexs:
                if k != index.row():
                    k = index.row()
                    self.selectRows.append(k)
            for row in self.selectRows:
                self.model.takeRow(row)
                
    def unselectAll(self):
        if len(self.attributeTable.selectedIndexes()) > 0 :
            self.attributeTable.clearSelection()
            
    def selectedToZoom(self):  
        if len(self.attributeTable.selectedIndexes()) > 0 :   
            self.baseLayer.removeSelection() 
                   
            selectedIndexs = self.attributeTable.selectedIndexes()
            k = -1
            self.selectRows = []
            for index in selectedIndexs:
                if k != index.row():
                    k = index.row()
                    self.selectRows.append(k)
            self.baseLayer.setSelectedFeatures(self.selectRows)
#             for row in self.selectRows:
#                 self.model.takeRow(row)
        define._canvas.zoomToSelected( self.baseLayer )
    
    def validate(self, condition):        
        if self.baseLayer.dataProvider().capabilities() & condition :
            return True
        else:
            return False            
                