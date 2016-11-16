# separate
import random


# train classifier
def crossvalidation(dataset, classifier, params={}, fold=10):
    class_count = len(dataset)
    datas = [(data, label) for label in xrange(0, len(dataset)) for data in dataset[label]]
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
        test_set = datas[start:last + 1]
        train_set = datas[0:start] + datas[last + 1:]
        if params:
            classifier = classifier.train(train_set, params)
        else:
            classifier = classifier.train(train_set)
        correct = len(filter(lambda (data, label): classifier.classify(data) == label, test_set))
        classification_rate[i] = correct / float(len(test_set))
        # correct = 0
        # for test in test_set:
        #     file, label = test
        #     classification = classifier.classify(file)
        #     if classification == label:
        #         correct += 1
        start = last + 1
    return classification_rate
