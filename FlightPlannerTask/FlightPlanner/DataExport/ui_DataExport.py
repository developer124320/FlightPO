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
from FlightPlanner.Panels.SpeedBoxPanel import SpeedBoxPanel, SpeedUnits
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.ListBox import ListBox
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.CheckBox import CheckBox
from FlightPlanner.Panels.Frame import Frame



class Ui_DataExport(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(473, 580)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        Form.setFont(font)
        # sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        # Form.setSizePolicy(sizePolicy)
        self.vlForm = QtGui.QVBoxLayout(Form)
        self.vlForm.setObjectName(("vlForm"))

        # listWidget = ListBox(Form)
        # listWidget.Items = ["asfdas", "sdafasfd", "3545"]
        # self.vlForm.addWidget(listWidget)

        self.gbFile = GroupBox(Form)
        self.gbFile.Title = "Database File"
        self.vlForm.addWidget(self.gbFile)

        self.pnlFile = TextBoxPanel(self.gbFile)
        self.pnlFile.Caption = ""
        self.pnlFile.Button = "openData.png"
        self.pnlFile.ReadOnly = True
        self.pnlFile.textBox.setMaximumWidth(1000000)
        self.pnlFile.hLayoutBoxPanel.removeItem(self.pnlFile.spacerItem)
        self.gbFile.Add = self.pnlFile


        self.pnlDelimiter = Frame(self.gbFile, "HL")
        self.gbFile.Add = self.pnlDelimiter

        self.cmbDelimiter = ComboBoxPanel(self.pnlDelimiter)
        self.cmbDelimiter.Caption = "Delimiter"
        self.pnlDelimiter.Add = self.cmbDelimiter

        self.txtDelimiter = TextBoxPanel(self.pnlDelimiter)
        self.txtDelimiter.Caption = ""
        self.txtDelimiter.LabelWidth = 0
        self.pnlDelimiter.Add = self.txtDelimiter

        self.chbUnicode = CheckBox(self.gbFile)
        self.chbUnicode.Caption = "Unicode"
        self.gbFile.Add = self.chbUnicode

        self.gbSettings = GroupBox(Form)
        self.gbSettings.Title = "Settings"
        self.vlForm.addWidget(self.gbSettings)

        self.pnlObjectType = Frame(self.gbSettings, "HL")
        self.gbSettings.Add = self.pnlObjectType

        self.cmbObjectType = ComboBoxPanel(self.pnlObjectType)
        self.cmbObjectType.Caption = "Object Type"
        self.pnlObjectType.Add = self.cmbObjectType

        self.cmbPolyType = ComboBoxPanel(self.pnlObjectType)
        self.cmbPolyType.Caption = ""
        self.cmbPolyType.LabelWidth = 0
        self.pnlObjectType.Add = self.cmbPolyType

        self.pnlSelectionMethod = ComboBoxPanel(self.gbSettings)
        self.pnlSelectionMethod.Caption = "Selection Method"
        self.gbSettings.Add = self.pnlSelectionMethod

        self.chbExcludeObjectsAtZero = CheckBox(self.gbSettings)
        self.chbExcludeObjectsAtZero.Caption = "Exclude Objects at Zero Altitude"
        self.gbSettings.Add = self.chbExcludeObjectsAtZero

        self.gbFields = GroupBox(self.gbSettings)
        self.gbFields.Caption = "Fields"
        self.gbSettings.Add = self.gbFields

        self.pnlFields = Frame(self.gbFields)
        self.gbFields.Add = self.pnlFields

        f0 = Frame(self.pnlFields, "HL")
        self.pnlFields.Add = f0

        self.chbName = CheckBox(f0)
        self.chbName.Caption = "Name"
        f0.Add = self.chbName

        self.pnlTolerance = NumberBoxPanel(f0)
        self.pnlTolerance.Button = "coordinate_capture.png"
        self.pnlTolerance.Caption = "Tolerance"
        self.pnlTolerance.LabelWidth = 70
        self.pnlTolerance.Value = 50
        f0.Add = self.pnlTolerance

        self.chbXY = CheckBox(self.pnlFields)
        self.chbXY.Caption = "Cartesian X / Y"
        self.pnlFields.Add = self.chbXY

        self.chbLatLon = CheckBox(self.pnlFields)
        self.chbLatLon.Caption = "Latitude / Longitude"
        self.chbLatLon.LabelWidth = 185
        self.pnlFields.Add = self.chbLatLon

        self.chbAltitude = CheckBox(self.pnlFields)
        self.chbAltitude.Caption = "Altitude (Z value)"
        self.pnlFields.Add = self.chbAltitude

        self.chbRadius = CheckBox(self.pnlFields)
        self.chbRadius.Caption = "Radius"
        self.pnlFields.Add = self.chbRadius



        self.pnlLatLonFormat = ComboBoxPanel(self.chbLatLon)
        self.pnlLatLonFormat.Caption = ""
        self.pnlLatLonFormat.LabelWidth = 0
        self.chbLatLon.hLayout.addWidget(self.pnlLatLonFormat)

        self.pnlNumberPrecision = ComboBoxPanel(self.gbFields)
        self.pnlNumberPrecision.Caption = "Number Precision"
        self.gbFields.Add = self.pnlNumberPrecision

        self.pnlLatLonPrecision = ComboBoxPanel(self.gbFields)
        self.pnlLatLonPrecision.Caption = "Latitude / Longitude Precision"
        self.gbFields.Add = self.pnlLatLonPrecision

        self.chbCRC = CheckBox(self.gbFields)
        self.chbCRC.Caption = "CRC Checksum (CRC32Q)"
        self.gbFields.Add = self.chbCRC









