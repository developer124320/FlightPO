from PyQt4.QtCore import QFileInfo

from FlightPlanner.types import CodeCatAcftAixm, CodeTypeApchAixm
from Type.DataRow import DataRow
from Type.String import String
from Type.DataBaseProcedureData import DataBaseProcedureData
from Type.DataBaseProcedureLegs import DataBaseProcedureLegs, DataBaseProcedureLegsEx

class DataBase:
    def __init__(self, string_0):
        self.fileName = string_0;
        self.symbols = DataBaseSymbols();
        self.obstacles = DataBaseObstacles();
        self.routes = DataBaseRoutes();
        self.airspace = DataBaseAirspace();
        self.contours = DataBaseContours();
        self.procedures = DataBaseProcedures();
        self.geoBorder = DataBaseGeoBorder();
        self.procData = DataBaseProcedureData();
        self.sids = DataBaseSIDs();
        self.stars = DataBaseSTARs();
        self.iaps = DataBaseIAPs();
        self.holdings = DataBaseHoldings();

        self.version = None;
        self.effectiveDate = None;
        self.isDisposed = False;

    def get_Airspace(self):
        return self.airspace
    Airspace = property(get_Airspace, None, None, None)

    def get_Contours(self):
        return self.contours
    Contours = property(get_Contours, None, None, None)

    def get_EffectiveDate(self):
        return self.effectiveDate
    def set_EffectiveDate(self, value):
        self.effectiveDate = value
    EffectiveDate = property(get_EffectiveDate, set_EffectiveDate, None, None)

    def get_FileName(self):
        return self.fileName
    FileName = property(get_FileName, None, None, None)

    def get_GeoBorder(self):
        return self.geoBorder
    GeoBorder = property(get_GeoBorder, None, None, None)

    def get_Holdings(self):
        return self.holdings
    Holdings = property(get_Holdings, None, None, None)

    def get_IAPs(self):
        return self.iaps
    IAPs = property(get_IAPs, None, None, None)

    def get_IsDisposed(self):
        return self.isDisposed
    IsDisposed = property(get_IsDisposed, None, None, None)

    def get_Obstacles(self):
        return self.obstacles
    Obstacles = property(get_Obstacles, None, None, None)

    def get_ProcedureData(self):
        return self.procData
    ProcedureData = property(get_ProcedureData, None, None, None)

    def get_Procedures(self):
        return self.procedures
    Procedures = property(get_Procedures, None, None, None)

    def get_Routes(self):
        return self.routes
    Routes = property(get_Routes, None, None, None)

    def get_SIDs(self):
        return self.sids
    SIDs = property(get_SIDs, None, None, None)

    def get_STARs(self):
        return self.stars
    STARs = property(get_STARs, None, None, None)

    def get_Symbols(self):
        return self.symbols
    Symbols = property(get_Symbols, None, None, None)

    def get_Version(self):
        return self.version
    def set_Version(self, value):
        self.version = value
    Version = property(get_Version, None, None, None)

    def get_HasAirspace(self):
        return self.airspace.RowsCount() > 0
    HasAirspace = property(get_HasAirspace, None, None, None)

    def get_HasContours(self):
        return self.contours.RowsCount() > 0
    HasContours = property(get_HasContours, None, None, None)

    def get_HasGeoBorder(self):
        return self.geoBorder.RowsCount() > 0
    HasGeoBorder = property(get_HasGeoBorder, None, None, None)

    def get_HasObstacles(self):
        return self.obstacles.RowsCount() > 0
    HasObstacles = property(get_HasObstacles, None, None, None)

    def get_HasProcedures(self):
        return self.procedures.RowsCount() > 0
    HasProcedures = property(get_HasProcedures, None, None, None)

    def get_HasRoutes(self):
        return self.routes.RowsCount() > 0
    HasRoutes = property(get_HasRoutes, None, None, None)

    def get_HasSymbols(self):
        return self.symbols.RowsCount() > 0
    HasSymbols = property(get_HasSymbols, None, None, None)

    def get_Title(self):
        fileInfo = QFileInfo(self.fileName)
        return String.QString2Str(fileInfo.fileName())
    Title = property(get_Title, None, None, None)
    
    
    def method_0(self, string_0, double_0, double_1, degrees_0, degrees_1, altitude_0, symbol_0, symbolAttributes_0):
        return self.symbols.method_0(string_0, double_0, double_1, degrees_0, degrees_1, altitude_0, symbol_0, symbolAttributes_0);

    def method_1(self, string_0, degrees_0, degrees_1, altitude_0, symbol_0, symbolAttributes_0):
        return self.symbols.method_0(string_0, None, None, degrees_0, degrees_1, altitude_0, symbol_0, symbolAttributes_0);

    def method_2(self, string_0, double_0, double_1, degrees_0, degrees_1, altitude_0, symbol_0, symbolAttributes_0):
        return self.obstacles.method_0(string_0, double_0, double_1, degrees_0, degrees_1, altitude_0, symbol_0, symbolAttributes_0);

    def method_3(self, string_0, degrees_0, degrees_1, altitude_0, symbol_0, symbolAttributes_0):
        return self.obstacles.method_0(string_0, None, None, degrees_0, degrees_1, altitude_0, symbol_0, symbolAttributes_0);

    def method_4(self, string_0, dataBaseCoordinates_0):
        return self.routes.method_0(string_0, dataBaseCoordinates_0);

    def method_5(self, string_0, altitude_0, altitude_1, distance_0, dataBaseCoordinates_0):
        return self.airspace.method_0(string_0, altitude_0, altitude_1, distance_0, dataBaseCoordinates_0);

    def method_6(self, string_0, altitude_0, altitude_1, distance_0, bool_0, bool_1, dataBaseCoordinates_0):
        return self.airspace.method_1(string_0, altitude_0, altitude_1, distance_0, bool_0, bool_1, dataBaseCoordinates_0);

    def method_7(self, string_0, dataBaseGeoBorderType_0, dataBaseCoordinates_0):
        return self.geoBorder.method_0(string_0, dataBaseGeoBorderType_0, dataBaseCoordinates_0);

    def method_8(self, string_0, altitude_0, bool_0, dataBaseCoordinates_0):
        return self.contours.method_0(string_0, altitude_0, bool_0, dataBaseCoordinates_0);

    def method_9(self, string_0, bool_0, dataBaseCoordinates_0):
        return self.procedures.method_0(string_0, bool_0, dataBaseCoordinates_0);









