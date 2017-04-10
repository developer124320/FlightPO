'''
This part was made of using PHX_15.
'''



# from PyQt4.QtXml import QDomNode, QDomElement
# from QA.QAAttached import QAAttached, QARecord
# from QA.QASession import QASession
# from QA.QASnapshot import QASnapshot
# from QA.QAUnknown import QAUnknown
# from QA.QATable import QATable
# from QA.QAComment import QAComment

from Type.switch import switch
from Type.String import String, StringBuilder, QString
import math

class XmlNode:
    @staticmethod
    def smethod_29(xmlNode_0, string_0):
        xmlElement = xmlNode_0.ownerDocument().createElement(string_0)
        xmlNode_0.appendChild(xmlElement)
        return xmlElement

    @staticmethod
    def smethod_30(xmlNode_0, string_0, string_1):
        if string_1 == None:
            string_1 = ""
        doc = xmlNode_0.ownerDocument()
        string1 = doc.createElement(string_0)
        string1.appendChild(doc.createTextNode(string_1))
        xmlNode_0.appendChild(string1)
        return string1
class Extensions:
    @staticmethod
    def smethod_0(string_0):
        stringBuilder = StringBuilder(string_0)
        num = 0
        tempChrList = String.ToCharArray(string_0)
        while (num < stringBuilder.Length):
            if (tempChrList[num] == '\r'):
                if (num >= stringBuilder.Length - 1 or stringBuilder[num + 1] != '\n'):
                    num += 1
                    stringBuilder.Insert(num, '\n')
                else:
                    num = num + 2
                    continue
            num += 1
        return stringBuilder.ToString()
    @staticmethod
    def smethod_3(string_0):
        strs = String.Str2QString(Extensions.smethod_0(string_0)).split('\n')
        count = strs.count()
        if (count > 0 and String.IsNullOrEmpty(strs[count - 1])):
            strs.removeAt(count - 1)
        return strs

    @staticmethod
    def smethod_4(string_0):
        string_0 = String.QString2Str(string_0)
        return string_0.split('\t')

    @staticmethod
    def smethod_6(string_0):
        num = 0
        string0 = string_0
        string0 = String.QString2Str(string0)
        for si in string0:
            if (si != ' '):
                return num
            num += 1
        return num

    @staticmethod
    def smethod_11(string_0, string_1, string_2):
        if (String.IsNullOrEmpty(string_1)):
            return string_0
        stringBuilder = StringBuilder()
        if not isinstance(string_0, QString):
            string_0 = QString(string_0)
        if not isinstance(string_1, QString):
            string_1 = QString(string_1)
        if not isinstance(string_2, QString):
            string_2 = QString(string_2)
        length = string_1.length()
        num = -1
        num1 = 0
        while (True):
            num = string_0.indexOf(string_1, num + 1)
            if (num < 0):
                break
            stringBuilder.Append(string_0, num1, num - num1)
            stringBuilder.Append(string_2)
            num1 = num + length
        stringBuilder.Append(string_0, num1, string_0.length()- num1)
        return QString(stringBuilder.ToString())

    @staticmethod
    def smethod_17(double_0):
        if double_0 == None:
            return 0
        if (not math.isnan(double_0) and not math.isinf(double_0)):
            return float(double_0)
        return 0

    @staticmethod
    def smethod_18(double_0):
        if double_0 == None:
            return False
        if (math.isnan(double_0)):
            return False
        return not math.isinf(double_0)

    @staticmethod
    def smethod_19(dateTime_0):
        return "{0}, {1}".format(dateTime_0.toString("dddd, MMMM d, yyyy"), dateTime_0.toString("h:mm:ss AP"))

    @staticmethod
    def smethod_26(bool_0):
        return "{0}".format(str(bool_0))

    # @staticmethod
    # def QARecordSmethod_2(binaryReader_0, qafileVersion_0):
    #     qAUnknown = None
    #     num = 0
    #     for case in switch (binaryReader_0.ReadByte()):
    #         if case(0):
    #             qAUnknown = QAUnknown()
    #             break
    #         elif case(1):
    #             qAUnknown = QAAttached()
    #             break
    #         elif case(2):
    #             qAUnknown = QATable()
    #             break
    #         elif case(3):
    #             qAUnknown = QAComment()
    #             break
    #         elif case(4):
    #             qAUnknown = QASnapshot()
    #             break
    #         elif case(5):
    #             qAUnknown = QASession()
    #             break
    #         else:
    #             raise  SystemError
    #     qAUnknown.LoadData(binaryReader_0, qafileVersion_0)
    #     num = binaryReader_0.ReadInt32()
    #     for i in range(num):
    #         qAUnknown.Children.append(Extensions.QARecordSmethod_2(binaryReader_0, qafileVersion_0))
    #     return qAUnknown
    #
