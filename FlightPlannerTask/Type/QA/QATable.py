
from QARecord import QARecord
from FlightPlanner.types import QARecordType, QATableType, QAFileVersion
from Type.Extensions import Extensions
from Type.String import String, StringBuilder
from Type.switch import switch

class QATable(QARecord):
    def __init__(self):
        QARecord.__init__(self)
        self.Type = QARecordType.Table
        self.tableType = None;
        self.value = None;
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

    def method_12(self, string_0):
        num = 0;
        string0 = string_0;
        for i in range(len(string0)):
            str0 = string0[i];
            num1 = 1;
            str1 = str0;
            # str1 = String.Str2QString(str1)
            for sj in str1:
                if (sj == '\t'):
                    num1 += 1;
            if (num < num1):
                num = num1;
            if (self.tableType == QATableType.ObstacleList):
                return num;
        return num;

    def method_13(self, string_0, bool_0):
        if (String.IsNullOrEmpty(string_0)):
            return "<br>";
        if (not bool_0):
            return string_0;
        string_0 = String.QString2Str(string_0)
        return string_0.replace(" ", "&nbsp;");

    def method_14(self, string_0, int_0, int_1):
        str0 = "";
        stringBuilder = StringBuilder();
        strArrays = Extensions.smethod_4(string_0);
        for i in range(len(strArrays) - 1):
            str1 = strArrays[i];
            for case in switch (self.tableType):
                if case(QATableType.General):
                    stringBuilder.Append("<td>{0}</td>".format(self.method_13(str1, True)));
                    break;
                elif case(QATableType.OCAH):
                    if (int_0 == 0 or i == 0):
                        stringBuilder.Append("<th>{0}</th>".format(self.method_13(str1, False)));
                        break;
                    else:
                        stringBuilder.Append("<td>{0}</td>".format(self.method_13(str1, False)));
                        break;
                elif case(QATableType.ObstacleList):
                    if (int_0 != 0):
                        stringBuilder.Append("<td>{0}</td>".format(self.method_13(str1, False)));
                        break;
                    else:
                        stringBuilder.Append("<th>{0}</th>".format(self.method_13(str1, False)));
                        break;
        str0 = "<br>" if(len(strArrays) <= 0) else strArrays[len(strArrays) - 1];
        for case in switch (self.tableType):
            if case(QATableType.General):
                if (len(strArrays) == 1 and int_1 > 1):
                    num = str0.smethod_6();
                    if (num < 4):
                        str0 = "<b>{0}</b>".format(str0);
                    elif (num < 8):
                        str0 = "<b><i>{0}</i></b>".format(str0);
                if (len(strArrays) >= int_1):
                    stringBuilder.Append("<td>{0}</td>".format(self.method_13(str, True)));
                    break;
                else:
                    int1 = int_1 - len(strArrays) + 1;
                    stringBuilder.Append("<td colspan=\"{0}\">{1}</td>".format(str(int1), self.method_13(str, True)));
                    break;
            elif case(QATableType.OCAH):
                if (int_0 != 0):
                    if (len(strArrays) == 1):
                        stringBuilder.Append("<th>{0}</th>".format(self.method_13(str, False)));
                        for j in range(len(strArrays), int_1):
                            stringBuilder.Append("<td><br></td>");
                        break;
                    stringBuilder.Append("<td>{0}</td>".format(self.method_13(str, False)));
                stringBuilder.Append("<th>{0}</th>".format(self.method_13(str, False)));
                for j in range(len(strArrays), int_1):
                    stringBuilder.Append("<td><br></td>");
                break;
            elif case(QATableType.ObstacleList):
                if (int_0 != 0):
                    stringBuilder.Append("<td>{0}</td>".format(self.method_13(str, False)));
                else:
                    stringBuilder.Append("<th>{0}</th>".format(self.method_13(str, False)));
                for k in range(len(strArrays), int_1):
                    stringBuilder.Append("<td><br></td>");
                break;
        return stringBuilder.ToString();

    def HtmlBody(self, lines, title):
        lines.AppendLine("<div align=\"center\">");
        if (not String.IsNullOrEmpty(title)):
            lines.AppendLine("<p align=\"center\"><b>{0}</b></p>".format(title));
        lines.AppendLine("<table border=\"0\" cellpadding=\"2\" cellspacing=\"0\">");
        lines.AppendLine("<tbody>");
        strArrays = Extensions.smethod_3(self.Text);
        num = self.method_12(strArrays);
        for i in range(len(strArrays)):
            lines.AppendLine("<tr>{0}</tr>".format(self.method_14(strArrays[i], i, num)));
        lines.AppendLine("</tbody>");
        lines.AppendLine("</table>");
        lines.AppendLine("</div>");

    def LoadData(self, reader, version):
        QARecord.LoadData(reader, version);
        for case in switch (version):
            if case(QAFileVersion.V8) or case(QAFileVersion.V8_1):
                self.tableType = reader.ReadByte();
                self.method_0(self.value, reader.ReadBytes(int(reader.ReadInt64())), False);
                return;
            elif case(QAFileVersion.V10):
                self.tableType = reader.ReadByte();
                self.method_0(self.value, reader.ReadBytes(int(reader.ReadInt64())), True);
                return;
            else:
                raise SystemError
    def SaveData(self, writer, version):
        numArray = [];
        QARecord.SaveData(writer, version);
        for case in switch (version):
            if case(QAFileVersion.V8) or case(QAFileVersion.V8_1):
                writer.write(self.tableType);
                numArray = self.method_1(self.value, False);
                writer.write(numArray.LongLength);
                writer.write(numArray);
                return;
            elif case(QAFileVersion.V10):
                writer.write(self.tableType);
                numArray = self.method_1(self.value, True);
                writer.write(numArray.LongLength);
                writer.write(numArray);
                return;
            else:
                raise SystemError
    def WordDocumentBody(self, wordApp, wordDoc, title):
        #TODO : UnCompleted
        pass
        # string[] strArrays = this.Text.smethod_3();
        # int num = this.method_12(strArrays);
        # if ((int)strArrays.Length < 1 || num < 1)
        # {
        #     return;
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
        # object obj2 = wordDoc.smethod_24("Tables");
        # object[] objArray = new object[] { obj.smethod_24("Range"), (int)strArrays.Length, num, 1, 1 };
        # object obj3 = obj2.smethod_23("Add", objArray);
        # obj3.smethod_25("ApplyStyleHeadingRows", true);
        # obj3.smethod_25("ApplyStyleLastRow", true);
        # obj3.smethod_25("ApplyStyleFirstColumn", true);
        # obj3.smethod_25("ApplyStyleLastColumn", true);
        # object obj4 = obj3.smethod_24("Rows");
        # for (int i = 0; i < (int)strArrays.Length; i++)
        # {
        #     this.method_15(obj3, strArrays[i], i, num);
        #     obj4.smethod_22("Item", i + 1).smethod_24("Cells").smethod_25("VerticalAlignment", 1);
        # }
        # obj4.smethod_25("Alignment", 1);
        # obj3.smethod_22("AutoFitBehavior", 1);
        # obj3.smethod_24("Range").smethod_20("Select");
        # obj.smethod_25("Start", obj.smethod_24("End"));
        # obj.smethod_21("TypeText", "\r");

    def getTableType(self):
        return self.tableType
    def setTableType(self, val):
        self.tableType = val
    TableType = property(getTableType, setTableType, None, None)
    
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

