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
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame



class Ui_FasDataBlock(object):
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

         ######### ------- InPut Group -------------##########
        self.gbInput = GroupBox(Form)
        self.gbInput.Title = "Input Data"
        self.vlForm.addWidget(self.gbInput)

        self.pnlOperationType = ComboBoxPanel(self.gbInput)
        self.pnlOperationType.Caption = "Operation Type"
        self.gbInput.Add = self.pnlOperationType

        self.pnlSbasProvider = ComboBoxPanel(self.gbInput)
        self.pnlSbasProvider.Caption = "SBAS Provider"
        self.gbInput.Add = self.pnlSbasProvider

        self.pnlAirportId = TextBoxPanel(self.gbInput)
        self.pnlAirportId.Caption = "Airport Identifier"
        self.pnlAirportId.Value = "ESSP"
        self.gbInput.Add = self.pnlAirportId

        self.pnlRunway = Frame(self.gbInput, "HL")
        self.pnlRunway.Margin = 0
        self.gbInput.Add = self.pnlRunway

        self.txtRunwayDesignator = NumberBoxPanel(self.pnlRunway, "0")
        self.txtRunwayDesignator.Caption = "Runway"
        self.txtRunwayDesignator.Value = 19
        self.pnlRunway.Add = self.txtRunwayDesignator

        self.cmbRunwayLetter = ComboBoxPanel(self.pnlRunway)
        self.cmbRunwayLetter.Caption = ""
        self.pnlRunway.Add = self.cmbRunwayLetter

        self.pnlApproachPerformanceDesignator = ComboBoxPanel(self.gbInput)
        self.pnlApproachPerformanceDesignator.Caption = "Approach Performance Designator"
        self.gbInput.Add = self.pnlApproachPerformanceDesignator

        self.pnlRouteIndicator = ComboBoxPanel(self.gbInput)
        self.pnlRouteIndicator.Caption = "Route Indicator"
        self.gbInput.Add = self.pnlRouteIndicator

        self.pnlReferencePathDataSelector = NumberBoxPanel(self.gbInput, "0")
        self.pnlReferencePathDataSelector.Caption = "Reference Path Data Selector"
        self.pnlReferencePathDataSelector.Value = 1
        self.gbInput.Add = self.pnlReferencePathDataSelector

        self.pnlReferencePathId = TextBoxPanel(self.pnlRunway)
        self.pnlReferencePathId.Caption = "Reference Path Identifier"
        self.pnlReferencePathId.Value = "4klk"
        self.gbInput.Add = self.pnlReferencePathId

        self.gbLtpFtp = GroupBox(self.gbInput)
        self.gbLtpFtp.Caption = "LTP/FTP Position"
        self.gbInput.Add = self.gbLtpFtp

        self.pnlLtpFtp = PositionPanel(self.gbLtpFtp, None, None, "Degree")
        self.pnlLtpFtp.btnCalculater.hide()
        self.pnlLtpFtp.hideframe_Altitude()
        self.pnlLtpFtp.degreeFormat = "ddmmss.ssssH"
        self.gbLtpFtp.Add = self.pnlLtpFtp

        self.pnlLtpFtpEllipsoidalHeight = NumberBoxPanel(self.gbLtpFtp, "0.0")
        self.pnlLtpFtpEllipsoidalHeight.CaptionUnits = "m"
        self.pnlLtpFtpEllipsoidalHeight.Caption = "LTP/FTP Ellipsoidal Height"
        self.pnlLtpFtpEllipsoidalHeight.Value = 343
        self.gbLtpFtp.Add = self.pnlLtpFtpEllipsoidalHeight

        self.gbFpap = GroupBox(self.gbInput)
        self.gbFpap.Caption = "FPAP Position"
        self.gbInput.Add = self.gbFpap

        self.pnlFpap = PositionPanel(self.gbFpap, None, None, "Degree")
        self.pnlFpap.btnCalculater.hide()
        self.pnlFpap.hideframe_Altitude()
        self.pnlFpap.degreeFormat = "ddmmss.ssssH"
        self.gbFpap.Add = self.pnlFpap

        self.pnlApproachTCH = Frame(self.gbFpap, "HL")
        self.pnlApproachTCH.Margin = 0
        self.gbFpap.Add = self.pnlApproachTCH

        self.txtApproachTCH = NumberBoxPanel(self.pnlApproachTCH, "0.0")
        self.txtApproachTCH.Caption = "Threshold Crossing Height"
        self.txtApproachTCH.Value = 50
        self.pnlApproachTCH.Add = self.txtApproachTCH

        self.cmbApproachTCHunits = ComboBoxPanel(self.pnlApproachTCH)
        self.cmbApproachTCHunits.Width = 40
        self.cmbApproachTCHunits.Caption = ""
        self.pnlApproachTCH.Add = self.cmbApproachTCHunits

        self.pnlGPA = NumberBoxPanel(self.gbInput, "0.00")
        self.pnlGPA.CaptionUnits = "degree"
        self.pnlGPA.Caption = "GlidePath Angle"
        self.pnlGPA.Value = 3
        self.gbInput.Add = self.pnlGPA

        self.pnlCourseWidth = NumberBoxPanel(self.gbInput, "0.00")
        self.pnlCourseWidth.CaptionUnits = "m"
        self.pnlCourseWidth.Caption = "Course Width"
        self.pnlCourseWidth.Value = 80
        self.gbInput.Add = self.pnlCourseWidth

        self.pnlLengthOffset = NumberBoxPanel(self.gbInput, "0")
        self.pnlLengthOffset.CaptionUnits = "m"
        self.pnlLengthOffset.Caption = "Length Offset"
        self.pnlLengthOffset.Value = 0
        self.gbInput.Add = self.pnlLengthOffset

        self.pnlHAL = NumberBoxPanel(self.gbInput, "0.0")
        self.pnlHAL.CaptionUnits = "m"
        self.pnlHAL.Caption = "HAL"
        self.pnlHAL.Value = 40
        self.gbInput.Add = self.pnlHAL

        self.pnlVAL = NumberBoxPanel(self.gbInput, "0.0")
        self.pnlVAL.CaptionUnits = "m"
        self.pnlVAL.Caption = "VAL"
        self.pnlVAL.Value = 40
        self.gbInput.Add = self.pnlVAL

        ######### ------- OutPut Group -------------##########

        self.gbOutput = GroupBox(Form)
        self.gbOutput.Caption = "Output Data"
        self.vlForm.addWidget(self.gbOutput)

        self.txtDataBlock = TextBoxPanel(self.gbOutput, True)
        self.txtDataBlock.Caption = "Data Block"
        self.txtDataBlock.Enabled = False
        self.gbOutput.Add = self.txtDataBlock

        self.pnlCRC = TextBoxPanel(self.gbOutput)
        self.pnlCRC.Caption = "CRC Value"
        self.pnlCRC.Enabled = False
        self.gbOutput.Add = self.pnlCRC

        ######### ------- Additional Data Group -------------##########

        self.gbAdditionalData = GroupBox(Form)
        self.gbAdditionalData.Caption = "Required Additional Data"
        self.vlForm.addWidget(self.gbAdditionalData)

        self.pnlIcaoCode = TextBoxPanel(self.gbAdditionalData)
        self.pnlIcaoCode.Caption = "ICAO Code"
        self.gbAdditionalData.Add = self.pnlIcaoCode

        self.pnlLtpFtpOrthoHeight = NumberBoxPanel(self.gbAdditionalData, "0.0")
        self.pnlLtpFtpOrthoHeight.CaptionUnits = "m"
        self.pnlLtpFtpOrthoHeight.Caption = "LTP/FTP Orthometic Height"
        self.gbAdditionalData.Add = self.pnlLtpFtpOrthoHeight

        self.pnlFpapOrthoHeight = NumberBoxPanel(self.gbAdditionalData, "0.0")
        self.pnlFpapOrthoHeight.CaptionUnits = "m"
        self.pnlFpapOrthoHeight.Caption = "FPAP Orthometic Height"
        self.gbAdditionalData.Add = self.pnlFpapOrthoHeight












