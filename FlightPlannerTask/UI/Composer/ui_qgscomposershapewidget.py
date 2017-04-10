# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qgscomposershapewidgetbase.ui'
#
# Created: Tue Sep 27 10:23:26 2016
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

class Ui_QgsComposerShapeWidgetBase(object):
    def setupUi(self, QgsComposerShapeWidgetBase):
        QgsComposerShapeWidgetBase.setObjectName(_fromUtf8("QgsComposerShapeWidgetBase"))
        QgsComposerShapeWidgetBase.resize(285, 148)
        self.verticalLayout = QtGui.QVBoxLayout(QgsComposerShapeWidgetBase)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(QgsComposerShapeWidgetBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet(_fromUtf8("padding: 2px; font-weight: bold; background-color: rgb(200, 200, 200);"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.scrollArea = QtGui.QScrollArea(QgsComposerShapeWidgetBase)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -22, 267, 147))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.mainLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.mainLayout.setObjectName(_fromUtf8("mainLayout"))
        self.groupBox = QgsCollapsibleGroupBoxBasic(self.scrollAreaWidgetContents)
        self.groupBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.groupBox.setProperty("syncGroup", _fromUtf8("composeritem"))
        self.groupBox.setProperty("collapsed", False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.mCornerRadiusSpinBox = QgsDoubleSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mCornerRadiusSpinBox.sizePolicy().hasHeightForWidth())
        self.mCornerRadiusSpinBox.setSizePolicy(sizePolicy)
        self.mCornerRadiusSpinBox.setMaximum(999.0)
        self.mCornerRadiusSpinBox.setObjectName(_fromUtf8("mCornerRadiusSpinBox"))
        self.gridLayout.addWidget(self.mCornerRadiusSpinBox, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.mShapeStyleButton = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mShapeStyleButton.sizePolicy().hasHeightForWidth())
        self.mShapeStyleButton.setSizePolicy(sizePolicy)
        self.mShapeStyleButton.setObjectName(_fromUtf8("mShapeStyleButton"))
        self.gridLayout.addWidget(self.mShapeStyleButton, 2, 1, 1, 1)
        self.mShapeComboBox = QtGui.QComboBox(self.groupBox)
        self.mShapeComboBox.setObjectName(_fromUtf8("mShapeComboBox"))
        self.gridLayout.addWidget(self.mShapeComboBox, 0, 0, 1, 2)
        self.mainLayout.addWidget(self.groupBox)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(QgsComposerShapeWidgetBase)
        QtCore.QMetaObject.connectSlotsByName(QgsComposerShapeWidgetBase)
        QgsComposerShapeWidgetBase.setTabOrder(self.groupBox, self.scrollArea)
        QgsComposerShapeWidgetBase.setTabOrder(self.scrollArea, self.mShapeComboBox)
        QgsComposerShapeWidgetBase.setTabOrder(self.mShapeComboBox, self.mCornerRadiusSpinBox)
        QgsComposerShapeWidgetBase.setTabOrder(self.mCornerRadiusSpinBox, self.mShapeStyleButton)

    def retranslateUi(self, QgsComposerShapeWidgetBase):
        QgsComposerShapeWidgetBase.setWindowTitle(_translate("QgsComposerShapeWidgetBase", "Form", None))
        self.label_2.setText(_translate("QgsComposerShapeWidgetBase", "Shape", None))
        self.groupBox.setTitle(_translate("QgsComposerShapeWidgetBase", "Main properties", None))
        self.label_3.setText(_translate("QgsComposerShapeWidgetBase", "Corner radius", None))
        self.mCornerRadiusSpinBox.setSuffix(_translate("QgsComposerShapeWidgetBase", " mm", None))
        self.label.setText(_translate("QgsComposerShapeWidgetBase", "Style", None))
        self.mShapeStyleButton.setText(_translate("QgsComposerShapeWidgetBase", "Change...", None))

from qgscollapsiblegroupbox import QgsCollapsibleGroupBoxBasic
from qgsdoublespinbox import QgsDoubleSpinBox
