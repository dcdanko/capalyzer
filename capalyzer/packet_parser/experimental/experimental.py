import pandas as pd
import numpy as np

from umap import UMAP
from sklearn.decomposition import PCA

from ..normalize import proportions

def umap(mytbl, **kwargs):
    """Retrun a Pandas dataframe with UMAP, make a few basic default decisions."""
    metric = 'jaccard'
    if mytbl.shape[0] == mytbl.shape[1]:
        metric = 'precomputed'
    n_comp = kwargs.get('n_components', 2)
    umap_tbl = pd.DataFrame(UMAP(
        n_neighbors=kwargs.get('n_neighbors', min(100, int(mytbl.shape[0] / 4))),
        n_components=n_comp,
        metric=kwargs.get('metric', metric),
        random_state=kwargs.get('random_state', 42)
    ).fit_transform(mytbl))
    umap_tbl.index = mytbl.index
    umap_tbl = umap_tbl.rename(columns={i: f'C{i}' for i in range(n_comp)})
    return umap_tbl


def fractal_dimension(tbl, scales=range(1, 10)):
    """Return a box-method curve used to estimate fractal dimension."""
    ranges = pd.DataFrame({
        'min': tbl.min(),
        'max': tbl.max(),
        'width': tbl.max() - tbl.min()
    })
    ranges = ranges.query('width > 0').T
    tbl = tbl[ranges.columns]
    print(ranges)
    Ns = []
    for scale in scales:
        bins = [
            np.arange(
                ranges[col_name]['min'],
                ranges[col_name]['max'] + 0.00001,
                ranges[col_name]['width'] / scale
            )
            for col_name in tbl.columns
        ]
        try:
            H, _ = np.histogramdd(tbl.values, bins=bins)
            Ns.append(np.sum(H > 0))
        except MemoryError:
            break
    return list(zip(scales, Ns))


def subsample_row(row, n):
    pvals = row.values
    pvals /= sum(pvals)
    vals = np.random.choice(row.index, p=pvals, size=(n,))
    tbl = {val: 0 for val in row.index}
    for val in vals:
        tbl[val] += 1
    tbl = pd.Series(tbl)
    return tbl


def train_validate_split(tbl, train_size):
    train_tbl = tbl.copy(deep=True).apply(
        lambda row: subsample_row(row, int(row.sum() * train_size)),
        axis=1
    ).fillna(0)
    val_tbl = (tbl - train_tbl).copy(deep=True)
    val_tbl = val_tbl.applymap(lambda el: 0 if el < 0 else el)
    return train_tbl, val_tbl


def run_pca(tbl, n_comp, zero_thresh):
    pca = PCA(n_components=n_comp)
    tbl_pca = pca.fit_transform(tbl)
    tbl_rev = pd.DataFrame(pca.inverse_transform(tbl_pca))
    tbl_rev.index = tbl.index
    tbl_rev.columns = tbl.columns
    tbl_rev = tbl_rev.applymap(lambda el: el if el > zero_thresh else 0)
    return tbl_rev


def pca_sample_cross_val(tbl,
                         train_size=0.9, min_comp=1, max_comp=100,
                         comp_step=1, decimals=5, zero_thresh=0.001,
                         transformer=lambda el: el, losses=[]):
    """Return a PCA normalized table based on molecular cross validation.

    Works by splitting each sample into train/validate subsets. Performs PCA
    on train then measures difference of INVPCA to validate. Returns the
    table normalized with the number of components minimizing loss.
    """
    max_comp = min(max_comp, tbl.shape[0])
    train_tbl, val_tbl = train_validate_split(tbl, train_size)
    val_prop = transformer(proportions(val_tbl))
    for i in range(min_comp, max_comp + 1, comp_step):
        predict = transformer(proportions(run_pca(train_tbl, i, zero_thresh)))
        loss = np.linalg.norm(val_prop.values - predict)
        loss = np.round(loss, decimals=decimals)
        losses.append((i, loss))
    losses.sort(key=lambda el: el[0])
    losses.sort(key=lambda el: el[1])
    return run_pca(tbl, losses[0][0], zero_thresh)
