# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox, QFileDialog
from PyQt4.QtCore import QString, QFileInfo
from PyQt4.QtCore import  SIGNAL, QCoreApplication
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from Type.FasDataBlockFile import FasDataBlockFile


class DlgCrcReadWrite(QDialog):
    def __init__(self, parent, rwFlag = "r"):
        QDialog.__init__(self, parent)
        self.rwFlag = rwFlag
        self.resize(100, 70);
        if self.rwFlag == "r":
            self.setWindowTitle("CRC Reader")
        else:
            self.setWindowTitle("CRC Writer")
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

        self.pnlFile = TextBoxPanel(self.groupBox1)
        self.pnlFile.Caption = "File"
        self.pnlFile.LabelWidth = 120
        self.pnlFile.textBox.setMaximumWidth(200)
        self.pnlFile.textBox.setMinimumWidth(200)
        self.pnlFile.Button = "openData.png"
        self.groupBox1.Add = self.pnlFile

        self.pnlSuppliedCrcValue = TextBoxPanel(self.groupBox1)
        self.pnlSuppliedCrcValue.Caption = "Supplied CRC Value"
        self.pnlSuppliedCrcValue.LabelWidth = 120
        self.pnlSuppliedCrcValue.Enabled = False
        self.groupBox1.Add = self.pnlSuppliedCrcValue

        if self.rwFlag == "w":
            self.pnlSuppliedCrcValue.Visible = False


        self.pnlCalculatedCrcValue = TextBoxPanel(self.groupBox1)
        self.pnlCalculatedCrcValue.Caption = "Calculated CRC Value"
        self.pnlCalculatedCrcValue.LabelWidth = 120
        self.pnlCalculatedCrcValue.Enabled = False
        self.groupBox1.Add = self.pnlCalculatedCrcValue

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        btnQuit = self.btnBoxOkCancel.button(QDialogButtonBox.Ok)
        btnQuit.setText("Quit")
        btnCancel = self.btnBoxOkCancel.button(QDialogButtonBox.Cancel)
        btnCancel.setVisible(False)

        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)

        self.connect(self.pnlFile, SIGNAL("Event_1"), self.pnlFileEvent_1)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)

    def pnlFileEvent_1(self):

        inputFilePath = QFileDialog.getOpenFileName(self, "Open Xml File",QCoreApplication.applicationDirPath (),"Xml Files (*.xml)")
        if inputFilePath == "":
            return
        fileInfo = QFileInfo(inputFilePath)
        self.pnlFile.Value = fileInfo.fileName()
        contents = None
        with open(inputFilePath, 'rb', 0) as tempFile:
            contents = tempFile.read()
            tempFile.close()
        bytes = FasDataBlockFile.CRC_Calculation(contents)

        string_0 = QString(inputFilePath)

        crcFileDir = string_0.left(string_0.length() - 3) + "crc"
        fileInfo = QFileInfo(crcFileDir)
        if self.rwFlag == "r":
            if not fileInfo.exists():
                QMessageBox.warning(self, "Warning", "CRC file is not existing.")
                return
            crcFileContents = None
            with open(crcFileDir, 'rb', 0) as tempFileCrc:
                crcFileContents = tempFileCrc.read()
                tempFileCrc.close()
            if bytes != crcFileContents:
                self.pnlCalculatedCrcValue.textBox.setStyleSheet("color: rgb(255, 0, 0);");
            else:
                self.pnlCalculatedCrcValue.textBox.setStyleSheet("color: rgb(0, 0, 0);");
            self.pnlSuppliedCrcValue.Value = crcFileContents
            self.pnlCalculatedCrcValue.Value = bytes
        else:
            fileStream = open(crcFileDir, 'wb')
            fileStream.write(bytes)
            fileStream.close()
            self.pnlCalculatedCrcValue.Value = bytes




    def acceptDlg(self):

        self.accept()



    @staticmethod
    def smethod_0(parent, inputFilePath, rwFlag = "r"):
        flag = False;
        dlgCrcReadWrite = DlgCrcReadWrite(parent, rwFlag)

        resultDlg = dlgCrcReadWrite.exec_()
        if (resultDlg == 0):
            flag = False;
        else:
            flag = True;
        return flag
