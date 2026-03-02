import spacy

def parse_query(query_text: str) -> dict:
    """
    Parse a natural language query into AND/OR structured elements.

    Returns a dict with:
      - "AND": list of terms always required
      - "OR_GROUPS": list of lists, each inner list is one OR branch
    """
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load("en_core_web_sm")

    doc = nlp(query_text)

    # Find indices of 'or' tokens
    or_indices = [token.i for token in doc if token.lower_ == "or"]

    if not or_indices:
        return {"AND": _extract_keywords(doc), "OR_GROUPS": []}

    # Split doc into spans around each 'or'
    parts = []
    start = 0
    for idx in or_indices:
        parts.append(doc[start:idx])
        start = idx + 1
    parts.append(doc[start:])

    # Re-parse each part so NER runs fresh on the full sub-string
    extracted_parts = [_extract_keywords(nlp(span.text)) for span in parts]

    # Strategy:
    #   - The LAST keyword of the part before 'or' is an OR candidate
    #   - The FIRST keyword of each subsequent part is an OR candidate
    #   - Everything else is a global AND

    global_and: list[str] = []
    or_groups: list[list[str]] = []

    if len(extracted_parts) >= 2:
        # Last item of part[0] is the first OR choice
        if extracted_parts[0]:
            or_groups.append([extracted_parts[0][-1]])
            global_and = extracted_parts[0][:-1]

        # Each subsequent part: first item is an OR choice, rest go to global AND
        for part_keywords in extracted_parts[1:]:
            if part_keywords:
                or_groups.append([part_keywords[0]])
                global_and.extend(part_keywords[1:])

    return {"AND": global_and, "OR_GROUPS": or_groups}


def _extract_keywords(doc) -> list[str]:
    """
    Extract meaningful keywords from a spaCy doc:
    - Non-stop nouns, proper nouns, adjectives not in a named entity (listed first)
    - Named entities appended after (so location entities are last and become OR candidates)
    """
    entity_keywords: list[str] = []
    non_entity_keywords: list[str] = []
    entity_token_indices: set[int] = set()

    for ent in doc.ents:
        text = ent.text
        if text.lower().startswith("the "):
            text = text[4:]
        entity_keywords.append(text)
        entity_token_indices.update(range(ent.start, ent.end))

    for token in doc:
        if (
            token.i not in entity_token_indices
            and not token.is_stop
            and not token.is_punct
            and token.pos_ in {"NOUN", "PROPN", "ADJ"}
        ):
            non_entity_keywords.append(token.text)

    # Non-entity keywords first, named entities last.
    # This ensures geographic entities (OR candidates) sit at the end of part[0].
    return non_entity_keywords + entity_keywords


def generate_sparql(structured_results: dict) -> str:
    """Build a SPARQL query with UNION blocks for OR groups."""
    prefix = """\
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX gn: <https://www.geonames.org/ontology#>
PREFIX text: <http://jena.apache.org/text#>
PREFIX vrank: <http://purl.org/voc/vrank#>
PREFIX ql: <http://qlever.cs.uni-freiburg.de/builtin-functions/>
prefix schema: <https://schema.org/>

SELECT *
WHERE {"""

    global_ands: list[str] = structured_results["AND"]
    or_groups: list[list[str]] = structured_results["OR_GROUPS"]

    def build_block(extra_words: list[str]) -> str:
        lines = [
            "   {",
            "    ?s schema:description ?item .",
            "    ?text ql:contains-entity ?item .",
        ]
        for word in global_ands:
            lines.append(f'    ?text ql:contains-word "{word}" .')
        for word in extra_words:
            lines.append(f'    ?text ql:contains-word "{word}" .')
        lines.append("    }")
        return "\n".join(lines)

    if or_groups:
        blocks = [build_block(group) for group in or_groups]
        query_body = "\nUNION\n".join(blocks)
    else:
        query_body = build_block([])

    return prefix + "\n" + query_body + "\n}"


if __name__ == "__main__":
    example_query = "I would like sediment deposition in the North Atlantic or North Pacific"
    print(f"Query: {example_query}\n")

    results = parse_query(example_query)

    print("Extracted Elements:")
    print(f"  AND (always required): {results['AND']}")
    for i, group in enumerate(results["OR_GROUPS"]):
        print(f"  OR Group {i + 1}:          {group}")

    sparql = generate_sparql(results)
    print("\nGenerated SPARQL:\n")
    print(sparql)
