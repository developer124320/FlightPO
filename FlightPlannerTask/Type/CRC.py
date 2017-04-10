from Type.String import StringBuilder, String
from PyQt4.QtCore import QString
import  math
class CRC:
    CRC32POLY = [True, True, False, True, False, True, False, True, True, False, False, False, False, False, True, False, True, False, False, False, False, False, True, False, True, False, False, False, False, False, False, True]
    POLYNOMIALLENGTH = len(CRC32POLY)

    def __init__(self):
        pass
    @staticmethod
    def smethod_0(string_0):
        result = CRC.smethod_7(CRC.smethod_2(string_0));
        CRC.CRC32POLY = [True, True, False, True, False, True, False, True, True, False, False, False, False, False, True, False, True, False, False, False, False, False, True, False, True, False, False, False, False, False, False, True]
        CRC.POLYNOMIALLENGTH = len(CRC.CRC32POLY)
        return result

    @staticmethod
    def smethod_2(string_0):
        str0 = ""
        if isinstance(string_0, QString):
            str0 = String.QString2Str(string_0)
        else:
            str0 = string_0
        charArray = String.CharArray2Str(str0)
        flagArray = CRC.CRC32POLY;
        for i in range(len(string_0)):
            CRC.smethod_6(flagArray, CRC.smethod_3(charArray[i]));
        return CRC.smethod_5(flagArray);

    @staticmethod
    def smethod_3(char_0):
        flagArray = []
        for i in range(8):
            flagArray.append(False)
        # flagArray = new bool[8];
        for i in range(8):
            if (CRC.smethod_4(char_0, i)):
                flagArray[7 - i] = True;
        return flagArray;

    @staticmethod
    def smethod_4(char_0, int_0):
        return (ord(char_0) & ord(chr(int(math.pow(2, float(int_0))))) > 0);

    @staticmethod
    def smethod_5(bool_0):
        bool0 = []
        for i in range(len(bool_0)):
            bool0.append(False)
        # bool0 = new bool[(int)bool_0.Length];
        for i in range(len(bool_0)):
            bool0[len(bool_0) - 1 - i] = bool_0[i];
        return bool0;

    @staticmethod
    def smethod_6(bool_0, bool_1):
        for i in range(8):
            pOLYNOMIALLENGTH = CRC.POLYNOMIALLENGTH - 1;
            bool0 = bool_0[pOLYNOMIALLENGTH] ^ bool_1[i];
            while (pOLYNOMIALLENGTH > 0):
                if (not CRC.CRC32POLY[pOLYNOMIALLENGTH]):
                    bool_0[pOLYNOMIALLENGTH] = bool_0[pOLYNOMIALLENGTH - 1];
                else:
                    bool_0[pOLYNOMIALLENGTH] = bool_0[pOLYNOMIALLENGTH - 1] ^ bool0;
                pOLYNOMIALLENGTH -= 1;
            bool_0[pOLYNOMIALLENGTH] = bool0;

    @staticmethod
    def smethod_7(bool_0):
        stringBuilder = StringBuilder();
        i = 0
        while i < len(bool_0):
            stringBuilder.Append(CRC.smethod_8(i, bool_0));
            i = i + 4
        # for (int i = 0; i < (int)bool_0.Length; i = i + 4)
        # {
        #     stringBuilder.Append(CRC.smethod_8(i, bool_0));
        # }
        return stringBuilder.ToString().upper();

    @staticmethod
    def smethod_8(int_0, bool_0):
        chrC = '\0';

        for i in range(4):
            if (bool_0[int_0 + (3 - i)]):
                chrC = chr(ord(chrC) + int(math.pow(2, float(i))));
        resultStr = hex(ord(chrC))
        resultStr = resultStr.replace("0x", "")
        # resultStr.replace("0X", "")
        return resultStr
        # return Convert.ToInt32(chrC).ToString("X1");

