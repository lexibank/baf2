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
                'language_name',
                'language_family',
                'language_subgroup',
                'concept_name',
                'concept_concepticon_id',
                'concept_french_gloss',
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
                ('language_subgroup', 'subgroup'),
                ('concept_french_gloss', 'french'),
                ('concept_in_source', 'concept_in_source'), 
                ('language_name', 'doculect_name'),
                ('segments', 'tokens'),
                ('language_glottocode', 'glottolog'),
                ('concept_concepticon_id', 'concepticon'),
                ('language_latitude', 'latitude'),
                ('language_longitude', 'longitude'),
                ('cognacy', 'cognacy'),
                ('local_id', 'id_in_source'),
                ('cogid_cognateset_id', 'cogid')))
    args.log.info('loaded data')    
    lex = LexStat(wl)
    lex.cluster(method='sca', threshold=0.45, ref='borid')
    lex.add_entries('cog', 'family,borid', lambda x, y:
            x[y[0]]+'-'+str(x[y[1]]))
    lex.renumber('cog')
    lex.add_entries('stratum', 'value', lambda x: '')
    lex.add_entries('cogids', 'cognacy', lambda x: x)

    etd = lex.get_etymdict(ref='borid')
    for key, values in etd.items():
        idxs = []
        for idx in values:
            if idx:
                idxs += idx
        subs = [lex[idx, 'family'] for idx in idxs]
        lang = [lex[idx, 'doculect'] for idx in idxs]
        if len(set(subs)) == 1 or len(set(lang)) == 1:
            for idx in idxs:
                lex[idx, 'borid'] = 0
                
    D = {0: [
        'id_in_source',
        'doculect',
        'doculect_name',
        'family',
        'subgroup',
        'concepticon',
        'concept',
        'french',
        'value',
        'form',
        'tokens',
        'cogids',
        'cogid',
        'borid',
        'stratum']}


    for idx in wl:
        D[idx] = [lex[idx, h] for h in D[0]]
    
    lex = LexiBase(D, dbase=ds.dir.joinpath('analysis',
        'bangime.sqlite3').as_posix())
    lex.create('bangime')

    lex.output('tsv', filename=ds.dir.joinpath(
        'analysis',
        'wordlist').as_posix(), ignore='all', prettify=False)

