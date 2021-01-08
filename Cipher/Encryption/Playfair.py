####################################################################
#              Dominick Johnson's Encription program               #
#              Using elements from previous programs,              #
#          such as Ceasar Cipher and One-Time Pad Cipher           #
# Plus addtional elements including new GUI and additional ciphers #
####################################################################
#Playfair Cipher

#TODO: Bugs
##> letters in the same pair as the missing letter disappear during encryption




import random
from string import ascii_lowercase as alphabet
from ..Utilities import ENCODE, DECODE, initialize, chunker
from ..GuiElements import EntryGrid, LetterSpinner
from PySide.QtGui import *
from PySide.QtCore import *
from .Substitution import keyFromWord

NAME="Playfair"




class Grid:
    def __init__(self, key):
        key=key.upper()
        self.key=tuple(tuple(items) for items in chunker(key, 5))
        self.missing=self.findMissing(key)
    
    
    def findMissing(self, key):
        for letter in alphabet.upper():
            if letter not in key:
                return letter
    
    
    def swap(self, letter1, letter2, mode=ENCODE):
        x1, y1=self.getCoord(letter1)
        x2, y2=self.getCoord(letter2)
        
        addition=1 if mode==ENCODE else -1

        if y1==y2:
            #Same Row
            return self.key[(x1+addition)%5][y1]+self.key[(x2+addition)%5][y2]
        elif x1==x2:
            #same Column
            return self.key[x1][(y1+addition)%5]+self.key[x2][(y2+addition)%5]
        else:
            return self.key[x1][y2]+self.key[x2][y1]
    

    def getCoord(self, letter):
        letter=letter.upper()
        for y in range (5):
            for x in range (5):
                if self.key[x][y]==letter:
                    return (x, y)
                
                
    def getLetter(self, x, y):
        return self.key[x][y]
    
    
            

def randomKey(message=""):
    key=alphabet
    key=key.replace(random.choice(key), "")
    key=list(key)
    random.shuffle(key)
    return "".join(key)




def checkKey(key, message=""):
    numMissing=0
    #key must be 25 letters long
    if len(key)!=25:
        return False
    key=key.lower()
    #key must contain every letter of the alphabet except one exactly one time
    for letter in alphabet:
        if not letter in key:
            numMissing+=1
            if numMissing>1:
                return False
    #if everything works out, then the key is good
    return True



def baseEncode (message, key=None, fillLetter='x', mode=ENCODE):
    if not key:
        key=Interface.getKey()
    if not checkKey(key):
        return
    fillLetter=fillLetter.lower() #just in case
    grid=Grid(key)
    if grid.missing.lower()==fillLetter:
        fillLetter=random.choice("qwzxv".replace(fillLetter, ""))
    
    letter1=""
    letter2=""
    inBetween=[]
    ciphered=[]
    for letter in message:
        if letter.isalpha():
            if letter.upper()==grid.missing:
                ciphered.append(letter)
            elif not letter1: # first letter has not been assigned
                letter1=letter.lower()
                isUpper1=letter.isupper()
            else:
                letter2=letter.lower()
                isUpper2=letter.isupper()
                
                #now start encoding
                if letter1==letter2:
                    letterHold=letter2
                    isUpperHold=isUpper2
                    letter2=fillLetter
                    isUpper2=False
                    
                    letter1, letter2 = grid.swap(letter1, letter2, mode)
                    if not isUpper1: letter1=letter1.lower()
                    if not isUpper2: letter2=letter2.lower()
                    
                    ciphered.append(letter1)
                    ciphered += inBetween
                    ciphered.append(letter2)
                    
                    letter1=letterHold
                    isUpper1=isUpperHold
                    letter2=""
                    inBetween=[]
                
                else:
                    letter1, letter2 = grid.swap(letter1, letter2, mode)
                    if not isUpper1: letter1=letter1.lower()
                    if not isUpper2: letter2=letter2.lower()
                    
                    ciphered.append(letter1)
                    ciphered += inBetween
                    ciphered.append(letter2)
                    
                    letter1=""
                    letter2=""
                    inBetween=[]
        else: #not a letter
            if letter1:
                inBetween.append(letter)
            else:
                ciphered.append(letter)
    return "".join(ciphered)




def encode(message, key=None, fillValue='x'):
    return baseEncode(message, key, fillValue, ENCODE)



def decode(message, key=None, fillValue='x'):
    return baseEncode(message, key, fillValue, DECODE)
    

@initialize
class Interface(QWidget):
    SAVE_LOAD=True
    HACK=False
    
    def __init__(self):
        QWidget.__init__(self)
        grid=QGridLayout()
        grid.setSpacing(10)
        
##        self.table=QTableWidget(5, 5)
##        delegate=QItemDelegate() #TODO: fix bug "RuntimeError: Internal C++ object (PySide.QtGui.QItemDelegate) already deleted."
##        delegate.createEditor(QSpinBox())
##        self.table.setItemDelegate(delegate)  
        
        self.entryGrid=EntryGrid(5, 5, LetterSpinner)
        self.entryGrid.setMaximumSize(QSize(300, 300))
        
        randomizer=QPushButton("Randomize")
        randomizer.setToolTip("Generate a pseudo-random key")
        randomizer.clicked.connect(lambda:self.setKey(randomKey()))
        
        fromWord=QPushButton("From Keyword")
        fromWord.setToolTip("Generate a key from a word or phrase")
        fromWord.clicked.connect(lambda:self.setKey(keyFromWord()))
        
        
        grid.addWidget(self.entryGrid, 0, 0, 5, 2)
        grid.addWidget(randomizer, 2, 2)
        grid.addWidget(fromWord, 3, 2)
        grid.addWidget(QWidget(), 6, 0, 1, 6)
        self.setLayout(grid)
    
    
    def getKey(self):
        out=[]
        for x in range(5):
            for y in range(5):
                out.append(self.entryGrid.getItem(x, y).getValue())
        return "".join(out)
    
    def setKey(self, key):
        items=iter(key)
        for x in range(5):
            for y in range(5):
                self.entryGrid.getItem(x, y).setValue(next(items))
    