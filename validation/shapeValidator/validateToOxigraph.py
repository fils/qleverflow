import sys
import os
from defs.getGraphs import query_sparql_endpoint
from defs.getShape import read_shapefile
from defs.getConstruct import construct_graph
from defs.shaclValidator import validate_with_shacl
import pyoxigraph
from pyoxigraph import RdfFormat
from tqdm import tqdm

def main():
    """
    Main function that takes a URL and shapefile from command line arguments and queries the SPARQL endpoint.
    """

    store = pyoxigraph.Store()  # memory store

    if len(sys.argv) != 3:
        print("Usage: python main.py <url> <shapefile>")
        print("Example: python main.py http://ghost.lan:7007 myshape.ttl")
        sys.exit(1)

    url = sys.argv[1]
    shapefile = sys.argv[2]

    print(f"Querying SPARQL endpoint: {url}")
    print(f"Using shapefile: {shapefile}")

    uris = query_sparql_endpoint(url)

    sf = read_shapefile("../shapes/ERDDAP.ttl")

    if uris:
        print(f"\nFound {len(uris)} unique URIs:")
        # Wrap sorted(uris) with tqdm to create a progress bar
        for uri in tqdm(sorted(uris), desc="Processing URIs"):
            r = construct_graph(uri)
            shr = validate_with_shacl(r, sf)
            try:
                store.load(shr, RdfFormat.TURTLE, base_iri=None, to_graph=None)
            except Exception as e:
                print(f"An error occurred: {e}")
            # print(shr)
    else:
        print("No URIs found or query failed.")

    output = "results.nq"
    store.dump(output, RdfFormat.N_QUADS)


if __name__ == "__main__":
    main()