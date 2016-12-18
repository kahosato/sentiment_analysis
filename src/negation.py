from tokens import PunctuationToken


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