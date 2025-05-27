# from pydantic import BaseModel
# from typing import Optional, Literal
# from enum import Enum
# from google.adk.agents import Agent

# class EmailClassification(str, Enum):
#     SPAM = "Spam"
#     NOT_SPAM = "Not Spam"
#     GENERAL_INQUIRY = "General Inquiry"
#     AFTERCARE = "Aftercare"

# # Email metadata nested structure
# class EmailMetadata(BaseModel):
#     sender_name: Optional[str] = None
#     sender_email: Optional[str] = None
#     sender_phone: Optional[str] = None

# class EmailAnalysisResult(BaseModel):
#     classification_type: EmailClassification
#     email: EmailMetadata
#     reasoning: Optional[str] = None

# # Simple agent without response_config
# root_agent = Agent(
#     name="email_classifier",
#     model="gemini-1.5-flash",
#     description="Classifies emails into categories and extracts metadata",
#     instruction="""
#     You are an advanced email classifier that categorizes emails and extracts metadata.

#     CLASSIFICATION RULES:

#     Spam: 
#     - Unsolicited commercial content
#     - Deceptive subject lines or sender addresses
#     - Phishing attempts or suspicious links
#     - Requests for personal/financial information
#     - Urgent threats or too-good-to-be-true offers
#     - Poor grammar, excessive capitalization, or suspicious formatting

#     Not Spam:
#     - Legitimate personal or business communication
#     - Expected newsletters or notifications
#     - Genuine inquiries or responses
#     - Official communications from known entities

#     General Inquiry:
#     - Questions about products, services, or general information
#     - New customer inquiries
#     - Information requests that don't relate to existing customers
#     - First-time contact from potential customers

#     Aftercare:
#     - Follow-up communications from existing customers
#     - Support requests from current customers
#     - Feedback, complaints, or reviews from past customers
#     - Questions about previous purchases or services

#     RESPONSE FORMAT:
#     You must respond with valid JSON in exactly this format:

#     {
#         "classification_type": "Spam" | "Not Spam" | "General Inquiry" | "Aftercare",
#         "email": {
#             "sender_name": "extracted name or null",
#             "sender_email": "extracted email address or null",
#             "sender_phone": "extracted phone number or null"
#         },
#         "reasoning": "brief explanation of classification"
#     }

#     METADATA EXTRACTION:
#     - Extract sender's name from email header, signature, or content and put in email.sender_name
#     - Extract sender's email address and put in email.sender_email
#     - Extract phone number if present in signature or content and put in email.sender_phone
#     - If information is not available, use null

#     Always respond with only the JSON object, no additional text.
#     """,
#     # tools=[check_user_in_database],
# )

# # Helper function to parse response if needed
# def parse_agent_response(response_text: str) -> EmailAnalysisResult:
#     """
#     Parse the agent's JSON response into a structured object
#     """
#     import json
#     try:
#         # Clean the response in case there's extra text
#         response_text = response_text.strip()

#         # Find JSON in the response
#         start_idx = response_text.find('{')
#         end_idx = response_text.rfind('}') + 1

#         if start_idx != -1 and end_idx != -1:
#             json_str = response_text[start_idx:end_idx]
#             result_dict = json.loads(json_str)
#             return EmailAnalysisResult(**result_dict)
#         else:
#             raise ValueError("No JSON found in response")

#     except Exception as e:
#         # Fallback if parsing fails
#         return EmailAnalysisResult(
#             classification_type=EmailClassification.NOT_SPAM,
#             reasoning=f"Parse error: {str(e)}"
#         )