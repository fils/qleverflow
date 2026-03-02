# Entities Directory Overview

This directory contains Python scripts for entity extraction and RDF processing related to marine biodiversity datasets. It uses tools like SPARQL, GLiNER2, pyoxigraph, and langextract to query endpoints, extract entities from descriptions, and generate RDF graphs.

Entity Resolution: Merging structured datasets using the Senzing SDK.

Semantic Layer: Building a domain taxonomy and ontology.

Content Processing: Crawling and parsing unstructured text (e.g., news articles) to extract entities.

Human-in-the-Loop (HITL): (Planned) A step for human curation of extracted entities.


Looking at this step in the workflow, in essence we’re “building up” from a ground floor of structured data and unstructured content in the form of resource descriptons., leveraging domain context and computable semantics as much as possible to make definitions clearer. This diagram illustrates the process of “building up” in layers.



## Scripts

### graphview_marimo.py
- **Description**: A Marimo notebook that loads an RDF graph from an NT file, queries for dataset descriptions and properties, builds a NetworkX graph of entities and values, exports to GEXF/GML formats, and computes graph metrics like density and PageRank.
- **How it works**: Parses NT file with rdflib, runs SPARQL query, constructs graph with nodes/edges colored by property names, exports files, and analyzes with NetworkX.
- **Input**: NT file path (hardcoded: "./graphs/entityGraph-20-1-2026.nt").
- **Output**: Graph files (sparql_graph.gexf, sparql_graph.gml), printed metrics, optional visualization.

### defs/getGraphs.py
- **Description**: Queries a SPARQL endpoint to retrieve unique graph URIs containing schema:Dataset instances.
- **How it works**: Uses SPARQLWrapper to execute a SELECT query with LIMIT 150000, extracts graph values from JSON results.
- **Input**: SPARQL endpoint URL.
- **Output**: List of unique graph URIs.

### defs/getEntities.py
- **Description**: Extracts entities from text using GLiNER2 model with predefined marine biodiversity categories (e.g., person, geospatial region, species).
- **How it works**: Loads GLiNER2 model, extracts entities with detailed prompts for each category, filters empty results, adds original text to output.
- **Input**: Text string and extractor instance.
- **Output**: JSON string with entities grouped by category and the original description.

### results.py
- **Description**: Contains a large list of ExampleData objects for entity extraction training/prompting, focused on marine biodiversity contexts.
- **How it works**: Defines static data with text samples and annotated extractions for categories like policies, species, regions.
- **Input/Output**: Not executable; serves as data for other scripts (e.g., langExtracttest.py).

### doQuery.py
- **Description**: Executes a SPARQL query on an NT RDF file to group dataset descriptions and properties, then generates Python code for extraction examples.
- **How it works**: Parses NT with rdflib, queries for descriptions and additional properties, groups results, outputs formatted Python list code avoiding duplicates.
- **Input**: Paths to query file and NT RDF file via command-line args.
- **Output**: Printed Python code string representing grouped examples.

### langExtracttest.py
- **Description**: Tests entity extraction on a sample marine dataset description using langextract library, groups results, saves to JSONL, and generates HTML visualization.
- **How it works**: Loads OpenAI model via langextract, extracts business-like entities (adapted for marine context), groups by class, writes files.
- **Input**: Hardcoded sample text (marine dataset description).
- **Output**: Printed grouped entities, extraction_results.jsonl, visualization.html.

### main_er.py
- **Description**: Main pipeline script that queries SPARQL for graphs, extracts descriptions, performs entity recognition with GLiNER2, generates JSON-LD, loads into pyoxigraph, and dumps to NT file.
- **How it works**: Iterates over graph URIs, gets descriptions, extracts entities if present, converts to RDF via JSON-LD, stores triples, exports quads.
- **Input**: SPARQL endpoint URL via command-line arg.
- **Output**: entityGraph.nt file containing processed RDF quads.

### defs/entities2RDF.py
- **Description**: Converts extracted entities JSON to schema.org JSON-LD format for datasets.
- **How it works**: Maps entity categories to PropertyValue structures under additionalProperty, includes description and URI.
- **Input**: Entities JSON (dict or string) and dataset URI.
- **Output**: JSON-LD string.

### defs/getDescriptions.py
- **Description**: Queries a SPARQL endpoint for descriptions of Datasets in a specific named graph.
- **How it works**: Executes SELECT query via SPARQLWrapper, groups descriptions by subject URI from JSON results.
- **Input**: Named graph URI.
- **Output**: Dictionary of subject URIs to lists of descriptions.

### defs/getConstruct.py
- **Description**: Performs a SPARQL CONSTRUCT query to retrieve all triples from a named graph.
- **How it works**: Uses SPARQLWrapper to construct and return Turtle-serialized graph content.
- **Input**: Named graph URI.
- **Output**: Bytes of Turtle RDF data or empty on error.

## Usage
- Run `main_er.py` with a SPARQL URL to process datasets and generate entityGraph.nt.
- Other scripts support this pipeline or provide standalone utilities for querying and extraction.
- Dependencies: rdflib, SPARQLWrapper, gliner2, pyoxigraph, langextract, etc. (see requirements.txt in parent repo).
