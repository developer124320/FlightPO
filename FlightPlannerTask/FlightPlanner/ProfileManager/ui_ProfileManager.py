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
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits, Distance
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel, Altitude
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame



class Ui_ProfileManager(object):
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

        self.gbBaseLine = GroupBox(Form)
        self.gbBaseLine.Title = "Base Line"
        self.vlForm.addWidget(self.gbBaseLine)

        self.pnlBasePoint = PositionPanel(self.gbBaseLine)
        self.pnlBasePoint.btnCalculater.hide()
        self.pnlBasePoint.hideframe_Altitude()
        self.gbBaseLine.Add = self.pnlBasePoint

        self.pnlBaseAltitude = AltitudeBoxPanel(self.gbBaseLine)
        self.pnlBaseAltitude.CaptionUnits = "m"
        self.pnlBaseAltitude.Caption = "Altitude"
        self.pnlBaseAltitude.Value = Altitude(0)
        self.gbBaseLine.Add = self.pnlBaseAltitude

        self.cmbBaseOrientation = ComboBoxPanel(self.gbBaseLine)
        self.cmbBaseOrientation.Caption = "Orientation"
        self.gbBaseLine.Add = self.cmbBaseOrientation

        self.gbParameters = GroupBox(Form)
        self.gbParameters.Caption = "Parameters"
        self.gbParameters.layoutBoxPanel.setSpacing(9)
        self.vlForm.addWidget(self.gbParameters)

        self.pnlMode = ComboBoxPanel(self.gbParameters)
        self.pnlMode.Caption = "Mode (Obstacle Input)"
        self.gbParameters.Add = self.pnlMode

        self.pnlUsedFor = ComboBoxPanel(self.gbParameters)
        self.pnlUsedFor.Caption = "Used For"
        self.gbParameters.Add = self.pnlUsedFor

        self.pnlPDG = NumberBoxPanel(self.gbParameters)
        self.pnlPDG.CaptionUnits = "%"
        self.pnlPDG.Caption = "PDG"
        self.pnlPDG.Value = 3.3
        self.gbParameters.Add = self.pnlPDG

        self.pnlMOC = NumberBoxPanel(self.gbParameters)
        self.pnlMOC.CaptionUnits = "%"
        self.pnlMOC.Caption = "MOC"
        self.pnlMOC.Value = 0.8
        self.gbParameters.Add = self.pnlMOC

        self.pnlGP = NumberBoxPanel(self.gbParameters)
        self.pnlGP.CaptionUnits = "degree"
        self.pnlGP.Caption = "GP"
        self.pnlGP.Value = 3
        self.gbParameters.Add = self.pnlGP

        self.pnlRDH = AltitudeBoxPanel(self.gbParameters)
        self.pnlRDH.CaptionUnits = "m"
        self.pnlRDH.Caption = "RDH"
        self.pnlRDH.Value = Altitude(15)
        self.gbParameters.Add = self.pnlRDH

        self.gbConstruction = GroupBox(self.gbParameters)
        self.gbConstruction.layoutBoxPanel.setSpacing(9)
        self.gbConstruction.Caption = "Construction"
        self.gbParameters.Add = self.gbConstruction

        self.pnlLength = DistanceBoxPanel(self.gbConstruction, DistanceUnits.NM)
        self.pnlLength.Caption = "Length"
        self.pnlLength.Value = Distance(10, DistanceUnits.NM)
        self.gbConstruction.Add = self.pnlLength

        self.gbCustom = GroupBox(self.gbConstruction)
        self.gbCustom.Caption = "Custom Distance / Text"
        self.gbConstruction.Add = self.gbCustom

        p1 = Frame(self.gbCustom, "HL")
        self.gbCustom.Add = p1

        self.txtDist1 = DistanceBoxPanel(p1, DistanceUnits.NM)
        self.txtDist1.Caption = "Distance"
        self.txtDist1.Value = Distance(0, DistanceUnits.NM)
        self.txtDist1.Button = None
        p1.Add = self.txtDist1

        self.txtDist2 = DistanceBoxPanel(p1, DistanceUnits.NM)
        self.txtDist2.LabelWidth = 0
        self.txtDist2.Value = Distance(0, DistanceUnits.NM)
        self.txtDist2.Button = None
        p1.Add = self.txtDist2

        self.txtDist3 = DistanceBoxPanel(p1, DistanceUnits.NM)
        self.txtDist3.LabelWidth = 0
        self.txtDist3.Value = Distance(0, DistanceUnits.NM)
        self.txtDist3.Button = None
        p1.Add = self.txtDist3

        p2 = Frame(self.gbCustom, "HL")
        self.gbCustom.Add = p2

        self.txtText1 = TextBoxPanel(p2)
        self.txtText1.Caption = "Text"
        # self.txtText1.Value = "ABC"
        p2.Add = self.txtText1

        self.txtText2 = TextBoxPanel(p2)
        self.txtText2.LabelWidth = 0
        p2.Add = self.txtText2

        self.txtText3 = TextBoxPanel(p2)
        self.txtText3.LabelWidth = 0
        p2.Add = self.txtText3

        self.chbMarkDistances = QtGui.QCheckBox(self.gbConstruction)
        self.chbMarkDistances.setText("Mark Standard Distances")
        self.gbConstruction.Add = self.chbMarkDistances

        self.pnlThrDer = PositionPanel(self.gbParameters)
        self.pnlThrDer.Caption = "THR/DER Position"
        self.pnlThrDer.btnCalculater.hide()
        self.pnlThrDer.hideframe_Altitude()
        self.gbParameters.Add = self.pnlThrDer

        self.pnlOutbound = TrackRadialBoxPanel(self.gbParameters)
        self.pnlOutbound.Caption = "Outbound Track"
        self.gbParameters.Add = self.pnlOutbound

        self.pnlEtp = PositionPanel(self.gbParameters)
        self.pnlEtp.Caption = "ETP Position"
        self.pnlEtp.btnCalculater.hide()
        self.pnlEtp.hideframe_Altitude()
        self.gbParameters.Add = self.pnlEtp

        self.pnlHASP = AltitudeBoxPanel(self.gbParameters)
        self.pnlHASP.CaptionUnits = "m"
        self.pnlHASP.Value = Altitude(5)
        self.pnlHASP.Caption = "Height Above Start Point"
        self.gbParameters.Add = self.pnlHASP

        self.pnlTA = AltitudeBoxPanel(self.gbParameters)
        self.pnlTA.CaptionUnits = "m"
        self.pnlTA.Value = Altitude(300)
        self.pnlTA.Caption = "Turning Altitude"
        self.gbParameters.Add = self.pnlTA

        self.pnlClimbGradient = NumberBoxPanel(self.gbParameters)
        self.pnlClimbGradient.CaptionUnits = "%"
        self.pnlClimbGradient.Value = 3.3
        self.pnlClimbGradient.Caption = "Climb-out Gradient"
        self.gbParameters.Add = self.pnlClimbGradient

        self.chbMarkTA = QtGui.QCheckBox(self.gbParameters)
        self.chbMarkTA.setText("Mark Turning Altitude")
        self.gbParameters.Add = self.chbMarkTA

        self.chbDeparture = QtGui.QCheckBox(self.gbParameters)
        self.chbDeparture.setText("Departure")
        self.gbParameters.Add = self.chbDeparture

        self.chbPolyline = QtGui.QCheckBox(self.gbParameters)
        self.chbPolyline.setText("Draw Polyline")
        self.gbParameters.Add = self.chbPolyline

        self.pnlInput = Frame(self.gbParameters)
        self.pnlInput.Margin = 0
        self.gbParameters.Add = self.pnlInput

        self.chbUseTolerance = QtGui.QCheckBox(self.pnlInput)
        self.chbUseTolerance.setText("Use Tolerance")
        self.pnlInput.Add = self.chbUseTolerance

        pnlInput_0 = Frame(self.pnlInput, "HL")
        pnlInput_0.Margin = 0
        # pnlInput_0.layoutBoxPanel.setSpacing(100)
        self.pnlInput.Add = pnlInput_0

        self.chbWriteName = QtGui.QCheckBox(pnlInput_0)
        self.chbWriteName.setText("Write Name")
        self.chbWriteName.setMaximumWidth(200)
        self.chbWriteName.setMinimumWidth(200)
        pnlInput_0.Add = self.chbWriteName

        self.pnlTextHeight = NumberBoxPanel(pnlInput_0)
        self.pnlTextHeight.Caption = "Text Height"
        self.pnlTextHeight.LabelWidth = 100
        self.pnlTextHeight.Value = 8
        pnlInput_0.Add = self.pnlTextHeight






