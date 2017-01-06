import os
import time

import spacy

from crossvalidation import crossvalidation
from naive_bayes_neg import NaiveBayesNeg
from negation import compute_neg_obj, compute_neg_after_x
from symbolic_neg import compute_negation_list
from tokeniser import Tokeniser

pos_path = os.path.abspath("../data/POS")
pos_files = [os.path.join(pos_path, f) for f in os.listdir(pos_path)]
neg_path = os.path.abspath("../data/NEG")
neg_files = [os.path.join(neg_path, f) for f in os.listdir(neg_path)]
dataset = [pos_files, neg_files]
datas = [(list(Tokeniser.tokenise(data)), label) for label in xrange(0, 2) for data in dataset[label]]

nlp = spacy.load('en')
print "loaded"
# methods = ["punc", "noneg", "nlp_flip_dep_1", "nlp_flip_dep_obj"]
#
# methods = [(compute_neg_obj, [nlp], "nlp_flip_dep_obj augment:{} stemmed:{}".format(a, s), a, s) for a in [True, False]
#            for s in
#            [True, False]]
methods = [(compute_neg_after_x, [3], "after 3", False, False)]
neg_words = compute_negation_list()
with open("NB_sing_result{}.txt".format(time.time()), 'w+') as f:
    f.write("smooth=1")
    for m in methods:
        print m[2]
        f.write(crossvalidation(datas, 2, m[2], NaiveBayesNeg(),
                        params={"smooth": 0.2, "neg_scope": m[0], "scope_arg": m[1],
                                "neg_words": compute_negation_list(), "augment": m[3], "stemmed": m[4]}))
