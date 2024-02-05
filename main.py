from syntax_tree import SyntaxTree

def main():
    regex = "(a|b)*abb#"
    tree = SyntaxTree(regex)
    tree.render()

if __name__ == "__main__":
    main()
