# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QDialogButtonBox
from PyQt4.QtCore import  SIGNAL, Qt
from FlightPlanner.Panels.CheckedListBox import CheckedListBox



class DlgAerodromeSurfaces(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(290, 136)
        self.setWindowTitle("Surfaces")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"))

        self.lstSurfaces = CheckedListBox(self)
        verticalLayoutDlg.addWidget(self.lstSurfaces)

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"))
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.btnOK = self.btnBoxOkCancel.button(QDialogButtonBox.Ok)

        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)

        # self.btnOK.setEnabled(len(self.lstSurfaces.CheckedItems) > 0)
        # self.connect(self.lstSurfaces, SIGNAL("ItemCheck"), self.lstSurfaces_ItemCheck)

    def acceptDlg(self):
        if len(self.lstSurfaces.CheckedItems) == 0:
            self.reject()
        else:
            self.accept()
    def lstSurfaces_ItemCheck(self, standardItem):
        # if checkBoxObj == None:
        #     return
        count = len(self.lstSurfaces.CheckedItems)
        if (count == 0):
            self.btnOK.setEnabled(standardItem.checkState() == Qt.Checked)
            return
        if (count != 1):
            self.btnOK.setEnabled(True)
            return
        self.btnOK.setEnabled(standardItem.checkState() == Qt.Checked)

    def method_5(self, bool_0):
        for i in range(len(bool_0)):
            bool_0[i] = self.lstSurfaces.GetItemChecked(i)
        return bool_0
    def method_6(self):
        self.btnOK.setEnabled(len(self.lstSurfaces.CheckedItems) > 0)

    def set_Surfaces(self, strList):
        self.lstSurfaces.Clear()
        strArrays = strList
        for i in range(len(strArrays)):
            str0 = strArrays[i]
            self.lstSurfaces.Add(str0, True)
    Surfaces = property(None, set_Surfaces, None, None)

    @staticmethod
    def smethod_0(parent, string_0, bool_0):
        flag = False
        dlgAerodromeSurface = DlgAerodromeSurfaces(parent)
        dlgAerodromeSurface.Surfaces = string_0
        resultDlg = dlgAerodromeSurface.exec_()
        if (not resultDlg == 1):
            flag = False
        else:
            dlgAerodromeSurface.method_5(bool_0)
            flag = True
        return flag
    

