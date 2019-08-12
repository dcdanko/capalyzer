import pandas as pd

from numpy.random import choice


def proportions(tbl):
    tbl = (tbl.T / tbl.T.sum()).T
    return tbl


def subsample_row(row, n):
    pvals = row.values
    pvals /= sum(pvals)
    vals = choice(row.index, p=pvals, size=(n,))
    tbl = {}
    for val in vals:
        tbl[val] = 1 + tbl.get(val, 0)
    tbl = pd.Series(tbl)
    return tbl


def subsample(tbl, n=-1, niter=1):
    if n <= 0:
        n = int(tbl.T.sum().min())
    tbl = pd.concat([
        tbl.apply(lambda row: subsample_row(row, n), axis=1).fillna(0)
        for _ in range(niter)
    ])
    tbl = proportions(tbl)
    return tbl
