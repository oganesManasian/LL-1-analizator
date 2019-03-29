from collections import defaultdict

from SyntaxAnalizator import SyntaxAnalizator
from LexicalAnalizator import LexicalAnalizator

# Define grmamatics
NON_TERMINALS = {"E", "E'", "T", "T'", "F"}
TERMINALS = {"+", "-", "*", "/", "a", "(", ")", "e"}
RULES = defaultdict(list)
RULES["E"].extend([[["T", "E'"], 1]])
RULES["E'"].extend([[["+", "T", "E'"], 2], [["-", "T", "E'"], 3], [["e"], 4]])
RULES["T"].extend([[["F", "T'"], 5]])
RULES["T'"].extend([[["*", "F", "T'"], 6], [["/", "F", "T'"], 7], [["e"], 8]])
RULES["F"].extend([[["(", "E", ")"], 9], [["a"], 10]])
START_ELEMENT = "E"

# Create Grammatics
syntax_analizator = SyntaxAnalizator(rules=RULES, terminals=TERMINALS,
                                     non_terminals=NON_TERMINALS, start_element=START_ELEMENT)


def test1():
    expression1 = "(a+a)"
    rules = syntax_analizator.translate(expression1)
    right_rules = [1, 5, 9, 1, 5, 10, 8, 2, 5, 10, 8, 4, 8, 4]
    passed = (rules == right_rules)
    print("Test1 passed:", passed)


def test2():
    expression2 = "(a*(a-a/a)+a)/a"
    rules = syntax_analizator.translate(expression2)
    right_rules = [1, 5, 9, 1, 5, 10, 6, 9, 1, 5, 10, 8, 3, 5, 10, 7, 10, 8, 4, 8, 2, 5, 10, 8, 4, 7, 10, 8, 4]
    passed = (rules == right_rules)
    print("Test2 passed:", passed)


def test3():
    expression3 = "(a*a"
    rules = syntax_analizator.translate(expression3)
    right_rules = []
    passed = (rules == right_rules)
    print("Test3 passed:", passed)


def test4():
    expression4 = "(a*a+++++++"
    rules = syntax_analizator.translate(expression4)
    right_rules = []
    passed = (rules == right_rules)
    print("Test4 passed:", passed)


def test5():
    expression4 = "a+a*a"
    rules = syntax_analizator.translate(expression4)
    right_rules = [1, 5, 10, 8, 2, 5, 10, 6, 10, 8, 4]
    passed = (rules == right_rules)
    print("Test5 passed:", passed)


tests__syntax = [test1, test2, test3, test4, test5]


def test_syntax_analysis():
    """Tests Grammatics class methods for parsing expressions defined by simple rpn grammatic"""
    print("Syntax analysis test")
    for test in tests__syntax:
        test()


test_syntax_analysis()