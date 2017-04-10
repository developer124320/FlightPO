# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QTreeView, QWidget, QHBoxLayout, QSizePolicy, QDialog, QIcon, QStandardItem, QStandardItemModel
from PyQt4.QtCore import SIGNAL, QSize, QString, Qt

from FlightPlanner.Panels.Frame import Frame

class TreeView(QTreeView):
    def __init__(self, parent):
        QTreeView.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("TreeView" + str(len(parent.findChildren(TreeView))))

        # self.setObjectName("TreeViewWidget")
        # self.hLayout = QHBoxLayout(self)
        # self.hLayout.setObjectName("hLayout")
        # 
        # sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        # self.setSizePolicy(sizePolicy)
        # 
        # # self.frame = Frame()
        # self = QTreeView(self)
        # self.hLayout.addWidget(self)

        self.stdModel = QStandardItemModel()
        self.setModel(self.stdModel)

        self.hasObject = False
        self.treeNodeList = []

        self.checkBoxList = []
        self.setHeaderHidden(True)
        # self.stdModel.appendRow(TreeNode("P"))
        # rootIndex = self.rootIndex()

        # rootItem = self.stdModel.itemFromIndex(rootIndex)
        # rootItem.setText("Root")

    def mouseMoveEvent(self, mouseEvent):
        pt = mouseEvent.pos()
        pass
    def Clear(self):
        self.stdModel.clear()
        self.hasObject = False
        self.treeNodeList = []
    def Add(self, caption):
        item = TreeNode(caption)
        if len(self.treeNodeList) > 0:
            item.PrevNode = self.treeNodeList[len(self.treeNodeList) - 1]
            item.PrevNode.NextNode = item
            item.Index = len(self.treeNodeList)
        # item.nodeIndex = len(self.treeNodeList)
        self.treeNodeList.append(item)
        self.stdModel.appendRow(item)
        return item
    def RemoveNode(self, i):
        self.stdModel.removeRow(i)
        self.treeNodeList.pop(i)
        for j in range(i, len(self.treeNodeList)):
            self.treeNodeList[j].nodeIndex -= 1
    def Remove(self, item):
        removedIndex = self.treeNodeList.index(item)
        if removedIndex == 0:
            self.treeNodeList[1].PrevNode = None
        elif removedIndex == len(self.treeNodeList) - 1:
            self.treeNodeList[len(self.treeNodeList) - 2].NextNode = None
        else:
            self.treeNodeList[removedIndex + 1].PrevNode = self.treeNodeList[removedIndex - 1]
            self.treeNodeList[removedIndex - 1].NextNode = self.treeNodeList[removedIndex + 1]
        self.treeNodeList.pop(removedIndex)
        self.stdModel.removeRow(removedIndex)
        i = 0
        for node in self.treeNodeList:
            node.Index = i
            node.LastNode = self.treeNodeList[len(self.treeNodeList) - 1]
            i += 1
    def Insert(self, index, text):
        if index == 0 and len(self.treeNodeList) == 0:
            self.Add(text)
            return
        node = TreeNode(text)
        node.Parent = self
        self.treeNodeList.insert(index, node)
        i = 0
        for node0 in self.treeNodeList:
            node0.Index = i
            i += 1
        if index == 0:
            self.treeNodeList[index].PrevNode = None
            if len(self.treeNodeList) == 1:
                self.treeNodeList[index].NextNode = None
                self.treeNodeList[index].LastNode = self.treeNodeList[index]
            else:
                self.treeNodeList[index].NextNode = self.treeNodeList[index + 1]
                self.treeNodeList[index].LastNode = self.treeNodeList[len(self.treeNodeList) - 1]
            
            self.treeNodeList[index + 1].PrevNode = self.treeNodeList[index]
            
        else:
            self.treeNodeList[index].PrevNode = self.treeNodeList[index - 1]
            self.treeNodeList[index].NextNode = self.treeNodeList[index + 1]
            self.treeNodeList[index].LastNode = self.treeNodeList[len(self.treeNodeList) - 1]
            
            self.treeNodeList[index + 1].PrevNode = self.treeNodeList[index]
            self.treeNodeList[index - 1].NextNode = self.treeNodeList[index]
            

        self.stdModel.insertRow(index, node)
        return node

    def get_Items(self):
        return self.treeNodeList
    Nodes = property(get_Items, None, None, None)

    def Node(self, index):
        if not self.stdModel.rowCount() > 0:
            return None
        return self.treeNodeList[index]

    def getSelectedNode(self):
        if not self.stdModel.rowCount() > 0:
            return None
        index = self.currentIndex()
        return self.stdModel.itemFromIndex(index)
    def setSelectedNode(self, node):
        if not self.stdModel.rowCount() > 0:
            return
        # self.s
        index = self.stdModel.indexFromItem(node)
        self.setCurrentIndex(index)
        # self.treeNodeList.pop(index)
        # self.treeNodeList.insert(index, node)
        # self.stdModel.setItem(index, node)

    SelectedNode = property(getSelectedNode, setSelectedNode, None, None)




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

