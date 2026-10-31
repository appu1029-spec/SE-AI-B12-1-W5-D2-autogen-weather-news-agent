import asyncio
from ddgs import DDGS
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

def search_weather_news(city: str) -> str:
    """Search the web for today's weather news for a given city.

    Use this tool when the user wants the current weather or today's
    weather news for a city. Do not use it for general trivia.
    """
    return str(DDGS().news(query=f"{city} weather today", max_results=5))

city = input("Which city? ")
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

agent = AssistantAgent(
    name="weather_news",
    model_client=model_client,
    tools=[search_weather_news],
    system_message="You are a weather news assistant. Use the search tool to find today's weather news for the city. Reply in exactly 3 short lines, one sentence per line, each on its own line. Only mention what applies to that city. Do not include links, URLs or markdown.",
    reflect_on_tool_use=True,
)

async def main():
    await Console(agent.run_stream(task=f"Give me today's weather news for {city} in exactly 3 short lines, one sentence per line, each on its own line."))
    await model_client.close()

asyncio.run(main())