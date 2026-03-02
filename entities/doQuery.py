import rdflib
import argparse
import json
from collections import defaultdict

def generate_examples(data):
    """
    Reads the JSON file and generates Python code in the specified style.
    Ensures no duplicate key-value pairs within a single result.
    :param data: Dictionary containing results
    :return: String containing the generated Python code
    """
    results = data.get('results', [])
    code = "examples = [\n"

    for result in results:
        # Escape double quotes in text
        text = result.get('text', '').replace('"', '\\"').replace('\r', '\\r').replace('\n', '\\n')
        code += "    lx.data.ExampleData(\n"
        code += f'        text="{text}",\n'
        code += "        extractions=[\n"

        kv_list = result.get('kv', [])
        seen_pairs = set()

        for kv in kv_list:
            key = kv.get('key', '').replace('\n', ' ').replace('\r', ' ').replace('"', '\\"')
            value = kv.get('value', '').replace('\n', ' ').replace('\r', ' ').replace('"', '\\"')

            # Create a tuple of (key, value) to check for duplicates
            pair = (key, value)

            # Skip if we've already seen this exact key-value pair
            if pair in seen_pairs:
                continue

            seen_pairs.add(pair)
            code += f'            lx.data.Extraction(extraction_class="{key}", extraction_text="{value}"),\n'

        code += "        ]\n"
        code += "    ),\n"

    code += "]"
    return code

def main():
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description='Run a SPARQL query on an NT RDF file.')
    parser.add_argument('--query', required=True, help='Path to the file containing the SPARQL query.')
    parser.add_argument('--rdf', required=True, help='Path to the NT RDF file.')

    args = parser.parse_args()

    # Read the SPARQL query from the file
    with open(args.query, 'r') as query_file:
        sparql_query = query_file.read()

    # Create an RDF graph and parse the NT file
    graph = rdflib.Graph()
    graph.parse(args.rdf, format='nt')

    # Execute the SPARQL query
    results = graph.query(sparql_query)

    # Group results by description
    grouped = defaultdict(list)
    for row in results:
        desc = str(row.description)  # Convert to string in case it's a Literal or URI
        apname = str(row.apname)
        apvalue = str(row.apvalue)
        grouped[desc].append({"key": apname, "value": apvalue})

    # Build the output structure
    the_results = []
    for desc, kvs in grouped.items():
        the_results.append({"text": desc, "kv": kvs})

    output = {"results": the_results}
    # print(json.dumps(output, indent=2))

    code = generate_examples(output)

    print(code)

if __name__ == '__main__':
    main()
