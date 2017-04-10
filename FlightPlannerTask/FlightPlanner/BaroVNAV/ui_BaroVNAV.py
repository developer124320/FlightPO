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
from FlightPlanner.Panels.OCAHPanel import OCAHPanel
from FlightPlanner.Panels.SpeedBoxPanel import SpeedBoxPanel, SpeedUnits, Speed
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits, Distance
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel, Altitude
from FlightPlanner.types import AltitudeUnits
from qgis.gui import QgsMapToolPan, QgsTextAnnotationItem
import  define



class Ui_BaroVNAV(object):
    def setupUi(self, Form):
        Form.setObjectName(("Form"))
        Form.resize(473, 580)
        font = QtGui.QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        Form.setFont(font)

        self.aprAnnotation = QgsTextAnnotationItem(define._canvas)
        self.aprAnnotation.setDocument(QtGui.QTextDocument("ARP"))
        self.aprAnnotation.setFrameSize( QtCore.QSizeF( 30, 20 ) )
        self.aprAnnotation.hide()
        self.thrAnnotation= QgsTextAnnotationItem(define._canvas)
        self.thrAnnotation.setDocument(QtGui.QTextDocument("THR"))
        self.thrAnnotation.setFrameSize( QtCore.QSizeF( 30, 20 ) )
        self.thrAnnotation.hide()

        self.vlForm = QtGui.QVBoxLayout(Form)
        self.vlForm.setObjectName(("vlForm"))
        self.vlForm.setSpacing(0)
        self.vlForm.setMargin(0)

        self.pnlPositions = QtGui.QFrame(Form)
        self.pnlPositions.setObjectName(("pnlPositions"))
        self.hl_pnlPositions = QtGui.QVBoxLayout(self.pnlPositions)
        self.hl_pnlPositions.setObjectName(("hl_pnlPositions"))
        self.hl_pnlPositions.setMargin(0)

        self.cmbAerodrome = ComboBoxPanel(self.pnlPositions, True)
        self.cmbAerodrome.Caption = "Aerodrome"
        self.cmbAerodrome.LabelWidth = 120
        self.hl_pnlPositions.addWidget(self.cmbAerodrome)

        self.cmbRwyDir = ComboBoxPanel(self.pnlPositions, True)
        self.cmbRwyDir.Caption = "Runway Direction"
        self.cmbRwyDir.LabelWidth = 120
        self.cmbRwyDir.Width = 120
        self.hl_pnlPositions.addWidget(self.cmbRwyDir)

        self.gbAerodrome = QtGui.QGroupBox(Form)
        self.gbAerodrome.setObjectName("gbAerodrome")
        self.gbAerodrome.setTitle("Aerodrome")
        self.vl_gbAerodrome = QtGui.QVBoxLayout(self.gbAerodrome)
        self.vl_gbAerodrome.setObjectName("vl_gbAerodrome")

        self.pnlArp = PositionPanel(self.gbAerodrome, self.aprAnnotation)
        self.pnlArp.groupBox.setTitle("Reference Point (ARP)")
        self.pnlArp.btnCalculater.hide()
        self.vl_gbAerodrome.addWidget(self.pnlArp)

        self.pnlMinTemp = NumberBoxPanel(self.gbAerodrome)
        self.pnlMinTemp.CaptionUnits = define._degreeStr
        self.pnlMinTemp.Caption = "Minimum Temperature"
        self.pnlMinTemp.Value = -15
        self.vl_gbAerodrome.addWidget(self.pnlMinTemp)

        self.hl_pnlPositions.addWidget(self.gbAerodrome)

        self.gbRunway = QtGui.QGroupBox(Form)
        self.gbRunway.setObjectName("gbRunway")
        self.gbRunway.setTitle("Runway")
        self.vl_gbRunway = QtGui.QVBoxLayout(self.gbRunway)
        self.vl_gbRunway.setObjectName("vl_gbRunway")

        self.pnlThr = PositionPanel(self.gbRunway, self.thrAnnotation)
        self.pnlThr.groupBox.setTitle("Threshold Position")
        self.pnlThr.btnCalculater.hide()
        self.vl_gbRunway.addWidget(self.pnlThr)

        self.pnlThrEnd = PositionPanel(self.gbRunway, self.thrAnnotation)
        self.pnlThrEnd.groupBox.setTitle("Runway End Position")
        self.pnlThrEnd.btnCalculater.hide()
        self.vl_gbRunway.addWidget(self.pnlThrEnd)
        self.pnlThrEnd.Visible = False

        self.pnlRwyDir = TrackRadialBoxPanel(self.gbRunway)
        self.pnlRwyDir.Caption = "Direction"
        self.pnlRwyDir.LabelWidth = 70
        self.vl_gbRunway.addWidget(self.pnlRwyDir)

        self.hl_pnlPositions.addWidget(self.gbRunway)
        self.vlForm.addWidget(self.pnlPositions)

        self.gbParameters = QtGui.QGroupBox(Form)
        font = QtGui.QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.gbParameters.setFont(font)
        self.gbParameters.setObjectName(("gbParameters"))
        self.gbParameters.setTitle("Parameters")
        self.vl_gbParameters = QtGui.QVBoxLayout(self.gbParameters)
        self.vl_gbParameters.setObjectName(("vl_gbParameters"))

        self.pnlOCAH = OCAHPanel(self.gbParameters)
        self.pnlOCAH.Caption = "Intermediate Segment"
        self.pnlOCAH.Value = Altitude(2000, AltitudeUnits.FT)
        self.pnlOCAH.LabelWidth = 200
        self.vl_gbParameters.addWidget(self.pnlOCAH)

        self.pnlMocI = AltitudeBoxPanel(self.gbParameters)
        self.pnlMocI.CaptionUnits = "m"
        self.pnlMocI.Caption = "Intermediate Segment MOC"
        self.pnlMocI.Value = Altitude(150)
        self.vl_gbParameters.addWidget(self.pnlMocI)

        self.pnlRDH = AltitudeBoxPanel(self.gbParameters)
        self.pnlRDH.CaptionUnits = "m"
        self.pnlRDH.Caption = "RDH at THR"
        self.pnlRDH.Value = Altitude(15)
        self.vl_gbParameters.addWidget(self.pnlRDH)

        self.pnlVPA = ComboBoxPanel(self.gbParameters)
        self.pnlVPA.Caption = "Vertical Path Angle [VPA]"
        # self.pnlVPA.comboBox.setToolTip()
        self.vl_gbParameters.addWidget(self.pnlVPA)

        self.lblAbove35 = QtGui.QLabel(self.gbParameters)
        self.lblAbove35.setText(QtCore.QString("A procedure with a promulgated VPA exceeding 3.5") + unicode("°", "utf-8") + QtCore.QString(" is a non-standard procedure.\nIt shall be subject to an aeronautical study and will require special approval \n    by the national competent authority (PANS-OPS Part III, Section 3, Chapter 4, Par. 4.2.1.3)"))
        self.vl_gbParameters.addWidget(self.lblAbove35)

        self.pnlThrFafDist = DistanceBoxPanel(self.gbParameters, DistanceUnits.NM)
        self.pnlThrFafDist.Caption = "THR to FAWP Distance"
        self.pnlThrFafDist.Value = Distance(5, DistanceUnits.NM)
        self.vl_gbParameters.addWidget(self.pnlThrFafDist)

        self.pnlAcCat = ComboBoxPanel(self.gbParameters)
        self.pnlAcCat.Caption = "Aircraft Category"
        self.vl_gbParameters.addWidget(self.pnlAcCat)

        self.pnlIas = SpeedBoxPanel(self.gbParameters, SpeedUnits.KTS)
        self.pnlIas.Caption = "Max. IAS"
        self.pnlIas.Value = Speed(185)
        self.vl_gbParameters.addWidget(self.pnlIas)

        self.pnlIasAtThr = SpeedBoxPanel(self.gbParameters, SpeedUnits.KTS)
        self.pnlIasAtThr.Caption = "Max. IAS at THR"
        self.pnlIasAtThr.Value = Speed(165)
        self.vl_gbParameters.addWidget(self.pnlIasAtThr)

        self.pnlHL = AltitudeBoxPanel(self.gbParameters)
        self.pnlHL.CaptionUnits = "m"
        self.pnlHL.Caption = "Height Loss"
        self.pnlHL.Value = Altitude(49)
        self.vl_gbParameters.addWidget(self.pnlHL)

        self.pnlTC = AltitudeBoxPanel(self.gbParameters)
        self.pnlTC.CaptionUnits = "m"
        self.pnlTC.Caption = "Temperature Correction"
        self.pnlTC.Value = Altitude(0)
        self.vl_gbParameters.addWidget(self.pnlTC)

        self.tableLayoutPanel1 = QtGui.QFrame(self.gbParameters)
        self.tableLayoutPanel1.setObjectName("tableLayoutPanel1")
        self.vl_tableLayoutPanel1 = QtGui.QVBoxLayout(self.tableLayoutPanel1)
        self.vl_tableLayoutPanel1.setObjectName("vl_tableLayoutPanel1")
        self.vl_tableLayoutPanel1.setSpacing(0)
        self.vl_tableLayoutPanel1.setMargin(0)

        self.upFrame = QtGui.QFrame(self.tableLayoutPanel1)
        self.upFrame.setObjectName("upFrame")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upFrame.sizePolicy().hasHeightForWidth())
        self.upFrame.setSizePolicy(sizePolicy)
        self.hl_upFrame = QtGui.QHBoxLayout(self.upFrame)
        self.hl_upFrame.setObjectName("hl_upFrame")
        self.hl_upFrame.setMargin(0)

        self.cmbTermination = ComboBoxPanel(self.upFrame)
        self.cmbTermination.Caption = "APV Segment Termination"
        self.cmbTermination.comboBox.setMinimumWidth(80)
        self.hl_upFrame.addWidget(self.cmbTermination)

        self.pnlTerminationDist = DistanceBoxPanel(self.upFrame, DistanceUnits.NM)
        self.pnlTerminationDist.Caption = "Dist."
        self.pnlTerminationDist.Value = Distance(5, DistanceUnits.NM)
        self.pnlTerminationDist.LabelWidth = 50
        self.hl_upFrame.addWidget(self.pnlTerminationDist)

        self.vl_tableLayoutPanel1.addWidget(self.upFrame)

        self.downFrame = QtGui.QFrame(self.tableLayoutPanel1)
        self.downFrame.setObjectName("downFrame")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downFrame.sizePolicy().hasHeightForWidth())
        self.downFrame.setSizePolicy(sizePolicy)
        self.hl_downFrame = QtGui.QHBoxLayout(self.downFrame)
        self.hl_downFrame.setObjectName("hl_downFrame")
        self.hl_downFrame.setMargin(0)

        self.cmbMAPt = ComboBoxPanel(self.downFrame)
        self.cmbMAPt.Caption = "Missed Approach Point"
        self.cmbMAPt.comboBox.setMinimumWidth(80)
        self.hl_downFrame.addWidget(self.cmbMAPt)

        self.pnlMAPtDist = DistanceBoxPanel(self.downFrame, DistanceUnits.NM)
        self.pnlMAPtDist.Caption = "Dist."
        # self.pnlMAPtDist.Value = Distance(5, DistanceUnits.NM)
        self.pnlMAPtDist.LabelWidth = 50
        self.hl_downFrame.addWidget(self.pnlMAPtDist)

        self.vl_tableLayoutPanel1.addWidget(self.downFrame)
        self.vl_gbParameters.addWidget(self.tableLayoutPanel1)

        self.pnlMACG = NumberBoxPanel(self.gbParameters)
        self.pnlMACG.CaptionUnits = "%"
        self.pnlMACG.Caption = "Missed Approach Climb Gradient"
        self.pnlMACG.Value = 2.5
        self.vl_gbParameters.addWidget(self.pnlMACG)

        self.pnlMocMA = AltitudeBoxPanel(self.gbParameters)
        self.pnlMocMA.CaptionUnits = "m"
        self.pnlMocMA.Caption = "Missed Approach MOC"
        self.pnlMocMA.Value = Altitude(30)
        self.vl_gbParameters.addWidget(self.pnlMocMA)

        self.pnlEvalMethodMA = ComboBoxPanel(self.gbParameters)
        self.pnlEvalMethodMA.Caption = "Missed Approach Evaluation"
        self.vl_gbParameters.addWidget(self.pnlEvalMethodMA)

        self.pnlConstructionType = ComboBoxPanel(self.gbParameters)
        self.pnlConstructionType.Caption = "Construction Type"
        self.vl_gbParameters.addWidget(self.pnlConstructionType)

        self.vlForm.addWidget(self.gbParameters)
        QtCore.QMetaObject.connectSlotsByName(Form)

