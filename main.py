from SyntaxAnalizator import SyntaxAnalizator
from collections import defaultdict
from LexicalAnalizator import LexicalAnalizator
from utils import prepare_expression_for_syntax_analysis

NUM_STR = "num"
ID_STR = "id"

# Define gramatiks for syntax analizator
NON_TERMINALS = {"P", "O", "I", "E", "E'", "N", "A"}
TERMINALS = {"+", "-", "*", "/", "(", ")", "=", ";", "id", "num", "e"}
RULES = defaultdict(list)
RULES["P"].extend([(["O", ";", "P"], 1), (["e"], 2)])
RULES["O"].extend([(["I", "=", "E"], 3)]) # , (["E"], 4)]) - Makes it LL(2)
RULES["E"].extend([(["N", "E'"], 5), (["I", "E'"], 6), (["(", "E", ")", "E'"], 7)])
RULES["E'"].extend([(["A", "E"], 8), (["e"], 9)])
RULES["A"].extend([(["+"], 10), (["-"], 11), (["*"], 12), (["/"], 13)])
RULES["I"].extend([([ID_STR], 14)])
RULES["N"].extend([([NUM_STR], 15)])
START_ELEMENT = "P"

# For lexical analizator
OPERATORS = TERMINALS.copy()
OPERATORS.difference_update({NUM_STR, ID_STR})

syntax_analizator = SyntaxAnalizator(rules=RULES, terminals=TERMINALS,
                                     non_terminals=NON_TERMINALS, start_element=START_ELEMENT)
lexical_analizator = LexicalAnalizator(number_str=NUM_STR, identificator_str=ID_STR,
                                       operators=OPERATORS)


print("Using LL(1) gramatik with rules:")
for rule_from, rules in RULES.items():
    for (rule_to, rule_number) in rules:
        print("Rule {}: {} -> {}".format(rule_number, rule_from, rule_to))
print("Possible expressions are like 'x=y + 7; y=2+2; w=x+y;'\n")

while True:
    expression = input("Please enter expression:")

    print("Doing lexical analysis:")
    tokens, subs = lexical_analizator.do_lexical_analysis(expression)
    print("Found tokens:", tokens, "\nMade substitutions:", subs)

    print("Doing syntax analysis:")
    tokens = prepare_expression_for_syntax_analysis(tokens, num_str=NUM_STR, id_str=ID_STR)
    rules = syntax_analizator.translate(tokens)
    if rules:
        print("Expression accepted\nFor translation used rules:", rules)
    else:
        print("Expression not accepted")
    print()

