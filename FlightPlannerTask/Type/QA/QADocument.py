
from QARecord import QARecord
from QA0 import QA0
from QASnapshot import QASnapshot
from FlightPlanner.types import QAExportType, QASessionType, QARecordType, QAFileVersion, QATableType
from FlightPlanner.Captions import Captions
from FlightPlanner.messages import Messages
from Type.String import StringBuilder, String
from Type.Extensions import Extensions
from Type.switch import switch
from Type.Path import Path
from Type.FileHelper import FileHelper
from PyQt4.QtCore import QFileInfo, QFile, QDateTime
from PyQt4.QtGui import QMessageBox
import define, sys
class QADocument:
    ProgressUpdate = None
    ProgressStop = None
    def __init__(self, string_0):
        self.fileNameQA = string_0
        self.sessions = []
        self.reportEntries = []
        self.selectedRecord = None
        self.selectedReportEntry = None
        self.fileNameDWG = Path.ChangeExtension(string_0, ".dwg")
        self.originalFileVersion = None
        self.useOriginalFileVersion = False
        self.itemsLoaded = -1
        self.noSave = False

    def method_0(self):
        count = 0
        for session in self.sessions:
            count = count + len(session.Children) + 1
        return count

    def method_2(self, iwin32Window_0):
        if (not self.useOriginalFileVersion):
            self.method_4(iwin32Window_0, self.fileNameQA, QA0.DefaultFileVersion)
            return
        self.method_4(iwin32Window_0, self.fileNameQA, self.originalFileVersion)

    def method_4(self, iwin32Window_0, string_0, qafileVersion_0):
        try:
            count = len(self.Sessions)
            if (count <= 0 or not self.sessions[count - 1].Corrupted or len(self.sessions[count - 1].Children) != 0):
                tempFileName = define.appPath + "/tempFile.txt"
                fileT = QFile(string_0)
                binaryWriter = file(tempFileName, "w")
                # using (FileStream fileStream = File.Open(tempFileName, FileMode.Create, FileAccess.write, FileShare.Read))
                # {
                #     using (BinaryWriter binaryWriter = new BinaryWriter(fileStream))
                #     {
                binaryWriter.write("PHXQAA")
                for case in switch (qafileVersion_0):
                    if case(QAFileVersion.V4) or case(QAFileVersion.V4_1):
                        if (qafileVersion_0 != QAFileVersion.V4):
                            binaryWriter.write(str(4.1))
                        else:
                            binaryWriter.write(str(4))
                        self.method_14(binaryWriter, qafileVersion_0)
                        break
                    elif case(QAFileVersion.V8) or case(QAFileVersion.V8_1):
                        if (qafileVersion_0 != QAFileVersion.V8):
                            binaryWriter.write(str(8.1))
                        else:
                            binaryWriter.write(str(8))
                        self.method_16(binaryWriter, qafileVersion_0)
                        break
                    elif case(QAFileVersion.V10):
                        binaryWriter.write(10)
                        self.method_16(binaryWriter, qafileVersion_0)
                        break
                    else:
                        QMessageBox.warning(iwin32Window_0, "Error", Messages.ERR_UNSUPPORTED_QA_FILE_VERSION)
                        raise SystemError
                if (fileT.exists()):
                    string_0 = String.Str2QString(string_0)
                    str0 = string_0.left(string_0.length() - 3) + "qab"
                    if (QFile.exists(str0)):
                        QFile.remove(str0)
                    QFile.copy(string_0, str0)
                QFile.copy(tempFileName, string_0)
        except:
            QMessageBox.warning(iwin32Window_0, "Error", Messages.ERR_FAILED_TO_SAVE_ACTIVE_QA_FILE.format(sys.exc_info()[0]))

    def method_5(self, string_0, qaexportType_0):
        resultStr = ""
        stringBuilder = StringBuilder()
        fileInfo = QFileInfo(string_0)
        QARecord.smethod_0(self.fileNameQA, stringBuilder)
        streamWriter = open(string_0, 'w')
        resultStr += stringBuilder.ToString() + "\n"
        # streamWriter.write(stringBuilder.ToString())
        directoryName = fileInfo.path()
        num = 1
        num1 = 1
        for i in range(len(self.sessions)):
            item = self.sessions[i]
            if (qaexportType_0 == QAExportType.QA):
                stringBuilder = StringBuilder()
                str0 = Extensions.smethod_19(item.Stamp)
                if (item.SessionType != QASessionType.Started):
                    stringBuilder.AppendLine("<p align=\"left\"><H2><br>{0} {1} ({2})<br></H2></p>".format(str(i + 1), Captions.QA_OPENED, str0))
                else:
                    stringBuilder.AppendLine("<p align=\"left\"><H2><br>{0} {1} ({2})<br></H2></p>".format(str(i + 1), Captions.QA_STARTED, str0))
                item.method_6(stringBuilder, None, False, False)
                resultStr += stringBuilder.ToString() + "\n"
                # streamWriter.write(stringBuilder.ToString())
            for j in range(len(item.Children)):
                qARecord = item.Children[j]
                if (qARecord.Type != QARecordType.Session):
                    stringBuilder = StringBuilder()
                    if (qaexportType_0 != QAExportType.QA):
                        stringBuilder.AppendLine("<p align=\"left\"><H2><br>{0}. {1}<br></H2></p>".format(str(num1), qARecord.Heading))
                    else:
                        longTimeString = qARecord.Stamp.ToLongTimeString()
                        heading = [i + 1, j + 1, qARecord.Heading, longTimeString]
                        stringBuilder.AppendLine("<p align=\"left\"><H3><br>{0}.{1} {2} ({3})<br></H3></p>".format(str(i + 1), str(j + 1), qARecord.Heading, longTimeString))
                    if (qARecord.Type != QARecordType.Snapshot):
                        qARecord.method_6(stringBuilder, None, False, False)
                    else:
                        qARecord._class_ = QASnapshot
                        num = qARecord.method_12(stringBuilder, qARecord, directoryName, num)
                    resultStr += stringBuilder.ToString() + "\n"
                    # streamWriter.write(stringBuilder.ToString())
                    num1 += 1
        stringBuilder = StringBuilder()
        QARecord.smethod_1(stringBuilder)
        resultStr += stringBuilder.ToString() + "\n"
        streamWriter.write(resultStr)
    
    def method_6(self, string_0, treeNodeCollection_0):
        value = None
        # using (TextWriter streamWriter = new StreamWriter(string_0, false, Encoding.Unicode))
        streamWriter = open(string_0, 'w')
        stringBuilder = StringBuilder()
        QARecord.smethod_0(self.fileNameQA, stringBuilder)
        streamWriter.write(stringBuilder.ToString())
        fileInfo = QFileInfo(string_0)
        directoryName = fileInfo.path()
        num = 1
        for treeNodeCollection0 in treeNodeCollection_0:
            tag = treeNodeCollection0.Tag# as QAReportEntry
            stringBuilder = StringBuilder()
            stringBuilder.AppendLine("<p align=\"left\"><H2><br>{0}. {1}<br></H2></p>".format(str(treeNodeCollection0.Index + 1), treeNodeCollection0.Text))
            if (tag.Value != None):
                value = tag.Value
                if (value.Type != QARecordType.Snapshot):
                    value.method_6(stringBuilder, None, False, False)
                else:
                    value._class_ = QASnapshot
                    num = value.method_12(stringBuilder, value, directoryName, num)
            else:
                for node in treeNodeCollection0.Nodes:
                    tag = node.Tag# as QAReportEntry
                    stringBuilder.AppendLine("<p align=\"left\"><H3><br>{0}.{1} {2}<br></H3></p>".format(str(treeNodeCollection0.Index + 1), str(node.Index + 1), node.Text))
                    value = tag.Value
                    if (value.Type != QARecordType.Snapshot):
                        value.method_6(stringBuilder, None, False, False)
                    else:
                        value._class_ = QASnapshot
                        num = value.method_12(stringBuilder, value, directoryName, num)
            streamWriter.write(stringBuilder.ToString())
        stringBuilder = StringBuilder()
        QARecord.smethod_1(stringBuilder)
        streamWriter.write(stringBuilder.ToString())

    def method_8(self, binaryWriter_0, string_0):
        string_0 = String.Str2QString(string_0)
        length = string_0.length();
        bytes = string_0# Encoding.Default.GetBytes(string_0);
        #TODO: UnCompleted
        # for i in range(length):
        #     num = bytes[i];
        #     if (num + 111 <= 255)
        #     {
        #         bytes[i] = (byte)(num + 111);
        #     }
        #     else
        #     {
        #         bytes[i] = (byte)(num + 111 - 255);
        #     }
        # }
        # binaryWriter_0.Write(length);
        # binaryWriter_0.Write(bytes);

    def method_10(self, binaryWriter_0, stream_0, bool_0):
        #TODO: UnCompleted
        pass
        # byte[] numArray = new byte[checked((IntPtr)stream_0.Length)];
        # stream_0.Seek((long)0, SeekOrigin.Begin);
        # if (stream_0.Read(numArray, 0, (int)numArray.Length) != (int)numArray.Length)
        # {
        #     throw new IOException(Messages.ERR_FAILED_TO_READ_QA_RECORD_STREAM);
        # }
        # numArray = Encoding.Convert(Encoding.Unicode, Encoding.Default, numArray);
        # int num = 0;
        # byte[] numArray1 = numArray;
        # for (int i = 0; i < (int)numArray1.Length; i++)
        # {
        #     if (numArray1[i] != 10 || !bool_0)
        #     {
        #         num++;
        #     }
        # }
        # binaryWriter_0.Write(num);
        # for (int j = 0; j < (int)numArray.Length; j++)
        # {
        #     byte num1 = numArray[j];
        #     if (num1 != 10 || !bool_0)
        #     {
        #         num1 = (num1 + 111 <= 255 ? (byte)(num1 + 111) : (byte)(num1 + 111 - 255));
        #         binaryWriter_0.Write(num1);
        #     }
        # }
    
    def method_14(self, binaryWriter_0, qafileVersion_0):
        if (qafileVersion_0 == QAFileVersion.V4_1):
            count = 0
            for session in self.sessions:
                count = count + len(session.Children) + 2
            binaryWriter_0.write(str(count))
        for i in range(len(self.sessions)):
            item = self.sessions[i]
            if (item.SessionType != QASessionType.Started):
                binaryWriter_0.write(str(1))
                binaryWriter_0.write(item.Stamp.toString())
                binaryWriter_0.write(item.DwgSaved.toString())
                binaryWriter_0.write(item.QaLastSaved.toString())
                binaryWriter_0.write(item.DwgSizeOpened)
                self.method_8(binaryWriter_0, item.DwgFileName)
                binaryWriter_0.write(item.Correlation)
                self.method_8(binaryWriter_0, item.TagName)
                self.method_8(binaryWriter_0, item.TagSection)
                self.method_8(binaryWriter_0, item.TagReason)
            else:
                binaryWriter_0.write(str(0))
                binaryWriter_0.write(item.Stamp.ToOADate())
                binaryWriter_0.write(item.DwgCreated.ToOADate())
                binaryWriter_0.write(item.DwgSaved.ToOADate())
                binaryWriter_0.write(item.DwgSizeOpened)
                self.method_8(binaryWriter_0, item.DwgFileName)
                self.method_8(binaryWriter_0, item.TagProject)
                self.method_8(binaryWriter_0, item.TagName)
                self.method_8(binaryWriter_0, item.TagSection)
                self.method_8(binaryWriter_0, item.TagReason)
            for j in range(len(item.Children)):
                qARecord = item.Children[j]
                oldRecordType = OldRecordType.ProcSummary
                if (len(qARecord.Children) == 0):
                    if (qARecord.Type == QARecordType.Attached):
                        oldRecordType = OldRecordType.Attached
                    elif (qARecord.Type == QARecordType.Comment):
                        oldRecordType = OldRecordType.Comment
                    elif (qARecord.Type == QARecordType.Snapshot):
                        oldRecordType = OldRecordType.Snapshot
                    elif (qARecord.Type == QARecordType.Table and qARecord.TableType == QATableType.General):
                        oldRecordType = OldRecordType.Program
                binaryWriter_0.write(oldRecordType)
                binaryWriter_0.write(qARecord.Stamp.ToOADate())
                self.method_8(binaryWriter_0, qARecord.Heading)
                if (oldRecordType == OldRecordType.Attached):
                    self.method_8(binaryWriter_0, String.Concat([Captions.STATUS, "\t", qARecord.Text]))
                elif (oldRecordType == OldRecordType.Comment):
                    self.method_10(binaryWriter_0, qARecord.Value, False)
                elif (oldRecordType == OldRecordType.Program):
                    self.method_10(binaryWriter_0, qARecord.Value, True)
                elif (oldRecordType == OldRecordType.Snapshot):
                    qASnapshot = qARecord# as QASnapshot
                    binaryWriter_0.write(qASnapshot.ImageRatio)
                    binaryWriter_0.write(qASnapshot.ViewSize)
                    binaryWriter_0.write(QADocument.smethod_0(qASnapshot.ViewCenter))
                    binaryWriter_0.write(qASnapshot.ModelSpace)
                    image = qASnapshot.Image
                    #TODO: UnCompleted
                    # using (MemoryStream memoryStream = new MemoryStream())
                    # {
                    #     image.Save(memoryStream, ImageHelper.smethod_2(ImageFormat.Jpeg), ImageHelper.smethod_3(QA.JpegQuality))
                    #     binaryWriter_0.write(memoryStream.Length)
                    #     binaryWriter_0.write(memoryStream.ToArray())
                    # }
                elif (oldRecordType == OldRecordType.ProcSummary):
                    num = len(qARecord.Children) - 1
                    if (qARecord.Type == QARecordType.Unknown):
                        binaryWriter_0.write(str(num))
                    else:
                        binaryWriter_0.write(str(num + 1))
                        if (len(qARecord.Children) <= 0):
                            self.method_8(binaryWriter_0, "")
                        else:
                            self.method_8(binaryWriter_0, Captions.GENERAL)
                        binaryWriter_0.write(str(1))
                        num1 = 0
                        if (qARecord.Type != QARecordType.Table):
                            num1 = 1
                        else:
                            tableType = qARecord.TableType
                            if (tableType == QATableType.General):
                                num1 = 0
                            elif (tableType == QATableType.OCAH):
                                num1 = 2
                            elif (tableType == QATableType.ObstacleList):
                                num1 = 3
                        binaryWriter_0.write(str(num1))
                        self.method_8(binaryWriter_0, "")
                        if (qARecord.Type != QARecordType.Table):
                            self.method_10(binaryWriter_0, qARecord.Value, False)
                        else:
                            self.method_10(binaryWriter_0, qARecord.Value, True)
                    for k in range(len(qARecord.Children)):
                        item1 = qARecord.Children[k]
                        self.method_8(binaryWriter_0, item1.Heading)
                        count1 = item1.Children.Count
                        if (item1.Type == QARecordType.Unknown):
                            binaryWriter_0.write(str(count1))
                        else:
                            binaryWriter_0.write(str(count1 + 1))
                            num2 = 0
                            if (item1.Type != QARecordType.Table):
                                num2 = 1
                            else:
                                qATableType = item1.TableType
                                if (qATableType == QATableType.General):
                                    num2 = 0
                                elif (qATableType == QATableType.OCAH):
                                    num2 = 2
                                elif (qATableType == QATableType.ObstacleList):
                                    num2 = 3
                            binaryWriter_0.write(str(num2))
                            if (len(item1.Children) <= 0):
                                self.method_8(binaryWriter_0, "")
                            else:
                                self.method_8(binaryWriter_0, Captions.GENERAL)
                            if (item1.Type != QARecordType.Table):
                                self.method_10(binaryWriter_0, item1.Value, False)
                            else:
                                self.method_10(binaryWriter_0, item1.Value, True)
                        for l in range(len(item1.Children)):
                            qARecord1 = item1.Children[l]
                            num3 = 0
                            if (qARecord1.Type != QARecordType.Table):
                                num3 = 1
                            else:
                                tableType1 = qARecord1.TableType
                                if (tableType1 == QATableType.General):
                                    num3 = 0
                                elif (tableType1 == QATableType.OCAH):
                                    num3 = 2
                                elif (tableType1 == QATableType.ObstacleList):
                                    num3 = 3
                            binaryWriter_0.write(str(num3))
                            self.method_8(binaryWriter_0, qARecord1.Heading)
                            if (qARecord1.Type != QARecordType.Table):
                                self.method_10(binaryWriter_0, qARecord1.Value, False)
                            else:
                                self.method_10(binaryWriter_0, qARecord1.Value, True)
            binaryWriter_0.write(str(6))
            if (i != len(self.sessions) - 1):
                binaryWriter_0.write(item.Stamp.toString())
            else:
                binaryWriter_0.write(QDateTime.currentDateTime().toString())
            if (i != len(self.sessions) - 1):
                binaryWriter_0.write(item.DwgSizeClosed)
            else:
                num4 = 0
                try:
                    fileInfo = QFileInfo(self.fileNameDWG)
                    num4 = round(float(fileInfo.size()) / float(1024), 2)
                except:
                    pass
                binaryWriter_0.write(str(num4))
    
    def method_16(self, binaryWriter_0, qafileVersion_0):
        num = 0;
        numArray = [];
        tempFileName = define.appPath + "/tempFile.txt"
        binaryWriter = file(tempFileName, "w")
        # using (TempFileStream tempFileStream = new TempFileStream())
        # {
        #     using (BinaryWriter binaryWriter = new BinaryWriter(tempFileStream))
        #     {
        num1 = self.method_0();
        if (qafileVersion_0 == QAFileVersion.V8_1 or qafileVersion_0 == QAFileVersion.V10):
            binaryWriter.write(str(num1));
        count = len(self.sessions) - 1;
        self.sessions[count].DwgSizeClosed = FileHelper.smethod_3(self.fileNameDWG);
        self.sessions[count].Closed = QDateTime.currentDateTime();
        for session in self.sessions:
            session.method_15(binaryWriter, qafileVersion_0);
        #TODO: UnCompleted
        # using (TempFileStream tempFileStream1 = new TempFileStream())
        # {
        #     using (Stream zlibStream = new ZlibStream(tempFileStream1, CompressionMode.Compress, CompressionLevel.BestCompression, true))
        #     {
        #         tempFileStream.Seek((long)0, SeekOrigin.Begin);
        #         num = -1;
        #         numArray = new byte[4096];
        #         while (true)
        #         {
        #             int num2 = tempFileStream.Read(numArray, 0, 4096);
        #             num = num2;
        #             if (num2 <= 0)
        #             {
        #                 break;
        #             }
        #             zlibStream.Write(numArray, 0, num);
        #         }
        #     }
        #     binaryWriter_0.Write(tempFileStream1.Length);
        #     tempFileStream1.Seek((long)0, SeekOrigin.Begin);
        #     num = -1;
        #     numArray = new byte[4096];
        #     while (true)
        #     {
        #         int num3 = tempFileStream1.Read(numArray, 0, 4096);
        #         num = num3;
        #         if (num3 <= 0)
        #         {
        #             break;
        #         }
        #         binaryWriter_0.Write(numArray, 0, num);

        try:
            binaryWriter_0.write(len(self.reportEntries));
            for reportEntry in self.reportEntries:
                reportEntry.method_1(binaryWriter_0, qafileVersion_0);
        except:
            pass

    @staticmethod
    def smethod_0(object_0):
        #TODO: UnCompleted
        return ""
        # byte[] numArray;
        # int num = Marshal.SizeOf(object_0);
        # IntPtr intPtr = Marshal.AllocHGlobal(Marshal.SizeOf(object_0));
        # try
        # {
        #     Marshal.StructureToPtr(object_0, intPtr, false);
        #     byte[] numArray1 = new byte[num];
        #     Marshal.Copy(intPtr, numArray1, 0, num);
        #     numArray = numArray1;
        # }
        # finally
        # {
        #     Marshal.FreeHGlobal(intPtr);
        # }
        # return numArray;
    
    def getFileNameDWG(self):
        return self.fileNameDWG
    def setFileNameDWG(self, val):
        self.fileNameDWG = val
        self.fileNameQA = Path.ChangeExtension(val, ".qaa")
    FileNameDWG = property(getFileNameDWG, setFileNameDWG, None, None)

    def getFileNameQA(self):
        return self.fileNameQA
    def setFileNameQA(self, val):
        self.fileNameQA = val
        self.fileNameDWG = Path.ChangeExtension(val, ".dwg")
    FileNameQA = property(getFileNameQA, setFileNameQA, None, None)

    def getItemsLoaded(self):
        return self.itemsLoaded
    ItemsLoaded = property(getItemsLoaded, None, None, None)

    def getNoSave(self):
        return self.noSave
    def setNoSave(self, val):
        self.noSave = val
    NoSave = property(getNoSave, setNoSave, None, None)

    def getOriginalFileVersion(self):
        return self.originalFileVersion
    OriginalFileVersion = property(getOriginalFileVersion, None, None, None)

    def getReportEntries(self):
        return self.reportEntries
    ReportEntries = property(getReportEntries, None, None, None)

    def getReportEntriesSupported(self):
        if (not self.useOriginalFileVersion):
            return QA0.DefaultFileVersion == QAFileVersion.V10
        return self.originalFileVersion == QAFileVersion.V10
    ReportEntriesSupported = property(getReportEntriesSupported, None, None, None)

    def getSelectedRecord(self):
        if (self.selectedRecord != None or len(self.sessions) <= 0):
            return self.selectedRecord
        return self.sessions[len(self.sessions) - 1]
    def setSelectedRecord(self, val):
        self.selectedRecord = val
    SelectedRecord = property(getSelectedRecord, setSelectedRecord, None, None)

    def getSelectedReportEntry(self):
        if (self.selectedReportEntry != None or len(self.reportEntries) <= 0):
            return self.selectedReportEntry
        return self.reportEntries[len(self.reportEntries) - 1]
    def setSelectedReportEntry(self, val):
        self.selectedReportEntry = val
    SelectedReportEntry = property(getSelectedReportEntry, setSelectedReportEntry, None, None)

    def getSessions(self):
        return self.sessions
    Sessions = property(getSessions, None, None, None)

    def getUseOriginalFileVersion(self):
        return self.useOriginalFileVersion
    UseOriginalFileVersion = property(getUseOriginalFileVersion, None, None, None)

class OldRecordType:
    Created = "Created"
    Opened = "Opened"
    Comment = "Comment"
    Program = "Program"
    Snapshot = "Snapshot"
    Attached = "Attached"
    Closed = "Closed"
    ProcSummary = "ProcSummary"

class OldSubRecordType:
    SubSegGeneral = "SubSegGeneral"
    SubSegComment = "SubSegComment"
    SubSegOCAH = "SubSegOCAH"
    SubSegObst = "SubSegObst"