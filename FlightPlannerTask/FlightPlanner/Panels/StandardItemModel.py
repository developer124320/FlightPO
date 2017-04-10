from PyQt4.QtCore import QString

from PyQt4.QtGui import QStandardItem, QStandardItemModel

class StandardItemModelQA(QStandardItemModel):
    def __init__(self = None):
        QStandardItemModel.__init__(self)
        self.selectedIndex = None

class StandardItemModel(QStandardItemModel):
    def __init__(self = None, data0 = None, hLabelArray = None):
        QStandardItemModel.__init__(self)
        self.dataSource = None
        self.hLabelList = []

        if hLabelArray != None:
            for name in hLabelArray:
                self.hLabelList.append(name)
            self.hLabelList.append("rowID")
            self.setHorizontalHeaderLabels(self.hLabelList)
        self.dataType = None
        if data0 != None:
            if isinstance(data0[0], dict):
                for name in data0[0]:
                    self.hLabelList.append(name)
                self.hLabelList.append("rowID")
                self.setHorizontalHeaderLabels(self.hLabelList)
                self.dataType = "dict"
            elif isinstance(data0[0] , list):
                self.dataType = "list"
            self.DataSource = data0
            self.dataSource = data0
            
            
        self.readOnly = True

    def Refresh(self, data0):
        self.DataSource = data0
    def get_ReadOnly(self):
        return self.readOnly
    def set_ReadOlny(self, val):
        self.readOnly = val
    ReadOnly = property(get_ReadOnly, set_ReadOlny, None, None)



    def get_DataSource(self):
        return self.dataSource
    def set_DataSource(self, data0):
        ######------------ dataSource : list of dictionary  ---------######
        if data0 == None or len(data0) == 0:
            return
        self.hLabelList = []
        self.clear()
        if isinstance(data0[0], dict):
            for name in data0.nameList:
                self.hLabelList.append(name)
            self.hLabelList.append("rowID")
            self.setHorizontalHeaderLabels(self.hLabelList)
        elif isinstance(data0[0], list):
            if len(self.hLabelList) != 0:
                self.setHorizontalHeaderLabels(self.hLabelList)
        else:
            for name in data0[0].nameList:
                self.hLabelList.append(name)
            self.hLabelList.append("rowID")
            self.setHorizontalHeaderLabels(self.hLabelList)
        for i in range(len(data0)):
            item = QStandardItem(str(i))
            self.setItem(i, len(self.hLabelList) - 1, item)
            if isinstance(data0[0], dict):
                # for name in data0[0]:
                #     self.hLabelList.append(name)
                # self.setHorizontalHeaderLabels(self.hLabelList)
                j = 0
                for name in data0.nameList:
                    item = None
                    if isinstance(data0[i][name], str) or isinstance(data0[i][name], QString):
                        item = QStandardItem(data0[i][name])
                    elif isinstance(data0[i][name], float) or isinstance(data0[i][name], int):
                        item = QStandardItem(str(data0[i][name]))
                    elif data0[i][name] == None:
                        item = QStandardItem("")
                    else:
                        item = QStandardItem(data0[i][name].ToString())
                    if self.ReadOnly:
                        item.setEditable(False)
                    self.setItem(i, j, item)
                    j += 1
                self.dataType = "dict"
            elif isinstance(data0[0] , list):
                # if len(self.hLabelList) != 0:
                #     self.setHorizontalHeaderLabels(self.hLabelList)
                j = 0
                for dt in data0[i]:
                    item = None
                    if isinstance(dt, str) or isinstance(dt, QString):
                        item = QStandardItem(dt)
                    elif isinstance(dt, float) or isinstance(dt, int):
                        item = QStandardItem(str(dt))
                    elif dt == None:
                        item = QStandardItem("")
                    else:
                        item = QStandardItem(dt.ToString())
                    if self.ReadOnly:
                        item.setEditable(False)
                    self.setItem(i, j, item)
                    j += 1
                self.dataType = "list"
            else:
                j = 0
                for k in range(len(data0[i].nameList)):
                    item = None
                    dt = data0[i].dataList[k]
                    if isinstance(dt, str) or isinstance(dt, QString):
                        item = QStandardItem(dt)
                    elif isinstance(dt, float) or isinstance(dt, int):
                        item = QStandardItem(str(dt))
                    elif dt == None:
                        item = QStandardItem("")
                    else:
                        item = QStandardItem(dt.ToString())
                    if self.ReadOnly:
                        item.setEditable(False)
                    self.setItem(i, j, item)
                    j += 1
                self.dataType = "object"
                    
        self.dataSource = data0

    DataSource = property(get_DataSource, set_DataSource, None, None)