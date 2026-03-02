import os
from dotenv import load_dotenv
import langextract as lx
from langextract import extract
from langextract.providers.openai import OpenAILanguageModel
from collections import defaultdict
from results import examples

# Load environment variables from .env file
load_dotenv()

# Load API key
#api_key = os.getenv('LANGEXTRACT_API_KEY')

def extract_entities_langextract(text):
    """Extract entities using langextract with proper API usage."""
    # Brief prompt - let examples guide the extraction
    prompt_description = """Extract business entities: companies, executives, financial figures, quarters, locations, percentages, products, startups, regulatory bodies, stock_symbols, market_reaction. Use exact text."""

    # Provide example data to guide extraction with all entity types
    # examples = [
    #     lx.data.ExampleData(
    #         text="Microsoft Corp. (NYSE: MSFT) CEO Satya Nadella reported Q2 2024 revenue of $65B, down 5% quarter-over-quarter. The Seattle campus announced Azure cloud grew $28B. The firm bought ML startup NeuralFlow pending FTC review.",
    #         extractions=[
    #             lx.data.Extraction(extraction_class="company", extraction_text="Microsoft Corp."),
    #             lx.data.Extraction(extraction_class="executive", extraction_text="CEO Satya Nadella"),
    #             lx.data.Extraction(extraction_class="quarter", extraction_text="Q2 2024"),
    #             lx.data.Extraction(extraction_class="financial_figure", extraction_text="$65B"),
    #             lx.data.Extraction(extraction_class="percentage", extraction_text="5%"),
    #             lx.data.Extraction(extraction_class="market_reaction", extraction_text="down 5% quarter-over-quarter"),
    #             lx.data.Extraction(extraction_class="location", extraction_text="Seattle campus"),
    #             lx.data.Extraction(extraction_class="product", extraction_text="Azure cloud"),
    #             lx.data.Extraction(extraction_class="financial_figure", extraction_text="$28B"),
    #             lx.data.Extraction(extraction_class="startup", extraction_text="NeuralFlow"),
    #             lx.data.Extraction(extraction_class="regulatory_body", extraction_text="FTC"),
    #             lx.data.Extraction(extraction_class="stock_symbol", extraction_text="NYSE: MSFT")
    #         ]
    #     )
    # ]

    # Extract using proper API
#    resultOrig  = extract(
#        text_or_documents=text,
#        prompt_description=prompt_description,
#        examples=examples,
#        model_id="gemini-2.5-flash"
#    )

    # Do the extraction
    result = lx.extract(
        text_or_documents=text,
        prompt_description=prompt_description,
        examples=examples,
        # use_schema_constraints=True,
        model = OpenAILanguageModel(
            model_id='grok-4-1-fast',
            base_url='https://api.x.ai/v1',
            api_key= os.environ.get('XAI_API_KEY'),
        ),
        # model_id="grok-3-mini",
        # model_url="https://api.x.ai/v1",
        # api_key = os.environ.get('XAI_API_KEY'),
        extraction_passes=3,    # Improves recall through multiple passes
        max_workers=20,         # Parallel processing for speed
        max_char_buffer=1000    # Smaller contexts for better accuracy
    )


    return result


# Define the earnings report locally for this section
earning_report = """
This dataset consists of measurements of temperature, pressure and depth collected using conductivity-temperature-depth (CTD) casts, chlorophyll, water chemistry and biogenic silica data taken from CTD and underway samples, and underway meteorology, navigation and sea surface hydrography. Data were collected in the Southern Ocean, specifically the Drake Passage, Weddell Sea and Powell Basin, on the RRS James Clark Ross cruises JR255A (20th January to 03rd February 2012) and recovery cruise JR255B (04th February 22nd March 2012) Biogenic silica and chlorophyll samples were collected from the non-toxic underway and CTD Niskin bottles, filtered, dried and processed spectrophotometrically post-cruise. Similarly, water chemistry samples were collected, filtered and dried before post-cruise processing with an elemental analyser. A SeaBird CTD rosette was launched at stations throughout the cruise collecting temperature, pressure and depth values with an attached deep ocean thermometer collecting temperature data which were used to calibrate the CTD data. The underway oceanlogger was running through the duration of the cruises, excepting times for cleaning, entering and leaving port, and while alongside. The data were collected as part of the “Gliders: Excellent New Tools for Observing the Ocean (GENTOO)” project. The objectives of the GENTOO project are: (i) To quantify and understand the possible new source of dense water overflow and its variability; to determine the outflow's potential as an early indicator of Antarctic climate change; to assess the impact of changing dense overflows on the locations and strengths of the surface currents and frontal jets; to provide valuable constraints for climate models that describe how changes in ocean circulation feedback on and regulate climate change in polar latitudes. (ii) To determine the krill biomass distribution and (temporal and spatial) variability to the east of the Antarctic Peninsula and its likely impact on the circumpolar krill ecosystem; to assess the impact of any variations in the location of the frontal jets (from objective i) on the krill biomass distribution; to alleviate a severe regional lack of field data on krill, a key species in the Antarctic food web. To achieve the two objectives, our technological deliverable is a critical evaluation of our ability to measure (a) current velocity from a glider and (b) krill biomass from a glider. The data were collected under NERC lead grant NE/H01439X/1, with child grants NE/H014217/1, NE/H014756/1 and NE/H015078/1. The principal investigators were Prof. Karen Heywood,University of East Anglia, Environmental Sciences, Prof. Gwyn Griffiths, National Oceanography Centre, Science and Technology, Dr. Sophie Fielding, NERC British Antarctic Survey, Science Programmes and Dr. Stuart Bruce Dalziel, University of Cambridge, Applied Maths and Theoretical Physics, respectively. With regard the samples data (Biogenic silica, water chemistry and chlorophyll) it is important to note that these data ARE NOT the property of NERC. They belong to Walker Smith of the Virginia Institute of Marine Science(VIMS) who has supplied them in support of GENTOO. As such, he must be credited for use of the data. The CTD and underway navigation, meteorology and sea surface hydrography data have been received by BODC as raw files from the RRS James Clark Ross, are currently being processed and are available in raw format from BODC enquiries. The SBE-35 Deep Ocean Thermometer and biogenic silica, chlorophyll-a and particulate organic carbon/nitrogen samples data have been received by BODC as raw files from the RRS James Clark Ross, processed and quality controlled using in-house BODC procedures and will be made available online in the near future."

"""

# Extract entities with langextract
langextract_entities = extract_entities_langextract(earning_report)

print(f"Extracted {len(langextract_entities.extractions)} entities:")


# Group extractions by class using defaultdict
grouped_extractions = defaultdict(list)
for extraction in langextract_entities.extractions:
    grouped_extractions[extraction.extraction_class].append(extraction)

# Display grouped results
for entity_class, extractions in grouped_extractions.items():
    print(f"\n{entity_class.upper()} ({len(extractions)} found):")
    for extraction in extractions:
        print(f"  '{extraction.extraction_text}'")


# Save the results to a JSONL file
#lx.io.save_annotated_documents([result], output_name="extraction_results.jsonl", output_dir=".")
lx.io.save_annotated_documents([langextract_entities], output_name="extraction_results.jsonl", output_dir=".")

# Generate the visualization from the file
html_content = lx.visualize("extraction_results.jsonl")
with open("visualization.html", "w") as f:
    if hasattr(html_content, 'data'):
        f.write(html_content.data)  # For Jupyter/Colab
    else:
        f.write(html_content)
