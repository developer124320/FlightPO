from PyQt4.QtCore import QString, Qt
from PyQt4.QtGui import QProgressBar, QApplication
from Type.String import String, StringBuilder
from FlightPlanner.types import FasDbApproachTchUnits
import math, Type.ByteFunc, define

class FasDataBlockFile:
    FasDbApproachPerformanceDesignator = [0,1,2,3,4,5,6,7]
    # APV = "APV"
    # Cat1 = "Cat1"
    # Cat2 = "Cat2"
    # Cat3 = "Cat3"
    # spare4 = "spare4"
    # spare5 = "spare5"
    # spare6 = "spare6"
    # spare7 = "spare7"

    FasDbOperationType = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    # StraightInOffset = "StraightInOffset"
    # spare1 = "spare1"
    # spare2 = "spare2"
    # spare3 = "spare3"
    # spare4 = "spare4"
    # spare5 = "spare5"
    # spare6 = "spare6"
    # spare7 = "spare7"
    # spare8 = "spare8"
    # spare9 = "spare9"
    # spare10 = "spare10"
    # spare11 = "spare11"
    # spare12 = "spare12"
    # spare13 = "spare13"
    # spare14 = "spare14"
    # spare15 = "spare15"

    FasDbRunwayLetter = [0,1,2,3]
    # Nothing = "None"
    # R = "R"
    # C = "C"
    # L = "L"

    FasDbSbasServiceProvider = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    # WAAS = "WAAS"
    # EGNOS = "EGNOS"
    # MSAS = "MSAS"
    # GAGAN = "GAGAN"
    # SDCM = "SDCM",
    # spare5 = "spare5"
    # spare6 = "spare6"
    # spare7 = "spare7"
    # spare8 = "spare8"
    # spare9 = "spare9"
    # spare10 = "spare10"
    # spare11 = "spare11"
    # spare12 = "spare12"
    # spare13 = "spare13"
    # GBASonly = "GBASonly"
    # AnySBASprovider = "AnySBASprovider"

    def __init__(self):
        self.bytes = bytearray(40)
        for i in range(40):
            self.bytes[i] = '0'

    def get_AirportId(self):
        num = 1
        chrArray = ['', '', '', '']
        i = 3
        while i >= 0:
            if (ord(chr(self.bytes[num])) >= 32):
                chrArray[i] = chr(ord(chr(self.bytes[num])))
            else:
                chrArray[i] = chr(ord(chr(self.bytes[num])) | 64)
            num += 1
            i -= 1
        return String.CharArray2Str(chrArray)
    def set_AirportId(self, value):
        num = 1
        while (len(value) < 4):
            value = String.Concat([value, " "])
        charArray = String.ToCharArray(value, 0, 4)
        i = 3
        while i >= 0:
            self.bytes[num] = Type.ByteFunc.d2b(ord(charArray[i]) & ord('?'))
            num += 1
            i -= 1
        self.method_3()
    AirportId = property(get_AirportId, set_AirportId, None, None)

    def get_ApproachPerformanceDesignator(self):
        return self.FasDbApproachPerformanceDesignator[ord(chr(self.bytes[6])) & 7]
    def set_ApproachPerformanceDesignator(self, value):
        num = Type.ByteFunc.d2b(value)
        self.bytes[6] = Type.ByteFunc.d2b(ord(chr(self.bytes[6])) ^ ((ord(chr(self.bytes[6])) ^ ord(num)) & 7))
        self.method_3()
    ApproachPerformanceDesignator = property(get_ApproachPerformanceDesignator, set_ApproachPerformanceDesignator, None, None)

    def get_ApproachTch(self):
        num = int(ord(chr(self.bytes[28])) | ord(chr(self.bytes[29])) << 8)
        num1 = int(num & 32767)
        if ((num >> 15) == 1):
            return float(num1) * 0.05
        return float(num1) * 0.1
    ApproachTch = property(get_ApproachTch, None, None, None)

    def get_ApproachTchUnits(self):
        if ((int(ord(chr(self.bytes[28])) | ord(chr(self.bytes[29])) << 8) >> 15) == 1):
            return FasDbApproachTchUnits.m
        return FasDbApproachTchUnits.ft
    ApproachTchUnits = property(get_ApproachTchUnits, None, None, None)

    def get_CourseWidth(self):
        return float(ord(chr(self.bytes[32]))) * 0.25 + 80
    def set_CourseWidth(self, value):
        self.bytes[32] = Type.ByteFunc.d2b(int(round((value - 80) * 4)))
        self.method_3()
    CourseWidth = property(get_CourseWidth, set_CourseWidth, None, None)


    def get_CRC(self):
        stringBuilder = StringBuilder()
        for i in range(36, 40):
            stringBuilder.Append(hex(ord(chr(self.bytes[i]))).replace("0x", "").upper())
        return stringBuilder.ToString()
    CRC = property(get_CRC, None, None, None)

    def get_DeltaFpapLatitude(self):
        num = ord(chr(self.bytes[22])) | ord(chr(self.bytes[23])) << 8 | ord(chr(self.bytes[24])) << 16
        num = num | -(num & 8388608)
        return float(num) * 0.0005 / 3600
    def set_DeltaFpapLatitude(self, value):
        num = int(round(value * 3600 / 0.0005))
        self.bytes[22] = Type.ByteFunc.d2b(num)
        self.bytes[23] = Type.ByteFunc.d2b(num >> 8)
        self.bytes[24] = Type.ByteFunc.d2b(num >> 16)
        self.method_3()
    DeltaFpapLatitude = property(get_DeltaFpapLatitude, set_DeltaFpapLatitude, None, None)

    def get_DeltaFpapLongitude(self):
        num = ord(chr(self.bytes[25])) | ord(chr(self.bytes[26])) << 8 | ord(chr(self.bytes[27])) << 16
        num = num | -(num & 8388608)
        return float(num) * 0.0005 / 3600
    def set_DeltaFpapLongitude(self, value):
        num = int(round(value * 3600 / 0.0005))
        self.bytes[25] = Type.ByteFunc.d2b(num)
        self.bytes[26] = Type.ByteFunc.d2b(num >> 8)
        self.bytes[27] = Type.ByteFunc.d2b(num >> 16)
        self.method_3()
    DeltaFpapLongitude = property(get_DeltaFpapLongitude, set_DeltaFpapLongitude, None, None)

    def get_DeltaLengthOffset(self):
        if (ord(chr(self.bytes[33])) == 255):
            return None
        return float(ord(chr(self.bytes[33]))) * 8
    def set_DeltaLengthOffset(self, value):
        if (not math.isnan(value)):
            self.bytes[33] = Type.ByteFunc.d2b(int(round(value * 0.125)))
        else:
            self.bytes[33] = Type.ByteFunc.d2b(255)
        self.method_3()
    DeltaLengthOffset = property(get_DeltaLengthOffset, set_DeltaLengthOffset, None, None)

    def get_GPA(self):
        num = int(ord(chr(self.bytes[30])) | ord(chr(self.bytes[31])) << 8)
        return float(num) * 0.01
    def set_GPA(self, value):
        num = int(round(value * 100))
        self.bytes[30] = Type.ByteFunc.d2b(num)
        self.bytes[31] = Type.ByteFunc.d2b(num >> 8)
        self.method_3()
    GPA = property(get_GPA, set_GPA, None, None)

    def get_HAL(self):
        return float(ord(chr(self.bytes[34])) * 0.2)
    def set_HAL(self, value):
        self.bytes[34] = Type.ByteFunc.d2b(int(round(value * 5)))
        self.method_3()
    HAL = property(get_HAL, set_HAL, None, None)

    def get_HexString(self):
        stringBuilder = StringBuilder()
        for i in range(40):
            str0 = hex(ord(chr(self.bytes[i]))).replace("0x", "").upper()
            if len(str0) == 1:
                str0 = "0" + str0
            stringBuilder.Append(str0)
            if (i < 39):
                stringBuilder.Append(" ")
        return stringBuilder.ToString()
    def set_HexString(self, value):
        if value == "":
            return
        # value = value.replace(" ", "")
        if (self.bytes == None or len(self.bytes) != 40):
            self.bytes = bytearray(40)
        i = 0

        valueList = value.split(' ')
        while i< 40:
            if isinstance(value, QString):
                # ss = value.mid(i, 2)
                self.bytes[i] = Type.ByteFunc.d2b(int(String.QString2Str(valueList[i]), 16))
            else:
                self.bytes[i] = Type.ByteFunc.d2b(int(valueList[i], 16))
            i += 1
    HexString = property(get_HexString, set_HexString, None, None)

    def get_LtpFtpHeight(self):
        num = int(ord(chr(self.bytes[20])) | ord(chr(self.bytes[21])) << 8)
        return float(num) * 0.1 - 512
    def set_LtpFtpHeight(self, value):
        num = int(round((value + 512) * 10))
        self.bytes[20] = Type.ByteFunc.d2b(num)
        self.bytes[21] = Type.ByteFunc.d2b(num >> 8)
        self.method_3()
    LtpFtpHeight = property(get_LtpFtpHeight, set_LtpFtpHeight, None, None)

    def get_LtpFtpLatitude(self):
        num = ord(chr(self.bytes[12])) | ord(chr(self.bytes[13])) << 8 | ord(chr(self.bytes[14])) << 16 | ord(chr(self.bytes[15])) << 24
        return float(num) * 0.0005 / float(3600)
    def set_LtpFtpLatitude(self, value):
        num = int(round(value * 3600 / 0.0005))
        self.bytes[12] = Type.ByteFunc.d2b(num)
        self.bytes[13] = Type.ByteFunc.d2b(num >> 8)
        self.bytes[14] = Type.ByteFunc.d2b(num >> 16)
        self.bytes[15] = Type.ByteFunc.d2b(num >> 24)
        self.method_3()
    LtpFtpLatitude = property(get_LtpFtpLatitude, set_LtpFtpLatitude, None, None)

    def get_LtpFtpLongitude(self):
        num = ord(chr(self.bytes[16])) | ord(chr(self.bytes[17])) << 8 | ord(chr(self.bytes[18])) << 16 | ord(chr(self.bytes[19])) << 24
        return float(num) * 0.0005 / float(3600)
    def set_LtpFtpLongitude(self, value):
        num = int(round(value * 3600 / 0.0005))
        self.bytes[16] = Type.ByteFunc.d2b(num)
        self.bytes[17] = Type.ByteFunc.d2b(num >> 8)
        self.bytes[18] = Type.ByteFunc.d2b(num >> 16)
        self.bytes[19] = Type.ByteFunc.d2b(num >> 24)
        self.method_3()
    LtpFtpLongitude = property(get_LtpFtpLongitude, set_LtpFtpLongitude, None, None)

    def get_OperationType(self):
        return self.FasDbOperationType[ord(chr(self.bytes[0])) & 15]
    def set_OperationType(self, value):
        self.bytes[0] = Type.ByteFunc.d2b(ord(chr(self.bytes[0])) ^ (ord(chr(self.bytes[0])) ^ value) & 15)
        self.method_3()
    OperationType = property(get_OperationType, set_OperationType, None, None)

    def get_ReferencePathDataSelector(self):
        return self.bytes[7]
    def set_ReferencePathDataSelector(self, value):
        self.bytes[7] = value
        self.method_3()
    ReferencePathDataSelector = property(get_ReferencePathDataSelector, set_ReferencePathDataSelector, None, None)

    def get_ReferencePathIdentifier(self):
        num = 8
        chrArray = ['','','','']
        i = 3
        while i>=0:
            if (ord(chr(self.bytes[num])) >= 32):
                chrArray[i] = chr(ord(chr(self.bytes[num])))
            else:
                chrArray[i] = chr(ord(chr(self.bytes[num])) | 64)
            num += 1
            i -= 1
        return String.CharArray2Str(chrArray)
    def set_ReferencePathIdentifier(self, value):
        num = 8
        value = "<doc>"
        while (len(value) < 4):
            value = String.Concat([value, " "])
        charArray = String.ToCharArray(value, 0, 4)
        i = 3
        while i >= 0:
            self.bytes[num] = Type.ByteFunc.d2b(ord(charArray[i]) & ord('?'))
            num += 1
            i -= 1
        self.method_3()
    ReferencePathIdentifier = property(get_ReferencePathIdentifier, set_ReferencePathIdentifier, None, None)

    def get_RouteIndicator(self):
        num = Type.ByteFunc.d2b((ord(chr(self.bytes[6])) & 248) >> 3)
        if (ord(num) == 0):
            return " "
        chrArray = [chr(ord(num) | 64) ]
        return String.CharArray2Str(chrArray)
    def set_RouteIndicator(self, value):
        num = None

        while (len(value) < 1):
            value = QString(" ")
        chrC = value[0].toAscii()[0] 
        if (value == " "):
            num = Type.ByteFunc.d2b(0)
        else:
            num = Type.ByteFunc.d2b(ord(chrC) & 63)
        num1 = num
        self.bytes[6] = Type.ByteFunc.d2b(ord(chr(self.bytes[6])) ^ ((ord(chr(self.bytes[6])) ^ ord(num1) << 3) & 248))
        self.method_3()
    RouteIndicator = property(get_RouteIndicator, set_RouteIndicator, None, None)

    def get_RunwayLetter(self):
        return self.FasDbRunwayLetter[ord(chr(self.bytes[5])) >> 6]
    def set_RunwayLetter(self, value):
        num = Type.ByteFunc.d2b(value)
        self.bytes[5] = Type.ByteFunc.d2b(ord(chr(self.bytes[5])) ^ ((ord(chr(self.bytes[5])) ^ ord(num) << 6) & 192))
        self.method_3()
    RunwayLetter = property(get_RunwayLetter, set_RunwayLetter, None, None)

    def get_RunwayNumber(self):
        return ord(chr(self.bytes[5])) & 63
    def set_RunwayNumber(self, value):
        self.bytes[5] = Type.ByteFunc.d2b(ord(chr(self.bytes[5])) ^ ((ord(chr(self.bytes[5])) ^ ord(value)) & 63))
        self.method_3()
    RunwayNumber = property(get_RunwayNumber, set_RunwayNumber, None, None)

    def get_SbasProviderId(self):
        return self.FasDbSbasServiceProvider[ord(chr(self.bytes[0])) >> 4]
    def set_SbasProviderId(self, value):
        num = Type.ByteFunc.d2b(value)
        self.bytes[0] = Type.ByteFunc.d2b(ord(chr(self.bytes[0])) ^ ((ord(chr(self.bytes[0])) ^ ord(num) << 4) & 240))
        self.method_3()
    SbasProviderId = property(get_SbasProviderId, set_SbasProviderId, None, None)

    def get_VAL(self):
        return float(ord(chr(self.bytes[35])) * 0.2)
    def set_VAL(self, value):
        self.bytes[35] = Type.ByteFunc.d2b(int(round(value * 5)))
        self.method_3()
    VAL = property(get_VAL, set_VAL, None, None)

    def method_0(self, double_0, fasDbApproachTchUnits_0):
        num = None
        num = (fasDbApproachTchUnits_0 != FasDbApproachTchUnits.m) and int(int(round(double_0 * 10)) & -32769) or int(int(round(double_0 * 20)) | 32768)
        self.bytes[28] = Type.ByteFunc.d2b(num)
        self.bytes[29] = Type.ByteFunc.d2b(num >> 8)
        self.method_3()

    def method_1(self, string_0):
        fileStream = open(string_0, 'r')
        n = fileStream.readinto(self.bytes)
        fileStream.close()

        pass
        # using (FileStream fileStream = new FileStream(string_0, FileMode.Open))
        # {
        #     if (fileStream.Length != (long)40)
        #     {
        #         throw new Exception(string.Format(Messages.ERR_FAS_DB_INVALID_BIN_FILE, string_0))
        #     }
        #     using (BinaryReader binaryReader = new BinaryReader(fileStream))
        #     {
        #         self.bytes = binaryReader.ReadBytes(40)

    def method_2(self, string_0):
        fileStream = open(string_0, 'wb')
        fileStream.write(self.bytes)
        fileStream.close()
        pass
        # using (FileStream fileStream = new FileStream(string_0, FileMode.OpenOrCreate))
        # {
        #     using (BinaryWriter binaryWriter = new BinaryWriter(fileStream))
        #     {
        #         binaryWriter.Write(self.bytes)
    def method_3(self):
        num = FasDataBlockFile.smethod_0(self.bytes, 36)
        self.bytes[36] = Type.ByteFunc.d2b(num)
        self.bytes[37] = Type.ByteFunc.d2b(num >> 8)
        self.bytes[38] = Type.ByteFunc.d2b(num >> 16)
        self.bytes[39] = Type.ByteFunc.d2b(num >> 24)

    @staticmethod
    def smethod_0(byte_0, int_0):
        numArray = [0, 2577006594, 2553349383, 27985157, 2607222541, 50138895, 55970314, 2597063176, 2647333657, 72424219, 100277790, 2623544860, 111940628, 2671121430, 2661093651, 117903633, 2425566001, 151597875, 144848438, 2436380212, 200555580, 2456697918, 2479175995, 174012729, 223881256, 2495752234, 2506698031, 217263405, 2520721189, 262481703, 235807266, 2543067680, 2317575009, 330916707, 303195750, 2340972132, 289696876, 2296278126, 2306173291, 284125545, 401111160, 2389866618, 2413395327, 373521789, 2358212469, 353728375, 348025458, 2367976048, 447762512, 2200588370, 2189514071, 454776149, 2178375517, 407723871, 434526810, 2155633240, 2273004361, 518081355, 524963406, 2261798476, 471614532, 2240169030, 2217558339, 498549057, 3208889281, 651805635, 661833414, 3202926276, 606391500, 3183398094, 3155544523, 630180297, 579393752, 3138574554, 3132743135, 589553117, 3119503317, 544593879, 568251090, 3091518160, 802222320, 3058364658, 3085039095, 779875829, 3031957501, 757989375, 747043578, 3038575352, 2988174313, 729934827, 707456750, 3014717164, 696050916, 2967921894, 2974671331, 685236705, 895525024, 2902106274, 2907809191, 885761445, 2919739309, 933081007, 909552298, 2947328680, 2829827001, 825342907, 815447742, 2835398332, 869053620, 2857809078, 2885530035, 845656497, 2784203665, 1013552019, 1036162710, 2757269140, 1049926812, 2802752670, 2795870619, 1061132697, 943229064, 2711783562, 2684980623, 965971341, 2740946821, 986023815, 997098114, 2733933184, 3582100097, 1276674691, 1303611270, 3559491460, 1323666828, 3615460750, 3604252811, 1330546825, 1212783000, 3520305562, 3497565343, 1239587997, 3543045781, 1253349015, 1260360594, 3531969424, 1158787504, 3700142514, 3709908151, 1153086645, 3732324029, 1206697663, 1179106234, 3755850680, 3638209193, 1094757035, 1089187758, 3648106412, 1136502180, 3660031398, 3683426467, 1108779169, 1604444640, 3325813218, 3348161767, 1577772261, 3301371629, 1566371567, 1559751658, 3312315368, 3261790969, 1542519547, 1515978750, 3284271100, 1494087156, 3231184374, 3241996531, 1487335665, 3476214481, 1453904595, 1459869654, 3466188756, 1414913500, 3452952030, 3429161179, 1442765017, 1392101832, 3412314570, 3402157263, 1397935309, 3382625989, 1342490311, 1370473410, 3358966720, 1791050048, 4082843970, 4075832391, 1802126405, 4054208077, 1748782671, 1771522890, 4027403080, 4144650841, 1854954075, 1866162014, 4137770844, 1819104596, 4126627158, 4099690579, 1841713233, 4199707249, 1674080883, 1650685814, 4227430260, 1630895484, 4172250494, 4177819771, 1620998265, 1738107240, 4261636458, 4289227887, 1714580589, 4244530789, 1701078631, 1691312994, 4250231648, 3772916257, 2037916195, 2027104038, 3779667748, 2072325420, 3793693998, 3820234795, 2049845289, 2099853624, 3836950842, 3843570751, 2088909885, 3863885365, 2144613943, 2122265394, 3890557744, 1886458128, 3924496658, 3896513559, 1910117397, 3944095261, 1921785375, 1931942682, 3938261784, 3988392457, 1948256779, 1972047630, 3960540940, 1994196228, 4014408966, 4008443907, 2004221953]
        num = 0
        for i in range(int_0):
            byte0 = Type.ByteFunc.d2b(num ^ ord(chr(byte_0[i])))
            num = num >> 8
            num = num ^ numArray[ord(byte0)]
        return num

    @staticmethod
    def CRC_Calculation(byteArray):
        numArray = [0, 2577006594, 2553349383, 27985157, 2607222541, 50138895, 55970314, 2597063176, 2647333657, 72424219, 100277790, 2623544860, 111940628, 2671121430, 2661093651, 117903633, 2425566001, 151597875, 144848438, 2436380212, 200555580, 2456697918, 2479175995, 174012729, 223881256, 2495752234, 2506698031, 217263405, 2520721189, 262481703, 235807266, 2543067680, 2317575009, 330916707, 303195750, 2340972132, 289696876, 2296278126, 2306173291, 284125545, 401111160, 2389866618, 2413395327, 373521789, 2358212469, 353728375, 348025458, 2367976048, 447762512, 2200588370, 2189514071, 454776149, 2178375517, 407723871, 434526810, 2155633240, 2273004361, 518081355, 524963406, 2261798476, 471614532, 2240169030, 2217558339, 498549057, 3208889281, 651805635, 661833414, 3202926276, 606391500, 3183398094, 3155544523, 630180297, 579393752, 3138574554, 3132743135, 589553117, 3119503317, 544593879, 568251090, 3091518160, 802222320, 3058364658, 3085039095, 779875829, 3031957501, 757989375, 747043578, 3038575352, 2988174313, 729934827, 707456750, 3014717164, 696050916, 2967921894, 2974671331, 685236705, 895525024, 2902106274, 2907809191, 885761445, 2919739309, 933081007, 909552298, 2947328680, 2829827001, 825342907, 815447742, 2835398332, 869053620, 2857809078, 2885530035, 845656497, 2784203665, 1013552019, 1036162710, 2757269140, 1049926812, 2802752670, 2795870619, 1061132697, 943229064, 2711783562, 2684980623, 965971341, 2740946821, 986023815, 997098114, 2733933184, 3582100097, 1276674691, 1303611270, 3559491460, 1323666828, 3615460750, 3604252811, 1330546825, 1212783000, 3520305562, 3497565343, 1239587997, 3543045781, 1253349015, 1260360594, 3531969424, 1158787504, 3700142514, 3709908151, 1153086645, 3732324029, 1206697663, 1179106234, 3755850680, 3638209193, 1094757035, 1089187758, 3648106412, 1136502180, 3660031398, 3683426467, 1108779169, 1604444640, 3325813218, 3348161767, 1577772261, 3301371629, 1566371567, 1559751658, 3312315368, 3261790969, 1542519547, 1515978750, 3284271100, 1494087156, 3231184374, 3241996531, 1487335665, 3476214481, 1453904595, 1459869654, 3466188756, 1414913500, 3452952030, 3429161179, 1442765017, 1392101832, 3412314570, 3402157263, 1397935309, 3382625989, 1342490311, 1370473410, 3358966720, 1791050048, 4082843970, 4075832391, 1802126405, 4054208077, 1748782671, 1771522890, 4027403080, 4144650841, 1854954075, 1866162014, 4137770844, 1819104596, 4126627158, 4099690579, 1841713233, 4199707249, 1674080883, 1650685814, 4227430260, 1630895484, 4172250494, 4177819771, 1620998265, 1738107240, 4261636458, 4289227887, 1714580589, 4244530789, 1701078631, 1691312994, 4250231648, 3772916257, 2037916195, 2027104038, 3779667748, 2072325420, 3793693998, 3820234795, 2049845289, 2099853624, 3836950842, 3843570751, 2088909885, 3863885365, 2144613943, 2122265394, 3890557744, 1886458128, 3924496658, 3896513559, 1910117397, 3944095261, 1921785375, 1931942682, 3938261784, 3988392457, 1948256779, 1972047630, 3960540940, 1994196228, 4014408966, 4008443907, 2004221953]
        num = 0
        j = 0

        progressMessageBar = define._messagBar.createMessage("Reading the file ...")
        progress = QProgressBar()
        progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        progressMessageBar.layout().addWidget(progress)
        define._messagBar.pushWidget(progressMessageBar, define._messagBar.INFO)
        maxium = len(byteArray)
        progress.setMaximum(maxium)
        progress.setValue(0)

        for i in range(len(byteArray)):
            byte0 = None
            if isinstance(byteArray, bytearray):
                byte0 = Type.ByteFunc.d2b(num ^ ord(chr(byteArray[i])))
            else:
                byte0 = Type.ByteFunc.d2b(num ^ ord(byteArray[i]))
            num = num >> 8
            num = num ^ numArray[ord(byte0) % 36]
            progress.setValue(i)
            QApplication.processEvents()
        progress.setValue(maxium)
        define._messagBar.hide()

        resultByteArray = bytearray(4)
        for i in range(4):
            resultByteArray[i] = '0'
        resultByteArray[0] = Type.ByteFunc.d2b(num)
        resultByteArray[1] = Type.ByteFunc.d2b(num >> 8)
        resultByteArray[2] = Type.ByteFunc.d2b(num >> 16)
        resultByteArray[3] = Type.ByteFunc.d2b(num >> 24)

        stringBuilder = StringBuilder()
        for i in range(4):
            stringBuilder.Append(hex(ord(chr(resultByteArray[i]))).replace("0x", "").upper())
        return stringBuilder.ToString()





