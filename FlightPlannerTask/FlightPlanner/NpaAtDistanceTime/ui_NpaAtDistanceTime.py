# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RnavTurningSegmentAnalyser.ui'
#
# Created: Wed Nov 25 17:23:08 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

# from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QString, QSize, QMetaObject
from PyQt4.QtGui import QVBoxLayout, QApplication, QTextDocument, QSpinBox, QFont, QSizePolicy, QRadioButton, QSpacerItem
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
from qgis.gui import QgsTextAnnotationItem
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

class Ui_NpaAtDistanceTime(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(435, 580)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.gbParameters = GroupBox(Form)
        self.gbParameters.Caption = "General"
        self.verticalLayout.addWidget(self.gbParameters)

        self.cmbAerodrome = ComboBoxPanel(self.gbParameters, True)
        self.cmbAerodrome.Caption = "Aerodrome"
        self.cmbAerodrome.LabelWidth = 220
        self.cmbAerodrome.Width = 220
        self.gbParameters.Add = self.cmbAerodrome

        self.cmbRwyDir = ComboBoxPanel(self.gbParameters, True)
        self.cmbRwyDir.Caption = "Runway Direction"
        self.cmbRwyDir.LabelWidth = 220
        self.cmbRwyDir.Width = 220
        self.gbParameters.Add = self.cmbRwyDir

        self.annotationFAWP = QgsTextAnnotationItem(define._canvas)
        self.annotationFAWP.setDocument(QTextDocument("FAF"))
        self.annotationFAWP.hide()

        self.pnlFafPosition = PositionPanel(self.gbParameters, self.annotationFAWP)
        self.pnlFafPosition.Caption = "FAF Position"
        self.pnlFafPosition.btnCalculater.hide()
        self.pnlFafPosition.hideframe_Altitude()
        self.gbParameters.Add = self.pnlFafPosition

        self.pnlThrPosition = PositionPanel(self.gbParameters)
        self.pnlThrPosition.Caption = "Threshold Position"
        self.pnlThrPosition.btnCalculater.hide()
        self.gbParameters.Add = self.pnlThrPosition

        # self.annotationMapt = QgsTextAnnotationItem(define._canvas)
        # self.annotationMapt.setDocument(QTextDocument("MAPt"))
        # self.annotationMapt.hide()

        self.pnlMaPtPosition = PositionPanel(self.gbParameters)
        self.pnlMaPtPosition.Caption = "MAPt Position"
        self.pnlMaPtPosition.btnCalculater.hide()
        self.pnlMaPtPosition.hideframe_Altitude()
        self.gbParameters.Add = self.pnlMaPtPosition

        self.pnlRwyEndPosition = PositionPanel(self.gbParameters)
        self.pnlRwyEndPosition.Caption = "Rwy End Position"
        self.pnlRwyEndPosition.btnCalculater.hide()
        self.pnlRwyEndPosition.hideframe_Altitude()
        self.gbParameters.Add = self.pnlRwyEndPosition
        self.pnlRwyEndPosition.Visible = False



        self.pnlInboundTrack = TrackRadialBoxPanel(self.gbParameters)
        self.pnlInboundTrack.Caption = "In-bound Track"
        self.pnlInboundTrack.LabelWidth = 220
        self.pnlInboundTrack.Enabled = False
        self.gbParameters.Add = self.pnlInboundTrack

        self.pnlEstimatedAltitude = AltitudeBoxPanel(self.gbParameters)
        self.pnlEstimatedAltitude.Caption = "Estimated Altitude"
        self.pnlEstimatedAltitude.LabelWidth = 220
        self.pnlEstimatedAltitude.Value = Altitude(1000)
        self.gbParameters.Add = self.pnlEstimatedAltitude

        self.pnlAerodromeAltitude = AltitudeBoxPanel(self.gbParameters)
        self.pnlAerodromeAltitude.Caption = "Aerodrome Altitude"
        self.pnlAerodromeAltitude.LabelWidth = 220
        self.pnlAerodromeAltitude.Value = Altitude(1000)
        self.gbParameters.Add = self.pnlAerodromeAltitude

        self.pnlIsa = NumberBoxPanel(self.gbParameters, "0.0")
        self.pnlIsa.CaptionUnits = define._degreeStr + "C"
        self.pnlIsa.Caption = "ISA"
        self.pnlIsa.LabelWidth = 220
        self.pnlIsa.Value = 15
        self.gbParameters.Add = self.pnlIsa

        self.cmbAircraftCategory = ComboBoxPanel(self.gbParameters)
        self.cmbAircraftCategory.Caption = "Aircraft Category"
        self.cmbAircraftCategory.LabelWidth = 220
        self.gbParameters.Add = self.cmbAircraftCategory

        # self.pnlHeightLoss = AltitudeBoxPanel(self.gbParameters)
        # self.pnlHeightLoss.Caption = "Height Loss"
        # self.pnlHeightLoss.LabelWidth = 220
        # self.gbParameters.Add = self.pnlHeightLoss

        self.pnlIas = SpeedBoxPanel(self.gbParameters)
        self.pnlIas.Caption = "IAS"
        self.pnlIas.LabelWidth = 220
        self.pnlIas.Value = Speed(100)
        self.pnlIas.Enabled = False
        self.gbParameters.Add = self.pnlIas

        self.pnlTas = SpeedBoxPanel(self.gbParameters)
        self.pnlTas.Caption = "TAS"
        self.pnlTas.Enabled = False
        self.pnlTas.LabelWidth = 220
        self.gbParameters.Add = self.pnlTas

        self.pnlWind = WindPanel(self.gbParameters)
        self.pnlWind.LabelWidth = 214
        self.gbParameters.Add = self.pnlWind

        self.pnlSocAltitude = AltitudeBoxPanel(self.gbParameters)
        self.pnlSocAltitude.Caption = "SOC Altitude"
        self.pnlSocAltitude.LabelWidth = 220
        self.gbParameters.Add = self.pnlSocAltitude

        self.pnlDistA = DistanceBoxPanel(self.gbParameters, DistanceUnits.M, DistanceUnits.NM)
        self.pnlDistA.Caption = "a Distance"
        self.pnlDistA.LabelWidth = 220
        self.pnlDistA.Button = "coordinate_capture.png"
        self.pnlDistA.Value = Distance(900)
        # self.pnlDistA.Enabled = False
        self.gbParameters.Add = self.pnlDistA

        self.pnlDistB = DistanceBoxPanel(self.gbParameters, DistanceUnits.M, DistanceUnits.NM)
        self.pnlDistB.Caption = "b Distance"
        self.pnlDistB.LabelWidth = 220
        self.pnlDistB.Button = "coordinate_capture.png"
        self.pnlDistB.Value = Distance(900)
        # self.pnlDistB.Enabled = False
        self.gbParameters.Add = self.pnlDistB

        self.pnlDistOfFafMapt = DistanceBoxPanel(self.gbParameters, DistanceUnits.M, DistanceUnits.NM)
        self.pnlDistOfFafMapt.Caption = "FAP-MAPt Distance"
        self.pnlDistOfFafMapt.LabelWidth = 220
        self.pnlDistOfFafMapt.Button = None
        self.pnlDistOfFafMapt.Enabled = False
        self.gbParameters.Add = self.pnlDistOfFafMapt

        self.pnlDistOfEarliestToNominalMapt = DistanceBoxPanel(self.gbParameters, DistanceUnits.M, DistanceUnits.NM)
        self.pnlDistOfEarliestToNominalMapt.Caption = "Earliest To Nominal MAPt Distance"
        self.pnlDistOfEarliestToNominalMapt.LabelWidth = 220
        self.pnlDistOfEarliestToNominalMapt.Button = None
        self.pnlDistOfEarliestToNominalMapt.Enabled = False
        self.gbParameters.Add = self.pnlDistOfEarliestToNominalMapt

        self.pnlDistOfNominalToLatestMapt = DistanceBoxPanel(self.gbParameters, DistanceUnits.M, DistanceUnits.NM)
        self.pnlDistOfNominalToLatestMapt.Caption = "Nominal To Latest MAPt Distance"
        self.pnlDistOfNominalToLatestMapt.LabelWidth = 220
        self.pnlDistOfNominalToLatestMapt.Button = None
        self.pnlDistOfNominalToLatestMapt.Enabled = False
        self.gbParameters.Add = self.pnlDistOfNominalToLatestMapt


        self.pnlDistOfMaptSoc = DistanceBoxPanel(self.gbParameters, DistanceUnits.M, DistanceUnits.NM)
        self.pnlDistOfMaptSoc.Caption = "MAPt-SOC Distance"
        self.pnlDistOfMaptSoc.LabelWidth = 220
        self.pnlDistOfMaptSoc.Button = None
        self.pnlDistOfMaptSoc.Enabled = False
        self.gbParameters.Add = self.pnlDistOfMaptSoc

        self.pnlDistOfMaptThr = DistanceBoxPanel(self.gbParameters, DistanceUnits.M, DistanceUnits.NM)
        self.pnlDistOfMaptThr.Caption = "MAPt-THR Distance"
        self.pnlDistOfMaptThr.LabelWidth = 220
        self.pnlDistOfMaptThr.Button = None
        self.pnlDistOfMaptThr.Enabled = False
        self.gbParameters.Add = self.pnlDistOfMaptThr

        self.pnlDistOfSocThr = DistanceBoxPanel(self.gbParameters, DistanceUnits.M, DistanceUnits.NM)
        self.pnlDistOfSocThr.Caption = "SOC-THR Distance"
        self.pnlDistOfSocThr.LabelWidth = 220
        self.pnlDistOfSocThr.Button = None
        self.pnlDistOfSocThr.Enabled = False
        self.gbParameters.Add = self.pnlDistOfSocThr






