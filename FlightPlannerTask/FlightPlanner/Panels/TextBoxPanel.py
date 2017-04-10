# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QWidget, QFrame, QSpacerItem, QTextEdit, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QToolButton, QIcon, QPixmap, QDialog, QPushButton
from PyQt4.QtCore import QSize, QSizeF, SIGNAL

class TextBoxPanel(QWidget):
    def __init__(self, parent, isArea = False):
        QWidget.__init__(self, parent)

        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("TextBoxPanel" + str(len(parent.findChildren(TextBoxPanel))))

        self.hLayoutBoxPanel = QHBoxLayout(self)
        self.hLayoutBoxPanel.setSpacing(0)
        self.hLayoutBoxPanel.setContentsMargins(0,0,0,0)
        self.hLayoutBoxPanel.setObjectName(("hLayoutBoxPanel"))
        self.frameBoxPanel = QFrame(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameBoxPanel.sizePolicy().hasHeightForWidth())
        self.frameBoxPanel.setSizePolicy(sizePolicy)
        self.frameBoxPanel.setFrameShape(QFrame.NoFrame)
        self.frameBoxPanel.setFrameShadow(QFrame.Raised)
        self.frameBoxPanel.setObjectName(("frameBoxPanel"))
        self.hLayoutframeBoxPanel = QHBoxLayout(self.frameBoxPanel)
        self.hLayoutframeBoxPanel.setSpacing(0)
        self.hLayoutframeBoxPanel.setMargin(0)
        self.hLayoutframeBoxPanel.setObjectName(("hLayoutframeBoxPanel"))
        self.captionLabel = QLabel(self.frameBoxPanel)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.captionLabel.sizePolicy().hasHeightForWidth())
        self.captionLabel.setSizePolicy(sizePolicy)
        self.captionLabel.setMinimumSize(QSize(200, 0))
        self.captionLabel.setMaximumSize(QSize(200, 16777215))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.captionLabel.setFont(font)
        self.captionLabel.setObjectName(("captionLabel"))
        self.hLayoutframeBoxPanel.addWidget(self.captionLabel)

        if not isArea:
            self.textBox = QLineEdit(self.frameBoxPanel)
            self.textBox.setEnabled(True)
            font = QFont()
            font.setBold(False)
            font.setWeight(50)
            self.textBox.setFont(font)
            self.textBox.setObjectName(("textBox"))
            self.textBox.setMinimumWidth(70)
            self.textBox.setMaximumWidth(70)
            # self.textBox.setText("0.0")
            self.hLayoutframeBoxPanel.addWidget(self.textBox)
        else:
            self.textBox = QTextEdit(self.frameBoxPanel)
            self.textBox.setEnabled(True)
            font = QFont()
            font.setBold(False)
            font.setWeight(50)
            self.textBox.setFont(font)
            self.textBox.setObjectName(("textBox"))
            # self.textBox.setText("0.0")
            self.textBox.setMaximumHeight(60)
            self.hLayoutframeBoxPanel.addWidget(self.textBox)

        self.imageButton = QPushButton(self.frameBoxPanel)
        self.imageButton.setText((""))
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/convex_hull.png")), QIcon.Normal, QIcon.Off)
        self.imageButton.setIcon(icon)
        self.imageButton.setObjectName(("imageButton"))
        self.imageButton.setVisible(False)
        self.hLayoutframeBoxPanel.addWidget(self.imageButton)

        self.hLayoutBoxPanel.addWidget(self.frameBoxPanel)

        self.spacerItem = QSpacerItem(0,0,QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayoutframeBoxPanel.addItem(self.spacerItem)

        self.textBox.textChanged.connect(self.textBoxChanged)
        self.imageButton.clicked.connect(self.imageButtonClicked)

        self.textBox.setText("")

        self.captionUnits = ""

        self.isArea = isArea

    def method_2(self, string0):
        self.textBox.setText(string0)
    def method_8(self, string_0):
        return "%s%s\t%s"%(string_0, self.Caption, self.Value);

    def textBoxChanged(self):
        self.emit(SIGNAL("Event_0"), self)

    def imageButtonClicked(self):
        self.emit(SIGNAL("Event_1"), self)
    def get_Caption(self):
        caption = self.captionLabel.text()
        findIndex = caption.indexOf("(")
        if findIndex > 0:
            val = caption.left(findIndex)
            return val
        return caption
    def set_Caption(self, captionStr):
        if captionStr == "":
            self.captionLabel.setText("")
            self.LabelWidth = 0
            return
        if self.CaptionUnits != "" and self.CaptionUnits != None:
            self.captionLabel.setText(captionStr + "(" + str(self.CaptionUnits) + ")" + ":")
        else:
            self.captionLabel.setText(captionStr + ":")
    Caption = property(get_Caption, set_Caption, None, None)

    def get_CaptionUnits(self):
        return self.captionUnits
    def set_CaptionUnits(self, captionUnits):
        self.captionUnits = captionUnits
    CaptionUnits = property(get_CaptionUnits, set_CaptionUnits, None, None)

    def set_ButtonVisible(self, bool):
        self.imageButton.setVisible(bool)
    ButtonVisible = property(None, set_ButtonVisible, None, None)

    def get_Value(self):
        if not self.isArea:
            return self.textBox.text()
        else:
            return self.textBox.toPlainText()

    def set_Value(self, valueStr):
        try:
            self.textBox.setText(valueStr)
        except:
            self.textBox.setText("")
    Value = property(get_Value, set_Value, None, None)
    Text = property(get_Value, set_Value, None, None)

    def get_IsEmpty(self):
        return self.textBox.text() == "" or self.textBox.text() == None
    IsEmpty = property(get_IsEmpty, None, None, None)

    def get_ReadOnly(self):
        return self.textBox.isReadOnly()
    def set_ReadOnly(self, bool):
        self.textBox.setReadOnly(bool)
    ReadOnly = property(get_ReadOnly, set_ReadOnly, None, None)

    def set_LabelWidth(self, width):
        self.captionLabel.setMinimumSize(QSize(width, 0))
        self.captionLabel.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)

    def get_Enabled(self):
        return self.textBox.isEnabled()
    def set_Enabled(self, bool):
        self.textBox.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)

    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)

    def set_Button(self, imageName):
        if imageName == None or imageName == "":
            self.imageButton.setVisible(False)
            return
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/" + imageName)), QIcon.Normal, QIcon.Off)
        self.imageButton.setIcon(icon)
        self.imageButton.setVisible(True)
    Button = property(None, set_Button, None, None)

    def set_Width(self, val):
        try:
            self.textBox.setMaximumWidth(val)
            self.textBox.setMinimumWidth(val)
        except:
            pass
    Width = property(None, set_Width, None, None)

    def set_EchoMode(self, value):
        if value == "Password":
            self.textBox.setEchoMode(QLineEdit.Password)
    EchoMode = property(None, set_EchoMode, None, None)
