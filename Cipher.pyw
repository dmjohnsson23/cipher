#! /usr/bin/python3
import os
import datetime
try:
    import Cipher
    Cipher.main()
except Exception as ex:
    filename=os.path.join("log.txt")
    log=open(filename, 'a')
    log.write("\t-- Failed run @ %s--\n\n"%datetime.datetime.now())
    import traceback
    traceback.print_exc(file=log) # Output Error message to file
    log.write("\n\t-- End Traceback--\n\n")
    log.write('-'*45)
    log.write("\n\n")
    log.close()
    print("An error has occurred. Please see %s for details.\n"%os.path.abspath(filename))
    traceback.print_exc()
