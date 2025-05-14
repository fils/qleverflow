# Deployment for Portainer.


# Three containers run:
* qlever-base.{HOST}
* qlever-ui.{HOST}
* qlever-petrimaps.{HOST}

use the qlever_services.yml for now.

Deploy with cut and paste for now.


| Variable      | default | note |
|---------------| --------| ------|
| HOST          | the host, | eg geocodes-aws-dev.earthcube.org |
| PROJECT       | geocodesexamples | the namespace for objects in portainer and traefik |
| QLEVER_CONFIG | geocodesexamples | name of the docker config | 
| QLEVER_NET    |  base | base namespace for that the qlevels might talk over |


## Untested. Run an additional container using qlever_namespace.yaml
