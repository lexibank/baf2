from lingpy import *

wl = Wordlist('../raw/bangime.tsv')

etd = wl.get_etymdict(ref='borid')

families = sorted(set([wl[idx, 'subgroup'] for idx in wl]))

table = []
for cogid, refs in etd.items():
    if cogid not in ['0', 0]:
        idxs = []
        for ref in refs:
            if ref:
                idxs += ref
        concept = wl[idxs[0], 'concept']
        famis = [wl[idx, 'subgroup'] for idx in idxs]
        
        count = str(len(set(famis)))
        ptn = ' '.join(['1' if f in famis else '0' for f in families])
        table += [[concept]+[
            str(famis.count(f)) for f in families]+[str(cogid), ptn, count,
                str(len(idxs))]]

with open('patterns2.tsv', 'w') as f:
    f.write('Concept\t'+'\t'.join(families)+'\tBORROWING\tPATTERN\tSUBGROUP\tREFLEXES\n')
    for line in sorted(table, key=lambda x: (x[-2], x[-3])):
        f.write('\t'.join(line)+'\n')