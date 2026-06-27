"""
Root entry point for uvicorn.

Run from the project root:
    uvicorn main:app --reload
"""

import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Firebase Admin SDK using local credentials file
cred_path = os.path.join(os.path.dirname(__file__), "firebase_credentials.json")
if os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
else:
    try:
        firebase_admin.initialize_app()
    except Exception as e:
        print(f"Warning: Could not initialize Firebase Admin: {e}")

from app.main import app

__all__ = ["app"]
