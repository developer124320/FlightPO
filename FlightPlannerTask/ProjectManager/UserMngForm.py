
from PyQt4.QtGui import QDialog, QPushButton, QVBoxLayout, QFont, QFileDialog, QMessageBox, QRadioButton
from PyQt4.QtCore import SIGNAL, QFileInfo, QDir
from FlightPlanner.Panels.ListBox import ListBox
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame

from ProjectManager.MYUSERINFO import MYUSERINFO, enumUserRight
from ProjectManager.ProjectInfo import ProjectInfo, ProjectList
from AircraftOperation import AirCraftOperation

class UserMngForm(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self)

        self.setObjectName(("ui_UserMngForm"))
        self.resize(200, 200)
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)

        self.vlForm = QVBoxLayout(self)
        self.vlForm.setObjectName(("vl_UserMngForm"))
        self.vlForm.setSpacing(9)
        self.vlForm.setMargin(9)

        self.basicFrame = Frame(self)
        self.vlForm.addWidget(self.basicFrame)

        self.userContentFrm = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.userContentFrm

        self.groupbox = GroupBox(self.userContentFrm)
        self.groupbox.Caption = "Users"
        self.userContentFrm.Add = self.groupbox

        self.listBoxUser = ListBox(self.groupbox)
        self.groupbox.Add = self.listBoxUser

        self.userDataFrm = Frame(self.userContentFrm)
        self.userContentFrm.Add = self.userDataFrm

        self.groupBoxUserinfo = GroupBox(self.userDataFrm)
        self.groupBoxUserinfo.Caption = "User Information"
        self.userDataFrm.Add = self.groupBoxUserinfo

        self.userFullFrm = Frame(self.groupBoxUserinfo, "HL")
        self.groupBoxUserinfo.Add = self.userFullFrm

        self.textFirstName = TextBoxPanel(self.userFullFrm)
        self.textFirstName.Caption = "First Name"
        self.textFirstName.LabelWidth = 70
        self.textFirstName.Width = 120
        self.userFullFrm.Add = self.textFirstName

        self.textLastName = TextBoxPanel(self.userFullFrm)
        self.textLastName.Caption = "Last Name"
        self.textLastName.LabelWidth = 70
        self.textLastName.Width = 120
        self.userFullFrm.Add = self.textLastName

        self.userEmailPhoneFrm = Frame(self.groupBoxUserinfo, "HL")
        self.groupBoxUserinfo.Add = self.userEmailPhoneFrm

        self.textEMail = TextBoxPanel(self.userEmailPhoneFrm)
        self.textEMail.Caption = "E-Mail"
        self.textEMail.LabelWidth = 70
        self.textEMail.Width = 120
        self.userEmailPhoneFrm.Add = self.textEMail

        self.textPhone = TextBoxPanel(self.userEmailPhoneFrm)
        self.textPhone.Caption = "Phone"
        self.textPhone.LabelWidth = 70
        self.textPhone.Width = 120
        self.userEmailPhoneFrm.Add = self.textPhone

        self.userAddressCityFrm = Frame(self.groupBoxUserinfo, "HL")
        self.groupBoxUserinfo.Add = self.userAddressCityFrm

        self.textAddress = TextBoxPanel(self.userAddressCityFrm)
        self.textAddress.Caption = "Address"
        self.textAddress.LabelWidth = 70
        self.textAddress.Width = 120
        self.userAddressCityFrm.Add = self.textAddress

        self.textCity = TextBoxPanel(self.userAddressCityFrm)
        self.textCity.Caption = "City"
        self.textCity.LabelWidth = 70
        self.textCity.Width = 120
        self.userAddressCityFrm.Add = self.textCity

        self.userPostCodeStateFrm = Frame(self.groupBoxUserinfo, "HL")
        self.groupBoxUserinfo.Add = self.userPostCodeStateFrm

        self.textPostcode = TextBoxPanel(self.userPostCodeStateFrm)
        self.textPostcode.Caption = "Post Code"
        self.textPostcode.LabelWidth = 70
        self.textPostcode.Width = 120
        self.userPostCodeStateFrm.Add = self.textPostcode

        self.textState = TextBoxPanel(self.userPostCodeStateFrm)
        self.textState.Caption = "State"
        self.textState.LabelWidth = 70
        self.textState.Width = 120
        self.userPostCodeStateFrm.Add = self.textState

        self.groupBoxUserRoles = GroupBox(self.userDataFrm, "HL")
        self.groupBoxUserRoles.Caption = "User Roles"
        self.userDataFrm.Add = self.groupBoxUserRoles

        self.radioAdmin = QRadioButton(self.groupBoxUserRoles)
        self.radioAdmin.setObjectName("radioAdmin")
        self.radioAdmin.setText("Administrator")
        self.radioAdmin.setChecked(True)
        self.groupBoxUserRoles.Add = self.radioAdmin

        self.radioSuperuser = QRadioButton(self.groupBoxUserRoles)
        self.radioSuperuser.setObjectName("radioSuperuser")
        self.radioSuperuser.setText("Super User")
        self.groupBoxUserRoles.Add = self.radioSuperuser

        self.radioReadwrite = QRadioButton(self.groupBoxUserRoles)
        self.radioReadwrite.setObjectName("radioReadwrite")
        self.radioReadwrite.setText("Read / Write")
        self.groupBoxUserRoles.Add = self.radioReadwrite

        self.radioReadonly = QRadioButton(self.groupBoxUserRoles)
        self.radioReadonly.setObjectName("radioReadonly")
        self.radioReadonly.setText("Read Only")
        self.groupBoxUserRoles.Add = self.radioReadonly

        self.groupBoxUserDisplayInfo = GroupBox(self.userDataFrm, "HL")
        self.groupBoxUserDisplayInfo.Caption = "User Display Information"
        self.userDataFrm.Add = self.groupBoxUserDisplayInfo

        self.textName = TextBoxPanel(self.groupBoxUserDisplayInfo)
        self.textName.Caption = "Name"
        self.textName.LabelWidth = 70
        self.textName.Width = 120
        self.groupBoxUserDisplayInfo.Add = self.textName

        self.textPassword = TextBoxPanel(self.groupBoxUserDisplayInfo)
        self.textPassword.Caption = "Password"
        self.textPassword.LabelWidth = 70
        self.textPassword.Width = 120
        self.textPassword.EchoMode = "Password"
        self.groupBoxUserDisplayInfo.Add = self.textPassword

        self.btnFrame = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.btnFrame

        self.buttonAddUser = QPushButton(self.btnFrame)
        self.buttonAddUser.setObjectName("buttonAddUser")
        self.buttonAddUser.setText("Add")
        self.btnFrame.Add = self.buttonAddUser

        self.buttonModifyUser = QPushButton(self.btnFrame)
        self.buttonModifyUser.setObjectName("buttonModifyUser")
        self.buttonModifyUser.setText("Modify")
        self.btnFrame.Add = self.buttonModifyUser

        self.buttonDeleteUser = QPushButton(self.btnFrame)
        self.buttonDeleteUser.setObjectName("buttonDeleteUser")
        self.buttonDeleteUser.setText("Delete")
        self.btnFrame.Add = self.buttonDeleteUser

        self.buttonSaveUser = QPushButton(self.btnFrame)
        self.buttonSaveUser.setObjectName("buttonSaveUser")
        self.buttonSaveUser.setText("Save")
        self.btnFrame.Add = self.buttonSaveUser

        self.buttonCloseUser = QPushButton(self.btnFrame)
        self.buttonCloseUser.setObjectName("buttonCloseProject")
        self.buttonCloseUser.setText("Close")
        self.btnFrame.Add = self.buttonCloseUser

        self.connect(self.listBoxUser, SIGNAL("Event_0"), self.listBoxUser_SelectedIndexChanged)
        self.buttonAddUser.clicked.connect(self.buttonAddUser_Click)
        self.buttonModifyUser.clicked.connect(self.buttonModifyUser_Click)
        self.buttonDeleteUser.clicked.connect(self.buttonDeleteUser_Click)
        self.buttonSaveUser.clicked.connect(self.buttonSaveUser_Click)
        self.buttonCloseUser.clicked.connect(self.buttonCloseUser_Click)

        for ui in AirCraftOperation.g_userList.ListUserInfo:
            self.listBoxUser.Add(ui.Name)

    def listBoxUser_SelectedIndexChanged(self):
        try:
            if (self.listBoxUser.SelectedIndex < 0):
                return
            selectedName = self.listBoxUser.Items[self.listBoxUser.SelectedIndex]
            ui = AirCraftOperation.g_userList.FindUser(selectedName)
            if (ui.FName != None):
                self.textFirstName.Text = ui.FName
            else:
                self.textFirstName.Text = ""
            if (ui.LName != None):
                self.textLastName.Text = ui.LName
            else:
                self.textLastName.Text = ""
            if (ui.EMail != None):
                self.textEMail.Text = ui.EMail
            else:
                self.textEMail.Text = ""
            if (ui.Phone != None):
                self.textPhone.Text = ui.Phone
            else:
                self.textPhone.Text = ""
            if (ui.Address != None):
                self.textAddress.Text = ui.Address
            else:
                self.textAddress.Text = ""
            if (ui.PCode != None):
                self.textPostcode.Text = ui.PCode
            else:
                self.textPostcode.Text = ""
            if (ui.City != None):
                self.textCity.Text = ui.City
            else:
                self.textCity.Text = ""
            if (ui.State != None):
                self.textState.Text = ui.State
            else:
                self.textState.Text = ""
            if (ui.Name != None):
                self.textName.Text = ui.Name
            else:
                self.textName.Text = ""
            if (ui.Password != None):
                self.textPassword.Text = ui.Password
            else:
                self.textPassword.Text = ""
        except:
            pass
    def buttonAddUser_Click(self):
        if(not self.CheckInputValues()):
            return
        newUser = self.SetUserInfo()

        if( AirCraftOperation.g_userList.AddUser(newUser) ):
            self.listBoxUser.Add(newUser.Name)
            self.buttonSaveUser.Enabled = True

    def buttonModifyUser_Click(self):
        try:
            if (self.listBoxUser.SelectedIndex < 0):
                QMessageBox.warning(self, "Warning", "Please select an user in users list box!")
            if (not self.CheckInputValues()):
                return
            newUser = self.SetUserInfo()
            oldUser = AirCraftOperation.g_userList.FindUser(self.listBoxUser.Items[self.listBoxUser.SelectedIndex])
            
            if (oldUser != None):
                AirCraftOperation.g_userList.DeleteUser(oldUser)
                AirCraftOperation.g_userList.AddUser(newUser)
                self.listBoxUser.Clear()
                for ui in AirCraftOperation.g_userList.ListUserInfo:
                    self.listBoxUser.Add(ui.Name)
                self.buttonSaveUser.setEnabled(True)
        except:
            pass

    def buttonDeleteUser_Click(self):
        if (self.listBoxUser.SelectedIndex > -1):
            res = QMessageBox.question(self, "Question", "Save changes to user information?", QMessageBox.Yes | QMessageBox.No)
            if (res == QMessageBox.No):
                return
            userName = self.listBoxUser.Items[self.listBoxUser.SelectedIndex]
            AirCraftOperation.g_userList.DeleteUser(userName)
            self.listBoxUser.Clear()
            for ui in AirCraftOperation.g_userList.ListUserInfo:
                self.listBoxUser.Add(ui.Name)
            self.buttonSaveUser.setEnabled(True)
            self.listBoxUser.SelectedIndex = self.listBoxUser.SelectedIndex - 1 if(self.listBoxUser.SelectedIndex > 0) else 0
            self.listBoxUser_SelectedIndexChanged()

        
    def buttonSaveUser_Click(self):
        if (self.buttonSaveUser.isEnabled() == True):
            res = QMessageBox.question(self, "Question", "Save changes to user information?", QMessageBox.Yes | QMessageBox.No)
            if (res == QMessageBox.Yes):
                AirCraftOperation.g_userList.WriteUserInfoFile()
                self.buttonSaveUser.setEnabled(False)

    def buttonCloseUser_Click(self):
        # if (self.buttonSaveUser.isEnabled() == True):
        #     res = QMessageBox.question(self, "Question", "Save changes to user information?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        #     if (res == QMessageBox.Yes):
        #         self.buttonSaveUser_Click()
        #     elif (res == QMessageBox.No):
        #         pass
        #     elif (res == QMessageBox.Cancel):
        #         self.DialogResult = QMessageBox.Cancel
        #         return
        self.accept()
    
    def CheckInputValues(self):
        try:
            if (self.textFirstName.Text == ""):
                QMessageBox.warning(self, "Warning", "First name is required! Please input first name.")
                return False
            if (self.textLastName.Text == ""):
                QMessageBox.warning(self, "Warning", "Last name is required! Please input last name.")
                return False
            if (self.textName.Text == ""):
                QMessageBox.warning(self, "Warning", "Name is required! Please input display name.")
                return False
            return True
        except:
            return False
    
    def SetUserInfo(self):
        ui = MYUSERINFO()
        try:
            if (self.radioAdmin.isChecked()):
                ui.Right = enumUserRight.ur_Admin
            elif (self.radioSuperuser.isChecked()):
                ui.Right = enumUserRight.ur_SuperUser
            elif (self.radioReadwrite.isChecked()):
                ui.Right = enumUserRight.ur_ReadWrite
            elif (self.radioReadonly.isChecked()):
                ui.Right = enumUserRight.ur_ReadOnly

            if (self.textFirstName.Text != None):
                ui.FName = self.textFirstName.Text
            if (self.textFirstName.Text != None):
                ui.LName = self.textLastName.Text
            if (self.textFirstName.Text != None):
                ui.EMail = self.textEMail.Text
            if (self.textFirstName.Text != None):
                ui.Phone = self.textPhone.Text
            if (self.textFirstName.Text != None):
                ui.Address = self.textAddress.Text
            if (self.textFirstName.Text != None):
                ui.PCode = self.textPostcode.Text
            if (self.textFirstName.Text != None):
                ui.City = self.textCity.Text
            if (self.textFirstName.Text != None):
                ui.State = self.textState.Text
            if (self.textFirstName.Text != None):
                ui.Name = self.textName.Text
            if (self.textFirstName.Text != None):
                ui.Password = self.textPassword.Text

            return ui
        except:
            return None