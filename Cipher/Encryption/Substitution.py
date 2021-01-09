####################################################################
#              Dominick Johnson's Encription program               #
#              Using elements from previous programs,              #
#          such as Ceasar Cipher and One-Time Pad Cipher           #
# Plus addtional elements including new GUI and additional ciphers #
####################################################################
#Substitution Cipher
import sys
print(sys.argv)
import random
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from ..Utilities import LETTER_GOODNESS, getkey, initialize, removeNonAlpha, removeDuplicates
from ..GuiElements import LineInput
from ..LetterMath import charToNum, numToChar
from string import ascii_lowercase as alphabet

NAME="Simple Substitution"



def _swap(letter, key, abcs):
    ABCS=abcs.upper()
    if letter in abcs:
        key=key.lower()
        return key[abcs.index(letter)]
    elif letter in ABCS:
        key=key.upper()
        return key[ABCS.index(letter)]
    else:
        return letter

def randomKey(message=""):
    letters=list(alphabet.upper())
    random.shuffle(letters)
    return ''.join(letters)


def checkKey(key, message=""):
    key=key.lower()
    if not len(key)==26:
        return False
    #Key must be exactly 26 chars long
    for letter in alphabet:
        if letter not in key:
            return False
        #Key must have one of each letter
    return True

def keyFromWord(word=None):   #Still Buggy?
    if not word:
        word, ok = QInputDialog.getText(None, 
                                        "Key from Keyword or Phrase", 
                                        "Enter a keyword or phrase")
        if not ok:
            return
    word=word.upper()
    word=removeNonAlpha(word)
    word=removeDuplicates(word)
    
    # now append any unused letters
    for letter in alphabet.upper():
        if not letter in word:
            word+=letter
    
    return word


##@initialized
##class KeyAlgorithms:
##    def __init__(self):
##        self.algs={
##                   "Affine":self.AffineUi,
##                   "Atbash":self.Atbash
##                   }
##    
##    def getKey(self):
##        pass
##    
##    
##    def AffineUi(self):
##        def submit():
##            pass
##        window.QWidget(self)
##        box=QHBoxLayout()
##        spinA=QSpinBox(window)
##        spinA.setPrefix("a: ")
##        spinA.setRange(0, 26)
##    
##    def Affine(self, a, b):
##        out=[]
##        for letter in alphabet:
##            out.append(numToChar(((a*charToNum(letter))+b)%26))
##        return "".join(out)
##    
##    
##    def Atbash(self):
##        return alphabet[::-1].upper()
    
    
    
def hack(message):
    letterGoodness=LETTER_GOODNESS.copy()
    #First, get frequency of letters in message
    freq={letter:0 for letter in alphabet}
    for letter in message:
        if letter.isalpha():
            freq[letter.lower()]+=1
    #Then use that information to construct a key
    key=[" "]*26
    for x in range(26):
        maxG=max(letterGoodness.values())
        maxF=max(freq.values())
        theLetter=getkey(freq, maxF)
        keyLetter=getkey(letterGoodness, maxG)
        key[alphabet.index(theLetter)]=keyLetter
        letterGoodness.pop(keyLetter)
        freq.pop(theLetter)
    #Turn the key into a usable format
    outkey=""
    for letter in key:
        outkey+=letter
    outkey=decode(alphabet.upper(), outkey.upper())
    #And try to decode the message with that key
    Interface.setKey(outkey)
    return encode(message, outkey)
            

def encode (message, key=None):
    if not key:
        key = Interface.getKey()
    if not checkKey(key):
        return
    return ''.join(_swap(letter, key, alphabet) for letter in message)
       

def decode (message, key=None):
    if not key:
        key = Interface.getKey()
    if  not checkKey(key):
        return
    return ''.join(_swap(letter, alphabet, key.lower()) for letter in message)



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
        keyRand.clicked.connect(lambda: self.setKey(randomKey()))
        keyRand.setToolTip("Generate a pseudo-random key")
        grid.addWidget(keyRand, 0, 2)
        
        keyword=QPushButton("From Keyword")
        keyword.clicked.connect(lambda: self.setKey(keyFromWord() or self.key.text()))
        keyword.setToolTip("Generate a key from a word or phrase")
        grid.addWidget(keyword, 0, 3)
        
##        keyAlg=QPushButton("From Algorithm")
##        keyAlg.clicked.connect(lambda
##                               key=self.entry:
##                               key.setText(KeyAlgorithms.getKey() or key.text()))
##        keyAlg.setToolTip("Generate a key based on an algorithm")
##        grid.addWidget(keyAlg, 0, 3)
        
        grid.addWidget(QWidget(), 1, 0, 6, 7) #Spacer

        self.setLayout(grid)

    def getKey(self):
        return self.entry.text().upper()
    
    
    def setKey(self, value):
        self.entry.setText(value.upper())
