from CharIO import CharIO
from Scanner import Scanner
from Token import Token


class Parser:
    NONE = 0
    SCOPE = 1
    ROLE = 2

    chario = CharIO()
    scanner = Scanner()
    token = Token()
    # table = SymbolTable()

    addingOperator = {}
    multiplyingOperator = {}
    relationalOperator = {}
    basicDeclarationHandles = {}
    statementHandles = {}
    leftNames = {}
    rightNames = {}

    #constructor for the parser
    def __init__(self, c, s, mode):
        self.chario = c
        self.scanner = s
        self.mode = mode
        self.initHandles()
        self.initTables()
        token = self.scanner.nextToken()

    def reset(self):
        self.scanner.reset()
        self.initTable()
        token = self.scanner.nextToken()

    def initHandles(self):
        self.addingOperator.add(Token.PLUS)
        self.addingOperator.add(Token.MINUS)
        self.multiplyingOperator.add(Token.MUL)
        self.multiplyingOperator.add(Token.DIV)
        self.multiplyingOperator.add(Token.MOD)
        self.relationalOperator.add(Token.EQ)
        self.relationalOperator.add(Token.NE)
        self.relationalOperator.add(Token.LE)
        self.relationalOperator.add(Token.GE)
        self.relationalOperator.add(Token.LT)
        self.relationalOperator.add(Token.GT)
        self.basicDeclarationHandles.add(Token.TYPE)
        self.basicDeclarationHandles.add(Token.ID)
        self.basicDeclarationHandles.add(Token.PROC)
        self.statementHandles.add(Token.EXIT)
        self.statementHandles.add(Token.ID)
        self.statementHandles.add(Token.IF)
        self.statementHandles.add(Token.LOOP)
        self.statementHandles.add(Token.NULL)
        self.statementHandles.add(Token.WHILE)

    def accept(self, expected, errorMessage):
        if(self.token.code != expected):
            self.fatalError(errorMessage)
        token = self.scanner.nextToken()

    def fatalError(self, errorMessage):
        self.chario.putError()
