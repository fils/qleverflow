from gliner2 import GLiNER2
import json

# Function to remove empty lists from the entities dict
def filter_empty_entities(entities):
    return {k: v for k, v in entities.items() if v}

def entities(extractor, text):

    # Load the model

    # Extract entities with descriptions for higher precision
    result = extractor.extract_entities(
        text,
        {
            "person": "Individuals involved in biodiversity research or conservation, such as scientists, researchers, or expedition participants like Graham J B Ross",
            "geospatial region": "Geographic areas or locations relevant to biodiversity studies, such as Albatross Bay, Gulf of Carpentaria, or Schirmacher Oasis",
            "marine biodiversity": "Diversity of life in marine environments, including flora, fauna, and ecosystems like coral reefs or mangrove habitats",
            "species occurrence": "Records of where and when species are found, such as sightings of copepods or scleractinian corals in specific reefs",
            "occurrence records": "Data entries documenting species presence, including counts, locations, and dates from surveys or expeditions",
            "marine species": "Species inhabiting marine environments, such as reef fishes, zooplankton, or marine algae collected in expeditions",
            "taxon": "Taxonomic units like species, genera, or families, including examples like Acropora spp. or Copepods",
            "species distribution": "Geographic spread of species, such as the range of zoanthids across the Great Barrier Reef and Torres Strait",
            "dna sequences": "Genetic material sequences used for analysis, such as allozymes or enzyme loci in population genetics studies of zoanthids",
            "measurements and facts": "Quantitative data and observations, like abundance counts, biomass, or environmental metrics such as depth and salinity",
            "migratory marine species": "Marine species that migrate, potentially including fish or sharks observed in surveys across reefs or shelves",
            "organizations": "Entities involved in research or conservation, such as Australian Institute of Marine Science (AIMS) or Conservation International (CI)",
            "projects": "Initiatives or studies, like the Marine Rapid Assessment Program (RAP) or expeditions to the Kimberley for marine flora and fauna documentation",
            "invasive species": "Non-native species impacting ecosystems, potentially referenced in biodiversity assessments or surveys of introduced taxa",
            "marine regions": "Defined marine areas, such as the Great Barrier Reef World Heritage Area or MOU74 Box in the Australian Exclusive Economic Zone",
            "ecosystem health": "Condition of ecosystems, assessed through indicators like coral cover, bleaching severity, or nutrient budgets",
            "undescribed biodiversity": "Unidentified or newly discovered species, such as potentially new molluscs or crustaceans from expeditions",
            "genetic analysis": "Studies of genetic variation, like electrophoresis or gene frequency analysis in zoanthid populations",
            "range shifts": "Changes in species distribution over time, potentially due to environmental factors like climate change in marine habitats",
            "area-based management": "Management strategies for specific areas, such as zoning in Marine Protected Areas (MPAs) or green zones on shoals",
            "conservation efforts": "Actions to protect biodiversity, like bans on fishing in Ashmore Reef or baseline monitoring in Plymouth Sound",
            "policies": "Guidelines or regulations, such as those from the National Estates Grant Program or MOU74 agreements for fishing access",
            "procedures": "Methods or protocols in research, like sampling designs, replication, or rapid assessment techniques in surveys",
            "indicators": "Metrics for ecosystem assessment, such as indicator species, taxonomic distinctness, or degree heating weeks (DHWs)",
            "ecosystems": "Interconnected biological communities and environments, like coral reef ecosystems, mangrove systems, or sediment habitats"
        }
        # {
        #     "person": "Individuals involved in biodiversity research or conservation, such as scientists, researchers, or expedition participants like Graham J B Ross",
        #     "geospatial region": "Geographic areas or locations relevant to biodiversity studies, such as Albatross Bay, Gulf of Carpentaria, or Schirmacher Oasis",
        #     "marine biodiversity": "Diversity of life in marine environments, including flora, fauna, and ecosystems like coral reefs or mangrove habitats",
        #     "species occurrence": "Records of where and when species are found, such as sightings of copepods or scleractinian corals in specific reefs",
        #     "occurrence records": "Data entries documenting species presence, including counts, locations, and dates from surveys or expeditions",
        #     "marine species": "Species inhabiting marine environments, such as reef fishes, zooplankton, or marine algae collected in expeditions",
        #     "taxon": "Taxonomic units like species, genera, or families, including examples like Acropora spp. or Copepods",
        #     "species distribution": "Geographic spread of species, such as the range of zoanthids across the Great Barrier Reef and Torres Strait",
        #     "dna sequences": "Genetic material sequences used for analysis, such as allozymes or enzyme loci in population genetics studies of zoanthids",
        #     "measurements and facts": "Quantitative data and observations, like abundance counts, biomass, or environmental metrics such as depth and salinity",
        #     "migratory marine species": "Marine species that migrate, potentially including fish or sharks observed in surveys across reefs or shelves",
        #     "organizations": "Entities involved in research or conservation, such as Australian Institute of Marine Science (AIMS) or Conservation International (CI)",
        #     "projects": "Initiatives or studies, like the Marine Rapid Assessment Program (RAP) or expeditions to the Kimberley for marine flora and fauna documentation",
        #     "invasive species": "Non-native species impacting ecosystems, potentially referenced in biodiversity assessments or surveys of introduced taxa",
        #     "marine regions": "Defined marine areas, such as the Great Barrier Reef World Heritage Area or MOU74 Box in the Australian Exclusive Economic Zone",
        #     "ecosystem health": "Condition of ecosystems, assessed through indicators like coral cover, bleaching severity, or nutrient budgets",
        #     "undescribed biodiversity": "Unidentified or newly discovered species, such as potentially new molluscs or crustaceans from expeditions",
        #     "genetic analysis": "Studies of genetic variation, like electrophoresis or gene frequency analysis in zoanthid populations",
        #     "range shifts": "Changes in species distribution over time, potentially due to environmental factors like climate change in marine habitats",
        #     "area-based management": "Management strategies for specific areas, such as zoning in Marine Protected Areas (MPAs) or green zones on shoals",
        #     "conservation efforts": "Actions to protect biodiversity, like bans on fishing in Ashmore Reef or baseline monitoring in Plymouth Sound",
        #     "policies": "Guidelines or regulations, such as those from the National Estates Grant Program or MOU74 agreements for fishing access",
        #     "procedures": "Methods or protocols in research, like sampling designs, replication, or rapid assessment techniques in surveys",
        #     "indicators": "Metrics for ecosystem assessment, such as indicator species, taxonomic distinctness, or degree heating weeks (DHWs)",
        #     "ecosystems": "Interconnected biological communities and environments, like coral reef ecosystems, mangrove systems, or sediment habitats"
        # }
    )

    #print(result)
    # print(json.dumps(result, indent=4))
    # Output: {'entities': {'medication': ['ibuprofen'], 'dosage': ['400mg'], 'symptom': ['severe headache'], 'time': ['2 PM']}}

    # Apply the filter
    result['entities'] = filter_empty_entities(result['entities'])
    result['description'] = text

    return(json.dumps(result, indent=4))
