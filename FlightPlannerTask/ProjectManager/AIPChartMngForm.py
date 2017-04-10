

from PyQt4.QtGui import QDialog, QPushButton, QVBoxLayout, QFont, QFileDialog, QMessageBox, QIcon
from PyQt4.QtCore import SIGNAL, QFileInfo, QDir, QCoreApplication, QFile
from FlightPlanner.Panels.ListBox import ListBox
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame

from ProjectManager.ProjectInfo import enumProjectType
from ProjectManager.ProjectInfo import ProjectInfo, ProjectList
from AircraftOperation import AirCraftOperation

class AIPChartMngForm(QDialog):
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

        self.groubox = GroupBox(self.basicFrame)
        self.groubox.Caption = "Select a project"
        self.basicFrame.Add = self.groubox

        self.listBoxAIPChart = ListBox(self.groubox)
        self.groubox.Add = self.listBoxAIPChart

        self.textNameAIPChart = TextBoxPanel(self.basicFrame)
        self.textNameAIPChart.Caption = "Name"
        self.textNameAIPChart.LabelWidth = 50
        self.textNameAIPChart.Width = 120
        self.basicFrame.Add = self.textNameAIPChart

        self.textPathAIPChart = TextBoxPanel(self.basicFrame)
        self.textPathAIPChart.Caption = "Path"
        self.textPathAIPChart.imageButton.setIcon(QIcon())
        self.textPathAIPChart.Button = "opens.png"
        self.textPathAIPChart.LabelWidth = 50
        self.textPathAIPChart.textBox.setMaximumWidth(10000)
        self.textPathAIPChart.textBox.setMinimumWidth(100)
        self.basicFrame.Add = self.textPathAIPChart

        self.btnFrame = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.btnFrame

        self.buttonAddAIPChart = QPushButton(self.btnFrame)
        self.buttonAddAIPChart.setObjectName("buttonAddAIPChart")
        self.buttonAddAIPChart.setText("Add")
        self.btnFrame.Add = self.buttonAddAIPChart

        self.buttonModifyAIPChart = QPushButton(self.btnFrame)
        self.buttonModifyAIPChart.setObjectName("buttonModifyAIPChart")
        self.buttonModifyAIPChart.setText("Modify")
        self.btnFrame.Add = self.buttonModifyAIPChart

        self.buttonDeleteAIPChart = QPushButton(self.btnFrame)
        self.buttonDeleteAIPChart.setObjectName("buttonDeleteAIPChart")
        self.buttonDeleteAIPChart.setText("Delete")
        self.btnFrame.Add = self.buttonDeleteAIPChart

        self.buttonSaveAIPChart = QPushButton(self.btnFrame)
        self.buttonSaveAIPChart.setObjectName("buttonSaveAIPChart")
        self.buttonSaveAIPChart.setText("Save")
        self.btnFrame.Add = self.buttonSaveAIPChart

        self.buttonCloseAIPChart = QPushButton(self.btnFrame)
        self.buttonCloseAIPChart.setObjectName("buttonCloseAIPChart")
        self.buttonCloseAIPChart.setText("Close")
        self.btnFrame.Add = self.buttonCloseAIPChart

        self.connect(self.listBoxAIPChart, SIGNAL("Event_0"), self.listBoxProject_SelectedIndexChanged)
        self.connect(self.textPathAIPChart, SIGNAL("Event_1"), self.buttonBrowseProject_Click)

        self.buttonAddAIPChart.clicked.connect(self.buttonAddProject_Click)
        self.buttonModifyAIPChart.clicked.connect(self.buttonModifyProject_Click)
        self.buttonDeleteAIPChart.clicked.connect(self.buttonDeleteProject_Click)
        self.buttonSaveAIPChart.clicked.connect(self.buttonSaveProject_Click)
        self.buttonCloseAIPChart.clicked.connect(self.buttonCloseProject_Click)
        
        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if (pi.Pt == enumProjectType.ptAipChart):
                self.listBoxAIPChart.Add(pi.Name)

    def buttonBrowseProject_Click(self):
        filePathDir = QFileDialog.getOpenFileName(self, "Open Project File",QCoreApplication.applicationDirPath (),"QGIS Project Files (*.qgs)")
        if filePathDir == "":
            return
        self.textPathAIPChart.Value = filePathDir
        
    def buttonAddProject_Click(self):
        if (not self.CheckInputValues()):
            return

        if (AirCraftOperation.g_projectList.Find(self.textNameAIPChart.Text) != None):
            QMessageBox.warning(self, "Warning", "The same project exist!")
        pi = ProjectInfo()
        pi.Pt = enumProjectType.ptAipChart
        pi.Name = self.textNameAIPChart.Text
        pi.Path = self.textPathAIPChart.Text
        pi.UserName = AirCraftOperation.g_loginedUser.Name

        AirCraftOperation.g_projectList.Add(pi)

        nIndex = self.listBoxAIPChart.Add(pi.Name)
        self.listBoxAIPChart.SelectedIndex = nIndex
        self.buttonSaveAIPChart.setEnabled(True)

    def buttonSaveProject_Click(self):
        res = QMessageBox.question(self, "Alert", "Save changes to project information?", QMessageBox.Yes | QMessageBox.No)
        if (res == QMessageBox.Yes):
            AirCraftOperation.g_projectList.WriteProjectInfoXml()
            self.buttonSaveAIPChart.setEnabled(False)

    def buttonCloseProject_Click(self):
        self.accept()
    #     if (self.buttonSaveAIPChart.Enabled == True)
    #     {
    #         DialogResult res = MessageBox.Show("Save changes to project information?", "Alert", MessageBoxButtons.YesNoCancel)
    #         if (res == DialogResult.Yes)
    #         {
    #             self.buttonSaveProject_Click(sender, e)
    #         }
    #         else if (res == DialogResult.No)
    #         {
    #         }
    #         else if (res == DialogResult.Cancel)
    #         {
    #             self.DialogResult = DialogResult.None
    #             return
    #         }
    #     }
    # }

    def CheckInputValues(self):
        if (self.textNameAIPChart.Text == None or self.textNameAIPChart.Text == ""):
            QMessageBox.warning(self, "Warning", "Please input project name!")
            return False
        if (self.textPathAIPChart.Text == None or self.textPathAIPChart.Text == ""):
            QMessageBox.warning(self, "Warning", "Please input project path!")
            return False

        if (not QFile.exists(self.textPathAIPChart.Text)):
            QMessageBox.warning(self, "Warning", "Invalid AIP Chart!")
            return False
        return True

    def buttonModifyProject_Click(self):
        if (self.listBoxAIPChart.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select project in the projects list!")
        if (not self.CheckInputValues()):
            return
        index = AirCraftOperation.g_projectList.Find(self.listBoxAIPChart.Items[self.listBoxAIPChart.SelectedIndex])
        AirCraftOperation.g_projectList.ProjectsList[index].Pt = enumProjectType.ptAipChart
        AirCraftOperation.g_projectList.ProjectsList[index].Name = self.textNameAIPChart.Text
        AirCraftOperation.g_projectList.ProjectsList[index].Path = self.textPathAIPChart.Text
        AirCraftOperation.g_projectList.ProjectsList[index].UserName = AirCraftOperation.g_loginedUser.Name
        self.buttonSaveAIPChart.setEnabled(True)
        self.listBoxAIPChart.Clear()
        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if (pi.Pt == enumProjectType.ptAipChart):
                self.listBoxAIPChart.Add(pi.Name)


    def buttonDeleteProject_Click(self):
        if (self.listBoxAIPChart.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select project in the projects list!")
            return
        AirCraftOperation.g_projectList.Remove(self.listBoxAIPChart.Items[self.listBoxAIPChart.SelectedIndex])
        self.buttonSaveAIPChart.setEnabled(True)
        self.listBoxAIPChart.Clear()
        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if (pi.Pt == enumProjectType.ptAipChart):
                self.listBoxAIPChart.Add(pi.Name)

    def listBoxProject_SelectedIndexChanged(self):
        if (self.listBoxAIPChart.SelectedIndex < 0):
            return
        index = AirCraftOperation.g_projectList.Find(self.listBoxAIPChart.Items[self.listBoxAIPChart.SelectedIndex])
        self.textNameAIPChart.Text = AirCraftOperation.g_projectList.ProjectsList[index].Name
        self.textPathAIPChart.Text = AirCraftOperation.g_projectList.ProjectsList[index].Path

