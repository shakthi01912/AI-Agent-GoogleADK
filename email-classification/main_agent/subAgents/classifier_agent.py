from google.adk.agents import Agent
import os
import sys
root_path = os.path.join(os.path.dirname(__file__), '../..')
sys.path.append(root_path)

# Now import from the root directory
from system_instruction.classifier_instruction import CLASSIFIER_INSTRUCTION  
from utils.check_user_in_db_tool import check_user_in_database


root_agent = Agent(
    name="email_classifier",
    model="gemini-1.5-flash",
    description="Classifies emails into categories and extracts metadata",
    instruction=CLASSIFIER_INSTRUCTION,
    tools=[check_user_in_database]
)

def classify_email(email_content: str):
    return root_agent.run(email_content)