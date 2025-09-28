from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth
from config.firebase_config import db
import os
from datetime import datetime, timedelta
#import load_dotenv
from jose import jwt, JWTError
from typing import Optional


SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/teams/login")

# --- Token Functions ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- Dependency to get current team ---
async def get_current_team(token: str = Depends(oauth2_scheme)):
    """
    Decodes the JWT token to get the team ID and fetches team data.
    This protects all endpoints that need an authenticated team.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        team_id: str = payload.get("sub")
        if team_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    team_doc = db.collection('teams_bp').document(team_id).get()
    if not team_doc.exists:
        raise credentials_exception
    
    team_data = team_doc.to_dict()
    team_data['id'] = team_doc.id # Add the document ID to the data
    return team_data