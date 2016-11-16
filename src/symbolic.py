import os

from signtest import compute_significance_two_tails
from tokeniser import Tokeniser


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


class SymbolicScore(object):
    def __init__(self):
        pass

    @staticmethod
    def compute_binary(tokens, lexicon):
        score = 0
        for token in tokens:
            try:
                entry = lexicon[token.value]
                score += entry.sentiment_score
            except KeyError:
                continue
        return score

    @staticmethod
    def compute_weighted(tokens, lexicon):
        score = 0
        for token in tokens:
            try:
                entry = lexicon[token.value]
                score += entry.sentiment_score * entry.weight
            except KeyError:
                continue
        return score


if __name__ == "__main__":
    lex = LexiconGenerator.generate(os.path.abspath("../resources/sent_lexicon"))
    pos_path = os.path.abspath("../data/POS")
    pos_files = [os.path.join(pos_path, f) for f in os.listdir(pos_path)]
    bin_win = 0
    wei_win = 0
    bin_correct = 0
    wei_correct = 0
    for pos_file in pos_files:
        # files not too long + use twice, so compute list
        tokens = list(Tokeniser.tokenise(pos_file))
        bin_score = SymbolicScore.compute_binary(tokens, lex)
        wei_score = SymbolicScore.compute_weighted(tokens, lex)
        if bin_score >= 0: bin_correct += 1
        if wei_score >= 0: wei_correct += 1
        # 0 : positive
        # bin: positive, wei: negative
        if bin_score >= 0 > wei_score:
            bin_win += 1
        # bin: positive, wei: negative
        elif bin_score < 0 <= wei_score:
            wei_win += 1
        else:
            bin_win += 0.5
            wei_win += 0.5
    neg_path = os.path.abspath("../data/NEG")
    neg_files = [os.path.join(neg_path, f) for f in os.listdir(neg_path)]
    for neg_file in neg_files:
        # files not too long + use twice, so compute list
        tokens = list(Tokeniser.tokenise(neg_file))
        bin_score = SymbolicScore.compute_binary(tokens, lex)
        wei_score = SymbolicScore.compute_weighted(tokens, lex)
        if bin_score < 0: bin_correct += 1
        if wei_score < 0: wei_correct += 1
        # bin: positive, wei: negative
        if bin_score >= 0 > wei_score:
            wei_win += 1
        # bin: positive, wei: negative
        elif bin_score < 0 <= wei_score:
            bin_win += 1
        else:
            bin_win += 0.5
            wei_win += 0.5
    print "bin_sin: {}".format(bin_win)
    print "wei_win: {}".format(wei_win)
    print "bin got: {} cases right".format(bin_correct)
    print "wei got: {} cases right".format(wei_correct)
    bin_win = int(round(bin_win))
    wei_win = int(round(wei_win))
    print "significance: {}".format(compute_significance_two_tails(wei_win, bin_win + wei_win))
