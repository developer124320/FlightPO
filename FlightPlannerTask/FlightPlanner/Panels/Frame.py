# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QFrame, QHBoxLayout, QVBoxLayout, QMessageBox, QSizePolicy


class Frame(QFrame):
    def __init__(self, parent, layoutStyle = "VL"):
        QFrame.__init__(self, parent)

        # sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        # self.setSizePolicy(sizePolicy)

        self.layoutBoxPanel = None
        if layoutStyle == "VL":
            self.layoutBoxPanel = QVBoxLayout(self)
            self.layoutBoxPanel.setSpacing(6)
            self.layoutBoxPanel.setContentsMargins(0,0,0,0)
            self.layoutBoxPanel.setObjectName(("layoutBoxPanel"))
        elif layoutStyle == "HL":
            self.layoutBoxPanel = QHBoxLayout(self)
            self.layoutBoxPanel.setSpacing(6)
            self.layoutBoxPanel.setContentsMargins(0,0,0,0)
            self.layoutBoxPanel.setObjectName(("layoutBoxPanel"))

    def set_Margin(self, value):
        try:
            # if top == None:
            #     self.layoutBoxPanel.setMargin(left, left, left, left)
            #     return
            # elif right == None:
            #     self.layoutBoxPanel.setMargin(left, top, left, top)
            #     return
            self.layoutBoxPanel.setMargin(value)
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

    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)

    def set_Spacing(self, val):
        self.layoutBoxPanel.setSpacing(val)
    Spacing = property(None, set_Spacing, None, None)

    # def set_LayoutSpacing(self, value):
    #     self.setLa