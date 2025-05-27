import requests
from typing import Optional
import os

DATABASE_API_URL = os.getenv("DATABASE_API_URL", "http://localhost:8080")

def check_user_in_database(email: str, phone: Optional[str] = None) -> bool:
 
    print(f"TOOL CALLED: check_user_in_database(email='{email}', phone='{phone}')")
    print(f" Making API call to: {DATABASE_API_URL}/check-user")
    
    try:
        # Prepare request payload
        payload = {
            "email": email,
            "phone": phone
        }
        
        # Make API call to mock database
        response = requests.post(
            f"{DATABASE_API_URL}/check-user",
            json=payload,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📊 API Response Status: {response.status_code}")
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        user_exists = result.get("user_exists", False)
        patient_name = result.get("patient_name")
        message = result.get("message", "")
        
        print(f"API Response: {message}")
        
        if user_exists:
            print(f"User found via API: {patient_name} ({email})")
        else:
            print(f" User not found via API: {email}")
        
        return user_exists
        
    except requests.exceptions.ConnectionError as e:
        print(f"Database API connection error: {str(e)}")
        print(f"Make sure database API is running on: {DATABASE_API_URL}")
        print("   Start it with: python db.py")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"API request error: {str(e)}")
        return False
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False