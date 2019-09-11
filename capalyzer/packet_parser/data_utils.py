

def group_small_cols(tbl, top=9, other_name='other', stat='mean'):
    """Return a table where all columns not in the <top> most abundant are pooled.

    Useful for visualization.
    """
    if stat in ['mean', 'ave', 'average']:
        vals = tbl.mean()
    elif stat in ['median']:
        vals = tbl.median()
    top_cols = list(vals.sort_values(ascending=False)[:top].index)
    other_cols = [col for col in tbl.columns if col not in top_cols]
    tbl[other_name] = tbl[other_cols].sum(axis=1)
    tbl = tbl.drop(columns=other_cols)
    return tbl
