class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        
    def nullable(self):
        if self.value == '.':
            return self.left.nullable() and self.right.nullable()
        elif self.value == '|':
            return self.left.nullable() or self.right.nullable()
        elif self.value == '*':
            return True
        else:
            return False
          
    def firstpos(self):
        if self.value == '.':
            return self.left.firstpos() | self.right.firstpos() if self.left.nullable() else self.left.firstpos()
        elif self.value == '|':
            return self.left.firstpos() | self.right.firstpos()
        elif self.value == '*':
            return self.left.firstpos()
        else:
            return {self}
          
    def lastpos(self):
        if self.value == '.':
            return self.left.lastpos() | self.right.lastpos() if self.right.nullable() else self.right.lastpos()
        elif self.value == '|':
            return self.left.lastpos() | self.right.lastpos()
        elif self.value == '*':
            return self.left.lastpos()
        else:
            return {self}

