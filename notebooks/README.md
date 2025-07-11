# Notebooks

## About

Just some playing around with visualizations on the graph.

![graph.png](../docs/images/graph.png)


```sparql
PREFIX pathSearch: <https://qlever.cs.uni-freiburg.de/pathSearch/>
PREFIX schema: <https://schema.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?start ?pred ?end ?source ?path ?edge ?target ?start_name
WHERE {
  SERVICE pathSearch: {
    _:path pathSearch:algorithm pathSearch:allPaths ;
           pathSearch:source ?source ;
           pathSearch:target ?target ;
		   pathSearch:edgeProperty ?pred ;
           pathSearch:pathColumn ?path ;
           pathSearch:edgeColumn ?edge ;
           pathSearch:start ?start ;
           pathSearch:end ?end ;
    {
      SELECT * WHERE {
	   VALUES ?pred {<https://schema.org/keywords>}
        ?start ?pred ?end .
      }
    }
  }
    OPTIONAL {?start schema:name ?start_name .}
}
```
