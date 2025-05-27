import os
import sys
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Windows-specific asyncio event loop policy
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# FastAPI app
app = FastAPI(
    title="Mock Patient Database API",
    description="Mock database API for patient data",
    version="1.0.0"
)

# Pydantic Models
class UserCheckRequest(BaseModel):
    email: str
    phone: Optional[str] = None

class UserCheckResponse(BaseModel):
    user_exists: bool
    patient_id: Optional[str] = None
    patient_name: Optional[str] = None
    message: str

class UserRegistrationRequest(BaseModel):
    name: str
    email: str
    phone: str
    customer_id: Optional[str] = None
    consent_form_id: Optional[str] = None  
    workplace_id: Optional[str] = None

class UserRegistrationResponse(BaseModel):
    success: bool
    user_id: Optional[str] = None
    message: str
    user_data: Optional[Dict] = None

# Mock database
MOCK_PATIENTS_DB: List[Dict] = [
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        "name": "John Doe",
        "phone": "+1234567890",
        "email": "john.doe@email.com",
        "customer_id": "550e8400-e29b-41d4-a716-446655440010",
        "consent_form_id": "550e8400-e29b-41d4-a716-446655440020",
        "workplace_id": "550e8400-e29b-41d4-a716-446655440030"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "created_at": "2024-02-20T14:15:00Z",
        "updated_at": "2024-02-20T14:15:00Z",
        "name": "Jane Smith",
        "phone": "+1987654321",
        "email": "jane.smith@email.com",
        "customer_id": "550e8400-e29b-41d4-a716-446655440011",
        "consent_form_id": "550e8400-e29b-41d4-a716-446655440021",
        "workplace_id": "550e8400-e29b-41d4-a716-446655440031"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440003",
        "created_at": "2024-03-10T09:45:00Z",
        "updated_at": "2024-03-10T09:45:00Z",
        "name": "Bob Johnson",
        "phone": "+1122334455",
        "email": "bob.johnson@email.com",
        "customer_id": "550e8400-e29b-41d4-a716-446655440012",
        "consent_form_id": None,
        "workplace_id": "550e8400-e29b-41d4-a716-446655440032"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440004",
        "created_at": "2024-04-05T16:20:00Z",
        "updated_at": "2024-04-05T16:20:00Z",
        "name": "Alice Wilson",
        "phone": "+1555666777",
        "email": None,
        "customer_id": "550e8400-e29b-41d4-a716-446655440013",
        "consent_form_id": "550e8400-e29b-41d4-a716-446655440023",
        "workplace_id": "550e8400-e29b-41d4-a716-446655440033"
    }
]

class DatabaseService:
    def __init__(self):
        self.patients = MOCK_PATIENTS_DB
        print(f" Mock Database API initialized with {len(self.patients)} patients")
    
    def check_user_exists(self, email: str, phone: Optional[str] = None) -> tuple[bool, Optional[Dict]]:
        """Check if user exists and return user data"""
        print(f" Database check: email='{email}', phone='{phone}'")
        
        try:
            for i, patient in enumerate(self.patients):
                print(f"   Checking patient {i+1}: {patient.get('name')} - {patient.get('email')}")
                
                email_match = patient.get("email") and patient["email"].lower() == email.lower()
                print(f"   Email match: {email_match}")
                
                if phone:
                    phone_match = patient.get("phone") == phone
                    print(f"   Phone match: {phone_match}")
                    if email_match and phone_match:
                        print(f" MATCH FOUND: {patient['name']}")
                        return True, patient
                else:
                    if email_match:
                        print(f" MATCH FOUND: {patient['name']}")
                        return True, patient
            
            print(f" NO MATCH FOUND")
            return False, None
            
        except Exception as e:
            print(f" Database error: {str(e)}")
            return False, None

    def register_new_user(self, name: str, email: str, phone: str, 
                         customer_id: Optional[str] = None,
                         consent_form_id: Optional[str] = None,
                         workplace_id: Optional[str] = None) -> tuple[bool, Optional[Dict]]:
        """Register a new user"""
        print(f"🆕 Registering new user: {name} ({email})")
        
        try:
            new_user = {
                "id": str(uuid.uuid4()),
                "created_at": datetime.now().isoformat() + "Z",
                "updated_at": datetime.now().isoformat() + "Z", 
                "name": name,
                "phone": phone,
                "email": email,
                "customer_id": customer_id,
                "consent_form_id": consent_form_id,
                "workplace_id": workplace_id
            }
            
            # Add to mock database
            self.patients.append(new_user)
            print(f"✅ User registered successfully: {new_user['id']}")
            return True, new_user
            
        except Exception as e:
            print(f"❌ Registration failed: {str(e)}")
            return False, None

