import requests
import os
from urllib.parse import urlparse


def read_shapefile(shapefile):
    """
    Read a shapefile that can be either a URL or a local file path.

    Args:
        shapefile (str): Either a URL or a local file path to the shapefile

    Returns:
        str: The content of the shapefile as a string
    """
    try:
        # Check if the shapefile argument is a URL
        parsed = urlparse(shapefile)
        if parsed.scheme in ('http', 'https'):
            # It's a URL, fetch it
            response = requests.get(shapefile)
            response.raise_for_status()
            return response.text
        else:
            # It's a local file path
            if not os.path.exists(shapefile):
                raise FileNotFoundError(f"Local file not found: {shapefile}")

            with open(shapefile, 'r', encoding='utf-8') as file:
                return file.read()

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching URL {shapefile}: {e}")
    except FileNotFoundError as e:
        raise Exception(f"File error: {e}")
    except Exception as e:
        raise Exception(f"Error reading shapefile {shapefile}: {e}")