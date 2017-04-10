# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BaseTurnTS.ui'
#
# Created: Wed Nov 25 15:21:09 2015
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

class Ui_BaseTurnTS(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(461, 472)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        Form.setFont(font)
        self.verticalLayout_AAC = QtGui.QVBoxLayout(Form)
        self.verticalLayout_AAC.setObjectName(_fromUtf8("verticalLayout_AAC"))

        self.gbNavAid = QtGui.QGroupBox(Form)
        self.gbNavAid.setObjectName(_fromUtf8("gbNavAid"))
        self.verticalLayout_gbNavAid = QtGui.QVBoxLayout(self.gbNavAid)
        self.verticalLayout_gbNavAid.setObjectName(_fromUtf8("verticalLayout_gbNavAid"))

        self.cmbNavAidType = ComboBoxPanel(self.gbNavAid)
        self.cmbNavAidType.Caption = "Type"
        self.cmbNavAidType.LabelWidth = 120
        self.verticalLayout_gbNavAid.addWidget(self.cmbNavAidType)

        self.cmbBasedOn = ComboBoxPanel(self.gbNavAid, True)
        self.cmbBasedOn.Caption = "Based On"
        self.cmbBasedOn.LabelWidth = 120
        self.cmbBasedOn.Width = 120
        self.verticalLayout_gbNavAid.addWidget(self.cmbBasedOn)
        # self.frameType = QtGui.QFrame(self.gbNavAid)
        # self.frameType.setFrameShape(QtGui.QFrame.NoFrame)
        # self.frameType.setFrameShadow(QtGui.QFrame.Raised)
        # self.frameType.setObjectName(_fromUtf8("frameType"))
        # self.horizontalLayout_59 = QtGui.QHBoxLayout(self.frameType)
        # self.horizontalLayout_59.setSpacing(0)
        # self.horizontalLayout_59.setMargin(0)
        # self.horizontalLayout_59.setObjectName(_fromUtf8("horizontalLayout_59"))
        # self.label_67 = QtGui.QLabel(self.frameType)
        # self.label_67.setMinimumSize(QtCore.QSize(140, 0))
        # self.label_67.setMaximumSize(QtCore.QSize(140, 16777215))
        # font = QtGui.QFont()
        # font.setBold(False)
        # font.setWeight(50)
        # self.label_67.setFont(font)
        # self.label_67.setObjectName(_fromUtf8("label_67"))
        # self.horizontalLayout_59.addWidget(self.label_67)
        # self.cmbNavAidType = QtGui.QComboBox(self.frameType)
        # sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.cmbNavAidType.sizePolicy().hasHeightForWidth())
        # self.cmbNavAidType.setSizePolicy(sizePolicy)
        # font = QtGui.QFont()
        # font.setBold(False)
        # font.setWeight(50)
        # self.cmbNavAidType.setFont(font)
        # self.cmbNavAidType.setObjectName(_fromUtf8("cmbNavAidType"))
        # self.horizontalLayout_59.addWidget(self.cmbNavAidType)
        # self.verticalLayout_gbNavAid.addWidget(self.frameType)
        self.verticalLayout_AAC.addWidget(self.gbNavAid)
        self.grbParameters = QtGui.QGroupBox(Form)
        self.grbParameters.setObjectName(_fromUtf8("grbParameters"))
        self.vLayout_grbParameters = QtGui.QVBoxLayout(self.grbParameters)
        self.vLayout_grbParameters.setObjectName(_fromUtf8("vLayout_grbParameters"))
        self.frame_IasIA1 = QtGui.QFrame(self.grbParameters)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_IasIA1.sizePolicy().hasHeightForWidth())
        self.frame_IasIA1.setSizePolicy(sizePolicy)
        self.frame_IasIA1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_IasIA1.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_IasIA1.setObjectName(_fromUtf8("frame_IasIA1"))
        self.horizontalLayout_16 = QtGui.QHBoxLayout(self.frame_IasIA1)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setMargin(0)
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.label_7 = QtGui.QLabel(self.frame_IasIA1)
        self.label_7.setMinimumSize(QtCore.QSize(140, 0))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_16.addWidget(self.label_7)
        self.txtIas = QtGui.QLineEdit(self.frame_IasIA1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtIas.sizePolicy().hasHeightForWidth())
        self.txtIas.setSizePolicy(sizePolicy)
        self.txtIas.setMinimumSize(QtCore.QSize(60, 0))
        self.txtIas.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.txtIas.setFont(font)
        self.txtIas.setObjectName(_fromUtf8("txtIas"))
        self.horizontalLayout_16.addWidget(self.txtIas)
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(horizontalSpacer)
        self.vLayout_grbParameters.addWidget(self.frame_IasIA1)
        self.frameTas = QtGui.QFrame(self.grbParameters)
        self.frameTas.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameTas.setFrameShadow(QtGui.QFrame.Raised)
        self.frameTas.setObjectName(_fromUtf8("frameTas"))
        self.horizontalLayout_69 = QtGui.QHBoxLayout(self.frameTas)
        self.horizontalLayout_69.setSpacing(0)
        self.horizontalLayout_69.setMargin(0)
        self.horizontalLayout_69.setObjectName(_fromUtf8("horizontalLayout_69"))
        self.label_77 = QtGui.QLabel(self.frameTas)
        self.label_77.setMinimumSize(QtCore.QSize(140, 0))
        self.label_77.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_77.setFont(font)
        self.label_77.setObjectName(_fromUtf8("label_77"))
        self.horizontalLayout_69.addWidget(self.label_77)
        self.txtTas = QtGui.QLineEdit(self.frameTas)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtTas.setFont(font)
        self.txtTas.setText(_fromUtf8(""))
        self.txtTas.setObjectName(_fromUtf8("txtTas"))
        self.txtTas.setMinimumSize(QtCore.QSize(90, 0))
        self.txtTas.setMaximumSize(QtCore.QSize(90, 16777215))
        self.horizontalLayout_69.addWidget(self.txtTas)
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_69.addItem(horizontalSpacer)
        self.vLayout_grbParameters.addWidget(self.frameTas)
        self.frame_AltitudeIA1 = QtGui.QFrame(self.grbParameters)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_AltitudeIA1.sizePolicy().hasHeightForWidth())
        self.frame_AltitudeIA1.setSizePolicy(sizePolicy)
        self.frame_AltitudeIA1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_AltitudeIA1.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_AltitudeIA1.setObjectName(_fromUtf8("frame_AltitudeIA1"))
        self.horizontalLayout_27 = QtGui.QHBoxLayout(self.frame_AltitudeIA1)
        self.horizontalLayout_27.setSpacing(0)
        self.horizontalLayout_27.setMargin(0)
        self.horizontalLayout_27.setObjectName(_fromUtf8("horizontalLayout_27"))
        self.label_17 = QtGui.QLabel(self.frame_AltitudeIA1)
        self.label_17.setMinimumSize(QtCore.QSize(140, 0))
        self.label_17.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.label_17.setFont(font)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.horizontalLayout_27.addWidget(self.label_17)
        self.txtAltitudeM = QtGui.QLineEdit(self.frame_AltitudeIA1)
        self.txtAltitudeM.setObjectName(_fromUtf8("txtAltitudeM"))
        self.txtAltitudeM.setMinimumSize(QtCore.QSize(90, 0))
        self.txtAltitudeM.setMaximumSize(QtCore.QSize(90, 16777215))
        self.horizontalLayout_27.addWidget(self.txtAltitudeM)
        self.label_2 = QtGui.QLabel(self.frame_AltitudeIA1)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_27.addWidget(self.label_2)
        self.txtAltitude = QtGui.QLineEdit(self.frame_AltitudeIA1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtAltitude.sizePolicy().hasHeightForWidth())
        self.txtAltitude.setSizePolicy(sizePolicy)
        self.txtAltitude.setMinimumSize(QtCore.QSize(90, 0))
        self.txtAltitude.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.txtAltitude.setFont(font)
        self.txtAltitude.setObjectName(_fromUtf8("txtAltitude"))
        self.horizontalLayout_27.addWidget(self.txtAltitude)
        self.label = QtGui.QLabel(self.frame_AltitudeIA1)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_27.addWidget(self.label)
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_27.addItem(horizontalSpacer)
        self.vLayout_grbParameters.addWidget(self.frame_AltitudeIA1)
        self.frame_IasMA = QtGui.QFrame(self.grbParameters)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_IasMA.sizePolicy().hasHeightForWidth())
        self.frame_IasMA.setSizePolicy(sizePolicy)
        self.frame_IasMA.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_IasMA.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_IasMA.setObjectName(_fromUtf8("frame_IasMA"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout(self.frame_IasMA)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setMargin(0)
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.label_3 = QtGui.QLabel(self.frame_IasMA)
        self.label_3.setMinimumSize(QtCore.QSize(140, 0))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_11.addWidget(self.label_3)
        self.txtIsa = QtGui.QLineEdit(self.frame_IasMA)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtIsa.sizePolicy().hasHeightForWidth())
        self.txtIsa.setSizePolicy(sizePolicy)
        self.txtIsa.setMinimumSize(QtCore.QSize(60, 0))
        self.txtIsa.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.txtIsa.setFont(font)
        self.txtIsa.setObjectName(_fromUtf8("txtIsa"))
        self.horizontalLayout_11.addWidget(self.txtIsa)
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(horizontalSpacer)
        self.vLayout_grbParameters.addWidget(self.frame_IasMA)
        self.frame_IasMA_2 = QtGui.QFrame(self.grbParameters)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_IasMA_2.sizePolicy().hasHeightForWidth())
        self.frame_IasMA_2.setSizePolicy(sizePolicy)
        self.frame_IasMA_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_IasMA_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_IasMA_2.setObjectName(_fromUtf8("frame_IasMA_2"))
        self.horizontalLayout_12 = QtGui.QHBoxLayout(self.frame_IasMA_2)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setMargin(0)
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.label_4 = QtGui.QLabel(self.frame_IasMA_2)
        self.label_4.setMinimumSize(QtCore.QSize(140, 0))
        self.label_4.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_12.addWidget(self.label_4)
        self.txtOffset = QtGui.QLineEdit(self.frame_IasMA_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtOffset.sizePolicy().hasHeightForWidth())
        self.txtOffset.setSizePolicy(sizePolicy)
        self.txtOffset.setMinimumSize(QtCore.QSize(60, 0))
        self.txtOffset.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.txtOffset.setFont(font)
        self.txtOffset.setObjectName(_fromUtf8("txtOffset"))
        self.horizontalLayout_12.addWidget(self.txtOffset)
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(horizontalSpacer)
        self.vLayout_grbParameters.addWidget(self.frame_IasMA_2)
        self.frame_RNVA_2 = QtGui.QFrame(self.grbParameters)
        self.frame_RNVA_2.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_RNVA_2.sizePolicy().hasHeightForWidth())
        self.frame_RNVA_2.setSizePolicy(sizePolicy)
        self.frame_RNVA_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_RNVA_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_RNVA_2.setObjectName(_fromUtf8("frame_RNVA_2"))
        self.horizontalLayout_17 = QtGui.QHBoxLayout(self.frame_RNVA_2)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setMargin(0)
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        self.label_8 = QtGui.QLabel(self.frame_RNVA_2)
        self.label_8.setMinimumSize(QtCore.QSize(140, 0))
        self.label_8.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_17.addWidget(self.label_8)
        self.cmbTurnLimitation = QtGui.QComboBox(self.frame_RNVA_2)
        self.cmbTurnLimitation.setMinimumSize(QtCore.QSize(100, 0))
        self.cmbTurnLimitation.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.cmbTurnLimitation.setFont(font)
        self.cmbTurnLimitation.setFrame(True)
        self.cmbTurnLimitation.setObjectName(_fromUtf8("cmbTurnLimitation"))
        self.horizontalLayout_17.addWidget(self.cmbTurnLimitation)
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(horizontalSpacer)
        self.vLayout_grbParameters.addWidget(self.frame_RNVA_2)
        self.frame_DMEDistance = QtGui.QFrame(self.grbParameters)
        self.frame_DMEDistance.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_DMEDistance.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_DMEDistance.setObjectName(_fromUtf8("frame_DMEDistance"))
        self.horizontalLayout_66 = QtGui.QHBoxLayout(self.frame_DMEDistance)
        self.horizontalLayout_66.setSpacing(0)
        self.horizontalLayout_66.setMargin(0)
        self.horizontalLayout_66.setObjectName(_fromUtf8("horizontalLayout_66"))
        self.label_74 = QtGui.QLabel(self.frame_DMEDistance)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_74.sizePolicy().hasHeightForWidth())
        self.label_74.setSizePolicy(sizePolicy)
        self.label_74.setMinimumSize(QtCore.QSize(140, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_74.setFont(font)
        self.label_74.setObjectName(_fromUtf8("label_74"))
        self.horizontalLayout_66.addWidget(self.label_74)
        self.frame_APV_10 = QtGui.QFrame(self.frame_DMEDistance)
        self.frame_APV_10.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_APV_10.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_APV_10.setObjectName(_fromUtf8("frame_APV_10"))
        self.horizontalLayout_18 = QtGui.QHBoxLayout(self.frame_APV_10)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setMargin(0)
        self.horizontalLayout_18.setObjectName(_fromUtf8("horizontalLayout_18"))
        self.txtDmeDistance = QtGui.QLineEdit(self.frame_APV_10)
        self.txtDmeDistance.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtDmeDistance.setFont(font)
        self.txtDmeDistance.setObjectName(_fromUtf8("txtDmeDistance"))
        self.txtDmeDistance.setMinimumSize(QtCore.QSize(100, 0))
        self.txtDmeDistance.setMaximumSize(QtCore.QSize(100, 16777215))
        self.horizontalLayout_18.addWidget(self.txtDmeDistance)
        self.btnCaptureDME = QtGui.QToolButton(self.frame_APV_10)
        self.btnCaptureDME.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/coordinate_capture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCaptureDME.setIcon(icon)
        self.btnCaptureDME.setObjectName(_fromUtf8("btnCaptureDME"))
        self.horizontalLayout_18.addWidget(self.btnCaptureDME)
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(horizontalSpacer)
        self.horizontalLayout_66.addWidget(self.frame_APV_10)
        self.vLayout_grbParameters.addWidget(self.frame_DMEDistance)
        self.frame_IasMA_3 = QtGui.QFrame(self.grbParameters)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_IasMA_3.sizePolicy().hasHeightForWidth())
        self.frame_IasMA_3.setSizePolicy(sizePolicy)
        self.frame_IasMA_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_IasMA_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_IasMA_3.setObjectName(_fromUtf8("frame_IasMA_3"))
        self.horizontalLayout_14 = QtGui.QHBoxLayout(self.frame_IasMA_3)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setMargin(0)
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.label_5 = QtGui.QLabel(self.frame_IasMA_3)
        self.label_5.setMinimumSize(QtCore.QSize(140, 0))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_14.addWidget(self.label_5)
        self.txtTime = QtGui.QLineEdit(self.frame_IasMA_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtTime.sizePolicy().hasHeightForWidth())
        self.txtTime.setSizePolicy(sizePolicy)
        self.txtTime.setMinimumSize(QtCore.QSize(60, 0))
        self.txtTime.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.txtTime.setFont(font)
        self.txtTime.setObjectName(_fromUtf8("txtTime"))
        self.horizontalLayout_14.addWidget(self.txtTime)
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(horizontalSpacer)
        self.vLayout_grbParameters.addWidget(self.frame_IasMA_3)
        self.frameMoc = QtGui.QFrame(self.grbParameters)
        self.frameMoc.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameMoc.setFrameShadow(QtGui.QFrame.Raised)
        self.frameMoc.setObjectName(_fromUtf8("frameMoc"))
        self.horizontalLayout_74 = QtGui.QHBoxLayout(self.frameMoc)
        self.horizontalLayout_74.setSpacing(0)
        self.horizontalLayout_74.setMargin(0)
        self.horizontalLayout_74.setObjectName(_fromUtf8("horizontalLayout_74"))
        self.label_82 = QtGui.QLabel(self.frameMoc)
        self.label_82.setMinimumSize(QtCore.QSize(140, 0))
        self.label_82.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_82.setFont(font)
        self.label_82.setObjectName(_fromUtf8("label_82"))
        self.horizontalLayout_74.addWidget(self.label_82)
        self.txtMoc = QtGui.QLineEdit(self.frameMoc)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtMoc.setFont(font)
        self.txtMoc.setObjectName(_fromUtf8("txtMoc"))
        self.txtMoc.setMinimumSize(QtCore.QSize(90, 0))
        self.txtMoc.setMaximumSize(QtCore.QSize(90, 16777215))
        self.horizontalLayout_74.addWidget(self.txtMoc)
        self.label_6 = QtGui.QLabel(self.frameMoc)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_74.addWidget(self.label_6)
        self.txtMocFt = QtGui.QLineEdit(self.frameMoc)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtMocFt.setFont(font)
        self.txtMocFt.setText(_fromUtf8(""))
        self.txtMocFt.setObjectName(_fromUtf8("txtMocFt"))
        self.txtMocFt.setMinimumSize(QtCore.QSize(90, 0))
        self.txtMocFt.setMaximumSize(QtCore.QSize(90, 16777215))
        self.horizontalLayout_74.addWidget(self.txtMocFt)
        self.labelMocFt = QtGui.QLabel(self.frameMoc)
        self.labelMocFt.setObjectName(_fromUtf8("labelMocFt"))
        self.horizontalLayout_74.addWidget(self.labelMocFt)
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_74.addItem(horizontalSpacer)
        self.vLayout_grbParameters.addWidget(self.frameMoc)
        self.frameIas_2 = QtGui.QFrame(self.grbParameters)
        self.frameIas_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameIas_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frameIas_2.setObjectName(_fromUtf8("frameIas_2"))
        self.horizontalLayout_62 = QtGui.QHBoxLayout(self.frameIas_2)
        self.horizontalLayout_62.setSpacing(0)
        self.horizontalLayout_62.setMargin(0)
        self.horizontalLayout_62.setObjectName(_fromUtf8("horizontalLayout_62"))
        self.label_70 = QtGui.QLabel(self.frameIas_2)
        self.label_70.setMinimumSize(QtCore.QSize(140, 0))
        self.label_70.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_70.setFont(font)
        self.label_70.setObjectName(_fromUtf8("label_70"))
        self.horizontalLayout_62.addWidget(self.label_70)
        self.spinBoxMocmulipiler = QtGui.QSpinBox(self.frameIas_2)
        self.spinBoxMocmulipiler.setProperty("value", 1)
        self.spinBoxMocmulipiler.setObjectName(_fromUtf8("spinBoxMocmulipiler"))
        self.spinBoxMocmulipiler.setMinimumSize(QtCore.QSize(60, 0))
        self.spinBoxMocmulipiler.setMaximumSize(QtCore.QSize(60, 16777215))
        self.horizontalLayout_62.addWidget(self.spinBoxMocmulipiler)
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_62.addItem(horizontalSpacer)
        self.vLayout_grbParameters.addWidget(self.frameIas_2)
        self.verticalLayout_AAC.addWidget(self.grbParameters)
        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))

        self.txtTrackRadial = TrackRadialBoxPanel(self.groupBox_2)
        self.txtTrackRadial.Caption = "In-bound Track"
        self.txtTrackRadial.LabelWidth = 140
        self.verticalLayout_2.addWidget(self.txtTrackRadial)
        # self.frame_ThrFaf = QtGui.QFrame(self.groupBox_2)
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
        # self.label_73.setMinimumSize(QtCore.QSize(140, 0))
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
        # self.txtTrackRadial = QtGui.QLineEdit(self.frame_APV_9)
        # self.txtTrackRadial.setEnabled(True)
        # font = QtGui.QFont()
        # font.setBold(False)
        # font.setWeight(50)
        # self.txtTrackRadial.setFont(font)
        # self.txtTrackRadial.setObjectName(_fromUtf8("txtTrackRadial"))
        # self.horizontalLayout_13.addWidget(self.txtTrackRadial)
        # self.btnCaptureTrack = QtGui.QToolButton(self.frame_APV_9)
        # self.btnCaptureTrack.setText(_fromUtf8(""))
        # self.btnCaptureTrack.setIcon(icon)
        # self.btnCaptureTrack.setObjectName(_fromUtf8("btnCaptureTrack"))
        # self.horizontalLayout_13.addWidget(self.btnCaptureTrack)
        # self.horizontalLayout_65.addWidget(self.frame_APV_9)
        # self.verticalLayout_2.addWidget(self.frame_ThrFaf)
        self.frame_60 = QtGui.QFrame(self.groupBox_2)
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
        self.label_69.setMinimumSize(QtCore.QSize(140, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_69.setFont(font)
        self.label_69.setObjectName(_fromUtf8("label_69"))
        self.horizontalLayout_61.addWidget(self.label_69)
        self.cmbOrientation = QtGui.QComboBox(self.frame_60)
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
        self.cmbOrientation.setMinimumSize(QtCore.QSize(70, 0))
        self.cmbOrientation.setMaximumSize(QtCore.QSize(70, 16777215))
        self.horizontalLayout_61.addWidget(self.cmbOrientation)
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_61.addItem(horizontalSpacer)
        self.verticalLayout_2.addWidget(self.frame_60)
        self.verticalLayout_AAC.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.gbNavAid.setTitle(_translate("Form", "Navigational Aid", None))
        # self.label_67.setText(_translate("Form", "Type:", None))
        self.grbParameters.setTitle(_translate("Form", "Parameters", None))
        self.label_7.setText(_translate("Form", "IAS (kts):", None))
        self.txtIas.setText(_translate("Form", "185", None))
        self.label_77.setText(_translate("Form", "TAS (kts):", None))
        self.label_17.setText(_translate("Form", "Altitude:", None))
        self.label_2.setText(_translate("Form", "m", None))
        self.txtAltitude.setText(_translate("Form", "5000", None))
        self.label.setText(_translate("Form", "ft", None))
        self.label_3.setText(_translate("Form", "ISA (C):", None))
        self.txtIsa.setText(_translate("Form", "15", None))
        self.label_4.setText(_translate("Form", "Offset Entry Angle ():", None))
        self.txtOffset.setText(_translate("Form", "30", None))
        self.label_8.setText(_translate("Form", "Turn Limitation:", None))
        self.label_74.setText(_translate("Form", "DME Distance (nm):", None))
        self.txtDmeDistance.setText(_translate("Form", "10", None))
        self.label_5.setText(_translate("Form", "Time (min):", None))
        self.txtTime.setText(_translate("Form", "1", None))
        self.label_82.setText(_translate("Form", "Moc:", None))
        self.txtMoc.setText(_translate("Form", "300", None))
        self.label_6.setText(_translate("Form", "m", None))
        self.labelMocFt.setText(_translate("Form", "ft", None))
        self.label_70.setText(_translate("Form", "MOCmultipiler:", None))
        self.groupBox_2.setTitle(_translate("Form", "Orientation", None))
        # self.label_73.setText(_translate("Form", "In-bound Track ():", None))
        # self.txtTrackRadial.setText(_translate("Form", "0", None))
        self.label_69.setText(_translate("Form", "Major Turn:", None))
