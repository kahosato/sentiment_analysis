from decimal import Decimal

from negation import compute_neg_punc
from symbolic_neg import compute_stopwords_list
from tokens import PunctuationToken, WordToken


# NB with negation - NB without negation can be instantiated from this by giving
# neg_scope: a function that takes an array of tokens, and returns an array of False(as in, not negated),
# whose length is the same as the input array
# scope_arg: []
class NaiveBayesNeg(object):
    __smooth_constant = 1

    # todo: training_docs
    def train(self, training_docs, classes_count, params={"smooth": 0.2, "neg_scope": compute_neg_punc, "bulk": False}):
        """all_docs: all_docs[class_index] = array of paths to a document classified as class_index"""
        self.__smooth_constant = params["smooth"]
        try:
            use_stopwords = params["stopwords"]
        except KeyError:
            use_stopwords = False
        stopwords = compute_stopwords_list()
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
        # [{}] * n create a list with dictionaries of same reference, jeez
        vocabs = [{} for i in xrange(0, classes_count)]

        # Array of vocabulary size for each class
        vocab_sizes = [0] * classes_count

        # populate
        # total_tokens[i] - increment for each token
        # vocabs[i][token] - 1 if unseen, increment if seen
        # vocab_sizes - increment for each unseen token

        for tokens, label in training_docs:
            vocab = vocabs[label]
            count_docs_per_class[label] += 1
            other_label = [l for l in xrange(0, classes_count) if l != label]
            neg_array = params["neg_scope"](tokens, params["neg_words"], *params["scope_arg"])
            assert len(tokens) == len(neg_array)
            for i in xrange(0, len(tokens)):
                token = tokens[i]
                if isinstance(token, PunctuationToken):
                    continue
                if use_stopwords and token.value in stopwords:
                    continue
                negated = neg_array[i]
                if negated:
                    neg_token = token
                    token = WordToken("NOT_{}".format(token.value))
                else:
                    neg_token = WordToken("NOT_{}".format(token.value))
                freq_so_far = 0
                try:
                    freq_so_far = vocab[token]
                except KeyError:
                    vocab_sizes[label] += 1
                vocab[token] = freq_so_far + 1
                total_tokens[label] += 1
                if params["augment"]:
                    for l in other_label:
                        other_vocab = vocabs[l]
                        neg_freq_so_far = 0
                        try:
                            neg_freq_so_far = other_vocab[neg_token]
                        except KeyError:
                            vocab_sizes[l] += 1
                        other_vocab[neg_token] = neg_freq_so_far + 1
                        total_tokens[l] += 1
        p_c = map(lambda x: x / float(total_docs), count_docs_per_class)

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

    def classify(self, tokens, params={"smooth": 0.2, "neg_scope": compute_neg_punc}):
        try:
            use_stopwords = params["stopwords"]
        except KeyError:
            use_stopwords = False
        stopwords = compute_stopwords_list()
        best_prob = 0
        best_class = 0
        # token -> frequency in file
        vocabs_in_file = {}
        # how many unseen
        unseen_vocabs_count = [0] * self.classes_count
        # count unseen words
        neg_array = params["neg_scope"](tokens, params["neg_words"], *params["scope_arg"])
        assert len(neg_array) == len(tokens)

        for j in xrange(0, len(tokens)):
            token = tokens[j]
            if isinstance(token, PunctuationToken):
                continue
            if use_stopwords and token.value in stopwords:
                continue
            if neg_array[j]:
                token = WordToken("NOT_{}".format(token.value))
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
            prob = Decimal(self.p_c[i])
            w = self.vocab_sizes[i] + unseen_vocabs_count[i]
            for j in xrange(0, len(tokens)):
                token = tokens[j]
                if neg_array[j]:
                    token = WordToken("NOT_{}".format(token.value))
                try:
                    freq_in_c = self.vocabs[i][token]
                except KeyError:
                    freq_in_c = 0
                # p(f|c) ->
                # count of f in document c + smooth
                # / total tokens in the document classified as c + (vocab in class c + unseen_vocab) * smooth
                p_f_c = Decimal(
                    (freq_in_c + self.__smooth_constant) / float(self.total_tokens[i] + self.__smooth_constant * w))
                prob *= p_f_c
            if prob > best_prob:
                best_class = i
                best_prob = prob
        return best_class
