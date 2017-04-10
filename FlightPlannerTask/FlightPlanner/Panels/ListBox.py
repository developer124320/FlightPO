# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QWidget, QFrame, QVBoxLayout, QListWidget, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QToolButton, QIcon, QPixmap, QDialog
from PyQt4.QtCore import QSize, QString, SIGNAL
import define

class ListBox(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("ListBox" + str(len(parent.findChildren(ListBox))))


        self.hLayoutBoxPanel = QHBoxLayout(self)
        self.hLayoutBoxPanel.setSpacing(0)
        self.hLayoutBoxPanel.setContentsMargins(3,3,3,3)
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

        self.listBox = QListWidget(self.frameBoxPanel)
        self.listBox.setEnabled(True)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.listBox.setFont(font)
        self.listBox.setObjectName(("listBox"))
        # self.listBox.setText("0.0")
        self.hLayoutframeBoxPanel.addWidget(self.listBox)

        self.imageButton = QToolButton(self.frameBoxPanel)
        self.imageButton.setText((""))
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/convex_hull.png")), QIcon.Normal, QIcon.Off)
        self.imageButton.setIcon(icon)
        self.imageButton.setObjectName(("imageButton"))
        self.imageButton.setVisible(False)
        self.hLayoutframeBoxPanel.addWidget(self.imageButton)

        self.hLayoutBoxPanel.addWidget(self.frameBoxPanel)

        self.listBox.currentRowChanged.connect(self.listBoxChanged)
        self.imageButton.clicked.connect(self.imageButtonClicked)

        

        self.captionUnits = ""

        self.hasObject = False

        self.objectList = []
        self.captionLabel.setVisible(False)
    def get_Count(self):
        return self.listBox.count()
    Count = property(get_Count, None, None, None)
    def method_3(self, string_0):
        return self.listBox.row(self.listBox.findItems(string_0)[0]);

    def method_11(self, string_0):
        if (self.IsEmpty):
            return "%s%s\t"%(string_0, self.Caption);
        return "%s%s\t%s %s"%(string_0, self.Caption, self.Value, self.CaptionUnits);

    def listBoxChanged(self, index):
        i = index
        self.emit(SIGNAL("Event_0"), self)
    def IndexOf(self, item):
        if isinstance(item, str):
            return self.listBox.row(self.listBox.findItems(item)[0]);
        else:
            return self.listBox.row(self.listBox.findItems(item.ToString())[0]);

    def Contains(self, item):
        compStr = None
        if isinstance(item, str):
            compStr = item
        elif isinstance(item, float) or isinstance(item, int):
            compStr = str(item)
        else:
            compStr = item.ToString()
        for i in range(self.listBox.count()):
            comboItemstr = self.listBox.item(i).text()
            if compStr == comboItemstr:
                return True
        return False


    def Clear(self):
        self.listBox.clear()
        self.objectList = []
        self.hasObject = False
    def Add(self, item):
        if not isinstance(item, str) and not isinstance(item, QString):
            self.listBox.addItem(item.ToString())
            self.objectList.append(item)
            self.hasObject = True
            return
        self.listBox.addItem(item)
        self.hasObject = False
        return self.listBox.count() - 1
    def Insert(self, index, item):
        if not isinstance(item, str):
            self.listBox.insertItem(index, item.ToString())
            self.objectList.insert(index, item)
            self.hasObject = True
            return
        self.listBox.insertItem(index, item)
        self.hasObject = False
    def imageButtonClicked(self):
        self.emit(SIGNAL("Event_3"), self)
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

    # def get_Value(self):
    #     return self.listBox.currentIndex()
    #
    # def set_Value(self, value):
    #     try:
    #         self.listBox.setCurrentIndex(value)
    #     except:
    #         self.textBox.setText("")
    # Value = property(get_Value, set_Value, None, None)

    # def get_IsEmpty(self):
    #     return self.listBox.currentText() == "" or self.listBox.currentIndex() == -1
    # IsEmpty = property(get_IsEmpty, None, None, None)

    # def get_ReadOnly(self):
    #     return self.listBox.isReadOnly()
    # # def set_ReadOnly(self, bool):
    # #     self.listBox.setR.setReadOnly(bool)
    # # ReadOnly = property(get_ReadOnly, set_ReadOnly, None, None)

    def set_LabelWidth(self, width):
        self.captionLabel.setMinimumSize(QSize(width, 0))
        self.captionLabel.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)

    def set_Width(self, width):
        self.listBox.setMinimumSize(QSize(width, 0))
        self.listBox.setMaximumSize(QSize(width, 16777215))
    Width = property(None, set_Width, None, None)

    def set_Button(self, imageName):
        if imageName == None or imageName == "":
            self.imageButton.setVisible(False)
            return
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/" + imageName)), QIcon.Normal, QIcon.Off)
        self.imageButton.setIcon(icon)
        self.imageButton.setVisible(True)
    Button = property(None, set_Button, None, None)

    def get_SelectedIndex(self):
        try:
            return self.listBox.currentRow()
        except:
            return 0
    def set_SelectedIndex(self, index):
        if self.listBox.count() == 0:
            return
        if index > self.listBox.count() - 1:
            self.listBox.setCurrentRow(0)
        else:
            self.listBox.setCurrentRow(index)
    SelectedIndex = property(get_SelectedIndex, set_SelectedIndex, None, None)

    # def get_Value(self):
    #     return self.listBox.currentIndex()
    # def set_Value(self, valueStr):
    #     if self.listBox.count() == 0:
    #         return
    #     self.listBox.setCurrentIndex(self.listBox.findText(valueStr))
    # Value = property(get_Value, set_Value, None, None)

    def get_Items(self):
        if self.hasObject:
            return self.objectList
        itemList = []
        if self.listBox.count() > 0:
            for i in range(self.listBox.count()):
                itemList.append(self.listBox.item(i).text())
        return itemList
    def set_AddItems(self, strList):
        if len(strList) != 0 and not isinstance(strList[0], str):
            for obj in strList:
                self.listBox.addItem(obj.ToString())
                self.objectList.append(obj)
            self.hasObject = True
            return
        self.listBox.addItems(strList)
    Items = property(get_Items, set_AddItems, None, None)

    def get_Enabled(self):
        return self.listBox.isEnabled()
    def set_Enabled(self, bool):
        self.listBox.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)

    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)

    def get_SelectedItem(self):
        if self.listBox.count() == 0:
            return None
        if self.hasObject:
            return self.objectList[self.SelectedIndex]
        return self.listBox.currentItem().text()
    # def set_SelectedItem(self, val):
    #     index = self.listBox.findText(val)
    #     self.listBox.setCurrentIndex(index)
    SelectedItem = property(get_SelectedItem, None, None, None)
