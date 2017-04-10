# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HoldingRnav.ui'
#
# Created: Wed Nov 25 16:19:08 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtGui
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.CheckBox import CheckBox



class Ui_HeliportSurfacesAltitude(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setObjectName(("Ui_AerodromeSurfacesAltitude"))
        self.resize(473, 580)
        font = QtGui.QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)

        self.vlForm = QtGui.QVBoxLayout(self)
        self.vlForm.setObjectName(("vlForm"))
        self.vlForm.setSpacing(0)
        self.vlForm.setMargin(0)

        self.gbEvalParameters = GroupBox(self)
        self.gbEvalParameters.Caption = "Parameters"
        self.vlForm.addWidget(self.gbEvalParameters)

        self.chbOnlyPenetratingObstacles = CheckBox(self.gbEvalParameters)
        self.chbOnlyPenetratingObstacles.Caption = "Evaluate Only Penetrating Obstacles"
        self.gbEvalParameters.Add = self.chbOnlyPenetratingObstacles

        self.pnlInsertPointAndText = Frame(self.gbEvalParameters, "HL")
        self.gbEvalParameters.Add = self.pnlInsertPointAndText

        self.chbInsertPointAndText = CheckBox(self.pnlInsertPointAndText)
        self.chbInsertPointAndText.Caption = "Insert Point And Text"
        self.pnlInsertPointAndText.Add = self.chbInsertPointAndText

        self.pnlTextHeight = NumberBoxPanel(self.pnlInsertPointAndText)
        self.pnlTextHeight.Caption = "Text Height"
        self.pnlInsertPointAndText.Add = self.pnlTextHeight

        self.pnlEvalPosition = PositionPanel(self.gbEvalParameters)
        self.pnlEvalPosition.Caption = "Position"
        self.pnlEvalPosition.frameID.setVisible(True)
        self.pnlEvalPosition.btnCalculater.setVisible(False)
        self.gbEvalParameters.Add = self.pnlEvalPosition

        self.pnlEvalMode = ComboBoxPanel(self.gbEvalParameters)
        self.pnlEvalMode.Caption = "Mode"
        self.pnlEvalMode.LabelWidth = 70
        self.gbEvalParameters.Add = self.pnlEvalMode