import os

import crossvalidation
from tokeniser import Tokeniser


class NaiveBayes(object):
    __smooth_constant = 1

    # todo: training_docs
    def train(self, training_docs, classes_count, params={"smooth": 1}):
        """all_docs: all_docs[class_index] = array of paths to a document classified as class_index"""
        self.__smooth_constant = params["smooth"]
        # p(c) -> count of documents classified as c / all docs
        # p(f|c) ->
        # count of f in document c + smooth
        # / total tokens in the document classified as c + (vocab in class c + unseen_vocab) * smooth
        # As we keep vocabulary for each class separate, have an array of dictionaries
        # vocabs[class][word] = frequency of word in the class
        count_docs_per_class = [0] * classes_count
        total_docs = len(training_docs)

        # total tokens per class
        total_tokens = [0] * classes_count

        # Array of vocabularies for each class
        vocabs = [{}] * classes_count

        # Array of vocabulary size for each class
        vocab_sizes = [0] * classes_count

        # populate
        # total_tokens[i] - increment for each token
        # vocabs[i][token] - 1 if unseen, increment if seen
        # vocab_sizes - increment for each unseen token
        for file, label in training_docs:
            vocab = vocabs[label]
            count_docs_per_class[label] += 1
            tokens = Tokeniser.tokenise(file)
            for token in tokens:
                freq_so_far = 0
                try:
                    freq_so_far = vocab[token]
                except KeyError:
                    vocab_sizes[label] += 1
                vocab[token] = freq_so_far + 1
                total_tokens[label] += 1
        p_c = map(lambda x: x / total_docs, count_docs_per_class)

        self.total_tokens = total_tokens
        self.vocabs = vocabs
        self.vocab_sizes = vocab_sizes
        self.classes_count = classes_count
        self.p_c = p_c

    def __init__(self):
        self.total_tokens = []
        self.vocabs = []
        self.vocab_sizes = []
        self.classes_count = 0
        self.p_c = []

    def reset(self):
        self.total_tokens = []
        self.vocabs = []
        self.vocab_sizes = []
        self.classes_count = 0
        self.p_c = []

    def classify(self, file):
        tokens = list(Tokeniser.tokenise(file))
        best_prob = 0
        best_class = 0
        # token -> frequency in file
        vocabs_in_file = {}
        # how many unseen
        unseen_vocabs_count = [0] * self.classes_count
        # count unseen words
        for token in tokens:
            # if we have seen this before in this document, increment frequency
            try:
                vocabs_in_file[token] += 1
            # if we haven't, then
            # - initialise its frequency in this document to 1
            # - check if it was seen in a document of class i. If not then increment unseen_vocabs_count[i]
            except KeyError:
                vocabs_in_file[token] = 1
                for i in xrange(0, self.classes_count):
                    if token not in self.vocabs[i]:
                        unseen_vocabs_count[i] += 1
        for i in xrange(0, self.classes_count):
            prob = self.p_c[i]
            w = self.vocab_sizes[i] + unseen_vocabs_count[i]
            for token in tokens:
                try:
                    freq_in_c = self.vocabs[i][token]
                except KeyError:
                    freq_in_c = 0
                # p(f|c) ->
                # count of f in document c + smooth
                # / total tokens in the document classified as c + (vocab in class c + unseen_vocab) * smooth
                prob *= (freq_in_c + self.__smooth_constant) \
                        / float(self.total_tokens[i] + self.__smooth_constant * w)
            if prob > best_prob:
                best_class = i
                best_prob = prob
        return best_class


if __name__ == "__main__":
    pos_path = os.path.abspath("../data/POS")
    pos_files = [os.path.join(pos_path, f) for f in os.listdir(pos_path)]
    neg_path = os.path.abspath("../data/NEG")
    neg_files = [os.path.join(neg_path, f) for f in os.listdir(neg_path)]
    print crossvalidation.crossvalidation([pos_files, neg_files], NaiveBayes())
    # print crossvalidation.crossvalidation([pos_files[:10], neg_files[:10]], NaiveBayes())
