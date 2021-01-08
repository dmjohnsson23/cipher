import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .Utilities import DIRECTORY
from .GuiElements import ICONS
import os
from PySide.QtGui import *

TO_ADDRESS = "dmjohn235@gmail.com"
LOG_PATH=os.path.join(DIRECTORY, "log.txt")

def send(message, fromAddress):
    msg = MIMEText(message)
    msg["Subject"] = "Cipher"
    msg["From"] = fromAddress
    msg["To"] = TO_ADDRESS
    
    server = smtplib.SMTP('localhost')
    server.send_message(msg)
    server.quit()


def sendBugreport(message, fromAddress):
    msg = MIMEMultipart()
    msg["Subject"] = "Cipher Bug Report"
    msg["From"] = fromAddress
    msg["To"] = TO_ADDRESS
    
    file = open(LOG_PATH)
    log = MIMEText(file.read())
    file.close()
    msg.attach(log)
    
    body = MIMEText(message)
    msg.attach(body)
    
    server = smtplib.SMTP('localhost')
    server.send_message(msg)
    server.quit()



def contact(bugReport=False):
    global window
    if bugReport:
        titleText="Submit Bug Report"
        messageText="Please describe what you where doing when the problem\n occurred: "
        icon=ICONS.BUG
        def submit(message, fromAddress):
            try:
                sendBugreport(message, fromAddress)
                
            except Exception as ex:
                import traceback
                fullTraceback=traceback.format_exc()
                errMsg=fullTraceback.splitlines()[-1]
                msgBox=QMessageBox()
                msgBox.setText("There was a problem sending the bug report. "
                               "Please send me an email at %s. Please be sure "
                               "to include what you where doing when the problem "
                               "occurred, as well as the contents of the file \"%s\" "
                               "(located in the same folder as this program.)\n\n%s"%
                               (TO_ADDRESS, os.path.abspath(LOG_PATH), errMsg))
                msgBox.setDetailedText(fullTraceback)
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setWindowTitle("Error")
                msgBox.exec_()
                
            finally:
                window.close()
    else:
        titleText="Contact"
        messageText="Please type your message here: "
        icon=ICONS.CONTACT
        def submit(message, fromAddress):
            try:
                send(message, fromAddress)
                
            except Exception as ex:
                import traceback
                fullTraceback=traceback.format_exc()
                errMsg=fullTraceback.splitlines()[-1]
                msgBox=QMessageBox()
                msgBox.setText("There was a problem sending the message. "
                               "You can send me an email at %s. \n\n%s"%(TO_ADDRESS, errMsg))
                msgBox.setDetailedText(fullTraceback)
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setWindowTitle("Error")
                msgBox.exec_()
                
            finally:
                window.close()
        
    window=QWidget()
    window.setMaximumWidth(300)
    window.setWindowTitle(titleText)
    window.setWindowIcon(icon)
    
    form=QFormLayout()
    form.setRowWrapPolicy(QFormLayout.WrapLongRows)
    
    emailInput=QLineEdit(window)
    emailInput.setToolTip("Required to establish communication.\n"
                          "I promise not to sell it or give it to anyone for any reason.")
    form.addRow("Email Address: ", emailInput)

    messageInput=QTextEdit(window)
    messageInput.setMinimumWidth(250)
    form.addRow(messageText, messageInput)
    
    submitButton=QPushButton("Submit")
    submitButton.clicked.connect(lambda:submit(messageInput.toPlainText(), emailInput.text()))
    
    footer=QHBoxLayout()
    footer.addStretch()
    footer.addWidget(submitButton)
    
    box=QVBoxLayout()
    box.addLayout(form)
    box.addLayout(footer)
    
    window.setLayout(box)
    
    window.show()
    