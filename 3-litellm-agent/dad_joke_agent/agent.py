import random
from google.adk.agents import Agent

def get_dad_joke():
    jokes = [
        "Why did the chicken cross the road? To get to the other side!",
        "What do you call a belt made of watches? A waist of time.",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
    ]
    return random.choice(jokes)

# Much simpler! No LiteLLM needed
root_agent = Agent(
    name="dad_joke_agent",
    model="gemini-2.0-flash",  # Free Google model - no API key needed
    description="Dad joke agent",
    instruction="""
    You are a helpful assistant that can tell dad jokes. 
    Only use the tool `get_dad_joke` to tell jokes.
    """,
    tools=[get_dad_joke],
)