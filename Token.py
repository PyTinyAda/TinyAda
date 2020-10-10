class Token:

#Some reserved words or operator symbols
   AND = 0
   ARRAY = 1
   BEGIN = 2
   CHAR = 3
   COLON = 4
   COMMA = 5
   CONST = 6
   DIV = 7
   ELSE = 8
   ELSIF = 9
   END = 10
   EOF = 11
   EQ = 12  #"="
   ERROR = 13
   EXIT = 14
   EXPO = 15
   GE = 16
   GETS = 17
   GT = 18
   ID = 19
   IF = 20
   IN = 21
   INT = 22
   IS = 23
   LE = 24
   LT = 25
   LOOP = 26
   L_PAR = 27
   MINUS = 28
   MOD = 29
   MUL = 30
   NE = 31
   NOT = 32
   NULL = 33
   OF = 34
   OR = 35
   OUT = 36
   PLUS = 37
   PROC = 38
   R_PAR = 39
   RANGE = 40
   SEMI = 41
   THEN = 42
   THRU = 43
   TYPE = 44
   WHEN = 45
   WHILE = 46

   code=0

   #for keywords or operators, these two variables have no meaning
   #integer seems to be used when this token represents a number literal
   integer=0
   #string seems to be used when this token represents a char, an identifier or a keyword
   string=""

   def Token(newCode):
      code = newCode
      integer = 0
      string = ""
   

   def toString():
      s = "Code    = " + CODES[code]
      if code == INT:
          s += "\nInteger = " + integer
      elif code == ID:
          s += "\nString = " + string;  
      return s
   

   CODES = ["AND", "ARRAY", "BEGIN", "CHAR", "COLON", "COMMA", "CONST", "DIV", "ELSE", "ELSIF",
                                  "END", "EOF", "EQ", "ERROR", "EXIT", "EXPO", "GE", "GETS", "GT", "ID", "IF", "IN",
                                  "INT", "IS", "LE", "LT", "LOOP", "L_PAR", "MINUS", "MOD", "MUL", "NE", "NOT", "NULL",
                                  "OF", "OR", "OUT", "PERIOD", "PLUS", "PROC", "R_PAR", "RANGE", "RECORD", "SEMI", 
                                  "THEN", "THRU", "TYPE", "WHEN", "WHILE"]
