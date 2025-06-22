import sys
import os
import lancedb
from defs.getGraphs import query_sparql_endpoint
from defs.getShape import read_shapefile
from defs.getConstruct import construct_graph
from defs.shaclValidator import validate_with_shacl, validate_with_shacl_simple
from lancedb.pydantic import Vector, LanceModel
from pyoxigraph import RdfFormat
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

DEFAULT_TABLE_NAME = 'shaclresults'

MODEL_NAME = 'all-MiniLM-L6-v2'
model = SentenceTransformer(MODEL_NAME)
VECTOR_DIM = model.get_sentence_embedding_dimension()

# Severity, Source Shape, Focus Node, ResultPath, Message
class WikipediaSchema(LanceModel):
    emb: Vector(VECTOR_DIM) # This stores vector embedding
    identifier: int # This is an id for the chunk
    chunk_index: int # This is the chunk number of the context
    content: str # The content of the chunk
    url: str # The link to the article
    title: str # The title of the article

def get_or_create_table(table_name: str = None):
    """Get an existing table or create a new one if it doesn't exist."""
    db = get_db_connection()
    table_name = table_name or DEFAULT_TABLE_NAME

    try:
        return db.open_table(table_name)
    except Exception:
        return db.create_table(table_name, schema=WikipediaSchema)

def get_db_connection():
    uri = "store/val-lancedb"
    return lancedb.connect(uri)

def main():
    """
    Main function that takes a URL and shapefile from command line arguments and queries the SPARQL endpoint.
    """

    db = get_db_connection()
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # table = db.create_table("my_embeddings", data=[
    #     {"id": id_value,
    #      "text": text,
    #      "vector": embedding.tolist()}
    #     for id_value, (text, embedding) in zip(ids, (zip(texts, embeddings)))
    # ])

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

            # TODO  rather than Lance, could just go into parquet too.
            # We have the graph URI to associate with the SHACL results
            # and either would work.

            # TODO likely write to Polars then batch into Lance?
            # OR into arrow table then to Lance (or Polars - Parquet)

            # print(shr)
            # try:
            #     store.load(shr, RdfFormat.TURTLE, base_iri=None, to_graph=None)
            # except Exception as e:
            #     print(f"An error occurred: {e}")
            # print(shr)
    else:
        print("No URIs found or query failed.")

    # these 2 lines will end up being a save to parquet stage
    # output = "results.nq"
    # store.dump(output, RdfFormat.N_QUADS)


if __name__ == "__main__":
    main()