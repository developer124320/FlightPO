# -*- coding: UTF-8 -*-

# Form implementation generated from reading ui file 'VSS.ui'
#
# Created: Fri Apr 25 09:39:28 2014
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.AngleGradientBoxPanel import AngleGradientBoxPanel, AngleGradientSlopeUnits, AngleGradientSlope
from FlightPlanner.Panels.OCAHPanel import OCAHPanel, AltitudeUnits, Altitude
from FlightPlanner.Panels.MCAHPanel import MCAHPanel
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.CheckBox import CheckBox
from FlightPlanner.Panels.DistanceBoxPanel import Distance, DistanceBoxPanel, DistanceUnits
from FlightPlanner.types import OCAHType

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_form_VSS(object):
    def setupUi(self, form_VSS):
        form_VSS.setObjectName(_fromUtf8("form_VSS"))
        form_VSS.resize(375, 372)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        form_VSS.setFont(font)
        self.verticalLayout = QtGui.QVBoxLayout(form_VSS)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.grbRunway = QtGui.QGroupBox(form_VSS)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.grbRunway.setFont(font)
        self.grbRunway.setObjectName(_fromUtf8("grbRunway"))
        self.vLayout_grbRunway = QtGui.QVBoxLayout(self.grbRunway)
        self.vLayout_grbRunway.setObjectName(_fromUtf8("vLayout_grbRunway"))

        self.cmbAerodrome = ComboBoxPanel(self.grbRunway, True)
        self.cmbAerodrome.Caption = "Aerodrome"
        self.cmbAerodrome.LabelWidth = 120
        self.vLayout_grbRunway.addWidget(self.cmbAerodrome)

        self.cmbRwyDir = ComboBoxPanel(self.grbRunway, True)
        self.cmbRwyDir.Caption = "Runway Direction"
        self.cmbRwyDir.LabelWidth = 120
        self.cmbRwyDir.Width = 120
        self.vLayout_grbRunway.addWidget(self.cmbRwyDir)

        self.pnlTHR = PositionPanel(self.grbRunway)
        self.pnlTHR.groupBox.setTitle("Runway Thr")
        self.pnlTHR.btnCalculater.hide()
        self.pnlTHR.setObjectName("positionTHR")
        self.vLayout_grbRunway.addWidget(self.pnlTHR)

        self.pnlRwyEnd = PositionPanel(self.grbRunway)
        self.pnlRwyEnd.groupBox.setTitle("Runway End")
        self.pnlRwyEnd.hideframe_Altitude()
        self.pnlRwyEnd.btnCalculater.hide()
        self.pnlRwyEnd.setObjectName("positionRwyEnd")
        self.vLayout_grbRunway.addWidget(self.pnlRwyEnd)

        self.txtRwyDir = TrackRadialBoxPanel(self.grbRunway)
        self.txtRwyDir.Caption = "Runway In-bound Direction"
        self.txtRwyDir.LabelWidth = 160
        self.vLayout_grbRunway.addWidget(self.txtRwyDir)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/coordinate_capture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.cmbRwyCode = ComboBoxPanel(self.grbRunway)
        self.cmbRwyCode.Caption = "Code"
        self.cmbRwyCode.LabelWidth = 160
        self.vLayout_grbRunway.addWidget(self.cmbRwyCode)

        self.txtStripWidth = DistanceBoxPanel(self.grbRunway, DistanceUnits.M)
        self.txtStripWidth.Caption = "Strip Width"
        self.txtStripWidth.Value = Distance(300)
        self.txtStripWidth.LabelWidth = 160
        self.vLayout_grbRunway.addWidget(self.txtStripWidth)

        self.verticalLayout.addWidget(self.grbRunway)

        self.grbParameters = QtGui.QGroupBox(form_VSS)
        self.grbParameters.setObjectName(_fromUtf8("grbParameters"))
        self.vLayout_grbParameters = QtGui.QVBoxLayout(self.grbParameters)
        self.vLayout_grbParameters.setObjectName(_fromUtf8("vLayout_grbParameters"))

        self.cmbApproachType = ComboBoxPanel(self.grbParameters)
        self.cmbApproachType.Caption = "Approach Type"
        self.cmbApproachType.LabelWidth = 160
        self.vLayout_grbParameters.addWidget(self.cmbApproachType)

        self.txtTrack = TrackRadialBoxPanel(self.grbParameters)
        self.txtTrack.Caption = "In-bound Track"
        self.txtTrack.LabelWidth = 160
        self.vLayout_grbParameters.addWidget(self.txtTrack)

        self.txtThrFaf = DistanceBoxPanel(self.grbParameters, DistanceUnits.NM)
        self.txtThrFaf.Caption = "THR to FAF Distance"
        self.txtThrFaf.Value = Distance(5, DistanceUnits.NM)
        self.txtThrFaf.LabelWidth = 160
        self.vLayout_grbParameters.addWidget(self.txtThrFaf)

        self.txtDescAngle = AngleGradientBoxPanel(self.grbParameters)
        self.txtDescAngle.CaptionUnits = AngleGradientSlopeUnits.Degrees
        self.txtDescAngle.Caption = "Descent Angle"
        self.txtDescAngle.LabelWidth = 160
        self.txtDescAngle.Value = AngleGradientSlope(3, AngleGradientSlopeUnits.Degrees)
        self.vLayout_grbParameters.addWidget(self.txtDescAngle)

        self.pnlOCAH = MCAHPanel(self.grbParameters)
        self.pnlOCAH.lblMCAH.setText("Minimum Altitude (ft):")
        self.pnlOCAH.lblMCAH.setMaximumWidth(160)
        self.pnlOCAH.lblMCAH.setMinimumWidth(160)
        self.pnlOCAH.setValue(Altitude(800, AltitudeUnits.FT))
        self.pnlOCAH.cmbMCAH.clear()
        self.pnlOCAH.cmbMCAH.addItems([OCAHType.OCA, OCAHType.OCH])
        self.vLayout_grbParameters.addWidget(self.pnlOCAH)


        self.cmbConstructionType = ComboBoxPanel(self.grbParameters)
        self.cmbConstructionType.Caption = "Construction Type"
        self.cmbConstructionType.LabelWidth = 160
        self.vLayout_grbParameters.addWidget(self.cmbConstructionType)

        self.chbAdCodeF = CheckBox(self.grbParameters)
        self.chbAdCodeF.Caption = "Aerodrome Code Letter"
        self.vLayout_grbParameters.addWidget(self.chbAdCodeF)

        self.verticalLayout.addWidget(self.grbParameters)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(form_VSS)
        QtCore.QMetaObject.connectSlotsByName(form_VSS)

    def retranslateUi(self, form_VSS):
        form_VSS.setWindowTitle(_translate("form_VSS", "Form", None))
        self.grbRunway.setTitle(_translate("form_VSS", "Runway", None))
        # self.label_69.setText(_translate("form_VSS", "Direction (°):", None))
        # self.txtRwyDir.setText(_translate("form_VSS", "0", None))
        # self.label_66.setText(_translate("form_VSS", "Code :", None))
        # self.label_70.setText(_translate("form_VSS", "Strip Width (m):", None))
        # self.txtStripWidth.setText(_translate("form_VSS", "300", None))
        self.grbParameters.setTitle(_translate("form_VSS", "Parameters", None))
        # self.label_67.setText(_translate("form_VSS", "Approach Type :", None))
        # self.label_71.setText(_translate("form_VSS", "In-bound Track (°):", None))
        # self.txtTrack.setText(_translate("form_VSS", "360", None))
        # self.label_72.setText(_translate("form_VSS", "THR to FAF Distance (nm):", None))
        # self.txtThrFaf.setText(_translate("form_VSS", "5", None))
        # self.label_73.setText(_translate("form_VSS", "Descent Angle (°):", None))
        # self.txtDescAngle.setText(_translate("form_VSS", "3", None))
        # self.label_68.setText(_translate("form_VSS", "Construction Type:", None))
        # self.chbAdCodeF.setText(_translate("form_VSS", "Aerodrome Code Letter \'F\'", None))

