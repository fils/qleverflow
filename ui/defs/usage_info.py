


def about():
    html_content = """
    
<h1>Usage Information</h1>

<h2>Comparative Search</h2>

<p>
This tab performs a search for a term across both the 
text index and vector index.  It exposed the two results
side by side and color codes the results to the user can 
more easily see the similar results and their relative 
position in the results.
</p>

<p>
Future version of this will then include a third column
that is the re-ranked results from these two searches.
</p>

<h2>Chat</h2>

<p>
Classic LLM parlor trick where the results from the 
vector search, as seein the Comparative Search tab, are
used at RAG elements feed to the LLM for a narrative 
response. 
</p>

<h2>Search terms</h2>

<p>
The following are some examples of search terms. you could try.
</p>

<blockquote>
What data associated with urban development and land cover is available
</blockquote>

<blockquote>
What air quality data is available for Florida and what sources is it from
</blockquote>

    
    """

    return html_content
