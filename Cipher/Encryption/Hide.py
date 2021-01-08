####################################################################
#              Dominick Johnson's Encription program               #
#              Using elements from previous programs,              #
#          such as Ceasar Cipher and One-Time Pad Cipher           #
# Plus addtional elements including new GUI and additional ciphers #
####################################################################
#Hide

from PySide.QtGui import *
import random
from ..Utilities import initialize


NAME="Hide"


from string import printable as allChars

freeChars=[]
def _getAvailable(message):
    global freeChars
    freeChars=allChars[:]
    for letter in message:
        if letter in freeChars:
            freeChars.replace(letter, '')
    
def encode(message):
    mess=""
    _getAvailable(message)
    if len(freeChars)<2:
        QMessageBox.critical(None, "Error", "Error:\nNot enough unused characters")
        return
    message=list(message)
    for x in range(len(message)):
        for n in range(0, random.randint(50, 2000)):
            mess+=random.choice(freeChars)
        mess+=message[0]
        message.pop(0)
    for n in range(0, random.randint(50, 2000)):
        mess+=random.choice(freeChars)
    return mess


def decode(mess):
    freq={}
    for letter in mess:
        try:
            freq[letter]+=1
        except:
            freq[letter]=1
    ave=sum(freq.values())/(len(freq.values())*2)
    message=""
    for letter in mess:
        if freq[letter]<ave:
            message+=letter
    return message


@initialize
class Interface(QWidget):
    SAVE_LOAD=False
    HACK=False
