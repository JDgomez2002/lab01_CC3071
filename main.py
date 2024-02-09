from syntax_tree import SyntaxTree
from directConstruction import DirectDFA
from render import render_nfa, render_dfa
from regex_nfa import regex_to_nfa
from nfa_dfa import nfa_to_dfa


def main():
    directDFA = DirectDFA("a(b|c)*d#")
    directDFA.render()
    directDFA.run("abbc")

    regex = "a(b|c)*d"
    tree = SyntaxTree(regex)
    tree.render()
    nfa = regex_to_nfa(regex)
    render_nfa(nfa)
    dfa = nfa_to_dfa(nfa)
    render_dfa(dfa)
    # dfa.printme()
    dfa.minimize()
    render_dfa(dfa, "min_dfa")

    print(nfa.run("abd"))
    print(dfa.run("abd"))


if __name__ == "__main__":
    main()
