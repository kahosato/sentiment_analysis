import time

from symbolic_neg import run_experiment, gen_pos_tokens, gen_neg_tokens, gen_lex

if __name__ == "__main__":
    methods = ["punc", "noneg"]
    bin = ['b', 'w']
    stem = ['s', 'ns']
    exps = ["{} {} {}".format(m, b, s) for m in methods for b in bin for s in stem]
    exps += ["x {} {} {}".format(b, s, c) for b in bin for s in stem for c in xrange(1, 6)]
    comb = [(exps[i], exps[j]) for i in xrange(0, len(exps)) for j in xrange(i+1, len(exps))]
    pos = gen_pos_tokens()
    neg = gen_neg_tokens()
    lex = gen_lex()
    with open("symb_result{}.txt".format(time.time()), 'w+') as f:
        for c in comb:
            f.write(run_experiment(c[0], c[1], pos, neg, lex))
            f.write("\n\n")