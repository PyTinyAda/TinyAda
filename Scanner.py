from Token import Token
from CharIO import CharIO

class Scanner:
    token = Token()
    chario = CharIO()
    ch = ''
    keywords = {}
    singleOps = {}
    doubleOps = {}
    tokenBuffer = []
    MAX_KEY_SPELLING = 9
    
    def __init__(self, c):
        self.chario = c
        self.initKeywords()
        self.initSingleOps()
        self.initDoubleOps()
        self.ch = self.chario.getChar()

    def reset(self):
        self.chario.reset()
        self.ch = self.chario.getChar()

    def initKeywords(self):
        self.keywords['AND'] = Token(Token.AND)
        self.keywords['ARRAY'] = Token(Token.ARRAY)
        self.keywords['BEGIN'] = Token(Token.BEGIN)
        self.keywords['CONSTANT'] = Token(Token.CONST)
        self.keywords['ELSE'] = Token(Token.ELSE)
        self.keywords['ELSIF'] = Token(Token.ELSIF)
        self.keywords['END'] = Token(Token.END)
        self.keywords['EXIT'] = Token(Token.EXIT)
        self.keywords['IF'] = Token(Token.IF)
        self.keywords['IN'] = Token(Token.IN)
        self.keywords['IS'] = Token(Token.IS)
        self.keywords['LOOP'] = Token(Token.LOOP)
        self.keywords['MOD'] = Token(Token.MOD)
        self.keywords['NOT'] = Token(Token.NOT)
        self.keywords['NULL'] = Token(Token.NULL)
        self.keywords['OF'] = Token(Token.OF)
        self.keywords['OR'] = Token(Token.OR)
        self.keywords['OUT'] = Token(Token.OUT)
        self.keywords['PROCEDURE'] = Token(Token.PROC)
        self.keywords['RANGE'] = Token(Token.RANGE)
        self.keywords['THEN'] = Token(Token.THEN)
        self.keywords['TYPE'] = Token(Token.TYPE)
        self.keywords['WHEN'] = Token(Token.WHEN)
        self.keywords['WHILE'] = Token(Token.WHILE)
        
    def initSingleOps(self):
        self.singleOps[':'] = Token(Token.COLON)
        self.singleOps['='] = Token(Token.COMMA)
        self.singleOps['>'] = Token(Token.GT)
        self.singleOps['<'] = Token(Token.LT)
        self.singleOps['('] = Token(Token.L_PAR)
        self.singleOps['-'] = Token(Token.MINUS)
        self.singleOps['*'] = Token(Token.MUL)
        self.singleOps['/'] = Token(Token.DIV)
        self.singleOps['+'] = Token(Token.PLUS)
        self.singleOps[')'] = Token(Token.R_PAR)
        self.singleOps[';'] = Token(Token.SEMI)

    def initDoubleOps(self):
        self.doubleOps['**'] = Token(Token.EXPO)
        self.doubleOps['>='] = Token(Token.GE)
        self.doubleOps[':='] = Token(Token.GETS)
        self.doubleOps['<='] = Token(Token.LE)
        self.doubleOps['/='] = Token(Token.NE)
        self.doubleOps['..'] = Token(Token.THRU)

    def findToken(self, table, target):
        t = table[target]
        if t is None :
            return Token(Token.ERROR)
        else :
            return t
        
    def skipBlanks(self):
        while (self.ch == ' ' or self.ch == CharIO.EL or self.ch == CharIO.TAB) :
            self.ch = self.chario.getChar() 
    
    def getIdentifierOrKeyword(self):
        i = 0
        barCount = 0
        idBuffer = []
        self.tokenBuffer = []
        self.token = Token(Token.ID)
        if self.ch == '_':
            self.chario.putError("illegal leading '_")
        while True:
            self.ch = self.ch.upper()
            i = i + 1
            self.tokenBuffer.append(self.ch)
            if i <= self.MAX_KEY_SPELLING:
                idBuffer.append(self.ch)
            if self.ch == '_':
                self.ch = self.chario.getChar()
                if self.ch == '_':
                    barCount = barCount + 1
                if not (self.ch.isdigit() or self.ch.isalpha()) and self.ch != '_':
                    self.chario.putError("letter or digit expected after '_'")
            else:
                self.ch = self.chario.getChar()
            if self.ch.isdigit() or self.ch.isalpha() or self.ch == '_':
                continue
            break
        if barCount > 0 :
            self.chario.putError("letter or digit expected after '-'")
        if i <= self.MAX_KEY_SPELLING :
            self.token = self.findToken(self.keywords, ''.join(idBuffer))
            if self.token.code == Token.ERROR:
                self.token.code = Token.ID
        if self.token.code == Token.ID :
            self.token.string = ''.join(self.tokenBuffer)
    
    def getInteger(self) :
        base = 16

        self.token = Token(Token.INT)
        self.getBasedInteger(10)
        if self.ch == '#':
            base = self.token.integer
            if base < 2 and base > 16:
                self.chario.putError('base must be between 2 and 16')
                base = 16
            self.ch = self.chario.getChar()
            if not (self.ch.isdigit() or self.ch.isalpha()):
                self.chario.putError("letter or digit expected after '#")
            self.getBasedInteger(base)
            if self.ch == '#':
                self.ch = self.chario.getChar()
            else:
                self.chario.putError("'# expected")

    def getBasedInteger(self, base) :
        barCount = 0
        self.token.integer = 0
        while self.ch.isdigit() or self.ch.isalpha() or self.ch == '_':
            if self.ch == '_':
                self.ch = self.chario.getChar()
                if self.ch == '_':
                    barCount += 1
                if not (self.ch.isdigit() or self.ch.isalpha()) and self.ch != '_':
                    self.chario.putError("letter or digit expected after '_'")
            else :
                self.token.integer = base * self.token.integer + self.charToInt(self.ch, base)
                self.ch = self.chario.getChar()
        if barCount > 0:
            self.chario.putError("letter or digit expected after '_'")

    def charToInt(self, ch, base):
        digit = int(ch, base)
        if digit == -1:
            self.chario.putError("digit not in range of base")
            digit = 0
        return digit
    
    def getCharacter(self):
        self.token = Token(Token.CHAR)
        self.ch = self.chario.getChar()
        if self.ch == CharIO.EL:
            self.chario.putError("''' expected")
            self.tokenBuffer.append(' ')
            self.ch = self.chario.getChar()
        else :
            self.token.string = '' + self.ch
            self.ch = self.chario.getChar()
            if self.ch == '\'':
                self.ch = self.chario.getChar()
            else :
                self.chario.putError("''' expected")
    
    def getDoubleOp(self):
        self.tokenBuffer = []
        self.tokenBuffer.append(self.ch)
        self.ch = self.chario.getChar()
        self.tokenBuffer.append(self.ch)
        self.token = self.findTokenfindTokken(self.doubleOps, ''.join(self.tokenBuffer))
        if self.token.code != Token.ERROR:
            self.ch = self.chario.getChar()

    def getSingleOp(self):
        self.token = self.findToken(self.singleOps, "" + self.tokenBuffer[0])

    def nextToken(self):
        while True:
            self.skipBlanks()
            if self.ch.isalpha() or self.ch == '_':
                self.getIdentifierOrKeyword()
            elif self.ch.isdigit():
                self.getInteger()
            elif self.ch == '\'' :
                self.getCharacter()
            elif self.ch == CharIO.EF :
                self.token = Token(Token.EOF)
            else :
                self.getDoubleOp()
                if self.token.code == Token.ERROR :
                    self.getSingleOp()
                    if self.token.code == Token.ERROR:
                        self.chario.putError("unrecognized symbol")
            if self.token.code == Token.ERROR:
                continue
            return self.token


        
