

from PyQt4.QtGui import QDialog, QPushButton, QVBoxLayout, QFont, QFileDialog, QMessageBox, QIcon
from PyQt4.QtCore import SIGNAL, QFileInfo, QDir
from FlightPlanner.Panels.ListBox import ListBox
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel

from ProjectManager.ProjectInfo import enumProjectType
from ProjectManager.ProjectInfo import ProjectInfo, ProjectList
from AircraftOperation import AirCraftOperation

class WorkspaceMngForm(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self)

        self.setObjectName(("ui_WorkspaceMngForm"))
        self.resize(200, 200)
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)

        self.vlForm = QVBoxLayout(self)
        self.vlForm.setObjectName(("vl_ProjectMngForm"))
        self.vlForm.setSpacing(9)
        self.vlForm.setMargin(9)

        self.basicFrame = Frame(self)
        self.vlForm.addWidget(self.basicFrame)

        self.frameName = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.frameName

        self.frame = Frame(self.frameName)
        self.frameName.Add = self.frame

        self.comboProjectWorkspace = ComboBoxPanel(self.frame)
        self.comboProjectWorkspace.Caption = "Project"
        self.comboProjectWorkspace.LabelWidth = 120
        self.frame.Add = self.comboProjectWorkspace

        self.comboSubProjectWorkspace = ComboBoxPanel(self.frame)
        self.comboSubProjectWorkspace.Caption = "Sub-Project"
        self.comboSubProjectWorkspace.LabelWidth = 120
        self.frame.Add = self.comboSubProjectWorkspace

        self.textNameWorkspace = TextBoxPanel(self.frame)
        self.textNameWorkspace.Caption = "Workspace Name"
        self.textNameWorkspace.LabelWidth = 120
        self.textNameWorkspace.Width = 120
        self.frame.Add = self.textNameWorkspace

        self.groubox = GroupBox(self.frameName)
        self.groubox.Caption = "Workspaces"
        self.frameName.Add = self.groubox

        self.listBoxWorkspace = ListBox(self.groubox)
        self.groubox.Add = self.listBoxWorkspace

        self.textPathWorkspace = TextBoxPanel(self.basicFrame)
        self.textPathWorkspace.Caption = "Workspace Path"
        self.textPathWorkspace.imageButton.setIcon(QIcon())
        self.textPathWorkspace.Button = "opens.png"
        self.textPathWorkspace.LabelWidth = 120
        self.textPathWorkspace.textBox.setMaximumWidth(10000)
        self.textPathWorkspace.textBox.setMinimumWidth(100)
        self.basicFrame.Add = self.textPathWorkspace

        self.btnFrame = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.btnFrame

        self.buttonAddWorkspace = QPushButton(self.btnFrame)
        self.buttonAddWorkspace.setObjectName("buttonAddWorkspace")
        self.buttonAddWorkspace.setText("Add")
        self.btnFrame.Add = self.buttonAddWorkspace

        self.buttonModifyWorkspace = QPushButton(self.btnFrame)
        self.buttonModifyWorkspace.setObjectName("buttonModifyWorkspace")
        self.buttonModifyWorkspace.setText("Modify")
        self.btnFrame.Add = self.buttonModifyWorkspace

        self.buttonDeleteWorkspace = QPushButton(self.btnFrame)
        self.buttonDeleteWorkspace.setObjectName("buttonDeleteWorkspace")
        self.buttonDeleteWorkspace.setText("Delete")
        self.btnFrame.Add = self.buttonDeleteWorkspace

        self.buttonSaveWorkspace = QPushButton(self.btnFrame)
        self.buttonSaveWorkspace.setObjectName("buttonSaveWorkspace")
        self.buttonSaveWorkspace.setText("Save")
        self.btnFrame.Add = self.buttonSaveWorkspace

        self.buttonCloseWorkspace = QPushButton(self.btnFrame)
        self.buttonCloseWorkspace.setObjectName("buttonCloseWorkspace")
        self.buttonCloseWorkspace.setText("Close")
        self.btnFrame.Add = self.buttonCloseWorkspace

        self.connect(self.listBoxWorkspace, SIGNAL("Event_0"), self.listBoxWorkspace_SelectedIndexChanged)
        self.connect(self.comboProjectWorkspace, SIGNAL("Event_0"), self.comboProjectWorkspace_SelectedIndexChanged)
        self.connect(self.textPathWorkspace, SIGNAL("Event_1"), self.buttonBrowseWorkspace_Click)

        self.buttonCloseWorkspace.clicked.connect(self.buttonCloseWorkspace_Click)
        self.buttonSaveWorkspace.clicked.connect(self.buttonSaveWorkspace_Click)
        self.buttonDeleteWorkspace.clicked.connect(self.buttonDeleteWorkspace_Click)
        self.buttonModifyWorkspace.clicked.connect(self.buttonModifyWorkspace_Click)
        self.buttonAddWorkspace.clicked.connect(self.buttonAddWorkspace_Click)

        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if (pi.Pt == enumProjectType.ptWorkspace):
                self.listBoxWorkspace.Add(pi.Name)
            elif (pi.Pt == enumProjectType.ptProject):
                self.comboProjectWorkspace.Add(pi.Name)
            elif (pi.Pt == enumProjectType.ptSubProject):
                self.comboSubProjectWorkspace.Add(pi.Name)
        self.comboProjectWorkspace_SelectedIndexChanged()

        
        
    def CheckInputValues(self):
        if (self.textNameWorkspace.Text == None or self.textNameWorkspace.Text == ""):
            QMessageBox.warning(self, "Warning", "Please input project name!")
            return
        if (self.textPathWorkspace.Text == None or self.textPathWorkspace.Text == ""):
            QMessageBox.warning(self, "Warning", "Please input project path!")
            return
        if (self.comboProjectWorkspace.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select an Project!")
            return
        if (self.comboSubProjectWorkspace.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select an Sub-Project!")
            return
        directory = QDir(self.textPathWorkspace.Text)
        if (not directory.exists()):
            if (QMessageBox.question(self, "Question", "Procedure path dose not exist! Do you create the directory?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes):
                directory.mkpath(self.textPathWorkspace.Text)
            else:
                return False
        return True


    # private void WorkspaceMngForm_Load(object sender, EventArgs e)
    # {
    #     try
    #     {
    #         foreach (ProjectInfo pi in AirCraftOperation.g_projectList.ProjectsList)
    #         {
    #             if (pi.Pt == enumProjectType.ptWorkspace)
    #             {
    #                 self.listBoxWorkspace.Items.Add(pi.Name)
    #             }
    #             else if (pi.Pt == enumProjectType.ptProject)
    #             {
    #                 self.comboProjectWorkspace.Items.Add(pi.Name)
    #             }
    #             else if (pi.Pt == enumProjectType.ptSubProject)
    #             {
    #                 self.comboSubProjectWorkspace.Items.Add(pi.Name)
    #             }
    #         }
    #     }
    #     catch (System.Exception ex)
    #     {
    #         MessageBox.Show(ex.Message)
    #     }
    # }

    def listBoxWorkspace_SelectedIndexChanged(self):
        if (self.listBoxWorkspace.SelectedIndex < 0):
            return
        pi = AirCraftOperation.g_projectList.Find(self.listBoxWorkspace.Items[self.listBoxWorkspace.SelectedIndex])
        self.textNameWorkspace.Text = AirCraftOperation.g_projectList.ProjectsList[pi].Name
        self.textPathWorkspace.Text = AirCraftOperation.g_projectList.ProjectsList[pi].Path
        self.comboProjectWorkspace.SelectedIndex = self.comboProjectWorkspace.IndexOf(AirCraftOperation.g_projectList.ProjectsList[pi].ProjName)
        self.comboSubProjectWorkspace.SelectedIndex = self.comboSubProjectWorkspace.IndexOf(AirCraftOperation.g_projectList.ProjectsList[pi].SubProjName)

    def buttonBrowseWorkspace_Click(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Open Project Path")
        if (folderPath != None and folderPath != ""):
            self.textPathWorkspace.Value = folderPath

    def buttonSaveWorkspace_Click(self):
        res = QMessageBox.question(self, "Question", "Save changes to project information?", QMessageBox.Yes | QMessageBox.No)
        if (res == QMessageBox.Yes):
            AirCraftOperation.g_projectList.WriteProjectInfoXml()
            self.buttonSaveWorkspace.setEnabled(False)

    def buttonCloseWorkspace_Click(self):
        # if (self.buttonSaveWorkspace.Enabled == True)
        # {
        #     DialogResult res = MessageBox.Show("Save changes to project information?", "Alert", MessageBoxButtons.YesNoCancel)
        #     if (res == DialogResult.Yes)
        #     {
        #         self.buttonSaveWorkspace_Click(sender, e)
        #     }
        #     else if (res == DialogResult.No)
        #     {
        #     }
        #     else if (res == DialogResult.Cancel)
        #     {
        #         self.DialogResult = DialogResult.None
        #         return
        self.accept()

    def buttonAddWorkspace_Click(self):
        if (not self.CheckInputValues()):
            return

        if (AirCraftOperation.g_projectList.Find(self.textNameWorkspace.Text) != None):
            QMessageBox.warning(self, "Warning", "The same name exist!")
            return
        pi = ProjectInfo()
        pi.Pt = enumProjectType.ptWorkspace
        pi.Name = self.textNameWorkspace.Text
        pi.Path = self.textPathWorkspace.Text
        pi.ProjName = self.comboProjectWorkspace.SelectedItem
        pi.SubProjName = self.comboSubProjectWorkspace.SelectedItem
        pi.UserName = AirCraftOperation.g_loginedUser.Name

        AirCraftOperation.g_projectList.Add(pi)

        nIndex = self.listBoxWorkspace.Add(pi.Name)
        self.listBoxWorkspace.SelectedIndex = nIndex
        self.buttonSaveWorkspace.setEnabled(True)

    def buttonModifyWorkspace_Click(self):
        if (self.listBoxWorkspace.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select project in the projects list!")
            return
        if (not self.CheckInputValues()):
            return

        index = AirCraftOperation.g_projectList.Find(self.listBoxWorkspace.Items[self.listBoxWorkspace.SelectedIndex])
        AirCraftOperation.g_projectList.ProjectsList[index].Pt = enumProjectType.ptWorkspace
        AirCraftOperation.g_projectList.ProjectsList[index].Name = self.textNameWorkspace.Text
        AirCraftOperation.g_projectList.ProjectsList[index].Path = self.textPathWorkspace.Text
        AirCraftOperation.g_projectList.ProjectsList[index].ProjName = self.comboProjectWorkspace.SelectedItem
        AirCraftOperation.g_projectList.ProjectsList[index].SubProjName = self.comboSubProjectWorkspace.SelectedItem
        AirCraftOperation.g_projectList.ProjectsList[index].UserName = AirCraftOperation.g_loginedUser.Name

        self.listBoxWorkspace.Clear()

        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if (pi.Pt == enumProjectType.ptWorkspace):
                self.listBoxWorkspace.Add(pi.Name)
            # elif (pi.Pt == enumProjectType.ptProject):
            #     self.comboProjectWorkspace.Add(pi.Name)
            # elif (pi.Pt == enumProjectType.ptSubProject):
            #     self.comboSubProjectWorkspace.Add(pi.Name)

        # AirCraftOperation.g_projectList.Remove(pi)

        # AirCraftOperation.g_projectList.Add(pi)
        self.buttonSaveWorkspace.setEnabled(True)

    def buttonDeleteWorkspace_Click(self):
        if (self.listBoxWorkspace.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select project in the projects list!")
            return

        if (QMessageBox.question(self, "Question", "Are you sure to delete " + self.listBoxWorkspace.Items[self.listBoxWorkspace.SelectedIndex] + "?",QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
            return
        AirCraftOperation.g_projectList.Remove(self.listBoxWorkspace.Items[self.listBoxWorkspace.SelectedIndex], enumProjectType.ptWorkspace)
        self.buttonSaveWorkspace.setEnabled(True)

        self.listBoxWorkspace.Clear()

        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if (pi.Pt == enumProjectType.ptWorkspace):
                self.listBoxWorkspace.Add(pi.Name)
            # elif (pi.Pt == enumProjectType.ptProject):
            #     self.comboProjectWorkspace.Add(pi.Name)
            # elif (pi.Pt == enumProjectType.ptSubProject):
            #     self.comboSubProjectWorkspace.Add(pi.Name)

    def comboProjectWorkspace_SelectedIndexChanged(self):
        listSubprojects = AirCraftOperation.g_projectList.GetLinkedProjects(self.comboProjectWorkspace.SelectedItem, enumProjectType.ptProject, enumProjectType.ptSubProject)
        if (listSubprojects != None and len(listSubprojects) > 0):
            self.comboSubProjectWorkspace.Clear()
            self.comboSubProjectWorkspace.Items = listSubprojects
            self.comboSubProjectWorkspace.SelectedIndex = 0