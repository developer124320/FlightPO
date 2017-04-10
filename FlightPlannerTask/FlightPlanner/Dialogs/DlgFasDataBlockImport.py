# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QFileDialog, QDialog, QPushButton, QDialogButtonBox
from PyQt4.QtCore import QSizeF, SIGNAL, QCoreApplication
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.GroupBox import GroupBox
from Type.FasDataBlockFile import FasDataBlockFile
import define



class DlgFasDataBlockImport(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(290, 136);
        self.setWindowTitle("Reference Positions")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth());
        self.setSizePolicy(sizePolicy);
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"));

        self.groupBox = GroupBox(self)
        self.groupBox.Caption = "Output Data"
        verticalLayoutDlg.addWidget(self.groupBox)

        self.txtDataBlock = TextBoxPanel(self.groupBox, True)
        self.txtDataBlock.Caption = "Data Block"
        self.txtDataBlock.Value = "10 20 10 07 05 8C 20 02 01 36 30 05 54 9D AA 18 7C E8 D5 FC 72 16 A0 F5 00 94 96 02 2C 81 2C 01 64 01 C8 FA 6A E4 AF 51"
        self.groupBox.Add = self.txtDataBlock

        self.pnlSuppliedCRC = TextBoxPanel(self.groupBox)
        self.pnlSuppliedCRC.Caption = "Supplied CRC Value"
        self.pnlSuppliedCRC.ReadOnly = True
        self.groupBox.Add = self.pnlSuppliedCRC

        self.pnlCalculatedCRC = TextBoxPanel(self.groupBox)
        self.pnlCalculatedCRC.Caption = "Calculated CRC Value"
        self.pnlCalculatedCRC.ReadOnly = True
        self.groupBox.Add = self.pnlCalculatedCRC

        self.frameBtn = Frame(self, "HL")
        verticalLayoutDlg.addWidget(self.frameBtn)

        self.btnFile = QPushButton(self.frameBtn)
        self.btnFile.setObjectName(("btnFile"));
        self.btnFile.setText("File...")
        self.frameBtn.Add = self.btnFile

        self.btnBoxOkCancel = QDialogButtonBox(self.frameBtn)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        self.btnFile.clicked.connect(self.btnFile_clicked)


        self.frameBtn.Add = self.btnBoxOkCancel

        self.txtDataBlock.textBox.textChanged.connect(self.txtDataBlock_TextChanged)
    def acceptDlg(self):
        if self.txtDataBlock.Value == "":
            self.reject()
            return
        self.accept()
    # def reject(self):
    #     self.reject()
    def btnFile_clicked(self):
        filePathDir = QFileDialog.getOpenFileName(self, "Open Fas Data",QCoreApplication.applicationDirPath (),"FAS Data Block Binary Files (*.bin)")
        if filePathDir == "":
            return
        fasDataBlockFile = FasDataBlockFile();
        fasDataBlockFile.method_1(filePathDir);
        self.txtDataBlock.Value = fasDataBlockFile.HexString;
    def method_5(self):
        flag = False;
        # self.errorProvider.method_1();
        fasDataBlockFile = FasDataBlockFile()
        fasDataBlockFile.set_HexString(self.txtDataBlock.Value)
        if self.txtDataBlock.Value == "":
            self.pnlCalculatedCRC.set_Value("");
        else:
            self.pnlCalculatedCRC.set_Value(fasDataBlockFile.CRC);
        if self.txtDataBlock.Value == "":
            self.pnlSuppliedCRC.set_Value("");
        else:
            value = fasDataBlockFile.HexString.split(' ')
            str0 = ""
            for i in range(36, 40):
                str0 += value[i]
            self.pnlSuppliedCRC.set_Value(str0);
        flag = True;
        # except:
        #     # self.errorProvider.method_0(self.txtDataBlock, exception.Message);
        #     self.pnlCalculatedCRC.Value = "";
        #     self.pnlSuppliedCRC.Value = "";
        #     return False;
        return flag;

    @staticmethod
    def smethod_0(parent):
        fasDataBlockFile = None;
        dlgFasDataBlockImport = DlgFasDataBlockImport()
        dlgFasDataBlockImport.txtDataBlock.set_Value("");
        dlgFasDataBlockImport.pnlCalculatedCRC.set_Value("");
        dlgResult = dlgFasDataBlockImport.exec_()
        if dlgResult != 1:
            fasDataBlockFile = None;
        else:
            fasDataBlockFile = FasDataBlockFile()
            fasDataBlockFile.set_HexString(dlgFasDataBlockImport.txtDataBlock.get_Value())
        return fasDataBlockFile;

    def txtDataBlock_TextChanged(self):
        self.method_5();









