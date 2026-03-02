import sys
import os
import json
from rdflib import Graph
from tqdm import tqdm
from gliner2 import GLiNER2
import pyoxigraph
from pyoxigraph import RdfFormat

from defs.getGraphs import query_sparql_endpoint
from defs.getConstruct import construct_graph
from defs.getDescriptions import get_descriptions
from defs.getEntities import entities
from defs.entities2RDF import generate_jsonld

def main():
    """
    Main function that takes a URL and shapefile from command line arguments and queries the SPARQL endpoint.
    """

    extractor = GLiNER2.from_pretrained("fastino/gliner2-large-v1")
    store = pyoxigraph.Store()  # memory store

    if len(sys.argv) != 2:
        print("Usage: python main_er.py <url>")
        print("Example: python main.py http://ghost.lan:7007")
        sys.exit(1)

    url = sys.argv[1]

    print(f"Querying SPARQL endpoint: {url}")
    uris = query_sparql_endpoint(url)

    if uris:
        print(f"\nFound {len(uris)} unique URIs:")
        # Wrap sorted(uris) with tqdm to create a progress bar
        for uri in tqdm(sorted(uris), desc="Processing URIs"):
            # r = construct_graph(uri)
            r = get_descriptions(uri)
            has_entities = True
            er_list = []
            for subj, desc_list in r.items():
                for desc in desc_list:
                    er = entities(extractor, desc)
                    er = json.loads(er)
                    if not er.get('entities'):
                        has_entities = False
                        break
                    er_list.append(er)
                if not has_entities:
                    break
            if has_entities:
                for er in er_list:
                    # pretty = json.dumps(er, indent=4)
                    # print(pretty)

                    jld = generate_jsonld(er, uri)

                    # pretty = json.dumps(jld, indent=4)
                    # print(jld)

                    try:
                        # Use rdflib to parse JSON-LD and convert to N-Triples
                        g = Graph()
                        g.parse(data=jld, format='json-ld')

                        # Serialize to N-Triples (or N-Quads)
                        ntriples = g.serialize(format='nt')

                        # Load N-Triples into pyoxigraph store
                        store.load(ntriples.encode('utf-8'), RdfFormat.N_TRIPLES, base_iri=None, to_graph=None)
                    except Exception as e:
                        print(f"An error occurred: {e}")

    else:
        print("No URIs found or query failed.")

    output = "entityGraph.nt"
    store.dump(output, RdfFormat.N_QUADS)
    print("Processing complete")

if __name__ == "__main__":
    main()
