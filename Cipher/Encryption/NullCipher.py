####################################################################
#              Dominick Johnson's Encription program               #
#              Using elements from previous programs,              #
#          such as Ceasar Cipher and One-Time Pad Cipher           #
# Plus addtional elements including new GUI and additional ciphers #
####################################################################
#Null Cipher

import random
from ..Utilities import initialize
from .. import Words
from PySide2.QtGui import *
from PySide2.QtWidgets import *

NAME="Null Cipher"




def encode(message):
    #Create the cipher text
    ciphered=[]
    cap=True
    firstTime=True
    for letter in message:
        if letter.isalpha():
            if not firstTime:
                ciphered.append(" ")
            else:
                firstTime=False
                
                
            if cap:
                ciphered.append(Words.getRandomWord(letter).capitalize())
                cap=False
            else:
                ciphered.append(Words.getRandomWord(letter).lower())
        elif letter in " .,?!\n\t":
            if cap==False:
                ciphered.append(random.choice((".", ".", ".", ",", ",", "?", "!")))
                cap=True
        else:
            ciphered.append(letter)
            
    return "".join(ciphered)


def decode(message):
    first=True
    out=[]
    for letter in message:
        if first and letter.isalpha():
            out.append(letter)
            first=False
        elif letter.isspace():
            first=True
        elif letter in ",.?!":
            out.append(" ")
        elif not letter.isalpha():
            out.append(letter)
            
    return "".join(out).title()



        
@initialize
class Interface(QWidget):
    SAVE_LOAD=False
    HACK=False