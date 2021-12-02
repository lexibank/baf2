import pathlib

import attr
import lingpy
from pyedictor import fetch

from clldutils.misc import slug
from pylexibank import Concept, Language, Lexeme, Cognate, Dataset as BaseDataset, progressbar
import re
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
                columns=["DOCULECT", "CONCEPT", "VALUE", "FORM", "TOKENS",
                    "COGID", "COGIDS", "BORID", "CONCEPT_IN_SOURCE"]
                )
        with codecs.open(self.raw_dir / "raw-data.tsv", "w", "utf-8") as f:
            f.write(data)
        wl = lingpy.Wordlist(str(self.raw_dir / "raw-data.tsv"))
        reps = {
                "dw": "d w",
                "ŋ̀": "ŋ̀/ŋ",
                "⁵j": "⁵/j",
                "/⁵i": "⁵/i",
                "+l": "+ l",
                "sɔː": "s ɔː",
                "¹/a+": "¹/a +",
                "sɔː": "s ɔː",
                "vj": "v j",
                "⁵¹/uŋ": "⁵¹/u ŋ",
                "⁵¹/ul": "⁵¹/u l",
                "¹/aː+": "¹/aː +",
                "¹+": "+",
                "⁵/o+": "⁵/o +",
                "Ø": "",
                "⁵¹/u+": "⁵¹/u +",
                "∼/⁵ɔ": "⁵/ɔ̃",
                "∼/w̃": "w̃",
                "∼/j": "j̃",
                }
        #for idx, tokens in wl.iter_rows("tokens"):
        #    if "/ ∼" in str(tokens):
        #        tokens = re.sub("/ ∼/(.)", r"/\1"+"\u0303", str(tokens)).split()
        #        wl[idx, "tokens"] = tokens
        #    elif "/∼/" in str(tokens):
        #        tokens = re.sub("/∼/(.)", r"/\1"+"\u0303", str(tokens)).split()
        #        wl[idx, "tokens"] = tokens
        #    elif "/¹/" in str(tokens) or "/⁵/" in str(tokens) or "⁵¹/u" in str(tokens):
        #        tokens = str(tokens).replace("/¹", "").replace("/⁵", "").replace("⁵¹/u ", "⁵¹/u").split()
        #        wl[idx, "tokens"] = tokens
        #    elif "/¹ " in str(tokens) or "∼/ " in str(tokens) or "¹/ " in str(tokens):
        #        tokens = str(tokens).replace("/¹ ", "").replace("∼/ ", "").replace("¹/ ", "").split()
        #        wl[idx, "tokens"] = tokens
        #    wl[idx, "tokens"] = " ".join([reps.get(t, t) for t in
        #            wl[idx, "tokens"]]).split()

        
        for idx, concept, doculect, cogids, tokens in wl.iter_rows(
                "concept", "doculect", "cogids", "tokens"):
            if len(cogids) != len(" ".join(tokens).split(" + ")):
                args.log.warning("{0:4}: {1:15} | {2:20} | {3:10} | {4}".format(
                    idx, 
                    concept[:15], 
                    doculect, 
                    " ".join([str(x) for x in cogids]), 
                    " ".join(tokens)))

        wl.output("tsv", filename=str(self.raw_dir.joinpath("bangime-edited")))


    def cmd_makecldf(self, args):
        wl = lingpy.Wordlist(str(self.raw_dir / 'bangime-edited.tsv'))
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
        for language in self.languages:
            args.writer.add_language(**language)

        for idx in progressbar(wl, desc='cldfify'):
            if wl[idx, 'tokens']:
                row = args.writer.add_form_with_segments(
                    Language_ID=wl[idx, 'doculect'],
                    Local_ID=idx,
                    Parameter_ID=concepts[wl[idx, 'concept']],
                    Value=wl[idx, 'value'].strip() or '?',
                    Form=wl[idx, 'form'].strip() or '?',
                    Segments=wl[idx, 'tokens'],
                    Source=['hantganfc'],
                    Cognacy=wl[idx, 'cogid'],
                    Borrowing=wl[idx, "borid"],
                    Concept_in_Source=wl[idx, 'concept_in_source']
                )
