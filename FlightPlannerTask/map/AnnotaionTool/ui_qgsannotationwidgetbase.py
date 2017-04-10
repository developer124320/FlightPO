# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qgsannotationwidgetbase.ui'
#
# Created: Sun Apr 27 17:56:50 2014
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

class Ui_QgsAnnotationWidgetBase(object):
    def setupUi(self, QgsAnnotationWidgetBase):
        QgsAnnotationWidgetBase.setObjectName(_fromUtf8("QgsAnnotationWidgetBase"))
        QgsAnnotationWidgetBase.resize(221, 172)
        self.gridLayout_2 = QtGui.QGridLayout(QgsAnnotationWidgetBase)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.mMapPositionFixedCheckBox = QtGui.QCheckBox(QgsAnnotationWidgetBase)
        self.mMapPositionFixedCheckBox.setObjectName(_fromUtf8("mMapPositionFixedCheckBox"))
        self.gridLayout_2.addWidget(self.mMapPositionFixedCheckBox, 0, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.mFrameColorButton = QgsColorButton(QgsAnnotationWidgetBase)
        self.mFrameColorButton.setText(_fromUtf8(""))
        self.mFrameColorButton.setObjectName(_fromUtf8("mFrameColorButton"))
        self.gridLayout.addWidget(self.mFrameColorButton, 3, 1, 1, 1)
        self.mBackgroundColorLabel = QtGui.QLabel(QgsAnnotationWidgetBase)
        self.mBackgroundColorLabel.setObjectName(_fromUtf8("mBackgroundColorLabel"))
        self.gridLayout.addWidget(self.mBackgroundColorLabel, 2, 0, 1, 1)
        self.mMapMarkerLabel = QtGui.QLabel(QgsAnnotationWidgetBase)
        self.mMapMarkerLabel.setObjectName(_fromUtf8("mMapMarkerLabel"))
        self.gridLayout.addWidget(self.mMapMarkerLabel, 0, 0, 1, 1)
        self.mBackgroundColorButton = QgsColorButton(QgsAnnotationWidgetBase)
        self.mBackgroundColorButton.setText(_fromUtf8(""))
        self.mBackgroundColorButton.setObjectName(_fromUtf8("mBackgroundColorButton"))
        self.gridLayout.addWidget(self.mBackgroundColorButton, 2, 1, 1, 1)
        self.mMapMarkerButton = QtGui.QPushButton(QgsAnnotationWidgetBase)
        self.mMapMarkerButton.setText(_fromUtf8(""))
        self.mMapMarkerButton.setObjectName(_fromUtf8("mMapMarkerButton"))
        self.gridLayout.addWidget(self.mMapMarkerButton, 0, 1, 1, 1)
        self.mFrameWidthLabel = QtGui.QLabel(QgsAnnotationWidgetBase)
        self.mFrameWidthLabel.setObjectName(_fromUtf8("mFrameWidthLabel"))
        self.gridLayout.addWidget(self.mFrameWidthLabel, 1, 0, 1, 1)
        self.mFrameWidthSpinBox = QtGui.QDoubleSpinBox(QgsAnnotationWidgetBase)
        self.mFrameWidthSpinBox.setObjectName(_fromUtf8("mFrameWidthSpinBox"))
        self.gridLayout.addWidget(self.mFrameWidthSpinBox, 1, 1, 1, 1)
        self.mFrameColorLabel = QtGui.QLabel(QgsAnnotationWidgetBase)
        self.mFrameColorLabel.setObjectName(_fromUtf8("mFrameColorLabel"))
        self.gridLayout.addWidget(self.mFrameColorLabel, 3, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.mMapMarkerLabel.setBuddy(self.mMapMarkerButton)
        self.mFrameWidthLabel.setBuddy(self.mFrameWidthSpinBox)

        self.retranslateUi(QgsAnnotationWidgetBase)
        QtCore.QMetaObject.connectSlotsByName(QgsAnnotationWidgetBase)

    def retranslateUi(self, QgsAnnotationWidgetBase):
        QgsAnnotationWidgetBase.setWindowTitle(_translate("QgsAnnotationWidgetBase", "Form", None))
        self.mMapPositionFixedCheckBox.setText(_translate("QgsAnnotationWidgetBase", "Fixed map position", None))
        self.mBackgroundColorLabel.setText(_translate("QgsAnnotationWidgetBase", "Background color", None))
        self.mMapMarkerLabel.setText(_translate("QgsAnnotationWidgetBase", "Map marker", None))
        self.mFrameWidthLabel.setText(_translate("QgsAnnotationWidgetBase", "Frame width", None))
        self.mFrameColorLabel.setText(_translate("QgsAnnotationWidgetBase", "Frame color", None))

from qgscolorbutton import QgsColorButton
