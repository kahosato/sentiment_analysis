import Queue

import time

import spacy
from nltk import Tree
from nltk.parse.stanford import StanfordDependencyParser
from spacy.symbols import ccomp, dobj, acomp

from tokens import PunctuationToken, TokenFactory


def compute_neg_punc(tokens, neg_words):
    negated = False
    neg_array = []
    for token in tokens:
        if isinstance(token, PunctuationToken):
            neg_array.append(False)
            negated = False
        elif token.value in neg_words:
            neg_array.append(False)
            negated = not negated
        else:
            neg_array.append(negated)
    return neg_array


def compute_neg_after_x(tokens, neg_words, scope_size):
    negated = False
    neg_array = []
    scope_index = 0
    for token in tokens:
        if token.value in [".", "?", "!"]:
            neg_array.append(False)
            scope_index = 0
            negated = False
        elif token.value in neg_words:
            neg_array.append(False)
            negated = True
            scope_index = 0
        else:
            if negated and scope_index < scope_size:
                neg_array.append(True)
            else:
                neg_array.append(False)
            if negated:
                scope_index += 1
                if scope_index >= scope_size:
                    negated = False
                    scope_index = 0
    return neg_array


def compute_neg_dir_dep(tokens, neg_words, nlp):
    # [0.82, 0.78, 0.79, 0.795, 0.755, 0.8, 0.8, 0.795, 0.775, 0.795]
    # 0.7905
    sentence = []
    neg_array = []
    negated = set()
    old_tokenizer = nlp.tokenizer
    u_tokens = lambda x: map(lambda t: unicode(t.value, "utf-8"), tokens)
    nlp.tokenizer = lambda ts: old_tokenizer.tokens_from_list(u_tokens(ts))
    text = unicode(" ".join(map(lambda t: t.value, tokens)), "utf-8")
    doc = nlp(text)
    for w in doc:
        if w.text in neg_words:
            negated.add(w.head.i)
    for j in xrange(0, len(tokens)):
        neg_array.append(j in negated)
    nlp.tokenizer = old_tokenizer
    return neg_array


if __name__ == "__main__":
    tokens = map(TokenFactory.create, "I do not have any idea and I am not alright .".split(" "))
    print tokens
    print compute_neg_dir_dep(tokens, ["not", "any"])
    dep_parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    # parse
    tree = next(dep_parser.parse("I do not have any idea and I am not alright.".split(" "))).tree()
    # Can't deal with the duplicate because the dependency graph does not label each token
    negated = []
    parent = tree.label()
    queue = Queue.Queue()
    queue.put((parent, tree))
    while not queue.empty():
        elem = queue.get()
        print elem
        parent, current = elem
        if isinstance(current, Tree):
            label = current.label()
            for c in current:
                queue.put((label, c))
        else:
            label = current
        if label in ["not", "any"]:
            negated.append(parent)
    print negated


def compute_neg_head_obj(tokens, neg_words, nlp):
    sentence = []
    neg_array = []
    negated = set()
    old_tokenizer = nlp.tokenizer
    u_tokens = lambda x: map(lambda t: unicode(t.value, "utf-8"), tokens)
    nlp.tokenizer = lambda ts: old_tokenizer.tokens_from_list(u_tokens(ts))
    text = unicode(" ".join(map(lambda t: t.value, tokens)), "utf-8")
    doc = nlp(text)
    for w in doc:
        if w.text in neg_words:
            negated.add(w.head.i)
            for c in w.head.children:
                if is_complement(c.dep):
                    for c_dec in c.subtree:
                        negated.add(c_dec.i)
    for j in xrange(0, len(tokens)):
        neg_array.append(j in negated)
    nlp.tokenizer = old_tokenizer
    return neg_array


def is_complement(dep):
    return dep in {ccomp, dobj, acomp}