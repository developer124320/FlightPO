# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_MSA.ui'
#
# Created: Wed Jul 15 15:10:04 2015
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

class Ui_MSADlg(object):
    def setupUi(self, ui_MSA):
        ui_MSA.setObjectName(_fromUtf8("ui_MSA"))
        ui_MSA.resize(476, 226)
        self.uiMsa = ui_MSA
        self.verticalLayout = QtGui.QVBoxLayout(self.uiMsa)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        

        self.gbParameters = QtGui.QGroupBox(ui_MSA)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.gbParameters.setFont(font)
        self.gbParameters.setObjectName(_fromUtf8("gbParameters"))
        self.gbParameters.setTitle(_fromUtf8("Parameters"))
        self.vl_gbParameters = QtGui.QVBoxLayout(self.gbParameters)
        self.vl_gbParameters.setObjectName(_fromUtf8("vl_gbParameters"))
        self.frameMoc = QtGui.QFrame(self.gbParameters)
        self.frameMoc.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameMoc.setFrameShadow(QtGui.QFrame.Raised)
        self.frameMoc.setObjectName(_fromUtf8("frameMoc"))
        self.horizontalLayoutMoc = QtGui.QHBoxLayout(self.frameMoc)
        self.horizontalLayoutMoc.setSpacing(0)
        self.horizontalLayoutMoc.setMargin(0)
        self.horizontalLayoutMoc.setObjectName(_fromUtf8("horizontalLayoutMoc"))
        self.label_82 = QtGui.QLabel(self.frameMoc)
        self.label_82.setMinimumSize(QtCore.QSize(100, 0))
        self.label_82.setMaximumSize(QtCore.QSize(100, 121221))
        self.label_82.setText(_fromUtf8("Moc(m):"))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_82.setFont(font)
        self.label_82.setObjectName(_fromUtf8("label_82"))
        self.horizontalLayoutMoc.addWidget(self.label_82)
        self.txtMoc = QtGui.QLineEdit(self.frameMoc)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtMoc.setFont(font)
        self.txtMoc.setObjectName(_fromUtf8("txtMoc"))
        self.txtMoc.setText(_fromUtf8("300"))
        self.txtMoc.setMinimumSize(QtCore.QSize(60, 0))
        self.txtMoc.setMaximumSize(QtCore.QSize(60, 121221))
        self.horizontalLayoutMoc.addWidget(self.txtMoc)
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayoutMoc.addItem(horizontalSpacer)
        self.vl_gbParameters.addWidget(self.frameMoc)
        
        self.frameMOCmultipiler = QtGui.QFrame(self.gbParameters)
        self.frameMOCmultipiler.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameMOCmultipiler.setFrameShadow(QtGui.QFrame.Raised)
        self.frameMOCmultipiler.setObjectName(_fromUtf8("frameMOCmultipiler"))
        self.horizontalLayoutMOCmultipiler = QtGui.QHBoxLayout(self.frameMOCmultipiler)
        self.horizontalLayoutMOCmultipiler.setSpacing(0)
        self.horizontalLayoutMOCmultipiler.setMargin(0)
        self.horizontalLayoutMOCmultipiler.setObjectName(_fromUtf8("horizontalLayoutMOCmultipiler"))
        self.label_85 = QtGui.QLabel(self.frameMOCmultipiler)
        self.label_85.setMinimumSize(QtCore.QSize(100, 0))
        self.label_85.setMaximumSize(QtCore.QSize(100, 121221))
        self.label_85.setText(_fromUtf8("MOCmultipiler:"))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_85.setFont(font)
        self.label_85.setObjectName(_fromUtf8("label_85"))
        self.horizontalLayoutMOCmultipiler.addWidget(self.label_85)
        self.mocSpinBox = QtGui.QSpinBox(self.frameMOCmultipiler)
        self.mocSpinBox.setMinimum(1)
        self.mocSpinBox.setProperty("value", 1)
        self.mocSpinBox.setObjectName(_fromUtf8("mocSpinBox"))
        self.mocSpinBox.setMinimumSize(QtCore.QSize(60, 0))
        self.mocSpinBox.setMaximumSize(QtCore.QSize(60, 121221))
        self.horizontalLayoutMOCmultipiler.addWidget(self.mocSpinBox)
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayoutMOCmultipiler.addItem(horizontalSpacer)
        self.vl_gbParameters.addWidget(self.frameMOCmultipiler)
        
        self.verticalLayout.addWidget(self.gbParameters)
        
        self.grbSectors = QtGui.QGroupBox(ui_MSA)
        self.grbSectors.setObjectName(_fromUtf8("grbSectors"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.grbSectors)
        self.verticalLayout_2.setMargin(5)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frameSelectors = QtGui.QFrame(self.grbSectors)
        self.frameSelectors.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameSelectors.setFrameShadow(QtGui.QFrame.Raised)
        self.frameSelectors.setObjectName(_fromUtf8("frameSelectors"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frameSelectors)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.picPreview = QtGui.QGraphicsView(self.frameSelectors)
        self.picPreview.setFixedWidth(100)
#         self.picPreview.setMinimumSize(QtCore.QSize(0, 150))
#         self.picPreview.setMaximumSize(QtCore.QSize(120, 16777215))
        self.picPreview.setObjectName(_fromUtf8("picPreview"))
        self.horizontalLayout.addWidget(self.picPreview)
        self.tableViewSectors = QtGui.QTableView(self.frameSelectors)
        self.tableViewSectors.setMinimumSize(QtCore.QSize(0, 150))
        self.tableViewSectors.setObjectName(_fromUtf8("tableViewSectors"))
        self.horizontalLayout.addWidget(self.tableViewSectors)
        self.verticalLayout_2.addWidget(self.frameSelectors)
        self.frameButton = QtGui.QFrame(self.grbSectors)
        self.frameButton.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameButton.setFrameShadow(QtGui.QFrame.Raised)
        self.frameButton.setObjectName(_fromUtf8("frameButton"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frameButton)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(120, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnSectorNew = QtGui.QPushButton(self.frameButton)
        self.btnSectorNew.setObjectName(_fromUtf8("btnSectorNew"))
        self.horizontalLayout_2.addWidget(self.btnSectorNew)
        self.btnSectorSplit = QtGui.QPushButton(self.frameButton)
        self.btnSectorSplit.setObjectName(_fromUtf8("btnSectorSplit"))
        self.horizontalLayout_2.addWidget(self.btnSectorSplit)
        self.btnSectorModify = QtGui.QPushButton(self.frameButton)
        self.btnSectorModify.setObjectName(_fromUtf8("btnSectorModify"))
        self.horizontalLayout_2.addWidget(self.btnSectorModify)
        self.btnSectorDelete = QtGui.QPushButton(self.frameButton)
        self.btnSectorDelete.setObjectName(_fromUtf8("btnSectorDelete"))
        self.horizontalLayout_2.addWidget(self.btnSectorDelete)
        self.verticalLayout_2.addWidget(self.frameButton)
        self.verticalLayout.addWidget(self.grbSectors)

        self.retranslateUi(ui_MSA)
        QtCore.QMetaObject.connectSlotsByName(ui_MSA)

    def retranslateUi(self, ui_MSA):
        ui_MSA.setWindowTitle(_translate("ui_MSA", "Minimum Sector Altitudes(MSA)", None))
        self.grbSectors.setTitle(_translate("ui_MSA", "Sectors", None))
        self.btnSectorNew.setText(_translate("ui_MSA", "New...", None))
        self.btnSectorSplit.setText(_translate("ui_MSA", "Split...", None))
        self.btnSectorModify.setText(_translate("ui_MSA", "Modify...", None))
        self.btnSectorDelete.setText(_translate("ui_MSA", "Delete...", None))