# Initialize database service
db_service = DatabaseService()

# API Endpoints
@app.get("/", tags=["HealthAgent"])
async def health_check():
    return {
        "status": "healthy",
        "service": "Mock Patient Database API",
        "timestamp": datetime.now().isoformat(),
        "total_patients": len(MOCK_PATIENTS_DB),
        "patients": [p["name"] for p in MOCK_PATIENTS_DB]
    }

@app.post("/check-user", response_model=UserCheckResponse, tags=["User Verification"])
async def check_user_endpoint(request: UserCheckRequest):
    print(f" API call received: {request}")
    
    try:
        user_exists, patient_data = db_service.check_user_exists(
            email=request.email,
            phone=request.phone
        )
        
        if user_exists and patient_data:
            message = f"User found: {patient_data['name']} ({request.email})"
            print(f" Returning: user_exists=True, patient={patient_data['name']}")
            return UserCheckResponse(
                user_exists=True,
                patient_id=patient_data["id"],
                patient_name=patient_data["name"],
                message=message
            )
        else:
            message = f"No user found with email: {request.email}"
            if request.phone:
                message += f" and phone: {request.phone}"
            
            print(f" Returning: user_exists=False")
            return UserCheckResponse(
                user_exists=False,
                patient_id=None,
                patient_name=None,
                message=message
            )
    
    except Exception as e:
        print(f" API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/register-user", response_model=UserRegistrationResponse, tags=["User Registration"])
async def register_user_endpoint(request: UserRegistrationRequest):
    """Register a new user"""
    print(f"🆕 Registration request: {request}")
    
    try:
        # Check if user already exists
        exists, _ = db_service.check_user_exists(request.email, request.phone)
        if exists:
            return UserRegistrationResponse(
                success=False,
                message=f"User already exists: {request.email}"
            )
        
        # Register new user
        success, user_data = db_service.register_new_user(
            name=request.name,
            email=request.email, 
            phone=request.phone,
            customer_id=request.customer_id,
            consent_form_id=request.consent_form_id,
            workplace_id=request.workplace_id
        )
        
        if success:
            return UserRegistrationResponse(
                success=True,
                user_id=user_data["id"],
                message=f"User registered successfully: {request.name}",
                user_data=user_data
            )
        else:
            return UserRegistrationResponse(
                success=False,
                message="Registration failed"
            )
            
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Registration error: {str(e)}")

@app.get("/patients", tags=["Database"])
async def get_all_patients():
    """Get all patients (for testing)"""
    return {
        "total_patients": len(MOCK_PATIENTS_DB),
        "patients": MOCK_PATIENTS_DB
    }

# Main execution
if __name__ == "__main__":
    import uvicorn
    print(" Starting Mock Database API...")
    print(" Database contains:")
    for patient in MOCK_PATIENTS_DB:
        print(f"   - {patient['name']}: {patient.get('email', 'No email')}")
    print("\n API will be available at: http://localhost:8080")
    print(" Documentation: http://localhost:8080/docs")
    
    uvicorn.run(
        "mock_database:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )