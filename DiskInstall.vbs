Dim WshShell : Set WshShell = WScript.CreateObject("WScript.Shell")  

MsgBox("Welcome! This program will install Cipher on your computer. First though, we have some dependencies to install. If you get any errors, just re-try.")

ok = MsgBox("First up, we need to install Python. This one's mandatory. Only skip if you've already installed it.", vbOKCancel)
if ok = vbOK then
	WshShell.Run "PythonSetup.exe", 1, True  'Runs the program and waits for it to exit. Thanks to http://www.visualbasicscript.com/Launching-vbscript-from-a-vbscript-and-wait-until-it39s-completed-running-m92825.aspx for this info.
else
	MsgBox("The program can't run without Python. If you haven't installed it previously, you'll get an error.")
end if

ok = MsgBox("Alright. Next up is Numpy. This one is optional, but recommended.", vbOKCancel)
if ok = vbOK then
	WshShell.Run "NumpySetup.exe", 1, True 
else
	MsgBox("Numpy Installation skipped. Some of the more mathematical ciphers will be unavailable.")
end if

ok = MsgBox("Okay, Now for PySide. This is the last dependency before we can install Cipher! Oh, and it's mandatory.", vbOKCancel)
if ok = vbOK then
	WshShell.Run "PysideSetup.exe", 1, True 
else
	MsgBox("Okay, but you'd have better already installed PySide. It's needed for the user interface!")
end if

ok = MsgBox("Now for the moment you've all been waiting for! If you see any errors pop up, that probably means you didn't install all the mandatory dependencies. If you're sure you have, you may need to restart your computer.", vbOKCancel)
if ok = vbOK then
	pyExit = WshShell.Run("python setup.py install" , 1, True)
	if pyExit <> 0 then
		MsgBox "Error installing Cipher. Did you install all the dependencies?", vbCritical
		WScript.Quit(pyExit)
	end if
	
	'Make the desktop shortcut (From http://stackoverflow.com/questions/346107/creating-a-shortcut-for-a-exe-from-a-batch-file)
	strDesktop = WshShell.SpecialFolders("Desktop" )
	set oShellLink = WshShell.CreateShortcut(strDesktop & "\Cipher.lnk" )
	oShellLink.TargetPath = "c:\Unprotected Programs\dmjohnson\Cipher\Cipher.pyw"
	oShellLink.WindowStyle = 1
	oShellLink.IconLocation = "c:\Unprotected Programs\dmjohnson\Cipher\Files\Icon.ico"
	oShellLink.Description = "Cipher, by Dominick Johnson"
	oShellLink.WorkingDirectory = "c:\Unprotected Programs\dmjohnson\Cipher"
	oShellLink.Save
else
	MsgBox "Really? Why even bother. Whatever..."
end if



MsgBox "All Done!"