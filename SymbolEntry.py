class SymbolEntry:

   NONE = 0
   CONST = 1
   PARAM = 2
   PROC = 3
   TYPE = 4
   VAR = 5

   def __init__(self, id):
      this.name = id
      this.role = NONE
      this.next = null
   

   def toString(mode):
      if mode == Parser.ROLE :
         return "Name: " + this.name + "\n" + "Role: " + this.roleToString()
      
      else:
         return "Name: " + this.name
 

   # "role" is an integer defined above
   def setRole(r):
      this.role = r
      if this.next != null:
         this.next.setRole(r)


   def append(entry):
      if this.next == null:
         this.next = entry
      else:
         this.next.append(entry)


   def roleToString():
      s = ""
      if this.role==this.NONE: s = "NONE"  
      elif this.role==this.CONST: s = "CONSTANT"  
      elif this.role==this.PARAM: s = "PARAMETER" 
      elif this.role==this.PROC: s = "PROCEDURE" 
      elif this.role==this.TYPE:  s = "TYPE"     
      elif this.role==this.VAR:   s = "VARIABLE"  
      else: s = "None"
      return s
