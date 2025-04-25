from fastapi import FastAPI, HTTPException, Query
from typing import Dict
import requests
import xml.etree.ElementTree as ET
from requests.exceptions import HTTPError
from xml.etree.ElementTree import ParseError
from fastapi_mcp import FastApiMCP

from .tools import fetch_weather, fetch_news, geocode_city

app = FastAPI()

@app.get("/get_geocode", operation_id="get_geocode" )
async def get_geocode(city: str = Query(..., description="City name (e.g. São Paulo, Brazil)")):
    try:
        return geocode_city(city)
    except HTTPError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/get_weather", operation_id="get_weather")
async def get_weather(
    latitude: float = Query(..., description="Latitude of location"),
    longitude: float = Query(..., description="Longitude of location")
):
    try:
        return {"weather": fetch_weather(latitude, longitude)}
    except HTTPError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Unexpected response format: {e}")


@app.get("/get_news",  operation_id="get_news")
async def get_news(query: str = Query(..., description="Search term for news")):
    try:
        return {"headlines": fetch_news(query)}
    except HTTPError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ParseError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse RSS feed: {e}")

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for basic uptime monitoring."""
    return {"status": "ok"}



mcp = FastApiMCP(
    app,
    name="Get the Weather, Latitudes & Longitudes and News",
    description="This MCP server creates functions for Getting the Weather, Latitudes & Longitudes and News",
    base_url="http://localhost:8001",
)
mcp.mount()
