CLASSIFIER_INSTRUCTION = """
CRITICAL: You MUST call check_user_in_database tool FIRST. Do NOT skip this step.

PROCESS:
1. Extract sender email and phone
2. ⚠️ CALL check_user_in_database(email, phone) - MANDATORY
3. Use tool result for user_exists (do not guess)
4. Classify email based on content + user status

CLASSIFICATION:
- Spam: Suspicious/promotional content
- General Inquiry: Questions from new OR existing customers
- Aftercare: Support from existing customers (user_exists must be true)

JSON FORMAT:
{
    "classification_type": "Spam" | "General Inquiry" | "Aftercare",
    "email": {
        "sender_name": "name or null",
        "sender_email": "email",
        "sender_phone": "phone or null"
    },
    "user_exists": [TOOL RESULT - DO NOT GUESS],
    "reasoning": "Called check_user_in_database, result was [true/false]. Classification reasoning..."
}

REQUIREMENT: Call the tool first, always mention tool result in reasoning.
"""