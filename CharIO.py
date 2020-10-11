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
    # sourceProgram=""
    line = ""

    # newvariables
    filename = ""
    data = []

    # Constructor
    def Chario(self, stream):
        # modification needed.
        self.filename = stream  # how is 'stream' type used in main function exatly? I assumed 'stream' is a file name
        self.terminalBased = True
        self.readFile(stream)
        self.reset()

    def reset(self):
        self.totalErrors = 0
        self.column = 0
        self.lineNumber = 0
        self.line = ""

    def print(self, s):
        if self.terminalBased:
            print(s)

    def makeSpaces(number):  # private
        s = ""
        for i in range(1, number):
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
