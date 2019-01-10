from json import loads


def readJSON(jsonf):
    return loads(open(jsonf).read())


def tokenize(file_name, skip=0, sep='\t', skipchar='#'):
    with open(file_name) as f:
        for _ in range(skip):
            f.readline()
        for line in f:
            stripped = line.strip()
            if stripped[0] == skipchar:
                continue
            tkns = stripped.split(sep)
            if len(tkns) >= 2:
                yield tkns


def parse_key_val_file(filename,
                       skip=0, skipchar='#', sep='\t',
                       kind=float, key_column=0, val_column=1):
    out = {tkns[key_column]: kind(tkns[val_column])
           for tkns in tokenize(filename,
                                skip=skip, sep=sep, skipchar=skipchar)
           }
    return out
