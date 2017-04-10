# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QDialogButtonBox, QTreeView,\
    QStandardItem, QStandardItemModel, QPushButton, QIcon, QPixmap, QFont
from PyQt4.QtCore import SIGNAL, QString
from FlightPlanner.Panels.CheckedListBox import CheckedListBox
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.PositionPanel import PositionPanel, Point3D
from FlightPlanner.Panels.TreeView import TreeNode, TreeView
from Type.Position import Position, PositionType
from Type.Runway import RunwayList, Runway



class DlgRunway(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(290, 136)
        self.setWindowTitle("Runway Setup")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"))

        self.basicFrame = Frame(self)
        verticalLayoutDlg.addWidget(self.basicFrame)

        self.groupBox = GroupBox(self.basicFrame)
        self.basicFrame.Add = self.groupBox

        self.pnlName = TextBoxPanel(self.groupBox)
        self.pnlName.Caption = "Name"
        self.pnlName.LabelWidth = 70
        self.groupBox.Add = self.pnlName

        self.pnlDesignatorFrame = Frame(self.groupBox, "HL")
        self.groupBox.Add = self.pnlDesignatorFrame

        self.pnlDesignator = TextBoxPanel(self.groupBox)
        self.pnlDesignator.Caption = "Designator"
        self.pnlDesignator.LabelWidth = 70
        self.pnlDesignator.Button = "Calculator.bmp"
        self.pnlDesignatorFrame.Add = self.pnlDesignator

        self.cmbDesignator = ComboBoxPanel(self.groupBox)
        self.cmbDesignator.Caption = ""
        self.cmbDesignator.LabelWidth = 0
        self.cmbDesignator.Items = ["", "L", "C", "R"]
        self.pnlDesignatorFrame.Add = self.cmbDesignator

        self.gbPositions = GroupBox(self.groupBox)
        self.gbPositions.Caption = "Positions"
        self.groupBox.Add = self.gbPositions

        self.pnlPosition = PositionPanel(self.gbPositions)
        # self.pnlPosition.hideframe_Altitude()
        self.pnlPosition.btnCalculater.setVisible(False)
        self.gbPositions.Add = self.pnlPosition

        self.pnlTree = Frame(self.gbPositions)
        self.gbPositions.Add = self.pnlTree

        self.trvPositions = TreeView(self.pnlTree)
        self.pnlTree.Add = self.trvPositions

        self.pnlButtons = Frame(self.pnlTree, "HL")
        self.pnlTree.Add = self.pnlButtons

        self.btnPrevious = QPushButton(self.pnlButtons)
        self.btnPrevious.setObjectName("btnPrevious")
        self.btnPrevious.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/btnImage/Prev_32x32.png"), QIcon.Normal, QIcon.Off)
        self.btnPrevious.setIcon(icon)
        self.pnlButtons.Add = self.btnPrevious

        self.btnInsert = QPushButton(self.pnlButtons)
        self.btnInsert.setObjectName("btnInsert")
        self.btnInsert.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/add.png"), QIcon.Normal, QIcon.Off)
        self.btnInsert.setIcon(icon)
        self.pnlButtons.Add = self.btnInsert

        self.btnRemove = QPushButton(self.pnlButtons)
        self.btnRemove.setObjectName("btnRemove")
        self.btnRemove.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/remove.png"), QIcon.Normal, QIcon.Off)
        self.btnRemove.setIcon(icon)
        self.pnlButtons.Add = self.btnRemove

        self.btnNext = QPushButton(self.pnlButtons)
        self.btnNext.setObjectName("btnNext")
        self.btnNext.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/btnImage/Next_32x32.png"), QIcon.Normal, QIcon.Off)
        self.btnNext.setIcon(icon)
        self.pnlButtons.Add = self.btnNext



        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"))
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.btnOK = self.btnBoxOkCancel.button(QDialogButtonBox.Ok)

        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)

        self.btnOK.setText("Save")
        self.connect(self.pnlDesignator, SIGNAL("Event_1"), self.method_14)

        self.connect(self.pnlPosition, SIGNAL("captureFinished"), self.method_13)
        self.btnInsert.clicked.connect(self.btnInsert_Click)
        self.btnNext.clicked.connect(self.btnNext_Click)
        self.btnPrevious.clicked.connect(self.btnPrevious_Click)
        self.btnRemove.clicked.connect(self.btnRemove_Click)

        self.trvPositions.clicked.connect(self.trvPositions_clicked)

        # item = self.trvPositions.Add("Parent")
        # item.appendRow(TreeNode("Child0"))
        #
        # item00 = item0.appendRow(TreeNode("Child00"))

    def trvPositions_clicked(self):
        selectedNode = self.trvPositions.SelectedNode
        if (selectedNode == None):
            return
        tag = selectedNode.Tag
        if (tag == None):
            return
        if not tag.IsEmpty and tag.IsValid:
            self.pnlPosition.Point3d = tag.Point3d
        else:
            self.pnlPosition.Point3d = None
    def get_Runway(self):
        return self.method_6()
    def set_Runway(self, runway):
        if (runway != None):
            self.pnlName.Value = runway.Name
            self.pnlDesignator.Value = runway.DesignatorHeading
            self.cmbDesignator.SelectedIndex = self.cmbDesignator.comboBox.findText((runway.DesignatorCode))
        self.method_5(runway)
    RunwayValue = property(get_Runway, set_Runway, None, None)


    def acceptDlg(self):
        current = None
        # self.errorProvider.method_1()
        # self.pnlName.method_0()
        for current in self.trvPositions.Nodes:
        # IEnumerator enumerator = self.trvPositions.Nodes.GetEnumerator()
        # try
        # {
        #     while (true)
        #     {
        #         if (enumerator.MoveNext())
        #         {
        #     current = (TreeNode)enumerator.Current
            tag = current.Tag
            if (not tag.IsValidIncludingAltitude):
                if (tag.Type == PositionType.THR):
                    break
                if (tag.Type == PositionType.END):
                    break
                elif (not tag.IsEmpty):
                    self.trvPositions.SelectedNode = current
                    self.emit(SIGNAL("DlgRunway_accept"), self.method_6())
                    # self.pnlPosition.method_6()
                    return
            for treeNode in current.Nodes:
            # IEnumerator enumerator1 = current.Nodes.GetEnumerator()
            # try
            # {
            #     while (enumerator1.MoveNext())
            #     {
            #         TreeNode treeNode = (TreeNode)enumerator1.Current
                position = current.Tag
                if (position.IsValidIncludingAltitude or position.IsEmpty):
                    continue
                self.trvPositions.SelectedNode = treeNode
                self.pnlPosition.method_6()
                self.emit(SIGNAL("DlgRunway_accept"), self.method_6())
                return
            #     }
            # }
            # finally
            # {
            #     IDisposable disposable = enumerator1 as IDisposable
            #     if (disposable != null)
            #     {
            #         disposable.Dispose()
            #     }
            # }
            #     }
            #     else
            #     {
            #         goto Label0
            #     }
            # }
        self.trvPositions.SelectedNode = current
        # self.pnlPosition.method_6()
        self.emit(SIGNAL("DlgRunway_accept"), self.method_6())
        # }
        # finally
        # {
        #     IDisposable disposable1 = enumerator as IDisposable
        #     if (disposable1 != null)
        #     {
        #         disposable1.Dispose()
        #     }
        # }
        # return
    # Label0:
    #     if (!self.errorProvider.HasErrors)
    #     {
    #         if (self.method_6().method_7(self))
    #         {
    #             base.DialogResult = System.Windows.Forms.DialogResult.OK
    #         }
    #         return
    #     }
    #     else
    #     {
    #         return
    #     }
        self.accept()
    
    def btnInsert_Click(self):
        selectedNode = self.trvPositions.SelectedNode
        if (selectedNode == None):
            return
        tag = selectedNode.Tag
        if (tag == None):
            return
        if (tag.Type == PositionType.THR):
            selectedNode = selectedNode.Insert(0, PositionType.VariableNames[PositionType.Position - 1])
            selectedNode.Tag = Position(PositionType.Position)
        elif (tag.Type != PositionType.END):
            if (tag.Type != PositionType.Position):
                return
            if selectedNode.Parent == None:
                selectedNode = self.trvPositions.Insert(selectedNode.Index, PositionType.VariableNames[PositionType.Position - 1])
            else:
                selectedNode = selectedNode.Parent.Insert(selectedNode.Index, PositionType.VariableNames[PositionType.Position - 1])
            selectedNode.Tag = Position(PositionType.Position)
        else:
            selectedNode = selectedNode.PrevNode.Add(PositionType.VariableNames[PositionType.Position - 1])
            selectedNode.Tag = Position(PositionType.Position)
        self.trvPositions.SelectedNode = selectedNode
    
    def btnNext_Click(self):
        selectedNode = self.trvPositions.SelectedNode
        if (selectedNode == None):
            return
        if (selectedNode.Parent != None):
            if (selectedNode.NextNode == None):
                self.trvPositions.SelectedNode = selectedNode.Parent.NextNode
                return
            self.trvPositions.SelectedNode = selectedNode.NextNode
        else:
            if (len(selectedNode.Nodes) > 0):
                self.trvPositions.SelectedNode = selectedNode.Nodes[0]
                return
            if (selectedNode.NextNode != None):
                self.trvPositions.SelectedNode = selectedNode.NextNode
                return

    def btnPrevious_Click(self):
        selectedNode = self.trvPositions.SelectedNode
        if (selectedNode == None):
            return
        if (selectedNode.Parent != None):
            if (selectedNode.Index == 0):
                self.trvPositions.SelectedNode = selectedNode.Parent
                return
            self.trvPositions.SelectedNode = selectedNode.PrevNode
        else:
            selectedNode = selectedNode.PrevNode
            if (selectedNode != None):
                if (len(selectedNode.Nodes) <= 0):
                    self.trvPositions.SelectedNode = selectedNode
                    return
                self.trvPositions.SelectedNode = selectedNode.LastNode
                return

    def btnRemove_Click(self):
        selectedNode = self.trvPositions.SelectedNode
        if (selectedNode == None):
            return
        if (selectedNode.Parent != None):
            if (selectedNode.NextNode != None):
                self.trvPositions.SelectedNode = selectedNode.NextNode
            elif (selectedNode.Parent.NextNode != None):
                self.trvPositions.SelectedNode = selectedNode.Parent.NextNode
            else:
                self.trvPositions.SelectedNode = selectedNode.Parent
            parentNode = selectedNode.Parent
            if parentNode == None:
                self.trvPositions.Remove(selectedNode)
            else:
                parentNode.Remove(selectedNode)
        else:
            self.trvPositions.Remove(selectedNode)
    
    def method_5(self, runway_0):
        self.trvPositions.treeNodeList = []
        if (runway_0 != None):
            position = runway_0.method_1(PositionType.START)
            self.trvPositions.Add(PositionType.VariableNames[position.Type - 1]).Tag = position
            position = runway_0.method_1(PositionType.THR)
            self.trvPositions.Add(PositionType.VariableNames[position.Type - 1]).Tag = position
            position = runway_0.method_1(PositionType.END)
            self.trvPositions.Add(PositionType.VariableNames[position.Type - 1]).Tag = position
            position = runway_0.method_1(PositionType.SWY)
            self.trvPositions.Add(PositionType.VariableNames[position.Type - 1]).Tag = position
            position = runway_0.method_1(PositionType.CWY)
            self.trvPositions.Add(PositionType.VariableNames[position.Type - 1]).Tag = position
            item = self.trvPositions.Nodes[1]
            for position0 in runway_0:
                if (position0.Type != PositionType.Position):
                    continue
                item.Add(PositionType.VariableNames[position0.Type - 1]).Tag = position0
            # item.Expand()
        else:
            self.trvPositions.Add("START").Tag = Position(PositionType.START)
            self.trvPositions.Add("THR").Tag = Position(PositionType.THR)
            self.trvPositions.Add("END").Tag = Position(PositionType.END)
            self.trvPositions.Add("SWY").Tag = Position(PositionType.SWY)
            self.trvPositions.Add("CWY").Tag = Position(PositionType.CWY)
        self.trvPositions.SelectedNode = self.trvPositions.Nodes[0]
        self.method_10()
    
    def method_6(self):
        runway = Runway()
        runway.Name = self.pnlName.Value
        runway.DesignatorHeading = self.pnlDesignator.Value
        if (self.cmbDesignator.SelectedIndex > 0):
            runway.DesignatorCode = self.cmbDesignator.SelectedItem#.ToString()
        for node in self.trvPositions.Nodes:
            tag = node.Tag
            runway[node.Index] = tag
            if (tag.Type != PositionType.THR):
                continue
            for treeNode in node.Nodes:
                position = treeNode.Tag
                if position == None:
                    continue
                if (not position.IsValidIncludingAltitude):
                    continue
                runway.Add(position)
        return runway
    
    def method_7(self):
        selectedNode = self.trvPositions.SelectedNode
        flag = False
        if (selectedNode != None):
            flag = True if(selectedNode.PrevNode != None) else selectedNode.Parent != None
        self.btnPrevious.setEnabled(flag)
        nextNode = False
        if (selectedNode != None):
            if (selectedNode.NextNode != None):
                nextNode = True
            elif (selectedNode.Parent != None):
                nextNode = selectedNode.Parent.NextNode != None
        self.btnNext.setEnabled(nextNode)
        flag1 = False
        if (selectedNode != None):
            tag = selectedNode.Tag
            if (tag != None):
                flag1 = True if(tag.Type == PositionType.THR or tag.Type == PositionType.Position) else tag.Type == PositionType.END
        self.btnInsert.setEnabled(flag1)
        type = False
        if (selectedNode != None):
            position = selectedNode.Tag
            if (position != None):
                type = position.Type == PositionType.Position
        self.btnRemove.setEnabled(type)
    
    def method_8(self, treeNode_0, bool_0):
        if (treeNode_0 != None):
            text = treeNode_0.Text
            treeNode_0.Text = " "
            if (not bool_0):
                treeNode_0.NodeFont = QFont()
            else:
                font = QFont()
                font.setBold(True)
                treeNode_0.NodeFont = font
            treeNode_0.Text = text
    
    def method_9(self, treeNode_0):
        position = treeNode_0.Tag
        if not isinstance(position, Position):
            return
        num = 0
        if (not position.IsValidIncludingAltitude):
            if (position.Type != PositionType.THR):
                if (position.Type == PositionType.END):
                    num = 2
                else:
                    if (not position.IsEmpty):
                        num = 2
                        # treeNode_0.ImageIndex = num
                        # treeNode_0.SelectedImageIndex = num
                        for node in treeNode_0.Nodes:
                            self.method_9(node)
                        return
                    else:
                        # treeNode_0.ImageIndex = num
                        # treeNode_0.SelectedImageIndex = num
                        for treeNode in treeNode_0.Nodes:
                            self.method_9(treeNode)
                        return
            num = 2
        else:
            num = 1
        # treeNode_0.ImageIndex = num
        # treeNode_0.SelectedImageIndex = num
        for node1 in treeNode_0.Nodes:
            self.method_9(node1)
    
    def method_10(self):
        for node in self.trvPositions.Nodes:
            self.method_9(node)
    
    def method_11(self):
        point3d_0 = Point3D.get_Origin()
        selectedNode = self.trvPositions.SelectedNode
        if (selectedNode != None):
            selectedNode = selectedNode.PrevNode
            if (selectedNode != None):
                if (len(selectedNode.Nodes) > 0):
                    selectedNode = selectedNode.LastNode
                point3d_0 = selectedNode.Tag.Point3d
                return True, point3d_0
        return False, None

    def method_12(self):
        # Point3d point3d
        # Point3d point3d1
        # if (AcadHelper.Ready)
        # {
        #     AcadHelper.smethod_27(DrawingSpace.ModelSpace, true)
        #     Position tag = self.trvPositions.SelectedNode.Tag as Position
        #     string rUNWAYPOSITION = Captions.RUNWAY_POSITION
        #     if (tag.Type != PositionType.Position)
        #     {
        #         rUNWAYPOSITION = string.Format(Captions.RUNWAY_X_POSITION, EnumHelper.smethod_0(tag.Type))
        #     }
        #     if (self.method_11(out point3d1))
        #     {
        #         if (!AcadHelper.smethod_82(this, rUNWAYPOSITION, point3d1, out point3d))
        #         {
        #             return
        #         }
        #     }
        #     else if (!AcadHelper.smethod_80(this, rUNWAYPOSITION, out point3d))
        #     {
        #         return
        #     }
        #     self.pnlPosition.Point3d = point3d
        self.method_13()
    def method_13(self):
        if self.trvPositions.SelectedNode == None:
            return
        self.pnlPosition.posType = self.trvPositions.SelectedNode.Tag.Type
        self.trvPositions.SelectedNode.Tag = self.pnlPosition.PositionValue
        self.method_10()

    def method_14(self):
        runway = self.method_6()
        self.pnlDesignator.Value = runway.method_0()
    
    @staticmethod
    def smethod_0(iwin32Window_0, runway_0):
        flag = False
        dlgRunway = DlgRunway(iwin32Window_0)
        dlgRunway.RunwayValue = runway_0
        dlgRunway.show()
        # if (dlgRunway.method_2(iwin32Window_0) != System.Windows.Forms.DialogResult.OK)
        # {
        #     flag = false
        # }
        # else
        # {
        #     runway_0 = dlgRunway.Runway
        #     flag = true
        # }
        # }
        return dlgRunway

