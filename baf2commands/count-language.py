"""
Counts per doculect.
"""
from lingpy import Wordlist
from lexibank_baf2 import Dataset


def run(args):
    ds = Dataset()
    wl = Wordlist(str(ds.dir / 'raw/bangime-edited.tsv'))

    etd = wl.get_etymdict(ref='borid')
    doc2fam = {language["ID"]: language["Family"] for language in ds.languages}
    wl.add_entries("family", "doculect", lambda x: doc2fam[x])
    families = sorted(set([wl[idx, 'doculect'] for idx in wl]))

    table = []
    for cogid, refs in etd.items():
        if cogid not in ['0', 0]:
            idxs = []
            for ref in refs:
                if ref:
                    idxs += ref
            concept = wl[idxs[0], 'concept']
            famis = [wl[idx, 'doculect'] for idx in idxs]

            count = str(len(set(famis)))
            ptn = ' '.join(['1' if f in famis else '0' for f in families])
            table += [[concept]+[
                str(famis.count(f)) for f in families]+[str(cogid), ptn, count, str(len(idxs))]]

    with open(ds.dir / "analysis" / 'patterns-language.tsv', 'w') as f:
        f.write('Concept\t'+'\t'.join(families)+'\tBORROWING\tPATTERN\tDOCULECT\tREFLEXES\n')
        for line in sorted(table, key=lambda x: (x[-2], x[-3])):
            f.write('\t'.join(line)+'\n')
    args.log.info("written file 'analysis/patterns-language.tsv'")
