class LexiconGenerator(object):
    def __init__(self):
        pass

    @staticmethod
    def generate(file):
        to_return = {}
        with open(file) as f:
            for line in f:
                key, entry = LexiconGenerator.__generate_key_entry(line)
                to_return[key] = entry
        return to_return

    @staticmethod
    def __generate_key_entry(line):
        # drop \n at the end if exists
        line = line.split("\n")[0]
        elements = line.split(" ")
        values = map(lambda elem: elem.split("=")[1], elements)
        key = values[2]
        return (key, LexiconEntry(values[0] == "weaksubj", int(values[1]), key, values[3], values[4] == "y",
                                  values[5] == "positive"))


class LexiconEntry(object):
    def __init__(self, is_weak, length, word, pos1, is_stemmed, is_positive):
        super(LexiconEntry, self).__init__()
        self.is_weak = is_weak
        self.weight = is_weak and 0.5 or 1
        self.length = length
        self.word = word
        self.pos1 = pos1
        self.is_stemmed = is_stemmed
        self.is_positive = is_positive

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.is_weak == other.is_weak \
                   and self.length == other.length \
                   and self.word == other.word \
                   and self.pos1 == other.pos1 \
                   and self.is_stemmed == other.is_stemmed \
                   and self.is_positive == other.is_positive


class SymbolicScore(object):
    def __init__(self):
        pass

    @staticmethod
    def compute_binary(tokens, lexicon):
        score = 0
        for token in tokens:
            try:
                entry = lexicon[token.value]
                if entry.is_positive:
                    score += 1
                else:
                    score -= 1
            except KeyError:
                continue
        return score

    @staticmethod
    def compute_weighted(tokens, lexicon):
        score = 0
        for token in tokens:
            try:
                entry = lexicon[token.value]
                if entry.is_positive:
                    score += entry.weight
                else:
                    score -= entry.weight
            except KeyError:
                continue
        return score
