# Analysis of Bangime and Friends (2)

The data in EDICTOR can be accessed from [https://digling.org/links/bangime.html](https://digling.org/links/bangime.html).

To run the analysis, make sure to install all requirements:

```
$ pip install -e ./
```

As a second step, you can then run the data lifting analysis:

```
$ cldfbench lexibank.makecldf baf2
```

And in order to run the cognate detection analysis, run:

```
$ cldfbench baf2commands.edictor
```

This analysis results in an SQLITE3 database file, which we uploaded to the EDICTOR tool for a convenient manual refinement of the data. The data can be accessed at [https://digling.org/edictor/http://digling.org/edictor/?remote_dbase=bangime&file=bangime&split_on_tones=false](http://digling.org/edictor/?remote_dbase=bangime&file=bangime&basics=DOCULECT|CONCEPT|TOKENS|COGID|COGIDS|COGID|BORID|NOTE&columns=DOCULECT|CONCEPT|CONCEPT_FRENCH|FAMILY|SUBGROUP|VALUE|FORM|TOKENS|COGID|COGIDS|BORID|STRATUM&split_on_tones=false). 

To run the followin analyses to analyse the data after manual refinement, we offer Python scripts in the folder `scripts`. Our EDICTOR file with the manuall annotated data is available as `raw/bangime.tsv`.

To run our main analysis, type:

```
$ cd scripts
$ python average.py
```

This will create the file `scripts/relations.md`, which offers very detailed relations with respect to potential borrowings. 



