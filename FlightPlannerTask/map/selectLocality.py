# -*- coding: utf-8 -*-
"""
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.gui import *
from qgis.core import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.utils import iface
# from qgis.utils import*

class SelectLocality(QDialog):

    def __init__(self, layer):
        '''
        Constructor
        '''
        self.cellsize=2.0
        QDialog.__init__(self)
        self.resize(359, 439)
        self.setFixedWidth(359)
        self.setFixedHeight(439)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(0, 400, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QGroupBox(self)
        self.groupBox.setGeometry(QRect(10, 10, 341, 381))
        self.groupBox.setObjectName("groupBox")
        
        self.tableViewOld = QTableView(self.groupBox)
        self.tableViewOld.setGeometry(QRect(10, 20, 155, 311))
        self.tableViewOld.setObjectName("tableViewOld")
        
        self.tableViewNew = QTableView(self.groupBox)
        self.tableViewNew.setGeometry(QRect(175, 20, 155, 311))
        self.tableViewNew.setObjectName("tableViewNew")
        
        self.btSortAscending = QPushButton(self.groupBox)
        self.btSortAscending.setGeometry(QRect(10, 340, 32, 32))
        self.btSortAscending.setText("")
        icon = QIcon("Resource/sort1.png")
        #icon.addPixmap(QPixmap("Resource/sort1.png"), QIcon.Normal, QIcon.Off)
        self.btSortAscending.setIcon(icon)
        self.btSortAscending.setObjectName("btSortAscending")
        self.btSortDescending = QPushButton(self.groupBox)
        self.btSortDescending.setGeometry(QRect(60, 340, 32, 32))
        self.btSortDescending.setText("")
        icon1 = QIcon("Resource/sort2.png")
        #icon1.addPixmap(QPixmap("Resource/sort2.png"), QIcon.Normal, QIcon.Off)
        self.btSortDescending.setIcon(icon1)
        self.btSortDescending.setObjectName("btSortDescending")
        self.btAdd = QPushButton(self.groupBox)
        self.btAdd.setGeometry(QRect(110, 340, 32, 32))
        self.btAdd.setText("")
        icon2 = QIcon("Resource/add.png")
        #icon2.addPixmap(QPixmap("Resource/add.png"), QIcon.Normal, QIcon.Off)
        self.btAdd.setIcon(icon2)
        self.btAdd.setIconSize(QSize(31, 23))
        self.btAdd.setObjectName("btAdd")
        self.btRemove = QPushButton(self.groupBox)
        self.btRemove.setGeometry(QRect(160, 340, 32, 32))
        self.btRemove.setText("")
        icon3 = QIcon("Resource/remove.png")
        #icon3.addPixmap(QPixmap("Resource/remove.png"), QIcon.Normal, QIcon.Off)
        self.btRemove.setIcon(icon3)
        self.btRemove.setObjectName("btRemove")
        self.btReset = QPushButton(self.groupBox)
        self.btReset.setGeometry(QRect(210, 340, 61, 31))
        self.btReset.setObjectName("btReset")
        self.setWindowTitle("Select attributes")
        self.groupBox.setTitle("Columns")
        self.btReset.setText("Reset")
        
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        QMetaObject.connectSlotsByName(self)
        
       
        self.standardItemModelOld=QStandardItemModel()
        self.standardItemModelNew=QStandardItemModel()
        self.tableViewOld.setModel(self.standardItemModelOld)
        self.tableViewNew.setModel(self.standardItemModelNew)
        
        headerOld = QHeaderView(Qt.Horizontal)
        headerNew = QHeaderView(Qt.Horizontal)
        
        headersListOld = [] 
        headersListNew = [] 
        headersListOld.append("All layers")   
        headersListNew.append("Selected layers")
                
        self.standardItemModelOld.setHorizontalHeaderLabels(headersListOld)
        headerOld.setModel(self.standardItemModelOld)
        self.tableViewOld.setHorizontalHeader(headerOld)
        
        self.standardItemModelNew.setHorizontalHeaderLabels(headersListNew)
        headerNew.setModel(self.standardItemModelNew)
        self.tableViewNew.setHorizontalHeader(headerNew)
        rowIndex = 0
        features = layer.getFeatures()
        self.AllRecord = []
        record = []
        for feature in features:
            
            attribute = feature.attribute("GAZETTEER").toString()
            fID = str(feature.id())     
                 
            stdItemValue = QStandardItem(attribute)
            stdItemValue.setEditable(False)
            stdItemIDValue = QStandardItem(fID)
            stdItemIDValue.setEditable(False)
            self.standardItemModelOld.setItem(rowIndex, 0, stdItemIDValue)
            self.standardItemModelOld.setItem(rowIndex, 1, stdItemValue)
            rowIndex += 1
            record = [stdItemIDValue, stdItemValue]
            self.AllRecord.append(record)
                 
            #self.column.append(stdItemValue)
            #self.standardItemModelOld.appendRow(record)
           
        #self.standardItemModelOld.clicked.connect(self.standardItemModelOldClicked)
        #self.tableViewOld.clicked.connect(self.tableViewOldClicked)
        self.connect(self.tableViewOld , SIGNAL("clicked(QModelIndex)"), self.tableViewOldClicked)
        self.connect(self.tableViewNew , SIGNAL("clicked(QModelIndex)"), self.tableViewNewClicked)
        #self.standardItemModelNew.itemChanged.connect(self.standardItemModelNewClicked)
        self.btReset.clicked.connect(self.btResetClicked)
        self.btAdd.clicked.connect(self.btAddClicked)
        self.btRemove.clicked.connect(self.btRemoveClicked)
        self.btSortAscending.clicked.connect(self.btSortAscendingClicked)
        self.btSortDescending.clicked.connect(self.btSortDescendingClicked)
        
        self.stdItemOld = None
        self.stdItemNew = None
        
    def tableViewOldClicked(self, modelIndex):
        
        #aa=len(self.AllRecord)
        self.rowNumberOld = modelIndex.row()
        self.stdItemOld = QStandardItem(self.standardItemModelOld.itemFromIndex(modelIndex).text())
        
    def tableViewNewClicked(self, modelIndex):
        self.rowNumberNew = modelIndex.row()
        self.stdItemNew = QStandardItem(self.standardItemModelNew.itemFromIndex(modelIndex).text())
        
    def btResetClicked(self):
        rowCountNew = self.standardItemModelNew.rowCount()
        #self.standardItemModelNew.removeRows(0, self.standardItemModelNew.rowCount())
        #rowIndex = 0
        for rowNum in range(self.standardItemModelOld.rowCount()):            
            
            itemID = QStandardItem(self.standardItemModelOld.item(rowNum, 0).text())
            item = QStandardItem(self.standardItemModelOld.item(rowNum, 1).text())
            self.standardItemModelNew.setItem(rowCountNew + rowNum, 0, itemID)
            self.standardItemModelNew.setItem(rowCountNew + rowNum, 1, item)
            
            #stdItemValue = column0
            #aa= stdItemValue.text()
            #stdItemValue.setEditable(False)
            #self.standardItemModelNew.appendRow(stdItemValue)
        self.standardItemModelOld.removeRows(0, self.standardItemModelOld.rowCount())
    def btAddClicked(self):
        if self.stdItemOld == None:
            return
        stdItemIDValue = self.standardItemModelOld.takeRow(self.rowNumberOld)
        self.standardItemModelNew.appendRow(stdItemIDValue)
        self.stdItemOld = None
    def btRemoveClicked(self):
        if self.stdItemNew == None:
            return        
        stdItemIDValue = self.standardItemModelNew.takeRow(self.rowNumberNew)
        self.standardItemModelOld.appendRow(stdItemIDValue)
        self.stdItemNew = None
    def btSortAscendingClicked(self):
        self.standardItemModelOld.sort(1, Qt.AscendingOrder)
        self.standardItemModelNew.sort(1, Qt.AscendingOrder)
    def btSortDescendingClicked(self):
        self.standardItemModelOld.sort(1, Qt.DescendingOrder)
        self.standardItemModelNew.sort(1, Qt.DescendingOrder)
    def popPointData(self):
        data = []
        pointData = []
        for rowNum in range(self.standardItemModelNew.rowCount()):            
            
            data = [self.standardItemModelNew.item(rowNum, 0).text(), self.standardItemModelNew.item(rowNum, 1).text()]
            pointData.append(data)
        return pointData
        
        
        
        

    
   