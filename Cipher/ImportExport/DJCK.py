FILTER="Cipher Key File (*.djck)"
TYPE="KEY"
from ..LetterMath import charToNum
from ..Utilities import removeNonAlpha
from .Misc import KeyError
import pickle

def save(data, path, cipherName):
    file = open(path, "wb")
    file.write(_getHeader(cipherName))
    file.write(pickle.dumps(data))
    file.close


def load(path, cipherName):
    file=open(path, "rb")
    header=_getHeader(cipherName)
    data=file.read()
    if not data.startswith(header):
        raise KeyError("The provided file does not a valid key for "+cipherName)
    return pickle.loads(data[len(header):])


def _getHeader(cipherName):
    return bytes(charToNum(char) for char in 
                 ("This is a valid cipher key file for "+cipherName) 
                 if char.isalpha())
    
    
