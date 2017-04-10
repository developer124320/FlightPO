
from QARecord import QARecord
from FlightPlanner.types import QARecordType, QAFileVersion, Point3D
from Type.String import String
from Type.switch import switch
from PyQt4.QtGui import QApplication

class QASnapshot(QARecord):
    def __init__(self):
        QARecord.__init__()
        self.Type = QARecordType.Snapshot
        self.value = None;
        self.imageRatio = None;
        self.imageFormatType = None;
        self.modelSpace = None
        self.viewCenter = None;
        self.viewSize = None;
    def method_6(self, stringBuilder_0, string_0, bool_0, bool_1):
        if (bool_0):
            QARecord.smethod_0(self.title, stringBuilder_0);
        self.HtmlBody(stringBuilder_0, string_0);
        for child in self.children:
            string0 = string_0;
            if (not String.IsNullOrEmpty(child.Heading)):
                string0 = "{0} - {1}".format(string0, child.title) if(not String.IsNullOrEmpty(string0)) else child.title
            child.method_6(stringBuilder_0, string0, False, False);
        if (bool_1):
            QARecord.smethod_1(stringBuilder_0);
    def method_10(self, object_0, object_1, string_0):
        self.WordDocumentBody(object_0, object_1, string_0);
        QARecord.method_10(object_0, object_1, string_0)
    def method_11(self):
        clipboard = QApplication.clipboard()
        clipboard.clear()
        clipboard.setImage(self.Image);

    def method_12(self, stringBuilder_0, qasnapshot_0, string_0, int_0):
        #TODO: UnCompleted
        return int_0
        # string str;
        # using (System.Drawing.Image image = qasnapshot_0.Image)
        # {
        #     if (qasnapshot_0.ImageFormatType == QASnapshotFormat.Png)
        #     {
        #         str = string.Format("img{0:000}.png", int_0);
        #         image.Save(Path.Combine(string_0, str), ImageFormat.Png);
        #     }
        #     else if (qasnapshot_0.ImageFormatType != QASnapshotFormat.Gif)
        #     {
        #         str = string.Format("img{0:000}.jpg", int_0);
        #         image.Save(Path.Combine(string_0, str), ImageHelper.smethod_2(ImageFormat.Jpeg), ImageHelper.smethod_3(QA.JpegQuality));
        #     }
        #     else
        #     {
        #         str = string.Format("img{0:000}.gif", int_0);
        #         image.Save(Path.Combine(string_0, str), ImageFormat.Gif);
        #     }
        # }
        # stringBuilder_0.AppendLine("<div align=\"center\">");
        # stringBuilder_0.AppendLine(string.Format("<img style=\"border: 1px solid;\" alt=\"{0}\" src=\"{1}\">", qasnapshot_0.Heading, str));
        # stringBuilder_0.AppendLine("</div>");
        # int_0 = int_0 + 1;

    def HtmlBody(self, lines, title):
        raise SystemError
    
    def LoadData(self, reader, version):
        QARecord.LoadData(reader, version);
        for case in switch (version):
            if case(QAFileVersion.V8) or case(QAFileVersion.V8_1) or case(QAFileVersion.V10):
                self.modelSpace = reader.ReadBoolean();
                self.viewSize = reader.ReadDouble();
                self.viewCenter = Point3D(reader.ReadDouble(), reader.ReadDouble(), reader.ReadDouble());
                self.imageFormatType = reader.ReadByte();
                self.imageRatio = reader.ReadDouble();
                num = reader.ReadInt64();
                self.value.SetLength(num);
                # self.value.Seek((long)0, SeekOrigin.Begin);
                self.value.write(reader.ReadBytes(int(num)), 0, int(num));
                return;
            else:
                raise  SystemError
    
    def SaveData(self, writer, version):
        QARecord.SaveData(writer, version);
        for case in switch (version):
            if case(QAFileVersion.V8) or case(QAFileVersion.V8_1) or case(QAFileVersion.V10):
                writer.write(self.modelSpace);
                writer.write(self.viewSize);
                writer.write(self.viewCenter.get_X());
                writer.write(self.viewCenter.get_Y());
                writer.write(self.viewCenter.get_Z());
                writer.write(self.imageFormatType);
                writer.write(self.imageRatio);
                writer.write(self.value.Length);
                writer.write(self.value.ToArray());
                return;
            else:
                raise SystemError
    def WordDocumentBody(self, wordApp, wordDoc, title):
        #TODO: UnColpleted
        pass
        # string str = null;
        # using (System.Drawing.Image image = this.Image)
        # {
        #     switch (this.imageFormatType)
        #     {
        #         case QASnapshotFormat.Jpeg:
        #         {
        #             str = FileHelper.smethod_1(".jpg");
        #             break;
        #         }
        #         case QASnapshotFormat.Gif:
        #         {
        #             str = FileHelper.smethod_1(".gif");
        #             break;
        #         }
        #         case QASnapshotFormat.Png:
        #         {
        #             str = FileHelper.smethod_1(".png");
        #             break;
        #         }
        #     }
        #     if (!string.IsNullOrEmpty(str))
        #     {
        #         image.Save(str);
        #     }
        #     else
        #     {
        #         return;
        #     }
        # }
        # object obj = wordApp.smethod_24("Selection");
        # if (!string.IsNullOrEmpty(title))
        # {
        #     object obj1 = obj.smethod_24("Font");
        #     obj1.smethod_25("Bold", true);
        #     obj.smethod_21("TypeText", string.Format("{0}\r", title));
        #     obj1.smethod_25("Bold", false);
        #     obj.smethod_21("TypeText", "\r");
        # }
        # object obj2 = obj.smethod_24("InlineShapes");
        # object[] objArray = new object[] { str, false, true };
        # object obj3 = obj2.smethod_23("AddPicture", objArray);
        # obj3.smethod_24("Borders").smethod_25("Enable", true);
        # obj.smethod_22("GoToNext", 3);

    def getImageFormatType(self):
        return self.imageFormatType
    def setImageFormatType(self, val):
        self.imageFormatType = val
    ImageFormatType = property(getImageFormatType, setImageFormatType, None, None)

    def getImageRatio(self):
        return self.imageRatio
    def setImageRatio(self, val):
        self.imageRatio = val
    ImageRatio = property(getImageRatio, setImageRatio, None, None)

    def getModelSpace(self):
        return self.modelSpace
    def setModelSpace(self, val):
        self.modelSpace = val
    ModelSpace = property(getModelSpace, setModelSpace, None, None)

    def getValue(self):
        return self.value
    def setValue(self, val):
        self.value = val
    Value = property(getValue, setValue, None, None)

    def getViewCenter(self):
        return self.viewCenter
    def setViewCenter(self, val):
        self.viewCenter = val
    ViewCenter = property(getViewCenter, setViewCenter, None, None)

    def getViewSize(self):
        return self.viewSize
    def setViewSize(self, val):
        self.viewSize = val
    ViewSize = property(getViewSize, setViewSize, None, None)
