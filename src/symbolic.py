class LexiconGenerator(object):
    sentiment_score = {
        "positive": 1,
        "neutral": 0,
        "negative": -1,
        "both": 0
    }
    sentiment_weight = {
        "weaksubj": 0.5,
        "strongsubj": 1
    }

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
        return (key, LexiconEntry(LexiconGenerator.sentiment_weight[values[0]], int(values[1]), key, values[3],
                                  values[4] == "y",
                                  LexiconGenerator.sentiment_score[values[5]]))


class LexiconEntry(object):
    def __init__(self, weight, length, word, pos1, is_stemmed, sentiment_score):
        super(LexiconEntry, self).__init__()
        self.weight = weight
        self.length = length
        self.word = word
        self.pos1 = pos1
        self.is_stemmed = is_stemmed
        self.sentiment_score = sentiment_score

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.weight == other.weight \
                   and self.length == other.length \
                   and self.word == other.word \
                   and self.pos1 == other.pos1 \
                   and self.is_stemmed == other.is_stemmed \
                   and self.sentiment_score == other.sentiment_score


# Symbolic approach without negation
class SymbolicScore(object):
    def __init__(self):
        pass

    @staticmethod
    def compute(tokens, lexicon, bin=False):
        score = 0
        for token in tokens:
            try:
                entry = lexicon[token.value]
                if bin:
                    score += entry.sentiment_score
                else:
                    score += entry.sentiment_score * entry.weight
            except KeyError:
                continue
        return score
