from CharIO import CharIO
from SymbolEntry import SymbolEntry

class SymbolTable:
    
    def __init__(self, c):
        self.chario = c
        self.reset()

    def reset(self):
        self.level = -1
        self.stack = []
    
    def enterScope(self):
        self.stack.append({})
        level += 1
    
    def exitScope(self, mode):
        table = self.stack.pop()
        self.printTable(table, mode)
        level -= 1

    def enterSymbol(self, id):
        table = self.stack[-1]
        if self.table.containsKey(id):
            self.chario.putError(id + "already declared in this block")
            return None
        else:
            s = SymbolEntry(id)
            self.table.append({id:s})
            return s
    
    def findSymbol(self, id):
        for i in range(len(self.stack)-1, -1, -1):
            table = self.stack[i]
            s = self.table[id]
            if s != None:
                return s
        self.chario.putError(id + "is undeclared identifier")
        return None

    def printTable(self, table, mode):
        self.chario.print("\nLevel" + str(self.level) +'\n')
        self.chario.print("--------------"+'\n')
        for s in table.values():
            self.chario.print(s.toString(mode))