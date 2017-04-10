# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RnavTurningSegmentAnalyser.ui'
#
# Created: Wed Nov 25 17:23:08 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

# from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QString, QSize, QMetaObject
from PyQt4.QtGui import QVBoxLayout, QApplication, QLabel, QSpinBox, QFont, QSizePolicy, QRadioButton, QSpacerItem
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.Panels.DistanceBoxPanel import DistanceUnits, Distance, DistanceBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.SpeedBoxPanel import SpeedBoxPanel, Speed, SpeedUnits
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel, Altitude
from FlightPlanner.Panels.CheckBox import CheckBox
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.WindPanel import WindPanel

import define

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_TurnProtectionAndObstacleAssessment(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(435, 580)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.gbGeneral = GroupBox(Form)
        self.gbGeneral.Caption = "General"
        self.verticalLayout.addWidget(self.gbGeneral)

        # self.cmbAerodrome = ComboBoxPanel(self.gbGeneral, True)
        # self.cmbAerodrome.Caption = "Aerodrome"
        # self.cmbAerodrome.LabelWidth = 120
        # self.gbGeneral.Add = self.cmbAerodrome
        #
        # self.cmbRwyDir = ComboBoxPanel(self.gbGeneral, True)
        # self.cmbRwyDir.Caption = "Runway Direction"
        # self.cmbRwyDir.LabelWidth = 120
        # self.cmbRwyDir.Width = 120
        # self.gbGeneral.Add = self.cmbRwyDir

        self.cmbRnavSpecification = ComboBoxPanel(self.gbGeneral)
        self.cmbRnavSpecification.Caption = "Rnav Specification"
        self.cmbRnavSpecification.LabelWidth = 150
        self.gbGeneral.Add = self.cmbRnavSpecification

        self.frameChbThree = Frame(self.gbGeneral, "HL")
        self.gbGeneral.Add = self.frameChbThree

        self.chbUseTwoWpt = CheckBox(self.frameChbThree)
        self.chbUseTwoWpt.Caption = "Use 2 Waypoints"
        self.frameChbThree.Add = self.chbUseTwoWpt

        self.chbInsertSymbol = CheckBox(self.frameChbThree)
        self.chbInsertSymbol.Caption = "Insert Symbol(s)"
        self.frameChbThree.Add = self.chbInsertSymbol

        self.chbCatH = CheckBox(self.frameChbThree)
        self.chbCatH.Caption = "Cat.H"
        self.frameChbThree.Add = self.chbCatH

        self.cmbPhaseOfFlight = ComboBoxPanel(self.gbGeneral)
        self.cmbPhaseOfFlight.Caption = "Phase Of Flight"
        self.cmbPhaseOfFlight.LabelWidth = 150
        self.gbGeneral.Add = self.cmbPhaseOfFlight

        self.pnlArp = PositionPanel(self.gbGeneral)
        self.pnlArp.Caption = "Aerodrome Reference Point(ARP)"
        self.pnlArp.btnCalculater.hide()
        self.pnlArp.hideframe_Altitude()
        self.gbGeneral.Add = self.pnlArp

        self.gbWaypoint1 = GroupBox(self.gbGeneral)
        self.gbWaypoint1.Caption = "Waypoint1"
        self.gbGeneral.Add = self.gbWaypoint1

        self.cmbType1 = ComboBoxPanel(self.gbWaypoint1)
        self.cmbType1.Caption = "Type"
        self.cmbType1.LabelWidth = 150
        self.gbWaypoint1.Add = self.cmbType1

        self.pnlTolerances = RnavTolerancesPanel(self.gbWaypoint1)
        self.pnlTolerances.set_Att(Distance(0.8, DistanceUnits.NM))
        self.pnlTolerances.set_Xtt(Distance(1, DistanceUnits.NM))
        self.pnlTolerances.set_Asw(Distance(2, DistanceUnits.NM))
        self.gbWaypoint1.Add = self.pnlTolerances

        self.pnlWaypoint1 = PositionPanel(self.gbWaypoint1)
        self.pnlWaypoint1.btnCalculater.hide()
        self.pnlWaypoint1.hideframe_Altitude()
        self.gbWaypoint1.Add = self.pnlWaypoint1

        self.gbWaypoint2 = GroupBox(self.gbGeneral)
        self.gbWaypoint2.Caption = "Waypoint2"
        self.gbGeneral.Add = self.gbWaypoint2

        self.cmbType2 = ComboBoxPanel(self.gbWaypoint2)
        self.cmbType2.Caption = "Type"
        self.cmbType2.LabelWidth = 150
        self.gbWaypoint2.Add = self.cmbType2

        self.pnlTolerances2 = RnavTolerancesPanel(self.gbWaypoint2)
        self.pnlTolerances2.set_Att(Distance(0.8, DistanceUnits.NM))
        self.pnlTolerances2.set_Xtt(Distance(1, DistanceUnits.NM))
        self.pnlTolerances2.set_Asw(Distance(2, DistanceUnits.NM))
        self.gbWaypoint2.Add = self.pnlTolerances2

        self.pnlWaypoint2 = PositionPanel(self.gbWaypoint2)
        self.pnlWaypoint2.btnCalculater.hide()
        self.pnlWaypoint2.hideframe_Altitude()
        self.gbWaypoint2.Add = self.pnlWaypoint2

        self.frmRadioBtns = Frame(self.gbGeneral, "HL")
        self.gbGeneral.Add = self.frmRadioBtns

        self.rdnTF = QRadioButton(self.frmRadioBtns)
        self.rdnTF.setObjectName("rdnTF")
        self.rdnTF.setText("TF")
        self.rdnTF.setChecked(True)
        self.frmRadioBtns.Add = self.rdnTF

        self.rdnDF = QRadioButton(self.frmRadioBtns)
        self.rdnDF.setObjectName("rdnDF")
        self.rdnDF.setText("DF")
        self.frmRadioBtns.Add = self.rdnDF

        self.rdnCF = QRadioButton(self.frmRadioBtns)
        self.rdnCF.setObjectName("rdnCF")
        self.rdnCF.setText("CF")
        self.frmRadioBtns.Add = self.rdnCF


        self.chbCircularArcs = CheckBox(self.gbGeneral)
        self.chbCircularArcs.Caption = "Use Circular Arcs Method for Turns <= 30"
        self.gbGeneral.Add = self.chbCircularArcs

        self.gbParameters = GroupBox(Form)
        self.gbParameters.Caption = "Parameters"
        self.verticalLayout.addWidget(self.gbParameters)

        self.cmbSelectionMode = ComboBoxPanel(self.gbParameters)
        self.cmbSelectionMode.Caption = "Selection Mode"
        self.cmbSelectionMode.LabelWidth = 150
        self.gbParameters.Add = self.cmbSelectionMode


        self.pnlInbound = TrackRadialBoxPanel(self.gbParameters)
        self.pnlInbound.Caption = "In-bound Track"
        self.pnlInbound.LabelWidth = 150
        self.gbParameters.Add = self.pnlInbound

        self.pnlOutbound = TrackRadialBoxPanel(self.gbParameters)
        self.pnlOutbound.Caption = "Out-bound Track"
        self.pnlOutbound.LabelWidth = 150
        self.gbParameters.Add = self.pnlOutbound


        # icon = QIcon()
        # icon.addPixmap(QPixmap(_fromUtf8("Resource/coordinate_capture.png")), QIcon.Normal, QIcon.Off)

        self.pnlIas = SpeedBoxPanel(self.gbParameters)
        self.pnlIas.Caption = "IAS"
        self.pnlIas.LabelWidth = 150
        self.pnlIas.Value = Speed(250)
        self.gbParameters.Add = self.pnlIas

        self.pnlTas = SpeedBoxPanel(self.gbParameters)
        self.pnlTas.Caption = "TAS"
        self.pnlTas.Enabled = False
        self.pnlTas.LabelWidth = 150
        self.gbParameters.Add = self.pnlTas

        self.pnlAltitude = AltitudeBoxPanel(self.gbParameters)
        self.pnlAltitude.Caption = "Altitude"
        self.pnlAltitude.LabelWidth = 150
        self.pnlAltitude.Value = Altitude(1000)
        self.gbParameters.Add = self.pnlAltitude

        self.pnlIsa = NumberBoxPanel(self.gbParameters, "0.0")
        self.pnlIsa.CaptionUnits = define._degreeStr + "C"
        self.pnlIsa.Caption = "ISA"
        self.pnlIsa.LabelWidth = 150
        self.pnlIsa.Value = 15
        self.gbParameters.Add = self.pnlIsa

        self.pnlBankAngle = NumberBoxPanel(self.gbParameters, "0.0")
        self.pnlBankAngle.CaptionUnits = define._degreeStr
        self.pnlBankAngle.Caption = "Bank Angle"
        self.pnlBankAngle.LabelWidth = 150
        self.pnlBankAngle.Value = 25
        self.gbParameters.Add = self.pnlBankAngle

        self.pnlBankEstTime = NumberBoxPanel(self.gbParameters, "0.0")
        self.pnlBankEstTime.Caption = "Bank Establishment Time"
        self.pnlBankEstTime.Value = 1
        self.pnlBankEstTime.LabelWidth = 150
        self.pnlBankEstTime.Value = 5
        self.gbParameters.Add = self.pnlBankEstTime

        self.pnlPilotTime = NumberBoxPanel(self.gbParameters, "0.0")
        self.pnlPilotTime.Caption = "Pilot Reaction Time"
        self.pnlPilotTime.Value = 6
        self.pnlPilotTime.LabelWidth = 150
        self.gbParameters.Add = self.pnlPilotTime

        self.pnlWind = WindPanel(self.gbParameters)
        self.pnlWind.LabelWidth = 145
        self.gbParameters.Add = self.pnlWind

        self.pnlPrimaryMoc = AltitudeBoxPanel(self.gbParameters)
        self.pnlPrimaryMoc.Caption = "Primary Moc"
        self.pnlPrimaryMoc.LabelWidth = 150
        self.gbParameters.Add = self.pnlPrimaryMoc

        self.cmbConstructionType = ComboBoxPanel(self.gbParameters)
        self.cmbConstructionType.Caption = "Construction Type"
        self.cmbConstructionType.LabelWidth = 150
        self.gbParameters.Add = self.cmbConstructionType

        self.frameMOCmultipiler = Frame(self.gbParameters, "HL")
        self.gbParameters.Add = self.frameMOCmultipiler

        self.labelMOCmultipiler = QLabel(self.frameMOCmultipiler)
        self.labelMOCmultipiler.setMinimumSize(QSize(145, 0))
        self.labelMOCmultipiler.setMaximumSize(QSize(145, 16777215))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelMOCmultipiler.setFont(font)
        self.labelMOCmultipiler.setObjectName(_fromUtf8("labelMOCmultipiler"))
        self.labelMOCmultipiler.setText("MOCmultipiler")
        self.frameMOCmultipiler.Add = self.labelMOCmultipiler

        self.mocSpinBox = QSpinBox(self.frameMOCmultipiler)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mocSpinBox.sizePolicy().hasHeightForWidth())
        self.mocSpinBox.setSizePolicy(sizePolicy)
        self.mocSpinBox.setMinimumSize(QSize(70, 0))
        self.mocSpinBox.setMaximumSize(QSize(70, 16777215))
        self.mocSpinBox.setMinimum(1)
        self.mocSpinBox.setObjectName(_fromUtf8("mocSpinBox"))
        self.frameMOCmultipiler.Add = self.mocSpinBox

        spacerItem = QSpacerItem(10,10,QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.frameMOCmultipiler.layoutBoxPanel.addItem(spacerItem)

        self.chbDrawTolerance = CheckBox(self.gbParameters)
        self.chbDrawTolerance.Caption = "Draw Waypoint Tolerance"
        self.gbParameters.Add = self.chbDrawTolerance