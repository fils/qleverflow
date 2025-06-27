# Summary needs to be redone.
endpoint:
https://qlever.geocodes-aws-dev.earthcube.org/graphspace/facetsearch

https://qlever.geocodes-aws-dev.earthcube.org/graphspace/facetsearch?cmd=stats

ui for testing:
https://qlever-iu.geocodes-aws-dev.earthcube.org/facetsearch

we do a full text query, so that needs to be replaced



The queries come from utilities, and facetsearch
loose files from utilities

original from facetsearch:
* [blaze](https://github.com/earthcube/facetsearch/tree/master/client/src/sparql_blaze)
* [others](https://github.com/earthcube/facetsearch/tree/master/client/src/sparql)

experiments are from working on the search
## NOTES
Best to test the UI. it provides feedback that is better than just running RDF/SParql from jetbrains

### UI Saving query.
Python templates (aka ${q}) using in old queries break the saving in the ui of qlever. **EVEN IF IN A COMMENT**

## Present Status
in experimental, there are queries that work (best)[text_g_old_v4_nospatial.rq]

Getting LAT/LONG kills the server (see)[text_g_old_killer.rq]

### Troubleshooting:
If the server dies, it rebuilds and reboots... that's the good and bad of it.



