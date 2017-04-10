

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

class ProcedureMngForm(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self)

        self.setObjectName(("ui_ProcedureMngForm"))
        self.resize(200, 200)
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)

        self.vlForm = QVBoxLayout(self)
        self.vlForm.setObjectName(("vl_ProceduretMngForm"))
        self.vlForm.setSpacing(9)
        self.vlForm.setMargin(9)

        self.basicFrame = Frame(self)
        self.vlForm.addWidget(self.basicFrame)

        self.frameName = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.frameName

        self.frame = Frame(self.frameName)
        self.frameName.Add = self.frame

        self.comboProjectProcedure = ComboBoxPanel(self.frame)
        self.comboProjectProcedure.Caption = "Project"
        self.comboProjectProcedure.LabelWidth = 120
        self.frame.Add = self.comboProjectProcedure

        self.comboSubProjectProcedure = ComboBoxPanel(self.frame)
        self.comboSubProjectProcedure.Caption = "Sub-Project"
        self.comboSubProjectProcedure.LabelWidth = 120
        self.frame.Add = self.comboSubProjectProcedure

        self.comboWorkspaceProcedure = ComboBoxPanel(self.frame)
        self.comboWorkspaceProcedure.Caption = "Workspace"
        self.comboWorkspaceProcedure.LabelWidth = 120
        self.frame.Add = self.comboWorkspaceProcedure

        self.textNameProcedure = TextBoxPanel(self.frame)
        self.textNameProcedure.Caption = "Procedure Name"
        self.textNameProcedure.LabelWidth = 120
        self.textNameProcedure.Width = 120
        self.frame.Add = self.textNameProcedure

        self.groubox = GroupBox(self.frameName)
        self.groubox.Caption = "Procedures"
        self.frameName.Add = self.groubox

        self.listBoxProcedure = ListBox(self.groubox)
        self.groubox.Add = self.listBoxProcedure

        self.textPathProcedure = TextBoxPanel(self.basicFrame)
        self.textPathProcedure.Caption = "Procedure Path"
        self.textPathProcedure.imageButton.setIcon(QIcon())
        self.textPathProcedure.Button = "opens.png"
        self.textPathProcedure.LabelWidth = 120
        self.textPathProcedure.textBox.setMaximumWidth(10000)
        self.textPathProcedure.textBox.setMinimumWidth(100)
        self.basicFrame.Add = self.textPathProcedure

        self.btnFrame = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.btnFrame

        self.buttonAddProcedure = QPushButton(self.btnFrame)
        self.buttonAddProcedure.setObjectName("buttonAddProcedure")
        self.buttonAddProcedure.setText("Add")
        self.btnFrame.Add = self.buttonAddProcedure

        self.buttonModifyProcedure = QPushButton(self.btnFrame)
        self.buttonModifyProcedure.setObjectName("buttonModifyProcedure")
        self.buttonModifyProcedure.setText("Modify")
        self.btnFrame.Add = self.buttonModifyProcedure

        self.buttonDeleteProcedure = QPushButton(self.btnFrame)
        self.buttonDeleteProcedure.setObjectName("buttonDeleteProcedure")
        self.buttonDeleteProcedure.setText("Delete")
        self.btnFrame.Add = self.buttonDeleteProcedure

        self.buttonSaveProcedure = QPushButton(self.btnFrame)
        self.buttonSaveProcedure.setObjectName("buttonSaveProcedure")
        self.buttonSaveProcedure.setText("Save")
        self.btnFrame.Add = self.buttonSaveProcedure

        self.buttonCloseProcedure = QPushButton(self.btnFrame)
        self.buttonCloseProcedure.setObjectName("buttonCloseProcedure")
        self.buttonCloseProcedure.setText("Close")
        self.btnFrame.Add = self.buttonCloseProcedure

        self.connect(self.listBoxProcedure, SIGNAL("Event_0"), self.listBoxProcedure_SelectedIndexChanged)
        self.connect(self.comboProjectProcedure, SIGNAL("Event_0"), self.comboProjectProcedure_SelectedIndexChanged)
        self.connect(self.comboSubProjectProcedure, SIGNAL("Event_0"), self.comboSubProjectProcedure_SelectedIndexChanged)
        self.connect(self.textPathProcedure, SIGNAL("Event_1"), self.buttonBrowseWorkspace_Click)

        self.buttonCloseProcedure.clicked.connect(self.buttonCloseProcedure_Click)
        self.buttonSaveProcedure.clicked.connect(self.buttonSaveProcedure_Click)
        self.buttonDeleteProcedure.clicked.connect(self.buttonDeleteProcedure_Click)
        self.buttonModifyProcedure.clicked.connect(self.buttonModifyProcedure_Click)
        self.buttonAddProcedure.clicked.connect(self.buttonAddProcedure_Click)

        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if (pi.Pt == enumProjectType.ptFile):
                self.listBoxProcedure.Add(pi.Name)
            elif (pi.Pt == enumProjectType.ptProject):
                self.comboProjectProcedure.Add(pi.Name)
            elif (pi.Pt == enumProjectType.ptSubProject):
                self.comboSubProjectProcedure.Add(pi.Name)
            elif (pi.Pt == enumProjectType.ptWorkspace):
                self.comboWorkspaceProcedure.Add(pi.Name)
        self.comboProjectProcedure_SelectedIndexChanged()
        self.comboSubProjectProcedure_SelectedIndexChanged()

    
    def CheckInputValues(self):
        if (self.textNameProcedure.Text == None or self.textNameProcedure.Text == ""):
            QMessageBox.warning(self, "Warning", "Please input project name!")
            return False
        if (self.textPathProcedure.Text == None or self.textPathProcedure.Text == ""):
            QMessageBox.warning(self, "Warning", "Please input project path!")
            return False
        if (self.comboProjectProcedure.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select an Project!")
            return False
        if (self.comboSubProjectProcedure.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select an Sub-Project!")
            return False
        if (self.comboWorkspaceProcedure.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select an Workspace!")
            return
        directory = QDir(self.textPathProcedure.Text)
        if (not directory.exists()):
            if (QMessageBox.question(self, "Question", "Procedure path dose not exist! Do you create the directory?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes):
                directory.mkpath(self.textPathProcedure.Text)
            else:
                return False
        return True


    # private void WorkspaceMngForm_Load(object sender, EventArgs e)
    # {
    #     try
    #     {
    #         foreach (ProjectInfo pi in AirCraftOperation.g_projectList.ProjectsList)
    #         {
    #             if (pi.Pt == enumProjectType.ptFile)
    #             {
    #                 self.listBoxProcedure.Items.Add(pi.Name)
    #             }
    #             else if (pi.Pt == enumProjectType.ptProject)
    #             {
    #                 self.comboProjectProcedure.Items.Add(pi.Name)
    #             }
    #             else if (pi.Pt == enumProjectType.ptSubProject)
    #             {
    #                 self.comboSubProjectProcedure.Items.Add(pi.Name)
    #             }
    #             else if (pi.Pt == enumProjectType.ptWorkspace)
    #             {
    #                 self.comboWorkspaceProcedure.Items.Add(pi.Name)
    #             }
    #         }
    #     }
    #     catch (System.Exception ex)
    #     {
    #         MessageBox.Show(ex.Message)
    #     }
    # }

    def listBoxProcedure_SelectedIndexChanged(self):
        if (self.listBoxProcedure.SelectedIndex < 0):
            return
        pi = AirCraftOperation.g_projectList.Find(self.listBoxProcedure.Items[self.listBoxProcedure.SelectedIndex])
        self.textNameProcedure.Text = AirCraftOperation.g_projectList.ProjectsList[pi].Name
        self.textPathProcedure.Text = AirCraftOperation.g_projectList.ProjectsList[pi].Path
        self.comboProjectProcedure.SelectedIndex = self.comboProjectProcedure.IndexOf(AirCraftOperation.g_projectList.ProjectsList[pi].ProjName)
        self.comboSubProjectProcedure.SelectedIndex = self.comboSubProjectProcedure.IndexOf(AirCraftOperation.g_projectList.ProjectsList[pi].SubProjName)
        self.comboWorkspaceProcedure.SelectedIndex = self.comboWorkspaceProcedure.IndexOf(AirCraftOperation.g_projectList.ProjectsList[pi].WorkspaceName)

    def buttonBrowseWorkspace_Click(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Open Project Path")
        if (folderPath != None and folderPath != ""):
            self.textPathProcedure.Value = folderPath

    def buttonSaveProcedure_Click(self):
        res = QMessageBox.question(self, "Question", "Save changes to project information?", QMessageBox.Yes | QMessageBox.No)
        if (res == QMessageBox.Yes):
            AirCraftOperation.g_projectList.WriteProjectInfoXml()
            self.buttonSaveProcedure.setEnabled(False)

    def buttonCloseProcedure_Click(self):
        # if (self.buttonSaveProcedure.isEnabled() == True):
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
        #     }
        # }
        self.accept()

    def buttonAddProcedure_Click(self):
        if (not self.CheckInputValues()):
            return

        if (AirCraftOperation.g_projectList.Find(self.textNameProcedure.Text) != None):
            QMessageBox.warning(self, "Warning", "The same name exist!")
            return
        pi = ProjectInfo()
        pi.Pt = enumProjectType.ptFile
        pi.Name = self.textNameProcedure.Text
        pi.Path = self.textPathProcedure.Text
        pi.ProjName = self.comboProjectProcedure.SelectedItem
        pi.SubProjName = self.comboSubProjectProcedure.SelectedItem
        pi.WorkspaceName = self.comboWorkspaceProcedure.SelectedItem
        pi.UserName = AirCraftOperation.g_loginedUser.Name

        AirCraftOperation.g_projectList.Add(pi)

        nIndex = self.listBoxProcedure.Add(pi.Name)
        self.listBoxProcedure.SelectedIndex = nIndex
        self.buttonSaveProcedure.setEnabled(True)

    def buttonModifyProcedure_Click(self):
        if (self.listBoxProcedure.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select project in the projects list!")
            return
        if (not self.CheckInputValues()):
            return
        index = AirCraftOperation.g_projectList.Find(self.listBoxProcedure.Items[self.listBoxProcedure.SelectedIndex])
        AirCraftOperation.g_projectList.ProjectsList[index].Pt = enumProjectType.ptFile
        AirCraftOperation.g_projectList.ProjectsList[index].Name = self.textNameProcedure.Text
        AirCraftOperation.g_projectList.ProjectsList[index].Path = self.textPathProcedure.Text
        AirCraftOperation.g_projectList.ProjectsList[index].ProjName = self.comboProjectProcedure.SelectedItem
        AirCraftOperation.g_projectList.ProjectsList[index].SubProjName = self.comboSubProjectProcedure.SelectedItem
        AirCraftOperation.g_projectList.ProjectsList[index].WorkspaceName = self.comboWorkspaceProcedure.SelectedItem
        AirCraftOperation.g_projectList.ProjectsList[index].UserName = AirCraftOperation.g_loginedUser.Name

        self.listBoxProcedure.Clear()
        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if (pi.Pt == enumProjectType.ptFile):
                self.listBoxProcedure.Add(pi.Name)

        # AirCraftOperation.g_projectList.Remove(pi)
        #
        # AirCraftOperation.g_projectList.Add(pi)
        self.buttonSaveProcedure.setEnabled(True)

    def buttonDeleteProcedure_Click(self):
        if (self.listBoxProcedure.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select project in the projects list!")
            return

        if (QMessageBox.question(self, "Question", "Are you sure to delete " + self.listBoxProcedure.Items[self.listBoxProcedure.SelectedIndex] + "?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
            return
        AirCraftOperation.g_projectList.Remove(self.listBoxProcedure.Items[self.listBoxProcedure.SelectedIndex], enumProjectType.ptFile)
        self.buttonSaveProcedure.setEnabled(True)
        self.listBoxProcedure.Clear()
        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if (pi.Pt == enumProjectType.ptFile):
                self.listBoxProcedure.Add(pi.Name)

    def comboProjectProcedure_SelectedIndexChanged(self):
        listSubprojects = AirCraftOperation.g_projectList.GetLinkedProjects(self.comboProjectProcedure.SelectedItem, enumProjectType.ptProject, enumProjectType.ptSubProject)
        self.comboSubProjectProcedure.Clear()
        if (listSubprojects != None and len(listSubprojects) > 0):

            self.comboSubProjectProcedure.Items = listSubprojects
            self.comboSubProjectProcedure.SelectedIndex = 0
        self.comboSubProjectProcedure_SelectedIndexChanged()

    def comboSubProjectProcedure_SelectedIndexChanged(self):
        listWorkspace = AirCraftOperation.g_projectList.GetLinkedProjects(self.comboSubProjectProcedure.SelectedItem, enumProjectType.ptSubProject, enumProjectType.ptWorkspace)
        self.comboWorkspaceProcedure.Clear()
        if (listWorkspace != None and len(listWorkspace) > 0):

            self.comboWorkspaceProcedure.Items = listWorkspace
            self.comboWorkspaceProcedure.SelectedIndex = 0