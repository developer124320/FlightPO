
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QFile, QIODevice, QDataStream, QString
from ProjectManager.MYUSERINFO import MYUSERINFO
import os

class UserList:
    # des = DESCryptoServiceProvider()
    def __init__(self, strPath = None):
        self.currentDir = os.getcwdu()
        self.USERINFO_FILENAME = "\\user.coc"
        if strPath == None:
            self.ListUserInfo = []
            self.m_strUserInfoFullName = self.currentDir + self.USERINFO_FILENAME
        else:
            self.ListUserInfo = []
            self.m_strUserInfoFullName = strPath + self.USERINFO_FILENAME
        self.m_Key = "user320"
        self.m_IV = "1985120"
        # self.m_strUserInfoFullName = None



    # def get_ListUserInfo(self):
    #     return self.ListUserInfo
    # def set_ListUserInfo(self, value):
    #     self.ListUserInfo = value
    # ListUserInfo = property(get_ListUserInfo, set_ListUserInfo, None, None)

    def SetUserInfoPath(self, val):
        self.m_strUserInfoFullName = val + self.USERINFO_FILENAME
        self.currentDir = val + self.USERINFO_FILENAME

    def FindUser(self, userInfo):
        if isinstance(userInfo, MYUSERINFO):
            for myUserInfo in self.ListUserInfo:
                if (myUserInfo.equal(userInfo)):
                    return self.ListUserInfo.index(myUserInfo)
            return -1
        else:
            for ui in self.ListUserInfo:
                if (ui.Name == userInfo):
                    return ui
            return None

    def AddUser(self, userInfo):
        if (self.FindUser(userInfo) > -1):
            QMessageBox.warning(None, "Warning", "User already exist!")
            return False
        self.ListUserInfo.append(userInfo)
        return True

    def DeleteUser(self, userinfo):
        if isinstance(userinfo, MYUSERINFO):
            nUserID = self.FindUser(userinfo)
            if (nUserID < 0):
                QMessageBox.warning(None, "Error", "Unable to delete user info.")
                return
            self.ListUserInfo.pop(nUserID)
        else:
            try:
                nIndex = self.FindUserID(userinfo)
                if (nIndex > -1):
                    self.ListUserInfo.pop(nIndex)
            except:
                pass
    def FindUserID(self, p):
        for ui in self.ListUserInfo:
            if (ui.Name == p):
                return self.ListUserInfo.index(ui)
        return -1

    def ReadUserInfoFile(self):
        try:
            if not QFile.exists(self.m_strUserInfoFullName):
                return
            file0 = QFile(self.m_strUserInfoFullName)
            file0.open(QIODevice.ReadOnly)
            dataStream = QDataStream(file0)
            str0 = dataStream.readQString()
            self.m_strUserInfoFullName = dataStream.readQString()
            self.m_Key = dataStream.readQString()
            self.m_IV = dataStream.readQString()
            userInfoCount = dataStream.readInt()
            for i in range(userInfoCount):
                userInfo = MYUSERINFO()
                userInfo.readData(dataStream)
                self.ListUserInfo.append(userInfo)

            file0.close()
            return True
        except:
            return False
    def WriteUserInfoFile(self):
        if QFile.exists(self.m_strUserInfoFullName):
            fl = QFile.remove(self.m_strUserInfoFullName)
            f = open(self.m_strUserInfoFullName, 'w')
            f.flush()
            f.close()

        else:
            f = open(self.m_strUserInfoFullName, 'w')
            # f = open("D:/xml/phxasar.txt")
            f.flush()
            f.close()

        file0 = QFile(self.m_strUserInfoFullName)
        file0.open(QIODevice.WriteOnly)
        dataStream = QDataStream(file0)
        dataStream.writeQString(QString("UserList"))
        dataStream.writeQString(QString(self.m_strUserInfoFullName))
        dataStream.writeQString(QString(self.m_Key))
        dataStream.writeQString(QString(self.m_IV))
        dataStream.writeInt(len(self.ListUserInfo))

        for userInfo in self.ListUserInfo:
            userInfo.writeData(dataStream)
        file0.flush()
        file0.close()
        return True