class DataBaseSymbols(list):
    def __init__(self):
        list.__init__(self)

        self.nameList = ["Name", "X", "Y", "Latitude", "Longitude",
                         "Altitude", "Type", "Remarks", "Attributes", "Symbol"]
    def NewRow(self):
        return DataRow(self.nameList)
    def RowsAdd(self, dataRow):
        self.append(dataRow)

    def RowsCount(self):
        return len(self)
    def ColumnsCount(self):
        return len(self.nameList)

    def method_0(self, string_0, double_0, double_1, degrees_0, degrees_1, altitude_0, symbol_0, symbolAttributes_0):
        string0 = self.NewRow();
        string0.setItem(0, string_0);
        string0.setItem(1, double_0);
        string0.setItem(2, double_1);
        string0.setItem(3, degrees_0);
        string0.setItem(4, degrees_1);
        string0.setItem(5, altitude_0);
        string0.setItem(6, symbol_0.Type);
        if (symbolAttributes_0 != None and len(symbolAttributes_0) != 0):
            string0.setItem(7, symbolAttributes_0.Remarks);
            string0.setItem(8, symbolAttributes_0);
        string0.setItem(9, symbol_0);
        self.RowsAdd(string0);
        return string0;

    def method_1(self, string_0, degrees_0, degrees_1, altitude_0, symbol_0, symbolAttributes_0):
        return self.method_0(string_0, None, None, degrees_0, degrees_1, altitude_0, symbol_0, symbolAttributes_0);
    def method_2(self, degrees_0, degrees_1, symbolType_0):
        strS = "";
        dataRowArray = []
        for i in range(len(symbolType_0)):
            for data in self:
                if data["Type"] == symbolType_0[i]:
                    dataRowArray.append(data)
                    break
            # strS = (i >= len(symbolType_0) - 1) and String.Concat([strS, "(Type = '{0}')".format(symbolType_0[i])]) or String.Concat([strS, "(Type = '{0}') OR ".format(symbolType_0[i])]);
        # dataRowArray = base.Select(strS);
        for j in range(len(dataRowArray)):
            dataRow = dataRowArray[j];
            if (dataRow["Latitude"] == degrees_0 and dataRow["Longitude"] == degrees_1):
                return dataRow;
        return None;

    def get_UsedTypes(self):
        strs = [];
        for row in self:
            strS = row["Type"];
            try:
                index = strs.index(strS)
                continue;
            except:
                strs.append(strS);
        strs.sort();
        strs.insert(0, "");
        return strs;
    UsedTypes = property(get_UsedTypes, None, None, None)

