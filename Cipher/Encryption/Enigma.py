####################################################################
#              Dominick Johnson's Encription program               #
#              Using elements from previous programs,              #
#          such as Ceasar Cipher and One-Time Pad Cipher           #
# Plus addtional elements including new GUI and additional ciphers #
####################################################################
#Enigma Machine

#ready for debug


import random

#custom Moduels
from ..Utilities import getkey, initialize
from .Substitution import checkKey, randomKey, keyFromWord
from ..LetterMath import letterAdd, modAdd, numToChar, charToNum
from ..GuiElements import ListSelector, LineInput, ICONS
from PySide2.QtCore import Qt

NAME="Enigma Machine"


BACKWARD="Backward"
FORWARD="Forward"
 
class Rotor:
    def __init__(self, mapping:"A substitution-cipher style key",
                 initRot:"Initaial Rotation"=0):
        if not checkKey(mapping):
            raise ValueError("\"%s\" is not a valid key")
        self.mapping=[charToNum(x) for x in mapping]
        self.rot=initRot

    def rotate(self) -> "Returns True if next rotor needs rotated, else False":
        self.rot=modAdd(self.rot, 1)
        ##print("Rotation at %s"%self.rot)
        
        if self.rot==0:
            ##print("next")
            return True
        else:
            return False


    def _acountForRot(self, value, direction=FORWARD):
        if direction==FORWARD:
            return modAdd(value, -self.rot)
        else: #BACKWARD
            return modAdd(value, self.rot)


##    def encode(self, contact, direction=FORWARD):        
##        if direction==FORWARD:
##            x=self._acountForRot(contact)
##            x=self.mapping[x]
##            x=self._acountForRot(x, BACKWARD)
##        else: #BACKWARD
##            x=self._acountForRot(contact, BACKWARD)
##            x=self.mapping.index(x)
##            x=self._acountForRot(x)
##        return x
    
    def encode(self, contact, direction=FORWARD):
        x=self._acountForRot(contact)
        
        if direction==FORWARD:
            x=self.mapping[x]
        else: #BACKWARD
            x=self.mapping.index(x)
            
        x=self._acountForRot(x, BACKWARD)
        return x
    
def _reflect(contact):
    if contact<=13:
        return contact+13
    elif contact>13:
        return contact-13



def checkFullKey(keys):
        for key in keys:
                if not checkKey(key[0] if isinstance(key, (tuple, list)) else key):
                        return False
        return True

            


##def encrypt(message, inkey, mode="Encode"):
##    if not inkey and mode=="Decode":
##        mb.showerror(title="Error", message="Error\nAutodecode not available for Enigma Machine Cipher")
##        return ("", "")
##    if not inkey and mode=="Encode":
##        inkey=randomKey()
##    keys=inkey.split(":")
##    if checkKey(keys):
##        rotors=[]
##        for key in keys:
##            rotors.append(Rotor(key))
##            ciphered=""
##        for letter in message:
##            if letter.isalpha():
##                ##print ("\nProcessing", letter)
##                isUpper=letter.isupper()
##                num=charToNum(letter)
##                x=0
##                for rotor in rotors:
##                    ##print ("Forward through rotor", x)
##                    x+=1
##                    num=rotor.encode(num)
##                x=0
##                ##print ("Reflecting")
##                num=_reflect(num)
##                for rotor in reversed(rotors):
##                    ##print ("Backward through rotor", x)
##                    num=rotor.encode(num, BACKWARD)
##                    x+=1
##                ciphered+=numToChar(num, isUpper)
##                x=0
##                for rotor in rotors:
##                    ##print ("rotating rotor ", x)
##                    x+=1
##                    if not rotor.rotate():
##                        #rotor.rotate returns True if it reaches pass point
##                        #meaning next rotor needs to rotate. Otherwise, it
##                        #returns False, thereby breaking the loop.
##                        break
##            else: ciphered+=letter #For non-alpha
##        return (ciphered, inkey)
##    else:
##        mb.showerror(title="Error", message="Error: Invalid Key\n"
##                    "For Enigma Machine, enter one substitution "
##                    "style key for every rotor, seperating them "
##                    "with colons (:)")
##        return ("" ,"")


