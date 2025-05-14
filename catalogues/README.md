# README.md

NAMES MUST BE DNS COMPLIANT. These are used as PROJECT variables, MUST BE A DNS COMPLAINT NAME. NO UNDER_SCORES

## About


When trying to deploy a Qlever instance with data into Docker[swarm] there is no need to build the index and then try and sync
that into the swarm or a data volume.

Qlever has the concept of a qlever file that can pull down and build indexes.   We can do all this through docker native.  

> Note:  I'm not using UID and GID correctly here

### Test call for help

We should be able to see the help results with the following docker command.

```bash
docker run -it --rm -e UID=1111 -e GID=1111 -v ./data-odis:/data -w /data  adfreiburg/qlever:latest -c "qlever --help"

usage: qlever [-h] [--version] [--qleverfile QLEVERFILE]
              {start,setup-config,query,index-stats,add-text-index,log,index,stop,clear-cache,system-info,example-queries,status,ui,settings,warmup,cache-stats,extract-queries,get-data}
              ...

This is the qlever command line tool, it's all you need to work with QLever

positional arguments:
  {start,setup-config,query,index-stats,add-text-index,log,index,stop,clear-cache,system-info,example-queries,status,ui,settings,warmup,cache-stats,extract-queries,get-data}
    start               Start the QLever server (requires that you have built an index with `qlever index` before)
    setup-config        Get a pre-configured Qleverfile
    query               Send a query to a SPARQL endpoint
    index-stats         Breakdown of the time and space used for the index build
    add-text-index      Add text index to an index built with `qlever index`
    log                 Show the last lines of the server log file and follow it
    index               Build the index for a given RDF dataset
    stop                Stop QLever server for a given datasedataset or port
    clear-cache         Clear the query processing cache
    system-info         Gather some system info to help with troubleshooting
    example-queries     Run the given queries and show their processing times and result sizes
    status              Show QLever processes running on this machine
    ui                  Launch the QLever UI web application
    settings            Show or set server settings (after `qlever start`)
    warmup              Execute WARMUP_CMD
    cache-stats         Show how much of the cache is currently being used
    extract-queries     Extract all SPARQL queries from the server log
    get-data            Get data using the GET_DATA_CMD in the Qleverfile

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --qleverfile QLEVERFILE, -q QLEVERFILE

```


### Get data and build index

We will use some of these above commands to get data and index it next.  Sever of the commands
qlever can do have some interesting potential, though, if you browse through them.

My Qleverfile is located in the data-odis directory here, and you can inspect it to 
see where I am pulling down my data from and the process of unzipping, indexing and removing
the old zip file.

If we want to write over an existing index we can do that with  ``` --overwrite-existing``` but
for now we will be doing the initial fetch and index.

Try:

> Note: I had to have data-odis set world writable with ```chmod 777 data-odis  ```, since my UID GID mapping is wrong here.  


```bash
docker run -it --rm -e UID=1111 -e GID=1111 -v ./data-odis:/data -w /data  adfreiburg/qlever:latest -c "qlever -q Qleverfile.odis get-data && qlever -q Qleverfile.odis  index"
```

The results of running this should look like:

