
from QaWindowTemp import QaWindowTemp
from FlightPlanner.types import QAFileVersion, QASnapshotFormat, Point3D
from FlightPlanner.AcadHelper import AcadHelper
from PyQt4.QtGui import QMessageBox
import sys

class QA:
    Window = None
    
    EXTENSION = ".qaa";
    EXTENSION_BACKUP = ".qab";
    TABLE_IDENT_LEVEL1 = "    ";
    TABLE_IDENT_LEVEL2 = "        ";
    EnabledChanged = None;
    LoadedChanged = None;
    enabled = False
    DefaultFileVersion = None
    DefaultImageFormat = None;
    ChangeBackgroundToWhite = False;
    DwgList = [];
    Documents = [];
    JpegQuality = None;
    AutoReportEntry = False;
    def __init__(self):
        QA.Window = None;
        QA.enabled = True;
        QA.DefaultFileVersion = QAFileVersion.V10;
        QA.DefaultImageFormat = QASnapshotFormat.Gif;
        QA.ChangeBackgroundToWhite = True;
        QA.DwgList = None;
        QA.Documents = None;
        QA.JpegQuality = 90;
        QA.AutoReportEntry = True;
        QA.Window = QaWindowTemp.CreateQaWindow()
        QA.DwgList = [];
        QA.Documents = [];

    @staticmethod
    def smethod_2(qarecord_0):
        qa = QA()
        if (not QA.enabled):
            QA.Window.ActiveDocument = None;
            return;

        QA.Window.method_25(qarecord_0);

    @staticmethod
    def smethod_5(form_0, qasnapshot_0):
        try:
            # if (AcadHelper.Ready)
            # {
            #     AcadHelper.smethod_2();
            #     if (!qasnapshot_0.ModelSpace)
            #     {
            #         AcadHelper.smethod_27(DrawingSpace.PaperSpace, true);
            #     }
            #     else
            #     {
            #         AcadHelper.smethod_27(DrawingSpace.ModelSpace, true);
            #     }
            viewCenter = qasnapshot_0.ViewCenter;
            x = viewCenter.get_X() - qasnapshot_0.ViewSize / float(2);
            point3d = qasnapshot_0.ViewCenter;
            point2d = Point3D(x, point3d.get_Y() - qasnapshot_0.ViewSize / float(2));
            viewCenter1 = qasnapshot_0.ViewCenter;
            num = viewCenter1.get_X() + qasnapshot_0.ViewSize / float(2);
            point3d1 = qasnapshot_0.ViewCenter;
            point2d1 = Point3D(num, point3d1.get_Y() + qasnapshot_0.ViewSize / float(2));
            AcadHelper.smethod_66(point2d, point2d1);
            # AcadHelper.smethod_3();
        except:
            QMessageBox.warning(form_0, "Error", sys.exc_info()[0]);

    def getLoaded(self):
        return QA.Window.ActiveDocument != None;
    Loaded = property(getLoaded, None, None, None)

    def getEnabled(self):
        return QA.enabled
    def setEnabled(self, val):
        if (QA.enabled != val):
            QA.enabled = val;
            # if (QA.EnabledChanged != None):
            #     QA.EnabledChanged();
            if (not QA.enabled):
                loaded = QA.Loaded;
                QA.Window.ActiveDocument = None;
                # if (loaded != QA.Loaded and QA.LoadedChanged != None):
                #     QA.LoadedChanged();
    Enabled = property(getEnabled, setEnabled, None, None)