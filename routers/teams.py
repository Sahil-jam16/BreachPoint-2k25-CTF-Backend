from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from firebase_admin.firestore import firestore

from auth import create_access_token, get_current_team
from config.firebase_config import db
from schemas import TeamAuth, Token

router = APIRouter(prefix="/teams", tags=["Teams"])

# Setup for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

def verify_password(plain_password, hashed_password):
    # Truncate password to 72 bytes to comply with bcrypt limitation
    truncated_password = plain_password[:72]
    return pwd_context.verify(truncated_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

def get_password_hash(password):
    # Truncate password to 72 bytes before hashing to ensure consistency
    truncated_password = password[:72]
    return pwd_context.hash(truncated_password)

@router.get("/me", status_code=status.HTTP_200_OK)
async def read_team_me(current_team: dict = Depends(get_current_team)):
    """
    Get the data for the currently authenticated team.
    """
    return current_team

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_team(team_data: TeamAuth):
    """
    Registers a new team with a hashed password.
    """
    teams_ref = db.collection('teams_bp')
    existing_team = teams_ref.where('teamName', '==', team_data.teamName).limit(1).stream()
    if len(list(existing_team)) > 0:
        raise HTTPException(status_code=400, detail="Team name already exists.")

    hashed_password = get_password_hash(team_data.password)

    new_team_data = {
        "teamName": team_data.teamName,
        "passwordHash": hashed_password,
        "score": 0,
        "lastSubmissionTimestamp": None,
        "solvedChallenges": [],
        "badges": []
    }
    
    # Add the new team to the database
    teams_ref.add(new_team_data)
    
    return {"status": "success", "message": f"Team '{team_data.teamName}' registered successfully."}


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a team and returns a JWT access token.
    Your frontend should send 'teamName' in the 'username' field of the form data.
    """
    team_name = form_data.username
    password = form_data.password

    teams_ref = db.collection('teams_bp')
    team_query = teams_ref.where('teamName', '==', team_name).limit(1).stream()
    
    found_team = None
    team_id = None
    for team in team_query:
        found_team = team.to_dict()
        team_id = team.id
        break

    if not found_team or not verify_password(password, found_team["passwordHash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect team name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": team_id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/leaderboard", status_code=status.HTTP_200_OK)
async def get_leaderboard():
    """
    Fetches all teams and ranks them to create a leaderboard.
    - Primary sort: score (descending)
    - Secondary sort (tie-breaker): lastSubmissionTimestamp (ascending)
    """
    try:
        teams_ref = db.collection('teams_bp')
        
        # This query sorts by score, then by time for tie-breaking.
        # It requires a Firestore index (see instructions below).
        query = teams_ref.order_by(
            'score', direction=firestore.Query.DESCENDING
        ).order_by(
            'lastSubmissionTimestamp', direction=firestore.Query.ASCENDING
        )
        
        leaderboard_data = []
        for doc in query.stream():
            team_data = doc.to_dict()
            
            # IMPORTANT: Exclude sensitive data before sending to the client
            team_data.pop('passwordHash', None) 
            
            # Add the document ID, useful for keys in the frontend
            team_data['id'] = doc.id
            
            leaderboard_data.append(team_data)
            
        return leaderboard_data
        
    except Exception as e:
        # This will catch errors, including the one about a missing index.
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")