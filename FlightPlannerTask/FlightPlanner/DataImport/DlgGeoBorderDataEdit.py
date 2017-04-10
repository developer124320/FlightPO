# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox
from PyQt4.QtCore import QString, QFileInfo
from PyQt4.QtCore import SIGNAL
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits, Distance


class DlgGeoBorderDataEdit(QDialog):
    def __init__(self, parent, title, valueList = None):
        QDialog.__init__(self, parent)
        
        self.resize(100, 70);
        self.setWindowTitle(title)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth());
        self.setSizePolicy(sizePolicy);
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"));

        self.frameBasic = Frame(self)
        verticalLayoutDlg.addWidget(self.frameBasic)

        self.pnlName = TextBoxPanel(self.frameBasic)
        self.pnlName.Caption = "Name"
        self.pnlName.LabelWidth = 120
        self.frameBasic.Add = self.pnlName

        self.pnlType = ComboBoxPanel(self.frameBasic)
        self.pnlType.Caption = "Type"
        self.pnlType.LabelWidth = 120
        self.frameBasic.Add = self.pnlType


        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)


        self.name = ""
        self.type = ""
        self.pnlType.Items = ["ST", "TW", "CS", "RW", "RB", "OTHER"]
        if valueList != None:
            self.pnlName.Value = valueList[0]
            self.pnlType.Value = valueList[1]
    def acceptDlg(self):
        self.name = self.pnlName.Value
        self.type = self.pnlType.SelectedItem
        self.accept()