class Node:
  
    leaf_index = 0
  
    def __init__(self, value, left=None, right=None, position=None):
        self.value = value
        self.left = left
        self.right = right
        self.position = position 
    def nullable(self):
        if self.value == '.':
            return self.left.nullable() and self.right.nullable()
        elif self.value == '|':
            return self.left.nullable() or self.right.nullable()
        elif self.value == '*':
            return True
        else:  
            return False if self.value else True 

    def firstpos(self):
        if self.value == '.':
            if self.left.nullable():
                return self.left.firstpos().union(self.right.firstpos())
            else:
                return self.left.firstpos()
        elif self.value == '|':
            return self.left.firstpos().union(self.right.firstpos())
        elif self.value == '*':
            return self.left.firstpos()
        else:  
            return {self.position} if self.position is not None else set()

    def lastpos(self):
        if self.value == '.':
            if self.right.nullable():
                return self.left.lastpos().union(self.right.lastpos())
            else:
                return self.right.lastpos()
        elif self.value == '|':
            return self.left.lastpos().union(self.right.lastpos())
        elif self.value == '*':
            return self.left.lastpos()
        else:  
            return {self.position} if self.position is not None else set()
