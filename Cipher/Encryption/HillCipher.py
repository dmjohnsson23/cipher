import random
from ..Utilities import initialize
from ..LetterMath import numToChar, charToNum, modMatInv
from ..GuiElements import EntryGrid
from PySide.QtGui import *
from PySide.QtCore import *

NAME="Hill Cipher"

try:
    import numpy
##    from decimal import Decimal as dec

except:
    import webbrowser
    def encode(*a, **k): pass
    def decode(*a, **k): pass
    
    @initialize
    class Interface(QLabel):
        SAVE_LOAD=False
        HACK=False
        def __init__(self, parent=None):
            QLabel.__init__(self, "Sorry, this cipher requires <a href=\"www.numpy.org\">numpy</a> to be installed")
            self.linkActivated.connect(lambda:webbrowser.open("www.numpy.org"))
    

else:
    def encode(message, key=None):
        if key is None:
            key=Interface.getKey()
            
        key=numpy.matrix(key)
        
        if not checkMatrix(key):
            QMessageBox.critical(None, "Key Error", 
                                 "The given key matrix is not invertible, it cannot be used for the Hill Cipher")
            return
        
        return baseEncode(message, key)
    
    def decode(message, key=None):
        if key is None:
            key=Interface.getKey()
            
        key=numpy.matrix(key)
        
        
        if not checkMatrix(key):
            QMessageBox.critical(None, "Key Error", 
                                 "The given key matrix is not invertible, it cannot be used for the Hill Cipher")
            return
        
        key=modMatInv(key, 26) #Invert mod 26
        return baseEncode(message, key)
    
    
    def baseEncode(message, keyMatrix):
        letters=[]
        uppercases=[]
        inBetween1=[]
        inBetween2=[]
        out=[]
        for char in message:
            if char.isalpha():
                letters.append(char)
                uppercases.append(char.isupper())
                
                if len(letters)==3:
                    #Encrypt letters 3 at a time
                    letterMatrix=lettersToMatrix(letters)
                    
                    encipheredMatrix = keyMatrix * letterMatrix
                    ##encipherdMatrix=numpy.rint(encipheredMatrix) #round to nearest int
                    
                    letters=matrixToLetters(encipheredMatrix % 26)
                    
                    #do some work with capitalization
                    for index, isUpper in zip(range(3), uppercases):
                        if not isUpper:
                            letters[index]=letters[index].lower()
                    
                    
                    #Now add everything into 'out'
                    
                    out.append(letters[0])
                    out += inBetween1
                    out.append(letters[1])
                    out += inBetween2
                    out.append(letters[2])
                    
                    #and start over
                    letters=[]
                    uppercases=[]
                    inBetween1=[]
                    inBetween2=[]
                    
                    
            else:
                #Not a letter
                if len(letters)==0:
                    out.append(char)
                    
                elif len(letters)==1:
                    inBetween1.append(char)
                    
                elif len(letters)==2:
                    inBetween2.append(char)
        return "".join(out)
    
    
##    def decimalize(key):
##        for x in range(3):
##            for y in range(3):
##                key[x][y]=dec(key[x][y])
##        return key
##    
##    
    def checkMatrix(matrix):
        return round(numpy.linalg.det(matrix)) != 0
    
    
    def randomKey(message=""):
        [[random.randint(1, 100) for x in range(3)] for y in range(3)]
    
    
    def lettersToMatrix(strings):
        return numpy.matrix([charToNum(char) for char in strings]).T  #matrix.T = transpose

    
    def matrixToLetters(matrix):
        return [numToChar(int(num)) for num in matrix.flat]
    
##    
##    def matrixDet2x2(matrix):
##        a=matrix[(0, 0)]
##        b=matrix[(0, 1)]
##        c=matrix[(1, 0)]
##        d=matrix[(1, 1)]
##        return (a*d-c*b) % 26
##    
##    
##    def matrixDet3x3(matrix):
##        return (matrix[0, 0]*matrixDet2x2(matrixMinor(matrix, 0, 0))-
##                matrix[0, 1]*matrixDet2x2(matrixMinor(matrix, 0, 1))+
##                matrix[0, 2]*matrixDet2x2(matrixMinor(matrix, 0, 2)))
##    
##    
##    def matrixApplySignChart(matrix):
##        matrix[1, 0]*=-1
##        matrix[0, 1]*=-1
##        matrix[1, 2]*=-1
##        matrix[2, 1]*=-1
##
##    
##    def matrixInverse3x3(matrix):
##        n=matrix.copy()
##        for x in range(3):
##            for y in range(3):
##                n[x, y]=matrixDet2x2(matrixMinor(matrix, x, y))
##                
##        matrixApplySignChart(n)
##        n=n.T
##        print(n)
##        scalar=1/(matrixDet3x3(matrix) % 26)
##        print(scalar)
##        for x in range(3):
##            for y in range(3):
##                n[x, y]*=scalar
##        return n % 26
##        
##                         
##    
##    
##    #adapted from http://stackoverflow.com/questions/3858213/numpy-routine-for-computing-matrix-minors
##    def matrixMinor(arr,i,j):
##        # ith row, jth column removed
##        return arr[numpy.array(list(range(i))+list(range(i+1,arr.shape[0])))[:,numpy.newaxis],
##                   numpy.array(list(range(j))+list(range(j+1,arr.shape[1])))]
    
    
    
    @initialize
    class Interface(QWidget):
        SAVE_LOAD=True
        HACK=False
        
        def __init__(self):
            QWidget.__init__(self)
            grid=QGridLayout()
            grid.setSpacing(10)
            
            
            self.entryGrid=EntryGrid(3, 3, QSpinBox)
            self.entryGrid.setMaximumSize(QSize(150, 100))
            
            randomizer=QPushButton("Randomize")
            randomizer.setToolTip("Generate a pseudo-random matrix")
            randomizer.clicked.connect(lambda:self.setKey(randomKey()))
            
            
            
            grid.addWidget(self.entryGrid, 0, 0, 2, 1)
            grid.addWidget(QWidget(), 2, 0, 5, 6)
            self.setLayout(grid)
        
        
        def getKey(self):
            key = self.entryGrid.getAllItems()
            for x in range(3):
                for y in range(3):
                    key[x][y]=key[x][y].value()
            return key
        
        def setKey(self, key):
            for x in range(3):
                for y in range(3):
                    self.entryGrid.getItem(x, y).setValue(key[x][y])