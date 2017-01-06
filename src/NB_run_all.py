import os
import time

import spacy
from stemming.porter2 import stem

from crossvalidation import crossvalidation_compare, crossvalidation_compare_proper
from naive_bayes import NaiveBayes
from naive_bayes_neg import NaiveBayesNeg
from negation import compute_neg_punc, compute_neg_direct_dep, compute_neg_obj, compute_neg_after_x
from symbolic_neg import compute_negation_list
from tokeniser import Tokeniser
from tokens import WordToken

pos_path = os.path.abspath("../data/POS")
pos_files = [os.path.join(pos_path, f) for f in os.listdir(pos_path)]
neg_path = os.path.abspath("../data/NEG")
neg_files = [os.path.join(neg_path, f) for f in os.listdir(neg_path)]
dataset = [pos_files, neg_files]
datas = [(list(Tokeniser.tokenise(data)), label) for label in xrange(0, 2) for data in dataset[label]]

nlp = spacy.load('en')
print "loaded"
# methods = ["punc", "noneg", "nlp_flip_dep_1", "nlp_flip_dep_obj"]

# result = crossvalidation.crossvalidation([pos_files, neg_files], NaiveBayes(), params={"smooth": 0.2, "neg_scope": compute_neg_obj, "scope_arg": [nlp], "neg_words":compute_negation_list()})
methods = [(compute_neg_punc, [], "punc"), (compute_neg_direct_dep, [nlp], "nlp_flip_dep_1"),
           (compute_neg_obj, [nlp], "nlp_flip_dep_obj")]
for i in xrange(1, 6):
    methods += [(compute_neg_after_x, [i], "x {}".format(i))]

comb = [((m[0], m[1], m[2]+"_stop", True, False), (m[0], m[1], m[2], True, False)) for m in methods]

neg_words = compute_negation_list()
with open("NB_result{}.txt".format(time.time()r), 'w+') as f:
    for c in comb:
        print c[0][2]
        print c[1][2]
        params_1 = {"smooth": 0.2, "neg_scope": c[0][0], "scope_arg": c[0][1], "neg_words": neg_words, "augment": c[0][3], "stemmed": c[0][4], "stopwords": True}
        params_2 = {"smooth": 0.2, "neg_scope": c[1][0], "scope_arg": c[1][1], "neg_words": neg_words, "augment": c[1][3], "stemmed": c[1][4], "stopwords": False}
        f.write(crossvalidation_compare_proper(datas, 2, c[0][2], NaiveBayesNeg(), params_1,
                                        c[1][2], NaiveBayesNeg(), params_2, 10))
    # for m in methods:
    #     print "baseline"
    #     print m[2]
    #     params_1 = {"smooth": 0.2, "neg_scope": lambda x, y: [False] * len(x),
    #                                                     "scope_arg": [],
    #                                                     "neg_words": compute_negation_list(), "stemmed": False,
    #                                                     "augment": False, "stopwords": True}
    #     params_2 = {"smooth": 0.2, "neg_scope": m[0], "scope_arg": m[1], "neg_words": neg_words, "augment": False, "stemmed": False, "stopwords": True}
    #     f.write(crossvalidation_compare_proper(datas, 2, "baseline-noaungment-stopwords", NaiveBayesNeg(), params_1,
    #                                     m[2], NaiveBayesNeg(), params_2, 10))
    # for m in methods:
    #     print "augment"
    #     print "baseline"
    #     print m[2]
    #     params_1 = {"smooth": 0.2, "neg_scope": lambda x, y: [False] * len(x),
    #                                                     "scope_arg": [],
    #                                                     "neg_words": compute_negation_list(), "stemmed": False,
    #                                                     "augment": False, "stopwords": True}
    #     params_2 = {"smooth": 0.2, "neg_scope": m[0], "scope_arg": m[1], "neg_words": neg_words, "augment": True, "stemmed": False, "stopwords": True}
    #     f.write(crossvalidation_compare_proper(datas, 2, "baseline-aungment-stopwords", NaiveBayesNeg(), params_1,
    #                                     m[2], NaiveBayesNeg(), params_2, 10))
