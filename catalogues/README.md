# README.md

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
qlever can do have some very interesting potential though if you browse through them.

My Qleverfile is located in the data-odis directory here and you can inspect it to 
see where I am pulling down my data from and process of unzipping, indexing and removing
the old zip file.

If we want to write over an existing index we can do that with  ``` --overwrite-existing``` but
for now we will be doing the initial fetch and index.

Try:

> Note:  I had to have data-odis set for world write with ```chmod 777 data-odis  ```, since my UID GID mapping is wrong here.  


```bash
docker run -it --rm -e UID=1111 -e GID=1111 -v ./data-odis:/data -w /data  adfreiburg/qlever:latest -c "qlever -q Qleverfile.odis get-data && qlever -q Qleverfile.odis  index"
```

We now have an index we are reading to run qlever on via Docker like in the compose file in the main level of this repo.

We could just as easily done this in a data volume.  All we need to do is fetch the Qleverfile in that case.  



