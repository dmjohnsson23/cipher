####################################################################
#              Dominick Johnson's Encription program               #
#              Using elements from previous programs,              #
#          such as Ceasar Cipher and One-Time Pad Cipher           #
# Plus addtional elements including new GUI and additional ciphers #
####################################################################
#Vinegre Cipher

NAME="Vigenère Cipher"


REPEAT="Repeat"
AUTOKEY="Autokey"


from .OneTimePad import _shift
from ..Utilities import removeNonAlpha, initialize, ENCODE, DECODE
from .. import Words
from ..GuiElements import LineInput
from itertools import cycle
from PySide2.QtGui import *
from PySide2.QtWidgets import *




def encode(message, key=None, extentionMethod=None):
    if not key:
        key=Interface.getKey()
    key=removeNonAlpha(key)
    if not extentionMethod:
        extentionMethod=Interface.extentionMethod
    
    out=[]
    
    if extentionMethod == REPEAT:
        key=cycle(key)
        for letter in message:
            if letter.isalpha():
                letter = _shift(letter, next(key), ENCODE)
            out.append(letter)
            
    elif extentionMethod == AUTOKEY:
        key=list(key)
        keyIter=key.__iter__()
        for letter in message:
            if letter.isalpha():
                letter = _shift(letter, next(keyIter), ENCODE)
                key.append(letter)
            out.append(letter)
    
    else:
        raise ValueError("\"%s\" is not a recognized extention method for a Vigenère Cipher key")
    
    return ''.join(out)
    

def decode(message, key=None, extentionMethod=None):
    if not key:
        key=Interface.getKey()
    key=removeNonAlpha(key)
    if not extentionMethod:
        extentionMethod=Interface.extentionMethod
    
    out=[]
    
    if extentionMethod == REPEAT:
        key=cycle(key)
        for letter in message:
            if letter.isalpha():
                letter = _shift(letter, next(key), DECODE)
            out.append(letter)
            
    elif extentionMethod == AUTOKEY:
        key=list(key)+list(removeNonAlpha(message))
        key=key.__iter__()
        for letter in message:
            if letter.isalpha():
                letter = _shift(letter, next(key), DECODE)
            out.append(letter)
    
    else:
        raise ValueError("\"%s\" is not a recognized extention method for a Vigenère Cipher key")
    
    return ''.join(out)    



@initialize
class Interface(QWidget):
    SAVE_LOAD=True
    HACK=False  #Set to true when hack() function is working
    def __init__(self):
        QWidget.__init__(self)
        grid=QGridLayout()
        grid.setSpacing(10)
        
        self.entry = LineInput(self, "Key: ")
        self.entry.setToolTip("Input key here")
        grid.addWidget(self.entry, 0, 0, 1, 2)
        
        keyRand=QPushButton("Randomize")
        keyRand.clicked.connect(lambda:self.setKey(Words.getRandomWord()))
        keyRand.setToolTip("Generate a pseudo-random key")
        grid.addWidget(keyRand, 0, 2)
        
        grid.addWidget(QLabel("Key Extention Method: "), 1, 0)
        
        self.extentionMethodBox=QComboBox(self)
        self.extentionMethodBox.setToolTip("The method for key extention")
        self.extentionMethodBox.addItems((REPEAT, 
                                       AUTOKEY))
        grid.addWidget(self.extentionMethodBox, 1, 1)
        
        grid.addWidget(QWidget(), 2, 0, 6, 7) #Spacer

        self.setLayout(grid)

    def getKey(self):
        return self.entry.text()
    
    
    def setKey(self, value):
        self.entry.setText(value)
    
    @property
    def extentionMethod(self):
        return self.extentionMethodBox.currentText()
    
  