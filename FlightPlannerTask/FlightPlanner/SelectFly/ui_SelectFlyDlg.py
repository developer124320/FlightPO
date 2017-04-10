# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_SelectFlyDlg.ui'
#
# Created: Sun Dec 13 15:57:04 2015
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

class Ui_SelectFly(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(228, 153)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBoxWaypoint1 = QtGui.QGroupBox(Form)
        self.groupBoxWaypoint1.setObjectName(_fromUtf8("groupBoxWaypoint1"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBoxWaypoint1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.rBtnFlyby1 = QtGui.QRadioButton(self.groupBoxWaypoint1)
        self.rBtnFlyby1.setChecked(True)
        self.rBtnFlyby1.setObjectName(_fromUtf8("rBtnFlyby1"))
        self.horizontalLayout.addWidget(self.rBtnFlyby1)
        self.rBtnFlyover1 = QtGui.QRadioButton(self.groupBoxWaypoint1)
        self.rBtnFlyover1.setObjectName(_fromUtf8("rBtnFlyover1"))
        self.horizontalLayout.addWidget(self.rBtnFlyover1)
        self.verticalLayout.addWidget(self.groupBoxWaypoint1)
        self.groupBoxWaypoint2 = QtGui.QGroupBox(Form)
        self.groupBoxWaypoint2.setObjectName(_fromUtf8("groupBoxWaypoint2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBoxWaypoint2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.rBtnFlyby2 = QtGui.QRadioButton(self.groupBoxWaypoint2)
        self.rBtnFlyby2.setChecked(True)
        self.rBtnFlyby2.setObjectName(_fromUtf8("rBtnFlyby2"))
        self.horizontalLayout_2.addWidget(self.rBtnFlyby2)
        self.rBtnFlyover2 = QtGui.QRadioButton(self.groupBoxWaypoint2)
        self.rBtnFlyover2.setObjectName(_fromUtf8("rBtnFlyover2"))
        self.horizontalLayout_2.addWidget(self.rBtnFlyover2)
        self.verticalLayout.addWidget(self.groupBoxWaypoint2)
        self.frame = QtGui.QFrame(Form)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btnOK = QtGui.QPushButton(self.frame)
        self.btnOK.setObjectName(_fromUtf8("btnOK"))
        self.horizontalLayout_3.addWidget(self.btnOK)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBoxWaypoint1.setTitle(_translate("Form", "Waypoint 1", None))
        self.rBtnFlyby1.setText(_translate("Form", "Fly By", None))
        self.rBtnFlyover1.setText(_translate("Form", "Fly Over", None))
        self.groupBoxWaypoint2.setTitle(_translate("Form", "Waypoint 2", None))
        self.rBtnFlyby2.setText(_translate("Form", "Fly By", None))
        self.rBtnFlyover2.setText(_translate("Form", "Fly Over", None))
        self.btnOK.setText(_translate("Form", "OK", None))

