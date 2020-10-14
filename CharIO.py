class CharIO:
    EL = '\n'
    EF = chr(26)
    TAB = '\t'

    # private
    totalErrors = 0
    terminalBased = False
    column = 0
    lineNumber = 0
    MaxlineNumber = 0
    sourceProgram = ""
    line = ""

    # newvariables
    filename = ""
    data = []

    # Constructor

    def __init__(self, stream=None):
        # modification needed.
        self.filename = stream  # how is 'stream' type used in main function exatly? I assumed 'stream' is a file name
        self.terminalBased = True
        self.readFile(self.filename)
        self.reset()

    def reset(self):
        self.totalErrors = 0
        self.column = 0
        self.lineNumber = 0
        self.line = ""

    def print(self, s):
        print(s)

    def makeSpaces(self, number):  # private
        s = ""
        for i in range(1, number+1):
            s += " "
        return s

    def putError(self, message):
        self.totalErrors += 1
        spaces = self.makeSpaces(self.column)
        if self.terminalBased:
            print(spaces + "ERROR > " + message)

    def reportErrors(self):
        print("\nCompilation complete.")
        if self.totalErrors == 0:
            print("No errors reported.")
        elif self.totalErrors == 1:
            print("1 error reported.")
        else:
            print(self.totalErrors + " errors reported.")

    def getChar(self):
        if self.column >= len(self.line):
            self.nextline()
        ch = self.line[self.column]
        self.column += 1
        return ch

    def nextline(self):
        column = 0
        line = self.getLine()
        if line[0] != self.EF:
            self.lineNumber += 1
            print(str(self.lineNumber) + " > " + line)

    def readFile(self, stream):
        reader = open(stream, 'r')
        try:
            with open(stream, 'r') as file:
                for text in file:
                    self.sourceProgram += text

        except IOError as e:
            print("Error in file input" + str(e))
    '''
    def readFile(self, stream):
        reader = open(stream, 'r')
        try:
            data = reader.readline()
            while data is not None:
                self.sourceProgram += data + "\n"
                data = reader.readline()
        except IOError as e:
            print("Error in file input" + str(e))
    '''
    def getLine(self):
        ln = ""
        if self.sourceProgram == "":
            ln = "" + self.EF
        else:
            first = self.sourceProgram.index(self.EL)
            last = len(self.sourceProgram)
            if first == -1:
                ln = self.sourceProgram + self.EL
                self.sourceProgram = ""
            else:
                ln = self.sourceProgram[0:first + 1]
                self.sourceProgram = self.sourceProgram[first + 1:last]
        return ln

    '''
    def getChar(self):
        if self.column >= len(self.line):
            if self.lineNumber >= self.MaxlineNumber:
                print("All characters in this file are done!\n")
            else:
                self.lineNumber += 1
                self.line = self.data[self.lineNumber]
        ch = self.line[self.column]
        self.column += 1
        return ch

    def readFile(self, stream):  # private
        reader = open(stream, 'r')
        self.data = reader.readlines()
        self.MaxlineNumber = len(self.data)
    '''

    '''def private nextLine(): #private
       column = 0
       line = getLine()
       if (line.charAt(0) != EF){
          lineNumber++
          if (terminalBased)
             print(lineNumber + " > " + line)
          else{
             output.append(lineNumber + " > ")
             output.append(line)
          }
       }
    }
 
    #def private getLine(){ #private
       ln
       int first, last
       if (sourceProgram.equals(""))
          ln = "" + EF
       else{
          first = sourceProgram.indexOf(EL)
          last = sourceProgram.length()
          if (first == -1){
             ln = sourceProgram + EL
             sourceProgram = ""
          }
          else{
             ln = sourceProgram.substring(0, first + 1)
             sourceProgram = sourceProgram.substring(first + 1, last)
          }
       }
       return ln
    }'''

    def openFile(self):
        return
        # do we need this function even when not using GUI?

    def saveFile(self, input):
        return
        # do we need this function even when not using GUI?

    def writeFile(self, stream, input):  # private
        return
    # do we need this function even when not using GUI?
