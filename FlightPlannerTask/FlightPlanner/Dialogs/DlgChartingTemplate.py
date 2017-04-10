# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox
from PyQt4.QtCore import QString, QFileInfo
from PyQt4.QtCore import  SIGNAL
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.types import DrawingSpace

from Type.String import String


class DlgChartingTemplate(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(100, 70)
        self.setWindowTitle("Template Properties")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"))

        self.groupBox1 = GroupBox(self)
        self.groupBox1.Caption = ""
        verticalLayoutDlg.addWidget(self.groupBox1)

        self.pnlSpace = ComboBoxPanel(self.groupBox1)
        self.pnlSpace.Caption = "Target Space"
        self.pnlSpace.LabelWidth = 120
        self.groupBox1.Add = self.pnlSpace

        self.pnlDwg = TextBoxPanel(self.groupBox1)
        self.pnlDwg.Caption = "Drawing File"
        self.pnlDwg.LabelWidth = 120
        self.groupBox1.Add = self.pnlDwg

        self.pnlTitle = TextBoxPanel(self.groupBox1)
        self.pnlTitle.Caption = "Titlee"
        self.pnlTitle.LabelWidth = 120
        self.groupBox1.Add = self.pnlTitle

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"))
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        # btnOK = self.btnBoxOkCancel.button(QDialogButtonBox.Ok)
        # btnOK.setText("Create")
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)


        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)


        self.pnlSpace.Add(DrawingSpace.ModelSpace)
        self.pnlSpace.Add(DrawingSpace.PaperSpace)
        self.pnlSpace.SelectedIndex = 1
        
        # if (String.IsNullOrEmpty(self.pnlDwg.Value)):
        #     # DlgChartingTemplate height = self
        #     # height.Height = height.Height - self.pnlDwg.Height
        #     self.pnlDwg.Visible = False

        # self.pnlCodeType.Items = CodeTypeDesigPtAixm.Items

    def acceptDlg(self):

        self.accept()

    def get_TemplateDrawing(self):
        return self.pnlDwg.Value
    def set_TemplateDrawing(self, val):
        self.pnlDwg.Value = val
    TemplateDrawing = property(get_TemplateDrawing, set_TemplateDrawing, None, None)

    def get_TemplateSpace(self):
        if (self.pnlSpace.SelectedIndex == 0):
            return DrawingSpace.ModelSpace
        return DrawingSpace.PaperSpace
    def set_TemplateSpace(self, val):
        if (val == DrawingSpace.ModelSpace):
            self.pnlSpace.SelectedIndex = 0
            return
        self.pnlSpace.SelectedIndex = 1
    TemplateSpace = property(get_TemplateSpace, set_TemplateSpace, None, None)

    def get_TemplateTitle(self):
        return self.pnlTitle.Value
    def set_TemplateTitle(self, val):
        self.pnlTitle.Value = val
    TemplateTitle = property(get_TemplateTitle, set_TemplateTitle, None, None)


    @staticmethod
    def smethod_0(parent, string_0, drawingSpace_0, string_1):
        flag = False
        dlgChartingTemplate = DlgChartingTemplate(parent)
        dlgChartingTemplate.TemplateTitle = string_0
        dlgChartingTemplate.TemplateDrawing = string_1
        dlgChartingTemplate.TemplateSpace = drawingSpace_0
        result = dlgChartingTemplate.exec_()
        if (not result):
            flag = False
        else:
            string_0 = dlgChartingTemplate.TemplateTitle
            drawingSpace_0 = dlgChartingTemplate.TemplateSpace
            flag = True
        return flag, string_0, drawingSpace_0

    @staticmethod
    def smethod_1(parent, string_0, drawingSpace_0):
        flag = False
        dlgChartingTemplate = DlgChartingTemplate(parent)
        dlgChartingTemplate.TemplateTitle = string_0
        dlgChartingTemplate.TemplateSpace = drawingSpace_0
        result = dlgChartingTemplate.exec_()
        if (not result):
            flag = False
        else:
            string_0 = dlgChartingTemplate.TemplateTitle
            drawingSpace_0 = dlgChartingTemplate.TemplateSpace
            flag = True
        return flag, string_0, drawingSpace_0