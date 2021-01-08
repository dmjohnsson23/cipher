from ..Utilities import chunker
from itertools import zip_longest

def encode(message, key):
    return "".join("".join(letters) for letters in zip_longest(chunker(message, key)))


def decode(message, key):
    