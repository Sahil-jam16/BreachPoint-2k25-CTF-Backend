import os
import hashlib
import json
from fastapi import APIRouter, Depends, HTTPException, status, Header, UploadFile, File, Form
from typing import Optional, List
import re


from config.firebase_config import db
from schemas import ZoneCreate, ChallengeCreate

# --- Admin Security ---
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")

async def verify_admin_key(x_admin_api_key: str = Header(...)):
    """Dependency to verify the admin API key."""
    if x_admin_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Admin API Key")

# --- Admin Router ---
router = APIRouter(
    prefix="/admin", 
    tags=["Admin"], 
    dependencies=[Depends(verify_admin_key)]
)

# 2. Add the URL conversion helper function
def convert_to_gdrive_download_link(url: str) -> str:
    """
    Converts a standard Google Drive file view link to a direct download link.
    Returns the original URL if the format is not recognized.
    """
    # Use regex to find the file ID in a URL like:
    # https://drive.google.com/file/d/FILE_ID/view?usp=sharing
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return url # Return original url if no match is found

@router.post("/zones", status_code=status.HTTP_201_CREATED)
async def create_zone(zone_data: ZoneCreate):
    """
    Creates a new challenge zone, lets Firestore auto-generate the ID,
    and returns the new ID in the response.
    """
    zones_ref = db.collection('zones_bp')
    
    existing_zone = zones_ref.where('name', '==', zone_data.name).limit(1).stream()
    if len(list(existing_zone)) > 0:
        raise HTTPException(status_code=400, detail=f"Zone with name '{zone_data.name}' already exists.")
    
    update_time, new_zone_ref = zones_ref.add(zone_data.dict())

    return {
        "status": "success", 
        "message": f"Zone '{zone_data.name}' created successfully.",
        "zoneId": new_zone_ref.id
    }


@router.post("/challenges", status_code=status.HTTP_201_CREATED)
async def create_challenge(challenge_data: ChallengeCreate):
    """
    Creates a new challenge and auto-converts any Google Drive links to direct downloads.
    """
    zone_ref = db.collection('zones_bp').document(challenge_data.zoneId)
    if not zone_ref.get().exists:
        raise HTTPException(status_code=400, detail=f"Zone with ID '{challenge_data.zoneId}' does not exist.")

    # 3. ADD THIS BLOCK: Loop through source files and convert their links
    if challenge_data.sourceFiles:
        for file_info in challenge_data.sourceFiles:
            file_info.filePath = convert_to_gdrive_download_link(file_info.filePath)

    flag_hash = hashlib.sha256(challenge_data.flag.encode()).hexdigest()
    
    challenge_doc_data = challenge_data.dict()
    challenge_doc_data['flagHash'] = flag_hash
    
    db.collection('challenges_bp').add(challenge_doc_data)
    
    return {"status": "success", "message": f"Challenge '{challenge_data.title}' created successfully."}

@router.get("/zones", response_model=List[dict])
async def list_zones():
    """
    Lists all challenge zones.
    """
    zones_ref = db.collection('zones_bp')
    zones = [doc.to_dict() | {"id": doc.id} for doc in zones_ref.stream()]
    return zones

@router.get("/challenges", status_code=status.HTTP_200_OK)
async def list_all_challenges():
    """
    Admin endpoint to fetch a complete list of all challenges with full details.
    """
    challenges_list = []
    challenges_ref = db.collection('challenges_bp').stream()
    
    for challenge in challenges_ref:
        challenge_data = challenge.to_dict()
        challenge_data['id'] = challenge.id
        # Note: We DO NOT remove the flagHash for the admin view
        challenges_list.append(challenge_data)
        
    return challenges_list