# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FlightPlannerBase_NoTab.ui'
#
# Created: Sun May 18 16:23:34 2014
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

class Ui_FlightPlannerSimpleBase(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(538, 499)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        Dialog.setFont(font)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.scrollArea = QtGui.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget(Dialog)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 412, 479))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_ScrollWidget = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_ScrollWidget.setObjectName(_fromUtf8("verticalLayout_ScrollWidget"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.addWidget(self.scrollArea)
        self.frame_Btns = QtGui.QFrame(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_Btns.sizePolicy().hasHeightForWidth())
        self.frame_Btns.setSizePolicy(sizePolicy)
        self.frame_Btns.setMinimumSize(QtCore.QSize(0, 20))
        self.frame_Btns.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        self.frame_Btns.setFont(font)
        self.frame_Btns.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_Btns.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_Btns.setObjectName(_fromUtf8("frame_Btns"))
        self.verticalLayout_Btns = QtGui.QVBoxLayout(self.frame_Btns)
        self.verticalLayout_Btns.setObjectName(_fromUtf8("verticalLayout_Btns"))
        self.btnOpenData = QtGui.QPushButton(self.frame_Btns)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.btnOpenData.setFont(font)
        self.btnOpenData.setObjectName(_fromUtf8("btnOpenData"))
        self.verticalLayout_Btns.addWidget(self.btnOpenData)
        self.btnSaveData = QtGui.QPushButton(self.frame_Btns)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.btnSaveData.setFont(font)
        self.btnSaveData.setObjectName(_fromUtf8("btnSaveData"))
        self.verticalLayout_Btns.addWidget(self.btnSaveData)
        
        self.btnPDTCheck = QtGui.QPushButton(self.frame_Btns)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.btnPDTCheck.setFont(font)
        self.btnPDTCheck.setObjectName(_fromUtf8("btnPDTCheck"))
        self.verticalLayout_Btns.addWidget(self.btnPDTCheck)
        
        self.btnConstruct = QtGui.QPushButton(self.frame_Btns)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.btnConstruct.setFont(font)
        self.btnConstruct.setObjectName(_fromUtf8("btnConstruct"))
        self.verticalLayout_Btns.addWidget(self.btnConstruct)

        self.btnUpdateQA = QtGui.QPushButton(self.frame_Btns)
        # self.btnUpdateQA.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnUpdateQA.setFont(font)
        self.btnUpdateQA.setObjectName(_fromUtf8("btnUpdateQA"))
        self.btnUpdateQA.setText("Update QA")
        self.verticalLayout_Btns.addWidget(self.btnUpdateQA)

        self.btnExportResult = QtGui.QPushButton(self.frame_Btns)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.btnExportResult.setFont(font)
        self.btnExportResult.setObjectName(_fromUtf8("btnExportResult"))
        self.verticalLayout_Btns.addWidget(self.btnExportResult)
        self.btnClose = QtGui.QPushButton(self.frame_Btns)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.btnClose.setFont(font)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.verticalLayout_Btns.addWidget(self.btnClose)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_Btns.addItem(spacerItem)
        self.horizontalLayout_3.addWidget(self.frame_Btns)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/btnImage/openData.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnOpenData.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/btnImage/saveData.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSaveData.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/btnImage/construct.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnConstruct.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/btnImage/evaluate.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.btnEvaluate.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/btnImage/close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClose.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/btnImage/locate.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.btnEvaluate_2.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/btnImage/pdtCheck.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPDTCheck.setIcon(icon)
        icon = QtGui.QIcon()        
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/btnImage/close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.btnClose_2.setIcon(icon)
        icon = QtGui.QIcon()        
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/btnImage/exportResult.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnExportResult.setIcon(icon)
        
        self.btnClose.setToolTip(_fromUtf8("Close"))
#         self.btnClose_2.setToolTip(_fromUtf8("Close"))
        self.btnConstruct.setToolTip(_fromUtf8("Construct"))
#         self.btnEvaluate.setToolTip(_fromUtf8("Evaluate"))
#         self.btnLocate.setToolTip(_fromUtf8("Locate"))
        self.btnExportResult.setToolTip(_fromUtf8("Export Result"))
        self.btnOpenData.setToolTip(_fromUtf8("Open Data"))
        self.btnSaveData.setToolTip(_fromUtf8("Save Data"))
        self.btnPDTCheck.setToolTip(_fromUtf8("PDT Check"))
        self.btnUpdateQA.setToolTip(_fromUtf8("Update QA"))

        self.btnClose.setIconSize(QtCore.QSize(32,32))
        # self.btnClose_2.setIconSize(QtCore.QSize(32,32))
        self.btnConstruct.setIconSize(QtCore.QSize(32,32))
        # self.btnEvaluate.setIconSize(QtCore.QSize(32,32))
        # self.btnLocate.setIconSize(QtCore.QSize(32,32))
        self.btnExportResult.setIconSize(QtCore.QSize(32,32))
        self.btnOpenData.setIconSize(QtCore.QSize(32,32))
        self.btnSaveData.setIconSize(QtCore.QSize(32,32))
        self.btnPDTCheck.setIconSize(QtCore.QSize(32,32))
        self.btnUpdateQA.setIconSize(QtCore.QSize(32,32))

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
#         self.btnOpenData.setText(_translate("Dialog", "Open Data", None))
#         self.btnSaveData.setText(_translate("Dialog", "Save Data", None))
#         self.btnConstruct.setText(_translate("Dialog", "Construct", None))
#         self.btnPDTCheck.setText(_translate("Dialog", "PDT Check", None))
#         self.btnExportResult.setText(_translate("Dialog", "Export Result", None))
#         self.btnClose.setText(_translate("Dialog", "Close", None))

