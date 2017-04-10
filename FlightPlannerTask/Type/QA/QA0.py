
from FlightPlanner.AcadHelper import AcadHelper, Point3D
from FlightPlanner.types import QAFileVersion, QASnapshotFormat
from FlightPlanner.Dialogs.DlgQaComment import DlgQaComment
from PyQt4.QtGui import QMessageBox, QDialog


class QA0:
    AutoReportEntry = True;
    DefaultFileVersion = QAFileVersion.V10;
    DefaultImageFormat = QASnapshotFormat.Gif;

    @staticmethod
    def smethod_4(form_0, string_0):
        flag = False;
        dlgQaComment = DlgQaComment(form_0, string_0)
        resultDialog = dlgQaComment.exec_()
        if (resultDialog != QDialog.Accepted):
            return False, string_0;
        else:
            string_0 = dlgQaComment.Comment;
            flag = True;
        return flag, string_0;

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