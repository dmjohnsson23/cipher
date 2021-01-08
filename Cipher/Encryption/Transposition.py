from ..Utilities import chunker, initialize
from itertools import zip_longest
from PySide.QtGui import *

NAME="Simple Transposition"



def encode(message, key=None):
    if key is None:
        key=Interface.getKey()
    return "".join("".join(x) for x in zip_longest(*chunker(message, key), fillvalue=" "))



def decode(message, key=None):
    if key is None:
        key=Interface.getKey()
    n=len(message)//key
    return "".join("".join(x) for x in zip_longest(*chunker(message, n), fillvalue="")).rstrip()

from PySide.QtGui import *
@initialize
class Interface(QWidget):
    SAVE_LOAD=False
    HACK=False # for now
    def __init__(self):
        QWidget.__init__(self)
        grid=QGridLayout()
        grid.setSpacing(10)


        self.key=QSpinBox()
        self.key.setPrefix("Grid Size: ")
        self.key.setRange(1, 100)
        self.key.setToolTip("The length of the transposition grid")
        grid.addWidget(self.key, 0, 0)

        keyRand=QPushButton("Randomize")
        keyRand.clicked.connect(lambda
                                      key=self.key:
                                      key.setValue(random.randint(1, 100)))
        keyRand.setToolTip("Generate a random shift value")
        grid.addWidget(keyRand, 0, 1)

        grid.addWidget(QWidget(), 2, 1, 4, 5) #Spacer

        self.setLayout(grid)

    def getKey(self):
        return self.key.value()
    
    
    def setKey(self, value):
        self.key.setValue(value)