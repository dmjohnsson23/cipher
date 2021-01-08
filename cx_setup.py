#from cx_Freeze import setup, Executable
import os

exe = Executable(
    script=os.path.join("Cipher.pyw"),
    base="Win32GUI",
    icon=os.path.join("Files", "Icon.ico")
    )
includeFiles= [os.path.join("Files", file) for file in
               ["Dictionary.txt", "cipher.options", "Icon.ico", "Logo.png",
                "Missing_Dependancies.html", "Cipher Info.txt",
                "Licence.txt", "About.txt", "Attributions.txt"
                ]
               ]+[
                  os.path.join("Files", "ButtonIcons", file) for file in
                  ["Copy.png", "Cut.png", "Exit.png", "Info.png",
                   "Paste.png", "Redo.png", "Undo.png", "Red X.png",
                   "Green Check.png", "Open.png", "Save.png", 
                   "Save As.png", "Plus.png", "Minus.png", 
                   "Contact.png", "Bug.png", "About.png"]
                   ]

excludes = ["Tkinter"]

setup(
    name = "Cipher",
    version = "1.1",
    author = "Dominick Johnson",
    author_email = "dmjohn235@gmail.com",
    description = "Basic Text Encryption Software",
    executables = [exe],
    options = {'build_exe': {"excludes":excludes,
                             "include_files":includeFiles}}
    )
