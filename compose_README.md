# Notes on building indexes via docker

## Intro

As Qlever is run based on an initially pre-computed index, We need it 
to, in the context of docker, set up a data volume we can populate with
a Qleverfile.  The Qleverfile is a configuration file that provides
data source, citations, indexing and UI settings.

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
