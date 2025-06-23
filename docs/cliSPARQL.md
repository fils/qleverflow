# Command line SPARQL examples Snippets

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
