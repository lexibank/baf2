from lingpy import *

from collections import defaultdict
from itertools import combinations

wl = Wordlist('../raw/bangime.tsv')

etd = wl.get_etymdict(ref='borid')

shared = defaultdict(list)
families = {
        wl[idx, 'doculect']: wl[idx, 'family'] for idx in wl}

for cogid, refs in [c for c in etd.items() if c != '0']:
    for (i, tA), (j, tB) in combinations(enumerate(wl.cols), r=2):
        if refs[i] != 0 and refs[j] != 0:
            shared[tA, tB] += [cogid]

bangime = defaultdict(list)
for tA, tB in shared:
    if tA == 'Bangime':
        fB = families[tB]
    elif tB == 'Bangime':
        fB = families[tA]
    else:
        fB = ''
    if fB:
        bangime[fB] += [len(shared[tA, tB])]

for family, sharedi in bangime.items():
    print('{0:30} | {1:.2f}'.format(family,
        sum(sharedi)/len(sharedi)))