class DataBaseObstacles(list):
    def __init__(self):
        list.__init__(self)

        self.nameList = ["Name", "X", "Y", "Latitude", "Longitude",
                         "Altitude", "Type", "Remarks", "Attributes", "Symbol"]
    def NewRow(self):
        return DataRow(self.nameList)
    def RowsAdd(self, dataRow):
        self.append(dataRow)
    def RowsCount(self):
        return len(self)
    def ColumnsCount(self):
        return len(self.nameList)

    def method_0(self, string_0, double_0, double_1, degrees_0, degrees_1, altitude_0, symbol_0, symbolAttributes_0):
        string0 = self.NewRow();
        string0.setItem(0, string_0);
        string0.setItem(1, double_0);
        string0.setItem(2, double_1);
        string0.setItem(3, degrees_0);
        string0.setItem(4, degrees_1);
        string0.setItem(5, altitude_0);
        string0.setItem(6, symbol_0.Type);
        if (symbolAttributes_0 != None and len(symbolAttributes_0) != 0):
            string0.setItem(7, symbolAttributes_0.Remarks);
            string0.setItem(8, symbolAttributes_0);
        string0.setItem(9, symbol_0);
        self.RowsAdd(string0);
        return string0;

    def method_1(self, string_0, degrees_0, degrees_1, altitude_0, symbol_0, symbolAttributes_0):
        return self.method_0(string_0, None, None, degrees_0, degrees_1, altitude_0, symbol_0, symbolAttributes_0);
    def method_2(self, degrees_0, degrees_1, symbolType_0):
        strS = "";
        dataRowArray = []
        for i in range(len(symbolType_0)):
            for data in self:
                if data["Type"] == symbolType_0[i]:
                    dataRowArray.append(data)
                    break
            # strS = (i >= len(symbolType_0) - 1) and String.Concat([strS, "(Type = '{0}')".format(symbolType_0[i])]) or String.Concat([strS, "(Type = '{0}') OR ".format(symbolType_0[i])]);
        # dataRowArray = base.Select(strS);
        for j in range(len(dataRowArray)):
            dataRow = dataRowArray[j];
            if (dataRow["Latitude"] == degrees_0 and dataRow["Longitude"] == degrees_1):
                return dataRow;
        return None;

    def get_UsedTypes(self):
        strs = [];
        for row in self:
            strS = row["Type"];
            try:
                index = strs.index(strS)
                continue;
            except:
                strs.append(strS);
        strs.sort();
        strs.insert(0, "");
        return strs;
    UsedTypes = property(get_UsedTypes, None, None, None)



class DataBaseRoutes(list):
    def __init__(self):
        list.__init__(self)

        self.nameList = ["Name", "Coordinates"]
    def NewRow(self):
        return DataRow(self.nameList)
    def RowsAdd(self, dataRow):
        self.append(dataRow)
    def RowsCount(self):
        return len(self)
    def ColumnsCount(self):
        return len(self.nameList)

    def method_0(self, string_0, dataBaseCoordinates_0):
        string0 = self.NewRow();
        string0.setItem(0, string_0);
        string0.setItem(1, dataBaseCoordinates_0);
        self.RowsAdd(string0);
        return string0;

