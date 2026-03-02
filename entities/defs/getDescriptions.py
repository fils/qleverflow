from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://ghost.lan:7007/sparql")


def get_descriptions(url):
    sparql_query = f"""
    SELECT ?s ?description
    WHERE {{
      GRAPH <{url}> {{
        ?s a <https://schema.org/Dataset> .
        ?s <https://schema.org/description> ?description .
      }}
    }}
    """

    try:
        sparql.setReturnFormat(JSON)
        sparql.addCustomHttpHeader("Content-Type", "application/sparql-query")
        sparql.setQuery(sparql_query)
        results = sparql.query().convert()
        descs = {}
        for binding in results["results"]["bindings"]:
            s = binding["s"]["value"]
            d = binding["description"]["value"]
            if s not in descs:
                descs[s] = []
            descs[s].append(d)
        return descs

    except Exception as e:
        print(f"Error: {e}")
        return {}
