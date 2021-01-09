from PySide2.QtCore import *
from ..Utilities import ENCODE, DECODE, HACK


class ThreadedEncryption(QThread):
    
    encryptionFinished=Signal(str, str)
    
    def __init__(self, message, cipher, mode):
        QThread.__init__(self)
        self.message=message
        self.cipher=cipher
        self.mode=mode
        
        
    def run(self):
        if self.mode==ENCODE:
            ciphered=self.cipher.encode(self.message)
        elif self.mode==DECODE:
            ciphered=self.cipher.decode(self.message)
        else: #mode==HACK
            ciphered=self.cipher.hack(self.message)

        self.encryptionFinished.emit(ciphered, self.mode)
    
    
    