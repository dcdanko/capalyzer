import pandas as pd


def get_sample_name(filename):
    """Extract sample name from filename."""
    return filename.split('/')[-1].split('.')[0]


def tokenize(line):
    tkns = line.split('\t')
    cov = float('nan')
    if tkns[5].lower() != 'na':
        cov = float(tkns[5])
    blank_count = 0
    for char in tkns[8]:
        if char == ' ':
            blank_count += 1
        else:
            break
    return blank_count, {
        'percent': float(tkns[0]),
        'reads': int(tkns[1]),
        'tax_reads': int(tkns[2]),
        'kmers': int(tkns[3]),
        'dup': float(tkns[4]),
        'cov': cov,
        'tax_id': tkns[6],
        'rank': tkns[7],
        'tax_name': tkns[8].strip(),
    }


RANK_MAP = {
    'domain': 'd',
    'superkingdom': 'd',
    'kingdom': 'k',
    'phylum': 'p',
    'class': 'c',
    'order': 'o',
    'family': 'f',
    'genus': 'g',
    'species': 's',
    'strain': 't',
}
def get_mpa_str(node):
    """Return an MPA string to this nodes lineage."""
    code = RANK_MAP.get(node['info']['rank'].lower(), 'x')
    taxa_name = '_'.join(node['info']['tax_name'].split())
    segment = f'{code}__{taxa_name}'
    if node['parent'] and not node['parent']['info']['rank'].lower() in ['no rank', 'no_rank']:
        segment = get_mpa_str(node['parent']) + ';' + segment
    return segment


NODE_MAP = {}
def get_node(parent, sample_name, depth, tkns):
    tax_id = tkns['tax_id']
    try:
        node = NODE_MAP[tax_id]
    except KeyError:
        node = {'depth': depth, 'info': tkns, 'samples': {}, 'children': [], 'parent': parent}
        if parent:
            parent['children'].append(node)
        NODE_MAP[tax_id] = node
    node['samples'][sample_name] = tkns
    return node


def add_to_tree(sample_name, report_file, root, min_rank=None, min_abundance=0, min_kmer=0, min_cov=0):
    """Return a root node with the file as a tree."""
    report_file.readline()  # header
    current_parent = get_node(root, sample_name, *tokenize(report_file.readline()))
    for line in report_file:
        depth, tkns = tokenize(line)
        if tkns['percent'] < min_abundance or tkns['kmers'] < min_kmer or tkns['cov'] < min_cov:
            continue
        while depth <= current_parent['depth']:
            current_parent = current_parent['parent']
        if min_rank and current_parent['info']['rank'] == min_rank:
            continue
        node = get_node(current_parent, sample_name, depth, tkns)
        current_parent = node

    return root


def report_from_tree(root_node, features, rank, wide=True):
    """Return a pandas dataframe with all requested info about child nodes of root."""
    tbl = {}
    for node in root_node['children']:
        if rank and node['info']['rank'].lower() != rank:
            continue
        for feature in features:
            header = (
                node['info']['tax_name'],
                node['info']['tax_id'],
                node['info']['rank'],
                get_mpa_str(node),
            )
            if wide:
                if len(features) > 1:
                    header += (feature,)  # do not report feature if only 1
                tbl[header] = {
                    sample_name: tkns[feature] for sample_name, tkns in node['samples'].items()
                }
            else:
                for sample_name, tkns in node['samples'].items():
                    try:
                        tbl[(sample_name,) + header][feature] = tkns[feature]
                    except KeyError:
                        tbl[(sample_name,) + header] = {feature: tkns[feature]}

    orient = 'columns' if wide else 'index'
    tables = [pd.DataFrame.from_dict(tbl, orient=orient)]
    for child_node in root_node['children']:
        tables += report_from_tree(child_node, features, rank, wide=wide)
    return tables


def build_table(report_files, features, rank, min_abundance=0, min_kmer=0, min_cov=0, wide=True):
    """Return a pandas dataframe with data from all files."""
    root_tkns = {'tax_name': 'ROOT', 'rank': 'no rank', 'tax_id': float('nan')}
    root_node = get_node(None, 'all', -1, root_tkns)
    for sample_name, report_file in report_files.items():
        add_to_tree(sample_name, report_file, root_node,
                    min_rank=rank, min_abundance=min_abundance, min_kmer=min_kmer, min_cov=min_cov)
    all_tbls = report_from_tree(root_node, features, rank, wide=wide)
    axis = 1 if wide else 0
    tbl = pd.concat(all_tbls, axis=axis, sort=True)
    return tbl


def longform_taxa(report_filenames,
                  min_abundance=0, min_kmer=256, min_cov=0, wide=False,
                  rank=None, features='reads,kmers,dup,cov,percent,tax_reads'):
    """Return a longform taxa table as a pandas dataframe."""
    try:
        report_files = {
            report_filename[0]: open(report_filename[1])
            for report_filename in report_filenames
        }
        tbl = build_table(
            report_files, features.split(','), rank,
            min_abundance=min_abundance, min_kmer=min_kmer, min_cov=min_cov, wide=wide
        )
        return tbl
    except Exception:
        [report_file.close() for report_file in report_files.values()]
        raise
