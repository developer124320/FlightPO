# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DepartureRnav.ui'
#
# Created: Wed Sep 09 11:40:11 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_DepartureRnav(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(478, 316)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        Form.setFont(font)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbRunway = QtGui.QGroupBox(Form)
        self.gbRunway.setObjectName(_fromUtf8("gbRunway"))
        self.vl_gbRunway = QtGui.QVBoxLayout(self.gbRunway)
        self.vl_gbRunway.setObjectName(_fromUtf8("vl_gbRunway"))
        self.frame_TrackFrom_2 = QtGui.QFrame(self.gbRunway)
        self.frame_TrackFrom_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_TrackFrom_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_TrackFrom_2.setObjectName(_fromUtf8("frame_TrackFrom_2"))
        self.horizontalLayout_66 = QtGui.QHBoxLayout(self.frame_TrackFrom_2)
        self.horizontalLayout_66.setSpacing(0)
        self.horizontalLayout_66.setMargin(0)
        self.horizontalLayout_66.setObjectName(_fromUtf8("horizontalLayout_66"))
        self.label_74 = QtGui.QLabel(self.frame_TrackFrom_2)
        self.label_74.setMinimumSize(QtCore.QSize(240, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_74.setFont(font)
        self.label_74.setObjectName(_fromUtf8("label_74"))
        self.horizontalLayout_66.addWidget(self.label_74)
        self.frame_APV_9 = QtGui.QFrame(self.frame_TrackFrom_2)
        self.frame_APV_9.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_APV_9.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_APV_9.setObjectName(_fromUtf8("frame_APV_9"))
        self.horizontalLayout_13 = QtGui.QHBoxLayout(self.frame_APV_9)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setMargin(0)
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.txtDer = QtGui.QLineEdit(self.frame_APV_9)
        self.txtDer.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtDer.setFont(font)
        self.txtDer.setObjectName(_fromUtf8("txtDer"))
        self.horizontalLayout_13.addWidget(self.txtDer)
        self.btnCaptureDer = QtGui.QToolButton(self.frame_APV_9)
        self.btnCaptureDer.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/coordinate_capture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCaptureDer.setIcon(icon)
        self.btnCaptureDer.setObjectName(_fromUtf8("btnCaptureDer"))
        self.horizontalLayout_13.addWidget(self.btnCaptureDer)
        self.horizontalLayout_66.addWidget(self.frame_APV_9)
        self.vl_gbRunway.addWidget(self.frame_TrackFrom_2)
        self.verticalLayout.addWidget(self.gbRunway)
        self.gbParameters = QtGui.QGroupBox(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.gbParameters.setFont(font)
        self.gbParameters.setObjectName(_fromUtf8("gbParameters"))
        self.vl_gbParameters = QtGui.QVBoxLayout(self.gbParameters)
        self.vl_gbParameters.setObjectName(_fromUtf8("vl_gbParameters"))
        self.frame_58 = QtGui.QFrame(self.gbParameters)
        self.frame_58.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_58.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_58.setObjectName(_fromUtf8("frame_58"))
        self.horizontalLayout_58 = QtGui.QHBoxLayout(self.frame_58)
        self.horizontalLayout_58.setSpacing(0)
        self.horizontalLayout_58.setMargin(0)
        self.horizontalLayout_58.setObjectName(_fromUtf8("horizontalLayout_58"))
        self.label_66 = QtGui.QLabel(self.frame_58)
        self.label_66.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_66.setFont(font)
        self.label_66.setObjectName(_fromUtf8("label_66"))
        self.horizontalLayout_58.addWidget(self.label_66)
        self.cmbSensorType = QtGui.QComboBox(self.frame_58)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSensorType.sizePolicy().hasHeightForWidth())
        self.cmbSensorType.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbSensorType.setFont(font)
        self.cmbSensorType.setObjectName(_fromUtf8("cmbSensorType"))
        self.horizontalLayout_58.addWidget(self.cmbSensorType)
        self.vl_gbParameters.addWidget(self.frame_58)
        self.frame_OutBoundLimit = QtGui.QFrame(self.gbParameters)
        self.frame_OutBoundLimit.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_OutBoundLimit.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_OutBoundLimit.setObjectName(_fromUtf8("frame_OutBoundLimit"))
        self.horizontalLayout_59 = QtGui.QHBoxLayout(self.frame_OutBoundLimit)
        self.horizontalLayout_59.setSpacing(0)
        self.horizontalLayout_59.setMargin(0)
        self.horizontalLayout_59.setObjectName(_fromUtf8("horizontalLayout_59"))
        self.label_67 = QtGui.QLabel(self.frame_OutBoundLimit)
        self.label_67.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_67.setFont(font)
        self.label_67.setObjectName(_fromUtf8("label_67"))
        self.horizontalLayout_59.addWidget(self.label_67)
        self.cmbSpecification = QtGui.QComboBox(self.frame_OutBoundLimit)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSpecification.sizePolicy().hasHeightForWidth())
        self.cmbSpecification.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbSpecification.setFont(font)
        self.cmbSpecification.setObjectName(_fromUtf8("cmbSpecification"))
        self.horizontalLayout_59.addWidget(self.cmbSpecification)
        self.vl_gbParameters.addWidget(self.frame_OutBoundLimit)
        self.frame_63 = QtGui.QFrame(self.gbParameters)
        self.frame_63.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_63.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_63.setObjectName(_fromUtf8("frame_63"))
        self.horizontalLayout_70 = QtGui.QHBoxLayout(self.frame_63)
        self.horizontalLayout_70.setSpacing(0)
        self.horizontalLayout_70.setMargin(0)
        self.horizontalLayout_70.setObjectName(_fromUtf8("horizontalLayout_70"))
        self.label_78 = QtGui.QLabel(self.frame_63)
        self.label_78.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_78.setFont(font)
        self.label_78.setObjectName(_fromUtf8("label_78"))
        self.horizontalLayout_70.addWidget(self.label_78)
        self.cmbDmeCount = QtGui.QComboBox(self.frame_63)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbDmeCount.sizePolicy().hasHeightForWidth())
        self.cmbDmeCount.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbDmeCount.setFont(font)
        self.cmbDmeCount.setObjectName(_fromUtf8("cmbDmeCount"))
        self.horizontalLayout_70.addWidget(self.cmbDmeCount)
        self.vl_gbParameters.addWidget(self.frame_63)
        self.chbCatH = QtGui.QCheckBox(self.gbParameters)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chbCatH.setFont(font)
        self.chbCatH.setObjectName(_fromUtf8("chbCatH"))
        self.vl_gbParameters.addWidget(self.chbCatH)
        self.frame_62 = QtGui.QFrame(self.gbParameters)
        self.frame_62.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_62.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_62.setObjectName(_fromUtf8("frame_62"))
        self.horizontalLayout_69 = QtGui.QHBoxLayout(self.frame_62)
        self.horizontalLayout_69.setSpacing(0)
        self.horizontalLayout_69.setMargin(0)
        self.horizontalLayout_69.setObjectName(_fromUtf8("horizontalLayout_69"))
        self.label_77 = QtGui.QLabel(self.frame_62)
        self.label_77.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_77.setFont(font)
        self.label_77.setObjectName(_fromUtf8("label_77"))
        self.horizontalLayout_69.addWidget(self.label_77)
        self.txtMoc = QtGui.QLineEdit(self.frame_62)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtMoc.setFont(font)
        self.txtMoc.setObjectName(_fromUtf8("txtMoc"))
        self.horizontalLayout_69.addWidget(self.txtMoc)
        self.vl_gbParameters.addWidget(self.frame_62)
        self.frame_61 = QtGui.QFrame(self.gbParameters)
        self.frame_61.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_61.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_61.setObjectName(_fromUtf8("frame_61"))
        self.horizontalLayout_60 = QtGui.QHBoxLayout(self.frame_61)
        self.horizontalLayout_60.setSpacing(0)
        self.horizontalLayout_60.setMargin(0)
        self.horizontalLayout_60.setObjectName(_fromUtf8("horizontalLayout_60"))
        self.label_68 = QtGui.QLabel(self.frame_61)
        self.label_68.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_68.setFont(font)
        self.label_68.setObjectName(_fromUtf8("label_68"))
        self.horizontalLayout_60.addWidget(self.label_68)
        self.txtPdg = QtGui.QLineEdit(self.frame_61)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtPdg.setFont(font)
        self.txtPdg.setObjectName(_fromUtf8("txtPdg"))
        self.horizontalLayout_60.addWidget(self.txtPdg)
        self.vl_gbParameters.addWidget(self.frame_61)
        self.frame_66 = QtGui.QFrame(self.gbParameters)
        self.frame_66.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_66.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_66.setObjectName(_fromUtf8("frame_66"))
        self.horizontalLayout_75 = QtGui.QHBoxLayout(self.frame_66)
        self.horizontalLayout_75.setSpacing(0)
        self.horizontalLayout_75.setMargin(0)
        self.horizontalLayout_75.setObjectName(_fromUtf8("horizontalLayout_75"))
        self.label_83 = QtGui.QLabel(self.frame_66)
        self.label_83.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_83.setFont(font)
        self.label_83.setObjectName(_fromUtf8("label_83"))
        self.horizontalLayout_75.addWidget(self.label_83)
        self.cmbConstruct = QtGui.QComboBox(self.frame_66)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbConstruct.sizePolicy().hasHeightForWidth())
        self.cmbConstruct.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbConstruct.setFont(font)
        self.cmbConstruct.setObjectName(_fromUtf8("cmbConstruct"))
        self.horizontalLayout_75.addWidget(self.cmbConstruct)
        self.vl_gbParameters.addWidget(self.frame_66)
        self.frame_67 = QtGui.QFrame(self.gbParameters)
        self.frame_67.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_67.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_67.setObjectName(_fromUtf8("frame_67"))
        self.horizontalLayout_76 = QtGui.QHBoxLayout(self.frame_67)
        self.horizontalLayout_76.setSpacing(0)
        self.horizontalLayout_76.setMargin(0)
        self.horizontalLayout_76.setObjectName(_fromUtf8("horizontalLayout_76"))
        self.label_84 = QtGui.QLabel(self.frame_67)
        self.label_84.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_84.setFont(font)
        self.label_84.setObjectName(_fromUtf8("label_84"))
        self.horizontalLayout_76.addWidget(self.label_84)
        self.mocSpinBox = QtGui.QSpinBox(self.frame_67)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mocSpinBox.sizePolicy().hasHeightForWidth())
        self.mocSpinBox.setSizePolicy(sizePolicy)
        self.mocSpinBox.setObjectName(_fromUtf8("mocSpinBox"))
        self.mocSpinBox.setMinimum(1)
        self.horizontalLayout_76.addWidget(self.mocSpinBox)
        self.vl_gbParameters.addWidget(self.frame_67)
        self.verticalLayout.addWidget(self.gbParameters)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.gbRunway.setTitle(_translate("Form", "Runway", None))
        self.label_74.setText(_translate("Form", "Direction ():", None))
        self.txtDer.setText(_translate("Form", "0", None))
        self.gbParameters.setTitle(_translate("Form", "Parameters", None))
        self.label_66.setText(_translate("Form", "Sensor Type:", None))
        self.label_67.setText(_translate("Form", "Rnav Specification:", None))
        self.label_78.setText(_translate("Form", "Number of DMEs Used:", None))
        self.chbCatH.setText(_translate("Form", "Cat. H", None))
        self.label_77.setText(_translate("Form", "MOC(%):", None))
        self.txtMoc.setText(_translate("Form", "0.8", None))
        self.label_68.setText(_translate("Form", "PDG(%):", None))
        self.txtPdg.setText(_translate("Form", "3.3", None))
        self.label_83.setText(_translate("Form", "Construction Type:", None))
        self.label_84.setText(_translate("Form", "MOCmultiplier:", None))