class DataBaseAirspace(list):
    def __init__(self):
        list.__init__(self)

        self.nameList = ["Name", "LowerLimit", "UpperLimit",
                         "Radius", "Is3D", "IsClosed",
                         "Coordinates"]
    def NewRow(self):
        return DataRow(self.nameList)
    def RowsAdd(self, dataRow):
        self.append(dataRow)
    def RowsCount(self):
        return len(self)
    def ColumnsCount(self):
        return len(self.nameList)

    def method_0(self, string_0, altitude_0, altitude_1, distance_0, dataBaseCoordinates_0):
        string0 = self.NewRow();
        string0.setItem(0, string_0);
        string0.setItem(1, altitude_0);
        string0.setItem(2, altitude_1);
        string0.setItem(3, distance_0);
        string0.setItem(4, False);
        string0.setItem(5, False);
        string0.setItem(6, dataBaseCoordinates_0);
        self.RowsAdd(string0);
        return string0;
    
    def method_1(self, string_0, altitude_0, altitude_1, distance_0, bool_0, bool_1, dataBaseCoordinates_0):
        string0 = self.NewRow();
        string0.setItem(0, string_0);
        string0.setItem(1, altitude_0);
        string0.setItem(2, altitude_1);
        string0.setItem(3, distance_0);
        string0.setItem(4, bool_0);
        string0.setItem(5, bool_1);
        string0.setItem(6, dataBaseCoordinates_0);
        self.RowsAdd(string0);
        return string0;

    def method_2(self, string_0):
        if len(self) == 0:
            return None
        dataRowArray = []
        for data in self:
            if data["Name"] == string_0:
                dataRowArray.append(data)
        # dataRowArray = base.Select(string.Format("name LIKE '{0}'", string_0));
        if (len(dataRowArray) == 0):
            return None
        return dataRowArray[0];

    def method_3(self):
        num = 0;
        while (num < len(self)):
            item = self[num];
            dataBaseCoordinate = item["Coordinates"];
            if (dataBaseCoordinate == None or dataBaseCoordinate.Count == 0):
                self.remove(item);
            else:
                num += 1;

class DataBaseContours(list):
    def __init__(self):
        list.__init__(self)

        self.nameList = ["Name", "Altitude", "IsClosed",
                         "Coordinates"]
    def NewRow(self):
        return DataRow(self.nameList)
    def RowsAdd(self, dataRow):
        self.append(dataRow)
    def RowsCount(self):
        return len(self)
    def ColumnsCount(self):
        return len(self.nameList)
    def method_0(self, string_0, altitude_0, bool_0, dataBaseCoordinates_0):
        string0 = self.NewRow();
        string0.setItem(0, string_0);
        string0.setItem(1, altitude_0);
        string0.setItem(2, bool_0);
        string0.setItem(3, dataBaseCoordinates_0);
        self.RowsAdd(string0);
        return string0;


class DataBaseProcedures(list):
    def __init__(self):
        list.__init__(self)

        self.nameList = ["Name", "IsClosed", "Coordinates"]
    def NewRow(self):
        return DataRow(self.nameList)
    def RowsAdd(self, dataRow):
        self.append(dataRow)
    def RowsCount(self):
        return len(self)
    def ColumnsCount(self):
        return len(self.nameList)
    def method_0(self, string_0, bool_0, dataBaseCoordinates_0):
        string0 = self.NewRow();
        string0.setItem(0, string_0);
        string0.setItem(1, bool_0);
        string0.setItem(2, dataBaseCoordinates_0);
        self.RowsAdd(string0);
        return string0;


