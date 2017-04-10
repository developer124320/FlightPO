# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HoldingRnav.ui'
#
# Created: Wed Nov 25 16:19:08 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QSize
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel, Altitude
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.CheckBox import CheckBox
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.DistanceBoxPanel import DistanceUnits, DistanceBoxPanel, Distance
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.types import AltitudeUnits


class Ui_ShieldingGeneral(object):
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

        self.pnlNavType = ComboBoxPanel(self.gbParameters)
        self.pnlNavType.Caption = "Navigation Type"
        self.pnlNavType.LabelWidth = 120
        self.gbParameters.Add = self.pnlNavType

        self.gbNavAid = GroupBox(Form)
        self.gbNavAid.Caption = "Navigational Aid"
        self.gbParameters.Add = self.gbNavAid

        self.pnlRunwayGroup = Frame(self.gbNavAid, "HL")
        self.gbNavAid.Add = self.pnlRunwayGroup

        self.pnlNavAid = ComboBoxPanel(self.pnlRunwayGroup, False, True)
        self.pnlNavAid.Caption = ""
        self.pnlNavAid.LabelWidth = 0
        self.pnlRunwayGroup.Add = self.pnlNavAid

        self.btnNavAidAdd = QtGui.QPushButton(self.pnlRunwayGroup)
        self.btnNavAidAdd.setObjectName("btnNavAidAdd")
        self.btnNavAidAdd.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNavAidAdd.setIcon(icon)
        self.pnlRunwayGroup.Add = self.btnNavAidAdd

        self.btnNavAidModify = QtGui.QPushButton(self.pnlRunwayGroup)
        self.btnNavAidModify.setObjectName("btnNavAidModify")
        self.btnNavAidModify.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/mIconEditableEdits.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNavAidModify.setIcon(icon)
        self.pnlRunwayGroup.Add = self.btnNavAidModify

        self.btnNavAidRemove = QtGui.QPushButton(self.pnlRunwayGroup)
        self.btnNavAidRemove.setObjectName("btnNavAidRemove")
        self.btnNavAidRemove.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNavAidRemove.setIcon(icon)
        self.pnlRunwayGroup.Add = self.btnNavAidRemove

        self.pnlNavAidPos = PositionPanel(self.gbNavAid)
        self.pnlNavAidPos.Caption = "Position"
        self.pnlNavAidPos.btnCalculater.setVisible(False)
        self.gbNavAid.Add = self.pnlNavAidPos

        self.gbWaypoint1 = GroupBox(self.gbParameters)
        self.gbWaypoint1.Caption = "Waypoint 1"
        self.gbParameters.Add = self.gbWaypoint1

        self.pnlWaypoint1 = PositionPanel(self.gbWaypoint1)
        self.pnlWaypoint1.Caption = ""
        self.pnlWaypoint1.btnCalculater.setVisible(False)
        self.pnlWaypoint1.hideframe_Altitude()
        self.gbWaypoint1.Add = self.pnlWaypoint1

        self.chbTurningWaypoint1 = CheckBox(self.gbWaypoint1)
        self.chbTurningWaypoint1.Caption = "Turning Waypoint"
        self.gbWaypoint1.Add = self.chbTurningWaypoint1

        self.gbWaypoint2 = GroupBox(self.gbParameters)
        self.gbWaypoint2.Caption = "Waypoint 2"
        self.gbParameters.Add = self.gbWaypoint2

        self.pnlWaypoint2 = PositionPanel(self.gbWaypoint2)
        self.pnlWaypoint2.Caption = ""
        self.pnlWaypoint2.btnCalculater.setVisible(False)
        self.pnlWaypoint2.hideframe_Altitude()
        self.gbWaypoint2.Add = self.pnlWaypoint2

        self.chbTurningWaypoint2 = CheckBox(self.gbWaypoint2)
        self.chbTurningWaypoint2.Caption = "Turning Waypoint"
        self.gbWaypoint2.Add = self.chbTurningWaypoint2

        self.pnlTrack = TrackRadialBoxPanel(self.gbParameters)
        self.pnlTrack.Caption = "Track"
        self.pnlTrack.LabelWidth = 150
        self.gbParameters.Add = self.pnlTrack

        self.pnlDistToThr = DistanceBoxPanel(self.gbParameters, DistanceUnits.M)
        self.pnlDistToThr.Caption = "Distance to Threshold"
        self.pnlDistToThr.LabelWidth = 150
        self.gbParameters.Add = self.pnlDistToThr

        self.pnlMinimumAltitude = AltitudeBoxPanel(self.gbParameters)
        self.pnlMinimumAltitude.CaptionUnits = "ft"
        self.pnlMinimumAltitude.Caption = "Minimum Altitude"
        self.pnlMinimumAltitude.Value = Altitude(2000, AltitudeUnits.FT)
        self.pnlMinimumAltitude.LabelWidth = 150
        self.gbParameters.Add = self.pnlMinimumAltitude

        self.pnlSegmentWidth = DistanceBoxPanel(self.gbParameters, DistanceUnits.NM)
        self.pnlSegmentWidth.Caption = "Segment Width"
        self.pnlSegmentWidth.LabelWidth = 150
        self.pnlSegmentWidth.Value = Distance(5, DistanceUnits.NM)
        self.gbParameters.Add = self.pnlSegmentWidth

        self.chbEarthCurvature = CheckBox(self.gbParameters)
        self.chbEarthCurvature.Caption = "Allow for Earth Curvature"
        self.gbParameters.Add = self.chbEarthCurvature

        self.gbConstruction = GroupBox(Form)
        self.gbConstruction.Caption = "Construction"
        self.vlForm.addWidget(self.gbConstruction)

        self.pnlConstructionType = ComboBoxPanel(self.gbConstruction)
        self.pnlConstructionType.Caption = "Construction Type"
        self.pnlConstructionType.LabelWidth = 150
        self.gbConstruction.Add = self.pnlConstructionType

        self.pnlMarkAltitudes = Frame(self.gbConstruction, "HL")
        self.gbConstruction.Add = self.pnlMarkAltitudes

        self.chbMarkAltitudes = CheckBox(self.pnlMarkAltitudes)
        self.chbMarkAltitudes.Caption = "Mark Contour Altitudes"
        self.chbMarkAltitudes.setMinimumSize(QSize(150, 0))
        self.chbMarkAltitudes.setMaximumSize(QSize(150, 16777215))
        self.pnlMarkAltitudes.Add = self.chbMarkAltitudes

        self.pnlMarkAltitudesIn = Frame(self.pnlMarkAltitudes)
        self.pnlMarkAltitudes.Add = self.pnlMarkAltitudesIn

        self.pnlAltitudesEvery = AltitudeBoxPanel(self.pnlMarkAltitudesIn)
        self.pnlAltitudesEvery.CaptionUnits = "m"
        self.pnlAltitudesEvery.Caption = "Every"
        self.pnlAltitudesEvery.Value = Altitude(5)
        # self.pnlAltitudesEvery.LabelWidth = 60
        self.pnlMarkAltitudesIn.Add = self.pnlAltitudesEvery

        self.pnlAltitudesTextHeight = NumberBoxPanel(self.pnlMarkAltitudesIn)
        self.pnlAltitudesTextHeight.Caption = "Text Height"
        self.pnlAltitudesTextHeight.Value = 5
        # self.pnlAltitudesTextHeight.LabelWidth = 60
        self.pnlMarkAltitudesIn.Add = self.pnlAltitudesTextHeight

        self.pnl3DQuality = Frame(self.gbConstruction, "HL")
        self.gbConstruction.Add = self.pnl3DQuality

        self.lbl3DQuality = QtGui.QLabel(self.pnl3DQuality)
        self.lbl3DQuality.setObjectName("lbl3DQuality")
        self.lbl3DQuality.setText("Rendering Quality:")
        self.lbl3DQuality.setMinimumSize(QSize(150, 0))
        self.lbl3DQuality.setMaximumSize(QSize(150, 16777215))
        self.pnl3DQuality.Add = self.lbl3DQuality

        self.pnlTrackbar = Frame(self.pnl3DQuality, "HL")
        self.pnl3DQuality.Add = self.pnlTrackbar

        self.lblCoarse = QtGui.QLabel(self.pnlTrackbar)
        self.lblCoarse.setObjectName("lblCoarse")
        self.lblCoarse.setText("Coarse")
        self.pnlTrackbar.Add = self.lblCoarse
        
        self.trackBar = QtGui.QSlider(self.pnlTrackbar)
        self.trackBar.setObjectName("trackBar")
        self.trackBar.setOrientation(Qt.Horizontal)
        self.trackBar.setMinimum(10)
        self.trackBar.setMaximum(200)
        # self.trackBar.setSingleStep(10)
        self.trackBar.setValue(20)
        self.pnlTrackbar.Add = self.trackBar

        self.lblSmooth = QtGui.QLabel(self.pnlTrackbar)
        self.lblSmooth.setObjectName("lblSmooth")
        self.lblSmooth.setText("Smooth")
        self.pnlTrackbar.Add = self.lblSmooth







