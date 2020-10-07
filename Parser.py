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
        self.token = self.scanner.nextToken()

    def reset(self):
        self.scanner.reset()
        self.initTable()
        self.token = self.scanner.nextToken()

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

    #def acceptTole

    #def setRole

    #def appendEntry

    def accept(self, expected, errorMessage):
        if self.token.code != expected:
            self.fatalError(errorMessage)
        self.token = self.scanner.nextToken()

    def fatalError(self, errorMessage):
        self.chario.putError()
        raise RuntimeError("Fatal Error")

    #def initTable

    def enterScope(self):
        if self.mode == Parser.ROLE or self.mode == Parser.SCOPE:
            self.table.enterscope()

    def exitScope(self):
        if self.mode == Parser.ROLE or self.mode == Parser.SCOPE:
            self.table.exitScope(self.mode)

    #def enterId

    #def findId

    def Parse(self):
        self.subprogramBody()
        self.accept(Token.EOF, "extra symbols after logical end of program")
        self.exitScope()

    #def subprogramBody

    #def subprogramSpecification

    def formalPart(self):
        self.accept(Token.L_PAR, "'(' expected")
        self.parameterSpecification()
        while self.token.code == Token.SEMI:
            self.token = self.scanner.nextToken()
            self.parameterSpecification()
        self.accept(Token.R_PAR, "')' expected")

    #def parameterSpecification

    def mode(self):
        if self.token.code == Token.IN:
            self.token = self.scanner.nextToken()
            if self.token.code == Token.OUT:
                self.token = self.scanner.nextTOken()
        elif self.token.code == Token.OUT:
            self.token = self.scanner.nextToken()

    def declarativePart(self):
        while self.token.code in self.basicDeclarationHandles:
            self.basicDeclaration()

    #def basicDeclaration

    #def numberOrObjectDeclaration

    #def typeDeclaration

    #def typeDefinition