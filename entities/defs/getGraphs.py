from SPARQLWrapper import SPARQLWrapper, JSON

def query_sparql_endpoint(url):
    """
    Query a SPARQL endpoint (QLever) and return a list of URIs from the response.

    Args:
        url (str): The URL of the SPARQL endpoint (e.g., "http://ghost.lan:7007/sparql").

    Returns:
        list: A list of unique URIs found in the query results
    """
    sparql = SPARQLWrapper(url)
    sparql_query = (
        "SELECT * WHERE { graph ?g { ?s a <https://schema.org/Dataset> } } LIMIT 150000"
    )


    try:
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        # Handle None and extract in one go
        graphs = [
            result["g"]["value"]
            for result in (results or {}).get("results", {}).get("bindings", [])
            if "g" in result and "value" in result["g"]
        ]
        return graphs
    except Exception as e:
        print(f"Error querying SPARQL endpoint: {e}")
        return []
