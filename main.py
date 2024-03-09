from Regex import Regex
from Yalex import Yalex
from syntax_tree import SyntaxTree

from directConstruction import DirectDFA
from render import render_nfa, render_dfa
from regex_nfa import regex_to_nfa
from nfa_dfa import nfa_to_dfa
from utils import isValidExpression


def main():
    yal = Yalex("examples/slr-3-3.yal")
    postfix = Regex(yal.final_regex).shunting_yard()
    print(yal.final_regex)
    ast = SyntaxTree(postfix)
    ast.render()

    # nfa = regex_to_nfa(regex)
    # render_nfa(nfa)
    # dfa = nfa_to_dfa(nfa)
    # render_dfa(dfa)

    # nfa.run(string)
    # dfa.run(string)

    # dfa.minimize()
    # render_dfa(dfa, "min_dfa")
    # dfa.run(string, True)


if __name__ == "__main__":
    main()
