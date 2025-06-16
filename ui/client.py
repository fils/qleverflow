import gradio as gr
import lancedb
from sentence_transformers import SentenceTransformer
import random
from ollama import Client
from rich.console import Console
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import EmbeddingFunctionRegistry

from defs import usage_info

# Global dictionary to store colors for IDs
id_colors = {}

def get_color_for_id_grey(id):
    if id not in id_colors:
        # Generate a shade of grey
        # We'll use values between 220 and 240 to ensure light shades
        # that don't interfere with text readability
        grey_value = random.randint(10, 110)
        id_colors[id] = f"rgb({grey_value},{grey_value},{grey_value})"
    return id_colors[id]

def get_color_for_id(id):
    if id not in id_colors:
        # Generate a light, pastel color
        r = random.randint(5, 150)
        g = random.randint(5, 150)
        b = random.randint(5, 150)
        id_colors[id] = f"rgb({r},{g},{b})"
    return id_colors[id]

def greet(n, db):
    table = db.open_table("my_embeddings")

    results = table.search(n).limit(10).select(["id", "text"]).to_list()

    output = f"<h3>Full text index results for '{n}':</h3>"
    for result in results:
        background_color = get_color_for_id(result['id'])
        output += f"""
        <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; background-color: {background_color};">
            <strong>ID:</strong> {result['id']}<br>
            <strong>Text:</strong> {result['text']}<br>
            <strong>Score:</strong> {result['_score']}
        </div>
        """

    return output

def ss_search(n, db):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    table = db.open_table("my_embeddings")

    search_embedding = model.encode([n])[0]  # We get the first (and only) embedding
    results = table.search(search_embedding.tolist()).limit(10).to_list()  # or to_pandas()

    output = f"<h3>Semanitc similarity results for '{n}':</h3>"
    for result in results:
        background_color = get_color_for_id(result['id'])
        output += f"""
        <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; background-color: {background_color};">
            <strong>ID:</strong> {result['id']}<br>
            <strong>Text:</strong> {result['text']}<br>
            <strong>Distance:</strong> {result['_distance']}
        </div>
        """

    return output

# ref: https://github.com/lancedb/vectordb-recipes/blob/main/examples/Hybrid_search_bm25_lancedb/main.ipynb

def hybrid_Search(n, db):
    # Initialize the BM25 retriever
    bm25_retriever = BM25Retriever.from_documents(pages)
    bm25_retriever.k = 2  # Retrieve top 2 results

    print("type of bm25", type(bm25_retriever))

    # Initialize LanceDB retriever
    docsearch = LanceDB.from_documents(pages, embedding, connection=db)
    retriever_lancedb = docsearch.as_retriever(search_kwargs={"k": 2})

    # Initialize the ensemble retriever
    ensemble_retriever = EnsembleRetriever( retrievers=[bm25_retriever, retriever_lancedb], weights=[0.2, 0.8])

    results = ensemble_retriever.get_relevant_documents(query)


def combined_search(n):
    # Clear previous color assignments
    id_colors.clear()

    # set up elements
    uri = "data/sample-lancedb"
    db = lancedb.connect(uri)

    text_result = greet(n, db)
    ss_result = ss_search(n, db)
    return text_result, ss_result


# CHAT Section
# registry = EmbeddingFunctionRegistry.get_instance()
# embedder = registry.get("ollama").create(name="mxbai-embed-large")
model = SentenceTransformer('all-MiniLM-L6-v2')
#
# class Schema(LanceModel):
#     id: str
#     text: str = embedder.SourceField()
#     vector: Vector(embedder.ndims()) = embedder.VectorField()

def extract_context(rows):
    return sorted(
        [
            {"id": r['id'], "text": r['text'], "index": r['_distance']}
            for r in rows
        ],
        key=lambda x: x['id']
    )

def chat_search(n):
    # set up elements
    uri = "data/sample-lancedb"
    db = lancedb.connect(uri)

    client = Client(host='http://192.168.202.88:11434')

    SYSTEM = """
    You will receive paragraphs of text from a news article.
    Answer the subsequent question using that context.  Try to cite your sources using the "id" field and
    provide a coherent response but do not feel obligated to use all the context items.
    """

    search_text = n
    table = db.open_table("my_embeddings")

    search_embedding = model.encode([search_text])[0]  # We get the first (and only) embedding
    results = table.search(search_embedding.tolist()).limit(10).to_list()  # or to_pandas()

    # rows = (table.search(question).limit(5).to_pydantic(Schema))  # AH!   here is the cast to pydantic vrs to list.
    # context = extract_context(rows)
    context = extract_context(results)
    stream = client.chat(
        model="llama3.1", stream=False,
        messages=[
            {"role": "system", 'content': SYSTEM},
            {"role": "user", 'content': f"Context: {context}"},
            {"role": "user", 'content': f"Question: {search_text}"}
        ]
    )
    # for chunk in stream:
    #     print(chunk['message']['content'], end='', flush=True)

    return stream['message']['content']


# Create a true light theme with lite tones
light_theme = gr.themes.Soft(
    primary_hue=gr.themes.colors.blue,
    secondary_hue=gr.themes.colors.gray,
    neutral_hue=gr.themes.colors.gray
)

with gr.Blocks(title="OHDSI Catalog Explorer", theme=light_theme) as demo:
    gr.Markdown("# OHDSI Catalog Explorer")

    with gr.Tab("Comparative Search"):
        name = gr.Textbox(label="Search Phrase")
        greet_btn = gr.Button("Search")

        with gr.Row():
            with gr.Column(scale=2):
                output1 = gr.HTML(label="Text Search")
            with gr.Column(scale=2):
                output2 = gr.HTML(label="Semantic Similarity")

        greet_btn.click(fn=combined_search, inputs=name, outputs=[output1, output2], api_name="combined_search")

    with gr.Tab("Chat"):
        name_input = gr.Textbox(label="Enter your question")
        greet_button = gr.Button("LLM RAG query")
        greeting_output = gr.Markdown(label="Response")

        greet_button.click(fn=chat_search, inputs=name_input, outputs=greeting_output)

    with gr.Tab("About & Examples"):
        gr.HTML(usage_info.about())



if __name__ == "__main__":
    demo.launch()


