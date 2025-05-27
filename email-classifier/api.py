# api.py
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/classify', methods=['POST'])
def classify_email():
    try:
        # Get request data
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Log the request (remove in production)
        logger.info(f"Received request: {data}")
        
        # Extract email components with validation
        email_content = data.get('content', '')
        subject = data.get('subject', '')
        sender = data.get('sender', '')
        
        if not email_content:
            return jsonify({"error": "Email content is required"}), 400
        
        # Import the agent only when needed to avoid startup errors
        try:
            from spam_classifier.agent import classify_spam
            
            # Call the classification function
            result = classify_spam(email_content, subject, sender)
            
            # Process the result text
            if hasattr(result, 'text'):
                result_text = result.text
            elif hasattr(result, 'parts') and len(result.parts) > 0:
                result_text = result.parts[0].text
            else:
                result_text = str(result)
            
            # Determine if it's spam
            is_spam = "SPAM" in result_text.upper() and "NOT SPAM" not in result_text.upper()
            
            # Return the API response
            response = {
                "is_spam": is_spam,
                "explanation": result_text
            }
            
            logger.info(f"Classification result: {is_spam}")
            return jsonify(response)
            
        except ImportError as e:
            logger.error(f"Import error: {str(e)}")
            return jsonify({"error": "Agent module not found"}), 500
        except Exception as e:
            logger.error(f"Agent error: {str(e)}")
            return jsonify({"error": str(e)}), 500
            
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return jsonify({"error": "Server error", "details": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """Homepage to verify API is running"""
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'Not configured')
    return jsonify({
        "status": "Online",
        "project": project_id,
        "endpoints": {
            "/api/classify": "POST - Classify emails as spam or not"
        }
    })

if __name__ == '__main__':
    # Set debug=False for production
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5001)), debug=True)