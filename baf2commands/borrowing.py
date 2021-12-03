"""Convert to edictor application"""

from lingpy import *
from lexibase.lexibase import LexiBase
from clldutils.misc import slug

from clldutils.text import split_text, strip_brackets
from collections import defaultdict
from lexibank_baf2 import Dataset

def run(args):
    ds = Dataset()

    wl = Wordlist.from_cldf(
            str(ds.cldf_specs().metadata_path),
            columns = (
                'local_id',
                'language_id',
                'language_family',
                'language_subgroup',
                'concept_name',
                'value',
                'form',
                'segments',
                'cognacy',
                ),
            namespace = (
                ('concept_name', 'concept'),
                ('parameter_id', 'concepticon_id'),
                ('language_id', 'doculect'),
                ('language_family', 'family'),
                ('segments', 'tokens'))
            )

    args.log.info('loaded data')
    lex = LexStat(wl)
    lex.cluster(method='sca', threshold=0.45, ref='borid')
    lex.add_entries('cog', 'family,borid', lambda x, y:
            x[y[0]]+'-'+str(x[y[1]]))
    lex.renumber('cog')
    args.log.info("computed cognates")

    etd = lex.get_etymdict(ref='borid')
    for cogid, (idxs, families, languages) in lex.iter_cognates(
            "borid", "family", "doculect"):
        if len(set(families)) == 1 or len(set(languages)) == 1:
            for idx in idxs:
                lex[idx, 'borid'] = 0
    
    lex.add_entries("subgroup", "family", lambda x: x)
    lex.output(
        'tsv', 
        filename=str(ds.dir.joinpath(
            'analysis',
            'wordlist')), ignore='all', prettify=False)

