# CURL for construct and SHACL pipeline

Construct SPARQL

1) Use the named graph query (with filter perhaps) to get list of named graphs
2) Use those named graphs in a CONSTRUCT call to get the triples to check.

TODO:
 - [ ] convert this to a python program.
 - [ ] load the results into pyoxigraph and then download the graph there to a file
 - [ ] alternatively, load directly to QLever or to a directory of graphs to load to Qlever
 - Defs needed
   - function to take a SPARQL query and return a dataframe with the results - this is the graph with filter ?g returned
   - function to take an argument (named graph) and do a construct call, return a nq/nt graph
   - SHACL function that takes a datagraph and shapegraph and returns a graph




```SPARQL
CONSTRUCT {
  ?s ?p ?o
}
WHERE {
  GRAPH <urn:gleaner.io:oih:medin:data:04bd1d47761a03e2329931964f63fdfc8617b4c1> {
    {
      ?s ?p ?o
    }
  }
}
```


```bash
curl -s "http://ghost.lan:7007"  -H "Accept: text/tab-separated-values" -H "Content-type: application/sparql-query" --data @./construct.rq > results.nt
```

```bash
 rapper -c -i ntriples results.nt 
```

```bash
rapper  -i ntriples -o turtle  results.nt > resultsv2.ttl   
```

```bash
pyshacl -s  ./ERDDAP.ttl -sf turtle -df nt -f table ./resultsv2.nt
```

example results

```
+----------+
| Conforms |
+----------+
|  False   |
+----------+

+-----+-----------+---------------------------+---------------------------+---------------------------+---------------------------+---------------------------+-------+
| No. | Severity  | Focus Node                | Result Path               | Message                   | Component                 | Shape                     | Value |
+-----+-----------+---------------------------+---------------------------+---------------------------+---------------------------+---------------------------+-------+
| 1   | Warning   | http://portal.medin.org.u | https://schema.org/contac | Contact information shoul | MinCountConstraintCompone | https://oceans.collaboriu | -     |
|     |           | k/portal/json-ld/00040230 | ts                        | d be provided             | nt                        | m.io/voc/validation/1.0.1 |       |
|     |           | -d455-4fea-8747-6179d77ab |                           |                           |                           | /shacl#coreContacts       |       |
|     |           | 103.jsonld                |                           |                           |                           |                           |       |
|     |           |                           |                           |                           |                           |                           |       |
| 2   | Violation | http://portal.medin.org.u | https://schema.org/licens | License information shoul | MinCountConstraintCompone | https://oceans.collaboriu | -     |
|     |           | k/portal/json-ld/00040230 | e                         | d be provided             | nt                        | m.io/voc/validation/1.0.1 |       |
|     |           | -d455-4fea-8747-6179d77ab |                           |                           |                           | /shacl#coreLicense        |       |
|     |           | 103.jsonld                |                           |                           |                           |                           |       |
|     |           |                           |                           |                           |                           |                           |       |
| 3   | Warning   | http://portal.medin.org.u | https://schema.org/citati | Citation information shou | MinCountConstraintCompone | https://oceans.collaboriu | -     |
|     |           | k/portal/json-ld/00040230 | on                        | ld be provided            | nt                        | m.io/voc/validation/1.0.1 |       |
|     |           | -d455-4fea-8747-6179d77ab |                           |                           |                           | /shacl#coreCitation       |       |
|     |           | 103.jsonld                |                           |                           |                           |                           |       |
|     |           |                           |                           |                           |                           |                           |       |
| 4   | Warning   | http://portal.medin.org.u | https://schema.org/variab | variable measured check   | MinCountConstraintCompone | https://oceans.collaboriu | -     |
|     |           | k/portal/json-ld/00040230 | leMeasured                |                           | nt                        | m.io/voc/validation/1.0.1 |       |
|     |           | -d455-4fea-8747-6179d77ab |                           |                           |                           | /shacl#recMesType         |       |
|     |           | 103.jsonld                |                           |                           |                           |                           |       |
|     |           |                           |                           |                           |                           |                           |       |
| 5   | Violation | http://portal.medin.org.u | https://schema.org/variab | At least one PropertyValu | QualifiedMinCountConstrai | https://oceans.collaboriu | -     |
|     |           | k/portal/json-ld/00040230 | leMeasured                | e in variableMeasured mus | ntComponent               | m.io/voc/validation/1.0.1 |       |
|     |           | -d455-4fea-8747-6179d77ab |                           | t have the name 'latitude |                           | /shacl#recLatitude        |       |
|     |           | 103.jsonld                |                           | '.                        |                           |                           |       |
|     |           |                           |                           |                           |                           |                           |       |
| 6   | Violation | http://portal.medin.org.u | https://schema.org/variab | At least one PropertyValu | QualifiedMinCountConstrai | https://oceans.collaboriu | -     |
|     |           | k/portal/json-ld/00040230 | leMeasured                | e in variableMeasured mus | ntComponent               | m.io/voc/validation/1.0.1 |       |
|     |           | -d455-4fea-8747-6179d77ab |                           | t have the name 'latitude |                           | /shacl#recLongitude       |       |
|     |           | 103.jsonld                |                           | '.                        |                           |                           |       |
|     |           |                           |                           |                           |                           |                           |       |
| 7   | Warning   | http://portal.medin.org.u | https://schema.org/measur | measurement method check  | MinCountConstraintCompone | https://oceans.collaboriu | -     |
|     |           | k/portal/json-ld/00040230 | ementMethod               |                           | nt                        | m.io/voc/validation/1.0.1 |       |
|     |           | -d455-4fea-8747-6179d77ab |                           |                           |                           | /shacl#recMesMethod       |       |
|     |           | 103.jsonld                |                           |                           |                           |                           |       |
|     |           |                           |                           |                           |                           |                           |       |
+-----+-----------+---------------------------+---------------------------+---------------------------+---------------------------+---------------------------+-------+%         
```

