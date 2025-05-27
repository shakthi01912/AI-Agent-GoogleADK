from google.adk.agents import Agent
from .instruction import CLASSIFIER_INSTRUCTION  
from .tool import check_user_in_database

# Create the agent WITHOUT output_schema
root_agent = Agent(
    name="email_classifier",
    model="gemini-1.5-flash",
    description="Classifies emails into categories and extracts metadata",
    instruction=CLASSIFIER_INSTRUCTION,
    tools=[check_user_in_database]
)

def classify_email(email_content: str):
    """Classify email content"""
    return root_agent.run(email_content)