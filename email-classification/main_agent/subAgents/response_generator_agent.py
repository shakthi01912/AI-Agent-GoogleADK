from google.adk.agents import Agent
import sys
import os

# Add root directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from system_instruction.response_generator_instruction import RESPONSE_GENERATOR_INSTRUCTION

root_agent = Agent(
    name="response_generator",
    model="gemini-1.5-flash",
    description="Generates personalized email responses based on classification and user status",
    instruction=RESPONSE_GENERATOR_INSTRUCTION,
    tools=[]  # No tools needed for response generation
)

def generate_response(combined_input: str):
    """Generate email response based on Agent 1 + Agent 2 output"""
    return root_agent.run(combined_input)