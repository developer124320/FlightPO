
from PyQt4.QtGui import QMessageBox
from ProjectManager.ProjectInfo import ProjectList, ProjectInfo
from ProjectManager.UserList import UserList
from ProjectManager.MYUSERINFO import MYUSERINFO

class AirCraftOperation:
#region global members
        # //////////////////////////////////////////////////////////////////////////
        # // global members for management user and project.

    g_userList = None
    g_loginedUser = None
    g_projectList = None

    g_currentProject = None
    g_currentSubproject = None
    g_currentWorkspace = None
    g_currentProcedure = None
    g_currentAIP = None

    g_stateList = None
    g_aeroList = None
    g_runwayList = None
    g_AppSetting = None

    g_geoForms = []
    g_proForms = []

    g_snapping = True

    def __init__(self):
        pass
    def ResetProject(self):
        AirCraftOperation.g_loginedUser = None
        AirCraftOperation.g_currentProcedure = None
        AirCraftOperation.g_currentProject = None
        AirCraftOperation.g_currentSubproject = None
        AirCraftOperation.g_currentWorkspace = None
        AirCraftOperation.g_userList.ListUserInfo = []
        AirCraftOperation.g_projectList.ProjectsList = []

        if(AirCraftOperation.g_userList.ReadUserInfoFile()):
            if (len(AirCraftOperation.g_userList.ListUserInfo) > 0):
                # LoginForm loginForm = new LoginForm()
                # if (loginForm.ShowDialog() != DialogResult.OK)
                # {
                #     return
                # }

                AirCraftOperation.g_projectList = ProjectList()
                AirCraftOperation.g_projectList.SetProjectInfoPath(AirCraftOperation.g_AppSetting.ProjectFolderPath)
                if (not AirCraftOperation.g_projectList.ReadProjectInfoXml()):
                    QMessageBox.warning(None, "Warning", "Project information file is not exist! Please create project.")
                # AirCraftOperation.g_stateList = StateList()
                # AirCraftOperation.g_stateList.ReadStateInfoXml(AirCraftOperation.g_AppSetting.ProjectFolderPath + AirCraftOperation.g_AppSetting.StateInfoFile)
                #
                # AirCraftOperation.g_aeroList = AerodromeList()
                # AirCraftOperation.g_aeroList.ReadAerodromeInfoXml(AirCraftOperation.g_AppSetting.ProjectFolderPath + AirCraftOperation.g_AppSetting.AeroInfoFile)

            else:
                QMessageBox.warning(None, "Warning", "User information file dose not contain any user!")

