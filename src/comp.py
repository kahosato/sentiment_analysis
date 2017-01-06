import os
import random

from naive_bayes import NaiveBayes
from signtest import compute_significance_two_tails
from symbolic import SymbolicScore, LexiconGenerator
from tokeniser import Tokeniser

if __name__ == "__main__":
    classifier = NaiveBayes()
    pos_path = os.path.abspath("../data/POS")
    pos_files = [os.path.join(pos_path, f) for f in os.listdir(pos_path)]
    neg_path = os.path.abspath("../data/NEG")
    neg_files = [os.path.join(neg_path, f) for f in os.listdir(neg_path)]
    dataset = [pos_files, neg_files]
    fold = 10
    class_count = len(dataset)
    datas = [(list(Tokeniser.tokenise(data)), label) for label in xrange(0, len(dataset)) for data in dataset[label]]
    random.shuffle(datas)
    one_fold_length = len(datas) / fold
    fold_with_extra = len(datas) % fold
    classification_rate = [0] * fold
    start = 0
    lex = LexiconGenerator.generate(os.path.abspath("../resources/sent_lexicon"))
    nb_win_bin = 0
    nb_win_wei = 0
    bin_win = 0
    wei_win = 0
    for i in xrange(0, fold):
        classifier.reset()
        if i < fold_with_extra:
            last = start + one_fold_length + 1
        else:
            last = start + one_fold_length
        test_set = datas[start:last]
        train_set = datas[0:start] + datas[last:]
        classifier.train(train_set, class_count, params={"smooth": 0})
        for data, label in test_set:
            nb_result = classifier.classify(data)
            if SymbolicScore.compute(data, lex, bin=True, stemmed=False) >= 0:
                bin_result = 0
            else:
                bin_result = 1
            if SymbolicScore.compute(data, lex, bin=False, stemmed=False) >= 0:
                win_result = 0
            else:
                win_result = 1
            print (label, nb_result, bin_result, win_result)
            if label == nb_result and label != bin_result:
                nb_win_bin += 1
            if label != nb_result and label == bin_result:
                bin_win += 1
            if label == nb_result and label != win_result:
                nb_win_wei += 1
            if label != nb_result and label == win_result:
                wei_win += 1
        start = last
    print nb_win_bin
    print nb_win_wei
    print bin_win
    print wei_win
    print "significance wei: {}".format(compute_significance_two_tails(wei_win, nb_win_wei + wei_win))
    print "significance bin: {}".format(compute_significance_two_tails(bin_win, bin_win + nb_win_bin))
