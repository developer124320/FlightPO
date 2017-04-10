
from QARecord import QARecord
from FlightPlanner.types import QARecordType, QAFileVersion
from Type.String import String
from Type.switch import switch

class QAAttached(QARecord):
    def __init__(self):
        QARecord.__init__()
        self.Type = QARecordType.Attached
        self.value = None
    def LoadData(self, reader, version):
        QARecord.LoadData(reader, version);
        for case in switch (version):
            if case(QAFileVersion.V8) or case(QAFileVersion.V8_1):
                self.method_0(self.value, reader.ReadBytes(reader.ReadInt32()), False)
                return;
            elif case(QAFileVersion.V10):
                self.method_0(self.value, reader.ReadBytes(reader.ReadInt32()), True);
                return;
            else:
                raise SystemError
    def SaveData(self, writer, version):
        numArray = [];
        QARecord.SaveData(writer, version);
        for case in switch (version):
            if case(QAFileVersion.V8) or case(QAFileVersion.V8_1):
                numArray = self.method_1(self.value, False);
                writer.write(int(len(numArray)));
                writer.write(numArray);
                return;
            elif case(QAFileVersion.V10):
                numArray = QARecord.method_1(self.value, True);
                writer.Write(int(len(numArray)));
                writer.write(numArray);
                return;
            else:
                raise SystemError
    def HtmlBody(self, lines, title):
        lines.AppendLine("<div align=\"center\">");
        if (not String.IsNullOrEmpty(title)):
            lines.AppendLine(String.Concat(["<p align=\"center\"><b>", title, "</b></p>"]));
        lines.AppendLine("<table border=\"0\" cellpadding=\"2\" cellspacing=\"0\">");
        lines.AppendLine("<tbody>");
        lines.AppendLine(String.Concat(["<tr><td>", self.Text, "</td></tr>"]));
        lines.AppendLine("</tbody>");
        lines.AppendLine("</table>");
        lines.AppendLine("</div>");
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
    def WordDocumentBody(self, wordApp, wordDoc, title):
        #TODO: UnCompleted
        pass
        # object obj = wordApp.smethod_24("Selection");
        # if (!string.IsNullOrEmpty(title))
        # {
        #     object obj1 = obj.smethod_24("Font");
        #     obj1.smethod_25("Bold", true);
        #     obj.smethod_21("TypeText", string.Format("{0}\r", title));
        #     obj1.smethod_25("Bold", false);
        #     obj.smethod_21("TypeText", "\r");
        # }
        # object obj2 = wordDoc.smethod_24("Tables");
        # object[] objArray = new object[] { obj.smethod_24("Range"), 1, 1, 1, 1 };
        # object obj3 = obj2.smethod_23("Add", objArray);
        # obj3.smethod_25("ApplyStyleHeadingRows", true);
        # obj3.smethod_25("ApplyStyleLastRow", true);
        # obj3.smethod_25("ApplyStyleFirstColumn", true);
        # obj3.smethod_25("ApplyStyleLastColumn", true);
        # object[] objArray1 = new object[] { 1, 1 };
        # obj3.smethod_23("Cell", objArray1).smethod_24("Range").smethod_25("Text", this.Text);
        # obj3.smethod_24("Rows").smethod_22("Item", 1).smethod_24("Cells").smethod_25("VerticalAlignment", 1);
        # obj.smethod_22("GoToNext", 3);
    def method_10(self, object_0, object_1, string_0):
        self.WordDocumentBody(object_0, object_1, string_0);
        QARecord.method_10(object_0, object_1, string_0)

    def getText(self):
        return self.method_2(self.value)
    def setText(self, val):
        self.method_3(self.value, val)
    Text = property(getText, setText, None, None)

    def getValue(self):
        return self.value
    def setValue(self, val):
        self.value = val
    Value = property(getValue, setValue, None, None)
