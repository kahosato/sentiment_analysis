import os
import time

import spacy

from crossvalidation import crossvalidation_compare_proper
from naive_bayes_neg import NaiveBayesNeg
from negation import compute_neg_punc, compute_neg_direct_dep, compute_neg_obj, compute_neg_after_x
from symbolic_neg import compute_negation_terms
from tokeniser import Tokeniser

pos_path = os.path.abspath("../data/POS")
pos_files = [os.path.join(pos_path, f) for f in os.listdir(pos_path)]
neg_path = os.path.abspath("../data/NEG")
neg_files = [os.path.join(neg_path, f) for f in os.listdir(neg_path)]
dataset = [pos_files, neg_files]

# list of (tokens, label), where label are either 0:positive or 1:negative
datas = [(list(Tokeniser.tokenise(data)), label) for label in xrange(0, 2) for data in dataset[label]]

# load spacy language model, used to compute dependency structures
nlp = spacy.load('en')
print "spacy loaded"

# TODO rename methods as they are called in the report
methods = [(compute_neg_punc, [], "punc"), (compute_neg_direct_dep, [nlp], "nlp_flip_dep_1"),
           (compute_neg_obj, [nlp], "nlp_flip_dep_obj")]
for i in xrange(1, 6, 2):
    methods += [(compute_neg_after_x, [i], "x {}".format(i))]

#
negation_terms = compute_negation_terms()

with open("NB_result{}.txt".format(time.time()), 'w+') as f:
    # baseline
    # TODO refactor symbolic approach to have train/classify interface

    # symbolic
    # TODO
    params_nb_baseline = {"smooth": 0.2, "neg_scope": lambda x, y: [False] * len(x), "scope_arg": [],
                          "neg_words": negation_terms, "augment": False}
    # NB + simple negation
    for m in methods:
        print "Running with simple negation: {}".format(m[2])
        params = {"smooth": 0.2, "neg_scope": m[0], "scope_arg": m[1], "neg_words": negation_terms, "augment": False}
        f.write(
            crossvalidation_compare_proper(datas, 2, "baseline", NaiveBayesNeg(), params_nb_baseline, m[2] + "_simple",
                                           NaiveBayesNeg(), params, 10))
    # NB + augmented negation
    for m in methods:
        print "Running with augmented nagation: {}".format(m[2])
        params = {"smooth": 0.2, "neg_scope": m[0], "scope_arg": m[1], "neg_words": negation_terms, "augment": True}
        f.write(crossvalidation_compare_proper(datas, 2, "baseline", NaiveBayesNeg(), params_nb_baseline,
                                               m[2] + "_augmented",
                                               NaiveBayesNeg(), params, 10))
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
