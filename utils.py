import logging
import datetime

logging.basicConfig(filename="translating.log", level=logging.DEBUG)


def log(method):
    logging.debug("Called function: %s at %s", method.__name__, datetime.datetime.now())

    def inner(*args, **kwargs):
        res = method(*args, **kwargs)
        return res
    return inner


def prepare_expression_for_syntax_analysis(tokens, num_str, id_str):
    new_tokens = []
    for token in tokens:
        if token.startswith(num_str):
            token = num_str
        if token.startswith(id_str):
            token = id_str
        new_tokens.append(token)
    return new_tokens