from .Utilities import removeNonAlpha
from . import Words

def isEnglish(message, threshold=70):
    return True if percentEnglish(message) >= threshold else False


def percentEnglish(message):
    words=message.split()
    numRealWords=sum(1 if Words.isWord(word) else 0 for word in words)
    return round(100*(numRealWords/len(words)))


def chooseBest(messages):
    percents=[percentEnglish(message) for message in messages]
    maxId=percents.index(max(percents))
    return messages[maxId], maxId
    
