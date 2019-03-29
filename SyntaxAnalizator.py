import collections
from collections import defaultdict
from dataclasses import dataclass
import logging
from utils import log


@dataclass
class Configuration:
    expression: list
    store: list
    used_rules: list


@dataclass
class Gramatik:
    rules: defaultdict
    terminals: set
    non_terminals: set
    start_element: str


@dataclass
class SyntaxAnalizator:
    """Class implementing functions for syntax analysis of expression
    using defined LL(1) gramatiks"""
    rules: defaultdict
    terminals: set
    non_terminals: set
    start_element: str

    MRK = "$"  # End marker
    e_SYMBOL = "e"  # e symbol of gramatics
    ACP = 0  # Expression accepted code
    ERROR = -1  # Parsing error code
    RLS = -2  # Release code

    def __post_init__(self):
        self.table = dict()
        self._generate_table()

    def _first(self, non_terminal: str):
        """Recursive method for finding first of non terminal"""
        if non_terminal in self.terminals:
            print("Trying to find first of terminal")
            return None

        firsts = set()
        rules = self.rules[non_terminal]
        for (translation, *_), *_ in rules:
            if translation in self.terminals:
                firsts.add(translation)
            else:
                firsts.update(self._first(translation))

        return firsts

    def _find_translation(self, non_terminal, terminal):
        """Recursive method for finding rules for translating
        non terminal to terminal"""
        if terminal not in self._first(non_terminal=non_terminal):
            logging.error("There is no translation")
            return None

        rules = self.rules[non_terminal]
        for rule in rules:
            translation = rule[0]

            if translation[0] in self.terminals:
                if translation[0] == terminal:
                    # Found needed element, so all translation rules are found
                    return [rule]
                else:
                    continue
            elif translation[0] in self.non_terminals:
                # Nonterminal, so we have to look for its translations
                next_translation_rules = self._find_translation(translation[0], terminal)
                if next_translation_rules is not None:
                    # Add next rules
                    next_translation_rules.insert(0, rule)
                    return next_translation_rules

        return None

    def _generate_table(self):
        """Generates translation table using grammatics"""
        all_elements = self.terminals | self.non_terminals | {self.MRK}
        for element in all_elements:
            element_translations = dict()

            if element in self.non_terminals:
                firsts = self._first(element)
                for terminal in self.terminals:
                    if terminal in firsts:
                        # Find first rule using for translation
                        translation_rules = self._find_translation(non_terminal=element, terminal=terminal)
                        if translation_rules is None:
                            logging.error("Error generating table")
                            return
                        element_translations[terminal] = translation_rules[0]  # First rule used for translation
                    else:
                        element_translations[terminal] = self.ERROR

            elif element in self.terminals:
                # Delete first elements from store and expression
                element_translations = {terminal: self.RLS if terminal == element else self.ERROR
                                        for terminal in self.terminals}

            elif element == self.MRK:
                # Expression accepted
                element_translations = {terminal: self.ACP if terminal == self.e_SYMBOL else self.ERROR
                                        for terminal in self.terminals}

            self.table[element] = element_translations

    @log
    def translate(self, expr):
        """Translates expression to rules list using translation table
        Returns empty list if translation is impossible"""
        if type(expr) != list:
            expr = list(expr)

        logging.debug("Translating expression %s", expr)
        config = Configuration(expression=expr, store=[self.start_element, self.MRK], used_rules=[])

        step = 0
        while config.expression:
            logging.debug("Step: %s %s", step, config)
            step += 1

            try:
                rule = self.table[config.store[0]][config.expression[0]]
            except KeyError:
                print("Impossible symbol detected: " + config.expression[0])
                logging.error("Impossible symbol detected: " + config.expression[0])
                logging.debug("Expression not accepted")
                return []

            if rule == self.ERROR and config.store[0] != self.MRK:  # Handling e rules
                logging.debug("Trying to find e rule")
                rule = self.table[config.store[0]][self.e_SYMBOL]
                if rule != self.ERROR:
                    config.expression.insert(0, self.e_SYMBOL)

            if rule == self.ERROR:
                print("Error: No rule in gramatiks translating {} to {}".format(config.store[0], config.expression[0]))
                logging.error("Error: No rule in gramatiks translating {} to {}"
                              .format(config.store[0], config.expression[0]))
                logging.debug("Expression not accepted")
                return []
            elif rule == self.ACP:
                logging.debug("Expression accepted")
                return config.used_rules
            elif rule == self.RLS:
                logging.debug("Deleting same elements")
                del config.store[0]
                del config.expression[0]
            # elif isinstance(rule, list) or isinstance(rule, tuple):  # Maybe this is better?
            # elif hasattr(rule, "__getitem__"):
            elif isinstance(rule, collections.Sequence):
                logging.debug("Make translation using rule %s", rule)
                new_value = rule[0]
                rule_number = rule[1]
                config.store[0:1] = list(new_value)
                config.used_rules.append(rule_number)
            else:
                logging.error("Unknown symbol in table")
                return []

            if len(config.expression) == 0 and len(config.store) > 0:
                config.expression.insert(0, self.e_SYMBOL)  # Add e symbols for possibility to use e rules

    def draw_syntax_tree(self, expr, used_rules):
        """Draw syntax tree using rules list used for translation"""
        pass
