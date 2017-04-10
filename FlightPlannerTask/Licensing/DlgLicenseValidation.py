# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Licensing.ui'
#
# Created: Thu May 19 12:45:18 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from Type.String import String
try:
    import clr, define, sys, mmsystem
except BaseException as ex:
    print ex.message
    print ex
mydll = clr.AddReference('SKGL')
from SKGL import Validate, Generate


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

class DlgLicenseValidation(QtGui.QDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setObjectName(_fromUtf8("DlgLicenseValidation"))
        self.setWindowTitle("FlightPlanner License Validation")
        self.resize(747, 388)
        self.setMinimumSize(QtCore.QSize(747, 450))
        # self.setMaximumSize(QtCore.QSize(747, 450))
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pnlHeader = QtGui.QFrame(self)
        self.pnlHeader.setMinimumSize(QtCore.QSize(742, 63))
        self.pnlHeader.setMaximumSize(QtCore.QSize(16777215, 63))
        self.pnlHeader.setStyleSheet(_fromUtf8("background-color: rgb(192, 187, 255);"))
        self.pnlHeader.setFrameShape(QtGui.QFrame.StyledPanel)
        self.pnlHeader.setFrameShadow(QtGui.QFrame.Raised)
        self.pnlHeader.setObjectName(_fromUtf8("pnlHeader"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.pnlHeader)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.labelHeader = QtGui.QLabel(self.pnlHeader)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.labelHeader.setFont(font)
        self.labelHeader.setFrameShape(QtGui.QFrame.NoFrame)
        self.labelHeader.setFrameShadow(QtGui.QFrame.Plain)
        self.labelHeader.setObjectName(_fromUtf8("labelHeader"))
        self.verticalLayout_2.addWidget(self.labelHeader)
        self.verticalLayout.addWidget(self.pnlHeader)
        self.pnlBody = QtGui.QFrame(self)
        self.pnlBody.setFrameShape(QtGui.QFrame.StyledPanel)
        self.pnlBody.setFrameShadow(QtGui.QFrame.Raised)
        self.pnlBody.setObjectName(_fromUtf8("pnlBody"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.pnlBody)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        # self.verticalLayout_3.addItem(spacerItem)
        self.frame_2 = QtGui.QFrame(self.pnlBody)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame_4 = QtGui.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.frame_4)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))

        self.lblMachineCode = QtGui.QLabel(self.frame_4)
        self.verticalLayout_6.addWidget(self.lblMachineCode)

        self.frame_6 = QtGui.QFrame(self.frame_4)
        self.frame_6.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_6.setObjectName(_fromUtf8("frame_6"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame_6)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelHeader_3 = QtGui.QLabel(self.frame_6)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.labelHeader_3.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.labelHeader_3.setFont(font)
        self.labelHeader_3.setAlignment(QtCore.Qt.AlignCenter)
        self.labelHeader_3.setObjectName(_fromUtf8("labelHeader_3"))
        self.horizontalLayout_3.addWidget(self.labelHeader_3)
        self.lnkWhatItIs = QtGui.QLabel(self.frame_6)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.lnkWhatItIs.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(True)
        self.lnkWhatItIs.setFont(font)
        self.lnkWhatItIs.setObjectName(_fromUtf8("lnkWhatItIs"))
        self.horizontalLayout_3.addWidget(self.lnkWhatItIs)
        spacerItem1 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_6.addWidget(self.frame_6)
        self.frame_5 = QtGui.QFrame(self.frame_4)
        self.frame_5.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_5.setObjectName(_fromUtf8("frame_5"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.frame_5)
        self.verticalLayout_7.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.frame = QtGui.QFrame(self.frame_5)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.txtKeyPart1 = QtGui.QLineEdit(self.frame)
        self.txtKeyPart1.setObjectName(_fromUtf8("txtKeyPart1"))
        self.txtKeyPart1.setMinimumHeight(23)
        self.txtKeyPart1.setMaximumWidth(80)

        self.horizontalLayout_5.addWidget(self.txtKeyPart1)
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.txtKeyPart2 = QtGui.QLineEdit(self.frame)
        self.txtKeyPart2.setObjectName(_fromUtf8("txtKeyPart2"))
        self.txtKeyPart2.setMinimumHeight(23)
        self.txtKeyPart2.setMaximumWidth(80)

        self.horizontalLayout_5.addWidget(self.txtKeyPart2)
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_5.addWidget(self.label_3)
        self.txtKeyPart3 = QtGui.QLineEdit(self.frame)
        self.txtKeyPart3.setObjectName(_fromUtf8("txtKeyPart3"))
        self.txtKeyPart3.setMinimumHeight(23)
        self.txtKeyPart3.setMaximumWidth(80)

        self.horizontalLayout_5.addWidget(self.txtKeyPart3)
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_5.addWidget(self.label_4)
        self.txtKeyPart4 = QtGui.QLineEdit(self.frame)
        self.txtKeyPart4.setObjectName(_fromUtf8("txtKeyPart4"))
        self.txtKeyPart4.setMinimumHeight(23)
        self.txtKeyPart4.setMaximumWidth(80)

        self.horizontalLayout_5.addWidget(self.txtKeyPart4)
        self.btnActivateNow = QtGui.QPushButton(self.frame)
        self.btnActivateNow.setMinimumSize(QtCore.QSize(160, 23))
        self.btnActivateNow.setObjectName(_fromUtf8("btnActivateNow"))
        self.btnActivateNow.setMinimumHeight(23)
        self.horizontalLayout_5.addWidget(self.btnActivateNow)
        self.verticalLayout_7.addWidget(self.frame)
        self.label = QtGui.QLabel(self.frame_5)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_7.addWidget(self.label)
        self.frame_7 = QtGui.QFrame(self.frame_5)
        self.frame_7.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_7.setObjectName(_fromUtf8("frame_7"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame_7)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.lnkBuyActivationCode = QtGui.QLabel(self.frame_7)
        self.lnkBuyActivationCode.setMinimumHeight(35)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.lnkBuyActivationCode.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(True)
        self.lnkBuyActivationCode.setFont(font)
        self.lnkBuyActivationCode.setObjectName(_fromUtf8("lnkBuyActivationCode"))
        self.horizontalLayout_4.addWidget(self.lnkBuyActivationCode)
        spacerItem2 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_7.addWidget(self.frame_7)
        self.verticalLayout_6.addWidget(self.frame_5)
        self.horizontalLayout.addWidget(self.frame_4)
        self.verticalLayout_3.addWidget(self.frame_2)
        spacerItem3 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        # self.verticalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.pnlBody)
        self.pnlFooter = QtGui.QFrame(self)
        self.pnlFooter.setMinimumSize(QtCore.QSize(0, 40))
        self.pnlFooter.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pnlFooter.setStyleSheet(_fromUtf8("background-color: rgb(192, 187, 255);"))
        self.pnlFooter.setFrameShape(QtGui.QFrame.StyledPanel)
        self.pnlFooter.setFrameShadow(QtGui.QFrame.Raised)
        self.pnlFooter.setObjectName(_fromUtf8("pnlFooter"))
        self.btnClose = QtGui.QPushButton(self.pnlFooter)
        self.btnClose.setGeometry(QtCore.QRect(666, 8, 75, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.btnClose.setPalette(palette)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.btnHelp = QtGui.QPushButton(self.pnlFooter)
        self.btnHelp.setGeometry(QtCore.QRect(10, 10, 41, 23))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 20, 158))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 20, 158))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.btnHelp.setPalette(palette)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.btnHelp.setFont(font)
        self.btnHelp.setFlat(True)
        self.btnHelp.setObjectName(_fromUtf8("btnHelp"))
        self.btnEndUserLicenceAgreement = QtGui.QPushButton(self.pnlFooter)
        self.btnEndUserLicenceAgreement.setGeometry(QtCore.QRect(60, 10, 171, 23))
        self.btnEndUserLicenceAgreement.setMinimumHeight(23)
        self.btnEndUserLicenceAgreement.setMinimumWidth(200)

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 20, 158))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 20, 158))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 187, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.btnEndUserLicenceAgreement.setPalette(palette)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.btnEndUserLicenceAgreement.setFont(font)
        self.btnEndUserLicenceAgreement.setFlat(True)
        self.btnEndUserLicenceAgreement.setObjectName(_fromUtf8("btnEndUserLicenceAgreement"))
        self.verticalLayout.addWidget(self.pnlFooter)

        self.btnClose.clicked.connect(self.btnClose_clicked)
        self.btnHelp.clicked.connect(self.btnHelp_clicked)
        self.btnActivateNow.clicked.connect(self.btnActivateNow_Click)
        self.btnEndUserLicenceAgreement.clicked.connect(self.btnEndUserLicenceAgreement_clicked)

        self.lnkBuyActivationCode.setTextFormat(QtCore.Qt.RichText)
        self.lnkBuyActivationCode.setText("<html><head/><body><p><a href=\"asd\"><span style=\" text-decoration: underline; color:#0000ff;\">Buy activation code</span></a></p></body></html>")
        self.lnkBuyActivationCode.linkActivated.connect(self.btnBuy_clicked)

        self.txtKeyPart1.textChanged.connect(self.txtKeyPart1_TextChanged)
        self.txtKeyPart2.textChanged.connect(self.txtKeyPart1_TextChanged)
        self.txtKeyPart3.textChanged.connect(self.txtKeyPart1_TextChanged)
        self.txtKeyPart4.textChanged.connect(self.txtKeyPart1_TextChanged)
        self.lnkWhatItIs.setVisible(False)
        

        # self.btnRequest.setVisible(False)
        # self.btnBuy.setMinimumWidth(130)
        # self.btnActivate.setMinimumWidth(130)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setWindowFlags(QtCore.Qt.SplashScreen)

        self.load()

        # dll = windll[r'E:\CholNam\FlightPlanner\Resource\dlls\SKGL.DLL']
        # result = dll.DllRegisterServer()
        # print result
    def load(self):
        # path = define.appPath
        # path += "/Resource/dlls/SKGL.dll"



        objValidate = Validate()

        # generate = Generate()
        # keyString = generate.doKey(72, objValidate.MachineCode)

        self.lblMachineCode.setText("    Your Machine Code is " + str(objValidate.MachineCode));
        self.btnActivateNow.setEnabled(False)
        # generate  = Generate()
        # keyString = generate.doKey(72)
        pass
        # print path

    def retranslateUi(self, Form):
        # Form.setWindowTitle(_translate("Form", "Form", None))
        self.labelHeader.setText(_translate("Form", "FlightPlanner Licensing", None))
        self.labelHeader_3.setText(_translate("Form", "Enter activation code.", None))
        self.lnkWhatItIs.setText(_translate("Form", "What it is?", None))
        self.label_2.setText(_translate("Form", "-", None))
        self.label_3.setText(_translate("Form", "-", None))
        self.label_4.setText(_translate("Form", "-", None))
        self.btnActivateNow.setText(_translate("Form", "Activate this application", None))
        self.label.setText(_translate("Form", "    If you do not have an activation code, you can purchse on online store.", None))
        # self.lnkBuyActivationCode.setText(_translate("Form", "Buy activation code", None))
        self.btnClose.setText(_translate("Form", "Close", None))
        self.btnHelp.setText(_translate("Form", "Help", None))
        self.btnEndUserLicenceAgreement.setText(_translate("Form", "End User Licence Agreement", None))


    def btnHelp_clicked(self):
        path = "http://www.flightplanner.se/help.html"
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(path))
    def btnEndUserLicenceAgreement_clicked(self):
        path = "http://www.flightplanner.se/eula.html"
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(path))
    def btnClose_clicked(self):
        self.reject()

    def btnBuy_clicked(self):
        path = "http://www.flightplanner.se"
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(path))

    def getLicenceKey(self):
        licanceKey = "";
        if (String.IsNullOrEmpty(self.txtKeyPart1.text()) == False and String.IsNullOrEmpty(self.txtKeyPart2.text()) == False and String.IsNullOrEmpty(self.txtKeyPart3.text()) == False and String.IsNullOrEmpty(self.txtKeyPart4.text()) == False):
            if (self.txtKeyPart1.text().length() == 5 and self.txtKeyPart2.text().length() == 5 and self.txtKeyPart3.text().length() == 5 and self.txtKeyPart4.text().length() == 5):
                licanceKey = self.txtKeyPart1.text() + "-" + self.txtKeyPart2.text() + "-" + self.txtKeyPart3.text() + "-" + self.txtKeyPart4.text();
        return licanceKey;

    def txtKeyPart1_TextChanged(self):
        if (String.IsNullOrEmpty(self.getLicenceKey()) == False):
            self.btnActivateNow.setEnabled(True);
        else:
            self.btnActivateNow.setEnabled(False);
    def btnActivateNow_Click(self):
        licenceKey = self.getLicenceKey();
        if (String.IsNullOrEmpty(licenceKey) == False):
            objValidate = Validate();
            objValidate.secretPhase = "aerodrome$pw3s$Pa$$W0rd"#Constants.SKGLSecretPhase;
            objValidate.Key = String.QString2Str(licenceKey).replace("-", "")

            # filePath = define.appPath + "/key.key"
            # fileStream = open(filePath, 'wb')
            # fileStream.write(licenceKey)
            # fileStream.close()
            # self.accept();


            if (objValidate.IsValid and objValidate.IsOnRightMachine):
                import _winreg as wr

                aReg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
                aKey = None
                try:
                    targ = r'SOFTWARE\Microsoft\Windows\FlightPlannerLicense'
                    print "*** Writing to", targ, "***"
                    try:
                        aKey = wr.OpenKey(aReg, targ, 0, wr.KEY_WRITE)
                    except:
                        aKey = wr.CreateKey(aReg, targ)
                    try:
                        try:
                            wr.SetValueEx(aKey, "License", 0, wr.REG_SZ, String.QString2Str(licenceKey))
                        except Exception:
                            print "Encountered problems writing into the Registry..."
                    except:
                        print "NO"
                    finally:
                        wr.CloseKey(aKey)
                except:
                    print "no"
                finally:
                    try:
                        wr.CloseKey(aReg)
                        self.accept()
                    except:
                        pass
            else:
                QtGui.QMessageBox.warning(self, "Warning", "Please enter a valid key.");