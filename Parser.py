from CharIO import CharIO
from Scanner import Scanner
from Token import Token

from SymbolEntry import SymbolEntry
from SymbolTable import SymbolTable


class Parser:
    NONE = 0
    SCOPE = 1
    ROLE = 2

    addingOperator = set()
    multiplyingOperator = set()
    relationalOperator = set()
    basicDeclarationHandles = set()
    statementHandles = set()
    leftNames = set()
    rightNames = set()

    # constructor for the parser
    def __init__(self, c, s, mode):
        self.chario = c
        self.scanner = s
        self.mode = mode
        self.initHandles()
        self.initTable()
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
        self.leftNames.add(SymbolEntry.PARAM)
        self.leftNames.add(SymbolEntry.VAR)
        self.rightNames.add(SymbolEntry.CONST)

    def acceptRole(self, s, expected, errorMessage):
        if self.mode == Parser.ROLE:
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
        self.chario.putError(errorMessage)
        raise RuntimeError("Fatal Error")

    def initTable(self):
        if self.mode == Parser.ROLE or self.mode == Parser.SCOPE:
            self.table = SymbolTable(self.chario)
            self.enterScope()
            entry = self.table.enterSymbol("BOOLEAN")
            self.setRole(entry, SymbolEntry.TYPE)
            entry = self.table.enterSymbol("CHAR")
            self.setRole(entry, SymbolEntry.TYPE)
            entry = self.table.enterSymbol("INTEGER")
            self.setRole(entry, SymbolEntry.TYPE)
            entry = self.table.enterSymbol("TRUE")
            self.setRole(entry, SymbolEntry.CONST)
            entry = self.table.enterSymbol("FALSE")
            self.setRole(entry, SymbolEntry.CONST)

    def enterScope(self):
        if self.mode == Parser.ROLE or self.mode == Parser.SCOPE:
            self.table.enterScope()

    def exitScope(self):
        if self.mode == Parser.ROLE or self.mode == Parser.SCOPE:
            self.table.exitScope(self.mode)

    def enterId(self):
        entry = None
        if self.token.code == Token.ID:
            if self.mode == Parser.SCOPE or self.mode == Parser.ROLE:
                entry = self.table.enterSymbol(self.token.string)
        else:
            self.fatalError("identifier expected1")
        self.token = self.scanner.nextToken()
        return entry

    def findId(self):
        entry = None
        if self.token.code == Token.ID:
            if self.mode == Parser.SCOPE or self.mode == Parser.ROLE:
                entry = self.table.findSymbol(self.token.string)
        else:
            self.fatalError("identifier expected2")
        self.token = self.scanner.nextToken()
        return entry

    def parse(self):
        self.subprogramBody()
        self.accept(Token.EOF, "extra symbols after logical end of program")
        self.exitScope()

    def subprogramBody(self):
        self.subprogramSpecification()
        self.accept(Token.IS, "'is' expected")
        self.declarativePart()
        self.accept(Token.BEGIN, "'begin' expected")
        self.sequenceOfStatements()
        self.accept(Token.END, "'end' expected")
        self.exitScope()
        if self.token.code == Token.ID:
            entry = self.findId()
            self.acceptRole(entry, SymbolEntry.PROC, "must be a procedure name")
        self.accept(Token.SEMI, "semicolon expected")

    def subprogramSpecification(self):
        self.accept(Token.PROC, "'procedure' expected")
        entry = self.enterId()
        self.setRole(entry, SymbolEntry.PROC)
        self.enterScope()
        if self.token.code == Token.L_PAR:
            self.formalPart()

    def formalPart(self):
        self.accept(Token.L_PAR, "'(' expected")
        self.parameterSpecification()
        while self.token.code == Token.SEMI:
            self.token = self.scanner.nextToken()
            self.parameterSpecification()
        self.accept(Token.R_PAR, "')' expected")

    def parameterSpecification(self):
        list = self.identifierList()
        self.setRole(list, SymbolEntry.PARAM)
        self.accept(Token.COLON, "':' expected")
        self.mode()
        entry = self.findId()
        self.acceptRole(entry, SymbolEntry.TYPE, "must be a type name")

    def mode(self):
        if self.token.code == Token.IN:
            self.token = self.scanner.nextToken()
            if self.token.code == Token.OUT:
                self.token = self.scanner.nextToken()
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

    def numberOrObjectDeclaration(self):
        list = self.identifierList()
        self.accept(Token.COLON, "':' expected")
        if self.token.code == Token.CONST:
            self.setRole(list, SymbolEntry.CONST)
            self.token = self.scanner.nextToken()
            self.accept(Token.GETS, "':=' expected")
            self.expression()
        else:
            self.setRole(list, SymbolEntry.VAR)
            self.typeDefinition()
        self.accept(Token.SEMI, "semicolon expected")

    def typeDeclaration(self):
        self.accept(Token.TYPE, "'type' expected")
        entry = self.enterId()
        self.setRole(entry, SymbolEntry.TYPE)
        self.accept(Token.IS, "'is' expected")
        self.typeDefinition()
        self.accept(Token.SEMI, "semicolon expected")

    def typeDefinition(self):
        if self.token.code == Token.L_PAR:
            self.enumerationTypeDefinition()
        elif self.token.code == Token.ARRAY:
            self.arrayTypeDefinition()
        elif self.token.code == Token.RANGE:
            self.range()
        elif self.token.code == Token.ID:
            entry = self.findId()
            self.acceptRole(entry, SymbolEntry.TYPE, "must be a type name")
        else:
            self.fatalError("error in type definition")

    def enumerationTypeDefinition(self):
        self.accept(Token.L_PAR, "left parenthesis expected")
        list = self.identifierList()
        self.setRole(list, SymbolEntry.CONST)
        self.accept(Token.R_PAR, "right parenthesis expected")

    def arrayTypeDefinition(self):
        self.accept(Token.ARRAY, "'array' expected")
        self.accept(Token.L_PAR, "left parenthesis expected")
        self.index()
        while self.token.code == Token.COMMA:
            self.token = self.scanner.nextToken()
            self.index()
        self.accept(Token.R_PAR, "right parenthesis expected")
        self.accept(Token.OF, "'of' expected")
        entry = self.findId()
        self.acceptRole(entry, SymbolEntry.TYPE, "must be a type name")

    def index(self):
        if self.token.code == Token.RANGE:
            self.range()
        elif self.token.code == self.token.ID:
            entry = self.findId()
            self.acceptRole(entry, SymbolEntry.TYPE, "must be a type name")
        else:
            self.fatalError("error in index")

    def range(self):
        self.accept(Token.RANGE, "'range' expected")
        self.simpleExpression()
        self.accept(Token.THRU, "dot dot expected")
        self.simpleExpression()

    def identifierList(self):
        list = self.enterId()
        while self.token.code == Token.COMMA:
            self.token = self.scanner.nextToken()
            self.appendEntry(list, self.enterId())
        return list

    def sequenceOfStatements(self):
        self.statement()
        while self.token.code in self.statementHandles:
            self.statement()

    def statement(self):
        if self.token.code == Token.ID:
            self.assignmentOrCallStatement()
        elif self.token.code == Token.EXIT:
            self.exitStatement()
        elif self.token.code == Token.IF:
            self.ifStatement()
        elif self.token.code == Token.NULL:
            self.nullStatement()
        elif (self.token.code == Token.WHILE) or (self.token.code == Token.LOOP):
            self.loopStatement()
        elif self.token.code == Token.PRINT:
            self.printStatement()
        else:
            self.fatalError("error in statement")

    def printStatement(self):
        self.accept(Token.PRINT, "'print' expected")
        self.scanner.nextToken()
        self.accept(Token.L_PAR, "'(' expected")
        self.chario.print(self.scanner.nextToken())
        self.accept(Token.R_PAR, "')' expected")

    def nullStatement(self):
        self.accept(Token.NULL, "'null' expected")
        self.accept(Token.SEMI, "semicolon expected")

    def loopStatement(self):
        if self.token.code == Token.WHILE:
            self.iterationScheme()
        self.accept(Token.LOOP, "'loop' expected")
        self.sequenceOfStatements()
        self.accept(Token.END, "'end' expected")
        self.accept(Token.LOOP, "'loop' expected")
        self.accept(Token.SEMI, "semicolon expected")

    def iterationScheme(self):
        self.accept(Token.WHILE, "'while' expected")
        self.condition()

    def ifStatement(self):
        self.accept(Token.IF, "'if' expected")
        self.condition()
        self.accept(Token.THEN, "'then' expected")
        self.sequenceOfStatements()
        while self.token.code == Token.ELSIF:
            self.token = self.scanner.nextToken()
            self.condition()
            self.accept(Token.THEN, "'then' expected")
            self.sequenceOfStatements()

        if self.token.code == Token.ELSE:
            self.token = self.scanner.nextToken()
            self.sequenceOfStatements()

        self.accept(Token.END, "'end' expected")
        self.accept(Token.IF, "'if' expected")
        self.accept(Token.SEMI, "semicolon expected")

    def exitStatement(self):
        self.accept(Token.EXIT, "'exit' expected")
        if self.token.code == Token.WHEN:
            self.token = self.scanner.nextToken()
            self.condition()
        self.accept(Token.SEMI, "semicolon expected")

    def assignmentOrCallStatement(self):
        entry = self.name()
        if self.token.code == Token.GETS:
            self.acceptRole(entry, self.leftNames, "must be a parameter of variable name")
            self.token = self.scanner.nextToken()
            self.expression()
        else:
            self.acceptRole(entry, SymbolEntry.PROC, "must be a procedure name")
        self.accept(Token.SEMI, "semicolon expected")

    def condition(self):
        self.expression()

    def expression(self):
        self.relation()
        if self.token.code == Token.AND:
            while self.token.code == Token.AND:
                self.token = self.scanner.nextToken()
                self.relation()
        elif self.token.code == Token.OR:
            while self.token.code == Token.OR:
                self.token = self.scanner.nextToken()
                self.relation()

    def relation(self):
        self.simpleExpression()
        if self.token.code in self.relationalOperator:
            self.token = self.scanner.nextToken()
            self.simpleExpression()

    def simpleExpression(self):
        if self.token.code in self.addingOperator:
            self.token = self.scanner.nextToken()
        self.term()
        while self.token.code in self.addingOperator:
            self.token = self.scanner.nextToken()
            self.term()

    def term(self):
        self.factor()
        while self.token.code in self.multiplyingOperator:
            self.token = self.scanner.nextToken()
            self.factor()

    def factor(self):
        if self.token.code == Token.NOT:
            self.token = self.scanner.nextToken()
            self.primary()
        else:
            self.primary()
            if self.token.code == Token.EXPO:
                self.token = self.scanner.nextToken()
                self.primary()

    def primary(self):
        #print(self.token.code)
        if (self.token.code == Token.INT) or (self.token.code == Token.CHAR):
            # int 검출 token id 랑 매칭하기
            self.token = self.scanner.nextToken()
        elif self.token.code == Token.ID:
            entry = self.name()
            self.acceptRole(entry, self.rightNames, "must be a parameter, variable or constant name")
        elif self.token.code == Token.L_PAR:
            self.token = self.scanner.nextToken()
            self.expression()
            self.accept(Token.R_PAR, "')' expected")
        elif self.token.code == Token.SEMI:
            return
        else:
            self.fatalError("error in primary")

    def name(self):
        entry = self.findId()
        if self.token.code == Token.L_PAR:
            self.indexedComponent()
        return entry

    def indexedComponent(self):
        self.accept(Token.L_PAR, "Left parenthesis expected")
        self.expression()
        while self.token.code == Token.COMMA:
            self.token = self.scanner.nextToken()
            self.expression()
        self.accept(Token.R_PAR, "right parenthesis expected")

    # no longer used
    def actualParameterPart(self):
        self.accept(Token.L_PAR, "left parenthesis expected")
        self.expression()
        while self.token.code == Token.COMMA:
            self.token = self.scanner.nextToken()
            self.expression()

        self.accept(Token.R_PAR, "right parenthesis expected")
