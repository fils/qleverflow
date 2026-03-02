import gradio as gr
import pandas as pd
import plotly.express as px
from SPARQLWrapper import SPARQLWrapper, JSON
import os
import yaml

class Dashboard:
    def __init__(self, sparql_endpoint, config_path="ui/dashboard_config.yaml"):
        self.sparql = SPARQLWrapper(sparql_endpoint)
        self.config_path = config_path
        self.queries = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            # Default config if file doesn't exist
            default_config = [
                {
                    "id": "entity_count",
                    "name": "Entity Count by Predicate",
                    "query": "PREFIX ql: <http://qlever.cs.uni-freiburg.de/builtin-functions/>\nSELECT ?entity (COUNT(?predicate) AS ?count) WHERE {\n  ?entity ql:has-predicate ?predicate\n}\nGROUP BY ?entity \nORDER BY DESC(?count)\nLIMIT 10",
                    "type": "bar",
                    "x": "entity",
                    "y": "count"
                },
                {
                    "id": "count_by_type",
                    "name": "Count by Schema Type",
                    "query": "PREFIX schema: <https://schema.org/>\nSELECT ?type (COUNT(?entity) AS ?count) WHERE {\n  ?entity a ?type .\n  VALUES ?type {\n    schema:Dataset\n    schema:Person\n    schema:Map\n    schema:Organization\n    schema:Project\n  }\n}\nGROUP BY ?type\nORDER BY DESC(?count)",
                    "type": "pie",
                    "names": "type",
                    "values": "count"
                },
                {
                    "id": "predicate_count",
                    "name": "Predicate Distribution (Datasets)",
                    "query": "PREFIX schema: <https://schema.org/>\nPREFIX ql: <http://qlever.cs.uni-freiburg.de/builtin-functions/>\nSELECT ?predicate (COUNT(?predicate) as ?count) WHERE {\n  ?x a schema:Dataset .\n  ?x ql:has-predicate ?predicate\n}\nGROUP BY ?predicate\nORDER BY DESC(?count)\nLIMIT 15",
                    "type": "table"
                }
            ]
            # Save default config to file
            with open(self.config_path, 'w') as f:
                yaml.dump(default_config, f)
            return default_config

    def run_query(self, query_str):
        self.sparql.setQuery(query_str)
        self.sparql.setReturnFormat(JSON)
        try:
            results = self.sparql.query().convert()
            bindings = results["results"]["bindings"]

            data = []
            for b in bindings:
                row = {k: v["value"] for k, v in b.items()}
                data.append(row)

            df = pd.DataFrame(data)
            if not df.empty and "count" in df.columns:
                df["count"] = pd.to_numeric(df["count"])
            return df
        except Exception as e:
            print(f"Error running query: {e}")
            return pd.DataFrame()

    def create_visualization(self, config, df):
        if df.empty:
            return gr.Markdown("No data found or error in query.")

        viz_type = config.get("type", "table")

        if viz_type == "bar":
            fig = px.bar(df, x=config["x"], y=config["y"], title=config["name"])
            return gr.Plot(fig)
        elif viz_type == "pie":
            fig = px.pie(df, names=config["names"], values=config["values"], title=config["name"])
            return gr.Plot(fig)
        else:
            return gr.Dataframe(df, label=config["name"])

    def refresh_dashboard(self):
        outputs = []
        for q in self.queries:
            df = self.run_query(q["query"])
            outputs.append(df)
        return outputs

def create_dashboard_tab(sparql_endpoint):
    db = Dashboard(sparql_endpoint)

    with gr.Tab("Dashboard"):
        gr.Markdown("## Graph Statistics Dashboard")
        refresh_btn = gr.Button("Refresh Dashboard")

        # Single container that rebuilds all visualizations
        output_container = gr.HTML()
        plot_outputs = [gr.Plot(visible=False) for _ in range(10)]  # Hidden plot slots
        table_output = gr.Dataframe()

        @gr.render(triggers=[refresh_btn.click])
        def render_dashboard():
            db.queries = db.load_config()
            for q in db.queries:
                df = db.run_query(q["query"])
                gr.Markdown(f"### {q['name']}")
                if df.empty:
                    gr.Markdown("*No data found*")
                elif q["type"] == "bar":
                    gr.Plot(px.bar(df, x=q["x"], y=q["y"], title=q["name"]))
                elif q["type"] == "pie":
                    gr.Plot(px.pie(df, names=q["names"], values=q["values"], title=q["name"]))
                else:
                    gr.Dataframe(df)

    return db
