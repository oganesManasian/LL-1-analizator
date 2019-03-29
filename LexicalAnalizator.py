import string
import logging
from dataclasses import dataclass


@dataclass
class LexicalAnalizator:
    """Class implementing lexical analysis of expression"""
    number_str: str
    identificator_str: str
    operators: set

    TOKEN_NUMBER = 0
    TOKEN_IDENTIFICATOR = 1
    TOKEN_OPERATOR = 2

    def do_lexical_analysis(self, expression):
        """Tokenize expression
        Returns array of tokens and made substitutions"""
        expression = expression[:]

        expression = self._delete_whitespaces(expression)

        tokens = []
        substitutions = dict()
        identificators_count = 0
        numbers_count = 0

        for token, token_type in self._tokens(expression):
            if token_type == self.TOKEN_NUMBER:
                new_token = self.number_str + str(numbers_count)
                numbers_count += 1
                substitutions[new_token] = token
            elif token_type == self.TOKEN_IDENTIFICATOR:
                new_token = self.identificator_str + str(identificators_count)
                identificators_count += 1
                substitutions[new_token] = token
            elif token_type == self.TOKEN_OPERATOR:
                new_token = token
            elif token_type is None:
                break
            else:
                print("Error: Unknown token type")
                return [], {}

            tokens.append(new_token)

        return tokens, substitutions

    @staticmethod
    def _delete_whitespaces(expression):
        return expression.replace(" ", "")

    def _tokens(self, expression):
        """Generator, subsequently yields tokens from expression"""
        cur_pos = 0

        token_readers = {self.TOKEN_IDENTIFICATOR: self._read_identificator,
                         self.TOKEN_NUMBER: self._read_number,
                         self.TOKEN_OPERATOR: self._read_operator}

        while True:
            if cur_pos >= len(expression):
                break

            symbol = expression[cur_pos]
            if symbol in string.ascii_letters:
                token_type = self.TOKEN_IDENTIFICATOR
            elif symbol in string.digits:
                token_type = self.TOKEN_NUMBER
            elif symbol in self.operators:  # TODO Think what to do with id and numbers terminals
                token_type = self.TOKEN_OPERATOR
            else:
                logging.debug("Error: Unknown symbol:" + symbol)
                yield -1, -1

            token, cur_pos = token_readers[token_type](expression, cur_pos)
            yield token, token_type
        yield None, None

    @staticmethod
    def _read_identificator(expression, cur_pos):
        identificator = ""
        while cur_pos < len(expression) and expression[cur_pos] in string.ascii_letters:
            identificator += expression[cur_pos]
            cur_pos += 1

        return identificator, cur_pos  # TODO exclude the possibility of errors in order of returning values

    @staticmethod
    def _read_number(expression, cur_pos):
        number = ""
        while cur_pos < len(expression) and expression[cur_pos] in string.digits:
            number += expression[cur_pos]
            cur_pos += 1

        return number, cur_pos

    @staticmethod
    def _read_operator(expression, cur_pos):
        operator = expression[cur_pos]
        cur_pos += 1
        return operator, cur_pos






