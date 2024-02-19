import pathlib

import attr
import lingpy
from pyedictor import fetch

from clldutils.misc import slug
from pylexibank import Concept, Language, Lexeme, Dataset as BaseDataset, progressbar
import codecs


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
    Borrowing = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    concept_class = CustomConcept
    language_class = CustomLanguage
    lexeme_class = CustomLexeme

    id = 'baf2'

    def cmd_download(self, args):
        data = fetch(
                "bangime", 
                base_url="https://digling.org/edictor",
                to_lingpy=False,
                columns=[
                    "DOCULECT", "CONCEPT", "VALUE", "FORM", "TOKENS",
                    "COGID", "COGIDS", "BORID", "CONCEPT_IN_SOURCE"
                ]
                )
        
        with codecs.open(self.raw_dir / "raw-data.tsv", "w", "utf-8") as f:
            f.write(data)
        wl = lingpy.Wordlist(str(self.raw_dir / "raw-data.tsv"))
        
        for idx, concept, doculect, cogids, tokens in wl.iter_rows(
                "concept", "doculect", "cogids", "tokens"):
            if len(cogids) != len(" ".join(tokens).split(" + ")):
                args.log.warning("{0:4}: {1:15} | {2:20} | {3:10} | {4}".format(
                    idx, 
                    concept[:15], 
                    doculect, 
                    " ".join([str(x) for x in cogids]), 
                    " ".join(tokens)))
            if "Ø" in tokens:
                wl[idx, "tokens"] = [t for t in tokens if t != "Ø"]

        wl.output("tsv", filename=str(self.raw_dir.joinpath("bangime-edited")))

    def cmd_makecldf(self, args):
        wl = lingpy.Wordlist(str(self.raw_dir / 'bangime-edited.tsv'))
        args.writer.add_sources()
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = '{0}_{1}'.format(
                    concept.number,
                    slug(concept.english))

            args.writer.add_concept(
                ID=idx,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                French_Gloss=concept.attributes["french"]
            )
            if concept.attributes["lexibank_gloss"]:
                concepts[concept.attributes["lexibank_gloss"]] = idx
            else:
                concepts[concept.english] = idx
        for language in self.languages:
            args.writer.add_language(**language)
        
        errors = set()
        for idx in progressbar(wl, desc='cldfify'):
            if wl[idx, 'tokens']:
                try:
                    row = args.writer.add_form_with_segments(
                        Language_ID=wl[idx, 'doculect'],
                        Local_ID=idx,
                        Parameter_ID=concepts[wl[idx, 'concept']],
                        Value=wl[idx, 'value'].strip() or '?',
                        Form=wl[idx, 'form'].strip() or '?',
                        Segments=wl[idx, 'tokens'],
                        Source='Hantgan2022',
                        Cognacy=wl[idx, 'cogid'],
                        Borrowing=wl[idx, "borid"],
                        Concept_in_Source=wl[idx, 'concept_in_source']
                    )
                except KeyError:
                    errors.add(wl[idx, "concept"])
        for c in errors:
            print(c)
