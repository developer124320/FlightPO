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
from FlightPlanner.Panels.AngleGradientBoxPanel import AngleGradientBoxPanel, AngleGradientSlopeUnits, AngleGradientSlope
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits, Distance
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel, Altitude
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.SpeedBoxPanel import SpeedBoxPanel, SpeedUnits, Speed
from FlightPlanner.Panels.WindPanel import WindPanel
from FlightPlanner.QgisHelper import QgisHelper
import define


class Ui_MASegment(object):
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

        self.gbMASegmentType = GroupBox(Form)
        self.gbMASegmentType.Caption = "Missed Approach Segment Type"
        self.vlForm.addWidget(self.gbMASegmentType)

        self.txtMASegmentType = TextBoxPanel(self.gbMASegmentType)
        self.txtMASegmentType.Caption = "Type"
        self.txtMASegmentType.textBox.setEnabled(False)
        self.txtMASegmentType.Button = "sort2.png"
        self.txtMASegmentType.Value = "Straight"
        self.txtMASegmentType.textBox.setMaximumWidth(10000000)
        self.txtMASegmentType.hLayoutBoxPanel.removeItem(self.txtMASegmentType.spacerItem)
        QtCore.QObject.connect(self.txtMASegmentType, QtCore.SIGNAL("Event_1"), self.txtMASegmentType_Event_1)
        self.gbMASegmentType.Add = self.txtMASegmentType

        self.gbPosition = GroupBox(Form)
        self.gbPosition.Caption = "Positions"
        self.gbPosition.layoutBoxPanel.setSpacing(9)
        self.vlForm.addWidget(self.gbPosition)

        self.pnlFafPos = PositionPanel(self.gbPosition)
        self.pnlFafPos.Caption = "FAF Position"
        self.pnlFafPos.hideframe_Altitude()
        self.pnlFafPos.btnCalculater.hide()
        self.gbPosition.Add = self.pnlFafPos

        self.pnlMaptPos = PositionPanel(self.gbPosition)
        self.pnlMaptPos.Caption = "MAPt Position"
        self.pnlMaptPos.hideframe_Altitude()
        self.pnlMaptPos.btnCalculater.hide()
        self.gbPosition.Add = self.pnlMaptPos

        self.pnlMaTpPos = PositionPanel(self.gbPosition)
        self.pnlMaTpPos.Caption = "MA TP Position"
        self.pnlMaTpPos.hideframe_Altitude()
        self.pnlMaTpPos.btnCalculater.hide()
        self.gbPosition.Add = self.pnlMaTpPos
        self.pnlMaTpPos.Visible = False

        self.gbMaEndPos = GroupBox(self.gbPosition)
        self.gbMaEndPos.Caption = "MA End Position"
        self.gbPosition.Add = self.gbMaEndPos

        self.cmbMaEndType = ComboBoxPanel(self.gbMaEndPos)
        self.cmbMaEndType.Caption = "Type"
        self.cmbMaEndType.Items = ["NDB", "VOR"]
        self.gbMaEndPos.Add = self.cmbMaEndType
        self.cmbMaEndType.Visible = False

        self.pnlMaEndPos = PositionPanel(self.gbMaEndPos)
        self.pnlMaEndPos.hideframe_Altitude()
        self.pnlMaEndPos.btnCalculater.hide()
        self.gbMaEndPos.Add = self.pnlMaEndPos



        self.gbNavAid = GroupBox(self.gbPosition)
        self.gbNavAid.Caption = "Navigational Aid Position"
        self.gbPosition.Add = self.gbNavAid

        self.cmbNavAidType = ComboBoxPanel(self.gbNavAid)
        self.cmbNavAidType.Caption = "Type"
        self.cmbNavAidType.Items = ["NDB", "VOR"]
        self.gbNavAid.Add = self.cmbNavAidType

        self.pnlNavAidPos = PositionPanel(self.gbNavAid)
        self.pnlNavAidPos.btnCalculater.hide()
        self.pnlNavAidPos.hideframe_Altitude()
        self.gbNavAid.Add = self.pnlNavAidPos

        self.gbAddNavAid = GroupBox(self.gbPosition)
        self.gbAddNavAid.Caption = "Additional Navigational Aid Position"
        self.gbPosition.Add = self.gbAddNavAid

        self.cmbAddNavAidType = ComboBoxPanel(self.gbAddNavAid)
        self.cmbAddNavAidType.Caption = "Type"
        self.cmbAddNavAidType.Items = ["NDB", "VOR"]
        self.gbAddNavAid.Add = self.cmbAddNavAidType

        self.pnlAddNavAidPos = PositionPanel(self.gbAddNavAid)
        self.pnlAddNavAidPos.btnCalculater.hide()
        self.pnlAddNavAidPos.hideframe_Altitude()
        self.gbAddNavAid.Add = self.pnlAddNavAidPos



        self.gbParameters = GroupBox(Form)
        self.gbParameters.Caption = "Parameters"
        self.gbParameters.layoutBoxPanel.setSpacing(9)
        self.vlForm.addWidget(self.gbParameters)

        self.cmbTypeMapt = ComboBoxPanel(self.gbParameters)
        self.cmbTypeMapt.Caption = "MAPt Type"
        self.cmbTypeMapt.Items = ["Navigation facility", "FIX", "Timing"]
        self.gbParameters.Add = self.cmbTypeMapt

        self.cmbTypeTP = ComboBoxPanel(self.gbParameters)
        self.cmbTypeTP.Caption = "TP Type"
        self.cmbTypeTP.Items = ["Turn at FIX or Facility", "Turn at Altitude", "Turn at MAPt"]
        self.gbParameters.Add = self.cmbTypeTP
        self.cmbTypeTP.Visible = False

        self.cmbAircraftCatgory = ComboBoxPanel(self.gbParameters)
        self.cmbAircraftCatgory.Caption = "Aircraft Category"
        self.cmbAircraftCatgory.Items = ["A", "B", "C", "D", "E", "H"]
        self.gbParameters.Add = self.cmbAircraftCatgory

        self.cmbDirection = ComboBoxPanel(self.gbParameters)
        self.cmbDirection.Caption = "Direction"
        self.cmbDirection.Items = ["Left", "Right"]
        self.gbParameters.Add = self.cmbDirection
        self.cmbDirection.Visible = False


        self.pnlAerodromeAlt = AltitudeBoxPanel(self.gbParameters)
        self.pnlAerodromeAlt.CaptionUnits = "ft"
        self.pnlAerodromeAlt.Caption = "Aerodrome Altitude"
        self.gbParameters.Add = self.pnlAerodromeAlt

        self.pnlPrimaryMoc = AltitudeBoxPanel(self.gbParameters)
        self.pnlPrimaryMoc.CaptionUnits = "m"
        self.pnlPrimaryMoc.Caption = "Primary Moc"
        self.pnlPrimaryMoc.Value = Altitude(75)
        self.gbParameters.Add = self.pnlPrimaryMoc

        self.pnlOCA = AltitudeBoxPanel(self.gbParameters)
        self.pnlOCA.CaptionUnits = "ft"
        self.pnlOCA.Caption = "OCA"
        self.gbParameters.Add = self.pnlOCA

        self.pnlTpAlt = AltitudeBoxPanel(self.gbParameters)
        self.pnlTpAlt.CaptionUnits = "ft"
        self.pnlTpAlt.Caption = "TP Altitude"
        self.gbParameters.Add = self.pnlTpAlt
        self.pnlTpAlt.Visible = False

        self.pnlEndTurnAlt = AltitudeBoxPanel(self.gbParameters)
        self.pnlEndTurnAlt.CaptionUnits = "ft"
        self.pnlEndTurnAlt.Caption = "End Turn Altitude"
        self.gbParameters.Add = self.pnlEndTurnAlt
        self.pnlEndTurnAlt.Visible = False

        self.pnlEndAlt = AltitudeBoxPanel(self.gbParameters)
        self.pnlEndAlt.CaptionUnits = "ft"
        self.pnlEndAlt.Caption = "End Altitude"
        self.gbParameters.Add = self.pnlEndAlt
        self.pnlEndAlt.Visible = False

        self.pnlTurnGradient = AngleGradientBoxPanel(self.gbParameters)
        self.pnlTurnGradient.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlTurnGradient.Caption = "Turn Gradient"
        # self.pnlTurnGradient.Value = AngleGradientSlope(2.5, AngleGradientSlopeUnits.Percent)
        self.gbParameters.Add = self.pnlTurnGradient
        self.pnlTurnGradient.Visible = False

        self.pnlBearing = TrackRadialBoxPanel(self.gbParameters)
        self.pnlBearing.Caption = "Bearing"
        self.gbParameters.Add = self.pnlBearing
        self.pnlBearing.Visible = False

        self.pnlDistance = DistanceBoxPanel(self.gbParameters, DistanceUnits.NM)
        self.pnlDistance.Caption = "Distance FAF-MAPt"
        self.pnlDistance.Button = None
        self.gbParameters.Add = self.pnlDistance

        self.pnlClimbGradient = AngleGradientBoxPanel(self.gbParameters)
        self.pnlClimbGradient.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlClimbGradient.Caption = "Climb Gradient"
        self.pnlClimbGradient.Value = AngleGradientSlope(2.5, AngleGradientSlopeUnits.Percent)
        self.gbParameters.Add = self.pnlClimbGradient

        self.cmbTrackGuidance = ComboBoxPanel(self.gbParameters)
        self.cmbTrackGuidance.Caption = "Track Guidance"
        self.cmbTrackGuidance.Items = ["Yes", "No"]
        QtCore.QObject.connect(self.cmbTrackGuidance, QtCore.SIGNAL("Event_0"), self.cmbTrackGuidanceEvent_0)
        self.gbParameters.Add = self.cmbTrackGuidance

        self.cmbAddTrackGuidance = ComboBoxPanel(self.gbParameters)
        self.cmbAddTrackGuidance.Caption = "Additional Track Guidance"
        self.cmbAddTrackGuidance.Items = ["Yes", "No"]
        QtCore.QObject.connect(self.cmbAddTrackGuidance, QtCore.SIGNAL("Event_0"), self.cmbAddTrackGuidanceEvent_0)
        self.gbParameters.Add = self.cmbAddTrackGuidance

        self.cmbTurnMAPt = ComboBoxPanel(self.gbParameters)
        self.cmbTurnMAPt.Caption = "Turn Before MAPt"
        self.cmbTurnMAPt.Items = ["Yes", "No"]
        # QtCore.QObject.connect(self.cmbTrackGuidance, QtCore.SIGNAL("Event_0"), self.cmbTrackGuidanceEvent_0)
        self.gbParameters.Add = self.cmbTurnMAPt
        self.cmbTurnMAPt.Visible = False

        self.gbTpTolerance = GroupBox(self.gbParameters)
        self.gbTpTolerance.Caption = "TP Tolerance"
        self.gbParameters.Add = self.gbTpTolerance
        self.gbTpTolerance.Visible = False

        self.txtKEarlist = NumberBoxPanel(self.gbTpTolerance)
        self.txtKEarlist.CaptionUnits = "nm"
        self.txtKEarlist.Caption = "K Earliest"
        self.gbTpTolerance.Add = self.txtKEarlist

        self.txtLatestFix = NumberBoxPanel(self.gbTpTolerance)
        self.txtLatestFix.CaptionUnits = "nm"
        self.txtLatestFix.Caption = "Latest Fix"
        self.gbTpTolerance.Add = self.txtLatestFix

        self.txtC = NumberBoxPanel(self.gbTpTolerance)
        self.txtC.CaptionUnits = "nm"
        self.txtC.Caption = "C"
        self.gbTpTolerance.Add = self.txtC

        self.txtLatestTurn = NumberBoxPanel(self.gbTpTolerance)
        self.txtLatestTurn.CaptionUnits = "nm"
        self.txtLatestTurn.Caption = "Latest"
        self.gbTpTolerance.Add = self.txtLatestTurn

        self.gbNominalTrack = GroupBox(self.gbParameters)
        self.gbNominalTrack.Caption = "Nominal Track"
        self.gbParameters.Add = self.gbNominalTrack
        self.gbNominalTrack.Visible = False

        self.pnlTrueStartTrack = TrackRadialBoxPanel(self.gbNominalTrack)
        self.pnlTrueStartTrack.Caption = "True Start Track"
        self.gbNominalTrack.Add = self.pnlTrueStartTrack

        self.pnlTrueEndTrack = TrackRadialBoxPanel(self.gbNominalTrack)
        self.pnlTrueEndTrack.Caption = "True End Track"
        self.gbNominalTrack.Add = self.pnlTrueEndTrack

        self.txtArcLength = NumberBoxPanel(self.gbNominalTrack)
        self.txtArcLength.CaptionUnits = "nm"
        self.txtArcLength.Caption = "Arc Length"
        self.gbNominalTrack.Add = self.txtArcLength

        self.gbVelocity = GroupBox(self.gbParameters)
        self.gbVelocity.Caption = "ISA VAR Celsius,IAS,TAS and Wind Velocity"
        self.gbParameters.Add = self.gbVelocity

        self.txtISAVAR = NumberBoxPanel(self.gbVelocity, "0.0")
        self.txtISAVAR.CaptionUnits = define._degreeStr + QtCore.QString("C")
        self.txtISAVAR.Caption = "ISA"
        # self.txtISAVAR.Items = ["ISA-30", "ISA-20", "ISA-10", "ISA", "ISA+10", "ISA+15", "ISA+20", "ISA+30"]
        self.gbVelocity.Add = self.txtISAVAR

        self.pnlIAS = SpeedBoxPanel(self.gbVelocity, SpeedUnits.KTS)
        self.pnlIAS.Caption = "IAS"
        self.gbVelocity.Add = self.pnlIAS

        # self.pnlWind = WindPanel(self.gbVelocity)
        # self.gbVelocity.Add = self.pnlWind
        # self.pnlWind.Visible = False

        self.pnlTAS = SpeedBoxPanel(self.gbVelocity, SpeedUnits.KTS)
        self.pnlTAS.Caption = "TAS"
        self.gbVelocity.Add = self.pnlTAS

        self.gbTurn = GroupBox(self.gbParameters)
        self.gbTurn.Caption = "Turn"
        self.gbParameters.Add = self.gbTurn
        self.gbTurn.Visible = False

        self.txtBankAngle = NumberBoxPanel(self.gbTurn)
        self.txtBankAngle.CaptionUnits = define._degreeStr
        self.txtBankAngle.Caption = "Bank Angle"
        self.gbTurn.Add = self.txtBankAngle

        self.txtRateOfTurn = NumberBoxPanel(self.gbTurn)
        self.txtRateOfTurn.CaptionUnits = define._degreeStr + QtCore.QString("/sec")
        self.txtRateOfTurn.Caption = "Rate Of Turn"
        self.gbTurn.Add = self.txtRateOfTurn

        self.txtWindEffect = NumberBoxPanel(self.gbTurn)
        self.txtWindEffect.Caption = "Wind Effect"
        self.gbTurn.Add = self.txtWindEffect


        self.gbMAPtTolerance = GroupBox(self.gbParameters)
        self.gbMAPtTolerance.Caption = "MAPt Tolerance"
        self.gbParameters.Add = self.gbMAPtTolerance

        self.txtEarlist = NumberBoxPanel(self.gbMAPtTolerance)
        self.txtEarlist.CaptionUnits = "nm"
        self.txtEarlist.Caption = "Earliest"
        self.gbMAPtTolerance.Add = self.txtEarlist

        self.txtLatest = NumberBoxPanel(self.gbMAPtTolerance)
        self.txtLatest.CaptionUnits = "nm"
        self.txtLatest.Caption = "Latest"
        self.gbMAPtTolerance.Add = self.txtLatest

        self.txtD = NumberBoxPanel(self.gbMAPtTolerance)
        self.txtD.CaptionUnits = "nm"
        self.txtD.Caption = "D"
        self.gbMAPtTolerance.Add = self.txtD

        self.gbMAPtToSocDist = GroupBox(self.gbParameters)
        self.gbMAPtToSocDist.Caption = "MAPt to SOC Distance"
        self.gbParameters.Add = self.gbMAPtToSocDist

        self.txtX = NumberBoxPanel(self.gbMAPtToSocDist)
        self.txtX.CaptionUnits = "nm"
        self.txtX.Caption = "X"
        self.gbMAPtToSocDist.Add = self.txtX

        self.txtDistMAPtSOC = DistanceBoxPanel(self.gbMAPtToSocDist, DistanceUnits.NM)
        self.txtDistMAPtSOC.Caption = "MAPt - SOC Distance"
        self.txtDistMAPtSOC.Button = None
        self.gbMAPtToSocDist.Add = self.txtDistMAPtSOC

        self.txtEarlistTemp = NumberBoxPanel(self.gbParameters)
        self.gbParameters.Add = self.txtEarlistTemp
        self.txtEarlistTemp.Visible = False

        self.txtLatestTemp = NumberBoxPanel(self.gbParameters)
        self.gbParameters.Add = self.txtLatestTemp
        self.txtLatestTemp.Visible = False
        

        self.missedApproachMenu = QtGui.QMenu()

        self.strightCmd = QgisHelper.createAction(self.missedApproachMenu, "Straight", self.menuStrightClick)
        self.missedApproachMenu.addAction(self.strightCmd)

        self.turningCmd = QgisHelper.createAction(self.missedApproachMenu, "Turning", self.menuTurningClick)
        self.missedApproachMenu.addAction(self.turningCmd)

    def cmbTrackGuidanceEvent_0(self):
        self.cmbAddTrackGuidance.Enabled = self.cmbTrackGuidance.SelectedIndex == 0
        self.gbAddNavAid.Enabled = self.cmbTrackGuidance.SelectedIndex == 0 and self.cmbAddTrackGuidance.SelectedIndex == 0
    def cmbAddTrackGuidanceEvent_0(self):
        self.gbAddNavAid.Enabled = self.cmbAddTrackGuidance.SelectedIndex == 0

    def txtMASegmentType_Event_1(self):
        rcRect = self.txtMASegmentType.imageButton.geometry()
        ptPoint = rcRect.bottomLeft()
        self.missedApproachMenu.exec_(self.txtMASegmentType.mapToGlobal(ptPoint))
    def menuStrightClick(self):
        self.txtMASegmentType.Value = "Straight"

        self.cmbTypeTP.Visible = False
        self.cmbDirection.Visible = False
        self.pnlTpAlt.Visible = False
        self.pnlEndTurnAlt.Visible = False
        self.pnlEndAlt.Visible = False
        self.pnlTurnGradient.Visible = False
        self.pnlBearing.Visible = False
        self.pnlMaTpPos.Visible = False
        self.cmbTurnMAPt.Visible = False
        self.gbTpTolerance.Visible = False
        self.gbNominalTrack.Visible = False
        # self.pnlWind.Visible = False
        self.gbTurn.Visible = False
        self.cmbMaEndType.Visible = False

        self.cmbTypeMapt.Visible = True
        self.pnlAerodromeAlt.Visible = True
        self.pnlOCA.Visible = True
        self.pnlDistance.Visible = True
        self.pnlClimbGradient.Visible = True
        self.gbMAPtTolerance.Visible = True
        self.gbMAPtToSocDist.Visible = True
    def menuTurningClick(self):
        self.txtMASegmentType.Value = "Turning"

        self.cmbTypeTP.Visible = True
        self.cmbDirection.Visible = True
        self.pnlTpAlt.Visible = True
        self.pnlEndTurnAlt.Visible = True
        self.pnlEndAlt.Visible = True
        self.pnlTurnGradient.Visible = True
        self.pnlBearing.Visible = True
        self.pnlMaTpPos.Visible = True
        self.cmbTurnMAPt.Visible = True
        self.gbTpTolerance.Visible = True
        self.gbNominalTrack.Visible = True
        # self.pnlWind.Visible = True
        self.gbTurn.Visible = True
        self.cmbMaEndType.Visible = True

        self.cmbTypeMapt.Visible = False
        self.pnlAerodromeAlt.Visible = False
        self.pnlOCA.Visible = False
        self.pnlDistance.Visible = False
        self.pnlClimbGradient.Visible = False
        self.gbMAPtTolerance.Visible = False
        self.gbMAPtToSocDist.Visible = False
