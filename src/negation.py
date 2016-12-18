import Queue

import time
from nltk import Tree
from nltk.parse.stanford import StanfordDependencyParser

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
        if token == PunctuationToken("."):
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


def compute_neg_direct_dep(tokens, neg_words):
    dep_parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    sentence = []
    neg_array = []
    sentences = []
    for token in tokens:
        sentence.append(token.value)
        if token == PunctuationToken("."):
            sentences.append(sentence)
            sentence = []
    print len(tokens)
    print len(sentences)
    start = time.time()
    trees = map(lambda t: next(t).tree(), dep_parser.parse_sents(sentences[:50]))
    print time.time() - start
    assert len(trees) == len(sentences)
    for i in xrange(0, len(sentences)):
        tree = trees[i]
        sentence = sentences[i]
        negated = []
        parent = tree.label()
        queue = Queue.Queue()
        queue.put((parent, tree))
        while not queue.empty():
            parent, current = queue.get()
            if isinstance(current, Tree):
                label = current.label()
                for c in current:
                    queue.put((label, c))
            else:
                label = current
            if label in neg_words:
                negated.append(parent)
        for word in sentence:
            neg_array.append(word.value in negated)
    return neg_array


if __name__ == "__main__":
    tokens = map(TokenFactory.create, "I do not have any idea and I am not alright .".split(" "))
    print tokens
    print compute_neg_direct_dep(tokens, ["not", "any"])
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
