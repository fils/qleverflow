import gradio as gr
from SPARQLWrapper import SPARQLWrapper, JSON
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re

from defs import usage_info
from dashboard import create_dashboard_tab

import polars as pl
import plotly.express as px
import pandas as pd
from shapely import wkt

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("punkt_tab")

sparql = SPARQLWrapper("http://workstation.lan:7007/sparql")


def preprocess_search_string(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    filtered_tokens0 = [word for word in tokens if word not in stop_words]
    common = ["data", "resource"]
    filtered_tokens = [word for word in filtered_tokens0 if word not in common]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
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
    output = f"""
     <h3>Updated search: {n}</h3>
     """
    try:
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        results_list = results["results"]["bindings"]
    except Exception as e:
        return f"<div class='error'>Error executing query: {str(e)}</div>"
    print(len(results_list))
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
    return output


def combined_search(n):
    ss_result = ss_search(n)
    return ss_result


def get_mock_ocean_data():
    return pl.DataFrame(
        {
            "location": [
                "POINT(-74.0 40.7)",
                "POINT(-118.2 34.0)",
                "POLYGON((-122.4 37.8, -122.4 37.7, -122.3 37.7, -122.3 37.8, -122.4 37.8))",
            ],
            "depth": [100, 250, 50],
            "name": ["Atlantic Site", "Pacific Site", "Bay Area Polygon"],
        }
    )


def plot_map(wkt_input, depth_filter):
    df = get_mock_ocean_data()
    filtered_df = df.filter(pl.col("depth") > depth_filter)
    lats = []
    lons = []
    names = []
    depths = []
    polygons = []
    for row in filtered_df.iter_rows(named=True):
        try:
            geom = wkt.loads(row["location"])
            if geom.geom_type == "Point":
                lons.append(geom.x)
                lats.append(geom.y)
                names.append(row["name"])
                depths.append(row["depth"])
                polygons.append(None)
            elif geom.geom_type == "Polygon":
                centroid = geom.centroid
                lons.append(centroid.x)
                lats.append(centroid.y)
                names.append(row["name"])
                depths.append(row["depth"])
                polygons.append(geom)
        except Exception:
            pass
    if wkt_input:
        try:
            geom = wkt.loads(wkt_input)
            if geom.geom_type == "Point":
                lons.append(geom.x)
                lats.append(geom.y)
                names.append("Custom")
                depths.append(0)
                polygons.append(None)
            elif geom.geom_type == "Polygon":
                centroid = geom.centroid
                lons.append(centroid.x)
                lats.append(centroid.y)
                names.append("Custom")
                depths.append(0)
                polygons.append(geom)
        except Exception:
            pass
    plot_df = pd.DataFrame({"lat": lats, "lon": lons, "name": names, "depth": depths})
    fig = px.scatter_geo(
        plot_df,
        lat="lat",
        lon="lon",
        color="depth",
        hover_name="name",
        projection="orthographic",
    )
    for i, poly in enumerate(polygons):
        if poly is not None:
            poly_lons, poly_lats = poly.exterior.coords.xy
            fig.add_scattergeo(
                lon=list(poly_lons),
                lat=list(poly_lats),
                mode="lines",
                fill="toself",
                fillcolor="blue",
                opacity=0.5,
                line=dict(color="blue"),
                name=names[i],
                showlegend=False,
            )
    return fig


def extract_context(rows):
    return sorted(
        [{"id": r["id"], "text": r["text"], "index": r["_distance"]} for r in rows],
        key=lambda x: x["id"],
    )


with gr.Blocks(title="SPARQL text index search testing tool") as demo:
    gr.Markdown("# SPARQL text index search testing tool")

    with gr.Tab("Text Index Search"):
        name = gr.Textbox(label="Search Phrase")
        greet_btn = gr.Button("Search")

        with gr.Row():
            with gr.Column(scale=2):
                output1 = gr.HTML(label="Text Search")

        greet_btn.click(
            fn=combined_search,
            inputs=name,
            outputs=[output1],
            api_name="combined_search",
        )

    create_dashboard_tab("http://workstation.lan:7007/sparql")

    with gr.Tab("Chat"):
        name_input = gr.Textbox(label="Enter your question")
        greet_button = gr.Button("This service is not wired up")
        greeting_output = gr.Markdown(label="Response")

    with gr.Tab("About & Examples"):
        gr.HTML(usage_info.about())

    with gr.Tab("Map View"):
        wkt_input = gr.Textbox(label="Custom WKT")
        depth_filter = gr.Slider(label="Min Depth", minimum=0, maximum=500, value=0)
        plot_btn = gr.Button("Plot Map")
        map_output = gr.Plot()
        plot_btn.click(
            fn=plot_map, inputs=[wkt_input, depth_filter], outputs=map_output
        )

    demo.launch(
        server_name="0.0.0.0",
    )

if __name__ == "__main__":
    demo.launch()
