from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent


MCP_URL = "http://localhost:8001/mcp"

async def geocode_city_mcp(city: str, **kwargs) -> dict:
    """
    Proxy to MCP 'geocode_city' tool.
    Returns: {"latitude": float, "longitude": float}
    """
    tx = kwargs.get("tx")
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=SseServerParams(url=MCP_URL, headers={})
    )
    async with exit_stack:
        tool = next(t for t in tools if t.name == "get_geocode")
        return await tool.run_async(
            args={"city": city},
            tool_context=tx
        )

async def fetch_weather_mcp(latitude: float, longitude: float, **kwargs) -> str:
    """
    Proxy to MCP 'fetch_weather' tool.
    Returns: A string like "Location (...): 15.0°C, wind 10.0 km/h"
    """
    tx = kwargs.get("tx")
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=SseServerParams(url=MCP_URL, headers={})
    )
    async with exit_stack:
        tool = next(t for t in tools if t.name == "get_weather")
        return await tool.run_async(
            args={"latitude": latitude, "longitude": longitude},
            tool_context=tx
        )

async def fetch_news_mcp(query: str, **kwargs) -> str:
    """
    Proxy to MCP 'fetch_news' tool.
    Returns: A newline‐separated string of headlines.
    """
    tx = kwargs.get("tx")
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=SseServerParams(url=MCP_URL, headers={})
    )
    async with exit_stack:
        tool = next(t for t in tools if t.name == "get_news")
        return await tool.run_async(
            args={"query": query},
            tool_context=tx
        )

weather_agent = LlmAgent(
    name="WeatherAgent",
    model="gemini-2.0-flash",
    instruction=(
        "Given a city name, first call geocode_city_mcp(city) to get coords, "
        "then call fetch_weather_mcp(latitude, longitude) and save to state['weather']."
    ),
    output_key="weather",
    tools=[geocode_city_mcp, fetch_weather_mcp]
)

news_agent = LlmAgent(
    name="NewsAgent",
    model="gemini-2.0-flash",
    instruction=(
        "Given a topic, call fetch_news_mcp(query) and save the top headlines to state['headlines']."
    ),
    output_key="headlines",
    tools=[fetch_news_mcp]
)

root_agent = SequentialAgent(
    name="DailyBriefingWorkflow",
    sub_agents=[
        ParallelAgent(name="FetchAll", sub_agents=[weather_agent, news_agent]),
        LlmAgent(
            name="Reporter",
            model="gemini-2.0-flash",
            instruction=(
                "Combine state['weather'] and state['headlines'] into a concise briefing."
            )
        )
    ]
)
