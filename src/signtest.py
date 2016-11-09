import operator as op


# takes two values, count_event1, count_total, p value and returns true if we reject null hypothesis

def reject_null_hypothesis_two_tails(success, total, p):
    return compute_significance_two_tails(success, total) < p


def compute_significance_two_tails(success, total):
    const = pow(0.5, total)
    if success > (total / 2):
        success = total - success
    return sum(map(lambda i : ncr(total, i) * const, xrange(0, success+1))) * 2


def ncr(n, r):
    r = min(r, n - r)
    if r == 0: return 1
    numer = reduce(op.mul, xrange(n, n - r, -1))
    denom = reduce(op.mul, xrange(1, r + 1), 1)
    return numer / denom
