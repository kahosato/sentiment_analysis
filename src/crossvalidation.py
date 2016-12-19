import random

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
        correct = len(filter(lambda (data, label): classifier.classify(data, params=params) == label, test_set))
        classification_rate[i] = correct / float(len(test_set))
        start = last
    return classification_rate
