from enum import Enum

from util import accepts


class TokenFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def create(val):
        try:
            return PunctuationToken(val)
        except ValueError:
            return WordToken(val)


class Token(object):
    value = ""

    def __init__(self):
        pass

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        return False

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

class WordToken(Token):
    def __init__(self, word):
        super(WordToken, self).__init__()
        self.value = word


class PunctuationToken(Token):
    lookup = ".,;:!'\"-()[]{}<>?/"

    # lookup = {
    #     ".": Punctuation.period,
    #     ",": Punctuation.comma,
    #     ";": Punctuation.semicolon,
    #     "!": Punctuation.exclamation,
    #     "'": Punctuation.apostrophe,
    #     "\"": Punctuation.quotation,
    #     "-": Punctuation.hyphen,
    #     "(": Punctuation.left_round,
    #     ")": Punctuation.right_round,
    #     "[": Punctuation.left_square,
    #     "]": Punctuation.right_square,
    #     "{": Punctuation.left_curly,
    #     "}": Punctuation.right_curly,
    #     "<": Punctuation.left_angle,
    #     ">": Punctuation.right_angle,
    #     "?": Punctuation.question,
    #     "/": Punctuation.slash
    # }
    # punc : basestring, not sure how to check self

    def __init__(self, punc):
        super(Token, self).__init__()
        if punc in PunctuationToken.lookup:
            self.value = punc
        else:
            raise ValueError("Not a punctuation")
