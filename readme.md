# cipher

Classical cryptography application

This is one of my first ever programming projects, made years ago (2013 according to file metadata). It has several bugs I plan to fix, but beyond that I do not have long-term plans of maintaining this software, though I may update it occasionally. I decided to publish the source code for a couple of reasons. Firstly, I wanted something to show off to people to demonstrate my programming skills. This is of course an old project, and I have grown significantly as a coder since writing it, but I am actually still proud of this project despite its somewhat messy (and not entirely finished) code. And secondly, I thought some others might be able to use it, perhaps as a simple toy, or as a tool to discover how some old ciphers worked.

The [user manual](https://github.com/dmjohnsson23/cipher/blob/master/Cipher%20User%20Manual.pdf) is a good place to get started using the software. It also contains some information about the various ciphers included, such as historical information and details about how the cipher works.

I currently only have the source available. It relies on Python 3.5+, PySide2, and numpy. I may try to create an appimage package for it to run on Linux. The application is already set up to generate Windows binaries using CX Freeze, though I don't currently have a Windows machine to build that binary on. I have no intentions of ever supporting MacOS, though I expect it should work fine there too so long as you install the dependencies and run it from source.
