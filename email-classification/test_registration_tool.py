import sys
import os
sys.path.append('.')

from utils.user_registration_tool import register_new_user

# Test the tool
result = register_new_user(
    name="Agent Test User",
    email="agent.test@email.com", 
    phone="+1999999999"
)

print("Tool Result:")
print(result)