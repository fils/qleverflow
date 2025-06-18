# Deployment for Portainer.

**Local, see below**

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

# CONFIGURING THE UI
* initially the UI admin
* log into console in portainer/docker
* `python manage.py makemigrations --merge && python manage.py migrate`
* `./manage.py createsuperuser`
   * note this can be automated... 
* then go to the UI admin page in web browser: https://qlever-iu.geocodes-aws-dev.earthcube.org/admin
  * add the url, with the full path, since users will be using this.
  `https://qlever-base.geocodes-aws-dev.earthcube.org`
  * be ure that the Sort Key is NOT ZERO
  * map base (needs to be tested):
  `https://qlever-petrimaps.geocodes-aws-dev.earthcube.org`
  
 ![admin_add.png](admin_add.png)

## Untested. Run an additional container using qlever_namespace.yaml
```
QLEVER_NET=base
PROJECT=deepoceans
HOST=geocodes-aws-dev.earthcube.org
QLEVER_CONFIG=deepoceans
```

## LOCAL
run with qlever_services_override.yaml


`/usr/local/bin/docker compose -f /Users/valentin/development/dev_earthcube/qleverflow/deployment/qlever_services.yaml -p deployment up -d qlever-server-base
`

Quirks:
* catalogues/local/Qleverfile-ui-deploy.yml uses port 7019, because that is what is used in the geocodes demo and deepoceans ports
* you can't have the network treafik_proxy and qlever-network-base defined externally
