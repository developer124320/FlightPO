# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AAC.ui'
#
# Created: Sun May 18 16:45:46 2014
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

class Ui_Form_AAC(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(413, 224)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        Form.setFont(font)
        self.verticalLayout_AAC = QtGui.QVBoxLayout(Form)
        self.verticalLayout_AAC.setObjectName(_fromUtf8("verticalLayout_AAC"))

        self.cmbAerodrome = ComboBoxPanel(Form, True)
        self.cmbAerodrome.Caption = "Aerodrome"
        self.cmbAerodrome.LabelWidth = 120
        self.verticalLayout_AAC.addWidget(self.cmbAerodrome)

        self.cmbRwyDir = ComboBoxPanel(Form, True)
        self.cmbRwyDir.Caption = "Runway Direction"
        self.cmbRwyDir.LabelWidth = 120
        self.cmbRwyDir.Width = 120
        self.verticalLayout_AAC.addWidget(self.cmbRwyDir)

        self.grbParameters = QtGui.QGroupBox(Form)
        self.grbParameters.setObjectName(_fromUtf8("grbParameters"))
        self.vLayout_grbParameters = QtGui.QVBoxLayout(self.grbParameters)
        self.vLayout_grbParameters.setObjectName(_fromUtf8("vLayout_grbParameters"))

        self.txtDirection = TrackRadialBoxPanel(self.grbParameters)
        self.txtDirection.Caption = "Runway In-bound Direction"
        self.vLayout_grbParameters.addWidget(self.txtDirection)
        # self.frame_ThrFaf = QtGui.QFrame(self.grbParameters)
        # self.frame_ThrFaf.setFrameShape(QtGui.QFrame.NoFrame)
        # self.frame_ThrFaf.setFrameShadow(QtGui.QFrame.Raised)
        # self.frame_ThrFaf.setObjectName(_fromUtf8("frame_ThrFaf"))
        # self.horizontalLayout_65 = QtGui.QHBoxLayout(self.frame_ThrFaf)
        # self.horizontalLayout_65.setSpacing(0)
        # self.horizontalLayout_65.setMargin(0)
        # self.horizontalLayout_65.setObjectName(_fromUtf8("horizontalLayout_65"))
        # self.label_73 = QtGui.QLabel(self.frame_ThrFaf)
        # sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.label_73.sizePolicy().hasHeightForWidth())
        # self.label_73.setSizePolicy(sizePolicy)
        # self.label_73.setMinimumSize(QtCore.QSize(170, 0))
        # font = QtGui.QFont()
        # font.setBold(False)
        # font.setWeight(50)
        # self.label_73.setFont(font)
        # self.label_73.setObjectName(_fromUtf8("label_73"))
        # self.horizontalLayout_65.addWidget(self.label_73)
        # self.frame_APV_9 = QtGui.QFrame(self.frame_ThrFaf)
        # self.frame_APV_9.setFrameShape(QtGui.QFrame.StyledPanel)
        # self.frame_APV_9.setFrameShadow(QtGui.QFrame.Raised)
        # self.frame_APV_9.setObjectName(_fromUtf8("frame_APV_9"))
        # self.horizontalLayout_13 = QtGui.QHBoxLayout(self.frame_APV_9)
        # self.horizontalLayout_13.setSpacing(0)
        # self.horizontalLayout_13.setMargin(0)
        # self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        # self.txtDirection = QtGui.QLineEdit(self.frame_APV_9)
        # self.txtDirection.setEnabled(True)
        # font = QtGui.QFont()
        # font.setBold(False)
        # font.setWeight(50)
        # self.txtDirection.setFont(font)
        # self.txtDirection.setObjectName(_fromUtf8("txtDirection"))
        # self.horizontalLayout_13.addWidget(self.txtDirection)
        # self.btnCaptureDir = QtGui.QToolButton(self.frame_APV_9)
        # self.btnCaptureDir.setText(_fromUtf8(""))
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/coordinate_capture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.btnCaptureDir.setIcon(icon)
        # self.btnCaptureDir.setObjectName(_fromUtf8("btnCaptureDir"))
        # self.horizontalLayout_13.addWidget(self.btnCaptureDir)
        # self.horizontalLayout_65.addWidget(self.frame_APV_9)
        # self.vLayout_grbParameters.addWidget(self.frame_ThrFaf)
        self.frame_60 = QtGui.QFrame(self.grbParameters)
        self.frame_60.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_60.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_60.setObjectName(_fromUtf8("frame_60"))
        self.horizontalLayout_61 = QtGui.QHBoxLayout(self.frame_60)
        self.horizontalLayout_61.setSpacing(0)
        self.horizontalLayout_61.setMargin(0)
        self.horizontalLayout_61.setObjectName(_fromUtf8("horizontalLayout_61"))
        self.label_69 = QtGui.QLabel(self.frame_60)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_69.sizePolicy().hasHeightForWidth())
        self.label_69.setSizePolicy(sizePolicy)
        self.label_69.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_69.setFont(font)
        self.label_69.setObjectName(_fromUtf8("label_69"))
        self.horizontalLayout_61.addWidget(self.label_69)
        self.cmbCategory = QtGui.QComboBox(self.frame_60)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbCategory.sizePolicy().hasHeightForWidth())
        self.cmbCategory.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbCategory.setFont(font)
        self.cmbCategory.setObjectName(_fromUtf8("cmbCategory"))
        self.cmbCategory.setMinimumSize(QtCore.QSize(100, 0))
        self.cmbCategory.setMaximumSize(QtCore.QSize(100, 121221))
        self.horizontalLayout_61.addWidget(self.cmbCategory)
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_61.addItem(horizontalSpacer)
        self.vLayout_grbParameters.addWidget(self.frame_60)
        self.verticalLayout_AAC.addWidget(self.grbParameters)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.grbParameters.setTitle(_translate("Form", "Parameters", None))
        # self.label_73.setText(_translate("Form", "Runway In-bound Direction (°):", None))
#         self.txtDirection.setText(_translate("Form", "5", None))
        self.label_69.setText(_translate("Form", "Aircraft Category:", None))

