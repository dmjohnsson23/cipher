import os
from .Utilities import DIRECTORY
from string import ascii_uppercase as alphabet
import random

_WORDS_DICT={} #the 'in' operator works faster on dicts
_WORDS_LIST=[] #but random.choice only works on lists
_SORTED_ALPHABETICALLY={letter:[] for letter in alphabet}

with open(os.path.join(DIRECTORY, "Files", "Dictionary.txt")) as file:
    for word in file:
        word=word.strip()
        _WORDS_DICT[word]=None
        _WORDS_LIST.append(word)
        _SORTED_ALPHABETICALLY[word[0]].append(word)

            


def getRandomWord(firstLetter=None):
    if firstLetter:
        if len(firstLetter)==1 and firstLetter.isalpha():
            return random.choice(_SORTED_ALPHABETICALLY[firstLetter.upper()])
        else:
            raise ValueError("%s is not a valid first letter" % repr(firstLetter))
    else:
        return random.choice(_WORDS_LIST)

def isWord(word):
    return word.strip().upper() in _WORDS_DICT