from google.adk.agents import ParallelAgent, SequentialAgent, LlmAgent
from .tools import fetch_weather, fetch_news, geocode_city

weather_agent = LlmAgent(
    name="WeatherAgent",
    model="gemini-2.0-flash",
    instruction="Fetch today's weather forecast and save it to state['weather']. You are responsible for passing the latitude and longitude",
    output_key="weather",
    tools=[fetch_weather, geocode_city]
)
news_agent = LlmAgent(
    name="NewsAgent",
    model="gemini-2.0-flash",
    instruction="Fetch the top news headlines and save them to state['headlines'].",
    output_key="headlines",
    tools=[fetch_news]
)

fetch_parallel = ParallelAgent(
    name="WeatherAndNewsFetcher",
    sub_agents=[weather_agent, news_agent]
)

report_agent = LlmAgent(
    name="DailyBriefingReporter",
    model="gemini-2.0-flash",
    instruction=(
        "Combine state['weather'] and state['headlines'] "
        "into a concise daily briefing."
    )
)

root_agent = SequentialAgent(
    name="DailyBriefingWorkflow",
    sub_agents=[fetch_parallel, report_agent]
)
