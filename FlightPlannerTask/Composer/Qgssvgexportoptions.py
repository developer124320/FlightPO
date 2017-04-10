# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qgssvgexportoptions.ui'
#
# Created: Wed Jun 22 15:59:27 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from qgis.gui import QgsCollapsibleGroupBoxBasic
from qgis.gui import QgsDoubleSpinBox
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

class QgsSvgExportOptionsDialog(object):
    def setupUi(self, QgsSvgExportOptionsDialog):
        QgsSvgExportOptionsDialog.setObjectName(_fromUtf8("QgsSvgExportOptionsDialog"))
        QgsSvgExportOptionsDialog.resize(489, 282)
        self.verticalLayout = QtGui.QVBoxLayout(QgsSvgExportOptionsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QgsCollapsibleGroupBoxBasic(QgsSvgExportOptionsDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.chkMapLayersAsGroup = QtGui.QCheckBox(self.groupBox)
        self.chkMapLayersAsGroup.setChecked(False)
        self.chkMapLayersAsGroup.setObjectName(_fromUtf8("chkMapLayersAsGroup"))
        self.verticalLayout_2.addWidget(self.chkMapLayersAsGroup)
        self.chkTextAsOutline = QtGui.QCheckBox(self.groupBox)
        self.chkTextAsOutline.setEnabled(True)
        self.chkTextAsOutline.setChecked(True)
        self.chkTextAsOutline.setObjectName(_fromUtf8("chkTextAsOutline"))
        self.verticalLayout_2.addWidget(self.chkTextAsOutline)
        self.verticalLayout.addWidget(self.groupBox)
        self.mClipToContentGroupBox = QgsCollapsibleGroupBoxBasic(QgsSvgExportOptionsDialog)
        self.mClipToContentGroupBox.setCheckable(True)
        self.mClipToContentGroupBox.setChecked(False)
        self.mClipToContentGroupBox.setObjectName(_fromUtf8("mClipToContentGroupBox"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.mClipToContentGroupBox)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.mTopMarginSpinBox = QgsDoubleSpinBox(self.mClipToContentGroupBox)
        self.mTopMarginSpinBox.setSingleStep(0.1)
        self.mTopMarginSpinBox.setObjectName(_fromUtf8("mTopMarginSpinBox"))
        self.gridLayout_5.addWidget(self.mTopMarginSpinBox, 0, 2, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_5 = QtGui.QLabel(self.mClipToContentGroupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_7.addWidget(self.label_5)
        self.mLeftMarginSpinBox = QgsDoubleSpinBox(self.mClipToContentGroupBox)
        self.mLeftMarginSpinBox.setSingleStep(0.1)
        self.mLeftMarginSpinBox.setObjectName(_fromUtf8("mLeftMarginSpinBox"))
        self.horizontalLayout_7.addWidget(self.mLeftMarginSpinBox)
        self.label_11 = QtGui.QLabel(self.mClipToContentGroupBox)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_7.addWidget(self.label_11)
        self.mRightMarginSpinBox = QgsDoubleSpinBox(self.mClipToContentGroupBox)
        self.mRightMarginSpinBox.setSingleStep(0.1)
        self.mRightMarginSpinBox.setObjectName(_fromUtf8("mRightMarginSpinBox"))
        self.horizontalLayout_7.addWidget(self.mRightMarginSpinBox)
        self.gridLayout_5.addLayout(self.horizontalLayout_7, 1, 0, 1, 4)
        self.label_12 = QtGui.QLabel(self.mClipToContentGroupBox)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_5.addWidget(self.label_12, 2, 1, 1, 1)
        self.mBottomMarginSpinBox = QgsDoubleSpinBox(self.mClipToContentGroupBox)
        self.mBottomMarginSpinBox.setSingleStep(0.1)
        self.mBottomMarginSpinBox.setObjectName(_fromUtf8("mBottomMarginSpinBox"))
        self.gridLayout_5.addWidget(self.mBottomMarginSpinBox, 2, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.mClipToContentGroupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_5.addWidget(self.label_4, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 0, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem1, 0, 0, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_5)
        self.verticalLayout.addWidget(self.mClipToContentGroupBox)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.buttonBox = QtGui.QDialogButtonBox(QgsSvgExportOptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(QgsSvgExportOptionsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QgsSvgExportOptionsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QgsSvgExportOptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(QgsSvgExportOptionsDialog)
        QgsSvgExportOptionsDialog.setTabOrder(self.chkMapLayersAsGroup, self.chkTextAsOutline)
        QgsSvgExportOptionsDialog.setTabOrder(self.chkTextAsOutline, self.mClipToContentGroupBox)
        QgsSvgExportOptionsDialog.setTabOrder(self.mClipToContentGroupBox, self.mTopMarginSpinBox)
        QgsSvgExportOptionsDialog.setTabOrder(self.mTopMarginSpinBox, self.mLeftMarginSpinBox)
        QgsSvgExportOptionsDialog.setTabOrder(self.mLeftMarginSpinBox, self.mRightMarginSpinBox)
        QgsSvgExportOptionsDialog.setTabOrder(self.mRightMarginSpinBox, self.mBottomMarginSpinBox)

    def retranslateUi(self, QgsSvgExportOptionsDialog):
        QgsSvgExportOptionsDialog.setWindowTitle(_translate("QgsSvgExportOptionsDialog", "SVG export options", None))
        self.groupBox.setTitle(_translate("QgsSvgExportOptionsDialog", "SVG options", None))
        self.chkMapLayersAsGroup.setText(_translate("QgsSvgExportOptionsDialog", "Export map layers as svg groups (may affect label placement)", None))
        self.chkTextAsOutline.setToolTip(_translate("QgsSvgExportOptionsDialog", "Uncheck to render map labels as text objects. This will degrade the quality of the map labels but allow editing in vector illustration software.", None))
        self.chkTextAsOutline.setText(_translate("QgsSvgExportOptionsDialog", "Render map labels as outlines", None))
        self.mClipToContentGroupBox.setTitle(_translate("QgsSvgExportOptionsDialog", "Crop to content", None))
        self.label_5.setText(_translate("QgsSvgExportOptionsDialog", "Left", None))
        self.label_11.setText(_translate("QgsSvgExportOptionsDialog", "Right", None))
        self.label_12.setText(_translate("QgsSvgExportOptionsDialog", "Bottom", None))
        self.label_4.setText(_translate("QgsSvgExportOptionsDialog", "Top margin (mm)", None))


