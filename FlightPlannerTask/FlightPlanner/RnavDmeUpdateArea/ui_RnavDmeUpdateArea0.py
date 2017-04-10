# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RnavDmeUpdateArea.ui'
#
# Created: Mon Sep 21 15:49:48 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel

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

class Ui_RnavDmeUpdateAreaDlg(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(350, 166)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        Form.setFont(font)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbDme1 = QtGui.QGroupBox(Form)
        self.gbDme1.setObjectName(_fromUtf8("gbDme1"))
        self.vl_Dme1 = QtGui.QVBoxLayout(self.gbDme1)
        self.vl_Dme1.setObjectName(_fromUtf8("vl_Dme1"))

        self.cmbBasedOn1 = ComboBoxPanel(self.gbDme1, True)
        self.cmbBasedOn1.Caption = "Based On"
        self.cmbBasedOn1.LabelWidth = 120
        self.cmbBasedOn1.Width = 120
        self.vl_Dme1.addWidget(self.cmbBasedOn1)

        self.frame_TakeOffSurfaceTrack_4 = QtGui.QFrame(self.gbDme1)
        self.frame_TakeOffSurfaceTrack_4.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_TakeOffSurfaceTrack_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_TakeOffSurfaceTrack_4.setObjectName(_fromUtf8("frame_TakeOffSurfaceTrack_4"))
        self.horizontalLayout_68 = QtGui.QHBoxLayout(self.frame_TakeOffSurfaceTrack_4)
        self.horizontalLayout_68.setSpacing(0)
        self.horizontalLayout_68.setMargin(0)
        self.horizontalLayout_68.setObjectName(_fromUtf8("horizontalLayout_68"))
        self.label_76 = QtGui.QLabel(self.frame_TakeOffSurfaceTrack_4)
        self.label_76.setMinimumSize(QtCore.QSize(170, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_76.setFont(font)
        self.label_76.setObjectName(_fromUtf8("label_76"))
        self.horizontalLayout_68.addWidget(self.label_76)
        self.frame_APV_8 = QtGui.QFrame(self.frame_TakeOffSurfaceTrack_4)
        self.frame_APV_8.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_APV_8.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_APV_8.setObjectName(_fromUtf8("frame_APV_8"))
        self.horizontalLayout_12 = QtGui.QHBoxLayout(self.frame_APV_8)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setMargin(0)
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.txtDoc1 = QtGui.QLineEdit(self.frame_APV_8)
        self.txtDoc1.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtDoc1.setFont(font)
        self.txtDoc1.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.txtDoc1.setObjectName(_fromUtf8("txtDoc1"))
        self.horizontalLayout_12.addWidget(self.txtDoc1)
        self.btnMesureDoc1 = QtGui.QToolButton(self.frame_APV_8)
        self.btnMesureDoc1.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/coordinate_capture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnMesureDoc1.setIcon(icon)
        self.btnMesureDoc1.setObjectName(_fromUtf8("btnMesureDoc1"))
        self.horizontalLayout_12.addWidget(self.btnMesureDoc1)
        self.horizontalLayout_68.addWidget(self.frame_APV_8)
        self.vl_Dme1.addWidget(self.frame_TakeOffSurfaceTrack_4)
        self.verticalLayout.addWidget(self.gbDme1)
        self.gbDme2 = QtGui.QGroupBox(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        self.gbDme2.setFont(font)
        self.gbDme2.setObjectName(_fromUtf8("gbDme2"))
        self.vl_Dme2 = QtGui.QVBoxLayout(self.gbDme2)
        self.vl_Dme2.setObjectName(_fromUtf8("vl_Dme2"))

        self.cmbBasedOn2 = ComboBoxPanel(self.gbDme2, True)
        self.cmbBasedOn2.Caption = "Based On"
        self.cmbBasedOn2.LabelWidth = 120
        self.cmbBasedOn2.Width = 120
        self.vl_Dme2.addWidget(self.cmbBasedOn2)

        self.frame_TakeOffSurfaceTrack = QtGui.QFrame(self.gbDme2)
        self.frame_TakeOffSurfaceTrack.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_TakeOffSurfaceTrack.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_TakeOffSurfaceTrack.setObjectName(_fromUtf8("frame_TakeOffSurfaceTrack"))
        self.horizontalLayout_61 = QtGui.QHBoxLayout(self.frame_TakeOffSurfaceTrack)
        self.horizontalLayout_61.setSpacing(0)
        self.horizontalLayout_61.setMargin(0)
        self.horizontalLayout_61.setObjectName(_fromUtf8("horizontalLayout_61"))
        self.txtDmeAltitude = QtGui.QLabel(self.frame_TakeOffSurfaceTrack)
        self.txtDmeAltitude.setMinimumSize(QtCore.QSize(170, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtDmeAltitude.setFont(font)
        self.txtDmeAltitude.setObjectName(_fromUtf8("txtDmeAltitude"))
        self.horizontalLayout_61.addWidget(self.txtDmeAltitude)
        self.frame_APV_5 = QtGui.QFrame(self.frame_TakeOffSurfaceTrack)
        self.frame_APV_5.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_APV_5.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_APV_5.setObjectName(_fromUtf8("frame_APV_5"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.frame_APV_5)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setMargin(0)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.txtDoc2 = QtGui.QLineEdit(self.frame_APV_5)
        self.txtDoc2.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtDoc2.setFont(font)
        self.txtDoc2.setObjectName(_fromUtf8("txtDoc2"))
        self.horizontalLayout_9.addWidget(self.txtDoc2)
        self.btnMesureDoc2 = QtGui.QToolButton(self.frame_APV_5)
        self.btnMesureDoc2.setText(_fromUtf8(""))
        self.btnMesureDoc2.setIcon(icon)
        self.btnMesureDoc2.setObjectName(_fromUtf8("btnMesureDoc2"))
        self.horizontalLayout_9.addWidget(self.btnMesureDoc2)
        self.horizontalLayout_61.addWidget(self.frame_APV_5)
        self.vl_Dme2.addWidget(self.frame_TakeOffSurfaceTrack)
        self.verticalLayout.addWidget(self.gbDme2)
        self.frame_MOC = QtGui.QFrame(Form)
        self.frame_MOC.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_MOC.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_MOC.setObjectName(_fromUtf8("frame_MOC"))
        self.horizontalLayout_62 = QtGui.QHBoxLayout(self.frame_MOC)
        self.horizontalLayout_62.setSpacing(0)
        self.horizontalLayout_62.setMargin(0)
        self.horizontalLayout_62.setObjectName(_fromUtf8("horizontalLayout_62"))
        self.label_70 = QtGui.QLabel(self.frame_MOC)
        self.label_70.setMinimumSize(QtCore.QSize(170, 0))
        self.label_70.setMaximumSize(QtCore.QSize(170, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_70.setFont(font)
        self.label_70.setObjectName(_fromUtf8("label_70"))
        self.horizontalLayout_62.addWidget(self.label_70)
        self.cmbConstructionType = QtGui.QComboBox(self.frame_MOC)
        self.cmbConstructionType.setObjectName(_fromUtf8("cmbConstructionType"))
        self.horizontalLayout_62.addWidget(self.cmbConstructionType)
        self.verticalLayout.addWidget(self.frame_MOC)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.gbDme1.setTitle(_translate("Form", "DME 1", None))
        self.label_76.setText(_translate("Form", "Operational Coverage (nm):", None))
        self.txtDoc1.setText(_translate("Form", "200", None))
        self.gbDme2.setTitle(_translate("Form", "DME 2", None))
        self.txtDmeAltitude.setText(_translate("Form", "Operational Coverage (nm):", None))
        self.txtDoc2.setText(_translate("Form", "200", None))
        self.label_70.setText(_translate("Form", "Construction Type:", None))

