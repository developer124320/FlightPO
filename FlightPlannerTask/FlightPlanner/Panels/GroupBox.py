# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QGroupBox, QMessageBox, QSizePolicy


class GroupBox(QGroupBox):
    def __init__(self, parent, layoutStyle = "VL"):
        QGroupBox.__init__(self, parent)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.layoutBoxPanel = None
        if layoutStyle == "VL":
            self.layoutBoxPanel = QVBoxLayout(self)
            self.layoutBoxPanel.setSpacing(6)
            self.layoutBoxPanel.setContentsMargins(6,6,6,6)
            self.layoutBoxPanel.setObjectName(("layoutBoxPanel"))
        elif layoutStyle == "HL":
            self.layoutBoxPanel = QHBoxLayout(self)
            self.layoutBoxPanel.setSpacing(0)
            self.layoutBoxPanel.setContentsMargins(6,6,6,6)
            self.layoutBoxPanel.setObjectName(("layoutBoxPanel"))
        
        self.setTitle("GroupBox")
    
    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)
    def get_Title(self):
        return self.title()
    def set_Title(self, titleStr):
        self.setTitle(titleStr)
    Title = property(get_Title, set_Title, None, None)

    def set_Margin(self, left, top = None, right = None, bottom = None):
        try:
            if top == None:
                self.layoutBoxPanel.setMargin(left, left, left, left)
                return
            elif right == None:
                self.layoutBoxPanel.setMargin(left, top, left, top)
                return
            self.layoutBoxPanel.setMargin(left, top, right, bottom)
        except:
            str0 = "You must set the magin of frame with the int type."
            QMessageBox.warning(self, "Warning" , str0)
    Margin = property(None, set_Margin, None, None)

    def set_Add(self, widget):
        self.layoutBoxPanel.addWidget(widget)
    Add = property(None, set_Add, None, None)

    def get_Enabled(self):
        return self.isEnabled()
    def set_Enabled(self, bool):
        self.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)

    def get_Caption(self):
        caption = self.title()
        return caption
    def set_Caption(self, captionStr):
        self.setTitle(captionStr)
    Caption = property(get_Caption, set_Caption, None, None)