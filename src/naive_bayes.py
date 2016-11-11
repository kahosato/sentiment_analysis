import numpy as np

from tokeniser import Tokeniser


class NaiveBayes:
    def __init__(self, all_docs):
        # p(c) -> count of documents classified as c / all docs
        # p(f|c) -> count of f in document c / total words in the document classified as c
        # index of each word - list
        count_docs = map(len, all_docs)
        total_class = len(all_docs)
        total_docs = sum(count_docs)
        p_c = map(lambda x: x / total_docs, count_docs)
        # array of array of counts
        # count_words[word_index] = frequency in each class
        count_words = []
        # word -> index
        word_indexes = {}
        # total words per class
        total_tokens = [0] * total_class
        new_index = 0
        for i in xrange(0, total_class):
            for file in all_docs[i]:
                tokens = Tokeniser.tokenise(file)
                for token in tokens:
                    index = 0
                    try:
                        index = word_indexes[token]
                    except KeyError:
                        index = new_index
                        word_indexes[token] = index
                        count_words.append([0] * total_class)
                        new_index += 1
                    count_words[index][i] += 1
                    total_tokens[i] += 1
        for count_word in count_words:
            for i in xrange(0, total_class):
                count_word[i] /= total_tokens[i]
        self.count_docs = count_docs
        self.total_class = total_class
        self.word_indexes = word_indexes
        self.total_tokens = total_tokens
        self.vocab_size = len(word_indexes)
        self.p_c = p_c
        self.p_f_c = count_words

    def classify(self, file):
        tokens = Tokeniser.tokenise(file)
        best_prob = 0
        best_class = 0
        for i in xrange(0, self.total_class):
            prob = 1
            for token in tokens:
                try:
                    word_index = self.word_indexes[token]
                    prob *= self.p_f_c[word_index][i]
                except KeyError:
                    # todo, smoothing
                    pass
            prob *= self.p_c[i]
            if prob > best_prob:
                best_class = i
                best_prob = prob
        return best_class
    # p(c) -> count of documents classified as c / all docs
    # p(f|c) -> count of f in document c / total words in the document classified as c


