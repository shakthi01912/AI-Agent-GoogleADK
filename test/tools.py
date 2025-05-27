# from datetime import datetime
# from typing import Dict, List, Optional

# # Mock Patient Database
# MOCK_PATIENTS_DB: List[Dict] = [
#     {
#         "id": "550e8400-e29b-41d4-a716-446655440001",
#         "created_at": "2024-01-15T10:30:00Z",
#         "updated_at": "2024-01-15T10:30:00Z",
#         "name": "John Doe",
#         "phone": "+1234567890",
#         "email": "john.doe@email.com",
#         "customer_id": "550e8400-e29b-41d4-a716-446655440010",
#         "consent_form_id": "550e8400-e29b-41d4-a716-446655440020",
#         "workplace_id": "550e8400-e29b-41d4-a716-446655440030"
#     },
#     {
#         "id": "550e8400-e29b-41d4-a716-446655440002",
#         "created_at": "2024-02-20T14:15:00Z",
#         "updated_at": "2024-02-20T14:15:00Z",
#         "name": "Jane Smith",
#         "phone": "+1987654321",
#         "email": "jane.smith@email.com",
#         "customer_id": "550e8400-e29b-41d4-a716-446655440011",
#         "consent_form_id": "550e8400-e29b-41d4-a716-446655440021",
#         "workplace_id": "550e8400-e29b-41d4-a716-446655440031"
#     },
#     {
#         "id": "550e8400-e29b-41d4-a716-446655440003",
#         "created_at": "2024-03-10T09:45:00Z",
#         "updated_at": "2024-03-10T09:45:00Z",
#         "name": "Bob Johnson",
#         "phone": "+1122334455",
#         "email": "bob.johnson@email.com",
#         "customer_id": "550e8400-e29b-41d4-a716-446655440012",
#         "consent_form_id": None,
#         "workplace_id": "550e8400-e29b-41d4-a716-446655440032"
#     },
#     {
#         "id": "550e8400-e29b-41d4-a716-446655440004",
#         "created_at": "2024-04-05T16:20:00Z",
#         "updated_at": "2024-04-05T16:20:00Z",
#         "name": "Alice Wilson",
#         "phone": "+1555666777",
#         "email": None,
#         "customer_id": "550e8400-e29b-41d4-a716-446655440013",
#         "consent_form_id": "550e8400-e29b-41d4-a716-446655440023",
#         "workplace_id": "550e8400-e29b-41d4-a716-446655440033"
#     }
# ]

# def check_user_in_database(email: str, phone: Optional[str] = None) -> bool:
  
#     print(f"🔍 TOOL CALLED: check_user_in_database(email='{email}', phone='{phone}')")
    
#     try:
#         # Check against mock data
#         for i, patient in enumerate(MOCK_PATIENTS_DB):
#             print(f"   Checking patient {i+1}: {patient.get('name')} - {patient.get('email')}")
            
#             # Check email match (handle None emails)
#             email_match = patient.get("email") and patient["email"].lower() == email.lower()
#             print(f"   Email match: {email_match} ('{patient.get('email')}' vs '{email}')")
            
#             if phone:
#                 # If phone is provided, check both email and phone
#                 phone_match = patient.get("phone") == phone
#                 print(f"   Phone match: {phone_match} ('{patient.get('phone')}' vs '{phone}')")
#                 if email_match and phone_match:
#                     print(f"✅ MATCH FOUND: {patient['name']} ({email}) with phone {phone}")
#                     return True
#             else:
#                 # If only email is provided, check email only
#                 if email_match:
#                     print(f"✅ MATCH FOUND: {patient['name']} ({email})")
#                     return True
        
#         print(f" NO MATCH: {email} not found in database")
#         return False
        
#     except Exception as e:
#         print(f"⚠️ ERROR in check_user_in_database: {str(e)}")
#         return False