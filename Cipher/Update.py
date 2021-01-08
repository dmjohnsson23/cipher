from .Utilities import VERSION_NUMBER
import webbrowser
from PySide.QtGui import *

UPDATE_SITE="https://drive.google.com/folderview?id=0Bybx5H7UQYtURFF3UE5GVi1kM3c&usp=sharing"

LABEL_TEXT="""\
You are currently using Cipher %s. Click <a href="%s">here</a> to go to the update website. <br>
If you see a higher version there, simply download and install it.
"""%(VERSION_NUMBER, UPDATE_SITE)


window=None

def checkForUpdates():
    global window
    window=QWidget()
    window.setWindowTitle("Check for Updates")
    window.setMinimumHeight(150)
    window.setMinimumWidth(300)
    
    box=QVBoxLayout()
    footer=QHBoxLayout()
    footer.addStretch()
    
    label=QLabel(LABEL_TEXT)
    label.linkActivated.connect(update)
    box.addWidget(label)
    
    cancelButton=QPushButton("Cancel")
    cancelButton.clicked.connect(window.close)
    footer.addWidget(cancelButton)
    box.addLayout(footer)
    
    window.setLayout(box)
    window.show()



def update():
    webbrowser.open(UPDATE_SITE)
    window.close()