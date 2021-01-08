##import os
##ciphers = []
##for name in os.listdir(os.path.dirname(os.path.abspath(__file__))):
##    m, ext = os.path.splitext(name)
##    if ext == '.py':
##        ciphers.append(__import__(m))
##__all__ = ciphers

#NOTE:
#   You must register all new ciphers here for them to work!!

from . import Ceasar
from . import OneTimePad
from . import Substitution
from . import Playfair
from . import Hide
from . import NullCipher
from . import Enigma
from . import Vinegre
from . import Transposition
from . import HillCipher



ciphers={}
item=None #To prevent RuntimeError on next line
for item in globals().values():
    try:
        ciphers[item.NAME]=item
    except AttributeError:
        pass
del item

from ..Utilities import DIRECTORY
import os
info={}
with open(os.path.join(DIRECTORY, "Files", "Cipher Info.txt"), encoding="utf-8") as file:
    currentCipher=None
    lines=[]
    for line in file:
        if line.startswith('@'):
            info[currentCipher]="".join(lines).strip()
            
            currentCipher=line[1:-2]
            lines=[]
        else:
            lines.append(line)


from .__EncrypterThread__ import ThreadedEncryption
