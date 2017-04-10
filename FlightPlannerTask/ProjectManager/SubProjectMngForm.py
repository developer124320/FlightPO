

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

class SubProjectMngForm(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self)

        self.setObjectName(("ui_SubProjectMngForm"))
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

        self.comboProjectSubproject = ComboBoxPanel(self.frame)
        self.comboProjectSubproject.Caption = "Project"
        self.comboProjectSubproject.LabelWidth = 120
        self.frame.Add = self.comboProjectSubproject

        self.textNameSubproject = TextBoxPanel(self.frame)
        self.textNameSubproject.Caption = "Sub-Project Name"
        self.textNameSubproject.LabelWidth = 120
        self.textNameSubproject.Width = 120
        self.frame.Add = self.textNameSubproject

        self.groubox = GroupBox(self.frameName)
        self.groubox.Caption = "Sub-Projects"
        self.frameName.Add = self.groubox

        self.listBoxSubproject = ListBox(self.groubox)
        self.groubox.Add = self.listBoxSubproject

        self.textPathSubproject = TextBoxPanel(self.basicFrame)
        self.textPathSubproject.Caption = "Sub-Project Path"
        self.textPathSubproject.imageButton.setIcon(QIcon())
        self.textPathSubproject.Button = "opens.png"
        self.textPathSubproject.LabelWidth = 120
        self.textPathSubproject.textBox.setMaximumWidth(10000)
        self.textPathSubproject.textBox.setMinimumWidth(100)
        self.basicFrame.Add = self.textPathSubproject

        self.btnFrame = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.btnFrame

        self.buttonAddSubproject = QPushButton(self.btnFrame)
        self.buttonAddSubproject.setObjectName("buttonAddSubproject")
        self.buttonAddSubproject.setText("Add")
        self.btnFrame.Add = self.buttonAddSubproject

        self.buttonModifySubproject = QPushButton(self.btnFrame)
        self.buttonModifySubproject.setObjectName("buttonModifySubproject")
        self.buttonModifySubproject.setText("Modify")
        self.btnFrame.Add = self.buttonModifySubproject

        self.buttonDeleteSubproject = QPushButton(self.btnFrame)
        self.buttonDeleteSubproject.setObjectName("buttonDeleteSubproject")
        self.buttonDeleteSubproject.setText("Delete")
        self.btnFrame.Add = self.buttonDeleteSubproject

        self.buttonSaveSubproject = QPushButton(self.btnFrame)
        self.buttonSaveSubproject.setObjectName("buttonSaveProject")
        self.buttonSaveSubproject.setText("Save")
        self.btnFrame.Add = self.buttonSaveSubproject

        self.buttonCloseSubproject = QPushButton(self.btnFrame)
        self.buttonCloseSubproject.setObjectName("buttonCloseSubproject")
        self.buttonCloseSubproject.setText("Close")
        self.btnFrame.Add = self.buttonCloseSubproject

        self.connect(self.listBoxSubproject, SIGNAL("Event_0"), self.listBox1_SelectedIndexChanged)
        self.connect(self.textPathSubproject, SIGNAL("Event_1"), self.buttonBrowseSubproject_Click)

        self.buttonCloseSubproject.clicked.connect(self.buttonCloseSubproject_Click)
        self.buttonSaveSubproject.clicked.connect(self.buttonSaveSubproject_Click)
        self.buttonDeleteSubproject.clicked.connect(self.buttonDeleteSubproject_Click)
        self.buttonModifySubproject.clicked.connect(self.buttonModifySubproject_Click)
        self.buttonAddSubproject.clicked.connect(self.buttonAddSubproject_Click)

        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if (pi.Pt == enumProjectType.ptSubProject):
                self.listBoxSubproject.Add(pi.Name)
            elif (pi.Pt == enumProjectType.ptProject):
                self.comboProjectSubproject.Add(pi.Name)
        
    def CheckInputValues(self):
        if (self.textNameSubproject.Text == None or self.textNameSubproject.Text == ""):
            QMessageBox.warning(self, "Warning", "Please input project name!")
            return False
        if (self.textPathSubproject.Text == None or self.textPathSubproject.Text == ""):
            QMessageBox.warning(self, "Warning", "Please input project path!")
            return False
        if (self.comboProjectSubproject.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select an project!")
            return False
        directory = QDir(self.textPathSubproject.Text)
        if (not directory.exists()):
            if (QMessageBox.question(self, "Question", "Procedure path dose not exist! Do you create the directory?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes):
                directory.mkpath(self.textPathSubproject.Text)
            else:
                return False
        return True
    
    def listBox1_SelectedIndexChanged(self):
        if (self.listBoxSubproject.SelectedIndex < 0):
            return
        pi = AirCraftOperation.g_projectList.Find(self.listBoxSubproject.Items[self.listBoxSubproject.SelectedIndex])
        self.textNameSubproject.Text = AirCraftOperation.g_projectList.ProjectsList[pi].Name
        self.textPathSubproject.Text = AirCraftOperation.g_projectList.ProjectsList[pi].Path
        self.comboProjectSubproject.SelectedIndex = self.comboProjectSubproject.IndexOf(AirCraftOperation.g_projectList.ProjectsList[pi].ProjName)

    
    # def SubProjectMngForm_Load(object sender, EventArgs e)
    # {
    #     try
    #     {
    #         foreach (ProjectInfo pi in AirCraftOperation.g_projectList.ProjectsList)
    #         {
    #             if (pi.Pt == enumProjectType.ptSubProject)
    #             {
    #                 self.listBoxSubproject.Items.Add(pi.Name)
    #             }
    #             else if (pi.Pt == enumProjectType.ptProject)
    #             {
    #                 self.comboProjectSubproject.Items.Add(pi.Name)
    #             }
    #         }
    #     }
    #     catch (System.Exception ex)
    #     {
    #         MessageBox.Show(ex.Message)
    #     }
    # }
    
    def buttonBrowseSubproject_Click(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Open Project Path")
        if (folderPath != None and folderPath != ""):
            self.textPathSubproject.Value = folderPath

    def buttonSaveSubproject_Click(self):
        res = QMessageBox.question(self, "Question", "Save changes to project information?", QMessageBox.Yes | QMessageBox.No)
        if (res == QMessageBox.Yes):
            AirCraftOperation.g_projectList.WriteProjectInfoXml()
            self.buttonSaveSubproject.setEnabled(False)
    
    def buttonCloseSubproject_Click(self):
        # if (self.buttonSaveSubproject.isEnabled() == True):
        #     res = QMessageBox.question(self, "Question", "Save changes to project information?", QMessageBox.Yes | QMessageBox.No)
        #     if (res == QMessageBox.Yes):
        #         self.buttonSaveSubproject_Click()
        self.accept()
    
    def buttonAddSubproject_Click(self):
        if (not self.CheckInputValues()):
            return

        if (AirCraftOperation.g_projectList.Find(self.textNameSubproject.Text) != None):
            QMessageBox.warning(self, "Warning", "The same sub-project exist!")
            return
        pi = ProjectInfo()
        pi.Pt = enumProjectType.ptSubProject
        pi.Name = self.textNameSubproject.Text
        pi.Path = self.textPathSubproject.Text
        pi.ProjName = self.comboProjectSubproject.SelectedItem
        pi.UserName = AirCraftOperation.g_loginedUser.Name

        AirCraftOperation.g_projectList.Add(pi)

        nIndex = self.listBoxSubproject.Add(pi.Name)
        self.listBoxSubproject.SelectedIndex = nIndex
        self.buttonSaveSubproject.setEnabled(True)
    
    def buttonModifySubproject_Click(self):
        if (self.listBoxSubproject.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select project in the projects list!")
            return
        if (not self.CheckInputValues()):
            return
        index = AirCraftOperation.g_projectList.Find(self.listBoxSubproject.Items[self.listBoxSubproject.SelectedIndex])
        AirCraftOperation.g_projectList.ProjectsList[index].Pt = enumProjectType.ptSubProject
        AirCraftOperation.g_projectList.ProjectsList[index].Name = self.textNameSubproject.Text
        AirCraftOperation.g_projectList.ProjectsList[index].Path = self.textPathSubproject.Text
        AirCraftOperation.g_projectList.ProjectsList[index].ProjName = self.comboProjectSubproject.SelectedItem
        AirCraftOperation.g_projectList.ProjectsList[index].UserName = AirCraftOperation.g_loginedUser.Name

        # AirCraftOperation.g_projectList.Remove(pi)
        #
        # AirCraftOperation.g_projectList.Add(pi)
        # self.buttonSaveSubproject.Enabled = True

        self.listBoxSubproject.Clear()
        # self.comboProjectSubproject.Clear()
        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if (pi.Pt == enumProjectType.ptSubProject):
                self.listBoxSubproject.Add(pi.Name)
            # elif (pi.Pt == enumProjectType.ptProject):
            #     self.comboProjectSubproject.Add(pi.Name)
    
    def buttonDeleteSubproject_Click(self):
        if (self.listBoxSubproject.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select project in the projects list!")
            return

        if (QMessageBox.question(self, "Question", "Are you sure to delete " + self.listBoxSubproject.Items[self.listBoxSubproject.SelectedIndex] + "?",QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
            return
        AirCraftOperation.g_projectList.Remove(self.listBoxSubproject.Items[self.listBoxSubproject.SelectedIndex], enumProjectType.ptSubProject)

        self.listBoxSubproject.Clear()
        # self.comboProjectSubproject.Clear()
        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if (pi.Pt == enumProjectType.ptSubProject):
                self.listBoxSubproject.Add(pi.Name)
            # elif (pi.Pt == enumProjectType.ptProject):
            #     self.comboProjectSubproject.Add(pi.Name)
        self.buttonSaveSubproject.setEnabled(True)