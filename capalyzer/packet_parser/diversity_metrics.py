
import math

from scipy.stats import gmean, entropy
from numpy.linalg import norm
import numpy as np

# ALPHA Diversity`


def shannon_entropy(row):
    """Return the shannon entropy of an iterable."""
    H = 0
    for val in row:
        if val == 0:
            continue
        H += val * math.log2(val)
    if H < 0:
        H *= -1
    return H


def richness(row):
    """Return the richness of an iterable."""
    R = 0
    for val in row:
        if val > 0:
            R += 1
    return R


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
