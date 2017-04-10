
from PyQt4.QtXml import QDomDocument, QDomElement
from PyQt4.QtCore import QFile, QTextStream, QString
from Type.FasDataBlockFile import FasDataBlockFile
from FlightPlanner.Dialogs.DlgCrcCheck import DlgCrcCheck
from Type.switch import switch
import os

class enumProjectType:
    ptAipChart = "ptAipChart"
    ptProject = "ptProject"
    ptSubProject = "ptSubProject"
    ptWorkspace = "ptWorkspace"
    ptFile = "ptFile"

class ProjectInfo:
    def __init__(self):
        self.UserName = ""
        self.Created = ""
        self.Pt = ""
        self.ProjName = ""
        self.SubProjName = ""
        self.WorkspaceName = ""
        self.ProcedureName = ""
        self.Path = ""
        
    def get_Name(self):
        for case in switch (self.Pt):
            if case(enumProjectType.ptProject):
                return self.ProjName
            elif case(enumProjectType.ptSubProject):
                return self.SubProjName
            elif case(enumProjectType.ptWorkspace):
                return self.WorkspaceName
            elif case(enumProjectType.ptFile):
                return self.ProcedureName
            else:
                return self.ProjName
    def set_Name(self, value):
        for case in switch (self.Pt):
            if case(enumProjectType.ptProject):
                self.ProjName = value
                break
            elif case(enumProjectType.ptSubProject):
                self.SubProjName = value
                break
            elif case(enumProjectType.ptWorkspace):
                self.WorkspaceName = value
                break
            elif case(enumProjectType.ptFile):
                self.ProcedureName = value
                break
            else:
                self.ProjName = value
                break
    Name = property(get_Name, set_Name), None, None

