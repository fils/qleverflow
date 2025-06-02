# <llm-snippet-file>shapeGraphs/batch_shacl_validator.py</llm-snippet-file>
import argparse
import requests
import os
from pathlib import Path

# Configuration
SPARQL_ENDPOINT = "http://ghost.lan:7019"
# This placeholder should exactly match the URI string in your construct.rq file
# that needs to be replaced by each graph URI.
# Based on your construct.rq, it is:
CONSTRUCT_PLACEHOLDER = "<urn:gleaner.io:oih:medin:data:04bd1d47761a03e2329931964f63fdfc8617b4c1>"

# Attempt to import pyshacl and set a flag
try:
    from pyshacl import validate

    PYSHACL_AVAILABLE = True
except ImportError:
    PYSHACL_AVAILABLE = False


def execute_sparql_query(query_string: str, endpoint_url: str, accept_header: str = "text/tab-separated-values"):
    """
    Executes a SPARQL query against the given endpoint.
    """
    headers = {
        "Accept": accept_header,
        "Content-type": "application/sparql-query"
    }
    try:
        response = requests.post(endpoint_url, data=query_string.encode('utf-8'), headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error executing SPARQL query: {e}")
        print(f"Query: {query_string[:200]}...")  # Log part of the query for debugging
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text[:500]}...")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Executes a series of SPARQL queries and validates results with SHACL.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("initial_sparql_file",
                        help="Path to the initial SPARQL query file (fetches graph URIs, e.g., namedGraphFilter.rq).")
    parser.add_argument("construct_rq_file",
                        help="Path to the CONSTRUCT SPARQL query template file (e.g., construct.rq).")
    parser.add_argument("shacl_shape_file",
                        help="Path to the SHACL shape graph file (e.g., shapes.ttl).")
    parser.add_argument("output_dir",
                        help="Directory to save SHACL validation reports.")

    args = parser.parse_args()

    if not PYSHACL_AVAILABLE:
        print("Warning: The 'pyshacl' library is not installed. SHACL validation will be skipped.")
        print("To enable validation, please install it by running: pip install pyshacl")
        print("The script will still attempt to fetch data and generate placeholders for reports.")

    # Create output directory if it doesn't exist
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Output will be saved to: {output_path.resolve()}")

    # 1. Read and execute the initial SPARQL query
    try:
        with open(args.initial_sparql_file, 'r', encoding='utf-8') as f:
            initial_query = f.read()
    except FileNotFoundError:
        print(f"Error: Initial SPARQL file not found at {args.initial_sparql_file}")
        return
    except Exception as e:
        print(f"Error reading initial SPARQL file '{args.initial_sparql_file}': {e}")
        return

    print(f"Executing initial query from {args.initial_sparql_file} to fetch graph URIs...")
    # The curl command implies the variable is ?g and results are TSV
    # SPARQL TSV results enclose URIs in <>.
    g_values_tsv = execute_sparql_query(initial_query, SPARQL_ENDPOINT, accept_header="text/tab-separated-values")

    if not g_values_tsv:
        print("Failed to retrieve graph URIs from the initial query. Exiting.")
        return

    # 2. Parse graph URIs
    lines = g_values_tsv.strip().split('\n')

    # Expected TSV format:
    # ?g
    # <uri1>
    # <uri2>
    if not lines or lines[0].strip() != "?g":
        print(
            f"Unexpected TSV format from initial query. Expected '?g' header, got: '{lines[0] if lines else 'empty response'}'")
        if len(lines) == 1 and lines[0].strip() == "?g":  # Only header, no data
            print("No graph URIs (?g values) returned from the initial query.")
        return

    graph_uris = [line.strip() for line in lines[1:] if line.strip()]
    if not graph_uris:
        print("No graph URIs found in the results of the initial query.")
        return

    print(f"Found {len(graph_uris)} graph URIs to process.")

    # 3. Read the CONSTRUCT query template
    try:
        with open(args.construct_rq_file, 'r', encoding='utf-8') as f:
            construct_query_template = f.read()
    except FileNotFoundError:
        print(f"Error: CONSTRUCT query file not found at {args.construct_rq_file}")
        return
    except Exception as e:
        print(f"Error reading CONSTRUCT query file '{args.construct_rq_file}': {e}")
        return

    # 4. Loop, execute CONSTRUCT query, and (conditionally) validate
    for i, graph_uri_with_brackets in enumerate(graph_uris):
        print(f"\nProcessing graph {i + 1}/{len(graph_uris)}: {graph_uri_with_brackets}")

        # Replace the placeholder in the construct query.
        # graph_uri_with_brackets is already like "<http://...>" from TSV
        current_construct_query = construct_query_template.replace(CONSTRUCT_PLACEHOLDER, graph_uri_with_brackets)

        print(f"Executing CONSTRUCT query for {graph_uri_with_brackets}...")
        # We need an RDF format for pyshacl. Turtle is common.
        constructed_rdf = execute_sparql_query(current_construct_query, SPARQL_ENDPOINT, accept_header="text/turtle")

        if not constructed_rdf:
            print(f"Failed to construct RDF for {graph_uri_with_brackets}. Skipping.")
            # Create a placeholder error file
            error_file_path = output_path / f"error_construct_query_{i + 1}.txt"
            with open(error_file_path, 'w', encoding='utf-8') as f:
                f.write(f"Failed to execute CONSTRUCT query for graph URI: {graph_uri_with_brackets}\n")
                f.write(f"Attempted query (first 500 chars):\n{current_construct_query[:500]}...\n")
            print(f"Error details logged to {error_file_path}")
            continue

        # Define output filenames for reports
        # Using a simple index for filenames to ensure validity.
        # The graph URI will be included inside the report file.
        summary_report_path = output_path / f"validation_summary_{i + 1}.txt"
        rdf_report_path = output_path / f"validation_report_{i + 1}.ttl"  # SHACL reports are often in Turtle

        if PYSHACL_AVAILABLE:
            print(f"Attempting SHACL validation for {graph_uri_with_brackets} against {args.shacl_shape_file}...")
            try:
                # Determine SHACL shape file format (pyshacl can often auto-detect, but explicit is better)
                # Common formats: 'turtle', 'xml', 'n3', 'nt', 'json-ld'
                # For simplicity, we'll try to guess from extension or default to turtle.
                # You might want to make shacl_graph_format an explicit script argument if files vary.
                shacl_ext = Path(args.shacl_shape_file).suffix.lower()
                sg_format = {
                    '.ttl': 'turtle', '.turtle': 'turtle',
                    '.rdf': 'xml', '.owl': 'xml', '.xml': 'xml',
                    '.n3': 'n3', '.nt': 'nt', '.jsonld': 'json-ld'
                }.get(shacl_ext, 'turtle')  # Default to Turtle if extension unknown

                conforms, results_graph_str, results_text = validate(
                    data_graph=constructed_rdf,
                    data_graph_format='turtle',  # Matches our CONSTRUCT query's Accept header
                    shacl_graph=args.shacl_shape_file,  # Path to the SHACL shapes file
                    shacl_graph_format=sg_format,
                    inference='none',  # Or 'rdfs', 'owlrl', 'both' as needed
                    debug=False,
                    serialize_report_graph=True,  # Get the report as an RDF graph string
                    report_graph_format='turtle'  # Format for the RDF report string
                )

                # Save human-readable summary report
                with open(summary_report_path, 'w', encoding='utf-8') as f:
                    f.write(f"SHACL Validation Summary\n")
                    f.write(f"========================\n")
                    f.write(f"Data Graph Source URI: {graph_uri_with_brackets}\n")
                    f.write(f"SHACL Shape File: {args.shacl_shape_file}\n")
                    f.write(f"Conforms: {conforms}\n\n")
                    f.write("Validation Results (Textual):\n")
                    f.write("-----------------------------\n")
                    f.write(results_text)
                print(f"SHACL validation summary saved to {summary_report_path}")

                # Save RDF validation report
                if results_graph_str:
                    with open(rdf_report_path, 'w', encoding='utf-8') as f:
                        f.write(results_graph_str)
                    print(f"SHACL validation RDF report saved to {rdf_report_path}")

            except Exception as e:
                print(f"Error during SHACL validation for {graph_uri_with_brackets}: {e}")
                # Save error information to the summary file
                with open(summary_report_path, 'w', encoding='utf-8') as f:
                    f.write(f"Error during SHACL validation for graph: {graph_uri_with_brackets}\n")
                    f.write(f"SHACL Shape File: {args.shacl_shape_file}\n")
                    f.write(f"Error: {e}\n\n")
                    f.write("Constructed RDF Data (first 1000 chars):\n")
                    f.write(constructed_rdf[:1000] + "...\n" if len(constructed_rdf) > 1000 else constructed_rdf)
                print(f"Error details logged to {summary_report_path}")
        else:
            # pyshacl is not available, save a placeholder for the data.
            print(f"SHACL validation SKIPPED for {graph_uri_with_brackets} (pyshacl library not found).")
            with open(summary_report_path, 'w', encoding='utf-8') as f:
                f.write(f"SHACL Validation SKIPPED (pyshacl library not available)\n")
                f.write(f"========================================================\n")
                f.write(f"Data Graph Source URI: {graph_uri_with_brackets}\n")
                f.write(f"Intended SHACL Shape File: {args.shacl_shape_file}\n\n")
                f.write("Constructed RDF Data (would have been validated - first 1000 chars):\n")
                f.write("-----------------------------------------------------------------\n")
                f.write(constructed_rdf[:1000] + "...\n" if len(constructed_rdf) > 1000 else constructed_rdf)
                f.write("\n\nTo perform validation, please install pyshacl: pip install pyshacl\n")
            print(f"Placeholder report (containing constructed RDF) saved to {summary_report_path}")
            # Optionally save the RDF data separately as well if pyshacl is not available
            raw_rdf_output_path = output_path / f"constructed_rdf_for_graph_{i + 1}.ttl"
            with open(raw_rdf_output_path, 'w', encoding='utf-8') as f:
                f.write(constructed_rdf)
            print(f"Raw constructed RDF saved to {raw_rdf_output_path}")

    print("\nProcessing complete.")
    if not PYSHACL_AVAILABLE:
        print(
            "Reminder: 'pyshacl' is not installed. Validation steps were skipped. Install with 'pip install pyshacl'.")


if __name__ == "__main__":
    main()