class DataBaseGeoBorder(list):
    def __init__(self):
        list.__init__(self)

        self.nameList = ["Name", "Type", "Coordinates"]
    def NewRow(self):
        return DataRow(self.nameList)
    def RowsAdd(self, dataRow):
        self.append(dataRow)
    def RowsCount(self):
        return len(self)
    def ColumnsCount(self):
        return len(self.nameList)

    def method_0(self, string_0, dataBaseGeoBorderType_0, dataBaseCoordinates_0):
        string0 = self.NewRow();
        string0.setItem(0, string_0);
        string0.setItem(1, dataBaseGeoBorderType_0);
        string0.setItem(2, dataBaseCoordinates_0);
        self.RowsAdd(string0);
        return string0;
    def method_1(self, string_0):
        if len(self) == 0:
            return None
        dataRowArray = []
        for data in self:
            if data["Name"] == string_0:
                dataRowArray.append(data)
        # dataRowArray = base.Select(string.Format("name LIKE '{0}'", string_0));
        if (len(dataRowArray) == 0):
            return None
        return dataRowArray[0];

    def method_2(self):
        num = 0;
        while (num < len(self)):
            item = self[num];
            dataBaseCoordinate = item["Coordinates"];
            if (dataBaseCoordinate == None or dataBaseCoordinate.Count == 0):
                self.remove(item);
            else:
                num += 1;


class DataBaseSIDs(list):
    def __init__(self):
        list.__init__(self)

        self.nameList = ["oldAhpEnt", "oldTxtDesig", "oldCodeCatAcft",
                         "oldCodeTransId", "ahpEnt", "txtDesig",
                         "codeCatAcft", "codeTransId", "rdnEnt", "mgpEnt",
                         "codeRnp", "txtDescrComFail", "codeTypeRte",
                         "txtDescr", "txtRmk", "procLegs",
                         "procLegsEx", "new", "changed",
                         "deleted"]
        self.DefaultViewRowFilter = "(deleted = false) OR (deleted Is Null)";


    def NewRow(self):
        return DataRow(self.nameList)
    def RowsAdd(self, dataRow):
        if isinstance(dataRow["procLegs"], DataBaseProcedureLegs):
            dataRow["procLegs"].refresh()
        if isinstance(dataRow["procLegsEx"], DataBaseProcedureLegsEx):
            dataRow["procLegsEx"].refresh()
        if dataRow["deleted"] == None or dataRow["deleted"] == "":
            dataRow["deleted"] = "False"
        if dataRow["new"] == None or dataRow["new"] == "":
            dataRow["new"] = "False"
        if dataRow["changed"] == None or dataRow["changed"] == "":
            dataRow["changed"] = "False"
        self.append(dataRow)
    def RowsCount(self):
        return len(self)
    def ColumnsCount(self):
        return len(self.nameList)

    def Select(self, conditionDict):
        if conditionDict == None or len(conditionDict) == 0:
            return []
        resultList = []
        for dict0 in self:
            resultList.append(dict0)
        for name in conditionDict:
            data = conditionDict[name]
            i = 0
            while i < len(resultList):
                dict0 = resultList[i]
                if data != dict0[name]:
                    resultList.pop(i)
                    continue
                i += 1
        return resultList


class DataBaseIAPs(list):
    def __init__(self):
        list.__init__(self)

        self.nameList = ["oldAhpEnt", "oldTxtDesig", "oldCodeCatAcft",
                         "oldCodeTransId", "ahpEnt", "txtDesig",
                         "codeCatAcft", "codeTransId", "rdnEnt", "mgpEnt",
                         "codeRnp", "txtDescrComFail", "codeTypeRte",
                         "txtDescrMiss", "txtRmk", "ocah", "procLegs",
                         "procLegsEx", "new", "changed",
                         "deleted"]
        self.DefaultViewRowFilter = "(deleted = false) OR (deleted Is Null)";


    def NewRow(self):
        return DataRow(self.nameList)
    def RowsAdd(self, dataRow):
        if isinstance(dataRow["procLegs"], DataBaseProcedureLegs):
            dataRow["procLegs"].refresh()
        if isinstance(dataRow["procLegsEx"], DataBaseProcedureLegsEx):
            dataRow["procLegsEx"].refresh()
        if dataRow["deleted"] == None or dataRow["deleted"] == "":
            dataRow["deleted"] = "False"
        if dataRow["new"] == None or dataRow["new"] == "":
            dataRow["new"] = "False"
        if dataRow["changed"] == None or dataRow["changed"] == "":
            dataRow["changed"] = "False"
        self.append(dataRow)
    def RowsCount(self):
        return len(self)
    def ColumnsCount(self):
        return len(self.nameList)
    def Select(self, conditionDict):
        if conditionDict == None or len(conditionDict) == 0:
            return []
        resultList = []
        for dict0 in self:
            resultList.append(dict0)
        for name in conditionDict:
            data = conditionDict[name]
            i = 0
            while i < len(resultList):
                dict0 = resultList[i]
                if data != dict0[name]:
                    resultList.pop(i)
                    continue
                i += 1
        return resultList
