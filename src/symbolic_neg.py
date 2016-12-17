import os
import sys

from stemming.porter2 import stem

from signtest import compute_significance_two_tails
from symbolic import LexiconGenerator, SymbolicScore
from tokeniser import Tokeniser
from tokens import PunctuationToken


def compute_negation_list():
    list = []
    with open(os.path.abspath("../data/negation.txt")) as f:
        for word in f:
            list.append(word.rstrip())
    return list


def flip_punc(tokens, lexicon, neg_words, bin=True, stemmed=False):
    score = 0
    negated = False
    neg_array = []
    sentence = []
    for token in tokens:
        sentence.append(token)
        if isinstance(token, PunctuationToken):
            neg_array.append(False)
            if token == PunctuationToken("."):
                score += compute_score_sentence(sentence, neg_array, lexicon, bin, stemmed)
                sentence = []
                neg_array = []
            negated = False
        elif token.value in neg_words:
            neg_array.append(False)
            negated = not negated
        else:
            neg_array.append(negated)
    return score


def flip_prev(tokens, lexicon, neg_words, bin=True, stemmed=False):
    score = 0
    negated = False
    neg_array = []
    sentence = []
    for token in tokens:
        sentence.append(token)
        if token == PunctuationToken("."):
            neg_array.append(False)
            score += compute_score_sentence(sentence, neg_array, lexicon, bin, stemmed)
            neg_array = []
            sentence = []
            negated = False
            continue
        if token.value in neg_words:
            neg_array.append(False)
            negated = True
        else:
            neg_array.append(negated)
            negated = False
    return score


def compute_score_sentence(tokens, neg_array, lexicon, bin, stemmed):
    assert len(tokens) == len(neg_array)
    score = 0
    for i in xrange(len(tokens)):
        token = tokens[i]
        neg_weight = neg_array[i] and -1 or 1
        try:
            entry = lexicon[token.value]
            if bin:
                score += entry.sentiment_score * neg_weight
            else:
                score += entry.sentiment_score * entry.weight * neg_weight
        except KeyError:
            if stemmed:
                try:
                    entry = lexicon[stem(token.value)]
                    if bin:
                        score += entry.sentiment_score * neg_weight
                    else:
                        score += entry.sentiment_score * entry.weight * neg_weight
                except KeyError:
                    continue
    return score


scope_dict = {'punc': flip_punc, 'prev': flip_prev, 'noneg': SymbolicScore.compute}


def compute_score_document(tokens, lex, method, neg_words):
    if method[0] == "noneg":
        return scope_dict[method[0]](tokens, lex, bin=method[1] == "b", stemmed=method[2] == "s")
    else:
        return scope_dict[method[0]](tokens, lex, neg_words, bin=method[1] == "b", stemmed=method[2] == "s")


def gen_pos_tokens():
    pos_path = os.path.abspath("../data/POS")
    pos_files = [os.path.join(pos_path, f) for f in os.listdir(pos_path)]
    return [list(Tokeniser.tokenise(pos_file)) for pos_file in pos_files]


def gen_neg_tokens():
    pos_path = os.path.abspath("../data/NEG")
    pos_files = [os.path.join(pos_path, f) for f in os.listdir(pos_path)]
    return [list(Tokeniser.tokenise(pos_file)) for pos_file in pos_files]


def gen_lex():
    return LexiconGenerator.generate(os.path.abspath("../resources/sent_lexicon"))


def run_experiment(method1_disc, method2_disc, pos_files, neg_files, lex):
    method1 = method1_disc.split(" ")
    method2 = method2_disc.split(" ")
    neg_words = compute_negation_list()
    bin_win = 0
    wei_win = 0
    bin_correct = 0
    wei_correct = 0
    for tokens in pos_files:
        # files not too long + use twice, so compute list
        bin_score = compute_score_document(tokens, lex, method1, neg_words)
        wei_score = compute_score_document(tokens, lex, method2, neg_words)
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
    for tokens in neg_files:
        # files not too long + use twice, so compute list
        bin_score = compute_score_document(tokens, lex, method1, neg_words)
        wei_score = compute_score_document(tokens, lex, method2, neg_words)
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
    result = ""
    result += "{} won: {}\n".format(method1_disc, bin_win)
    result += "{} won: {}\n".format(method2_disc, wei_win)
    result += "method1 got: {} cases right\n".format(bin_correct)
    result += "method2 got: {} cases right\n".format(wei_correct)
    bin_win = int(round(bin_win))
    wei_win = int(round(wei_win))
    result += "significance: {}\n".format(compute_significance_two_tails(wei_win, bin_win + wei_win))
    return result


if __name__ == "__main__":
    method1_disc = sys.argv[1]
    method2_disc = sys.argv[2]
    print run_experiment(method1_disc, method2_disc, gen_pos_tokens(), gen_neg_tokens(), gen_lex())
    # punc
    # punc b ns won: 992.5
    # punc w ns won: 1007.5
    # method1 got: 1332 cases right
    # method2 got: 1347 cases right
    # significance: 0.7543114188928754012459104498

    # prev
    # prev b ns won: 978.0
    # prev w ns won: 1022.0
    # method1 got: 1279 cases right
    # method2 got: 1323 cases right
    # significance: 0.3362977202320874537223706582

    # punc + stem
    # bin_win: 986.0
    # wei_sin: 1014.0
    # bin got: 1322 cases right
    # wei got: 1350 cases right
    # significance: 0.5460282528675881653053042490