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
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.PositionPanel import Point3D, PositionPanel
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits, Distance

from FlightPlanner.types import SymbolType


class DlgPointDataEdit(QDialog):
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

        self.pnlObstacle = PositionPanel(self.frameBasic, None, None, "Degree")
        self.pnlObstacle.btnCalculater.setVisible(False)
        self.frameBasic.Add = self.pnlObstacle

        self.pnlType = ComboBoxPanel(self.frameBasic)
        self.pnlType.Caption = "Type"
        self.pnlType.LabelWidth = 120
        self.frameBasic.Add = self.pnlType

        self.pnlRemarks = TextBoxPanel(self.frameBasic, True)
        self.pnlRemarks.Caption = "Remarks"
        self.pnlRemarks.LabelWidth = 120
        self.frameBasic.Add = self.pnlRemarks


        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)


        self.name = ""
        self.latitude = ""
        self.longitude = ""
        self.altitude = ""
        self.type = ""
        self.remarks = ""

        if title == "Add Symbol" or title == "Modify Symbol":
            self.pnlType.Items = [SymbolType.Default,
                                  SymbolType.Arp,
                                  SymbolType.Be1,
                                  SymbolType.Dme,
                                  SymbolType.Faf,
                                  SymbolType.Gp,
                                  SymbolType.Ndb,
                                  SymbolType.Repnc,
                                  SymbolType.Tacan,
                                  SymbolType.Vor,
                                  SymbolType.Vord]
        elif title == "Add Obstacle" or title == "Modify Obstacle":
            self.pnlType.Items = [SymbolType.Obst1,
                                  SymbolType.Obst2,
                                  SymbolType.Obst3,
                                  SymbolType.Obst4]

        self.editingFlag = False
        if valueList != None:
            self.pnlName.Value = valueList[0]
            self.pnlObstacle.Point3d = Point3D(float(valueList[2]), float(valueList[1]), float(valueList[3]))
            self.pnlType.Value = valueList[4]
            self.pnlRemarks.Value = valueList[5]

            self.editingFlag = True



    def acceptDlg(self):
        self.name = self.pnlName.Value
        self.latitude = QString(str(self.pnlObstacle.Point3d.get_Y()))
        self.longitude = QString(str(self.pnlObstacle.Point3d.get_X()))
        self.altitude = QString(str(self.pnlObstacle.Altitude().Metres))
        self.type = self.pnlType.SelectedItem
        self.remarks = self.pnlRemarks.Value
        self.accept()