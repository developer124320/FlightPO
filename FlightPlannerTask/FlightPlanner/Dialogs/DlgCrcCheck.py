# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox, QTextEdit
from PyQt4.QtCore import QString, QFileInfo
from PyQt4.QtCore import  SIGNAL
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from Type.FasDataBlockFile import FasDataBlockFile


class DlgCrcCheck(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(100, 70);
        self.setWindowTitle("CRC Check")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth());
        self.setSizePolicy(sizePolicy);
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"));

        self.groupBox1 = GroupBox(self)
        self.groupBox1.Caption = ""
        verticalLayoutDlg.addWidget(self.groupBox1)

        self.pnlSuppliedCrcValue = TextBoxPanel(self.groupBox1)
        self.pnlSuppliedCrcValue.Caption = "Supplied CRC Value"
        self.pnlSuppliedCrcValue.LabelWidth = 120
        self.pnlSuppliedCrcValue.Enabled = False
        self.groupBox1.Add = self.pnlSuppliedCrcValue

        self.pnlCalculatedCrcValue = TextBoxPanel(self.groupBox1)
        self.pnlCalculatedCrcValue.Caption = "Calculated CRC Value"
        self.pnlCalculatedCrcValue.LabelWidth = 120
        self.pnlCalculatedCrcValue.Enabled = False
        self.groupBox1.Add = self.pnlCalculatedCrcValue

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        # btnOK = self.btnBoxOkCancel.button(QDialogButtonBox.Ok)
        # btnOK.setText("Create")
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)


        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)


        self.crcCalcMethodStr = None

        # self.pnlCodeType.Items = CodeTypeDesigPtAixm.Items

    def acceptDlg(self):

        self.accept()



    @staticmethod
    def smethod_0(parent, inputFilePath, crcCalcMethodStr = None):
        flag = False;
        dlgCrcCheck = DlgCrcCheck(parent)
        dlgCrcCheck.crcCalcMethodStr = crcCalcMethodStr;

        contents = None
        try:
            with open(inputFilePath, 'rb', 0) as tempFile:
                contents = tempFile.read()
                tempFile.close()
        except:
            return False
        bytes = FasDataBlockFile.CRC_Calculation(contents)

        string_0 = QString(inputFilePath)

        crcFileDir = string_0.left(string_0.length() - 3) + "crc"
        fileInfo = QFileInfo(crcFileDir)
        if not fileInfo.exists():
            if QMessageBox.warning(dlgCrcCheck, "Warning", "CRC file is not existing.\nDo you want to create the CRC file for this file?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return False
            contents = None
            # with open(inputFilePath, 'rb', 0) as tempFile:
            #     contents = tempFile.read()
            #     tempFile.flush()
            #     tempFile.close()
            # bytes = FasDataBlockFile.CRC_Calculation(contents)
            # string_0 = QString(inputFilePath)
            # path = string_0.left(string_0.length() - 3) + "crc"
            fileStream = open(crcFileDir, 'wb')
            fileStream.write(bytes)
            fileStream.close()

        crcFileContents = None
        with open(crcFileDir, 'rb', 0) as tempFileCrc:
            crcFileContents = tempFileCrc.read()
            tempFileCrc.close()
        if bytes != crcFileContents:
            dlgCrcCheck.pnlCalculatedCrcValue.textBox.setStyleSheet("color: rgb(255, 0, 0);");
        else:
            dlgCrcCheck.pnlCalculatedCrcValue.textBox.setStyleSheet("color: rgb(0, 0, 0);");
        dlgCrcCheck.pnlSuppliedCrcValue.Value = crcFileContents
        dlgCrcCheck.pnlCalculatedCrcValue.Value = bytes


        resultDlg = dlgCrcCheck.exec_()
        if (resultDlg == 0):
            flag = False;
        else:
            flag = True;
        return flag