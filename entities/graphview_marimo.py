import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import rdflib
    import networkx as nx
    import matplotlib.pyplot as plt
    from collections import defaultdict
    import random  # For random colors if needed
    import pandas as pd
    return defaultdict, nx, pd, random, rdflib


@app.cell
def _(rdflib):
    # Create an RDF graph and parse the NT file
    graph = rdflib.Graph()
    graph.parse("./graphs/entityGraph-20-1-2026.nt", format='nt')
    return (graph,)


@app.cell
def _():
    sparql_query = """
    PREFIX schema: <http://schema.org/>

    SELECT DISTINCT ?description ?apname ?apvalue
    WHERE {
        ?s schema:description ?description .
        ?s schema:additionalProperty ?ap .
        ?ap schema:name ?apname .
        ?ap schema:value ?apvalue
    }
    """
    return (sparql_query,)


@app.cell
def _(graph, sparql_query):
    # Execute the SPARQL query
    results = graph.query(sparql_query)
    return (results,)


@app.cell
def _(results):
    # for row in results:
    #     print(str(row.description))
    print(len(results))
    return


@app.cell
def _(defaultdict, nx, random, results):

    # Build the graph
    G = nx.Graph()

    # Track unique nodes and edge labels
    entity_nodes = set()
    value_nodes = set()
    apname_colors = defaultdict(lambda: f'#{random.randint(0, 0xFFFFFF):06x}')  # Assign colors to apnames

    for row in results:
        # desc = row['description']
        apname = row['apname']
        apvalue = row['apvalue']

        # Add nodes with attributes
        G.add_node(apname, type='variable', label=apname)
        G.add_node(apvalue, type='value', label=apvalue)

        # Add edge with label and color based on apname
        G.add_edge(apname, apvalue, label='has_value', color=apname_colors[apname])

        entity_nodes.add(apname)
        value_nodes.add(apvalue)

    # Force-directed layout (optional, for initial positions if desired in Gephi)
    pos = nx.spring_layout(G, seed=42, k=0.15, iterations=50)
    return (G,)


@app.cell
def _(G, nx):

    # Export to GEXF format for Gephi
    nx.write_gexf(G, 'sparql_graph.gexf')
    print("Graph exported to 'sparql_graph.gexf' for opening in Gephi.")

    # nx.write_graphml(G, 'sparql_graph.graphml')
    nx.write_gml(G, 'sparql_graph.gml')
    return


@app.cell
def _():

    # # # Optional: Draw the graph in Matplotlib (as before)
    # plt.figure(figsize=(12, 8))
    # nx.draw_networkx_nodes(G, pos, nodelist=entity_nodes, node_color='lightblue', node_size=500, label='Entities')
    # nx.draw_networkx_nodes(G, pos, nodelist=value_nodes, node_color='lightgreen', node_size=300, label='Values')
    # edges = G.edges(data=True)
    # edge_colors = [edge[2]['color'] for edge in edges]
    # nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v, d in edges], edge_color=edge_colors, width=2)
    # edge_labels = {(u, v): d['label'] for u, v, d in edges}
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    # nx.draw_networkx_labels(G, pos, {n: G.nodes[n]['label'] for n in G.nodes()}, font_size=10)
    # plt.title('Force-Directed Graph of SPARQL Results')
    # plt.legend()
    # plt.axis('off')
    # # plt.tight_layout()
    # plt.show()  # Or plt.savefig('graph.png') to save as image
    return


@app.cell
def _(G, nx):
    # density

    density = nx.density(G)
    print(density)

    # This is a very sparse graph which is what we would likely expect.  
    # We would not expect anything else.  We would not expect every EOV to be connected to every value recorded.  
    return


@app.cell
def _(G, nx, pd):
    # Pagerank
    pageranks = nx.pagerank(G)
    pagerank_df = pd.DataFrame.from_dict(pageranks, orient="index", columns=["pagerank"])

    return (pagerank_df,)


@app.cell
def _(pagerank_df):
    pagerank_df.sort_values(by="pagerank", ascending=False).head(20)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
