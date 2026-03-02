# Concurrent

# Notes

These are not doing SHACL  They are only demonstrating the use of concurrent pipelines.

* asyncPool.py Downloaded 1600 sites in 2.3 seconds
  * did not save them anywhere
* streamToParquet.py Downloaded 10,000 sites in 107 seconds   (94 / second)
  * saveed the web pages to Parquet.  I would save the SHACL RDF to parquet, then process into RDF and load to QLever
  * could qleverfile be set to read from parquet files?
