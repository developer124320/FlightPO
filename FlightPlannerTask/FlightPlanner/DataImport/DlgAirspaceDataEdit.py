# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox
from PyQt4.QtCore import QString, QFileInfo
from PyQt4.QtCore import SIGNAL
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits, Distance


class DlgAirspaceDataEdit(QDialog):
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


        self.pnlLowerLimit = DistanceBoxPanel(self.frameBasic, DistanceUnits.M)
        self.pnlLowerLimit.Caption = "Lower Limit"
        self.pnlLowerLimit.Button = None
        self.pnlLowerLimit.LabelWidth = 120
        self.frameBasic.Add = self.pnlLowerLimit

        self.pnlUpperLimit = DistanceBoxPanel(self.frameBasic, DistanceUnits.M)
        self.pnlUpperLimit.Caption = "Upper Limit"
        self.pnlUpperLimit.Button = None
        self.pnlUpperLimit.LabelWidth = 120
        self.frameBasic.Add = self.pnlUpperLimit

        self.pnlRadius = DistanceBoxPanel(self.frameBasic, DistanceUnits.M)
        self.pnlRadius.Caption = "Radius"
        self.pnlRadius.Button = None
        self.pnlRadius.LabelWidth = 120
        self.frameBasic.Add = self.pnlRadius

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)


        self.name = ""
        self.lowerLimit = ""
        self.upperLimit = ""
        self.radius = ""


        if valueList != None:
            self.pnlName.Value = valueList[0]
            self.pnlLowerLimit.Value = Distance(float(valueList[1]))
            self.pnlUpperLimit.Value = Distance(float(valueList[2]))
            if valueList[3] != None and valueList[3] != "":
                self.pnlRadius.Value = Distance(float(valueList[3]))
    def acceptDlg(self):
        self.name = self.pnlName.Value
        self.lowerLimit = QString(str(self.pnlLowerLimit.Value.Metres))
        self.upperLimit = QString(str(self.pnlUpperLimit.Value.Metres))
        if self.pnlRadius.Value.Metres == 0:
            self.radius = QString("")
        else:
            self.radius = QString(str(self.pnlRadius.Value.Metres))
        self.accept()