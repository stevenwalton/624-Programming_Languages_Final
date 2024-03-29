import sys, getopt
import generator as gen
import time
import signal # For timeouts
import re

'''
EIDOS interpreter program
Program has two available options: either interpretive mode or you can pass
a single file.
```
eidos
```
With no arguments we will be presented with creator notes and put into an
interpretive mode. This can handle single line Eidos functions and will return
a result. Memory is not saved between commands, so we cannot use a variable 
more than once.

```
eidos foo.e
```
by passing a file (must contain proper extension) we will run the single file
as an input and return the result. This will return you back to the command line
once it has finished.

Because this program is in alpha mode, we set a timeout to 60 seconds, and will
return the user to the command line if a program takes longer than 60 seconds 
to run.

Maintainers: Steven Walton (swalton2@cs.uoregon.edu)
             He He (贺赫)  (please add email)
             Priya Kudva   (please add email)
'''

TIMEOUT=60       # We limit programs to be 60 seconds long
global oldSym    # Global used to only display new values
global funcTable # Global used to store function tables

def timeoutHandler(signum, frame):
    raise Exception("WARNING: Program has timed out. Max program time set to {}".format(TIMEOUT))

def cat(f,dbg=False):
    '''
    Performs a unix like cat on a file and removes the trailing newline
    debug option pretty prints the contents of the file
    '''
    try:
        ffile = open(f,'r')
        text = ffile.read()[:-1] # remove trailing newline from EOF
        if dbg:
            print("Program: ", f)
            print("==========")
            print(text)
            print("==========")
        text = text.replace("\n","")
        return text
    except FileNotFoundError as e:
        raise Exception("File Not Found: Could not find file: {}".format(f))
    except Exception as e:
        raise Exception(e)


def runAFile(f,dbg=False):
    '''
    Runs a file
    '''
    if f[-2:] != ".e":
        print("Please provide an Eidos file, ending in '.e'")
        sys.exit(1)
    f_input = cat(f,dbg)
    i = f_input.split("\n")#[:-1]
    valTable={}
    for entry in i:
        entry = entry+";"
        valTable = eidos(valTable,entry)
    

def fileMain(argv):
    '''
    Main program for if a program is passed
    '''
    try:
        signal.signal(signal.SIGALRM, timeoutHandler)
        signal.alarm(TIMEOUT)
        runAFile(argv,dbg=False)
    except Exception as e:
        raise Exception(e)

def eidos(valTable,i=";"):
    '''
    runs a single line of eidos code
    We store previous values in oldSym (old symbol dictionary)
    and reassign each variable with each new line. This is slow
    but it works
    '''
    try:
        signal.signal(signal.SIGALRM, timeoutHandler)
        signal.alarm(TIMEOUT)
        ip = addTable(valTable) + i
        #ip = ip.replace("'",'"')
        (r,s,f) = gen.runReturn(ip,funcTable)
        #print("from int: {}".format(r))
        SymDiff(oldSym,s)
        signal.alarm(0) # Reset signal to infinite time
        if f is not {}:
            updateFunctionTable(f)
        #print("This is f {}".format(f))
        if re.match('^[a-zA-Z][a-zA-Z0-9]*;$',i):
            print("{{'{}': {}}}".format(i[:-1],oldSym[i[:-1]]))
            return oldSym
        if s == None:
            return oldSym
        else:
            return s
    except KeyError:        # Handles undefined variables
        print("That variable isn't defined")
        return oldSym
    except TypeError:
        print("I'm sorry Dave. I can't do that. Please type a valid input")
        return oldSym
    except Exception as e:  # General Exceptions
        raise Exception(e)

def SymDiff(oSym,nSym):
    '''
    Prints only newly updated variables
    '''
    global oldSym
    diff = {}
    # Need to make cleaner but whatever for now
    try:
        if oSym.keys() != nSym.keys():
            for key in nSym:
                #if type(nSym[key]) is str:
                #    nSym[key] = '"' + nSym[key][0:] + '"'
                if key not in oSym:
                    diff[key] = nSym[key]
        for key in nSym:
            if (key in oSym) and (oSym[key] != nSym[key]):
                diff[key] = nSym[key]
        oldSym = nSym
        if diff != {}: print(diff)
    except:
        print("Error in SymDiff. Continuing")
        pass

def updateFunctionTable(ftbl):
    '''
    update the function table
    '''
    global funcTable
    try:
        for key in ftbl:
            if key not in funcTable.keys():
                funcTable[key] = ftbl[key]
            elif ftbl[key] != funcTable[key]:
                funcTable[key] = ftbl[key]
            else:
                pass
    except:
        print("Error in updateFunctionTable. Continuing")
        pass


def addTable(valTable):
    '''
    adds past values and allows us to reuse variables
    '''
    s = ";"
    for key in valTable:
        s += "{}={};".format(key,valTable[key])
    return s

def display(valTable):
    '''
    displays all members of the value Table
    '''
    if valTable != {}:
        print("Variables stored: {}".format(valTable))
    else:
        print("No values stored")


def interpMain():
    '''
    Main program for if no arguments are passed. This is interpreter mode
    '''
    print("Version: 0.1")
    print("NOT:  We cannot handle functions that take multiple lines.")
    print("      We can keep a history of values, but not delete them.")
    print("      Functions that take longer than 60 seconds will error out.")
    print("      Use the 'display' function to display all stored variables.")
    print("      Please type 'exit' or 'quit' to exit")
    i = ""
    valTable = {}
    while(i != "exit" and i != "quit"):
        i = input("eidos > ")
        if (i == "exit") or (i == "quit"):
            sys.exit(0)
        elif i is "":
            pass
        elif i == "display":
            display(oldSym)
        else:
            valTable = eidos(valTable,i)


if __name__ == "__main__":
    argc = len(sys.argv)
    oldSym = {}
    funcTable = {}
    if argc == 1:
        interpMain()
    elif argc == 2:
        fileMain(sys.argv[1])
    else:
        print("Usage:")
        print("\tInterpreter Mode:")
        print("\t\t./eidos")
        print("\tRun a File:")
        print("\t\t./eidos eidosFile.e")
