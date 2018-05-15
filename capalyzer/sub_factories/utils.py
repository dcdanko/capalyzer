

def parse_gene_table(gene_table, metric):
    '''Return a parsed gene quantification table.'''
    with open(gene_table) as gt:
        gene_names = gt.readline().strip().split(',')[1:]
        rpks = gt.readline().strip().split(',')[1:]
        rpkms = gt.readline().strip().split(',')[1:]
        rpkmgs = gt.readline().strip().split(',')[1:]

    data = {}
    for i, gene_name in enumerate(gene_names):
        row = {
            'RPK': rpks[i],
            'RPKM': rpkms[i],
            'RPKMG': rpkmgs[i],
        }
        data[gene_name] = row[metric]
    return data
