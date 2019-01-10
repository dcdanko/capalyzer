from sys import stderr

def parse_gene_table(gene_table, metric):
    """Return a parsed gene quantification table."""
    data = {}
    warn = None
    with open(gene_table) as gfile:
        gfile.readline()
        for line in gfile:
            try:
                tkns = line.strip().split(',')
                gene_name = tkns[0]
                row = {
                    'rpk': float(tkns[1]),
                    'rpkm': float(tkns[2]),
                    'rpkmg': float(tkns[3]),
                }
                data[gene_name] = row[metric]
            except:
                warn = True
    if warn:
        print(f'[WARNING] one or more lines failed to parse in {gene_table}', file=stderr) 
    return data
