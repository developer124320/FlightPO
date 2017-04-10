

from QARecord import QARecord
from FlightPlanner.types import QARecordType
from Type.String import String
class QAUnknown(QARecord):
    def __init__(self):
        QARecord.__init__()

        self.Type = QARecordType.Unknown
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