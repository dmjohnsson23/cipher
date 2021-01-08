from PySide.QtGui import *
from PySide.QtCore import *
from .Utilities import initialize, DIRECTORY
from .LetterMath import numToChar, charToNum
import os
import itertools

@initialize
class ICONS:
    ICON_DIR=os.path.join(DIRECTORY, "Files", "ButtonIcons")
    
    MAIN=QIcon(os.path.join(DIRECTORY, "Files", "Icon.ico"))
    
    GREEN_CHECK=QIcon(os.path.join(ICON_DIR, "Green Check.png"))
    RED_X=QIcon(os.path.join(ICON_DIR, "Red X.png"))
    COPY=QIcon(os.path.join(ICON_DIR, "Copy.png"))
    CUT=QIcon(os.path.join(ICON_DIR, "Cut.png"))
    PASTE=QIcon(os.path.join(ICON_DIR, "Paste.png"))
    PLUS=QIcon(os.path.join(ICON_DIR, "Plus.png"))
    MINUS=QIcon(os.path.join(ICON_DIR, "Minus.png"))
    UNDO=QIcon(os.path.join(ICON_DIR, "Undo.png"))
    REDO=QIcon(os.path.join(ICON_DIR, "Redo.png"))
    INFO=QIcon(os.path.join(ICON_DIR, "Info.png"))
    NEW=QIcon(os.path.join(ICON_DIR, "New.png"))
    OPEN=QIcon(os.path.join(ICON_DIR, "Open.png"))
    SAVE=QIcon(os.path.join(ICON_DIR, "Save.png"))
    SAVE_AS=QIcon(os.path.join(ICON_DIR, "Save As.png"))
    EXIT=QIcon(os.path.join(ICON_DIR, "Exit.png"))
    CONTACT=QIcon(os.path.join(ICON_DIR, "Contact.png"))
    BUG=QIcon(os.path.join(ICON_DIR, "Bug.png"))
    ABOUT=QIcon(os.path.join(ICON_DIR, "About.png"))


class TablistWidget(QWidget):
    def __init__(self, parent=None, label="", **widgets):
        QWidget.__init__(self, parent)
        self.list=QComboBox(self)
        self.display=QStackedWidget(self)
        self.label=QLabel(label)
        self.tabs=dict()
        self.grid=QVBoxLayout()
        self.setLayout(self.grid)
        self.header=QHBoxLayout()
        self.grid.addLayout(self.header)

        self.header.addWidget(self.label)
        self.header.addWidget(self.list)
        self.header.addStretch()
        self.grid.addWidget(self.display)

        for w in widgets:
            self.addTab(w, widgets[w])

        self.list.activated.connect(self.update)

        self.currentTab=self.list.currentText()


    def addTab(self, widget, key):
        self.display.addWidget(widget)
        self.tabs[key]=self.display.count()-1
        self.list.addItem(key)
        self.update() #Update, just in case

    def update(self):
        self.currentTab=self.list.currentText()
        self.display.setCurrentIndex(self.tabs[self.currentTab])
        

class LineInput(QWidget):
    def __init__(self, parent=None, prompt=""):
        QWidget.__init__(self, parent)
        
        box=QHBoxLayout()
        
        self.prompt=QLabel(prompt)
        self.lineEdit=QLineEdit(self)
        
        box.addWidget(self.prompt)
        box.addWidget(self.lineEdit)
        self.setLayout(box)
    
    def text(self):
        return self.lineEdit.text()
    
    def setText(self, text):
        self.lineEdit.setText(text)
        
    def setPrompt(self, text):
        self.prompt.setText(text)


class ListSelector(QWidget):
    def __init__(self, parent, label):
        QWidget.__init__(self, parent)
        self.label=label
        
        self.selector=QListWidget(self)
        
        addButton=QToolButton(self)
        addAction=QAction(self)
        addAction.setIcon(ICONS.PLUS)
        addAction.triggered.connect(self.addItem)
        addButton.setDefaultAction(addAction)
        
        
        subButton=QToolButton(self)
        subAction=QAction(self)
        subAction.setIcon(ICONS.MINUS)
        subAction.triggered.connect(self.removeCurrentItem)
        subButton.setDefaultAction(subAction)
        
        
        upButton=QToolButton(self)
        upAction=QAction(self)
        upAction.triggered.connect(self.moveCurrentItemUp)
        upButton.setDefaultAction(upAction)
        upButton.setArrowType(Qt.UpArrow)
        
        
        downButton=QToolButton(self)
        downAction=QAction(self)
        downAction.triggered.connect(self.moveCurrentItemDown)
        downButton.setDefaultAction(downAction)
        downButton.setArrowType(Qt.DownArrow)
        
        hBox=QHBoxLayout()
        vBox=QVBoxLayout()
        
        vBox.addWidget(addButton)
        vBox.addWidget(subButton)
        vBox.addSpacing(20)
        vBox.addWidget(upButton)
        vBox.addWidget(downButton)
        vBox.addStretch()
        
        hBox.addWidget(self.selector)
        hBox.addLayout(vBox)
        self.setLayout(hBox)
        
        self.counter=itertools.count(1)
    
    
    def moveCurrentItemUp(self):
        index=self.selector.currentRow()
        self.selector.insertItem(index-1, self.selector.takeItem(index))
        self.selector.setCurrentRow(index-1)
    
    
    def moveCurrentItemDown(self):
        index=self.selector.currentRow()
        self.selector.insertItem(index+1, self.selector.takeItem(index))
        self.selector.setCurrentRow(index+1)
        
        
    def getCurrentItemData(self):
        currentItem=self.selector.currentItem()
        if currentItem:
            data=currentItem.data(Qt.UserRole)
            if data:
                return data
        
    
    
    def setCurrentItemData(self, data):
        currentItem=self.selector.currentItem()
        if not currentItem:
            self.addItem(data)
        else:
            self.selector.currentItem().setData(Qt.UserRole, data)
    
    
    def addItem(self, data=None):
        label=self.label+str(next(self.counter))
        item=QListWidgetItem(label)
        if data:
            item.setData(Qt.UserRole, data)
        self.selector.addItem(item)
        self.selector.setCurrentItem(item)
    
    def removeCurrentItem(self):
        self.selector.takeItem(self.selector.currentRow())
    
    
    def clear(self):
        self.selector.clear()
        self.counter=itertools.count(1)
    
    
    def items(self):
        for i in range(self.selector.count()):
            yield self.selector.item(i)
    
    
    def setItems(self, items):
        self.clear()
        for item in items:
            if isinstance(item, QWidgetItem):
                self.selector.addItem(item)
            else:
                self.addItem(item)


