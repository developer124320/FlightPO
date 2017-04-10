# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DlgComplexAreas.ui'
#
# Created: Sun Feb 28 15:07:22 2016
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

class Ui_DlgComplexAreas(object):
    def setupUi(self, DlgComplexAreas):
        DlgComplexAreas.setObjectName(_fromUtf8("DlgComplexAreas"))
        DlgComplexAreas.resize(382, 273)
        self.verticalLayout_2 = QtGui.QVBoxLayout(DlgComplexAreas)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(DlgComplexAreas)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lstAreas = QtGui.QListView(self.groupBox)
        self.lstAreas.setObjectName(_fromUtf8("lstAreas"))
        self.verticalLayout.addWidget(self.lstAreas)
        self.frame_Track = QtGui.QFrame(self.groupBox)
        self.frame_Track.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_Track.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_Track.setObjectName(_fromUtf8("frame_Track"))
        self.hLayoutTrack = QtGui.QHBoxLayout(self.frame_Track)
        self.hLayoutTrack.setSpacing(0)
        self.hLayoutTrack.setMargin(0)
        self.hLayoutTrack.setObjectName(_fromUtf8("hLayoutTrack"))
        self.label_75 = QtGui.QLabel(self.frame_Track)
        self.label_75.setMinimumSize(QtCore.QSize(70, 0))
        self.label_75.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_75.setFont(font)
        self.label_75.setObjectName(_fromUtf8("label_75"))
        self.hLayoutTrack.addWidget(self.label_75)
        self.frame_APV_10 = QtGui.QFrame(self.frame_Track)
        self.frame_APV_10.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_APV_10.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_APV_10.setObjectName(_fromUtf8("frame_APV_10"))
        self.horizontalLayout_14 = QtGui.QHBoxLayout(self.frame_APV_10)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setMargin(0)
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.txtTrack = QtGui.QLineEdit(self.frame_APV_10)
        self.txtTrack.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtTrack.setFont(font)
        self.txtTrack.setObjectName(_fromUtf8("txtTrack"))
        self.horizontalLayout_14.addWidget(self.txtTrack)
        self.btnCaptureTrack = QtGui.QToolButton(self.frame_APV_10)
        self.btnCaptureTrack.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/coordinate_capture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCaptureTrack.setIcon(icon)
        self.btnCaptureTrack.setObjectName(_fromUtf8("btnCaptureTrack"))
        self.horizontalLayout_14.addWidget(self.btnCaptureTrack)
        self.hLayoutTrack.addWidget(self.frame_APV_10)
        self.verticalLayout.addWidget(self.frame_Track)
        self.frame = QtGui.QFrame(self.groupBox)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnAddPrimaryArea = QtGui.QPushButton(self.frame)
        self.btnAddPrimaryArea.setMinimumSize(QtCore.QSize(110, 0))
        self.btnAddPrimaryArea.setObjectName(_fromUtf8("btnAddPrimaryArea"))
        self.horizontalLayout.addWidget(self.btnAddPrimaryArea)
        self.btnAddSecondaryArea = QtGui.QPushButton(self.frame)
        self.btnAddSecondaryArea.setMinimumSize(QtCore.QSize(110, 0))
        self.btnAddSecondaryArea.setMaximumSize(QtCore.QSize(110, 16777215))
        self.btnAddSecondaryArea.setObjectName(_fromUtf8("btnAddSecondaryArea"))
        self.horizontalLayout.addWidget(self.btnAddSecondaryArea)
        self.btnRemove = QtGui.QPushButton(self.frame)
        self.btnRemove.setMinimumSize(QtCore.QSize(110, 0))
        self.btnRemove.setObjectName(_fromUtf8("btnRemove"))
        self.horizontalLayout.addWidget(self.btnRemove)
        self.verticalLayout.addWidget(self.frame)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.buttonBoxOkCancel = QtGui.QDialogButtonBox(DlgComplexAreas)
        self.buttonBoxOkCancel.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBoxOkCancel.setObjectName(_fromUtf8("buttonBoxOkCancel"))
        self.verticalLayout_2.addWidget(self.buttonBoxOkCancel)

        self.retranslateUi(DlgComplexAreas)
        QtCore.QMetaObject.connectSlotsByName(DlgComplexAreas)

    def retranslateUi(self, DlgComplexAreas):
        DlgComplexAreas.setWindowTitle(_translate("DlgComplexAreas", "Complex Area", None))
        self.label_75.setText(_translate("DlgComplexAreas", "Track (°):", None))
        self.txtTrack.setText(_translate("DlgComplexAreas", "0", None))
        self.btnAddPrimaryArea.setText(_translate("DlgComplexAreas", "Primary Area", None))
        self.btnAddSecondaryArea.setText(_translate("DlgComplexAreas", "Secondary Area", None))
        self.btnRemove.setText(_translate("DlgComplexAreas", "Remove", None))
        self.groupBox.setTitle(_translate("DlgComplexAreas", "Defined Areas", None))

