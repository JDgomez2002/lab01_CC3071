from node import Node

class SyntaxTree:
    def __init__(self, regex):
      self.root = self.regex_to_syntax_tree(regex)
      print(self.root)

    def regex_to_syntax_tree(self,regex):
      
      postfix_regex = shunting_yard(regex)
      
      stack = []
      for char in postfix_regex:
          if char not in {'*', '|', '.'}:
              stack.append(Node(char))
          else:
              if char == '*':
                  operand = stack.pop()
                  stack.append(Node(char, operand))
              else:
                  right = stack.pop()
                  left = stack.pop()
                  stack.append(Node(char, left, right))

      return stack.pop() if stack else None
      
      
def shunting_yard(regex):
      precedence = {'|': 1, '.': 2, '*': 3}  
      output = []
      stack = []
      
      regex = add_concatenation_symbol(regex)

      for token in regex:
          if token.isalpha():
              output.append(token)
          elif token == '(':  
              stack.append(token)
          elif token == ')':
              while stack and stack[-1] != '(':
                  output.append(stack.pop())
              stack.pop()  
          else: 
              while stack and stack[-1] != '(' and precedence[token] <= precedence[stack[-1]]:
                  output.append(stack.pop())
              stack.append(token)

      while stack:
          output.append(stack.pop())

      return ''.join(output)


def add_concatenation_symbol(regex):
        output = ""
        operators = set(['.', '|', '*', '(', ')'])  # regex operators
        for i in range(len(regex) - 1):
            output += regex[i]
            if (regex[i] not in operators and regex[i+1] not in operators) or \
              (regex[i] not in operators and regex[i+1] == '(') or \
              (regex[i] == ')' and regex[i+1] not in operators) or \
              (regex[i] == '*' and regex[i+1] not in operators) or \
              (regex[i] == '*' and regex[i+1] == '('):
                output += '.'
        output += regex[-1]
        return output
