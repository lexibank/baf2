# CLDF dataset underlying the study "Detection of contact layers in Bangime" from 2021

## How to cite

If you use these data please cite
- the original source
  > Hantgan, Abbie and Babiker, Hiba and List, Johann-Mattis (2021): Detection of contact layers in Bangime.
- the derived dataset using the DOI of the [particular released version](../../releases/) you were using

## Description


This dataset is licensed under a CC-BY-4.0 license

Available online at http://digling.org/links/bangime.html

## Notes

# Analysis of Bangime and Friends (2)

The data in EDICTOR can be accessed from [https://digling.org/links/bangime.html](https://digling.org/links/bangime.html).

To run the analysis, make sure to install all requirements:

```
$ pip install -e .[full]
```

Also make sure to clone all repositories of Concepticon, Glottolog, and CLTS:

```
$ mkdir repos
$ cd repos
$ git clone https://github.com/glottolog/glottolog.git
$ git clone https://github.com/concepticon/concepticon-data.git
$ git clone https://github.com/cldf-clts/clts
```


The data is annotated with the help of the EDICTOR tool, where you can also inspect it using the link
[https://digling.org/edictor/http://digling.org/edictor/?remote_dbase=bangime&file=bangime](http://digling.org/edictor/?remote_dbase=bangime&file=bangime&basics=DOCULECT|CONCEPT|TOKENS|COGID|COGIDS|COGID|BORID|NOTE&columns=DOCULECT|CONCEPT|CONCEPT_FRENCH|FAMILY|SUBGROUP|VALUE|FORM|TOKENS|COGID|COGIDS|BORID|STRATUM&split_on_tones=false).

To download the most recent version of the data programmatically, type:

```
$ cldfbench download lexibank_baf2.py
```

In order to convert the updated data to cldf, run:

```
$ cldfbench lexibank.makecldf lexibank_baf2.py --concepticon-version=v2.5.0 --glottolog-version=v4.4 --clts-version=v2.1.0
```

In order to run the cognate and borrowing detection analysis, run:

```
$ cldfbench baf2commands.borrowing
```

This analysis will create a file `wordlist.tsv` in the folder `analysis`. Note that the analysis itself was only done once in the beginning of our investigation and later manually updated. As a result, the results of this comparison necessarily differ from the results of the manually updated version. 

To analyze the data, you can first compute average statistics of borrowed items:

```
$ cldfbench baf2.average
```

This will create a file `relations.md` in the folder `analysis`.

To count shared borrowing candidates, type:

```
$ cldfbench baf2.count
```

This will create a file `analysis/patterns.tsv`.

To yield the same for all language subgroups in the sample, type:

```
$ cldfbench baf2.count-subgroup
```

This will write the patterns to the file `analysis/patterns-subgroups.tsv`. 

To yield the same for all languages in the sample, type:

```
$ cldfbench baf2.count-language
```

This will write the patterns to the file `analysis/patterns-subgroups.tsv`. 




## Statistics


![Glottolog: 100%](https://img.shields.io/badge/Glottolog-100%25-brightgreen.svg "Glottolog: 100%")
![Concepticon: 97%](https://img.shields.io/badge/Concepticon-97%25-green.svg "Concepticon: 97%")
![Source: 100%](https://img.shields.io/badge/Source-100%25-brightgreen.svg "Source: 100%")
![BIPA: 100%](https://img.shields.io/badge/BIPA-100%25-brightgreen.svg "BIPA: 100%")
![CLTS SoundClass: 100%](https://img.shields.io/badge/CLTS%20SoundClass-100%25-brightgreen.svg "CLTS SoundClass: 100%")

- **Varieties:** 38
- **Concepts:** 344
- **Lexemes:** 9,460
- **Sources:** 1
- **Synonymy:** 1.08
- **Invalid lexemes:** 0
- **Tokens:** 45,577
- **Segments:** 275 (0 BIPA errors, 0 CLTS sound class errors, 274 CLTS modified)
- **Inventory size (avg):** 72.21

## CLDF Datasets

The following CLDF datasets are available in [cldf](cldf):

- CLDF [Wordlist](https://github.com/cldf/cldf/tree/master/modules/Wordlist) at [cldf/cldf-metadata.json](cldf/cldf-metadata.json)