class DataBaseSTARs(list):
    def __init__(self):
        list.__init__(self)

        self.nameList = ["oldAhpEnt", "oldTxtDesig", "oldCodeCatAcft",
                         "oldCodeTransId", "ahpEnt", "txtDesig",
                         "codeCatAcft", "codeTransId", "mgpEnt",
                         "codeRnp", "txtDescrComFail", "codeTypeRte",
                         "txtDescr", "txtRmk", "procLegs",
                         "procLegsEx", "new", "changed",
                         "deleted"]
        self.DefaultViewRowFilter = "(deleted = false) OR (deleted Is Null)";

    def NewRow(self):
        return DataRow(self.nameList)
    def RowsAdd(self, dataRow):
        if isinstance(dataRow["procLegs"], DataBaseProcedureLegs):
            dataRow["procLegs"].refresh()
        if isinstance(dataRow["procLegsEx"], DataBaseProcedureLegsEx):
            dataRow["procLegsEx"].refresh()
        if dataRow["deleted"] == None or dataRow["deleted"] == "":
            dataRow["deleted"] = "False"
        if dataRow["new"] == None or dataRow["new"] == "":
            dataRow["new"] = "False"
        if dataRow["changed"] == None or dataRow["changed"] == "":
            dataRow["changed"] = "False"
        self.append(dataRow)
    def RowsCount(self):
        return len(self)
    def ColumnsCount(self):
        return len(self.nameList)
    def Select(self, conditionDict):
        if conditionDict == None or len(conditionDict) == 0:
            return []
        resultList = []
        for dict0 in self:
            resultList.append(dict0)
        for name in conditionDict:
            data = conditionDict[name]
            i = 0
            while i < len(resultList):
                dict0 = resultList[i]
                if data != dict0[name]:
                    resultList.pop(i)
                    continue
                i += 1
        return resultList
class DataBaseHoldings(list):
    def __init__(self):
        list.__init__(self)

        self.nameList = ["oldBasedOnEnt", "oldCodeType", "basedOnEnt",
                         "codeType", "txtDescr", "txtRmk", "procLegs",
                         "procLegsEx", "new", "changed",
                         "deleted"]
        self.DefaultViewRowFilter = "(deleted = false) OR (deleted Is Null)";


    def NewRow(self):
        return DataRow(self.nameList)
    def RowsAdd(self, dataRow):
        if isinstance(dataRow["procLegs"], DataBaseProcedureLegs):
            dataRow["procLegs"].refresh()
        if isinstance(dataRow["procLegsEx"], DataBaseProcedureLegsEx):
            dataRow["procLegsEx"].refresh()
        if dataRow["deleted"] == None or dataRow["deleted"] == "":
            dataRow["deleted"] = "False"
        if dataRow["new"] == None or dataRow["new"] == "":
            dataRow["new"] = "False"
        if dataRow["changed"] == None or dataRow["changed"] == "":
            dataRow["changed"] = "False"
        self.append(dataRow)
    def RowsCount(self):
        return len(self)
    def ColumnsCount(self):
        return len(self.nameList)
    def Select(self, conditionDict):
        if conditionDict == None or len(conditionDict) == 0:
            return []
        resultList = []
        for dict0 in self:
            resultList.append(dict0)
        for name in conditionDict:
            data = conditionDict[name]
            i = 0
            while i < len(resultList):
                dict0 = resultList[i]
                if data != dict0[name]:
                    resultList.pop(i)
                    continue
                i += 1
        return resultList

