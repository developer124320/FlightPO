
from PyQt4.QtCore import QFileInfo
class FileHelper:
    @staticmethod
    def smethod_3(string_0):
        fileInfo = QFileInfo(string_0);
        return round(float(fileInfo.size()) / float(1024), 3);