```bash

Command: get-data

curl -sLo odis.nq.zip -C - http://ossapi.oceaninfohub.org/public/odis.nq.zip && unzip -q -o odis.nq.zip && rm odis.nq.zip

Download successful, total file size: 5,640,404,814 bytes


Command: index

echo '{ "add-text-index": true, "ascii-prefixes-only": false, "num-triples-per-batch": 100000 }' > odis.settings.json
cat odis.nq | IndexBuilderMain -i odis -s odis.settings.json -F nq -f - | tee odis.index-log.txt

2025-05-14 13:56:05.087 - INFO: QLever IndexBuilder, compiled on Tue Apr 29 10:52:48 UTC 2025 using git hash 20effa
2025-05-14 13:56:05.088 - INFO: Locale was not specified in settings file, default is en_US
2025-05-14 13:56:05.088 - INFO: You specified "locale = en_US" and "ignore-punctuation = 0"
2025-05-14 13:56:05.088 - INFO: You specified "num-triples-per-batch = 100,000", choose a lower value if the index builder runs out of memory
2025-05-14 13:56:05.088 - INFO: By default, integers that cannot be represented by QLever will throw an exception
2025-05-14 13:56:05.088 - WARN: Implicitly using the parallel parser for a single input file for reasons of backward compatibility; this is deprecated, please use the command-line option --parse-parallel or -p
2025-05-14 13:56:05.088 - INFO: Processing triples from single input stream /dev/stdin (parallel = true) ...
2025-05-14 13:56:05.088 - INFO: Parsing input triples and creating partial vocabularies, one per batch ...
2025-05-14 13:56:17.429 - INFO: Triples parsed: 27,478,421 [average speed 2.3 M/s, last batch 2.3 M/s, fastest 2.3 M/s, slowest 2.2 M/s] 
2025-05-14 13:56:17.441 - INFO: Number of triples created (including QLever-internal ones): 27,755,023 [may contain duplicates]
2025-05-14 13:56:17.441 - INFO: Number of partial vocabularies created: 238
2025-05-14 13:56:17.441 - INFO: Merging partial vocabularies ...
2025-05-14 13:56:21.459 - INFO: Words merged: 8,346,941 [average speed 2.1 M/s] 
2025-05-14 13:56:21.730 - INFO: Finished writing compressed internal vocabulary, size = 204 MB [uncompressed = 555.7 MB, ratio = 36%]
2025-05-14 13:56:21.730 - INFO: Number of words in external vocabulary: 8,346,941
2025-05-14 13:56:21.818 - INFO: Converting triples from local IDs to global IDs ...
2025-05-14 13:56:22.688 - INFO: Triples converted: 27,755,023 [average speed 45.4 M/s, last batch 46.3 M/s, fastest 46.3 M/s, slowest 43.2 M/s] 
2025-05-14 13:56:22.697 - INFO: Creating permutations SPO and SOP ...
2025-05-14 13:56:23.987 - INFO: Number of inputs to `uniqueView`: 27,478,421.3 M/s, last batch 36.1 M/s, fastest 36.1 M/s, slowest 13.2 M/s] 
2025-05-14 13:56:23.987 - INFO: Number of unique elements: 27,435,153
2025-05-14 13:56:23.987 - INFO: Triples sorted: 27,435,153 [average speed 21.4 M/s, last batch 36.1 M/s, fastest 36.1 M/s, slowest 13.2 M/s] 
2025-05-14 13:56:25.299 - INFO: Statistics for SPO: #relations = 6,035,152, #blocks = 592, #triples = 27,435,153
2025-05-14 13:56:25.299 - INFO: Statistics for SOP: #relations = 6,035,152, #blocks = 592, #triples = 27,435,153
2025-05-14 13:56:25.300 - INFO: Number of distinct patterns: 994
2025-05-14 13:56:25.300 - INFO: Number of subjects with pattern: 6,035,152 [all]
2025-05-14 13:56:25.300 - INFO: Total number of distinct subject-predicate pairs: 20,777,074
2025-05-14 13:56:25.300 - INFO: Average number of predicates per subject: 3.4
2025-05-14 13:56:25.300 - INFO: Average number of subjects per predicate: 97,089
2025-05-14 13:56:25.301 - INFO: Creating permutations OSP and OPS ...
2025-05-14 13:56:28.660 - INFO: Triples sorted: 27,435,153 [average speed 8.2 M/s, last batch 12.8 M/s, fastest 12.8 M/s, slowest 5.4 M/s] 
2025-05-14 13:56:28.680 - INFO: Statistics for OSP: #relations = 8,169,113, #blocks = 768, #triples = 27,435,153
2025-05-14 13:56:28.680 - INFO: Statistics for OPS: #relations = 8,169,113, #blocks = 768, #triples = 27,435,153
2025-05-14 13:56:28.687 - INFO: Adding 6,035,152 triples to the POS and PSO permutation for the internal `ql:has-pattern` ...
2025-05-14 13:56:28.859 - INFO: Creating permutations PSO and POS ...
2025-05-14 13:56:29.310 - INFO: Number of inputs to `uniqueView`: 6,311,754
2025-05-14 13:56:29.310 - INFO: Number of unique elements: 6,267,386
2025-05-14 13:56:29.310 - INFO: Triples sorted: 6,267,386 [average speed 13.9 M/s] 
2025-05-14 13:56:29.348 - INFO: Statistics for PSO: #relations = 12, #blocks = 203, #triples = 6,267,386
2025-05-14 13:56:29.348 - INFO: Statistics for POS: #relations = 12, #blocks = 203, #triples = 6,267,386
2025-05-14 13:56:29.348 - INFO: Creating permutations PSO and POS ...
2025-05-14 13:56:32.320 - INFO: Triples sorted: 27,435,153 [average speed 9.2 M/s, last batch 11.6 M/s, fastest 11.6 M/s, slowest 7.0 M/s] 
2025-05-14 13:56:32.335 - INFO: Statistics for PSO: #relations = 214, #blocks = 933, #triples = 27,435,153
2025-05-14 13:56:32.335 - INFO: Statistics for POS: #relations = 214, #blocks = 933, #triples = 27,435,153
2025-05-14 13:56:32.342 - INFO: Index build completed

```

We now have an index we are reading to run qlever on via Docker like in the compose file in the main level of this repo.

We could just as easily do this in a data volume.  All we need to do is fetch the Qleverfile in that case.  



