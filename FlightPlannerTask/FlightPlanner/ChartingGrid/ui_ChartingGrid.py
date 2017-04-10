# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HoldingRnav.ui'
#
# Created: Wed Nov 25 16:19:08 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.CheckBox import CheckBox
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.MapScalePanel import MapScaleDropDownType, MapScalePanel
from FlightPlanner.Panels.OCAHPanel import OCAHPanel
from FlightPlanner.Panels.SpeedBoxPanel import SpeedBoxPanel, SpeedUnits, Speed
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits, Distance
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel, Altitude
from FlightPlanner.types import AltitudeUnits
from qgis.gui import QgsMapToolPan, QgsTextAnnotationItem
import  define



class Ui_ChartingGrid(object):
    def setupUi(self, Form):
        Form.setObjectName(("Form"))
        Form.resize(473, 580)
        font = QtGui.QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        Form.setFont(font)

        self.vlForm = QtGui.QVBoxLayout(Form)
        self.vlForm.setObjectName(("vlForm"))
        self.vlForm.setSpacing(0)
        self.vlForm.setMargin(0)

        self.gbParameters = GroupBox(Form)
        self.gbParameters.Caption = "Parameters"
        self.vlForm.addWidget(self.gbParameters)

        self.chbDrawRectangle = CheckBox(self.gbParameters)
        self.chbDrawRectangle.Caption = "Draw Rectangle"
        # self.chbDrawRectangle.Visible = False
        self.gbParameters.Add = self.chbDrawRectangle

        self.pnlMinorLinesTickLength = DistanceBoxPanel(self.gbParameters, DistanceUnits.M)
        self.pnlMinorLinesTickLength.Caption = "Minor Lines Tick Length"
        # self.pnlMinorLinesTickLength.Visible = False
        self.gbParameters.Add = self.pnlMinorLinesTickLength

        self.pnlMinorLines = Frame(self.gbParameters, "HL")
        # self.pnlMinorLines.Visible = False
        self.gbParameters.Add = self.pnlMinorLines

        self.cmbMinorLines = ComboBoxPanel(self.pnlMinorLines)
        self.cmbMinorLines.Caption = "Minor Lines"
        self.pnlMinorLines.Add = self.cmbMinorLines

        self.txtMinorLinesEvery = NumberBoxPanel(self.pnlMinorLines, "0.0")
        self.txtMinorLinesEvery.LabelWidth = 0
        self.txtMinorLinesEvery.Value = 1
        self.pnlMinorLines.Add = self.txtMinorLinesEvery

        self.pnlIntermediateLinesTickLength = DistanceBoxPanel(self.gbParameters, DistanceUnits.M)
        self.pnlIntermediateLinesTickLength.Caption = "Intermediate Lines Tick Length"
        # self.pnlIntermediateLinesTickLength.Visible = False
        self.gbParameters.Add = self.pnlIntermediateLinesTickLength

        self.pnlIntermediateLines = Frame(self.gbParameters, "HL")
        # self.pnlIntermediateLines.Visible = False
        self.gbParameters.Add = self.pnlIntermediateLines

        self.cmbIntermediateLines = ComboBoxPanel(self.pnlIntermediateLines)
        self.cmbIntermediateLines.Caption = "Intermediate Lines"
        self.pnlIntermediateLines.Add = self.cmbIntermediateLines

        self.txtIntermediateLinesEvery = NumberBoxPanel(self.pnlIntermediateLines, "0.0")
        self.txtIntermediateLinesEvery.LabelWidth = 0
        self.txtIntermediateLinesEvery.Value = 5
        self.pnlIntermediateLines.Add = self.txtIntermediateLinesEvery

        self.pnlMajorLinesTickLength = DistanceBoxPanel(self.gbParameters, DistanceUnits.M)
        self.pnlMajorLinesTickLength.Caption = "Major Lines Tick Length"
        self.gbParameters.Add = self.pnlMajorLinesTickLength


        self.pnlMajorLines = Frame(self.gbParameters, "HL")
        # self.pnlMajorLines.Visible = False
        self.gbParameters.Add = self.pnlMajorLines

        self.cmbMajorLines = ComboBoxPanel(self.pnlMajorLines)
        self.cmbMajorLines.Caption = "Major Lines"
        self.pnlMajorLines.Add = self.cmbMajorLines

        self.txtMajorLinesEvery = NumberBoxPanel(self.pnlMajorLines, "0.0")
        self.txtMajorLinesEvery.LabelWidth = 0
        self.txtMajorLinesEvery.Value = 10
        self.pnlMajorLines.Add = self.txtMajorLinesEvery

        self.pnlLonFormat = ComboBoxPanel(self.gbParameters)
        self.pnlLonFormat.Caption = "Longitude Text Format"
        self.gbParameters.Add = self.pnlLonFormat

        self.pnlLatFormat = Frame(self.gbParameters, "HL")
        self.gbParameters.Add = self.pnlLatFormat

        self.cmbLatFormat = ComboBoxPanel(self.pnlLatFormat)
        self.cmbLatFormat.Caption = "Latitude Text Format"
        self.pnlLatFormat.Add = self.cmbLatFormat

        self.chbMultiline = CheckBox(self.pnlLatFormat)
        self.chbMultiline.Caption = "Multiline"
        self.pnlLatFormat.Add = self.chbMultiline

        self.pnlTextHeight = NumberBoxPanel(self.gbParameters, "0")
        self.pnlTextHeight.Caption = "Text Height"
        self.pnlTextHeight.Value = 6
        self.gbParameters.Add = self.pnlTextHeight

        self.pnlMapScale = MapScalePanel(self.gbParameters, MapScaleDropDownType.All)
        self.pnlMapScale.Caption = "Eventual Map Scale"
        self.gbParameters.Add = self.pnlMapScale


        self.gbArea = GroupBox(Form, "HL")
        self.gbArea.Caption = "Rectangular Grid Area"
        self.vlForm.addWidget(self.gbArea)

        self.frameAreaPosition = Frame(self.gbArea)
        self.gbArea.Add = self.frameAreaPosition

        self.pnlUR = PositionPanel(self.frameAreaPosition, None, None, "Degree")
        self.pnlUR.Caption = "Upper Right Corner"
        self.pnlUR.hideframe_Altitude()
        self.pnlUR.btnCalculater.setVisible(False)
        self.pnlUR.btnCapture.setVisible(False)
        self.pnlUR.groupBox.setEnabled(False)
        self.frameAreaPosition.Add = self.pnlUR

        self.pnlLL = PositionPanel(self.frameAreaPosition, None, None, "Degree")
        self.pnlLL.Caption = "Lower Left Corner"
        self.pnlLL.hideframe_Altitude()
        self.pnlLL.btnCalculater.setVisible(False)
        self.pnlLL.btnCapture.setVisible(False)
        self.pnlLL.groupBox.setEnabled(False)
        self.frameAreaPosition.Add = self.pnlLL

        self.btnPickArea = QtGui.QPushButton(self.gbArea)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnPickArea.sizePolicy().hasHeightForWidth())
        self.btnPickArea.setSizePolicy(sizePolicy)
        self.btnPickArea.setMinimumSize(QtCore.QSize(25, 0))
        self.btnPickArea.setMaximumSize(QtCore.QSize(25, 16777215))
        self.btnPickArea.setText((""))
        self.btnPickArea.setObjectName("btnCapture")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(("Resource/coordinate_capture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPickArea.setIcon(icon)
        self.gbArea.Add = self.btnPickArea











