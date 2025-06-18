# Qlever Test Instance

## About

First, if you are interested in Qlever and running it locally, DO NOT USE THIS REPO.  At least, it's very likely this is
not what you want.

You likely want to go to the [qlever-control](https://github.com/ad-freiburg/qlever-control) repo instead.  That
is the official repo for a nice server and UI onboarding experience with Qlever.   Also visit the main
[qlever](https://github.com/ad-freiburg/qlever) repo or the [Qlever Wiki](https://github.com/ad-freiburg/qlever/wiki).


## What does this repo do?
So why does this repo exist?   It is mostly to explore deploying Qlever via
docker compose files for some of our workflows and automated approaches.   In that case, qlever-control
was not quite what was needed.  So we basically decomposed qlever-control logic into docker compose files.

If you are interested in deploying Qlever leveraging Docker Compose and data volumes or interfaces such
as Portainer, this repository may provide some use for you.   Or you may provide us some insight (i.e., pull requests welcome).

## Graph as Data Product

One other goal for this repository is to explore and refine the approach to sharing graphs as
products for local use.  Similar to the manner in which Parquet or Zarr files might be generated 
and shared as a data product, a Knoledge Graph (KG) can too.  

The Qlever approach is to use a Qleverfile, and the development teams creation of the previously mentioned [qlever-control](https://github.com/ad-freiburg/qlever-control) makes this a solid approach to graph as a data product.  

Graphs can be stored in compressed n-quads files, for example, in an object store and then referenced in a small Qleverfile for people to download and leverage for then fetching, indexing and querying the KG.  


## References:

* [Qlever](https://github.com/ad-freiburg/qlever)
* [Qlever-ui](https://github.com/ad-freiburg/qlever-ui)
* [Petrimaps - mapping for Qlever GeoSPARQL](https://github.com/ad-freiburg/qlever-petrimaps)
* [Qlever-control](https://github.com/ad-freiburg/qlever-control)
* [SPARQL plus Text](https://github.com/ad-freiburg/qlever/blob/master/docs/sparql_plus_text.md)
* [Path Search Feature Documentation for SPARQL Engine](https://github.com/ad-freiburg/qlever/blob/master/docs/path_search.md)
