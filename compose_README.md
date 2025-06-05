# Notes on building indexes via docker

## Intro

As Qlever is run based on an initially pre-computed index, We need it 
to, in the context of docker, set up a data volume we can populate with
a Qleverfile.  The Qleverfile is a configuration file that provides
data source, citations, indexing and UI settings.


### Address locations:

There are a few locations where the address is set.

- [ ] compose files, can set these with environment variables
- [ ] Qleverfile-ui.yml
  - baseUrl 
  - mapViewBaseURL

### Building text index

The command to build the index and overwrite
```bash
 qlever -q  Qleverfile-odis index --overwrite-existing --text-index from_literals
 ```

which is materialized as

```bash

echo '{ "add-text-index": true, "ascii-prefixes-only": false, "num-triples-per-batch": 100000 }' > odis.settings.json
docker run --rm -u $(id -u):$(id -g) -v /etc/localtime:/etc/localtime:ro -v $(pwd):/index -w /index --name qlever.index.odis --init --entrypoint bash docker.io/adfreiburg/qlever:latest -c 'cat odis.nq | IndexBuilderMain -i odis -s odis.settings.json -F nq -f - --text-words-from-literals | tee odis.index-log.txt'     
```

where the key part is 

```bash
 IndexBuilderMain -i odis -s odis.settings.json -F nq -f - --text-words-from-literals 
 ```

Then for the server, when running, the -t I think must be the text index.

```bash
ServerMain -i odis -j 8 -p 7007 -m 25G -c 20G -e 1G -k 200 -s 240s -a odis_7643543846_6dMISzlPrD7i -t
```

### Prerequisists

- [X] ql_dvol data volume
- [X] Qlever file at an accessible network location
- [X] RDF data at an accessible network location
- [ ] X.settings.json at an accessible network location
- [ ] Qlever UI file at an accessible network location
  - Important, this is needed for the front end to work (sqlite error)

## Notes

This needs to become a script, since qlever will invoke docker, and we cannot call docker within docker (easily enough to want to do it here).


Part of what we need to resolve from the index step.   
```bash
myapp-1         | Command: index
myapp-1         | 
myapp-1         | echo '{ "ascii-prefixes-only": false, "num-triples-per-batch": 100000 }' > odis.settings.json
myapp-1         | docker run --rm -u $(id -u):$(id -g) -v /etc/localtime:/etc/localtime:ro -v $(pwd):/index -w /index --init --entrypoint bash --name qlever.index.odis docker.io/adfreiburg/qlever:latest -c 'cat odis.nq | IndexBuilderMain -i odis -s odis.settings.json -F nq -f - | tee odis.index-log.txt'                                                                                              
myapp-1         | 
myapp-1         | Building the index failed: /usr/bin/bash: line 1: docker: command not found
```

First, make a dvol from the command line.

```bash
docker volume create ql_dvol
```

I need to then run a command via docker to download and build
the index in the data volume.  Let's first download the Qleverfile.

```bash
docker run --rm \
  -v ql_dvol:/data_in_volume \
  alpine/curl \
  sh -c "curl -fLo /data_in_volume/Qleverfile.odis http://ossapi.oceaninfohub.org/public/Qleverfile-odis && echo 'File Qleverfile.odis downloaded successfully to /data_in_volume/'"
  ```

We can then build our index.

```bash
docker run -it --rm --user 1000:1000 \
 -v ql_dvol:/data -w /data  adfreiburg/qlever:latest -c "qlever -q Qleverfile.odis get-data && qlever -q Qleverfile.odis  index"
```

```bash
docker run \
  --user 1000:1000 \
  --volume ql_dvol:/data \
  --workdir /data \
  -i \
  -t \
  adfreiburg/qlever:latest "qlever -q Qleverfile.odis index"
  ```

echo '{ "ascii-prefixes-only": false, "num-triples-per-batch": 100000 }' > odis.settings.json
docker run --rm -u $(id -u):$(id -g) -v /etc/localtime:/etc/localtime:ro -v $(pwd):/index -w /index --init --entrypoint bash --name qlever.index.odis docker.io/adfreiburg/qlever:latest -c 'cat odis.nq | IndexBuilderMain -i odis -s odis.settings.json -F nq -f - | tee odis.index-log.txt'


The following is a simple help parameter example you can use to validate running the 
image.

```bash
docker run -it --rm -e UID=1111 -e GID=1111 -v ./data-odis:/data -w /data  adfreiburg/qlever:latest -c "qlever --help"
```
