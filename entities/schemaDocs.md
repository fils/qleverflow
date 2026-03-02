# Entity extraction


## Appendix


### Full schema

```json
{
    "entities": {
        "person": [
            "scientists"
        ],
        "geospatial region": [
            "Atlantic",
            "Southampton",
            "Cape Cod"
        ],
        "marine biodiversity": [],
        "species occurrence": [],
        "occurrence records": [],
        "marine species": [],
        "taxon": [],
        "species distribution": [],
        "dna sequences": [],
        "measurements and facts": [
            "salinity",
            "temperature",
            "surface hydrography",
            "pressure",
            "density time series"
        ],
        "migratory marine species": [],
        "organizations": [
            "National Oceanography Centre"
        ],
        "projects": [
            "RAPID-WATCH",
            "WAVE",
            "Western Atlantic Variability Experiment"
        ],
        "invasive species": [],
        "marine regions": [],
        "ecosystem health": [],
        "undescribed biodiversity": [],
        "genetic analysis": [],
        "range shifts": [],
        "area-based management": [],
        "conservation efforts": [],
        "policies": [],
        "procedures": [],
        "indicators": [],
        "ecosystems": []
    }
}
```


Here is an example encoding these elements


```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "Example Marine Habitat Dataset",
  "description": "A dataset describing maerl beds and related observations in Falmouth Harbour areas, from which entities have been extracted.",
  "additionalProperty": [
    {
      "@type": "PropertyValue",
      "name": "geospatial region",
      "value": [
        "Falmouth Harbour",
        "Queens Wharf"
      ]
    },
    {
      "@type": "PropertyValue",
      "name": "marine species",
      "value": [
        "Lithothamnion corallioides",
        "Phymatolithon calcareum"
      ]
    },
    {
      "@type": "PropertyValue",
      "name": "taxon",
      "value": [
        "Phymatolithon calcareum",
        "Lithothamnion corallioides"
      ]
    },
    {
      "@type": "PropertyValue",
      "name": "organizations",
      "value": [
        "Falmouth Harbour commission",
        "Royal Haskoning Ltd.",
        "Falmouth Docks and Engineering Co. Ltd.",
        "Falmouth Harbour Commissioners"
      ]
    },
    {
      "@type": "PropertyValue",
      "name": "procedures",
      "value": [
        "in situ habitat observations",
        "diver sediment coring",
        "diver video transects"
      ]
    },
    {
      "@type": "PropertyValue",
      "name": "ecosystems",
      "value": [
        "maerl beds"
      ]
    }
  ]
}
```


Desired JSON format from query is like:

```json
{
  "results": [
    {
      "text": "description1",
      "kv": [
        { "key": "apname1", "value": "apvalue1" },
        { "key": "apname2", "value": "apvalue2" },
        { "key": "apnameN", "value": "apvalueN" }
      ]
    },
    {
      "text": "description2",
      "kv": [
        { "key": "apname1", "value": "apvalue1" },
        { "key": "apname2", "value": "apvalue2" },
        { "key": "apnameN", "value": "apvalueN" }
      ]
    }
  ]
}
```

Desired langextract format of

```python
 examples = [
        lx.data.ExampleData(
            text="text",
            extractions=[
                lx.data.Extraction(extraction_class="kv.key", extraction_text="kv.value"),
            ]
        )
    ]

```
