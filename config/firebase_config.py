# firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
import os
from dotenv import load_dotenv

load_dotenv()

# IMPORTANT: Path to your Firebase service account key file
#SERVICE_ACCOUNT_KEY_PATH = os.getenv("SERVICE_ACCOUNT_KEY_PATH", r"D:\Axios - Breachpoint\CTF Website\Backend_BreachPoint\dyla-diva-style-quiz-app-firebase-adminsdk-fbsvc-24c35336a3.json")

#SERVICE_ACCOUNT_KEY_PATH = os.getenv("SERVICE_ACCOUNT_KEY_PATH_LOCAL")

SERVICE_ACCOUNT_KEY_PATH = os.getenv("SERVICE_ACCOUNT_KEY_PATH")

try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(cred, {
        'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET")
    })  
    print("✅ Firebase initialized successfully.")
except Exception as e:
    print(f"🔥 Firebase initialization failed: {e}")
    # Exit or handle the error appropriately if Firebase is critical
    # For this example, we'll let other modules import db/auth but they will fail on use
    
db = firestore.client()
bucket = storage.bucket()