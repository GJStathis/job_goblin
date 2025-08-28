import asyncio
from dotenv import load_dotenv
from src.profiler_agent import profiler_agent
from agents import Agent, Runner

async def main():
    load_dotenv()
    print("API keys loaded!")
    print ("Starting Profiler Agent...")
    result = Runner.run_sync(profiler_agent, "Create a job profile for a software developer")
    print("Profiler Agent result:", result)


if __name__ == "__main__":
    asyncio.run(main())