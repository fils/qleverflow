import json

def generate_jsonld(entities_json, uri):
    """
    Takes a JSON document containing entities and generates a JSON-LD structure.

    :param entities_json: A dictionary with an 'entities' key containing a dict of entity types to lists of values.
    :return: A dictionary representing the JSON-LD.
    """
    if isinstance(entities_json, str):
            entities_json = json.loads(entities_json)

    entities = entities_json.get("entities", {})

    additional_properties = []
    for key, value_list in entities.items():
        if value_list:  # Only include non-empty lists
            additional_properties.append({
                "@type": "PropertyValue",
                "name": key,
                "value": value_list
            })

    jsonld = {
        "@context": "https://schema.org",
        "@id" : uri,
        "@type": "Dataset",
        "description": entities_json.get("description", {}),
        "additionalProperty": additional_properties
    }

    return(json.dumps(jsonld, indent=4))
