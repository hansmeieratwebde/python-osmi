# -*- coding: utf-8 -*-
# Erstellen Sie ein Programm, welches einen Verzeichnisbaum durchwandert (inkl. der Unterverzeichnisse -- also rekursiv).
# Ermitteln Sie für jede Datei die MD5-Summe.  Das Programm soll auf der Standardausgabe für jede Datei den Dateinamen, den Dateipfad (relativ zum Startverzeichnis) sowie
# die MD5-Summe  ausgeben. So lassen sich Änderungen mit den UNIX-Bordmitteln diff, cat, cut, sort usw. erkennen. Das Startverzeichnis soll als Parameter übergeben werden.
#
# Verwenden Sie nicht os.walk oder os.path.walk. Fangen Sie Exceptions,
# die zum Beispiel auftreten, wenn die Leserechte fehlen.
#
# Nützliche Module bzw. Funktionen sind hashlib, os.listdir.


# ESA 1 - Sven Hinse SS 2015

import os, hashlib

#enter your startpath here
startPath = "C:/Users/Sven/Qsync"


#some colors for error highlighting
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#shows the md5 checksum of a file,
# @params filePath = path to File
def md5Checksum(filePath):  # adapted from: http://joelverhagen.com/blog/2011/02/md5-hash-of-file-in-python/
    try:
        with open(filePath, 'rb') as fh:
            m = hashlib.md5()
            while True:
                data = fh.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()
    except IOError, e:
        return bcolors.FAIL + "Cannot calculate MD5: "+str(e) + bcolors.ENDC

#shows the directory contents, additionalPath is used for path display and recursive function calling
def showDirectoryContents(startPath, additionalPath=""):
    startDir = startPath + additionalPath  # for file system we must use the complete path

    #get directory contents
    try:
        listing = os.listdir(startDir)
    except OSError, e:
       print bcolors.FAIL + "Cannot list directory contents of "+additionalPath+": "+str(e)+ bcolors.ENDC
       return None
    #check each entry
    for item in listing:
        # if the current entry is a file, we show the MD5 Checksum
        if os.path.isfile(startDir + "/" + item):
            fileChecksum = md5Checksum(startDir + "/" + item)
            print  additionalPath + "/" + item + "  MD5: " + fileChecksum
        # if entry is a directory, we call ourselves recursively with the new path
        if os.path.isdir(startDir + "/" + item):
            print additionalPath + "/" + item
            showDirectoryContents(startPath, additionalPath + "/" + item)


showDirectoryContents(startPath)
