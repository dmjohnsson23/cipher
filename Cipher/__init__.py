"""\
#####################################################################
#              Dominick Johnson's Encryption program                #
#              Using elements from previous programs,               #
#          such as Caesar Cipher and One-Time Pad Cipher            #
# Plus additional elements including new GUI and additional ciphers #
#####################################################################

---Main Module---

This is the actual script which runs the program as a whole,
Containing code for:
> The User Interface
> Saving and Opening Files
> And, in short, Telling the other module what to do

Functions & Classes:
> class Interface:
    > Inherits from QMainWindow
    > The bulk of the code for this module is in this class

    > Vars:
        > ciphers
            > A dictionary containing cipher names for keys and module
              references for values
            > Used to simplify code determining which cipher module
              to use when user encode/Decodes message
        > All other vars refer to Widgets

    > Functions:
        > center()
            > Centers window on screen, taken from ZetCode PySide2 tutorial
              No return type
        > closeEvent()
            > Upon close, propts user if they really want to exit,
              adapted from ZetCode PySide2 Tutorial
              No return type
        > translate(cipher, keyF, mode)
            > Calls the encrypt() function from individual cipher modules,
              Displays the resulting text depending on user preference
              No return type
            > cipher: A sting containing cipher name
            > keyF: A function to call that will generate the key expected by cipher
            > mode: Either "Encode" or "Decode"
        > dataOpen(default="")
            > Asks user for a text file. If user doesn't cancel and no error
              occur, returns raw data from file, otherwise returns default
        > dataSave(data, filename="")
            > Saves data to filename. If filename=="", prompts uer for filename,
              If user cancels or errors occur, does nothing
              No return type
        > dataSaveAs(data)
            > Prompts user for filename, and saves data to that file
              No return type
        > loadKey(cipher)
            > Loads key information from user-specified file,
              checks if key is compatible with cipher,
              if so, returns key, otherwise, returns nothing
        > saveKey(cipher, key)
            > Saves key to user-specified file.
              No return type
        > dispCipherInfo(cipher):
            > Displays information about current cipher
              No return type
            > cipher: String containing cipher name
> Function main():
    >Executes script

"""
import sys
import os
import random
import pickle

from .Utilities import *

try:
    #Make Sure Qt and PySide2 Exist on computer
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except ImportError:
    import webbrowser
    webbrowser.open(os.path.join("Files", "Missing_Dependancies.html"))
    sys.exit()

#Now we know we have PySide2, We need to make a QApplication before
#we do anything else (Otherwise we get some errors when the
#Encryption packages begins defining it's Interface objects.
app=QApplication(sys.argv)

from .GuiElements import TablistWidget, TextEditor, ICONS
    
from . import Options
from . import Encryption
from . import Contact
from . import Update
from . import ImportExport



