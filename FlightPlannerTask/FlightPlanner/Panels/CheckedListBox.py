# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QCheckBox, QWidget, QHBoxLayout, QSizePolicy, QDialog, QListView, QStandardItem, QStandardItemModel
from PyQt4.QtCore import SIGNAL, QSize, QString, Qt

from FlightPlanner.Panels.Frame import Frame

class CheckedListBox(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("CheckedListBox" + str(len(parent.findChildren(CheckedListBox))))

        self.setObjectName("checkBoxWidget")
        self.hLayout = QHBoxLayout(self)
        self.hLayout.setObjectName("hLayout")

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        # self.frame = Frame()
        self.listView = QListView(self)
        self.hLayout.addWidget(self.listView)

        self.stdModel = QStandardItemModel()
        self.listView.setModel(self.stdModel)

        self.hasObject = False
        self.objList = []

        self.checkBoxList = []

        self.listView.pressed.connect(self.listView_clicked)
    def listView_clicked(self, index):
        self.emit(SIGNAL("ItemCheck"), self.stdModel.itemFromIndex(index))
    def mouseMoveEvent(self, mouseEvent):
        pt = mouseEvent.pos()
        pass
    def Clear(self):
        self.stdModel.clear()
        self.hasObject = False
        self.objList = []
    def Add(self, caption, isCheckedFlag = False):
        captionStr = ""
        if isinstance(caption, str) or isinstance(caption, QString):
            captionStr = caption
        else:
            captionStr = caption.ToString()
            self.hasObject = True
            self.objList.append([self.stdModel.rowCount(), caption])
        item = QStandardItem(captionStr)
        item.setCheckable(True)
        if isCheckedFlag:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)
        self.stdModel.setItem(self.stdModel.rowCount(), item)

        # checkBox = QCheckBox(self)
        # checkBox.setText(captionStr)
        # checkBox.setChecked(isCheckedFlag)
        # checkBox.clicked.connect(self.checkBox_clicked)
        # self.hLayout.addWidget(checkBox)


    def GetItemChecked(self, index):
        if self.stdModel.rowCount() > 0:
            item = self.stdModel.item(index)
            if item.checkState() == Qt.Unchecked:
                return False
            return True
        return False

    def get_CheckedItems(self):
        if not self.stdModel.rowCount() > 0:
            return []
        resultCheckedItems = []
        for i in range(self.stdModel.rowCount()):
            item = self.stdModel.item(i)
            if item.checkState() == Qt.Checked:
                flag = False
                if self.hasObject:
                    for obj in self.objList:
                        if obj[0] == i:
                            resultCheckedItems.append(obj)
                            flag = True
                            break
                if not flag:
                    resultCheckedItems.append(item)
        return resultCheckedItems
    CheckedItems = property(get_CheckedItems, None, None, None)

    def get_Items(self):
        if not self.stdModel.rowCount() > 0:
            return None
        resultItems = []
        for i in range(self.stdModel.rowCount()):
            item = self.stdModel.item(i)
            flag = False
            if self.hasObject:
                for obj in self.objList:
                    if obj[0] == i:
                        resultItems.append(obj)
                        flag = True
                        break
            if not flag:
                resultItems.append(item.text())
        return resultItems
    Items = property(get_Items, None, None, None)






    def get_Enabled(self):
        return self.isEnabled()
    def set_Enabled(self, bool):
        self.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)

    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)
    #
    # def get_Checked(self):
    #     return self.checkBox.isChecked()
    # def set_Checked(elf, bool):
    #     self.checkBox.setChecked(bool)
    # Checked = property(get_Checked, set_Checked, None, None)
    #
    # def set_LabelWidth(self, width):
    #     self.checkBox.setMinimumSize(QSize(width, 0))
    #     self.checkBox.setMaximumSize(QSize(width, 16777215))
    # LabelWidth = property(None, set_LabelWidth, None, None)