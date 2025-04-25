import requests
import xml.etree.ElementTree as ET

def geocode_city(city: str) -> dict:
    """
    Look up latitude & longitude for a given city name via OSM Nominatim.

    Args:
        city: City name (e.g. "São Paulo, Brazil")

    Returns:
        A dict: {"latitude": float, "longitude": float}

    Raises:
        HTTPError: on network/HTTP errors
        ValueError: if no results are returned
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json", "limit": 1}
    headers = {"User-Agent": "ADK-Geocoder/1.0"}
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    results = resp.json()
    if not results:
        raise ValueError(f"No geocoding result for '{city}'")
    lat = float(results[0]["lat"])
    lon = float(results[0]["lon"])
    return {"latitude": lat, "longitude": lon}

def fetch_weather(latitude: float, longitude: float) -> str:
    """Fetch current weather from Open-Meteo for the given coordinates.

    Makes a GET request to the Open-Meteo API to retrieve the current
    weather conditions (temperature and wind speed) for the specified
    latitude and longitude.

    Args:
        latitude: The latitude of the location (float).
        longitude: The longitude of the location (float).

    Returns:
        A formatted string describing the current weather conditions
        (temperature and wind speed) at the location. Example:
        "Location (52.52, 13.41): 15.0°C, wind 10.0 km/h"

    Raises:
        requests.exceptions.HTTPError: If the API request fails (e.g., network
            issue, invalid coordinates causing a 4xx/5xx response).
        KeyError: If the expected 'current_weather' key or its sub-keys
            ('temperature', 'windspeed') are missing from the API response.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
    # Raises KeyError if 'current_weather' is not in the response
    cw = resp.json()["current_weather"]
    # Raises KeyError if 'temperature' or 'windspeed' are not in cw
    return (
        f"Location ({latitude}, {longitude}): "
        f"{cw['temperature']}°C, wind {cw['windspeed']} km/h"
    )


def fetch_news(query: str) -> str:
    """Fetch top 5 news headlines matching the query from Google News RSS.

    Constructs a Google News RSS feed URL based on the query, fetches the
    feed, parses the XML, and extracts the titles and links of the top 5
    news items.

    Args:
        query: The search term to use for finding news headlines (str).

    Returns:
        A string containing up to 5 news headlines, each formatted as
        "- Title — Link" and separated by newlines. Returns an empty
        string if no items are found or if the RSS feed structure is
        unexpected.

    Raises:
        requests.exceptions.HTTPError: If the request to the Google News RSS
            feed fails (e.g., network issue, server error).
        xml.etree.ElementTree.ParseError: If the content received from the
            RSS feed is not valid XML.
    """
    # URL encode the query to handle special characters safely
    encoded_query = requests.utils.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    resp = requests.get(url)
    resp.raise_for_status() # Raises HTTPError for bad responses
    # Raises ParseError if resp.content is not valid XML
    root = ET.fromstring(resp.content)
    # Find item elements within the channel
    items = root.findall(".//item")[:5] # Limit to top 5
    result = []
    for item in items:
        # Use .findtext() with default to handle potentially missing elements gracefully
        title = item.findtext("title", default="[No Title]")
        link  = item.findtext("link", default="#")
        result.append(f"- {title} — {link}")
    return "\n".join(result)
