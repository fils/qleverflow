# Notes on building indexes via docker

As Qlever is run based on an initially pre-computed index, We need 
to, in the context of docker, set up a data volume we can populate with
a Qleverfile.  The Qleverfile is a configuration file that provides
data source, citations, indexing and UI settings.

First, make a dvol from the command line.

```bash
docker volume create ql_dvol
```

I need to then run a command via docker to download and build
the index in the data volume.  Let's first download the Qleverfile.

```bash
docker run --rm \
  -v my_downloaded_data:/data_in_volume \
  alpine/curl \
  sh -c "curl -fLo /data_in_volume/Qleverfile.odis https://example.com/path/to/your/Qleverfile.odis && echo 'File Qleverfile.odis downloaded successfully to /data_in_volume/'"
  ```

We can then build our index.

```bash
docker run -it --rm -e UID=1111 -e GID=1111 -v my_downloaded_data:/data -w /data  adfreiburg/qlever:latest -c "qlever -q Qleverfile.odis get-data && qlever -q Qleverfile.odis  index"
```

The following is a simple help parameter example you can use to validate running the 
image.

```bash
docker run -it --rm -e UID=1111 -e GID=1111 -v ./data-odis:/data -w /data  adfreiburg/qlever:latest -c "qlever --help"
```
