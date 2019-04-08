import pandas as pd
import numpy as np

from umap import UMAP


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
