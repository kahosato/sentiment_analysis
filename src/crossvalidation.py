import random

from signtest import compute_significance_two_tails
from tokeniser import Tokeniser


def crossvalidation(dataset, classifier, params={}, fold=10):
    class_count = len(dataset)
    datas = [(list(Tokeniser.tokenise(data)), label) for label in xrange(0, len(dataset)) for data in dataset[label]]
    random.shuffle(datas)
    one_fold_length = len(datas) / fold
    fold_with_extra = len(datas) % fold
    classification_rate = [0] * fold
    start = 0
    for i in xrange(0, fold):
        classifier.reset()
        if i < fold_with_extra:
            last = start + one_fold_length + 1
        else:
            last = start + one_fold_length
        test_set = datas[start:last]
        train_set = datas[0:start] + datas[last:]
        if params:
            classifier.train(train_set, class_count, params)
        else:
            classifier.train(train_set, class_count)
        print "{}th fold training over".format(i)
        correct = len(filter(lambda (data, label): classifier.classify(data, params=params) == label, test_set))
        classification_rate[i] = correct / float(len(test_set))
        start = last
        print "{}th fold over".format(i)
    return classification_rate


def crossvalidation_compare(dataset, method1_disc, classifier_1, params_1, method2_disc, classifier_2, params_2, fold=10):
    class_count = len(dataset)
    datas = [(list(Tokeniser.tokenise(data)), label) for label in xrange(0, len(dataset)) for data in dataset[label]]
    random.shuffle(datas)
    one_fold_length = len(datas) / fold
    fold_with_extra = len(datas) % fold
    classification_rate_1 = [0] * fold
    classification_rate_2 = [0] * fold
    significance = [0] * fold
    start = 0
    for i in xrange(0, fold):
        win_1 = 0
        win_2 = 0
        correct_1 = 0
        correct_2 = 0
        classifier_1.reset()
        classifier_2.reset()
        if i < fold_with_extra:
            last = start + one_fold_length + 1
        else:
            last = start + one_fold_length
        test_set = datas[start:last]
        train_set = datas[0:start] + datas[last:]
        classifier_1.train(train_set, class_count, params_1)
        classifier_2.train(train_set, class_count, params_2)
        result = []
        for data, expected in test_set:
            result.append(
                (expected, classifier_1.classify(data, params=params_1), classifier_2.classify(data, params=params_2)))
        for expected, r_1, r_2 in result:
            par = r_1 == r_2
            if par:
                win_1 += 0.5
                win_2 += 0.5
            if expected == r_1:
                correct_1 += 1
                if not par:
                    win_1 += 1
            if expected == r_2:
                correct_2 += 1
                if not par:
                    win_2 += 1
        classification_rate_1[i] = float(correct_1) / len(test_set)
        classification_rate_2[i] = float(correct_2) / len(test_set)
        win_1 = int(round(win_1))
        win_2 = int(round(win_2))
        significance[i] = compute_significance_two_tails(win_1, win_1 + win_2)

    result = ""
    result += "{} CR: {}".format(method1_disc, classification_rate_1)
    result += "{} CR: {}".format(method2_disc, classification_rate_2)
    result += "Sig {}".format(significance)
    result += "\n\n"

    return result