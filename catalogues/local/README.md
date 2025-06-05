# Localhost  README

## About

Some notes for running locally to a machine named workstation.lan

## quickstart

### where to change to the local client address

```bash
server_compose.yaml
55:      QLEVER_HOST: "http://workstation.lan:7007"
```


```bash
Qleverfile-ui.yml
6:    baseUrl: https://workstation.lan:7007
252:    mapViewBaseURL: "https://workstation.lan:9090"
```

### where to change the locations to download from

```bash
Qleverfile-odis
10:BASE_URL          = http://ossapi.oceaninfohub.org/public
11:GET_DATA_CMD      = curl -sLo odis.nq.zip -C - ${BASE_URL}/odis.nq.zip && unzip -q -o odis.nq.zip && rm odis.nq.zip

initialize_compose.yaml
28:    image: alpine/curl
36:      sh -c "curl -fLo /data/Qleverfile.odis http://ossapi.oceaninfohub.org/public/ioc-local/Qleverfile-odis &&
37:      curl -fLo /data/Qleverfile-ui.yml http://ossapi.oceaninfohub.org/public/ioc-local/Qleverfile-ui.yml &&
38:      curl -fLo /data/odis.ui-db.sqlite3 http://ossapi.oceaninfohub.org/public/ioc-local/odis.ui-db.sqlite3 &&
39:      curl -fLo /data/odis.settings.json http://ossapi.oceaninfohub.org/public/ioc-local/odis.settings.json &&
```


## Notes

Do I need to address: 

```bash
docker exec -i qlever.ui.odis bash -c "python manage.py config default /app/db/Qleverfile-ui.yml --hide-all-other-backends"
```

domain: https://workstation.lan/

docker volume create ql_dvol

In Qleverfile:

```SYSTEM = docker```   vs  ```SYSTEM = native```

Simple SPARQL check via curl on the Qlever port for good feelings (jq is optional of course):

```bash
curl -s "http://workstation.lan:7007" -H "Accept: application/qlever-results+json" -H "Content-type: application/sparql-query" --data "SELECT * WHERE { ?s ?p ?o } LIMIT 10"  | jq
```

