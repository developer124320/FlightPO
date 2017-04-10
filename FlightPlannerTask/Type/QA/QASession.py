
from QARecord import QARecord
from FlightPlanner.types import QARecordType, QASessionType
from FlightPlanner.Captions import Captions
from Type.String import String, StringBuilder
from Type.Extensions import Extensions
from PyQt4.QtCore import QDateTime, QDate, QTime

class QASession(QARecord):
    def __init__(self):
        QARecord.__init__()
        self.Type = QARecordType.Session
        
        self.NULLDATE = QDateTime(QDate(2222, 2, 22), QTime(22, 22, 22, 22));
        self.dwgCreated = QDateTime();
        self.dwgSaved = QDateTime()
        self.dwgFileName = None
        self.dwgSizeOpened = 0
        self.dwgSizeClosed = 0
        self.tagName = None
        self.tagProject = None
        self.tagReason = None
        self.tagSection = None
        self.sessionType = None
        self.qaLastSaved = QDateTime()
        self.closed = QDateTime()
        self.correlation = None
        self.corrupted = None
    def method_6(self, stringBuilder_0, string_0, bool_0, bool_1):
        if (bool_0):
            QARecord.smethod_0(self.title, stringBuilder_0);
        self.HtmlBody(stringBuilder_0, string_0);

        if (bool_1):
            QARecord.smethod_1(stringBuilder_0);

    def method_9(self, stringBuilder_0, string_0):
        if (not String.IsNullOrEmpty(string_0)):
            stringBuilder_0.Append("\n{0}\n\n".format(string_0));
        stringBuilder_0.AppendLine(self.Text);

    def method_10(self, object_0, object_1, string_0):
        self.WordDocumentBody(object_0, object_1, string_0);
        QARecord.method_10(object_0, object_1, string_0)

    def method_12(self, string_0, string_1):
        return "<tr><td><b>{0}</b></td><td>{1}</td></tr>".format(string_0, string_1);

    def method_13(self, string_0, string_1, string_2):
        if (String.IsNullOrEmpty(string_2)):
            return self.method_12(string_0, string_1);
        return "<tr><td {0}><b>{1}</b></td><td {2}>{3}</td></tr>".format(string_2, string_0, string_2, string_1);

    def method_14(self, binaryReader_0, qafileVersion_0):
        #TODO: UnCompleted
        pass
        # switch (qafileVersion_0)
        # {
        #     case QAFileVersion.V8:
        #     case QAFileVersion.V8_1:
        #     {
        #         base.Stamp = DateTime.FromOADate(binaryReader_0.ReadDouble());
        #         this.dwgCreated = DateTime.FromOADate(binaryReader_0.ReadDouble());
        #         this.dwgSaved = DateTime.FromOADate(binaryReader_0.ReadDouble());
        #         this.dwgFileName = Encoding.Default.GetString(binaryReader_0.ReadBytes(binaryReader_0.ReadInt32()));
        #         this.dwgSizeOpened = binaryReader_0.ReadDouble();
        #         this.dwgSizeClosed = binaryReader_0.ReadDouble();
        #         this.tagName = Encoding.Default.GetString(binaryReader_0.ReadBytes(binaryReader_0.ReadInt32()));
        #         this.tagProject = Encoding.Default.GetString(binaryReader_0.ReadBytes(binaryReader_0.ReadInt32()));
        #         this.tagReason = Encoding.Default.GetString(binaryReader_0.ReadBytes(binaryReader_0.ReadInt32()));
        #         this.tagSection = Encoding.Default.GetString(binaryReader_0.ReadBytes(binaryReader_0.ReadInt32()));
        #         this.sessionType = (QASessionType)binaryReader_0.ReadByte();
        #         this.qaLastSaved = DateTime.FromOADate(binaryReader_0.ReadDouble());
        #         this.closed = DateTime.FromOADate(binaryReader_0.ReadDouble());
        #         this.correlation = binaryReader_0.ReadBoolean();
        #         break;
        #     }
        #     case QAFileVersion.V10:
        #     {
        #         base.Stamp = DateTime.FromBinary(binaryReader_0.ReadInt64());
        #         this.dwgCreated = DateTime.FromBinary(binaryReader_0.ReadInt64());
        #         this.dwgSaved = DateTime.FromBinary(binaryReader_0.ReadInt64());
        #         this.dwgFileName = Encoding.Unicode.GetString(binaryReader_0.ReadBytes(binaryReader_0.ReadInt32()));
        #         this.dwgSizeOpened = binaryReader_0.ReadDouble();
        #         this.dwgSizeClosed = binaryReader_0.ReadDouble();
        #         this.tagName = Encoding.Unicode.GetString(binaryReader_0.ReadBytes(binaryReader_0.ReadInt32()));
        #         this.tagProject = Encoding.Unicode.GetString(binaryReader_0.ReadBytes(binaryReader_0.ReadInt32()));
        #         this.tagReason = Encoding.Unicode.GetString(binaryReader_0.ReadBytes(binaryReader_0.ReadInt32()));
        #         this.tagSection = Encoding.Unicode.GetString(binaryReader_0.ReadBytes(binaryReader_0.ReadInt32()));
        #         this.sessionType = (QASessionType)binaryReader_0.ReadByte();
        #         this.qaLastSaved = DateTime.FromBinary(binaryReader_0.ReadInt64());
        #         this.closed = DateTime.FromBinary(binaryReader_0.ReadInt64());
        #         this.correlation = binaryReader_0.ReadBoolean();
        #         break;
        #     }
        #     default:
        #     {
        #         throw new NotSupportedException();
        #     }
        # }
        # if (QADocument.ProgressUpdate != null)
        # {
        #     QADocument.ProgressUpdate((int)(binaryReader_0.BaseStream.Position * (long)100 / binaryReader_0.BaseStream.Length));
        # }
        # int num = binaryReader_0.ReadInt32();
        # for (int i = 0; i < num; i++)
        # {
        #     base.Children.Add(QARecord.smethod_2(binaryReader_0, qafileVersion_0));
        # }

    def WordDocumentBody(self, wordApp, wordDoc, title):
        raise SystemError

    def HtmlBody(self, lines, title):
        lines.AppendLine("<div align=\"center\">");
        lines.AppendLine("<table border=\"0\" cellpadding=\"2\" cellspacing=\"0\">");
        lines.AppendLine("<tbody>");
        if (self.sessionType == QASessionType.Started):
            lines.AppendLine(self.method_12(Captions.PROJECT, self.tagProject));
        lines.AppendLine(self.method_12(Captions.NAME, self.tagName));
        lines.AppendLine(self.method_12(Captions.SECTION, self.tagSection));
        lines.AppendLine(self.method_12(Captions.REASON, self.tagReason));
        lines.AppendLine(self.method_12(Captions.DWG_NAME, self.dwgFileName));
        if (not self.dwgCreated.toString() == self.NULLDATE.toString()):
            lines.AppendLine(self.method_12(Captions.DWG_CREATED, Extensions.smethod_19(self.dwgCreated)));
        if (not self.dwgSaved.toString() == self.NULLDATE.toString()):
            lines.AppendLine(self.method_12(Captions.DWG_LAST_SAVED, Extensions.smethod_19(self.dwgSaved)));
        if (self.dwgSizeOpened > 0):
            if (self.dwgSizeOpened >= 1024):
                lines.AppendLine(self.method_12(Captions.DWG_SIZE_SESSION_OPENED, "{0:0.###} {1}".format(self.dwgSizeOpened / float(1024), Captions.MB)));
            else:
                lines.AppendLine(self.method_12(Captions.DWG_SIZE_SESSION_OPENED, "{0:0.###} {1}".format(self.dwgSizeOpened, Captions.KB)));
        if (self.dwgSizeClosed > 0):
            if (self.dwgSizeClosed >= 1024):
                lines.AppendLine(self.method_12(Captions.DWG_SIZE_SESSION_SAVED, "{0:0.###} {1}".format(self.dwgSizeClosed / float(1024), Captions.MB)));
            else:
                lines.AppendLine(self.method_12(Captions.DWG_SIZE_SESSION_SAVED, "{0:0.###} {1}".format(self.dwgSizeClosed, Captions.KB)));
        if (not self.qaLastSaved.toString() == self.NULLDATE.toString()):
            lines.AppendLine(self.method_12(Captions.QA_LAST_SAVED, Extensions.smethod_19(self.qaLastSaved)));
        if (not self.correlation):
            lines.AppendLine(self.method_13(Captions.WARNING, Captions.NO_CORRELATION, "style=\"color: rgb(255, 0, 0);\""));
        if (self.corrupted):
            lines.AppendLine(self.method_13(Captions.WARNING, Captions.POSSIBLE_QA_FILE_CORRUPTION, "style=\"color: rgb(255, 0, 0);\""));
        lines.AppendLine("</tbody>");
        lines.AppendLine("</table>");
        lines.AppendLine("</div>");
    
    def getClosed(self):
        return self.closed
    def setClosed(self, val):
        self.closed = val
    Closed = property(getClosed, setClosed, None, None)

    def getCorrelation(self):
        return self.correlation
    def setCorrelation(self, val):
        self.correlation = val
    Correlation = property(getCorrelation, setCorrelation, None, None)

    def getCorrupted(self):
        return self.corrupted
    def setCorrupted(self, val):
        self.corrupted = val
    Corrupted = property(getCorrupted, setCorrupted, None, None)

    def getDwgCreated(self):
        return self.dwgCreated
    def setDwgCreated(self, val):
        self.dwgCreated = val
    DwgCreated = property(getDwgCreated, setDwgCreated, None, None)

    def getDwgFileName(self):
        return self.dwgFileName
    def setDwgFileName(self, val):
        self.dwgFileName = val
    DwgFileName = property(getDwgFileName, setDwgFileName, None, None)

    def getDwgSaved(self):
        return self.dwgSaved
    def setDwgSaved(self, val):
        self.dwgSaved = val
    DwgSaved = property(getDwgSaved, setDwgSaved, None, None)

    def getDwgSizeClosed(self):
        return self.dwgSizeClosed
    def setDwgSizeClosed(self, val):
        self.dwgSizeClosed = val
    DwgSizeClosed = property(getDwgSizeClosed, setDwgSizeClosed, None, None)

    def getDwgSizeOpened(self):
        return self.dwgSizeOpened
    def setDwgSizeOpened(self, val):
        self.dwgSizeOpened = val
    DwgSizeOpened = property(getDwgSizeOpened, setDwgSizeOpened, None, None)

    def getQaLastSaved(self):
        return self.qaLastSaved
    def setQaLastSaved(self, val):
        self.qaLastSaved = val
    QaLastSaved = property(getQaLastSaved, setQaLastSaved, None, None)

    def getSessionType(self):
        return self.sessionType
    def setSessionType(self, val):
        self.sessionType = val
    SessionType = property(getSessionType, setSessionType, None, None)

    def getTagName(self):
        return self.tagName
    def setTagName(self, val):
        self.tagName = val
    TagName = property(getTagName, setTagName, None, None)

    def getTagProject(self):
        return self.tagProject
    def setTagProject(self, val):
        self.tagProject = val
    TagProject = property(getTagProject, setTagProject, None, None)

    def getTagReason(self):
        return self.tagReason
    def setTagReason(self, val):
        self.tagReason = val
    TagReason = property(getTagReason, setTagReason, None, None)

    def getTagSection(self):
        return self.tagSection
    def setTagSection(self, val):
        self.tagSection = val
    TagSection = property(getTagSection, setTagSection, None, None)

    def getText(self):
        stringBuilder = StringBuilder();
        if (self.sessionType == QASessionType.Started):
            stringBuilder.AppendLine("{0}\t{1}".format(Captions.PROJECT, self.tagProject));
        stringBuilder.AppendLine("{0}\t{1}".format(Captions.NAME, self.tagName));
        stringBuilder.AppendLine("{0}\t{1}".format(Captions.SECTION, self.tagSection));
        stringBuilder.AppendLine("{0}\t{1}".format(Captions.REASON, self.tagReason));
        stringBuilder.AppendLine("{0}\t{1}".format(Captions.DWG_NAME, self.dwgFileName));
        if (not self.dwgCreated.toString() == self.NULLDATE.toString()):
            stringBuilder.AppendLine("{0}\t{1}".format(Captions.DWG_CREATED, Extensions.smethod_19(self.dwgCreated)));
        if (not self.dwgSaved.toString() == self.NULLDATE.toString()):
            stringBuilder.AppendLine("{0}\t{1}".format(Captions.DWG_LAST_SAVED, Extensions.smethod_19(self.dwgSaved)));
        if (self.dwgSizeOpened > 0):
            if (self.dwgSizeOpened >= 1024):
                stringBuilder.AppendLine("{0}\t{1}".format(Captions.DWG_SIZE_SESSION_OPENED, "{0:0.###} {1}".format(self.dwgSizeOpened / float(1024), Captions.MB)));
            else:
                stringBuilder.AppendLine("{0}\t{1}".format(Captions.DWG_SIZE_SESSION_OPENED, "{0:0.###} {1}".format(self.dwgSizeOpened, Captions.KB)));
        if (self.dwgSizeClosed > 0):
            if (self.dwgSizeClosed >= 1024):
                stringBuilder.AppendLine("{0}\t{1}".format(Captions.DWG_SIZE_SESSION_SAVED, "{0:0.###} {1}".format(self.dwgSizeClosed / float(1024), Captions.MB)));
            else:
                stringBuilder.AppendLine("{0}\t{1}".format(Captions.DWG_SIZE_SESSION_SAVED, "{0:0.###} {1}".format(self.dwgSizeClosed, Captions.KB)));
        if (not self.qaLastSaved.toString() == self.NULLDATE.toString()):
            stringBuilder.AppendLine("{0}\t{1}".format(Captions.QA_LAST_SAVED, Extensions.smethod_19(self.qaLastSaved)));
        if (not self.correlation):
            stringBuilder.AppendLine("{0}\t{1}".format(Captions.WARNING, Captions.NO_CORRELATION));
        if (self.corrupted):
            stringBuilder.AppendLine("{0}\t{1}".format(Captions.WARNING, Captions.POSSIBLE_QA_FILE_CORRUPTION));
        return stringBuilder.ToString();
    def setText(self, val):
        raise SystemError
    Text = property(getText, None, None, None)


