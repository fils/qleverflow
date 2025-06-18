import requests
import json
from SPARQLWrapper import SPARQLWrapper, JSON, TSV, CSV, RDF, TURTLE

sparql = SPARQLWrapper("http://ghost.lan:7007/sparql")

def construct_graph(url):
    """
    Query a SPARQL endpoint (QLever) and return a list of URIs from the response.

    Args:
        url (str): The URL of the SPARQL endpoint
        sparql_query (str): The SPARQL query to execute

    Returns:
        list: A list of unique URIs found in the query results
    """
    headers = {
        "Accept": "application/qlever-results+json",
        "Content-type": "application/sparql-query"
    }

    sparql_query = f"""
    CONSTRUCT {{
  ?s ?p ?o
}}
WHERE {{
  GRAPH <{url}> {{
    {{
      ?s ?p ?o
    }}
  }}
}}
"""

    try:
        sparql.setReturnFormat(TURTLE)
        # Set the content type header
        sparql.addCustomHttpHeader("Content-Type", "application/sparql-query")
        # Optionally set the Accept header as well
        # sparql.addCustomHttpHeader("Accept", "text/tab-separated-values")
        sparql.setQuery(sparql_query)
        results = sparql.query().convert()
        return results

    except KeyError as e:
        print(f"Unexpected response structure: {e}")
        return []

# Example usage:
# uris = query_sparql_endpoint("http://ghost.lan:7007")
# print(uris)