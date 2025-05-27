from google.adk.agents import Agent
import sys
import os

# Add root directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from system_instruction.user_manager_instruction import USER_MANAGER_INSTRUCTION
from utils.user_registration_tool import register_new_user

root_agent = Agent(
    name="user_manager",
    model="gemini-1.5-flash",
    description="Manages user registration and status based on email classification results",
    instruction=USER_MANAGER_INSTRUCTION,
    tools=[register_new_user]
)

def manage_user(agent1_output: str):
    """Process Agent 1 output and manage user registration"""
    return root_agent.run(agent1_output)