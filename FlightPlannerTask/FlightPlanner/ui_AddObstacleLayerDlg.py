# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddObstacleLayerDlg.ui'
#
# Created: Fri Jan 23 14:38:37 2015
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

class Ui_AddObstacleLayerDlg(object):
    def setupUi(self, AddObstacleLayerDlg):
        AddObstacleLayerDlg.setObjectName(_fromUtf8("AddObstacleLayerDlg"))
        AddObstacleLayerDlg.resize(485, 220)
        self.buttonBox = QtGui.QDialogButtonBox(AddObstacleLayerDlg)
        self.buttonBox.setGeometry(QtCore.QRect(120, 170, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(AddObstacleLayerDlg)
        self.label.setGeometry(QtCore.QRect(10, 30, 54, 12))
        self.label.setObjectName(_fromUtf8("label"))
        self.txtPath = QtGui.QLineEdit(AddObstacleLayerDlg)
        self.txtPath.setGeometry(QtCore.QRect(70, 30, 331, 20))
        self.txtPath.setObjectName(_fromUtf8("txtPath"))
        self.btnBrowse = QtGui.QPushButton(AddObstacleLayerDlg)
        self.btnBrowse.setGeometry(QtCore.QRect(410, 30, 71, 23))
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.cmbCurrentCrs = QtGui.QComboBox(AddObstacleLayerDlg)
        self.cmbCurrentCrs.setGeometry(QtCore.QRect(59, 110, 131, 22))
        self.cmbCurrentCrs.setObjectName(_fromUtf8("cmbCurrentCrs"))
        self.label_2 = QtGui.QLabel(AddObstacleLayerDlg)
        self.label_2.setGeometry(QtCore.QRect(50, 80, 161, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(AddObstacleLayerDlg)
        self.label_3.setGeometry(QtCore.QRect(270, 80, 161, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.cmbDisplayCrs = QtGui.QComboBox(AddObstacleLayerDlg)
        self.cmbDisplayCrs.setGeometry(QtCore.QRect(280, 110, 131, 22))
        self.cmbDisplayCrs.setObjectName(_fromUtf8("cmbDisplayCrs"))

        self.retranslateUi(AddObstacleLayerDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddObstacleLayerDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddObstacleLayerDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(AddObstacleLayerDlg)

    def retranslateUi(self, AddObstacleLayerDlg):
        AddObstacleLayerDlg.setWindowTitle(_translate("AddObstacleLayerDlg", "Create a Layer From Obstacle File", None))
        self.label.setText(_translate("AddObstacleLayerDlg", "File Name: ", None))
        self.btnBrowse.setText(_translate("AddObstacleLayerDlg", "Browse...", None))
        self.label_2.setText(_translate("AddObstacleLayerDlg", "Current Coordinate System", None))
        self.label_3.setText(_translate("AddObstacleLayerDlg", "Display Coordinate System", None))

