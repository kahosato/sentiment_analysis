# separate
import random


# train classifier
def crossvalidation(dataset, classifier, params={}, fold=10):
    class_count = len(dataset)
    datas = [(data, label) for label in xrange(0, len(dataset)) for data in dataset[label]]
    random.shuffle(datas)
    print len(datas)
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
        correct = len(filter(lambda (data, label): classifier.classify(data) == label, test_set))
        print len(test_set)
        classification_rate[i] = correct / float(len(test_set))
        # correct = 0
        # for test in test_set:
        #     file, label = test
        #     classification = classifier.classify(file)
        #     if classification == label:
        #         correct += 1
        start = last
    return classification_rate
