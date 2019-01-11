
import math

from scipy.stats import gmean, entropy
from numpy.linalg import norm
from random import random

import numpy as np

MIL = 1000 * 1000

# ALPHA Diversity`

def shannon_entropy(row, rarefy=0):
    """Return the shannon entropy of an iterable.

    Shannon entropy is robust to rarefaction but we keep
    the param for consistency.
    """
    row_sum, H = sum(row), 0
    for val in row:
        val = val / row_sum
        if val == 0:
            continue
        H += val * math.log2(val)
    if H < 0:
        H *= -1
    return H


def richness(row, rarefy=0):
    """Return the richness of an iterable."""
    row_sum, R = sum(row), 0
    for val in row:
        pi = val / row_sum
        pr_no_detect = 1 - (1 - pi) ** rarefy
        if val and (rarefy <= 0 or random() > pr_no_detect):
            R += 1
    return R


def chao1(row, rarefy=0):
    """Return richnes of an iterable"""
    row_sum, R, S, D = sum(row), 0, 0, 0.0000001
    num_reads = MIL if math.isclose(row_sum, 1) else row_sum  # default to 1M reads if compositional
    num_reads = rarefy if rarefy > 0 else num_reads  # if rarefy is set use that as read count

    for val in row:
        pi = val / row_sum
        pr_no_detect = 1 - (1 - pi) ** num_reads
        pr_singleton = num_reads * pi * (1 - pi) ** (num_reads - 1)
        pr_doublet = (num_reads * (num_reads - 1) / 2) * (pi ** 2) * ((1 - pi) ** num_reads - 2)

        rand = random()
        R += 1 if rand > pr_no_detect else 0
        if pr_no_detect < rand < (pr_no_detect + pr_singleton):
            S += 1
        elif rand < (pr_no_detect + pr_singleton + pr_doublet):
            D += 2
    return R + (S ** 2 / D)



# Beta Diversity


def clr(X):
    _X = X + 0.0000001
    _X = _X / norm(_X, ord=1)
    g = gmean(_X)
    _X = np.divide(_X, g)
    _X = np.log(_X)
    return _X


def rho_proportionality(P, Q):
    _P, _Q = clr(P), clr(Q)
    N = np.var(_P - _Q)
    D = np.var(_P) + np.var(_Q)
    return 1 - (N / D)


def jensen_shannon_dist(P, Q):
    _P = P / norm(P, ord=1)
    _Q = Q / norm(Q, ord=1)
    _M = 0.5 * (_P + _Q)
    J = 0.5 * (entropy(_P, _M) + entropy(_Q, _M))
    return math.sqrt(J)