class DataBaseCoordinate:
    def __init__(self, double_0, double_1, degrees_0, degrees_1, altitude_0, degrees_2, degrees_3, dataBaseCoordinateType_0, symbolAttributes_0):
        self.x = None;
        self.y = None;
        self.latitude = None;
        self.longitude = None;
        self.altitude = None;
        self.centerLatitude = None;
        self.centerLongitude = None;
        self.type = None;
        self.attributes = None;
        self.variation = None;
        if double_0 == None and double_1 == None and degrees_2 == None and degrees_3 == None:
            self.latitude = degrees_0;
            self.longitude = degrees_1;
            self.altitude = altitude_0;
            self.type = dataBaseCoordinateType_0;
            self.attributes = symbolAttributes_0;
        elif degrees_2 == None and degrees_3 == None:
            self.x = double_0;
            self.y = double_1;
            self.latitude = degrees_0;
            self.longitude = degrees_1;
            self.altitude = altitude_0;
            self.type = dataBaseCoordinateType_0;
            self.attributes = symbolAttributes_0;
        elif degrees_3 == None:
            self.x = double_0;
            self.y = double_1;
            self.latitude = degrees_0;
            self.longitude = degrees_1;
            self.altitude = altitude_0;
            self.variation = degrees_2;
            self.type = dataBaseCoordinateType_0;
            self.attributes = symbolAttributes_0;
        else:
            self.x = double_0;
            self.y = double_1;
            self.latitude = degrees_0;
            self.longitude = degrees_1;
            self.altitude = altitude_0;
            self.centerLatitude = degrees_2;
            self.centerLongitude = degrees_3;
            self.type = dataBaseCoordinateType_0;
            self.attributes = symbolAttributes_0;

    def get_attributes(self):
        return self.attributes
    def set_attributes(self, value):
        self.attributes = value
    Attributes = property(get_attributes, set_attributes, None, None)

    def get_altitude(self):
        return self.altitude
    def set_altitude(self, value):
        self.altitude = value
    Altitude = property(get_altitude, set_altitude, None, None)

    def get_centerLatitude(self):
        return self.centerLatitude
    def set_centerLatitude(self, value):
        self.centerLatitude = value
    CenterLatitude = property(get_centerLatitude, set_centerLatitude, None, None)

    def get_centerLongitude(self):
        return self.centerLongitude
    def set_centerLongitude(self, value):
        self.centerLongitude = value
    CenterLongitude = property(get_centerLongitude, set_centerLongitude, None, None)

    def get_latitude(self):
        return self.latitude
    def set_latitude(self, value):
        self.latitude = value
    Latitude = property(get_latitude, set_latitude, None, None)

    def get_longitude(self):
        return self.longitude
    def set_longitude(self, value):
        self.longitude = value
    Longitude = property(get_longitude, set_longitude, None, None)

    def get_type(self):
        return self.type
    def set_type(self, value):
        self.type = value
    Type = property(get_type, set_type, None, None)

    def get_variation(self):
        return self.variation
    def set_variation(self, value):
        self.variation = value
    Variation = property(get_variation, set_variation, None, None)

    def get_x(self):
        return self.x
    def set_x(self, value):
        self.x = value
    X = property(get_x, set_x, None, None)

    def get_y(self):
        return self.y
    def set_y(self, value):
        self.y = value
    Y = property(get_y, set_y, None, None)

