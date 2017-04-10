# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_IasHelp.ui'
#
# Created: Sun Jul 12 15:45:24 2015
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

class ui_IasHelpDlg(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(630, 492)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.btnCaptureDistance = QtGui.QToolButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCaptureDistance.sizePolicy().hasHeightForWidth())
        self.btnCaptureDistance.setSizePolicy(sizePolicy)
        self.btnCaptureDistance.setStyleSheet(_fromUtf8("border-image: url(Resource/IasHelp.png);"))
        self.btnCaptureDistance.setText(_fromUtf8(""))
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/gnss_item/coordinate_capture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.btnCaptureDistance.setIcon(icon)
        self.btnCaptureDistance.setObjectName(_fromUtf8("btnCaptureDistance"))
        self.verticalLayout.addWidget(self.btnCaptureDistance)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Airspeeds for holding area construction", None))

# import Resources_rc