##def demo(msg="Hello World! I like Pie! Blah Blah Blah."
##         "Ding dong ding dong.... Llama llama. I LIKE PIE A LOT!!!",
##         key=randomKey()):
##    print("Oringinal Message:", msg)
##    print()
##    cipher, x=encrypt(msg, key)
##    print("Encrypted to:", cipher)
##    decipher, x=encrypt(cipher, key)
##    print()
##    print("Decrypted to:", decipher)
##    print()
##    if msg==decipher: print("Succsess!")
##    else: print("Failure... )-:")

def encode(message, key=None):
    if not key:
        key = Interface.getKey()
    if not checkFullKey(key):
        return
    
    rotors=[]
    for mapping in key:
        if isinstance(mapping, (tuple, list)):
            assert len(mapping)==2
            mapping, initRot = mapping
        else:
            initRot=0
        rotors.append(Rotor(mapping, initRot))
        
    ciphered=[]
    
    for letter in message:
        if letter.isalpha():
            isUpper=letter.isupper()
            num=charToNum(letter)
            
            for rotor in rotors:
                num=rotor.encode(num)
            num=_reflect(num)
            
            for rotor in reversed(rotors):
                num=rotor.encode(num, BACKWARD)
            ciphered.append(numToChar(num, isUpper))
            
            for rotor in rotors:
                if not rotor.rotate():
                    #rotor.rotate returns True if it reaches pass point
                    #meaning next rotor needs to rotate. Otherwise, it
                    #returns False, thereby breaking the loop.
                    break
        else: ciphered.append(letter) #For non-alpha
    return ''.join(ciphered)


def decode(message, key=None):
    #for Enigma, encoding is the same process as decoding, so
    return encode(message, key)
    


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
        
        self.selector=ListSelector(self, "Rotor ")
        self.selector.selector.currentItemChanged.connect(self.updateEntryFeilds)
        grid.addWidget(self.selector, 0, 0, 6, 3)
        
        
        
        self.entry = LineInput(self, "Rotor Mapping: ")
        self.entry.setToolTip("Input rotor mapping here")
        self.entry.lineEdit.editingFinished.connect(self.updateMapping)
        grid.addWidget(self.entry, 1, 3, 1, 3)
        
        keyRand=QPushButton("Randomize")
        keyRand.clicked.connect(self.randomKey)
        keyRand.setToolTip("Generate a pseudo-random mapping")
        grid.addWidget(keyRand, 2, 4)
        
        keyword=QPushButton("From Keyword")
        keyword.clicked.connect(self.keyFromWord)
        keyword.setToolTip("Generate a mapping from a word or phrase")
        grid.addWidget(keyword, 2, 5)
        
        
        fullRand=QPushButton("Randomize All")
        fullRand.clicked.connect(self.fullRandomKey)
        fullRand.setToolTip("Generate an random number of rotors with randomized mappings")
        grid.addWidget(fullRand, 5, 6)
        
        
        self.initRot=QSpinBox()
        self.initRot.setPrefix("Initial Rotation: ")
        self.initRot.setRange(0, 25)
        self.initRot.setToolTip("The initial rotation of this rotor")
        self.initRot.valueChanged.connect(self.updateMapping)
        grid.addWidget(self.initRot, 4, 3)

        self.setLayout(grid)

    def getKey(self):
        return [mapping.data(Qt.UserRole) for mapping in self.selector.items()]
    
    
    def setKey(self, mappings):
        self.selector.setItems(mappings)
    
    
    def fullRandomKey(self):
        self.selector.clear()
        for x in range(random.randint(3, 6)):
            self.selector.addItem((randomKey(), random.randint(0, 25)))
    
    
    def randomKey(self):
        key=randomKey()
        self.selector.setCurrentItemData((key, random.randint(0, 25)))
        self.entry.setText(key)
        self.updateMapping()
    
    
    def keyFromWord(self):
        key=keyFromWord()
        if key:
            self.selector.setCurrentItemData(key)
            self.entry.setText(key)
        self.updateMapping()
    
    
    def updateMapping(self):
        data=(self.entry.text(), self.initRot.value())
        self.selector.setCurrentItemData(data)
        if checkKey(data[0]):
            self.selector.selector.currentItem().setIcon(ICONS.GREEN_CHECK)
        else:
            self.selector.selector.currentItem().setIcon(ICONS.RED_X)
    
    
    def updateEntryFeilds(self):
        data=self.selector.getCurrentItemData()
        if not data is None:
            text, initRot=data
        else:
            text=""
            initRot=0
            
        self.entry.setText(text)
        self.initRot.setValue(initRot)

        
        
    
        