class DataBaseCoordinates(list):
    def __init__(self, dataBaseCoordinatesType_0):
        self.type = dataBaseCoordinatesType_0;
        pass
    def method_0(self, degrees_0, degrees_1, altitude_0, dataBaseCoordinateType_0, symbolAttributes_0):
        dataBaseCoordinate = DataBaseCoordinate(None, None, degrees_0, degrees_1, altitude_0, None, None, dataBaseCoordinateType_0, symbolAttributes_0);
        self.append(dataBaseCoordinate);
        return dataBaseCoordinate;
    def method_1(self, double_0, double_1, degrees_0, degrees_1, altitude_0, dataBaseCoordinateType_0, symbolAttributes_0):
        dataBaseCoordinate = DataBaseCoordinate(double_0, double_1, degrees_0, degrees_1, altitude_0, None, None, dataBaseCoordinateType_0, symbolAttributes_0);
        self.append(dataBaseCoordinate);
        return dataBaseCoordinate;
    def  method_2(self, double_0, double_1, degrees_0, degrees_1, altitude_0, degrees_2, dataBaseCoordinateType_0, symbolAttributes_0):
        dataBaseCoordinate = DataBaseCoordinate(double_0, double_1, degrees_0, degrees_1, altitude_0, degrees_2, None, dataBaseCoordinateType_0, symbolAttributes_0);
        self.append(dataBaseCoordinate);
        return dataBaseCoordinate;
    def method_3(self, double_0, double_1, degrees_0, degrees_1, altitude_0, degrees_2, degrees_3, dataBaseCoordinateType_0, symbolAttributes_0):
        dataBaseCoordinate = DataBaseCoordinate(double_0, double_1, degrees_0, degrees_1, altitude_0, degrees_2, degrees_3, dataBaseCoordinateType_0, symbolAttributes_0);
        self.append(dataBaseCoordinate);
        return dataBaseCoordinate;
    def method_4(self):
        self = []
    def method_5(self, dataBaseCoordinate_0):
        return self.index(dataBaseCoordinate_0);
    def method_6(self, dataBaseCoordinate_0):
        self.remove(dataBaseCoordinate_0);
    def method_7(self, int_0):
        self.pop(int_0);

    def get_Count(self):
        return len(self)
    Count = property(get_Count, None, None, None)

    def get_List(self):
        return self
    List = property(get_List, None, None, None)

    def get_Type(self):
        return self.type
    Type = property(get_Type, None, None, None)

    def __eq__(self, other):
        if (other == None):
            return 0;
        return self.Count == other.Count;

class DataBaseIapOcaOch:
    def __init__(self):
        self.CodeCatAcft = CodeCatAcftAixm.Other;
        self.CodeTypeApch = CodeTypeApchAixm.OTHER;
        self.ValOca = None;
        self.ValOch = None;
        self.CodeRefOch = None;
        self.TxtRmk = None;
        
        self.nameList = ["Ac. Category", "Approach Type", "OCA", "OCH", "OCH Ref.", "Remarks"]
        self.dataList = []
    def refresh(self):
        self.dataList = [self.CodeCatAcft, self.CodeTypeApch,
                          self.ValOca, self.ValOch,
                          self.CodeRefOch, self.TxtRmk]
    def method_0(self):
        dataBaseIapOcaOch = DataBaseIapOcaOch()
        dataBaseIapOcaOch.CodeCatAcft = self.CodeCatAcft,
        dataBaseIapOcaOch.CodeTypeApch = self.CodeTypeApch,
        dataBaseIapOcaOch.ValOca = self.ValOca,
        dataBaseIapOcaOch.ValOch = self.ValOch,
        dataBaseIapOcaOch.CodeRefOch = self.CodeRefOch,
        dataBaseIapOcaOch.TxtRmk = self.TxtRmk
        dataBaseIapOcaOch.dataList = [dataBaseIapOcaOch.CodeCatAcft, dataBaseIapOcaOch.CodeTypeApch,
                                      dataBaseIapOcaOch.ValOca, dataBaseIapOcaOch.ValOch,
                                      dataBaseIapOcaOch.CodeRefOch, dataBaseIapOcaOch.TxtRmk]
        return dataBaseIapOcaOch;
    def ToString(self):
        return "DataBaseIapOcaOch"
class DataBaseIapOcaOchs(list):
    def __init__(self):
        list.__init__(self)
    def Add(self, dataBaseIapOcaOch1):
        self.append(dataBaseIapOcaOch1)
    def method_0(self):
        dataBaseIapOcaOch = DataBaseIapOcaOchs();
        for dataBaseIapOcaOch1 in self:
            dataBaseIapOcaOch.Add(dataBaseIapOcaOch1.method_0());
        return dataBaseIapOcaOch;
    def refresh(self):
        if len(self) == 0:
            return
        for item in self:
            item.refresh()
    def ToString(self):
        return "DataBaseIapOcaOchs"
