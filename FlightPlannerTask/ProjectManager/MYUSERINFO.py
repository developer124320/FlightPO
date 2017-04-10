
from PyQt4.QtCore import QString

class enumUserRight:
    ur_None = 0
    ur_Admin = 1
    ur_SuperUser = 2
    ur_ReadWrite = 3
    ur_ReadOnly = 4

class MYUSERINFO:
    def __init__(self):
        self.Name = ""
        self.Password = ""
        self.FName = ""
        self.LName = ""
        self.EMail = ""
        self.Phone = ""
        self.PCode = ""
        self.City = ""
        self.State = ""
        self.Address = ""

        self.Right = 0
    def writeData(self, dataStream):
        dataStream.writeQString(QString(self.Name))
        dataStream.writeQString(QString(self.Password))
        dataStream.writeQString(QString(self.FName))
        dataStream.writeQString(QString(self.LName))
        dataStream.writeQString(QString(self.EMail))
        dataStream.writeQString(QString(self.Phone))
        dataStream.writeQString(QString(self.PCode))
        dataStream.writeQString(QString(self.City))
        dataStream.writeQString(QString(self.State))
        dataStream.writeQString(QString(self.Address))
        dataStream.writeInt(self.Right)
    def readData(self, dataStream):
        self.Name = dataStream.readQString()
        self.Password = dataStream.readQString()
        self.FName = dataStream.readQString()
        self.LName = dataStream.readQString()
        self.EMail = dataStream.readQString()
        self.Phone = dataStream.readQString()
        self.PCode = dataStream.readQString()
        self.City = dataStream.readQString()
        self.State = dataStream.readQString()
        self.Address = dataStream.readQString()
        self.Right = dataStream.readInt()
    def equal(self, other):
        try:
            if (self.Name == other.Name) or self.EMail == other.EMail:
                return True
            return False
        except:
            # MessageBox.Show(ex.Message);
            return False
