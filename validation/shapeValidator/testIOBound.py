import sys
import os
from defs.getGraphs import query_sparql_endpoint
from defs.getShape import read_shapefile
from defs.getConstruct import construct_graph
from defs.shaclValidator import validate_with_shacl
import pyoxigraph
from pyoxigraph import RdfFormat
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed # Import these

def process_uri(uri, sf):
    """
    Helper function to process a single URI, to be used with concurrent.futures.
    """
    r = construct_graph(uri)
    shr = validate_with_shacl(r, sf)
    return shr

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

    # Note: If ERDDAP.ttl is large, consider reading it once outside the loop
    sf = read_shapefile("../shapes/ERDDAP.ttl")

    if uris:
        print(f"\nFound {len(uris)} unique URIs:")
        # Determine an appropriate max_workers. A good starting point might be 2x or 4x the number of CPU cores
        # or adjust based on how many concurrent network requests your SPARQL endpoint can handle.
        max_workers = os.cpu_count() * 2 if os.cpu_count() else 4 # Example: 2x CPU cores, min 4

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks and get future objects
            future_to_uri = {executor.submit(process_uri, uri, sf): uri for uri in sorted(uris)}

            # Use tqdm to show progress as tasks complete
            for future in tqdm(as_completed(future_to_uri), total=len(uris), desc="Processing URIs"):
                shr = future.result() # Get the result of the completed task
                try:
                    store.load(shr, RdfFormat.TURTLE, base_iri=None, to_graph=None)
                except Exception as e:
                    print(f"An error occurred: {e}")
    else:
        print("No URIs found or query failed.")

    output = "resultsIOBound.nq"
    store.dump(output, RdfFormat.N_QUADS)

if __name__ == "__main__":
    main()
