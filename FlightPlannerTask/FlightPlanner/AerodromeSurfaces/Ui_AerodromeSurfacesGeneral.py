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
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel, Altitude
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.CheckBox import CheckBox


class Ui_AerodromeSurfacesGeneral(object):
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

        self.gbRunway = GroupBox(Form)
        self.gbRunway.Caption = "Runway"
        self.vlForm.addWidget(self.gbRunway)

        self.pnlRunwayGroup = Frame(self.gbRunway, "HL")
        self.gbRunway.Add = self.pnlRunwayGroup

        self.pnlRunway = ComboBoxPanel(self.pnlRunwayGroup, False, True)
        self.pnlRunway.Caption = ""
        self.pnlRunway.LabelWidth = 0
        self.pnlRunwayGroup.Add = self.pnlRunway

        self.btnRwyAdd = QtGui.QPushButton(self.pnlRunwayGroup)
        self.btnRwyAdd.setObjectName("btnRwyAdd")
        self.btnRwyAdd.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRwyAdd.setIcon(icon)
        self.pnlRunwayGroup.Add = self.btnRwyAdd

        self.btnRwyModify = QtGui.QPushButton(self.pnlRunwayGroup)
        self.btnRwyModify.setObjectName("btnRwyModify")
        self.btnRwyModify.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/mIconEditableEdits.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRwyModify.setIcon(icon)
        self.pnlRunwayGroup.Add = self.btnRwyModify

        self.btnRwyRemove = QtGui.QPushButton(self.pnlRunwayGroup)
        self.btnRwyRemove.setObjectName("btnRwyRemove")
        self.btnRwyRemove.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRwyRemove.setIcon(icon)
        self.pnlRunwayGroup.Add = self.btnRwyRemove

        self.pnlRwyCode = ComboBoxPanel(self.gbRunway)
        self.pnlRwyCode.Caption = "Code"
        self.pnlRwyCode.LabelWidth = 120
        self.gbRunway.Add = self.pnlRwyCode

        self.gbAerodrome = GroupBox(Form)
        self.gbAerodrome.Caption = "Aerodrome"
        self.vlForm.addWidget(self.gbAerodrome)

        self.pnlDatumElevation = ComboBoxPanel(self.gbAerodrome)
        self.pnlDatumElevation.Caption = "Datum Elevation"
        self.pnlDatumElevation.LabelWidth = 120
        self.gbAerodrome.Add = self.pnlDatumElevation

        self.pnlARP = PositionPanel(self.gbAerodrome)
        self.pnlARP.Caption = "Aerodrome Reference Point (ARP)"
        self.pnlARP.btnCalculater.setVisible(False)
        self.gbAerodrome.Add = self.pnlARP

        self.chbLetterF = CheckBox(self.gbAerodrome)
        self.chbLetterF.Caption = "Code Letter 'F'"
        self.gbAerodrome.Add = self.chbLetterF

        self.gbParameters = GroupBox(Form)
        self.gbParameters.Caption = "Parameters"
        self.vlForm.addWidget(self.gbParameters)

        self.pnlCriteriaGroup = Frame(self.gbParameters, "HL")
        self.gbParameters.Add = self.pnlCriteriaGroup

        self.pnlCriteria = ComboBoxPanel(self.pnlCriteriaGroup, False, True)
        self.pnlCriteria.Caption = "Criteria"
        self.pnlCriteria.LabelWidth = 120
        self.pnlCriteriaGroup.Add = self.pnlCriteria

        self.btnCriteriaModify = QtGui.QPushButton(self.pnlCriteriaGroup)
        self.btnCriteriaModify.setObjectName("btnCriteriaModify")
        self.btnCriteriaModify.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/mIconEditableEdits.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCriteriaModify.setIcon(icon)
        self.pnlCriteriaGroup.Add = self.btnCriteriaModify

        self.btnCriteriaRemove = QtGui.QPushButton(self.pnlCriteriaGroup)
        self.btnCriteriaRemove.setObjectName("btnCriteriaRemove")
        self.btnCriteriaRemove.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCriteriaRemove.setIcon(icon)
        self.pnlCriteriaGroup.Add = self.btnCriteriaRemove

        self.pnlApproachType = ComboBoxPanel(self.gbParameters)
        self.pnlApproachType.Caption = "Approach Type"
        self.pnlApproachType.LabelWidth = 120
        self.gbParameters.Add = self.pnlApproachType

        self.pnlApproachObstacleAltitude = AltitudeBoxPanel(self.gbParameters)
        self.pnlApproachObstacleAltitude.CaptionUnits = "m"
        self.pnlApproachObstacleAltitude.Caption = "Approach Obstacle Altitude"
        self.pnlApproachObstacleAltitude.Value = Altitude(15)
        self.pnlApproachObstacleAltitude.LabelWidth = 180
        self.gbParameters.Add = self.pnlApproachObstacleAltitude

        self.chbDepTrackMoreThan15 = CheckBox(self.gbParameters)
        self.chbDepTrackMoreThan15.Caption = "Departure Track Heading Change > 15°"
        self.gbParameters.Add = self.chbDepTrackMoreThan15

        self.chbSecondSlope = CheckBox(self.gbParameters)
        self.chbSecondSlope.Caption = "1.6% Take Off Climb Surface"
        self.gbParameters.Add = self.chbSecondSlope

        self.gbConstruction = GroupBox(Form)
        self.gbConstruction.Caption = "Construction"
        self.vlForm.addWidget(self.gbConstruction)

        self.pnlConstructionType = ComboBoxPanel(self.gbConstruction)
        self.pnlConstructionType.Caption = "Construction Type"
        self.pnlConstructionType.LabelWidth = 120
        self.gbConstruction.Add = self.pnlConstructionType

        self.pnlMarkAltitudes = Frame(self.gbConstruction, "HL")
        self.pnlMarkAltitudes.layoutBoxPanel.setSpacing(50)
        self.gbConstruction.Add = self.pnlMarkAltitudes

        self.chbMarkAltitudes = CheckBox(self.pnlMarkAltitudes)
        self.chbMarkAltitudes.Caption = "Mark Contour Altitudes"
        self.pnlMarkAltitudes.Add = self.chbMarkAltitudes

        self.pnlAltitudesEvery = AltitudeBoxPanel(self.pnlMarkAltitudes)
        self.pnlAltitudesEvery.CaptionUnits = "m"
        self.pnlAltitudesEvery.Caption = "Every"
        self.pnlAltitudesEvery.Value = Altitude(5)
        self.pnlAltitudesEvery.LabelWidth = 70
        self.pnlMarkAltitudes.Add = self.pnlAltitudesEvery