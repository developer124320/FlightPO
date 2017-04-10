
from PyQt4.QtCore import QDateTime, Qt
from PyQt4.QtGui import QApplication
from FlightPlanner.types import QARecordType, QAFileVersion
from Type.String import String, StringBuilder
# from QADocument import QADocument
from Type.switch import switch

class QARecord:
    def __init__(self, childName = None):
        self.childName = childName
        self.children = []
        self.title = None;
        self.reportTitle = None;
        self.stamp = QDateTime.currentDateTime();
        self.colorCode = None;
        self.Type = None
    def HtmlBody(self, lines, title):
        pass
    def WordDocumentBody(self, wordApp, wordDoc, title):
        pass
    def LoadData(self, reader, version):
        # reader = open("")
        for case in switch (version):
            if case(QAFileVersion.V8) or case(QAFileVersion.V8_1):
                self.stamp = QDateTime.fromString(reader.readline());
                self.title = reader.readline();
                break;
            elif case(QAFileVersion.V10):
                self.stamp = QDateTime.fromString(reader.readline());
                self.title = reader.readline();
                break;
            else:
                raise SystemError;
        #TODO: UnCompleted
        # if (QADocument.ProgressUpdate != None):
        #     QADocument.ProgressUpdate(int(reader.BaseStream.Position * 100 / reader.BaseStream.Length));
    def method_0(self, memoryStream_0, byte_0, bool_0):
        if (not bool_0):
            pass
            # byte_0 = Encoding.Convert(Encoding.Default, Encoding.Unicode, byte_0);

        memoryStream_0.SetLength(int(len(byte_0)));
        # memoryStream_0.Seek(0, SeekOrigin.Begin);
        memoryStream_0.Write(byte_0, 0, int(len(byte_0)));

    def method_1(self, memoryStream_0, bool_0):
        if (bool_0):
            return memoryStream_0.ToArray();
        return memoryStream_0.ToArray();
        # return Encoding.Convert(Encoding.Unicode, Encoding.Default, memoryStream_0.ToArray());
    def method_2(self , memoryStream_0):
        if (memoryStream_0 == None):
            return None;
        return memoryStream_0.ToArray()
        # return Encoding.Unicode.GetString(memoryStream_0.ToArray());
    def method_3(self, memoryStream_0, string_0):
        if (memoryStream_0 != None):
            bytes = string_0#Encoding.Unicode.GetBytes(string_0);
            memoryStream_0.SetLength(int(len(bytes)));
            # memoryStream_0.Seek(0, SeekOrigin.Begin);
            memoryStream_0.Write(bytes, 0, len(bytes));
    def method_4(self, binaryWriter_0, qafileVersion_0):
        binaryWriter_0.write(self.Type);
        self.SaveData(binaryWriter_0, qafileVersion_0);
        binaryWriter_0.write(str(len(self.children)));
        for child in self.children:
            child.method_4(binaryWriter_0, qafileVersion_0);
    def method_5(self):
        stringBuilder = StringBuilder();
        self.method_6(stringBuilder, None, True, True);
        return stringBuilder.ToString();
    def method_6(self, stringBuilder_0, string_0, bool_0, bool_1):
        pass
    def method_7(self):
        #TODO: UnCompleted
        # rtfDocument = new RtfDocument(PaperSize.A4, PaperOrientation.Portrait, Lcid.English);
        # this.method_8(rtfDocument, null);
        # return rtfDocument.rtf;
        return ""
    def method_8(self, rtfDocument_0, string_0):
        #TODO: UnCompleted
        return ""
    def method_9(self, stringBuilder_0, string_0):
        if (not String.IsNullOrEmpty(string_0)):
            stringBuilder_0.Append("\n{0}\n\n".format(string_0));
        stringBuilder_0.AppendLine(self.Text);

        for child in self.children:
            string0 = string_0;
            if (not String.IsNullOrEmpty(child.Heading)):
                string0 = "{0} - {1}".format(string0, child.title) if(not String.IsNullOrEmpty(string0)) else child.title;
            child.method_9(stringBuilder_0, string0);
    def method_10(self, object_0, object_1, string_0):
        # self.WordDocumentBody(object_0, object_1, string_0);
        for child in self.children:
            string0 = string_0;
            if (not String.IsNullOrEmpty(child.Heading)):
                string0 = "{0} - {1}".format(string0, child.title) if(not String.IsNullOrEmpty(string0)) else child.title
            child.method_10(object_0, object_1, string0);
    def method_11(self):
        clipboard = QApplication.clipboard()
        clipboard.clear()
        # if (self.childName == "QASnapshot"):
        #     clipboard.setImage(self.Image);
        #     return;
        # dataObject = DataObject();
        dataObject = ""
        stringBuilder = StringBuilder();
        stringBuilder.Append("Version:0.9\r\n");
        stringBuilder.Append("StartHTML:aaaaaaaaaa\r\n");
        stringBuilder.Append("EndHTML:bbbbbbbbbb\r\n");
        stringBuilder.Append("StartFragment:cccccccccc\r\n");
        stringBuilder.Append("EndFragment:dddddddddd\r\n");
        length = stringBuilder.Length;
        num = stringBuilder.Length;
        stringBuilder.Append("<!--StartFragment-->\r\n");
        stringBuilder.Append(self.method_5());
        stringBuilder.Append("<!--EndFragment-->\r\n");
        length1 = stringBuilder.Length;
        num1 = stringBuilder.Length;
        stringBuilder.Replace("aaaaaaaaaa", String.Number2String(length, "0000000000"), 0, length);
        stringBuilder.Replace("bbbbbbbbbb", String.Number2String(num1, "0000000000"), 0, length);
        stringBuilder.Replace("cccccccccc", String.Number2String(num, "0000000000"), 0, length);
        stringBuilder.Replace("dddddddddd", String.Number2String(length1, "0000000000"), 0, length);
        dataObject += stringBuilder.ToString() + "\n"
        dataObject += self.ToString() + "\n"
        # dataObject.SetData(DataFormats.Html, stringBuilder.ToString());
        # dataObject.SetData(DataFormats.UnicodeText, this.ToString());
        clipboard.setText(dataObject);
    def SaveData(self, writer, version):
        for case in switch (version):
            if case(QAFileVersion.V8) or case(QAFileVersion.V8_1):
                writer.write(self.stamp.toString(Qt.TextDate));
                writer.write(len(self.title));
                writer.Write(self.title);
                return;
            elif case(QAFileVersion.V10):
                writer.write(self.stamp.toString(Qt.TextDate));
                writer.write(len(self.title));
                writer.write(self.title);
                return;
            else:
                raise SystemError
    def getChildren(self):
        return self.children
    Children = property(getChildren, None, None, None)

    def getColorCode(self):
        return self.colorCode
    def setColorCode(self, val):
        self.colorCode = val
    ColorCode = property(getColorCode, setColorCode, None, None)

    def getHeading(self):
        return self.title
    def setHeading(self, val):
        self.title = val
        self.reportTitle = None
    Heading = property(getHeading, setHeading, None, None)

    def getReportTitle(self):
        if (not String.IsNullOrEmpty(self.reportTitle)):
            return self.reportTitle;
        return self.title;
    def setReportTitle(self, val):
        if (val == self.title):
            self.reportTitle = None;
            return;
        self.reportTitle = val;
    ReportTitle = property(getReportTitle, setReportTitle, None, None)

    def getStamp(self):
        return self.stamp
    def setStamp(self, val):
        self.stamp = val
    Stamp = property(getStamp, setStamp, None, None)

    def ToString(self):
        stringBuilder = StringBuilder();
        self.method_9(stringBuilder, None);
        return stringBuilder.ToString();

    @staticmethod
    def smethod_0(string_0, stringBuilder_0):
        stringBuilder_0.AppendLine("<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\">");
        stringBuilder_0.AppendLine("<html>");
        stringBuilder_0.AppendLine("<head>");
        stringBuilder_0.AppendLine(String.Concat(["<title>", string_0, "</title>"]));
        stringBuilder_0.AppendLine("<style type=\"text/css\">");
        stringBuilder_0.AppendLine("body { font:12px tahoma,12px helvetica,12px arial,12px verdana; font:size: 100%; }");
        stringBuilder_0.AppendLine("table { font:12px tahoma,12px helvetica,12px arial,12px verdana; font:size: 100%; border-collapse: collapse; }");
        stringBuilder_0.AppendLine("th { border: 1px solid black; text-align: center; vertical-align: middle; }");
        stringBuilder_0.AppendLine("td { border: 1px solid black; text-align: left; vertical-align: middle; }");
        stringBuilder_0.AppendLine("tr { border: 1px solid black; text-align: left; vertical-align: middle; }");
        stringBuilder_0.AppendLine("</style>");
        stringBuilder_0.AppendLine("</head>");
        stringBuilder_0.AppendLine("<body>");
    @staticmethod
    def smethod_1(stringBuilder_0):
        stringBuilder_0.AppendLine("</body>");
        stringBuilder_0.AppendLine("</html>");