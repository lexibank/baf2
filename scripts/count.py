from lingpy import *
from collections import defaultdict
from itertools import combinations

wl = Wordlist('../raw/bangime.tsv')

etd = wl.get_etymdict(ref='borid')

families = sorted(set([wl[idx, 'family'] for idx in wl]))

shared = defaultdict(list)

table = []
for cogid, refs in etd.items():
    if cogid not in ['0', 0]:
        idxs = []
        for ref in refs:
            if ref:
                idxs += ref
        concept = wl[idxs[0], 'concept']
        famis = [wl[idx, 'family'] for idx in idxs]
        
        count = str(len(set(famis)))
        ptn = ' '.join(['1' if f in famis else '0' for f in families])
        table += [[concept]+[
            str(famis.count(f)) for f in families]+[str(cogid), ptn, count,
                str(len(idxs))]]
        for f1, f2 in combinations(families, r=2):
            if f1 in famis and f2 in famis:
                shared[f1, f2] += [concept]

with open('patterns.tsv', 'w') as f:
    f.write('Concept\t'+'\t'.join(families)+'\tBORROWING\tPATTERN\tFAMILIES\tREFLEXES\n')
    for line in sorted(table, key=lambda x: (x[-2], x[-3])):
        f.write('\t'.join(line)+'\n')

for (f1, f2), concepts in sorted(shared.items()):
    print('{0:20}\t{1:20}\t{2}'.format(f1, f2, len(concepts)))
