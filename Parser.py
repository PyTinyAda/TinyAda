from CharIO import CharIO
from Scanner import Scanner
from Token import Token
# from SymbolEntry import SymbolEntry
# from SymbolTable import SymbolTable


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

    # constructor for the parser
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

    def acceptRole(self, s, expected, errorMessage):
        if self.mode == Parser.Role:
            if s is None or (s.role != SymbolEntry.NONE and s.role != expected):
                self.chario.putError(errorMessage)
            elif s is None or (s.role != SymbolEntry.NONE and not (s.role in expected)):
                self.chario.putError(errorMessage)

    def setRole(self, s, role):
        if self.mode == Parser.ROLE and s is not None:
            s.setRole(role)

    def appendEntry(self, head, tail):
        if self.mode == Parser.SCOPE or self.mode == Parser.ROLE:
            if head is not None:
                head.append(tail)

    def accept(self, expected, errorMessage):
        if self.token.code != expected:
            self.fatalError(errorMessage)
        self.token = self.scanner.nextToken()

    def fatalError(self, errorMessage):
        self.chario.putError()
        raise RuntimeError("Fatal Error")

    # def initTable(self):
    #     if self.mode == Parser.ROLE or self.mode == Parser.SCOPE:
    #         self.table = SymbolTable(self.chario)
    #         self.enterScope()
    #         entry = self.table.enterSymbol("BOOLEAN")
    #         self.setRole(entry, SymbolEntry.TYPE)
    #         entry = self.table.enterSymbol("CHAR")
    #         self.setRole(entry, SymbolEntry.TYPE)
    #         entry = self.table.enterSymbol("INTEGER")
    #         self.setRole(entry, SymbolEntry.TYPE)
    #         entry = self.table.enterSymbol("TRUE")
    #         self.setRole(entry, SymbolEntry.CONST)
    #         entry = self.table.enterSymbol("FALSE")
    #         self.setRole(entry, SymbolEntry.CONST)

    def enterScope(self):
        if self.mode == Parser.ROLE or self.mode == Parser.SCOPE:
            self.table.enterscope()

    def exitScope(self):
        if self.mode == Parser.ROLE or self.mode == Parser.SCOPE:
            self.table.exitScope(self.mode)

    def enterId(self):
        entry = None
        if self.token.code == Token.ID:
            if self.token.mode == Parser.SCOPE or self.mode == Parser.mode:
                entry = self.table.enterSymbol(self.token.string)
        else:
            self.fatalError("identifier expected")
        self.token = self.scanner.nextToken()
        return entry

    def findId(self):
        entry = None
        if self.token.code == Token.ID:
            if self.mode == Parser.SCOPE or self.mode == Parser.ROLE:
                entry = self.table.findSymbol(self.token.string)
        else:
            self.fatalError("identifier expected")
        self.token = self.scanner.nextToken()
        return entry

    def parse(self):
        self.subprogramBody()
        self.accept(Token.EOF, "extra symbols after logical end of program")
        self.exitScope()

    # def subprogramBody(self):
    #     self.subprogramSpecification()
    #     self.accept(Token.IS, "'is' expected")
    #     self.declarativePart()
    #     self.accept(Token.BEGIN, "'begin' expected")
    #     self.sequenceOfStatements()
    #     self.exitScope()
    #     if self.token.code == Token.ID:
    #         entry = self.findID()
    #         self.acceptRole(entry, SymbolEntry.PROC, "must be a procedure name")
    #     self.accept(Token.SEMI, "';' expected")

    # def subprogramSpecification(self):

    def formalPart(self):
        self.accept(Token.L_PAR, "'(' expected")
        self.parameterSpecification()
        while self.token.code == Token.SEMI:
            self.token = self.scanner.nextToken()
            self.parameterSpecification()
        self.accept(Token.R_PAR, "')' expected")

    # def parameterSpecification(self):
    #     list = self.identifierList()
    #     self.setRole(list, SymbolEntry.PARAM)
    #     self.accept(Token.COLON, "':' expected")
    #     self.mode()
    #     entry = self.findID()
    #     self.acceptRole(entry, SymbolEntry.TYPE, "must be a type name")

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

    def basicDeclaration(self):
        if self.token.code == Token.ID:
            self.numberOrObjectDeclaration()
        elif self.token.code == Token.TYPE:
            self.typeDeclaration()
        elif self.token.code == Token.PROC:
            self.subprogramBody()
        else:
            self.fatalError("error in declaration part")

    # def numberOrObjectDeclaration(self):
    #     list = self.identifierList()
    #     self.accept(Token.COLON, "':' expected")
    #     if self.token.code == Token.CONST:
    #         self.setRole(list, SymbolEntry.CONST)
    #         self.token = self.scanner.nextToken()
    #         self.accept(Token.GETS, "':=' expected")
    #         self.expression()
    #     else:
    #         self.setRole(list, SymbolEntry.VAR)
    #         self.typeDefinition()
    #     self.accept(Token.SEMI, "';' expected")

    # # def typeDeclaration

    # # def typeDefinition

    # def enumerationTypeDefinition(self):
    #     self.accept(Token.L_PAR,"'(' expected")
    
    def range(self):
        self.accept(Token.RANGE, "'range' expected")
        self.simpleExpression()
        self.accept(Token.THRU, "'..' expected")
        self.simpleExpression()