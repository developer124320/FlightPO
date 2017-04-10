
from PyQt4.QtCore import QString, QFileInfo, QFile
from String import String

class Path:
    @staticmethod
    def ChangeExtension(oldFileName, extentionStr = ".txt"):
        oldFileName = String.Str2QString(oldFileName)
        index = oldFileName.indexOf('.')
        if index == -1:
            return None
        newFileName = oldFileName.left(index) + extentionStr
        return newFileName

    @staticmethod
    def GetFileNameWithoutExtension(fileName):
        oldFileName = String.Str2QString(fileName)
        index = oldFileName.indexOf('.')
        if index == -1:
            return fileName
        return oldFileName.left(index)
