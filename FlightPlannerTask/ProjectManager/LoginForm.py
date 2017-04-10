


from PyQt4.QtGui import QDialog, QPushButton, QVBoxLayout, QFont, QSpacerItem, QSizePolicy, QMessageBox
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.Frame import Frame
from AircraftOperation import AirCraftOperation

class LoginForm(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self)

        self.parentDlg = parent
        self.setObjectName(("ui_ProjectMngForm"))
        self.resize(100, 100)
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)
        self.setWindowTitle("User Login")

        self.vlForm = QVBoxLayout(self)
        self.vlForm.setObjectName(("vl_ProjectMngForm"))
        self.vlForm.setSpacing(9)
        self.vlForm.setMargin(9)

        self.basicFrame = Frame(self)
        self.vlForm.addWidget(self.basicFrame)

        self.textNameLogin = TextBoxPanel(self.basicFrame)
        self.textNameLogin.LabelWidth = 70
        self.textNameLogin.Width = 120
        self.textNameLogin.Caption = "User Name"
        self.basicFrame.Add = self.textNameLogin

        self.textPasswordLogin = TextBoxPanel(self.basicFrame)
        self.textPasswordLogin.LabelWidth = 70
        self.textPasswordLogin.Width = 120
        self.textPasswordLogin.Caption = "Password"
        self.textPasswordLogin.EchoMode = "Password"
        self.basicFrame.Add = self.textPasswordLogin

        self.btnFrame = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.btnFrame

        horizontalSpacer = QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.btnFrame.layoutBoxPanel.addItem(horizontalSpacer)

        self.buttonLogin = QPushButton(self.btnFrame)
        self.buttonLogin.setObjectName("buttonLogin")
        self.buttonLogin.setText("Login")
        self.btnFrame.Add = self.buttonLogin

        horizontalSpacer1 = QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.btnFrame.layoutBoxPanel.addItem(horizontalSpacer1)

        # self.connect(self.listBoxProject, SIGNAL("Event_0"), self.listBoxProject_SelectedIndexChanged)
        # self.connect(self.textPathProject, SIGNAL("Event_1"), self.buttonBrowseProject_Click)

        self.buttonLogin.clicked.connect(self.buttonLogin_Click)
    
    def buttonLogin_Click(self):
        try:
            if (self.textNameLogin.Value == ""):
                QMessageBox.warning(self, "Warning", "Please, input your user name.")
            else:
                ui = AirCraftOperation.g_userList.FindUser(self.textNameLogin.Value)
                if (ui != None):
                    if (ui.Password != None):
                        if (ui.Password == self.textPasswordLogin.Value):
                            AirCraftOperation.g_loginedUser = ui
                            self.accept()
                        else:
                            QMessageBox.warning(self, "Warning", "Your password is incorrect! Please retry.")
                    elif (self.textPasswordLogin.Value == ""):
                        AirCraftOperation.g_loginedUser = ui
                        self.accept()
                    else:
                        QMessageBox.warning(self, "Warning", "Your password is incorrect! Please retry.")
                else:
                    if (AirCraftOperation.g_userList.m_IV == self.textPasswordLogin.Value) and (AirCraftOperation.g_userList.m_Key == self.textNameLogin.Value):
                        self.parentDlg.procedureMenuUserManagementAction.setEnabled(True)
                        self.reject()
                    else:
                        QMessageBox.warning(self, "Warning", "Your password is incorrect! Please retry.")
                    # QMessageBox.warning(self, "Warning", "The name you filled is not exist! Please retry.")
        except:
            self.result()