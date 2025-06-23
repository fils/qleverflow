from fastmcp import FastMCP
from SPARQLWrapper import SPARQLWrapper, JSON
from fastmcp.prompts.prompt import Message

# TODO add a tool or resources that is all the labels and or names for all the subject of type X
# TODO perform text search on index
# TODO search for shared schema:identifier
# TODO shared variable measured
# TODO how to look for shared "entities" in the description
# TODO need a way to return the IDs (citation information) for the queries
# TODO explore validation either by SHACL or BAML to get things like schema:url for citation
# TODO make a tool that calls lancedb first then uses the results to query and return graph elements

# Initialize SPARQL endpoint (replace with your triplestore's endpoint)
sparql = SPARQLWrapper("http://ghost.lan:7007/sparql")
# sparql = SPARQLWrapper("http://homelab.lan:7879/query")

# Create an MCP server
mcp = FastMCP("RDF Query Server")

@mcp.tool()
def text_search(text: str):
    """Search for datasets containing a specific text term within their descriptions.

       This tool performs a full-text search across dataset descriptions in the RDF triplestore
       to find datasets that contain a specified search term. It uses QLever's built-in text
       search capabilities to locate datasets where the search term appears in text entities
       that are linked to dataset descriptions.

       Parameters:
           text (str): The search term or phrase to look for within dataset descriptions.
                       The search is case-sensitive and looks for exact word matches.
                       For example: "climate", "ocean temperature", "biodiversity"

       Returns:
           list: A list of dictionaries, where each dictionary represents a dataset match.
                 Each result contains:
                 - uri: The URI identifier of the dataset
                 - count: Number of text occurrences containing the search term
                 - example_text: A sample text snippet showing the search term in context
                 - item: The description text that matched the search criteria

                 Results are ordered by count (descending) and limited to 50 matches.

       Usage:
           Use this tool to discover datasets related to specific topics or research areas.
           The search helps identify relevant datasets by examining their descriptive metadata
           rather than requiring exact knowledge of dataset identifiers or classifications.

       Examples:
           - Find climate-related datasets: text_search("climate")
           - Locate oceanographic data: text_search("ocean")
           - Search for biodiversity research: text_search("species")

       Note:
           The search excludes datasets from "gleaner.io" domains and filters out blank nodes
           to focus on well-defined, accessible datasets. The function uses QLever-specific
           SPARQL extensions for efficient text search operations.
       """
    query = f"""
        PREFIX ql: <http://qlever.cs.uni-freiburg.de/builtin-functions/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?uri (COUNT(?text) AS ?count) (SAMPLE(?text) AS ?example_text) ?item  WHERE {{
          ?uri rdf:type <https://schema.org/Dataset> .
            ?uri <https://schema.org/description> ?item .
            ?text ql:contains-entity ?item .
            ?text ql:contains-word "{text}" .
                  FILTER (!CONTAINS(STR(?uri), "gleaner.io"))
          FILTER (!isBLANK(?uri))
        }}
        GROUP BY ?uri ?item
        ORDER BY DESC(?count)
        LIMIT 50
        """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    # Get the variable names from the head.vars section of the results
    variables = results["head"]["vars"]

    resp = []
    for result in results["results"]["bindings"]:
        item = {}
        # Extract all available variables dynamically based on what was in the SELECT
        for var in variables:
            if var in result:
                item[var] = result[var]["value"]
        resp.append(item)

    return resp


@mcp.tool()
def generic_sparql(query):
    """Execute any SPARQL query against the RDF triplestore and return structured results.
    
    This tool allows you to run custom SPARQL queries and get back all selected variables
    from the results. It dynamically extracts all variables specified in your SELECT clause
    and returns them in a structured format.
    
    Parameters:
        query (str): A valid SPARQL query string to execute. For example:
                     "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10"
    
    Returns:
        list: A list of dictionaries, where each dictionary represents one result row.
              Each key in the dictionary corresponds to a variable from your SELECT clause
              (without the ? prefix), and its value is the matching RDF term's value.
              
    Examples:
        - To get all triples: "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10"
        - To find specific data: "SELECT ?label WHERE { <http://example.org/resource> rdfs:label ?label }"
        - To count entities: "SELECT (COUNT(?s) as ?count) WHERE { ?s a <http://schema.org/Person> }"
    
    Note: The query must be syntactically valid SPARQL or an error will be returned.
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    # Get the variable names from the head.vars section of the results
    variables = results["head"]["vars"]
    
    resp = []
    for result in results["results"]["bindings"]:
        item = {}
        # Extract all available variables dynamically based on what was in the SELECT
        for var in variables:
            if var in result:
                item[var] = result[var]["value"]
        resp.append(item)
    
    return resp


@mcp.tool()
def count_sparql(query):
    """Execute a SPARQL COUNT query against the RDF triplestore and return the count value.
    
    This tool is specifically designed for SPARQL queries that return count results using
    aggregation functions like COUNT. It simplifies working with numerical results by
    extracting just the count value from the SPARQL result set.
    
    Parameters:
        query (str): A valid SPARQL query string that includes a COUNT aggregation. 
                     The query should use "COUNT" and alias the result as "?count".
                     For example: "SELECT (COUNT(?s) as ?count) WHERE { ?s ?p ?o }"
    
    Returns:
        list: A list containing the count value(s) as strings. Typically this will be 
              a single-item list, but multiple counts could be returned if the query 
              includes multiple COUNT operations with the "?count" variable name.
    
    Examples:
        - Count total triples: "SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }"
        - Count instances of a class: "SELECT (COUNT(?s) as ?count) WHERE { ?s a <http://schema.org/Person> }"
        - Count unique subjects: "SELECT (COUNT(DISTINCT ?s) as ?count) WHERE { ?s ?p ?o }"
    
    Note: The query must use "?count" as the variable name for the count result.
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    predicates = [result["count"]["value"] for result in results["results"]["bindings"]]
    return predicates

