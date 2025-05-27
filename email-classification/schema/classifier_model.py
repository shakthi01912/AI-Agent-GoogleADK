from pydantic import BaseModel
from typing import Optional
from enum import Enum

class EmailClassification(str, Enum):
    SPAM = "Spam"
    NOT_SPAM = "Not Spam"
    GENERAL_INQUIRY = "General Inquiry"
    AFTERCARE = "Aftercare"

class EmailMetadata(BaseModel):
    sender_name: Optional[str] = None
    sender_email: Optional[str] = None
    sender_phone: Optional[str] = None

class EmailAnalysisResult(BaseModel):
    classification_type: EmailClassification
    email: EmailMetadata
    user_exists: bool = False
    reasoning: Optional[str] = None