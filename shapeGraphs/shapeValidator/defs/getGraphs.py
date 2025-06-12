import requests
import json
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://ghost.lan:7007/sparql")


def query_sparql_endpoint(url):
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

    sparql_query = "SELECT * WHERE { graph ?g { ?s a <https://schema.org/Dataset> } } LIMIT 1000"

    try:
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        predicates = [result["g"]["value"] for result in results["results"]["bindings"]]

        return predicates

    except KeyError as e:
        print(f"Unexpected response structure: {e}")
        return []

# Example usage:
# uris = query_sparql_endpoint("http://ghost.lan:7007")
# print(uris)