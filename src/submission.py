import os
import time

import spacy

from crossvalidation import crossvalidation_compare
from naive_bayes_neg import NaiveBayesNeg
from negation import compute_neg_punc, compute_neg_dir_dep, compute_neg_head_obj, compute_neg_after_x
from symbolic import LexiconGenerator
from symbolic_neg import compute_negation_terms, SymbolicClassifier
from tokeniser import Tokeniser

no_negation = lambda x, y: [False] * len(x)

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
methods = [(compute_neg_punc, [], "punc"), (compute_neg_dir_dep, [nlp], "dir_dep"),
           (compute_neg_head_obj, [nlp], "head_obj")]
for i in xrange(1, 6, 2):
    methods += [(compute_neg_after_x, [i], "after_{}".format(i))]

#
negation_terms = compute_negation_terms()
lexicon = LexiconGenerator.generate(os.path.abspath("../resources/sent_lexicon"))

baselines = [
    ("Binary", SymbolicClassifier(),
     {"bin": True, "lexicon": lexicon, "scope_arg": [], "neg_scope": no_negation, "neg_words": negation_terms}),
    ("Weighted", SymbolicClassifier(),
     {"bin": False, "lexicon": lexicon, "scope_arg": [], "neg_scope": no_negation, "neg_words": negation_terms}),
    ("NB", NaiveBayesNeg(),
     {"smooth": 0.2, "neg_scope": no_negation, "scope_arg": [], "neg_words": negation_terms, "augment": False}),
    ("UNB", NaiveBayesNeg(),
     {"smooth": 0, "neg_scope": no_negation, "scope_arg": [], "neg_words": negation_terms, "augment": False})
]

comb = [(baselines[i], baselines[j]) for i in xrange(0, len(baselines)) for j in xrange(0, i)]
with open("result{}.txt".format(time.time()), 'w+') as f:
    # baseline
    for ((name_1, c_1, param_1), (name_2, c_2, param_2)) in comb:
        print "{} vs {}".format(name_1, name_2)
        f.write(crossvalidation_compare(datas, 2, name_1, c_1, param_1, name_2, c_2, param_2, 10))

    # symbolic bin + negation
    for m in methods:
        print "Symbolic Binary"
        (b_n, b_c, b_p) = baselines[0]
        params = {"bin": True, "lexicon": lexicon, "neg_scope": m[0], "scope_arg": m[1], "neg_words": negation_terms}
        f.write(crossvalidation_compare(datas, 2, b_n, b_c, b_p, m[2], SymbolicClassifier(), params, 10))
    # symbolic weighted + negation
    for m in methods:
        print "Symbolic Binary"
        (b_n, b_c, b_p) = baselines[1]
        params = {"bin": False, "lexicon": lexicon, "neg_scope": m[0], "scope_arg": m[1], "neg_words": negation_terms}
        f.write(crossvalidation_compare(datas, 2, b_n, b_c, b_p, m[2], SymbolicClassifier(), params, 10))

    (b_n, b_c, b_p) = baselines[2]

    params_nb_baseline = {"smooth": 0.2, "neg_scope": lambda x, y: [False] * len(x), "scope_arg": [],
                          "neg_words": negation_terms, "augment": False}
    # NB + simple negation
    for m in methods:
        print "Running with simple negation: {}".format(m[2])
        params = {"smooth": 0.2, "neg_scope": m[0], "scope_arg": m[1], "neg_words": negation_terms, "augment": False}
        f.write(
            crossvalidation_compare(datas, 2, b_n, b_c, b_p, "{}_simple".format(m[2]), NaiveBayesNeg(), params,
                                    10))
    # NB + augmented negation
    for m in methods:
        print "Running with augmented nagation: {}".format(m[2])
        params = {"smooth": 0.2, "neg_scope": m[0], "scope_arg": m[1], "neg_words": negation_terms, "augment": True}
        f.write(crossvalidation_compare(datas, 2, b_n, b_c, b_p, "{}_augmented".format(m[2]), NaiveBayesNeg(),
                                        params, 10))

    # augmented negation vs augmented negation + stoplist
    for m in methods:
        print "Running with augmented nagation: {}".format(m[2])
        params = {"smooth": 0.2, "neg_scope": m[0], "scope_arg": m[1], "neg_words": negation_terms, "augment": True}
        params_2 = {"smooth": 0.2, "neg_scope": m[0], "scope_arg": m[1], "neg_words": negation_terms, "augment": True,
                    "stopwords": True}
        f.write(
            crossvalidation_compare(datas, 2, "{}_augmented_stopwords".format(m[2]), NaiveBayesNeg(), params_2,
                                    "{}_augmented".format(m[2]), NaiveBayesNeg(), params, 10))