class TreeNode(QStandardItem):
    def __init__(self, string_0 = None):
        QStandardItem.__init__(self)
        self.Tag = None
        self.childNodeList = []
        self.Index = 0
        self.ParentLevel = 0
        self.imageKey = None
        self.PrevNode = None
        self.NextNode = None
        self.LastNode = None
        self.Parent = None
        if string_0 != None:
            if isinstance(string_0, str) or isinstance(string_0, QString):
                self.setText(string_0)
            else:
                self.setText(string_0.ToString())
                self.Tag = string_0
    def Add(self, text):
        node = TreeNode(text)
        if isinstance(node, TreeNode):
            node.Parent = self
            node.ParentLevel = node.Parent.ParentLevel + 1
            node.Index = len(self.childNodeList)
            if len(self.childNodeList) == 0:
                node.PrevNode = None
            else:
                node.PrevNode = self.childNodeList[len(self.childNodeList) - 1]
                node.PrevNode.NextNode = node
            self.childNodeList.append(node)
            for node0 in self.childNodeList:
                node0.LastNode = node
            self.appendRow(node)
            return self.childNodeList[len(self.childNodeList) - 1]
        else:
            raise SyntaxError

    def Insert(self, index, text):
        if index == 0 and len(self.childNodeList) == 0:
            self.Add(text)
            return
        node = TreeNode(text)
        node.Parent = self
        self.childNodeList.insert(index, node)
        i = 0
        for node0 in self.childNodeList:
            node0.Index = i
            i += 1
        if index == 0:
            self.childNodeList[index].PrevNode = None
            if len(self.childNodeList) == 1:
                self.childNodeList[index].NextNode = None
                self.childNodeList[index].LastNode = self.childNodeList[index]
            else:
                self.childNodeList[index].NextNode = self.childNodeList[index + 1]
                self.childNodeList[index].LastNode = self.childNodeList[len(self.childNodeList) - 1]
            
            self.childNodeList[index + 1].PrevNode = self.childNodeList[index]
            
        else:
            self.childNodeList[index].PrevNode = self.childNodeList[index - 1]
            self.childNodeList[index].NextNode = self.childNodeList[index + 1]
            self.childNodeList[index].LastNode = self.childNodeList[len(self.childNodeList) - 1]
            
            self.childNodeList[index + 1].PrevNode = self.childNodeList[index]
            self.childNodeList[index - 1].NextNode = self.childNodeList[index]
            

        self.insertRow(index, node)
        return self.childNodeList[index]

    def Remove(self, item):
        removedIndex = self.childNodeList.index(item)
        if removedIndex == 0:
            self.childNodeList[1].PrevNode = None
        elif removedIndex == len(self.childNodeList) - 1:
            self.childNodeList[len(self.childNodeList) - 2].NextNode = None
        else:
            self.childNodeList[removedIndex + 1].PrevNode = self.childNodeList[removedIndex - 1]
            self.childNodeList[removedIndex - 1].NextNode = self.childNodeList[removedIndex + 1]
        self.childNodeList.pop(removedIndex)
        i = 0
        for node in self.childNodeList:
            node.Index = i
            node.LastNode = self.childNodeList[len(self.childNodeList) - 1]
            i += 1

    # def getLastNode(self):
    #     if len(self.childNodeList) == 0:
    #         return self
    #     return self.childNodeList[len(self.childNodeList) - 1]
    # LastNode = property(getLastNode, None, None, None)
    #
    # def getNextNode(self):
    #     if self.Parent == None:
    #         return self
    #     return self.childNodeList[self.Index + 1]
    # NextNode = property(getLastNode, None, None, None)

    def get_Text(self):
        return self.text()
    def set_Text(self, val):
        self.setText(val)
    Text = property(get_Text, set_Text, None, None)

    def getImageKey(self):
        return self.imageKey
    def setImageKey(self, val):
        self.imageKey = val
        self.setIcon(QIcon("Resource/btnImage/" + val));
    ImageKey = property(getImageKey, setImageKey, None, None)

    def getNodes(self):
        return self.childNodeList
    Nodes = property(getNodes, None, None, None)

    # def getParent(self):
    #     return self.parentTree
    # def setParent(self, p):
    #     self.parentTree = p
    # Parent = property(getParent, setParent, None, None)

    def getNodeFont(self):
        return self.font()
    def setNodeFont(self, font):
        self.setFont(font)
    NodeFont = property(getNodeFont, setNodeFont, None, None)
    
    def RemoveChild(self, i):        
        self.removeRow(i)
        self.childNodeList.pop(i)
        for j in range(i, len(self.childNodeList)):
            self.childNodeList[j].nodeIndex -= 1

