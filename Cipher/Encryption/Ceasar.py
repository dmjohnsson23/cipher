####################################################################
#              Dominick Johnson's Encription program               #
#              Using elements from previous programs,              #
#          such as Ceasar Cipher and One-Time Pad Cipher           #
# Plus addtional elements including new GUI and additional ciphers #
####################################################################
#Ceasar Cipher
from ..Utilities import initialize
from ..LetterMath import letterAdd
from .. import EnglishChecker
import random

NAME="Ceasar Cipher"


def _shift(inp, shift):
    if inp.isalpha():
        return letterAdd(inp, shift)
    else:
        return inp


def randomKey(message=""):
    return str(random.randint(1, 25))

def checkKey(key, message=""):
    return key.isdigit() and 0<int(key)<26


def encode(message, key=None):
    if key is None:
        key=Interface.getKey()
    string=""
    for letter in message:
        string+=_shift(letter, key)
    return string


def decode(message, key=None):
    if key is None:
        key=Interface.getKey()
    string=""
    for letter in message:
        string+=_shift(letter, 0-key)
    return string


def hack(message):
    shortMessage=message[:100] #crop to 100 chars when checking (for optimization)
    bestPercent=0
    bestKey=None
    for key in range(26):
        decoded=decode(shortMessage, key)
        percent=EnglishChecker.percentEnglish(decoded)
        if percent > 70:
            #pretty good chance it's English
            bestKey=key
            break
        elif percent > bestPercent:
            bestPercent = percent
            bestKey = key
    Interface.setKey(bestKey)
    return decode(message, bestKey)

from PySide.QtGui import *
@initialize
class Interface(QWidget):
    SAVE_LOAD=False
    HACK=True
    def __init__(self):
        QWidget.__init__(self)
        grid=QGridLayout()
        grid.setSpacing(10)


        self.key=QSpinBox()
        self.key.setPrefix("Shift Value: ")
        self.key.setRange(1, 25)
        self.key.setToolTip("The number of places to shift the letters of your message")
        grid.addWidget(self.key, 0, 0)

        keyRand=QPushButton("Randomize")
        keyRand.clicked.connect(lambda
                                      key=self.key:
                                      key.setValue(random.randint(1, 25)))
        keyRand.setToolTip("Generate a random shift value")
        grid.addWidget(keyRand, 0, 1)

        grid.addWidget(QWidget(), 2, 1, 4, 5) #Spacer

        self.setLayout(grid)

    def getKey(self):
        return self.key.value()
    
    
    def setKey(self, value):
        self.key.setValue(value)
        

