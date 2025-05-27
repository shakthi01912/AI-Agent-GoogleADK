from google.adk.agents import SequentialAgent  # Corrected module path
from main_agent.subAgents.classifier_agent import root_agent as classifier_agent
from .subAgents.user_manager_agent import root_agent as user_manager_agent
from .subAgents.response_generator_agent import root_agent as response_generator_agent

# Create sequential agent with just Agent 1 for now
root_agent = SequentialAgent(
    name="EmailClassificationPipeline",
    sub_agents=[classifier_agent , user_manager_agent , response_generator_agent],
    description="Pipeline that classifies emails and checks user existence",
)