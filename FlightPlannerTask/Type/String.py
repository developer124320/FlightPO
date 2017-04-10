
from PyQt4.QtCore import QString, QChar

class String:
    def __init__(self):
        pass
    @staticmethod
    def StartsWith(obj, string0):
        compStr = None
        if isinstance(obj, str) or isinstance(obj, QString):
            compStr = obj
        elif isinstance(obj, int) or isinstance(obj, float):
            compStr = str(obj)
        else:
            compStr = obj.ToString()
        try:
            index0 = compStr.index(string0)
            return True
        except:
            return False
        return False
    @staticmethod
    def Equals(obj, string0):
        if isinstance(obj, str) or isinstance(obj, QString):
            return obj == string0
        elif isinstance(obj, int) or isinstance(obj, float):
            return str(obj) == string0
        else:
            return obj.ToString() == string0
    @staticmethod
    def CharArray2Str(charArray):
        resultStr = ""
        for char in charArray:
            resultStr += char
        return resultStr

    @staticmethod
    def Concat(strList):
        if len(strList) == 0:
            return ""
        resultStr = ""
        for str0 in strList:
            resultStr += str0
        return resultStr

    @staticmethod
    def Join(delimiter, strList):
        if len(strList) == 0:
            return ""
        resultStr = ""
        i = 0
        n = len(strList)
        for str0 in strList:
            i += 1
            if i == n:
                resultStr += str0
            else:
                resultStr += str0 + delimiter
        return resultStr
    @staticmethod
    def Number2String(num, numTypeStr):
        if numTypeStr == None:
            return str(num)
        index = 0
        index0 = 0
        length0 = 0
        length = 0
        try:
            index = numTypeStr.index(".")
            length = len(numTypeStr[index + 1 :len(numTypeStr)])
            num = round(num, length)

            numStr = str(num)
            index0 = numStr.index(".")
            length0 = len(numStr[index0 + 1 :len(numStr)])
        except:
            if len(numTypeStr) <= len(str(num)):
                return str(num)
            s = ""
            for i in range(len(numTypeStr) - len(str(num))):
                s += "0"
            s += str(num)
            return s
        d = int(round(num))
        if index == 0:
            resultStr = str(d)
        else:
            resultStr = str(num)
        if len(numTypeStr) - len(str(d)) > 0:
            if index == 0:
                for i in range(len(numTypeStr) - len(str(d))):
                    resultStr = "0" + resultStr
            elif index > 0:
                for i in range(index - len(str(d))):
                    resultStr = "0" + resultStr
        if length > 0:
            if length0 < length:
                if index0 == 0:
                    resultStr += "."
                for i in range(length - length0):
                    resultStr += "0"
        return resultStr

    @staticmethod
    def IsNoneOrEmpty(string0):
        return string0 == None or string0 == ""
    @staticmethod
    def IsNullOrEmpty(string0):
        return string0 == None or string0 == ""

    @staticmethod
    def ToCharArray(string, startIndex, length):
        string = String.QString2Str(string)
        str0 = string[startIndex:startIndex + length]
        charArray = []
        if isinstance(str0, QString):
            str0 = str0.toAscii()
        for c in str0:

            charArray.append(c)
        return charArray
    @staticmethod
    def QString2Str(qStr):
        qStr = QString(qStr)
        byteArray0 = qStr.toAscii()
        resultStr = ""
        for i in range(byteArray0.length()):
            resultStr += byteArray0.at(i)
        return resultStr
    @staticmethod
    def Str2QString(str0):
        return QString(str0)

    @staticmethod
    def smethod_11(string_0, string_1, string_2):
        string_0 = String.Str2QString(string_0)
        if (String.IsNullOrEmpty(string_1)):
            return string_0;
        stringBuilder = StringBuilder();
        string_1 = String.Str2QString(string_1)
        length = string_1.length();
        num = -1;
        num1 = 0;
        while (True):
            num = string_0.indexOf(string_1, num + 1);
            if (num < 0):
                break;
            stringBuilder.Append(string_0, num1, num - num1);
            stringBuilder.Append(string_2);
            num1 = num + length;
        stringBuilder.Append(string_0, num1, string_0.length() - num1);
        return stringBuilder.ToString();


    # @staticmethod
    # def Format(strList):
    #     if len(strList) == 0:
    #         return ""
    #     strIn = strList[0]
    #     j = 1
    #     s = "as  df"
    #     s.format()
    #     dd = s.replace("as", "[dffh]", 2)
    #     if isinstance(strIn, QString):
    #         startIndex = None
    #         i = 0
    #         for a in strIn:
    #             if a == "{":
    #                 startIndex = i
    #             if startIndex != None:
    #                 if a == "}":
    #                     endIndex = i
    #                     strIn.replace(startIndex, endIndex - startIndex + 1, strList[j])
    #                     startIndex = None
    #                     j += 1
    #             i += 1
    #         return strIn
class StringBuilder:
    def __init__(self, string = ""):
        self.resultStr = string
    def AppendLine(self, string0):
        if self.resultStr == "":
            self.resultStr += string0
            return
        self.resultStr += "\n" + string0

    def Append(self, string, startIndex = None, count = None):
        if startIndex == None:
            self.resultStr += string
        else:
            string = String.Str2QString(string)
            s = string.mid(startIndex, count)
            self.resultStr += s
    def Replace(self, oldStr, newStr, startIndex, count):
        str0 = String.QString2Str(self.resultStr)
        str0.replace(oldStr, newStr, count)
    def Insert(self, index, string):
        if index == len(self.resultStr):
            self.resultStr += string
        elif index < len(self.resultStr):
            resultStr = ""
            i = 0
            for str0 in self.resultStr:
                if i == index:
                    resultStr += string
                resultStr += str0
                i += 1
            self.resultStr = resultStr

    def ToString(self):
        return self.resultStr
    def get_Length(self):
        return len(self.resultStr)
    Length = property(get_Length, None, None, None)