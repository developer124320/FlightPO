# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HoldingRnav.ui'
#
# Created: Wed Nov 25 16:19:08 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel

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

class Ui_Form_HoldingRnav(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(473, 580)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        Form.setFont(font)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbWaypoint = QtGui.QGroupBox(Form)
        self.gbWaypoint.setObjectName(_fromUtf8("gbWaypoint"))
        self.vl_gbWaypoint = QtGui.QVBoxLayout(self.gbWaypoint)
        self.vl_gbWaypoint.setObjectName(_fromUtf8("vl_gbWaypoint"))
        self.verticalLayout.addWidget(self.gbWaypoint)
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
        self.cmbHoldingFunctionality = QtGui.QComboBox(self.frame_58)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbHoldingFunctionality.sizePolicy().hasHeightForWidth())
        self.cmbHoldingFunctionality.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbHoldingFunctionality.setFont(font)
        self.cmbHoldingFunctionality.setObjectName(_fromUtf8("cmbHoldingFunctionality"))
        self.horizontalLayout_58.addWidget(self.cmbHoldingFunctionality)
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
        self.cmbOutboundLimit = QtGui.QComboBox(self.frame_OutBoundLimit)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOutboundLimit.sizePolicy().hasHeightForWidth())
        self.cmbOutboundLimit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbOutboundLimit.setFont(font)
        self.cmbOutboundLimit.setObjectName(_fromUtf8("cmbOutboundLimit"))
        self.horizontalLayout_59.addWidget(self.cmbOutboundLimit)
        self.vl_gbParameters.addWidget(self.frame_OutBoundLimit)
        self.frame_59 = QtGui.QFrame(self.gbParameters)
        self.frame_59.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_59.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_59.setObjectName(_fromUtf8("frame_59"))
        self.horizontalLayout_61 = QtGui.QHBoxLayout(self.frame_59)
        self.horizontalLayout_61.setSpacing(0)
        self.horizontalLayout_61.setMargin(0)
        self.horizontalLayout_61.setObjectName(_fromUtf8("horizontalLayout_61"))
        self.label_69 = QtGui.QLabel(self.frame_59)
        self.label_69.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_69.setFont(font)
        self.label_69.setObjectName(_fromUtf8("label_69"))
        self.horizontalLayout_61.addWidget(self.label_69)
        self.cmbAircraftCategory = QtGui.QComboBox(self.frame_59)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbAircraftCategory.sizePolicy().hasHeightForWidth())
        self.cmbAircraftCategory.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbAircraftCategory.setFont(font)
        self.cmbAircraftCategory.setObjectName(_fromUtf8("cmbAircraftCategory"))
        self.horizontalLayout_61.addWidget(self.cmbAircraftCategory)
        self.vl_gbParameters.addWidget(self.frame_59)
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
        self.txtIas = QtGui.QLineEdit(self.frame_61)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtIas.setFont(font)
        self.txtIas.setObjectName(_fromUtf8("txtIas"))
        self.horizontalLayout_60.addWidget(self.txtIas)
        self.vl_gbParameters.addWidget(self.frame_61)
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
        self.txtAltitudeM = QtGui.QLineEdit(self.frame_62)
        self.txtAltitudeM.setObjectName(_fromUtf8("txtAltitudeM"))
        self.horizontalLayout_69.addWidget(self.txtAltitudeM)
        self.label_2 = QtGui.QLabel(self.frame_62)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_69.addWidget(self.label_2)
        self.txtAltitude = QtGui.QLineEdit(self.frame_62)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtAltitude.setFont(font)
        self.txtAltitude.setObjectName(_fromUtf8("txtAltitude"))
        self.horizontalLayout_69.addWidget(self.txtAltitude)
        self.label = QtGui.QLabel(self.frame_62)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_69.addWidget(self.label)
        self.vl_gbParameters.addWidget(self.frame_62)
        self.frame_63 = QtGui.QFrame(self.gbParameters)
        self.frame_63.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_63.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_63.setObjectName(_fromUtf8("frame_63"))
        self.horizontalLayout_72 = QtGui.QHBoxLayout(self.frame_63)
        self.horizontalLayout_72.setSpacing(0)
        self.horizontalLayout_72.setMargin(0)
        self.horizontalLayout_72.setObjectName(_fromUtf8("horizontalLayout_72"))
        self.label_80 = QtGui.QLabel(self.frame_63)
        self.label_80.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_80.setFont(font)
        self.label_80.setObjectName(_fromUtf8("label_80"))
        self.horizontalLayout_72.addWidget(self.label_80)
        self.txtIsa = QtGui.QLineEdit(self.frame_63)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtIsa.setFont(font)
        self.txtIsa.setObjectName(_fromUtf8("txtIsa"))
        self.horizontalLayout_72.addWidget(self.txtIsa)
        self.btnIasHelp = QtGui.QPushButton(self.frame_61)

        self.frame_Tas = QtGui.QFrame(self.gbParameters)
        self.frame_Tas.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_Tas.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_Tas.setObjectName(_fromUtf8("frame_Tas"))
        self.horizontalLayout_Tas = QtGui.QHBoxLayout(self.frame_Tas)
        self.horizontalLayout_Tas.setSpacing(0)
        self.horizontalLayout_Tas.setMargin(0)
        self.horizontalLayout_Tas.setObjectName(_fromUtf8("horizontalLayout_Tas"))
        self.label_Tas = QtGui.QLabel(self.frame_Tas)
        self.label_Tas.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_Tas.setFont(font)
        self.label_Tas.setObjectName(_fromUtf8("label_Tas"))
        self.horizontalLayout_Tas.addWidget(self.label_Tas)
        self.txtTas = QtGui.QLineEdit(self.frame_Tas)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtTas.setFont(font)
        self.txtTas.setObjectName(_fromUtf8("txtTas"))
        self.horizontalLayout_Tas.addWidget(self.txtTas)
        self.vl_gbParameters.addWidget(self.frame_Tas)

        self.btnIasHelp.setText(_fromUtf8("?"))
        self.btnIasHelp.setObjectName(_fromUtf8("btnIasHelp"))
        self.btnIasHelp.setFixedWidth(23)
        self.horizontalLayout_60.addWidget(self.btnIasHelp)
        self.vl_gbParameters.addWidget(self.frame_63)
        self.frame_Time = QtGui.QFrame(self.gbParameters)
        self.frame_Time.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_Time.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_Time.setObjectName(_fromUtf8("frame_Time"))
        self.horizontalLayout_73 = QtGui.QHBoxLayout(self.frame_Time)
        self.horizontalLayout_73.setSpacing(0)
        self.horizontalLayout_73.setMargin(0)
        self.horizontalLayout_73.setObjectName(_fromUtf8("horizontalLayout_73"))
        self.label_81 = QtGui.QLabel(self.frame_Time)
        self.label_81.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_81.setFont(font)
        self.label_81.setObjectName(_fromUtf8("label_81"))
        self.horizontalLayout_73.addWidget(self.label_81)
        self.txtTime = QtGui.QLineEdit(self.frame_Time)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtTime.setFont(font)
        self.txtTime.setObjectName(_fromUtf8("txtTime"))
        self.horizontalLayout_73.addWidget(self.txtTime)
        self.vl_gbParameters.addWidget(self.frame_Time)
        self.frame_Length = QtGui.QFrame(self.gbParameters)
        self.frame_Length.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_Length.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_Length.setObjectName(_fromUtf8("frame_Length"))
        self.horizontalLayout_65 = QtGui.QHBoxLayout(self.frame_Length)
        self.horizontalLayout_65.setSpacing(0)
        self.horizontalLayout_65.setMargin(0)
        self.horizontalLayout_65.setObjectName(_fromUtf8("horizontalLayout_65"))
        self.label_73 = QtGui.QLabel(self.frame_Length)
        self.label_73.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_73.setFont(font)
        self.label_73.setObjectName(_fromUtf8("label_73"))
        self.horizontalLayout_65.addWidget(self.label_73)
        self.frame_APV_8 = QtGui.QFrame(self.frame_Length)
        self.frame_APV_8.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_APV_8.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_APV_8.setObjectName(_fromUtf8("frame_APV_8"))
        self.horizontalLayout_12 = QtGui.QHBoxLayout(self.frame_APV_8)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setMargin(0)
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.txtLength = QtGui.QLineEdit(self.frame_APV_8)
        self.txtLength.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtLength.setFont(font)
        self.txtLength.setObjectName(_fromUtf8("txtLength"))
        self.horizontalLayout_12.addWidget(self.txtLength)
        self.btnCaptureLength = QtGui.QToolButton(self.frame_APV_8)
        self.btnCaptureLength.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/coordinate_capture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCaptureLength.setIcon(icon)
        self.btnCaptureLength.setObjectName(_fromUtf8("btnCaptureLength"))
        self.horizontalLayout_12.addWidget(self.btnCaptureLength)
        self.horizontalLayout_65.addWidget(self.frame_APV_8)
        self.vl_gbParameters.addWidget(self.frame_Length)
        self.frame_Distance = QtGui.QFrame(self.gbParameters)
        self.frame_Distance.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_Distance.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_Distance.setObjectName(_fromUtf8("frame_Distance"))
        self.horizontalLayout_64 = QtGui.QHBoxLayout(self.frame_Distance)
        self.horizontalLayout_64.setSpacing(0)
        self.horizontalLayout_64.setMargin(0)
        self.horizontalLayout_64.setObjectName(_fromUtf8("horizontalLayout_64"))
        self.label_72 = QtGui.QLabel(self.frame_Distance)
        self.label_72.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_72.setFont(font)
        self.label_72.setObjectName(_fromUtf8("label_72"))
        self.horizontalLayout_64.addWidget(self.label_72)
        self.frame_APV_7 = QtGui.QFrame(self.frame_Distance)
        self.frame_APV_7.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_APV_7.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_APV_7.setObjectName(_fromUtf8("frame_APV_7"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout(self.frame_APV_7)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setMargin(0)
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.txtDistance = QtGui.QLineEdit(self.frame_APV_7)
        self.txtDistance.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtDistance.setFont(font)
        self.txtDistance.setObjectName(_fromUtf8("txtDistance"))
        self.horizontalLayout_11.addWidget(self.txtDistance)
        self.btnCaptureDistance = QtGui.QToolButton(self.frame_APV_7)
        self.btnCaptureDistance.setText(_fromUtf8(""))
        self.btnCaptureDistance.setIcon(icon)
        self.btnCaptureDistance.setObjectName(_fromUtf8("btnCaptureDistance"))
        self.horizontalLayout_11.addWidget(self.btnCaptureDistance)
        self.horizontalLayout_64.addWidget(self.frame_APV_7)
        self.vl_gbParameters.addWidget(self.frame_Distance)
        self.frame_69 = QtGui.QFrame(self.gbParameters)
        self.frame_69.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_69.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_69.setObjectName(_fromUtf8("frame_69"))
        self.horizontalLayout_74 = QtGui.QHBoxLayout(self.frame_69)
        self.horizontalLayout_74.setSpacing(0)
        self.horizontalLayout_74.setMargin(0)
        self.horizontalLayout_74.setObjectName(_fromUtf8("horizontalLayout_74"))
        self.label_82 = QtGui.QLabel(self.frame_69)
        self.label_82.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_82.setFont(font)
        self.label_82.setObjectName(_fromUtf8("label_82"))
        self.horizontalLayout_74.addWidget(self.label_82)
        self.txtMoc = QtGui.QLineEdit(self.frame_69)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtMoc.setFont(font)
        self.txtMoc.setObjectName(_fromUtf8("txtMoc"))
        self.horizontalLayout_74.addWidget(self.txtMoc)
        self.label_6 = QtGui.QLabel(self.frame_69)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_74.addWidget(self.label_6)
        self.txtMocFt = QtGui.QLineEdit(self.frame_69)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtMocFt.setFont(font)
        self.txtMocFt.setText(_fromUtf8(""))
        self.txtMocFt.setObjectName(_fromUtf8("txtMocFt"))
        self.horizontalLayout_74.addWidget(self.txtMocFt)
        self.labelMocFt = QtGui.QLabel(self.frame_69)
        self.labelMocFt.setObjectName(_fromUtf8("labelMocFt"))
        self.horizontalLayout_74.addWidget(self.labelMocFt)
        self.vl_gbParameters.addWidget(self.frame_69)
        self.chbCatH = QtGui.QCheckBox(self.gbParameters)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chbCatH.setFont(font)
        self.chbCatH.setObjectName(_fromUtf8("chbCatH"))
        self.vl_gbParameters.addWidget(self.chbCatH)
        self.gbEntryAreas = QtGui.QGroupBox(self.gbParameters)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.gbEntryAreas.setFont(font)
        self.gbEntryAreas.setObjectName(_fromUtf8("gbEntryAreas"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gbEntryAreas)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.frame_Limitation = QtGui.QFrame(self.gbEntryAreas)
        self.frame_Limitation.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_Limitation.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_Limitation.setObjectName(_fromUtf8("frame_Limitation"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_Limitation)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.chbIntercept = QtGui.QCheckBox(self.frame_Limitation)
        self.chbIntercept.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chbIntercept.setFont(font)
        self.chbIntercept.setObjectName(_fromUtf8("chbIntercept"))
        self.horizontalLayout_2.addWidget(self.chbIntercept)
        self.chbSector1 = QtGui.QCheckBox(self.frame_Limitation)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chbSector1.setFont(font)
        self.chbSector1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chbSector1.setObjectName(_fromUtf8("chbSector1"))
        self.horizontalLayout_2.addWidget(self.chbSector1)
        self.chbSector2 = QtGui.QCheckBox(self.frame_Limitation)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chbSector2.setFont(font)
        self.chbSector2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chbSector2.setObjectName(_fromUtf8("chbSector2"))
        self.horizontalLayout_2.addWidget(self.chbSector2)
        self.chbSectors12 = QtGui.QCheckBox(self.frame_Limitation)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chbSectors12.setFont(font)
        self.chbSectors12.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chbSectors12.setObjectName(_fromUtf8("chbSectors12"))
        self.horizontalLayout_2.addWidget(self.chbSectors12)
        self.chbSector3 = QtGui.QCheckBox(self.frame_Limitation)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chbSector3.setFont(font)
        self.chbSector3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chbSector3.setObjectName(_fromUtf8("chbSector3"))
        self.horizontalLayout_2.addWidget(self.chbSector3)
        self.verticalLayout_4.addWidget(self.frame_Limitation)
        self.vl_gbParameters.addWidget(self.gbEntryAreas)
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
        self.cmbConstruction = QtGui.QComboBox(self.frame_66)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbConstruction.sizePolicy().hasHeightForWidth())
        self.cmbConstruction.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbConstruction.setFont(font)
        self.cmbConstruction.setObjectName(_fromUtf8("cmbConstruction"))
        self.horizontalLayout_75.addWidget(self.cmbConstruction)
        self.vl_gbParameters.addWidget(self.frame_66)
        self.frame_Time_2 = QtGui.QFrame(self.gbParameters)
        self.frame_Time_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_Time_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_Time_2.setObjectName(_fromUtf8("frame_Time_2"))
        self.horizontalLayout_76 = QtGui.QHBoxLayout(self.frame_Time_2)
        self.horizontalLayout_76.setSpacing(0)
        self.horizontalLayout_76.setMargin(0)
        self.horizontalLayout_76.setObjectName(_fromUtf8("horizontalLayout_76"))
        self.label_84 = QtGui.QLabel(self.frame_Time_2)
        self.label_84.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_84.setFont(font)
        self.label_84.setObjectName(_fromUtf8("label_84"))
        self.horizontalLayout_76.addWidget(self.label_84)
        self.txtTime_2 = QtGui.QLineEdit(self.frame_Time_2)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtTime_2.setFont(font)
        self.txtTime_2.setObjectName(_fromUtf8("txtTime_2"))
        self.horizontalLayout_76.addWidget(self.txtTime_2)
        self.vl_gbParameters.addWidget(self.frame_Time_2)
        self.verticalLayout.addWidget(self.gbParameters)
        self.gbOrientation = QtGui.QGroupBox(Form)
        self.gbOrientation.setObjectName(_fromUtf8("gbOrientation"))
        self.vl_gbOrientation = QtGui.QVBoxLayout(self.gbOrientation)
        self.vl_gbOrientation.setObjectName(_fromUtf8("vl_gbOrientation"))

        self.txtTrack = TrackRadialBoxPanel(self.gbOrientation)
        self.txtTrack.Caption = "In-bound Track"
        self.vl_gbOrientation.addWidget(self.txtTrack)
        # # self.frame_TrackFrom = QtGui.QFrame(self.gbOrientation)
        # # self.frame_TrackFrom.setFrameShape(QtGui.QFrame.NoFrame)
        # # self.frame_TrackFrom.setFrameShadow(QtGui.QFrame.Raised)
        # # self.frame_TrackFrom.setObjectName(_fromUtf8("frame_TrackFrom"))
        # # self.horizontalLayout_63 = QtGui.QHBoxLayout(self.frame_TrackFrom)
        # # self.horizontalLayout_63.setSpacing(0)
        # # self.horizontalLayout_63.setMargin(0)
        # # self.horizontalLayout_63.setObjectName(_fromUtf8("horizontalLayout_63"))
        # # self.label_71 = QtGui.QLabel(self.frame_TrackFrom)
        # # self.label_71.setMinimumSize(QtCore.QSize(240, 0))
        # # font = QtGui.QFont()
        # # font.setBold(False)
        # # font.setWeight(50)
        # # self.label_71.setFont(font)
        # # self.label_71.setObjectName(_fromUtf8("label_71"))
        # # self.horizontalLayout_63.addWidget(self.label_71)
        # # self.frame_APV_6 = QtGui.QFrame(self.frame_TrackFrom)
        # self.frame_APV_6.setFrameShape(QtGui.QFrame.StyledPanel)
        # self.frame_APV_6.setFrameShadow(QtGui.QFrame.Raised)
        # self.frame_APV_6.setObjectName(_fromUtf8("frame_APV_6"))
        # self.horizontalLayout_10 = QtGui.QHBoxLayout(self.frame_APV_6)
        # self.horizontalLayout_10.setSpacing(0)
        # self.horizontalLayout_10.setMargin(0)
        # self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        # self.txtTrack = QtGui.QLineEdit(self.frame_APV_6)
        # self.txtTrack.setEnabled(True)
        # font = QtGui.QFont()
        # font.setBold(False)
        # font.setWeight(50)
        # self.txtTrack.setFont(font)
        # self.txtTrack.setObjectName(_fromUtf8("txtTrack"))
        # self.horizontalLayout_10.addWidget(self.txtTrack)
        # self.btnCaptureTrack = QtGui.QToolButton(self.frame_APV_6)
        # self.btnCaptureTrack.setText(_fromUtf8(""))
        # self.btnCaptureTrack.setIcon(icon)
        # self.btnCaptureTrack.setObjectName(_fromUtf8("btnCaptureTrack"))
        # self.horizontalLayout_10.addWidget(self.btnCaptureTrack)
        # self.horizontalLayout_63.addWidget(self.frame_APV_6)
        # self.vl_gbOrientation.addWidget(self.frame_TrackFrom)
        self.frame_67 = QtGui.QFrame(self.gbOrientation)
        self.frame_67.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_67.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_67.setObjectName(_fromUtf8("frame_67"))
        self.horizontalLayout_67 = QtGui.QHBoxLayout(self.frame_67)
        self.horizontalLayout_67.setSpacing(0)
        self.horizontalLayout_67.setMargin(0)
        self.horizontalLayout_67.setObjectName(_fromUtf8("horizontalLayout_67"))
        self.label_75 = QtGui.QLabel(self.frame_67)
        self.label_75.setMinimumSize(QtCore.QSize(240, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_75.setFont(font)
        self.label_75.setObjectName(_fromUtf8("label_75"))
        self.horizontalLayout_67.addWidget(self.label_75)
        self.cmbOrientation = QtGui.QComboBox(self.frame_67)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrientation.sizePolicy().hasHeightForWidth())
        self.cmbOrientation.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbOrientation.setFont(font)
        self.cmbOrientation.setObjectName(_fromUtf8("cmbOrientation"))
        self.horizontalLayout_67.addWidget(self.cmbOrientation)
        self.vl_gbOrientation.addWidget(self.frame_67)
        self.verticalLayout.addWidget(self.gbOrientation)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.gbWaypoint.setTitle(_translate("Form", "Waypoint", None))
        self.gbParameters.setTitle(_translate("Form", "Parameters", None))
        self.label_66.setText(_translate("Form", "Holding Functionality Required:", None))
        self.label_67.setText(_translate("Form", "Out-bound Leg Limitation:", None))
        self.label_69.setText(_translate("Form", "Aircraft Category:", None))
        self.label_68.setText(_translate("Form", "IAS (kts):", None))
        self.txtIas.setText(_translate("Form", "250", None))
        self.label_77.setText(_translate("Form", "Altitude:", None))
        self.label_2.setText(_translate("Form", "m", None))
        self.txtAltitude.setText(_translate("Form", "1000", None))
        self.label.setText(_translate("Form", "ft", None))
        self.label_80.setText(_translate("Form", "ISA (C):", None))
        self.txtIsa.setText(_translate("Form", "15", None))
        self.label_81.setText(_translate("Form", "Time (min):", None))
        self.txtTime.setText(_translate("Form", "1", None))
        self.label_73.setText(_translate("Form", "Length(nm):", None))
        self.txtLength.setText(_translate("Form", "4", None))
        self.label_72.setText(_translate("Form", "Distance(nm):", None))
        self.txtDistance.setText(_translate("Form", "0", None))
        self.label_82.setText(_translate("Form", "Moc:", None))
        self.txtMoc.setText(_translate("Form", "300", None))
        self.label_6.setText(_translate("Form", "m", None))
        self.labelMocFt.setText(_translate("Form", "ft", None))
        self.chbCatH.setText(_translate("Form", "Cat. H ( linear MOC reduction up to 2NM )", None))
        self.gbEntryAreas.setTitle(_translate("Form", "Entry Areas", None))
        self.chbIntercept.setText(_translate("Form", "70 Intercept", None))
        self.chbSector1.setText(_translate("Form", "Sector 1 ", None))
        self.chbSector2.setText(_translate("Form", "Sector 2", None))
        self.chbSectors12.setText(_translate("Form", "Sectors 1 & 2", None))
        self.chbSector3.setText(_translate("Form", "Sectors 3", None))
        self.label_83.setText(_translate("Form", "Construction Type:", None))
        self.label_84.setText(_translate("Form", "Time (min):", None))
        self.txtTime_2.setText(_translate("Form", "1", None))
        self.gbOrientation.setTitle(_translate("Form", "Orientation", None))
        # self.label_71.setText(_translate("Form", "In-bound Track ():", None))
        # self.txtTrack.setText(_translate("Form", "0", None))
        self.label_75.setText(_translate("Form", "Turns:", None))
        self.label_Tas.setText(_translate("Form", "TAS (kts):", None))

