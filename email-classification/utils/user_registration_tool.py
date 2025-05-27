import requests
from typing import Optional, Dict
import os

DATABASE_API_URL = os.getenv("DATABASE_API_URL", "http://localhost:8080")

def register_new_user(name: str, email: str, phone: str) -> Dict:
    """Register a new user in the database"""
    
    print(f"TOOL CALLED: register_new_user(name='{name}', email='{email}', phone='{phone}')")
    print(f"Making API call to: {DATABASE_API_URL}/register-user")
    
    try:
        # Prepare request payload
        payload = {
            "name": name,
            "email": email,
            "phone": phone
        }
        
        # Make API call to registration endpoint
        response = requests.post(
            f"{DATABASE_API_URL}/register-user",
            json=payload,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📊 API Response Status: {response.status_code}")
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        success = result.get("success", False)
        user_id = result.get("user_id")
        message = result.get("message", "")
        
        print(f"Registration API Response: {message}")
        
        if success:
            print(f"User registered successfully: {name} (ID: {user_id})")
            return {
                "registration_success": True,
                "user_id": user_id,
                "message": message,
                "user_status": "newly_registered"
            }
        else:
            print(f"Registration failed: {message}")
            return {
                "registration_success": False,
                "user_id": None,
                "message": message,
                "user_status": "registration_failed"
            }
            
    except requests.exceptions.ConnectionError as e:
        print(f" Database API connection error: {str(e)}")
        print(f"Make sure database API is running on: {DATABASE_API_URL}")
        return {
            "registration_success": False,
            "user_id": None,
            "message": "Database API connection failed",
            "user_status": "connection_error"
        }
        
    except requests.exceptions.RequestException as e:
        print(f" API request error: {str(e)}")
        return {
            "registration_success": False,
            "user_id": None,
            "message": f"API request failed: {str(e)}",
            "user_status": "api_error"
        }
        
    except Exception as e:
        print(f" Unexpected error: {str(e)}")
        return {
            "registration_success": False,
            "user_id": None,
            "message": f"Unexpected error: {str(e)}",
            "user_status": "unknown_error"
        }