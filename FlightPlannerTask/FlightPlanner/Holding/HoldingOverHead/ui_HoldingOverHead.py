# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HoldingOverHead.ui'
#
# Created: Wed Nov 25 16:24:07 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FlightPlanner.types import AltitudeUnits
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.SpeedBoxPanel import SpeedBoxPanel, Speed, SpeedUnits
from FlightPlanner.Panels.AltitudeBoxPanel import Altitude, AltitudeBoxPanel
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.WindPanel import WindPanel
from FlightPlanner.Panels.CheckBox import CheckBox

import define

class Ui_HoldingOverHead(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(467, 464)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")

        self.gbNavAid = GroupBox(Form)
        self.gbNavAid.Caption = "Navigational Aid"
        self.verticalLayout.addWidget(self.gbNavAid)

        self.cmbNavAidType = ComboBoxPanel(self.gbNavAid)
        self.cmbNavAidType.Caption = "Type"
        self.cmbNavAidType.LabelWidth = 120
        self.gbNavAid.Add = self.cmbNavAidType

        self.cmbBasedOn = ComboBoxPanel(self.gbNavAid, True)
        self.cmbBasedOn.Caption = "Based On"
        self.cmbBasedOn.LabelWidth = 120
        self.cmbBasedOn.Width = 120
        self.gbNavAid.Add = self.cmbBasedOn

        self.pnlNavAid = PositionPanel(self.gbNavAid)
        self.pnlNavAid.btnCalculater.hide()
        self.pnlNavAid.setObjectName("pnlNavAid")
        self.gbNavAid.Add = self.pnlNavAid

        self.gbParameters = GroupBox(Form)
        self.gbParameters.Caption = "Parameters"
        self.verticalLayout.addWidget(self.gbParameters)

        self.cmbUsedFor = ComboBoxPanel(self.gbParameters)
        self.cmbUsedFor.Caption = "Type"
        self.cmbUsedFor.LabelWidth = 120
        self.gbParameters.Add = self.cmbUsedFor

        self.txtIas = SpeedBoxPanel(self.gbParameters, SpeedUnits.KTS)
        self.txtIas.Caption = "IAS"
        self.txtIas.Value = Speed(250)
        self.txtIas.LabelWidth = 120
        self.gbParameters.Add = self.txtIas

        self.txtTas = SpeedBoxPanel(self.gbParameters, SpeedUnits.KTS)
        self.txtTas.Caption = "TAS"
        self.txtTas.LabelWidth = 120
        self.txtTas.Enabled = False
        self.gbParameters.Add = self.txtTas

        self.txtAltitude = AltitudeBoxPanel(self.gbParameters)
        self.txtAltitude.CaptionUnits = "ft"
        self.txtAltitude.Caption = "Altitude"
        self.txtAltitude.Value = Altitude(10000, AltitudeUnits.FT)
        self.txtAltitude.LabelWidth = 120
        self.gbParameters.Add = self.txtAltitude


        self.txtIsa = NumberBoxPanel(self.gbParameters, "0.0")
        self.txtIsa.CaptionUnits = define._degreeStr
        self.txtIsa.Caption = "ISA"
        self.txtIsa.Value = 15
        self.txtIsa.LabelWidth = 120
        self.gbParameters.Add = self.txtIsa

        self.pnlWind = WindPanel(self.gbParameters)
        self.pnlWind.lblIA.setMinimumSize(113, 0)
        self.gbParameters.Add = self.pnlWind

        self.txtTime = NumberBoxPanel(self.gbParameters, "0.0")
        self.txtTime.CaptionUnits = "min"
        self.txtTime.Caption = "Time"
        self.txtTime.Value = 1
        self.txtTime.LabelWidth = 120
        self.gbParameters.Add = self.txtTime

        self.txtMoc = AltitudeBoxPanel(self.gbParameters)
        self.txtMoc.CaptionUnits = "m"
        self.txtMoc.Caption = "Moc"
        self.txtMoc.Value = Altitude(300)
        self.txtMoc.LabelWidth = 120
        self.gbParameters.Add = self.txtMoc


        self.chbCatH = CheckBox(self.gbParameters)
        self.chbCatH.Caption = "Cat. H ( linear MOC reduction up to 2NM )"
        self.gbParameters.Add = self.chbCatH

        self.gbEntryAreas = GroupBox(self.gbParameters, "HL")
        self.gbEntryAreas.Caption = "Entry Areas"
        self.gbParameters.Add = self.gbEntryAreas

        self.chbIntercept = CheckBox(self.gbEntryAreas)
        self.chbIntercept.Caption = "Intercept"
        self.gbEntryAreas.Add = self.chbIntercept

        self.chbSector1 = CheckBox(self.gbEntryAreas)
        self.chbSector1.Caption = "Sector 1"
        self.gbEntryAreas.Add = self.chbSector1

        self.chbSector2 = CheckBox(self.gbEntryAreas)
        self.chbSector2.Caption = "Sector 2"
        self.gbEntryAreas.Add = self.chbSector2

        self.chbSectors12 = CheckBox(self.gbEntryAreas)
        self.chbSectors12.Caption = "Sectors 1 & 2"
        self.gbEntryAreas.Add = self.chbSectors12

        self.chbSector3 = CheckBox(self.gbEntryAreas)
        self.chbSector3.Caption = "Sectors 3"
        self.gbEntryAreas.Add = self.chbSector3

        self.cmbConstruction = ComboBoxPanel(self.gbParameters)
        self.cmbConstruction.Caption = "Construction Type"
        self.cmbConstruction.LabelWidth = 120
        self.cmbConstruction.Width = 50
        self.gbParameters.Add = self.cmbConstruction

        self.mocSpinBox = NumberBoxPanel(self.gbParameters, None)
        self.mocSpinBox.Caption = "MOCmultiplier"
        self.mocSpinBox.LabelWidth = 120
        self.mocSpinBox.Value = 1
        self.mocSpinBox.Width = 50
        self.gbParameters.Add = self.mocSpinBox

        self.gbOrientation = GroupBox(Form)
        self.gbOrientation.Caption = "Orientation"
        self.verticalLayout.addWidget(self.gbOrientation)

        self.txtTrack = TrackRadialBoxPanel(self.gbOrientation)
        self.txtTrack.Caption = "In-bound Track"
        self.txtTrack.LabelWidth = 120
        self.gbOrientation.Add = self.txtTrack

        self.cmbOrientation = ComboBoxPanel(self.gbOrientation)
        self.cmbOrientation.Caption = "Turns"
        self.cmbOrientation.LabelWidth = 120
        self.gbOrientation.Add = self.cmbOrientation

        QtCore.QMetaObject.connectSlotsByName(Form)

