import requests
import os

# Configuration - put these in your environment variables
HASURA_ENDPOINT = os.getenv("HASURA_ENDPOINT", "your-hasura-endpoint")
HASURA_ADMIN_SECRET = os.getenv("HASURA_ADMIN_SECRET", "your-admin-secret")

def check_user_in_database(email: str, phone: str = None) -> dict:
 
    if phone:
        query = """
        query CheckUser($email: String!, $phone: String!) {
            patients(where: {
                email: { _eq: $email },
                phone: { _eq: $phone }
            }) {
                id
                created_at
            }
        }
        """
        variables = {"email": email, "phone": phone}
    else:
        query = """
        query CheckUser($email: String!) {
            patients(where: {
                email: { _eq: $email }
            }) {
                id
                created_at
            }
        }
        """
        variables = {"email": email}

    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": HASURA_ADMIN_SECRET,
    }

    try:
        response = requests.post(
            HASURA_ENDPOINT,
            json={"query": query, "variables": variables},
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
        result = response.json()

        patients = result.get("data", {}).get("patients", [])
        if not patients:
            return {
                "user_exists": False,
                "user_status": "new",
                "registration_date": None,
                "previous_interactions": 0
            }

        patient = patients[0]
        return {
            "user_exists": True,
            "user_status": "existing",
            "registration_date": patient["created_at"],
            "previous_interactions": 5  # Placeholder until integrated
        }

    except Exception as e:

        return {
            "user_exists": False,
            "user_status": "error",
            "error": str(e),
            "registration_date": None,
            "previous_interactions": 0
        }