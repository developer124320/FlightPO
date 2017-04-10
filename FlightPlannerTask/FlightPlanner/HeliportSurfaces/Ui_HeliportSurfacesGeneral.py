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
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel


class Ui_HeliportSurfacesGeneral(object):
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

        self.gbFato = GroupBox(Form)
        self.gbFato.Caption = "Final Approach && Take Off area (FATO)"
        self.vlForm.addWidget(self.gbFato)

        self.pnlRunwayGroup = Frame(self.gbFato, "HL")
        self.gbFato.Add = self.pnlRunwayGroup

        self.pnlFato = ComboBoxPanel(self.pnlRunwayGroup, False, True)
        self.pnlFato.Caption = ""
        self.pnlFato.LabelWidth = 15
        self.pnlRunwayGroup.Add = self.pnlFato

        self.btnFatoAdd = QtGui.QPushButton(self.pnlRunwayGroup)
        self.btnFatoAdd.setObjectName("btnFatoAdd")
        self.btnFatoAdd.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnFatoAdd.setIcon(icon)
        self.pnlRunwayGroup.Add = self.btnFatoAdd

        self.btnFatoModify = QtGui.QPushButton(self.pnlRunwayGroup)
        self.btnFatoModify.setObjectName("btnFatoModify")
        self.btnFatoModify.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/mIconEditableEdits.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnFatoModify.setIcon(icon)
        self.pnlRunwayGroup.Add = self.btnFatoModify

        self.btnFatoRemove = QtGui.QPushButton(self.pnlRunwayGroup)
        self.btnFatoRemove.setObjectName("btnFatoRemove")
        self.btnFatoRemove.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnFatoRemove.setIcon(icon)
        self.pnlRunwayGroup.Add = self.btnFatoRemove

        self.gbParameters = GroupBox(Form)
        self.gbParameters.Caption = "Parameters"
        self.vlForm.addWidget(self.gbParameters)

        self.pnlTurningTakeOffTrack = TrackRadialBoxPanel(self.gbParameters)
        self.pnlTurningTakeOffTrack.Caption = "Turning Take-off Climb In-bound Track"
        self.pnlTurningTakeOffTrack.LabelWidth = 230
        self.gbParameters.Add = self.pnlTurningTakeOffTrack

        self.pnlTurningTakeOffCenter = PositionPanel(self.gbParameters)
        self.pnlTurningTakeOffCenter.Caption = "Turning Take-off Climb Center Position"
        self.pnlTurningTakeOffCenter.hideframe_Altitude()
        self.pnlTurningTakeOffCenter.btnCalculater.setVisible(False)
        self.gbParameters.Add = self.pnlTurningTakeOffCenter

        self.pnlTurningTakeOff = ComboBoxPanel(self.gbParameters)
        self.pnlTurningTakeOff.Caption = "Take-off Climb Surface Involving a Turn"
        self.pnlTurningTakeOff.LabelWidth = 230
        self.gbParameters.Add = self.pnlTurningTakeOff

        self.pnlTurningApproachTrack = TrackRadialBoxPanel(self.gbParameters)
        self.pnlTurningApproachTrack.Caption = "Turning Approach In-bound Track"
        self.pnlTurningApproachTrack.LabelWidth = 230
        self.gbParameters.Add = self.pnlTurningApproachTrack

        self.pnlTurningApproachCenter = PositionPanel(self.gbParameters)
        self.pnlTurningApproachCenter.Caption = "Turning Approach Center Position"
        self.pnlTurningApproachCenter.hideframe_Altitude()
        self.pnlTurningApproachCenter.btnCalculater.setVisible(False)
        self.gbParameters.Add = self.pnlTurningApproachCenter

        self.pnlTurningApproach = ComboBoxPanel(self.gbParameters)
        self.pnlTurningApproach.Caption = "Approach Surface Involving a Turn"
        self.pnlTurningApproach.LabelWidth = 230
        self.gbParameters.Add = self.pnlTurningApproach

        self.pnlSlopeCategory = ComboBoxPanel(self.gbParameters)
        self.pnlSlopeCategory.Caption = "Slope Category"
        self.pnlSlopeCategory.LabelWidth = 230
        self.gbParameters.Add = self.pnlSlopeCategory

        self.pnlUsage = ComboBoxPanel(self.gbParameters)
        self.pnlUsage.Caption = "Usage"
        self.pnlUsage.LabelWidth = 230
        self.gbParameters.Add = self.pnlUsage

        self.pnlHeightAboveFATO = ComboBoxPanel(self.gbParameters)
        self.pnlHeightAboveFATO.Caption = "Height Above FATO"
        self.pnlHeightAboveFATO.LabelWidth = 230
        self.gbParameters.Add = self.pnlHeightAboveFATO

        self.pnlApproachAngle = ComboBoxPanel(self.gbParameters)
        self.pnlApproachAngle.Caption = "Approach Angle"
        self.pnlApproachAngle.LabelWidth = 230
        self.gbParameters.Add = self.pnlApproachAngle

        self.pnlApproachType = ComboBoxPanel(self.gbParameters)
        self.pnlApproachType.Caption = "Approach Type"
        self.pnlApproachType.LabelWidth = 230
        self.gbParameters.Add = self.pnlApproachType

        self.pnlCriteriaGroup = Frame(self.gbParameters, "HL")
        self.gbParameters.Add = self.pnlCriteriaGroup

        self.pnlCriteria = ComboBoxPanel(self.pnlCriteriaGroup, False, True)
        self.pnlCriteria.Caption = "Criteria"
        self.pnlCriteria.LabelWidth = 70
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

        self.gbConstruction = GroupBox(Form)
        self.gbConstruction.Caption = "Construction"
        self.vlForm.addWidget(self.gbConstruction)

        self.pnlMarkAltitudes = Frame(self.gbConstruction, "HL")
        self.gbConstruction.Add = self.pnlMarkAltitudes

        self.chbMarkAltitudes = CheckBox(self.pnlMarkAltitudes)
        self.chbMarkAltitudes.Caption = "Mark Contour Altitudes"
        self.pnlMarkAltitudes.Add = self.chbMarkAltitudes

        self.pnlAltitudesEvery = AltitudeBoxPanel(self.pnlMarkAltitudes)
        self.pnlAltitudesEvery.CaptionUnits = "m"
        self.pnlAltitudesEvery.Caption = "Every"
        self.pnlAltitudesEvery.Value = Altitude(15)
        self.pnlAltitudesEvery.LabelWidth = 62
        self.pnlMarkAltitudes.Add = self.pnlAltitudesEvery

        self.pnlConstructionType = ComboBoxPanel(self.gbConstruction)
        self.pnlConstructionType.Caption = "Construction Type"
        self.pnlConstructionType.LabelWidth = 230
        self.gbConstruction.Add = self.pnlConstructionType




