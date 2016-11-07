from util import *

class Tokeniser:
    def __init__(self):
        pass

    @staticmethod
    @accepts(basestring, basestring)
    def tokenise(file, config):
        delimiter = ""
        with open(config) as c:
            delimiter = ""
            # set delimiter
        tokens = []
        with open(file) as f:
            for line in f:
                tokens.append(Tokeniser.__tokenise_sentence(line))
        return []

    @staticmethod
    def __tokenise_sentence(line):
        pass

