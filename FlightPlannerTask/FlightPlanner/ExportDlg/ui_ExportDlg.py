# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ExportDlg.ui'
#
# Created: Fri Oct 02 10:17:46 2015
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

class Ui_ExportDlg(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(300, 352)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        Dialog.setFont(font)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setMinimumSize(QtCore.QSize(70, 0))
        self.label.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.txtHeading = QtGui.QLineEdit(self.frame)
        self.txtHeading.setObjectName(_fromUtf8("txtHeading"))
        self.horizontalLayout.addWidget(self.txtHeading)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.chbLimit = QtGui.QCheckBox(self.frame_2)
        self.chbLimit.setMinimumSize(QtCore.QSize(200, 0))
        self.chbLimit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.chbLimit.setObjectName(_fromUtf8("chbLimit"))
        self.horizontalLayout_2.addWidget(self.chbLimit)
        self.txtLimit = QtGui.QLineEdit(self.frame_2)
        self.txtLimit.setObjectName(_fromUtf8("txtLimit"))
        self.horizontalLayout_2.addWidget(self.txtLimit)
        self.verticalLayout.addWidget(self.frame_2)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.listColumns = QtGui.QListView(self.groupBox)
        self.listColumns.setObjectName(_fromUtf8("listColumns"))
        self.verticalLayout_2.addWidget(self.listColumns)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
#         self.connect(self.buttonBox, SIGNAL(accepted()), Dialog, SLOT(accept()));
#         self.connect(self.buttonBox, SIGNAL(rejected()), Dialog, SLOT(reject()));
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Export Dialog", None))
        self.label.setText(_translate("Dialog", "Title:", None))
        self.txtLimit.setText(_translate("Dialog", "10", None))
        self.chbLimit.setText(_translate("Dialog", "Limit # of table entries to:", None))
        self.groupBox.setTitle(_translate("Dialog", "Columns", None))

