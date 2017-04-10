# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_IlsBasic.ui'
#
# Created: Mon Mar 07 14:03:43 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.AltitudeBoxPanel import Altitude,AltitudeBoxPanel
from FlightPlanner.Panels.AngleGradientBoxPanel import AngleGradientBoxPanel, AngleGradientSlopeUnits, AngleGradientSlope

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

class Ui_IlsBasic(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(366, 261)
        self.form = Form
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.tabCtrlGeneral = QtGui.QTabWidget(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.tabCtrlGeneral.setFont(font)
        self.tabCtrlGeneral.setAutoFillBackground(False)
        self.tabCtrlGeneral.setStyleSheet(_fromUtf8(""))
        self.tabCtrlGeneral.setObjectName(_fromUtf8("tabCtrlGeneral"))
        self.verticalLayout.addWidget(self.tabCtrlGeneral)

        self.tabInputData = QtGui.QWidget(self.tabCtrlGeneral)
        self.tabInputData.setObjectName(_fromUtf8("tabInputData"))

        self.vLayoutTabInputData = QtGui.QVBoxLayout(self.tabInputData)
        self.vLayoutTabInputData.setMargin(3)
        self.vLayoutTabInputData.setObjectName(_fromUtf8("vLayoutTabInputData"))
        self.tabCtrlGeneral.addTab(self.tabInputData, "Input Data")

        self.tabIls = QtGui.QWidget(self.tabCtrlGeneral)
        self.tabIls.setObjectName(_fromUtf8("tabOasIls"))
        self.vLayoutTabIls = QtGui.QHBoxLayout(self.tabIls)
        self.vLayoutTabIls.setMargin(3)
        self.vLayoutTabIls.setObjectName(_fromUtf8("vLayoutTabIls"))
        self.tabCtrlGeneral.addTab(self.tabIls, "ILS Basic")

        self.cmbAerodrome = ComboBoxPanel(self.tabInputData, True)
        self.cmbAerodrome.Caption = "Aerodrome"
        self.cmbAerodrome.LabelWidth = 120
        self.vLayoutTabInputData.addWidget(self.cmbAerodrome)

        self.cmbRwyDir = ComboBoxPanel(self.tabInputData, True)
        self.cmbRwyDir.Caption = "Runway Direction"
        self.cmbRwyDir.LabelWidth = 120
        self.cmbRwyDir.Width = 120
        self.vLayoutTabInputData.addWidget(self.cmbRwyDir)

        self.pnlThr = PositionPanel(self.tabInputData)
        self.pnlThr.groupBox.setTitle("Threshold Position")
        self.pnlThr.setObjectName("positionThr")
        self.pnlThr.btnCalculater.hide()
        self.vLayoutTabInputData.addWidget(self.pnlThr)

        self.pnlRwyEnd = PositionPanel(self.tabInputData)
        self.pnlRwyEnd.groupBox.setTitle("Runway End Position")
        self.pnlRwyEnd.btnCalculater.setVisible(False)
        self.pnlRwyEnd.hideframe_Altitude()
        self.vLayoutTabInputData.addWidget(self.pnlRwyEnd)

        self.txtTrack = TrackRadialBoxPanel(self.tabInputData)
        self.txtTrack.Caption = "In-bound Track"
        self.txtTrack.LabelWidth = 120
        self.vLayoutTabInputData.addWidget(self.txtTrack)


        self.grbParameters = QtGui.QGroupBox(self.tabIls)
        self.grbParameters.setObjectName(_fromUtf8("grbParameters"))
        self.vLayout_grbParameters = QtGui.QVBoxLayout(self.grbParameters)
        self.vLayout_grbParameters.setObjectName(_fromUtf8("vLayout_grbParameters"))

        self.cmbGPA = ComboBoxPanel(self.grbParameters)
        self.cmbGPA.Caption = "Glide Path Angle"
        self.vLayout_grbParameters.addWidget(self.cmbGPA)

        self.txtRDH = AltitudeBoxPanel(self.grbParameters)
        self.txtRDH.CaptionUnits = "m"
        self.txtRDH.Caption = "ILS RDH at Threshold"
        self.txtRDH.Value = Altitude(15)
        self.vLayout_grbParameters.addWidget(self.txtRDH)

        self.cmbSelectionMode = ComboBoxPanel(self.grbParameters)
        self.cmbSelectionMode.Caption = "Selection Mode"
        self.vLayout_grbParameters.addWidget(self.cmbSelectionMode)

        self.cmbConstructionType = ComboBoxPanel(self.grbParameters)
        self.cmbConstructionType.Caption = "Construction Type"
        self.vLayout_grbParameters.addWidget(self.cmbConstructionType)

        self.groupBox_3 = QtGui.QGroupBox(self.grbParameters)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setMargin(0)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.frame_8 = QtGui.QFrame(self.groupBox_3)
        self.frame_8.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_8.setObjectName(_fromUtf8("frame_8"))
        self.verticalLayout_14 = QtGui.QVBoxLayout(self.frame_8)
        self.verticalLayout_14.setContentsMargins(6, 0, -1, -1)
        self.verticalLayout_14.setObjectName(_fromUtf8("verticalLayout_14"))

        self.cmbAcCategory = ComboBoxPanel(self.frame_8)
        self.cmbAcCategory.Caption = "Category"
        self.cmbAcCategory.LabelWidth = 194
        self.verticalLayout_14.addWidget(self.cmbAcCategory)

        self.txtHL = AltitudeBoxPanel(self.frame_8)
        self.txtHL.CaptionUnits = "m"
        self.txtHL.Caption = "Height Loss"
        self.txtHL.Value = Altitude(40)
        self.txtHL.LabelWidth = 194
        self.verticalLayout_14.addWidget(self.txtHL)

        self.horizontalLayout_6.addWidget(self.frame_8)
        self.vLayout_grbParameters.addWidget(self.groupBox_3)
        self.vLayoutTabIls.addWidget(self.grbParameters)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.grbParameters.setTitle(_translate("Form", "Parameters", None))
        # self.label_73.setText(_translate("Form", "In-bound Track ():", None))
        # self.txtTrack.setText(_translate("Form", "0", None))
        # self.label_69.setText(_translate("Form", "Glide Path Angle:", None))
        # self.txtRDH.setText(_translate("Form", "15", None))
        # self.label_4.setText(_translate("Form", "ILS RDH at Threshold(m):", None))
        # self.label_68.setText(_translate("Form", "Selection Mode:", None))
        # self.label_8.setText(_translate("Form", "Construction Type:", None))
        self.groupBox_3.setTitle(_translate("Form", "Aircraft", None))
        # self.label_84.setText(_translate("Form", "Category:", None))
        # self.label_85.setText(_translate("Form", "Height Loss (m):", None))
        # self.txtHL.setText(_translate("Form", "40", None))

