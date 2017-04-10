# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layerSaveAsDlg.ui'
#
# Created: Fri Feb 13 11:46:13 2015
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

class ui_layerSaveAsDlg(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(397, 213)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame_2 = QtGui.QFrame(self.frame)
        self.frame_2.setMaximumSize(QtCore.QSize(70, 16777215))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(0, 0, -1, -1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.frame_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(self.frame_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.frame_3 = QtGui.QFrame(self.frame_2)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.verticalLayout_2.addWidget(self.frame_3)
        self.horizontalLayout.addWidget(self.frame_2)
        self.frame_4 = QtGui.QFrame(self.frame)
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.cmbFormat = QtGui.QComboBox(self.frame_4)
        self.cmbFormat.setObjectName(_fromUtf8("cmbFormat"))
        self.verticalLayout_3.addWidget(self.cmbFormat)
        self.frame_5 = QtGui.QFrame(self.frame_4)
        self.frame_5.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_5.setObjectName(_fromUtf8("frame_5"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.txtSavePath = QtGui.QLineEdit(self.frame_5)
        self.txtSavePath.setObjectName(_fromUtf8("txtSavePath"))
        self.horizontalLayout_2.addWidget(self.txtSavePath)
        self.btnBrowse = QtGui.QPushButton(self.frame_5)
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.horizontalLayout_2.addWidget(self.btnBrowse)
        self.verticalLayout_3.addWidget(self.frame_5)
        self.cmbCrs = QtGui.QComboBox(self.frame_4)
        self.cmbCrs.setObjectName(_fromUtf8("cmbCrs"))
        self.verticalLayout_3.addWidget(self.cmbCrs)
        self.frame_6 = QtGui.QFrame(self.frame_4)
        self.frame_6.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_6.setObjectName(_fromUtf8("frame_6"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame_6)
        self.horizontalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.txtCrs = QtGui.QLineEdit(self.frame_6)
        self.txtCrs.setEnabled(True)
        self.txtCrs.setObjectName(_fromUtf8("txtCrs"))
        self.horizontalLayout_3.addWidget(self.txtCrs)
        self.btnChange = QtGui.QPushButton(self.frame_6)
        self.btnChange.setObjectName(_fromUtf8("btnChange"))
        self.horizontalLayout_3.addWidget(self.btnChange)
        self.verticalLayout_3.addWidget(self.frame_6)
        self.horizontalLayout.addWidget(self.frame_4)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
#         QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Format", None))
        self.label_2.setText(_translate("Dialog", "Save as", None))
        self.label_3.setText(_translate("Dialog", "CRS", None))
        self.btnBrowse.setText(_translate("Dialog", "Browse", None))
        self.btnChange.setText(_translate("Dialog", "Change...", None))

