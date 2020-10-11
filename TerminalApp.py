#Tests the classes CharIO, Scanner, Parser

from CharIO import CharIO
from Scanner import Scanner
from Parser import Parser
from Token import Token

stream = None

class TerminalApp:
    def __init__(self):
        print("Enter the input file name: ")
        filename = input()
        try:
            global stream
            stream = open(filename, 'r')
        except:
            print("Error opening file")
            return
        self.testChario()
        self.testScanner()
        self.testParser()

    chario = CharIO(stream)
    scanner = Scanner()
    parser = Parser()

    def testChario(self):
        ch = self.chario.getChar()
        while ch != CharIO.EF:
            ch = self.chario.getChar()
        self.chario.reportErrors()

    def testScanner(self):
        token = self.scanner.nextToken()
        while token.code != Token.EOF:
            self.chario.print(self.token.toString())
            token = self.scanner.nextToken()
        self.chario.reportErrors()

    def testParser(self):
        try:
            self.parser.parse()
        except:
            self.chario.reportErrors()
        self.chario.reportErrors()

def main():
    TerminalApp()

main()