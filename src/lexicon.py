# type=weaksubj len=1 word1=abandoned pos1=adj stemmed1=n priorpolarity=negative
from util import accepts


class LexiconGenerator(object):
    def __init__(self):
        pass

    @staticmethod
    def generate(file):
        to_return = []
        with open(file) as f:
            return map(LexiconGenerator.__generate_one, f)

    @staticmethod
    def __generate_one(line):
        # drop \n at the end if exists
        line = line.split("\n")[0]
        elements = line.split(" ")
        values = map(lambda elem: elem.split("=")[1], elements)
        return LexiconEntry(values[0] == "weaksubj", int(values[1]), values[2], values[3], values[4] == "y",
                            values[5] == "positive")


class LexiconEntry(object):
    def __init__(self, is_weak, length, word, pos1, is_stemmed, is_positive):
        super(LexiconEntry, self).__init__()
        self.is_weak = is_weak
        self.length = length
        self.word = word
        self.pos1 = pos1
        self.is_stemmed = is_stemmed
        self.is_positive = is_positive

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.is_weak == other.is_weak\
                and self.length == other.length\
                and self.word == other.word\
                and self.pos1 == other.pos1\
                and self.is_stemmed == other.is_stemmed\
                and self.is_positive == other.is_positive

if __name__ == "__main__":
    lex = LexiconGenerator.generate("../resources/sent_lexicon")
    # 0: type=weaksubj len=1 word1=abandoned pos1=adj stemmed1=n priorpolarity=negative
    assert lex[0] == LexiconEntry(True, 1, "abandoned", "adj", False, False, "")
    # 1