@mcp.tool()
def get_distinct_type():
    """Retrieve all distinct RDF classes (types) defined in the triplestore.
    
    This tool queries the RDF triplestore for all unique class types that have been used
    to classify entities within the dataset. It looks for all distinct objects of "rdf:type"
    or "a" predicates, providing a comprehensive overview of the data model's class hierarchy.
    
    Parameters:
        None
        
    Returns:
        list: A list of strings representing the URIs of all distinct RDF classes (types)
              found in the triplestore. These URIs typically follow ontology patterns like:
              - http://schema.org/Person
              - http://xmlns.com/foaf/0.1/Agent
              - http://www.w3.org/2002/07/owl#Class
              
    Usage:
        Use this tool to explore the data model, understand what kinds of entities exist
        in the triplestore, or to identify specific classes for further querying.
        
    Note:
        The results are returned as full URIs without prefixes, making them suitable for
        direct use in subsequent SPARQL queries.
    """
    query = """
    SELECT DISTINCT ?type
    WHERE {
        ?s a ?type
    }
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    predicates = [result["type"]["value"] for result in results["results"]["bindings"]]
    return predicates


@mcp.tool()
def get_all_predicates_for_type(type: str):
    """Retrieve all distinct predicates (properties) used with entities of a specific RDF class.
    
    This tool identifies all the predicates (properties, relationships) that are associated
    with entities of a specified RDF class type in the triplestore. It helps explore the
    data model by showing what properties are available for a particular class of entities.
    
    Parameters:
        type (str): The full URI of an RDF class type (e.g., "http://schema.org/Person").
                    Must be provided exactly as it appears in the triplestore, including
                    the complete namespace.
    
    Returns:
        list: A list of strings representing the URIs of all distinct predicates that
              are used with entities of the specified type. These may include:
              - Standard RDF/RDFS/OWL properties (e.g., rdfs:label, owl:sameAs)
              - Domain-specific properties (e.g., foaf:name, schema:birthDate)
              - Custom properties defined in the dataset
    
    Usage:
        After discovering available types with get_distinct_type(), use this tool to
        understand what properties are available for entities of a specific type.
        This helps in formulating more targeted SPARQL queries.
    
    Example:
        To find all predicates used with Person entities:
        get_all_predicates_for_type("http://schema.org/Person")
    """
    query = f"""
    SELECT DISTINCT ?p
    WHERE {{
	    ?s a <{type}> .
        ?s ?p ?o .
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    predicates = [result["p"]["value"] for result in results["results"]["bindings"]]
    return predicates


@mcp.tool()
def get_all_distinct_predicates():
    """Retrieve all distinct predicates (properties and relationships) used in the RDF triplestore.
    
    This tool performs a comprehensive scan of the entire triplestore to identify all
    unique predicates that connect subjects to objects in RDF triples. It provides
    a complete catalog of all properties, relationships, and attributes used across
    all entity types in the knowledge graph.
    
    Parameters:
        None
        
    Returns:
        list: A list of strings representing the URIs of all distinct predicates found 
              in the triplestore. This typically includes:
              - Core RDF/RDFS predicates (rdf:type, rdfs:label, rdfs:comment)
              - OWL predicates (owl:sameAs, owl:equivalentClass)
              - Domain-specific predicates from various ontologies
              - Custom predicates defined specifically for this dataset
    
    Usage:
        This tool is valuable for:
        - Data exploration: Understanding what kinds of relationships exist in the data
        - Schema discovery: Identifying the vocabulary/ontologies used
        - Query planning: Finding available predicates to use in more complex SPARQL queries
        - Data quality assessment: Identifying unexpected or non-standard predicates
        
    Note:
        Unlike get_all_predicates_for_type(), this function returns ALL predicates
        regardless of which entity types they are associated with. For large triplestores,
        this may return a substantial number of predicates.
    """
    query = """
    SELECT DISTINCT ?p
    WHERE {
        ?s ?p ?o .
    }
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    predicates = [result["p"]["value"] for result in results["results"]["bindings"]]
    return predicates

@mcp.resource("resource://greeting")
def get_greeting() -> str:
    """Provides a simple greeting message for MCP clients.
    
    This function creates a dynamic resource that can be accessed by clients
    connecting to this MCP server. It demonstrates the basic pattern for
    exposing server-side data as a resource with a custom URI scheme.
    
    Resource URI:
        resource://greeting
        
    Access Pattern:
        Clients can request this resource directly using the resource:// protocol,
        which is handled by the MCP middleware. The resource can be fetched using
        standard MCP client APIs or integrated into client-side components that
        support MCP resource references.
    
    Return Value:
        str: A simple greeting message string that is delivered to the client
             without any additional processing. The string is returned exactly
             as provided and can be used in client-side display contexts.
    
    Usage Examples:
        - Welcome messages in client applications
        - Testing MCP resource connectivity
        - Simple demonstration of the resource protocol
        - Template for more complex dynamic string resources
    
    Note:
        This resource does not require any parameters and always returns the same
        static message. For parameterized or dynamic content, consider using a
        resource that accepts query parameters or implements session-specific logic.
    """
    return "Hello from FastMCP Resources!"


@mcp.resource("data://config")
def get_config() -> dict:
    """Provides application configuration as JSON."""
    return {
        "theme": "dark",
        "version": "1.2.0",
        "features": ["tools", "resources"],
    }

@mcp.prompt()
def ask_about_topic(topic: str) -> str:
    """Generates a user message asking for an explanation of a topic.
    
    This function creates a standardized prompt template that MCP clients can use
    to generate consistent user messages for topic explanations. The MCP framework
    automatically converts the returned string into a properly formatted UserMessage
    object that can be sent to language models or other conversational services.
    
    Parameters:
        topic (str): The specific subject, concept, term, or idea that the client
                     wants explained. This should be a concise descriptor that clearly
                     identifies what needs to be explained (e.g., "quantum computing",
                     "SPARQL queries", "semantic web").
    
    Returns:
        str: A formatted question string that will be converted to a UserMessage
             by the MCP framework. This string follows a consistent, polite
             question format that is optimized for clear responses from AI systems.
    
    Usage in MCP Context:
        Clients can invoke this prompt function through the MCP interface, passing
        only the topic parameter. The MCP server handles the generation of the
        full message, ensuring consistent formatting across all explanation requests.
        This provides several advantages:
        - Reduces client-side code complexity
        - Ensures consistent prompt engineering practices
        - Allows server-side updates to prompt patterns without client changes
        - Supports prompt versioning and optimization
        
    Example Client Usage:
        request_explanation("neural networks")
        # The MCP server generates: "Can you please explain the concept of 'neural networks'?"
    
    Note:
        This prompt uses a simple template, but can be extended to include additional
        context, formatting instructions, or system-specific parameters based on 
        the needs of the connected AI services.
    """
    return f"Can you please explain the concept of '{topic}'?"

@mcp.prompt()
def generate_code_request(language: str, task_description: str) -> str:
    """Generates a user message requesting code generation for MCP clients.

       This prompt function creates a structured UserMessage object that specifically requests
       code generation in a designated programming language. Unlike basic string-returning
       prompts, this function explicitly returns a UserMessage object with formatted content,
       giving clients more control over message construction while maintaining consistent
       code generation requests.

       Parameters:
           language (str): The programming language for the requested code. Should be a
                           valid language name (e.g., "Python", "JavaScript", "SQL", "SPARQL").
                           The language name is inserted directly into the prompt to ensure
                           the generated code matches client requirements.

           task_description (str): A detailed description of what the code should accomplish.
                                  This should clearly explain the functionality, inputs,
                                  outputs, and any specific requirements or constraints.
                                  More detailed descriptions typically yield better results.

       Returns:
           UserMessage: A fully constructed UserMessage object with content field containing
                       the formatted code generation request. The MCP framework handles this
                       object type directly, preserving any metadata or special formatting.

       Usage in MCP Architecture:
           - Clients invoke this prompt through the MCP interface by providing the language
             and task description parameters
           - The MCP server constructs the appropriate UserMessage with optimized formatting
           - The message is sent to the connected AI service (LLM)
           - The response (typically containing generated code) is returned to the client

       Benefits for MCP Clients:
           - Standardized code request format ensures consistent AI responses
           - Reduces prompt engineering burden on client implementations
           - Allows for server-side prompt improvements without client changes
           - Provides explicit typing via UserMessage objects rather than raw strings

       Example Client Usage:
           request_code("Python", "Sort a list of dictionaries by a specific key")

       Integration Notes:
           This prompt works best with AI services that understand code generation requests
           and can produce properly formatted, functional code snippets in the requested
           language. The prompt is designed to be clear and direct to maximize the quality
           of generated code.
       """
    content = f"Write a {language} function that performs the following task: {task_description}"
    return content


# # Template with multiple parameters
# @mcp.resource("repos://{owner}/{repo}/info")
# def get_repo_info(owner: str, repo: str) -> dict:
#     """Retrieves information about a GitHub repository."""
#     # In a real implementation, this would call the GitHub API
#     return {
#         "owner": owner,
#         "name": repo,
#         "full_name": f"{owner}/{repo}",
#         "stars": 120,
#         "forks": 48
#     }

# Run the server
if __name__ == "__main__":
       mcp.run(transport="sse", host="localhost", port=8898)
