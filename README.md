# Qlever Test Instance

## About

This repo is for testing approaches to deploying Qlever and the UI and Mapping via 
Docker compose files. 

If you are interested in these components, you should check out them directly at;

* [Qlever](https://github.com/ad-freiburg/qlever)
* [Qlever-ui](https://github.com/ad-freiburg/qlever-ui)
* [Petrimaps - mapping for Qlever GeoSPARQL](https://github.com/ad-freiburg/qlever-petrimaps)

Also, if you just want to run Qlever local with data for testing, you should use
[Qlever-control](https://github.com/ad-freiburg/qlever-control)

This repo is really focused on leveraging the above in custom Docker compose workflows and 
eventually in tools like Dagster.

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
