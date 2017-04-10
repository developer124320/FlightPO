# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qgsmeasurebase.ui'
#
# Created: Mon Mar 23 09:16:33 2015
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MeasureDialog(object):
    def setupUi(self, MeasureDialog):
        MeasureDialog.setObjectName(_fromUtf8("MeasureDialog"))
        MeasureDialog.resize(285, 145)
        self.verticalLayout = QtGui.QVBoxLayout(MeasureDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(MeasureDialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.textLabel2 = QtGui.QLabel(self.frame)
        self.textLabel2.setObjectName(_fromUtf8("textLabel2"))
        self.horizontalLayout.addWidget(self.textLabel2)
        self.txtToal = QtGui.QLineEdit(self.frame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.txtToal.setFont(font)
        self.txtToal.setAlignment(QtCore.Qt.AlignRight)
        self.txtToal.setReadOnly(True)
        self.txtToal.setObjectName(_fromUtf8("txtToal"))
        self.horizontalLayout.addWidget(self.txtToal)
        self.cmbMeasureType = QtGui.QComboBox(self.frame)
        self.cmbMeasureType.setObjectName(_fromUtf8("cmbMeasureType"))
        self.horizontalLayout.addWidget(self.cmbMeasureType)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(MeasureDialog)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnNew = QtGui.QPushButton(self.frame_2)
        self.btnNew.setObjectName(_fromUtf8("btnNew"))
        self.horizontalLayout_2.addWidget(self.btnNew)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnClose = QtGui.QPushButton(self.frame_2)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout_2.addWidget(self.btnClose)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(MeasureDialog)
        QtCore.QMetaObject.connectSlotsByName(MeasureDialog)

    def retranslateUi(self, MeasureDialog):
        MeasureDialog.setWindowTitle(QtGui.QApplication.translate("MeasureDialog", "Measure Distance", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel2.setText(QtGui.QApplication.translate("MeasureDialog", "Total", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNew.setText(QtGui.QApplication.translate("MeasureDialog", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setText(QtGui.QApplication.translate("MeasureDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

