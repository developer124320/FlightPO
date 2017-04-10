

from PyQt4.QtGui import QDialog, QPushButton, QVBoxLayout, QFont, QFileDialog, QMessageBox, QIcon
from PyQt4.QtCore import SIGNAL, QFileInfo, QDir, QFile
from FlightPlanner.Panels.ListBox import ListBox
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame

from ProjectManager.ProjectInfo import enumProjectType
from ProjectManager.ProjectInfo import ProjectInfo, ProjectList
from AircraftOperation import AirCraftOperation

class SelectProcedureForm(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self)

        self.setObjectName(("ui_ProjectMngForm"))
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

        self.comboUser = ComboBoxPanel(self.basicFrame)
        self.comboUser.Caption = "Select User"
        self.comboUser.LabelWidth = 120
        self.comboUser.Width = 200
        self.basicFrame.Add = self.comboUser

        self.comboAIP = ComboBoxPanel(self.basicFrame)
        self.comboAIP.Caption = "AIP Chart"
        self.comboAIP.LabelWidth = 120
        self.comboAIP.Width = 200
        self.basicFrame.Add = self.comboAIP

        self.comboProject = ComboBoxPanel(self.basicFrame)
        self.comboProject.Caption = "Project"
        self.comboProject.LabelWidth = 120
        self.comboProject.Width = 200
        self.basicFrame.Add = self.comboProject

        self.comboSubproject = ComboBoxPanel(self.basicFrame)
        self.comboSubproject.Caption = "Sub-Project"
        self.comboSubproject.LabelWidth = 120
        self.comboSubproject.Width = 200
        self.basicFrame.Add = self.comboSubproject

        self.comboWorkspace = ComboBoxPanel(self.basicFrame)
        self.comboWorkspace.Caption = "Workspace"
        self.comboWorkspace.LabelWidth = 120
        self.comboWorkspace.Width = 200
        self.basicFrame.Add = self.comboWorkspace

        self.comboProcedure = ComboBoxPanel(self.basicFrame)
        self.comboProcedure.Caption = "Procedure"
        self.comboProcedure.LabelWidth = 120
        self.comboProcedure.Width = 200
        self.basicFrame.Add = self.comboProcedure

        self.btnFrame = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.btnFrame

        self.buttonStart = QPushButton(self.btnFrame)
        self.buttonStart.setObjectName("buttonStart")
        self.buttonStart.setText("Start")
        self.btnFrame.Add = self.buttonStart

        self.buttonCalcel = QPushButton(self.btnFrame)
        self.buttonCalcel.setObjectName("buttonCalcel")
        self.buttonCalcel.setText("Cancel")
        self.btnFrame.Add = self.buttonCalcel

        self.connect(self.comboProject, SIGNAL("Event_0"), self.comboProject_SelectedIndexChanged)
        self.connect(self.comboSubproject, SIGNAL("Event_0"), self.comboSubproject_SelectedIndexChanged)
        self.connect(self.comboWorkspace, SIGNAL("Event_0"), self.comboWorkspace_SelectedIndexChanged)

        self.buttonStart.clicked.connect(self.buttonStart_Click)
        self.buttonCalcel.clicked.connect(self.buttonCalcel_Click)
        
        for ui in AirCraftOperation.g_userList.ListUserInfo:
            self.comboUser.Add(ui.Name)

        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if (pi.Pt == enumProjectType.ptAipChart):
                self.comboAIP.Add(pi.Name)
            elif (pi.Pt == enumProjectType.ptProject):
                self.comboProject.Add(pi.Name)
        self.comboUser.SelectedIndex = 0
        self.comboAIP.SelectedIndex = 0
        self.comboProject.SelectedIndex = 0

    def comboUser_SelectedIndexChanged(self):
        pass
    def buttonCalcel_Click(self):
        self.reject()

    def buttonStart_Click(self):
        index = AirCraftOperation.g_projectList.Find(self.comboAIP.SelectedItem, enumProjectType.ptAipChart)
        if index != None:
            AirCraftOperation.g_currentAIP = AirCraftOperation.g_projectList.ProjectsList[index]
            if (not QFile.exists(AirCraftOperation.g_currentAIP.Path)):
                QMessageBox.warning(self, "Warning", "Invalid AIPChart!")
                return

        index = AirCraftOperation.g_projectList.Find(self.comboProcedure.SelectedItem, enumProjectType.ptFile)
        if index != None:
            AirCraftOperation.g_currentProcedure = AirCraftOperation.g_projectList.ProjectsList[index]
        else:
            QMessageBox.warning(self, "Warning", "Invalid Procedure!\nPlease create or modify a procedure!")
            self.reject()
        # IWorkspaceFactory ipWSF = new ShapefileWorkspaceFactoryClass()
        # IWorkspace ipWS = ipWSF.OpenFromFile(AirCraftOperation.g_currentProcedure.Path, 0)
        # if (ipWS == null)
        # {
        #     throw new Exception("Failed in opening the procedure path!")
        # }

        index = AirCraftOperation.g_projectList.Find(self.comboProject.SelectedItem, enumProjectType.ptProject)
        if index != None:
            AirCraftOperation.g_currentProject = AirCraftOperation.g_projectList.ProjectsList[index]
        else:
            QMessageBox.warning(self, "Warning", "Invalid Project!\nPlease create or modify a project!")
            self.reject()

        index = AirCraftOperation.g_projectList.Find(self.comboSubproject.SelectedItem, enumProjectType.ptSubProject)
        if index != None:
            AirCraftOperation.g_currentSubproject = AirCraftOperation.g_projectList.ProjectsList[index]
        else:
            QMessageBox.warning(self, "Warning", "Invalid Sub-Project!\nPlease create or modify a sub-project!")
            self.reject()

        index = AirCraftOperation.g_projectList.Find(self.comboWorkspace.SelectedItem, enumProjectType.ptWorkspace)
        if index != None:
            AirCraftOperation.g_currentWorkspace = AirCraftOperation.g_projectList.ProjectsList[index]
        else:
            QMessageBox.warning(self, "Warning", "Invalid Workspace!\nPlease create or modify a Workspace!")
            self.reject()

        self.accept()

    def comboProject_SelectedIndexChanged(self):
        listSubprojects = AirCraftOperation.g_projectList.GetLinkedProjects(self.comboProject.SelectedItem, enumProjectType.ptProject, enumProjectType.ptSubProject)
        self.comboSubproject.Clear()
        if (listSubprojects != None and len(listSubprojects) > 0):

            self.comboSubproject.Items = listSubprojects
            self.comboSubproject.SelectedIndex = 0

    def comboSubproject_SelectedIndexChanged(self):
        listWorkspace = AirCraftOperation.g_projectList.GetLinkedProjects(self.comboSubproject.SelectedItem, enumProjectType.ptSubProject, enumProjectType.ptWorkspace)
        self.comboWorkspace.Clear()
        if (listWorkspace != None and len(listWorkspace) > 0):

            self.comboWorkspace.Items = listWorkspace
            self.comboWorkspace.SelectedIndex = 0

    def comboWorkspace_SelectedIndexChanged(self):
        listProcedures = AirCraftOperation.g_projectList.GetLinkedProjects(self.comboWorkspace.SelectedItem, enumProjectType.ptWorkspace, enumProjectType.ptFile)
        self.comboProcedure.Clear()
        if (listProcedures != None and len(listProcedures) > 0):

            self.comboProcedure.Items = listProcedures
            self.comboProcedure.SelectedIndex = 0