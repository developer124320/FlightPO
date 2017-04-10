# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qgstextannotationdialogbase.ui'
#
# Created: Mon Apr 28 10:35:31 2014
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

class Ui_QgsTextAnnotationDialogBase(object):
    def setupUi(self, QgsTextAnnotationDialogBase):
        QgsTextAnnotationDialogBase.setObjectName(_fromUtf8("QgsTextAnnotationDialogBase"))
        QgsTextAnnotationDialogBase.resize(517, 364)
        self.gridLayout = QtGui.QGridLayout(QgsTextAnnotationDialogBase)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.mFontComboBox = QtGui.QFontComboBox(QgsTextAnnotationDialogBase)
        self.mFontComboBox.setObjectName(_fromUtf8("mFontComboBox"))
        self.horizontalLayout.addWidget(self.mFontComboBox)
        spacerItem = QtGui.QSpacerItem(38, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.mFontSizeSpinBox = QtGui.QSpinBox(QgsTextAnnotationDialogBase)
        self.mFontSizeSpinBox.setObjectName(_fromUtf8("mFontSizeSpinBox"))
        self.horizontalLayout.addWidget(self.mFontSizeSpinBox)
        self.mBoldPushButton = QtGui.QPushButton(QgsTextAnnotationDialogBase)
        self.mBoldPushButton.setMinimumSize(QtCore.QSize(50, 0))
        self.mBoldPushButton.setCheckable(True)
        self.mBoldPushButton.setObjectName(_fromUtf8("mBoldPushButton"))
        self.horizontalLayout.addWidget(self.mBoldPushButton)
        self.mItalicsPushButton = QtGui.QPushButton(QgsTextAnnotationDialogBase)
        self.mItalicsPushButton.setMinimumSize(QtCore.QSize(50, 0))
        self.mItalicsPushButton.setCheckable(True)
        self.mItalicsPushButton.setObjectName(_fromUtf8("mItalicsPushButton"))
        self.horizontalLayout.addWidget(self.mItalicsPushButton)
        self.mFontColorButton = QgsColorButton(QgsTextAnnotationDialogBase)
        self.mFontColorButton.setText(_fromUtf8(""))
        self.mFontColorButton.setAutoDefault(False)
        self.mFontColorButton.setObjectName(_fromUtf8("mFontColorButton"))
        self.horizontalLayout.addWidget(self.mFontColorButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.mButtonBox = QtGui.QDialogButtonBox(QgsTextAnnotationDialogBase)
        self.mButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.mButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.mButtonBox.setObjectName(_fromUtf8("mButtonBox"))
        self.gridLayout.addWidget(self.mButtonBox, 3, 0, 1, 1)
        self.mTextEdit = QtGui.QTextEdit(QgsTextAnnotationDialogBase)
        self.mTextEdit.setObjectName(_fromUtf8("mTextEdit"))
        self.gridLayout.addWidget(self.mTextEdit, 1, 0, 1, 1)
        self.mStackedWidget = QtGui.QStackedWidget(QgsTextAnnotationDialogBase)
        self.mStackedWidget.setObjectName(_fromUtf8("mStackedWidget"))
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.mStackedWidget.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.mStackedWidget.addWidget(self.page_2)
        self.gridLayout.addWidget(self.mStackedWidget, 2, 0, 1, 1)

        self.retranslateUi(QgsTextAnnotationDialogBase)
        self.mStackedWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.mButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QgsTextAnnotationDialogBase.accept)
        QtCore.QObject.connect(self.mButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QgsTextAnnotationDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(QgsTextAnnotationDialogBase)
        QgsTextAnnotationDialogBase.setTabOrder(self.mFontComboBox, self.mFontSizeSpinBox)
        QgsTextAnnotationDialogBase.setTabOrder(self.mFontSizeSpinBox, self.mBoldPushButton)
        QgsTextAnnotationDialogBase.setTabOrder(self.mBoldPushButton, self.mItalicsPushButton)
        QgsTextAnnotationDialogBase.setTabOrder(self.mItalicsPushButton, self.mFontColorButton)
        QgsTextAnnotationDialogBase.setTabOrder(self.mFontColorButton, self.mTextEdit)
        QgsTextAnnotationDialogBase.setTabOrder(self.mTextEdit, self.mButtonBox)

    def retranslateUi(self, QgsTextAnnotationDialogBase):
        QgsTextAnnotationDialogBase.setWindowTitle(_translate("QgsTextAnnotationDialogBase", "Annotation text", None))
        self.mBoldPushButton.setText(_translate("QgsTextAnnotationDialogBase", "B", None))
        self.mItalicsPushButton.setText(_translate("QgsTextAnnotationDialogBase", "I", None))

from qgscolorbutton import QgsColorButton
