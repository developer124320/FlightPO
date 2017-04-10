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
from FlightPlanner.Panels.SpeedBoxPanel import SpeedBoxPanel, SpeedUnits, Speed
from FlightPlanner.Panels.AngleGradientBoxPanel import AngleGradientBoxPanel, AngleGradientSlopeUnits
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits, Distance
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel, Altitude
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.QgisHelper import QgisHelper

import  define

class Ui_RaceTrackAndHolding(object):
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

        self.gbPosition = GroupBox(Form)
        self.gbPosition.Caption = "Positions"
        self.gbPosition.layoutBoxPanel.setSpacing(9)
        self.vlForm.addWidget(self.gbPosition)

        self.gbNavAid = GroupBox(self.gbPosition)
        self.gbNavAid.Caption = "Navigational Aid"
        self.gbPosition.Add = self.gbNavAid

        self.cmbNavAidType = ComboBoxPanel(self.gbNavAid)
        self.cmbNavAidType.Caption = "Type"
        self.cmbNavAidType.Items = ["NDB", "NDB/DME", "VOR", "VOR/DME"]
        self.cmbNavAidType.LabelWidth = 140
        self.gbNavAid.Add = self.cmbNavAidType

        self.cmbBasedOn = ComboBoxPanel(self.gbNavAid, True)
        self.cmbBasedOn.Caption = "Based On"
        self.cmbBasedOn.LabelWidth = 140
        self.cmbBasedOn.Width = 121
        self.gbNavAid.Add = self.cmbBasedOn

        self.pnlNavAidPos = PositionPanel(self.gbNavAid)
        self.pnlNavAidPos.btnCalculater.hide()
        self.pnlNavAidPos.hideframe_Altitude()
        self.gbNavAid.Add = self.pnlNavAidPos

        self.pnlDmePos = PositionPanel(self.gbPosition)
        self.pnlDmePos.Caption = "DME Position"
        self.pnlDmePos.btnCalculater.hide()
        self.pnlDmePos.hideframe_Altitude()
        self.gbPosition.Add = self.pnlDmePos

        self.cmbEntry = ComboBoxPanel(self.gbPosition)
        self.cmbEntry.Caption = "Entry"
        self.cmbEntry.Items = ["Omnidirectional", "On Track"]
        self.cmbEntry.LabelWidth = 140
        self.gbPosition.Add = self.cmbEntry

        self.txtBearing = TrackRadialBoxPanel(self.gbPosition)
        self.txtBearing.Caption = "Outbound Track"
        self.txtBearing.LabelWidth = 140
        self.gbPosition.Add = self.txtBearing



        self.gbParameters = GroupBox(Form)
        self.gbParameters.Caption = "Parameters"
        self.gbParameters.layoutBoxPanel.setSpacing(9)
        self.vlForm.addWidget(self.gbParameters)

        self.cmbDirection = ComboBoxPanel(self.gbParameters)
        self.cmbDirection.Caption = "Turn Direction"
        self.cmbDirection.Items = ["Right", "Left"]
        self.cmbDirection.LabelWidth = 140
        self.cmbDirection.Width = 70
        self.gbParameters.Add = self.cmbDirection

        self.cmbAircraftCatgory = ComboBoxPanel(self.gbParameters)
        self.cmbAircraftCatgory.Caption = "Aircraft Category"
        self.cmbAircraftCatgory.Items = ["A", "B", "C", "D", "E"]
        self.cmbAircraftCatgory.LabelWidth = 140
        self.cmbAircraftCatgory.Width = 50
        self.gbParameters.Add = self.cmbAircraftCatgory

        self.cmbCondition = ComboBoxPanel(self.gbParameters)
        self.cmbCondition.Caption = "Condition"
        self.cmbCondition.Items = ["Normal Condition", "Turbulence Condition"]
        self.cmbCondition.LabelWidth = 140
        self.gbParameters.Add = self.cmbCondition

        self.txtNAVAlt = AltitudeBoxPanel(self.gbParameters)
        self.txtNAVAlt.CaptionUnits = "ft"
        self.txtNAVAlt.Caption = "NAV Altitude"
        self.txtNAVAlt.LabelWidth = 140
        self.gbParameters.Add = self.txtNAVAlt

        self.txtInitialAlt = AltitudeBoxPanel(self.gbParameters)
        self.txtInitialAlt.CaptionUnits = "ft"
        self.txtInitialAlt.Caption = "Initial Altitude"
        self.txtInitialAlt.LabelWidth = 140
        self.gbParameters.Add = self.txtInitialAlt

        self.txtTurnAlt = AltitudeBoxPanel(self.gbParameters)
        self.txtTurnAlt.CaptionUnits = "ft"
        self.txtTurnAlt.Caption = "Turn Altitude"
        self.txtTurnAlt.LabelWidth = 140
        self.gbParameters.Add = self.txtTurnAlt

        self.txtFinalAlt = AltitudeBoxPanel(self.gbParameters)
        self.txtFinalAlt.CaptionUnits = "ft"
        self.txtFinalAlt.Caption = "Final Altitude"
        self.txtFinalAlt.LabelWidth = 140
        self.gbParameters.Add = self.txtFinalAlt

        self.txtLimitDistance = DistanceBoxPanel(self.gbParameters, DistanceUnits.NM)
        self.txtLimitDistance.Caption = "Limiting Distance"
        self.txtLimitDistance.Button = None
        self.txtLimitDistance.LabelWidth = 140
        self.gbParameters.Add = self.txtLimitDistance

        self.txtOutboundTime = NumberBoxPanel(self.gbParameters )
        self.txtOutboundTime.Caption = "Outbound Time"
        self.txtOutboundTime.LabelWidth = 140
        self.gbParameters.Add = self.txtOutboundTime

        self.txtOutboundLeg = DistanceBoxPanel(self.gbParameters, DistanceUnits.NM)
        self.txtOutboundLeg.Caption = "Outbound Leg"
        self.txtOutboundLeg.Button = None
        self.txtOutboundLeg.LabelWidth = 140
        self.gbParameters.Add = self.txtOutboundLeg

        self.txtISA = NumberBoxPanel(self.gbParameters, "0.0")
        self.txtISA.CaptionUnits = define._degreeStr
        self.txtISA.Caption = "ISA"
        self.txtISA.LabelWidth = 140
        self.gbParameters.Add = self.txtISA

        self.txtIAS = SpeedBoxPanel(self.gbParameters, SpeedUnits.KTS)
        self.txtIAS.Caption = "IAS"
        self.txtIAS.LabelWidth = 140
        self.gbParameters.Add = self.txtIAS

        self.txtTAS = SpeedBoxPanel(self.gbParameters, SpeedUnits.KTS)
        self.txtTAS.Caption = "TAS"
        self.txtTAS.LabelWidth = 140
        self.gbParameters.Add = self.txtTAS









