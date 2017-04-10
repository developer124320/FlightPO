# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QWidget, QFrame, QSpacerItem, QComboBox, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QToolButton, QIcon, QPixmap, QDialog
from PyQt4.QtCore import QSize, QString, SIGNAL
from FlightPlanner.Panels.Frame import Frame
class ComboBoxPanel(QWidget):
    def __init__(self, parent, editable = False, spacerItemMove = False):
        QWidget.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("ComboBoxPanel" + str(len(parent.findChildren(ComboBoxPanel))))


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

        self.comboBox = QComboBox(self.frameBoxPanel)
        self.comboBox.setEnabled(True)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName(self.objectName() + "_comboBox")
        self.comboBox.setMinimumWidth(70)
        # self.comboBox.setMaximumWidth(70)


        # self.hLayoutframeBoxPanel.addWidget(self.lineEdit)
        self.hLayoutframeBoxPanel.addWidget(self.comboBox)

        self.imageButton = QToolButton(self.frameBoxPanel)
        self.imageButton.setText((""))
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/convex_hull.png")), QIcon.Normal, QIcon.Off)
        self.imageButton.setIcon(icon)
        self.imageButton.setObjectName(("imageButton"))
        self.imageButton.setVisible(False)
        self.hLayoutframeBoxPanel.addWidget(self.imageButton)

        self.hLayoutBoxPanel.addWidget(self.frameBoxPanel)
        if not spacerItemMove:
            spacerItem = QSpacerItem(10,10,QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.hLayoutBoxPanel.addItem(spacerItem)

        self.comboBox.currentIndexChanged.connect(self.comboBoxChanged)
        # self.comboBox.editTextChanged.connect(self.comboBoxEditTextChanged)
        self.imageButton.clicked.connect(self.imageButtonClicked)

        

        self.captionUnits = ""

        self.hasObject = False

        self.objectList = []
        if editable == True:
            self.lineEdit = QLineEdit(self.frameBoxPanel)
            self.lineEdit.setObjectName("lineEdit")
            self.hLayoutframeBoxPanel.insertWidget(1, self.lineEdit)
            self.comboBox.setLineEdit(self.lineEdit)
            self.lineEdit.returnPressed.connect(self.comboBoxEditTextChanged)
    def FindString(self, string):
        return self.comboBox.findText(string)
    def comboBoxEditTextChanged(self):
        self.comboBox.showPopup()
    def get_Count(self):
        return self.comboBox.count()
    Count = property(get_Count, None, None, None)

    def method_0(self):
        return self.comboBox.currentIndex() >= 0 and self.SelectedItem != None and self.SelectedItem != ""

    def method_3(self, string_0):
        return self.comboBox.findText(string_0);

    def method_11(self, string_0):
        if (self.IsEmpty):
            return "%s%s\t"%(string_0, self.Caption);
        return "%s%s\t%s %s"%(string_0, self.Caption, self.Value, self.CaptionUnits);

    def comboBoxChanged(self):
        self.emit(SIGNAL("Event_0"), self)
    def IndexOf(self, item):
        if isinstance(item, str) or isinstance(item, QString):
            return self.comboBox.findText(item)
        else:
            return self.comboBox.findText(item.ToString())

    def Contains(self, item):
        compStr = None
        if isinstance(item, str):
            compStr = item
        elif isinstance(item, float) or isinstance(item, int):
            compStr = str(item)
        else:
            compStr = item.ToString()
        for i in range(self.comboBox.count()):
            comboItemstr = self.comboBox.itemText(i)
            if compStr == comboItemstr:
                return True
        return False


    def Clear(self):
        self.comboBox.clear()
        self.objectList = []
        self.hasObject = False
    def Add(self, item):
        if not isinstance(item, str) and not isinstance(item, QString):
            self.comboBox.addItem(item.ToString())
            self.objectList.append(item)
            self.hasObject = True
            return
        self.comboBox.addItem(item)
        self.hasObject = False
    def Insert(self, index, item):
        if not isinstance(item, str) and not isinstance(item, QString):
            self.comboBox.insertItem(index, item.ToString())
            self.objectList.insert(index, item)
            self.hasObject = True
            return
        self.comboBox.insertItem(index, item)
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
            self.captionLabel.setText(captionStr + "(" + QString(self.CaptionUnits) + ")" + ":")
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
    #     return self.comboBox.currentIndex()

    # def set_Value(self, value):
    #     try:
    #         self.comboBox.setCurrentIndex(value)
    #     except:
    #         self.textBox.setText("")
    # Value = property(get_Value, set_Value, None, None)

    def get_IsEmpty(self):
        return self.comboBox.currentText() == "" or self.comboBox.currentIndex() == -1
    IsEmpty = property(get_IsEmpty, None, None, None)

    def get_ReadOnly(self):
        return self.textBox.isReadOnly()
    # def set_ReadOnly(self, bool):
    #     self.comboBox.setR.setReadOnly(bool)
    # ReadOnly = property(get_ReadOnly, set_ReadOnly, None, None)

    def set_LabelWidth(self, width):
        self.captionLabel.setMinimumSize(QSize(width, 0))
        self.captionLabel.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)

    def set_Width(self, width):
        self.comboBox.setMinimumSize(QSize(width, 0))
        self.comboBox.setMaximumSize(QSize(width, 16777215))
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
        return self.comboBox.currentIndex()
    def set_SelectedIndex(self, index):
        if self.comboBox.count() == 0:
            return
        if index > self.comboBox.count() - 1:
            self.comboBox.setCurrentIndex(0)
        else:
            self.comboBox.setCurrentIndex(index)
    SelectedIndex = property(get_SelectedIndex, set_SelectedIndex, None, None)

    def get_Value(self):
        return self.comboBox.currentIndex()
    def set_Value(self, valueStr):
        if self.comboBox.count() == 0:
            return
        if valueStr == None:
            self.SelectedIndex = -1
            return
        self.comboBox.setCurrentIndex(self.comboBox.findText(str(valueStr)))
    Value = property(get_Value, set_Value, None, None)

    def get_Items(self):
        # if self.hasObject:
        #     return self.objectList
        itemList = []
        if self.comboBox.count() > 0:
            for i in range(self.comboBox.count()):
                itemList.append(self.comboBox.itemText(i))
        return itemList
    def set_AddItems(self, strList):
        self.Clear()
        if len(strList) != 0 and (not isinstance(strList[0], str) and not isinstance(strList[0], QString)):
            for obj in strList:
                self.comboBox.addItem(obj.ToString())
                self.objectList.append(obj)
            self.hasObject = True
            return
        self.comboBox.addItems(strList)
    Items = property(get_Items, set_AddItems, None, None)

    def get_Enabled(self):
        return self.comboBox.isEnabled()
    def set_Enabled(self, bool):
        self.comboBox.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)

    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)
    
    def get_Editable(self):
        return self.comboBox.isEditable()
    def set_Editable(self, bool):
        self.comboBox.setEditable(bool)
    Editable = property(get_Editable, set_Editable, None, None)

    def get_SelectedItem(self):
        if self.comboBox.count() == 0:
            return None
        if self.hasObject:
            return self.objectList[self.SelectedIndex]
        return self.comboBox.currentText()
    def set_SelectedItem(self, val):
        index = self.comboBox.findText(val)
        self.comboBox.setCurrentIndex(index)
    SelectedItem = property(get_SelectedItem, set_SelectedItem, None, None)
