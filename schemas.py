# schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List

# --- Request Models ---
class TeamAuth(BaseModel):
    teamName: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class TeamCreate(BaseModel):
    teamName: str = Field(..., min_length=3, max_length=50)

class TeamJoin(BaseModel):
    teamId: str

class FlagSubmit(BaseModel):
    challengeId: str
    flag: str

class HintRequest(BaseModel):
    challengeId: str
    hintIndex: int


# --- Admin Models ---
class ZoneCreate(BaseModel):
    #id: str = Field(..., description="The unique ID for the zone, e.g., 'boot-sector'")
    name: str
    description: str
    order: int = Field(..., description="The display order for the zone, e.g., 1, 2, 3")

class SourceFile(BaseModel):
    fileName: str
    filePath: str
    
class ChallengeCreate(BaseModel):
    title: str
    description: str
    zoneId: str
    difficulty: str
    points: int
    flag: str
    hints: List[str]
    sourceFiles: Optional[List[SourceFile]] = None


# --- Response Models ---

class UserData(BaseModel):
    uid: str
    email: Optional[str] = None
    teamId: Optional[str] = None
    
class Team(BaseModel):
    teamName: str
    score: int

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"