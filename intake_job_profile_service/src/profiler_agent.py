from openai import OpenAI
from openai_agents import Agent, WebSearchTool, function_tool

@function_tool
def save_results(output):
    print("Saving responses to memories...")
    return "Results saved to the memory database."

profiler_agent = Agent(
    name ="Profiler Agent",
    instructions="An agent that creates a profile for the ideal job for the candidate.",
    tools=[WebSearchTool(), save_results],
)

    