class ProjectList:
    def __init__(self):
        self.PROJECTINFO_FILENAME = "\\ProjectInfo.xml"
        self.ProjectsList = []
        self.m_strProjectInfoFullName = os.getcwdu() + self.PROJECTINFO_FILENAME


    def Add(self, project):
        self.ProjectsList.append(project)

    def GetProjectCount(self):
        return len(self.ProjectsList)

    def Find(self, strName, type = None):
        try:
            if type == None:
                i = 0
                for pi in self.ProjectsList:
                    if (pi.Name == strName):
                        return i
                    i += 1
                return None
            else:
                i = 0
                for pi in self.ProjectsList:
                    if (pi.Name == strName) and pi.Pt == type:
                        return i
                    i += 1
                return None
        except:
            # MessageBox.Show(ex.Message)
            return None

    def SetProjectInfoPath(self, path):
        self.m_strProjectInfoFullName = path + self.PROJECTINFO_FILENAME

    def ReadProjectInfoXml(self):
        try:
            result = DlgCrcCheck.smethod_0(None, self.m_strProjectInfoFullName)
        except:
            return False
        if not result:
            return False

        doc = QDomDocument()
        qFile = QFile(self.m_strProjectInfoFullName)
        if qFile.open(QFile.ReadOnly):
            doc.setContent(qFile)
            qFile.close()
        else:
            raise UserWarning, "can not open file:" + self.m_strProjectInfoFullName
        dialogNodeList = doc.elementsByTagName("ProjectListClass")
        if dialogNodeList.isEmpty():
            raise UserWarning, "This file is not correct."
        dialogElem = dialogNodeList.at(0).toElement()

        ctrlNodesList = dialogElem.elementsByTagName("ProjectInfo")
        for i in range(ctrlNodesList.count()):
            pj = ProjectInfo()
            lineEditElem = ctrlNodesList.at(i).toElement()
            objectNameNode = lineEditElem.elementsByTagName("Name").at(0)
            objectNameElem = objectNameNode.toElement()
            pj.Name = objectNameElem.text()

            pathElem = objectNameNode.nextSiblingElement()
            pj.Path = pathElem.text()

            createdElem = pathElem.nextSiblingElement()
            pj.Created = createdElem.text()

            procedureNameElem = createdElem.nextSiblingElement()
            pj.ProcedureName = procedureNameElem.text()

            projNameElem = procedureNameElem.nextSiblingElement()
            pj.ProjName = projNameElem.text()

            ptElem = projNameElem.nextSiblingElement()
            pj.Pt = ptElem.text()

            subProjNameElem = ptElem.nextSiblingElement()
            pj.SubProjName = subProjNameElem.text()

            userNameElem = subProjNameElem.nextSiblingElement()
            pj.UserName = userNameElem.text()

            workspaceNameElem = userNameElem.nextSiblingElement()
            pj.WorkspaceName = workspaceNameElem.text()

            self.ProjectsList.append(pj)
        return True




    def WriteProjectInfoXml(self):
        doc = QDomDocument()
        rootElem = doc.createElement("ProjectListClass")
        xmlDeclaration = doc.createProcessingInstruction( "xml", "version=\"1.0\" encoding=\"utf-8\"" )
        doc.appendChild( xmlDeclaration )

        elem = doc.createElement("ProjectCount")
        elem.appendChild(doc.createTextNode(str(len(self.ProjectsList))))
        rootElem.appendChild(elem)

        for i in range(len(self.ProjectsList)):
            elem = doc.createElement("ProjectInfo")
            objNameElem = doc.createElement("Name")
            objNameElem.appendChild(doc.createTextNode(self.ProjectsList[i].Name))
            elem.appendChild(objNameElem)

            objNameElem = doc.createElement("Path")
            objNameElem.appendChild(doc.createTextNode(self.ProjectsList[i].Path))
            elem.appendChild(objNameElem)

            objNameElem = doc.createElement("Created")
            objNameElem.appendChild(doc.createTextNode(self.ProjectsList[i].Created))
            elem.appendChild(objNameElem)

            objNameElem = doc.createElement("ProcedureName")
            objNameElem.appendChild(doc.createTextNode(self.ProjectsList[i].ProcedureName))
            elem.appendChild(objNameElem)

            objNameElem = doc.createElement("ProjName")
            objNameElem.appendChild(doc.createTextNode(self.ProjectsList[i].ProjName))
            elem.appendChild(objNameElem)

            objNameElem = doc.createElement("Pt")
            objNameElem.appendChild(doc.createTextNode(self.ProjectsList[i].Pt))
            elem.appendChild(objNameElem)

            objNameElem = doc.createElement("SubProjName")
            objNameElem.appendChild(doc.createTextNode(self.ProjectsList[i].SubProjName))
            elem.appendChild(objNameElem)

            objNameElem = doc.createElement("UserName")
            objNameElem.appendChild(doc.createTextNode(self.ProjectsList[i].UserName))
            elem.appendChild(objNameElem)

            objNameElem = doc.createElement("WorkspaceName")
            objNameElem.appendChild(doc.createTextNode(self.ProjectsList[i].WorkspaceName))
            elem.appendChild(objNameElem)

            rootElem.appendChild(elem)
        doc.appendChild(rootElem)
        qFile = QFile(self.m_strProjectInfoFullName)
        if qFile.open(QFile.WriteOnly):
            textStream = QTextStream(qFile)
            doc.save(textStream, 4)
            qFile.close()

            # ###CRC file is created.
            contents = None
            with open(self.m_strProjectInfoFullName, 'rb', 0) as tempFile:
                contents = tempFile.read()
                tempFile.flush()
                tempFile.close()
            bytes = FasDataBlockFile.CRC_Calculation(contents)
            string_0 = QString(self.m_strProjectInfoFullName)
            path = string_0.left(string_0.length() - 3) + "crc"
            fileStream = open(path, 'wb')
            fileStream.write(bytes)
            fileStream.close()

        else:
            raise UserWarning, "can not open file:" + self.m_strProjectInfoFullName
    def Insert(self, index, pi):
        self.ProjectsList.insert(index, pi)
    def Remove(self, p, type = None):
        try:
            if isinstance(p, int):
                self.ProjectsList.pop(p)
                return
            if type == None:
                if not isinstance(p, ProjectInfo):
                    i = self.Find(p)
                    if (i == None):
                        return
                    self.ProjectsList.pop(i)
                else:
                    i = self.Find(p.Name, p.Pt)
                    if (i == None):
                        return
                    self.ProjectsList.pop(i)
            else:
                i = self.Find(p, type)
                if (i == None):
                    return
                self.ProjectsList.pop(i)
        except:
            pass


    def GetLinkedProjects(self, pi, refProjectType, outProjectType = None):
        try:
            if outProjectType == None:
                listProject = []
                for piItem in self.ProjectsList:
                    if (piItem.Pt != refProjectType):
                        continue
                    for case in switch (pi.Pt):
                        if case(enumProjectType.ptProject):
                            if (pi.Name == piItem.ProjName):
                                listProject.append(piItem)
                            break
                        elif case(enumProjectType.ptSubProject):
                            if (pi.Name == piItem.SubProjName):
                                listProject.append(piItem)
                            break
                        elif case(enumProjectType.ptWorkspace):
                            if (pi.Name == piItem.WorkspaceName):
                                listProject.append(piItem)
                            break
                        elif case(enumProjectType.ptFile):
                            if (pi.Name == piItem.ProcedureName):
                                listProject.append(piItem)
                            break
                return listProject
            else:
                listProject = []
                for piItem in self.ProjectsList:
                    if (piItem.Pt != outProjectType):
                        continue
                    for case in switch (refProjectType):
                        if case(enumProjectType.ptProject):
                            if (pi == piItem.ProjName):
                                listProject.append(piItem.Name)
                            break
                        elif case(enumProjectType.ptSubProject):
                            if (pi == piItem.SubProjName):
                                listProject.append(piItem.Name)
                            break
                        elif case(enumProjectType.ptWorkspace):
                            if (pi == piItem.WorkspaceName):
                                listProject.append(piItem.Name)
                            break
                        elif case(enumProjectType.ptFile):
                            if (pi == piItem.ProcedureName):
                                listProject.append(piItem.Name)
                            break
                return listProject
        except:
            # MessageBox.Show(ex.Message)
            return None