class Interface(QMainWindow):
    """\
Displays the main window. This class is basically the center or the whole program.\
"""
    def __init__(self):
        super(Interface, self).__init__()
        self.resize(1000, 600)
        self.center()
        self.setWindowTitle(MAIN_TITLE)
        self.setWindowIcon(ICONS.MAIN)

        self.bar=self.statusBar()

        self.lastFileName=""



        ###Make Widgets
        self.inp=TextEditor
        self.inp.setToolTip("Type or Paste your message here")


        

        ###Menu Bar
        menu=self.menuBar()

        #File Menu
        fileMenu=menu.addMenu("&File")
        
        newAction=QAction(ICONS.NEW, "New", self)
        newAction.setShortcut("Ctrl+N")
        newAction.triggered.connect(lambda:self.inp.setText(""))
        fileMenu.addAction(newAction)
        
        openAction=QAction(ICONS.OPEN, "Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(lambda:self.inp.setText(ImportExport.loadText() or self.inp.toPlainText()))
        fileMenu.addAction(openAction)
        
        saveAction=QAction(ICONS.SAVE, "Save", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(lambda:ImportExport.saveText(self.inp.toPlainText()))
        fileMenu.addAction(saveAction)
        
        saveAsAction=QAction(ICONS.SAVE_AS, "Save As", self)
        saveAsAction.setShortcut("Ctrl+Shift+S")
        saveAsAction.triggered.connect(lambda:ImportExport.saveTextAs(self.inp.toPlainText))
        fileMenu.addAction(saveAsAction)
        
        fileMenu.addSeparator()
        
        exitAction=QAction(ICONS.EXIT, "Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        #Edit menu
        editMenu=menu.addMenu("&Edit")
        
        undoAction=QAction(ICONS.UNDO, "Undo", self)
        undoAction.setShortcut("Ctrl+Z")
        undoAction.triggered.connect(self.inp.undo)
        editMenu.addAction(undoAction)
        
        redoAction=QAction(ICONS.REDO, "Redo", self)
        redoAction.setShortcut("Ctrl+Shift+Z")
        redoAction.triggered.connect(self.inp.redo)
        editMenu.addAction(redoAction)
        
        editMenu.addSeparator()
        
        copyAction=QAction(ICONS.COPY, "Copy", self)
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self.inp.copy)
        editMenu.addAction(copyAction)

        cutAction=QAction(ICONS.CUT, "Cut", self)
        cutAction.setShortcut("Ctrl+X")
        cutAction.triggered.connect(self.inp.cut)
        editMenu.addAction(cutAction)

        pasteAction=QAction(ICONS.PASTE, "Paste", self)
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.triggered.connect(self.inp.paste)
        editMenu.addAction(pasteAction)

        #Seperator

##        findAction=QAction(QIcon("search.png"), "Find", self)
##        findAction.setShortcut("Ctrl+F")
##        findAction.triggered.connect(self.inp.find)
##        editMenu.addAction(findAction)


        #Options Menu
        optionsMenu=menu.addMenu("&Options")

        
        textAG=QActionGroup(self, exclusive=True)
        textSubmenu=QMenu(optionsMenu)
        textSubmenu.setTitle("Text Display")

        textOverwriteAction=QAction("Overwrite Existing Text", self, checkable=True)
        textOverwriteAction.triggered.connect(lambda:self.newTextDisp("Overwrite"))
        a=textAG.addAction(textOverwriteAction)
        textSubmenu.addAction(a)

        textExternalAction=QAction("Display in Pop-up Window", self, checkable=True)
        textExternalAction.triggered.connect(lambda:self.newTextDisp("External"))
        a=textAG.addAction(textExternalAction)
        textSubmenu.addAction(a)

        if Options.TEXTDISP=="External":
            textExternalAction.setChecked(True)
        else:
            textOverwriteAction.setChecked(True)

        optionsMenu.addMenu(textSubmenu)



        themeAG=QActionGroup(self, exclusive=True)
        themeSubmenu=QMenu(optionsMenu)
        themeSubmenu.setTitle("Theme")
        
        formatSubmenu=QMenu(optionsMenu)
        formatSubmenu.setTitle("Formatting")
        
        fontAction=QAction(QIcon(), "Set Font", self)
        fontAction.triggered.connect(lambda:self.inp.setCurrentFont(QFontDialog.getFont(self.inp.currentFont())[0]))
        formatSubmenu.addAction(fontAction)
        
        wordwrapAction=QAction("Allow Word Wrap", self, checkable=True)
        wordwrapAction.triggered.connect(lambda:self.inp.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere
                                                                         if wordwrapAction.isChecked() else
                                                                         QTextOption.NoWrap))
        wordwrapAction.setChecked(True)
        formatSubmenu.addAction(wordwrapAction)
        
        optionsMenu.addMenu(formatSubmenu)
        
        
        
        
        #Note: There is a better way to do theme changes, as it is done in
        #C:\Python32\Lib\site-packages\PySide2\examples\widgets\icons\icons.py.
        #Try that way.
        themeActions=[]
        for theme in QStyleFactory.keys():
            themeActions.append(QAction(theme, self, checkable=True))
            themeActions[-1].triggered.connect(lambda
                                               theme=theme:
                                               self.newStyle(theme))
            if theme==Options.STYLE:
                themeActions[-1].setChecked(True)
            a=themeAG.addAction(themeActions[-1])
            themeSubmenu.addAction(a)

        themeSubmenu.addSeparator()
        themeResetAction=QAction("Reset to Default", self)
        themeResetAction.triggered.connect(lambda:self.newStyle(Options.DEFAULT))
        themeSubmenu.addAction(themeResetAction)

        optionsMenu.addMenu(themeSubmenu)


        
        

        #help menu
        helpMenu=menu.addMenu("&Help")
        
        aboutAction=QAction(ICONS.ABOUT, "About", self)
        aboutAction.triggered.connect(self.dispAboutInfo)
        helpMenu.addAction(aboutAction)
        
        aboutQtAction=QAction(ICONS.ABOUT, "About Qt", self)
        aboutQtAction.triggered.connect(qApp.aboutQt)
        helpMenu.addAction(aboutQtAction)
        
        licenceAction=QAction(QIcon(), "License", self)
        licenceAction.triggered.connect(self.dispLicenceInfo)
        helpMenu.addAction(licenceAction)
        
        attrAction=QAction(QIcon(), "Attributions", self)
        attrAction.triggered.connect(self.dispAttributionsInfo)
        helpMenu.addAction(attrAction)
        
        helpMenu.addSeparator()
        
        updateAction=QAction(QIcon(), "Check for Updates", self)
        updateAction.triggered.connect(Update.checkForUpdates)
        helpMenu.addAction(updateAction)
        
        helpMenu.addSeparator()
        
        contactAction=QAction(ICONS.CONTACT, "Contact", self)
        contactAction.triggered.connect(Contact.contact)
        helpMenu.addAction(contactAction)
        
        bugAction=QAction(ICONS.BUG, "Submit Bug Report", self)
        bugAction.triggered.connect(lambda:Contact.contact(True))
        helpMenu.addAction(bugAction)
        
        

        

        ###Layout Stuff

        self.tabs=TablistWidget(self, label="Select a Cipher: ")
        
        infoButton=QPushButton(ICONS.INFO, "Cipher Info")
        infoButton.setToolTip("Display information about this cipher")
        infoButton.clicked.connect(self.dispCipherInfo)
        self.tabs.header.addWidget(infoButton)
        self.tabs.list.setInsertPolicy(QComboBox.InsertAlphabetically)
        
        for cipher in Encryption.ciphers:
            self.tabs.addTab(Encryption.ciphers[cipher].Interface, cipher)
        
        


        self.saveKeyButton=QPushButton("Save Key", self.tabs)
        self.saveKeyButton.setToolTip("Save the key to a file")
        self.saveKeyButton.clicked.connect(lambda:ImportExport.saveKey(self.currentCipher.Interface.getKey(), 
                                                                       self.currentCipher.NAME))
        
        self.loadKeyButton=QPushButton("Load Key", self.tabs)
        self.loadKeyButton.setToolTip("Load a key from a file")
        self.loadKeyButton.clicked.connect(lambda:self.currentCipher.Interface.setKey(
                                                                ImportExport.loadKey(self.currentCipher.NAME)))
        
        self.hackButton=QPushButton("Hack", self.tabs)
        self.hackButton.setToolTip("Attempt to hack your message")
        self.hackButton.clicked.connect(lambda: self.translate(HACK))
        
        self.decodeButton=QPushButton("Decode", self.tabs)
        self.decodeButton.setToolTip("Decode your message")
        self.decodeButton.clicked.connect(lambda: self.translate(DECODE))
        
        self.encodeButton=QPushButton("Encode", self.tabs)
        self.encodeButton.setToolTip("Encode your message")
        self.encodeButton.clicked.connect(lambda: self.translate(ENCODE))
        



        footer=QHBoxLayout()
        footer.addWidget(self.saveKeyButton)
        footer.addWidget(self.loadKeyButton)
        footer.addStretch()
        footer.addWidget(self.hackButton)
        footer.addWidget(self.decodeButton)
        footer.addWidget(self.encodeButton)
        self.updateFooter()

        self.tabs.grid.addLayout(footer)
        self.tabs.list.activated.connect(self.updateFooter)
        self.tabs.list.setToolTip("Change the current cipher")

        splitter=QSplitter(Qt.Vertical)
        splitter.addWidget(self.inp)
        splitter.addWidget(self.tabs)

        self.setCentralWidget(splitter)


        ###Show Window
        self.show()
                                                                           
        if Options.FIRST_TIME:
            self.dispLicenceInfo()
            Options.setOptions(firstTime=False)


        

####Fuctions for dealing with interface:
    def center(self):
        """\
Centers the window on the screen.
Taken from ZetCode PySide2 tutorial.\
"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def closeEvent(self, event):
        """\
Provides that lovely "Are you sure you want to quit?" message.
Adapted from ZetCode PySide2 tutorial\
"""
        if Options.MODE=="DEBUG":
            event.accept()
            return
        reply = QMessageBox.question(self, "Quit?",
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



    def newStyle(self, theme):
        QMessageBox.information(self, "Theme Change",
            "Theme change will take effect time program starts.")

        Options.setOptions(style=theme)

    def newTextDisp(self, textDisp):
        Options.setOptions(textDisp=textDisp)
        
    
    @property
    def currentCipher(self):
        return Encryption.ciphers[self.tabs.currentTab]
        
        
####Non Interface related functions

    def updateFooter(self):
        currentUi=Encryption.ciphers[self.tabs.currentTab].Interface
        saveLoad=currentUi.SAVE_LOAD
        hack=currentUi.HACK
        
        self.saveKeyButton.setVisible(saveLoad)
        self.loadKeyButton.setVisible(saveLoad)
        self.hackButton.setVisible(hack)
                                     
    def translate(self, mode):
        """\
Enciphers and displays the message according to user preferences
No return\
"""
        message=self.inp.toPlainText()
        if message is None or message.strip()=="":
            QMessageBox.critical(None, "Error", "There is no message to "+mode)
            return
        
        self.encrypterThread=Encryption.ThreadedEncryption(message, self.currentCipher, mode)
        self.encrypterThread.encryptionFinished.connect(self.displayText)
        
        self.encodeButton.setEnabled(False)
        self.decodeButton.setEnabled(False)
        self.hackButton.setEnabled(False)

        self.encrypterThread.start()
    
    @Slot(str, str)
    def displayText(self, ciphered, mode):
        
        if not ciphered:
            #We got no return from cipher
            #i.e, there was no input, or translation failed
            # Individual ciphers should implement their own Error Messages
            return

        if Options.TEXTDISP==Options.TEXT_DISPLAY_MODE_OVERWRITE:
            self.inp.setText(ciphered)
        else:
            self.textDisplayExternal(ciphered, mode)
        
        self.encodeButton.setEnabled(True)
        self.decodeButton.setEnabled(True)
        self.hackButton.setEnabled(True)
    
    
    def textDisplayExternal(self, text, mode):
            self.infoWindow=QWidget()
            self.infoWindow.setWindowTitle("Your "+
                                           mode+
                                           ('e' if mode==HACK else "")+
                                           "d Message")
            self.infoWindow.setWindowIcon(ICONS.MAIN)
            box=QVBoxLayout()

            box.addWidget(QLabel("<b>Your "+
                                 mode+
                                 ('e' if mode==HACK else "")+
                                 "d Message:</b>"))
            
            infoLabel=QTextEdit(self.infoWindow)
            infoLabel.setText(text)
            infoLabel.setReadOnly(True)
            box.addWidget(infoLabel)

            okbut=QPushButton("OK")
            okbut.clicked.connect(self.infoWindow.close)
            okbut.setMaximumSize(okbut.sizeHint())
            
            box2=QHBoxLayout()
            box2.addWidget(QWidget())
            box2.addWidget(okbut)
            box.addLayout(box2)

            self.infoWindow.setLayout(box)
            self.infoWindow.show()
            

        
    def dispCipherInfo(self):
        cipher=self.currentCipher.NAME
        info=Encryption.info[cipher]
        self.infoWindow=QWidget()
        self.infoWindow.setWindowTitle(cipher+" Info")
        self.infoWindow.setWindowIcon(ICONS.INFO)
        box=QVBoxLayout()
        infoLabel=QLabel(info)
        infoLabel.setWordWrap(True)
        box.addWidget(infoLabel)

        okbut=QPushButton("OK")
        okbut.clicked.connect(self.infoWindow.close)
        okbut.setMaximumSize(okbut.sizeHint())
        
        box2=QHBoxLayout()
        box2.addWidget(QWidget())
        box2.addWidget(okbut)
        box.addLayout(box2)

        self.infoWindow.setLayout(box)
        self.infoWindow.show()
        
        
        
    def dispAboutInfo(self):
        self.infoWindow=QWidget()
        self.infoWindow.setWindowTitle("About Cipher")
        self.infoWindow.setWindowIcon(ICONS.ABOUT)
        
        box=QVBoxLayout()

        img=QLabel()
        img.setPixmap(QPixmap(os.path.join("Files", "Logo.png")))
        box.addWidget(img)
        
        infoLabel=QTextBrowser(self.infoWindow)
        infoLabel.setText(MAIN_ABOUT_TEXT)
        infoLabel.setOpenExternalLinks(True)
        box.addWidget(infoLabel)

        okbut=QPushButton("OK")
        okbut.clicked.connect(self.infoWindow.close)
        okbut.setMaximumSize(okbut.sizeHint())
        
        box2=QHBoxLayout()
        box2.addWidget(QWidget())
        box2.addWidget(okbut)
        box.addLayout(box2)

        self.infoWindow.setLayout(box)
        self.infoWindow.show()
                                     
        
      
    def dispLicenceInfo(self):
        self.infoWindow=QWidget()
        self.infoWindow.setWindowTitle("License")
        self.infoWindow.setWindowIcon(ICONS.ABOUT)
        
        box=QVBoxLayout()

        img=QLabel()
        img.setPixmap(QPixmap(os.path.join("Files", "Logo.png")))
        box.addWidget(img)
        
        infoLabel=QTextEdit(self.infoWindow)
        infoLabel.setText(LICENCE_TEXT)
        infoLabel.setReadOnly(True)
        box.addWidget(infoLabel)

        okbut=QPushButton("OK")
        okbut.clicked.connect(self.infoWindow.close)
        okbut.setMaximumSize(okbut.sizeHint())
        
        box2=QHBoxLayout()
        box2.addWidget(QWidget())
        box2.addWidget(okbut)
        box.addLayout(box2)

        self.infoWindow.setLayout(box)
        self.infoWindow.show()



    def dispAttributionsInfo(self):
        self.infoWindow=QWidget()
        self.infoWindow.setWindowTitle("Attributions")
        self.infoWindow.setWindowIcon(ICONS.ABOUT)
        
        box=QVBoxLayout()

        img=QLabel()
        img.setPixmap(QPixmap(os.path.join("Files", "Logo.png")))
        box.addWidget(img)
        
        infoLabel=QTextEdit(self.infoWindow)
        infoLabel.setText(ATTRIBUTIONS_TEXT)
        infoLabel.setReadOnly(True)
        box.addWidget(infoLabel)

        okbut=QPushButton("OK")
        okbut.clicked.connect(self.infoWindow.close)
        okbut.setMaximumSize(okbut.sizeHint())
        
        box2=QHBoxLayout()
        box2.addWidget(QWidget())
        box2.addWidget(okbut)
        box.addLayout(box2)

        self.infoWindow.setLayout(box)
        self.infoWindow.show()
        
        

##            
##    def openHelp(self):
##        helpWindow=tk.Toplevel()
##        helpWindow.title("Cipher Help")
##        helpText=st.ScrolledText(helpWindow, width=50, wrap=tk.WORD)
##        helpText.pack()
##        helpText.insert(tk.END, HELP_TEXT)
##        helpText.config(state=tk.DISABLED)
##



#######################################################################################################################################################################


def main():
    global app
    if Options.STYLE != Options.DEFAULT:
        QApplication.setStyle(Options.STYLE)
    GUI=Interface()
    sys.exit(app.exec_())
