# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PinsApp.ui'
#
# Created: Wed Apr 23 14:12:14 2014
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.AngleGradientBoxPanel import AngleGradientBoxPanel, AngleGradientSlopeUnits, AngleGradientSlope
from FlightPlanner.Panels.OCAHPanel import OCAHPanel, AltitudeUnits, Altitude
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.CheckBox import CheckBox
from FlightPlanner.Panels.DistanceBoxPanel import Distance, DistanceBoxPanel, DistanceUnits


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

class Ui_PinsApp(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(515, 570)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_20 = QtGui.QGroupBox(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_20.setFont(font)
        self.groupBox_20.setObjectName(_fromUtf8("groupBox_20"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_20)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))

        self.cmbSegmentType = ComboBoxPanel(self.groupBox_20)
        self.cmbSegmentType.Caption = "Visual Segment Type"
        self.cmbSegmentType.LabelWidth = 250
        self.verticalLayout_5.addWidget(self.cmbSegmentType)

        self.cmbApproachType = ComboBoxPanel(self.groupBox_20)
        self.cmbApproachType.Caption = "Approach Type"
        self.cmbApproachType.LabelWidth = 250
        self.verticalLayout_5.addWidget(self.cmbApproachType)

        self.txtVSDG = AngleGradientBoxPanel(self.groupBox_20)
        self.txtVSDG.CaptionUnits = AngleGradientSlopeUnits.Degrees
        self.txtVSDG.Caption = "Visual Segment Design Gradient [VSDG]"
        self.txtVSDG.LabelWidth = 250
        self.txtVSDG.Value = AngleGradientSlope(8.3, AngleGradientSlopeUnits.Degrees)
        self.verticalLayout_5.addWidget(self.txtVSDG)

        self.txtApproachSurfaceTrack = TrackRadialBoxPanel(self.groupBox_20)
        self.txtApproachSurfaceTrack.Caption = "In-bound Approach Surface Track"
        self.verticalLayout_5.addWidget(self.txtApproachSurfaceTrack)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/coordinate_capture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.txtMOC = AltitudeBoxPanel(self.groupBox_20)
        self.txtMOC.CaptionUnits = "m"
        self.txtMOC.Caption = "MOC"
        self.txtMOC.Value = Altitude(75)
        self.txtMOC.LabelWidth = 250
        self.verticalLayout_5.addWidget(self.txtMOC)

        self.frame_Limitation = QtGui.QFrame(self.groupBox_20)
        self.frame_Limitation.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_Limitation.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_Limitation.setObjectName(_fromUtf8("frame_Limitation"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_Limitation)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))

        self.chbLeftFlyOverProhibited = CheckBox(self.frame_Limitation)
        self.chbLeftFlyOverProhibited.Caption = "Left fly-over prohibited"
        self.horizontalLayout_2.addWidget(self.chbLeftFlyOverProhibited)

        self.chbRightFlyOverProhibited = CheckBox(self.frame_Limitation)
        self.chbRightFlyOverProhibited.Caption = "Right fly-over prohibited"
        self.horizontalLayout_2.addWidget(self.chbRightFlyOverProhibited)

        self.verticalLayout_5.addWidget(self.frame_Limitation)

        self.grbIDF = QtGui.QGroupBox(self.groupBox_20)
        self.grbIDF.setObjectName(_fromUtf8("grbIDF"))
        self.verticalLayout_IDF = QtGui.QVBoxLayout(self.grbIDF)
        self.verticalLayout_IDF.setObjectName(_fromUtf8("verticalLayout_IDF"))

        self.txtTrackTo = TrackRadialBoxPanel(self.grbIDF)
        self.txtTrackTo.Caption = "Track To"
        self.txtTrackTo.LabelWidth = 100
        self.verticalLayout_IDF.addWidget(self.txtTrackTo)

        self.frame_Tolerance = QtGui.QFrame(self.grbIDF)
        self.frame_Tolerance.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_Tolerance.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_Tolerance.setObjectName(_fromUtf8("frame_Tolerance"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_Tolerance)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame_2 = QtGui.QFrame(self.frame_Tolerance)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))

        self.frame_TrackFrom_2 = QtGui.QFrame(self.frame_2)
        self.frame_TrackFrom_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_TrackFrom_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_TrackFrom_2.setObjectName(_fromUtf8("frame_TrackFrom_2"))
        self.horizontalLayout_70 = QtGui.QHBoxLayout(self.frame_TrackFrom_2)
        self.horizontalLayout_70.setSpacing(0)
        self.horizontalLayout_70.setMargin(0)
        self.horizontalLayout_70.setObjectName(_fromUtf8("horizontalLayout_70"))
        self.label_78 = QtGui.QLabel(self.frame_TrackFrom_2)
        self.label_78.setMinimumSize(QtCore.QSize(240, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_78.setFont(font)
        self.label_78.setObjectName(_fromUtf8("label_78"))
        self.horizontalLayout_70.addWidget(self.label_78)
        self.frame_APV_12 = QtGui.QFrame(self.frame_TrackFrom_2)
        self.frame_APV_12.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_APV_12.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_APV_12.setObjectName(_fromUtf8("frame_APV_12"))
        self.horizontalLayout_16 = QtGui.QHBoxLayout(self.frame_APV_12)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setMargin(0)
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.txtAtt = QtGui.QLineEdit(self.frame_APV_12)
        self.txtAtt.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtAtt.setFont(font)
        self.txtAtt.setObjectName(_fromUtf8("txtAtt"))
        self.txtAtt.setMinimumWidth(50)
        self.txtAtt.setMaximumWidth(50)
        self.horizontalLayout_16.addWidget(self.txtAtt)
        self.horizontalLayout_70.addWidget(self.frame_APV_12)
        self.verticalLayout_3.addWidget(self.frame_TrackFrom_2)
        self.frame_TrackFrom_3 = QtGui.QFrame(self.frame_2)
        self.frame_TrackFrom_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_TrackFrom_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_TrackFrom_3.setObjectName(_fromUtf8("frame_TrackFrom_3"))
        self.horizontalLayout_71 = QtGui.QHBoxLayout(self.frame_TrackFrom_3)
        self.horizontalLayout_71.setSpacing(0)
        self.horizontalLayout_71.setMargin(0)
        self.horizontalLayout_71.setObjectName(_fromUtf8("horizontalLayout_71"))
        self.label_79 = QtGui.QLabel(self.frame_TrackFrom_3)
        self.label_79.setMinimumSize(QtCore.QSize(240, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_79.setFont(font)
        self.label_79.setObjectName(_fromUtf8("label_79"))
        self.horizontalLayout_71.addWidget(self.label_79)
        self.frame_APV_13 = QtGui.QFrame(self.frame_TrackFrom_3)
        self.frame_APV_13.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_APV_13.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_APV_13.setObjectName(_fromUtf8("frame_APV_13"))
        self.horizontalLayout_17 = QtGui.QHBoxLayout(self.frame_APV_13)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setMargin(0)
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        self.txtAsw = QtGui.QLineEdit(self.frame_APV_13)
        self.txtAsw.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtAsw.setFont(font)
        self.txtAsw.setObjectName(_fromUtf8("txtAsw"))
        self.txtAsw.setMinimumWidth(50)
        self.txtAsw.setMaximumWidth(50)
        self.horizontalLayout_17.addWidget(self.txtAsw)
        self.horizontalLayout_71.addWidget(self.frame_APV_13)
        self.verticalLayout_3.addWidget(self.frame_TrackFrom_3)
        self.horizontalLayout.addWidget(self.frame_2)
        self.btnDropDown = QtGui.QToolButton(self.frame_Tolerance)
        self.btnDropDown.setMaximumSize(QtCore.QSize(16777215, 50))
        self.btnDropDown.setText(_fromUtf8(""))
        self.btnDropDown.setObjectName(_fromUtf8("btnDropDown"))
        self.horizontalLayout.addWidget(self.btnDropDown)
        spacerItem = QtGui.QSpacerItem(0,10,QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_IDF.addWidget(self.frame_Tolerance)

        self.verticalLayout_5.addWidget(self.grbIDF)

        self.grbHRP = QtGui.QGroupBox(self.groupBox_20)
        self.grbHRP.setObjectName(_fromUtf8("grbHRP"))
        self.verticalLayout_HRP = QtGui.QVBoxLayout(self.grbHRP)
        self.verticalLayout_HRP.setObjectName(_fromUtf8("verticalLayout_HRP"))

        self.txtHCH = NumberBoxPanel(self.grbHRP)
        self.txtHCH.CaptionUnits = "m"
        self.txtHCH.Caption = "Crossing Height [HCH]"
        self.txtHCH.LabelWidth = 140
        self.txtHCH.Value = 15
        self.verticalLayout_HRP.addWidget(self.txtHCH)

        self.txtHSAL = DistanceBoxPanel(self.grbHRP, DistanceUnits.M)
        self.txtHSAL.Caption = "Safety Area Length"
        self.txtHSAL.Value = Distance(30)
        self.txtHSAL.LabelWidth = 140
        self.verticalLayout_HRP.addWidget(self.txtHSAL)

        self.txtHSAW = DistanceBoxPanel(self.grbHRP, DistanceUnits.M)
        self.txtHSAW.Caption = "Safety Area Width"
        self.txtHSAW.Value = Distance(30)
        self.txtHSAW.LabelWidth = 140
        self.verticalLayout_HRP.addWidget(self.txtHSAW)

        self.verticalLayout_5.addWidget(self.grbHRP)

        self.cmbConstructionType = ComboBoxPanel(self.groupBox_20)
        self.cmbConstructionType.Caption = "Construction Type"
        self.cmbConstructionType.LabelWidth = 150
        self.verticalLayout_5.addWidget(self.cmbConstructionType)

        self.verticalLayout.addWidget(self.groupBox_20)
        spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox_20.setTitle(_translate("Form", "Parameters", None))
        self.grbIDF.setTitle(_translate("Form", "Missed Approach Point(MAPt)", None))
        self.label_78.setText(_translate("Form", "ATT (nm):", None))
        self.txtAtt.setText(_translate("Form", "180", None))
        self.label_79.setText(_translate("Form", "1/2 A/W (nm):", None))
        self.txtAsw.setText(_translate("Form", "180", None))
        self.grbHRP.setTitle(_translate("Form", "Heliport", None))
