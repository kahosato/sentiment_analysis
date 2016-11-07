from enum import Enum

from util import accepts


class Token(object):
    value = ""

    def __init__(self):
        pass


class WordToken(Token):
    def __init__(self, word):
        super(WordToken, self).__init__()
        self.value = word

class PunctuationToken(Token):
    # punc : basestring, not sure how to check self
    def __init__(self, punc):
        super(Token, self).__init__()
        self.value = Punctuation.create(punc)


class Punctuation(Enum):
    period = 1
    comma = 2
    semicolon = 3
    exclamation = 4
    apostrophe = 5
    quotation = 6
    hyphen = 7
    left_round = 8
    right_round = 9
    left_square = 10
    right_square = 11
    left_curly = 12
    right_curly = 13
    left_angle = 14
    right_angle = 15
    question = 16
    slash = 17

    lookup = {
        ".": period,
        ",": comma,
        ";": semicolon,
        "!": exclamation,
        "'": apostrophe,
        "\"": quotation,
        "-": hyphen,
        "(": left_round,
        ")": right_round,
        "[": left_square,
        "]": right_square,
        "{": left_curly,
        "}": right_curly,
        "<": left_angle,
        ">": right_angle,
        "?": question,
        "/": slash
    }

    @staticmethod
    @accepts(basestring)
    def create(punc):
        try:
            return Punctuation.lookup[punc]
        except KeyError:
            raise ValueError("Not a punctuation")