#TODO: improve TextEditor
@initialize
class TextEditor(QTextEdit):
    def __init__(self):
        QTextEdit.__init__(self)
        
        self.setAcceptRichText(False)




class LetterSpinner(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)

        grid=QGridLayout()
        grid.setSpacing(0)

        
        self.textEntry=QLineEdit()
        self.textEntry.textChanged.connect(lambda:self.setValue(self.textEntry.text()))


        upButton=QToolButton(self)
        upAction=QAction(self)
        upAction.triggered.connect(self.stepUp)
        upButton.setDefaultAction(upAction)
        upButton.setArrowType(Qt.UpArrow)
        upButton.setMaximumSize(QSize(15, 12))
        
        
        downButton=QToolButton(self)
        downAction=QAction(self)
        downAction.triggered.connect(self.stepDown)
        downButton.setDefaultAction(downAction)
        downButton.setArrowType(Qt.DownArrow)
        downButton.setMaximumSize(QSize(15, 12))

        grid.addWidget(self.textEntry, 0, 0, 2, 1)
        grid.addWidget(upButton, 0, 1)
        grid.addWidget(downButton, 1, 1)

        self.setLayout(grid)

        self.text="A"
        self.textEntry.setText("A")
        
        
    def resizeEvent(self, event):
        event.size().setHeight(event.oldSize().height())
        event.accept()


    
    def getValue(self):
        return self.text

    
    def setValue(self, text):
        text=text.upper()
        if len(text) > 1:
            for char in text:
                if char.isalpha() and char != self.text:
                    self.text = char
                    self.textEntry.setText(char)
                    return
            self.textEntry.setText(self.text)

        elif len(text) == 1:
            self.text = text
            self.textEntry.setText(text)
    
    def step(self, amount=1):
        self.setValue(numToChar((charToNum(self.getValue())+amount)%26))


    def stepUp(self):
        self.step(1)


    def stepDown(self):
        self.step(-1)
##class LetterSpinner(QAbstractSpinBox):
##    def __init__(self, parent=None):
##        QAbstractSpinBox.__init__(self, parent)
##        self.oldText="A"
##        
####    def valueFromText(self, text):
####        if len(text)>1:
####            for char in text:
####                if char.isalpha() and char.upper() != self.oldText:
####                    text=char
####                    break
####        elif len(text)==0:
####            text="a"
####        self.oldText=text
####        return text
####    
####    
####    def textFromValue(self, value):
####        return value
##    
##    def validate(self, text, pos=None):
##        if len(text)==1 and text.isalpha():
##            return QValidator.Acceptable
##        elif len(text)==0:
##            return QValidator.Intermediate
##        return QValidator.Invalid
##    
##        
##        
##    def getValue(self):
##        return self.text()
##    
##    
##    def setValue(self, text):
##        if not self.validate(text) == QValidator.Acceptable:
##            text = self.fixup(text)
##            
##        self.lineEdit().setText(text)
##
##    
##    def fixup(self, text):
##        text=text.upper()
##        if len(text) > 1:
##            for char in text:
##                if char.isalpha() and char != self.text:
##                    self.text = char
##                    self.textEntry.setText(char)
##                    return
##            self.textEntry.setText(self.text)
##        
##        return self.oldText
##    
##    
##    def stepBy(self, amount):
##        self.setValue(numToChar((charToNum(self.getValue())+amount)%26))

    



class EntryGrid(QWidget):
    def __init__(self, rows, columns, entryWidget, parent=None):
        QWidget.__init__(self, parent)
        
        self.entryWidget=entryWidget
        
        self.grid=QGridLayout()
        self.grid.setSpacing(1)
        
        #Setting bacground color will give the appearence of borders arounf the individual cells
        
        for row in range(rows):
            for column in range(columns):
                self.grid.addWidget(entryWidget(self), row, column)
        
        self.setLayout(self.grid)
    
    def getItem(self, row, column):
        return self.grid.itemAtPosition(row, column).widget()
    
    
    def getAllItems(self):
        allRows=[]
        for x in range(self.grid.columnCount()):
            row=[]
            for y in range(self.grid.rowCount()):
                row.append(self.getItem(x, y))
            allRows.append(row)
        return allRows
