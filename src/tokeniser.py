import re

from tokens import TokenFactory
from util import *


class Tokeniser(object):
    def __init__(self):
        pass

    @staticmethod
    @accepts(basestring)
    def tokenise(file):
        with open(file) as f:
            for line in f:
                line = line.split("\n")[0]
                if line:
                    tokens = Tokeniser.tokenise_sentence(line)
                    for token in tokens:
                        yield token

    @staticmethod
    def tokenise_sentence(line):
        tokens = filter(lambda token: token != "", line.split(" "))
        tokens = Tokeniser.__lower_start(tokens)
        to_return = []
        for token in tokens:
            # i guess one could assume that they are mutually exclusive ?
            split_tokens = map(Tokeniser.__normalise, Tokeniser.__split_token(token))
            to_return += split_tokens
        factory = TokenFactory()
        return map(factory.create, filter(lambda x: x, to_return))

    @staticmethod
    def __normalise(token):
        if token == "I":
            token = "i"
        return token

    @staticmethod
    def __split_token(token):
        split_tokens = [token]
        split_tokens = Tokeniser.__split_hyphen(split_tokens)
        split_tokens = Tokeniser.__split_slash(split_tokens)
        split_tokens = Tokeniser.__split_comma(split_tokens)
        split_tokens = Tokeniser.__split_left_bracket(split_tokens)
        split_tokens = Tokeniser.__split_right_bracket(split_tokens)
        split_tokens = Tokeniser.__split_ll(split_tokens)
        split_tokens = Tokeniser.__split_nt(split_tokens)
        split_tokens = Tokeniser.__split_d(split_tokens)
        split_tokens = Tokeniser.__split_s(split_tokens)
        split_tokens = Tokeniser.__split_ve(split_tokens)
        split_tokens = Tokeniser.__split_last_period(split_tokens)

        return split_tokens

    @staticmethod
    def __apply_rule(rule, t):
        pass

    @staticmethod
    def __split_with_punctuation(to_split, punc):
        # a/b -> a, /, b
        # /a -> /, a
        # a/ -> a, /
        # assume to_split doesn't include space
        tokens = to_split.split(punc)
        to_return = []
        if tokens[0]:
            to_return.append(tokens[0])
        for token in tokens[1:]:
            to_return.append(punc)
            to_return.append(token)
        if not tokens[-1]:
            return to_return[:-1]
        return to_return

    @staticmethod
    def __split_hyphen(tokens):
        pattern = re.compile(r"([a-z|A-Z]+)(\-[a-z|A-Z]+)+")
        to_return = []
        for token in tokens:
            if pattern.match(token):
                to_return += Tokeniser.__split_with_punctuation(token, "-")
            else:
                to_return.append(token)
        return to_return

    @staticmethod
    def __split_slash(tokens):
        pattern = re.compile(r".*/.*")
        to_return = []
        for token in tokens:
            if pattern.match(token):
                to_return += Tokeniser.__split_with_punctuation(token, "/")
            else:
                to_return.append(token)
        return to_return

    @staticmethod
    def __split_comma(tokens):
        pattern = re.compile(r".*,")
        to_return = []
        for token in tokens:
            if pattern.match(token):
                to_return += Tokeniser.__split_with_punctuation(token, ",")
            else:
                to_return.append(token)
        return to_return

    @staticmethod
    def __split_left_bracket(tokens):
        pattern = re.compile(r"([\(\[{\"])(.*)")
        to_return = []
        for token in tokens:
            match = pattern.match(token)
            if match:
                to_return += [match.group(1), match.group(2)]
            else:
                to_return.append(token)
        return to_return

    @staticmethod
    def __split_right_bracket(tokens):
        pattern = re.compile(r"(.*)([\"\)\[{])")
        to_return = []
        for token in tokens:
            match = pattern.match(token)
            if match:
                to_return += [match.group(1), match.group(2)]
            else:
                to_return.append(token)
        return to_return

    @staticmethod
    def __split_ll(tokens):
        pattern = re.compile(r"(.+)'ll$")
        to_return = []
        for token in tokens:
            match = pattern.match(token)
            if match:
                to_return += [match.group(1), "will"]
            else:
                to_return.append(token)
        return to_return

    @staticmethod
    def __split_nt(tokens):
        pattern = re.compile(r"(.+)n't$")
        to_return = []
        for token in tokens:
            match = pattern.match(token)
            if match:
                return [match.group(1), "not"]
            else:
                to_return.append(token)
        return to_return

    @staticmethod
    def __split_d(tokens):
        pattern = re.compile(r"(.+)'d$")
        to_return = []
        for token in tokens:
            match = pattern.match(token)
            if match:
                return [match.group(1), "'d"]
            else:
                to_return.append(token)
        return to_return

    @staticmethod
    def __split_s(tokens):
        pattern = re.compile(r"(.+)'s$")
        to_return = []
        for token in tokens:
            match = pattern.match(token)
            if match:
                return [match.group(1), "'s"]
            else:
                to_return.append(token)
        return to_return

    @staticmethod
    def __split_ve(tokens):
        pattern = re.compile(r"(.+)'ve$")
        to_return = []
        for token in tokens:
            match = pattern.match(token)
            if match:
                return [match.group(1), "have"]
            else:
                to_return.append(token)
        return to_return

    @staticmethod
    def __lower_start(tokens):
        pattern = re.compile(r"([A-Z])(.*)")
        match = pattern.match(tokens[0])
        if match:
            return [match.group(1).lower() + match.group(2)] + tokens[1:]
        else:
            return tokens

    @staticmethod
    def __split_last_period(tokens):
        pattern = re.compile(r"(.+)([\?\!\.;:]+)$")
        to_return = []
        for token in tokens:
            match = pattern.match(token)
            if match:
                to_return += [match.group(1), match.group(2)]
            else:
                to_return.append(token)
        return to_return
