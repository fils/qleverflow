import gradio as gr
from SPARQLWrapper import SPARQLWrapper, JSON
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re

from defs import usage_info


# Download necessary NLTK data (run once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

sparql = SPARQLWrapper("http://ghost.lan:7007/sparql") # change to your endpoint

def preprocess_search_string(text):
    # 1. Convert to lowercase
    text = text.lower()

    # 2. Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text) # Keep only alphanumeric and whitespace

    # 3. Tokenize the text
    tokens = word_tokenize(text)

    # 4. Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens0 = [word for word in tokens if word not in stop_words]

    # 4.5 Remove words too common to allow like data or resource or others
    common = ['data', 'resource'] # can add things here
    filtered_tokens = [word for word in filtered_tokens0 if word not in common]

    # 5. Stemming (or Lemmatization - see note below)
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]

    # Alternatively, for better accuracy, use lemmatization:
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    # Join the processed tokens back into a string for searching (optional, depends on search engine)
    # processed_string = " ".join(stemmed_tokens) # or lemmatized_tokens below
    processed_string = " ".join(lemmatized_tokens)

    return processed_string

def ss_search(nin):

    n = preprocess_search_string(nin)

    sparql_query = f"""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX gn: <https://www.geonames.org/ontology#>
PREFIX text: <http://jena.apache.org/text#>
PREFIX vrank: <http://purl.org/voc/vrank#>
PREFIX ql: <http://qlever.cs.uni-freiburg.de/builtin-functions/>
PREFIX gn: <https://www.geonames.org/ontology#>

SELECT ?uri ?name (COUNT(?text) AS ?count) (SAMPLE(?item) AS ?example_text)  WHERE {{
  ?uri rdf:type <https://schema.org/Dataset> .
        ?uri <https://schema.org/name> ?name .
    ?uri <https://schema.org/description> ?item .
    ?text ql:contains-entity ?item .
    ?text ql:contains-word "{n}" .
}}
GROUP BY ?uri ?name ?item ?text
ORDER BY DESC(?count)
LIMIT 25
"""

    output = f"<h3>Updated search query: {n}</h3>"

    try:
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        results_list = results["results"]["bindings"]

    except Exception as e:
        return f"<div class='error'>Error executing query: {str(e)}</div>"

    for result in results_list:
        output += f"""
               <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                   <strong>URI:</strong> <a href="{result.get("uri", {}).get("value", "0")}">{result.get("name", {}).get("value", "0")}</a>
                   <br>
                   <br>
                   {result.get("example_text", {}).get("value", "0")[:600]}...
                   <br>
                   <br>
                   {result.get("count", {}).get("value", "0")}

               </div>
               """

        # uri = result.get("uri", {}).get("value", "0")
        # count = result.get("example_text", {}).get("value", "0")

    return output


def combined_search(n):
    # Clear previous color assignments
    # id_colors.clear()

    # text_result = greet(n)
    ss_result = ss_search(n)
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
# light_theme = gr.themes.Soft(
#     primary_hue=gr.themes.colors.blue,
#     secondary_hue=gr.themes.colors.slate,
#     neutral_hue=gr.themes.colors.slate,
# ).set(
#     background_fill_primary='*neutral_50',
#     background_fill_secondary='*neutral_100',
#     block_background_fill='white',
#     input_background_fill='white'
# )

with gr.Blocks(title="SPARQL text index search testing tool",  theme=gr.themes.Soft()) as demo:
    gr.Markdown("# SPARQL text index search testing tool")

    with gr.Tab("Text Index Search"):
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
        greet_button = gr.Button("This service is not wired up")
        greeting_output = gr.Markdown(label="Response")

        # greet_button.click(fn=chat_search, inputs=name_input, outputs=greeting_output)

    with gr.Tab("About & Examples"):
        gr.HTML(usage_info.about())

if __name__ == "__main__":
    demo.launch()
