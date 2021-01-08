#NOTE:
#   You must register all new scripts here for them to work!!

from . import TXT
from . import DJCK #Custom File Type

from . import Misc

from ..Utilities import USER_HOME
from PySide.QtGui import *

cipherText = {}
cipherKeys = {}
item, filetype = None, None #To prevent RuntimeError on next line
for item in globals().values():
    try:
        filetype = item.TYPE
    except AttributeError:
        continue

    if filetype == "TEXT":
        cipherText[item.FILTER] = item
    elif filetype == "KEY":
        cipherKeys[item.FILTER] = item
del item


import os

lastFile=None
lastFilter=None


keysFilter=";;".join(cipherKeys.keys())
textFilter=";;".join(cipherText.keys())


def saveText(text):
    if not lastFile:
        saveTextAs(text)
        return
    try:
        cipherText[lastFilter].save(text, lastFile)
    except IOError:
        QMessageBox.critical(None, "Error", "Problem opening file \"%s\""%lastFile)


def saveTextAs(text):
    global lastFile, lastFilter
    file, filter = QFileDialog.getSaveFileName(dir=USER_HOME, filter=textFilter)
    try:
        cipherText[filter].save(text, file)
    except IOError:
        QMessageBox.critical(None, "Error", "Problem opening file \"%s\""%file)
        return
    lastFile, lastFilter = file, filter


def loadText():
    global lastFile, lastFilter
    file, filter = QFileDialog.getOpenFileName(dir=USER_HOME, filter=textFilter)
    try:
        text=cipherText[filter].load(file)
    except IOError:
        QMessageBox.critical(None, "Error", "Problem opening file \"%s\""%file)
        return
    lastFile, lastFilter = file, filter
    
    return text


def saveKey(key, cipher):
    file, filter = QFileDialog.getSaveFileName(dir=USER_HOME, filter=keysFilter)
    try:
        cipherKeys[filter].save(key, file, cipher)
    except IOError:
        QMessageBox.critical(None, "Error", "Problem opening file \"%s\""%file)
        return


def loadKey(cipher):
    file, filter = QFileDialog.getOpenFileName(dir=USER_HOME, filter=keysFilter)
    try:
        key = cipherKeys[filter].load(file, cipher)
    except IOError:
        QMessageBox.critical(None, "Error", "Problem opening file \"%s\""%lastFile)
        return
    except Misc.KeyError:
        QMessageBox.critical(None, "Error", "\"%s\" is not a valid file for %s"%(file, cipher))
        return
    return key