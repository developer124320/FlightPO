
from PyQt4.QtCore import QDateTime
from FlightPlanner.types import QAColorCode

class QAReportEntry:
    def __init__(self):
        self.title = "Folder";
        self.stamp = QDateTime.currentDateTime();
        self.value = None;
        self.colorCode = QAColorCode.Nothing;
        self.children = [];

    def getChildren(self):
        return self.children
    Children = property(getChildren, None, None, None)

    def getColorCode(self):
        return self.colorCode
    def setColorCode(self, val):
        self.colorCode = val
    ColorCode = property(getColorCode, setColorCode, None, None)

    def getStamp(self):
        if (self.value == None):
            return self.stamp;
        return self.value.Stamp;
    Stamp = property(getStamp, None, None, None)

    def getTitle(self):
        if (self.value == None):
            return self.title;
        return self.value.ReportTitle;
    def setTitle(self, val):
        if (self.value == None):
            self.title = val;
            return;
        self.value.ReportTitle = val;
    Title = property(getTitle, setTitle, None, None)

    def getValue(self):
        return self.value
    def setValue(self, val):
        self.value = val
    Value = property(getValue, setValue, None, None)
    
    def method_0(self, binaryReader_0, qafileVersion_0):
        num = binaryReader_0.ReadInt32();
        self.title = GZipStream.UncompressString(binaryReader_0.ReadBytes(num));
        self.stamp = QDateTime.fromMSecsSinceEpoch(binaryReader_0.ReadInt64());
        self.colorCode = binaryReader_0.ReadInt32();
        num1 = binaryReader_0.ReadInt32();
        for i in range(num1):
            qAReportEntry = QAReportEntry();
            qAReportEntry.method_0(binaryReader_0, qafileVersion_0);
            self.children.append(qAReportEntry);
    def method_1(self, binaryWriter_0, qafileVersion_0):
        numArray = GZipStream.CompressString(self.Title);
        binaryWriter_0.Write(int(numArray.Length));
        binaryWriter_0.Write(numArray);
        binaryWriter_0.Write(self.Stamp.toMSecsSinceEpoch());
        binaryWriter_0.Write(int(self.colorCode));
        binaryWriter_0.Write(self.children.__len__());
        for child in self.children:
            child.method_1(binaryWriter_0, qafileVersion_0);
