from syntax_tree import SyntaxTree
from render import render_nfa
from regex_nfa import regex_to_nfa


def main():
    regex = "(a|b)*ac"
    # tree = SyntaxTree(regex)
    # tree.render()
    dfa = regex_to_nfa(regex)
    print(dfa.input_symbols())
    render_nfa(dfa)


if __name__ == "__main__":
    main()
