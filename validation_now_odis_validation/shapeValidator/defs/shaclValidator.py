from pyshacl import __version__, validate
from pyshacl.errors import (
    ConstraintLoadError,
    ReportableRuntimeError,
    RuleLoadError,
    ShapeLoadError,
    ValidationFailure,
)


def validate_with_shacl(rdf_graph_text, shacl_shape_text):
    """
    Validate an RDF graph against a SHACL shape graph using pyshacl.

    Args:
        rdf_graph_text (str): RDF graph content as text
        shacl_shape_text (str): SHACL shape graph content as text
        output_format (str): Output format - one of: human, table, turtle, xml, json-ld, nt, n3

    Returns:
        tuple: (is_valid, validation_report, validation_text)
            - is_valid (bool): True if validation passed, False otherwise
            - validation_report (Graph): The validation report as an RDF graph
            - validation_text (str): The validation report in the requested format
    """

    try:
        # Perform SHACL validation
        is_valid, validation_graph, validation_text = validate(
            rdf_graph_text,
            data_graph_format="ttl",
            shacl_graph_format="ttl",
            shacl_graph=shacl_shape_text, inference='rdfs',  serialize_report_graph = False
        )

        # print("--------------------------------------------")
        # print(is_valid)
        # print("--------------------------------------------")
        # print(validation_graph)
        # print("--------------------------------------------")
        # print(validation_text)

        # return is_valid, validation_graph, validation_text

        skolemver = validation_graph.skolemize(authority="http://gleaner.io")
        # return skolemver.serialize(format="nt")

        return skolemver.serialize(format="nt")

    except Exception as e:
        raise Exception(f"SHACL validation error: {e}")


def validate_with_shacl_simple(rdf_graph_text, shacl_shape_text):
    """
    Simplified version that returns only the validation text result.

    Args:
        rdf_graph_text (str): RDF graph content as text
        shacl_shape_text (str): SHACL shape graph content as text
        output_format (str): Output format - one of: human, table, turtle, xml, json-ld, nt, n3

    Returns:
        str: The validation report in the requested format
    """

    try:
        # Perform SHACL validation
        is_valid, validation_graph, validation_text = validate(
            rdf_graph_text,
            data_graph_format="ttl",
            shacl_graph_format="ttl",
            shacl_graph=shacl_shape_text, inference='rdfs',  serialize_report_graph = True
        )

        # print("--------------------------------------------")
        # print(is_valid)
        # print("--------------------------------------------")
        # print(validation_graph)
        # print("--------------------------------------------")
        # print(validation_text)

        # return is_valid, validation_graph, validation_text
        return validation_text

    except Exception as e:
        raise Exception(f"SHACL validation error: {e}")