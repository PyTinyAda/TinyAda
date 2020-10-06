from Token import Token
from CharIO import CharIO

class Scanner:
    token = Token()
    chario = CharIO()
    ch = ''
    keywords = {}
    singleOps = {}
    doubleOps = {}
    MAX_KEY_SPELLING = 9
    
    def __init__(self):
        self.ch = ''
        self.keywords = {}
        self.singleOps = {}
        self.doubleOps = {}

    def scanner(self, c):
        self.chario = c


    def reset(self):
        self.chario.reset()
        ch = self.chario.getChar()

    def initKeywords(self):
        keywords['AND'] = Token(Token.AND)
        keywords['ARRAY'] = Token(Token.ARRAY)
        keywords['BEGIN'] = Token(Token.BEGIN)
        keywords['CONSTANT'] = Token(Token.CONST)
        keywords['ELSE'] = Token(Token.ELSE)
        keywords['ELSIF'] = Token(Token.ELSIF)
        keywords['END'] = Token(Token.END)
        keywords['EXIT'] = Token(Token.EXIT)
        keywords['IF'] = Token(Token.IF)
        keywords['IN'] = Token(Token.IN)
        keywords['IS'] = Token(Token.IS)
        keywords['LOOP'] = Token(Token.LOOP)
        keywords['MOD'] = Token(Token.MOD)
        keywords['NOT'] = Token(Token.NOT)
        keywords['NULL'] = Token(Token.NULL)
        keywords['OF'] = Token(Token.OF)
        keywords['OR'] = Token(Token.OR)
        keywords['OUT'] = Token(Token.OUT)
        keywords['PROCEDURE'] = Token(Token.PROC)
        keywords['RANGE'] = Token(Token.RANGE)
        keywords['THEN'] = Token(Token.THEN)
        keywords['TYPE'] = Token(Token.TYPE)
        keywords['WHEN'] = Token(Token.WHEN)
        keywords['WHILE'] = Token(Token.WHILE)
        
    def initSingleOps(self):
        singleOps[':'] = Token(Token.COLON)
        singleOps['='] = Token(Token.COMMA)
        singleOps['>'] = Token(Token.GT)
        singleOps['<'] = Token(Token.LT)
        singleOps['('] = Token(Token.L_PAR)
        singleOps['-'] = Token(Token.MINUS)
        singleOps['*'] = Token(Token.MUL)
        singleOps['/'] = Token(Token.DIV)
        singleOps['+'] = Token(Token.PLUS)
        singleOps[')'] = Token(Token.R_PAR)
        singleOps[';'] = Token(Token.SEMI)

    def initDoubleOps(self):
        doubleOps['**'] = Token(Token.EXPO)
        doubleOps['>='] = Token(Token.GE)
        doubleOps[':='] = Token(Token.GETS)
        doubleOps['<='] = Token(Token.LE)
        doubleOps['/='] = Token(Token.NE)
        doubleOps['..'] = Token(Token.THRU)

    def findToken(self, table, target):
        t = table[target]
        if t is None :
            return Token(Token.ERROR)
        else :
            return t
        
    def skipBlanks(self):
        while (self.ch is ' ' or self.ch is CharIO.EL or self.ch == CharIO.TAB) :
            self.ch = chario.getChar() 
    
    def getIdentifierOrKeyword(self):
        i = 0
        barCount = 0
        idBuffer = []
        tokenBuffer = []
        self.token = Token(Token.ID)
        if self.ch is '_':
            self.chario.putError("illegal leading '_")
        while True:
            self.ch = self.ch.upper()
            i = i + 1
            tokenBuffer.append(ch)
            if i <= self.MAX_KEY_SPELLING:
                idBuffer.append(self.ch)
            if self.ch is '_':
                self.ch = self.chario.getChar()
                if self.ch is '_':
                    barCount = barCount + 1
                if not (self.ch.isdigit() or self.ch.isalpha()) and self.ch is not '_':
                    self.chario.putError("letter or digit expected after '_'")
            else:
                self.ch = self.chario.getChar()
            if self.ch.isdigit() or self.ch.isalpha() or self.ch is '_':
                continue
            break
        if barCount > 0 :
            self.chario.putError("letter or digit expected after '-'")
        if i <= self.MAX_KEY_SPELLING :
            self.token = self.findToken(self.keywords, ''.join(idBuffer))
            if self.token.code is Token.ERROR:
                self.token.code = Token.ID
        if self.token.code is Token.ID :
            self.token.string = ''.join(tokenBuffer)
    
    def getInteger(self) :
        base = 16

        self.token = Token(Token.INT)
        self.getBasedInteger(10)
        if self.ch is '#':
            base = self.token.integer
            if base < 2 and base > 16:
                self.chario.putError('base must be between 2 and 16')
                base = 16
            self.ch = self.chario.getChar()
            if not (self.ch.isdigit() or self.ch.isalpha()):
                self.chario.putError("letter or digit expected after '#")
            self.getBasedInteger(base)
            if self.ch is '#':
                self.ch = self.chario.getChar()
            else:
                self.chario.putError("'# expected")

    def getBasedInteger(self, base) :
        base

        