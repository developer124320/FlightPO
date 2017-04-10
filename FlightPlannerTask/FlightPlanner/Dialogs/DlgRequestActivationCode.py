# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox, QFileDialog
from PyQt4.QtCore import QString, QFileInfo
from PyQt4.QtCore import  SIGNAL, QCoreApplication
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from Type.String import String
import define, sys
try:
    import clr
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
except SystemError as e1:
    print e1.message
except:
    print "Unexpected error:", sys.exc_info()[0]


try:
    mydll = clr.AddReference('SKGL')
    from SKGL import Validate, Generate, SerialKeyConfiguration
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
except SystemError as e1:
    print e1.message
except:
    print "Unexpected error:", sys.exc_info()[0]
import define
class DlgRequestActivationCode(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.resize(100, 70);
        self.setWindowTitle("Request Activation Code")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth());
        self.setSizePolicy(sizePolicy);
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"));

        self.groupBox1 = GroupBox(self)
        self.groupBox1.Caption = ""
        verticalLayoutDlg.addWidget(self.groupBox1)

        self.txtName = TextBoxPanel(self.groupBox1)
        self.txtName.Caption = "Name"
        self.txtName.LabelWidth = 80
        self.txtName.Width = 200
        self.groupBox1.Add = self.txtName

        self.txtCompany = TextBoxPanel(self.groupBox1)
        self.txtCompany.Caption = "Company"
        self.txtCompany.LabelWidth = 80
        self.txtCompany.Width = 200
        self.groupBox1.Add = self.txtCompany

        self.txtAddress = TextBoxPanel(self.groupBox1, True)
        self.txtAddress.Caption = "Address"
        self.txtAddress.LabelWidth = 80
        self.txtAddress.Width = 200
        self.groupBox1.Add = self.txtAddress

        self.txtPhoneNo = TextBoxPanel(self.groupBox1)
        self.txtPhoneNo.Caption = "Phone No."
        self.txtPhoneNo.LabelWidth = 80
        self.txtPhoneNo.Width = 200
        self.groupBox1.Add = self.txtPhoneNo

        self.txtEmail = TextBoxPanel(self.groupBox1)
        self.txtEmail.Caption = "Email"
        self.txtEmail.LabelWidth = 80
        self.txtEmail.Width = 200
        self.groupBox1.Add = self.txtEmail

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        btnSendRequest = self.btnBoxOkCancel.button(QDialogButtonBox.Ok)
        btnSendRequest.setText("Send Request")
        btnCancel = self.btnBoxOkCancel.button(QDialogButtonBox.Cancel)
        btnCancel.setVisible(False)

        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)

    def acceptDlg(self):
        try:
            if (String.IsNullOrEmpty(self.txtName.Value) == False and String.IsNullOrEmpty(self.txtEmail.Value) == False):
                machinCode = "";
                obj = SerialKeyConfiguration();

                # //string code = objGenerate.doKey(30);
                machinCode = str(obj.MachineCode);
                messagebody = "";
                messagebody += "Name: " + self.txtName.Value + "\n"
                messagebody += "Email: " + self.txtEmail.Value + "\n"
                messagebody += "Phone Number : " + self.txtPhoneNo.Value + "\n"
                messagebody += "Company: " + self.txtCompany.Value + "\n"
                messagebody += "Address: " + self.txtAddress.Value + "\n"
                messagebody += "Machine code: " + str(machinCode) + "\n"

                import smtplib
                from email.mime.text import MIMEText
                subject = define.MailSubject
                msg = MIMEText(String.QString2Str(messagebody))
                msg['Subject'] = define.MailSubject
                message = self.createhtmlmail(subject, None, messagebody)
                server = smtplib.SMTP_SSL(define.smtpServer + ":" + str(define.smtpPort))
                server.login(define.email, define.password)
                server.sendmail(define.FromEmail, define.ToEmail, msg.as_string())
                server.quit()
                # client = new SmtpClient(SMTPSERVER);
                # client.Port = SMTPPORT;
                # client.EnableSsl = true;
                # client.Timeout = 100000;
                # client.DeliveryMethod = SmtpDeliveryMethod.Network;
                # client.UseDefaultCredentials = false;
                # client.Credentials = new NetworkCredential(
                #   SMTPEmail, SMTPPassword);
                # MailMessage msg = new MailMessage();
                # msg.To.Add(ToEmail);
                # msg.From = new MailAddress(FromEmail);
                # msg.Subject = MailSubject;
                # msg.Body = messagebody;
                # System.Net.ServicePointManager.ServerCertificateValidationCallback = delegate(object s, System.Security.Cryptography.X509Certificates.X509Certificate certificate, System.Security.Cryptography.X509Certificates.X509Chain chain, System.Net.Security.SslPolicyErrors sslPolicyErrors) { return true; };
                # client.Send(msg);
                # MessageBox.Show("Successfully Sent Message.");
            else:
                QMessageBox.warning(self, "Warning", "Sorry! Name and email is required field.");
        except Exception as ex:
            QMessageBox.warning(self, "Warning", ex.message);
        self.accept()

    def createhtmlmail(self, subject, html, text):
        " Create a mime-message that will render as HTML or text, as appropriate"
        import MimeWriter, mimetools, cStringIO
        if text is None:
        # Produce an approximate textual rendering of the HTML string,
        # unless you have been given a better version as an argument
            import htmllib, formatter
            textout = cStringIO.StringIO( )
            formtext = formatter.AbstractFormatter(formatter.DumbWriter(textout))
            parser = htmllib.HTMLParser(formtext)
            parser.feed(html)
            parser.close( )
            text = textout.getvalue( )
            del textout, formtext, parser
        out = cStringIO.StringIO( ) # output buffer for our message
        # htmlin = cStringIO.StringIO(html) # input buffer for the HTML
        txtin = cStringIO.StringIO(text) # input buffer for the plain text
        writer = MimeWriter.MimeWriter(out)
# Set up some basic headers. Place subject here because smtplib.sendmail
# expects it to be in the message, as relevant RFCs prescribe.
        writer.addheader("Subject", subject)
        writer.addheader("MIME-Version", "1.0")
# Start the multipart section of the message. Multipart/alternative seems
# to work better on some MUAs than multipart/mixed.
        writer.startmultipartbody("")
        writer.flushheaders( )
# the plain-text section: just copied through, assuming iso-8859-1
        subpart = writer.nextpart( )
        pout = subpart.startbody("text/plain", [("charset", 'iso-8859-1')])
        pout.write(txtin.read( ))
        txtin.close( )
# the HTML subpart of the message: quoted-printable, just in case
#         subpart = writer.nextpart( )
#         subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
#         pout = subpart.startbody("text/html", [("charset", 'us-ascii')])
#         mimetools.encode(htmlin, pout, 'quoted-printable')
#         htmlin.close( )
# You're done; close your writer and return the message as a string
        writer.lastpart( )
        msg = out.getvalue( )
        out.close( )
        return msg

