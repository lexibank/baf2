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


