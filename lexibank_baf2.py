import pathlib

import attr
import lingpy

from clldutils.misc import slug
from pylexibank import Concept, Language, Lexeme, Cognate, Dataset as BaseDataset, progressbar

@attr.s
class CustomCognate(Cognate):
    Segment_Slice = attr.ib(default=None)

@attr.s
class CustomConcept(Concept):
    French_Gloss = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    SubGroup = attr.ib(default=None)
    Source = attr.ib(default=None)

@attr.s
class CustomLexeme(Lexeme):
    Concept_in_Source = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    concept_class = CustomConcept
    language_class = CustomLanguage
    lexeme_class = CustomLexeme
    cognate_class = CustomCognate

    id = 'baf2'

    def cmd_makecldf(self, args):
        wl = lingpy.Wordlist(str(self.raw_dir / 'data.tsv'))
        args.writer.add_sources()
        concepts = {}
        for concept in self.concepts:
            idx = '{0}_{1}'.format(
                    concept['NUMBER'], 
                    slug(concept['ENGLISH']))
            args.writer.add_concept(
                ID=idx,
                Name=concept['ENGLISH'],
                Concepticon_ID=concept['CONCEPTICON_ID'],
                French_Gloss=concept['FRENCH']
            )
            concepts[concept['ENGLISH']] = idx
        languages = {}
        for language in self.languages:
            args.writer.add_language(**language)
            languages[language['Name']] = language['ID']

        for idx in progressbar(wl, desc='cldfify'):
            if wl[idx, 'tokens']:
                row = args.writer.add_form_with_segments(
                    Language_ID=languages[wl[idx, 'doculect']],
                    Local_ID=idx,
                    Parameter_ID=concepts[wl[idx, 'concept']],
                    Value=wl[idx, 'value'].strip() or '?',
                    Form=wl[idx, 'form'].strip() or '?',
                    Segments=wl[idx, 'tokens'],
                    Source=['hantganfc'],
                    Cognacy=wl[idx, 'cogids'],
                    Concept_in_Source=wl[idx, 'concept_in_source']
                )
                for morpheme_idx, cogid in enumerate(wl[idx, 'cogids']):
                    args.writer.add_cognate(
                        lexeme=row,
                        Cognateset_ID=cogid,
                        Source='hantganfc',
                        Segment_Slice=morpheme_idx+1
                    )
