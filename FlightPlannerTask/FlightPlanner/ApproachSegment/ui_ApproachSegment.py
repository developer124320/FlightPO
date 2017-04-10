# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HoldingRnav.ui'
#
# Created: Wed Nov 25 16:19:08 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.AngleGradientBoxPanel import AngleGradientBoxPanel, AngleGradientSlopeUnits
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits, Distance
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel, Altitude
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.QgisHelper import QgisHelper



class Ui_ApproachSegment(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(473, 580)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        Form.setFont(font)
        self.vlForm = QtGui.QVBoxLayout(Form)
        self.vlForm.setObjectName(("vlForm"))

        self.gbApproachSegmentType = GroupBox(Form)
        self.gbApproachSegmentType.Caption = "Approach Segment Type"
        self.vlForm.addWidget(self.gbApproachSegmentType)

        self.txtApproachSegmentType = TextBoxPanel(self.gbApproachSegmentType)
        self.txtApproachSegmentType.Caption = "Type"
        self.txtApproachSegmentType.textBox.setEnabled(False)
        self.txtApproachSegmentType.Button = "sort2.png"
        self.txtApproachSegmentType.Value = "Final Segment"
        self.txtApproachSegmentType.textBox.setMaximumWidth(10000000)
        self.txtApproachSegmentType.hLayoutBoxPanel.removeItem(self.txtApproachSegmentType.spacerItem)
        QtCore.QObject.connect(self.txtApproachSegmentType, QtCore.SIGNAL("Event_1"), self.txtApproachSegmentType_Event_1)
        self.gbApproachSegmentType.Add = self.txtApproachSegmentType

        self.gbPosition = GroupBox(Form)
        self.gbPosition.Caption = "Positions"
        self.gbPosition.layoutBoxPanel.setSpacing(9)
        self.vlForm.addWidget(self.gbPosition)

        self.gbNavAid = GroupBox(self.gbPosition)
        self.gbNavAid.Caption = "Navigational Aid"
        self.gbPosition.Add = self.gbNavAid

        self.cmbNavAidType = ComboBoxPanel(self.gbNavAid)
        self.cmbNavAidType.Caption = "Type"
        self.cmbNavAidType.Items = ["NDB", "VOR"]
        self.cmbNavAidType.LabelWidth = 120
        self.gbNavAid.Add = self.cmbNavAidType

        self.cmbBasedOn = ComboBoxPanel(self.gbNavAid, True)
        self.cmbBasedOn.Caption = "Based On"
        self.cmbBasedOn.LabelWidth = 120
        self.cmbBasedOn.Width = 120
        self.gbNavAid.Add = self.cmbBasedOn

        self.pnlNavAidPos = PositionPanel(self.gbNavAid)
        self.pnlNavAidPos.btnCalculater.hide()
        self.pnlNavAidPos.hideframe_Altitude()
        self.gbNavAid.Add = self.pnlNavAidPos

        self.pnlFafPos = PositionPanel(self.gbPosition)
        self.pnlFafPos.Caption = "FAF Position"
        self.pnlFafPos.btnCalculater.hide()
        self.gbPosition.Add = self.pnlFafPos

        self.pnlMaptPos = PositionPanel(self.gbPosition)
        self.pnlMaptPos.Caption = "MAPt Position"
        self.pnlMaptPos.btnCalculater.hide()
        self.gbPosition.Add = self.pnlMaptPos

        self.pnlDerPos = PositionPanel(self.gbPosition)
        self.pnlDerPos.Caption = "Approach THR Position"
        self.pnlDerPos.btnCalculater.hide()
        self.gbPosition.Add = self.pnlDerPos

        self.gbParameters = GroupBox(Form)
        self.gbParameters.Caption = "Parameters"
        self.gbParameters.layoutBoxPanel.setSpacing(9)
        self.vlForm.addWidget(self.gbParameters)

        self.cmbTurnDirection = ComboBoxPanel(self.gbParameters)
        self.cmbTurnDirection.Caption = "Turn Direction"
        self.cmbTurnDirection.Items = ["Left", "Right"]
        self.gbParameters.Add = self.cmbTurnDirection

        self.cmbAircraftCatgory = ComboBoxPanel(self.gbParameters)
        self.cmbAircraftCatgory.Caption = "Aircraft Category"
        self.cmbAircraftCatgory.Items = ["A/B", "C/D/E", "H"]
        self.gbParameters.Add = self.cmbAircraftCatgory

        self.gbJoin = GroupBox(self.gbParameters, "HL")
        self.gbJoin.Caption = "Join the intermediate segment"
        self.gbParameters.Add = self.gbJoin

        self.radioJoinYes = QtGui.QRadioButton(self.gbJoin)
        self.radioJoinYes.setText("Yes")
        self.radioJoinYes.setChecked(True)
        self.gbJoin.Add = self.radioJoinYes

        self.radioJoinNo = QtGui.QRadioButton(self.gbJoin)
        self.radioJoinNo.setText("No")
        self.gbJoin.Add = self.radioJoinNo

        self.pnlDistance = DistanceBoxPanel(self.gbParameters, DistanceUnits.NM)
        self.pnlDistance.Caption = "Distance FAF - MAPt"
        self.pnlDistance.Button = None
        self.gbParameters.Add = self.pnlDistance

        self.pnlGradient = AngleGradientBoxPanel(self.gbParameters)
        self.pnlGradient.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlGradient.Caption = "Descent Gradient"
        self.gbParameters.Add = self.pnlGradient

        self.approachMenu = QtGui.QMenu()

        self.finalCmd = QgisHelper.createAction(self.approachMenu, "Final Segment", self.menuFinalClick)
        self.approachMenu.addAction(self.finalCmd)

        self.intermediateMnu = QtGui.QMenu("Intermediate Approach Segment")
        self.approachMenu.addMenu(self.intermediateMnu)

        self.interStraightCmd = QgisHelper.createAction(self.intermediateMnu, "Intermediate Segment Straight", self.menuInterStrightClick)
        self.intermediateMnu.addAction(self.interStraightCmd)

        self.interWithIFCmd = QgisHelper.createAction(self.intermediateMnu, "Intermediate Segment With IF", self.menuInterWithIFClick)
        self.intermediateMnu.addAction(self.interWithIFCmd)

        self.interWithNoIFCmd = QgisHelper.createAction(self.intermediateMnu, "Intermediate Segment With No IF", self.menuInterWithNoIFClick)
        self.intermediateMnu.addAction(self.interWithNoIFCmd)

        self.initialMnu = QtGui.QMenu("Initial Approach Segment")
        self.approachMenu.addMenu(self.initialMnu)

        self.initialStraigtCmd = QgisHelper.createAction(self.initialMnu, "Initial Segment Straight", self.menuInitialStrightClick)
        self.initialMnu.addAction(self.initialStraigtCmd)

        self.initialDMEArcCmd = QgisHelper.createAction(self.initialMnu, "Initial Segment DME ARCS", self.menuInitialDMEArcClick)
        self.initialMnu.addAction(self.initialDMEArcCmd)

    def txtApproachSegmentType_Event_1(self):
        rcRect = self.txtApproachSegmentType.imageButton.geometry()
        ptPoint = rcRect.bottomLeft()
        self.approachMenu.exec_(self.txtApproachSegmentType.mapToGlobal(ptPoint))
    def menuFinalClick(self):
        self.txtApproachSegmentType.Value = "Final Segment"
        self.pnlDistance.Caption = "Distance FAF - MAPt"
        self.gbNavAid.Caption = "Navigational Aid"
        self.pnlDerPos.Caption = "Approach THR Position"
        self.pnlFafPos.Caption = "FAF Position"
        self.pnlMaptPos.Caption = "MAPt Position"
        self.pnlDerPos.frameAltitude.setVisible(True)
        self.cmbNavAidType.Visible = True
        self.cmbBasedOn.Value = True
        # self.cmbRwyDir.Visible = True
    def menuInterStrightClick(self):
        self.txtApproachSegmentType.Value = "Intermediate Segment Straight"
        self.pnlFafPos.Caption = "IF Position"
        self.pnlMaptPos.Caption = "FAF Position"
        self.pnlDerPos.Caption = "MApt Position"
        self.pnlDerPos.hideframe_Altitude()
        self.pnlDistance.Caption = "Distance IF - FAF"
        self.gbNavAid.Caption = "Navigational Aid"
        self.cmbNavAidType.Visible = True
        self.cmbBasedOn.Value = True
        # self.cmbRwyDir.Visible = True
    def menuInterWithIFClick(self):
        self.txtApproachSegmentType.Value = "Intermediate Segment With IF"

        self.pnlFafPos.Caption = "IF Position"
        self.pnlMaptPos.Caption = "FAF Position"
        self.pnlDerPos.Caption = "MApt Position"
        self.pnlDerPos.hideframe_Altitude()
        self.pnlDistance.Caption = "Distance IF - FAF"
        self.gbNavAid.Caption = "Navigational Aid"
        self.cmbNavAidType.Visible = True
        self.cmbBasedOn.Value = True
        # self.cmbRwyDir.Visible = True
    def menuInterWithNoIFClick(self):
        self.txtApproachSegmentType.Value = "Intermediate Segment With No IF"

        self.pnlFafPos.Caption = "Start Position"
        self.pnlMaptPos.Caption = "FAF Position"
        self.pnlDerPos.Caption = "MApt Position"
        self.pnlDerPos.hideframe_Altitude()
        self.pnlDistance.Caption = "Distance Start - FAF"
        self.gbNavAid.Caption = "Navigational Aid"
        self.cmbNavAidType.Visible = True
        self.cmbBasedOn.Value = True
        # self.cmbRwyDir.Visible = True
    def menuInitialStrightClick(self):
        self.txtApproachSegmentType.Value = "Initial Segment Straight"

        self.pnlFafPos.Caption = "IAF Position"
        self.pnlMaptPos.Caption = "IF Position"
        self.pnlDerPos.Caption = "FAF Position"
        self.pnlDerPos.hideframe_Altitude()
        self.pnlDistance.Caption = "Distance IAF - IF"
        self.gbNavAid.Caption = "Navigational Aid"
        self.cmbNavAidType.Visible = True
        self.cmbBasedOn.Value = True
        # self.cmbRwyDir.Visible = True
    def menuInitialDMEArcClick(self):
        self.txtApproachSegmentType.Value = "Initial Segment DME ARCS"

        self.pnlFafPos.Caption = "IAF Position"
        self.pnlMaptPos.Caption = "IF Position"
        self.pnlDerPos.Caption = "FAF Position"
        self.pnlDerPos.hideframe_Altitude()
        self.pnlDistance.Caption = "Distance IAF - IF"
        self.gbNavAid.Caption = "DME Position"
        self.cmbNavAidType.Visible = False
        self.cmbBasedOn.Value = False
        # self.cmbRwyDir.Visible = False





