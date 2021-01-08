####################################################################
#              Dominick Johnson's Encription program               #
#              Using elements from previous programs,              #
#          such as Ceasar Cipher and One-Time Pad Cipher           #
# Plus addtional elements including new GUI and additional ciphers #
####################################################################
#Options

from .Utilities import DIRECTORY
import os.path
_optionFileName=os.path.join(DIRECTORY, "Files", "cipher.options")

MODE_DEBUG="DEBUG"
MODE_REGULAR="Regular"

TEXT_DISPLAY_MODE_OVERWRITE="Overwrite"
TEXT_DISPLAY_MODE_EXTERNAL="External"

DEFAULT="Default"


_header="Cipher Options File"
_compatNum="2"

def main():
    try:
        file=open(_optionFileName,)
    except IOError:
        #File does not exist
        setToDefault()
    else:
        fileStr=file.read().split("\n")
        if fileStr[0]==_header and fileStr[1]==_compatNum:
            #Valid Options File
            dit=eval(fileStr[2])  #Dictionary containing options data
            global STYLE
            global TEXTDISP
            global MODE
            global FIRST_TIME
            STYLE=dit["STYLE"]
            TEXTDISP=dit["TEXTDISP"]
            MODE=dit["MODE"]
            FIRST_TIME=dit["FIRST_TIME"]
        else:
            setToDefault()

def setToDefault():
    global STYLE
    global TEXTDISP
    global MODE
    global FIRST_TIME
    
    STYLE=DEFAULT
    TEXTDISP=TEXT_DISPLAY_MODE_EXTERNAL
    MODE=MODE_REGULAR
    FIRST_TIME=True

    file=open(_optionFileName, "w")
    file.write(_header+"\n")
    file.write(_compatNum+"\n")
    file.write(str({"STYLE":STYLE,
                "TEXTDISP":TEXTDISP,
                "MODE":MODE,
                "FIRST_TIME":FIRST_TIME}))
    file.close()

main()


def setOptions(style=None, textDisp=None, mode=None, firstTime=None):
    global STYLE
    global TEXTDISP
    global MODE
    global FIRST_TIME
    
    if not style is None:
        STYLE=style
    if not textDisp is None:
        TEXTDISP=textDisp
    if not mode is None:
        MODE=mode
    if not firstTime is None:
        FIRST_TIME=firstTime

    file=open(_optionFileName, "w")
    file.write(_header+"\n")
    file.write(_compatNum+"\n")
    file.write(str({"STYLE":STYLE,
                "TEXTDISP":TEXTDISP,
                "MODE":MODE,
                "FIRST_TIME":FIRST_TIME}))
    file.close()














        
        
        
