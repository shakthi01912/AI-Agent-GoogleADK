def preprocess_email(email_content: str) -> str:
    """
    Preprocesses email content to improve classification accuracy.
    
    Args:
        email_content: Raw email content
        
    Returns:
        Preprocessed email content
    """
    # Remove email signatures, clean formatting, normalize text
    # For MVP, just do basic cleaning
    
    # Remove multiple newlines
    cleaned_content = ' '.join(email_content.split())
    
    return cleaned_content