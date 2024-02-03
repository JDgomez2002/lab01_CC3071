from syntax_tree import SyntaxTree
def print_tree(node, indent=0):
    if node is not None:
        print_tree(node.right, indent + 4)
        print( indent * ' ' + str(node.value))
        print_tree(node.left, indent + 4)

regex = "(a|b)a"
root = SyntaxTree(regex).root 

print_tree(root)

