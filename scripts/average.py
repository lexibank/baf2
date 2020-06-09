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



