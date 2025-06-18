import gradio as gr
import lancedb
import random
from rich.console import Console
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import EmbeddingFunctionRegistry
from SPARQLWrapper import SPARQLWrapper, JSON

from defs import usage_info

sparql = SPARQLWrapper("http://ghost.lan:7007/sparql")


def ss_search(n, db):
    # model = SentenceTransformer('all-MiniLM-L6-v2')
    # table = db.open_table("my_embeddings")

    # search_embedding = model.encode([n])[0]  # We get the first (and only) embedding
    # results = table.search(search_embedding.tolist()).limit(10).to_list()  # or to_pandas()
    sparql_query = "SELECT * WHERE { graph ?g { ?s a <https://schema.org/Dataset> } } LIMIT 100"

    output = f"<h3>Semanitc similarity results: {n}</h3>"

    try:
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        predicates = [result["g"]["value"] for result in results["results"]["bindings"]]

    except KeyError as e:
        print(f"Unexpected response structure: {e}")

    for result in predicates:
        # background_color = get_color_for_id(result['id'])
        output += f"""
        <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
            <strong>Predicate:</strong> {result}<br>
         
        </div>
        """

    return output


def combined_search(n):
    # Clear previous color assignments
    # id_colors.clear()

    # set up elements
    uri = "data/sample-lancedb"
    db = lancedb.connect(uri)

    # text_result = greet(n, db)
    ss_result = ss_search(n, db)
    return ss_result


def extract_context(rows):
    return sorted(
        [
            {"id": r['id'], "text": r['text'], "index": r['_distance']}
            for r in rows
        ],
        key=lambda x: x['id']
    )


# Create a true light theme with lite tones
light_theme = gr.themes.Soft(
    primary_hue=gr.themes.colors.blue,
    secondary_hue=gr.themes.colors.gray,
    neutral_hue=gr.themes.colors.gray
)

with gr.Blocks(title="ODIS SPARQL text index search", theme=light_theme) as demo:
    gr.Markdown("# ODIS SPARQL text index search")

    with gr.Tab("Comparative Search"):
        name = gr.Textbox(label="Search Phrase")
        greet_btn = gr.Button("Search")

        with gr.Row():
            with gr.Column(scale=2):
                output1 = gr.HTML(label="Text Search")
            # with gr.Column(scale=2):
            #     output2 = gr.HTML(label="Semantic Similarity")

        greet_btn.click(fn=combined_search, inputs=name, outputs=[output1], api_name="combined_search")

    with gr.Tab("Chat"):
        name_input = gr.Textbox(label="Enter your question")
        greet_button = gr.Button("LLM RAG query")
        greeting_output = gr.Markdown(label="Response")

        # greet_button.click(fn=chat_search, inputs=name_input, outputs=greeting_output)

    with gr.Tab("About & Examples"):
        gr.HTML(usage_info.about())

if __name__ == "__main__":
    demo.launch()
