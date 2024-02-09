from syntax_tree import SyntaxTree
from directConstruction import directConstruction
from render import render_nfa, render_dfa
from regex_nfa import regex_to_nfa
from nfa_dfa import nfa_to_dfa


def main():
    regex = "(a|b)*abb"
    tree = SyntaxTree(regex)
    tree.render()
    nfa = regex_to_nfa(regex)
    print(nfa.input_symbols())
    render_nfa(nfa)
    dfa = nfa_to_dfa(nfa)
    render_dfa(dfa)
    dfa.printme()
    dfa.minimize()
    render_dfa(dfa, "min_dfa")


if __name__ == "__main__":
    main()
