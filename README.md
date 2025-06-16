# Qlever Test Instance

## About

First, if you are interested in Qlever and running it locally, DO NOT USE THIS REPO.  At least, it's very likely
not what you want.

You should go to the [qlever-control](https://github.com/ad-freiburg/qlever-control) repo instead.  That 
is the official repo for a nice server and UI onboarding experience with Qlever.   Also visit the main 
[qlever](https://github.com/ad-freiburg/qlever) repo or the [Qlever Wiki](https://github.com/ad-freiburg/qlever/wiki).

So why does this repo exist?   I wanted to play with ways to leverage deploying Qlever via 
docker compose files for some of the workflows and automated approaches I have.   In that case, qlever-control
was not quite what I needed.  So I basically decomposed its approach into docker compose files.

This repo is for testing those approaches and ideas. 

If you are interested in these components, you should check them out directly at;

* [Qlever](https://github.com/ad-freiburg/qlever)
* [Qlever-ui](https://github.com/ad-freiburg/qlever-ui)
* [Petrimaps - mapping for Qlever GeoSPARQL](https://github.com/ad-freiburg/qlever-petrimaps)

Also, if you just want to run Qlever local with data for testing, you should use
[Qlever-control](https://github.com/ad-freiburg/qlever-control)

Also see the [README.md](catalogues/README.md) in catalogues for how to download and index data
from your own Qleverfile.

At present the compose.yaml is the main config we are working with.  

## SPARQL Extensions

The following two extensions to QLever are of interest.

[SPARQL plus Text](https://github.com/ad-freiburg/qlever/blob/master/docs/sparql_plus_text.md)

[Path Search Feature Documentation for SPARQL Engine](https://github.com/ad-freiburg/qlever/blob/master/docs/path_search.md)


## Command line SPARQL examples Snippets

May also want to try qlever format: Accept: application/qlever-results+json


```bash
curl -s "http://workstation.lan:7001" -H "Accept: text/tab-separated-values" -H "Content-type: application/sparql-query" --data "SELECT * WHERE { ?s ?p ?o } LIMIT 10" ;

```

```bash
curl -s "http://workstation.lan:7001" -H "Accept: text/tab-separated-values" -H "Content-type: application/sparql-query" --data @./searchODIS/dataset.rq ;

```

```bash
curl -s "http://workstation.lan:7019?timeout=600s&access-token=odis_7643543846_6dMISzlPrD7i" -H "Accept: text/csv" -H "Content-type: application/sparql-query" --data "SELECT * WHERE { ?s ?p ?o  }" >  results.csv
```
