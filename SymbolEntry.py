from Parser import Parser

class SymbolEntry:

   NONE = 0
   CONST = 1
   PARAM = 2
   PROC = 3
   TYPE = 4
   VAR = 5

   def __init__(self, id):
      self.name = id
      self.role = NONE
      self.next = None
   

   def toString(self, mode):
      if mode == Parser.ROLE :
         return "Name: " + self.name + "\n" + "Role: " + self.roleToString()
      
      else:
         return "Name: " + self.name
 

   # "role" is an integer defined above
   def setRole(self, r):
      this.role = r
      if self.next != None:
         self.next.setRole(r)


   def append(self, entry):
      if self.next == None:
         self.next = entry
      else:
         self.next.append(entry)


   def roleToString(self):
      s = ""
      if self.role == self.NONE: s = "NONE"  
      elif self.role == self.CONST: s = "CONSTANT"  
      elif self.role == self.PARAM: s = "PARAMETER" 
      elif self.role == self.PROC: s = "PROCEDURE" 
      elif self.role == self.TYPE:  s = "TYPE"     
      elif self.role == self.VAR:   s = "VARIABLE"  
      else: s = "NONE"
      return s
