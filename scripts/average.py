from lingpy import *

from collections import defaultdict
from itertools import combinations

wl = Wordlist('../raw/bangime.tsv')

etd = wl.get_etymdict(ref='borid')

shared = defaultdict(list)
families = {
        wl[idx, 'doculect']: wl[idx, 'family'] for idx in wl}

for cogid, refs in [c for c in etd.items() if c != '0']:
    idxs = []
    for ref in refs:
        if ref:
            idxs += ref
    famis = [wl[idx, 'family'] for idx in idxs]
    if len(set(famis)) == 2:
        for (i, tA), (j, tB) in combinations(enumerate(wl.cols), r=2):
            if refs[i] != 0 and refs[j] != 0:
                shared[tA, tB] += [cogid]

bangime = defaultdict(list)
dogon = defaultdict(list)
for tA, tB in shared:
    if tA == 'Bangime':
        fB = families[tB]
        t = tB
    elif tB == 'Bangime':
        fB = families[tA]
        t = tA
    else:
        fB = ''
    if fB:
        bangime[fB] += [(t, len(shared[tA, tB]))]

    fA, fB = families[tA], families[tB]
    if fA == 'Dogon' and fB != 'Dogon':
        dogon[fB] += [(tA, len(shared[tA, tB]))]
    elif fA != 'Dogon' and fB == 'Dogon':
        dogon[fA] += [(tB, len(shared[tA, tB]))]

for family, sharedi in bangime.items():
    print('{0:30} | {1:.2f}'.format(family,
        sum([x[1] for x in sharedi])/len(sharedi)))

print('')
for language, sharedi in dogon.items():
    print('{0:30} | {1:.2f}'.format(language,
        sum([x[1] for x in sharedi])/len(sharedi)))


relations = defaultdict(list)
for (tA, tB), values in shared.items():
    fA, fB = families[tA], families[tB]
    relations[tA, fB] += [(tB, values)]
    

with open('relations.md', 'w') as f:
    current_family = ''
    for (t, fm), reflexes in sorted(relations.items(), key=lambda x:
            (families[x[0][0]], x[0][1], x[0][0])):
        if families[t] != current_family:
            current_family = families[t]
            f.write('# Binary relations of {0} \n'.format(families[t]))
        f.write('## Binary relations between {0} and {1}\n\n'.format(t, fm))
        f.write('Language | Number | Candidates | Concepts \n')
        f.write('--- | --- | --- | --- \n')
        for tB, cogids in reflexes:
            concepts = []
            for cogid in cogids:
                concepts += [wl[[x[0] for x in etd[cogid] if x][0], 'concept']]
            f.write('{0} | {1} | {2} | {3} \n'.format(
                tB, len(cogids), ', '.join(cogids), ', '.join(concepts)))
        f.write('\n\n')
