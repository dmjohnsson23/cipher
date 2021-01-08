####################################################################
#              Dominick Johnson's Encryption program               #
#              Using elements from previous programs,              #
#          such as Ceasar Cipher and One-Time Pad Cipher           #
# Plus additional elements including new GUI and additional ciphers #
####################################################################
#Variables and utility functions

import os
import sys
import re
import itertools

DIRECTORY=os.path.dirname(sys.argv[0]) #Main program Directory
USER_HOME=os.path.expanduser("~")


VERSION_NUMBER="1.1"

MAIN_TITLE="Cipher by Dominick Johnson"

with open(os.path.join(DIRECTORY, "Files", "About.html"), encoding="utf-8") as file:
    MAIN_ABOUT_TEXT=file.read().format(title=MAIN_TITLE, version=VERSION_NUMBER)

HELP_TEXT="""

"""

LETTER_GOODNESS={"a":0.0817,
                 "b":0.0149,
                 "c":0.0278,
                 "d":0.0425,
                 "e":0.127,
                 "f":0.0223,
                 "g":0.0202,
                 "h":0.0609,
                 "i":0.0697,
                 "j":0.0015,
                 "k":0.0077,
                 "l":0.0402,
                 "m":0.0241,
                 "n":0.0675,
                 "o":0.0751,
                 "p":0.0193,
                 "q":0.0009,
                 "r":0.0599,
                 "s":0.0633,
                 "t":0.0906,
                 "u":0.0276,
                 "v":0.0098,
                 "w":0.0236,
                 "x":0.0015,
                 "y":0.0197,
                 "z":0.0007}

ENCODE="Encode"
DECODE="Decode"
HACK="Hack"



      
with open(os.path.join(DIRECTORY, "Files", "Licence.txt")) as file:
    LICENCE_TEXT=file.read()
    
with open(os.path.join(DIRECTORY, "Files", "Attributions.txt")) as file:
    ATTRIBUTIONS_TEXT=file.read()
    
    
def getkey(dictionary, value):
      for key, val in dictionary.items():
            if val == value:
                   return key

def initialize(cls):
      "A Class Decorator that initializes the class right off the bat"
      return cls()


_strip_pattern=re.compile(r"[\W\d_]+")
def removeNonAlpha(string):
    "Returns the string with all non-alphabetic characters removed"
    return _strip_pattern.sub('', string)


def countAlpha(string):
    return sum(1 if char.isalpha() else 0 for char in string)


_duplicates_pattern=re.compile(r"([a-zA-Z])(.*)\1")
def removeDuplicates(string):
    """\
For any alphabetic character in the string, remove all but the 
first occurrence of that character\
"""
    while _duplicates_pattern.search(string):
        string = _duplicates_pattern.sub(r"\1\2", string)
    return string


##def everyNItems(n, iterable):
##    out=[]
##    for item in iterable:
##        out.append(item)
##        if len(out)==n:
##            yield out
##            out=[]
##    yield out
##            
##            
##def everyNLetters(n, string):
##    out=[]
##    for letter in string:
##        if letter.isalpha():
##            out.append(item)
##        if len(out)==n:
##            yield "".join(out)
##            out=[]
##    yield "".join(out)


#Adpted from http://stackoverflow.com/questions/434287/what-is-the-most-pythonic-way-to-iterate-over-a-list-in-chunks
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))



