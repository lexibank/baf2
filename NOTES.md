# Analysis of Bangime and Friends (2)

The data in EDICTOR can be accessed from [https://digling.org/links/bangime.html](https://digling.org/links/bangime.html).

To run the analysis, make sure to install all requirements:

```shell
pip install -e ".[full]"
```

Also make sure to clone all repositories of Concepticon, Glottolog, and CLTS:

```shell
mkdir repos
cd repos
git clone https://github.com/glottolog/glottolog.git
git clone https://github.com/concepticon/concepticon-data.git
git clone https://github.com/cldf-clts/clts
```

The data is annotated with the help of the EDICTOR tool, where you can also inspect it using the link
[https://digling.org/edictor/http://digling.org/edictor/?remote_dbase=bangime&file=bangime](http://digling.org/edictor/?remote_dbase=bangime&file=bangime&basics=DOCULECT|CONCEPT|TOKENS|COGID|COGIDS|COGID|BORID|NOTE&columns=DOCULECT|CONCEPT|CONCEPT_FRENCH|FAMILY|SUBGROUP|VALUE|FORM|TOKENS|COGID|COGIDS|BORID|STRATUM&split_on_tones=false).

To download the most recent version of the data programmatically, type:

```shell
cldfbench download lexibank_baf2.py
```

In order to convert the updated data to cldf, run:

```shell
cldfbench lexibank.makecldf lexibank_baf2.py --concepticon-version=v3.2.0 --glottolog-version=v5.0 --clts-version=v2.3.0
```

In order to run the cognate and borrowing detection analysis, run:

```shell
cldfbench baf2.borrowing
```

This analysis will create a file `wordlist.tsv` in the folder `analysis`. Note that the analysis itself was only done once in the beginning of our investigation and later manually updated. As a result, the results of this comparison necessarily differ from the results of the manually updated version.

To analyze the data, you can first compute average statistics of borrowed items:

```shell
cldfbench baf2.average
```

This will create a file `relations.md` in the folder `analysis`.

To count shared borrowing candidates, type:

```shell
cldfbench baf2.count
```

This will create a file `analysis/patterns.tsv`.

To yield the same for all language subgroups in the sample, type:

```shell
cldfbench baf2.count-subgroup
```

This will write the patterns to the file `analysis/patterns-subgroups.tsv`.

To yield the same for all languages in the sample, type:

```shell
cldfbench baf2.count-language
```

This will write the patterns to the file `analysis/patterns-subgroups.tsv`.
