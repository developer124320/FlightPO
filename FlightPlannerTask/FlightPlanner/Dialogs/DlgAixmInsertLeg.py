# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QMessageBox, QDialogButtonBox, QRadioButton

from PyQt4.QtCore import  SIGNAL
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.types import ListInsertPosition, CodeTypeDesigPtAixm, DegreesType
from FlightPlanner.validations import Validations
from Type.Degrees import Degrees
from Type.ProcEntity import ProcEntityDPN



class DlgAixmInsertLeg(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(290, 136);
        self.setWindowTitle("Insert Leg")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth());
        self.setSizePolicy(sizePolicy);
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"));

        self.groupBox = GroupBox(self)
        verticalLayoutDlg.addWidget(self.groupBox)

        self.optBefore = QRadioButton(self.groupBox)
        self.optBefore.setObjectName("optBefore")
        self.optBefore.setText("Insert Before")
        self.groupBox.Add = self.optBefore

        self.optAfter = QRadioButton(self.groupBox)
        self.optAfter.setObjectName("optAfter")
        self.optAfter.setText("Insert After")
        self.groupBox.Add = self.optAfter

        self.optAppend = QRadioButton(self.groupBox)
        self.optAppend.setObjectName("optAppend")
        self.optAppend.setText("Append")
        self.groupBox.Add = self.optAppend

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        # btnOK = self.btnBoxOkCancel.button(QDialogButtonBox.Ok)
        # btnOK.setText("Create")
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)



    def acceptDlg(self):
        self.accept()

    @staticmethod
    def smethod_0(listInsertPosition_0):
        flag = False;
        dlgAixmInsertLeg = DlgAixmInsertLeg()
        if (listInsertPosition_0 == ListInsertPosition.Before):
            dlgAixmInsertLeg.optBefore.setChecked(True);
        elif (listInsertPosition_0 != ListInsertPosition.After):
            dlgAixmInsertLeg.optAppend.setChecked(True)
        else:
            dlgAixmInsertLeg.optAfter.setChecked(True)
        resultDlg = dlgAixmInsertLeg.exec_()
        if (resultDlg != 1):
            flag = False;
        else:
            if (dlgAixmInsertLeg.optBefore.isChecked()):
                listInsertPosition_0 = ListInsertPosition.Before;
            elif (not dlgAixmInsertLeg.optAfter.isChecked()):
                listInsertPosition_0 = ListInsertPosition.Append;
            else:
                listInsertPosition_0 = ListInsertPosition.After;
            flag = True;
        return flag, listInsertPosition_0;