####################################################################
#              Dominick Johnson's Encription program               #
#              Using elements from previous programs,              #
#          such as Ceasar Cipher and One-Time Pad Cipher           #
# Plus addtional elements including new GUI and additional ciphers #
####################################################################
#One-Time Pad Cipher
from ..Utilities import initialize, removeNonAlpha, ENCODE, DECODE, countAlpha
from ..GuiElements import TextEditor
from random import SystemRandom
random=SystemRandom()
from ..LetterMath import charToNum, numToChar, letterAdd

NAME="One Time Pad"



def _shift(letter, keyLetter, mode):
    if letter.isalpha():
        keyLetter=keyLetter.upper()
        
        if mode==ENCODE:
            shift=charToNum(keyLetter)
        elif mode==DECODE:
            shift=0-charToNum(keyLetter)

        return letterAdd(letter, shift)
    
    else:
        #For non-alphabet symbols (EG Spaces) to remain unchanged
        return letter


    
def randomKey(message):
    ok=QMessageBox.warning(None, "Warning!", "With a truely random key, the One-Time pad cipher is unbreakable. However, computers cannot create "
                      "a truely random key. It is recomended that you use a truely random key, such as one generated by random.org's random string generator.", 
                      QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
    if ok==QMessageBox.Ok:
        return _randomKey(countAlpha(message))
    else:
        return ""
    
    
def _randomKey(length):
    key=""
    for x in range(length):
        key+=random.choice("Q W E R T Y U I O P A S D F G H J K L Z X C V B N M".split())
    return key


def checkKey(key, message):
    return _checkKey(key, countAlpha(message))


def _checkKey(key, messageLen):
    if len(key)>=messageLen and key.isalpha(): return True
    else: return False


def encode(message, key=None):
    if not key:
        key=Interface.getKey()
    if not _checkKey(key, countAlpha(message)):
        return
        
    keyIter=key.__iter__()
    out=''.join(_shift(letter, next(keyIter), ENCODE) 
                if letter.isalpha() else letter for letter in message)
    return out


def decode(message, key=None):
    if not key:
        key=Interface.getKey()
    if not _checkKey(key, countAlpha(message)):
        return
    
    keyIter=key.__iter__()
    out=''.join(_shift(letter, next(keyIter), DECODE) 
                if letter.isalpha() else letter for letter in message)
    return out


from PySide2.QtGui import *
from PySide2.QtWidgets import *
@initialize
class Interface(QWidget):
    SAVE_LOAD=True
    HACK=False
    def __init__(self):
        QWidget.__init__(self)

        grid=QGridLayout()
        grid.setSpacing(10)



        self.key=QTextEdit()
        self.key.setToolTip("Type your One-Time Pad key here. It must be a "
                               "string of letters of the\nsame length as your message. "
                               "No puctuation or symbols allowed")
        self.key.setAcceptRichText(False)

        keyRand=QPushButton("Randomize")
        keyRand.clicked.connect(lambda
                                inp=TextEditor,
                                keyInp=self.key:
                                keyInp.setText(randomKey(removeNonAlpha(inp.toPlainText()))))
        keyRand.setToolTip("Generate a pseudo-random key. WARNING: Less secure than a true random key!")
        grid.addWidget(QLabel("Key: "), 1, 1)
        grid.addWidget(keyRand, 1, 2)
        grid.addWidget(self.key, 2, 1, 1, 8)
        

        self.setLayout(grid)
        
    
    def getKey(self):
        return self.key.toPlainText().upper()
    
    
    def setKey(self, value):
        self.key.setText(value.upper())
